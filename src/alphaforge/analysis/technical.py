from alphaforge.models.analysis import TechnicalIndicators
from alphaforge.models.stock import PriceHistory


def _closes(history: PriceHistory) -> list[float]:
    return [bar.close for bar in history.bars]


def _sma(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def _rsi(values: list[float], period: int = 14) -> float | None:
    if len(values) < period + 1:
        return None

    gains: list[float] = []
    losses: list[float] = []

    for i in range(-period, 0):
        delta = values[i] - values[i - 1]
        if delta >= 0:
            gains.append(delta)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(delta))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def _ema(values: list[float], period: int) -> list[float]:
    if not values:
        return []

    multiplier = 2 / (period + 1)
    ema_values = [values[0]]

    for price in values[1:]:
        ema_values.append((price - ema_values[-1]) * multiplier + ema_values[-1])

    return ema_values


def _macd(values: list[float]) -> tuple[float | None, float | None]:
    if len(values) < 26:
        return None, None

    ema_12 = _ema(values, 12)
    ema_26 = _ema(values, 26)
    macd_line = [a - b for a, b in zip(ema_12, ema_26)]
    signal_line = _ema(macd_line, 9)

    return macd_line[-1], signal_line[-1]


def _detect_trend(price: float, sma_20: float | None, sma_50: float | None, sma_200: float | None) -> str:
    if sma_20 is None or sma_50 is None:
        return "NEUTRAL"

    if price > sma_20 > sma_50 and (sma_200 is None or sma_50 > sma_200):
        return "BULLISH"
    if price < sma_20 < sma_50 and (sma_200 is None or sma_50 < sma_200):
        return "BEARISH"
    return "NEUTRAL"


def compute_technical_indicators(history: PriceHistory) -> TechnicalIndicators:
    closes = _closes(history)
    price = closes[-1]

    sma_20 = _sma(closes, 20)
    sma_50 = _sma(closes, 50)
    sma_200 = _sma(closes, 200)
    rsi_14 = _rsi(closes)
    macd, macd_signal = _macd(closes)

    return TechnicalIndicators(
        rsi_14=rsi_14,
        sma_20=sma_20,
        sma_50=sma_50,
        sma_200=sma_200,
        macd=macd,
        macd_signal=macd_signal,
        trend=_detect_trend(price, sma_20, sma_50, sma_200),
    )
