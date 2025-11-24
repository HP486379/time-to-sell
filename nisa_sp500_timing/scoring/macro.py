from __future__ import annotations

from typing import Dict, List


def _percentile(values: List[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    sorted_values = sorted(values)
    current = values[-1]
    less_or_equal = sum(1 for v in sorted_values if v <= current)
    return less_or_equal / len(sorted_values)


def calculate_macro_score(
    r_values: List[float],
    cpi_values: List[float],
    vix_values: List[float],
) -> tuple[float, Dict[str, float]]:
    """
    各リストの最後を『現在値』とみなし、過去全体とのパーセンタイルを計算する。
    戻り値:
        M: マクロスコア 0〜100
        details: {
          "p_r": p_r,
          "p_cpi": p_cpi,
          "p_vix": p_vix,
        }
    """
    p_r = _percentile(r_values)
    p_cpi = _percentile(cpi_values)
    p_vix = _percentile(vix_values)

    macro_score = 100 * (0.4 * p_r + 0.3 * p_cpi + 0.3 * p_vix)
    return macro_score, {"p_r": p_r, "p_cpi": p_cpi, "p_vix": p_vix}
