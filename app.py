from yolomodel.detector import ObjectDetector
from yolomodel.utils import format_detections_for_speech

detector = ObjectDetector(target_classes=["person", "car", "bicycle"])

detections = detector.detect_objects(frame) # frame from webcam or video
description = format_detections_for_speech(detections)

print(description) # Output: "A person is on your left, a car is on your center."
