from alphaforge.foundation.formatter import (
    format_money,
    format_percent,
)

from alphaforge.services.price_summary_service import (
    get_price_summary,
)

summary = get_price_summary("RKLB")

print("=" * 80)
print("PRICE SUMMARY")
print("=" * 80)

print()

print("Current Price :", format_money(summary.current_price))
print("Highest Price :", format_money(summary.highest_price))
print("Lowest Price  :", format_money(summary.lowest_price))

print()

print("Average Volume :", f"{summary.average_volume:,.0f}")

print("6M Return      :", format_percent(summary.total_return))