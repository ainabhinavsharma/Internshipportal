# DBERT Internship Portal — Next Phase Master Development Plan

**Document:** `DBERT_PORTAL_NEXT_PHASE_MASTER_PLAN.md`  
**Repository:** `https://github.com/ainabhinavsharma/Internshipportal`  
**Environment:** Live production system with active users  
**Purpose:** Production stabilization, QA hardening, safe migration, reliability improvement, architecture evolution, and controlled rollout.

---

# 0. EXECUTIVE DIRECTIVE

You are the local AI development agent responsible for taking the existing DBERT Internship Portal from its current feature-rich state to a stable, production-grade platform.

This is **not a greenfield project**.

The application already has active users and important historical data. Therefore:

> **Preserve existing behavior and user data unless a documented change is explicitly required.**

The primary objective is not to add more features immediately.

The primary objective is to make the existing platform:

- deterministic
- testable
- auditable
- secure
- migration-safe
- regression-resistant
- operationally reliable
- maintainable
- ready for controlled future scaling

The agent must work phase-by-phase.

**Do not skip phases merely because a later phase appears easier.**

---

# 1. NON-NEGOTIABLE SAFETY RULES

## 1.1 Never modify production directly during development

Development environments:

```text
LOCAL
  ↓
STAGING
  ↓
PRODUCTION
```

Never:

```text
LOCAL AI AGENT
      ↓
PRODUCTION DATABASE
```

Never use production credentials for local experiments.

Never run experimental migrations against production.

Never use production payment credentials in staging.

Never send real user emails from local development.

---

# 2. ACTIVE USER PROTECTION

The system currently has active users.

Existing users must not lose:

- account access
- user IDs
- email
- phone
- profile data
- applications
- application history
- application status
- domain
- joining date
- enrollment
- payment records
- payment evidence
- course progress
- task progress
- attendance
- mentor assignments
- projects
- submissions
- certificates
- messages
- notifications
- referrals
- relevant audit history

If a migration cannot preserve a data item:

```text
STOP MIGRATION
```

Do not silently discard or overwrite data.

---

# 3. GOLDEN MIGRATION PRINCIPLE

Every schema/data migration must follow:

```text
EXPAND
   ↓
MIGRATE
   ↓
VERIFY
   ↓
SWITCH
   ↓
MONITOR
   ↓
CONTRACT
```

Never use:

```text
DROP OLD
↓
CREATE NEW
↓
HOPE
```

---

# 4. PROJECT STATE MODEL

Maintain these statuses for development tasks:

```text
DISCOVERED
READY
IN_PROGRESS
BLOCKED
IMPLEMENTED
TESTING
VERIFIED
RELEASED
REGRESSION
```

A task is **not complete** merely because code has been written.

---

# 5. REQUIRED PROJECT DOCUMENTATION

Create and maintain:

```text
docs/
├── PROJECT_STATE.md
├── DEVELOPMENT_PLAN.md
├── CURRENT_PHASE.md
├── CHANGE_CONTROL.md
├── USER_MIGRATION_PLAN.md
├── DATABASE_SAFETY.md
├── RELEASE_PROCESS.md
├── ROLLBACK_PLAN.md
├── QA_MASTER_PLAN.md
├── STATE_MACHINES.md
├── ROLE_PERMISSION_MATRIX.md
├── ROUTE_INVENTORY.md
├── FEATURE_INVENTORY.md
├── DEPENDENCY_MAP.md
├── EXTERNAL_SERVICES.md
└── INCIDENT_RUNBOOK.md
```

Also create:

```text
.agent/
├── CURRENT_PHASE.md
├── TASK_QUEUE.md
├── COMPLETED.md
├── BLOCKED.md
├── DECISIONS.md
├── TEST_RESULTS.md
├── MIGRATION_STATUS.md
├── FILES_CHANGED.md
└── SESSION_LOG.md
```

---

# 6. AGENT SESSION PROTOCOL

At the beginning of every coding session:

1. Read `.agent/CURRENT_PHASE.md`.
2. Read `.agent/TASK_QUEUE.md`.
3. Read `.agent/BLOCKED.md`.
4. Read `.agent/DECISIONS.md`.
5. Read relevant `docs/` files.
6. Run `git status`.
7. Inspect uncommitted changes.
8. Determine the current phase.
9. Identify the highest-priority unblocked task.
10. Inspect the existing implementation before changing it.

At the end of every session:

1. Run relevant tests.
2. Record test results.
3. Record files changed.
4. Record unresolved issues.
5. Record decisions.
6. Update current phase.
7. Update task status.
8. Update migration status if relevant.
9. Write a concise session log.
10. Never mark work complete without verification.

If the session is interrupted, the next session must resume from `.agent/CURRENT_PHASE.md` and `.agent/TASK_QUEUE.md`.

---

# 7. GIT SAFETY

Recommended branch structure:

```text
main
production
feature/*
fix/*
qa/*
migration/*
refactor/*
hotfix/*
```

Preferred development flow:

```text
feature/fix
   ↓
local tests
   ↓
code review
   ↓
CI
   ↓
staging
   ↓
UAT
   ↓
production
```

Do not rewrite Git history unless explicitly authorized.

Do not force-push shared branches.

---

# 8. PHASE 0 — SYSTEM INVENTORY

## Objective

Understand the complete existing system before modifying it.

## Tasks

### INV-001 — Route inventory

Inspect every route.

Create:

```text
docs/ROUTE_INVENTORY.md
```

For each route record:

```text
Route
HTTP method
Authentication required
Role
Owner
Purpose
Database tables
External services
Template/API response
Redirects
Error states
Tests
```

---

### INV-002 — Feature inventory

Create:

```text
docs/FEATURE_INVENTORY.md
```

Categorize:

```text
Authentication
Intern
Application
Enrollment
Payment
LMS
Courses
Tasks
Projects
Mentor
Company
Marketplace
Certificates
CV
AI Interview
Messaging
Notifications
Referral
Admin
Analytics
SEO
Security
```

Mark each:

```text
ACTIVE
PARTIAL
LEGACY
UNKNOWN
BROKEN
UNUSED
```

Do not delete anything solely because it appears unused.

---

### INV-003 — Database inventory

Document:

- tables
- columns
- indexes
- constraints
- foreign keys
- relationships
- migrations
- seed data
- legacy tables
- duplicated concepts

Create:

```text
docs/DATABASE_INVENTORY.md
```

---

### INV-004 — External services

Document:

```text
Email
AI APIs
Payment services
Cloud storage
OAuth
Turnstile/CAPTCHA
Push notifications
Analytics
Search/indexing
Other APIs
```

Create:

```text
docs/EXTERNAL_SERVICES.md
```

For each:

```text
Provider
Purpose
Credentials location
Failure behavior
Timeout
Retry
Fallback
Production dependency
Staging behavior
```

---

## PHASE 0 GATE

Do not proceed until:

- route inventory complete
- feature inventory complete
- database inventory complete
- external service inventory complete
- unknown critical dependencies identified

---

# 9. PHASE 1 — PRODUCTION SAFETY FOUNDATION

## Objective

Create reliable backup, staging and rollback mechanisms before changing business logic.

---

## SAFE-001 — Database backup

Implement automated backup.

For SQLite:

```text
backups/
```

with timestamped names.

Example:

```text
dbert_YYYY_MM_DD_HH_MM_SS.db
```

Backups required:

- daily
- pre-release
- pre-migration
- emergency/manual

---

## SAFE-002 — Backup verification

A backup is invalid until restoration is tested.

Procedure:

```text
backup
 ↓
restore isolated copy
 ↓
database integrity check
 ↓
start application
 ↓
smoke tests
```

Document:

```text
docs/DATABASE_SAFETY.md
```

---

## SAFE-003 — Staging

Create a staging environment mirroring production as closely as practical.

Example:

```text
production:
internship.dbert.online

staging:
staging-internship.dbert.online
```

Staging must use:

- test payment mode
- test email inbox
- test credentials
- non-production AI credentials where possible
- separate database
- separate file storage

---

## SAFE-004 — Rollback

Create:

```text
docs/ROLLBACK_PLAN.md
```

Document:

```text
application rollback
database rollback
migration rollback
configuration rollback
static asset rollback
external service rollback
```

---

## PHASE 1 GATE

Must have:

- verified backup
- verified restore
- working staging
- documented rollback
- production backup procedure
- no production credentials in source code

---

# 10. PHASE 2 — ACTIVE USER MIGRATION FRAMEWORK

## Objective

Create a safe migration mechanism before changing schemas or workflows.

---

## MIG-001 — User lifecycle classification

Create a report identifying existing users:

```text
A — Registered but not applied
B — Application pending
C — Under review
D — Selected
E — Enrollment pending
F — Payment pending
G — Enrolled
H — Active internship
I — Completed
J — Certificate issued
K — Rejected
L — Inactive/abandoned
```

Use the actual database statuses.

Do not invent replacements until the existing values are documented.

---

## MIG-002 — Data preservation checklist

For each user verify preservation of:

```text
identity
authentication
profile
applications
application history
enrollment
payment
courses
progress
attendance
tasks
mentor
projects
submissions
certificates
messages
notifications
referrals
```

---

## MIG-003 — Migration dry run

Every migration must first run on:

```text
production backup copy
```

and then:

```text
staging
```

Generate:

```text
migration report
```

containing:

```text
records read
records migrated
records skipped
records transformed
errors
duplicates
orphaned records
inconsistent records
```

---

## MIG-004 — Data inconsistency report

Create:

```text
DATA_INCONSISTENCIES.csv
```

If an existing record appears logically inconsistent, do not silently repair it.

Example:

```text
application = rejected
enrollment = active
```

Report it for controlled resolution.

---

## PHASE 2 GATE

No production migration until:

- dry run successful
- backup verified
- migration report reviewed
- data integrity checks pass
- rollback tested

---

# 11. PHASE 3 — APPLICATION STATE MACHINE

## Objective

Make application lifecycle deterministic.

Create:

```text
docs/STATE_MACHINES.md
```

