import streamlit as st
import os
import sys
from yolomodel.detector import detect_on_image
from vision.describer import prepare_detections, describe_scene
from tts.tts_engine import speak_text
from ultralytics import YOLO

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Blind Navigator AI", layout="centered")

# UI Header
st.title("Blind Navigator AI")
st.markdown("---")

model = YOLO("yolov8n.pt")

def get_assets(extensions):
    assets = []
    if os.path.exists("assets"):
        for file in os.listdir("assets"):
            if file.lower().endswith(tuple(extensions)):
                assets.append(file)
    return assets

tab1, tab2 = st.tabs(["Upload Image", "Upload Video"])

with tab1:
    images = get_assets(["jpg", "jpeg", "png"])
    if images:
        selected_image = st.selectbox("Choose an image:", images)
        if selected_image and st.button("Describe Image"):
            image_path = os.path.join("assets", selected_image)
            results = detect_on_image(image_path)
            detections = prepare_detections(results, frame_width=640, model=model)
            description = describe_scene(detections)
            st.image(image_path, caption="Processed Image", use_column_width=True)
            st.success("Image description generated successfully!")
            st.info(description)
            speak_text(description)
