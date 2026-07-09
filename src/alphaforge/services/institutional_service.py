from alphaforge.models.institutional import (
    FundPosition,
    InstitutionalOwnership,
)

from alphaforge.providers.sec_edgar import (
    TRACKED_FUNDS,
    find_holding_by_company_name,
    get_fund_holdings,
)


def get_institutional_ownership(
    ticker: str,
    company_name: str,
) -> InstitutionalOwnership:
    """
    Check each tracked fund's two most recent 13F filings for a position
    matching the given company, and classify how that position changed
    quarter-over-quarter.

    Note: this only queries the small curated TRACKED_FUNDS list, not
    all 5000+ 13F filers. A fund not appearing in the results does not
    necessarily mean no institution holds the stock — it means none of
    the *tracked* funds do.

    This fetches every fund's holdings on demand, which is fine for a
    single ticker (the `analyze` command). Do NOT call this in a loop
    over many tickers — each call repeats ~20 SEC EDGAR requests. For
    scanning a watchlist, fetch once with `fetch_all_fund_quarters()`
    and call `match_ownership_from_cache()` per ticker instead (see
    `scan_service.py`).
    """

    ownership = InstitutionalOwnership(
        ticker=ticker.upper(),
        company_name=company_name,
    )

    for fund in TRACKED_FUNDS:

        quarters = _fetch_fund_quarters(fund)

        if quarters is None:
            continue

        position = _match_fund_position(fund, quarters, company_name)

        if position is not None:
            ownership.positions.append(position)

    return ownership


def fetch_all_fund_quarters() -> dict:
    """
    Fetch the last two quarterly 13F filings for every tracked fund,
    ONCE — keyed by fund CIK. Intended to be called a single time
    before scanning a whole watchlist, then reused via
    `match_ownership_from_cache()` for every ticker in it. This is what
    keeps a scan of 50-100 tickers from repeating ~20 SEC EDGAR requests
    per ticker.
    """

    cache = {}

    for fund in TRACKED_FUNDS:
        cache[fund["cik"]] = _fetch_fund_quarters(fund)

    return cache


def match_ownership_from_cache(
    ticker: str,
    company_name: str,
    fund_quarters_cache: dict,
) -> InstitutionalOwnership:
    """
    Same matching logic as `get_institutional_ownership`, but against
    already-fetched fund holdings (from `fetch_all_fund_quarters()`)
    instead of making network calls on every invocation.
    """

    ownership = InstitutionalOwnership(
        ticker=ticker.upper(),
        company_name=company_name,
    )

    for fund in TRACKED_FUNDS:

        quarters = fund_quarters_cache.get(fund["cik"])

        if quarters is None:
            continue

        position = _match_fund_position(fund, quarters, company_name)

        if position is not None:
            ownership.positions.append(position)

    return ownership


def _fetch_fund_quarters(fund: dict):

    try:
        return get_fund_holdings(fund["cik"], quarters_back=2)
    except Exception as e:
        print(f"Failed to fetch holdings for {fund['name']}: {e}")
        return None


def _match_fund_position(
    fund: dict,
    quarters: list,
    company_name: str,
) -> FundPosition | None:
    """
    Determine a single fund's position (and change) for the given
    company from already-fetched quarterly holdings. Returns None if
    neither quarter shows a holding for this company at this fund.
    """

    current_holdings = quarters[0] if len(quarters) > 0 else []
    previous_holdings = quarters[1] if len(quarters) > 1 else []

    current = find_holding_by_company_name(current_holdings, company_name)
    previous = find_holding_by_company_name(previous_holdings, company_name)

    if current is None and previous is None:
        return None

    change_type, change_percent = _classify_change(current, previous)

    return FundPosition(
        fund_name=fund["name"],
        fund_cik=fund["cik"],
        current_holding=current,
        previous_holding=previous,
        change_type=change_type,
        change_percent=change_percent,
    )


def _classify_change(current, previous):

    if current is not None and previous is None:
        return "NEW_POSITION", None

    if current is None and previous is not None:
        return "SOLD_OUT", -100.0

    if current is not None and previous is not None:

        if previous.shares == 0:
            return "NEW_POSITION", None

        change_percent = (
            (current.shares - previous.shares) / previous.shares
        ) * 100

        if abs(change_percent) < 1:
            return "UNCHANGED", change_percent
        elif change_percent > 0:
            return "INCREASED", change_percent
        else:
            return "DECREASED", change_percent

    return "UNKNOWN", None
