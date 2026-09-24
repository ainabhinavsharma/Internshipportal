# DBERT Internship Portal — UI/UX + Security Audit & Remediation Plan

**Repository audited:** `https://github.com/ainabhinavsharma/Internshipportal`  
**Branch reviewed:** `main`  
**Repository type:** Monolithic Flask + SQLite + server-rendered Jinja + Vanilla JS/CSS  
**Audit perspectives:**
1. UI/UX / product experience audit
2. Application security / privacy / reliability audit

**Primary audience:** Local coding agent / senior developer responsible for remediation.

---

## 0. Executive Summary

This repository is not a simple internship landing page. It is a fairly large monolithic platform containing:

- Intern authentication and profiles
- Company accounts and job/internship posting
- Admin/staff operations
- Applications and enrollment workflows
- Payments/deposit verification
- Courses, quizzes, projects and learning progress
- Mentor booking
- Messaging
- Referral/coin systems
- AI interview functionality
- CV generation
- Notifications/email
- Device tracking
- CSV import/export
- SSO/token functionality
- Multiple legacy compatibility routes

The current implementation already contains several deliberate security improvements: database-backed sessions, CSRF enforcement, rate limiting, password-hash migration, nonce-based CSP, upload magic-byte checking, admin authorization checks and production startup guards.

However, the application is still at a point where **security correctness and product UX are highly dependent on a large 11k+ line monolithic `app.py` and dozens of templates/scripts**. That creates a high regression risk.

The most important findings are:

### Critical / P0

1. **`/generate-tutor-token` is functionally broken and must be repaired or removed.**
   The route references `course_id` without defining it and therefore cannot correctly perform its stated SSO operation. More importantly, the route's current behavior does not visibly perform the `_intern_payment_verified()` authorization gate documented immediately above it.

2. **Production configuration contains intentionally dangerous development fallbacks.**
   The source contains fallback secrets/default admin credentials and a development secret. Production guards reduce the risk, but the design is unnecessarily dangerous and makes configuration mistakes possible.

3. **Turnstile fails open.**
   When Turnstile is enabled but Cloudflare verification fails, the function returns `True`. This means an availability failure in an anti-bot control becomes a security bypass.

4. **Admin/session authorization is duplicated and includes a legacy session path.**
   `require_admin()` accepts either the current user role or `session["admin_id"]`. This creates two authentication authorities that can drift apart and makes the security model harder to reason about.

### High / P1

5. **Legacy authentication compatibility remains broader than necessary.**
   The app accepts a legacy auth cookie and a custom `X-Session-Token` header. This increases attack surface and complicates logout/session invalidation.

6. **Admin endpoints return very broad datasets.**
   Examples include `SELECT *` from mentors/devices and user data aggregation. Even though these routes are admin-protected, returning unnecessary columns increases the blast radius of an admin-session compromise and risks accidental exposure in browser tooling/logging.

7. **Admin UI displays newly generated/reset passwords in the browser.**
   The admin panel contains code that displays generated/reset passwords directly in the UI. This is a sensitive secret-handling anti-pattern.

8. **Payment screenshots and other user uploads require stronger isolation.**
   Extension + magic-byte checks are good, but uploaded files are stored in a generic upload directory. The design should enforce storage outside the web root, content-type headers, download disposition and per-object authorization.

9. **The public application exposes a large amount of marketing/claim content that needs product/legal consistency review.**
   Examples include “guaranteed placement opportunity”, “95%”, “10K+”, “MSME-registered”, “refundable security deposit”, and “offer letter within 2 hours”. These should be backed by a single source of truth rather than hardcoded independently across templates.

10. **The homepage has substantial visual complexity but weak information hierarchy around the actual application journey.**
    The current page looks polished, but the user journey is interrupted by multiple navigation destinations, paid-program messaging, jobs, courses, tasks, mentor booking, sign-up and FAQs before the primary conversion path is fully understood.

---

# 1. Audit Method and Scope

## 1.1 Evidence reviewed

Primary repository evidence:

- `app.py`
- `.env.example`
- `templates/index.html`
- `templates/_head.html`
- `templates/portal.html`
- `templates/admin.html`
- repository README and project structure
- live homepage at `https://internship.dbert.online/`

The GitHub repository identifies itself as a Flask-based monolithic internship platform with multi-role dashboards, application pipeline, LMS, AI interview system, referrals, messaging, CV generation and security controls.

The current `app.py` is approximately 11,765 lines and the repository contains 60+ templates according to the README. This is an important architectural finding: even small changes can have cross-feature effects.

## 1.2 Important limitation

This is a **static source + live public-surface audit**, not a full authenticated penetration test.

The following should therefore be treated as:

- **Confirmed source-level findings** when directly observable in code.
- **High-confidence risks** where the architecture strongly indicates a problem.
- **Verification tasks** where an authenticated runtime test is required.

Do not tell the remediation agent that an unverified exploit is definitely exploitable. It should reproduce each finding with tests before changing behavior.

---

# 2. Risk Rating

| Priority | Meaning | Required action |
|---|---|---|
| P0 | Critical security, data-loss, auth or payment risk | Fix before production |
| P1 | High security, privacy, broken workflow or severe UX issue | Fix in next release |
| P2 | Medium risk / important reliability or UX issue | Fix during hardening |
| P3 | Quality, accessibility, maintainability or polish | Fix progressively |

---

# 3. UI/UX Audit

## 3.1 Overall product impression

The public homepage has a modern visual language:

- dark/cosmic visual treatment
- glassmorphism
- amber/indigo accents
- large hero imagery
- animated interactions
- domain cards
- FAQ accordion
- paid-program section

The repository itself describes the visual stack as Lenis, GSAP/ScrollTrigger, spotlight cards, aurora backgrounds and magnetic CTA buttons.

The problem is not lack of visual polish.

The problem is **product hierarchy**.

The portal currently behaves like several products placed into one application:

- internship application platform
- jobs marketplace
- courses/LMS
- micro-task platform
- mentor booking platform
- paid training program
- referral/coins system
- AI interview system
- messaging platform

For a first-time student, this can create cognitive overload.

### UX principle to enforce

Every page should answer three questions within the first screen:

1. Where am I?
2. What can I do here?
3. What is the next best action?

The current system frequently answers #2 and #3 less clearly than it could.

---

# 4. Homepage UX Findings

## UX-001 — Too many competing navigation destinations

**Priority:** P1

The homepage navigation contains:

- Home
- Courses & Learning
- Micro-Tasks
- Book Mentor
- Internships
- Jobs
- Benefits
- FAQ
- Search
- Sign In
- Sign Up

This is too much for the top navigation of a student acquisition page.

### Why it matters

The primary conversion is application.

Every additional destination competes with:

> Sign Up Free → Explore Roles → Apply

### Fix

Use a two-level information architecture:

**Primary navigation**

- Internships
- Jobs
- Courses
- Mentors
- FAQ

**Primary CTA**

- Apply Now

**Secondary**

