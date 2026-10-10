from __future__ import annotations

import streamlit as st
from services import fmt_number


def render_hero() -> None:
    st.markdown("""
    <div class="hero-box">
        <div>
            <div class="hero-pill">● MONOCHROME LAB · EDITION V2</div>
            <h1 style="margin:10px 0 6px 0; font-size:2.2rem; font-weight:800;">L'Obsession du Jour</h1>
            <p style="margin:0; color:#9ba3b2; font-size:0.95rem; max-width:680px;">
                Mesure l'attention collective et détecte les pics d'engouement soudains sur les pages Wikipédia.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_status_card(status: str, desc: str, gauge_percent: int) -> None:
    st.markdown(f"""
    <div class="status-card">
        <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);letter-spacing:0.08em;text-transform:uppercase;">
            Baromètre de Hype
        </div>
        <div style="margin:10px 0;">
            <span class="status-badge">{status}</span>
        </div>
        <div class="gauge-container">
            <div class="gauge-fill" style="width: {gauge_percent}%;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:var(--text-muted);font-weight:600;">
            <span>Calme</span>
            <span>Standard</span>
            <span>Viral</span>
        </div>
        <p style="font-size:0.86rem;color:#b2b9c7;margin:14px 0 0 0;line-height:1.45;">
            {desc}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_ranking_card(ranking_df, active_topic: str, max_total: int | float) -> None:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.95rem;font-weight:700;margin-bottom:12px;'>🏆 Classement d'Attention</div>", unsafe_allow_html=True)

    for rank_idx, row in ranking_df.iterrows():
        bar_w = int((row["Vues Totales"] / max_total) * 100) if max_total > 0 else 0
        is_active = (row["Sujet"] == active_topic)
        border_color = "rgba(255,255,255,0.3)" if is_active else "rgba(255,255,255,0.06)"
        badge_bg = "#293040" if is_active else "#181a21"

        st.markdown(f"""
            <div style="background:{badge_bg};border:1px solid {border_color};border-radius:14px;padding:12px 14px;margin-bottom:10px;box-shadow:0 3px 0 #090a0d;">
                <div style="display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:0.95rem;">
                    <span>#{rank_idx + 1} {row['Sujet']} {'⭐' if is_active else ''}</span>
                    <span>{fmt_number(row['Vues Totales'])}</span>
                </div>
                <div style="background:#0c0d12;height:6px;border-radius:999px;margin:8px 0 6px 0;overflow:hidden;">
                    <div style="background:#ffffff;height:100%;width:{bar_w}%;border-radius:999px;"></div>
                </div>
                <div style="font-size:0.75rem;color:var(--text-muted);display:flex;justify-content:space-between;">
                    <span>Moyenne: {fmt_number(row['Moyenne / Jour'])}/j</span>
                    <span>Pic: {fmt_number(row['Pic Enregistré'])}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown("""
    <div style="text-align:center;padding:28px 0 10px 0;font-size:0.8rem;color:#6b7280;border-top:1px solid rgba(255,255,255,0.06);margin-top:20px;">
        Radar d'Attention · Données officielles Wikimedia Analytics API · Traitement analytique indépendant.
    </div>
    """, unsafe_allow_html=True)
