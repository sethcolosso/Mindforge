from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView, ProfileViewSet, MoodEntryViewSet,
    ExerciseViewSet, WorkoutSessionViewSet, BadgeViewSet
)
from .views import CoachRecommendationView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'moods', MoodEntryViewSet, basename='mood')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workouts', WorkoutSessionViewSet, basename='workout')
router.register(r'badges', BadgeViewSet, basename='badge')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('coach/recommendation/', CoachRecommendationView.as_view(), name='coach-recommendation'),
    path('', include(router.urls)),
]
