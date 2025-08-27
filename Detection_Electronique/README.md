# Laser Target Assist — Aide à la visée pour malvoyant par guidage sonore

Un système de détection de cible pour le handisport: guidé par un viseur caméra détectant le centre de la cible à l'aide d'une LED IR. Il permet aux personnes malvoyantes d'être assistées par retour sonore lors de la visée, solution adaptée à faible coût (200 -400 euro contre 4000 pour les systèmes actuels)


## Contexte et objectifs
- Produire un modèle à faible coût, performant et facile d'utilisation
- Traitement d'image en temps réel, filtrage et détection

## Données utilisées

- Les données proviennent de la caméra du détecteur, relié à l'ordinateur permettant leur traitement
- Les structures générales des fonctions de détections proviennent de F.A.I.R. Data.

## Structure
- `notebooks/Test_Laser_Detect.ipynb` – Notebook principal d’analyse & visualisation
- `assets/` – Dossier local contenant l'image test ainsi que le son guide
- `alert/` – Dossier contenant les fonctions principales d'avertissement
- `detection/` - Dossier contenant les fonctions principales de détection
- `requirements.txt`
- `README.md`

## Méthodologie
1. Chargement des images/ du flux de données
2. Prétraitements des images si nécessaire
3. Détection de la cible
4. Guidage sonore

## Résultats clés
- Son de détection ok

## Usage
```bash
pip install -r requirements.txt
jupyter lab notebooks/Test_Laser_Detect.ipynb
