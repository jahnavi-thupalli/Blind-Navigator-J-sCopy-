detections = [
    {"label": "person", "bbox": [80, 120, 160, 300]},
    {"label": "bicycle", "bbox": [400, 100, 520, 280]}
]

frame_width = 640  
PIXELS_PER_METER = 400  

def analyze_object(obj):
    x_min, y_min, x_max, y_max = obj["bbox"]
    x_center = (x_min + x_max) / 2
    bbox_width = x_max - x_min

    if x_center < frame_width / 3:
        pos = "on your left"
    elif x_center < 2 * frame_width / 3:
        pos = "ahead"
    else:
        pos = "on your right"

    # Estimate distance: smaller width = further away
    # Inverse relationship: closer objects have wider boxes
    approx_distance_m = round((1.0 / bbox_width) * 100 * (PIXELS_PER_METER / frame_width), 2)

    return f"a {obj['label']} {pos}, approximately {approx_distance_m} meters away"

# Build spoken summary
spoken_descriptions = [analyze_object(obj) for obj in detections]
scene_summary = " and ".join(spoken_descriptions)

# Build LLM prompt
prompt = f"""<|system|>You are a voice assistant helping a blind user navigate their surroundings.</s>
<|user|>The camera detected: {scene_summary}.
{f"Note: {preference}" if preference else ""}
Respond with one short spoken sentence summarizing this scene in a helpful, friendly tone.</s>
<|assistant|>"""

# Feed to TinyLLaMA or any pipeline
from transformers import pipeline
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")  # or your model
output = pipe(prompt, max_new_tokens=90)[0]['generated_text']

# Extract model response
spoken_response = output.split("<|assistant|>")[-1].strip()
print("🗣️", spoken_response)