Document actual existing statuses first.

Then define valid transitions.

Example conceptual model:

```text
APPLIED
   ↓
UNDER_REVIEW
   ├── ON_HOLD
   ├── SELECTED
   └── REJECTED

ON_HOLD
   ↓
UNDER_REVIEW

SELECTED
   ↓
ENROLLMENT_PENDING
```

Do not implement these exact values until reconciled with the existing database.

---

## APP-001 — Central transition function

Create a single backend transition service.

Conceptually:

```python
transition_application(
    application_id,
    target_status,
    actor,
    reason,
    request_id
)
```

Validate:

- current state
- target state
- allowed transition
- actor permission
- business conditions
- ownership

---

## APP-002 — Status history

Create:

```text
application_status_history
```

Recommended fields:

```text
id
application_id
old_status
new_status
changed_by
changed_at
reason
request_id
metadata
```

---

## APP-003 — Prevent direct status mutation

Search the entire codebase for direct application status updates.

Replace business-critical updates with the transition service.

---

## APP-004 — Transition tests

Test:

- valid transitions
- invalid transitions
- unauthorized transitions
- duplicate transitions
- concurrent transitions
- stale UI submission
- repeated API request

---

## PHASE 3 GATE

No impossible application state may be creatable through normal application APIs.

---

# 12. PHASE 4 — ENROLLMENT STATE MACHINE

Separate:

```text
Application status
```

from:

```text
Enrollment status
```

Document actual existing values before introducing new ones.

Potential conceptual lifecycle:

```text
NOT_STARTED
ENROLLMENT_PENDING
PAYMENT_PENDING
PAYMENT_SUBMITTED
PAYMENT_UNDER_REVIEW
PAYMENT_ACCEPTED
PAYMENT_REJECTED
ENROLLED
CANCELLED
COMPLETED
```

---

## ENR-001

Centralize enrollment transitions.

---

## ENR-002

Prevent:

```text
rejected application
+
active enrollment
```

unless an explicitly documented business rule allows it.

---

## ENR-003

Test duplicate enrollment attempts.

---

## ENR-004

Test browser refresh during enrollment.

---

## ENR-005

Test network failure during enrollment.

---

# 13. PHASE 5 — PAYMENT STATE MACHINE

Payment must have an independent lifecycle.

Conceptually:

```text
NOT_REQUIRED
PENDING
SUBMITTED
UNDER_REVIEW
ACCEPTED
REJECTED
REFUNDED
CANCELLED
```

Create:

```text
payment_history
```

Record:

```text
payment_id
old_status
new_status
actor
timestamp
reason
request_id
```

---

## PAY-001 — Payment consistency

Prevent:

```text
payment accepted
+
enrollment inactive
```

unless intentionally supported.

---

## PAY-002 — Double submission

Test:

```text
double click
refresh
multiple tabs
multiple devices
retry after timeout
```

---

## PAY-003 — Payment evidence privacy

Payment screenshots must not be publicly accessible through predictable URLs.

Test:

```text
user A → user B payment
anonymous → payment
company → payment
mentor → payment
```

All unauthorized access must fail.

---

## PAY-004 — Razorpay Payment Gateway Integration Architecture

Integrate Razorpay as the primary automated payment processing gateway across all platform checkout places.

### Core Architecture Principles:
1. **Zero Hardcoded Secrets**: `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` must reside strictly in environment variables (`.env`).
2. **Server-Side Order Creation**: Orders must be generated server-side via Razorpay Orders API (`POST https://api.razorpay.com/v1/orders`) with unique receipts and cryptographically bound amounts. Clients must never dictate the payment amount.
3. **Cryptographic Signature Verification**: Every client payment completion must be authenticated on the backend using HMAC SHA256 before granting course access or mutating enrollment status.
4. **Asynchronous Webhook Reconciliation**: Implement webhook handlers (`/api/payment/razorpay/webhook`) with secret validation to catch and credit payments where users close the browser before returning to the portal.

---

## PAY-005 — Dynamic Fallback & Feature Flagging (Razorpay vs QR Code)

The platform must dynamically adapt its UI and payment ingestion based on the presence of Razorpay API credentials:

```text
               ┌───────────────────────────────┐
               │ Check Razorpay API Keys       │
               │ (RAZORPAY_KEY_ID & SECRET)    │
               └───────────────┬───────────────┘
                               │
                Is configured and enabled?
                               │
               ┌───────────────┴───────────────┐
              YES                              NO
               │                               │
               ▼                               ▼
    ┌──────────────────────┐        ┌──────────────────────┐
    │  RAZORPAY ONLINE     │        │  MANUAL UPI QR CODE  │
    │  - Hide QR Code      │        │  - Display QR Code   │
    │  - Hide Screenshot UI│        │  - Enable File Upload│
    │  - Show Razorpay CTA │        │  - Admin Review Queue│
    │  - Instant Approval  │        │  - Manual Approval   │
    └──────────────────────┘        └──────────────────────┘
```

### Operational Rules:
- **When Keys Are Present (`RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` set)**:
  - Automatically **turn off and hide the static UPI QR code image** (`/static/img/qrcode.jpeg` / `/static/qr.jpg`) across all payment touchpoints.
  - Turn off and hide the manual payment screenshot upload input (`#paidFile`, `#rec_file`, etc.).
  - Render the official Razorpay Checkout modal button ("Pay Online with UPI / Cards / Netbanking").
  - Upon server-side signature verification, **instantly transition candidate enrollment to `Enrolled` / `Paid`** without requiring manual admin approval.
- **When Keys Are Absent or Empty**:
  - Automatically fall back to the existing manual UPI QR code and screenshot upload workflow.
  - Transactions enter the `Under Review` queue in `/admin/enrollments` for manual admin inspection.
  - Ensures zero downtime and zero deployment breakage when gateway credentials are not yet provisioned.

---

## PAY-006 — Complete Payment Places Mapping

Razorpay must be unified across every payment touchpoint in the application:

### 1. Internship Security Deposit / Seat Confirmation (₹499)
- **Location**: `templates/portal.html` -> `#ovSelected` (Candidate selected modal).
- **Current Flow**: Shows UPI QR code and file upload for screenshot.
- **Razorpay Flow**: Replaces QR container with "Pay ₹499 Security Deposit" Razorpay modal trigger; verifies payment; instantly marks enrollment as `Enrolled` and unlocks orientation courses.

### 2. Onboarding Data Completion Wizard (Step 3: Payment Verification)
- **Location**: `templates/portal.html` -> `#onboardingWizardModal` Step 3.
- **Current Flow**: Shows static QR and file input.
- **Razorpay Flow**: Provides one-click online payment via Razorpay; advances wizard step automatically to Academic Profile upon payment success.

### 3. Post-Hire Job Offer Guarantee Deposit (₹499)
- **Location**: `templates/portal.html` -> `#ovJobDeposit` (Track 5: Job Guarantee Deposit).
- **Backend**: `/intern/post-hire-deposit`, `post_hire_deposits` table.
- **Razorpay Flow**: Generates order for ₹499; logs `razorpay_payment_id` and `razorpay_order_id` in `post_hire_deposits`; confirms guarantee instantly.

### 4. Paid Fast-Track Program Seat Fee (₹1,599)
- **Location**: `templates/program.html` -> `#ctaForm`.
- **Backend**: `/enroll` with `product='paid_program'`.
- **Razorpay Flow**: Replaces UPI ID box and screenshot upload with instant Razorpay checkout; marks paid enrollment active and grants immediate learning access.

### 5. Standalone LMS Course Purchases
- **Location**: `templates/course_pay.html` -> Course checkout (`course.price_inr`).
- **Backend**: `course_payments` table, `/admin/course-payments`.
- **Razorpay Flow**: Direct checkout for individual courses; unlocks course modules immediately upon signature verification.

### 6. Company Paid Cohorts / Workshops
- **Location**: `/cohorts/<cohort_id>/enroll`.
- **Backend**: `cohort_enrollments` table.
- **Razorpay Flow**: Instant seat purchase for live mentor workshops.

---

## PAY-007 — Order Lifecycle & Cryptographic Verification

Implement standard backend endpoints:
1. `POST /api/payment/razorpay/create-order`:
   - Authenticates current intern/user session.
   - Determines authorized product and canonical amount from database (never from request body).
   - Calls Razorpay API: `POST /v1/orders`.
   - Returns `{ status: "success", order_id: "order_...", amount: ..., key_id: ... }`.
2. `POST /api/payment/razorpay/verify-payment`:
   - Receives `{ razorpay_order_id, razorpay_payment_id, razorpay_signature, product_type, metadata }`.
   - Recomputes HMAC SHA256:
     ```python
     generated_signature = hmac.new(
         RAZORPAY_KEY_SECRET.encode(),
         f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
         hashlib.sha256
     ).hexdigest()
     ```
   - If signatures match, executes state transition within an atomic database transaction.

---

## PAY-008 — Webhook Integration & Server Reconciliation

Create:
```text
POST /api/payment/razorpay/webhook
```
- Authenticates incoming `X-Razorpay-Signature` against `RAZORPAY_WEBHOOK_SECRET`.
- Handles events:
  - `payment.captured`
  - `payment.failed`
  - `refund.processed`
- Prevents race conditions with idempotent event processing based on `event_id` and `razorpay_payment_id`.

---

## PAY-009 — Content Security Policy (CSP) Updates for Razorpay

Update `csp_policy_for()` in `app.py`:
- `script-src`: Add `https://checkout.razorpay.com`
- `frame-src`: Add `https://api.razorpay.com`
- `connect-src`: Add `https://lumberjack.razorpay.com https://api.razorpay.com`

---

## PAY-010 — Database Schema Expansion for Gateway Records

Expand `payments`, `enrollments`, `post_hire_deposits`, and `course_payments` tables:
```sql
ALTER TABLE payments ADD COLUMN gateway TEXT DEFAULT 'manual_upi';
ALTER TABLE payments ADD COLUMN razorpay_order_id TEXT;
ALTER TABLE payments ADD COLUMN razorpay_payment_id TEXT;
ALTER TABLE payments ADD COLUMN razorpay_signature TEXT;
ALTER TABLE payments ADD COLUMN webhook_event_id TEXT;
```
Enforce unique index on `razorpay_payment_id` where not null to prevent double crediting.

