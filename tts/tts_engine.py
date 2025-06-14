from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io

def speak_text(text):
    tts = gTTS(text)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_file(fp, format="mp3")
    play(audio)
