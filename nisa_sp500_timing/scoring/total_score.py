from __future__ import annotations


def _clip(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def calculate_total_score(T: float, M: float, E_adj: float) -> float:
    """
    S_total = clip(0.7*T + 0.3*M + E_adj, 0, 100) を計算して返す。
    """
    raw_score = 0.7 * T + 0.3 * M + E_adj
    return _clip(raw_score)
