import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # Make sure this file exists in your root directory

def detect_on_image(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model(img_rgb)[0]
    return results

def detect_on_video(video_path, output_path='output.mp4'):
    cap = cv2.VideoCapture(video_path)
    width, height = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    class_counts = {}
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            class_counts[label] = class_counts.get(label, 0) + 1

        out.write(frame)

    cap.release()
    out.release()
    return [f"{label}: {count}" for label, count in class_counts.items()]
