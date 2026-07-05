from alphaforge.models.quote import StockQuote
from alphaforge.providers.yahoo_finance import get_stock_quote


def get_quote(ticker: str) -> StockQuote:
    return get_stock_quote(ticker)