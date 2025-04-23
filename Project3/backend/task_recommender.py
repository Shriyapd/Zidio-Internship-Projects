class TaskRecommender:
    def recommend_task(self, mood):
        tasks = {
            'happy': 'Work on creative projects',
            'neutral': 'Complete routine tasks',
            'stressed': 'Take a break or work on light tasks',
            'angry': 'Do breathing exercises or talk to someone',
            'sad': 'Take a short walk or listen to music'
        }
        return tasks.get(mood.lower(), 'No recommendation available')
