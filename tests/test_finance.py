from alphaforge.services.financial_service import get_financial
from alphaforge.foundation.formatter import (
    format_money,
    format_percent,
    format_number,
)

tickers = [
    "RKLB",
    "ASTS",
    "BBCA",
]

for ticker in tickers:

    print("=" * 80)
    print(ticker)
    print("=" * 80)

    try:

        f = get_financial(ticker)

        print("Market Cap       :", format_money(f.market_cap))
        print("Revenue          :", format_money(f.revenue))
        print("Net Income       :", format_money(f.net_income))

        print("EPS              :", format_number(f.eps))

        print("PE               :", format_number(f.pe))
        print("Forward PE       :", format_number(f.forward_pe))

        print("ROE              :", format_percent(f.roe))
        print("Gross Margin     :", format_percent(f.gross_margin))
        print("Operating Margin :", format_percent(f.operating_margin))

        print("Cash             :", format_money(f.cash))
        print("Debt             :", format_money(f.debt))
        print("Free Cash Flow   :", format_money(f.free_cash_flow))

    except Exception as e:
        print("FAILED:", e)