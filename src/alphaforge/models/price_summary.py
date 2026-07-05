from dataclasses import dataclass


@dataclass
class PriceSummary:
    current_price: float

    highest_price: float
    lowest_price: float

    average_volume: float

    total_return: float