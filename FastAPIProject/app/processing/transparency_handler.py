import cv2
import numpy as np
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransparencyHandler:
    def __init__(self):
        logger.info("Initializing TransparencyHandler")

    def detect_windows(self, car_image):
        car_np = np.array(car_image)

        if car_np.shape[2] == 3:
            alpha_channel = np.ones(car_np.shape[:2], dtype=np.uint8) * 255
            car_np = np.dstack((car_np, alpha_channel))

        bgr = car_np[:, :, :3]

        hsv = cv2.cvtColor(bgr, cv2.COLOR_RGB2HSV)

        lower_window = np.array([0, 0, 0])
        upper_window = np.array([180, 30, 200])

        window_mask = cv2.inRange(hsv, lower_window, upper_window)

        kernel = np.ones((5, 5), np.uint8)
        window_mask = cv2.morphologyEx(window_mask, cv2.MORPH_CLOSE, kernel)
        window_mask = cv2.morphologyEx(window_mask, cv2.MORPH_OPEN, kernel)

        window_mask = cv2.GaussianBlur(window_mask, (21, 21), 0)

        window_mask = window_mask / 255.0

        car_np[:, :, 3] = np.clip(car_np[:, :, 3] * (1 - window_mask * 0.7), 0, 255).astype(np.uint8)

        return Image.fromarray(car_np)
