from dataclasses import dataclass


@dataclass
class StockQuote:
    ticker: str

    current_price: float
    previous_close: float

    change: float
    change_percent: float

    market_state: str