from dataclasses import dataclass


@dataclass
class Company:
    ticker: str
    name: str
    sector: str
    industry: str
    country: str