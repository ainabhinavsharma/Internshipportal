#!/usr/bin/env python3
"""
scripts/compensate_attendance.py - Bulk Attendance Compensation Utility

Safely credits attendance minutes to eligible interns (e.g. +30 productive minutes)
for the current active week to compensate for past tracking issues.

Features:
- Non-destructive by default (--dry-run)
- Pre-execution automated backup via scripts.backup_db
- Computes canonical Sun-Sat week bounds automatically
- Flexible scoping:
    --scope all-active       : All active intern accounts within valid internship window
    --scope course-enrolled  : Interns enrolled in at least one course
    --scope course-active    : Interns with quiz/chat/progress in courses
    --scope email <address>  : Specific intern for targeted compensation
- Atomic transaction with SQLite UPSERT (ON CONFLICT DO UPDATE)
"""

import os
import sys
import argparse
import sqlite3
from datetime import datetime, date, timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from scripts.backup_db import resolve_source_db, create_backup


def get_current_week_bounds(ref_date=None):
    """Return (week_start_str, week_end_str) for the Sun-Sat week containing ref_date."""
    if ref_date is None:
        ref_date = date.today()
    days_since_sunday = (ref_date.weekday() + 1) % 7
    week_start = ref_date - timedelta(days=days_since_sunday)
    week_end = week_start + timedelta(days=6)
    return week_start.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d")


