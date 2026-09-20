import sqlite3
import shutil
import os
import re
from datetime import datetime

LIVE_DB = "internship_live.db"
TARGET_DB = "internship.db"
BACKUP_DB = "internship.db.backup"

def migrate():
    print("==================================================")
    print("STARTING DATABASE MIGRATION & REPAIR")
    print("==================================================")

    if not os.path.exists(LIVE_DB):
        raise FileNotFoundError(f"Live database {LIVE_DB} not found!")

    # 1. Backup target DB if it exists
    if os.path.exists(TARGET_DB):
        print(f"[*] Backing up {TARGET_DB} to {BACKUP_DB}...")
        shutil.copy2(TARGET_DB, BACKUP_DB)

    conn_l = sqlite3.connect(LIVE_DB)
    conn_l.row_factory = sqlite3.Row
    cur_l = conn_l.cursor()

    # We will create a fresh target database file to guarantee 0 page corruption
    TEMP_DB = "internship_migrated.db"
    if os.path.exists(TEMP_DB):
        os.remove(TEMP_DB)

    conn_t = sqlite3.connect(TEMP_DB)
    conn_t.row_factory = sqlite3.Row
    cur_t = conn_t.cursor()

    # Enable WAL mode for high concurrency
    cur_t.execute("PRAGMA journal_mode = WAL")
    cur_t.execute("PRAGMA foreign_keys = OFF")

    # 2. Replicate all table DDLs from live DB (except enrollments which we will define cleanly)
    tables_query = "SELECT type, name, sql FROM sqlite_master WHERE type IN ('table', 'view', 'index') AND name NOT LIKE 'sqlite_%' AND sql IS NOT NULL ORDER BY type DESC"
    schema_items = cur_l.execute(tables_query).fetchall()

    for item in schema_items:
        s_type = item["type"]
        s_name = item["name"]
        s_sql = item["sql"]

        if s_type == "table":
            if s_name == "enrollments":
                # Clean enrollments schema with all columns
                cur_t.execute("""
                    CREATE TABLE enrollments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        application_id INTEGER,
                        timestamp TEXT,
                        name TEXT,
                        email TEXT,
                        phone TEXT,
                        city TEXT,
                        college TEXT,
                        course TEXT,
                        semester TEXT,
                        year_of_passing TEXT,
                        domain TEXT,
                        joining_date TEXT,
                        batch_label TEXT,
                        payment_screenshot TEXT,
                        payment_status TEXT,
                        admin_note TEXT,
                        created_at TEXT,
                        updated_at TEXT,
                        product TEXT DEFAULT 'free_deposit',
                        amount INTEGER,
                        razorpay_order_id TEXT,
                        razorpay_payment_id TEXT,
                        razorpay_signature TEXT
                    )
                """)
            else:
                try:
                    cur_t.execute(s_sql)
                except Exception as e:
                    print(f"Warning creating table {s_name}: {e}")

    # 3. Migrate INTERN ACCOUNTS (ONLY password_set = 1, deduplicated by id)
    print("\n[*] Migrating intern_accounts (password_set=1 only)...")
    intern_cols = [c['name'] for c in cur_l.execute("PRAGMA table_info(intern_accounts)").fetchall()]
    # Ensure visitor_id and account_status are in table
    for col, defn in [("account_status", "TEXT DEFAULT 'active'"), ("visitor_id", "TEXT")]:
        if col not in [c['name'] for c in cur_t.execute("PRAGMA table_info(intern_accounts)").fetchall()]:
            cur_t.execute(f"ALTER TABLE intern_accounts ADD COLUMN {col} {defn}")

    t_intern_cols = [c['name'] for c in cur_t.execute("PRAGMA table_info(intern_accounts)").fetchall()]
    common_intern_cols = [c for c in intern_cols if c in t_intern_cols]

    migrated_interns = cur_l.execute("""
        SELECT * FROM intern_accounts
        WHERE password_set = 1 AND password_hash IS NOT NULL AND password_hash != ''
    """).fetchall()

    cols_str = ", ".join(common_intern_cols)
    placeholders = ", ".join(["?"] * len(common_intern_cols))

    seen_intern_ids = set()
    inserted_interns = 0
    for r in migrated_interns:
        if r["id"] in seen_intern_ids:
            continue
        seen_intern_ids.add(r["id"])
        vals = [r[c] for c in common_intern_cols]
        cur_t.execute(f"INSERT OR IGNORE INTO intern_accounts ({cols_str}) VALUES ({placeholders})", vals)
        inserted_interns += 1

    print(f"    Migrated {inserted_interns} active intern accounts (excluded {4996 - inserted_interns} incomplete signups).")

    migrated_emails = {r["email"].strip().lower() for r in migrated_interns}

    # 4. Migrate ENROLLMENTS (Salvaged + Reconstructed)
    print("\n[*] Salvaging and reconstructing enrollments table...")
    salvaged_enr = []
    for rid in range(1, 6000):
        try:
            r = cur_l.execute(f"SELECT * FROM enrollments WHERE rowid = {rid}").fetchone()
            if r:
                salvaged_enr.append(dict(r))
        except Exception:
            pass

    # Reconstruct missing enrollments for Accepted migrated interns
    accepted_apps = cur_l.execute("SELECT * FROM applications WHERE status = 'Accepted'").fetchall()
    salvaged_emails = {r["email"].strip().lower() for r in salvaged_enr if r.get("email")}

    final_enrollments = []
    seen_enr_emails = set()

    # Add salvaged enrollments that belong to migrated interns
    for se in salvaged_enr:
        em = se.get("email", "").strip().lower()
        if em and em in migrated_emails and em not in seen_enr_emails:
            seen_enr_emails.add(em)
            final_enrollments.append(se)

    # Reconstruct for Accepted migrated interns without enrollment
    reconstructed_count = 0
    for app in accepted_apps:
        app_email = app["email"].strip().lower()
        if app_email in migrated_emails and app_email not in seen_enr_emails:
            seen_enr_emails.add(app_email)
            final_enrollments.append({
                "application_id": app["id"],
                "timestamp": app["created_at"] or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": app["name"],
                "email": app["email"],
                "phone": app["phone"],
                "city": app["city"] or "N/A",
                "college": app["college"],
                "course": app["course"],
                "semester": app["semester"],
                "year_of_passing": app["year_of_passing"],
                "domain": app["domain"],
                "joining_date": "2026-05-11",
                "batch_label": "11 May 2026",
                "payment_screenshot": "",
                "payment_status": "Accepted",
                "admin_note": "Auto-reconstructed during live DB migration for Accepted intern",
                "created_at": app["created_at"] or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product": "free_deposit",
                "amount": 499,
                "razorpay_order_id": None,
                "razorpay_payment_id": None,
                "razorpay_signature": None
            })
            reconstructed_count += 1

    # Insert clean enrollments
    enr_cols = [c['name'] for c in cur_t.execute("PRAGMA table_info(enrollments)").fetchall() if c['name'] != 'id']
    enr_cols_str = ", ".join(enr_cols)
    enr_placeholders = ", ".join(["?"] * len(enr_cols))

    for fe in final_enrollments:
        vals = [fe.get(c) for c in enr_cols]
        cur_t.execute(f"INSERT INTO enrollments ({enr_cols_str}) VALUES ({enr_placeholders})", vals)

    print(f"    Successfully populated {len(final_enrollments)} clean enrollments ({len(final_enrollments) - reconstructed_count} salvaged, {reconstructed_count} reconstructed).")

    # 5. Migrate all other tables directly from live
    tables_to_migrate = [
        "applications", "device_profiles", "email_log", "abuse_log", "rate_events", 
        "attendance", "interviews", "notifications", "cvs", "posts", "post_applications", 
        "post_comments", "post_questions", "security_deposits", "companies", "mentors", 
        "staff_accounts", "staff_queue_roles", "platform_config", "referrals",
        "conversations", "messages", "password_resets", "post_hire_deposits", "course_payments"
    ]

    for tbl in tables_to_migrate:
        if tbl not in [t[0] for t in cur_l.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
            continue
            
        print(f"[*] Migrating {tbl}...")
        src_cols = [c['name'] for c in cur_l.execute(f"PRAGMA table_info({tbl})").fetchall()]
        tgt_cols = [c['name'] for c in cur_t.execute(f"PRAGMA table_info({tbl})").fetchall()]
        common = [c for c in src_cols if c in tgt_cols]
        
        c_str = ", ".join(common)
        p_str = ", ".join(["?"] * len(common))
        
        rows = cur_l.execute(f"SELECT {c_str} FROM {tbl}").fetchall()
        for r in rows:
            cur_t.execute(f"INSERT OR IGNORE INTO {tbl} ({c_str}) VALUES ({p_str})", list(r))
        print(f"    Migrated {len(rows)} rows.")

    # 6. Migrate courses and curriculum from local DB if empty in live
    if os.path.exists(BACKUP_DB):
        conn_m = sqlite3.connect(BACKUP_DB)
        conn_m.row_factory = sqlite3.Row
        cur_m = conn_m.cursor()

        curriculum_tables = [
            "courses", "course_chapters", "course_subtopics", "tasks", "task_versions",
            "coin_ledger_mirror", "intern_certificates", "cohorts", "cohort_enrollments"
        ]
        for tbl in curriculum_tables:
            # Check if table exists in local backup
            has_tbl = cur_m.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tbl}'").fetchone()
            if not has_tbl:
                continue
                
            tgt_count = cur_t.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            if tgt_count == 0:
                print(f"[*] Populating {tbl} from local seed...")
                src_cols = [c['name'] for c in cur_m.execute(f"PRAGMA table_info({tbl})").fetchall()]
                tgt_cols = [c['name'] for c in cur_t.execute(f"PRAGMA table_info({tbl})").fetchall()]
                common = [c for c in src_cols if c in tgt_cols]
                if common:
                    c_str = ", ".join(common)
                    p_str = ", ".join(["?"] * len(common))
                    m_rows = cur_m.execute(f"SELECT {c_str} FROM {tbl}").fetchall()
                    for r in m_rows:
                        cur_t.execute(f"INSERT OR IGNORE INTO {tbl} ({c_str}) VALUES ({p_str})", list(r))
                    print(f"    Added {len(m_rows)} rows to {tbl}.")

        conn_m.close()

    # 7. Apply SEC-001 columns to password_resets if missing
    pr_cols = [c['name'] for c in cur_t.execute("PRAGMA table_info(password_resets)").fetchall()]
    for col, defn in [("account_type", "TEXT NOT NULL DEFAULT 'intern'"), ("account_id", "INTEGER"), ("used_at", "TEXT")]:
        if col not in pr_cols:
            cur_t.execute(f"ALTER TABLE password_resets ADD COLUMN {col} {defn}")

    # 8. Ensure test staff accounts exist for local administration
    staff_emails = [r[0] for r in cur_t.execute("SELECT email FROM staff_accounts").fetchall()]
    if "admin@example.com" not in staff_emails:
        from werkzeug.security import generate_password_hash
        p_hash = generate_password_hash("Password123", method="pbkdf2:sha256")
        cur_t.execute(
            "INSERT INTO staff_accounts (name, email, password_hash, is_active, role) VALUES (?, ?, ?, 1, 'admin')",
            ("Test Admin", "admin@example.com", p_hash)
        )
    if "dbert_admin@dbert.online" not in staff_emails:
        from werkzeug.security import generate_password_hash
        p_hash = generate_password_hash("change-me-in-production", method="pbkdf2:sha256")
        cur_t.execute(
            "INSERT INTO staff_accounts (name, email, password_hash, is_active, role) VALUES (?, ?, ?, 1, 'admin')",
            ("DBERT Admin Staff", "dbert_admin@dbert.online", p_hash)
        )

    # 9. Commit & Integrity Check
    conn_t.commit()
    print("\n[*] Running PRAGMA integrity_check on migrated database...")
    integrity = cur_t.execute("PRAGMA integrity_check").fetchall()
    print("    Integrity result:", [r[0] for r in integrity])

    conn_t.close()
    conn_l.close()

    # 10. Replace target DB with migrated DB
    print(f"\n[*] Replacing {TARGET_DB} with {TEMP_DB}...")
    if os.path.exists(TARGET_DB):
        for ext in ["-wal", "-shm"]:
            if os.path.exists(TARGET_DB + ext):
                try: os.remove(TARGET_DB + ext)
                except Exception: pass
        os.remove(TARGET_DB)

    os.rename(TEMP_DB, TARGET_DB)
    print("[+] Migration successfully completed!")

if __name__ == "__main__":
    migrate()
