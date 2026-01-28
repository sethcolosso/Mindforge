from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    home,
    RegisterView,
    ProfileViewSet,
    MoodEntryViewSet,
    ExerciseViewSet,
    WorkoutSessionViewSet,
    BadgeViewSet,
    CoachRecommendationView,
    focus_reset_view, 
    ease_anxiety_view,
        visualization_view,
            visualization_player_view,  # ← added here
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'moods', MoodEntryViewSet, basename='mood')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workouts', WorkoutSessionViewSet, basename='workout')
router.register(r'badges', BadgeViewSet, basename='badge')

urlpatterns = [
    # Authentication endpoints (public)
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Coach recommendation
    path('coach/recommendation/', CoachRecommendationView.as_view(), name='coach-recommendation'),

    # All API endpoints under /api/
    path('api/', include(router.urls)),

    # IMPORTANT: The actual web page (your MindForge UI) served at ROOT
    path('', home, name='home'),

    # Focus Reset page
    path('exercises/focus-reset/', focus_reset_view, name='focus_reset'),

    # Ease Anxiety page
    path('exercises/ease-anxiety/', ease_anxiety_view, name='ease_anxiety'),

    # Visualization page
    path('exercises/visualization/', visualization_view, name='visualization'),

     # Visualization Player Page (The new route)
    path('exercises/visualization/player/', visualization_player_view, name='visualization_player'),
]