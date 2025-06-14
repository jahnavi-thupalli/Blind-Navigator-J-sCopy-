from transformers import pipeline
from ultralytics import YOLO

# Load a light language model suitable for Streamlit Cloud
pipe = pipeline("text2text-generation", model="google/flan-t5-large")

# Load YOLO only once (optional - you can move this to main app)
model = YOLO('yolov8n.pt')

def describe_position(x_center, frame_width):
    if x_center < frame_width / 3:
        return "on your left"
    elif x_center < 2 * frame_width / 3:
        return "ahead"
    else:
        return "on your right"

def estimate_distance(x1, x2):
    width_pixels = x2 - x1
    return round(2.0 * (1 / (width_pixels / 100)), 1)

def input_for_func(results, model=model):
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls_id = int(box.cls[0].item())
        label = model.names[cls_id]
        detections.append({"label": label, "bbox": [x1, y1, x2, y2]})
    return detections

def describe_scene(detections, frame_width, use_llm=True):
    if not detections:
        return "I couldn't detect anything in your surroundings."

    if not use_llm:
        description = []
        for det in detections:
            label = det["label"]
            x1, _, x2, _ = det["bbox"]
            x_center = (x1 + x2) / 2
            position = describe_position(x_center, frame_width)
            distance = estimate_distance(x1, x2)
            description.append(f"{label} {position}, about {distance} meters away")
        return ". ".join(description)

    # Prepare summary input
    summary_parts = []
    for det in detections:
        label = det["label"]
        x1, _, x2, _ = det["bbox"]
        x_center = (x1 + x2) / 2
        pos = describe_position(x_center, frame_width)
        dist = estimate_distance(x1, x2)
        summary_parts.append(f"{label} {pos} approximately {dist} meters")
    grounded_summary = ", ".join(summary_parts)

    prompt = f"Describe to a blind user what is seen: {grounded_summary}. Respond concisely and clearly."

    response = pipe(prompt, max_new_tokens=100)[0]["generated_text"]
    return response.strip()
