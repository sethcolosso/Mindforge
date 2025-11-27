import os
import logging

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

logger = logging.getLogger(__name__)


def get_recommendation_prompt(profile_goals, recent_mood):
    goals_text = ', '.join(profile_goals) if profile_goals else 'general wellbeing'
    return (
        f"User goals: {goals_text}. Recent mood: {recent_mood}. "
        "Suggest a single short daily mental workout (title, duration_seconds, and a brief rationale)."
    )


def call_openai(prompt):
    try:
        import openai
    except Exception:
        logger.exception('openai package not installed')
        return None

    if not OPENAI_API_KEY:
        logger.info('OPENAI_API_KEY not set; skipping OpenAI call')
        return None

    openai.api_key = OPENAI_API_KEY
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'system', 'content': 'You are a concise mental fitness coach.'},
                      {'role': 'user', 'content': prompt}],
            max_tokens=200,
            temperature=0.7,
        )
        text = resp['choices'][0]['message']['content']
        return text
    except Exception:
        logger.exception('OpenAI call failed')
        return None


def get_coach_recommendation(profile_goals=None, recent_mood=None):
    prompt = get_recommendation_prompt(profile_goals or [], recent_mood or 'neutral')
    text = call_openai(prompt)
    if text:
        return {'source': 'openai', 'text': text}

    # Fallback simple rule-based recommender
    mood = recent_mood or 'neutral'
    if isinstance(mood, int):
        mood_score = mood
    else:
        try:
            mood_score = int(mood)
        except Exception:
            mood_score = 2

    if mood_score <= 1:
        rec = {
            'title': '2-Min Anxiety Cooldown',
            'duration_seconds': 120,
            'rationale': 'Short breathing exercise to down-regulate stress.'
        }
    elif mood_score == 2:
        rec = {
            'title': '5-Min Focus Ritual',
            'duration_seconds': 300,
            'rationale': 'Brief focus reset to improve attention.'
        }
    else:
        rec = {
            'title': 'Confidence Boost Visualization',
            'duration_seconds': 420,
            'rationale': 'Visualization to amplify positive momentum.'
        }

    return {'source': 'rule-based', 'recommendation': rec}
