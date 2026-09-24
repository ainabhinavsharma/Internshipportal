# DBERT Internship Portal — Feature Inventory (INV-002)

**Document Date:** 2026-09-23  
**Status Key:**
- `ACTIVE`: Implemented, tested, actively used in production.
- `PARTIAL`: Functional but incomplete or undergoing enhancement.
- `LEGACY`: Maintained strictly for backward compatibility with older clients or links.
- `BROKEN`: Identified bug or regression requiring remediation before release.
- `UNKNOWN`: Code present but usage / dependencies unverified.
- `UNUSED`: Dead code or deprecated feature slated for controlled deprecation.

---

## 1. Feature Domain Breakdown

### 1. Authentication & Session Management
- **Status:** `ACTIVE` (with `LEGACY` compatibility paths)
- **Components:**
  - Intern Signup with Email OTP (`/auth/send-otp`, `/auth/verify-otp`): `ACTIVE`
  - Intern Password Login & Legacy Direct Signin (`/intern/login`, `/check-email`): `ACTIVE`
  - Company Signup & Login (`/company/signup`, `/company/login`): `ACTIVE`
  - Admin & Staff Login (`/admin/login`, `/staff/login`): `ACTIVE`
  - Password Reset Request & Confirmation (`/forgot-password`, `/reset-password/<token>`): `ACTIVE`
  - Database-backed user sessions (`user_sessions` table): `ACTIVE`
  - Legacy `auth_token` cookie and `X-Session-Token` header: `LEGACY` (slated for Phase 7 review)
