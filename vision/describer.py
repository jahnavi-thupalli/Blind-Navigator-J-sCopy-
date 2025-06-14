from transformers import pipeline
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", device_map="auto")

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


def describe_scene_tinyllama(detections, frame_width, use_llm=True):
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

    summary_parts = []
    for det in detections:
        label = det["label"]
        x1, _, x2, _ = det["bbox"]
        x_center = (x1 + x2) / 2
        pos = describe_position(x_center, frame_width)
        dist = estimate_distance(x1, x2)
        summary_parts.append(f"{label} {pos} approximately {dist} meters")
    grounded_summary = ", ".join(summary_parts)


    prompt = f"""<|system|>Your job is to assist a blind user as their camera sees with no nonsense just facts . Be concise and speak as if you are guiding them in real time.only return a sentence describing their positions and distances.
    </s><|user|>The following objects were detected in a {frame_width}px wide frame:{grounded_summary}.</s><|assistant|>"""

    response = pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)[0]["generated_text"]
    return response.split("<|assistant|>")[-1].strip()


def input_for_func(results,model = YOLO('yolov8n.pt')):
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls_id = int(box.cls[0].item())
        label = model.names[cls_id]
        detections.append({"label": label, "bbox": [x1, y1, x2, y2]})
    return detections

#Sample test
#detections = input_for_func(results)
#describe_scene_tinyllama(detections, frame_width=640)
