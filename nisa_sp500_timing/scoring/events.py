from __future__ import annotations

from datetime import date
from typing import Dict, List, NamedTuple


class EconomicEvent(NamedTuple):
    name: str
    importance: int  # 1〜5
    date: date


def _importance_weight(importance: int) -> float:
    if importance == 5:
        return 1.0
    if importance == 4:
        return 0.7
    if importance == 3:
        return 0.4
    return 0.2


def _proximity_factor(event_date: date, today: date) -> float:
    days = (event_date - today).days
    if abs(days) > 7:
        return 0.0
    return 1 - abs(days) / 7.0


def calculate_event_adjustment(
    events: List[EconomicEvent],
    today: date,
) -> tuple[float, Dict]:
    """
    戻り値:
        E_adj: -10〜0
        details: {
          "R_max": float,
          "effective_event": EconomicEvent | None
        }
    """
    r_max = 0.0
    effective_event: EconomicEvent | None = None

    for event in events:
        w_imp = _importance_weight(event.importance)
        f_prox = _proximity_factor(event.date, today)
        r_i = w_imp * f_prox
        if r_i > r_max:
            r_max = r_i
            effective_event = event

    e_adj = -10 * r_max
    return e_adj, {"R_max": r_max, "effective_event": effective_event}
