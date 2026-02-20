from django.contrib.auth.models import User
from ..models import Profile
from typing import Dict, Optional

class ProfileService:
    """Layer 1: Internal business logic for user profiles"""
    
    @staticmethod
    def update_profile(user: User, profile_data: Dict) -> Profile:
        """Update user profile with validation"""
        profile = user.profile
        
        # Update allowed fields
        if 'bio' in profile_data:
            profile.bio = profile_data['bio']
        
        if 'goals' in profile_data:
            profile.goals = profile_data['goals']
        
        if 'career_type' in profile_data and profile.account_type == 'work':
            profile.career_type = profile_data['career_type']
        
        if 'is_visible_for_search' in profile_data and profile.account_type == 'work':
            profile.is_visible_for_search = profile_data['is_visible_for_search']
        
        profile.save()
        return profile
    
    @staticmethod
    def get_professionals(search_query: Optional[str] = None) -> list[Profile]:
        """Get visible mental health professionals"""
        profiles = Profile.objects.filter(
            account_type='work',
            is_visible_for_search=True
        )
        
        if search_query:
            profiles = profiles.filter(career_type__icontains=search_query)
        
        return list(profiles)
    
    @staticmethod
    def can_access_professional_features(user: User) -> bool:
        """Check if user can access work account features"""
        return hasattr(user, 'profile') and user.profile.account_type == 'work'