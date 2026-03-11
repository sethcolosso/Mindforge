from urllib import request
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile, MoodEntry, Exercise, WorkoutSession, Badge, ExerciseOpenEvent
from .serializers import (
    UserSerializer, RegisterSerializer, ProfileSerializer,
    MoodEntrySerializer, ExerciseSerializer, WorkoutSessionSerializer,
    BadgeSerializer, ExerciseOpenEventSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import render
from .services.openai_service import get_coach_recommendation
from .services.MoodService import MoodService
from .services.ExerciseService import ExerciseService
from .services.ProfileService import ProfileService

def home(request):
    """
    Main dashboard view with dynamic greeting.
    Tries to authenticate via JWT Bearer token in header.
    """
    user = request.user

    # Attempt JWT authentication from header (for SPA-like behavior after sign-in)
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            request.user = user  # Override anonymous user
        except (InvalidToken, TokenError, KeyError):
            pass  # Invalid token → remain anonymous

    # Time-based greeting
    now = timezone.now()
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "Good Morning,"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon,"
    elif 17 <= hour < 22:
        greeting = "Good Evening,"
    else:
        greeting = "Good Night,"

    context = {
        'greeting': greeting,
    }

    if user.is_authenticated:
        context['user'] = user
        context['profile'] = user.profile if hasattr(user, 'profile') else None
    else:
        context['greeting'] += " Guest"

    return render(request, 'api/home.html', context)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['put'], url_path='update')
    def update_profile(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Delegate to Layer 1
        return MoodService.get_user_moods(self.request.user)

    def create(self, request, *args, **kwargs):
        # Layer 2: Validation and response formatting
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delegate to Layer 1
        mood_entry = MoodService.create_mood_entry(request.user, serializer.validated_data)
        
        # Layer 2: Format response
        response_serializer = self.get_serializer(mood_entry)
        return Response({
            'status': 'success',
            'message': 'Mood entry created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='infer')
    def infer(self, request):
        """Infer mood score from a text note using LLM/fallback logic."""
        note = request.data.get('note', '')
        if not str(note).strip():
            return Response({
                'status': 'error',
                'message': 'note is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        result = MoodService.infer_mood(note)
        return Response({
            'status': 'success',
            'data': result
        })

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get mood analytics for dashboard"""
        # Delegate to Layer 1
        analytics = MoodService.get_mood_analytics(request.user)
        
        # Layer 2: Format for API response
        return Response({
            'status': 'success',
            'data': analytics,
            'message': 'Mood analytics retrieved successfully'
        })

class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    """Layer 2: Public API for exercises"""
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Exercise.objects.all()
    
    @action(detail=True, methods=['post'])
    def open(self, request, pk=None):
        """Log that the user opened an exercise."""
        exercise = self.get_object()
        event = ExerciseService.log_open_event(user=request.user, exercise_id=exercise.id)
        return Response({
            'status': 'success',
            'message': 'Exercise open event recorded',
            'data': ExerciseOpenEventSerializer(event).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get personalized exercise recommendations"""
        # Delegate to Layer 1
        exercises = ExerciseService.get_recommended_exercises(request.user)
        
        # Layer 2: Serialize and format
        serializer = self.get_serializer(exercises, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': len(exercises),
            'message': 'Recommendations generated successfully'
        })
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Log completion of an exercise"""
        exercise = self.get_object()
        
        # Layer 2: Extract and validate data
        duration = request.data.get('duration_seconds')
        notes = request.data.get('notes', '')
        
        try:
            # Delegate to Layer 1
            session = ExerciseService.log_session(
                user=request.user,
                exercise_id=exercise.id,
                duration=duration,
                notes=notes
            )
            # Layer 2: Response
            return Response({
                'status': 'success',
                'message': 'Exercise completed successfully',
                'session_id': session.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Failed to log session: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class ExerciseOpenEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExerciseOpenEventSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ExerciseOpenEvent.objects.filter(user=self.request.user)

class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (IsAuthenticated,)


class CoachRecommendationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        recent_mood = request.data.get('recent_mood')
        profile_goals = request.data.get('profile_goals')
        result = get_coach_recommendation(profile_goals=profile_goals, recent_mood=recent_mood)
        return Response(result)


class ProfessionalSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        
        # Delegate to Layer 1
        professionals = ProfileService.get_professionals(search_query)
        
        # Layer 2: Serialize and format
        serializer = ProfileSerializer(professionals, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': len(professionals)
        })
    
class DashboardStatsView(APIView):
    """Layer 2: Dashboard statistics endpoint"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all dashboard statistics"""
        try:
            # Delegate to Layer 1 services
            mood_stats = MoodService.get_mood_analytics(request.user)
            exercise_stats = ExerciseService.get_user_stats(request.user)
            
            # Layer 2: Combine and format response
            return Response({
                'status': 'success',
                'data': {
                    'mood': mood_stats,
                    'exercises': exercise_stats
                }
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Failed to retrieve stats: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Update existing views to use services
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Layer 2: Handle file uploads and validation
        serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Delegate to Layer 1
            profile = ProfileService.update_profile(request.user, serializer.validated_data)
            
            # Layer 2: Return formatted response
            response_serializer = ProfileSerializer(profile)
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully',
                'data': response_serializer.data
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Failed to update profile: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ── API to get current user (for frontend after login) ──────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# HTML exercise pages
def focus_reset_view(request):
    return render(request, 'api/exercises/focus_reset.html')


def ease_anxiety_view(request):
    return render(request, 'api/exercises/ease_anxiety.html')


def visualization_view(request):
    return render(request, 'api/exercises/visualization.html')


def visualization_player_view(request):
    return render(request, 'api/exercises/player.html')