---

# 14. PHASE 6 — DATABASE INTEGRITY

Create:

```text
scripts/check_data_integrity.py
```

It should detect:

```text
orphan users
orphan applications
orphan enrollments
orphan payments
duplicate active applications
duplicate enrollment
impossible statuses
missing references
invalid certificates
invalid assignments
```

Run:

```text
before release
after migration
after restore
on demand
```

---

# 15. PHASE 7 — AUTHENTICATION REGRESSION

Create automated tests for:

```text
signup
login
logout
forgot password
reset password
expired reset token
used reset token
duplicate email
duplicate phone
session expiry
deep link
back button
multiple tabs
multiple devices
admin login
mentor login
company login
intern login
```

Critical journey:

```text
login
→ portal
→ logout
→ browser back
→ portal
```

Expected:

```text
authenticated access denied
```

---

# 16. PHASE 8 — AUTHORIZATION

Create:

```text
docs/ROLE_PERMISSION_MATRIX.md
```

Roles:

```text
PUBLIC
INTERN
MENTOR
COMPANY
STAFF
ADMIN
SUPERADMIN
```

For every protected endpoint define:

```text
authentication
role
ownership
special permission
```

Test IDOR:

```text
User A accessing User B data
```

for:

```text
applications
CV
payment
certificate
messages
tasks
submissions
profile
```

---

# 17. PHASE 9 — GOLDEN APPLICANT JOURNEY

This is the most important E2E test.

Automate:

```text
new visitor
 ↓
signup
 ↓
application
 ↓
login
 ↓
portal
 ↓
admin review
 ↓
selection
 ↓
candidate sees selection
 ↓
enrollment
 ↓
payment submission
 ↓
admin payment review
 ↓
payment accepted
 ↓
enrollment activated
 ↓
course access
 ↓
task
 ↓
submission
 ↓
completion
 ↓
certificate
```

If this fails:

```text
PRODUCTION RELEASE = BLOCKED
```

---

# 18. PHASE 10 — MARKETPLACE

Test:

```text
company registration
company verification
company approval
company suspension
create internship
draft
publish
expire
close
candidate application
shortlist
interview
selection
hire
```

Verify that:

```text
homepage count
search result
category count
listing page
application availability
```

all use the same source of truth.

---

# 19. MARKETPLACE INVENTORY RULE

Never hardcode claims such as:

```text
120+ openings
95+ openings
110+ openings
```

if those numbers are supposed to represent current inventory.

Generate counts from the live database.

If there are no live listings:

```text
No live internships in this category.
```

must not coexist with misleading category counts.

---

# 20. EXPIRED LISTING RULE

An expired listing must never show an active application CTA.

Instead:

```text
APPLICATIONS CLOSED
```

and optionally:

```text
Similar opportunities
```

Historical pages may remain if useful.

---

# 21. PHASE 11 — EMAIL AND EVENT ARCHITECTURE

Avoid coupling business transactions directly to email delivery.

Bad:

```text
DB update
 ↓
send email
 ↓
email fails
 ↓
API reports failure
```

Preferred:

```text
DB transaction
 ↓
event/outbox record
 ↓
background worker
 ↓
email
```

Events:

```text
application.submitted
application.selected
application.rejected
enrollment.created
payment.submitted
payment.accepted
payment.rejected
mentor.assigned
task.assigned
task.reviewed
certificate.issued
```

---

# 22. Notification Delivery States

Every notification should support:

```text
PENDING
SENT
FAILED
RETRYING
DEAD_LETTER
```

Do not lose business state because an external email provider is unavailable.

---

# 23. PHASE 12 — FILE SECURITY

Audit:

```text
CV
payment screenshot
profile image
certificate
project submission
company documents
```

Validate:

```text
extension
MIME type
magic bytes
size
filename
storage location
authorization
download permission
```

Test malicious uploads.

---

# 24. PHASE 13 — PUBLIC/PRIVATE DATA

Explicitly classify fields:

```text
PUBLIC
PRIVATE
ADMIN_ONLY
SENSITIVE
```

Public CV endpoints must expose only intentionally public fields.

Never serialize an entire user/database record into a public endpoint.

---

# 25. PHASE 14 — DEAD-END AND UX AUDIT

Every user-facing page must answer:

```text
Where am I?
What can I do?
What happens next?
```

Every error must explain:

```text
what happened
why
what the user can do
```

Avoid:

```text
Error 400
Something went wrong
```

without actionable information.

---

# 26. PHASE 15 — ROUTE COMPATIBILITY

Create:

```text
docs/ROUTE_COMPATIBILITY.md
```

Document old routes.

Example:

```text
/profile
/dashboard
/signin
/signup
```

For each:

```text
current destination
reason
usage
created date
removal criteria
```

Do not remove compatibility routes until usage has been checked.

---

# 27. PHASE 16 — DEAD LINK AND FRONTEND FAILURE TESTING

Build automated scanning for:

```text
internal links
forms
buttons
API endpoints
redirects
assets
images
scripts
```

Detect:

```text
404
401
403
500
redirect loops
missing assets
JavaScript exceptions
failed API requests
infinite loading
```

Playwright tests should fail on:

```text
console.error
uncaught exception
unhandled rejection
critical network failure
```

---

# 28. PHASE 17 — MOBILE AND ACCESSIBILITY

Test:

```text
360x800
390x844
412x915
768x1024
1366x768
1920x1080
```

Test:

```text
signup
login
portal
courses
tasks
applications
payment
admin
company
```

Accessibility:

```text
keyboard navigation
focus
contrast
labels
ARIA
modal behavior
escape key
focus trapping
form errors
```

---

# 29. PHASE 18 — PERFORMANCE

Measure:

```text
TTFB
page load
API latency
DB query time
template rendering
JavaScript execution
image size
```

Identify:

```text
N+1 queries
unbounded queries
large joins
large responses
slow external APIs
```

Paginate all large administrative datasets.

---

# 30. PHASE 19 — SECURITY REGRESSION

Automate:

```text
CSRF
XSS
SQL injection
IDOR
broken access control
file upload attacks
session fixation
session reuse
rate limiting
password reset abuse
private data exposure
```

Never weaken:

```text
CSRF
CSP
authentication
authorization
rate limits
```

to make a feature work.

---

# 31. PHASE 20 — OBSERVABILITY

Every request should have a request ID.

Where practical propagate it to:

```text
database audit
email log
notification
AI request
exception
payment operation
```

Monitor:

```text
5xx rate
4xx rate
latency
DB errors
email failures
payment failures
AI failures
login failures
upload failures
```

Create:

```text
/health
/ready
```

where appropriate.

---

# 32. PHASE 21 — INCIDENT RESPONSE

Create:

```text
docs/INCIDENT_RUNBOOK.md
```

Cover:

```text
site down
database corruption
email outage
payment problem
AI outage
authentication failure
file storage outage
bad deployment
security incident
```

For every incident:

```text
DETECT
 ↓
CONTAIN
 ↓
INVESTIGATE
 ↓
ROLLBACK/REPAIR
 ↓
VERIFY
 ↓
COMMUNICATE
 ↓
POSTMORTEM
```

---

# 33. PHASE 22 — MONOLITH MODULARIZATION

Do not rewrite the application.

The existing Flask application is already large.

Refactor gradually.

Target:

```text
services/
├── auth_service.py
├── application_service.py
├── enrollment_service.py
├── payment_service.py
├── notification_service.py
├── certificate_service.py
├── marketplace_service.py
└── interview_service.py
```

Routes:

```text
routes/
├── auth.py
├── applications.py
├── enrollment.py
├── marketplace.py
├── admin.py
├── mentor.py
├── company.py
└── intern.py
```

Every extraction must preserve existing behavior.

---

# 34. REFACTORING RULE

Before refactoring:

```text
existing behavior
+
test
```

Then:

```text
refactor
 ↓
same tests
 ↓
new tests
```

Never perform a large rewrite without characterization tests.

---

# 35. PHASE 23 — DATABASE ABSTRACTION

Before PostgreSQL migration:

Remove unnecessary SQLite-specific assumptions from business logic.

Business services should not care whether the database is:

```text
SQLite
PostgreSQL
```

where practical.

---

# 36. PHASE 24 — POSTGRESQL PREPARATION

Do not immediately switch production.

First:

```text
SQLite
 ↓
schema compatibility
 ↓
PostgreSQL staging
 ↓
data migration
 ↓
verification
 ↓
comparison
 ↓
rollback test
```

Keep the existing database as a rollback source.

---

# 37. PHASE 25 — POSTGRESQL MIGRATION

Production migration sequence:

```text
backup
 ↓
freeze risky writes if required
 ↓
migration
 ↓
integrity check
 ↓
smoke test
 ↓
controlled traffic
 ↓
monitor
```

Keep rollback capability until the new system has passed a defined stability period.

---

# 38. PHASE 26 — DATA INTEGRITY DASHBOARD

Admin should eventually be able to see:

```text
System Health

Users
Applications
Enrollments
Payments
Active Interns
Completed Interns
Certificates

Integrity

No orphan applications
No orphan enrollments
No duplicate active applications
No impossible states
No expired live listings
No failed critical jobs
```

---

# 39. PHASE 27 — RELEASE PROCESS

Every release requires:

## Backend

```text
unit tests
integration tests
database tests
security tests
```

## Frontend

```text
Playwright
mobile
desktop
responsive
console errors
```

## Business

```text
signup
application
selection
enrollment
payment
acceptance
internship
certificate
```

## Infrastructure

```text
backup
restore
migration
health
rollback
```

---

# 40. PRODUCTION CANARY

Preferred:

```text
staging
 ↓
production deployment
 ↓
internal/admin smoke test
 ↓
controlled exposure
 ↓
monitor
 ↓
full rollout
```

