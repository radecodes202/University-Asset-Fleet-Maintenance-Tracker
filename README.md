# 🚐 FleetTrack — University Asset & Fleet Maintenance Tracker

> A centralized Django web application for managing the maintenance lifecycle of university vehicles (motorpool) and high-value IT equipment. Staff file maintenance requests, motorpool managers approve and assign work orders, and auditors review an immutable audit trail.

![Django 6.0](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-3.17-ff1709?logo=django&logoColor=white)
![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-blue)

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start (Local)](#-quick-start-local)
- [Environment Variables](#-environment-variables)
- [Database Setup](#-database-setup)
- [Running the App](#-running-the-app)
- [Deployment (Render / Railway)](#-deployment-render--railway)
- [User Roles & RBAC](#-user-roles--rbac)
- [API Endpoints](#-api-endpoints)
- [Security](#-security)
- [Project Structure](#-project-structure)
- [Contributing Team](#-contributing-team)

---

## ✨ Features

- **📦 Asset Registry** — Centralized inventory of vehicles and IT equipment with categories, serial numbers, purchase info, and current status.
- **🛠️ Maintenance Request Workflow** — Staff submit requests → Managers approve/reject → Work orders are created → Technicians execute → History is recorded.
- **👥 Role-Based Access Control** — Three roles (Standard Staff, Motorpool Manager, Auditor) with strictly enforced permissions.
- **📊 Dashboard with KPIs** — Real-time metrics: total assets, pending requests, completed repairs, under-maintenance count, total maintenance cost.
- **🔐 JWT-Protected REST API** — Mobile-ready endpoints for drivers to submit mileage and dashboard alerts.
- **💰 Field-Level Masking** — Costs and procurement values are hidden from non-manager JWT tokens.
- **🛡️ Active Defense** — Custom brute-force lockout (5 failed attempts → 10-minute lock), DRF throttling, audit logging on every auth event.
- **📋 Immutable Audit Logs** — Every create/update/approve/reject/status-change/login/logout is logged with user, timestamp, IP, and before/after values.
- **🖼️ Cloud-Hosted Media** — Asset images stored on Cloudinary (zero local storage risk).
- **📖 Built-in User Guide** — Interactive `/userguide/` page accessible to all roles.

---

## 🏗️ Architecture

```
                          ┌──────────────────────┐
                          │   Browser (Web UI)   │
                          └──────────┬───────────┘
                                     │ HTTPS
                                     ▼
                          ┌──────────────────────┐
                          │   Django + DRF       │
                          │   (Gunicorn)         │
                          └────┬───────┬────┬────┘
                               │       │    │
              ┌────────────────┘       │    └────────────────┐
              ▼                        ▼                     ▼
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │  PostgreSQL      │   │  Cloudinary      │   │  WhiteNoise      │
   │  (data)          │   │  (media)         │   │  (static files)  │
   └──────────────────┘   └──────────────────┘   └──────────────────┘
```

| Layer | Technology |
|---|---|
| **Web framework** | Django 6.0 |
| **API framework** | Django REST Framework 3.17 |
| **Authentication** | SimpleJWT (Bearer tokens, refresh rotation, blacklisting) |
| **Database** | PostgreSQL 15+ (production) / SQLite (local dev fallback) |
| **Media storage** | Cloudinary |
| **Static files** | WhiteNoise (compressed manifest) |
| **WSGI server** | Gunicorn 23 |
| **Configuration** | python-decouple (.env) |
| **Filtering** | django-filter + DRF SearchFilter + OrderingFilter |
| **Pagination** | DRF PageNumberPagination (20 items/page) |
| **Throttling** | DRF UserRateThrottle (1000/hr) + AnonRateThrottle (100/hr) |

---

## 🧰 Tech Stack

**Backend:** Django 6.0 · DRF 3.17 · SimpleJWT 5.5 · django-filter 25.2 · Pillow 12.2
**Database:** PostgreSQL 15+ (prod) · SQLite (dev) · psycopg2-binary 2.9
**Media:** Cloudinary 1.44 · django-cloudinary-storage 0.3
**Infra:** Gunicorn 23 · WhiteNoise 6.12 · dj-database-url 2.3
**Security:** python-decouple 3.8 · django-cors-headers 4.9

---

## 🚀 Quick Start (Local)

### Prerequisites

- **Python 3.12+**
- **pip** (or `uv` / `poetry`)
- **Git**
- *(Optional but recommended)* A virtual environment

### 1. Clone the repo

```bash
git clone https://github.com/radecodes202/University-Asset-Fleet-Maintenance-Tracker.git
cd University-Asset-Fleet-Maintenance-Tracker
```

### 2. Create a virtual environment & install dependencies

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in the values. For a quick local-only start, the **only** required value is `SECRET_KEY`:

```bash
# Generate a random secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste it into `.env` as `SECRET_KEY=...`. Leave `DEBUG=True` for local dev. Leave `DATABASE_URL=` blank to use SQLite.

> 💡 **Cloudinary is optional for local dev.** If you leave the Cloudinary fields blank, the app falls back to local `media/` storage (which is fine on your laptop but not on Render).

### 4. Apply migrations & seed the database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the dev server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> — you'll be redirected to the login page.

---

## 🔐 Environment Variables

All environment variables are read by `python-decouple` from a `.env` file in the project root. **Never commit `.env` to source control** — it's already in `.gitignore`.

| Variable | Required? | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | ✅ Yes | — | Django secret key. Generate a long random one. |
| `DEBUG` | ✅ Yes | `False` | `True` for local dev, `False` for production. |
| `ALLOWED_HOSTS` | ✅ Yes | `127.0.0.1,localhost` | Comma-separated hostnames. |
| `DATABASE_URL` | ⚠️ Production only | *(empty)* | PostgreSQL connection string. Empty = SQLite. |
| `CLOUDINARY_CLOUD_NAME` | ⚠️ Production | `''` | From cloudinary.com/console. |
| `CLOUDINARY_API_KEY` | ⚠️ Production | `''` | From cloudinary.com/console. |
| `CLOUDINARY_API_SECRET` | ⚠️ Production | `''` | From cloudinary.com/console. |
| `CORS_ALLOWED_ORIGINS` | ⚠️ If using a separate front-end | localhost | Comma-separated allowed origins. |

See **`.env.example`** for a ready-to-copy template.

---

## 🗄️ Database Setup

### Local (SQLite — no setup needed)

Just leave `DATABASE_URL=` blank. Django will create `db.sqlite3` automatically on first migrate.

### Production (PostgreSQL on Render)

Render provides a free managed PostgreSQL instance:

1. In your Render dashboard, create a new **PostgreSQL** service.
2. Copy the **Internal Database URL** it gives you.
3. In your Render web service's **Environment** tab, add:
   ```
   DATABASE_URL = postgresql://user:password@host/dbname
   ```
4. Render's `Procfile` runs `python manage.py migrate` on every deploy, so the schema is always up to date.

### Manual PostgreSQL (anywhere)

```bash
createdb fleettrack
export DATABASE_URL=postgres://user:password@localhost:5432/fleettrack
python manage.py migrate
```

---

## ▶️ Running the App

```bash
# Development server
python manage.py runserver

# Production (what Render runs)
gunicorn enterprise_tracker.wsgi:application --bind 0.0.0.0:$PORT
```

The `Procfile` at the project root automates the production command:

```procfile
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn enterprise_tracker.wsgi:application --bind 0.0.0.0:$PORT
```

---

## ☁️ Deployment (Render / Railway)

### One-time setup on Render

1. **Push your code to GitHub** (the repo is already at <https://github.com/radecodes202/University-Asset-Fleet-Maintenance-Tracker>).

2. **Create a new Web Service** on Render pointing to this repo.

3. **Build & start commands:** Render auto-detects the `Procfile`. Override only if needed:
   - Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start: `gunicorn enterprise_tracker.wsgi:application --bind 0.0.0.0:$PORT`

4. **Add a managed PostgreSQL instance** (free tier is fine for the demo). Copy its **Internal Database URL** into the web service's environment as `DATABASE_URL`.

5. **Add a Cloudinary account** (free tier is fine) at <https://cloudinary.com/>. Copy `Cloud Name`, `API Key`, `API Secret` into the environment.

6. **Set all the env vars** in Render's Environment tab:

   | Key | Value |
   |---|---|
   | `SECRET_KEY` | *(a long random string)* |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-app.onrender.com` |
   | `DATABASE_URL` | *(from step 4)* |
   | `CLOUDINARY_CLOUD_NAME` | *(from step 5)* |
   | `CLOUDINARY_API_KEY` | *(from step 5)* |
   | `CLOUDINARY_API_SECRET` | *(from step 5)* |

7. **Deploy.** The `Procfile` runs migrations + collectstatic + gunicorn automatically.

### After first deploy

- Visit `https://<your-app>.onrender.com/login/`
- Sign in with the superuser you created locally (you'll need to seed one — see below).

### Seeding an initial superuser in production

Open a Render shell (`Shell` tab in the dashboard) and run:

```bash
python manage.py createsuperuser
```

---

## 👥 User Roles & RBAC

The system has three roles, defined in `accounts/models.py`:

| Role | Can do |
|---|---|
| **Standard Staff** (default) | View assets, submit maintenance requests, track own request status. |
| **Motorpool Manager** | Everything Staff can do + approve/reject requests, create & assign work orders, record completed maintenance, manage users & assets, view costs & audit logs. |
| **Auditor** | Read-only: view all data, view audit logs, export CSV reports. Cannot create or edit anything. |

The active role is stored in `User.role` and exposed via convenience properties: `is_manager`, `is_auditor`, `is_standard_staff`, `can_view_costs`, `can_approve_requests`, `can_create_work_orders`, `is_read_only`.

Permission classes in the API:
- `IsAuthenticated` (default for every endpoint)
- `IsManager` (for user-management endpoints)
- Object-level filtering is done in `get_queryset()` of each view (e.g. staff only see their own requests)

---

## 🔌 API Endpoints

All endpoints are under `/api/`. Authentication uses JWT Bearer tokens.

### Auth

| Method | URL | Purpose |
|---|---|---|
| POST | `/api/auth/login/` | Obtain JWT access + refresh tokens |
| POST | `/api/auth/refresh/` | Refresh an access token |
| POST | `/api/auth/logout/` | Blacklist a refresh token |

### Assets

| Method | URL | Purpose | Manager-only? |
|---|---|---|---|
| GET | `/api/assets/` | List all assets | No |
| POST | `/api/assets/` | Create an asset | Yes |
| GET | `/api/assets/<id>/` | Retrieve an asset | No |
| PATCH | `/api/assets/<id>/` | Update an asset | Yes |
| DELETE | `/api/assets/<id>/` | Delete an asset | Yes |

### Maintenance

| Method | URL | Purpose | Manager-only? |
|---|---|---|---|
| GET | `/api/maintenance/requests/` | List requests (staff see only their own) | No |
| POST | `/api/maintenance/requests/` | Submit a request | No (staff) |
| PATCH | `/api/maintenance/requests/<id>/` | Approve / reject | Yes |
| POST | `/api/maintenance/requests/bulk-update/` | Bulk approve / reject | Yes |
| GET | `/api/maintenance/workorders/` | List work orders | Yes |
| POST | `/api/maintenance/workorders/` | Create a work order | Yes |
| GET | `/api/maintenance/history/` | List maintenance history | No |
| GET | `/api/maintenance/history-export-csv/` | Export history as CSV | No |

### Accounts

| Method | URL | Purpose | Manager-only? |
|---|---|---|---|
| GET | `/api/accounts/users/list/` | List users | Yes |
| POST | `/api/accounts/users/list/` | Create a user | Yes |

### Dashboard

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/dashboard/summary/` | Get KPI counts |
| GET | `/api/dashboard/recent-activity/` | Get last 5 requests / work orders / completed |

### Audit

| Method | URL | Purpose | Roles |
|---|---|---|---|
| GET | `/api/audit/logs/` | List audit log entries | Manager, Auditor |

### Field-level masking (costs)

The `MaintenanceHistorySerializer` and `AssetSerializer` strip out `maintenance_cost` and `purchase_cost` whenever `request.user.is_manager` is `False`. Standard staff and auditors see a redacted record; managers see the full numbers.

---

## 🛡️ Security

- **Brute-force lockout:** After 5 failed login attempts, the account is locked for 10 minutes. Every failed attempt and the lockout itself are recorded in the audit log. Implementation: `accounts/views.py::FailedLoginTrackingBackend`.
- **JWT with rotation + blacklisting:** Refresh tokens are rotated on every use, and old ones are blacklisted.
- **API throttling:** 1000 requests/hour for authenticated users, 100/hour for anonymous.
- **Strict transport security:** HSTS enabled, `SECURE_SSL_REDIRECT` in production, `SECURE_HSTS_PRELOAD` enabled.
- **Content Security Policy:** CSP explicitly whitelists `cdn.jsdelivr.net` (Bootstrap), `res.cloudinary.com` (images), and `api.cloudinary.com` (uploads). All other sources are blocked.
- **Session hardening:** HTTPOnly, `Secure` (when not DEBUG), `SameSite=Lax`, expires on browser close.
- **Audit logging on every state-changing action** plus every login / logout / failed attempt.
- **Environment isolation:** All secrets via `python-decouple`. `DEBUG` defaults to `False` in production. `SECRET_KEY` is never hard-coded.
- **Password validation:** Django's four built-in validators (length, common, similarity, numeric).

To run the official Django security audit:

```bash
python manage.py check --deploy
```

---

## 📁 Project Structure

```
University-Asset-Fleet-Maintenance-Tracker/
├── accounts/           # User model, roles, auth, login views
├── assets/             # Asset & AssetCategory models + API
├── audit/              # Audit log model + NIST-style action logger
├── dashboard/          # Dashboard KPIs, recent activity, user guide page
├── maintenance/        # MaintenanceRequest, WorkOrder, MaintenanceHistory
├── enterprise_tracker/ # Django project settings, URL conf, WSGI
├── static/             # CSS, JS, images
├── .env.example        # Template for environment variables
├── .gitignore
├── manage.py
├── Procfile            # Render/Railway entrypoint
├── requirements.txt    # Pinned dependencies
└── README.md           # This file
```

---

## 🤝 Contributing Team

This project was built as part of a 5-member academic capstone group.

| Member | Role | Domain |
|---|---|---|
| **Member 1** | Lead Cloud & DevOps Engineer | PaaS deployment, env vars, Cloudinary, PostgreSQL |
| **Member 2** | API & IAM Engineer | DRF REST API, JWT auth, role seeding, field-level masking |
| **Member 3** | Database Architect & RBAC Lead | Models, Anti-IDOR, Mine/All querysets, bulk updates |
| **Member 4** | Frontend UI & Component Engineer | Templates, filtering, formsets, custom tags |
| **Member 5** | DevSecOps & Compliance Analyst | Active defense, audit logging, Bandit/pip-audit |

---

## 📜 License

This project is released under an academic-use license. All rights reserved by the contributing team.

---

## 🆘 Troubleshooting

**`django.db.utils.OperationalError: could not translate host name` to db**
→ Your `DATABASE_URL` is malformed. Check that the URL is in the form
  `postgresql://user:password@host:port/dbname` and that you've URL-encoded
  any special characters in the password.

**`DisallowedHost` at the deployed URL**
→ Add your Render hostname to `ALLOWED_HOSTS` in the environment, then redeploy.
  Example value: `my-fleettrack.onrender.com`

**`ALLOWED_HOSTS`, `CSRF`, or `HSTS` warnings from `check --deploy`**
→ These are expected in local dev with `DEBUG=True`. They become errors in production
  with `DEBUG=False`. See `enterprise_tracker/settings.py` for the production overrides.

**Asset images not showing up**
→ Either configure Cloudinary env vars (recommended) or confirm the local
  `media/` directory was created on first upload. In production, **Cloudinary is
  required** because the dyno's disk is ephemeral.

**`psycopg2` import error on Render**
→ The build is failing because the system Postgres dev headers aren't available.
  `psycopg2-binary` (already in `requirements.txt`) avoids this — if you see
  `psycopg2` (without `-binary`) being installed, remove it.

**`bandit` and `pip-audit` not installed**
→ They're dev tools; install them on demand:
  ```bash
  pip install bandit pip-audit
  ```
  Or as a one-shot, no-install alternative, use the prebuilt Docker images.

---

## 📞 Support

For questions or issues with this repo:
- Open an issue on GitHub
- See the in-app **User Guide** at `/userguide/` (available after sign-in)
- Review the audit log in the **Audit Logs** page to see what changed and when

---

**Built with care by the FleetTrack team.**
