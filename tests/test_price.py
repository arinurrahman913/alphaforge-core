from alphaforge.services.price_service import get_prices

prices = get_prices("RKLB")

print("=" * 80)
print("Total Candles :", len(prices))
print("=" * 80)

print()

print("First Candle")
print(prices[0])

print()

print("Last Candle")
print(prices[-1])