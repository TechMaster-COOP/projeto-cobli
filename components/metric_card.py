import streamlit as st
from utils.formatters import format_currency, format_large_number, format_percentage


def render_metric_cards(info: dict, symbol: str, label: str):
    currency = info.get("currency", "USD")
    price = info.get("price")
    change = info.get("change_pct")
    high_52w = info.get("high_52w")
    low_52w = info.get("low_52w")
    mkt_cap = info.get("market_cap")
    market_open = info.get("market_open", False)

    status_color = "🟢" if market_open else "🔴"
    status_text = "Mercado Aberto" if market_open else "Mercado Fechado"

    st.caption(f"{status_color} {status_text}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Preço Atual",
            value=format_currency(price, currency),
            delta=format_percentage(change) if change is not None else None,
        )
    with col2:
        st.metric(label="Market Cap", value=format_large_number(mkt_cap))
    with col3:
        st.metric(label="Máx. 52 Semanas", value=format_currency(high_52w, currency))
    with col4:
        st.metric(label="Mín. 52 Semanas", value=format_currency(low_52w, currency))
