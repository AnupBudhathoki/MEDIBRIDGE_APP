# MediBridge

A Django-based patient-doctor appointment and health management platform with eSewa payment integration.

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install django

# 3. Configure environment (optional)
cp .env.example .env
# Edit .env with your settings

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

Visit http://127.0.0.1:8000

## User Roles

- **Patient** — Browse doctors, book appointments, view health records
- **Doctor** — Manage available slots, view appointments via dashboard

## Payment

Uses eSewa sandbox (test) by default. Set `ESEWA_MERCHANT_ID`, `ESEWA_SECRET_KEY`, and `ESEWA_PAYMENT_URL` in `.env` for production.
