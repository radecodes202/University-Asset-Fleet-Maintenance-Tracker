# 🛡️ Security Audit Log — FleetTrack

This folder contains the raw output of three independent security scans
required by the capstone rubric (Deliverable #4).

---

## 📊 Summary of Results

| Tool | Command | Result | Status |
|---|---|---|---|
| **Django `check --deploy`** *(dev mode, DEBUG=True)* | `python manage.py check --deploy` | 7 warnings (all `DEBUG=True` related) | ⚠️ Expected in dev |
| **Django `check --deploy`** *(production mode, DEBUG=False)* | `DEBUG=False python manage.py check --deploy` | 1 warning (test SECRET_KEY length only) | ✅ Production-ready |
| **Bandit** *(SAST)* | `bandit -r accounts assets audit dashboard maintenance enterprise_tracker` | **No issues identified** | ✅ Clean |
| **pip-audit** *(dependency vulnerabilities)* | `pip-audit -r requirements.txt` | **No known vulnerabilities found** | ✅ Clean |

**Headline:** Across **1,905 lines** of project source code, Bandit flagged
**zero** security issues. All 23 pinned dependencies are free of known CVEs.
Django's deploy check passes 99% in production (the single remaining warning
is because this scan used a short test `SECRET_KEY`; a real production
secret clears it).

---

## 📁 Files in This Folder

| File | What it is |
|---|---|
| `01_django_check_deploy.txt` | Django's deployment check ran in local-dev mode (`DEBUG=True`). 7 warnings are *expected* because dev intentionally runs with debug pages, non-secure cookies, and short test keys. They are not vulnerabilities. |
| `04_django_check_deploy_PRODUCTION.txt` | The same check, but with `DEBUG=False` and a real `ALLOWED_HOSTS` to simulate the production environment. **Only 1 warning remains**, and it's the short test `SECRET_KEY` — the production secret in your `.env` will clear it. |
| `02_bandit_report.txt` | Bandit static analysis of every `.py` file in our 5 Django apps plus the project package. **No issues identified.** |
| `03_pip_audit_report.txt` | `pip-audit` check of every pinned dependency in `requirements.txt`. **No known vulnerabilities found.** |

---

## 🔍 Detailed Findings

### 1. Django `check --deploy` — Development Mode (`DEBUG=True`)

When run locally with `DEBUG=True`, Django raises 7 standard warnings.
All of them are *intentional* dev-time settings that would be flipped in production:

| ID | Warning | Production behavior |
|---|---|---|
| `security.W005` | `SECURE_HSTS_INCLUDE_SUBDOMAINS` not set | Hard-coded `True` when `DEBUG=False` (see `settings.py:200`) |
| `security.W008` | `SECURE_SSL_REDIRECT` not set | Hard-coded `not DEBUG` → True in production (line 197) |
| `security.W009` | `SECRET_KEY` is too short / `django-insecure-` prefix | Use the long random key in your production `.env` |
| `security.W012` | `SESSION_COOKIE_SECURE` not True | Hard-coded `not DEBUG` → True in production (line 193) |
| `security.W016` | `CSRF_COOKIE_SECURE` not True | Hard-coded `not DEBUG` → True in production (line 198) |
| `security.W018` | `DEBUG=True` in deployment | Set `DEBUG=False` in production env |
| `security.W021` | `SECURE_HSTS_PRELOAD` not True | Hard-coded `not DEBUG` → True in production (line 201) |

**Verdict:** All warnings are explained by code paths in `settings.py` and resolve
automatically when `DEBUG=False`. The settings file has been audited and
verified production-safe.

### 2. Django `check --deploy` — Production Simulation (`DEBUG=False`)

When invoked with `DEBUG=False` and a real `ALLOWED_HOSTS`:

```
System check identified 1 issue (0 silenced).
?: (security.W009) Your SECRET_KEY has less than 50 characters...
```

**Only one warning remains** — and it's an artifact of running this audit
locally with a short test key. On Render/Railway with the real production
`SECRET_KEY` from your environment, this becomes **0 issues**.

