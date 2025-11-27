from django.core.management.base import BaseCommand
from api.models import Exercise, Badge


class Command(BaseCommand):
    help = 'Seed initial exercises and badges for MindForge'

    def handle(self, *args, **options):
        exercises = [
            {
                'title': '5-Min Focus Ritual',
                'slug': '5-min-focus-ritual',
                'description': 'Quick breathing and single-point focus to reset attention.',
                'duration_seconds': 300,
                'category': 'focus',
            },
            {
                'title': '2-Min Anxiety Cooldown',
                'slug': '2-min-anxiety-cooldown',
                'description': 'Short guided breathing to lower acute anxiety.',
                'duration_seconds': 120,
                'category': 'anxiety',
            },
            {
                'title': 'Confidence Boost Visualization',
                'slug': 'confidence-visualization',
                'description': 'Visualization exercise to build confident mental imagery.',
                'duration_seconds': 420,
                'category': 'confidence',
            },
            {
                'title': '5-Min Reflection Journal',
                'slug': '5-min-reflection-journal',
                'description': 'Prompts to reflect on wins and learning from the day.',
                'duration_seconds': 300,
                'category': 'journaling',
            },
        ]

        badges = [
            {'name': 'First Session', 'description': 'Completed your first workout.'},
            {'name': '3-Day Streak', 'description': 'Completed exercises 3 days in a row.'},
        ]

        for ex in exercises:
            obj, created = Exercise.objects.get_or_create(slug=ex['slug'], defaults=ex)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created exercise: {obj.title}"))
            else:
                self.stdout.write(f"Exercise exists: {obj.title}")

        for b in badges:
            obj, created = Badge.objects.get_or_create(name=b['name'], defaults={'description': b['description']})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created badge: {obj.name}"))
            else:
                self.stdout.write(f"Badge exists: {obj.name}")

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
