# DBERT Internship Portal — Staging Environment Guide (SAFE-003)

**Document Date:** 2026-09-23  
**Target Host:** `staging-internship.dbert.online`  
**Purpose:** Pre-production validation, schema migration dry runs, and regression testing under identical infrastructure conditions without risking production data or real users.

---

## 1. Non-Negotiable Staging Isolation Rules

In compliance with Section 1 and Section 9 (SAFE-003) of `DBERT_PORTAL_NEXT_PHASE_MASTER_PLAN.md`:

```text
       PRODUCTION                                 STAGING
  internship.dbert.online              staging-internship.dbert.online
            │                                         │
     internship.db                             internship_staging.db
            │                                         │
        uploads/                                uploads_staging/
            │                                         │
  Live Email / Real Users                    EMAILS_ENABLED=false (Mock)
            │                                         │
  Real Payments (₹499/₹1599)                 Test UPI / Mock Verification
```

1. **Zero Production Credential Sharing**: Staging must never use `FLASK_SECRET_KEY`, `ADMIN_PASSWORD`, or encryption keys from production.
2. **Database Isolation**: Staging operates exclusively on `internship_staging.db`. Never attach or mount production database files to staging.
3. **Email Suppression**: `EMAILS_ENABLED=false` must be set in staging. Staging must never dispatch real emails to student inboxes.
4. **Isolated Storage**: Uploaded files and payment receipts reside in `uploads_staging/`.
5. **Turnstile Testing Mode**: Cloudflare Turnstile is either disabled (`TURNSTILE_ENABLED=false`) or uses Cloudflare's always-pass dummy test keys (`1x00000000000000000000AA` / `2x00000000000000000000AB`).

---

## 2. Staging Database Seeding (Sanitized Mirror)

To test migrations or realistic query performance on staging:

1. **Generate Verified Production Backup**:
   ```powershell
   python scripts/backup_db.py --reason staging-seed
   ```
2. **Sanitize Data (Scrub PII)**:
   Never copy un-sanitized user passwords or contact details to unhardened environments. A sanitized seed replaces:
   - User emails with `user_<id>@staging.dbert.local`
   - User phone numbers with `+919000000000`
   - Passwords with standard test hash
   - UPI IDs with `staging@upi`
3. **Mount as `internship_staging.db`**:
   Deploy the sanitized database to the staging environment root.

---

## 3. Deployment Checklist for Staging

Before promoting any release branch (`release/*` or `main`) to staging:
- [ ] Pull latest branch
- [ ] Verify `.env` points to `internship_staging.db` and has `EMAILS_ENABLED=false`
- [ ] Run automated migrations in dry-run mode
- [ ] Run test suite (`pytest`)
- [ ] Execute smoke test across login, course view, and application submission
- [ ] Verify no real emails were dispatched
