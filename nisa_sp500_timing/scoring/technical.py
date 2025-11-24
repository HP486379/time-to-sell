from __future__ import annotations

from typing import Dict, List, Tuple


def _moving_average(values: List[float], window: int) -> List[float]:
    if len(values) < window:
        raise ValueError(f"Need at least {window} values to compute moving average")
    averages: List[float] = []
    window_sum = sum(values[:window])
    averages.append(window_sum / window)
    for i in range(window, len(values)):
        window_sum += values[i] - values[i - window]
        averages.append(window_sum / window)
    return averages


def _clip(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def _calculate_trend_adjustment(ma20: List[float], ma60_value: float, ma200_value: float) -> float:
    if not ma20:
        return 0.0
    ma20_current = ma20[-1]
    if len(ma20) >= 20:
        ma20_past = ma20[-20]
    else:
        ma20_past = ma20[0]

    is_up_trend = ma20_current > ma60_value > ma200_value and ma20_past < ma20_current
    is_down_trend = ma20_current < ma60_value < ma200_value and ma20_past > ma20_current

    if is_up_trend:
        return 10.0
    if is_down_trend:
        return -10.0
    return 0.0


def _calculate_base_score(d: float) -> float:
    if d <= -20:
        return 0.0
    if -20 < d < 0:
        return 30 * (d + 20) / 20
    if 0 <= d < 10:
        return 30 + 20 * d / 10
    if 10 <= d < 25:
        return 50 + 30 * (d - 10) / 15
    return 100.0


def calculate_technical_score(
    price_history: List[Tuple[str, float]],
) -> tuple[float, Dict[str, float]]:
    """
    price_history: [(date_str, close), ...] 古い順
    戻り値:
        T: テクニカルスコア 0〜100
        details: {
          "d": 乖離率,
          "T_base": 基礎点,
          "T_trend": トレンド補正,
        }
    """
    if len(price_history) < 200:
        raise ValueError("price_history must contain at least 200 data points")

    closes = [close for _, close in price_history]
    current_price = closes[-1]

    ma20_series = _moving_average(closes, 20)
    ma60_series = _moving_average(closes, 60)
    ma200_series = _moving_average(closes, 200)

    ma200_value = ma200_series[-1]
    ma60_value = ma60_series[-1]

    d = (current_price - ma200_value) / ma200_value * 100
    t_base = _calculate_base_score(d)
    t_trend = _calculate_trend_adjustment(ma20_series, ma60_value, ma200_value)
    technical_score = _clip(t_base + t_trend)

    return technical_score, {"d": d, "T_base": t_base, "T_trend": t_trend}
