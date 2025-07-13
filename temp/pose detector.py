import cv2
import numpy as np
import math

def get_car_orientation(image_path):
    # Carica l'immagine (mantiene il canale alpha)
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Usa il canale alfa per creare una maschera binaria
    alpha = img[:, :, 3]
    _, mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)

    # Trova i contorni
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("Nessun oggetto trovato")

    # Trova il contorno più grande (l’auto)
    largest_contour = max(contours, key=cv2.contourArea)

    # Fit di un'ellisse per stimare l'orientamento
    if len(largest_contour) < 5:
        raise ValueError("Contorno troppo piccolo per una stima affidabile")

    ellipse = cv2.fitEllipse(largest_contour)
    angle = ellipse[2]  # Angolo in gradi

    # L'angolo va interpretato:
    # - 0°/180° è orizzontale (vista laterale)
    # - 90° è verticale (frontalmente)

    # Calcolo aspect ratio bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)
    aspect_ratio = w / h

    # Logica semplificata
    if 75 <= angle <= 105:
        pose = "Frontale"
    else:
        pose = "Inclinata"

    return {
        "pose": pose,
        "inclinazione_angolo": round(angle, 2),
        "aspect_ratio": round(aspect_ratio, 2)
    }

# Esempio di utilizzo
if __name__ == "__main__":
    image_path = r"C:\Users\NOAHDECASTRO\Desktop\auto.png"
    result = get_car_orientation(image_path)
    print(result)
