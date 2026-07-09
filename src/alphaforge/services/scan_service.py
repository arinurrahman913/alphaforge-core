"""
Scan service — runs the analysis pipeline across a watchlist of tickers
and ranks them by a combined (financial + technical + institutional)
signal.

Performance note: institutional (13F) data is fetched ONCE for all
tracked funds at the start of the scan, then matched against each
ticker locally in memory. Fetching institutional data per-ticker (the
approach used by the single-ticker `analyze` command) does not scale —
10 funds x ~2 requests each x N tickers would mean hundreds or
thousands of SEC requests for a 50+ ticker watchlist.
"""

from alphaforge.foundation.exceptions import DataError
from alphaforge.models.scan import ScanResult
from alphaforge.scoring.financial_engine import FinancialScoringEngine

from alphaforge.providers.sec_edgar import (
    TRACKED_FUNDS,
    find_holding_by_company_name,
    get_fund_holdings,
)

from alphaforge.services.company_service import get_company_profile
from alphaforge.services.financial_service import get_financial
from alphaforge.services.technical_service import get_technical_summary

# Heuristic scoring weights for combining signals into one ranking
# number. These are a starting point, not a validated model — treat the
# composite_score as a rough sort order, not a precise prediction.
TECHNICAL_TREND_BONUS = {
    "Strong Bullish": 15,
    "Bullish": 10,
    "Bullish Pullback": 5,
    "Neutral": 0,
    "Bearish Rebound": -5,
    "Strong Bearish": -15,
}

INSTITUTIONAL_NEW_POSITION_WEIGHT = 10
INSTITUTIONAL_INCREASED_WEIGHT = 3
INSTITUTIONAL_DECREASED_WEIGHT = -3
INSTITUTIONAL_SOLD_OUT_WEIGHT = -10

# Standard market cap bands (USD). "Small cap" here follows the common
# ~$300M–$2B definition used by most screeners; adjust if your own
# strategy uses a different cutoff.
def _categorize_market_cap(market_cap: float | None) -> str:

    if market_cap is None:
        return "-"

    if market_cap < 50_000_000:
        return "nano"
    elif market_cap < 300_000_000:
        return "micro"
    elif market_cap < 2_000_000_000:
        return "small"
    elif market_cap < 10_000_000_000:
        return "mid"
    elif market_cap < 200_000_000_000:
        return "large"
    else:
        return "mega"


def load_watchlist(path: str) -> list[str]:
    """
    Load tickers from a plain text file, one ticker per line. Blank
    lines and lines starting with # (comments) are ignored.
    """

    tickers = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:

                # Strip inline comments (everything from the first '#'
                # onward), not just full-line comments. Without this,
                # "NVDA   # AI chips" was being read as one literal
                # ticker string instead of just "NVDA".
                line = raw_line.split("#", 1)[0].strip()

                if not line:
                    continue

                tickers.append(line.upper())

    except FileNotFoundError:
        raise DataError(f"Watchlist file not found: {path}")

    if not tickers:
        raise DataError(f"Watchlist file is empty: {path}")

    return tickers


def _load_fund_cache() -> dict:
    """
    Fetch each tracked fund's two most recent 13F filings once, and
    return them keyed by fund name. Funds that fail to fetch are
    skipped (with a printed warning) rather than aborting the whole
    scan — partial institutional data is better than no scan at all.
    """

    cache = {}

    for fund in TRACKED_FUNDS:

        try:
            quarters = get_fund_holdings(fund["cik"], quarters_back=2)

            cache[fund["name"]] = {
                "current": quarters[0] if len(quarters) > 0 else [],
                "previous": quarters[1] if len(quarters) > 1 else [],
            }

        except Exception as e:
            print(f"Warning: could not load {fund['name']} holdings: {e}")

    return cache


def _classify_change(current, previous):

    if current is not None and previous is None:
        return "NEW_POSITION"

    if current is None and previous is not None:
        return "SOLD_OUT"

    if current is not None and previous is not None:

        if previous.shares == 0:
            return "NEW_POSITION"

        change_percent = (
            (current.shares - previous.shares) / previous.shares
        ) * 100

        if abs(change_percent) < 1:
            return "UNCHANGED"
        elif change_percent > 0:
            return "INCREASED"
        else:
            return "DECREASED"

    return None


