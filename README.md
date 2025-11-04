**# 🧠 Mood Matcher  

**Mood Matcher** is a simple Flask web app that analyzes user-entered text and detects their **mood or emotion** using natural language processing.  
It uses the **TextBlob** library for sentiment analysis and presents the result interactively on a web page.

---

## 🚀 Features  

- 🗣️ Analyzes text to determine mood (Positive / Negative / Neutral)  
- ⚙️ Built with lightweight **Flask** backend  
- 💬 Uses **TextBlob** for sentiment analysis  
- 🎨 Simple and clean web interface  
- 📱 Runs locally or deploys easily to any cloud or container platform  

---

## 🧩 Tech Stack  

| Layer | Technology |
|-------|-------------|
| Backend | Flask (Python) |
| NLP | TextBlob |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Localhost / Render / Docker (optional) |

---

## 🛠️ Installation & Setup  

### 1️⃣ Clone this repository  
```bash
git clone https://github.com/yourusername/mood-matcher.git
cd mood-matcher
**
python -m venv venv
source venv/bin/activate       # for Linux/Mac
venv\Scripts\activate          # for Windows
pip install -r requirements.txt
python app.py
Visit 👉 http://127.0.0.1:5000/
 in your browser.
**
```
## 🧠 How It Works
The Mood Matcher app uses a simple Natural Language Processing (NLP) technique to detect how positive, negative, or neutral a sentence feels.

Here’s the step-by-step breakdown:

🧍‍♂️ User Input:
The user types any text in the input box (for example: “I’m feeling great today!”).

⚙️ Request Sent to Flask Backend:
When the user clicks “Analyze”, the input text is sent to the Flask server.

🧮 Text Analysis with TextBlob:
The Flask app uses TextBlob to calculate the sentiment polarity of the text.

A positive polarity (> 0) means the mood is Positive 😊

A neutral polarity (= 0) means the mood is Neutral 😐

A negative polarity (< 0) means the mood is Negative 😞

💡 Result Displayed on Screen:
The detected mood (Positive / Negative / Neutral) is shown to the user instantly on the web page.

## Project Structure
mood_matcher_project/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies (Flask, TextBlob)
├── static/                # CSS, JS, and other assets
├── templates/             # HTML templates (Jinja2)
└── README.md              # Project documentation
## Requirements
Python 3.8+

Flask

TextBlob
pip install -r requirements.txt
