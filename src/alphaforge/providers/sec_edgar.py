"""
SEC EDGAR provider — fetches and parses Form 13F-HR filings.

Data source: SEC EDGAR (data.sec.gov), official and free, no API key
required. SEC requires a descriptive User-Agent header identifying the
application and a contact — requests without this are commonly blocked
or rate-limited more aggressively.

Important limitations of 13F data (make sure calling code / UI reflects
these — do not present this as real-time):
- Only long U.S. equity positions are reported. No shorts, no options
  positions (calls/puts are flagged but not full derivative detail), no
  cash, no non-U.S. holdings.
- Filed up to 45 calendar days after quarter end — always historical,
  never real-time.
- Only managers with >$100M AUM are required to file.
"""

import re
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher

import requests

from alphaforge.foundation.exceptions import DataError
from alphaforge.models.institutional import FundHolding

USER_AGENT = "AlphaForge research tool contact@alphaforge.local"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
}

# Curated list of well-known funds. Expand further over time rather than
# trying to track all 5000+ 13F filers at once — each additional fund
# adds more sequential SEC requests per `analyze` run.
#
# Note on Scion Asset Management (Michael Burry): as of mid-2026 this
# fund has missed several consecutive quarterly filings, reportedly
# after closing to outside capital. Expect this entry to frequently
# return no data — that is expected behavior, not a bug.
TRACKED_FUNDS = [
    {"name": "Berkshire Hathaway", "cik": "0001067983"},
    {"name": "Renaissance Technologies", "cik": "0001037389"},
    {"name": "Bridgewater Associates", "cik": "0001350694"},
    {"name": "Third Point", "cik": "0001040273"},
    {"name": "Tiger Global Management", "cik": "0001167483"},
    {"name": "Pershing Square Capital Management", "cik": "0001336528"},
    {"name": "Scion Asset Management", "cik": "0001649339"},
    {"name": "ARK Investment Management", "cik": "0001697748"},
    {"name": "Duquesne Family Office", "cik": "0001536411"},
    {"name": "Soros Fund Management", "cik": "0001029160"},
]


def _get_recent_13f_filings(cik: str, limit: int = 2) -> list[dict]:
    """
    Return metadata for the most recent 13F-HR filings for a given CIK,
    most recent first. Each item has accessionNumber, filingDate,
    primaryDocument.
    """

    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

    response = requests.get(url, headers=HEADERS, timeout=15)

    if response.status_code != 200:
        raise DataError(
            f"Failed to fetch SEC submissions for CIK {cik} "
            f"(status {response.status_code})."
        )

    data = response.json()

    recent = data.get("filings", {}).get("recent", {})

    forms = recent.get("form", [])
    accession_numbers = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    primary_docs = recent.get("primaryDocument", [])

    results = []

    for i, form in enumerate(forms):

        if form != "13F-HR":
            continue

        results.append(
            {
                "accessionNumber": accession_numbers[i],
                "filingDate": filing_dates[i],
                "primaryDocument": primary_docs[i],
            }
        )

        if len(results) >= limit:
            break

    return results


def _get_info_table_url(
    cik: str,
    accession_number: str,
    primary_document: str,
) -> str:
    """
    13F holdings live in a separate "information table" XML document
    within the filing, not the primary document. Filename conventions
    for this file are NOT standardized across filers (e.g. some use
    "*infotable.xml", others just a generic name), so instead of
    guessing via regex we query SEC's own index.json for the filing,
    which lists every file in it reliably.
    """

    accession_no_dashes = accession_number.replace("-", "")
    cik_int = str(int(cik))

    index_json_url = (
        f"https://www.sec.gov/Archives/edgar/data/"
        f"{cik_int}/{accession_no_dashes}/index.json"
    )

    response = requests.get(index_json_url, headers=HEADERS, timeout=15)

    if response.status_code != 200:
        raise DataError(
            f"Failed to fetch filing index.json for accession "
            f"{accession_number}."
        )

    items = response.json().get("directory", {}).get("item", [])

    xml_files = [
        item["name"] for item in items
        if item["name"].lower().endswith(".xml")
        and item["name"] != primary_document
    ]

    if not xml_files:
        raise DataError(
            f"Could not locate information table XML for accession "
            f"{accession_number}."
        )

    # Prefer a file whose name hints at holdings data; otherwise take
    # the first (and usually only) remaining XML file.
    info_table_file = next(
        (f for f in xml_files if "info" in f.lower() or "table" in f.lower()),
        xml_files[0],
    )

    return (
        f"https://www.sec.gov/Archives/edgar/data/"
        f"{cik_int}/{accession_no_dashes}/{info_table_file}"
    )


