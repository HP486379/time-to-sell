from __future__ import annotations

from datetime import date, timedelta
from typing import List

from nisa_sp500_timing.scoring.events import EconomicEvent


class DummyEventClient:
    def fetch_events(self, days_ahead: int) -> List[EconomicEvent]:
        today = date.today()
        return [
            EconomicEvent("FOMC", 5, today + timedelta(days=3)),
            EconomicEvent("CPI", 4, today + timedelta(days=10)),
            EconomicEvent("雇用統計", 5, today - timedelta(days=1)),
        ]


class EventService:
    def __init__(self, event_client=None):
        self.event_client = event_client or DummyEventClient()

    def get_upcoming_events(self, days_ahead: int = 30) -> List[EconomicEvent]:
        return self.event_client.fetch_events(days_ahead)

    def get_today(self) -> date:
        return date.today()
