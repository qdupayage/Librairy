# Laser Target Assist — Audio-Guided Aiming Aid for the Visually Impaired

A target detection system designed for parasports: guided by a camera scope detecting the center of the target using an IR LED.  
It enables visually impaired individuals to be assisted by audio feedback while aiming, providing a low-cost solution (€200–400 vs. ~€4000 for current systems).

## Context and Objectives
- Develop a low-cost, efficient, and user-friendly model
- Real-time image processing, filtering, and detection

## Data Used
- Data comes from the detector’s camera, connected to the computer for processing
- General detection function structures are inspired by F.A.I.R. Data

## Structure
- `notebooks/Test_Laser_Detect.ipynb` – Main notebook for analysis & visualization
- `assets/` – Local folder containing the test image and guidance sound
- `alert/` – Main audio warning functions
- `detection/` – Main detection functions
- `requirements.txt`
- `README.md`

## Methodology
1. Load images/data stream
2. Apply preprocessing if necessary
3. Target detection
4. Audio guidance

## Key Results
- Detection sound working successfully

## Usage
```bash
pip install -r requirements.txt
jupyter lab notebooks/Test_Laser_Detect.ipynb
