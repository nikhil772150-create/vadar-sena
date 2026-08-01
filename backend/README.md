# BVSMS Backend Architecture & Service Engine

Enterprise Django 5.0 REST API engine for the **Bharatiya Vadar Sena Management System (BVSMS)**.

## Architecture Highlights
- **Decoupled Architecture:** Clean separation of concerns (Views $\rightarrow$ Services $\rightarrow$ Selectors $\rightarrow$ ORM Models).
- **Custom Identity Model:** Custom `auth_users` model (`User`) using phone numbers as primary login identifier.
- **Base Model Foundation:** Abstract `BaseModel` providing UUID identity, audit timestamps, and soft deletion (`is_deleted`, `deleted_at`).
- **Standardized API Envelope:** Every API response strictly conforms to:
  ```json
  {
    "success": true,
    "message": "Status description",
    "data": {},
    "errors": null
  }
  ```
- **Global Exception Handler:** Catches all API and unhandled server errors into the standard JSON envelope.

---

## Folder Structure

```
backend/
├── apps/
│   ├── common/               # Foundation: BaseModel, Exception Handler, Responses, Permissions
│   ├── authentication/       # Custom User model, JWT, OTP service, Auth views
│   ├── organization/         # State, District, Taluka, Village schemas
│   ├── members/              # Member profile & registration module
│   ├── events_meetings/      # Events and meeting schedules
│   ├── news_cms/             # CMS for news and static content
│   ├── gallery/              # Photo & Video albums
│   ├── donations/            # Donation verification logs
│   ├── communications/       # Contact forms and alerts
│   └── audit_system/         # System audit & settings
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── .env.example
├── Dockerfile
└── manage.py
```

---

## Local Development Setup

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements/local.txt
   ```
3. **Execute Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Create Super Admin:**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run Dev Server:**
   ```bash
   python manage.py runserver
   ```
6. **Health Check Endpoint:**
   `GET http://127.0.0.1:8000/api/v1/health/`
