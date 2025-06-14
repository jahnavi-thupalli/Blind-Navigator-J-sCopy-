#!pip install ultralytics opencv-python-headless --quiet
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from ultralytics import YOLO
#from google.colab import files

model = YOLO('yolov8n.pt')

def detect_on_image(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model(img_rgb)[0]

    class_counts = {}

    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_rgb, f'{label} {conf:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        class_counts[label] = class_counts.get(label, 0) + 1



    # Generate description
    description = [f"{label}: {count}" for label, count in class_counts.items()]

    return description


def detect_on_video(video_path, output_path='output.mp4'):
    cap = cv2.VideoCapture(video_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_num = 0
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

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            class_counts[label] = class_counts.get(label, 0) + 1

        out.write(frame)
        frame_num += 1
        if frame_num % 10 == 0:
            print(f"Processed {frame_num} frames...")

    cap.release()
    out.release()


    # Generate description
    description = [f"{label}: {count}" for label, count in class_counts.items()]
    return description

