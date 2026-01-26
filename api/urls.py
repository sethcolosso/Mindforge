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
    ProfessionalSearchView,
    current_user,
    focus_reset_view,
    ease_anxiety_view,
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'moods', MoodEntryViewSet, basename='mood')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workouts', WorkoutSessionViewSet, basename='workout')
router.register(r'badges', BadgeViewSet, basename='badge')

urlpatterns = [
    # Authentication endpoints
    path('api/auth/register/', RegisterView.as_view(), name='auth-register'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', current_user, name='current_user'),

    # Professional Search
    path('api/professionals/search/', ProfessionalSearchView.as_view(), name='professional-search'),

    # Coach Recommendation
    path('api/coach/recommendation/', CoachRecommendationView.as_view(), name='coach-recommendation'),

    # All ViewSet APIs
    path('api/', include(router.urls)),

    # HTML Pages
    path('', home, name='home'),
    path('exercises/focus-reset/', focus_reset_view, name='focus_reset'),
    path('exercises/ease-anxiety/', ease_anxiety_view, name='ease_anxiety'),
]