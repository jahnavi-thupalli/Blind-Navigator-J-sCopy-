# Blind Navigator AI

**Blind Navigator AI** is a web-based assistive tool that helps visually impaired users understand their surroundings using only their device’s camera and audio output. It uses computer vision (YOLOv8) and text-to-speech to describe objects nearby in plain language.

---

## Problem Statement

Navigating unfamiliar or crowded places can be difficult and even dangerous for people who are blind or visually impaired. Traditional aids like canes and guide dogs provide limited feedback about the environment.

This app uses accessible AI tools to detect objects and narrate surroundings through the user’s phone or laptop — with no extra hardware required.

---

## Features

- Object detection
- Image and Video upload for offline analysis
- Natural spoken descriptions using text-to-speech
- Spatial awareness (“on your left”, “ahead”)
- Browser-based and cross-platform (no installation required)

---

## Tech Stack

| Component        | Technology                             |
|------------------|----------------------------------------|
| Frontend         | Streamlit                              |
| Webcam Streaming | streamlit-webrtc                       |
| Object Detection | YOLOv8 (Ultralytics), OpenCV           |
| Text-to-Speech   | gTTS (online) or pyttsx3 (offline)     |
| Frame Handling   | OpenCV, NumPy                          |
| Deployment       | Streamlit Cloud / Render / Railway     |

---

## Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed.

Install the required libraries:

```bash
pip install -r requirements.txt

