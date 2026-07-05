from alphaforge.models.price_summary import PriceSummary
from alphaforge.services.price_service import get_prices


def get_price_summary(
    ticker: str,
    period: str = "6mo",
) -> PriceSummary:

    prices = get_prices(ticker, period)

    first = prices[0]
    last = prices[-1]

    current_price = last.close

    highest_price = max(p.high for p in prices)
    lowest_price = min(p.low for p in prices)

    average_volume = sum(p.volume for p in prices) / len(prices)

    total_return = (
        (last.close - first.close)
        / first.close
    )

    return PriceSummary(
        current_price=current_price,
        highest_price=highest_price,
        lowest_price=lowest_price,
        average_volume=average_volume,
        total_return=total_return,
    )