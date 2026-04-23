import streamlit as st
from config import TICKERS, PERIODS, CURRENCY_MAP
from data.fetcher import get_ticker_info, get_all_histories
from charts.price_chart import build_price_chart
from charts.volume_chart import build_volume_chart
from charts.return_chart import build_return_chart
from charts.comparison_chart import build_comparison_chart
from components.metric_card import render_metric_cards
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Dashboard de Ações",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Dashboard de Ações")
st.caption("Petrobras · Itaú Unibanco · Nvidia")
st.markdown("---")

selected_period = render_sidebar()
period_config = PERIODS[selected_period]
interval = period_config["interval"]

symbols = list(TICKERS.keys())

with st.spinner("Buscando dados de mercado..."):
    all_histories = get_all_histories(symbols, selected_period, interval)
    all_infos = {sym: get_ticker_info(sym) for sym in symbols}

ticker_tabs = st.tabs([TICKERS[sym]["label"] for sym in symbols])

for tab, symbol in zip(ticker_tabs, symbols):
    with tab:
        meta = TICKERS[symbol]
        info = all_infos[symbol]
        df = all_histories[symbol]
        currency = CURRENCY_MAP[symbol]

        render_metric_cards(info, symbol, meta["label"])

        st.markdown("####")

        chart_tab1, chart_tab2, chart_tab3 = st.tabs(["📊 Preço", "📦 Volume", "📉 Retorno %"])

        with chart_tab1:
            fig = build_price_chart(df, meta["label"], meta["color"], currency)
            st.plotly_chart(fig, use_container_width=True)

        with chart_tab2:
            fig = build_volume_chart(df, meta["label"], meta["color"])
            st.plotly_chart(fig, use_container_width=True)

        with chart_tab3:
            fig = build_return_chart(df, meta["label"], meta["color"])
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🔀 Comparação de Performance")
st.caption("Retorno normalizado (base 100) — permite comparar ações em moedas diferentes")

comparison_fig = build_comparison_chart(all_histories)
st.plotly_chart(comparison_fig, use_container_width=True)
