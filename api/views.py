from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .models import Profile, MoodEntry, Exercise, WorkoutSession, Badge
from .serializers import (
    UserSerializer, RegisterSerializer, ProfileSerializer,
    MoodEntrySerializer, ExerciseSerializer, WorkoutSessionSerializer,
    BadgeSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import render
from .services.openai_service import get_coach_recommendation


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

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='update')
    def update_profile(self, request):
        profile = request.user.profile
        if profile.account_type != 'work':
            return Response({"error": "Only work accounts can update profiles."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsAuthenticated,)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        search_query = request.query_params.get('search', '')
        professionals = Profile.objects.filter(
            account_type='work',
            is_visible_for_search=True
        )
        if search_query:
            professionals = professionals.filter(career_type__icontains=search_query)
        serializer = ProfileSerializer(professionals, many=True)
        return Response(serializer.data)


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