import os
from datetime import datetime, timedelta
from app import app, init_db, get_db, set_password_hash

def seed():
    with app.app_context():
        # Ensure schema is up to date
        init_db()
        with get_db() as conn:
            # 1. Base test accounts
            p = set_password_hash("Password123")
            
            # Intern
            conn.execute(
                "INSERT OR IGNORE INTO intern_accounts (name, email, password_hash, password_set, is_active) VALUES (?,?,?,1,1)",
                ("Test Intern", "intern@example.com", p)
            )
            conn.execute("UPDATE intern_accounts SET password_hash=?, password_set=1, is_active=1 WHERE email=?", (p, "intern@example.com"))
            
            # Default Company
            conn.execute(
                "INSERT OR IGNORE INTO companies (name, email, password_hash, is_active, is_approved) VALUES (?,?,?,1,1)",
                ("Test Corp", "company@example.com", p)
            )
            conn.execute("UPDATE companies SET password_hash=?, is_active=1, is_approved=1 WHERE email=?", (p, "company@example.com"))
            
            # Staff & Admin
            conn.execute(
                "INSERT OR IGNORE INTO staff_accounts (name, email, password_hash, is_active) VALUES (?, ?, ?, 1)",
                ("Test Staff", "staff@example.com", p)
            )
            conn.execute("UPDATE staff_accounts SET password_hash=?, is_active=1 WHERE email=?", (p, "staff@example.com"))
            
            conn.execute(
                "INSERT OR IGNORE INTO staff_accounts (name, email, password_hash, is_active) VALUES (?, ?, ?, 1)",
                ("Test Admin", "admin@example.com", p)
            )
            conn.execute("UPDATE staff_accounts SET password_hash=?, is_active=1 WHERE email=?", (p, "admin@example.com"))
            
            # Mentor
            conn.execute(
                "INSERT OR IGNORE INTO mentors (name, email, password_hash) VALUES (?, ?, ?)",
                ("Test Mentor", "mentor@example.com", p)
            )
            conn.execute("UPDATE mentors SET password_hash=? WHERE email=?", (p, "mentor@example.com"))

            # 2. Company: AivaraTech InfoMatics
            aivara_email = "contactus@aivaratech.online"
            aivara_name = "AivaraTech InfoMatics"
            aivara_about = (
                "AivaraTech InfoMatics (AIVARA Technologies) operates under incubation with DBERT, "
                "delivering project-driven technology solutions, AI automation, and advanced data analytics "
                "across enterprise and research domains."
            )
            aivara_site = "https://aivaratechnologies.com"
            
            conn.execute(
                """
                INSERT OR IGNORE INTO companies (name, email, phone, website, about, password_hash, is_approved, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 1, 1)
                """,
                (aivara_name, aivara_email, "+91 9998887776", aivara_site, aivara_about, p)
            )
            conn.execute(
                """
                UPDATE companies 
                SET name=?, website=?, about=?, password_hash=?, is_approved=1, is_active=1
                WHERE email=?
                """,
                (aivara_name, aivara_site, aivara_about, p, aivara_email)
            )
            
            company_row = conn.execute("SELECT id FROM companies WHERE email=?", (aivara_email,)).fetchone()
            company_id = company_row["id"]

            # 3. Post: Data Analytics Internship (from aivara_offer_sender project brain)
            post_title = "Data Analytics Intern"
            post_slug = "data-analytics-intern-aivaratech"
            post_domain = "Data Analyst"
            post_type = "internship"
            post_openings = 50
            post_work_mode = "remote"
            post_location = "Remote"
            post_duration = "2 months"
            post_stipend = 5000
            
            post_description = (
                "Think of this as a working, learning-first role in a genuine, project-driven technology environment "
                "incubated with DBERT. As a Data Analytics Intern at AivaraTech InfoMatics, you will build up your analytical "
                "capabilities, work through assigned structured learning modules, and move into live project contribution "
                "across enterprise datasets, reporting pipelines, and BI dashboards.\n\n"
                "Internship Pathway:\n"
                "1. Learn: Orientation and structured technical learning covering Python, SQL, and data transformation concepts.\n"
                "2. Practise: Hands-on assignments, exploratory data analysis exercises, and reviewed mentor feedback.\n"
                "3. Contribute: Live project contributions across Aivara's data repositories and client analytics pipelines.\n"
                "4. Complete: Final project assessment, technical documentation, and formal exit clearances.\n\n"
                "Expected participation is approximately 10 hours per week, with full remote flexibility."
            )
            
            post_responsibilities = (
                "• Perform exploratory data analysis (EDA) on structured and semi-structured datasets to uncover actionable business insights.\n"
                "• Write and optimize clean SQL queries to extract, transform, and aggregate data across relational databases.\n"
                "• Build, maintain, and automate interactive dashboards and performance reports using Power BI, Tableau, or Python (Streamlit/Dash).\n"
                "• Develop Python data cleaning and preprocessing pipelines using Pandas and NumPy.\n"
                "• Collaborate closely with assigned mentors and technical supervisors on live client analytics deliverables.\n"
                "• Maintain clear data documentation, schema definitions, and version control via Git and GitHub."
            )
            
            post_skills = "Python, SQL, Excel, Power BI, Tableau, Pandas, NumPy, Data Visualization, EDA, Git"
            post_eligibility = "Pursuing or completed Bachelor's or Master's degree in Engineering, Computer Science, IT, BCA/MCA, Statistics, Mathematics, or related quantitative fields. Basic knowledge of Python, SQL, and Excel required."
            
            now = datetime.now()
            published_at = now.strftime("%Y-%m-%d %H:%M:%S")
            expires_at = (now + timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
            apply_by = (now + timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Insert or replace post
            conn.execute("DELETE FROM posts WHERE company_id=? AND title=?", (company_id, post_title))
            conn.execute(
                """
                INSERT INTO posts (
                    company_id, post_type, domain, title, slug, description,
                    responsibilities, skills, location, work_mode,
                    stipend_min, stipend_max, pay_period, is_unpaid,
                    duration, openings, apply_by, certifications_json,
                    eligibility, status, published_at, expires_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', ?, ?, ?, ?)
                """,
                (
                    company_id, post_type, post_domain, post_title, post_slug, post_description,
                    post_responsibilities, post_skills, post_location, post_work_mode,
                    post_stipend, post_stipend, "monthly", 0,
                    post_duration, post_openings, apply_by, "[]",
                    post_eligibility, published_at, expires_at, published_at, published_at
                )
            )
            
            conn.commit()
            print("Seeded successfully:")
            print(f" - Company: {aivara_name} (ID: {company_id}, Email: {aivara_email})")
            print(f" - Internship: {post_title} (Openings: {post_openings}, Domain: {post_domain}, Mode: {post_work_mode})")

if __name__ == "__main__":
    seed()