- Sign In

Move Micro-Tasks, Coins, Leaderboard, Notifications, etc. into the authenticated portal.

---

# 5. UX-002 — Paid program competes with free internship conversion

The homepage places a large paid-program banner immediately after domain discovery.

This is commercially understandable, but from a UX perspective it introduces a major decision before the student has completed the free-program mental model.

### Recommended flow

1. Discover internship
2. Understand role
3. Apply free
4. Track application
5. Only then surface accelerated/paid options when relevant

Do not make the free user feel that the platform is primarily selling a paid program.

---

# 6. UX-003 — Static numbers create trust risk

The homepage contains hardcoded values such as:

- 120+ openings
- 95+ openings
- 110+ openings
- 80+ openings
- 75+ openings
- 10K+ students
- 95% better career opportunities

These values appear to be presentation content rather than data-driven metrics.

### Fix

Create a single backend-controlled metrics object.

Example:

```python
PUBLIC_METRICS = {
    "active_students": ...,
    "active_roles": ...,
    "domains": ...,
    "completion_rate": ...
}
```

Only show metrics that can be verified.

If a metric is unavailable, remove it.

Do not manufacture social proof.

---

# 7. UX-004 — Application funnel is long and multi-step

The live signup flow contains:

1. Account
2. Academics
3. Profile
4. Quick questions
5. Submission

This is reasonable, but the form asks for a large amount of information before the applicant has experienced any value.

### Fix

Split fields into:

### Step 1 — Minimum account

- Name
- Email
- Phone
- Password
- Consent

### Step 2 — Eligibility

- City
- College
- Course
- Semester
- Graduation year

### Step 3 — Profile

- Why join?
- LinkedIn
- GitHub
- Portfolio

### Step 4 — Preferences

- Career start
- Skill-building
- Internship preference

Make Step 1 immediately useful and save progress after every step.

---

# 8. UX-005 — “Offer letter within 2 hours” is a dangerous expectation

The live application UI says:

> Takes 2 minutes · Offer letter within 2 hours of enrollment

This is a very strong promise.

If operationally inaccurate, it damages trust and creates support load.

### Fix

Replace with a service-level statement only if the operations team can actually meet it.

Example:

> Applications are reviewed on a rolling basis. You’ll receive an email when your status changes.

---

# 9. UX-006 — Accessibility gaps

The system uses icons extensively.

Positive examples exist: hamburger buttons and several controls have `aria-label`.

But the overall portal should be audited systematically for:

- keyboard navigation
- focus visibility
- focus trapping in auth modals
- ESC-to-close modal behavior
- semantic headings
- button vs div interaction
- screen-reader state updates
- form error association
- accessible tabs
- accessible dialogs
- reduced-motion support

The portal uses clickable `<div>` navigation elements in places.

Example:

```html
<div class="nav-item"
     data-tab="editprofile"
     data-act-click="switchTab">
```

This should normally be a `<button>` when it changes UI state.

### Fix

Use:

- `<button>` for actions
- `<a>` for navigation
- ARIA only when native semantics are insufficient

---

# 10. UX-007 — Excessive inline styles

The portal contains many inline style attributes.

Example patterns include:

```html
style="display:none;"
style="color:var(--tx-muted);..."
style="display:flex;..."
```

This creates:

- inconsistent design tokens
- harder responsive tuning
- harder theme changes
- larger HTML
- weaker maintainability

### Fix

Move repeated styles to semantic classes:

```css
.is-hidden { display: none !important; }
.text-muted { color: var(--tx-muted); }
.stack-row { ... }
```

---

# 11. UX-008 — Loading states need skeletons

The portal initially displays:

> Loading your portal...

A spinner alone is poor UX for a data-heavy dashboard.

### Fix

Create skeleton states for:

- profile
- applications
- messages
- notifications
- courses
- leaderboard
- certificates

The page should progressively reveal usable content rather than waiting for the entire portal state.

---

# 12. UX-009 — Error handling should preserve user context

The application contains many generic responses such as:

> Error

or

> Server error

These are safe from an information disclosure perspective, but poor for UX.

### Use two layers

Server:

```json
{
  "status": "error",
  "code": "APPLICATION_UPDATE_FAILED",
  "message": "Unable to update application."
}
```

UI:

> We couldn't update your application. Your previous information is still safe. Please try again.

Never expose stack traces.

---

# 13. UX-010 — Messaging UI needs stronger conversation semantics

The portal messaging UI uses an inbox + thread model, which is good.

However, it should include:

- sender name
- timestamp
- read/unread state
- delivery state where applicable
- message length feedback
- send failure state
- retry
- connection state
- empty-state guidance
- mobile keyboard behavior
- conversation title/context

The current message rendering escapes message body, which is good security-wise, but the UI should not feel like a raw chat stream.

---

# 14. UX-011 — Mobile navigation is too dense

The portal sidebar has many entries:

- Apply
- Applications
- CV
- Interview
- Paid Program
- Coins
- Certificate
- Leaderboard
- Cohorts
- Messages
- Notifications
- Profile
- Password
- Mentor

This is too many first-class destinations.

### Recommended mobile information architecture

**Home**

- Application status
- Next action
- Current internship
- Progress

**My Work**

- Applications
- Tasks
- Courses
- Interview

**Career**

- CV
- Mentor
- Jobs

**Community**

- Messages
- Cohort
- Leaderboard

**Account**

- Profile
- Password
- Logout

---

# 15. UX-012 — Application status should be the central dashboard object

The portal should be status-first.

Instead of presenting a menu of features, the first screen should say:

> Your application: Under Review

Then:

- submitted date
- selected domain
- next step
- expected action
- documents
- messages
- interview status

This reduces cognitive load dramatically.

---

# 16. UX-013 — Payment UX needs exceptional trust design

The portal shows a UPI ID and ₹499 amount.

Because money is involved, the UX must include:

- exact recipient name
- exact amount
- payment purpose
- warning not to send extra money
- refund conditions
- verification timeline
- support contact
- transaction reference field
- status
- duplicate submission protection
- screenshot preview
- secure upload explanation

The current UI displays the UPI ID and amount, but this should be treated as a high-trust transaction screen rather than a normal form.

---

# 17. UX-014 — Dark visual system needs contrast audit

The design uses:

- `#07080E`
- `#0E111D`
- translucent surfaces
- amber
- electric indigo
- muted text

This can look excellent, but dark glass interfaces frequently fail WCAG contrast requirements.

### Required testing

Automate contrast checks for:

- body text
- placeholder text
- disabled text
- secondary labels
- badges
- buttons
- links
- error states
- success states
- focus rings

---

# 18. UX-015 — Motion should respect reduced-motion preferences

GSAP, Lenis, magnetic buttons, spotlight effects and scrolling effects can create accessibility and performance problems.

Add:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Also disable JS-driven smooth scrolling and nonessential parallax for reduced-motion users.

---

# 19. Security Audit

## SEC-001 — Development secret fallback exists in application code

**Priority: P1**

