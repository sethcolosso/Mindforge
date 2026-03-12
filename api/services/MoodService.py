from django.contrib.auth.models import User
from ..models import MoodEntry
from typing import List, Optional
from django.db.models import Avg, Count
from datetime import datetime, timedelta
from .openai_service import analyze_mood_from_text


class MoodService:
    """Layer 1: Internal business logic for mood operations"""

    POSITIVE_HINTS = ['good', 'great', 'happy', 'calm', 'focused', 'hopeful', 'grateful']
    NEGATIVE_HINTS = ['sad', 'anxious', 'stress', 'overwhelmed', 'angry', 'tired', 'down']

    @staticmethod
    def create_mood_entry(user: User, mood_data: dict) -> MoodEntry:
        """Create a mood entry for a user"""
        return MoodEntry.objects.create(
            user=user,
            mood=mood_data['mood'],
            emoji=mood_data.get('emoji', ''),
            note=mood_data.get('note', '')
        )

    @staticmethod
    def infer_mood(note: str) -> dict:
        """Infer mood from free text using OpenAI with a rule-based fallback."""
        note = (note or '').strip()
        if not note:
            return {
                'mood': 2,
                'confidence': 0.0,
                'reason': 'No note provided',
                'source': 'fallback',
            }

        llm_result = analyze_mood_from_text(note)
        if llm_result:
            return llm_result

        lowered = note.lower()
        positive_hits = sum(1 for hint in MoodService.POSITIVE_HINTS if hint in lowered)
        negative_hits = sum(1 for hint in MoodService.NEGATIVE_HINTS if hint in lowered)

        if positive_hits > negative_hits:
            mood = 3 if positive_hits < 3 else 4
            reason = 'Detected more positive than negative language'
        elif negative_hits > positive_hits:
            mood = 1 if negative_hits < 3 else 0
            reason = 'Detected more negative than positive language'
        else:
            mood = 2
            reason = 'Could not detect a clear positive/negative direction'

        confidence = min(0.85, 0.45 + 0.1 * max(positive_hits, negative_hits))
        return {
            'mood': mood,
            'confidence': round(confidence, 2),
            'reason': reason,
            'source': 'fallback',
        }

    @staticmethod
    def get_user_moods(user: User, limit: Optional[int] = None) -> List[MoodEntry]:
        """Get mood entries for a user"""
        queryset = MoodEntry.objects.filter(user=user).order_by('-created_at')
        if limit:
            queryset = queryset[:limit]
        return list(queryset)

    @staticmethod
    def get_mood_analytics(user: User) -> dict:
        """Calculate mood analytics for dashboard.

        `average` is intentionally based on the last 24 hours so it naturally
        resets each day for the home card.
        """
        now = datetime.now()
        last_30_days = MoodEntry.objects.filter(
            user=user,
            created_at__gte=now - timedelta(days=30)
        )

        if not recent_moods.exists():
            return {'average': 0, 'count': 0, 'trend': 'neutral'}

        stats = recent_moods.aggregate(
            avg_mood=Avg('mood'),
            total_count=Count('id')
        )

        # Calculate trend (last 7 days vs previous 7 days)
        last_week = recent_moods.filter(
            created_at__gte=datetime.now() - timedelta(days=7)
        ).aggregate(avg=Avg('mood'))['avg'] or 0

        prev_week = recent_moods.filter(
            created_at__gte=datetime.now() - timedelta(days=14),
            created_at__lt=datetime.now() - timedelta(days=7)
        ).aggregate(avg=Avg('mood'))['avg'] or 0

        trend = 'improving' if last_week > prev_week else 'declining' if last_week < prev_week else 'stable'

        return {
            'average': round((daily_avg or 0) * 20, 1),  # 24h average as percentage
            'count': daily_count,
            'trend': trend,
            'latest': recent_moods.first().mood if recent_moods.exists() else None
        }
