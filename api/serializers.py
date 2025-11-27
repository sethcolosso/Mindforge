from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, MoodEntry, Exercise, WorkoutSession, Badge


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'goals')


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ('id', 'user', 'mood', 'emoji', 'note', 'created_at')
        read_only_fields = ('user', 'created_at')


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'slug', 'description', 'duration_seconds', 'category', 'audio_url')


class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = ('id', 'user', 'exercise', 'completed_at', 'duration_seconds', 'notes')
        read_only_fields = ('user', 'completed_at')


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'description')
