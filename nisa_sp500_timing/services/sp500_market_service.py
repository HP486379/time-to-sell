from __future__ import annotations

from datetime import date, timedelta
from typing import List, Tuple


class DummyPriceClient:
    def fetch_price_history(self, symbol: str, period: str) -> List[Tuple[str, float]]:
        today = date.today()
        base_price = 4000.0
        history: List[Tuple[str, float]] = []
        for i in range(300):
            day_price = base_price + (i - 150) * 2
            history.append(((today - timedelta(days=300 - i)).isoformat(), day_price))
        return history

    def fetch_current_price(self, symbol: str) -> float:
        return 4500.0


class Sp500MarketService:
    def __init__(self, price_client=None, symbol: str = "^GSPC"):
        self.price_client = price_client or DummyPriceClient()
        self.symbol = symbol

    def get_price_history(self, period: str = "5y") -> List[Tuple[str, float]]:
        return self.price_client.fetch_price_history(self.symbol, period)

    def get_current_price(self) -> float:
        return self.price_client.fetch_current_price(self.symbol)
