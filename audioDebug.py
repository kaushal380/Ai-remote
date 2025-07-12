import streamlit as st
from audiorecorder import audiorecorder  # pip install streamlit-audiorecorder
import speech_recognition as sr
import tempfile
import os

st.set_page_config(page_title="Audio Transcription Test", layout="centered")
st.title("🎙️ Browser Mic Transcription Demo")

st.write("Click the button below, speak into your browser’s mic, then wait for the transcription.")

# Record audio via browser component
# Returns a pydub.AudioSegment
audio_segment = audiorecorder(
    label="🎤 Click to start/stop recording",
    text="Recording... Click to stop",
    key="rec"
)

if audio_segment:
    st.success("✅ Audio recorded. Transcribing...")
    # Save to temp WAV using export
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp_path = tmp.name
    audio_segment.export(tmp_path, format="wav")

    # Transcribe with SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio_data = recognizer.record(source)
    os.remove(tmp_path)

    try:
        text = recognizer.recognize_google(audio_data)
        st.write(f"📝 Transcription: **{text}**")
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio.")
    except sr.RequestError:
        st.error("⚠️ STT service unavailable.")

