# Prédiction météorologique avec Machine Learning

Ce projet a été réalisé dans le cadre d’une initiation au machine learning. L’objectif était de construire un modèle prédictif basé sur des données météorologiques (ex : température, humidité, pression) afin de prédire une variable cible (ex : pluie, température max).

## Contexte et objectifs
-La commune de grenoble, très industrialisée, est proie à des pics de pollution. Le but étend de prédire ces pics de pollution en fonction de données météorologiques fournies.
-Construction et comparaison de plusieurs modèle de ML pour la prédiction des pics de pollution de l'année 2018

## Données utilisées
-Un dataset "meteo.csv" nous a été fournie, disposant des données de 2017 et 2018

## Structure
- `notebooks/prediction_meteo.ipynb` – Notebook principal d’analyse & visualisation
- `data/meteo.csv` – DataSet regroupant les données de chaques stations météorologique sur 2017/2018
- `src/` – Dossier contenant les fonctions principales de traitements de données
- `utils/` - Dossier contenant les fonctions principales d'affichage
- `requirements.txt`
- `README.md`

## Étapes du projet

1. Chargement et nettoyage du dataset météo
2. Prétraitement des données (valeurs manquantes, normalisation, encoding)
3. Visualisation des corrélations
4. Séparation du dataset (train/test, validation croisée k-folds)
5. Comparaison de plusieurs algorithmes de ML :
   - KNN
   - Régression logistique
   - Arbre de décision
   - RandomForest
6. Évaluation (accuracy, F1-score, confusion matrix, RSE, RMSE, MAE, R²)
7. Choix du meilleur modèle

## Tech stack

- Python (pandas, scikit-learn, matplotlib, seaborn)
- Jupyter Notebook

## Usage
```bash
pip install -r requirements.txt
jupyter lab notebooks/prediction_meteo.ipynb
