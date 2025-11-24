from __future__ import annotations

import streamlit as st

from nisa_sp500_timing.domain.position import Sp500Position
from nisa_sp500_timing.domain.score_breakdown import ScoreBreakdown
from nisa_sp500_timing.scoring.events import calculate_event_adjustment
from nisa_sp500_timing.scoring.macro import calculate_macro_score
from nisa_sp500_timing.scoring.technical import calculate_technical_score
from nisa_sp500_timing.scoring.total_score import calculate_total_score
from nisa_sp500_timing.services.event_service import EventService
from nisa_sp500_timing.services.macro_data_service import MacroDataService
from nisa_sp500_timing.services.sp500_market_service import Sp500MarketService


st.set_page_config(page_title="S&P500 売り時ダッシュボード v1", layout="wide")


@st.cache_data
def load_market_data():
    market_service = Sp500MarketService()
    price_history = market_service.get_price_history()
    current_price = market_service.get_current_price()
    return price_history, current_price


@st.cache_data
def load_macro_data():
    macro_service = MacroDataService()
    return macro_service.get_macro_series()


@st.cache_data
def load_events():
    event_service = EventService()
    today = event_service.get_today()
    events = event_service.get_upcoming_events()
    return events, today


def get_label(score: float) -> str:
    if score >= 80:
        return "一部利確を強く検討"
    if score >= 60:
        return "利確を検討"
    if score >= 40:
        return "ホールド"
    return "買い増し・追加投資検討"


def calculate_scores() -> ScoreBreakdown:
    price_history, current_price = load_market_data()
    r_values, cpi_values, vix_values = load_macro_data()
    events, today = load_events()

    T, t_details = calculate_technical_score(price_history)
    M, m_details = calculate_macro_score(r_values, cpi_values, vix_values)
    E_adj, e_details = calculate_event_adjustment(events, today)
    total = calculate_total_score(T, M, E_adj)

    comments = [
        f"乖離率 d: {t_details['d']:.2f}%",
        f"パーセンタイル(金利/CPI/VIX): {m_details['p_r']:.2f}, {m_details['p_cpi']:.2f}, {m_details['p_vix']:.2f}",
    ]
    if e_details["effective_event"]:
        ev = e_details["effective_event"]
        comments.append(f"影響の強いイベント: {ev.name} ({ev.date.isoformat()})")

    return ScoreBreakdown(total, T, M, E_adj, comments)


st.title("S&P500 売り時ダッシュボード v1")
st.write("テクニカル、マクロ、イベントから売り時スコアを算出します。")

with st.sidebar:
    st.header("ポジション入力")
    quantity = st.number_input("保有数量", min_value=0.0, value=10.0, step=1.0)
    avg_cost = st.number_input("平均取得単価", min_value=0.0, value=4000.0, step=10.0)
    account_type = st.selectbox("口座区分", ["NISA", "特定", "一般"])

position = Sp500Position(quantity, avg_cost, account_type)
price_history, current_price = load_market_data()
breakdown = calculate_scores()

st.subheader("ポジション概要")
col1, col2, col3 = st.columns(3)
col1.metric("現在価格", f"{current_price:,.2f}")
col2.metric("評価額", f"{position.market_value(current_price):,.2f}")
pnl_value = position.unrealized_pnl(current_price)
pnl_label = "含み益" if pnl_value >= 0 else "含み損"
col3.metric(pnl_label, f"{pnl_value:,.2f}")

st.subheader("売り時スコア")
st.metric("総合スコア", f"{breakdown.total:.2f}", help="0〜100で高いほど売り寄り")
st.write(f"判定: **{get_label(breakdown.total)}**")

col_t, col_m, col_e = st.columns(3)
with col_t:
    st.markdown("### テクニカル T")
    st.write(f"T = {breakdown.technical:.2f}")
with col_m:
    st.markdown("### マクロ M")
    st.write(f"M = {breakdown.macro:.2f}")
with col_e:
    st.markdown("### イベント補正 E_adj")
    st.write(f"E_adj = {breakdown.event_adjustment:.2f}")

st.markdown("### コメント")
for c in breakdown.comments:
    st.write("- " + c)


if __name__ == "__main__":
    import sys
    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        __file__,
        "--server.address",
        "0.0.0.0",
        "--server.port",
        "8501",
    ]
    sys.exit(stcli.main())
