import streamlit as st
import os
import tempfile
import cv2
from ultralytics import YOLO
from transformers import pipeline
from gtts import gTTS
from pydub import AudioSegment
import io
import torch

# UI Configuration with Dark Theme
st.set_page_config(
    page_title="Blind Navigator AI",
    layout="centered"
)

# Apply Enhanced Dark Theme with Custom Styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&family=Kalam:wght@300;400;700&family=Comfortaa:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables for Color Scheme */
    :root {
        --bg-primary: #1a1a1d;
        --bg-secondary: #25252a;
        --bg-tertiary: #2f2f35;
        --bg-card: #3a3a42;
        --accent-primary: #6366f1;
        --accent-secondary: #8b5cf6;
        --accent-tertiary: #06b6d4;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --border-primary: #334155;
        --border-secondary: #475569;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --gradient-secondary: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Global Styles */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 800px;
        background: var(--bg-secondary);
        border-radius: 16px;
        border: 1px solid var(--border-primary);
        box-shadow: var(--shadow-xl);
        margin: 2rem auto;
    }
    
    /* Headers */
    h1, .stMarkdown h1, div[data-testid="stMarkdownContainer"] h1 {
        color: #ff7f00 !important;
        font-family: 'Marker Felt', cursive !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.05em !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: #ff7f00 !important;
        background-clip: initial !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: var(--gradient-primary);
        margin: 2rem 0;
        opacity: 0.6;
    }
    
    /* Tab Styling */
    .stTabs {
        background: var(--bg-tertiary);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid var(--border-primary);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid var(--border-secondary);
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-card);
        color: var(--text-primary);
        border-color: var(--accent-primary);
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: var(--shadow-md);
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 2rem 1rem;
        background: var(--bg-secondary);
        border-radius: 0 0 12px 12px;
    }
    
    /* Select Box Styling */
    .stSelectbox > div > div {
        background: var(--bg-card);
        border: 1px solid var(--border-primary);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .stSelectbox label {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    /* Button Styling - Exact same as Upload tab */
    .stButton > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        width: 100% !important;
        margin-top: 1rem !important;
        border-color: transparent !important;
    }
    
    .stButton > button:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: white !important;
    }
    
    .stButton > button:active,
    div[data-testid="stButton"] button:active {
        transform: translateY(0) !important;
    }
    
    .stButton > button:disabled,
    div[data-testid="stButton"] button:disabled {
        background: var(--bg-card) !important;
        color: var(--text-muted) !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Image Container */
    .image-container {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-primary);
        text-align: center;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
    }
    
    .image-container img {
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-secondary);
    }
    
    /* Video Container */
    .video-container {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-primary);
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
    }
    
    .video-container video {
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-secondary);
    }
    
    /* Alert Styling */
    .stAlert {
        border-radius: 8px;
        border: none;
        margin: 1rem 0;
    }
    
    .stAlert[data-baseweb="notification"] {
        background: var(--bg-card);
        border: 1px solid var(--border-primary);
    }
    
    /* Success Alert */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: var(--success);
    }
    
    /* Info Alert */
    .stInfo {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: var(--accent-tertiary);
    }
    
    /* Warning Alert */
    .stWarning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: var(--warning);
    }
    
    /* Error Alert */
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: var(--error);
    }
    
    /* Sidebar Styling (if used) */
    .css-1d391kg {
        background: var(--bg-tertiary);
        border-right: 1px solid var(--border-primary);
    }
    
    /* Metric Styling */
    .metric-container {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-primary);
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-tertiary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-secondary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-primary);
    }
    
    /* Animation for loading states */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            margin: 1rem;
            padding: 1rem;
            border-radius: 12px;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# INTEGRATION OF YOUR EXISTING MODULES
# =============================================