def _parse_info_table(xml_content: bytes) -> list[FundHolding]:
    """
    Parse a 13F information table XML into a list of FundHolding.
    """

    holdings = []

    root = ET.fromstring(xml_content)

    # The information table XML uses a namespace that varies slightly
    # between filers/years, so we match tags by local name instead of
    # requiring an exact namespace URI.
    for entry in root.iter():

        tag = entry.tag.split("}")[-1]

        if tag != "infoTable":
            continue

        def _find_text(parent, local_name, default=""):
            for child in parent.iter():
                if child.tag.split("}")[-1] == local_name:
                    return (child.text or default).strip()
            return default

        issuer_name = _find_text(entry, "nameOfIssuer")
        cusip = _find_text(entry, "cusip")

        shares_text = _find_text(entry, "sshPrnamt", "0")
        value_text = _find_text(entry, "value", "0")

        put_call = _find_text(entry, "putCall", "") or None

        try:
            shares = int(float(shares_text))
        except ValueError:
            shares = 0

        try:
            # SEC EDGAR Release 22.4.1 (effective January 3, 2023) changed
            # the reporting unit for this field from thousands of dollars
            # to whole dollars. Since we only ever fetch recent filings
            # (current + previous quarter), every filing we parse uses the
            # post-2023 whole-dollar format — no conversion needed. Do
            # NOT multiply by 1000 here; that was correct for pre-2023
            # filings only and previously caused values to be inflated
            # ~1000x (e.g. reporting $818B for a position actually worth
            # ~$818M).
            value_usd = float(value_text)
        except ValueError:
            value_usd = 0.0

        holdings.append(
            FundHolding(
                issuer_name=issuer_name,
                cusip=cusip,
                shares=shares,
                value_usd=value_usd,
                put_call=put_call,
            )
        )

    return holdings


def get_fund_holdings(cik: str, quarters_back: int = 2) -> list[list[FundHolding]]:
    """
    Return holdings for the most recent N 13F-HR filings of a fund,
    most recent first. Each element is the full holdings list for one
    quarter's filing.
    """

    filings = _get_recent_13f_filings(cik, limit=quarters_back)

    if not filings:
        raise DataError(f"No 13F-HR filings found for CIK {cik}.")

    all_quarters = []

    for filing in filings:

        info_table_url = _get_info_table_url(
            cik, filing["accessionNumber"], filing["primaryDocument"]
        )

        response = requests.get(info_table_url, headers=HEADERS, timeout=20)

        if response.status_code != 200:
            raise DataError(
                f"Failed to fetch information table at {info_table_url}."
            )

        holdings = _parse_info_table(response.content)

        all_quarters.append(holdings)

    return all_quarters


def find_holding_by_company_name(
    holdings: list[FundHolding],
    company_name: str,
    threshold: float = 0.90,
) -> FundHolding | None:
    """
    Find a holding matching the given company name.

    IMPORTANT: this is a heuristic name match, not an exact identifier
    lookup (13F filings use CUSIP, which we don't map to ticker). A
    loose match here silently attaches one company's share count/value
    to a completely different company — e.g. "BlackBerry Limited" was
    previously matched to an unrelated issuer, reporting a position
    worth $38B against a company with a $6.5B market cap. To avoid this:

    - The threshold is intentionally high (0.90 default). A lower
      threshold trades false negatives (missing a real match due to
      naming differences) for false positives (attaching the wrong
      company's data) — false positives are worse here because they
      look like valid data instead of failing visibly.
    - Exact match after normalization always wins immediately.
    - Fuzzy match additionally requires that one normalized name is
      fully contained in the other, not just "textually similar" —
      pure similarity ratios can score unrelated short names highly
      by coincidence.
    """

    normalized_target = _normalize_name(company_name)

    if len(normalized_target) < 3:
        return None

    for holding in holdings:
        if _normalize_name(holding.issuer_name) == normalized_target:
            return holding

    best_match = None
    best_score = 0.0

    for holding in holdings:

        normalized_issuer = _normalize_name(holding.issuer_name)

        if not normalized_issuer:
            continue

        contains = (
            normalized_target in normalized_issuer
            or normalized_issuer in normalized_target
        )

        if not contains:
            continue

        score = SequenceMatcher(
            None, normalized_target, normalized_issuer
        ).ratio()

        if score > best_score:
            best_score = score
            best_match = holding

    if best_score >= threshold:
        return best_match

    return None


def _normalize_name(name: str) -> str:
    """
    Strip common corporate suffixes and punctuation so "NVIDIA Corp"
    and "NVIDIA CORPORATION" compare as equal. Suffixes are removed on
    whole-word boundaries only, so a suffix token never accidentally
    eats part of the real company name (e.g. "COINCO" must not lose
    "CO").
    """

    name = name.upper()
    name = re.sub(r"[.,]", "", name)

    suffix_pattern = re.compile(
        r"\b(CORPORATION|CORP|INCORPORATED|INC|COMPANY|CO|"
        r"LIMITED|LTD|LLC|PLC|HOLDINGS?|GROUP)\b"
    )

    name = suffix_pattern.sub("", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()
