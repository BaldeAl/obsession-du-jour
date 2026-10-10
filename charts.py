from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def create_overview_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["date"],
        y=df["views"],
        name="Vues du jour",
        marker=dict(
            color="#4a6fa5",
            line=dict(color="#6b8fc2", width=0.8)
        ),
        opacity=0.78,
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Vues : <b>%{y:,.0f}</b><extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["avg7"],
        name="Tendance lissée (7j)",
        mode="lines",
        line=dict(color="#f0c060", width=3, shape="spline"),
        hovertemplate="Moyenne 7j : <b>%{y:,.0f}</b><extra></extra>"
    ))

    spike_points = df.loc[df["spike"]]
    if not spike_points.empty:
        fig.add_trace(go.Scatter(
            x=spike_points["date"],
            y=spike_points["views"],
            name="Anomalie / Pic détecté",
            mode="markers",
            marker=dict(
                symbol="diamond-tall",
                size=13,
                color="#ff7b5c",
                line=dict(color="#1a1e27", width=2)
            ),
            hovertemplate="<b>⚠️ PIC INHABITUEL</b><br>Vues : %{y:,.0f}<extra></extra>"
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=390,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#9ca3af", size=11),
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            zeroline=False,
            tickfont=dict(color="#8b93a3", size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            zeroline=False,
            tickfont=dict(color="#8b93a3", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#1a1e27",
            bordercolor="rgba(255,255,255,0.2)",
            font=dict(color="#ffffff", family="Plus Jakarta Sans")
        )
    )
    return fig


def create_duel_chart(combined_df: pd.DataFrame, ranking_df: pd.DataFrame) -> go.Figure:
    palette = ["#f0c060", "#6eb5ff", "#7ee8a2", "#ff8fa3", "#c4a9f5", "#ffb347"]
    fig = go.Figure()

    for idx, item_name in enumerate(ranking_df["Sujet"]):
        sub = combined_df[combined_df["article"] == item_name]
        color = palette[idx % len(palette)]
        dash_style = "solid" if idx == 0 else ("dot" if idx % 2 == 1 else "dash")

        fig.add_trace(go.Scatter(
            x=sub["date"],
            y=sub["views"],
            mode="lines",
            name=item_name,
            line=dict(color=color, width=2.5 if idx == 0 else 1.8, dash=dash_style),
            hovertemplate=f"<b>{item_name}</b>: %{{y:,.0f}} vues<extra></extra>"
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=5, r=5, t=10, b=5),
        legend=dict(orientation="h", y=1.12, x=0, font=dict(color="#a0aec0", size=11)),
        xaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)", zeroline=False)
    )
    return fig
