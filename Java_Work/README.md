# 🎼 Java Modular Synth - Patch-Based Audio Engine

Ce projet est un moteur de synthèse modulaire Java permettant de créer des sons complexes à partir de modules élémentaires (oscillateurs, enveloppes, filtres, mixeurs). Inspiré des DAWs comme FL Studio.

## 🧩 Fonctionnalités
- Générateurs de signaux : `GenSine`, `GenSquare`, etc.
- Modules de traitement : `Multiplier`, `Mixer`, `ADSR`, `Filter`, etc.
- Système de `PatchScheduler` pour jouer des séquences de notes
- Support des enveloppes ADSR et modulation dynamique de fréquence
- Interface en ligne de commande / visualisation dans un notebook

## ⚙️ Objectifs techniques
- Analyse fréquentielle des signaux
- Contrôle temps réel et séquentiel
- Extensible pour futurs modules MIDI ou synthèse additive/FFT

## 📊 Mesures de performance
- Rapport signal/bruit, dissonance
- Précision temporelle dans la lecture des patchs
- Utilisation mémoire et CPU

## 📁 Structure
- `/src` : code source Java
- `/patches` : exemples de patchs
- `/tests` : tests unitaires audio

## ▶️ Exécution
Compilez le projet avec :
```bash
javac src/*.java
java Main
