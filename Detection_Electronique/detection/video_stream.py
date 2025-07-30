# detection/video_stream.py
import cv2
from config import CAMERA_INDEX

def open_camera():
    """ Ouvre la caméra et retourne l'objet VideoCapture. """
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise IOError(f"Impossible d'ouvrir la caméra à l'index {CAMERA_INDEX}")
    return cap
