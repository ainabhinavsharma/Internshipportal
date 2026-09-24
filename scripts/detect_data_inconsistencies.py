#!/usr/bin/env python3
"""
scripts/detect_data_inconsistencies.py - Data Inconsistency Detector & Reporter (MIG-004)
Fulfills MIG-004 requirements of DBERT_PORTAL_NEXT_PHASE_MASTER_PLAN.md

Detects logical anomalies and exports DATA_INCONSISTENCIES.csv without silent mutation:
- Foreign key reference breaks (orphans)
- Status contradictions (e.g. Application Rejected + Active Enrollment)
- Multiple conflicting active applications per email
- Orphaned enrollments / attendance without accounts
- Certificate issued without enrollment
"""
import os
import sys
import sqlite3
import csv
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "internship.db")
CSV_PATH = os.path.join(BASE_DIR, "DATA_INCONSISTENCIES.csv")

def detect_inconsistencies():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    inconsistencies = []

    print("[*] Running Data Inconsistency Audit across internship.db...")

    # 1. PRAGMA foreign_key_check
    fk_violations = cursor.execute("PRAGMA foreign_key_check").fetchall()
    for fk in fk_violations:
        inconsistencies.append({
            "severity": "P1",
            "entity": fk[0],
            "record_id": fk[1],
            "issue_type": "FOREIGN_KEY_VIOLATION",
            "details": f"Table '{fk[0]}' row {fk[1]} references missing key in parent table '{fk[2]}' (fkid={fk[3]})",
            "recommended_action": "Investigate parent record deletion or establish safe dummy placeholder"
        })

    # 2. Contradiction: Application Rejected, but Enrollment is Accepted
    cur_contra = cursor.execute("""
        SELECT a.id as app_id, a.email, a.status as app_status, e.id as enr_id, e.payment_status as enr_status
        FROM applications a
        JOIN enrollments e ON lower(a.email) = lower(e.email)
        WHERE a.status = 'Rejected' AND e.payment_status = 'Accepted'
    """).fetchall()
    for row in cur_contra:
        inconsistencies.append({
            "severity": "P0",
            "entity": "applications / enrollments",
            "record_id": f"app_{row['app_id']} / enr_{row['enr_id']}",
            "issue_type": "STATUS_CONTRADICTION",
            "details": f"Email '{row['email']}' has Rejected application (id {row['app_id']}) but Accepted enrollment (id {row['enr_id']})",
            "recommended_action": "Review with admissions: determine if student was granted manual override or enrolled via separate track"
        })

    # 3. Duplicate Active Applications for Same Email
    cur_dup = cursor.execute("""
        SELECT lower(email) as norm_email, count(*) as cnt, group_concat(id) as app_ids, group_concat(status) as statuses
        FROM applications
        WHERE status IN ('Selected', 'Accepted', 'Under Review')
        GROUP BY lower(email)
        HAVING count(*) > 1
    """).fetchall()
    for row in cur_dup:
        inconsistencies.append({
            "severity": "P2",
            "entity": "applications",
            "record_id": row["app_ids"],
            "issue_type": "DUPLICATE_ACTIVE_APPLICATIONS",
            "details": f"Email '{row['norm_email']}' has {row['cnt']} active applications: {row['statuses']}",
            "recommended_action": "Consolidate into latest application record; mark older ones as Superseded"
        })

    # 4. Attendance logged for intern with no accepted enrollment
    cur_att = cursor.execute("""
        SELECT a.intern_id, u.email, sum(a.total_minutes) as mins
        FROM attendance a
        LEFT JOIN intern_accounts u ON a.intern_id = u.id
        LEFT JOIN enrollments e ON lower(u.email) = lower(e.email) AND e.payment_status = 'Accepted'
        WHERE e.id IS NULL
        GROUP BY a.intern_id
    """).fetchall()
    for row in cur_att:
        inconsistencies.append({
            "severity": "P1",
            "entity": "attendance",
            "record_id": f"intern_{row['intern_id']}",
            "issue_type": "ATTENDANCE_WITHOUT_ENROLLMENT",
            "details": f"Intern ID {row['intern_id']} ({row['email']}) logged {row['mins']} attendance minutes without an Accepted enrollment record",
            "recommended_action": "Verify if user was enrolled via legacy import or offline batch"
        })

    # 5. Certificate issued to intern without accepted enrollment
    cur_cert = cursor.execute("""
        SELECT c.id as cert_table_id, c.cert_id, c.intern_id, u.email
        FROM intern_certificates c
        LEFT JOIN intern_accounts u ON c.intern_id = u.id
        LEFT JOIN enrollments e ON lower(u.email) = lower(e.email) AND e.payment_status = 'Accepted'
        WHERE e.id IS NULL
    """).fetchall()
    for row in cur_cert:
        inconsistencies.append({
            "severity": "P1",
            "entity": "intern_certificates",
            "record_id": row["cert_id"],
            "issue_type": "CERTIFICATE_WITHOUT_ENROLLMENT",
            "details": f"Certificate '{row['cert_id']}' issued to Intern ID {row['intern_id']} ({row['email']}) without matching Accepted enrollment",
            "recommended_action": "Preserve certificate row; audit completion evidence"
        })

    # 6. Orphaned security deposits
    cur_dep = cursor.execute("""
        SELECT d.id as dep_id, d.intern_id, d.amount
        FROM security_deposits d
        LEFT JOIN intern_accounts u ON d.intern_id = u.id
        WHERE u.id IS NULL
    """).fetchall()
    for row in cur_dep:
        inconsistencies.append({
            "severity": "P1",
            "entity": "security_deposits",
            "record_id": f"dep_{row['dep_id']}",
            "issue_type": "ORPHANED_DEPOSIT",
            "details": f"Security deposit {row['dep_id']} of amount {row['amount']} references non-existent intern_id {row['intern_id']}",
            "recommended_action": "Investigate financial transaction match before deletion"
        })

    conn.close()

    # Write CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["severity", "entity", "record_id", "issue_type", "details", "recommended_action"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for inc in inconsistencies:
            writer.writerow(inc)

    print(f"[+] Inconsistency audit complete! Total issues identified: {len(inconsistencies)}")
    severity_counts = {}
    for inc in inconsistencies:
        severity_counts[inc["severity"]] = severity_counts.get(inc["severity"], 0) + 1
    for s, c in sorted(severity_counts.items()):
        print(f"    Severity {s}: {c} records")
    print(f"[+] Output written to: {CSV_PATH}")

    return inconsistencies

if __name__ == "__main__":
    detect_inconsistencies()
