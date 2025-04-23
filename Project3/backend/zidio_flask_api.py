from flask import Flask, request, jsonify
from flask_cors import CORS
from emotion_detection import EmotionDetector

app = Flask(__name__)
CORS(app)

detector = EmotionDetector()

task_recommendations = {
    "Happy": ["Organize your workspace", "Learn something new", "Help a teammate"],
    "Sad": ["Take a short walk", "Listen to music", "Write down your feelings"],
    "Stressed": ["Do breathing exercises", "Take a 5-minute break", "Prioritize urgent tasks"],
    "Angry": ["Take deep breaths", "Go for a quick walk", "Avoid responding immediately"],
    "Neutral": ["Review your to-do list", "Plan your next day", "Take a coffee break"]
}

@app.route('/analyze', methods=['POST'])
def analyze_mood():
    data = request.json
    mood = detector.detect_from_text(data.get('mood', ''))
    recommendations = task_recommendations.get(mood, ["Stay positive!", "Focus on your goals"])
    mood_counts = detector.get_mood_history()
    return jsonify({'mood': mood, 'recommendations': recommendations, 'history': mood_counts})

@app.route('/detect-speech', methods=['GET'])
def detect_speech():
    mood = detector.detect_from_speech()
    recommendations = task_recommendations.get(mood, ["Stay positive!", "Focus on your goals"])
    mood_counts = detector.get_mood_history()
    return jsonify({'mood': mood, 'recommendations': recommendations, 'history': mood_counts})

@app.route('/detect-webcam', methods=['GET'])
def detect_webcam():
    try:
        result = detector.detect_from_webcam()
        print(f"[API] Webcam detection result: {result}")
        mood = result if isinstance(result, str) else "Neutral"

        recommendations = task_recommendations.get(mood, ["Stay positive!", "Focus on your goals"])
        mood_counts = detector.get_mood_history()

        print(f"[API] Mood counts: {mood_counts}")
        return jsonify({'mood': mood, 'recommendations': recommendations, 'history': mood_counts})
    except Exception as e:
        print(f"[API] Error: {e}")
        return jsonify({"error": str(e)})

@app.route('/history', methods=['GET'])
def get_history():
    mood_counts = detector.get_mood_history()
    return jsonify({'history': mood_counts})

if __name__ == '__main__':
    app.run(debug=True)
