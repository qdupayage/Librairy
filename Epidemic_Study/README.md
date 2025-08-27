# Epidemic Study — Analyse et prévision épidémiologique

## Contexte et objectifs
- Étude des données de propagation virale (Google Open Data)
- Objectifs : calcul de R₀ / Rₜ, cartes mondiales, modèles de prévision (XGBoost, Kalman)

## Données utilisées

-Les données proviennent de Google COVID-19 Open Data.
-Elles sont téléchargées automatiquement par le notebook au besoin depuis :
https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv

## Structure
- `notebooks/Epidemic_Study.ipynb` – Notebook principal d’analyse & visualisation
- `data/` – Dossier local ignoré par Git (scripts en téléchargement automatique)
- `src/` – Fonctions utilitaires (chargement, prétraitement, modèle)
- `requirements.txt`
- `README.md`

## Méthodologie
1. Chargement des données
2. Prétraitements : agrégation, conversion ISO-3
3. Visualisation : carte choroplèthe, Rₜ estimé
4. Modèles : renouvellement + filtre Kalman, XGBoost, SARIMA, Prophet
5. Évaluation : MAE, comparaison, prédictions futures

## Résultats clés
- Carte par pays des cas cumulés au dernier jour
- Estimation de Rₜ avec carte et seuil épidémique
- Modèle XGBoost performant (MAE ~19k), comparaison avec Kalman

## Usage
```bash
pip install -r requirements.txt
jupyter lab notebooks/Epidemic_Study.ipynb
