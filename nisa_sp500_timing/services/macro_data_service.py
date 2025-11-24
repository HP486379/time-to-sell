from __future__ import annotations

from typing import List, Tuple


class DummyMacroClient:
    def fetch_macro_series(self) -> Tuple[List[float], List[float], List[float]]:
        r_values = [2.0 + i * 0.01 for i in range(100)] + [3.5]
        cpi_values = [1.5 + (i % 5) * 0.1 for i in range(100)] + [2.8]
        vix_values = [15 + (i % 10) * 0.2 for i in range(100)] + [18]
        return r_values, cpi_values, vix_values


class MacroDataService:
    def __init__(self, macro_client=None):
        self.macro_client = macro_client or DummyMacroClient()

    def get_macro_series(self):
        """
        r_values, cpi_values, vix_values の3つを返す。
        いずれも List[float] で、最後が現在値。
        """
        return self.macro_client.fetch_macro_series()
