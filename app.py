from flask import Flask, render_template, request, jsonify
from rapidfuzz import fuzz, process

app = Flask(__name__)

youtube_channel_catalogue = {
    "india tv": "https://www.youtube.com/embed/Xmm3Kr5P1Uw?autoplay=1",
    "ntv telugu": "https://www.youtube.com/embed/L0RktSIM980?autoplay=1",
    "aaj tak": "https://www.youtube.com/embed/Nq2wYlWFucg?autoplay=1",
    "love nature": "https://www.youtube.com/embed/daqB3i9WYIY?autoplay=1",
    "disney channel": "https://www.youtube.com/embed/0uUCyGKZm1M?autoplay=1",
    "india today": "https://www.youtube.com/embed/hLE6eNJ5N-c?autoplay=1"
}

channel_aliases = {
    "ntv": "ntv telugu",
    "disney": "disney channel",
    "india news": "india tv",
    "nature": "love nature",
    "news india": "india tv",
    "today": "india today",
    "indiatoday": "india today"
}


all_names = list(youtube_channel_catalogue) + list(channel_aliases)

def extract_channel_name(text):
    text = text.lower().strip().split()
    best_match, best_score = None, 0
    for size in range(1, 6):
        for i in range(len(text) - size + 1):
            phrase = " ".join(text[i:i+size])
            match, score, _ = process.extractOne(phrase, all_names, scorer=fuzz.token_sort_ratio)
            if score > best_score:
                best_score, best_match = score, match
    if best_score >= 70:
        canon = channel_aliases.get(best_match, best_match)
        return canon, youtube_channel_catalogue[canon]
    return None, None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save_transcript", methods=["POST"])
def save_transcript():
    data = request.get_json() or {}
    transcript = data.get("transcript", "")
    print("Received transcript:", transcript)
    channel, link = extract_channel_name(transcript)
    if link:
        return jsonify({
            "status": "success",
            "transcript": transcript,
            "channel": channel,
            "link": link
        })
    return jsonify({
        "status": "error",
        "message": "No matching channel",
        "transcript": transcript
    }), 404

if __name__ == "__main__":
    # Make sure you run on port 5000 and debug=True so you see errors in console
    app.run(host="0.0.0.0", port=5000)

