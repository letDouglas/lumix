import cv2
import numpy as np

def add_stretched_shadow_same_size(image_path, output_path, stretch=30, opacity=100):
    # Load image with alpha
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img.shape[2] != 4:
        raise ValueError("Image must have an alpha channel.")

    h, w = img.shape[:2]
    alpha = img[:, :, 3]

    # Create shadow layer (transparent RGBA)
    shadow_layer = np.zeros((h, w, 4), dtype=np.uint8)

    for x in range(w):
        column = alpha[:, x]
        non_transparent_indices = np.where(column > 0)[0]
        if non_transparent_indices.size == 0:
            continue
        bottom_y = non_transparent_indices[-1]

        # Define shadow stretch range
        y1 = bottom_y
        y2 = min(bottom_y + stretch, h)

        # Vertical black semi-transparent line
        for y in range(y1, y2):
            fade = 1 - (y - y1) / stretch  # linear fade
            shadow_layer[y, x] = [0, 0, 0, int(opacity * fade)]

    # Combine shadow and original image
    combined = img.copy()
    # Alpha blending
    alpha_shadow = shadow_layer[:, :, 3:] / 255.0
    for c in range(3):  # RGB channels
        combined[:, :, c] = (1 - alpha_shadow[:, :, 0]) * combined[:, :, c] + alpha_shadow[:, :, 0] * shadow_layer[:, :, c]

    # Update alpha channel
    combined[:, :, 3] = np.clip(combined[:, :, 3] + shadow_layer[:, :, 3], 0, 255)

    # Save result
    cv2.imwrite(output_path, combined)

# Example usage
add_stretched_shadow_same_size(r"C:\Users\NOAHDECASTRO\Desktop\auto.png", r"C:\Users\NOAHDECASTRO\Desktop\auto_shadow.png", stretch=40)
