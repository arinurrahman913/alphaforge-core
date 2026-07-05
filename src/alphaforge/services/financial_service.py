from alphaforge.models.financial import FinancialSnapshot
from alphaforge.providers.yahoo_finance import get_financial_snapshot


def get_financial(ticker: str) -> FinancialSnapshot:
    return get_financial_snapshot(ticker)