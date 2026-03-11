import json
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


def analyze_mood_from_text(note: str):
    """Use OpenAI to classify mood from free-text note."""
    try:
        import openai
    except Exception:
        logger.exception('openai package not installed')
        return None

    if not OPENAI_API_KEY:
        logger.info('OPENAI_API_KEY not set; skipping OpenAI mood analysis')
        return None

    prompt = (
        "Classify the following mood note into a score from 0-4, where "
        "0=very negative, 1=negative, 2=neutral, 3=positive, 4=very positive. "
        "Return strict JSON with keys: mood (int), confidence (0-1 float), reason (short string).\n\n"
        f"Mood note: {note}"
    )

    openai.api_key = OPENAI_API_KEY
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'You analyze mood notes and return only strict JSON.'},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=180,
            temperature=0,
        )
        text = resp['choices'][0]['message']['content']
        parsed = json.loads(text)
        mood = int(parsed.get('mood', 2))
        confidence = float(parsed.get('confidence', 0.0))
        reason = str(parsed.get('reason', ''))

        if mood < 0 or mood > 4:
            mood = 2

        return {
            'mood': mood,
            'confidence': max(0.0, min(1.0, confidence)),
            'reason': reason,
            'source': 'openai',
        }
    except Exception:
        logger.exception('OpenAI mood analysis failed')
        return None
