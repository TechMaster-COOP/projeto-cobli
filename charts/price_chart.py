import plotly.graph_objects as go
import pandas as pd


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def build_price_chart(df: pd.DataFrame, label: str, color: str, currency: str) -> go.Figure:
    fig = go.Figure()

    if df.empty or "Close" not in df.columns:
        fig.add_annotation(text="Dados indisponíveis", showarrow=False,
                           font=dict(size=16, color="gray"))
        return _apply_layout(fig)

    currency_symbol = "R$" if currency == "BRL" else "US$"

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        fill="tozeroy",
        fillcolor=_hex_to_rgba(color, 0.1),
        line=dict(color=color, width=2),
        name=label,
        hovertemplate=f"%{{x|%d/%m/%Y %H:%M}}<br>Preço: {currency_symbol} %{{y:,.2f}}<extra></extra>",
    ))

    return _apply_layout(fig)


def _apply_layout(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(showgrid=False, rangeslider=dict(visible=False)),
        yaxis=dict(gridcolor="#2a2a2a"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig
