import openai
import os

# Load OpenAI key securely (set this in Streamlit secrets or env)
openai.api_key = os.getenv("OPENAI_API_KEY", None)

def describe_position(x_center, frame_width):
    if x_center < frame_width / 3:
        return "on your left"
    elif x_center < 2 * frame_width / 3:
        return "ahead"
    else:
        return "on your right"

def estimate_distance(x1, x2):
    width_pixels = x2 - x1
    if width_pixels <= 0:
        return "unknown"
    return round(2.0 * (1 / (width_pixels / 100)), 1)  # approximate distance

def prepare_detections(results, frame_width, model):
    """
    Converts YOLO results into structured data for description.
    """
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls_id = int(box.cls[0].item())
        label = model.names[cls_id]
        x_center = (x1 + x2) / 2
        pos = describe_position(x_center, frame_width)
        dist = estimate_distance(x1, x2)
        detections.append(f"{label} {pos}, approx {dist} meters")
    return detections

def describe_scene(detections):
    """
    Uses OpenAI GPT to summarize scene detections.
    """
    if not detections:
        return "I couldn't detect anything around you."

    prompt = (
        "You are guiding a blind person. Based on the following observations, "
        "generate a clear and concise sentence describing their surroundings:\n\n"
        + "\n".join(detections)
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Failed to generate description: {e}"
