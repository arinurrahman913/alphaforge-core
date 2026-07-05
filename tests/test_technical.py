from alphaforge.foundation.formatter import format_money

from alphaforge.services.technical_service import (
    get_technical_summary,
)

summary, analysis = get_technical_summary("RKLB")

print("=" * 80)
print("TECHNICAL ANALYSIS")
print("=" * 80)

print()

print("Trend")
print("-----")
print(analysis.trend)

print()

print("Confidence")
print("----------")
print(f"{analysis.confidence}%")

print()

print("Evidence")
print("--------")

for item in analysis.evidence:
    print(f"✓ {item}")

print()

print("Indicators")
print("----------")
print("SMA20 :", format_money(summary.sma20.value))
print("SMA50 :", format_money(summary.sma50.value))

print()

print("Recommendation")
print("--------------")
print(analysis.recommendation)