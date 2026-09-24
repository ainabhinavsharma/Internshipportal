# DBERT Internship Portal — Comprehensive Database Inventory (INV-003)

**Database:** `internship_live.db` (SQLite 3)  
**Total Tables:** 57  
**Analysis Date:** 2026-09-23  

## 1. Executive Summary & Table Metrics

| Table Name | Row Count | Primary Key | Foreign Key Count | Index Count |
|---|---|---|---|---|
| `abuse_log` | 1082 | `id` | 0 | 1 |
| `ambassador_withdrawals` | 0 | `id` | 0 | 1 |
| `applications` | 4395 | `id` | 0 | 1 |
| `attendance` | 458 | `id` | 1 | 1 |
| `check_log` | 0 | `id` | 0 | 0 |
| `cohort_enrollments` | 1 | `id` | 2 | 2 |
| `cohorts` | 1 | `id` | 1 | 2 |
| `coin_ledger_mirror` | 1 | `id` | 0 | 3 |
| `companies` | 3 | `id` | 0 | 2 |
| `company_follows` | 0 | `id` | 2 | 3 |
| `conversations` | 93 | `id` | 0 | 3 |
| `course_chapters` | 10 | `id` | 1 | 1 |
| `course_day_quizzes` | 0 | `id` | 1 | 1 |
| `course_enrollments` | 0 | `id` | 2 | 2 |
| `course_payments` | 0 | `id` | 0 | 1 |
| `course_projects` | 0 | `id` | 1 | 1 |
| `course_subtopic_chats` | 0 | `id` | 2 | 1 |
| `course_subtopics` | 26 | `id` | 1 | 1 |
| `courses` | 2 | `id` | 0 | 1 |
| `cvs` | 140 | `id` | 1 | 3 |
| `day_quiz_attempts` | 0 | `id` | 2 | 1 |
| `dbert_fallback_usage` | 0 | `id` | 1 | 2 |
| `device_profiles` | 6356 | `id` | 0 | 1 |
| `email_log` | 6157 | `id` | 0 | 0 |
| `enrollments` | 308 | `id` | 0 | 0 |
| `intern_accounts` | 2230 | `id` | 1 | 2 |
| `intern_certificates` | 3 | `id` | 0 | 2 |
| `interviews` | 576 | `id` | 0 | 1 |
| `mentor_availability_slots` | 0 | `id` | 1 | 1 |
| `mentor_session_bookings` | 0 | `id` | 2 | 2 |
| `mentors` | 4 | `id` | 0 | 1 |
| `messages` | 105 | `id` | 1 | 1 |
| `mobile_refresh_tokens` | 0 | `id` | 0 | 3 |
| `notifications` | 5047 | `id` | 0 | 1 |
| `password_resets` | 359 | `id` | 0 | 1 |
| `payments` | 0 | `id` | 0 | 0 |
| `platform_config` | 10 | `key` | 0 | 1 |
| `post_applications` | 508 | `id` | 2 | 3 |
| `post_comments` | 14 | `id` | 2 | 1 |
| `post_hire_deposits` | 0 | `id` | 0 | 1 |
| `post_questions` | 0 | `id` | 1 | 1 |
| `posts` | 75 | `id` | 1 | 2 |
| `project_submissions` | 0 | `id` | 4 | 2 |
| `rate_events` | 12 | `id` | 0 | 1 |
| `referrals` | 1 | `id` | 0 | 3 |
| `review_log` | 0 | `id` | 1 | 2 |
| `security_deposits` | 52 | `id` | 0 | 0 |
| `signup_otps` | 0 | `id` | 0 | 1 |
| `sqlite_sequence` | 32 | `None` | 0 | 0 |
| `staff_accounts` | 3 | `id` | 0 | 2 |
| `staff_queue_roles` | 4 | `id` | 1 | 2 |
| `task_submissions` | 0 | `id` | 4 | 2 |
| `task_versions` | 0 | `id` | 1 | 2 |
| `tasks` | 2 | `id` | 0 | 1 |
| `tutor_progress` | 0 | `id` | 1 | 1 |
| `user_api_keys` | 0 | `id` | 1 | 2 |
| `user_sessions` | 3 | `id` | 0 | 1 |

---

## 2. Structural Analysis: Entity Clusters & Duplicated Concepts

### A. Applications Cluster
- `applications`: Main internship application pipeline (general candidate pool).
- `post_applications`: Job-board / specific post applications (company-specific marketplace).
- *Note for Migration*: Keep separate boundaries documented; do not merge without reconciling schemas.

### B. Enrollments Cluster
- `enrollments`: Core internship program onboarding, offer acceptance, deposit records.
- `cohort_enrollments`: Company/cohort-specific workshop registrations.
- `course_enrollments`: Self-paced or standalone LMS course enrollments.

