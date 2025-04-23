import speech_recognition as sr
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon if not already present
nltk.download('vader_lexicon')

# Initialize VADER and SpeechRecognizer
sid = SentimentIntensityAnalyzer()
recognizer = sr.Recognizer()

def detect_emotion_from_speech():
    with sr.Microphone() as source:
        print("🎤 Speak something (Recording will start after a short pause)...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("🔍 Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")

        scores = sid.polarity_scores(text)
        print(f"📊 Sentiment scores: {scores}")

        # Basic emotion classification
        if scores['compound'] >= 0.5:
            mood = "Happy 😀"
        elif scores['compound'] <= -0.5:
            mood = "Angry or Sad 😠😢"
        else:
            mood = "Neutral 😐"

        print(f"🧠 Detected Mood: {mood}")
        return mood

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return "Unknown"
    except sr.RequestError as e:
        print(f"⚠️ Could not request results; {e}")
        return "Error"

# Run detection
if __name__ == "__main__":
    detect_emotion_from_speech()
