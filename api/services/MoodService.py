from django.contrib.auth.models import User
from ..models import MoodEntry
from typing import List, Optional
from django.db.models import Avg, Count
from datetime import datetime, timedelta

class MoodService:
    """Layer 1: Internal business logic for mood operations"""
    
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
    def get_user_moods(user: User, limit: Optional[int] = None) -> List[MoodEntry]:
        """Get mood entries for a user"""
        queryset = MoodEntry.objects.filter(user=user).order_by('-created_at')
        if limit:
            queryset = queryset[:limit]
        return list(queryset)
    
    @staticmethod
    def get_mood_analytics(user: User) -> dict:
        """Calculate mood analytics for dashboard"""
        recent_moods = MoodEntry.objects.filter(
            user=user,
            created_at__gte=datetime.now() - timedelta(days=30)
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
            'average': round(stats['avg_mood'] * 20, 1),  # Convert to percentage
            'count': stats['total_count'],
            'trend': trend,
            'latest': recent_moods.first().mood if recent_moods.exists() else None
        }