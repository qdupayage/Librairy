from detection.laser_detector import detect_laser
from config import CENTER_TOLERANCE
from alert.sound_alert import play_beep

def main():
    for frame, center in detect_laser():
        if center is not None:
            cx, cy = center
            if abs(cx - 320) < CENTER_TOLERANCE and abs(cy - 240) < CENTER_TOLERANCE:
                play_beep()

if __name__ == "__main__":
    main()
