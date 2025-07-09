from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json

# Load Vosk model (point to downloaded folder)
model = Model("vosk-model-small-en-us-0.15")
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def record_and_transcribe_vosk(duration=5, samplerate=16000):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎙️ Listening...")
        rec = KaldiRecognizer(model, samplerate)
        for _ in range(int(duration * samplerate / 8000)):
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
        final_result = json.loads(rec.FinalResult())
        return final_result.get("text", "")


user_input = None
while user_input != "exit":
    user_input = record_and_transcribe_vosk(duration=5).strip()
    print(f"📝 You said: {user_input}")