Evidence:

```python
app.secret_key = _FLASK_SECRET_KEY or "digitalblinc2026secretkey"
```

Although production startup guards attempt to stop deployment with the fallback, a hardcoded authentication secret should not exist in the application at all.

### Fix

Production:

```python
if not FLASK_SECRET_KEY:
    raise RuntimeError("FLASK_SECRET_KEY is required")
```

Development should use a generated local `.env` value, never a repository constant.

---

# 20. SEC-002 — Default admin credentials remain in code

**Priority: P1**

Evidence includes defaults for:

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `ADMIN_KEY`

The application attempts to refuse production startup if defaults remain.

That is good defense-in-depth, but the safest design is:

- no default password
- no default admin username
- no reusable admin key
- explicit bootstrap command

### Recommended

```bash
python manage.py create-admin
```

The command should:

1. generate a random temporary credential
2. require immediate password change
3. disable the bootstrap credential after first use

---

# 21. SEC-003 — `.env.example` contains production-looking email configuration

The example file includes:

```text
SMTP_USER=careers@dbert.online
```

Even if this is not a password, repository configuration should avoid mixing production identity with development examples.

### Fix

Use:

```text
SMTP_USER=your-email@example.com
```

and clearly label it as a placeholder.

---

# 22. SEC-004 — Turnstile fails open

**Priority: P0**

Evidence:

```python
except Exception as e:
    log_error("turnstile", e)
    return True
```

This is a security weakness.

If Turnstile is intended to be a bot-defense control, failure of the verifier must not silently authorize the request.

### Better policy

For security-sensitive operations:

```python
except Exception:
    return False
```

For availability-sensitive flows, use a controlled fallback with rate limiting and logging.

Never silently fail open.

---

# 23. SEC-005 — Admin authorization has two authorities

**Priority:** P1

`require_admin()` accepts:

1. current database-backed session user
2. `session["admin_id"]`

This means two different authentication models coexist.

The second branch returns a synthetic user object:

```python
{
    "id": session.get("admin_id"),
    "role": "admin",
    ...
}
```

### Risk

Any code path that modifies Flask session state can potentially affect authorization.

### Fix

Use exactly one source of truth:

```text
auth cookie
   ↓
session token
   ↓
user_sessions
   ↓
role
   ↓
authorization
```

Remove `session["admin_id"]` authorization once compatibility migration is complete.

---

# 24. SEC-006 — Legacy auth cookie remains accepted

`get_session_token_from_request()` accepts:

- `dbert_auth`
- legacy `dbert_session`
- `X-Session-Token`

This is a broad compatibility surface.

### Risk

Every legacy path is another credential transport mechanism.

### Fix

Migration plan:

1. Stop issuing legacy cookie.
2. Log usage of legacy cookie.
3. Set sunset date.
4. Remove fallback.
5. Remove custom session header unless required by a trusted API client.
6. Use Authorization Bearer for mobile/API authentication where appropriate.

---

# 25. SEC-007 — Custom session token header increases credential exposure

Evidence:

```python
request.headers.get("X-Session-Token")
```

Browser credentials should generally remain in secure HTTP-only cookies for browser sessions.

Custom headers are appropriate for API clients but should use a separately scoped API access token.

### Fix

Do not accept the same browser session token through arbitrary transport mechanisms.

---

# 26. SEC-008 — Tutor SSO route is broken and requires immediate review

**Priority:** P0/P1 depending on product dependency.

The route:

```python
@app.route('/generate-tutor-token', methods=['POST'])
def generate_tutor_token():
    user = get_current_user()
    if not user:
        return ...
    return redirect(f"/courses/{course_id}")
```

`course_id` is not defined in the shown route.

This is a concrete functional defect.

More importantly, the immediately preceding `_intern_payment_verified()` helper describes the intended security gate for SSO token generation, but the shown route does not call it.

### Required action

Do not patch blindly.

First determine the intended flow:

```text
intern
  ↓
accepted/payment verified?
  ↓ yes
mint short-lived signed SSO token
  ↓
redirect to tutor
```

Then write a test proving:

- unpaid user → denied
- pending user → denied
- accepted user → token issued
- expired token → denied
- token replay → denied if one-time semantics are required
- token cannot be altered
- token cannot be used for another user

---

# 27. SEC-009 — Turnstile is optional and defaults OFF

The configuration says:

```python
TURNSTILE_ENABLED = ... "false"
```

This means the bot defense is normally disabled.

This is not automatically a vulnerability, because rate limiting exists, but public registration and application endpoints should have layered abuse protection.

### Recommended layered model

- IP rate limit
- account rate limit
- device/visitor anomaly detection
- signed timing token
- optional Turnstile
- email verification
- progressive friction

---

# 28. SEC-010 — `SELECT *` is overused in security-sensitive responses

Examples include:

```python
SELECT * FROM mentors
SELECT * FROM device_profiles
SELECT * FROM intern_accounts
```

This is dangerous for privacy and maintainability.

### Why

When a new column is added to a table, an existing API can accidentally start returning it.

That can turn a harmless migration into a data leak.

### Fix

Use explicit field lists:

```sql
SELECT id, name, email, domain, is_active, created_at
FROM mentors
```

Never expose:

- password hashes
- reset tokens
- internal authentication tokens
- API keys
- device secrets
- private payout information
- internal fraud metadata

---

# 29. SEC-011 — Admin mentor endpoint needs output allowlisting

The current mentor endpoint returns rows using:

```python
row_to_dict(r)
```

This is effectively schema-wide serialization.

### Fix

Create DTO/serializer functions:

```python
def mentor_admin_view(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "domain": row["domain"],
        "is_active": row["is_active"],
        "created_at": row["created_at"],
    }
```

---

# 30. SEC-012 — Admin users endpoint should never return authentication fields

The admin user aggregation starts with broad account rows.

It is essential to explicitly remove:

- `password_hash`
- `reset_token`
- API keys
- private identifiers
- device identifiers unless required
- internal anti-abuse fields

Do not rely on the template not rendering them.

The browser still receives JSON.

---

# 31. SEC-013 — Admin password reset displays generated password

Evidence in `templates/admin.html`:

```javascript
document.getElementById('newPwDisplay').textContent =
    'New PW: '+data.new_password;
```

This is a major secret-handling smell.

### Risk

The password can remain in:

- browser DOM
- screenshots
- screen recordings
- browser accessibility tree
- logs/debugging
- copied clipboard content
- support tickets

### Better design

Use a secure password setup link:

```text
Admin resets password
        ↓
one-time setup token
        ↓
user creates password
        ↓
token invalidated
```

Do not send or display passwords.

---

# 32. SEC-014 — Mentor creation also displays generated passwords

Evidence:

```javascript
msg.textContent =
    data.generated_password
        ? 'Saved. Password: '+data.generated_password
        : 'Mentor saved.';
```

Same issue as above.

### Fix

Replace generated password with:

> Mentor created. A password setup email has been sent.

