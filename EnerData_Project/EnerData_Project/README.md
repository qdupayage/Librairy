# Simulation d’un Réseau Électrique Européen avec PyPSA

Ce projet vise à modéliser un réseau électrique simplifié de l’Europe avec [PyPSA](https://pypsa.org), en exploitant des données énergétiques horaires de consommation et de production.

Il a été initié dans le cadre de travaux réalisés chez **Énerdata**, où j’ai participé à l’analyse de scénarios énergétiques et à la modélisation de systèmes multi-énergies.

---

## 🧰 Technologies utilisées

- Python (pandas, numpy, matplotlib)
- PyPSA (Python for Power System Analysis)
- Données de production/consommation horaires (CSV ou Excel)

---

## 📊 Données utilisées

- Données de charge (load) horaires par pays
- Données de production ENR (solaire/éolien)
- Données de production nucléaires
- Données de production fossilles (charbon/gaz, production taxée)
- Capacités installées par type
- Réseau de transport interconnecté entre pays
- Différents distributeurs de données (C3S, Ensoe, ...)

---

## 🚀 Objectifs

- Visualiser les courbes de charge horaires
- Construire un modèle PyPSA multi-nœuds (1 nœud = 1 pays)
- Simuler l’équilibre offre-demande sur 24h ou plus
- Évaluer les échanges entre pays
- Comparer les différents mix électriques
- Fournir un modèle de prévision du prix de l'électricité pour chaques zones

---

## 🚀 Visualisation Partielle

- Visualiser les courbes de charge horaires
- Construire un modèle PyPSA multi-nœuds (1 nœud = 1 pays)
- Simuler l’équilibre offre-demande sur 24h ou plus
- Évaluer les échanges entre pays
- Comparer les différents mix électriques
- Fournir un modèle de prévision du prix de l'électricité pour chaques zones

---

## 🔧 Lancer le projet

1. **Cloner ce dépôt** :
   ```bash
   git clone https://gitlab.ensimag.fr/dupayagq/bibliotheque/EnerData_Projet.git
   cd EnerData_Projet

2. **Lancer l'application Panel** :
   ```bash
   Commande à rentrer dans la console afin de lancer l'application: panel serve panel_app.py --autoreload