- **Key Files:** [`app.py`](file:///c:/Users/user/Desktop/internship/app.py), [`templates/index.html`](file:///c:/Users/user/Desktop/internship/templates/index.html)

### 2. Intern Profile & Portal Dashboard
- **Status:** `ACTIVE`
- **Components:**
  - Intern personal dashboard (`/portal`, `/intern/me`): `ACTIVE`
  - Profile update & resume upload (`/intern/profile`): `ACTIVE`
  - Attendance heartbeat & history (`/attendance/ping`, `/intern/attendance`): `ACTIVE`
  - Device profiling & multi-device alerts (`device_profiles` table): `ACTIVE`
- **Key Files:** [`templates/portal.html`](file:///c:/Users/user/Desktop/internship/templates/portal.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 3. Application Pipeline
- **Status:** `ACTIVE`
- **Components:**
  - Public Unified Apply modal & endpoint (`/apply`): `ACTIVE`
  - Candidate status tracker (`/intern/application-status`): `ACTIVE`
  - Admin application management & status updates (`/admin/applications`, `/admin/update-application-status`): `ACTIVE`
  - Multi-stage lifecycle (`Applied` → `Under Review` → `Selected` → `Enrollment Pending` → `Enrolled` / `Rejected`): `ACTIVE`
- **Key Files:** [`app.py`](file:///c:/Users/user/Desktop/internship/app.py), [`templates/admin.html`](file:///c:/Users/user/Desktop/internship/templates/admin.html)

### 4. Enrollment & Onboarding
- **Status:** `ACTIVE`
- **Components:**
  - Offer letter generation & display: `ACTIVE`
  - Enrollment submission with batch/domain selection (`/enroll`): `ACTIVE`
  - Admin enrollment review queue (`/admin/enrollments`, `/admin/enrollment/review`): `ACTIVE`
  - Bulk enrollment review (`/admin/enrollment/bulk-review`): `ACTIVE`
- **Key Files:** [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 5. Payments & Security Deposits
- **Status:** `ACTIVE`
- **Components:**
  - QR Code / UPI payment submission (`/enroll`, `payments` table): `ACTIVE`
  - Payment proof screenshot upload & storage: `ACTIVE`
  - Admin payment verification & deposit ledger (`/admin/enrollments`, `/admin/post-hire-deposits`): `ACTIVE`
  - Refund management (`/admin/post-hire-deposits/<id>/refund`): `ACTIVE`
- **Key Files:** [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 6. LMS, Courses & Guided Learning
- **Status:** `PARTIAL` (Target for Phase 28A Guided Learning 2.0 transformation)
- **Components:**
  - Course catalog (`/courses`, `/api/public/courses`): `ACTIVE`
  - Course chapter & subtopic player (`course_chapters`, `course_subtopics`): `ACTIVE`
  - Daily quizzes & attempt tracking (`course_day_quizzes`, `day_quiz_attempts`): `ACTIVE`
  - Subtopic AI chat tutor (`/intern/tutor-chat`, `/generate-tutor-token`):
    - Chat tutor: `ACTIVE`
    - `/generate-tutor-token`: `BROKEN` (undefined variable `course_id`)
- **Key Files:** [`templates/courses.html`](file:///c:/Users/user/Desktop/internship/templates/courses.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 7. Tasks & Project Submissions
- **Status:** `ACTIVE`
- **Components:**
  - Weekly task assignments (`/intern/tasks`, `tasks` table): `ACTIVE`
  - Student task submissions with github/live links (`/intern/tasks/submit`): `ACTIVE`
  - Admin / Mentor task evaluation and scoring (`task_submissions`): `ACTIVE`
  - Final project submission & review (`course_projects`, `project_submissions`): `ACTIVE`
- **Key Files:** [`templates/portal.html`](file:///c:/Users/user/Desktop/internship/templates/portal.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 8. Mentor Program
- **Status:** `ACTIVE`
- **Components:**
  - Mentor login & dashboard (`/mentor`, `/mentor/login`): `ACTIVE`
  - Mentor slot availability management (`mentor_availability_slots`): `ACTIVE`
  - Intern 1-on-1 mentor booking (`mentor_session_bookings`): `ACTIVE`
  - Mentor intern review and notes: `ACTIVE`
- **Key Files:** [`templates/mentor.html`](file:///c:/Users/user/Desktop/internship/templates/mentor.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 9. Company & Employer Portal
- **Status:** `ACTIVE`
- **Components:**
  - Company registration & profile (`/companies/<slug>`): `ACTIVE`
  - Admin company approval/suspension (`/admin/companies/approve`): `ACTIVE`
  - Job/Internship post creation (`/company/posts`): `ACTIVE`
  - Applicant review & status updates (`/company/applications/<id>/status`): `ACTIVE`
  - Company paid cohort creation (`/company/cohorts`): `ACTIVE`
- **Key Files:** [`templates/company.html`](file:///c:/Users/user/Desktop/internship/templates/company.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 10. Job & Internship Marketplace
- **Status:** `ACTIVE`
- **Components:**
  - Public job listing & search (`/jobs`, `/search`): `ACTIVE`
  - Job post details (`/jobs/<slug>`): `ACTIVE`
  - Automated 30-day post expiration cron (`/cron/expire-posts`): `ACTIVE`
  - Category listings & live opening count API (`/api/stats/openings`): `ACTIVE`
- **Key Files:** [`templates/jobs.html`](file:///c:/Users/user/Desktop/internship/templates/jobs.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 11. Certificates & Verification
- **Status:** `ACTIVE`
- **Components:**
  - Certificate generation on completion (`intern_certificates` table): `ACTIVE`
  - Public certificate validation (`/verify-certificate/<cert_id>`): `ACTIVE`
  - PDF export & social sharing preview: `ACTIVE`
- **Key Files:** [`templates/certificate.html`](file:///c:/Users/user/Desktop/internship/templates/certificate.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 12. Smart CV Builder
- **Status:** `ACTIVE`
- **Components:**
  - Interactive CV builder in intern portal: `ACTIVE`
  - Public CV URL (`/cv/<slug>`): `ACTIVE`
  - CV PDF generation (`/cv/<slug>.pdf`): `ACTIVE`
- **Key Files:** [`templates/cv_public.html`](file:///c:/Users/user/Desktop/internship/templates/cv_public.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 13. AI Technical Interview
- **Status:** `ACTIVE`
- **Components:**
  - AI question generation & adaptive follow-up (`/intern/interview/start`): `ACTIVE`
  - Candidate answer capture with anti-copy telemetry: `ACTIVE`
  - AI grading & evaluation (`/intern/interview/submit`): `ACTIVE`
  - Admin interview review & transcript view (`/admin/interview/<email>`): `ACTIVE`
- **Key Files:** [`templates/interview.html`](file:///c:/Users/user/Desktop/internship/templates/interview.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 14. Real-time Messaging
- **Status:** `ACTIVE`
- **Components:**
  - Threaded intern-mentor conversations (`conversations`, `messages`): `ACTIVE`
  - In-app messaging UI (`/intern/messages`, `/portal#messages`): `ACTIVE`
- **Key Files:** [`templates/portal.html`](file:///c:/Users/user/Desktop/internship/templates/portal.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 15. Notification System
- **Status:** `ACTIVE`
- **Components:**
  - In-app notification center (`notifications` table): `ACTIVE`
  - Transactional email dispatch via SMTP / cPanel: `ACTIVE`
  - OneSignal Web Push notifications: `PARTIAL` (active when keys provided)
- **Key Files:** [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 16. Ambassador & Referral Program
- **Status:** `ACTIVE`
- **Components:**
  - Referral code generation & cookie tracking (`/r/click`): `ACTIVE`
  - Coin ledger & balance tracking (`coin_ledger_mirror`): `ACTIVE`
  - Ambassador withdrawal requests via UPI (`/ambassador`, `/admin/ambassador-payouts`): `ACTIVE`
- **Key Files:** [`routes/ambassador.py`](file:///c:/Users/user/Desktop/internship/routes/ambassador.py), [`templates/ambassador.html`](file:///c:/Users/user/Desktop/internship/templates/ambassador.html)

### 17. Admin Operations & Queue Management
- **Status:** `ACTIVE`
- **Components:**
  - Admin overview dashboard with metrics (`/admin`, `/admin/stats`): `ACTIVE`
  - Staff delegation & task queues (`staff_queue_roles`): `ACTIVE`
  - Bulk actions (bulk accept, bulk delete, bulk interview reset): `ACTIVE`
  - System abuse log monitor (`/admin/abuse-log`): `ACTIVE`
- **Key Files:** [`templates/admin.html`](file:///c:/Users/user/Desktop/internship/templates/admin.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 18. Analytics & Telemetry
- **Status:** `ACTIVE`
- **Components:**
  - Page visit tracking (`/track-visit`, `check_log`): `ACTIVE`
  - Email open pixel tracking (`/e/o.gif`): `ACTIVE`
  - Rate limiting events logger (`rate_events`): `ACTIVE`
- **Key Files:** [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 19. SEO & Public Discovery
- **Status:** `ACTIVE`
- **Components:**
  - Dynamic XML Sitemap (`/sitemap.xml`): `ACTIVE`
  - Google AdSense sellers verification (`/ads.txt`): `ACTIVE`
  - Robots policy (`/robots.txt`): `ACTIVE`
  - OpenGraph social sharing meta tags: `ACTIVE`
- **Key Files:** [`templates/_head.html`](file:///c:/Users/user/Desktop/internship/templates/_head.html), [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)

### 20. Application Security Controls
- **Status:** `ACTIVE`
- **Components:**
  - CSP with cryptographic nonces: `ACTIVE`
  - CSRF protection via tokens & headers: `ACTIVE`
  - Magic-byte & MIME type file upload validator: `ACTIVE`
  - Sliding-window IP and account rate limiters: `ACTIVE`
  - Cloudflare Turnstile anti-bot: `ACTIVE` (with fail-open risk identified in audit)
- **Key Files:** [`app.py`](file:///c:/Users/user/Desktop/internship/app.py)
