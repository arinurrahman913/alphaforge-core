from dataclasses import dataclass


@dataclass
class FinancialSnapshot:
    ticker: str

    market_cap: float | None
    revenue: float | None
    net_income: float | None

    eps: float | None

    pe: float | None
    forward_pe: float | None

    roe: float | None

    gross_margin: float | None
    operating_margin: float | None

    cash: float | None
    debt: float | None

    free_cash_flow: float | None