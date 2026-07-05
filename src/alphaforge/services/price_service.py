from alphaforge.models.price import PriceBar
from alphaforge.providers.yahoo_finance import get_price_history


def get_prices(
    ticker: str,
    period: str = "6mo",
) -> list[PriceBar]:

    return get_price_history(
        ticker=ticker,
        period=period,
    )