If email is unavailable, require the admin to set a temporary password once and force a change on first login.

---

# 33. SEC-015 — File upload validation is good but incomplete

Positive controls:

- extension allowlist
- magic-byte sniffing
- UUID filename
- 6 MB global request limit

These are good.

But security still requires:

- storage outside public web root
- no executable interpretation
- response `Content-Disposition`
- response `X-Content-Type-Options: nosniff`
- authorization per object
- virus/malware scanning for PDFs
- PDF sanitization if PDFs are ever processed
- image decompression limits if images are transformed
- per-user quota
- upload count limits
- retention/deletion policy

---

# 34. SEC-016 — Payment screenshot endpoint must remain object-authorized

The admin screenshot route is protected by admin authorization and uses `secure_filename()`.

That is good.

But the long-term design should not make filename itself the authorization boundary.

Use:

```text
/admin/payments/{payment_id}/screenshot
```

Then:

1. load payment record
2. verify admin role
3. resolve internal storage key
4. stream file
5. set safe response headers

---

# 35. SEC-017 — Sensitive payment files need private storage

Do not store payment screenshots in a directory that could accidentally become static/public through future web-server configuration.

Recommended:

```text
storage/
  private/
    payments/
    resumes/
    certificates/
    identity/
```

Never serve these folders directly.

---

# 36. SEC-018 — CRON secrets in query strings are risky

Cron routes accept:

```python
request.args.get("key", "")
```

This means a secret may appear in:

- proxy logs
- browser history
- monitoring systems
- access logs
- analytics systems
- copied URLs

### Fix

Use only:

```http
X-Cron-Key: <secret>
```

or, preferably:

- HMAC-signed cron request
- cloud scheduler identity
- private network
- mTLS/service identity

Remove query-string secrets.

---

# 37. SEC-019 — IP extraction trust assumptions need infrastructure verification

The application uses ProxyFix and reads `X-Real-IP`.

This can be correct only if the reverse proxy overwrites the header.

The code comments explicitly assume Nginx does this.

### Required deployment test

Verify:

1. direct public access cannot reach Flask
2. only Nginx can reach Flask
3. Nginx overwrites `X-Forwarded-For`
4. Nginx overwrites `X-Real-IP`
5. attacker-supplied forwarding headers are discarded

If Flask is ever directly exposed, rate limits and audit logs can be manipulated.

---

# 38. SEC-020 — Rate limiting fails open on database errors

`login_locked()` catches DB errors and returns:

```python
(False, 0)
```

That means the system becomes less restrictive when the rate-limit datastore fails.

This is an availability/security tradeoff.

### Recommendation

For login protection:

- fail closed or apply a local emergency limiter
- use Redis or a dedicated shared rate-limit store in production
- avoid relying on SQLite for high-volume abuse controls

---

# 39. SEC-021 — SQLite is a scalability and security-control concern

SQLite with WAL is useful for small systems.

But this application has:

- messaging
- jobs
- courses
- payments
- admin operations
- analytics
- referrals
- device tracking
- rate limits

A production multi-worker deployment using SQLite increases:

- lock contention
- transaction complexity
- rate-limit consistency problems
- operational backup risk
- corruption/recovery complexity

### Recommended target

Move production data to PostgreSQL.

Keep SQLite only for:

- local development
- test fixtures
- disposable demos

---

# 40. SEC-022 — Database migrations inside application startup are risky

The README describes auto-initialization and migrations inside `app.py`.

This is convenient but dangerous when multiple production workers start simultaneously.

### Fix

Introduce explicit migrations:

```text
Alembic
    ↓
migration version
    ↓
deploy
    ↓
application
```

Never let every Gunicorn worker perform schema mutation during boot.

---

# 41. SEC-023 — Public email/account probing must be tested continuously

The `/check-email` endpoint is designed to reduce account enumeration.

It returns:

- `no_account`
- `no_password`
- `has_password`

For email input, that can still reveal account existence.

The comment says the reset flow was fixed to be neutral, but `/check-email` intentionally returns different states.

### Risk

An attacker can enumerate registered emails.

### Recommendation

If this endpoint is required for UX, replace the explicit account state with a generic response and let the next login step determine behavior.

For example:

```json
{
  "status": "success",
  "next": "continue"
}
```

Use stronger rate limiting and monitoring.

---

# 42. SEC-024 — Password reset flow should be tested for account-type confusion

The reset logic supports:

- intern
- company

and contains fallback behavior if the recorded account type does not update the expected table.

This is compatibility-friendly but security-sensitive.

### Required tests

- intern token cannot reset company account
- company token cannot reset intern account
- token cannot be reused
- expired token cannot be used
- malformed token cannot trigger DB errors
- email normalization cannot cross accounts
- reset invalidates every previous session
- reset does not automatically grant an unintended role

---

# 43. SEC-025 — Login throttling must be tested against distributed attacks

Current limits include IP and identity buckets.

That is good, but attackers can rotate:

- IP
- user agents
- devices
- networks

Add:

- per-account exponential backoff
- suspicious login detection
- device reputation
- CAPTCHA after threshold
- optional email verification

Do not rely only on IP.

---

# 44. SEC-026 — JWT dependency requires algorithm pinning audit

`jwt` is imported, but the static review should verify every JWT decode/encode call.

The agent must ensure:

```python
jwt.decode(
    token,
    secret,
    algorithms=["HS256"],
    audience=EXPECTED_AUDIENCE,
    issuer=EXPECTED_ISSUER,
)
```

Never accept an algorithm from the token.

Never use an unbounded `decode()`.

---

# 45. SEC-027 — AI API key handling needs strict isolation

Gemini keys are loaded server-side and the comments explicitly say they must never reach the browser.

This is good.

Required tests:

- browser cannot retrieve environment variables
- API responses never contain Gemini keys
- logs never contain Gemini keys
- exception messages never contain Gemini keys
- prompt failures do not expose request headers
- admin exports do not include keys

---

# 46. SEC-028 — GitHub token requires least privilege

`GITHUB_TOKEN` is loaded from environment.

Ensure the token:

- has only required repository scopes
- is not sent to browser
- is not logged
- is not embedded into AI prompts
- is not returned by debug endpoints
- is rotated regularly

Prefer GitHub App credentials over a long-lived personal access token where practical.

---

# 47. SEC-029 — Logging currently records IP and path globally

Structured logs include:

- request ID
- IP
- path
- security event details

This is useful operationally.

But log privacy must be explicit.

### Never log

- passwords
- reset tokens
- auth tokens
- CSRF tokens
- API keys
- payment credentials
- full uploaded documents
- sensitive application answers

### Consider

- hashing/pseudonymizing IP for long-term analytics
- short retention for raw security logs
- access controls on log storage

---

# 48. SEC-030 — Request ID is client-influenced

The code uses:

```python
request.headers.get("X-Request-ID", str(uuid.uuid4()))
```

This is acceptable for correlation only if treated as untrusted input.

### Fix

Validate:

- length
- allowed characters
- maximum size

