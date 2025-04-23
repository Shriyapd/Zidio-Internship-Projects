import cv2
import speech_recognition as sr
from deepface import DeepFace
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import defaultdict

class EmotionDetector:
    def __init__(self):
        self.text_analyzer = SentimentIntensityAnalyzer()
        self.mood_history = defaultdict(int)

    def normalize_mood(self, mood):
        mood_map = {
            "happy": "Happy",
            "sad": "Sad",
            "angry": "Angry",
            "disgust": "Stressed",
            "fear": "Stressed",
            "surprise": "Neutral",
            "neutral": "Neutral"
        }
        return mood_map.get(mood.lower(), "Neutral")

    def detect_from_text(self, text):
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        compound_score = scores['compound']
        print("[Text] Compound Score:", compound_score)

        text_lower = text.lower()
        if any(word in text_lower for word in ["happy", "joy", "great", "excited", "awesome", "ice cream"]):
            mood = "Happy"
        elif any(word in text_lower for word in ["sad", "depressed", "down", "upset", "unhappy"]):
            mood = "Sad"
        elif any(word in text_lower for word in ["angry", "mad", "furious", "annoyed", "pissed"]):
            mood = "Angry"
        elif any(word in text_lower for word in ["stress", "stressed", "tension", "anxiety", "nervous"]):
            mood = "Stressed"
        else:
            if compound_score >= 0.5:
                mood = "Happy"
            elif compound_score <= -0.5:
                mood = "Angry"
            elif -0.5 < compound_score < 0:
                mood = "Sad"
            else:
                mood = "Neutral"

        self.mood_history[mood] += 1  # Update mood history here
        return mood

    def detect_from_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                text = recognizer.recognize_google(audio)
                print(f"[Speech] Recognized Text: {text}")
                mood = self.detect_from_text(text)
                self.mood_history[mood] += 1  # Update mood history here
                return mood
            except sr.WaitTimeoutError:
                print("[Speech] Timeout: No speech detected.")
                return "Neutral"
            except sr.UnknownValueError:
                print("[Speech] Could not understand audio.")
                return "Neutral"
            except sr.RequestError as e:
                print(f"[Speech] API error: {e}")
                return "Neutral"

    def detect_from_webcam(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Error: Webcam not accessible")
            return "Neutral"

        emotion_scores = defaultdict(float)
        frame_count = 0

        print("[Webcam Detection] Capturing 15 frames...")

        for _ in range(50):
            ret, frame = cap.read()
            if not ret:
                continue

            try:
                results = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)[0]
                dominant_emotion = results['dominant_emotion']
                print(f"[Frame {frame_count + 1}] Detected Emotion: {dominant_emotion}")
                emotion_scores[dominant_emotion] += 1
                frame_count += 1

                cv2.putText(frame, f"Emotion: {dominant_emotion}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            except Exception as e:
                print("[Frame Error]", e)

            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if not emotion_scores:
            print("[Webcam Detection] No emotions detected.")
            return "Neutral"

        top_emotion = max(emotion_scores, key=emotion_scores.get)
        mood = self.normalize_mood(top_emotion)

        print(f"[Webcam Detection] Aggregated Emotion Scores: {dict(emotion_scores)}")
        print(f"[Webcam Detection] Top Emotion: {top_emotion} → {mood}")

        self.mood_history[mood] += 1  # Update mood history here
        return mood

    def get_mood_history(self):
        return dict(self.mood_history)