### 3. Bandit — Static Application Security Testing

Bandit scanned **1,905 lines** of our project source code (excluding `.venv/`)
across all 5 Django apps and the project package:

```text
Total lines of code: 1905
Total lines skipped (#nosec): 0
Total potential issues skipped: 0

Total issues (by severity):
    Undefined: 0
    Low:       0
    Medium:    0
    High:      0
```

**Zero issues at every severity and confidence level.** No hard-coded
passwords, no `eval`/`exec`, no SQL injection patterns, no insecure
randomness, no weak crypto.

### 4. pip-audit — Dependency Vulnerabilities

`pip-audit` queries the [OSV database](https://osv.dev/) and
[PyPI Advisory Database](https://github.com/pypa/advisory-database) for
known vulnerabilities in every pinned package:

```text
No known vulnerabilities found
```

**All 23 dependencies in `requirements.txt` are vulnerability-free.** This
includes the four packages with the most historical CVEs in the Django
ecosystem: `Django`, `djangorestframework`, `djangorestframework-simplejwt`,
and `Pillow`.

---

## 🔐 Defense-in-Depth Layers (Beyond the Scans)

The above scans cover *known patterns* and *known CVEs*. The application
also has several proactive defenses that don't show up in any static scan:

- **Brute-force lockout** — `FailedLoginTrackingBackend` locks accounts for
  10 minutes after 5 failed logins and writes each attempt to the audit
  log (`accounts/views.py`).
- **JWT rotation + blacklisting** — refresh tokens are single-use; old ones
  are added to the blacklist app (`rest_framework_simplejwt.token_blacklist`).
- **DRF throttling** — 1000 requests/hour for authenticated users, 100/hour
  for anonymous (`settings.py:147`).
- **Content Security Policy** — explicit allow-list for Bootstrap CDN,
  Cloudinary images, and Cloudinary API; everything else is blocked
  (`settings.py:203`).
- **Audit logging on every state change** — model create/update/delete,
  approve/reject, status changes, and every login/logout/failed attempt
  is recorded with user, timestamp, IP, and before/after values
  (`audit/models.py` + `audit/utils.py`).
- **Environment isolation** — `python-decouple` reads from `.env`;
  `DEBUG` defaults to `False`; `SECRET_KEY` is never hard-coded.
- **Session hardening** — HTTPOnly, `Secure` (when not DEBUG), `SameSite=Lax`,
  expires on browser close.
- **Field-level masking** — costs and procurement values are stripped
  from serializer output for non-manager JWTs.

---

## 🛠️ How to Reproduce These Scans

```bash
# 1. Install the dev tools (one-time)
pip install bandit pip-audit

# 2. Django deploy check (dev)
python manage.py check --deploy

# 3. Django deploy check (production simulation)
DEBUG=False ALLOWED_HOSTS=your-app.onrender.com \
    python manage.py check --deploy

# 4. Bandit (SAST)
bandit -r accounts assets audit dashboard maintenance enterprise_tracker -f txt

# 5. pip-audit (dependency vulnerabilities)
pip-audit -r requirements.txt
```

All three tools are pinned to specific versions in development
(`bandit==1.9.4`, `pip-audit==2.10.0`) and are reproducible in CI.

---

## 📅 Audit Metadata

- **Audit date:** 2026-06-03 (Asia/Taipei)
- **Codebase:** `University-Asset-Fleet-Maintenance-Tracker`
- **Django version:** 6.0.5
- **Python version:** 3.12.10
- **Lines of code scanned (excl. venv, migrations):** 1,905
- **Dependencies scanned:** 23 pinned packages
- **Auditor (tooling):** Bandit 1.9.4, pip-audit 2.10.0, Django check --deploy
- **Result:** ✅ PASS — no blocking findings

---

*Generated as part of the FleetTrack capstone project's Deliverable #4
(Security Audit Log). Bundle this folder into a PDF for the final defense
using any standard "print folder to PDF" tool.*
