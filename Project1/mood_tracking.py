from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Function to detect sentiment
def detect_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Happy"
    elif polarity < 0:
        return "Stressed"
    else:
        return "Neutral"

# Function to get task recommendations
def recommend_task(mood):
    tasks = {
        "Happy": "You should work on a creative task like brainstorming new ideas or reviewing positive feedback.",
        "Stressed": "Consider taking a break or working on a low-stress task such as organizing emails or cleaning your workspace.",
        "Neutral": "You could work on regular tasks like responding to emails or completing daily reports."
    }
    return tasks.get(mood, "Relax and take a moment to assess your day.")

# Function to save mood data to SQLite database
def save_mood_to_db(mood, timestamp):
    conn = sqlite3.connect('mood_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mood_history (mood TEXT, timestamp TEXT)''')
    cursor.execute('''INSERT INTO mood_history (mood, timestamp) VALUES (?, ?)''', (mood, timestamp))
    conn.commit()
    conn.close()

# Function to fetch historical mood trends
def get_mood_history():
    conn = sqlite3.connect('mood_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM mood_history ORDER BY timestamp DESC LIMIT 5''')
    moods = cursor.fetchall()
    conn.close()
    return moods

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.form['user_input']
    sentiment = detect_sentiment(user_input)
    task = recommend_task(sentiment)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    save_mood_to_db(sentiment, timestamp)
    
    return jsonify({
        'mood': sentiment,
        'task': task,
        'timestamp': timestamp
    })

@app.route('/history')
def history():
    moods = get_mood_history()
    return jsonify(moods)

if __name__ == "__main__":
    app.run(debug=True)