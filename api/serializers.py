from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, MoodEntry, Exercise, WorkoutSession, Badge


class UserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(
        source='profile.profile_photo',
        read_only=True
    )
    account_type = serializers.CharField(
        source='profile.account_type',
        read_only=True
    )
    career_type = serializers.CharField(
        source='profile.career_type',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'profile_photo',
            'account_type',
            'career_type'
        )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    account_type = serializers.ChoiceField(choices=Profile.ACCOUNT_TYPE_CHOICES, default='user')
    career_type = serializers.ChoiceField(choices=Profile.CAREER_TYPE_CHOICES, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'account_type', 'career_type']

    def validate(self, data):
        # Enforce career_type for work accounts
        if data['account_type'] == 'work' and not data.get('career_type'):
            raise serializers.ValidationError({
                "career_type": "This field is required for Mental Health Professionals."
            })
        return data

    def create(self, validated_data):
        account_type = validated_data.pop('account_type')
        career_type = validated_data.pop('career_type', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(
            user=user,
            account_type=account_type,
            career_type=career_type if account_type == 'work' else None
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'goals', 'account_type', 'career_type', 'profile_photo', 'is_visible_for_search')


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