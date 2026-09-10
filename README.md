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
  - `CompanySettings` — a singleton record for company-wide defaults (name, logo, default hours/allowance, whether weekends count toward holiday day totals)
  - A signal that automatically creates a `UserProfile` whenever a new `User` account is created
- [x] `Department`, `UserProfile`, and `CompanySettings` registered in Django admin
- [x] `holidays` app data model:
  - `HolidayRequest` — an employee's submitted request (dates, type, status, reviewer/rejection info)
  - `CompanyHoliday` — admin-set company-wide closures (e.g. Christmas)
  - Both calculate working-day counts based on the company's weekend-counting setting
- [x] `HolidayRequest` and `CompanyHoliday` registered in Django admin
- [x] Migrations run for the `include_weekends` field and the new `holidays` models
- [x] `timekeeping` app data model:
  - `TimeEntry` — one per person per calendar day, clock-in/out, plus hours-worked and current clock-state calculations
  - `BreakEntry` — individual breaks belonging to a time entry (a day can have several)
  - `TimeAuditEntry` — a record created whenever someone manually edits a time entry
- [x] `TimeEntry`, `BreakEntry`, and `TimeAuditEntry` registered in Django admin
- [x] Migrations run for the `timekeeping` app
- [x] Production-only security headers (HSTS, SSL redirect, secure cookies, content-type sniffing protection) added to `settings.py`, gated behind `if not DEBUG`
- [x] `SESSION_COOKIE_AGE` set to 2 days (internal tool — chosen over the shorter 8-hour enterprise standard for convenience)
- [x] `django-axes` installed for brute-force login protection — locks an account after 5 failed attempts, 1-hour cooldown, tracked by username
- [ ] Authentication — login (username or email), logout, password reset
- [ ] `holidays` app views (submit/approve/reject requests, team calendar, company closures admin page)
- [ ] `timekeeping` app views (clock in/out, timesheet, audit log)
- [ ] Remaining feature build-out against the project spec

[↑ To Contents](#table-of-contents)

## Design decisions worth knowing

- **No public self-registration.** Accounts are created by an Admin only.
- **Holiday approval is currently open to any Manager/Admin**, not restricted to a specific approver — this may be made more granular later. The `approver` field on `UserProfile` already exists to support that in future, it just isn't enforced by any view logic yet.
- **Departments are a proper model, not a hardcoded list** — an Admin will be able to add/rename/remove departments without any code changes.
- **Whether weekends count toward holiday day totals is a company-wide setting** (`CompanySettings.include_weekends`), not hardcoded — defaults to off (weekends excluded), but a company can switch it on. Applies consistently to both individual holiday requests and company-wide closures.
- **Managers, not just Admins, can edit any employee's timesheet.** This is a deliberate widening of the original spec (which only mentioned Admins) based on real usage — Employees can only edit their own entries.
- **`django-axes` locks by username only, not IP address** — a deliberate tradeoff. It avoids one person's mistyped password accidentally locking out the whole office (likely sharing one IP), at the cost of not rate-limiting an attacker who sprays guesses across many different usernames. Accepted given this is a small internal tool, not a public-facing target. `AXES_LOCKOUT_PARAMETERS` in `settings.py` is where this would change if that judgement call is ever revisited.
- **2FA for Admin accounts is deliberately deferred**, not rejected — noted as a real gap to revisit later, not forgotten.

[↑ To Contents](#table-of-contents)
