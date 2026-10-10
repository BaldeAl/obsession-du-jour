from __future__ import annotations

from datetime import date, timedelta
from urllib.parse import quote

import numpy as np
import pandas as pd
import streamlit as st

from config import LANGUAGES, TOPICS_PRESETS
from styles import CUSTOM_CSS
from services import enrich_analytics, fetch_views, fmt_number, get_diagnostic
from charts import create_duel_chart, create_overview_chart
from ui_components import render_footer, render_hero, render_ranking_card, render_status_card

st.set_page_config(
    page_title="L'Obsession du Jour · Radar Wikipedia",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "main_topic_input" not in st.session_state:
    st.session_state["main_topic_input"] = "Pigeon"


def select_preset(preset_name: str) -> None:
    st.session_state["main_topic_input"] = preset_name


with st.sidebar:
    st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
            <div style="background:#222734;border:1px solid rgba(255,255,255,0.15);border-radius:12px;width:38px;height:38px;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 0 #0d0f14;font-size:1.2rem;">👁️</div>
            <div>
                <div style="font-weight:700;font-size:1.05rem;line-height:1.2;">Radar d'Intérêt</div>
                <div style="font-size:0.75rem;color:var(--text-muted);">Wikimedia Analytics</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='margin:12px 0;border-color:rgba(255,255,255,0.07);'>", unsafe_allow_html=True)

    st.markdown("<div class='quick-picks-label'>Recherche d'Article</div>", unsafe_allow_html=True)
    st.text_input(
        "Article Wikipédia",
        key="main_topic_input",
        label_visibility="collapsed",
        placeholder="Ex: Pigeon, Tour Eiffel, Pizza..."
    )

    language_label = st.selectbox("Édition linguistique", list(LANGUAGES.keys()), index=0)
    lang_code = LANGUAGES[language_label]

    period_days = st.select_slider(
        "Période d'observation",
        options=[14, 30, 60, 90, 180, 365],
        value=90,
        format_func=lambda x: f"{x} jours"
    )

    st.markdown("<hr style='margin:18px 0;border-color:rgba(255,255,255,0.07);'>", unsafe_allow_html=True)
    st.markdown("<div class='quick-picks-label'>Comparateur (Multi-sujets)</div>", unsafe_allow_html=True)

    default_comparisons = ["Moustique", "Cornichon"] if lang_code == "fr" else ["Cat", "Pizza"]
    current_topic = st.session_state.get("main_topic_input", "Pigeon").strip().lower()
    available_presets = [p for p in TOPICS_PRESETS if p.strip().lower() != current_topic]
    valid_defaults = [c for c in default_comparisons if c in available_presets]
    compare_topics = st.multiselect(
        "Sujets à comparer",
        options=available_presets,
        default=valid_defaults,
        max_selections=5,
        key=f"compare_multiselect_{current_topic}",
        label_visibility="collapsed"
    )

    st.caption("ℹ️ Données officielles de consultation journalière d'articles Wikimedia.")


render_hero()

st.markdown("<div class='quick-picks-label'>💡 Explorer en un clic :</div>", unsafe_allow_html=True)
pill_cols = st.columns(len(TOPICS_PRESETS))
for idx, preset in enumerate(TOPICS_PRESETS):
    pill_cols[idx].button(
        preset,
        key=f"pill_{preset}",
        on_click=select_preset,
        args=(preset,),
        width="stretch"
    )

st.write("")

active_topic = st.session_state.get("main_topic_input", "Pigeon").strip()
if not active_topic:
    st.warning("⚠️ Renseigne un nom d'article pour lancer le radar.")
    st.stop()

today = date.today()
end_date = today - timedelta(days=1)
start_date = end_date - timedelta(days=period_days + 35)
start_str, end_str = start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")

try:
    with st.spinner(f"Analyse des consultations pour « {active_topic} »..."):
        raw_df = fetch_views(active_topic, lang_code, start_str, end_str)
        enriched_df = enrich_analytics(raw_df)

    cutoff_date = pd.Timestamp(end_date - timedelta(days=period_days - 1))
    visible_df = enriched_df.loc[enriched_df["date"] >= cutoff_date].copy()

    if visible_df.empty:
        raise ValueError("Aucune donnée collectée sur cette période.")

except ValueError as err:
    st.error(f"❌ {err}")
    st.info("💡 Astuce : essaie un mot clé simple présent dans le titre officiel de l'article.")
    st.stop()

latest_row = visible_df.iloc[-1]
prev_row = visible_df.iloc[-2] if len(visible_df) > 1 else None
pct_change = ((latest_row["views"] / prev_row["views"] - 1) * 100) if prev_row is not None and prev_row["views"] > 0 else np.nan
peak_row = visible_df.loc[visible_df["views"].idxmax()]
obsession_score = latest_row["obsession_index"]

diag_status, diag_desc, gauge_percent = get_diagnostic(obsession_score)

tab_overview, tab_duel, tab_data = st.tabs([
    "📈 Analyse & Tendances",
    "⚔️ Duel Comparatif",
    "📋 Données & Export"
])

with tab_overview:
    st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div style="font-size:1.35rem;font-weight:700;">
                {active_topic} <span style="font-size:0.9rem;color:var(--text-muted);font-weight:500;">· Édition {lang_code.upper()}</span>
            </div>
            <div style="font-size:0.85rem;color:var(--text-muted);background:#181b24;padding:4px 12px;border-radius:10px;border:1px solid rgba(255,255,255,0.08);">
                Dernier relevé : <b>{latest_row['date']:%d/%m/%Y}</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

    metric_cols = st.columns(4)
    delta_str = f"{pct_change:+.1f} % vs veille" if pd.notna(pct_change) else None
    metric_cols[0].metric(label="Vues (Dernier jour)", value=fmt_number(latest_row["views"]), delta=delta_str)
    metric_cols[1].metric(label="Moyenne 7 Jours", value=fmt_number(latest_row["avg7"]))
    metric_cols[2].metric(label="Record de Période", value=fmt_number(peak_row["views"]), delta=f"Le {peak_row['date']:%d/%m/%Y}", delta_color="off")
    metric_cols[3].metric(label="Total Cumulé", value=fmt_number(visible_df["views"].sum()))

    st.write("")

    chart_col, diag_col = st.columns([2.6, 1])

    with chart_col:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-size:1.05rem;font-weight:700;margin-bottom:6px;'>📈 Courbe d'Intérêt & Anomalies</div>", unsafe_allow_html=True)
        st.plotly_chart(create_overview_chart(visible_df), width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with diag_col:
        render_status_card(diag_status, diag_desc, gauge_percent)

        st.markdown("""<div class="content-card" style="padding:18px 20px;">""", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.82rem;font-weight:700;color:var(--text-muted);letter-spacing:0.06em;text-transform:uppercase;margin-bottom:10px;'>Signal & Volatilité</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        c1.metric("Pics Détectés", int(visible_df["spike"].sum()))
        volatility = (visible_df["views"].std() / visible_df["views"].mean() * 100) if len(visible_df) > 1 and visible_df["views"].mean() > 0 else np.nan
        c2.metric("Volatilité", f"{volatility:.1f} %" if pd.notna(volatility) else "—")

        st.caption("ℹ️ Un pic correspond à une variation supérieure à 2 écarts-types par rapport aux 28 jours précédents.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_duel:
    st.markdown("""
        <div style="margin-bottom:²14px;">
            <div style="font-size:1.2rem;font-weight:700;">⚔️ Duel d'Intérêt & Benchmarking</div>
            <div style="font-size:0.85rem;color:var(--text-muted);">Compare le volume d'attention de plusieurs sujets sur la même période.</div>
        </div>
    """, unsafe_allow_html=True)

    all_duel_topics = [active_topic] + [t for t in compare_topics if t.lower() != active_topic.lower()]
    duel_records = []
    duel_series = []

    for item in all_duel_topics:
        try:
            item_df = raw_df if item == active_topic else fetch_views(item, lang_code, start_str, end_str)
            item_cut = item_df.loc[item_df["date"] >= cutoff_date].copy()
            if item_cut.empty:
                continue
            duel_series.append(item_cut)
            duel_records.append({
                "Sujet": item,
                "Vues Totales": int(item_cut["views"].sum()),
                "Moyenne / Jour": round(item_cut["views"].mean()),
                "Pic Enregistré": int(item_cut["views"].max())
            })
        except ValueError:
            pass

    if duel_records:
        ranking_df = pd.DataFrame(duel_records).sort_values("Vues Totales", ascending=False).reset_index(drop=True)
        max_total = ranking_df["Vues Totales"].max()

        col_table, col_chart = st.columns([1.1, 1.9])

        with col_table:
            render_ranking_card(ranking_df, active_topic, max_total)

        with col_chart:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<div style='font-size:0.95rem;font-weight:700;margin-bottom:8px;'>📊 Confrontation Temporelle</div>", unsafe_allow_html=True)
            combined_df = pd.concat(duel_series, ignore_index=True)
            st.plotly_chart(create_duel_chart(combined_df, ranking_df), width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Sélectionne des sujets additionnels dans le menu latéral pour afficher le duel.")

with tab_data:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
            <div>
                <div style="font-size:1.05rem;font-weight:700;">Extraction & Données Calculées</div>
                <div style="font-size:0.8rem;color:var(--text-muted);">Série temporelle complète avec scores statistiques.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    export_df = visible_df[[
        "date", "views", "avg7", "baseline", "zscore", "obsession_index", "spike"
    ]].rename(columns={
        "date": "Date",
        "views": "Vues",
        "avg7": "Moyenne 7j",
        "baseline": "Base 28j",
        "zscore": "Z-Score",
        "obsession_index": "Indice Obsession",
        "spike": "Anomalie"
    }).sort_values("Date", ascending=False)

    st.dataframe(export_df, width="stretch", hide_index=True, height=320)

    csv_data = export_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 Télécharger le rapport CSV",
        data=csv_data,
        file_name=f"obsession_{quote(active_topic.lower(), safe='')}_{lang_code}.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()
