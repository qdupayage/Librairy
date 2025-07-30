from playsound import playsound
import os

def play_beep():
    sound_path = os.path.join(os.path.dirname(__file__), "../assets/sounds/beep.wav")
    playsound(sound_path)
