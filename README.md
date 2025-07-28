# 📚 Bibliothèque de traitements numériques & projets techniques

Bienvenue dans mon dépôt de projets personnels et académiques en Python, MATLAB et Java.  
Ce dépôt centralise plusieurs travaux réalisés dans les domaines du **traitement du signal**, **machine learning**, **vision par ordinateur**, **optimisation** et **applications énergétiques**.

---

## 🗂️ Structure du dépôt

---

## 🚀 Projets principaux

### 🔋 Enerdata — Simulation réseau électrique (Panel App + PyPSA)
- Visualisation des données énergétiques au pas horaire
- Interface multi-onglets avec **Panel**
- Modélisation réseau via **PyPSA**

---

### ☁️ Meteo Prediction — Machine Learning
- Dataset météo synthétique (`meteo.csv`)
- Prétraitement : normalisation, split
- Modèles ML : KNN, Régression logistique, Arbre, Random Forest
- Évaluation complète avec confusion matrix

---

### ☁️ Java Project — Synthétiseur de son
- Librairie fournie d'analyse audio: lib\phelmaaudio.jar
- Construction d'une structure de "module", ayant différents paramètres:
- Port de connexion, entrée, sortie, patch, etc...
- Synthétisation d'opérations de traitements audio: ecchos, atténuation, etc

---

### 🧠 data_process/
- Implémentations :
  - 📊 **ACP** (Python et MATLAB)
  - 🧠 **Réseaux de neurones convolutionnels**
  - 🧪 **Optimisation** (descente de gradient, Newton)
  - 🔍 **Filtrage de Kalman**, clustering, etc.
- Comparaisons MATLAB ↔ Python

---

### 🧪 Signal Process & Signal Analysis
- Extraction spectrale (Welch, FFT)
- Visualisation interactive (`App.py`)
- Filtres anti-aliasing, sur-/sous-échantillonnage
- Visualisation statistique (moyenne, écart-type...)

---

### 🖼️ Image Process
- Seuillage (global, adaptatif)
- Détection de formes (Hough)
- Détection de blobs et contours

---

### ☕ Java_Work
- Projets audio/numériques en Java
- Librairie externe `phelmaaudio.jar`
- Fichiers `.java` fonctionnels + tests

---

## ⚙️ Installation

```bash
# Installation des dépendances globales
pip install -r requirements.txt

