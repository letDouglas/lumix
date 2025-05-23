import cv2
import numpy as np
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnvironmentIntegrator:
    def __init__(self):
        logger.info("Initializing EnvironmentIntegrator")

    def place_car(self, car_image, background_image, position=(0.5, 0.8), scale=0.7):
        car_np = np.array(car_image)
        bg_np = np.array(background_image)

        car_height, car_width = car_np.shape[:2]
        bg_height, bg_width = bg_np.shape[:2]

        new_car_width = int(bg_width * scale)
        new_car_height = int(car_height * new_car_width / car_width)

        car_resized = cv2.resize(car_np, (new_car_width, new_car_height))

        x_offset = int(bg_width * position[0] - new_car_width / 2)
        y_offset = int(bg_height * position[1] - new_car_height)

        x_offset = max(0, min(x_offset, bg_width - new_car_width))
        y_offset = max(0, min(y_offset, bg_height - new_car_height))

        composite = bg_np.copy()

        y1, y2 = y_offset, y_offset + new_car_height
        x1, x2 = x_offset, x_offset + new_car_width

        if car_resized.shape[2] == 4:
            alpha_car = car_resized[:, :, 3] / 255.0
            alpha_car = np.expand_dims(alpha_car, axis=2)

            overlay_region = composite[y1:y2, x1:x2]

            for c in range(3):
                overlay_region[:, :, c] = overlay_region[:, :, c] * (1 - alpha_car[:, :, 0]) + \
                                          car_resized[:, :, c] * alpha_car[:, :, 0]

            composite[y1:y2, x1:x2] = overlay_region
        else:
            composite[y1:y2, x1:x2] = car_resized

        return Image.fromarray(composite)

    def add_shadow(self, composite_image, light_direction):
        comp_np = np.array(composite_image)

        gray = cv2.cvtColor(comp_np, cv2.COLOR_RGB2GRAY)
        _, car_mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

        shadow_offset_x = int(light_direction[0] * 20)
        shadow_offset_y = int(light_direction[1] * 20)

        shadow = cv2.GaussianBlur(car_mask, (21, 21), 0)

        h, w = shadow.shape
        M = np.float32([[1, 0, shadow_offset_x], [0, 1, shadow_offset_y]])
        shadow_shifted = cv2.warpAffine(shadow, M, (w, h))

        shadow_factor = 0.7
        shadow_shifted = shadow_shifted / 255.0 * 0.3

        for c in range(3):
            comp_np[:, :, c] = comp_np[:, :, c] * (1 - shadow_shifted)

        return Image.fromarray(comp_np)
