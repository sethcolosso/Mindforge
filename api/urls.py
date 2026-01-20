from django.urls import path, include
from .views import home
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, ProfileViewSet, MoodEntryViewSet,
    ExerciseViewSet, WorkoutSessionViewSet, BadgeViewSet
)
from .views import CoachRecommendationView
from .views import home   # ← add this if missing


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

    # All API endpoints under /api/ (protected by default if you have authentication classes)
    path('api/', include(router.urls)),

    # IMPORTANT: The actual web page (your MindForge UI) served at ROOT
    path('', home, name='home'),
]

