# DBERT Internship Portal — Comprehensive Route Inventory (INV-001)

**Document Date:** 2026-09-23  
**Total Registered Endpoints:** 231  
**Methodology:** Introspection of live `app.url_map` combined with AST/source code static analysis.

## 1. Summary by Role / Access Tier

| Access Role | Count | Description |
|---|---|---|
| **ADMIN** | 66 | Endpoints scoped to ADMIN permissions |
| **COMPANY** | 17 | Endpoints scoped to COMPANY permissions |
| **INTERN** | 42 | Endpoints scoped to INTERN permissions |
| **PUBLIC** | 98 | Endpoints scoped to PUBLIC permissions |
| **STAFF** | 8 | Endpoints scoped to STAFF permissions |

---

## Public & Visitor Endpoints (98)

| Route | Methods | Endpoint | Tables Touched | External Services | Response | Errors | Redirects | Purpose / Doc |
|---|---|---|---|---|---|---|---|---|
| `/` | `GET` | `index` | None direct | None | `HTML (Jinja)` | 500 | None |  |
| `/admin/logout` | `GET, POST` | `admin_logout` | None direct | None | `JSON` | 500 | "/admin-login" |  |
| `/ads.txt` | `GET` | `ads_txt` | None direct | None | `JSON` | 404 | None | Spec Â§7 â€” AdSense authorised-sellers file. |
| `/api/public/courses` | `GET` | `api_public_courses` | courses | None | `JSON` | 200/OK | None |  |
| `/api/stats/openings` | `GET` | `api_stats_openings` | None direct | None | `JSON` | 200/OK | None |  |
| `/apply` | `POST` | `apply` | applications, intern_accounts | Cloudflare Turnstile | `JSON` | 400, 500 | None | Unified signup+apply: creates intern_account and submits application |
| `/apply-token` | `GET` | `apply_token` | None direct | Cloudflare Turnstile | `JSON` | 500 | None | Issue a fresh signed timing token for the apply / re-apply / forgot forms (8.4). |
| `/attendance/ping` | `POST` | `attendance_ping` | attendance, enrollments, intern_accounts | None | `JSON` | 404, 401, 500 | None | Heartbeat endpoint called every 3 minutes from the dashboard. |
| `/auth/send-otp` | `POST` | `auth_send_otp` | signup_otps | Email (SMTP/Mailer) | `JSON` | 400 | None |  |
| `/auth/verify-otp` | `POST` | `auth_verify_otp` | intern_accounts, signup_otps | None | `JSON` | 400 | None |  |
| `/check-email` | `POST` | `check_email` | companies, intern_accounts | None | `JSON` | 400, 500 | None | Used by the signin panel to detect legacy no-password accounts. |
| `/company/login` | `GET` | `company_login_page` | None direct | None | `HTML (Jinja)` | 200/OK | None |  |
| `/company/login` | `POST` | `company_login` | companies | None | `JSON` | 401, 400, 500 | None |  |
| `/company/logout` | `POST` | `company_logout` | None direct | None | `JSON` | 200/OK | None |  |
| `/company/signup` | `GET` | `company_signup_page` | None direct | None | `HTML (Jinja)` | 200/OK | None |  |
| `/company/signup` | `POST` | `company_signup` | companies, posts | None | `JSON` | 400, 500 | None |  |
| `/cron/cohort-reminders` | `GET, POST` | `cron_cohort_reminders` | cohort_enrollments, cohorts | None | `JSON` | 403 | None | Send a one-time reminder ~1h before a cohort starts. CRON_SECRET-gated. |
| `/cron/enrollment-reminders` | `POST` | `cron_enrollment_reminders` | applications, enrollments | None | `JSON` | 401, 500 | None | Daily reminder to Selected-but-not-enrolled candidates. Secret-protected |
| `/cron/expire-posts` | `POST` | `cron_expire_posts` | posts | None | `JSON` | 403 | None | Daily cron: flip live posts past their 30-day window to 'expired'. |
| `/cv/<slug>` | `GET` | `cv_public` | None direct | None | `HTML (Jinja)` | 404 | None |  |
| `/cv/<slug>.pdf` | `GET` | `cv_pdf` | None direct | None | `JSON` | 404 | None |  |
| `/dashboard` | `GET` | `dashboard_page` | None direct | None | `Redirect` | 200/OK | "/portal" |  |
| `/e/o.gif` | `GET` | `email_open_pixel` | email_log | None | `HTML (Jinja)` | 200/OK | None | Phase 13 â€” email open tracking. Verifies the signed token, stamps opened_at on the |
| `/enroll` | `POST` | `enroll` | applications, enrollments, intern_accounts, mentors | File Storage | `JSON` | 404, 401, 403, 400, 500 | None |  |
| `/enrollment-count` | `GET` | `enrollment_count` | enrollments | None | `JSON` | 500 | None |  |
| `/forgot-password` | `POST` | `forgot_password` | companies, intern_accounts, password_resets | None | `JSON` | 400, 500 | None | Request a password reset. |
| `/generate-tutor-token` | `POST` | `generate_tutor_token` | courses | None | `JSON` | 401 | None |  |
| `/health` | `GET` | `health` | None direct | None | `JSON` | 200/OK | None | Lightweight liveness/readiness probe for EC2 monitoring / systemd / uptime checks. |
| `/intern/attendance` | `GET` | `intern_attendance` | attendance, intern_accounts | None | `JSON` | 404, 401, 500 | None | Return full attendance history for the logged-in intern. |
| `/intern/change-password` | `POST` | `intern_change_password` | intern_accounts | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/intern/interview/profile-urls` | `POST` | `interview_profile_urls` | intern_accounts | None | `JSON` | 401, 400, 500 | None | Optional/skippable. Save linkedin_url / github_url (host-validated). |
| `/intern/interview/start` | `POST` | `interview_start` | intern_accounts, interviews, post_applications, posts | File Storage | `JSON` | 404, 401, 403, 400, 500 | None | T5: post-gated. Requires post_id + a prior post_applications row for that |
| `/intern/interview/status` | `GET` | `interview_status` | intern_accounts, interviews, post_applications | None | `JSON` | 404, 401, 500 | None | Legacy (no ?post_id): global per-account snapshot, unchanged for old callers. |
| `/intern/interview/submit` | `POST` | `interview_submit` | applications, intern_accounts, interviews, post_applications | None | `JSON` | 404, 401, 400, 500 | None | Validate all answers, assess, store both blocks + anti-copy telemetry (informational |
| `/intern/learning-progress` | `GET` | `intern_tutor_progress` | course_chapters, course_day_quizzes, course_enrollments, course_subtopics, courses, day_quiz_attempts, enrollments, intern_accounts | None | `JSON` | 404, 401, 500 | None | Local guided-learning progress â€” reads course_enrollments, |
| `/intern/login` | `POST` | `intern_login` | intern_accounts, tasks | None | `JSON` | 401, 400, 500 | None |  |
| `/intern/me` | `GET` | `intern_me` | applications, attendance, companies, course_day_quizzes, course_enrollments, courses, day_quiz_attempts, enrollments, intern_accounts, post_applications, post_hire_deposits, posts, task_submissions, tasks | File Storage, Payment Gateway / UPI | `JSON` | 404, 401, 500 | None |  |
| `/intern/messages` | `GET` | `intern_messages_json` | conversations, messages | None | `JSON` | 401 | "/portal#messages" |  |
| `/intern/messages/<int:conv_id>` | `GET` | `intern_messages_thread_json` | conversations, messages | None | `JSON` | 404, 401 | None |  |
| `/intern/save-wizard-step` | `POST` | `intern_save_wizard_step` | applications, enrollments, intern_accounts, mentors | File Storage | `JSON` | 404, 401, 403, 400, 500 | None | Atomically saves an individual onboarding wizard step (domain, academic_profile, application_sop, joining_date, payment_screenshot) |
| `/intern/tutor-progress` | `GET` | `intern_tutor_progress` | course_chapters, course_day_quizzes, course_enrollments, course_subtopics, courses, day_quiz_attempts, enrollments, intern_accounts | None | `JSON` | 404, 401, 500 | None | Local guided-learning progress â€” reads course_enrollments, |
| `/intern/update-profile` | `POST` | `intern_update_profile` | intern_accounts | None | `JSON` | 401, 400, 500 | None | Update editable intern fields. email + domain are LOCKED (never changed). |
| `/intern/wizard-status` | `GET` | `intern_wizard_status` | mentors | File Storage, Payment Gateway / UPI | `JSON` | 404, 401, 500 | None | Inspects intern profile and stage according to the strict 5-stage lifecycle: |
| `/internship` | `GET` | `_legacy_internship_root` | None direct | None | `Redirect` | 200/OK | None | T0: collapsed dual-route migration â€” old root prefix now 301s to clean URLs. |
| `/internship/` | `GET` | `_legacy_internship_root` | None direct | None | `Redirect` | 200/OK | None | T0: collapsed dual-route migration â€” old root prefix now 301s to clean URLs. |
| `/internship/<path:rest>` | `GET` | `_legacy_internship_redirect` | None direct | None | `Redirect` | 200/OK | None | T0: collapsed dual-route migration â€” old /internship/... URLs 301 to their clean equivalent. |
| `/internships` | `GET` | `internships_listing` | None direct | None | `HTML (Jinja)` | 200/OK | None |  |
| `/internships/<int:post_id>` | `GET` | `post_detail_no_slug` | posts | None | `Redirect` | 404 | None | Slugless deep link â†’ 301 to the canonical <slug>-<id> URL (or 404/410). |
| `/internships/<slug>` | `GET` | `internships_by_city` | None direct | None | `Redirect` | 404 | None |  |
| `/internships/<slug>-<int:post_id>` | `GET` | `internship_detail` | None direct | None | `HTML (Jinja)` | 200/OK | None |  |
| `/interview` | `GET` | `interview_page` | None direct | None | `HTML (Jinja)` | 500 | "/#signin" | Phase 11.6 â€” candidate-initiated AI interview page. Intern session required. |
| `/jd/<domain>` | `GET` | `get_jd` | None direct | None | `JSON` | 404, 500 | None |  |
| `/jobs` | `GET` | `jobs_listing` | None direct | None | `HTML (Jinja)` | 200/OK | None |  |
| `/jobs/<int:post_id>` | `GET` | `post_detail_no_slug` | posts | None | `Redirect` | 404 | None | Slugless deep link â†’ 301 to the canonical <slug>-<id> URL (or 404/410). |
| `/jobs/<slug>` | `GET` | `jobs_by_city` | None direct | None | `Redirect` | 404 | None |  |
| `/jobs/<slug>-<int:post_id>` | `GET` | `job_detail` | None direct | None | `HTML (Jinja)` | 200/OK | None |  |
| `/logout` | `GET, POST` | `logout` | None direct | None | `JSON` | 500 | "/" |  |
| `/mentor` | `GET` | `mentor_page` | None direct | None | `HTML (Jinja)` | 500 | None |  |
| `/mentor/applications` | `GET` | `mentor_applications` | applications, enrollments, mentors | None | `JSON` | 404, 401, 500 | None |  |
| `/mentor/interview/<path:email>` | `GET` | `mentor_interview_view` | applications | None | `JSON` | 404, 401, 403, 500 | None |  |
| `/mentor/login` | `POST` | `mentor_login` | mentors | None | `JSON` | 401, 400, 500 | None |  |
| `/mentor/me` | `GET` | `mentor_me` | mentors | None | `JSON` | 404, 401, 500 | None |  |
| `/mentor/update-status` | `POST` | `mentor_update_status` | applications | None | `JSON` | 404, 401, 403, 400, 500 | None |  |
| `/messages` | `GET` | `messages_inbox` | conversations, messages | None | `HTML (Jinja)` | 200/OK | "/portal#messages", "/#signin" |  |
| `/messages/<int:conv_id>` | `GET` | `messages_thread` | conversations, messages | None | `HTML (Jinja)` | 404 | "/#signin" |  |
| `/messages/<int:conv_id>/poll` | `GET` | `messages_poll` | conversations, messages | None | `JSON` | 404, 401 | None |  |
| `/messages/<int:conv_id>/send` | `POST` | `messages_send` | conversations, messages | None | `JSON` | 404, 401, 403, 400 | None |  |
| `/messages/start` | `POST` | `messages_start` | intern_accounts, messages | None | `JSON` | 401, 403, 400 | None |  |
| `/paid/enroll` | `POST` | `paid_enroll` | applications, enrollments, intern_accounts | File Storage | `JSON` | 404, 401, 400, 500 | None |  |
| `/portal` | `GET` | `portal_page` | None direct | None | `HTML (Jinja)` | 500 | "/#signin" | Phase 13 — unified tabbed portal (merges the old /profile + /dashboard). |
| `/portal/certificate/<cert_id>` | `GET` | `portal_view_certificate` | intern_accounts, intern_certificates | None | `HTML (Jinja)` | 404 | None | View certificate verification page. |
| `/portal/messages` | `GET` | `messages_inbox` | conversations, messages | None | `HTML (Jinja)` | 200/OK | "/portal#messages", "/#signin" |  |
| `/portal/messages/<int:conv_id>` | `GET` | `messages_thread` | conversations, messages | None | `HTML (Jinja)` | 404 | "/#signin" |  |
| `/portal/messages/<int:conv_id>/poll` | `GET` | `messages_poll` | conversations, messages | None | `JSON` | 404, 401 | None |  |
| `/portal/messages/<int:conv_id>/send` | `POST` | `messages_send` | conversations, messages | None | `JSON` | 404, 401, 403, 400 | None |  |
| `/portal/messages/start` | `POST` | `messages_start` | intern_accounts, messages | None | `JSON` | 401, 403, 400 | None |  |
| `/post-hire/deposit` | `POST` | `post_hire_deposit` | intern_accounts, post_applications, post_hire_deposits | File Storage | `JSON` | 404, 401, 400, 500 | None | Track 5: â‚¹499 refundable security deposit for a job-board hire. Triggers only |
| `/posts/<int:post_id>/comments` | `GET` | `post_comments` | intern_accounts, post_applications, post_comments, posts | None | `JSON` | 200/OK | None | T4: public comment thread (post_comments) â€” any signed-up intern, no |
| `/privacy` | `GET` | `privacy_page` | None direct | None | `HTML (Jinja)` | 200/OK | None | Phase 13 â€” Privacy Policy (public, indexable). Linked from the signup consent. |
| `/profile` | `GET` | `profile_page` | None direct | None | `Redirect` | 200/OK | "/portal" |  |
| `/program` | `GET` | `program_page` | None direct | Payment Gateway / UPI | `HTML (Jinja)` | 500 | None | Phase 12.3 â€” public, indexable paid-program landing page (terms shown before any CTA). |
| `/r/click` | `GET` | `ambassador.referral_click` | None direct | None | `JSON` | 400 | None | Anonymous click beacon for /?ref=<code> (§6.1). Always 204 — a bad or |
| `/reset` | `GET` | `reset_password_page` | None direct | None | `HTML (Jinja)` | 500 | None | Render the reset-password page; JS reads ?token= from the URL. |
| `/reset-password` | `POST` | `reset_password` | companies, intern_accounts, password_resets, user_sessions | None | `JSON` | 400, 500 | None | Complete a password reset using a token. |
| `/robots.txt` | `GET` | `robots_txt` | messages | None | `JSON` | 200/OK | None | Phase 12.6 â€” public/JD/program indexable; private surfaces disallowed. |
| `/set-password` | `POST` | `set_password` | None direct | None | `JSON` | 200/OK | None |  |
| `/signin` | `GET` | `signin_page` | None direct | None | `Redirect` | 200/OK | "/#signin" | Redirect to index with hash â€” index.html handles the panel. |
| `/signup` | `GET` | `signup_page` | None direct | None | `Redirect` | 200/OK | "/#signup" |  |
| `/signup/stage1` | `POST` | `signup_stage1` | applications, intern_accounts, user_sessions | Cloudflare Turnstile | `JSON` | 400, 500 | None |  |
| `/signup/stage2` | `POST` | `signup_stage2` | intern_accounts | None | `JSON` | 401, 400, 500 | None |  |
| `/signup/stage3` | `POST` | `signup_stage3` | applications, intern_accounts, user_sessions | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/sitemap.xml` | `GET` | `sitemap_xml` | cvs, posts | None | `JSON` | 200/OK | None | Phase 12.6 / 13 â€” only the public, indexable URLs (homepage, program, legal). |
| `/staff/logout` | `GET` | `staff_logout` | None direct | None | `Redirect` | 200/OK | "/staff/login" |  |
| `/status` | `GET` | `check_status` | applications, check_log, enrollments | None | `JSON` | 401, 403, 400, 500 | None |  |
| `/terms` | `GET` | `terms_page` | None direct | None | `HTML (Jinja)` | 200/OK | None | Phase 13 â€” Terms & Conditions (public, indexable). Linked from the signup consent. |
| `/track-visit` | `POST` | `track_visit` | device_profiles | None | `JSON` | 400, 500 | None |  |
| `/unsubscribe` | `GET` | `unsubscribe` | intern_accounts, messages | None | `JSON` | 200/OK | None | Phase 13 â€” one-click newsletter unsubscribe (signed link from email footer / |
| `/upcoming-mondays` | `GET` | `upcoming_mondays` | None direct | None | `JSON` | 500 | None | Return list of upcoming Monday dates for the joining date picker. |

---

## Intern & Candidate Endpoints (42)

| Route | Methods | Endpoint | Tables Touched | External Services | Response | Errors | Redirects | Purpose / Doc |
|---|---|---|---|---|---|---|---|---|
| `/account/coins` | `GET` | `account_coins_ledger` | coin_ledger_mirror | None | `HTML (Jinja)` | 200/OK | "/#signin" |  |
| `/account/gemini-key` | `GET, POST` | `account_gemini_key` | user_api_keys | AI Service | `JSON` | 401, 400 | "/#signin" |  |
| `/ambassador` | `GET` | `ambassador.ambassador_page` | None direct | None | `HTML (Jinja)` | 200/OK | "/#signin" | Intern-facing College Ambassador tab (§6.6). |
| `/apply/<int:post_id>` | `GET` | `apply_entry` | posts | None | `Redirect` | 404 | "/signup" | Apply-Now entry. Logged-in â†’ post detail with the apply modal open. |
| `/cohorts/<int:cohort_id>/enroll` | `POST` | `cohort_enroll` | cohort_enrollments, cohorts | None | `JSON` | 404, 401 | None |  |
| `/companies/<slug>` | `GET` | `company_profile` | cohorts, companies, company_follows, posts | None | `HTML (Jinja)` | 404 | None |  |
| `/courses` | `GET` | `courses_catalog` | companies, course_chapters, courses | None | `HTML (Jinja)` | 200/OK | None |  |
| `/courses/<int:course_id>` | `GET` | `course_detail` | companies, course_chapters, course_enrollments, course_subtopics, courses | None | `HTML (Jinja)` | 404 | "/courses" |  |
| `/courses/<int:course_id>/enroll` | `POST` | `course_enroll` | course_enrollments, courses, enrollments | None | `JSON` | 404, 401, 403, 400 | "/courses", "/portal", "/#signin" |  |
| `/courses/<int:course_id>/enroll-coins` | `POST` | `course_enroll_coins` | coin_ledger_mirror, course_enrollments, courses | None | `JSON` | 404, 401, 400 | None |  |
| `/courses/<int:course_id>/learn` | `GET` | `course_learn_page` | course_chapters, course_enrollments, course_subtopics, courses, user_api_keys | AI Service | `HTML (Jinja)` | 404 | "/portal", "/#signin" |  |
| `/courses/<int:course_id>/quiz/<int:day_number>` | `GET` | `course_quiz_page` | course_chapters, course_day_quizzes, course_enrollments, course_subtopics, courses | AI Service | `JSON` | 404, 500 | "/#signin" |  |
| `/courses/<int:course_id>/quiz/<int:day_number>/submit` | `POST` | `course_quiz_submit` | course_day_quizzes, course_enrollments, courses, day_quiz_attempts | None | `JSON` | 404, 401, 403 | None |  |
| `/courses/<int:course_id>/submit-project` | `GET, POST` | `course_submit_project` | course_day_quizzes, course_enrollments, course_projects, courses, day_quiz_attempts, project_submissions | None | `JSON` | 404, 401, 403, 400 | "/#signin" |  |
| `/courses/<int:course_id>/subtopic/<int:subtopic_id>` | `GET` | `course_subtopic_detail` | course_chapters, course_enrollments, course_subtopic_chats, course_subtopics, courses, user_api_keys | AI Service | `JSON` | 404, 401, 403 | None |  |
| `/courses/<int:course_id>/subtopic/<int:subtopic_id>/chat` | `POST` | `course_subtopic_chat` | course_enrollments, course_subtopic_chats, course_subtopics, courses, user_api_keys | AI Service | `JSON` | 404, 401, 403, 400 | None |  |
| `/enrollment/paid-1999` | `POST` | `enrollment_paid_1999` | course_payments, courses | File Storage | `JSON` | 404, 401, 403, 400 | None |  |
| `/first-run` | `GET` | `first_run` | None direct | None | `HTML (Jinja)` | 200/OK | "/#signin" |  |
| `/intern/ambassador` | `GET` | `ambassador.intern_ambassador` | ambassador_withdrawals, intern_accounts, referrals | Payment Gateway / UPI | `JSON` | 404, 401, 500 | None | Funnel stats, referral link, referral-coin balance, masked UPI (Â§6.6). |
| `/intern/ambassador/upi` | `POST` | `ambassador.intern_ambassador_upi` | intern_accounts | Payment Gateway / UPI | `JSON` | 401, 400, 500 | None | Store the payout UPI id â€” encrypted at rest, never returned in clear. |
| `/intern/ambassador/withdraw` | `POST` | `ambassador.intern_ambassador_withdraw` | ambassador_withdrawals, intern_accounts | Payment Gateway / UPI | `JSON` | 401, 400, 500 | None | Request a payout. Draws ONLY on the referral ledger (§6.5). |
| `/intern/certificates` | `GET` | `intern_certificates_json` | intern_certificates | None | `JSON` | 401, 500 | None | Return earned certificates for the logged-in intern. |
| `/intern/cohorts` | `GET` | `intern_cohorts` | cohort_enrollments, cohorts, companies | None | `JSON` | 401 | None |  |
| `/intern/coins` | `GET` | `intern_coins_json` | coin_ledger_mirror | None | `JSON` | 401, 500 | None | Return intern's coin balances and ledger activity. |
| `/intern/cv-meta` | `GET` | `intern_cv_meta` | cvs | None | `JSON` | 401 | None | UAT #29: lightweight CV status for the dashboard card (exists / slug / public). |
| `/intern/follow/<int:company_id>` | `POST` | `intern_follow_company` | companies, company_follows | None | `JSON` | 404, 401 | None |  |
| `/intern/leaderboard` | `GET` | `intern_leaderboard_proxy` | None direct | None | `JSON` | 401, 500 | None | JSON for the portal Leaderboard tab — global + own-domain composite boards |
| `/intern/my-applications` | `GET` | `intern_my_applications` | applications, companies, interviews, post_applications, posts | None | `JSON` | 401, 500 | None | Track 2 Â§B (UAT #4): the logged-in intern's job/internship applications + |
| `/intern/notifications` | `GET` | `intern_notifications` | notifications | None | `JSON` | 401 | None |  |
| `/intern/notifications/<int:notif_id>/read` | `POST` | `intern_notification_read` | notifications | None | `JSON` | 401 | None |  |
| `/intern/notifications/read-all` | `POST` | `intern_notifications_read_all` | notifications | None | `JSON` | 401 | None |  |
| `/intern/unfollow/<int:company_id>` | `POST` | `intern_unfollow_company` | company_follows | None | `JSON` | 401 | None |  |
| `/mentors/slots` | `GET` | `intern_mentor_slots` | mentor_availability_slots, mentor_session_bookings, mentors, staff_accounts | None | `HTML (Jinja)` | 200/OK | "/#signin" |  |
| `/mentors/slots/<int:slot_id>/book` | `POST` | `intern_book_slot` | mentor_availability_slots, mentor_session_bookings, mentors | None | `JSON` | 401, 403, 400 | None |  |
| `/portal/cv` | `GET` | `portal_cv_editor` | cvs | None | `HTML (Jinja)` | 200/OK | "/portal" |  |
| `/portal/cv` | `POST` | `portal_cv_save` | cvs | File Storage | `JSON` | 401 | None |  |
| `/post-hire/launch-tasks` | `GET` | `post_hire_launch_tasks` | post_applications, post_hire_deposits, tasks | None | `Redirect` | 200/OK | "/portal?launch_tasks=ineligible#overview", "/tasks", "/#signin" | Track 6 / T6: hand a Hired + deposit-verified intern straight into the |
| `/posts/<int:post_id>/apply` | `POST` | `post_apply` | applications, companies, courses, cvs, intern_certificates, post_applications, posts | None | `JSON` | 404, 401, 400 | None |  |
| `/posts/<int:post_id>/comment` | `POST` | `post_comment_add` | intern_accounts, post_applications, post_comments, posts | None | `JSON` | 404, 401, 400 | None | T4: any signed-up intern can post a public comment on a post without |
| `/tasks` | `GET` | `tasks_list` | task_submissions, tasks | None | `HTML (Jinja)` | 200/OK | None |  |
| `/tasks/<int:task_id>` | `GET` | `task_detail` | task_submissions, task_versions, tasks | None | `JSON` | 404 | None |  |
| `/tasks/<int:task_id>/submit` | `POST` | `task_submit` | task_submissions, task_versions, tasks | File Storage | `JSON` | 404, 401, 403, 400 | None |  |

---

## Company & Employer Endpoints (17)

| Route | Methods | Endpoint | Tables Touched | External Services | Response | Errors | Redirects | Purpose / Doc |
|---|---|---|---|---|---|---|---|---|
| `/company` | `GET` | `company_dashboard` | posts | None | `HTML (Jinja)` | 200/OK | "/company/login" |  |
| `/company/applications/<int:app_id>/status` | `POST` | `company_app_status` | applications, courses, intern_accounts, intern_certificates, post_applications, posts | None | `JSON` | 404, 401, 400 | None |  |
| `/company/change-password` | `POST` | `company_change_password` | companies | None | `JSON` | 401, 400, 500 | None | Track 2 Â§B (UAT #4): company self-service password change (Account section). |
| `/company/cohorts` | `GET` | `company_cohorts` | cohort_enrollments, cohorts | None | `HTML (Jinja)` | 200/OK | "/company/login" |  |
| `/company/cohorts` | `POST` | `company_cohort_create` | cohorts | None | `JSON` | 401, 403, 400 | None |  |
| `/company/courses` | `POST` | `company_course_create` | course_chapters, course_subtopics, courses | None | `JSON` | 401, 400 | None | Company creates a priced (or free) course. Always inserted as content_status |
| `/company/earnings` | `GET` | `company_earnings` | course_payments, courses, intern_accounts, payments | None | `HTML (Jinja)` | 200/OK | "/company/login" |  |
| `/company/posts` | `POST` | `company_post_save` | posts | File Storage | `JSON` | 404, 401, 400 | None |  |
| `/company/posts/<int:post_id>` | `GET` | `company_post_manage` | posts | None | `HTML (Jinja)` | 404 | "/company/login" |  |
| `/company/posts/<int:post_id>/applicants` | `GET` | `company_applicants` | cvs, intern_accounts, intern_certificates, interviews, post_applications, posts | None | `HTML (Jinja)` | 404 | "/company/login" |  |
| `/company/posts/<int:post_id>/delete` | `POST` | `company_post_delete` | post_applications, posts | None | `JSON` | 404, 401 | None | T6: soft-delete only -- post_applications FKs to posts.id, so a hard DELETE |
| `/company/posts/<int:post_id>/publish` | `POST` | `company_post_publish` | posts | None | `JSON` | 404, 401, 403, 400 | None |  |
| `/company/posts/<int:post_id>/questions` | `GET` | `company_post_questions_list` | post_questions, posts | File Storage | `JSON` | 404, 401 | None | T6: a company's own uploaded interview questions for one post (any status). |
| `/company/posts/<int:post_id>/questions` | `POST` | `company_post_questions_save` | post_questions, posts | File Storage | `JSON` | 404, 401, 400, 500 | None | T6: replace this post's question set. UGC -- always re-inserted as 'pending'; |
| `/company/posts/<int:post_id>/unpublish` | `POST` | `company_post_unpublish` | posts | None | `JSON` | 401, 400 | None |  |
| `/company/posts/new` | `GET` | `company_post_new` | posts | None | `HTML (Jinja)` | 200/OK | "/company/login" |  |
| `/company/profile` | `GET, POST` | `company_profile_edit` | companies | None | `HTML (Jinja)` | 200/OK | "/#company", "/company/profile" |  |

---

## Mentor Endpoints (0)

| Route | Methods | Endpoint | Tables Touched | External Services | Response | Errors | Redirects | Purpose / Doc |
|---|---|---|---|---|---|---|---|---|

---

## Staff & Queue Review Endpoints (8)

| Route | Methods | Endpoint | Tables Touched | External Services | Response | Errors | Redirects | Purpose / Doc |
|---|---|---|---|---|---|---|---|---|
| `/mentor/earnings` | `GET` | `mentor_earnings` | course_payments, courses, intern_accounts, payments | None | `HTML (Jinja)` | 200/OK | "/mentor/login" |  |
| `/staff/dashboard` | `GET` | `staff_dashboard` | course_payments, courses, payments, project_submissions, staff_queue_roles, task_submissions, tasks | None | `HTML (Jinja)` | 200/OK | "/staff/login" |  |
| `/staff/login` | `GET, POST` | `staff_login` | staff_accounts | None | `JSON` | 401, 400 | "/staff/dashboard" |  |
| `/staff/mentor-slots` | `GET, POST` | `staff_mentor_slots` | intern_accounts, mentor_availability_slots, mentor_session_bookings | None | `JSON` | 401, 400 | "/staff/login" |  |
| `/staff/projects` | `GET` | `staff_project_queue` | courses, intern_accounts, project_submissions | None | `HTML (Jinja)` | 200/OK | "/staff/login" |  |
| `/staff/projects/<int:submission_id>/decision` | `POST` | `staff_project_decision` | courses, cvs, intern_accounts, intern_certificates, project_submissions | None | `JSON` | 404, 401, 400 | None |  |
| `/staff/tasks` | `GET` | `staff_task_queue` | intern_accounts, task_submissions, tasks | None | `HTML (Jinja)` | 200/OK | "/staff/login" |  |
| `/staff/tasks/<int:submission_id>/decision` | `POST` | `staff_task_decision` | intern_accounts, task_submissions, tasks | None | `JSON` | 404, 401, 400 | None |  |

---

## Admin & Executive Endpoints (66)

| Route | Methods | Endpoint | Tables Touched | External Services | Response | Errors | Redirects | Purpose / Doc |
|---|---|---|---|---|---|---|---|---|
| `/admin` | `GET` | `admin_page` | None direct | None | `HTML (Jinja)` | 500 | "/admin-login" |  |
| `/admin-login` | `GET` | `admin_login_page` | None direct | None | `HTML (Jinja)` | 500 | "/admin" |  |
| `/admin/abuse-log` | `GET` | `admin_abuse_log` | abuse_log | None | `JSON` | 401, 500 | None | Phase 8.6: read-only recent abuse/blocked events for the admin Security tab. |
| `/admin/add-application` | `POST` | `admin_add_application` | applications, intern_accounts | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/add-mentor` | `POST` | `admin_add_mentor` | mentors | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/ambassador-payouts` | `GET` | `ambassador.admin_ambassador_payouts` | ambassador_withdrawals, intern_accounts | None | `HTML (Jinja)` | 200/OK | "/admin/login" | Payout queue (Â§6.5) â€” mirrors /admin/post-hire-deposits. |
| `/admin/ambassador-payouts/<int:wid>/decision` | `POST` | `ambassador.admin_ambassador_decision` | ambassador_withdrawals | None | `JSON` | 404, 401, 400 | None | Mark a payout Paid or Rejected. On Paid, debit the referral ledger. |
| `/admin/ambassador-payouts/<int:wid>/upi` | `POST` | `ambassador.admin_ambassador_reveal_upi` | ambassador_withdrawals, intern_accounts | Payment Gateway / UPI | `JSON` | 404, 401 | None | Decrypt and return the UPI id ONCE, logging who looked and when (Â§6.5). |
| `/admin/application/edit` | `POST` | `admin_application_edit` | applications | None | `JSON` | 404, 401, 400, 500 | None | Allows admin to edit application details, status, and mentor notes. |
| `/admin/application/update` | `POST` | `admin_application_update` | applications | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/admin/applications` | `GET` | `admin_applications` | applications | None | `JSON` | 401, 500 | None |  |
| `/admin/applications/bulk-delete` | `POST` | `admin_applications_bulk_delete` | applications | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/attendance` | `GET` | `admin_attendance` | applications, attendance, enrollments, intern_accounts | None | `JSON` | 401, 500 | None | Return attendance data for all accepted interns â€” for the Attendance tab. |
| `/admin/cohorts` | `GET` | `admin_cohorts` | cohorts, companies | None | `HTML (Jinja)` | 200/OK | "/admin-login" |  |
| `/admin/cohorts/<int:cohort_id>/review` | `POST` | `admin_cohort_review` | cohorts, companies | None | `JSON` | 404, 401, 400 | None |  |
| `/admin/companies` | `GET` | `admin_companies` | companies | None | `HTML (Jinja)` | 200/OK | "/admin-login" |  |
| `/admin/companies/approve` | `POST` | `admin_company_approve` | companies | None | `JSON` | 401 | None |  |
| `/admin/companies/suspend` | `POST` | `admin_company_suspend` | companies | None | `JSON` | 401 | None |  |
| `/admin/course-payments` | `GET` | `admin_course_payments` | course_payments, intern_accounts, payments | None | `JSON` | 401 | None |  |
| `/admin/course-payments/<int:pay_id>/review` | `POST` | `admin_course_payment_review` | course_payments, courses, intern_accounts, payments | None | `JSON` | 404, 401, 400 | None |  |
| `/admin/courses` | `GET` | `admin_courses_list` | companies, courses | None | `JSON` | 401 | None | Default to pending (the review queue); ?status=approved|rejected for history. |
| `/admin/courses/<int:course_id>/review` | `POST` | `admin_course_review` | courses | None | `JSON` | 404, 401, 400 | None | Approve = DBERT co-signs the content (unlocks the industrial-cert attribute + |
| `/admin/courses/<int:course_id>/toggle` | `POST` | `admin_course_toggle` | courses | None | `JSON` | 404, 401 | None |  |
| `/admin/csv/applications` | `GET` | `admin_csv_applications` | applications, enrollments | None | `JSON` | 401, 500 | None |  |
| `/admin/csv/attendance` | `GET` | `admin_csv_attendance` | attendance, intern_accounts | None | `JSON` | 401, 500 | None |  |
| `/admin/csv/devices` | `GET` | `admin_csv_devices` | device_profiles | None | `JSON` | 401, 500 | None |  |
| `/admin/csv/enrollments` | `GET` | `admin_csv_enrollments` | enrollments | None | `JSON` | 401, 500 | None |  |
| `/admin/csv/incomplete-signups` | `GET` | `admin_csv_incomplete_signups` | applications, intern_accounts, post_applications | None | `JSON` | 401, 500 | None |  |
| `/admin/csv/interviews` | `GET` | `admin_csv_interviews` | intern_accounts, interviews | None | `JSON` | 401, 500 | None | Every interview's questions + answers, one row per question-answer pair, for |
| `/admin/csv/upload` | `POST` | `admin_csv_upload_legacy` | None direct | File Storage | `JSON` | 401, 400, 500 | None |  |
| `/admin/delete-application` | `POST` | `admin_delete_application` | applications | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/delete-mentor` | `POST` | `admin_delete_mentor` | mentors | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/devices` | `GET` | `admin_devices` | device_profiles | None | `JSON` | 401, 500 | None |  |
| `/admin/devices/bulk-delete` | `POST` | `admin_devices_bulk_delete` | device_profiles | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/enrollment/bulk-review` | `POST` | `admin_enrollment_bulk_review` | applications, enrollments | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/enrollment/edit` | `POST` | `admin_enrollment_edit` | applications, enrollments | None | `JSON` | 404, 401, 400, 500 | None | Allows admin to edit any field of an enrollment record (dates, batch, product, amount, payment status). |
| `/admin/enrollment/review` | `POST` | `admin_enrollment_review` | applications, enrollments | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/admin/enrollments` | `GET` | `admin_enrollments` | applications, course_day_quizzes, course_enrollments, device_profiles, enrollments, intern_accounts | None | `JSON` | 401, 500 | None |  |
| `/admin/enrollments/bulk-delete` | `POST` | `admin_enrollments_bulk_delete` | enrollments | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/intern/edit` | `POST` | `admin_intern_edit` | applications, attendance, device_profiles, enrollments, intern_accounts, interviews | None | `JSON` | 404, 401, 400, 500 | None | Allows admin to edit any field of an intern account, including direct password override. |
| `/admin/interview/<path:email>` | `GET` | `admin_interview_view` | None direct | None | `JSON` | 404, 401, 500 | None |  |
| `/admin/interview/bulk-reset` | `POST` | `admin_interview_bulk_reset` | intern_accounts | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/interview/reset` | `POST` | `admin_interview_reset` | None direct | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/admin/job-applications` | `GET` | `admin_job_applications` | applications, companies, intern_accounts, post_applications, posts | None | `HTML (Jinja)` | 200/OK | "/admin-login" | Admin-wide view of post_applications (job-board applications) across every |
| `/admin/ledger` | `GET` | `admin_ledger` | coin_ledger_mirror, intern_accounts, intern_certificates | None | `HTML (Jinja)` | 500 | "/admin-login" | All mirrored coin events + certificates (Track 1 Â§6). Read-only, filterable |
| `/admin/login` | `GET, POST` | `admin_login` | staff_accounts | None | `JSON` | 401, 400, 500 | "/admin" |  |
| `/admin/mentors` | `GET` | `admin_mentors` | mentors | None | `JSON` | 401, 500 | None |  |
| `/admin/mentors/bulk-delete` | `POST` | `admin_mentors_bulk_delete` | mentors | None | `JSON` | 401, 400, 500 | None |  |
| `/admin/post-hire-deposits` | `GET` | `admin_post_hire_deposits` | companies, enrollments, intern_accounts, payments, post_hire_deposits, posts | None | `HTML (Jinja)` | 200/OK | "/admin-login" | Track 5: admin view of â‚¹499 job-hire deposits -- verify payments and mark |
| `/admin/post-hire-deposits/<int:dep_id>/refund` | `POST` | `admin_post_hire_deposit_refund` | post_hire_deposits | None | `JSON` | 404, 401, 400 | None | Track 5: manual admin refund action, per your explicit call -- no auto-trigger. |
| `/admin/post-hire-deposits/<int:dep_id>/review` | `POST` | `admin_post_hire_deposit_review` | intern_accounts, post_hire_deposits, posts | None | `JSON` | 404, 401, 400 | None |  |
| `/admin/post-questions` | `GET` | `admin_post_questions` | companies, post_questions, posts | None | `JSON` | 401 | None | Default to pending (the moderation queue); ?status=approved|rejected to review history. |
| `/admin/post-questions/<int:question_id>/review` | `POST` | `admin_post_question_review` | post_questions | None | `JSON` | 404, 401, 400 | None |  |
| `/admin/push-test` | `POST` | `admin_push_test` | None direct | OneSignal Push | `JSON` | 401, 400, 500 | None | Admin-only self-test: send one push to an external_id and return OneSignal's raw |
| `/admin/reset-intern-password` | `POST` | `admin_reset_intern_password` | intern_accounts, password_resets | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/admin/screenshot/<filename>` | `GET` | `admin_screenshot` | None direct | None | `HTML (Jinja)` | 404, 401 | None |  |
| `/admin/stats` | `GET` | `admin_stats` | applications, attendance, device_profiles, enrollments, intern_accounts, mentors | None | `JSON` | 401, 500 | None |  |
| `/admin/update-application-status` | `POST` | `admin_update_application_status` | applications, intern_accounts | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/admin/update-enrollment-status` | `POST` | `admin_update_enrollment_status` | applications, enrollments | None | `JSON` | 404, 401, 400, 500 | None |  |
| `/admin/upload-csv` | `POST` | `admin_upload_csv` | None direct | File Storage | `JSON` | 401, 400, 500 | None |  |
| `/admin/upload-csv-accepted` | `POST` | `admin_upload_csv_accepted` | applications | File Storage | `JSON` | 401, 400, 500 | None | Bulk-accept interns already enrolled in real life, with one shared joining |
| `/admin/users` | `GET` | `admin_users` | applications, device_profiles, intern_accounts | None | `JSON` | 401, 500 | None |  |
| `/admin/users/bulk-delete` | `POST` | `admin_users_bulk_delete` | applications, attendance, coin_ledger_mirror, course_enrollments, course_payments, cvs, device_profiles, enrollments, intern_accounts, intern_certificates, interviews, mentor_session_bookings, mobile_refresh_tokens, notifications, password_resets, project_submissions, referrals, signup_otps, task_submissions, tutor_progress, user_sessions | None | `JSON` | 401, 400, 500 | None | Cascade delete by user accounts. Input = list of intern_accounts IDs. |
| `/staff/courses` | `GET` | `staff_courses_redirect` | courses | None | `Redirect` | 200/OK | "/staff/login", "/staff/projects" |  |
| `/staff/payments` | `GET` | `staff_payments_redirect` | payments | None | `Redirect` | 200/OK | "/staff/login", "/admin/course-payments" |  |
| `/staff/tasks/create` | `POST` | `staff_create_task` | task_versions, tasks | None | `JSON` | 401, 400 | None |  |

---

