from __future__ import annotations

import os

TOPICS_PRESETS = [
    "Pigeon", "Moustique", "Cornichon", "Dinosaure",
    "Pizza", "Toilettes", "Chat", "Licorne", "Cafard", "Banane"
]

LANGUAGES = {
    "Français": "fr",
    "English": "en",
    "Español": "es",
    "Deutsch": "de"
}

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"

USER_AGENT = os.getenv(
    "WIKIMEDIA_USER_AGENT",
    "ObsessionDuJourApp/2.0 (editorial-dashboard; contact: studio@obsession.app)"
)
