from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    goals = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (0, 'Very Negative'),
        (1, 'Negative'),
        (2, 'Neutral'),
        (3, 'Positive'),
        (4, 'Very Positive'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    mood = models.IntegerField(choices=MOOD_CHOICES)
    emoji = models.CharField(max_length=8, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Mood({self.user.username}:{self.mood} @ {self.created_at})"


class Exercise(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    duration_seconds = models.IntegerField(default=300)
    category = models.CharField(max_length=100, blank=True)
    audio_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)
    completed_at = models.DateTimeField(default=timezone.now)
    duration_seconds = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"Workout({self.user.username}:{self.exercise})"


class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='badges', blank=True)

    def __str__(self):
        return self.name
