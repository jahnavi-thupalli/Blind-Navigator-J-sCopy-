import streamlit as st
import os
from yolomodel.detector import detect_on_image, detect_on_video
from vision.describer import input_for_func, describe_scene_tinyllama
from tts.tts_engine import speak_text
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

# Get files from assets folder
def get_assets(extensions):
    assets = []
    if os.path.exists("assets"):
        for file in os.listdir("assets"):
            if file.split('.')[-1].lower() in extensions:
                assets.append(file)
    return assets

# Main UI
st.markdown("""
<h1 style="color: #ff7f00 !important; font-family: 'Marker Felt', cursive !important; font-weight: 700 !important; font-size: 3rem !important; text-align: center !important; margin-bottom: 0.5rem !important; letter-spacing: 0.05em !important; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;">Blind Navigator AI</h1>
""", unsafe_allow_html=True)
st.markdown("---")

# Create tabs with custom styling
tab1, tab2 = st.tabs(["Upload Image", "Upload Video"])

with tab1:
    images = get_assets(["jpg", "jpeg", "png"])
    if images:
        selected_image = st.selectbox("Choose an image:", images, index=None)
        if selected_image:
            st.image(f"assets/{selected_image}", width=300)
            if st.button("Describe Image"):
                try:
                    image_path = os.path.join("assets", selected_image)
                    results = detect_on_image(image_path)
                    detections = input_for_func(results)
                    description = describe_scene_tinyllama(detections, frame_width=640)
                    st.success("Image description generated successfully!")
                    st.info(description)
                    speak_text(description)
                except Exception as e:
                    st.error(f"Error processing image: {e}")
    else:
        st.warning("No images found in assets folder.")

# VIDEO TAB
with tab2:
    videos = get_assets(["mp4", "mov", "avi"])
    if videos:
        selected_video = st.selectbox("Choose a video:", videos, index=None)
        if selected_video:
            st.video(f"assets/{selected_video}")
            if st.button("Describe Video"):
                try:
                    video_path = os.path.join("assets", selected_video)
                    results = detect_on_video(video_path)
                    detections = input_for_func(results)
                    description = describe_scene_tinyllama(detections, frame_width=640)
                    st.success("Video description generated successfully!")
                    st.info(description)
                    speak_text(description)
                except Exception as e:
                    st.error(f"Error processing video: {e}")
    else:
        st.warning("No videos found in assets folder.")
