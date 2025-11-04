from flask import Flask, render_template, request, redirect, url_for, session
from textblob import TextBlob
import random
import json
import os

app = Flask(__name__)
app.secret_key = "replace_this_with_any_secret_for_session"  # change for production
SAVE_FILE = "last_mood.json"

# Expanded emotion groups: each has display emoji and several suggestions (title + optional link)
EMOTIONS = {
    "happy": {
        "emoji": "✨",
        "desc": "Happy",
        "suggestions": [
            {"title": "Happy — Pharrell Williams", "link": "https://www.youtube.com/results?search_query=Happy+Pharrell"},
            {"title": "Good Life — OneRepublic", "link": "https://www.youtube.com/results?search_query=Good+Life+OneRepublic"},
            {"title": "Mood Booster Playlist (YouTube)", "link": "https://www.youtube.com/results?search_query=mood+booster+playlist"}
        ]
    },
    "sad": {
        "emoji": "😢",
        "desc": "Sad",
        "suggestions": [
            {"title": "Someone Like You — Adele", "link": "https://www.youtube.com/results?search_query=Someone+Like+You+Adele"},
            {"title": "Fix You — Coldplay", "link": "https://www.youtube.com/results?search_query=Fix+You+Coldplay"},
            {"title": "Lo-fi Sad Beats", "link": "https://www.youtube.com/results?search_query=lofi+sad+beats"}
        ]
    },
    "calm": {
        "emoji": "🌙",
        "desc": "Calm",
        "suggestions": [
            {"title": "Weightless — Marconi Union", "link": "https://www.youtube.com/results?search_query=Weightless+Marconi+Union"},
            {"title": "Calm Piano Playlist", "link": "https://www.youtube.com/results?search_query=calm+piano+playlist"},
            {"title": "Lo-fi Chillhop", "link": "https://www.youtube.com/results?search_query=lofi+chillhop"}
        ]
    },
    "romantic": {
        "emoji": "💕",
        "desc": "Romantic",
        "suggestions": [
            {"title": "Perfect — Ed Sheeran", "link": "https://www.youtube.com/results?search_query=Perfect+Ed+Sheeran"},
            {"title": "Love Songs Playlist", "link": "https://www.youtube.com/results?search_query=love+songs+playlist"},
            {"title": "Acoustic Love Songs", "link": "https://www.youtube.com/results?search_query=acoustic+love+songs"}
        ]
    },
    "angry": {
        "emoji": "🔥",
        "desc": "Angry",
        "suggestions": [
            {"title": "Killing In The Name — Rage Against The Machine", "link": "https://www.youtube.com/results?search_query=Rage+Against+The+Machine+Killing+in+the+Name"},
            {"title": "Hard Rock Playlist", "link": "https://www.youtube.com/results?search_query=hard+rock+playlist"},
            {"title": "Metal Workout Mix", "link": "https://www.youtube.com/results?search_query=metal+workout+mix"}
        ]
    },
    "stressed": {
        "emoji": "😩",
        "desc": "Stressed",
        "suggestions": [
            {"title": "Calming Breath & Soft Piano", "link": "https://www.youtube.com/results?search_query=calming+breath+music+piano"},
            {"title": "Guided Relaxation Playlist", "link": "https://www.youtube.com/results?search_query=guided+relaxation+music"},
            {"title": "Ambient Chill", "link": "https://www.youtube.com/results?search_query=ambient+chill+music"}
        ]
    },
    "energetic": {
        "emoji": "⚡",
        "desc": "Energetic",
        "suggestions": [
            {"title": "Uptown Funk — Bruno Mars", "link": "https://www.youtube.com/results?search_query=Uptown+Funk+Bruno+Mars"},
            {"title": "Workout Beats Playlist", "link": "https://www.youtube.com/results?search_query=workout+beats+playlist"},
            {"title": "Electronic Energetic Mix", "link": "https://www.youtube.com/results?search_query=electronic+energetic+mix"}
        ]
    },
    "lonely": {
        "emoji": "💜",
        "desc": "Lonely",
        "suggestions": [
            {"title": "Someone You Loved — Lewis Capaldi", "link": "https://www.youtube.com/results?search_query=Someone+You+Loved+Lewis+Capaldi"},
            {"title": "Soothing Indie Ballads", "link": "https://www.youtube.com/results?search_query=soothing+indie+ballads"},
            {"title": "Comforting Acoustic", "link": "https://www.youtube.com/results?search_query=comforting+acoustic+songs"}
        ]
    }
}