If percentage-based canary deployment is not available, use:

```text
staging verification
+
backup
+
fast rollback
+
post-deployment smoke test
+
active monitoring
```

---

# 41. ACTIVE USER RELEASE RULE

During releases, existing users should retain:

```text
same URL
same login
same account
same user ID
same application
same enrollment
same progress
same certificate
```

Avoid forced:

```text
signup
reapplication
password reset
enrollment restart
```

unless explicitly required and communicated.

---

# 42. GOLDEN USER JOURNEYS

Maintain automated journeys for:

## Student

```text
signup
→ application
→ status
→ selection
→ enrollment
→ payment
→ acceptance
→ learning
→ task
→ completion
→ certificate
```

## Company

```text
registration
→ verification
→ post
→ applications
→ review
→ interview
→ hire
→ close
```

## Mentor

```text
login
→ assigned interns
→ review
→ task feedback
→ progress
→ final evaluation
```

## Admin

```text
login
→ applications
→ payment
→ users
→ companies
→ mentors
→ reports
→ audit
```

---

# 43. TEST CASE FORMAT

Every test case should contain:

```text
TEST ID
TITLE
PRIORITY
PRECONDITIONS
TEST DATA
STEPS
EXPECTED RESULT
ACTUAL RESULT
STATUS
EVIDENCE
REGRESSION RISK
```

Example:

```text
APP-TEST-001

Title:
New candidate can submit application

Priority:
P0

Precondition:
Fresh test account

Steps:
1. Open signup
2. Complete profile
3. Submit
4. Login
5. Open portal

Expected:
One user
One application
Correct domain
Correct status
No duplicate record
```

---

# 44. BUG SEVERITY

Use:

```text
P0 — production blocker/data loss/security critical
P1 — major workflow broken
P2 — significant defect with workaround
P3 — minor defect
P4 — cosmetic/low impact
```

---

# 45. RELEASE BLOCKERS

Any of these blocks release:

```text
data loss
authentication bypass
authorization bypass
payment inconsistency
broken application lifecycle
broken enrollment lifecycle
duplicate financial record
private data exposure
Golden Journey failure
database migration failure
backup failure
rollback failure
critical 500 error
```

---

# 46. DEFINITION OF DONE

A task is complete only when:

```text
CODE
+
TEST
+
TEST PASS
+
SECURITY REVIEW
+
DATA/MIGRATION REVIEW
+
DOCUMENTATION
+
ROLLBACK CONSIDERED
```

A phase is complete only when:

```text
all P0 tasks complete
all required P1 tasks complete
phase tests pass
regression suite passes
documentation updated
phase gate approved
```

---

# 47. MASTER PHASE ORDER

The agent must follow this order unless a documented dependency requires otherwise:

```text
PHASE 0
System Inventory
        ↓
PHASE 1
Backup + Staging + Rollback
        ↓
PHASE 2
Active User Migration Framework
        ↓
PHASE 3
Application State Machine
        ↓
PHASE 4
Enrollment State Machine
        ↓
PHASE 5
Payment State Machine
        ↓
PHASE 6
Database Integrity
        ↓
PHASE 7
Authentication Regression
        ↓
PHASE 8
Authorization
        ↓
PHASE 9
Golden Applicant Journey
        ↓
PHASE 10
Marketplace
        ↓
PHASE 11
Email + Events
        ↓
PHASE 12
File Security
        ↓
PHASE 13
Privacy
        ↓
PHASE 14
UX Dead Ends
        ↓
PHASE 15
Route Compatibility
        ↓
PHASE 16
Frontend Regression
        ↓
PHASE 17
Mobile + Accessibility
        ↓
PHASE 18
Performance
        ↓
PHASE 19
Security Regression
        ↓
PHASE 20
Observability
        ↓
PHASE 21
Incident Response
        ↓
PHASE 22
Monolith Modularization
        ↓
PHASE 23
Database Abstraction
        ↓
PHASE 24
PostgreSQL Preparation
        ↓
PHASE 25
PostgreSQL Migration
        ↓
PHASE 26
Integrity Dashboard
        ↓
PHASE 27
Production Release Process
        ↓
PHASE 28
Final UAT
        ↓
CONTROLLED PRODUCTION ROLLOUT
```

---

# 48. PHASE GATES

## Gate 0

Inventory complete.

## Gate 1

Backup, restore, staging and rollback operational.

## Gate 2

Active-user migration framework verified.

## Gate 3

Application state machine verified.

## Gate 4

Enrollment/payment consistency verified.

## Gate 5

Authentication and authorization regression suite passes.

## Gate 6

Golden Applicant Journey passes.

## Gate 7

Marketplace passes.

## Gate 8

Notification/email reliability passes.

## Gate 9

Security/privacy passes.

## Gate 10

Performance/mobile/accessibility passes.

## Gate 11

Database migration tested.

## Gate 12

Production UAT passes.

## Gate 13

Controlled rollout passes.

---

# 49. CURRENT PHASE TRACKING

The agent must keep:

```text
.agent/CURRENT_PHASE.md
```

Format:

```markdown
# Current Phase

Phase: 0
Name: System Inventory
Status: IN_PROGRESS

Current Task:
INV-001

Completed:
- None

In Progress:
- INV-001

Blocked:
- None

Next:
- INV-002

Last Verified:
YYYY-MM-DD HH:MM

Last Test Result:
N/A
```

---

# 50. TASK QUEUE FORMAT

`.agent/TASK_QUEUE.md`

```markdown
# Task Queue

## P0

- [ ] INV-001 Route inventory
- [ ] SAFE-001 Database backup
- [ ] SAFE-002 Backup verification
- [ ] SAFE-003 Staging
- [ ] SAFE-004 Rollback

## P1

- [ ] MIG-001 User lifecycle classification
- [ ] MIG-002 Data preservation
- [ ] MIG-003 Migration dry run

## P2

- [ ] Documentation cleanup
```

Update after every meaningful task.

---

# 51. DECISION LOG

`.agent/DECISIONS.md`

Every architectural decision must record:

```text
ID
Date
Decision
Reason
Alternatives
Impact
Migration impact
Rollback
```

Example:

```text
DEC-001

Decision:
Do not immediately replace SQLite.

Reason:
Active users and existing business logic create unnecessary migration risk.

Alternative:
Immediate PostgreSQL rewrite.

Rejected because:
Would combine infrastructure and workflow changes.

Impact:
SQLite remains temporarily.

Review:
After workflow stabilization.
```

---

# 52. BLOCKED TASK FORMAT

`.agent/BLOCKED.md`

```markdown
# Blocked Tasks

## TASK-ID

Reason:
Dependency:
What is required:
Who/what blocks it:
Workaround:
Date blocked:
```

Never silently skip blocked tasks.

---

# 53. COMPLETED TASK FORMAT

`.agent/COMPLETED.md`

Record:

```text
Task ID
Date
Implementation
Tests
Files changed
Migration impact
Security impact
Verification
```

---

# 54. SESSION LOG FORMAT

`.agent/SESSION_LOG.md`

```markdown
# Session YYYY-MM-DD

## Started

Time:

## Phase

Phase:

## Tasks

- TASK-ID

## Work Completed

...

## Tests

...

## Failures

...

## Files Changed

...

## Decisions

...

## Remaining Work

...

## Next Session

...
```

---

# 55. FILE CHANGE TRACKING

`.agent/FILES_CHANGED.md`

Maintain:

```text
File
Change
Reason
Phase
Risk
Tests
```

This helps recover after interrupted AI sessions.

---

# 56. AGENT BEHAVIOR WHEN DISCOVERING A NEW BUG

If a new bug is discovered:

1. Do not immediately modify unrelated code.
2. Record the bug.
3. Assign severity.
4. Identify affected users.
5. Identify reproduction steps.
6. Add a regression test.
7. Fix the smallest safe scope.
8. Run affected tests.
9. Run regression tests.
10. Document the fix.

---

# 57. AGENT BEHAVIOR WHEN DISCOVERING LEGACY CODE

Do not automatically delete it.

Classify:

```text
ACTIVE
LEGACY
DUPLICATE
UNUSED
UNKNOWN
```

If removal is proposed:

```text
usage analysis
 ↓
backup
 ↓
staging
 ↓
test
 ↓
approval
 ↓
production
```

---

# 58. AGENT BEHAVIOR WHEN DISCOVERING DATA INCONSISTENCY

Never silently rewrite production data.

Instead:

```text
detect
 ↓
report
 ↓
classify
 ↓
define correction rule
 ↓
dry run
 ↓
backup
 ↓
apply
 ↓
verify
```

---

# 59. AGENT BEHAVIOR WHEN A TEST FAILS

Never weaken the test merely to obtain green CI.

Determine:

```text
implementation bug
test bug
environment problem
expected behavior changed
data problem
dependency failure
```

Document the decision.

---

# 60. AGENT BEHAVIOR WHEN A SESSION BREAKS

When resuming:

```text
read CURRENT_PHASE.md
read TASK_QUEUE.md
read BLOCKED.md
read DECISIONS.md
git status
inspect last changed files
run relevant tests
continue from last VERIFIED task
```

Do not assume the previous AI completed the task.

---

# 61. PRODUCTION MIGRATION PROCEDURE

Before production migration:

```text
[ ] Staging migration successful
[ ] Backup verified
[ ] Restore verified
[ ] Data comparison complete
[ ] Integrity checker passes
[ ] Regression suite passes
[ ] Golden Journey passes
[ ] Rollback tested
[ ] Migration duration known
[ ] Communication prepared
[ ] Monitoring active
```

Production:

```text
backup
 ↓
migration
 ↓
integrity check
 ↓
smoke test
 ↓
Golden Journey
 ↓
monitor
```

If critical verification fails:

```text
ROLLBACK
```

---

# 62. POST-DEPLOYMENT MONITORING

Immediately after deployment monitor:

```text
5xx
4xx
login failures
signup failures
application failures
enrollment failures
payment failures
email failures
database errors
AI failures
latency
CPU
RAM
disk
```

Also manually verify:

