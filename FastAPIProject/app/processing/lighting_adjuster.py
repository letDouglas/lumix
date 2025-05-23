import cv2
import numpy as np
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LightingAdjuster:
    def __init__(self):
        logger.info("Initializing LightingAdjuster")

    def estimate_lighting(self, background_image):
        bg_np = np.array(background_image)
        bg_gray = cv2.cvtColor(bg_np, cv2.COLOR_RGB2GRAY)

        grad_x = cv2.Sobel(bg_gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(bg_gray, cv2.CV_64F, 0, 1, ksize=3)

        light_intensity = np.mean(bg_gray) / 255.0

        direction_x = np.mean(grad_x)
        direction_y = np.mean(grad_y)
        light_direction = (direction_x, direction_y)

        h, w = bg_gray.shape
        light_map = np.ones((h, w), dtype=np.float32) * light_intensity

        y, x = np.mgrid[0:h, 0:w]

        x = x - w / 2
        y = y - h / 2

        light_gradient = 0.2 * (x * light_direction[0] + y * light_direction[1]) / max(w, h)
        light_map += light_gradient

        light_map = np.clip(light_map, 0.5, 1.5)

        return light_map, light_direction

    def apply_lighting(self, car_image, light_map):
        car_np = np.array(car_image)

        rgb = car_np[:, :, :3]
        alpha = car_np[:, :, 3] if car_np.shape[2] == 4 else None

        light_map_resized = cv2.resize(light_map, (rgb.shape[1], rgb.shape[0]))

        adjusted_rgb = rgb.copy().astype(np.float32)
        for i in range(3):
            adjusted_rgb[:, :, i] = np.clip(adjusted_rgb[:, :, i] * light_map_resized, 0, 255)

        adjusted_rgb = adjusted_rgb.astype(np.uint8)
        if alpha is not None:
            result = np.dstack((adjusted_rgb, alpha))
        else:
            result = adjusted_rgb

        return Image.fromarray(result)
