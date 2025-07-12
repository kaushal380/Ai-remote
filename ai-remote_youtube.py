import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import numpy as np
import queue
import speech_recognition as sr
from rapidfuzz import fuzz, process
import tempfile
import wave
import os
import time

# ----------------------------------------
# Channel catalogue with YouTube links
# ----------------------------------------
youtube_channel_catalogue = {
    "india tv": "https://www.youtube.com/embed/Xmm3Kr5P1Uw",
    "ntv telugu": "https://www.youtube.com/embed/L0RktSIM980",
    "aaj tak": "https://www.youtube.com/embed/Nq2wYlWFucg",
    "love nature": "https://www.youtube.com/embed/daqB3i9WYIY",
    "disney channel": "https://www.youtube.com/embed/0uUCyGKZm1M"
}

channel_aliases = {
    "ntv": "ntv telugu",
    "disney": "disney channel",
    "india news": "india tv",
    "nature": "love nature",
    "news india": "india tv"
}

all_names = list(youtube_channel_catalogue.keys()) + list(channel_aliases.keys())

# ----------------------------------------
# Fuzzy channel name matching
# ----------------------------------------
def extract_channel_name(user_input):
    user_input = user_input.lower().strip()
    words = user_input.split()
    best_match = None
    best_score = 0

    for size in range(1, 6):
        for i in range(len(words) - size + 1):
            phrase = " ".join(words[i:i + size])
            match, score, _ = process.extractOne(phrase, all_names, scorer=fuzz.token_sort_ratio)
            if score > best_score:
                best_score = score
                best_match = match

    if best_score >= 70:
        canonical = channel_aliases.get(best_match, best_match)
        return canonical, youtube_channel_catalogue.get(canonical)
    return None, None

# ----------------------------------------
# Audio processor to collect audio data
# ----------------------------------------
audio_queue = queue.Queue()
recording = st.session_state.get("recording", False)

class AudioProcessor:
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        audio_queue.put(audio)
        return frame

# ----------------------------------------
# Transcribe numpy audio with SpeechRecognition
# ----------------------------------------
def transcribe_np_audio(np_audio, sample_rate=16000):
    if np_audio is None or len(np_audio) == 0:
        return ""

    if len(np_audio.shape) > 1 and np_audio.shape[1] > 1:
        np_audio = np.mean(np_audio, axis=1).astype(np.int16)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wavfile = f.name
        with wave.open(wavfile, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(np_audio.tobytes())

    recognizer = sr.Recognizer()
    with sr.AudioFile(wavfile) as source:
        audio = recognizer.record(source)
    os.remove(wavfile)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "[Error: Could not reach STT service]"

# ----------------------------------------
# Streamlit App
# ----------------------------------------
st.set_page_config(page_title="YouTube Voice Remote", layout="wide")
st.title("📺 YouTube Voice-Controlled Remote")

# --- Channel Catalogue
st.subheader("📃 Available YouTube Channels")
for ch, url in youtube_channel_catalogue.items():
    st.markdown(f"- **{ch.title()}** → [Watch Live](https://www.youtube.com/watch?v={url.split('/')[-1]})")

# --- Voice Command
st.subheader("🎤 Speak to Play a Channel")

webrtc_ctx = webrtc_streamer(
    key="client-audio",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    audio_frame_callback=AudioProcessor().recv,
    media_stream_constraints={"video": False, "audio": True},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    async_processing=True
)

start_button = st.button("🟢 Start Recording")
stop_button = st.button("🔴 Stop & Transcribe")

if start_button:
    st.session_state.recording = True
    st.info("🎙️ Recording started... speak now!")
    audio_queue.queue.clear()

if stop_button and st.session_state.get("recording", False):
    st.session_state.recording = False
    st.info("⏹️ Recording stopped. Processing...")

    audio_chunks = []
    while not audio_queue.empty():
        audio_chunks.append(audio_queue.get())

    if audio_chunks:
        full_audio = np.concatenate(audio_chunks, axis=0)
        user_input = transcribe_np_audio(full_audio)
        st.write(f"🗣️ You said: `{user_input}`")
        if user_input:
            channel_name, youtube_link = extract_channel_name(user_input)
            if channel_name:
                st.success(f"✅ Opening channel: **{channel_name.title()}**")
                st.video(youtube_link)
            else:
                st.error("❌ Could not recognize the channel. Please try again.")
        else:
            st.warning("⚠️ No speech detected or transcription failed.")
    else:
        st.warning("⚠️ No audio received. Please try again.")

# --- Optional: Text fallback
with st.expander("📝 Prefer typing?"):
    manual_input = st.text_input("Type the channel name")
    if manual_input:
        channel_name, youtube_link = extract_channel_name(manual_input)
        if channel_name:
            st.success(f"✅ Opening channel: **{channel_name.title()}**")
            st.video(youtube_link)
        else:
            st.error("❌ Could not recognize the channel. Please try again.")