```text
public homepage
login
signup
portal
application
admin
company
certificate
```

---

# 63. POST-RELEASE STABILITY WINDOW

After a major migration/release:

```text
do not immediately remove rollback assets
```

Keep:

- previous application version
- previous database backup
- migration logs
- deployment logs
- integrity report

until the defined stability window passes.

Document the stability window in:

```text
docs/RELEASE_PROCESS.md
```

---

# 64. FINAL PRODUCTION READINESS CHECKLIST

Before declaring the platform production-ready:

## Business

- [ ] New applicant can complete application.
- [ ] Admin can review.
- [ ] Valid state transitions work.
- [ ] Selection works.
- [ ] Enrollment works.
- [ ] Payment submission works.
- [ ] Payment verification works.
- [ ] Intern receives access.
- [ ] Course workflow works.
- [ ] Task workflow works.
- [ ] Mentor workflow works.
- [ ] Completion workflow works.
- [ ] Certificate workflow works.

## Security

- [ ] Authentication tested.
- [ ] Authorization tested.
- [ ] IDOR tested.
- [ ] CSRF tested.
- [ ] XSS tested.
- [ ] File uploads tested.
- [ ] Private data tested.
- [ ] Rate limiting tested.
- [ ] Password reset tested.

## Data

- [ ] No orphan records.
- [ ] No impossible states.
- [ ] No duplicate active applications.
- [ ] No duplicate enrollment.
- [ ] Payment data consistent.
- [ ] Certificate data consistent.

## Infrastructure

- [ ] Backup works.
- [ ] Restore works.
- [ ] Staging works.
- [ ] Rollback works.
- [ ] Monitoring works.
- [ ] Error logging works.

## UX

- [ ] No critical dead ends.
- [ ] No critical 404s.
- [ ] No redirect loops.
- [ ] No infinite loading.
- [ ] Mobile tested.
- [ ] Accessibility tested.

## Performance

- [ ] Critical pages measured.
- [ ] Critical APIs measured.
- [ ] Database bottlenecks investigated.
- [ ] Large datasets paginated.

---


---

# 28A. GUIDED LEARNING 2.0 — ADAPTIVE LEARNING TRANSFORMATION

## Objective

The current Guided Learning implementation must be treated as a major product subsystem rather than a simple lesson/task navigation layer.

The target is:

> **A learner-aware, evidence-driven, adaptive tutor that continuously determines what the intern understands, what they misunderstand, what they are ready to learn next, and how much scaffolding they need.**

The system must adapt to the **individual intern's demonstrated understanding**, not merely their completed modules, selected domain, or previous answers.

The target experience should feel like:

```text
Assess
  ↓
Understand learner
  ↓
Select concept
  ↓
Explain at appropriate level
  ↓
Check understanding
  ↓
Evaluate evidence
  ↓
Detect misconception / gap
  ↓
Adjust difficulty + teaching strategy
  ↓
Practice
  ↓
Mastery check
  ↓
Advance OR remediate
  ↓
Schedule review
  ↓
Repeat
```

This must become a first-class learning loop inside the portal.

---

# 28A.1 CURRENT GUIDED LEARNING PROBLEMS TO RESOLVE

Before implementation, verify the repository's current implementation rather than assuming these findings are still unchanged.

The previous audit identified the following architectural weaknesses that must be explicitly re-verified:

### GL-AUDIT-001 — Mastery is not sufficiently authoritative

The system must not infer mastery only from a transient answer or global state.

Mastery must be:

```text
student scoped
concept scoped
evidence based
time aware
confidence aware
historical
```

---

### GL-AUDIT-002 — Evaluation is too heuristic

Do not rely on simple:

```text
keyword matching
number matching
string similarity
```

as the authoritative evaluator for open-ended learning responses.

Use structured evaluation.

The evaluator should determine:

```text
correctness
partial correctness
reasoning quality
concept understanding
misconception
confidence
evidence strength
```

---

### GL-AUDIT-003 — Concept handling is too hard-coded

Concepts must not be scattered as arbitrary strings throughout the application.

Create a controlled concept model:

```text
domain
subject
module
topic
concept
sub-concept
skill
```

Each concept should have:

```text
concept_id
name
description
difficulty
prerequisites
learning objectives
assessment criteria
common misconceptions
supported learning resources
```

---

### GL-AUDIT-004 — Learning state must be student-specific

Never maintain a global mastery value that can accidentally represent one learner for another.

The authoritative state must be:

```text
student_id
+
concept_id
```

---

### GL-AUDIT-005 — Adaptive selection is incomplete

The next learning action must consider more than:

```text
current module
```

It should consider:

```text
mastery
confidence
recent performance
prerequisite readiness
misconceptions
difficulty
time since last review
learning velocity
attempt history
assessment evidence
review urgency
current session context
```

---

### GL-AUDIT-006 — Spaced review is incomplete

The system must distinguish:

```text
new learning
reinforcement
review
remediation
mastery validation
```

A concept that was understood three months ago should not be treated the same as a concept that was mastered yesterday.

---

### GL-AUDIT-007 — Learning state and streaming evaluation must be transactionally safe

A streaming tutor response must never update learner state in a way that races with evaluation or causes partial commits.

The learning event lifecycle must be deterministic:

```text
response generated
 ↓
evidence captured
 ↓
evaluation completed
 ↓
learning event committed
 ↓
mastery recalculated
 ↓
next action selected
```

---

# 28A.2 GUIDED LEARNING 2.0 ARCHITECTURE

Implement the following conceptual architecture:

```text
                    ┌─────────────────────┐
                    │     INTERN          │
                    │ chat / lesson / quiz│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ LEARNING SESSION     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ EVIDENCE COLLECTOR   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ANSWER EVALUATOR     │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
            correctness   misconception   confidence
                 │             │             │
                 └─────────────┼─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ LEARNING EVENT       │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ STUDENT MODEL        │
                    │ mastery / gaps /     │
                    │ misconceptions /    │
                    │ review history       │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ ADAPTIVE POLICY      │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ NEXT LEARNING ACTION │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ TUTOR / CONTENT      │
                    └─────────────────────┘
```

This is the authoritative loop:

```text
Student Evidence
→ Answer Evaluation
→ Learning Event
→ Student Mastery State
→ Adaptive Policy
→ Next Learning Action
→ Tutor Response
→ New Evidence
```

Do not bypass this loop for important learning-state changes.

---

# 28A.3 LEARNING DATA MODEL

Create a student learning model.

At minimum, design these logical entities:

```text
learning_concepts
concept_prerequisites
learning_objectives
student_concept_mastery
student_misconceptions
learning_events
assessment_attempts
learning_sessions
review_schedule
learning_recommendations
learning_content
```

The exact physical schema must be derived from the existing database before migration.

---

## Student Concept Mastery

Conceptually:

```text
student_concept_mastery

student_id
concept_id
mastery_score
confidence_score
evidence_count
correct_count
incorrect_count
partial_count
last_evaluated_at
last_practiced_at
last_mastered_at
next_review_at
retention_estimate
difficulty_estimate
status
version
```

Potential status:

```text
UNKNOWN
INTRODUCED
DEVELOPING
PRACTICING
NEAR_MASTERY
MASTERED
REVIEW_DUE
AT_RISK
```

Do not expose these labels as absolute psychological judgments. They represent system learning state.

---

# 28A.4 CONCEPT GRAPH

Build a prerequisite graph.

Example:

```text
Python Variables
      ↓
Data Types
      ↓
Conditions
      ↓
Loops
      ↓
Functions
      ↓
Collections
      ↓
OOP
```

A learner should not be pushed aggressively into:

```text
Functions
```

if evidence shows a prerequisite gap in:

```text
Variables
Conditions
Loops
```

The adaptive engine should identify the smallest useful prerequisite remediation.

---

# 28A.5 LEARNING OBJECTIVES

Every learning concept should have explicit objectives.

Example:

```text
Concept:
Python Functions

Objectives:

LO-001
Identify what a function is.

LO-002
Explain parameters and return values.

LO-003
Write a simple function.

LO-004
Debug a function.

LO-005
Apply functions to a practical problem.
```

This allows the tutor to distinguish:

```text
"I can define it"
```

from:

```text
"I can actually use it."
```

---

# 28A.6 BLOOM-STYLE COGNITIVE PROGRESSION

The adaptive engine should not only track topic completion.

Track evidence across levels:

```text
REMEMBER
UNDERSTAND
APPLY
ANALYZE
EVALUATE
CREATE
```

A learner who can define recursion but cannot implement it should not be marked fully mastered.

Example:

```text
Remember: 90
Understand: 85
Apply: 55
Analyze: 35
```

Overall mastery must not hide this profile.

---

# 28A.7 UNDERSTANDING-LEVEL ADAPTATION

The tutor must estimate the learner's current understanding level from evidence.

Possible learner levels:

```text
LEVEL 0 — No demonstrated understanding
LEVEL 1 — Recognition
LEVEL 2 — Basic understanding
LEVEL 3 — Guided application
LEVEL 4 — Independent application
LEVEL 5 — Transfer / advanced application
```

These are instructional states, not labels about intelligence.

The tutor must adapt:

```text
explanation depth
terminology
examples
question difficulty
scaffolding
hint strength
pace
recall frequency
assessment difficulty
```

---

# 28A.8 DO NOT ASSUME LEARNING STYLE

Do not permanently label a learner:

```text
visual learner
auditory learner
reading learner
```

unless there is strong product evidence and a specific reason.

Instead, track **observed instructional preferences and response effectiveness**.

Example:

```text
text explanation effectiveness
worked-example effectiveness
interactive-question effectiveness
analogy effectiveness
code-example effectiveness
```

The system can then adapt based on what actually helps the learner.

---

# 28A.9 INITIAL DIAGNOSTIC

When an intern starts a new subject/module:

```text
do not immediately start lesson 1
```

unless the product intentionally chooses that behavior.

Use a lightweight diagnostic.

Example:

```text
3–8 questions
```

covering:

```text
prerequisites
core concept
application
reasoning
confidence
```