Or always generate the canonical request ID server-side and preserve an incoming ID only as a separate `traceparent`/correlation field.

---

# 49. SEC-031 — CSP is good but still permissive in important areas

The CSP includes:

```text
style-src 'self' 'unsafe-inline'
img-src 'self' data: https:
```

The nonce-based script CSP is a strong improvement.

However:

- `unsafe-inline` remains for styles
- `img-src https:` allows images from any HTTPS origin
- third-party script sources are trusted
- Google/OneSignal/Cloudflare dependencies expand supply-chain exposure

### Next hardening step

Move toward:

```text
style-src 'self' 'nonce-...'
```

or eliminate inline styles.

Use explicit image domains instead of all HTTPS.

---

# 50. SEC-032 — Third-party JavaScript is part of the trust boundary

The homepage uses:

- OneSignal
- Google Tag Manager/Analytics
- Cloudflare Turnstile
- external fonts/CDN assets

Each external origin can affect privacy, availability or supply-chain posture.

### Fix

Maintain a third-party dependency inventory:

| Provider | Purpose | Data | Required? | Risk |
|---|---|---|---|---|
| OneSignal | Push | browser/device identifiers | Yes/No | Medium |
| GA4 | Analytics | behavioral telemetry | Yes/No | Medium |
| Cloudflare | bot defense | IP/challenge data | Yes | Medium |
| Fonts/CDN | UI | request metadata | Optional | Low |

Remove anything that is not necessary.

---

# 51. SEC-033 — User-controlled URLs need stronger normalization

The app validates URLs with a regex.

That is not enough for all security contexts.

For external links:

- parse with `urllib.parse`
- require `https`
- reject credentials in URL
- reject `javascript:`
- reject `data:`
- normalize hostname
- optionally restrict known social domains

Do not treat a regex as a complete URL security policy.

---

# 52. SEC-034 — HTML escaping strategy must remain consistent

The code imports:

```python
Markup
escape
```

and the message UI uses `escHtml()` before inserting message content.

This is good.

However, because the application uses many templates and dynamic JS, the agent must run a complete sink audit for:

- `innerHTML`
- `outerHTML`
- `insertAdjacentHTML`
- `document.write`
- `eval`
- `Function`
- URL construction
- template literals with server data

Every dynamic value needs an explicit output context.

---

# 53. SEC-035 — Do not trust `clean_text()` as an XSS defense

`clean_text()` converts values to strings and strips whitespace.

It is not sanitization.

The agent must treat:

```python
clean_text(value)
```

as normalization only.

Use context-specific output encoding.

---

# 54. SEC-036 — CSV import/export needs formula injection protection

The app supports CSV import/export.

For exported spreadsheets, attacker-controlled cells beginning with:

```text
=
+
-
@
```

can become spreadsheet formulas.

### Fix

When generating CSV:

- prefix dangerous values with `'`
- or escape according to spreadsheet-safe export policy

For CSV import:

- validate headers
- validate field counts
- limit rows
- limit field lengths
- reject unexpected formulas if re-exported

---

# 55. SEC-037 — CSV imports require transactional rollback

CSV imports can modify large amounts of application data.

Ensure:

```text
validate entire file
        ↓
begin transaction
        ↓
write all rows
        ↓
commit
```

or use chunked transactions with explicit failure recovery.

Never leave half-imported administrative data without a visible import report.

---

# 56. SEC-038 — Admin destructive operations need explicit confirmation

The admin interface contains operations such as:

- suspend company
- delete mentors
- delete devices
- application status changes
- payment verification
- CSV import

These need:

- confirmation dialogs
- impact summary
- undo where possible
- audit event
- actor identity
- timestamp
- before/after state

---

# 57. SEC-039 — Security-sensitive state transitions need server-side state machines

The repository correctly describes application statuses as a state machine.

Continue enforcing this at the backend.

Never trust the client to choose:

```text
Accepted
Enrolled
Paid-Enrolled
Selected
```

Every transition should validate:

```text
current_state
+
actor_role
+
actor_resource
+
business_conditions
→
allowed_transition
```

---

# 58. SEC-040 — Payment verification must be idempotent

Payment and enrollment operations should have a unique idempotency key.

The repository already uses idempotency concepts in referral processing.

Apply the same principle to:

- deposits
- course payments
- enrollment
- application transitions
- webhook-like actions

Double-clicking a button must never create two financial records.

---

# 59. SEC-041 — Payment amount must be server-authoritative

Never accept amount from the browser.

The browser may submit:

```json
{
  "amount": 1
}
```

but the server must derive:

```python
amount = UPI_AMOUNT
```

from authoritative server configuration and the selected transaction type.

---

# 60. SEC-042 — File upload must bind object ownership before saving

For every uploaded file:

```text
authenticate
→ validate ownership
→ validate business state
→ validate file
→ save
→ commit DB record
```

Never:

```text
save file
→ later discover user is not authorized
```

---

# 61. SEC-043 — Device fingerprinting creates privacy obligations

The application has device profiles and referral overlap detection.

This can be legitimate anti-fraud functionality.

But it should have:

- privacy notice
- retention policy
- purpose limitation
- admin access controls
- deletion policy
- documented legal basis where applicable

Do not collect more fingerprinting data than necessary.

---

# 62. SEC-044 — Referral fraud signals must not become permanent user labels

The code flags shared-device relationships for review rather than automatically blocking them. That is a good design.

Keep it that way.

Shared computers are normal for:

- campuses
- cyber cafes
- families
- libraries

Fraud signals should be evidence, not automatic guilt.

---

# 63. SEC-045 — Admin security dashboard must itself be protected against privacy overexposure

The abuse log includes:

- IP
- route
- bucket
- reason
- email

This is sensitive security telemetry.

Ensure:

- only authorized security/admin roles can see it
- no client-side filtering exposes more data than necessary
- export is restricted
- retention is defined
- email is masked in UI where full value is not needed

---

# 64. SEC-046 — Admin role should be separated from staff roles

The application has staff/admin concepts.

Do not let one `admin` role control everything indefinitely.

Introduce RBAC:

```text
super_admin
security_admin
application_reviewer
finance_admin
mentor_admin
content_admin
support_agent
```

Example:

A support agent should not be able to:

- download payment screenshots
- reset passwords
- export all users
- change enrollment state

---

# 65. SEC-047 — Principle of least privilege for admin API responses

Every admin endpoint should answer:

> What is the minimum data this screen actually needs?

Do not return entire database rows.

---

# 66. SEC-048 — Security regression tests need to become first-class

The repository contains tests, but security should have explicit regression tests for every historical fix.

Create:

```text
tests/security/
    test_auth.py
    test_csrf.py
    test_sessions.py
    test_admin_authz.py
    test_uploads.py
    test_password_reset.py
    test_rate_limits.py
    test_payment.py
    test_sso.py
    test_xss.py
    test_csv.py
```

---

# 67. Likely Bugs / Regression Hotspots

