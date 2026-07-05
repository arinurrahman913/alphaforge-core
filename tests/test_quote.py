from alphaforge.foundation.formatter import (
    format_money,
    format_percent,
)

from alphaforge.services.quote_service import get_quote

tickers = [
    "RKLB",
    "ASTS",
    "PLTR",
    "NVDA",
    "TSLA",
]

for ticker in tickers:

    q = get_quote(ticker)

    print("=" * 80)
    print(q.ticker)
    print("=" * 80)

    print("Price          :", format_money(q.current_price))
    print("Previous Close :", format_money(q.previous_close))
    print("Change         :", format_money(q.change))
    print("Change %       :", format_percent(q.change_percent))
    print("Market         :", q.market_state)

    print()