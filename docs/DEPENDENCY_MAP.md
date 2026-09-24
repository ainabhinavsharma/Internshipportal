# DBERT Internship Portal — Dependency Map

**Document Date:** 2026-09-23  

---

## 1. Runtime Python Dependencies (`requirements.txt`)

| Package | Version | Purpose | Criticality |
|---|---|---|---|
| `flask` | `3.1.3` | Core WSGI web framework and request dispatching | Critical |
| `werkzeug` | `3.1.8` | WSGI utilities, proxy fix, password hashing (`scrypt`/`pbkdf2`) | Critical |
| `gunicorn` | `26.0.0` | Production WSGI HTTP server | Critical (Prod) |
| `python-dotenv` | `1.2.2` | Environment configuration loading (`.env`, `_env`) | Critical |
| `requests` | `2.34.2` | Outbound HTTP requests (Turnstile verification, OneSignal push) | High |
| `PyJWT` | `2.13.0` | Stateless token encoding & signature verification | High |
| `cryptography` | `50.0.0` | Fernet symmetric encryption for financial PII (UPI IDs) | High |
| `xhtml2pdf` | `0.2.17` | Server-side PDF rendering for intern CV builder | Medium |
| `boto3` | `1.43.56` | AWS SES email transport client (when configured) | Medium |
| `pandas` | `2.2.3` | Offline data migration & Excel import scripts | Low (Offline) |
| `openpyxl` | `3.1.5` | Excel format reading/writing | Low (Offline) |

---

## 2. Test & QA Dependencies (`requirements-dev.txt`)

| Package | Purpose |
|---|---|
| `pytest` (`>=8.0.0`) | Unit, functional, and integration test runner |
| `pytest-flask` (`1.3.0`) | Flask test client fixtures and request context bindings |
| `pytest-playwright` (`0.9.0`) | End-to-end browser automation for UI & user flows |
| `axe-playwright-python` (`0.1.8`) | Automated WCAG 2.1 AA accessibility auditing |

---

## 3. Frontend & Static Assets

| Library | Distribution | Purpose |
|---|---|---|
| `lenis.min.js` | Local static bundle (`/static/js/lenis.min.js`) | Smooth kinetic scrolling |
| `gsap.min.js` | Local static bundle (`/static/js/gsap.min.js`) | UI transitions and micro-animations |
| `ScrollTrigger.min.js` | Local static bundle (`/static/js/ScrollTrigger.min.js`) | Scroll-based interaction triggers |
| `csp-actions.js` | Local static bundle (`/static/js/csp-actions.js`) | Nonce-safe unobtrusive DOM event dispatcher |
| `dbert-theme.css` | Local static bundle (`/static/css/dbert-theme.css`) | Primary glassmorphism design system |
