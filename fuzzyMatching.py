
from rapidfuzz import fuzz, process
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import tempfile
import speech_recognition as sr


# Define channel catalogue
channel_catalogue = {
    "star plus": 101,
    "zee tv": 102,
    "colors": 103,
    "sony entertainment television": 104,
    "sun tv": 105,
    "star maa": 106,
    "sun music": 107,
    "sony sab": 108,
    "star vijay": 109,
    "zee kannada": 110,
    "colors kannada": 111,
    "sony ten 1": 112,
    "sony ten 2": 113,
    "sony six": 114,
    "star sports 1": 115,
    "star sports 2": 116,
    "aaj tak": 117,
    "ndtv india": 118,
    "republic bharat": 119,
    "pogo": 120, 
    "maa": 121,
    "disney channel": 122, 
    "nickelodeon": 123,
    "cartoon network": 124,
    "disney junior": 125,
    "disney xd": 126,
    "history tv18": 127,
    "national geographic": 128,
    "discovery channel": 129,
    "animal planet": 130,
    "food food": 131,
    "travel xp": 132,
    "star bharat": 133,
    "zee anmol": 134,
    "sony pal": 135,
    "tv9 bharatvarsh": 136,
    "tv9 telugu": 137,
    "tv9 kannada": 138,
    "tv9 marathi": 139,
    "ntv": 140,
    "etv telugu": 141,
    "etv kannada": 142,
    "maa tv": 143,
    "tv5 news": 144, 
}

# Optional aliases
channel_aliases = {
    "starplus": "star plus",
    "set": "sony entertainment television",
    "sunnext": "sun tv",
    "sun next": "sun tv",
    "starvijay": "star vijay",
    "ten one": "sony ten 1",
    "ten two": "sony ten 2",
    "sports one": "star sports 1",
    "sports two": "star sports 2",
    "bharat": "republic bharat",
    "ndtv": "ndtv india", 
}

all_names = list(channel_catalogue.keys()) + list(channel_aliases.keys())

def extract_channel_name(user_input):
    user_input = user_input.lower().strip()
    words = user_input.split()
    best_match = None
    best_score = 0

    # Generate all n-gram substrings (1 to 5 words)
    for size in range(1, 6):
        for i in range(len(words) - size + 1):
            phrase = " ".join(words[i:i+size])
            match, score, _ = process.extractOne(phrase, all_names, scorer=fuzz.token_sort_ratio)
            if score > best_score:
                best_score = score
                best_match = match

    if best_score >= 70:
        canonical = channel_aliases.get(best_match, best_match)
        return canonical, channel_catalogue[canonical]
    return None, None

# model = whisper.load_model("tiny")

# def record_audio(duration=5, samplerate=16000):
#     print("🎙️ Listening... (speak now)")
#     audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
#     sd.wait()
#     return audio.flatten(), samplerate

# def transcribe_audio(audio, samplerate):
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
#         scipy.io.wavfile.write(tmpfile.name, samplerate, audio)
#         result = model.transcribe(tmpfile.name)
#     return result["text"]

# Test loop
if __name__ == "__main__":
    while True:
        # audio, rate = record_audio(duration=5)
        # user_input = transcribe_audio(audio, rate).strip()
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        user_input = r.recognize_google(audio)
        print(f"📝 You said: {user_input}")
        if not user_input:
            print("❌ No input detected. Please try again.")
            continue
        
        user_input = user_input.strip()
        # user_input = input("\nUser says: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        channel_name, channel_number = extract_channel_name(user_input)
        if channel_name:
            print(f"✅ Opening channel: {channel_name.title()} (Channel #{channel_number})")
        else:
            print("❌ Could not recognize the channel. Please try again.")

