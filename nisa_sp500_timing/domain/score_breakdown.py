from __future__ import annotations

from typing import List


class ScoreBreakdown:
    def __init__(
        self,
        total: float,
        technical: float,
        macro: float,
        event_adjustment: float,
        comments: List[str] | None = None,
    ):
        self.total = total
        self.technical = technical
        self.macro = macro
        self.event_adjustment = event_adjustment
        self.comments = comments or []
