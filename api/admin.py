from django.contrib import admin
from .models import Profile, MoodEntry, Exercise, WorkoutSession, Badge

admin.site.register(Profile)
admin.site.register(MoodEntry)
admin.site.register(Exercise)
admin.site.register(WorkoutSession)
admin.site.register(Badge)
