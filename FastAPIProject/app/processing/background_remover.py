import numpy as np
import cv2
from rembg import remove
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundRemover:
    def __init__(self):
        logger.info("Initializing BackgroundRemover")

    def remove_background(self, image_path):
        try:
            logger.info(f"Processing image: {image_path}")

            input_image = Image.open(image_path)

            output_image = remove(input_image)

            logger.info("Background removal completed successfully")
            return output_image

        except Exception as e:
            logger.error(f"Error during background removal: {str(e)}")
            raise

    def refine_edges(self, image):
        np_image = np.array(image)

        if np_image.shape[2] == 4:
            alpha = np_image[:, :, 3]

            alpha_smooth = cv2.GaussianBlur(alpha, (5, 5), 0)

            np_image[:, :, 3] = alpha_smooth

            return Image.fromarray(np_image)
        else:
            logger.warning("Image does not have alpha channel, skipping edge refinement")
            return image
