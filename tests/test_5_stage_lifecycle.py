"""
Comprehensive End-to-End Verification Test Suite for the 5-Stage Sequential Intern Lifecycle
Tests all 5 stages, domain course isolation, and live-data safety.
"""
import os
import sys
import unittest
import json
import sqlite3
import io

# Add parent directory to sys.path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import (
    app, get_db, init_db, create_session, AUTH_COOKIE,
    get_intern_flow_state, auto_enroll_intern_in_domain_courses, ensure_application_record,
    STAGE_APP_REQUIRED, STAGE_UNDER_REVIEW, STAGE_SELECTED, STAGE_PAYMENT_PENDING, STAGE_CONFIRMED, STAGE_REJECTED,
    STATUS_UNDER_REVIEW, STATUS_SELECTED, STATUS_ACCEPTED, STATUS_REJECTED,
    PLATFORM_DOMAIN_COURSES, VALID_DOMAINS
)

class Test5StageLifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        init_db()

    def setUp(self):
        self.client = app.test_client()
        self.email_base = "test_lifecycle_{}@dbert.test"
        self.csrf_token = "test_csrf_secret_12345"

    def login(self, email, role="intern"):
        token = create_session(email, role)
        self.client.set_cookie(AUTH_COOKIE, token)
        with self.client.session_transaction() as sess:
            sess["_csrf"] = self.csrf_token
        return token

    def post(self, url, **kwargs):
        with get_db() as conn:
            conn.execute("DELETE FROM rate_events")
            conn.commit()
        headers = kwargs.pop("headers", {})
        headers["X-CSRF-Token"] = self.csrf_token
        return self.client.post(url, headers=headers, **kwargs)

    def test_seeded_domain_courses(self):
        """Verify all 4 domain foundational courses exist in database with chapters and quizzes."""
        with get_db() as conn:
            courses = conn.execute("SELECT id, title, domain, is_active FROM courses WHERE domain IS NOT NULL").fetchall()
            domains_found = {c["domain"] for c in courses if c["is_active"]}
            for domain in VALID_DOMAINS:
                self.assertIn(domain, domains_found, f"Missing seeded course for domain: {domain}")

            # Check that each course has chapters and quizzes
            for c in courses:
                ch_count = conn.execute("SELECT COUNT(*) FROM course_chapters WHERE course_id=?", (c["id"],)).fetchone()[0]
                self.assertGreaterEqual(ch_count, 3, f"Course {c['title']} should have at least 3 chapters")
                q_count = conn.execute("SELECT COUNT(*) FROM course_day_quizzes WHERE course_id=?", (c["id"],)).fetchone()[0]
                self.assertGreaterEqual(q_count, 3, f"Course {c['title']} should have at least 3 quizzes")

    def test_full_5_stage_sequential_lifecycle(self):
        """End-to-end test walking a candidate through Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5."""
        email = self.email_base.format("candidate_full")
        with get_db() as conn:
            # 1. Simulate Sign Up (Account created, no application yet)
            conn.execute("DELETE FROM course_enrollments WHERE intern_id IN (SELECT id FROM intern_accounts WHERE email=?)", (email,))
            conn.execute("DELETE FROM user_sessions WHERE email=?", (email,))
            conn.execute("DELETE FROM enrollments WHERE email=?", (email,))
            conn.execute("DELETE FROM intern_accounts WHERE email=?", (email,))
            conn.execute("DELETE FROM applications WHERE email=?", (email,))
            conn.execute("""
                INSERT INTO intern_accounts (name, email, password_hash, domain, college, course, is_active, created_at)
                VALUES (?, ?, 'fakehash', 'AI Agent Development', 'IIT Delhi', 'B.Tech CS', 1, datetime('now'))
            """, ("Arjun Sharma", email))
            conn.commit()

        # Login session
        self.login(email, role="intern")

        # STAGE 1: APPLICATION REQUIRED
        with get_db() as conn:
            st1 = get_intern_flow_state(conn, email)
            self.assertEqual(st1["stage"], STAGE_APP_REQUIRED)
            self.assertEqual(st1["stage_num"], 1)
            self.assertFalse(st1["can_upload_payment"])

        wiz_res = self.client.get("/intern/wizard-status")
        self.assertEqual(wiz_res.status_code, 200)
        wiz_data = json.loads(wiz_res.data)
        self.assertEqual(wiz_data["stage_num"], 1)
        self.assertTrue(wiz_data["payment_locked"])

        # Valid PNG magic bytes for upload testing
        valid_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"\x00" * 50

        # Attempt deposit in Stage 1 -> MUST BE BLOCKED
        bad_enroll = self.post("/enroll", data={
            "name": "Arjun Sharma",
            "email": email,
            "phone": "9876543210",
            "joining_date": "2026-10-05",
            "domain": "AI Agent Development",
            "payment_screenshot": (io.BytesIO(valid_png), "receipt.png")
        }, content_type="multipart/form-data")
        self.assertIn(bad_enroll.status_code, (400, 403))
        self.assertIn("application", json.loads(bad_enroll.data)["message"].lower())

        # STAGE 2: SUBMIT APPLICATION (UNDER REVIEW)
        sop_text = "I am deeply passionate about building autonomous LLM agents and want to master RAG architectures at DBERT Labs."
        save_sop = self.post("/intern/save-wizard-step", json={
            "step_key": "application_sop",
            "why_join": sop_text
        })
        self.assertEqual(save_sop.status_code, 200)
        sop_res = json.loads(save_sop.data)
        self.assertEqual(sop_res["stage"], STAGE_UNDER_REVIEW)

        with get_db() as conn:
            st2 = get_intern_flow_state(conn, email)
            self.assertEqual(st2["stage"], STAGE_UNDER_REVIEW)
            self.assertEqual(st2["stage_num"], 2)
            self.assertFalse(st2["can_upload_payment"])

        # Attempt deposit in Stage 2 -> MUST BE BLOCKED (403 Under Review)
        bad_enroll2 = self.post("/enroll", data={
            "name": "Arjun Sharma",
            "email": email,
            "phone": "9876543210",
            "joining_date": "2026-10-05",
            "domain": "AI Agent Development",
            "payment_screenshot": (io.BytesIO(valid_png), "receipt.png")
        }, content_type="multipart/form-data")
        self.assertEqual(bad_enroll2.status_code, 403)
        self.assertIn("under review", json.loads(bad_enroll2.data)["message"].lower())

        # STAGE 3: ADMIN APPROVES APPLICATION (SELECTED)
        with get_db() as conn:
            conn.execute("UPDATE applications SET status=? WHERE email=?", (STATUS_SELECTED, email))
            conn.commit()

            st3 = get_intern_flow_state(conn, email)
            self.assertEqual(st3["stage"], STAGE_SELECTED)
            self.assertEqual(st3["stage_num"], 3)
            self.assertTrue(st3["can_upload_payment"])

        # Check wizard status in Stage 3 -> payment is UNLOCKED
        wiz_res3 = self.client.get("/intern/wizard-status")
        wiz_data3 = json.loads(wiz_res3.data)
        self.assertEqual(wiz_data3["stage_num"], 3)
        step_keys = [s["key"] for s in wiz_data3["steps"]]
        self.assertIn("payment_screenshot", step_keys)

        # STAGE 4: INTERN UPLOADS DEPOSIT RECEIPT
        enr_res = self.post("/enroll", data={
            "name": "Arjun Sharma",
            "email": email,
            "phone": "9876543210",
            "joining_date": "2026-10-05",
            "domain": "AI Agent Development",
            "payment_screenshot": (io.BytesIO(valid_png), "receipt.png")
        }, content_type="multipart/form-data")
        self.assertEqual(enr_res.status_code, 200)

        with get_db() as conn:
            st4 = get_intern_flow_state(conn, email)
            self.assertEqual(st4["stage"], STAGE_PAYMENT_PENDING)
            self.assertEqual(st4["stage_num"], 4)
            self.assertFalse(st4["is_accepted"])

            enr_row = conn.execute("SELECT payment_status FROM enrollments WHERE email=?", (email,)).fetchone()
            self.assertEqual(enr_row["payment_status"], "Pending Verification")

        # STAGE 5: ADMIN ACCEPTS PAYMENT RECEIPT
        with get_db() as conn:
            conn.execute("UPDATE enrollments SET payment_status='Accepted' WHERE email=?", (email,))
            conn.execute("UPDATE applications SET status=? WHERE email=?", (STATUS_ACCEPTED, email))
            conn.commit()

            st5 = get_intern_flow_state(conn, email)
            self.assertEqual(st5["stage"], STAGE_CONFIRMED)
            self.assertEqual(st5["stage_num"], 5)
            self.assertTrue(st5["is_accepted"])

        # /intern/me automatically enrolls the accepted intern in domain course
        me_res = self.client.get("/intern/me")
        self.assertEqual(me_res.status_code, 200)
        me_data = json.loads(me_res.data)
        self.assertEqual(me_data["flow_stage"], STAGE_CONFIRMED)
        self.assertEqual(me_data["flow_state"]["stage_num"], 5)
        self.assertTrue(me_data["flow_state"]["is_accepted"])
        self.assertGreaterEqual(len(me_data["course_enrollments"]), 1)
        self.assertEqual(me_data["course_enrollments"][0]["domain"], "AI Agent Development")

    def test_domain_course_catalog_isolation(self):
        """Verify interns see only their domain course in catalog, and cannot access other domain courses."""
        email_py = self.email_base.format("python_intern")
        email_ai = self.email_base.format("ai_intern")

        with get_db() as conn:
            for em in (email_py, email_ai):
                conn.execute("DELETE FROM course_enrollments WHERE intern_id IN (SELECT id FROM intern_accounts WHERE email=?)", (em,))
                conn.execute("DELETE FROM enrollments WHERE email=?", (em,))
                conn.execute("DELETE FROM user_sessions WHERE email=?", (em,))
                conn.execute("DELETE FROM intern_accounts WHERE email=?", (em,))
                conn.execute("DELETE FROM applications WHERE email=?", (em,))

            # Create Python intern
            conn.execute("""
                INSERT INTO intern_accounts (name, email, password_hash, domain, is_active, created_at)
                VALUES ('Python Intern', ?, 'fake', 'Python Automation', 1, datetime('now'))
            """, (email_py,))
            conn.execute("""
                INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at)
                VALUES ('Python Intern', ?, '9876543211', 'Pune', 'COEP', 'B.Tech', '6th', '2026', 'Python Automation', 'Passionate about Python automation', 'Accepted', datetime('now'))
            """, (email_py,))

            # Create AI intern
            conn.execute("""
                INSERT INTO intern_accounts (name, email, password_hash, domain, is_active, created_at)
                VALUES ('AI Intern', ?, 'fake', 'AI Agent Development', 1, datetime('now'))
            """, (email_ai,))
            conn.execute("""
                INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at)
                VALUES ('AI Intern', ?, '9876543212', 'Delhi', 'IITD', 'B.Tech', '6th', '2026', 'AI Agent Development', 'Passionate about AI agents', 'Accepted', datetime('now'))
            """, (email_ai,))
            conn.commit()

        # Login as Python intern
        self.login(email_py, role="intern")

        # Test catalog filtering
        catalog_res = self.client.get("/courses")
        self.assertEqual(catalog_res.status_code, 200)
        html = catalog_res.data.decode("utf-8")
        self.assertIn("Python Automation", html)
        self.assertIn("Your Assigned Internship Specialization Track", html)

        with get_db() as conn:
            ai_course = conn.execute("SELECT id FROM courses WHERE domain='AI Agent Development' LIMIT 1").fetchone()
            py_course = conn.execute("SELECT id FROM courses WHERE domain='Python Automation' LIMIT 1").fetchone()

        # Python intern accessing AI course -> should redirect with notice
        ai_detail = self.client.get(f"/courses/{ai_course['id']}")
        self.assertEqual(ai_detail.status_code, 302)
        self.assertIn("/courses", ai_detail.location)

        # Python intern accessing own course -> should succeed (200)
        py_detail = self.client.get(f"/courses/{py_course['id']}")
        self.assertEqual(py_detail.status_code, 200)

        # Python intern attempting to enroll in AI course -> should return 403
        bad_enroll = self.post(f"/courses/{ai_course['id']}/enroll", headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(bad_enroll.status_code, 403)
        self.assertIn("restricted", json.loads(bad_enroll.data)["message"].lower())


if __name__ == "__main__":
    unittest.main()
