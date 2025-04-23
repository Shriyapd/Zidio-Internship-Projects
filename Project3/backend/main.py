from emotion_detection import EmotionDetector
from task_recommender import TaskRecommender
from mood_tracker import MoodTracker
from notifications import Notifications

def main():
    employee_id = 1
    detector = EmotionDetector()
    recommender = TaskRecommender()
    tracker = MoodTracker()
    notifier = Notifications()

    print("Choose Input Method:")
    print("1. Text")
    print("2. Voice")
    print("3. Webcam")
    choice = input("Enter choice: ")

    if choice == '1':
        text = input("Enter your mood as text: ")
        mood = detector.detect_from_text(text)
    elif choice == '2':
        mood = detector.detect_from_speech()
    elif choice == '3':
        mood = detector.detect_from_webcam()
    else:
        print("Invalid choice.")
        return

    print(f"Detected mood: {mood}")
    tracker.record_mood(employee_id, mood)
    recommendation = recommender.recommend_task(mood)
    print(f"Recommended Task: {recommendation}")
    notifier.send_alert(employee_id, mood)

if __name__ == "__main__":
    main()