Do not make the diagnostic unnecessarily long.

Use it to estimate:

```text
known
unknown
uncertain
misconceived
```

---

# 28A.10 CONTINUOUS DIAGNOSTIC

Do not depend only on the initial diagnostic.

Every learning interaction is evidence.

Evidence sources:

```text
quiz answer
open-ended answer
coding exercise
task submission
hint request
number of retries
time-to-answer
self-reported confidence
explanation request
mistake pattern
mentor feedback
project result
```

Important:

> **Do not treat time spent as direct proof of comprehension.**

It is only supporting evidence.

---

# 28A.11 CONFIDENCE CALIBRATION

Ask the learner occasionally:

```text
How confident are you?
1 2 3 4 5
```

Compare:

```text
confidence
vs
actual performance
```

This enables detection of:

```text
overconfidence
underconfidence
calibrated confidence
```

Use this to determine when more assessment is needed.

Do not use it to make psychological claims.

---

# 28A.12 MISCONCEPTION ENGINE

Create explicit misconception tracking.

Example:

```text
Concept:
Python Lists

Misconception:
"Lists cannot contain different data types."

Evidence:
Student repeatedly makes this assumption.

Status:
ACTIVE

Severity:
MEDIUM

First detected:
...

Last observed:
...

Correction attempts:
2
```

The tutor should prioritize misconception correction before advancing when the misconception blocks a prerequisite.

---

# 28A.13 MISCONCEPTION LIFECYCLE

```text
DETECTED
 ↓
CONFIRMED
 ↓
REMEDIATION
 ↓
RETEST
 ↓
RESOLVED
```

Never mark a misconception resolved simply because the tutor explained it once.

Require new evidence.

---

# 28A.14 ADAPTIVE DIFFICULTY

Difficulty should change based on evidence.

Example:

```text
3 correct independent answers
→ increase difficulty

partial answer
→ maintain difficulty + scaffold

incorrect answer with prerequisite gap
→ prerequisite remediation

repeated failure
→ reduce complexity

correct answer after strong hints
→ do not treat as equivalent to independent mastery
```

This distinction is critical.

---

# 28A.15 HINT-AWARE MASTERY

Track whether success was:

```text
independent
light hint
strong hint
worked example
direct explanation
```

A correct answer after a full solution should not produce the same mastery update as an independent correct answer.

---

# 28A.16 ADAPTIVE TEACHING MODES

The tutor should support explicit internal modes:

```text
EXPLAIN
QUESTION
HINT
PRACTICE
EVALUATE
REMEDIATE
REVIEW
CHALLENGE
SUMMARY
TRANSFER
```

The system chooses the mode.

The learner may also request a mode where appropriate.

---

# 28A.17 EXPLAIN MODE

When the learner lacks understanding:

```text
simple explanation
→ example
→ check understanding
```

Avoid giant lectures.

Preferred loop:

```text
Explain one idea
↓
Ask one meaningful question
↓
Evaluate
↓
Continue
```

---

# 28A.18 SOCRATIC MODE

For appropriate questions, guide rather than immediately reveal the answer.

Example:

```text
Student:
I don't know why this loop stops.

Tutor:
What condition controls whether the loop continues?
```

Then:

```text
Student answer
→ evaluate
→ next hint
```

Do not use Socratic behavior when it would create unnecessary frustration.

---

# 28A.19 PRACTICE MODE

Generate targeted exercises from the student's current concept state.

Practice should target:

```text
weak concept
misconception
prerequisite
transfer skill
```

not random questions.

---

# 28A.20 ASSESSMENT MODE

Assessment must be more rigorous than normal tutoring.

Support:

```text
MCQ
short answer
explanation
numerical
code
debugging
scenario
application
```

Assessment questions should have metadata:

```text
concept_id
objective_id
difficulty
Bloom level
expected reasoning
common misconceptions
answer rubric
```

---

# 28A.21 OPEN-ENDED EVALUATION

For free-form answers, evaluator output should be structured.

Conceptually:

```json
{
  "correctness": 0.0,
  "concept_understanding": 0.0,
  "reasoning_quality": 0.0,
  "independence": 0.0,
  "confidence": 0.0,
  "misconceptions": [],
  "missing_concepts": [],
  "feedback": "",
  "evidence_strength": "high"
}
```

The exact schema must be versioned.

Never let free-form LLM text directly mutate mastery.

---

# 28A.22 EVALUATION CONFIDENCE

Every AI evaluation should have:

```text
evaluation_confidence
```

If confidence is low:

```text
do not make a large mastery change
```

Instead:

```text
ask another question
request explanation
run targeted assessment
```

This prevents one ambiguous response from corrupting the learner model.

---

# 28A.23 MASTERY UPDATE ENGINE

Use a deterministic server-side policy.

The LLM may provide evidence.

The backend determines the state update.

Conceptually:

```text
previous mastery
+
new evidence
+
evidence strength
+
independence
+
difficulty
+
historical performance
=
new mastery
```

Do not allow the LLM to directly say:

```text
mastery = 95
```

and persist that value without policy validation.

---

# 28A.24 MASTERY CONFIDENCE

Separate:

```text
mastery
```

from:

```text
confidence in mastery estimate
```

Example:

```text
Mastery:
82%

Confidence:
35%
```

This means the system thinks the learner may know the concept but does not have enough evidence yet.

That should trigger additional validation.

---

# 28A.25 SPACED REPETITION

Implement review scheduling.

Track:

```text
last_practice
last_success
last_failure
difficulty
stability
retention estimate
review count
next review
```

Review queue should prioritize:

```text
urgent prerequisite gaps
active misconceptions
due reviews
high-value concepts
recently weak concepts
```

Do not simply review everything at fixed intervals.

---

# 28A.26 FORGETTING / RETENTION MODEL

Start with a deterministic, explainable approach.

The system may estimate retention using a bounded decay model.

Do not introduce a complex ML model before enough real learner data exists.

First collect:

```text
practice history
delayed recall
review outcomes
```

Then improve the model using evidence.

---

# 28A.27 ADAPTIVE NEXT-ACTION ENGINE

Create one authoritative service:

```text
get_next_learning_action(student_id)
```

It considers:

```text
mastery gaps
prerequisites
misconceptions
review urgency
learning objective
difficulty
recent failures
recent successes
confidence
course requirements
internship relevance
```

Return a structured recommendation:

```json
{
  "action": "REMEDIATE",
  "concept_id": "...",
  "objective_id": "...",
  "difficulty": 2,
  "reason_codes": [
    "PREREQUISITE_GAP",
    "RECENT_FAILURE"
  ]
}
```

The UI should be able to explain the recommendation.

---

# 28A.28 EXPLAINABLE ADAPTATION

Do not make the system feel random.

Show:

```text
Recommended next:
"Practice Python functions"

Why:
"You understood parameters, but your last two exercises showed difficulty returning values."
```

This makes adaptive learning visible and trustworthy.

---

# 28A.29 LEARNING PATH

The system should maintain:

```text
required curriculum
```

and:

```text
personalized path
```

separately.

Example:

```text
Official curriculum:
Variables → Loops → Functions → OOP

Student path:
Variables
→ Loops
→ prerequisite review
→ Functions
→ targeted practice
→ OOP
```

The learner must not lose required curriculum coverage simply because the adaptive engine changes sequence.

---

# 28A.30 MASTERY GATES

A learner should advance automatically only when the mastery gate is satisfied.

Example:

```text
Concept:
Functions

Gate:
≥ 3 independent successful demonstrations
+
no unresolved blocking misconception
+
application objective ≥ threshold
```

The exact threshold must be configurable and tested.

---

# 28A.31 REMEDIATION ENGINE

When a learner struggles:

```text
detect gap
 ↓
identify prerequisite
 ↓
teach smallest missing concept
 ↓
practice
 ↓
retest
 ↓
return to original concept
```

Do not restart the entire module unnecessarily.

This minimizes wasted learning time.

---

# 28A.32 LEARNING SESSION STATE

A session should have:

```text
session_id
student_id
started_at
ended_at
current_concept
current_objective
current_mode
actions
evidence
summary
next_action
```

This allows interrupted learners to resume.

---

# 28A.33 SESSION RESUME

If an intern leaves halfway through:

```text
resume
```

should reconstruct:

```text
what was being learned
what was understood
what was unresolved
what should happen next
```

Do not restart from lesson 1.

---

# 28A.34 ADAPTIVE DASHBOARD

The intern dashboard should show:

```text
Today's Learning
     ↓
Recommended Action

Current Concept
Mastery
Confidence

Strengths
Learning Gaps
Misconceptions

Review Due
Upcoming Review

Course Progress
Skill Progress

Why this is recommended
```

Avoid overwhelming learners with raw analytics.

---

# 28A.35 LEARNER-FACING LANGUAGE

Never expose internal ML/AI terminology unnecessarily.

Do not say:

```text
Knowledge tracing probability = 0.61
```

Say:

```text
You are getting there. Let's practice one more example before moving on.
```

Admin/debug mode can expose the underlying metrics.

---

# 28A.36 ADMIN LEARNING ANALYTICS

Admins/mentors need more detail.

Show:

```text
concept mastery
confidence
attempts
recent performance
misconceptions
review due
learning velocity
stalled concepts
```

Allow drill-down:

```text
Student
 ↓
Concept
 ↓
Evidence
 ↓
Evaluation
 ↓
Mastery history
```

---

# 28A.37 MENTOR VIEW

Mentors should receive:

```text
Student is struggling with:
Concept X

Evidence:
3 failed attempts
1 partial attempt

Likely issue:
Prerequisite Y

Recommended mentor action:
Review Y for 10 minutes
```

Do not expose sensitive or speculative psychological labels.

---

# 28A.38 EARLY WARNING SYSTEM

Use learning evidence to identify:

```text
stalled learner
repeated failure
rapid guessing
repeated misconception
long inactivity
review backlog
```

The system should surface this as:

```text
Needs attention
```

not as a judgment about the learner.

---

# 28A.39 DO NOT USE SIMPLE ENGAGEMENT AS MASTERY