## BUG-001 — `/generate-tutor-token`

**Confirmed source-level defect.**

Undefined `course_id` reference.

**Expected:** either receive/validate a course ID or remove the route.

---

## BUG-002 — Portal loading regression history

The code comments explicitly describe a previous `/intern/me` crash caused by querying a non-existent `company_name` column.

This is evidence that the monolithic architecture has already produced cross-schema regressions.

### Recommendation

Introduce:

- typed data access layer
- schema tests
- integration tests for every portal API
- startup schema validation

---

## BUG-003 — Pagination inputs are directly converted

The courses route contains:

```python
page = int(request.args.get("page", 1))
per_page = int(request.args.get("per_page", 20))
```

Malformed query parameters can produce exceptions.

### Fix

Use a safe parser:

```python
page = clamp_int(request.args.get("page"), 1, 100000, 1)
per_page = clamp_int(request.args.get("per_page"), 1, 100, 20)
```

---

## BUG-004 — Public `/mentor` page should be reviewed

The route renders the mentor page without a visible role guard.

This may be intentional if it is a public booking/marketing page.

Confirm that it does not expose:

- mentor email addresses
- internal availability metadata
- admin-only information
- inactive mentors
- private booking identifiers

---

# 68. Potential Planted-Bug / Backdoor Review

No intentional malicious backdoor can be proven from static inspection alone.

However, the local agent should specifically audit suspicious patterns because the repository has evolved through many phases and compatibility patches.

Search for:

```text
eval(
exec(
compile(
__import__(
subprocess
os.system
popen(
pickle.loads
yaml.load(
requests.get(
requests.post(
base64.b64decode(
marshal.loads(
```

Also search for:

```text
if username == ...
if password == ...
if request.args.get("key")
if request.headers.get(...)
```

and hardcoded:

```text
secret
token
password
api_key
private_key
admin
bypass
debug
backdoor
test
temporary
legacy
migration
```

A special review is required for any code that:

- grants admin
- grants payment status
- creates SSO tokens
- changes application state
- disables verification
- bypasses CSRF
- disables Turnstile
- changes role
- marks payment verified
- creates staff accounts

---

# 69. Hardcoded Production Values Audit

The code contains production-looking defaults including:

- OneSignal app ID
- UPI ID
- GA4 measurement ID
- AdSense publisher ID
- production site origin
- SMTP sender

Not all of these are secrets.

Classify every environment value as:

### Public configuration

Safe to expose:

- site origin
- analytics ID
- public OneSignal app ID
- public publisher ID

### Secret configuration

Never commit:

- Flask secret
- admin password
- cron secret
- Gemini API key
- GitHub token
- SMTP password
- Fernet key
- AWS credentials
- CPANEL API key
- Turnstile secret
- GA API secret

---

# 70. Security Headers Checklist

Add and verify:

```http
Content-Security-Policy
Strict-Transport-Security
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

Potentially:

```http
Cross-Origin-Embedder-Policy
```

only after compatibility testing.

---

# 71. Cookie Policy

Target:

```text
HttpOnly = true
Secure = true
SameSite = Lax/Strict
Path = /
```

For high-risk operations, consider requiring reauthentication.

Add session rotation after:

- login
- password reset
- privilege elevation

Ensure old session IDs are invalidated.

---

# 72. Password Policy

Minimum 8 characters is better than nothing, but for a professional system:

- minimum 12 recommended
- breached-password screening
- no forced complexity rules that harm usability
- rate-limited authentication
- secure password reset
- no plaintext temporary passwords
- no admin-displayed passwords

---

# 73. AI Interview Security

The AI interview is a high-risk feature because it processes candidate-generated content.

Threat model:

```text
candidate input
     ↓
server
     ↓
prompt
     ↓
Gemini
     ↓
AI response
     ↓
candidate/admin
```

Required controls:

- prompt injection resistance
- output validation
- length limits
- HTML escaping
- no tool execution based on candidate text
- no secret inclusion in prompts
- no raw model response inserted as HTML
- audit logs without candidate-sensitive content
- per-user interview attempt limits

---

# 74. AI Cost Abuse

Current interview controls include attempt and IP limits.

Add:

- per-account daily token budget
- per-IP daily budget
- maximum prompt size
- maximum response size
- total request timeout
- circuit breaker
- API-key rotation/failover
- spend alerts

Do not let a single account exhaust all Gemini keys.

---

# 75. Database Security

## Required constraints

Every important relationship should have:

- foreign keys
- indexes
- unique constraints
- CHECK constraints where appropriate

Examples:

```sql
UNIQUE(email)
UNIQUE(referral_code)
UNIQUE(post_application_id)
UNIQUE(idempotency_key)
```

---

# 76. Race Conditions

Every state transition involving money or enrollment must be transactionally safe.

Bad pattern:

```text
SELECT status
if eligible:
    INSERT payment
```

Two requests can pass simultaneously.

Use:

```text
BEGIN
SELECT ... FOR UPDATE equivalent / transaction lock
verify state
write transition
COMMIT
```

SQLite limitations should be explicitly considered.

---

# 77. UX + Security Combined Risk: Trust

The portal handles:

- student identity
- college information
- phone numbers
- email
- resumes
- payment screenshots
- career applications
- AI interview responses
- device information

This means the UI must communicate security clearly.

Recommended trust UI:

- “Your data is encrypted in transit”
- “We never ask for your password over WhatsApp”
- “Payment status is verified by DBERT”
- “We will never ask you to send money to a personal account”
- clear support contact
- privacy policy
- terms
- refund policy

Only show claims that are operationally true.

---

# 78. Recommended Architecture Refactor

Do not rewrite the whole application at once.

Use strangler architecture.

Current:

```text
app.py
 ├── auth
 ├── admin
 ├── company
 ├── intern
 ├── payments
 ├── courses
 ├── mentor
 ├── messaging
 ├── referrals
 ├── AI
 ├── analytics
 └── utilities
```

Target:

```text
app/
├── __init__.py
├── config.py
├── extensions.py
├── auth/
│   ├── routes.py
│   ├── service.py
│   ├── models.py
│   └── security.py
├── interns/
├── companies/
├── applications/
├── payments/
├── courses/
├── mentors/
├── messaging/
├── referrals/
├── interviews/
├── admin/
├── uploads/
├── analytics/
├── templates/
├── static/
└── tests/
```

Use Flask Blueprints.

---

# 79. Phase-Based Remediation Plan

## Phase 0 — Freeze and Baseline

### Goals

- no new feature work
- reproduce current flows
- create security baseline

### Tasks

- install dependencies
- run unit tests
- run application locally
- create test accounts for each role
- document all routes
- capture screenshots of public, intern, company and admin pages
- export current DB schema
- run static security scans

### Deliverables

```text
docs/
  ROUTE_INVENTORY.md
  DATA_CLASSIFICATION.md
  SECURITY_BASELINE.md