def _get_institutional_signal(company_name: str, fund_cache: dict) -> dict:

    signal = {
        "new_positions": 0,
        "increased": 0,
        "decreased": 0,
        "sold_out": 0,
        "held_by": 0,
    }

    for fund_name, holdings in fund_cache.items():

        current = find_holding_by_company_name(
            holdings["current"], company_name
        )
        previous = find_holding_by_company_name(
            holdings["previous"], company_name
        )

        if current is None and previous is None:
            continue

        change = _classify_change(current, previous)

        if current is not None:
            signal["held_by"] += 1

        if change == "NEW_POSITION":
            signal["new_positions"] += 1
        elif change == "INCREASED":
            signal["increased"] += 1
        elif change == "DECREASED":
            signal["decreased"] += 1
        elif change == "SOLD_OUT":
            signal["sold_out"] += 1

    return signal


def _scan_ticker(ticker: str, fund_cache: dict) -> ScanResult:

    result = ScanResult(
        ticker=ticker,
        company_name=ticker,
        financial_grade=None,
        financial_score=None,
        financial_max=None,
        technical_trend=None,
    )

    try:
        company = get_company_profile(ticker)
        result.company_name = company.name
    except Exception as e:
        result.errors.append(f"company: {e}")
        company = None

    financial_component = 0.0

    try:
        financial = get_financial(ticker)

        if financial is not None:
            score_result = FinancialScoringEngine().score(financial)
            result.financial_grade = score_result.grade
            result.financial_score = score_result.total
            result.financial_max = score_result.maximum
            financial_component = score_result.total

            result.market_cap = financial.market_cap
            result.cap_category = _categorize_market_cap(financial.market_cap)

    except Exception as e:
        result.errors.append(f"financial: {e}")

    technical_component = 0.0

    try:
        technical_result = get_technical_summary(ticker)

        if technical_result is not None:
            _, analysis = technical_result
            result.technical_trend = analysis.trend
            technical_component = TECHNICAL_TREND_BONUS.get(
                analysis.trend, 0
            )

    except Exception as e:
        result.errors.append(f"technical: {e}")

    institutional_component = 0.0

    if company is not None:

        signal = _get_institutional_signal(company.name, fund_cache)

        result.institutional_new_positions = signal["new_positions"]
        result.institutional_increased = signal["increased"]
        result.institutional_decreased = signal["decreased"]
        result.institutional_sold_out = signal["sold_out"]
        result.institutional_held_by = signal["held_by"]

        institutional_component = (
            signal["new_positions"] * INSTITUTIONAL_NEW_POSITION_WEIGHT
            + signal["increased"] * INSTITUTIONAL_INCREASED_WEIGHT
            + signal["decreased"] * INSTITUTIONAL_DECREASED_WEIGHT
            + signal["sold_out"] * INSTITUTIONAL_SOLD_OUT_WEIGHT
        )

    result.composite_score = (
        financial_component + technical_component + institutional_component
    )

    return result


def run_scan(
    tickers: list[str],
    cap_categories: list[str] | None = None,
) -> list[ScanResult]:
    """
    Run the scan pipeline across all given tickers and return results
    sorted by composite_score, highest first.

    cap_categories: if given (e.g. ["small", "micro"]), tickers whose
    market cap falls outside these categories are excluded from the
    returned results. Tickers where market cap couldn't be determined
    are kept (category "-") rather than silently dropped, since a
    fetch failure isn't the same as "not a small cap".
    """

    print(f"Loading institutional holdings for {len(TRACKED_FUNDS)} tracked funds...")
    fund_cache = _load_fund_cache()

    results = []

    for i, ticker in enumerate(tickers, start=1):

        print(f"Scanning {ticker} ({i}/{len(tickers)})...")

        result = _scan_ticker(ticker, fund_cache)
        results.append(result)

    if cap_categories:
        results = [
            r for r in results
            if r.cap_category in cap_categories or r.cap_category == "-"
        ]

    results.sort(key=lambda r: r.composite_score, reverse=True)

    return results
