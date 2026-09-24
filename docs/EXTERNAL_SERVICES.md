# DBERT Internship Portal — External Services Inventory (INV-004)

**Document Date:** 2026-09-23  
**Scope:** Third-party integrations, external APIs, egress dependencies, and infrastructure fallbacks.

---

## 1. Inventory Matrix

| Service | Provider | Purpose | Credentials Location | Timeout | Failure Mode | Staging Safe? |
|---|---|---|---|---|---|---|
| **Transactional Email** | SMTP (Gmail) / AWS SES / cPanel Relay | OTPs, Status alerts, Offer letters | `.env`: `SMTP_*`, `CPANEL_*`, `AWS_*` | 10s | Logged to `email_log`, non-fatal | Yes (`EMAILS_ENABLED=false`) |
| **Generative AI** | Google Gemini (`gemini-1.5-flash`) / OpenAI | AI Interview & Guided Learning tutor | `.env`: `GEMINI_API_KEY`, `OPENAI_API_KEY` | 15s | Returns fallback questions / apology | Yes (mock/free tier) |
| **Anti-Bot / CAPTCHA** | Cloudflare Turnstile | Prevent form spam & brute force | `.env`: `TURNSTILE_SECRET`, `TURNSTILE_SITE_KEY` | 8s | Fails OPEN (Audit finding P0-3) | Yes (`TURNSTILE_ENABLED=false`) |
| **Web Push** | OneSignal REST API | Browser push alerts for events | `.env`: `ONESIGNAL_APP_ID`, `ONESIGNAL_REST_API_KEY` | 5s | Non-blocking warning log | Yes (dummy app ID) |
| **Analytics** | Google Analytics 4 (GA4) | Funnel tracking & conversion attribution | `.env`: `GA4_ID`, `GA4_API_SECRET` | 5s | Silent failure | Yes (staging GA4 tag) |
| **Payment Gateway** | Manual UPI QR / Dynamic Intent | Enrollment deposits (₹499 / ₹1599) | `.env`: `UPI_ID`, `UPI_AMOUNT` | N/A | Human verification in Admin queue | Yes (test UPI ID) |
| **File Storage** | Local File System (`uploads/`) | Resumes, receipts, certificates | `.env`: `UPLOAD_FOLDER` (default `uploads/`) | OS IO | Returns 400 Bad Request / 500 | Yes (isolated staging dir) |

---

## 2. Detailed Service Specifications

### 2.1 Email Infrastructure
- **Transports Supported:**
  1. `smtp`: Direct SMTP using Python's `smtplib.SMTP_SSL` or STARTTLS on port 587.
  2. `ses`: Amazon Simple Email Service via AWS SDK (`boto3`) on HTTPS port 443 (ideal when outbound SMTP ports are blocked).
  3. `cpanel_api`: REST relay via standalone `dbert-mailer` microservice.
- **Circuit Breaker / Master Toggle:**
  - `EMAILS_ENABLED=false`: When set to false, all emails are suppressed and logged as `SKIPPED` in `email_log`.
- **Known Risks:**
  - Currently, emails are sent synchronously within Flask request threads. A hanging SMTP socket blocks the worker.
  - *Phase 11 Target*: Implement transactional outbox / event-driven background email dispatch.

### 2.2 Generative AI Infrastructure
- **Integrations:**
  - `interview_submit` and `interview_start`: Evaluates candidate answers and generates follow-up technical questions.
  - `course_subtopic_chats`: Real-time contextual tutor for LMS lessons.
- **Failover & Resilience:**
  - If AI API is rate-limited or unreachable, returns deterministic curated questions.
  - Does not corrupt student state upon API timeout.

### 2.3 Cloudflare Turnstile Anti-Bot
- **Endpoints Protected:** `/apply`, `/intern/login`, `/company/signup`, `/company/login`.
- **Current Behavior:** Fails open when Cloudflare verification endpoint returns an exception or timeout.
- **Security Audit Note:** Audit item P0-3 identifies this as a potential bypass vulnerability. Phase 19 remediation will introduce strict retry with graceful throttling rather than blind fail-open.

### 2.4 OneSignal Web Push
- **Endpoints:** `/admin/push-test`, automated event triggers.
- **Payload:** User notification titles, action deep-links.
- **Isolation:** Failures are caught and logged; zero impact on core database transactions.

### 2.5 File Storage & Media
- **Storage Path:** Configurable via `UPLOAD_FOLDER`.
- **Validation Pipeline:**
  1. Extension whitelisting (`ALLOWED_EXT = {"png", "jpg", "jpeg", "pdf"}`).
  2. Content-length enforcement (`MAX_CONTENT_LENGTH = 6MB`).
  3. `secure_filename()` sanitization.
  4. Header magic-byte inspection (validates PDF `%PDF-`, PNG `\x89PNG`, JPEG `\xFF\xD8\xFF`).
- **Security Target (Phase 12):** Move sensitive payment receipts out of direct public document roots and enforce per-object RBAC authorization for downloads.
