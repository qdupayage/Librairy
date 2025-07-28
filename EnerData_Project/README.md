# Prédiction du Prix de l'électricité dans le parc Européen

Ce projet a été réalisé dans le cadre de mon stage de 2ème année. L’objectif était de construire un modèle prédictif basé sur des données météorologiques (ex : température, précipitation, ensoleillement), ainsi que des données de consomation et production énergétiques (ex : production de nucleaire, échange entre Pays1 et Pays2, consomation, prix de la taxe sur le CO2) afin de prédire le prix de l'électricité, et de fournir une prédiction horodatée. Je n'ai pu utiliser le code, ni les données de ce projet, car c'est un projet privé. Cependant, j'ai réalisé un projet similaire, en générant des données afin de simuler les fonctions d'affichages, de calculs de coûts, etc...

## Étapes du projet

1. Automatisation du chargement et nettoyage des data du serveur
2. Prétraitement des données (valeurs manquantes, normalisation, encoding)
3. Visualisation des différentes entités (prix, consomation,..)
4. Compréhension et interprétations des différents facteurs influant sur le prix de l'électricité
5. Construction d'une fonction "coût" de l'électricité 
6. Évaluation de notre prédiction en confrontant réal/pred
7. Construction d'un modèle pypsa, afin de simuler d'autres périodes météorologiques complexe afin de comprendre son influence sur le prix de l'électricité.

## Tech stack

- Python (pandas, pypsa, matplotlib, pathlib)
- Jupyter Notebook
