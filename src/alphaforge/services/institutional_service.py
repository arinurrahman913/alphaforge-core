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
    """

    ownership = InstitutionalOwnership(
        ticker=ticker.upper(),
        company_name=company_name,
    )

    for fund in TRACKED_FUNDS:

        position = _get_fund_position(fund, company_name)

        if position is not None:
            ownership.positions.append(position)

    return ownership


def _get_fund_position(fund: dict, company_name: str) -> FundPosition | None:
    """
    Fetch a single fund's last two quarterly filings and determine its
    position (and change) for the given company. Returns None only if
    the fund's filings themselves could not be fetched at all — a fund
    that simply doesn't hold the stock still returns a FundPosition with
    change_type reflecting that (or is skipped by the caller if neither
    quarter shows a holding).
    """

    try:
        quarters = get_fund_holdings(fund["cik"], quarters_back=2)
    except Exception as e:
        print(f"Failed to fetch holdings for {fund['name']}: {e}")
        return None

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
