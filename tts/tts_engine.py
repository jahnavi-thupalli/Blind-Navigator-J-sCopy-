from gtts import gTTS
import io

def speak_text(text: str) -> io.BytesIO:
    tts = gTTS(text)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp
