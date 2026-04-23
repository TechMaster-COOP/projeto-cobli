import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data(ttl=300)
def get_ticker_info(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        fi = ticker.fast_info

        current_price = getattr(fi, "last_price", None)
        prev_close = getattr(fi, "previous_close", None)

        if current_price and prev_close and prev_close != 0:
            daily_change = ((current_price - prev_close) / prev_close) * 100
        else:
            daily_change = None

        market_state = getattr(fi, "market_state", None)

        return {
            "price":        current_price,
            "change_pct":   daily_change,
            "high_52w":     getattr(fi, "fifty_two_week_high", None),
            "low_52w":      getattr(fi, "fifty_two_week_low", None),
            "market_cap":   getattr(fi, "market_cap", None),
            "currency":     getattr(fi, "currency", "USD"),
            "market_open":  market_state == "REGULAR",
            "market_state": market_state,
        }
    except Exception:
        return {
            "price": None, "change_pct": None, "high_52w": None,
            "low_52w": None, "market_cap": None, "currency": "USD",
            "market_open": False, "market_state": None,
        }


@st.cache_data(ttl=300)
def get_price_history(symbol: str, period: str, interval: str) -> pd.DataFrame:
    try:
        df = yf.download(symbol, period=period, interval=interval,
                         auto_adjust=True, progress=False, multi_level_index=False)
        if df.empty:
            # fallback: try fetching last 5 days for intraday
            if interval in ("5m", "1h"):
                df = yf.download(symbol, period="5d", interval=interval,
                                 auto_adjust=True, progress=False, multi_level_index=False)
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=300)
def get_all_histories(symbols: list, period: str, interval: str) -> dict:
    result = {}
    for symbol in symbols:
        result[symbol] = get_price_history(symbol, period, interval)
    return result
