def filter_detections(detections, min_conf=0.3):
    """
    Filters detections by confidence score.

    Args:
        detections (List[dict]): List of detection dictionaries with a 'conf' key.
        min_conf (float): Minimum confidence threshold.

    Returns:
        List[dict]: Filtered list of detections.
    """
    return [d for d in detections if d.get("conf", 0) >= min_conf]


def format_detections_for_speech(detections):
    """
    Converts detections into readable sentence fragments.

    Args:
        detections (List[dict]): List of detection dictionaries with 'name' and optionally 'position' keys.

    Returns:
        str: Sentence fragment like "A person is on your left, a car is on your right."
    """
    if not detections:
        return "No relevant objects detected."

    phrases = []
    for d in detections:
        name = d.get("name", "object")
        position = d.get("position", "nearby")  # default if position not specified
        phrases.append(f"A {name} is on your {position}")

    return ", ".join(phrases) + "."


parts = []
for d in detections:
    parts.append(f"A {d['name']} is on your {d['position']}")

return ", ".join(parts) + "."
