# MindForge Backend (Django)

Minimal Django backend for the MindForge MVP.

Quick setup (Windows PowerShell):

```powershell
# create and activate venv
python -m venv venv
.\venv\Scripts\Activate
django-cors-headers

# install dependencies
pip install -r requirements.txt

# set DJANGO_SECRET_KEY environment var (or edit settings)
$env:DJANGO_SECRET_KEY = 'dev-secret-for-local'

# apply migrations
python manage.py migrate

# create superuser (optional)
python manage.py createsuperuser

# run server
python manage.py runserver
```

Notes:
- Database is SQLite for development.
- JWT auth is configured via `djangorestframework-simplejwt`.
- API endpoints are under `/api/`.

Next steps: connect a frontend, add Stripe and OpenAI keys, and tune privacy settings for production.
