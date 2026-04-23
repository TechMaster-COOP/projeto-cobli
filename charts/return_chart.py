import plotly.graph_objects as go
import pandas as pd


def build_return_chart(df: pd.DataFrame, label: str, color: str) -> go.Figure:
    fig = go.Figure()

    if df.empty or "Close" not in df.columns or len(df) < 2:
        fig.add_annotation(text="Dados insuficientes", showarrow=False,
                           font=dict(size=16, color="gray"))
        return _apply_layout(fig)

    close = df["Close"].dropna()
    returns = (close / close.iloc[0] - 1) * 100

    line_color = "#26a69a" if returns.iloc[-1] >= 0 else "#ef5350"

    fig.add_trace(go.Scatter(
        x=returns.index,
        y=returns,
        mode="lines",
        line=dict(color=line_color, width=2),
        name=label,
        hovertemplate="%{x|%d/%m/%Y}<br>Retorno: %{y:+.2f}%<extra></extra>",
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="#555555", line_width=1)

    return _apply_layout(fig)


def _apply_layout(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#2a2a2a", ticksuffix="%"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig
