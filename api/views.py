from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

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
    Renders the main dashboard page with dynamic time-based greeting.
    """
    now = timezone.now()  # Use timezone-aware datetime
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
        # You can add more context variables here later if needed
        # e.g. 'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'api/home.html', context)


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CoachRecommendationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Accept optional `recent_mood` and `profile_goals` in body
        recent_mood = request.data.get('recent_mood')
        profile_goals = request.data.get('profile_goals')

        result = get_coach_recommendation(profile_goals=profile_goals, recent_mood=recent_mood)
        return Response(result)