import cv2
import numpy as np
import sys
sys.path.append("yolov10")  # Add the repo to Python path

from ultralytics import YOLO

# Load model and image
model = YOLO("yolov10n.pt")  # from local file
image = cv2.imread("input.jpg")

# Run detection
results = model(image)[0]

for box in results.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
    roi = image[y1:y2, x1:x2]

    # Basic preprocessing
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours (approximate shape)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw box and shape
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    for cnt in contours:
        cnt[:, 0, 0] += x1
        cnt[:, 0, 1] += y1
        cv2.drawContours(image, [cnt], -1, (0, 0, 255), 2)

# Show final output
cv2.imshow("YOLOv10 + Contours", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
