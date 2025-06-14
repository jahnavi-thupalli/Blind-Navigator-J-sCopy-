from ultralytics import YOLO
import numpy as np

class ObjectDetector:
    def __init__(self, model_path: str = "yolov8n.pt", target_classes: list = None, conf_threshold: float = 0.3):
        self.model = YOLO(model_path)
        self.target_classes = target_classes
        self.conf_threshold = conf_threshold


def detect_objects(self, frame):
    results = self.model.predict(frame, conf=self.conf_threshold, verbose=False)[0]

    detections = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        name = self.model.names[cls_id]

        if self.target_classes and name not in self.target_classes:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        bbox = (x1, y1, x2, y2)
        center_x = (x1 + x2) // 2

        # Basic spatial classification
        width = frame.shape[1]
        if center_x < width / 3:
            position = "left"
        elif center_x < 2 * width / 3:
            position = "center"
        else:
            position = "right"

        detections.append({
            "name": name,
            "conf": round(conf, 2),
            "bbox": bbox,
            "position": position
        })

    return detections
