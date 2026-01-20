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
from rest_framework.views import APIView
from .services.openai_service import get_coach_recommendation
from django.shortcuts import render

def home(request):
    # Add context if needed (e.g., dynamic data from API/models)
    context = {
        'greeting': 'Good Afternoon,',  # Can make dynamic based on time
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
