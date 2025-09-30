# Weather forecasting with machine learning

This project was carried out as part of an introduction to machine learning. The aim was to build a predictive model based on meteorological data (e.g. temperature, humidity, pressure) in order to predict a target variable (e.g. rain, maximum temperature).

## Context and objectives
-The highly industrialised city of Grenoble is prone to pollution peaks. The aim is to predict these pollution peaks based on the meteorological data provided.
-Construction and comparison of several ML models for predicting pollution peaks in 2018

## Data used
-A dataset called ‘meteo.csv’ was provided to us, containing data from 2017 and 2018.

## Structure
- `notebooks/prediction_meteo.ipynb` – Main analysis & visualisation notebook
- `data/meteo.csv` – DataSet containing data from each weather station for 2017/2018
- `src/` – Folder containing the main data processing functions
- `utils/` - Folder containing the main display functions
- `requirements.txt`
- `README.md`

## Project steps

1. Loading and cleaning the weather dataset
2. Pre-processing the data (missing values, normalisation, encoding)
3. Visualisation of correlations
4. Separation of the dataset (train/test, k-folds cross-validation)
5. Comparison of several ML algorithms:
   - KNN
   - Logistic regression
   - Decision tree
   - RandomForest
6. Evaluation
7. Choix du meilleur modèle

## Tech stack

- Python (pandas, scikit-learn, matplotlib, seaborn)
- Jupyter Notebook

## Utilisation
```bash
pip install -r requirements.txt
jupyter lab notebooks/prediction_meteo.ipynb