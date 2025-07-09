import streamlit as st
import pandas as pd
import speech_recognition as sr
from rapidfuzz import fuzz, process

# ----------------------------------------
# Channel Catalogue & Aliases
# ----------------------------------------
channel_catalogue = {
    "star plus": 101, "zee tv": 102, "colors": 103, "sony entertainment television": 104,
    "sun tv": 105, "star maa": 106, "sun music": 107, "sony sab": 108,
    "star vijay": 109, "zee kannada": 110, "colors kannada": 111, "sony ten 1": 112,
    "sony ten 2": 113, "sony six": 114, "star sports 1": 115, "star sports 2": 116,
    "aaj tak": 117, "ndtv india": 118, "republic bharat": 119, "pogo": 120,
    "maa": 121, "disney channel": 122, "nickelodeon": 123, "cartoon network": 124,
    "disney junior": 125, "disney xd": 126, "history tv18": 127, "national geographic": 128,
    "discovery channel": 129, "animal planet": 130, "food food": 131, "travel xp": 132,
    "star bharat": 133, "zee anmol": 134, "sony pal": 135, "tv9 bharatvarsh": 136,
    "tv9 telugu": 137, "tv9 kannada": 138, "tv9 marathi": 139, "ntv": 140,
    "etv telugu": 141, "etv kannada": 142, "maa tv": 143, "tv5 news": 144
}

channel_aliases = {
    "starplus": "star plus", "set": "sony entertainment television", "sunnext": "sun tv",
    "sun next": "sun tv", "starvijay": "star vijay", "ten one": "sony ten 1",
    "ten two": "sony ten 2", "sports one": "star sports 1", "sports two": "star sports 2",
    "bharat": "republic bharat", "ndtv": "ndtv india"
}

# ----------------------------------------
# Functions
# ----------------------------------------
def extract_channel_name(user_input):
    user_input = user_input.lower().strip()
    words = user_input.split()
    best_match = None
    best_score = 0
    all_names = list(channel_catalogue.keys()) + list(channel_aliases.keys())

    for size in range(1, 6):
        for i in range(len(words) - size + 1):
            phrase = " ".join(words[i:i+size])
            match, score, _ = process.extractOne(phrase, all_names, scorer=fuzz.token_sort_ratio)
            if score > best_score:
                best_score = score
                best_match = match

    if best_score >= 70:
        canonical = channel_aliases.get(best_match, best_match)
        return canonical, channel_catalogue.get(canonical)
    return None, None


def transcribe_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        info_placeholder = st.empty()
        info_placeholder.info("🎙️ Listening... Please speak now.")
        audio = recognizer.listen(source)
        info_placeholder.empty()
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "[Error: Could not reach STT service]"


# ----------------------------------------
# Streamlit UI
# ----------------------------------------
st.set_page_config(page_title="AI Remote", layout="wide")
st.title("📺 AI Voice-Controlled Remote")

# --- Column Layout
left, right = st.columns([2, 1])

# --- Left: Channel Catalogue
with left:
    st.subheader("📃 Channel Catalogue")
    df = pd.DataFrame([{"Channel Name": name.title(), "Number": num} for name, num in channel_catalogue.items()])
    st.dataframe(df.sort_values(by="Number"), use_container_width=True)

# --- Right: Alias Editor
with right:
    st.subheader("✏️ Channel Aliases")
    alias_df = pd.DataFrame([{"Alias": k, "Maps to Channel": v.title()} for k, v in channel_aliases.items()])
    edited_alias_df = st.data_editor(alias_df, use_container_width=True, num_rows="dynamic")
    # Update aliases from edited table
    channel_aliases.clear()
    for _, row in edited_alias_df.iterrows():
        if row["Alias"] and row["Maps to Channel"].lower() in channel_catalogue:
            channel_aliases[row["Alias"].strip().lower()] = row["Maps to Channel"].strip().lower()

# --- Record Button
if st.button("🎤 Record Voice Command"):
    user_input = transcribe_from_mic()
    st.write(f"🗣️ You said: `{user_input}`")
    if user_input:
        channel_name, channel_number = extract_channel_name(user_input)
        if channel_name:
            st.success(f"✅ Opening channel: **{channel_name.title()}** (Channel #{channel_number})")
        else:
            st.error("❌ Could not recognize the channel. Please try again.")
    else:
        st.warning("⚠️ No speech detected or transcription failed.")
