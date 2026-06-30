from dataclasses import dataclass


@dataclass
class Company:
    ticker: str
    name: str
    exchange: str
    sector: str
    industry: str
    current_price: float
    market_cap: float

    def summary(self):
        return (
            f"{self.ticker} | "
            f"{self.name} | "
            f"{self.current_price}"
        )