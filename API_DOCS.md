**MindForge Backend API**

This document explains how to use the MindForge Django backend API. It is intended for frontend and integration teams so they know how to authenticate, call endpoints, seed data, and test features locally.

**Base URL**: `http://127.0.0.1:8000/`

**Authentication**
- **Type**: JWT (JSON Web Tokens) via `djangorestframework-simplejwt`.
- **Obtain token**: POST `/api/auth/token/` with `username` and `password`.
- **Use token**: Add header `Authorization: Bearer <access_token>` to all authenticated requests.

Example (PowerShell curl to get tokens):
```powershell
curl -X POST http://127.0.0.1:8000/api/auth/token/ -H "Content-Type: application/json" -d '{"username":"<username>","password":"<password>"}'
```

Successful response:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

**Register (create user)**
- Method: `POST`
- Path: `/api/auth/register/`
- Auth: None
- Body:
  - `username` (string, required)
  - `email` (string, optional)
  - `password` (string, required)

Example:
```powershell
curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com","password":"s3cret"}'
```

Response (201): created user object:
```json
{ "id": 3, "username": "alice", "email": "alice@example.com" }
```

**Profiles**
- List/Get/Update current user's profile
- Base path: `/api/profiles/`
- Auth: Required

- GET `/api/profiles/` — returns profile(s) for authenticated user (this project returns their one profile)
- PUT/PATCH `/api/profiles/<id>/` — update `bio`, `goals` (JSON list)

Profile fields:
- `user`: object (id, username, email)
- `bio`: string
- `goals`: JSON array (e.g., `["reduce stress","boost focus"]`)

**Mood Entries**
- CRUD endpoints under `/api/moods/`
- Fields:
  - `id`, `mood` (integer 0-4), `emoji` (string), `note` (string), `created_at` (datetime)
- Auth: Required

Examples:
- Create mood (POST):
```powershell
curl -X POST http://127.0.0.1:8000/api/moods/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"mood":3,"emoji":"🙂","note":"Feeling okay"}'
```
- List moods (GET):
```powershell
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:8000/api/moods/
```


- Infer mood from note (POST):
```powershell
curl -X POST http://127.0.0.1:8000/api/moods/infer/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"note":"I feel stressed and overwhelmed today"}'
```

Response:
```json
{
  "status": "success",
  "data": {
    "mood": 1,
    "confidence": 0.79,
    "reason": "Detected more negative than positive language",
    "source": "fallback"
  }
}
```

**Exercises (read-only list)**
- Path: `/api/exercises/`
- Auth: Required
- Returns seeded exercises. Example seeded slugs: `5-min-focus-ritual`, `2-min-anxiety-cooldown`, `confidence-visualization`, `5-min-reflection-journal`.

Example:
```powershell
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:8000/api/exercises/
```


- Log when user opens an exercise (POST):
```powershell
curl -X POST http://127.0.0.1:8000/api/exercises/1/open/ -H "Authorization: Bearer <ACCESS_TOKEN>"
```

**Exercise Open Events**
- Path: `/api/exercise-opens/`
- Auth: Required
- Read-only feed of all exercise open events for the current user.


**Workout Sessions**
- Path: `/api/workouts/`
- Auth: Required
- Create a session (POST) after a user completes an exercise. Fields: `exercise` (id), optional `duration_seconds`, optional `notes`.

Example create:
```powershell
curl -X POST http://127.0.0.1:8000/api/workouts/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"exercise":1,"duration_seconds":300,"notes":"Focused session"}'
```

**Badges (read-only)**
- Path: `/api/badges/`
- Auth: Required
- Returns available badges. Users can earn badges via business logic (not auto-assigned here).

**Coach Recommendation**
- Path: `POST /api/coach/recommendation/`
- Auth: Required
- Purpose: returns a short personalized recommendation. If the server environment has an `OPENAI_API_KEY` set, the endpoint will attempt to call OpenAI (model configured in code). Otherwise, it returns a rule-based recommendation fallback.
- Body optional fields:
  - `recent_mood`: integer or small string describing recent mood (the code accepts integer mood values 0-4)
  - `profile_goals`: array of goal strings

Example call:
```powershell
curl -X POST http://127.0.0.1:8000/api/coach/recommendation/ -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"recent_mood":2,"profile_goals":["reduce stress","improve focus"]}'
```

Possible responses:
- When OpenAI is available:
```json
{ "source": "openai", "text": "<GPT-generated recommendation text>" }
```
- Fallback rule-based response:
```json
{ "source": "rule-based", "recommendation": { "title": "5-Min Focus Ritual", "duration_seconds": 300, "rationale": "Brief focus reset to improve attention." } }
```

**Seeding initial data**
- Run the management command to create starter `Exercise` and `Badge` records:
```powershell
python manage.py seed_data
```

**Admin**
- The Django admin is available at `/admin/`.
- Create an admin user locally with `python manage.py createsuperuser` (already done during setup earlier).

**Local setup & dependencies**
- Requirements are in `requirements.txt`. Install in your virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```
- Environment variables (dev):
  - `DJANGO_SECRET_KEY` — set to a value in production; default in settings is for local dev only.
  - `OPENAI_API_KEY` — optional; set this to enable GPT-based recommendations.

**Migrations**
- If you pull the repo: run
```powershell
python manage.py makemigrations
python manage.py migrate
```

**Testing the API (quick flow)**
1. Start server: `python manage.py runserver`
2. Register or use an existing user.
3. Obtain JWT tokens via `/api/auth/token/`.
4. Use `access` token to call protected endpoints.

**Where the code lives (quick pointers)**
- Models: `api/models.py`
- Serializers: `api/serializers.py`
- Views & endpoints: `api/views.py` and `api/urls.py`
- OpenAI integration & fallback: `api/services/openai_service.py`
- Seed command: `api/management/commands/seed_data.py`

**Errors & common responses**
- `401 Unauthorized` — missing/invalid token
- `400 Bad Request` — validation errors; response contains DRF error details
- `404 Not Found` — invalid resource id

**Notes for frontend / integration teams**
- All endpoints except register and token obtain require authentication.
- Use the `seed_data` command to ensure exercises are available in dev.
- For coach recommendations, include `recent_mood` and `profile_goals` in POST body to get personalized suggestions. If `OPENAI_API_KEY` is not set, you will receive a deterministic rule-based recommendation.
- If you want richer GPT responses, add `OPENAI_API_KEY` in the environment where the backend runs; be aware of cost and moderation requirements for public users.

**Next steps we can do for you**
- Add OpenAPI/Swagger schema and docs auto-generation.
- Add unit tests for the coach endpoint and other endpoints.
- Add Stripe integration and subscription endpoints for the Pro tier stub.

---

If you'd like, I can also generate a Postman collection or add an OpenAPI YAML for these endpoints — tell me which you prefer and I will add it to the repo.