### C. Financial & Ledger Cluster
- `payments`: Primary enrollment fee / deposit records.
- `security_deposits`: Legacy/specialized refundable security deposits.
- `post_hire_deposits`: ₹499 guarantee deposits for job-hire posts.
- `course_payments`: Standalone paid course purchases.
- `coin_ledger_mirror`: Ambassador referral reward coin ledger.
- `ambassador_withdrawals`: UPI cashout requests from ambassadors.

### D. Learning & Content Cluster
- `courses`, `course_chapters`, `course_subtopics`: Core LMS curriculum hierarchy.
- `course_day_quizzes`, `day_quiz_attempts`: Daily check-in tests.
- `course_subtopic_chats`, `tutor_progress`: AI guided learning chats and progress markers.
- `tasks`, `task_versions`, `task_submissions`: Weekly project/task assignments.
- `course_projects`, `project_submissions`: Capstone submissions.

---

## 3. Detailed Table Schema Definitions

### `abuse_log` (1082 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `timestamp` | `TEXT` | NO | `-` | - |
| `ip` | `TEXT` | YES | `-` | - |
| `route` | `TEXT` | YES | `-` | - |
| `bucket` | `TEXT` | YES | `-` | - |
| `reason` | `TEXT` | YES | `-` | - |
| `email` | `TEXT` | YES | `-` | - |

**Indexes:**
- `idx_abuse_time (NON-UNIQUE on id)`

---

### `ambassador_withdrawals` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `amount` | `INTEGER` | NO | `-` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `requested_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `reviewed_by_admin_id` | `INTEGER` | YES | `-` | - |
| `reviewed_at` | `TEXT` | YES | `-` | - |
| `admin_note` | `TEXT` | YES | `-` | - |
| `upi_viewed_by` | `TEXT` | YES | `-` | - |
| `upi_viewed_at` | `TEXT` | YES | `-` | - |

**Indexes:**
- `idx_withdrawals_intern (NON-UNIQUE on intern_id, status)`

---

### `applications` (4395 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `name` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `phone` | `TEXT` | NO | `-` | - |
| `city` | `TEXT` | NO | `-` | - |
| `college` | `TEXT` | NO | `-` | - |
| `course` | `TEXT` | NO | `-` | - |
| `semester` | `TEXT` | NO | `-` | - |
| `year_of_passing` | `TEXT` | NO | `-` | - |
| `domain` | `TEXT` | NO | `-` | - |
| `why_join` | `TEXT` | NO | `-` | - |
| `portfolio` | `TEXT` | YES | `-` | - |
| `status` | `TEXT` | YES | `'Apply Pending'` | - |
| `mentor_note` | `TEXT` | YES | `-` | - |
| `mentor_email` | `TEXT` | YES | `-` | - |
| `reviewed_at` | `TEXT` | YES | `-` | - |
| `visitor_id` | `TEXT` | YES | `-` | - |
| `source` | `TEXT` | YES | `'web'` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `rejected_at` | `TEXT` | YES | `-` | - |
| `enroll_reminders_sent` | `INTEGER` | YES | `0` | - |
| `last_reminder_at` | `TEXT` | YES | `-` | - |
| `intent_answers` | `TEXT` | YES | `-` | - |

**Indexes:**
- `sqlite_autoindex_applications_1 (UNIQUE on email, domain)`

---

### `attendance` (458 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `week_start` | `TEXT` | NO | `-` | - |
| `week_end` | `TEXT` | NO | `-` | - |
| `total_minutes` | `INTEGER` | YES | `0` | - |
| `updated_at` | `TEXT` | YES | `-` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `sqlite_autoindex_attendance_1 (UNIQUE on intern_id, week_start)`

---

### `check_log` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `timestamp` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `name` | `TEXT` | YES | `-` | - |
| `check_count` | `INTEGER` | YES | `-` | - |
| `ip` | `TEXT` | YES | `-` | - |

---

### `cohort_enrollments` (1 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `cohort_id` | `INTEGER` | NO | `-` | - |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `reminder_sent` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `cohort_id` -> `cohorts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_cohort_enr (NON-UNIQUE on cohort_id, intern_id)`
- `sqlite_autoindex_cohort_enrollments_1 (UNIQUE on cohort_id, intern_id)`

---

### `cohorts` (1 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `company_id` | `INTEGER` | NO | `-` | - |
| `title` | `TEXT` | NO | `-` | - |
| `description` | `TEXT` | YES | `-` | - |
| `skills` | `TEXT` | YES | `-` | - |
| `platform` | `TEXT` | YES | `-` | - |
| `meeting_url` | `TEXT` | YES | `-` | - |
| `starts_at` | `TEXT` | YES | `-` | - |
| `capacity` | `INTEGER` | YES | `0` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `company_id` -> `companies(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_cohorts_live (NON-UNIQUE on status, starts_at)`
- `idx_cohorts_company (NON-UNIQUE on company_id, status)`

---

