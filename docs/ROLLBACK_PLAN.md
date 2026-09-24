# DBERT Internship Portal — Comprehensive Rollback Plan (SAFE-004)

**Document Date:** 2026-09-23  
**Status:** Mandatory Production Operational Standard  
**Applicability:** All production deployments, database migrations, configuration updates, and service failures.

---

## 1. Rollback Decision Triggers (P0 Blockers)

An immediate rollback is mandatory if any of the following occur within the 24-hour post-deployment stability window:

1. **Database corruption** or unrecoverable constraint failure.
2. **Authentication or Authorization bypass** (e.g. IDOR, admin portal exposed).
3. **Data Loss / Unintended Mutation** of active user accounts, enrollments, or payments.
4. **Golden Applicant Journey failure** (candidates unable to sign up, apply, or log in).
5. **Elevated 5xx error rate** (> 1% of total requests over 5 minutes).
6. **Payment state inconsistency** (users charged or approved without enrollment activation).

---

## 2. The 6 Rollback Vectors

### Vector 1: Application Code Rollback
Used when a bug in `app.py`, routes, or templates causes runtime crashes or logic errors.

```bash
# 1. Identify previous stable commit or tag
PREV_COMMIT=$(git tag -l "prod-*" --sort=-creatordate | head -n 1)

# 2. Checkout previous stable release
git checkout $PREV_COMMIT

# 3. Restart production gunicorn service
sudo systemctl restart internship.service

# 4. Verify service health
curl -f http://127.0.0.1:5000/health
```

---

### Vector 2: Database Rollback
Used when a database state anomaly, corruption, or destructive data mutation occurs.

```bash
# 1. Stop application traffic immediately to prevent writes
sudo systemctl stop internship.service

# 2. Locate the pre-release verified backup in backups/
BACKUP_FILE=$(python -c "import json; m=json.load(open('backups/backup_manifest.json')); print([b['path'] for b in m if b['status']=='VERIFIED_OK'][-1])")

# 3. Quarantine corrupted database for forensic analysis
mv internship.db "internship.db.quarantine.$(date +%s)"

# 4. Copy verified backup to active database location
cp "$BACKUP_FILE" internship.db

# 5. Verify integrity of the restored database
python -c "import sqlite3; conn = sqlite3.connect('internship.db'); assert conn.execute('PRAGMA integrity_check').fetchall() == [('ok',)]"

# 6. Restart application
sudo systemctl start internship.service
```

---

### Vector 3: Migration Rollback
Used when a schema change fails halfway or causes application incompatibility.

- **Golden Principle**: Every migration script must be paired with an automated inverse script (e.g. `migrate_00X_up.py` and `migrate_00X_down.py`).
- **If Down Migration Exists**:
  ```bash
  python migrations/migrate_XXX_down.py
  ```
- **If Down Migration Is Unsafe**:
  Execute Vector 2 (Database Rollback) using the pre-migration snapshot taken via `python scripts/backup_db.py --reason pre-migration`.

---

### Vector 4: Configuration Rollback
Used when an invalid environment variable in `.env` causes startup crashes or misconfigured service credentials.

```bash
# 1. Restore previous .env backup
cp .env.bak .env

# 2. Gracefully reload gunicorn workers (zero connection drop)
sudo systemctl reload internship.service
```

---

### Vector 5: Static Asset Rollback
Used when CSS/JS changes break rendering or cause client-side script errors.

```bash
# 1. Revert static directory
git checkout HEAD~1 -- static/

# 2. Invalidate Nginx reverse proxy asset cache
sudo systemctl restart nginx
```

---

### Vector 6: External Service Emergency Kill-Switches
Used when a third-party vendor (AI API, SMTP server, Turnstile, OneSignal) is degraded or throwing errors.

- **Email Outage**: Set `EMAILS_ENABLED=false` in `.env` and `sudo systemctl reload internship.service`. Emails are logged as `SKIPPED` without crashing user requests.
- **Turnstile Outage**: Set `TURNSTILE_ENABLED=false` in `.env`.
- **Ambassador / UPI Payout Outage**: Set `AMBASSADOR_ENABLED=0` in `.env`.

---

## 3. Post-Rollback Stability & Post-Mortem

Following any rollback:
1. Announce recovery to team and users.
2. Maintain all quarantine logs and database snapshots for root-cause analysis.
3. Record incident in `docs/INCIDENT_RUNBOOK.md` and `.agent/DECISIONS.md`.
4. Prohibit re-deployment until regression tests reproducing the failure are added and passing in CI.