These are not mastery by themselves:

```text
login hours
page views
video completion
number of messages
time spent
```

They are engagement signals.

Mastery requires evidence of understanding/application.

---

# 28A.40 RAG FOR GUIDED LEARNING

Learning content should be grounded in curated material.

Use:

```text
concept documents
examples
worked solutions
misconception notes
assessment rubrics
course requirements
```

RAG retrieval should be:

```text
concept-aware
objective-aware
difficulty-aware
student-state-aware
```

The tutor must not retrieve arbitrary unrelated content simply because it has similar keywords.

---

# 28A.41 RAG CONTENT STRUCTURE

Recommended private/local content structure:

```text
learning-rag/
├── domains/
│   ├── python/
│   ├── ai/
│   ├── data-analytics/
│   └── fullstack/
├── concepts/
├── prerequisites/
├── misconceptions/
├── examples/
├── exercises/
├── assessments/
├── rubrics/
└── review/
```

Each source should contain metadata:

```text
domain
module
concept
objective
difficulty
Bloom level
prerequisites
content_type
version
```

---

# 28A.42 CONTENT VERSIONING

If learning content changes:

```text
content_version
```

must be tracked.

Historical learner evidence should not become ambiguous because the underlying lesson was rewritten.

---

# 28A.43 AI MODEL ABSTRACTION

Do not couple Guided Learning permanently to one model provider.

Create an abstraction:

```text
TutorModel
EvaluatorModel
ContentRetriever
AdaptivePolicy
```

This allows the current provider/model to change later without rewriting learning logic.

---

# 28A.44 MODEL FAILURE BEHAVIOR

If the AI model fails:

```text
do not corrupt learning state
```

The system should show:

```text
Learning assistant temporarily unavailable.

Your progress is safe.
```

The learner can retry.

---

# 28A.45 DETERMINISTIC CORE + AI FLEXIBILITY

The architecture should separate:

## Deterministic

```text
mastery updates
state transitions
prerequisite rules
review scheduling
permissions
assessment thresholds
audit
```

## AI-assisted

```text
explanation
question generation
feedback
misconception hypothesis
natural-language tutoring
summaries
```

This separation is critical for reliability.

---

# 28A.46 GUIDED LEARNING EVENT MODEL

Every important learning interaction should generate an event.

Example:

```text
LEARNING_EVENT

event_id
student_id
session_id
concept_id
objective_id
event_type
timestamp
input
evaluation
difficulty
hint_level
mastery_before
mastery_after
confidence_before
confidence_after
misconceptions_detected
next_action
model_version
policy_version
content_version
request_id
```

Do not store unnecessary sensitive free-form data indefinitely.

Apply retention rules.

---

# 28A.47 EVENT TYPES

Recommended:

```text
LESSON_STARTED
EXPLANATION_SHOWN
QUESTION_ASKED
ANSWER_SUBMITTED
ANSWER_EVALUATED
HINT_REQUESTED
HINT_SHOWN
MISCONCEPTION_DETECTED
MISCONCEPTION_RESOLVED
PRACTICE_STARTED
PRACTICE_COMPLETED
ASSESSMENT_STARTED
ASSESSMENT_COMPLETED
MASTERY_UPDATED
REVIEW_SCHEDULED
REVIEW_COMPLETED
REMEDIATION_STARTED
REMEDIATION_COMPLETED
CONCEPT_MASTERED
SESSION_RESUMED
```

---

# 28A.48 CONCURRENCY SAFETY

Learning-state updates must be versioned.

Conceptually:

```text
student_concept_mastery.version
```

When updating:

```text
read version
→ calculate
→ update where version = old_version
→ increment version
```

If the update fails because another event modified the record:

```text
reload
→ recompute
→ retry safely
```

This prevents two browser tabs or streaming requests from corrupting mastery.

---

# 28A.49 IDEMPOTENCY

Every learning event should have an idempotency key.

If:

```text
ANSWER_SUBMITTED
```

is received twice:

```text
one event
one mastery update
```

not two.

---

# 28A.50 ADAPTIVE POLICY VERSIONING

Store:

```text
policy_version
```

with learning decisions.

When the algorithm changes from:

```text
policy v1
```

to:

```text
policy v2
```

historical decisions remain explainable.

---

# 28A.51 A/B TESTING MUST NOT DESTABILIZE LEARNING

Do not randomly change educational behavior for production users before safety validation.

If experimentation is introduced:

```text
control
experiment
```

must be explicitly versioned and reversible.

Do not compare learner groups in a way that exposes individual performance publicly.

---

# 28A.52 GUIDED LEARNING TEST MATRIX

Create:

```text
tests/guided_learning/
├── test_concepts.py
├── test_prerequisites.py
├── test_mastery.py
├── test_evaluation.py
├── test_misconceptions.py
├── test_adaptive_policy.py
├── test_review.py
├── test_sessions.py
├── test_concurrency.py
├── test_idempotency.py
├── test_rag.py
└── test_e2e_guided_learning.py
```

---

# 28A.53 GUIDED LEARNING UNIT TESTS

Test:

```text
unknown concept
low mastery
high mastery
partial answer
correct answer
incorrect answer
hint-assisted answer
misconception
prerequisite gap
review due
review not due
repeated failure
rapid success
ambiguous answer
low evaluator confidence
```

---

# 28A.54 GUIDED LEARNING INTEGRATION TESTS

Verify:

```text
answer
 ↓
evaluation
 ↓
learning event
 ↓
mastery
 ↓
adaptive decision
 ↓
next action
```

All stages must remain consistent.

---

# 28A.55 GUIDED LEARNING E2E TESTS

### Scenario A — Beginner

```text
student knows nothing
→ diagnostic
→ simple explanation
→ basic question
→ correct
→ slightly harder question
```

Expected:

```text
difficulty increases gradually
```

### Scenario B — Advanced learner

```text
student passes diagnostic strongly
```

Expected:

```text
skip unnecessary introductory material
```

### Scenario C — Misconception

```text
student repeatedly demonstrates same misconception
```

Expected:

```text
misconception detected
→ remediation
→ retest
```

### Scenario D — Struggling learner

```text
multiple failures
```

Expected:

```text
difficulty reduced
→ prerequisite check
→ scaffolding
```

### Scenario E — Overconfident learner

```text
high confidence
+
incorrect answers
```

Expected:

```text
additional evidence requested
```

### Scenario F — Underconfident learner

```text
low confidence
+
strong performance
```

Expected:

```text
continue assessment
without unnecessarily lowering difficulty
```

---

# 28A.56 PERFORMANCE REQUIREMENTS

Guided Learning must not turn every interaction into a chain of expensive AI calls.

Use:

```text
deterministic rules
+
cached concept metadata
+
cached RAG retrieval
+
batched analytics
+
asynchronous summaries
```

Avoid unnecessary:

```text
LLM call
LLM call
LLM call
LLM call
```

for every UI event.

---

# 28A.57 AI CALL BUDGET

Define per-session budgets.

Example categories:

```text
tutor generation
evaluation
misconception analysis
session summary
```

Not every interaction requires every category.

For example:

```text
simple MCQ
→ deterministic evaluation
```

may not need an LLM.

Open-ended reasoning:

```text
→ structured evaluator
```

may require AI.

---

# 28A.58 FALLBACK EVALUATION

Where possible:

```text
MCQ
numeric
exact structured response
code tests
```

should use deterministic evaluation.

Use LLM evaluation when deterministic evaluation is insufficient.

This improves both performance and consistency.

---

# 28A.59 LEARNING QUALITY METRICS

Track system-level metrics:

```text
concept mastery rate
time to mastery
attempts to mastery
remediation rate
review completion
retention check success
misconception resolution
assessment accuracy
student abandonment
session completion
```

Do not optimize only for:

```text
lesson completion
```

because learners can complete lessons without understanding them.

---

# 28A.60 LEARNING QUALITY DASHBOARD

Admin/learning team should see:

```text
Most difficult concepts
Most common misconceptions
Concepts with high failure rate
Concepts with high remediation rate
Average attempts to mastery
Review effectiveness
Stalled learners
Content with poor outcomes
```

This creates a feedback loop for improving curriculum itself.

---

# 28A.61 CONTENT QUALITY LOOP

Guided Learning should improve not only the student model but the curriculum.

Example:

```text
Concept X
→ 65% of learners fail
→ 40% share misconception Y
→ remediation often required
```

Flag:

```text
CONTENT_REVIEW_REQUIRED
```

Possible actions:

```text
rewrite explanation
add example
add prerequisite
add practice
improve assessment
```

Do not automatically rewrite educational content in production.

Human review is required for curriculum changes.

---

# 28A.62 LEARNING PATH SAFETY

The adaptive engine must never permanently strand a learner.

Every learner must have:

```text
fallback lesson
fallback assessment
manual curriculum route
mentor escalation
```

If the adaptive engine becomes unavailable:

```text
standard curriculum remains usable
```

---

# 28A.63 MENTOR ESCALATION

If a learner repeatedly fails a concept:

```text
attempt threshold reached
```

create a mentor attention event.

Example:

```text
Student:
Intern #1234

Concept:
Python Functions

Status:
Repeated difficulty

Evidence:
5 attempts
2 hints
1 remediation
still below mastery threshold
```

Mentor can review evidence.

---

# 28A.64 ADAPTIVE LEARNING EXPLANATION PANEL

For the learner, provide a lightweight:

```text
Why am I seeing this?
```

Example:

```text
We recommended this practice because your last two answers showed difficulty with return values.
```

Avoid exposing internal scores unless useful.

---

# 28A.65 LEARNING MODES UI

Guided Learning should expose a clear primary interaction.

Possible interface:

```text
┌─────────────────────────────────────┐
│ Today's Learning                    │
│                                     │
│ Python Functions                    │
│                                     │
│ Mastery        ███████░░░  72%      │
│                                     │
│ Let's practice return values.       │
│                                     │
│ [Start Practice]                    │
│                                     │
│ Why this?                           │
│ Your recent answers show a gap here.│
└─────────────────────────────────────┘
```

