#!/usr/bin/env python3
"""
scripts/classify_user_lifecycle.py - User Lifecycle Classifier (MIG-001)
Fulfills MIG-001 requirements of DBERT_PORTAL_NEXT_PHASE_MASTER_PLAN.md

Classifies all active users in intern_accounts into actual operational categories:
A — Registered but not applied
B — Application pending / Incomplete onboarding
C — Under review
D — Selected
E — Enrollment pending
F — Payment pending / Under review
G — Enrolled (Confirmed seat)
H — Active internship (Attendance recorded / started)
I — Completed
J — Certificate issued
K — Rejected
L — Inactive / Abandoned
"""
import os
import sys
import sqlite3
import json
from collections import defaultdict
from datetime import datetime, date

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "internship.db")

def classify_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    users = cursor.execute("SELECT * FROM intern_accounts ORDER BY id ASC").fetchall()
    
    # Pre-fetch lookup maps
    apps_by_email = defaultdict(list)
    for app in cursor.execute("SELECT * FROM applications ORDER BY id DESC").fetchall():
        if app["email"]:
            apps_by_email[app["email"].strip().lower()].append(app)

    enr_by_email = defaultdict(list)
    for enr in cursor.execute("SELECT * FROM enrollments ORDER BY id DESC").fetchall():
        if enr["email"]:
            enr_by_email[enr["email"].strip().lower()].append(enr)

    certs_by_intern = defaultdict(list)
    for cert in cursor.execute("SELECT * FROM intern_certificates").fetchall():
        certs_by_intern[cert["intern_id"]].append(cert)

    attendance_by_intern = defaultdict(int)
    for att in cursor.execute("SELECT intern_id, sum(total_minutes) as mins FROM attendance GROUP BY intern_id").fetchall():
        attendance_by_intern[att["intern_id"]] = att["mins"] or 0

    classification_counts = defaultdict(int)
    detailed_records = []

    today = date.today().isoformat()

    for u in users:
        uid = u["id"]
        email = (u["email"] or "").strip().lower()
        user_apps = apps_by_email.get(email, [])
        user_enrs = enr_by_email.get(email, [])
        user_certs = certs_by_intern.get(uid, [])
        user_mins = attendance_by_intern.get(uid, 0)
        
        latest_app = user_apps[0] if user_apps else None
        latest_enr = user_enrs[0] if user_enrs else None

        app_status = latest_app["status"] if latest_app else None
        enr_pay_status = latest_enr["payment_status"] if latest_enr else None
        
        # Classification precedence:
        # 1. Certificate Issued (J)
        if user_certs:
            category = "J — Certificate issued"
            reason = f"Has {len(user_certs)} certificate(s) issued."
        # 2. Active Internship (H)
        elif latest_enr and enr_pay_status == "Accepted" and (user_mins > 0 or (latest_enr["joining_date"] and latest_enr["joining_date"] <= today)):
            category = "H — Active internship"
            reason = f"Enrolled (Accepted) with {user_mins} attendance minutes recorded."
        # 3. Enrolled Confirmed (G)
        elif latest_enr and enr_pay_status == "Accepted":
            category = "G — Enrolled"
            reason = f"Payment accepted, joining date {latest_enr['joining_date']} upcoming."
        # 4. Payment Pending / Under review (F)
        elif latest_enr and enr_pay_status in ("Pending", "Submitted", "Rejected") or (latest_enr and not enr_pay_status):
            category = "F — Payment pending / under review"
            reason = f"Enrollment recorded with payment_status='{enr_pay_status}'."
        # 5. Enrollment Pending (E)
        elif app_status == "Enrollment Pending" or (app_status == "Selected" and not latest_enr):
            category = "E — Enrollment pending"
            reason = f"Application status is '{app_status}', no enrollment record yet."
        # 6. Selected (D)
        elif app_status == "Selected":
            category = "D — Selected"
            reason = f"Application status is Selected."
        # 7. Under Review (C)
        elif app_status == "Under Review":
            category = "C — Under review"
            reason = "Application is currently under admin review."
        # 8. On Hold (C2)
        elif app_status == "On Hold":
            category = "C — Under review (On Hold)"
            reason = "Application is temporarily on hold."
        # 9. Rejected (K)
        elif app_status == "Rejected":
            category = "K — Rejected"
            reason = "Application rejected."
        # 10. Application Pending / Incomplete signup (B)
        elif u["signup_stage"] and u["signup_stage"] < 3:
            category = "B — Application pending (Incomplete signup)"
            reason = f"Account signup_stage is {u['signup_stage']} of 3."
        # 11. Registered but not applied (A)
        elif not latest_app:
            if u["created_at"] and (datetime.now() - datetime.fromisoformat(u["created_at"].split(".")[0])).days > 60:
                category = "L — Inactive / Abandoned"
                reason = "Registered over 60 days ago with no application."
            else:
                category = "A — Registered but not applied"
                reason = "Account created, no application submitted."
        else:
            category = "L — Inactive / Abandoned"
            reason = "Default fallback."

        classification_counts[category] += 1
        detailed_records.append({
            "intern_id": uid,
            "name": u["name"],
            "email": u["email"],
            "category": category,
            "app_id": latest_app["id"] if latest_app else None,
            "app_status": app_status,
            "enr_id": latest_enr["id"] if latest_enr else None,
            "enr_payment_status": enr_pay_status,
            "attendance_mins": user_mins,
            "cert_count": len(user_certs),
            "reason": reason
        })

    conn.close()

    # Generate Markdown Report
    report_path = os.path.join(BASE_DIR, "docs", "USER_LIFECYCLE_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# DBERT Internship Portal — User Lifecycle Classification Report (MIG-001)\n\n")
        f.write(f"**Generated Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Total Active User Accounts:** {len(users):,}  \n")
        f.write(f"**Database:** `internship.db`\n\n")
        
        f.write("## 1. Lifecycle Distribution Summary\n\n")
        f.write("| Lifecycle Stage | User Count | Percentage | Operational Meaning |\n")
        f.write("|---|---|---|---|\n")
        for cat in sorted(classification_counts.keys()):
            cnt = classification_counts[cat]
            pct = (cnt / len(users)) * 100
            f.write(f"| **{cat}** | {cnt:,} | {pct:.1f}% | Account state mapped by DB evidence |\n")
            
        f.write("\n---\n\n")
        f.write("## 2. Category Definitions & Actual Database States\n\n")
        f.write("1. **A — Registered but not applied**: Intern accounts with no record in `applications` created recently.\n")
        f.write("2. **B — Application pending**: Interns who stopped at signup step 1 or 2 (`signup_stage < 3`).\n")
        f.write("3. **C — Under review**: Candidates whose application status is `'Under Review'` or `'On Hold'`.\n")
        f.write("4. **D — Selected**: Candidates marked `'Selected'` who have not yet submitted deposit/enrollment.\n")
        f.write("5. **E — Enrollment pending**: Candidates marked `'Enrollment Pending'`.\n")
        f.write("6. **F — Payment pending**: Enrolled candidates whose deposit is `'Pending'` or `'Rejected'`.\n")
        f.write("7. **G — Enrolled**: Payment is `'Accepted'`, orientation/joining date is in the future.\n")
        f.write("8. **H — Active internship**: Payment is `'Accepted'` and attendance minutes are actively accumulating.\n")
        f.write("9. **J — Certificate issued**: Intern has satisfied requirements and `intern_certificates` entry exists.\n")
        f.write("10. **K — Rejected**: Application explicitly rejected.\n")
        f.write("11. **L — Inactive / Abandoned**: Old registered accounts with zero activity or applications.\n")

    print(f"[+] Classification complete! Total users analyzed: {len(users):,}")
    for cat, cnt in sorted(classification_counts.items()):
        print(f"    {cat:<35}: {cnt:>5} ({(cnt/len(users))*100:.1f}%)")
    print(f"[+] Report written to {report_path}")

    return classification_counts, detailed_records

if __name__ == "__main__":
    classify_users()
