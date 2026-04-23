import plotly.graph_objects as go
import pandas as pd


def build_volume_chart(df: pd.DataFrame, label: str, color: str) -> go.Figure:
    fig = go.Figure()

    if df.empty or "Volume" not in df.columns:
        fig.add_annotation(text="Dados indisponíveis", showarrow=False,
                           font=dict(size=16, color="gray"))
        return _apply_layout(fig)

    if "Close" in df.columns and "Open" in df.columns:
        bar_colors = [
            "#26a69a" if c >= o else "#ef5350"
            for c, o in zip(df["Close"], df["Open"])
        ]
    else:
        bar_colors = color

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volume"],
        marker_color=bar_colors,
        name="Volume",
        hovertemplate="%{x|%d/%m/%Y}<br>Volume: %{y:,.0f}<extra></extra>",
    ))

    return _apply_layout(fig)


def _apply_layout(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#2a2a2a"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
    )
    return fig
