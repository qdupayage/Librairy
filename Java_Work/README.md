# 🎼 Java Modular Synth - Patch-Based Audio Engine

This project is a Java modular synthesis engine that allows you to create complex sounds from basic modules (oscillators, envelopes, filters, mixers). Inspired by DAWs such as FL Studio.

## 🧩 Features
- Signal generators: `GenSine`, `GenSquare`, etc.
- Processing modules: `Multiplier`, `Mixer`, `ADSR`, `Filter`, etc.
- `PatchScheduler` system for playing note sequences
- Support for ADSR envelopes and dynamic frequency modulation
- Command line interface / visualisation in a notebook

## ⚙️ Technical objectives
- Frequency analysis of signals
- Real-time and sequential control
- Extensible for future MIDI or additive/FFT synthesis modules

## 📊 Performance metrics
- Signal-to-noise ratio, dissonance
- Temporal accuracy in patch playback
- Memory and CPU usage

## 📁 Structure
- `/src`: Java source code
- `/patches`: patch examples
- `/tests`: audio unit tests

## ▶️ Execution
Compile the project with:
```bash
javac src/*.java
java Main