Do not turn the dashboard into an analytics wall.

---

# 28A.66 LEARNING SESSION UX

Preferred interaction:

```text
CONTEXT
↓
ONE CONCEPT
↓
SHORT EXPLANATION
↓
ACTIVE QUESTION
↓
FEEDBACK
↓
NEXT ACTION
```

Avoid very long AI responses by default.

The tutor should teach through interaction rather than dumping content.

---

# 28A.67 PERSONALIZATION WITHOUT OVERPERSONALIZATION

Adapt to:

```text
demonstrated knowledge
pace
difficulty
mistakes
confidence
preferences inferred from actual behavior
```

Do not infer sensitive personal characteristics.

Do not create unsupported psychological profiles.

---

# 28A.68 MODEL TRAINING DATA SEPARATION

Guided Learning production data must be separated from future training data.

Use:

```text
production learning events
        ↓
privacy filtering
        ↓
quality filtering
        ↓
human/automated validation
        ↓
training dataset
```

Never directly train on raw user conversations.

Do not include:

```text
email
phone
private profile data
payment data
credentials
tokens
private documents
```

---

# 28A.69 OFFLINE/LOCAL DEVELOPMENT

The local AI agent must be able to generate and maintain:

```text
concept files
RAG documents
assessment data
misconception data
rubrics
evaluation examples
learning policy configs
test fixtures
synthetic learner profiles
```

These development assets must remain private unless explicitly approved for publication.

---

# 28A.70 SYNTHETIC LEARNER TEST PROFILES

Create synthetic profiles:

```text
GL-STUDENT-001
Beginner

GL-STUDENT-002
Fast progression

GL-STUDENT-003
Repeated prerequisite gap

GL-STUDENT-004
Misconception-heavy

GL-STUDENT-005
High confidence / low performance

GL-STUDENT-006
Low confidence / high performance

GL-STUDENT-007
Interrupted sessions

GL-STUDENT-008
Long inactivity

GL-STUDENT-009
Strong application / weak recall

GL-STUDENT-010
Strong recall / weak application
```

Use them for regression testing.

---

# 28A.71 ADAPTIVE POLICY SIMULATOR

Create a local simulator.

Input:

```text
learner profile
concept graph
evidence sequence
```

Output:

```text
mastery evolution
recommended actions
difficulty changes
review schedule
misconception state
```

This allows policy testing without involving production users.

---

# 28A.72 GUIDED LEARNING BENCHMARK

Before replacing the existing Guided Learning system, establish a baseline.

Measure current behavior:

```text
completion
assessment performance
time to task completion
repeat attempts
mentor intervention
student drop-off
```

Then compare the new system against the baseline using the same test cohorts or synthetic scenarios.

Do not deploy a new adaptive policy merely because it looks more sophisticated.

---

# 28A.73 GUIDED LEARNING ROLLOUT

Do not replace the current learning system for every user immediately.

Use:

```text
current Guided Learning
        +
new Guided Learning engine
```

behind a feature flag.

Example:

```text
GUIDED_LEARNING_V2=false
```

Initial rollout:

```text
admin/test accounts
 ↓
internal cohort
 ↓
small production cohort
 ↓
larger cohort
 ↓
all new learning sessions
```

Existing learner sessions should be allowed to finish safely.

---

# 28A.74 ACTIVE LEARNER MIGRATION

Existing interns must not suddenly receive a completely different learning path.

Migration strategy:

```text
existing learner
 ↓
preserve current progress
 ↓
map completed modules → concepts
 ↓
initialize mastery from verified evidence
 ↓
mark uncertain concepts as UNKNOWN/DEVELOPING
 ↓
run lightweight calibration
 ↓
activate adaptive recommendations
```

Do not assume:

```text
module completed = concept mastered
```

Use:

```text
completed content
+
assessment evidence
+
task evidence
```

to initialize the student model.

---

# 28A.75 EXISTING PROGRESS PRESERVATION

Before Guided Learning V2 rollout, create:

```text
student_learning_migration_report
```

For every active learner:

```text
old progress
new concept mapping
mastery initialization
unmapped concepts
potential issues
```

No learner should lose progress because of the adaptive-learning migration.

---

# 28A.76 GUIDED LEARNING ROLLBACK

Feature flag must allow:

```text
GUIDED_LEARNING_V2=false
```

to immediately return learners to the previous safe learning path.

The old system must remain operational until V2 has passed its stability window.

---

# 28A.77 GUIDED LEARNING RELEASE GATE

Do not release Guided Learning V2 until:

- [ ] concept graph verified
- [ ] prerequisites verified
- [ ] mastery model tested
- [ ] evaluator tested
- [ ] misconception detection tested
- [ ] adaptive policy tested
- [ ] review scheduling tested
- [ ] session resume tested
- [ ] concurrency tested
- [ ] idempotency tested
- [ ] RAG grounding tested
- [ ] AI failure tested
- [ ] fallback curriculum tested
- [ ] mentor escalation tested
- [ ] privacy reviewed
- [ ] synthetic learner suite passes
- [ ] Golden Guided Learning Journey passes
- [ ] production feature flag tested
- [ ] rollback tested

---

# 28A.78 GUIDED LEARNING GOLDEN JOURNEY

Automate:

```text
Student enters module
 ↓
Diagnostic
 ↓
Initial concept selection
 ↓
Explanation
 ↓
Question
 ↓
Answer
 ↓
Evaluation
 ↓
Mastery update
 ↓
Adaptive recommendation
 ↓
Practice
 ↓
Misconception detection
 ↓
Remediation
 ↓
Retest
 ↓
Mastery gate
 ↓
Next concept
 ↓
Review scheduling
 ↓
Session resume
```

The expected behavior must be deterministic at the policy layer even when the tutor language is generated.

---

# 28A.79 GUIDED LEARNING TASK IDs

Create tasks using this namespace:

```text
GL-INV-001
GL-DATA-001
GL-CONCEPT-001
GL-MASTERY-001
GL-EVAL-001
GL-MISCONCEPTION-001
GL-ADAPT-001
GL-REVIEW-001
GL-RAG-001
GL-SESSION-001
GL-CONCURRENCY-001
GL-UI-001
GL-METRICS-001
GL-MIGRATION-001
GL-ROLLOUT-001
GL-QA-001
```

Each task must use the standard project task lifecycle.

---

# 28A.80 GUIDED LEARNING DEVELOPMENT ORDER

The agent must implement Guided Learning V2 in this order:

```text
1. Audit current Guided Learning implementation
        ↓
2. Preserve current behavior with characterization tests
        ↓
3. Define concept model
        ↓
4. Define prerequisite graph
        ↓
5. Define learning objectives
        ↓
6. Define student mastery model
        ↓
7. Define learning events
        ↓
8. Implement evidence pipeline
        ↓
9. Implement deterministic mastery policy
        ↓
10. Implement structured evaluator
        ↓
11. Implement misconception tracking
        ↓
12. Implement adaptive next-action engine
        ↓
13. Implement spaced review
        ↓
14. Implement session persistence/resume
        ↓
15. Implement RAG-aware tutor
        ↓
16. Implement adaptive UI
        ↓
17. Implement mentor/admin analytics
        ↓
18. Implement synthetic learner simulator
        ↓
19. Run benchmark against existing Guided Learning
        ↓
20. Feature-flag rollout
        ↓
21. Migrate active learners safely
        ↓
22. Monitor
        ↓
23. Gradually expand rollout
```

Do not reverse this order without documenting the dependency.

---

# 28A.81 GUIDED LEARNING DEFINITION OF DONE

Guided Learning V2 is complete only when:

```text
The system knows what concept the learner is working on
+
It knows what evidence the learner has demonstrated
+
It maintains student-specific mastery
+
It distinguishes mastery from confidence
+
It tracks misconceptions
+
It respects prerequisites
+
It adjusts difficulty
+
It chooses the next learning action
+
It schedules review
+
It survives session interruption
+
It handles concurrency safely
+
It has deterministic fallback behavior
+
It is explainable to the learner
+
It is inspectable by mentors/admins
+
It can be rolled back
```

---

# 28A.82 CORE GUIDED LEARNING PRINCIPLE

Do not build:

```text
Chatbot + progress bar
```

Build:

```text
Evidence
→ Understanding Model
→ Adaptive Decision
→ Teaching
→ Practice
→ Assessment
→ Mastery
→ Retention
→ New Evidence
```

The learner should feel:

> "The platform understands what I know and changes the way it teaches me."

The backend must be able to demonstrate, with stored evidence, **why** it made the next-learning recommendation.

---


# 65. FINAL PROJECT PRINCIPLE

The goal is not:

> "Make the code look better."

The goal is:

> **Make the DBERT Internship Portal behave predictably for real users under real conditions while preserving existing users and data.**

Every change must answer:

```text
What problem does this solve?

Which users are affected?

What existing behavior could this break?

How is it tested?

How is existing data protected?

How can it be rolled back?

How do we know it is actually complete?
```

If those questions cannot be answered:

```text
DO NOT RELEASE.
```

---

# 66. FIRST EXECUTION INSTRUCTION

When this document is first given to the local AI agent:

### DO NOT START CODING FEATURES.

First execute only:

```text
PHASE 0
```

Create the project inventory.

Then:

```text
PHASE 1
```

Create backup, staging and rollback mechanisms.

Then stop and report:

```text
CURRENT PHASE
COMPLETED TASKS
BLOCKED TASKS
DISCOVERED RISKS
DATA RISKS
MIGRATION RISKS
TEST RESULTS
NEXT TASK
```

Only proceed to the next phase after its gate is satisfied.

---

# 67. SUCCESS CONDITION

The project is successful when:

```text
Existing users remain safe
        +
Existing data remains intact
        +
Critical workflows are deterministic
        +
Every critical workflow is tested
        +
Security controls are regression-tested
        +
Migrations are reversible
        +
Failures are observable
        +
Deployments are controlled
        +
The codebase can evolve without repeatedly breaking production
```

**End of Master Plan**