# Initialize models (cached for performance)
@st.cache_resource
def load_models():
    """Load YOLO and TinyLlama models - cached to avoid reloading"""
    try:
        # Initialize YOLO model (from your detector.py)
        model = YOLO('yolov8n.pt')
        
        # Initialize TinyLlama pipeline (from your describer.py)
        try:
            pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
                           device_map="auto" if torch.cuda.is_available() else "cpu")
        except Exception as e:
            st.warning(f"TinyLlama model not available: {e}. Using fallback descriptions.")
            pipe = None
        
        return model, pipe
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

# Functions from your existing modules (integrated inline)

# From tts_engine.py - speak_text function
def speak_text_for_streamlit(text):
    """Convert text to speech and return audio bytes for Streamlit"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.getvalue()
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# From describer.py functions
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

def describe_scene_tinyllama(detections, frame_width, pipe, use_llm=True):
    if not detections:
        return "I couldn't detect anything in your surroundings."

    if not use_llm or pipe is None:
        description = []
        for det in detections:
            label = det["label"]
            x1, _, x2, _ = det["bbox"]
            x_center = (x1 + x2) / 2
            position = describe_position(x_center, frame_width)
            distance = estimate_distance(x1, x2)
            description.append(f"{label} {position}, about {distance} meters away")
        return ". ".join(description)

    try:
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
    except Exception as e:
        st.warning(f"LLM generation failed: {e}. Using fallback.")
        return describe_scene_tinyllama(detections, frame_width, pipe, use_llm=False)

def input_for_func(results, model):
    """Convert YOLO results to detection format"""
    detections = []
    if results and results.boxes is not None:
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls_id = int(box.cls[0].item())
            label = model.names[cls_id]
            detections.append({"label": label, "bbox": [x1, y1, x2, y2]})
    return detections

# From detector.py functions
def detect_on_image(model, image_path):
    """Detect objects in image"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None, None
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = model(img_rgb)[0]
        return results, img_rgb.shape[1]
    except Exception as e:
        st.error(f"Error in image detection: {e}")
        return None, None

