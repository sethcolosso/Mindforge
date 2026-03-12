from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, account_type='user')

@receiver(post_save, sender=User)  
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Profile(models.Model):
    """
    User profile with account type (regular user or mental health professional)
    """
    ACCOUNT_TYPE_CHOICES = [
        ('user', 'Regular User'),
        ('work', 'Mental Health Professional'),
    ]

    CAREER_TYPE_CHOICES = [
        ('physician', 'Physician'),
        ('psychiatrist', 'Psychiatrist'),
        ('therapist', 'Therapist'),
        ('counselor', 'Counselor'),
        ('psychologist', 'Psychologist'),
        ('social_worker', 'Social Worker'),
        # You can add more professions later
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Account type & career (for professionals)
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default='user'
    )
    career_type = models.CharField(
        max_length=20,
        choices=CAREER_TYPE_CHOICES,
        blank=True,
        null=True  # Only required for work accounts
    )

    # Common fields
    bio = models.TextField(blank=True, null=True)
    goals = models.JSONField(default=list, blank=True)

    # Work account specific fields
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_visible_for_search = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.account_type})"


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


class ExerciseOpenEvent(models.Model):
    """Tracks whenever a user opens an exercise."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_open_events')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='open_events')
    opened_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-opened_at']

    def __str__(self):
        return f"ExerciseOpen({self.user.username}:{self.exercise.slug})"


class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='badges', blank=True)

    def __str__(self):
        return self.name