### `coin_ledger_mirror` (1 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `ledger_kind` | `TEXT` | NO | `-` | - |
| `delta` | `INTEGER` | NO | `-` | - |
| `balance_after` | `INTEGER` | YES | `-` | - |
| `reason` | `TEXT` | YES | `-` | - |
| `event_ts` | `TEXT` | YES | `-` | - |
| `received_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `idem_key` | `TEXT` | YES | `-` | - |

**Indexes:**
- `idx_coin_mirror_kind (NON-UNIQUE on intern_id, ledger_kind)`
- `idx_coin_mirror_intern (NON-UNIQUE on intern_id, event_ts)`
- `sqlite_autoindex_coin_ledger_mirror_1 (UNIQUE on idem_key)`

---

### `companies` (3 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `name` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `phone` | `TEXT` | YES | `-` | - |
| `website` | `TEXT` | YES | `-` | - |
| `about` | `TEXT` | YES | `-` | - |
| `password_hash` | `TEXT` | YES | `-` | - |
| `is_approved` | `INTEGER` | YES | `0` | - |
| `is_active` | `INTEGER` | YES | `1` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Indexes:**
- `idx_companies_email (NON-UNIQUE on email)`
- `sqlite_autoindex_companies_1 (UNIQUE on email)`

---

### `company_follows` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `company_id` | `INTEGER` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `company_id` -> `companies(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_follows_intern (NON-UNIQUE on intern_id)`
- `idx_follows_company (NON-UNIQUE on company_id)`
- `sqlite_autoindex_company_follows_1 (UNIQUE on intern_id, company_id)`

---

### `conversations` (93 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `counterparty_type` | `TEXT` | NO | `-` | - |
| `counterparty_id` | `INTEGER` | NO | `-` | - |
| `post_id` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Indexes:**
- `idx_conv_cp (NON-UNIQUE on counterparty_type, counterparty_id, updated_at)`
- `idx_conv_intern (NON-UNIQUE on intern_id, updated_at)`
- `sqlite_autoindex_conversations_1 (UNIQUE on intern_id, counterparty_type, counterparty_id, post_id)`

---

### `course_chapters` (10 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `course_id` | `INTEGER` | NO | `-` | - |
| `day_number` | `INTEGER` | NO | `-` | - |
| `title` | `TEXT` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `course_id` -> `courses(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_chapters_course (NON-UNIQUE on course_id, day_number)`

---

### `course_day_quizzes` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `course_id` | `INTEGER` | NO | `-` | - |
| `day_number` | `INTEGER` | NO | `-` | - |
| `questions_json` | `TEXT` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `course_id` -> `courses(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `sqlite_autoindex_course_day_quizzes_1 (UNIQUE on course_id, day_number)`

---

### `course_enrollments` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `course_id` | `INTEGER` | NO | `-` | - |
| `enrolled_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `last_accessed_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `current_day` | `INTEGER` | YES | `1` | - |
| `completed_at` | `TEXT` | YES | `-` | - |

**Foreign Keys:**
- `course_id` -> `courses(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_course_enr_intern (NON-UNIQUE on intern_id)`
- `sqlite_autoindex_course_enrollments_1 (UNIQUE on intern_id, course_id)`

---

### `course_payments` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `course_id` | `INTEGER` | NO | `-` | - |
| `course_title` | `TEXT` | YES | `-` | - |
| `amount` | `INTEGER` | YES | `-` | - |
| `payment_screenshot` | `TEXT` | YES | `-` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `admin_note` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `-` | - |
| `platform_commission_pct` | `REAL` | YES | `15.0` | - |
| `author_earnings_inr` | `INTEGER` | YES | `0` | - |
| `commission_pct_snapshot` | `REAL` | YES | `0.0` | - |
| `commission_amount` | `REAL` | YES | `0.0` | - |
| `payee_type` | `TEXT` | YES | `'admin'` | - |
| `settled_at` | `TEXT` | YES | `-` | - |
| `razorpay_order_id` | `TEXT` | YES | `-` | - |
| `razorpay_payment_id` | `TEXT` | YES | `-` | - |
| `razorpay_signature` | `TEXT` | YES | `-` | - |

**Indexes:**
- `idx_course_pay_active (UNIQUE on intern_id, course_id)`

---

### `course_projects` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `course_id` | `INTEGER` | NO | `-` | - |
| `brief` | `TEXT` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `course_id` -> `courses(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `sqlite_autoindex_course_projects_1 (UNIQUE on course_id)`

---

### `course_subtopic_chats` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `enrollment_id` | `INTEGER` | NO | `-` | - |
| `subtopic_id` | `INTEGER` | NO | `-` | - |
| `role` | `TEXT` | NO | `-` | - |
| `message` | `TEXT` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `subtopic_id` -> `course_subtopics(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `enrollment_id` -> `course_enrollments(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_chats_subtopic (NON-UNIQUE on enrollment_id, subtopic_id)`

---

### `course_subtopics` (26 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `chapter_id` | `INTEGER` | NO | `-` | - |
| `sort_order` | `INTEGER` | NO | `-` | - |
| `title` | `TEXT` | NO | `-` | - |
| `brief` | `TEXT` | NO | `-` | - |
| `key_takeaways_json` | `TEXT` | YES | `-` | - |
| `prompt_seed` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `chapter_id` -> `course_chapters(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_subtopics_chapter (NON-UNIQUE on chapter_id, sort_order)`

---

### `courses` (2 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `title` | `TEXT` | NO | `-` | - |
| `slug` | `TEXT` | YES | `-` | - |
| `domain` | `TEXT` | YES | `-` | - |
| `company_id` | `INTEGER` | YES | `-` | - |
| `is_paid` | `INTEGER` | YES | `0` | - |
| `price_inr` | `INTEGER` | YES | `0` | - |
| `content_status` | `TEXT` | YES | `'pending'` | - |
| `source` | `TEXT` | YES | `'custom'` | - |
| `is_active` | `INTEGER` | YES | `1` | - |
| `payout_note` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `level` | `TEXT` | YES | `'Beginner'` | - |
| `estimated_hours` | `INTEGER` | YES | `10` | - |
| `author_type` | `TEXT` | YES | `'admin'` | - |
| `author_id` | `INTEGER` | YES | `-` | - |
| `requires_project` | `INTEGER` | YES | `0` | - |
| `banner_gradient` | `TEXT` | YES | `'linear-gradient(135deg, #8B5CF6, #3B82F6)'` | - |
| `updated_at` | `TEXT` | YES | `''` | - |

**Indexes:**
- `idx_courses_status (NON-UNIQUE on content_status, is_active)`

---

### `cvs` (140 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `slug` | `TEXT` | YES | `-` | - |
| `headline` | `TEXT` | YES | `-` | - |
| `summary` | `TEXT` | YES | `-` | - |
| `skills_json` | `TEXT` | YES | `-` | - |
| `projects_json` | `TEXT` | YES | `-` | - |
| `experience_json` | `TEXT` | YES | `-` | - |
| `education_json` | `TEXT` | YES | `-` | - |
| `links_json` | `TEXT` | YES | `-` | - |
| `is_public` | `INTEGER` | YES | `1` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_cvs_slug (NON-UNIQUE on slug)`
- `sqlite_autoindex_cvs_2 (UNIQUE on slug)`
- `sqlite_autoindex_cvs_1 (UNIQUE on intern_id)`

---

### `day_quiz_attempts` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `enrollment_id` | `INTEGER` | NO | `-` | - |
| `day_quiz_id` | `INTEGER` | NO | `-` | - |
| `score` | `INTEGER` | NO | `-` | - |
| `max_score` | `INTEGER` | NO | `-` | - |
| `passed` | `INTEGER` | NO | `-` | - |
| `tab_switches` | `INTEGER` | YES | `0` | - |
| `time_taken_sec` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `day_quiz_id` -> `course_day_quizzes(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `enrollment_id` -> `course_enrollments(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_quiz_attempts_enr (NON-UNIQUE on enrollment_id, day_quiz_id)`

---

### `dbert_fallback_usage` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `usage_date` | `TEXT` | NO | `-` | - |
| `count` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_fallback_usage (NON-UNIQUE on intern_id, usage_date)`
- `sqlite_autoindex_dbert_fallback_usage_1 (UNIQUE on intern_id, usage_date)`

---

### `device_profiles` (6356 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `visitor_id` | `TEXT` | YES | `-` | - |
| `email` | `TEXT` | YES | `-` | - |
| `ip_address` | `TEXT` | YES | `-` | - |
| `user_agent` | `TEXT` | YES | `-` | - |
| `screen_res` | `TEXT` | YES | `-` | - |
| `timezone` | `TEXT` | YES | `-` | - |
| `language` | `TEXT` | YES | `-` | - |
| `device_type` | `TEXT` | YES | `-` | - |
| `referrer` | `TEXT` | YES | `-` | - |
| `is_return_visit` | `INTEGER` | YES | `0` | - |
| `visit_count` | `INTEGER` | YES | `1` | - |
| `time_on_page` | `INTEGER` | YES | `0` | - |
| `intent_score` | `INTEGER` | YES | `0` | - |
| `path` | `TEXT` | YES | `-` | - |
| `last_seen` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Indexes:**
- `idx_device_visitor (UNIQUE on visitor_id)`

---

### `email_log` (6157 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `timestamp` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `name` | `TEXT` | YES | `-` | - |
| `subject` | `TEXT` | YES | `-` | - |
| `email_sent` | `TEXT` | YES | `'YES'` | - |
| `opened_at` | `TEXT` | YES | `-` | - |

---

### `enrollments` (308 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `application_id` | `INTEGER` | YES | `-` | - |
| `timestamp` | `TEXT` | YES | `-` | - |
| `name` | `TEXT` | YES | `-` | - |
| `email` | `TEXT` | YES | `-` | - |
| `phone` | `TEXT` | YES | `-` | - |
| `city` | `TEXT` | YES | `-` | - |
| `college` | `TEXT` | YES | `-` | - |
| `course` | `TEXT` | YES | `-` | - |
| `semester` | `TEXT` | YES | `-` | - |
| `year_of_passing` | `TEXT` | YES | `-` | - |
| `domain` | `TEXT` | YES | `-` | - |
| `joining_date` | `TEXT` | YES | `-` | - |
| `batch_label` | `TEXT` | YES | `-` | - |
| `payment_screenshot` | `TEXT` | YES | `-` | - |
| `payment_status` | `TEXT` | YES | `-` | - |
| `admin_note` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `-` | - |
| `updated_at` | `TEXT` | YES | `-` | - |
| `product` | `TEXT` | YES | `'free_deposit'` | - |
| `amount` | `INTEGER` | YES | `-` | - |
| `razorpay_order_id` | `TEXT` | YES | `-` | - |
| `razorpay_payment_id` | `TEXT` | YES | `-` | - |
| `razorpay_signature` | `TEXT` | YES | `-` | - |

---

### `intern_accounts` (2230 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `application_id` | `INTEGER` | YES | `-` | - |
| `name` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `phone` | `TEXT` | YES | `-` | - |
| `city` | `TEXT` | YES | `-` | - |
| `college` | `TEXT` | YES | `-` | - |
| `course` | `TEXT` | YES | `-` | - |
| `semester` | `TEXT` | YES | `-` | - |
| `year_of_passing` | `TEXT` | YES | `-` | - |
| `domain` | `TEXT` | YES | `-` | - |
| `password_hash` | `TEXT` | YES | `-` | - |
| `password_set` | `INTEGER` | YES | `0` | - |
| `is_active` | `INTEGER` | YES | `1` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `tutor_completion_pct` | `REAL` | YES | `0.0` | - |
| `tutor_updated_at` | `TEXT` | YES | `-` | - |
| `tutor_seconds_credited` | `INTEGER` | YES | `0` | - |
| `tutor_week_credited` | `TEXT` | YES | `''` | - |
| `linkedin_url` | `TEXT` | YES | `-` | - |
| `github_url` | `TEXT` | YES | `-` | - |
| `interview_attempts` | `INTEGER` | YES | `0` | - |
| `interview_last_attempt_at` | `TEXT` | YES | `-` | - |
| `interview_locked` | `INTEGER` | YES | `0` | - |
| `terms_accepted_at` | `TEXT` | YES | `-` | - |
| `newsletter_opt_in` | `INTEGER` | YES | `0` | - |
| `signup_stage` | `INTEGER` | YES | `3` | - |
| `referral_code` | `TEXT` | YES | `-` | - |
| `referred_by_intern_id` | `INTEGER` | YES | `-` | - |
| `upi_id_encrypted` | `TEXT` | YES | `-` | - |
| `email_verified` | `INTEGER` | YES | `0` | - |
| `account_status` | `TEXT` | YES | `-` | - |
| `visitor_id` | `TEXT` | YES | `NULL` | - |

**Foreign Keys:**
- `application_id` -> `applications(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_intern_referral_code (UNIQUE on referral_code)`
- `sqlite_autoindex_intern_accounts_1 (UNIQUE on email)`

---

### `intern_certificates` (3 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `course_id` | `INTEGER` | YES | `-` | - |
| `course_title` | `TEXT` | YES | `-` | - |
| `cert_id` | `TEXT` | YES | `-` | - |
| `issued_at` | `TEXT` | YES | `-` | - |
| `url` | `TEXT` | YES | `-` | - |
| `received_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `tier` | `TEXT` | YES | `'completed'` | - |

**Indexes:**
- `idx_intern_certs_intern (NON-UNIQUE on intern_id)`
- `sqlite_autoindex_intern_certificates_1 (UNIQUE on intern_id, cert_id)`

---

### `interviews` (576 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `email` | `TEXT` | NO | `-` | - |
| `application_id` | `INTEGER` | YES | `-` | - |
| `domain` | `TEXT` | YES | `-` | - |
| `attempt_no` | `INTEGER` | YES | `1` | - |
| `status` | `TEXT` | YES | `'not_started'` | - |
| `questions_json` | `TEXT` | YES | `-` | - |
| `answers_json` | `TEXT` | YES | `-` | - |
| `mentor_assessment_json` | `TEXT` | YES | `-` | - |
| `candidate_focus_json` | `TEXT` | YES | `-` | - |
| `github_summary` | `TEXT` | YES | `-` | - |
| `started_at` | `TEXT` | YES | `-` | - |
| `completed_at` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `post_id` | `INTEGER` | YES | `-` | - |
| `time_taken_sec` | `INTEGER` | YES | `0` | - |
| `tab_switches` | `INTEGER` | YES | `0` | - |

**Indexes:**
- `idx_interviews_email (NON-UNIQUE on email)`

---

### `mentor_availability_slots` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `mentor_staff_id` | `INTEGER` | NO | `-` | - |
| `start_time` | `TEXT` | NO | `-` | - |
| `end_time` | `TEXT` | NO | `-` | - |
| `is_booked` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `mentor_staff_id` -> `staff_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_mentor_slots (NON-UNIQUE on mentor_staff_id, is_booked, start_time)`

---

### `mentor_session_bookings` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `slot_id` | `INTEGER` | NO | `-` | - |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `meeting_link` | `TEXT` | YES | `-` | - |
| `status` | `TEXT` | YES | `'booked'` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `slot_id` -> `mentor_availability_slots(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_mentor_bookings (NON-UNIQUE on intern_id, status)`
- `sqlite_autoindex_mentor_session_bookings_1 (UNIQUE on slot_id)`

---

### `mentors` (4 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `name` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `domain` | `TEXT` | NO | `-` | - |
| `password_hash` | `TEXT` | YES | `-` | - |
| `is_active` | `INTEGER` | YES | `1` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Indexes:**
- `sqlite_autoindex_mentors_1 (UNIQUE on email)`

---

### `messages` (105 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `conversation_id` | `INTEGER` | NO | `-` | - |
| `sender_type` | `TEXT` | NO | `-` | - |
| `sender_id` | `INTEGER` | NO | `-` | - |
| `body` | `TEXT` | NO | `-` | - |
| `is_read` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `conversation_id` -> `conversations(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_msg_conv (NON-UNIQUE on conversation_id, id)`

---

### `mobile_refresh_tokens` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `token_hash` | `TEXT` | NO | `-` | - |
| `intern_id` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `issued_at` | `TEXT` | NO | `-` | - |
| `expires_at` | `TEXT` | NO | `-` | - |
| `revoked` | `INTEGER` | NO | `0` | - |
| `last_used_at` | `TEXT` | YES | `-` | - |

**Indexes:**
- `idx_mobile_refresh_intern (NON-UNIQUE on intern_id)`
- `idx_mobile_refresh_hash (NON-UNIQUE on token_hash)`
- `sqlite_autoindex_mobile_refresh_tokens_1 (UNIQUE on token_hash)`

---

### `notifications` (5047 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `kind` | `TEXT` | YES | `'general'` | - |
| `title` | `TEXT` | NO | `-` | - |
| `body` | `TEXT` | YES | `-` | - |
| `link` | `TEXT` | YES | `-` | - |
| `is_read` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Indexes:**
- `idx_notif_intern (NON-UNIQUE on intern_id, is_read, created_at)`

---

### `password_resets` (359 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `email` | `TEXT` | NO | `-` | - |
| `token` | `TEXT` | NO | `-` | - |
| `expires_at` | `TEXT` | NO | `-` | - |
| `used` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `account_type` | `TEXT` | NO | `'intern'` | - |
| `account_id` | `INTEGER` | YES | `-` | - |
| `used_at` | `TEXT` | YES | `-` | - |

**Indexes:**
- `sqlite_autoindex_password_resets_1 (UNIQUE on token)`

---

### `payments` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `mentor_email` | `TEXT` | NO | `-` | - |
| `intern_name` | `TEXT` | YES | `-` | - |
| `course_title` | `TEXT` | YES | `-` | - |
| `amount` | `INTEGER` | YES | `-` | - |
| `verified` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

---

### `platform_config` (10 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `key` | `TEXT` | YES | `-` | YES |
| `value` | `TEXT` | NO | `-` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Indexes:**
- `sqlite_autoindex_platform_config_1 (UNIQUE on key)`

---

### `post_applications` (508 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `post_id` | `INTEGER` | NO | `-` | - |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `comment` | `TEXT` | NO | `-` | - |
| `cv_id` | `INTEGER` | YES | `-` | - |
| `status` | `TEXT` | YES | `'Applied'` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `needed_certs_json` | `TEXT` | YES | `-` | - |
| `decision_note` | `TEXT` | YES | `-` | - |
| `decided_at` | `TEXT` | YES | `-` | - |
| `notified_at` | `TEXT` | YES | `-` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `post_id` -> `posts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_postapps_intern (NON-UNIQUE on intern_id)`
- `idx_postapps_post (NON-UNIQUE on post_id, id)`
- `sqlite_autoindex_post_applications_1 (UNIQUE on post_id, intern_id)`

---

### `post_comments` (14 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `post_id` | `INTEGER` | NO | `-` | - |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `body` | `TEXT` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `post_id` -> `posts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_postcomments_post (NON-UNIQUE on post_id, id)`

---

### `post_hire_deposits` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `post_application_id` | `INTEGER` | NO | `-` | - |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `post_id` | `INTEGER` | NO | `-` | - |
| `amount` | `INTEGER` | YES | `-` | - |
| `payment_screenshot` | `TEXT` | YES | `-` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `admin_note` | `TEXT` | YES | `-` | - |
| `refunded_at` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `-` | - |
| `razorpay_order_id` | `TEXT` | YES | `-` | - |
| `razorpay_payment_id` | `TEXT` | YES | `-` | - |
| `razorpay_signature` | `TEXT` | YES | `-` | - |

**Indexes:**
- `idx_post_hire_deposit_active (UNIQUE on post_application_id)`

---

### `post_questions` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `post_id` | `INTEGER` | NO | `-` | - |
| `company_id` | `INTEGER` | NO | `-` | - |
| `text` | `TEXT` | NO | `-` | - |
| `sort_order` | `INTEGER` | YES | `0` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `options` | `TEXT` | YES | `'[]'` | - |

**Foreign Keys:**
- `post_id` -> `posts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_postq_post (NON-UNIQUE on post_id, sort_order)`

---

### `posts` (75 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `company_id` | `INTEGER` | NO | `-` | - |
| `post_type` | `TEXT` | NO | `-` | - |
| `domain` | `TEXT` | NO | `-` | - |
| `title` | `TEXT` | NO | `-` | - |
| `slug` | `TEXT` | YES | `-` | - |
| `description` | `TEXT` | YES | `-` | - |
| `responsibilities` | `TEXT` | YES | `-` | - |
| `skills` | `TEXT` | YES | `-` | - |
| `location` | `TEXT` | YES | `-` | - |
| `work_mode` | `TEXT` | YES | `-` | - |
| `stipend_min` | `INTEGER` | YES | `-` | - |
| `stipend_max` | `INTEGER` | YES | `-` | - |
| `pay_period` | `TEXT` | YES | `-` | - |
| `is_unpaid` | `INTEGER` | YES | `0` | - |
| `duration` | `TEXT` | YES | `-` | - |
| `openings` | `INTEGER` | YES | `1` | - |
| `apply_by` | `TEXT` | YES | `-` | - |
| `certifications_json` | `TEXT` | YES | `-` | - |
| `eligibility` | `TEXT` | YES | `-` | - |
| `status` | `TEXT` | YES | `'draft'` | - |
| `published_at` | `TEXT` | YES | `-` | - |
| `expires_at` | `TEXT` | YES | `-` | - |
| `views` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `company_id` -> `companies(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_posts_live (NON-UNIQUE on post_type, status, domain)`
- `idx_posts_company (NON-UNIQUE on company_id, status)`

---

### `project_submissions` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `enrollment_id` | `INTEGER` | NO | `-` | - |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `course_id` | `INTEGER` | NO | `-` | - |
| `github_repo_url` | `TEXT` | NO | `-` | - |
| `project_title` | `TEXT` | NO | `-` | - |
| `project_description` | `TEXT` | NO | `-` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `reviewed_by_staff_id` | `INTEGER` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `reviewed_by_staff_id` -> `staff_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `course_id` -> `courses(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `enrollment_id` -> `course_enrollments(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_project_sub_intern (NON-UNIQUE on intern_id, course_id)`
- `idx_project_sub_status (NON-UNIQUE on status, created_at)`

---

### `rate_events` (12 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `bucket` | `TEXT` | NO | `-` | - |
| `created_at` | `REAL` | NO | `-` | - |

**Indexes:**
- `idx_rate_bucket_time (NON-UNIQUE on bucket, created_at)`

---

### `referrals` (1 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `referrer_intern_id` | `INTEGER` | NO | `-` | - |
| `referred_email` | `TEXT` | YES | `-` | - |
| `referred_intern_id` | `INTEGER` | YES | `-` | - |
| `source_code` | `TEXT` | YES | `-` | - |
| `status` | `TEXT` | YES | `'clicked'` | - |
| `flagged` | `INTEGER` | YES | `0` | - |
| `flag_reason` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `-` | - |

**Indexes:**
- `idx_referrals_unique_referred (UNIQUE on referred_intern_id)`
- `idx_referrals_referred (NON-UNIQUE on referred_intern_id)`
- `idx_referrals_referrer (NON-UNIQUE on referrer_intern_id, status)`

---

### `review_log` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `queue_name` | `TEXT` | NO | `-` | - |
| `staff_id` | `INTEGER` | NO | `-` | - |
| `subject_type` | `TEXT` | NO | `-` | - |
| `subject_id` | `INTEGER` | NO | `-` | - |
| `decision` | `TEXT` | NO | `-` | - |
| `reason_code` | `TEXT` | YES | `-` | - |
| `reviewed_input_snapshot` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `staff_id` -> `staff_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_review_subject (NON-UNIQUE on subject_type, subject_id)`
- `idx_review_queue (NON-UNIQUE on queue_name, created_at)`

---

### `security_deposits` (52 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `amount` | `INTEGER` | YES | `499` | - |
| `payment_screenshot` | `TEXT` | YES | `-` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `payment_type` | `TEXT` | YES | `'pending'` | - |
| `razorpay_order_id` | `TEXT` | YES | `-` | - |
| `razorpay_payment_id` | `TEXT` | YES | `-` | - |
| `razorpay_signature` | `TEXT` | YES | `-` | - |
| `admin_note` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `updated_at` | `TEXT` | YES | `-` | - |

---

### `signup_otps` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `email` | `TEXT` | NO | `-` | - |
| `otp` | `TEXT` | NO | `-` | - |
| `expires_at` | `TEXT` | NO | `-` | - |
| `is_used` | `INTEGER` | YES | `0` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Indexes:**
- `idx_signup_otps (NON-UNIQUE on email, is_used, expires_at)`

---

### `sqlite_sequence` (32 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `name` | `` | YES | `-` | - |
| `seq` | `` | YES | `-` | - |

---

### `staff_accounts` (3 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `name` | `TEXT` | NO | `-` | - |
| `email` | `TEXT` | NO | `-` | - |
| `password_hash` | `TEXT` | NO | `-` | - |
| `is_active` | `INTEGER` | YES | `1` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `role` | `TEXT` | YES | `"admin"` | - |

**Indexes:**
- `idx_staff_email (NON-UNIQUE on email)`
- `sqlite_autoindex_staff_accounts_1 (UNIQUE on email)`

---

### `staff_queue_roles` (4 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `staff_id` | `INTEGER` | NO | `-` | - |
| `queue_name` | `TEXT` | NO | `-` | - |

**Foreign Keys:**
- `staff_id` -> `staff_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_staff_roles (NON-UNIQUE on staff_id, queue_name)`
- `sqlite_autoindex_staff_queue_roles_1 (UNIQUE on staff_id, queue_name)`

---

### `task_submissions` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `task_id` | `INTEGER` | NO | `-` | - |
| `task_version_id` | `INTEGER` | NO | `-` | - |
| `submission_content` | `TEXT` | NO | `-` | - |
| `status` | `TEXT` | YES | `'pending'` | - |
| `coins_awarded` | `INTEGER` | YES | `0` | - |
| `reviewed_by_staff_id` | `INTEGER` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `submission_file` | `TEXT` | YES | `''` | - |

**Foreign Keys:**
- `reviewed_by_staff_id` -> `staff_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `task_version_id` -> `task_versions(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `task_id` -> `tasks(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_task_sub_intern (NON-UNIQUE on intern_id, task_id)`
- `idx_task_sub_status (NON-UNIQUE on status, created_at)`

---

### `task_versions` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `task_id` | `INTEGER` | NO | `-` | - |
| `version_number` | `INTEGER` | NO | `-` | - |
| `instructions` | `TEXT` | NO | `-` | - |
| `rubric` | `TEXT` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `task_id` -> `tasks(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_task_ver (NON-UNIQUE on task_id, version_number)`
- `sqlite_autoindex_task_versions_1 (UNIQUE on task_id, version_number)`

---

### `tasks` (2 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `title` | `TEXT` | NO | `-` | - |
| `description` | `TEXT` | NO | `-` | - |
| `coin_reward` | `INTEGER` | NO | `10` | - |
| `is_active` | `INTEGER` | YES | `1` | - |
| `author_type` | `TEXT` | YES | `'admin'` | - |
| `author_id` | `INTEGER` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `task_type` | `TEXT` | YES | `'general'` | - |
| `target_domain` | `TEXT` | YES | `''` | - |
| `payment_type` | `TEXT` | YES | `'paid'` | - |
| `submission_type` | `TEXT` | YES | `'url'` | - |

**Indexes:**
- `idx_tasks_active (NON-UNIQUE on is_active, created_at)`

---

### `tutor_progress` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `lessons_json` | `TEXT` | YES | `'[]'` | - |
| `quizzes_json` | `TEXT` | YES | `'[]'` | - |
| `projects_json` | `TEXT` | YES | `'[]'` | - |
| `completion_pct` | `REAL` | YES | `0.0` | - |
| `total_lessons` | `INTEGER` | YES | `0` | - |
| `done_lessons` | `INTEGER` | YES | `0` | - |
| `updated_at` | `TEXT` | YES | `-` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `sqlite_autoindex_tutor_progress_1 (UNIQUE on intern_id)`

---

### `user_api_keys` (0 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `intern_id` | `INTEGER` | NO | `-` | - |
| `encrypted_key` | `TEXT` | NO | `-` | - |
| `key_hash` | `TEXT` | YES | `-` | - |
| `validated_at` | `TEXT` | YES | `-` | - |
| `available_models_json` | `TEXT` | YES | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |

**Foreign Keys:**
- `intern_id` -> `intern_accounts(id)` (ON UPDATE NO ACTION, ON DELETE NO ACTION)

**Indexes:**
- `idx_user_keys_intern (NON-UNIQUE on intern_id)`
- `sqlite_autoindex_user_api_keys_1 (UNIQUE on key_hash)`

---

### `user_sessions` (3 rows)

| Column | Type | Nullable | Default | PK |
|---|---|---|---|---|
| `id` | `INTEGER` | YES | `-` | YES |
| `email` | `TEXT` | NO | `-` | - |
| `role` | `TEXT` | YES | `'intern'` | - |
| `session_token` | `TEXT` | NO | `-` | - |
| `expires_at` | `TEXT` | NO | `-` | - |
| `created_at` | `TEXT` | YES | `datetime('now','localtime')` | - |
| `next_url` | `TEXT` | YES | `-` | - |

**Indexes:**
- `sqlite_autoindex_user_sessions_1 (UNIQUE on session_token)`

---