```

---

# 80. Phase 1 — P0 Security

Fix first:

1. Tutor SSO route
2. Turnstile fail-open
3. hardcoded auth secret fallback
4. default admin credential architecture
5. session authority duplication
6. payment-state authorization
7. secret transport through query strings

### Acceptance

No critical security test fails.

---

# 81. Phase 2 — Authentication Hardening

Implement:

- one auth authority
- secure session rotation
- strict session expiration
- role-based authorization middleware
- password reset tests
- account enumeration mitigation
- login throttling
- password policy
- forced password change flow

---

# 82. Phase 3 — File & Payment Security

Implement:

- private storage
- upload service
- MIME/magic validation
- virus scan integration
- authorization by object
- download headers
- payment idempotency
- payment state machine
- audit events

---

# 83. Phase 4 — Admin Security

Implement RBAC:

```text
Super Admin
Security
Finance
Applications
Mentors
Content
Support
```

Remove password display.

Replace reset-password with setup links.

Add audit trail:

```text
actor
action
target
before
after
timestamp
request_id
ip
```

---

# 84. Phase 5 — Data Privacy

Classify:

### Public

- job titles
- domains
- company names
- course titles

### Internal

- application status
- mentor assignments
- internal notes

### Confidential

- phone
- email
- CV
- interview answers

### Highly sensitive

- passwords
- payment documents
- tokens
- API keys
- financial payout details

Create a retention policy for each.

---

# 85. Phase 6 — UX Redesign

Redesign around the student journey.

### Public

```text
Home
  ↓
Explore Internship
  ↓
Role Detail
  ↓
Apply
```

### Authenticated

```text
Dashboard
  ↓
Application Status
  ↓
Next Action
  ↓
Learning / Interview / Mentor
```

Make everything else secondary.

---

# 86. Phase 7 — Accessibility

Run:

- axe-core
- Lighthouse
- keyboard-only testing
- screen-reader testing
- WCAG contrast audit

Targets:

- WCAG 2.2 AA
- keyboard complete
- focus visible
- reduced motion
- semantic HTML

---

# 87. Phase 8 — Performance

Audit:

- JS bundle sizes
- image sizes
- font loading
- third-party scripts
- GSAP usage
- Lenis usage
- layout shifts
- long tasks

Target:

- LCP < 2.5s
- CLS < 0.1
- INP < 200ms

Test mobile 4G, not just desktop broadband.

---

# 88. Phase 9 — Database Migration

Move production workload to PostgreSQL.

Use:

- SQLAlchemy or a disciplined repository/data-access layer
- Alembic migrations
- connection pooling
- transaction boundaries
- indexes
- foreign keys

Keep SQLite for local development only if desired.

---

# 89. Phase 10 — Automated Security Gates

CI should run:

```bash
pytest
ruff
bandit
pip-audit
semgrep
```

Frontend:

```bash
npm audit
eslint
```

Also add:

- secret scanning
- dependency scanning
- SBOM generation
- container scan if containerized

---

# 90. Required Security Test Matrix

## Authentication

- [ ] invalid password
- [ ] invalid email
- [ ] brute force
- [ ] session fixation
- [ ] session replay
- [ ] logout invalidates token
- [ ] password reset invalidates sessions
- [ ] role escalation
- [ ] legacy cookie rejection after migration

## Authorization

- [ ] intern cannot access company data
- [ ] company cannot access intern private data
- [ ] mentor cannot access another mentor's data
- [ ] support role cannot access payments
- [ ] admin endpoints require admin
- [ ] resource ownership is checked

## CSRF

- [ ] all POST/PUT/PATCH/DELETE protected
- [ ] JSON protected
- [ ] multipart protected
- [ ] file uploads protected
- [ ] cron is authenticated separately
- [ ] GET cannot mutate state

## Uploads

- [ ] fake extension
- [ ] wrong magic bytes
- [ ] oversized file
- [ ] path traversal
- [ ] duplicate filename
- [ ] SVG
- [ ] malicious PDF
- [ ] HTML disguised as image
- [ ] unauthorized download

## XSS

- [ ] application notes
- [ ] company descriptions
- [ ] job descriptions
- [ ] mentor messages
- [ ] chat messages
- [ ] profile URLs
- [ ] portfolio URL
- [ ] admin notes
- [ ] AI output

## Payment

- [ ] amount tampering
- [ ] duplicate submission
- [ ] wrong application ID
- [ ] unauthorized payment status
- [ ] replay
- [ ] race condition
- [ ] fake screenshot
- [ ] wrong user upload

---

# 91. Required UX Test Matrix

## Public

- [ ] desktop 1440px
- [ ] laptop 1024px
- [ ] tablet 768px
- [ ] mobile 390px
- [ ] mobile 320px
- [ ] slow network
- [ ] JavaScript disabled where feasible
- [ ] reduced motion

## Signup

- [ ] keyboard-only
- [ ] validation
- [ ] back/forward navigation
- [ ] accidental refresh
- [ ] duplicate submission
- [ ] mobile keyboard
- [ ] password manager
- [ ] screen reader

## Portal

- [ ] first-load skeleton
- [ ] empty states
- [ ] API failure
- [ ] expired session
- [ ] slow API
- [ ] mobile sidebar
- [ ] deep links
- [ ] browser back button

## Payment

- [ ] wrong screenshot
- [ ] slow upload
- [ ] duplicate click
- [ ] network failure
- [ ] mobile upload
- [ ] verification pending
- [ ] rejected payment
- [ ] successful payment

---

# 92. Route Inventory Requirement

The local agent should automatically generate a route inventory from Flask.

Required output:

| Method | Route | Auth | Role | CSRF | Rate limit | Data class | Notes |
|---|---|---|---|---|---|---|---|

Example:

```text
POST /admin/login
POST /admin/add-mentor
GET  /admin/users
GET  /admin/devices
POST /post-hire/deposit
POST /enroll
POST /generate-tutor-token
```

Every route must have a documented security contract.

---

# 93. Security Contract Pattern

For each sensitive route:

```python
@require_auth(role="intern")
@require_csrf
@rate_limit(...)
def route(...):
    ...