def detect_on_video(model, video_path, output_path='output.mp4'):
    """Detect objects in video - process first few frames"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None, None
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Process first frame for description
        ret, frame = cap.read()
        if ret:
            results = model(frame)[0]
            cap.release()
            return results, width
        else:
            cap.release()
            return None, None
    except Exception as e:
        st.error(f"Error in video detection: {e}")
        return None, None

# Get files from assets folder
def get_assets(extensions):
    assets = []
    if os.path.exists("assets"):
        for file in os.listdir("assets"):
            if file.split('.')[-1].lower() in extensions:
                assets.append(file)
    return assets

# =============================================
# MAIN UI
# =============================================

# Main UI
st.markdown("""
<h1 style="color: #ff7f00 !important; font-family: 'Marker Felt', cursive !important; font-weight: 700 !important; font-size: 3rem !important; text-align: center !important; margin-bottom: 0.5rem !important; letter-spacing: 0.05em !important; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;">Blind Navigator AI</h1>
""", unsafe_allow_html=True)
st.markdown("---")

# Load models
model, pipe = load_models()
if model is None:
    st.error("❌ Could not load AI models. Please check your installation.")
    st.stop()
else:
    st.success("✅ AI Vision System Loaded Successfully")

# Create tabs with custom styling
tab1, tab2 = st.tabs(["Upload Image", "Upload Video"])

with tab1:
    st.subheader("🖼️ Image Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload an image for object detection and audio description"
    )
    
    # Assets folder selection
    images = get_assets(["jpg", "png", "jpeg"])
    selected_image = None
    if images:
        st.write("Or select from assets folder:")
        selected_image = st.selectbox(
            "Choose an image:",
            [None] + images,
            index=0,
            key="image_select",
            help="Select an image from assets folder"
        )
    
    # Display selected image
    image_to_process = None
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            image_to_process = tmp_file.name
        st.image(uploaded_file, width=300, caption="Uploaded Image")
    elif selected_image:
        image_to_process = f"assets/{selected_image}"
        st.image(image_to_process, width=300, caption="Selected Image")
    
    # Process button
    if image_to_process:
        describe_image_clicked = st.button(
            "🔍 Describe Image",
            disabled=not image_to_process,
            help="Generate audio description of the selected image",
            key="describe_image_btn"
        )
        
        if describe_image_clicked:
            with st.spinner("🤖 AI is analyzing the image..."):
                try:
                    # Run detection using your detector.py logic
                    results, frame_width = detect_on_image(model, image_to_process)
                    
                    if results and frame_width:
                        # Convert to your detection format
                        detections = input_for_func(results, model)
                        
                        # Generate description using your describer.py logic
                        description = describe_scene_tinyllama(detections, frame_width, pipe)
                        
                        # Display results
                        st.success("✅ Analysis Complete!")
                        st.write("**Description:**")
                        st.info(description)
                        
                        # Generate audio using your tts_engine.py logic
                        audio_bytes = speak_text_for_streamlit(description)
                        if audio_bytes:
                            st.audio(audio_bytes, format='audio/mp3')
                        
                        # Show detected objects
                        if detections:
                            st.write("**Detected Objects:**")
                            for i, det in enumerate(detections, 1):
                                st.write(f"{i}. {det['label']}")
                    else:
                        st.warning("No objects detected in the image")
                        
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
                finally:
                    # Clean up temporary file
                    if uploaded_file is not None and os.path.exists(image_to_process):
                        os.unlink(image_to_process)

with tab2:
    st.subheader("🎥 Video Analysis")
    
    # File uploader for video
    uploaded_video = st.file_uploader(
        "Choose a video file", 
        type=['mp4', 'mov', 'avi'],
        help="Upload a video for object detection and audio description"
    )
    
    # Assets folder selection
    videos = get_assets(["mp4", "mov"])
    selected_video = None
    if videos:
        st.write("Or select from assets folder:")
        selected_video = st.selectbox(
            "Choose a video:", 
            [None] + videos,
            index=0,
            key="video_select",
            help="Select a video from assets folder"
        )
    
    # Display selected video
    video_to_process = None
    if uploaded_video is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_video.getvalue())
            video_to_process = tmp_file.name
        st.video(uploaded_video)
    elif selected_video:
        video_to_process = f"assets/{selected_video}"
        st.video(video_to_process)
    
    # Process button
    if video_to_process:
        describe_video_clicked = st.button(
            "🎬 Describe Video",
            disabled=not video_to_process,
            help="Generate audio description of the selected video",
            key="describe_video_btn"
        )
        
        if describe_video_clicked:
            with st.spinner("🤖 AI is analyzing the video..."):
                try:
                    # Run detection on first frame using your detector.py logic
                    results, frame_width = detect_on_video(model, video_to_process)
                    
                    if results and frame_width:
                        # Convert to your detection format
                        detections = input_for_func(results, model)
                        
                        # Generate description using your describer.py logic
                        description = describe_scene_tinyllama(detections, frame_width, pipe)
                        
                        # Display results
                        st.success("✅ Video Analysis Complete!")
                        st.write("**Scene Description:**")
                        st.info(description)
                        
                        # Generate audio using your tts_engine.py logic
                        audio_bytes = speak_text_for_streamlit(description)
                        if audio_bytes:
                            st.audio(audio_bytes, format='audio/mp3')
                        
                        # Show detected objects
                        if detections:
                            st.write("**Detected Objects:**")
                            for i, det in enumerate(detections, 1):
                                st.write(f"{i}. {det['label']}")
                    else:
                        st.warning("No objects detected in the video")
                        
                except Exception as e:
                    st.error(f"Error processing video: {str(e)}")
                finally:
                    # Clean up temporary file
                    if uploaded_video is not None and os.path.exists(video_to_process):
                        os.unlink(video_to_process)
