from alphaforge.models.technical import (
    MovingAverage,
    TechnicalAnalysis,
    TechnicalSummary,
)

from alphaforge.services.price_service import get_prices


def calculate_sma(prices, period):

    closes = [p.close for p in prices]

    if len(closes) < period:
        return 0

    return sum(closes[-period:]) / period


def get_technical_summary(ticker: str):

    prices = get_prices(ticker)

    current_price = prices[-1].close

    sma20 = calculate_sma(prices, 20)
    sma50 = calculate_sma(prices, 50)

    summary = TechnicalSummary(
        sma20=MovingAverage(
            period=20,
            value=sma20,
        ),
        sma50=MovingAverage(
            period=50,
            value=sma50,
        ),
    )

    evidence = []

    confidence = 50

    # Evidence 1
    if current_price > sma20:
        evidence.append(
            f"Current Price ({current_price:.2f}) above SMA20 ({sma20:.2f})"
        )
        confidence += 15
    else:
        evidence.append(
            f"Current Price ({current_price:.2f}) below SMA20 ({sma20:.2f})"
        )
        confidence -= 15

    # Evidence 2
    if sma20 > sma50:
        evidence.append(
            f"SMA20 ({sma20:.2f}) above SMA50 ({sma50:.2f})"
        )
        confidence += 15
    else:
        evidence.append(
            f"SMA20 ({sma20:.2f}) below SMA50 ({sma50:.2f})"
        )
        confidence -= 15

    # Trend
    if current_price > sma20 and sma20 > sma50:
        trend = "Strong Bullish"

    elif current_price > sma20 and sma20 <= sma50:
        trend = "Bearish Rebound"

    elif current_price <= sma20 and sma20 > sma50:
        trend = "Bullish Pullback"

    elif current_price < sma20 and sma20 < sma50:
        trend = "Strong Bearish"

    else:
        trend = "Neutral"

    confidence = max(0, min(confidence, 100))

    # Recommendation
    if trend == "Strong Bullish":
        recommendation = (
            "Trend masih kuat. "
            "Belum ada sinyal pelemahan."
        )

    elif trend == "Bullish Pullback":
        recommendation = (
            "Trend jangka menengah masih naik, tapi harga sedang koreksi. "
            "Pantau apakah SMA20 bisa jadi support."
        )

    elif trend == "Bearish Rebound":
        recommendation = (
            "Trend jangka menengah masih turun, harga sedang technical rebound. "
            "Waspadai potensi pelemahan lanjutan."
        )

    elif trend == "Strong Bearish":
        recommendation = (
            "Momentum mulai melemah. "
            "Perhatikan support terdekat."
        )

    else:
        recommendation = (
            "Momentum masih lemah. "
            "Belum ada konfirmasi pembalikan tren."
        )

    analysis = TechnicalAnalysis(
        trend=trend,
        confidence=confidence,
        evidence=evidence,
        recommendation=recommendation,
    )

    return summary, analysis
