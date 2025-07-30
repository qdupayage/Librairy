import cv2
import numpy as np
from config import CAMERA_INDEX

def detect_laser():
    cap = cv2.VideoCapture(CAMERA_INDEX)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.medianBlur(mask1 | mask2, 5)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        center = None
        if contours:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                center = (cx, cy)
                cv2.circle(frame, center, 10, (0, 255, 0), -1)

        cv2.imshow("Laser Detection", frame)

        yield frame, center

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
