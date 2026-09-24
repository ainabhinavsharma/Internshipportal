import os
import sys
import sqlite3
from datetime import datetime, timedelta

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.getcwd())

from app import app, init_db, get_db, set_password_hash, now_str, get_week_bounds

def seed_vikram():
    email = "accepted.intern@example.com"
    password = "Password123"
    name = "Vikram Malhotra"
    now = datetime.now()

    print(f"[*] Seeding demo intern {name} ({email})...")

    with app.app_context():
        init_db()
        with get_db() as conn:
            p = set_password_hash(password)

            # 1. Create or update intern_accounts
            conn.execute("""
                INSERT OR IGNORE INTO intern_accounts (
                    name, email, phone, city, college, course, semester,
                    year_of_passing, domain, password_hash, password_set, is_active, signup_stage, created_at, updated_at
                ) VALUES (?, ?, '+91 9876543214', 'Tiruchirappalli', 'NIT Trichy', 'B.Tech', '6', '2027', 'Data Analyst', ?, 1, 1, 1, ?, ?)
            """, (name, email, p, now_str(), now_str()))

            conn.execute("""
                UPDATE intern_accounts SET 
                    name=?, phone='+91 9876543214', city='Tiruchirappalli', college='NIT Trichy',
                    course='B.Tech', semester='6', year_of_passing='2027', domain='Data Analyst',
                    password_hash=?, password_set=1, is_active=1
                WHERE email=?
            """, (name, p, email))

            acct = conn.execute("SELECT id FROM intern_accounts WHERE email=?", (email,)).fetchone()
            acc_id = acct["id"]

            # 2. Create or update applications
            conn.execute("DELETE FROM applications WHERE email=?", (email,))
            cur_app = conn.execute("""
                INSERT INTO applications (
                    name, email, phone, city, college, course, semester,
                    year_of_passing, domain, why_join, status, mentor_note,
                    reviewed_at, created_at, updated_at
                ) VALUES (?, ?, '+91 9876543214', 'Tiruchirappalli', 'NIT Trichy', 'B.Tech', '6', '2027',
                          'Data Analyst', 'Passionate about data analytics.', 'Accepted',
                          'Verified & Accepted. Welcome to the Data Analytics team!', ?, ?, ?)
            """, (name, email, now_str(), now_str(), now_str()))
            app_id = cur_app.lastrowid

            conn.execute("UPDATE intern_accounts SET application_id=? WHERE id=?", (app_id, acc_id))

            # 3. Create or update enrollments
            conn.execute("DELETE FROM enrollments WHERE email=?", (email,))
            conn.execute("""
                INSERT INTO enrollments (
                    application_id, timestamp, name, email, phone,
                    city, college, course, semester, year_of_passing, domain,
                    joining_date, batch_label, payment_screenshot, payment_status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, '+91 9876543214',
                          'Tiruchirappalli', 'NIT Trichy', 'B.Tech', '6', '2027', 'Data Analyst',
                          ?, 'DA-Alpha-2026', 'uploads/verified_payment.jpg', 'Verified',
                          ?, ?)
            """, (app_id, now_str(), name, email, (now - timedelta(days=14)).strftime("%Y-%m-%d"), now_str(), now_str()))

            # 4. Seed attendance records (4 weeks)
            conn.execute("DELETE FROM attendance WHERE intern_id=?", (acc_id,))
            weeks_data = [
                (0, 435),  # Current week: 7h 15m
                (1, 690),  # Week -1: 11h 30m (Target Met)
                (2, 615),  # Week -2: 10h 15m (Target Met)
                (3, 480),  # Week -3: 8h 0m
            ]
            for off, mins in weeks_data:
                w_start, w_end = get_week_bounds(now.date() - timedelta(days=7 * off))
                conn.execute(
                    "INSERT INTO attendance (intern_id, week_start, week_end, total_minutes, updated_at) VALUES (?, ?, ?, ?, ?)",
                    (acc_id, w_start.strftime("%Y-%m-%d"), w_end.strftime("%Y-%m-%d"), mins, now_str())
                )

            # 5. Course enrollment in Course #2
            course = conn.execute("SELECT id FROM courses WHERE id=2 OR slug='data-analytics-accelerated' LIMIT 1").fetchone()
            if course:
                conn.execute("DELETE FROM course_enrollments WHERE course_id=? AND intern_id=?", (course["id"], acc_id))
                conn.execute("""
                    INSERT INTO course_enrollments (course_id, intern_id, payment_status, progress_percent, is_completed, enrolled_at)
                    VALUES (?, ?, 'completed', 45, 0, ?)
                """, (course["id"], acc_id, now_str()))

            conn.commit()

    print("[+] Successfully seeded Vikram Malhotra demo account!")
    print(f"    • Email:    {email}")
    print(f"    • Password: {password}")
    print(f"    • Status:   Accepted (Full features unlocked)")

if __name__ == "__main__":
    seed_vikram()
