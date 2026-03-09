# MindForge Setup & Deployment Guide

## Local Development (Preview)

### 1. Clone and Setup
```bash
git clone https://github.com/sethcolosso/Mindforge.git
cd Mindforge
```

### 2. Create Virtual Environment
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# Apply migrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

- Admin panel: `http://localhost:8000/admin/`
- API endpoints: `http://localhost:8000/api/`

---

## Production Deployment (Vercel)

### 1. Prepare Your Repository

Make sure all changes are committed:
```bash
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### 2. Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository (sethcolosso/Mindforge)
4. Select the project and click "Import"

### 3. Configure Environment Variables

In Vercel Project Settings → Environment Variables, add:

```
DJANGO_SECRET_KEY=<generate-a-secure-key>
DEBUG=False
ALLOWED_HOSTS=<your-vercel-domain>.vercel.app,localhost
```

**To generate a secure Django secret key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Deploy

Vercel will automatically detect and deploy your Django app. The build process will:
- Install dependencies
- Run migrations
- Collect static files

### 5. Access Your Live Site

Your app will be available at: `https://<your-project>.vercel.app/`

---

## Important Notes

- **Database**: Currently uses SQLite (local only). For production, configure `DATABASE_URL` environment variable pointing to PostgreSQL or another persistent database.
- **Static Files**: Collected automatically during build via `collectstatic` command.
- **CORS**: Configured to accept all origins (update for production security).
- **JWT**: Token lifetime set to 24 hours for testing.

---

## Troubleshooting

### "DJANGO_SECRET_KEY not set"
- Add the environment variable in Vercel dashboard or `.env.local` locally

### "Database is locked"
- This happens with SQLite in production. Switch to PostgreSQL for production.

### "Static files not loading"
- Run `python manage.py collectstatic` locally to test

### "CORS errors"
- Update `CORS_ALLOWED_ORIGINS` in `mindforge_backend/settings.py` for your domain