```

Inside:

```text
authenticate
authorize
validate input
validate business state
perform transaction
audit
respond
```

Never mix these responsibilities randomly throughout a giant function.

---

# 94. API Response Contract

Standardize responses:

### Success

```json
{
  "ok": true,
  "data": {}
}
```

### Error

```json
{
  "ok": false,
  "error": {
    "code": "APPLICATION_NOT_FOUND",
    "message": "Application not found."
  }
}
```

Never return:

- stack trace
- SQL error
- Python exception
- secret
- internal file path

---

# 95. Observability

Every security-sensitive action should have:

```text
request_id
actor_id
actor_role
action
resource_type
resource_id
result
timestamp
ip
```

Example:

```json
{
  "event": "payment_status_changed",
  "actor_id": 17,
  "actor_role": "finance_admin",
  "payment_id": 442,
  "from": "pending",
  "to": "verified",
  "request_id": "..."
}
```

---

# 96. Recommended Design System

Create one design token file:

```css
:root {
  --bg-0: #07080E;
  --bg-1: #0E111D;
  --surface: ...;
  --text: ...;
  --text-muted: ...;
  --primary: ...;
  --success: ...;
  --warning: ...;
  --danger: ...;
  --border: ...;
  --radius-sm: ...;
  --radius-md: ...;
  --radius-lg: ...;
  --shadow-card: ...;
}
```

Do not scatter raw values throughout templates.

---

# 97. Recommended Portal Layout

The student dashboard should become:

```text
┌─────────────────────────────────────────────┐
│ DBERT                     Notifications 👤  │
├───────────────┬─────────────────────────────┤
│ Dashboard     │ Application Status          │
│ Applications  │ ┌─────────────────────────┐ │
│ Learning      │ │ Under Review             │ │
│ Interview     │ │ AI Agent Development     │ │
│ Mentor        │ │ Submitted: 12 Sep        │ │
│ Jobs          │ │ Next: Await review       │ │
│ Messages      │ └─────────────────────────┘ │
│ CV            │                             │
│ Account       │ Next actions                │
│               │ [Complete Profile]          │
│               │ [Take Interview]            │
│               │ [Open Learning]             │
└───────────────┴─────────────────────────────┘
```

The dashboard should not feel like an admin control panel.

---

# 98. Definition of Done

The repository should not be considered production-ready until all of these are true:

### Security

- [ ] no default production secrets
- [ ] no hardcoded passwords
- [ ] no secrets in query strings
- [ ] Turnstile fail-closed or controlled fallback
- [ ] single authentication authority
- [ ] all state-changing requests protected
- [ ] all sensitive objects authorization-checked
- [ ] private file storage
- [ ] password reset hardened
- [ ] SSO tested
- [ ] payment state machine tested
- [ ] admin RBAC implemented
- [ ] audit logging implemented
- [ ] security CI enabled

### UX

- [ ] application is the primary public CTA
- [ ] dashboard is status-first
- [ ] mobile navigation simplified
- [ ] accessibility AA
- [ ] reduced motion
- [ ] loading skeletons
- [ ] meaningful empty states
- [ ] clear errors
- [ ] payment trust UX
- [ ] consistent design tokens

### Engineering

- [ ] route inventory
- [ ] explicit serializers
- [ ] explicit database columns
- [ ] migration system
- [ ] PostgreSQL production path
- [ ] integration tests
- [ ] security regression tests
- [ ] dependency scanning
- [ ] secret scanning

---

# 99. Agent Execution Rules

The local AI coding agent should follow these rules strictly:

1. **Do not rewrite the application in one shot.**
2. Make one phase at a time.
3. Before changing behavior, reproduce the current behavior with a test.
4. After each security fix, add a regression test.
5. Never weaken a security control just to make a UI test pass.
6. Never expose secrets while debugging.
7. Never print passwords or tokens.
8. Do not replace authorization with frontend hiding.
9. Do not use `SELECT *` in new code.
10. Do not introduce new hardcoded secrets.
11. Do not disable CSP because of a frontend problem.
12. Do not disable CSRF because a fetch request fails.
13. Do not make payment/enrollment state client-controlled.
14. Do not remove legacy behavior without identifying dependencies.
15. Prefer small commits.
16. Each commit should map to one remediation objective.
17. Run tests after every phase.
18. Keep a `SECURITY_CHANGELOG.md`.
19. Document every intentional exception.
20. If a finding cannot be reproduced, mark it `VERIFY`, not `FIXED`.

---

# 100. Suggested Commit Sequence

```text
audit: baseline route and security inventory

security: fix tutor SSO authorization and undefined route state
security: fail closed for Turnstile
security: remove production secret fallbacks
security: consolidate admin authorization
security: remove query-string cron secrets
security: harden password reset
security: remove admin password display
security: introduce explicit API serializers
security: isolate private uploads
security: harden payment idempotency

test: add authentication regression suite
test: add authorization matrix
test: add upload security tests
test: add payment state-machine tests
test: add SSO regression tests

ux: simplify public navigation
ux: redesign application funnel
ux: redesign portal dashboard around application status
ux: improve mobile navigation
ux: add skeleton loading states
ux: improve payment trust UI
a11y: keyboard and focus audit
a11y: reduced-motion support
a11y: contrast fixes

arch: introduce service boundaries
arch: introduce database migrations
arch: prepare PostgreSQL production backend
ci: add security scanning
```

---

# 101. Final Priority Board

## P0 — Do immediately

- [ ] Fix/replace `/generate-tutor-token`
- [ ] Verify payment/SSO authorization server-side
- [ ] Stop Turnstile fail-open behavior
- [ ] Verify every payment/enrollment state transition
- [ ] Remove any possibility of default production authentication

## P1 — Next release

- [ ] Consolidate auth/session authority
- [ ] Remove legacy auth transport
- [ ] Eliminate password display
- [ ] Remove query-string cron secrets
- [ ] Private file storage
- [ ] Explicit admin API serializers
- [ ] Account enumeration mitigation
- [ ] Payment idempotency
- [ ] Admin RBAC
- [ ] Security regression suite
- [ ] Simplify public UX
- [ ] Simplify portal navigation

## P2 — Hardening

- [ ] PostgreSQL
- [ ] migrations
- [ ] security headers
- [ ] CSP tightening
- [ ] third-party dependency reduction
- [ ] privacy/retention controls
- [ ] AI abuse controls
- [ ] CSV formula-injection protection
- [ ] performance optimization

## P3 — Quality

- [ ] design token cleanup
- [ ] remove inline styles
- [ ] better empty states
- [ ] skeleton loading
- [ ] motion polish
- [ ] accessibility refinements
- [ ] component standardization

---

# 102. Bottom Line

The repository has clearly received substantial security work already. The presence of CSRF middleware, nonce CSP, rate limiting, password migration, upload magic-byte validation, session revocation and production guards shows that security has been considered.

The bigger engineering problem is **complexity concentration**.

A 11k+ line Flask application now contains authentication, payments, education, messaging, referrals, AI, admin and company workflows. That makes security fixes fragile because unrelated features can share the same helpers, session state, database tables and templates.

The correct strategy is therefore:

```text
P0 security correctness
        ↓
regression tests
        ↓
data/authorization boundaries
        ↓
admin RBAC
        ↓
UX simplification
        ↓
service/module separation
        ↓
PostgreSQL + migrations
        ↓
continuous security CI
```

Do not chase visual polish before fixing the P0 security and state-transition issues.

The portal should ultimately become a **status-first, student-centered product with a small trusted security core**, rather than a collection of features exposed through one large application.

---

## Source evidence used for this audit

- Repository structure and feature claims
- `app.py` authentication, session, CSRF, upload, admin, payment and SSO logic
- `.env.example`
- `templates/index.html`
- `templates/portal.html`
- `templates/admin.html`
- live public homepage

This report intentionally distinguishes confirmed source-level defects from items that require runtime verification.
