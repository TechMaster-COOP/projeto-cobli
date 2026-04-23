import streamlit as st
from datetime import datetime
from config import PERIODS


def render_sidebar() -> str:
    st.sidebar.title("⚙️ Configurações")
    st.sidebar.markdown("---")

    period_labels = {k: v["label"] for k, v in PERIODS.items()}
    selected_key = st.sidebar.radio(
        "Período",
        options=list(period_labels.keys()),
        format_func=lambda k: period_labels[k],
        index=2,
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.sidebar.caption(f"Última atualização: {now}")

    st.sidebar.markdown("---")
    st.sidebar.caption("Dados fornecidos pelo Yahoo Finance via yfinance.\nAtualização automática a cada 5 minutos.")

    return selected_key
