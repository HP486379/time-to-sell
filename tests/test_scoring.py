from datetime import date

import pytest

from nisa_sp500_timing.scoring.events import EconomicEvent, calculate_event_adjustment
from nisa_sp500_timing.scoring.macro import calculate_macro_score
from nisa_sp500_timing.scoring.technical import calculate_technical_score


def _build_price_history(last_price: float):
    target_ma200 = 4000.0
    low_price = 3950.0
    low_days = 59
    remaining_days = 200 - low_days - 1
    mid_price = (target_ma200 * 200 - (low_price * low_days + last_price)) / remaining_days
    if mid_price <= 0:
        raise ValueError("mid_price must stay positive for test setup")

    prices = [mid_price] * 20  # extra buffer days before the 200-day window
    # build the 200-day window
    prices.extend([mid_price] * remaining_days)
    prices.extend([low_price] * low_days)
    prices.append(last_price)

    history = []
    start = date(2023, 1, 1)
    for i, price in enumerate(prices):
        history.append(((start.toordinal() + i).__str__(), price))
    return history


@pytest.mark.parametrize(
    "last_price, expected",
    [
        (4000, 30),
        (4400, 50),
        (5000, 80),
        (3000, 0),
    ],
)
def test_technical_score_base_cases(last_price, expected):
    history = _build_price_history(last_price)
    score, details = calculate_technical_score(history)
    assert pytest.approx(expected, rel=1e-3, abs=1e-2) == score


def test_macro_score_example():
    r_values = [1, 2, 3, 4, 5, 6, 7, 9, 10, 8]
    cpi_values = [1, 2, 3, 4, 10, 11, 12, 13, 14, 5]
    vix_values = [15, 16, 17, 18, 19, 20, 21, 22, 13, 14]

    score, details = calculate_macro_score(r_values, cpi_values, vix_values)
    assert pytest.approx(53, rel=1e-3, abs=1e-2) == score
    assert pytest.approx(0.8) == details["p_r"]
    assert pytest.approx(0.5) == details["p_cpi"]
    assert pytest.approx(0.2) == details["p_vix"]


def test_event_adjustment_example():
    today = date(2024, 3, 1)
    events = [EconomicEvent("FOMC", 5, date(2024, 3, 3))]
    e_adj, details = calculate_event_adjustment(events, today)
    assert pytest.approx(-7.1428, rel=1e-3) == e_adj
    assert details["effective_event"].name == "FOMC"
