# Meshed

An internal HR web app for managing employee time tracking and holiday requests — built with Django, Tailwind CSS, HTMX, and Alpine.js.

This project is a ground-up rebuild of an earlier HR system. Rather than refactor code nobody fully remembers the reasoning behind, it's being rebuilt fresh against a written spec, one feature at a time, with the old app kept purely as a reference.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [Current Status](#current-status)
- [Design Decisions Worth Knowing](#design-decisions-worth-knowing)

## Tech stack

- **Backend:** Django 5.2
- **Database:** SQLite locally, Postgres in production (via `DATABASE_URL`)
- **Frontend:** Tailwind CSS (compiled via the Tailwind CLI), HTMX for server-driven interactivity, Alpine.js for small client-side behaviour — no SPA framework, no JS build step beyond Tailwind's own compiler
- **Other key packages:** `django-htmx` (request.htmx detection), `openpyxl` (Excel export), `Pillow` (image uploads), `whitenoise` (static file serving), `pytest-django` (testing)

[↑ To Contents](#table-of-contents)

## Project structure

```
Meshed/
├── config/          # Django project settings, root URLs
├── accounts/        # Users, roles, departments, company-wide settings
├── holidays/        # Holiday requests, approvals, company closures
├── timekeeping/     # Clock in/out, timesheets, audit log
├── templates/       # Shared templates (base.html, etc.)
├── static/
│   ├── src/         # Tailwind input CSS
│   ├── css/         # Compiled Tailwind output
│   └── js/          # htmx.min.js, alpine.min.js
└── manage.py
```

[↑ To Contents](#table-of-contents)

## Local setup

1. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate   # Git Bash on Windows
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   npm install
   ```

4. **Build Tailwind CSS** (rebuilds on save while this is running)
   ```bash
   npx @tailwindcss/cli -i ./static/src/input.css -o ./static/css/tailwind.css --watch
   ```

5. **Create a `.env` file** in the project root:
   ```
   SECRET_KEY=<generate one — see below>
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
   Generate a secret key with:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Run migrations and start the server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

7. **Create an admin account** to explore the Django admin panel at `/admin/`
   ```bash
   python manage.py createsuperuser
   ```

[↑ To Contents](#table-of-contents)

## Current status

This project is under active development, built incrementally and reviewed step by step.

- [x] Django project scaffolded — `manage.py`, `config/`, three apps created
- [x] Environment-based settings — `SECRET_KEY` (with a fail-fast check), `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL` fallback to SQLite
- [x] `django-htmx` middleware wired in
- [x] Tailwind CSS, htmx, and Alpine.js installed and building correctly
- [x] `accounts` app data model:
  - `Department` — a configurable list of departments
  - `UserProfile` — role, weekly contracted hours, holiday allowance, department, approver
  - `CompanySettings` — a singleton record for company-wide defaults (name, logo, default hours/allowance)
  - A signal that automatically creates a `UserProfile` whenever a new `User` account is created
- [x] `Department`, `UserProfile`, and `CompanySettings` registered in Django admin
- [ ] Authentication — login (username or email), logout, password reset
- [ ] `holidays` app data model and views
- [ ] `timekeeping` app data model and views
- [ ] Remaining feature build-out against the project spec

[↑ To Contents](#table-of-contents)

## Design decisions worth knowing

- **No public self-registration.** Accounts are created by an Admin only.
- **Holiday approval is currently open to any Manager/Admin**, not restricted to a specific approver — this may be made more granular later. The `approver` field on `UserProfile` already exists to support that in future, it just isn't enforced by any view logic yet.
- **Departments are a proper model, not a hardcoded list** — an Admin will be able to add/rename/remove departments without any code changes.

[↑ To Contents](#table-of-contents)
