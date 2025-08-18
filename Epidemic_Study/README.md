# 📊 Étude épidémiologique – Analyse de propagation virale

Ce projet a pour objectif de démontrer des compétences en **science des données**, appliquées à une étude épidémiologique.  
À partir de données ouvertes (COVID-19 – Our World in Data), on analyse :

- Les vecteurs de propagation (par pays, continents, mobilité)
- La vitesse de propagation d’un virus
- L’estimation du taux de reproduction de base **R₀**
- Des visualisations temporelles et spatiales

## 🚀 Installation

Cloner le dépôt :

```bash
git clone https://github.com/ton_profil/EpidemioStudy.git
cd EpidemioStudy
```

```Instalation
pip install -r requirements.txt

📚 Données utilisées

Les données proviennent de Google COVID-19 Open Data.
👉 Pour alléger le dépôt, les données ne sont pas stockées dans le repo.
Elles sont téléchargées automatiquement par le notebook au besoin depuis :
https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv