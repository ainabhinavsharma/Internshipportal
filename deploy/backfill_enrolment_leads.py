import sqlite3
import os

DB_FILE = os.environ.get("DB_FILE", "internship.db")

def backfill():
    print(f"[*] Connecting to {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    no_apps = cur.execute("""
        SELECT ia.id, ia.name, ia.email, ia.phone, ia.city, ia.college, ia.course, 
               ia.semester, ia.year_of_passing, ia.domain, ia.visitor_id, ia.created_at
        FROM intern_accounts ia
        WHERE NOT EXISTS (
            SELECT 1 FROM applications a WHERE LOWER(a.email) = LOWER(ia.email)
        )
    """).fetchall()

    print(f"[*] Found {len(no_apps)} intern accounts without an application.")
    inserted = 0
    for acct in no_apps:
        domain = acct["domain"] or "AI Agent Development"
        res = cur.execute("""
            INSERT INTO applications (
                name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, source, visitor_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Selected', 'backfill_signup', ?, ?, ?)
        """, (
            acct["name"] or "Intern",
            acct["email"],
            acct["phone"] or "N/A",
            acct["city"] or "Online / Remote",
            acct["college"] or "Student",
            acct["course"] or "B.Tech",
            acct["semester"] or "6",
            acct["year_of_passing"] or "2026",
            domain,
            "Enrolled via DBERT portal direct registration.",
            acct["visitor_id"] or "",
            acct["created_at"],
            acct["created_at"]
        ))
        app_id = res.lastrowid
        cur.execute("UPDATE intern_accounts SET application_id=?, domain=? WHERE id=?", (app_id, domain, acct["id"]))
        inserted += 1

    conn.commit()
    conn.close()
    print(f"[+] Successfully backfilled {inserted} applications in 'Selected' status!")

if __name__ == "__main__":
    backfill()