# fallback mapping by polarity if no clear keywords
POLARITY_TO_EMOTION = {
    "positive": ["happy", "energetic"],
    "neutral": ["calm"],
    "negative": ["sad", "lonely", "stressed"]
}


def save_last_mood(mood_text, detected):
    data = {"mood_text": mood_text, "detected": detected}
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


def load_last_mood():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def detect_emotion(mood_text):
    """
    Returns a detected emotion key from EMOTIONS or None.
    Strategy:
      1) Keyword-based lookups (quick).
      2) Polarity-based fallback using TextBlob (if available).
    """
    text = mood_text.lower()

    # keyword mapping: look for words that strongly indicate an emotion
    keyword_map = {
        "happy": ["happy", "joy", "excited", "great", "amazing", "blessed", "cheerful", "good"],
        "sad": ["sad", "depressed", "broken", "tear", "unhappy", "miserable"],
        "calm": ["calm", "relaxed", "peace", "chill", "tranquil"],
        "romantic": ["love", "romantic", "crush", "heart"],
        "angry": ["angry", "mad", "furious", "annoyed", "irritated"],
        "stressed": ["stressed", "stress", "anxious", "anxiety", "overwhelmed"],
        "energetic": ["energetic", "hyper", "pumped", "energized"],
        "lonely": ["lonely", "alone", "isolated", "loneliness"]
    }

    for emo, words in keyword_map.items():
        for w in words:
            if w in text:
                return emo

    # fallback: try TextBlob polarity
    try:
        polarity = TextBlob(mood_text).sentiment.polarity
        if polarity > 0.25:
            return random.choice(POLARITY_TO_EMOTION["positive"])
        elif polarity < -0.25:
            # pick sad-like fallback
            return random.choice(POLARITY_TO_EMOTION["negative"])
        else:
            return random.choice(POLARITY_TO_EMOTION["neutral"])
    except Exception:
        # if TextBlob not available or fails, default to neutral
        return "calm"


@app.route("/", methods=["GET", "POST"])
def home():
    suggestion_list = []
    detected = None
    mood_text = ""
    last = load_last_mood()

    if request.method == "POST":
        mood_text = request.form.get("mood", "").strip()
        mood_boost = request.form.get("mood_boost", "no")  # "yes" or "no"

        if not mood_text:
            detected = None
        else:
            detected = detect_emotion(mood_text)  # key into EMOTIONS
            # If user wants to "cheer up" (mood_boost=yes), map negative -> happy/energetic
            if mood_boost == "yes" and detected in ["sad", "stressed", "lonely", "angry"]:
                detected = "happy"  # simple cheerful override
            # prepare randomized set of 3 suggestions
            base_suggestions = EMOTIONS.get(detected, EMOTIONS["calm"])["suggestions"]
            suggestion_list = random.sample(base_suggestions, min(3, len(base_suggestions)))

            # save last mood
            save_last_mood(mood_text, detected)

        # store in session to show immediate results
        session["last_mood"] = {"mood_text": mood_text, "detected": detected}

        return redirect(url_for("home"))

    # GET request: read last submission from session (most recent) or saved file
    session_data = session.get("last_mood")
    if session_data:
        mood_text = session_data.get("mood_text", "")
        detected = session_data.get("detected")
    elif last:
        mood_text = last.get("mood_text", "")
        detected = last.get("detected")

    if detected:
        base_suggestions = EMOTIONS.get(detected, EMOTIONS["calm"])["suggestions"]
        suggestion_list = random.sample(base_suggestions, min(3, len(base_suggestions)))

    return render_template(
        "index.html",
        mood_text=mood_text,
        detected=detected,
        emotions=EMOTIONS,
        suggestions=suggestion_list,
        last=last
    )


if __name__ == "__main__":
    app.run(debug=True)