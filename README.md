# L'Obsession du jour 🐦

Tableau de bord Python qui analyse les consultations d'articles Wikipédia pour révéler les obsessions les plus improbables d'Internet.

## Installation

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

L'application est disponible sur http://localhost:8501.

## Fonctionnalités

- Indicateurs: vues du dernier jour disponible, évolution J-1, moyenne mobile 7 jours, pic, cumul, volatilité
- Graphique temporel et moyenne mobile
- Score d'obsession relatif (écart à la tendance de référence), détection de pics (z-score)
- Comparaison de plusieurs articles et classement par vues
- Export CSV des données traitées
- Cache pour limiter les appels à Wikimedia
- Choix de la langue Wikipédia et de la période

## Source et limites

Source: Wikimedia Analytics Pageviews API (consultations d'articles, non visiteurs uniques). Les chiffres sont généralement publiés avec un délai; l'app affiche le dernier jour disponible et ne présente pas les résultats comme du temps réel. Les séries ne mesurent pas le nombre de recherches Google ni le nombre de personnes distinctes. Les données peuvent manquer ou changer selon la disponibilité de l'API.

L'API exige un User-Agent identifiable: configurez `WIKIMEDIA_USER_AGENT` dans votre environnement, par exemple `ObsessionDuJour/1.0 (contact: bonjour@example.org)`. Une valeur de secours est fournie pour le développement, mais un vrai contact est recommandé pour le déploiement.

Pour comparer des articles, leurs titres doivent exister sur le wiki sélectionné; les sujets par défaut ont des correspondances en français, à vérifier en cas de renommage.