def find_eligible_interns(conn, scope="all-active", target_email=None):
    """
    Query eligible interns based on the specified scope.
    Returns list of dicts: [{'id': ..., 'name': ..., 'email': ...}, ...]
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if target_email:
        query = """
            SELECT ia.id, ia.name, ia.email, e.joining_date
            FROM intern_accounts ia
            LEFT JOIN enrollments e ON LOWER(e.email) = LOWER(ia.email)
            WHERE LOWER(ia.email) = LOWER(?) AND ia.is_active = 1
            LIMIT 1
        """
        rows = cursor.execute(query, (target_email.strip(),)).fetchall()
        return [dict(r) for r in rows]

    if scope == "course-enrolled":
        query = """
            SELECT ia.id, ia.name, ia.email, e.joining_date
            FROM intern_accounts ia
            JOIN course_enrollments ce ON ce.intern_id = ia.id
            LEFT JOIN enrollments e ON LOWER(e.email) = LOWER(ia.email)
            WHERE ia.is_active = 1
              AND (e.joining_date IS NULL OR date(e.joining_date, '+60 days') >= date('now','localtime'))
            GROUP BY ia.id
            ORDER BY ia.name ASC
        """
        rows = cursor.execute(query).fetchall()
        return [dict(r) for r in rows]

    elif scope == "course-active":
        query = """
            SELECT ia.id, ia.name, ia.email, e.joining_date
            FROM intern_accounts ia
            LEFT JOIN enrollments e ON LOWER(e.email) = LOWER(ia.email)
            WHERE ia.is_active = 1
              AND (e.joining_date IS NULL OR date(e.joining_date, '+60 days') >= date('now','localtime'))
              AND (
                  EXISTS (SELECT 1 FROM course_subtopic_chats csc WHERE csc.intern_id = ia.id)
                  OR EXISTS (SELECT 1 FROM course_enrollments ce WHERE ce.intern_id = ia.id AND ce.last_accessed_at IS NOT NULL)
                  OR EXISTS (
                      SELECT 1 FROM course_enrollments ce 
                      JOIN day_quiz_attempts dqa ON dqa.enrollment_id = ce.id 
                      WHERE ce.intern_id = ia.id
                  )
              )
            GROUP BY ia.id
            ORDER BY ia.name ASC
        """
        rows = cursor.execute(query).fetchall()
        return [dict(r) for r in rows]

    else:  # all-active
        query = """
            SELECT ia.id, ia.name, ia.email, e.joining_date
            FROM intern_accounts ia
            LEFT JOIN enrollments e ON LOWER(e.email) = LOWER(ia.email)
            WHERE ia.is_active = 1
              AND (e.joining_date IS NULL OR date(e.joining_date, '+60 days') >= date('now','localtime'))
            GROUP BY ia.id
            ORDER BY ia.name ASC
        """
        rows = cursor.execute(query).fetchall()
        return [dict(r) for r in rows]


def apply_compensation(db_path, interns, week_start, week_end, minutes=30, dry_run=True):
    """
    Applies the compensation to the database.
    """
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    existing_recs = {}
    placeholders = ",".join("?" for _ in interns) if interns else ""
    if interns:
        intern_ids = [i["id"] for i in interns]
        # Query existing attendance rows for this week in batches
        batch_size = 500
        for i in range(0, len(intern_ids), batch_size):
            batch = intern_ids[i:i + batch_size]
            qmarks = ",".join("?" for _ in batch)
            q = f"SELECT intern_id, total_minutes FROM attendance WHERE week_start = ? AND intern_id IN ({qmarks})"
            for r in cursor.execute(q, [week_start] + batch).fetchall():
                existing_recs[r["intern_id"]] = r["total_minutes"]

    inserts = 0
    updates = 0
    preview = []

    for intern in interns:
        iid = intern["id"]
        old_mins = existing_recs.get(iid, 0)
        new_mins = old_mins + minutes
        if iid in existing_recs:
            updates += 1
        else:
            inserts += 1

        if len(preview) < 10:
            preview.append({
                "id": iid,
                "name": intern["name"],
                "email": intern["email"],
                "old_minutes": old_mins,
                "new_minutes": new_mins
            })

    if not dry_run and interns:
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        upsert_sql = """
            INSERT INTO attendance (intern_id, email, week_start, week_end, total_minutes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(intern_id, week_start) DO UPDATE SET
                total_minutes = attendance.total_minutes + excluded.total_minutes,
                updated_at = excluded.updated_at,
                email = COALESCE(attendance.email, excluded.email)
        """
        try:
            with conn:
                for intern in interns:
                    conn.execute(
                        upsert_sql,
                        (intern["id"], intern["email"], week_start, week_end, minutes, now_ts)
                    )
        except Exception as e:
            conn.close()
            raise RuntimeError(f"Database update failed: {e}")

    conn.close()
    return {
        "total_eligible": len(interns),
        "new_records": inserts,
        "existing_updated": updates,
        "minutes_added": minutes,
        "week_start": week_start,
        "week_end": week_end,
        "preview": preview,
        "dry_run": dry_run
    }


def main():
    parser = argparse.ArgumentParser(
        description="Safely compensate attendance minutes for eligible interns."
    )
    parser.add_argument(
        "--minutes", type=int, default=30,
        help="Number of productive minutes to credit (default: 30)"
    )
    parser.add_argument(
        "--scope",
        choices=["all-active", "course-enrolled", "course-active"],
        default="all-active",
        help="Target intern selection scope (default: all-active)"
    )
    parser.add_argument(
        "--email", type=str, default=None,
        help="Target a single specific intern email (for testing or individual credit)"
    )
    parser.add_argument(
        "--week-start", type=str, default=None,
        help="Target week start YYYY-MM-DD (defaults to current week Sun)"
    )
    parser.add_argument(
        "--apply", action="store_true", default=False,
        help="Commit changes to database. If omitted, operates in dry-run mode."
    )
    parser.add_argument(
        "--no-backup", action="store_true", default=False,
        help="Skip automatic database backup before applying."
    )

    args = parser.parse_args()

    db_path = resolve_source_db()
    if not os.path.exists(db_path):
        print(f"[ERROR] Database not found at: {db_path}", file=sys.stderr)
        sys.exit(1)

    if args.week_start:
        w_start = args.week_start
        try:
            ws_dt = datetime.strptime(w_start, "%Y-%m-%d").date()
            w_end = (ws_dt + timedelta(days=6)).strftime("%Y-%m-%d")
        except ValueError:
            print("[ERROR] --week-start must be formatted as YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    else:
        w_start, w_end = get_current_week_bounds()

    print("=" * 65)
    print("DBERT ATTENDANCE COMPENSATION UTILITY")
    print("=" * 65)
    print(f"Target Database : {db_path}")
    print(f"Target Week     : {w_start} to {w_end}")
    print(f"Compensation    : +{args.minutes} minutes")
    print(f"Scope Filter    : {f'Single user ({args.email})' if args.email else args.scope}")
    print(f"Mode            : {'*** LIVE APPLY ***' if args.apply else '[DRY-RUN - NO CHANGES]'}")
    print("-" * 65)

    conn = sqlite3.connect(db_path, timeout=15)
    interns = find_eligible_interns(conn, scope=args.scope, target_email=args.email)
    conn.close()

    if not interns:
        print("[INFO] No eligible interns matched the criteria.")
        return

    print(f"[1] Identified {len(interns):,} eligible intern accounts.")

    # Create backup before live apply
    if args.apply and not args.no_backup:
        print("[2] Creating automated pre-change database backup...")
        backup_file = create_backup(reason=f"pre_attendance_compensation_{args.minutes}m")
        print(f"    [OK] Backup secured: {backup_file}")
    else:
        print("[2] Backup step: Skipped (dry-run mode).")

    # Run compensation
    print(f"[3] {'Simulating' if not args.apply else 'Executing'} compensation (+{args.minutes} min)...")
    res = apply_compensation(
        db_path=db_path,
        interns=interns,
        week_start=w_start,
        week_end=w_end,
        minutes=args.minutes,
        dry_run=not args.apply
    )

    print("-" * 65)
    print("SUMMARY OF RESULTS:")
    print(f"  - Total Eligible Interns:   {res['total_eligible']:,}")
    print(f"  - Existing Records Updated: {res['existing_updated']:,} (+{args.minutes}m to their current total)")
    print(f"  - New Records Inserted:     {res['new_records']:,} (initialized to {args.minutes}m)")
    print("-" * 65)
    print("Sample Preview (First 10 records):")
    for item in res["preview"]:
        print(f"  * #{item['id']} {item['name']} ({item['email']}): {item['old_minutes']}m -> {item['new_minutes']}m")

    if not args.apply:
        print("\n" + "=" * 65)
        print("NOTE: This was a DRY-RUN. No changes were committed.")
        print("To execute this compensation on the live database, run:")
        apply_cmd = f"python scripts/compensate_attendance.py --scope {args.scope} --minutes {args.minutes} --apply"
        if args.email:
            apply_cmd = f"python scripts/compensate_attendance.py --email {args.email} --minutes {args.minutes} --apply"
        print(f"  {apply_cmd}")
        print("=" * 65)
    else:
        print("\n" + "=" * 65)
        print(f"[SUCCESS] Successfully credited +{args.minutes} minutes to {len(interns):,} interns!")
        print("Changes are committed and immediately visible on intern dashboards.")
        print("=" * 65)


if __name__ == "__main__":
    main()
