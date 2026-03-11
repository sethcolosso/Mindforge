from ..models import Exercise, WorkoutSession, Profile, ExerciseOpenEvent
from django.contrib.auth.models import User
from typing import List, Dict
from datetime import datetime, timedelta


class ExerciseService:
    """Layer 1: Internal business logic for exercises"""

    @staticmethod
    def get_recommended_exercises(user: User) -> List[Exercise]:
        """Get personalized exercise recommendations based on user profile and history"""
        profile = user.profile

        # Get recent sessions to avoid repetition
        recent_sessions = WorkoutSession.objects.filter(
            user=user,
            completed_at__gte=datetime.now() - timedelta(days=3)
        ).values_list('exercise_id', flat=True)

        # Base query excluding recent exercises
        exercises = Exercise.objects.exclude(id__in=recent_sessions)

        # Personalize based on goals
        if hasattr(profile, 'goals') and profile.goals:
            goal_categories = []
            for goal in profile.goals:
                if 'focus' in goal.lower():
                    goal_categories.append('focus')
                elif 'anxiety' in goal.lower() or 'stress' in goal.lower():
                    goal_categories.append('anxiety')
                elif 'confidence' in goal.lower():
                    goal_categories.append('confidence')

            if goal_categories:
                exercises = exercises.filter(category__in=goal_categories)

        return list(exercises[:3])

    @staticmethod
    def log_open_event(user: User, exercise_id: int) -> ExerciseOpenEvent:
        """Log that a user opened an exercise."""
        exercise = Exercise.objects.get(id=exercise_id)
        return ExerciseOpenEvent.objects.create(
            user=user,
            exercise=exercise,
        )

    @staticmethod
    def log_session(user: User, exercise_id: int, duration: int = None, notes: str = "") -> WorkoutSession:
        """Log a completed exercise session"""
        exercise = Exercise.objects.get(id=exercise_id)
        return WorkoutSession.objects.create(
            user=user,
            exercise=exercise,
            duration_seconds=duration,
            notes=notes
        )

    @staticmethod
    def get_user_stats(user: User) -> Dict:
        """Get exercise statistics for the user"""
        today = datetime.now().date()

        # Today's exercises
        today_count = WorkoutSession.objects.filter(
            user=user,
            completed_at__date=today
        ).count()

        opens_today = ExerciseOpenEvent.objects.filter(
            user=user,
            opened_at__date=today,
        ).count()

        # Streak calculation
        streak = ExerciseService._calculate_streak(user)

        return {
            'exercises_today': today_count,
            'exercise_opens_today': opens_today,
            'exercise_activity_today': today_count + opens_today,
            'streak_days': streak,
            'total_sessions': WorkoutSession.objects.filter(user=user).count(),
            'total_exercise_opens': ExerciseOpenEvent.objects.filter(user=user).count(),
        }

    @staticmethod
    def _calculate_streak(user: User) -> int:
        """Calculate current daily streak"""
        streak = 0
        current_date = datetime.now().date()

        while True:
            has_session = WorkoutSession.objects.filter(
                user=user,
                completed_at__date=current_date
            ).exists()

            has_open = ExerciseOpenEvent.objects.filter(
                user=user,
                opened_at__date=current_date
            ).exists()

            if not (has_session or has_open):
                break

            streak += 1
            current_date -= timedelta(days=1)

        return streak
