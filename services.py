from __future__ import annotations

from urllib.parse import quote
import numpy as np
import pandas as pd
import requests
import streamlit as st

from config import BASE_URL, USER_AGENT


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_views(title: str, lang: str, start: str, end: str) -> pd.DataFrame:
    article = quote(title.strip().replace(" ", "_"), safe="")
    url = f"{BASE_URL}/{lang}.wikipedia.org/all-access/user/{article}/daily/{start}/{end}"
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=25
        )
        if response.status_code == 404:
            raise ValueError(f"L'article « {title} » est introuvable sur {lang}.wikipedia.org. Vérifie l'orthographe exacte.")
        response.raise_for_status()
        items = response.json().get("items", [])
    except requests.RequestException as exc:
        raise ValueError(f"Le service Wikipedia Analytics est indisponible : {exc}") from exc

    if not items:
        raise ValueError(f"Aucune consultation enregistrée pour « {title} » sur cette période.")

    df = pd.DataFrame(items)
    if not {"timestamp", "views"}.issubset(df.columns):
        raise ValueError("Format de réponse inattendu.")

    df["date"] = pd.to_datetime(df["timestamp"].str.slice(0, 8), format="%Y%m%d", errors="coerce")
    df["views"] = pd.to_numeric(df["views"], errors="coerce")
    df = df[["date", "views"]].dropna().drop_duplicates("date").sort_values("date")
    df["article"] = title.strip()
    return df.reset_index(drop=True)


def enrich_analytics(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy().sort_values("date")
    d["avg7"] = d["views"].rolling(7, min_periods=3).mean()
    d["baseline"] = d["views"].shift(1).rolling(28, min_periods=7).mean()
    d["std28"] = d["views"].shift(1).rolling(28, min_periods=7).std()
    d["zscore"] = (d["views"] - d["baseline"]) / d["std28"].replace(0, np.nan)
    d["obsession_index"] = 100 * d["views"] / d["baseline"].replace(0, np.nan)
    d["spike"] = d["zscore"] >= 2.0
    return d


def fmt_number(n: float | int | None) -> str:
    if n is None or pd.isna(n):
        return "—"
    return f"{n:,.0f}".replace(",", " ")


def get_diagnostic(obsession_score: float | None) -> tuple[str, str, int]:
    if pd.isna(obsession_score):
        return (
            "Données limitées",
            "Historique en cours de constitution pour ce sujet.",
            50
        )
    if obsession_score >= 180:
        return (
            "🔥 Surchauffe Virale",
            f"L'intérêt actuel est supérieur de {obsession_score - 100:.0f}% au niveau habituel !",
            min(100, int((obsession_score / 250) * 100))
        )
    if obsession_score >= 120:
        return (
            "⚡ Regain d'Attention",
            f"Activité modérée à la hausse (+{obsession_score - 100:.0f}% vs moyenne 28j).",
            min(100, int((obsession_score / 200) * 100))
        )
    if obsession_score <= 75:
        return (
            "💤 Calme Plat",
            "Le sujet est actuellement en dessous de son régime de croisière habituel.",
            max(10, int((obsession_score / 150) * 100))
        )
    return (
        "⚖️ Rythme Régulier",
        "Consommation stable et habituelle. Aucun pic atypique décelé.",
        50
    )
