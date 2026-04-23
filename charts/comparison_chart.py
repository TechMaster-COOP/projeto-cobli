import plotly.graph_objects as go
import pandas as pd
from config import TICKERS


def build_comparison_chart(histories: dict) -> go.Figure:
    fig = go.Figure()
    has_data = False

    for symbol, df in histories.items():
        if df.empty or "Close" not in df.columns or len(df) < 2:
            continue

        close = df["Close"].dropna()
        if close.empty:
            continue

        normalized = (close / close.iloc[0]) * 100
        meta = TICKERS.get(symbol, {})

        fig.add_trace(go.Scatter(
            x=normalized.index,
            y=normalized,
            mode="lines",
            line=dict(color=meta.get("color", "#888888"), width=2),
            name=meta.get("label", symbol),
            hovertemplate=f"{meta.get('label', symbol)}<br>%{{x|%d/%m/%Y}}<br>%{{y:.2f}} (base 100)<extra></extra>",
        ))
        has_data = True

    if not has_data:
        fig.add_annotation(text="Dados indisponíveis para comparação", showarrow=False,
                           font=dict(size=16, color="gray"))

    fig.add_hline(y=100, line_dash="dash", line_color="#555555", line_width=1)

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#2a2a2a", ticksuffix=""),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400,
    )
    return fig
