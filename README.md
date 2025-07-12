
# 📺 AI Voice-Controlled Remote

A smart, Streamlit-based voice-controlled remote interface that listens to your voice commands and matches them to Indian TV channels. Designed to be low-latency, easily extendable, and user-friendly — perfect for integration with hardware-based remote control systems.

---

## 🚀 Features

- 🎤 **Voice Command Recognition** (Google STT via Microphone)
- 🔍 **Fuzzy Matching** using RapidFuzz to detect channel names and aliases
- 🗂️ **Editable Channel Aliases**: Add or modify alias mappings easily via the GUI
- 📃 **Live Channel Catalogue View**: See the full list of channels and numbers
- 💡 **Error Handling & Suggestions**: Alerts when a match is not found
- 🧠 Designed for offline/local usage — no backend or server required

---

## 📸 Demo
live link: [https://ai-voice-remote.streamlit.app/](https://voice-remote.onrender.com/)

<img width="2524" height="1247" alt="image" src="https://github.com/user-attachments/assets/960ac652-f088-4f86-9f57-5a4a6c92ecd6" />



---

## 🧠 How It Works

1. **User clicks "🎤 Record Voice Command"**
2. The app records audio via microphone using `speech_recognition`
3. Transcribed text is matched to the catalogue or alias list using fuzzy matching
4. If a valid match is found, the app displays the corresponding channel
5. If the command is unclear, the app shows a helpful error message

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ai-remote-streamlit.git
cd ai-remote-streamlit
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, here’s what you need:
```bash
pip install streamlit pandas speechrecognition rapidfuzz
```

---

## ▶️ Running the App

```bash
streamlit run ai_remote_gui.py
```

> Make sure your microphone is enabled and accessible by the app.

---

## ✏️ Editing Aliases

You can create aliases like:

- `starvijay → Star Vijay`
- `sunnext → Sun TV`
- `ndtv → NDTV India`

All aliases must map to a valid channel in the catalogue. The UI will help validate this mapping.

---

## 📚 Project Structure

```plaintext
├── ai_remote_gui.py       # Main Streamlit app
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

---

## 🧩 Future Improvements

- 🌐 Offline STT with Vosk or Whisper Tiny
- 📱 Mobile-friendly layout
- 💾 Alias persistence to JSON
- 🧪 Unit tests and test coverage

---

## 🧑‍💻 Built With

- [Streamlit](https://streamlit.io/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)
- [Pandas](https://pandas.pydata.org/)
- [docker](https://hub.docker.com)

---

## 🙏 Acknowledgements

Special thanks to the open-source libraries that made this possible. Built with ❤️ by Kaushal Sambanna.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
