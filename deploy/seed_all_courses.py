#!/usr/bin/env python3
"""
=============================================================================
DBERT LMS Multi-Domain Course Seeder (Production & EC2 Ready)
=============================================================================
Domains covered:
  1. Full Stack Development     (slug: full-stack-web-development)
  2. AI Agent Development       (slug: ai-agent-development)
  3. Python Automation          (slug: python-automation-engineering)

Idempotent: Safely re-runnable without corrupting enrollments or user data.
Zero External Dependencies: Uses pure Python standard library (sqlite3, json, sys, os).

Usage on EC2:
  python deploy/seed_all_courses.py --db-path /var/www/apps/internship/internship.db --all
  python deploy/seed_all_courses.py --domain fullstack
  python deploy/seed_all_courses.py --domain ai_agent
  python deploy/seed_all_courses.py --domain automation
"""

import os
import sys
import json
import sqlite3
import argparse
from datetime import datetime

# =============================================================================
# 1. CURRICULUM DATA DEFINITIONS
# =============================================================================

def get_full_stack_curriculum():
    return {
        "title": "Full Stack Web Development: Modern Architecture, REST APIs & Cloud Deployment",
        "slug": "full-stack-web-development",
        "domain": "Full Stack Development",
        "level": "Beginner to Intermediate",
        "estimated_hours": 18,
        "banner_gradient": "linear-gradient(135deg, #3B82F6, #1D4ED8)",
        "project_brief": """
<div class="capstone-brief">
  <h2>Capstone Assignment: Enterprise SaaS Task &amp; Workflow Management Portal</h2>
  <p><strong>Goal:</strong> Architect, implement, test, and deploy a full-featured, multi-tenant SaaS application that mirrors the modern production architecture used across enterprise web platforms.</p>
  
  <h3>1. Core Architecture Requirements</h3>
  <ul>
    <li><strong>Backend:</strong> Python Flask application utilizing modular Blueprints (<code>routes/auth.py</code>, <code>routes/tasks.py</code>, <code>routes/api.py</code>).</li>
    <li><strong>Database:</strong> SQLite with Write-Ahead Logging (WAL) mode or PostgreSQL, with proper foreign key constraints, indexes on query predicates, and transactional integrity.</li>
    <li><strong>Frontend:</strong> Responsive, accessible user interface built using modern React (Vite) or semantic HTML5, CSS design tokens / Tailwind, and asynchronous JavaScript (Fetch API / Axios).</li>
    <li><strong>Security:</strong> Password hashing via bcrypt/PBKDF2 with unique salts, HTTP-only/SameSite cookies, CSRF tokens, and Content Security Policy (CSP) headers.</li>
  </ul>

  <h3>2. Functional Requirements</h3>
  <ol>
    <li><strong>Authentication &amp; User State:</strong> User registration, secure login with rate-limiting, session management, and role-based access control (Admin vs Team Member).</li>
    <li><strong>CRUD Workflows:</strong> Create, view, update, and archive tasks with priorities, status tags (Backlog, In Progress, In Review, Completed), and deadlines.</li>
    <li><strong>Activity Audit Log:</strong> Automated database tracking of every update (who changed status, timestamp, previous value).</li>
    <li><strong>File Attachment &amp; Multipart Handling:</strong> Ability to attach supporting documentation or screenshots to tasks with MIME-type validation and sanitized file naming.</li>
    <li><strong>Search &amp; Filtering:</strong> Real-time asynchronous search by keyword, priority, and date range without full page reloads.</li>
  </ol>

  <h3>3. Deliverables &amp; Evaluation Criteria</h3>
  <ul>
    <li>A public GitHub repository containing clean, committed source code.</li>
    <li>A production-ready <code>README.md</code> with system architecture diagrams, database schema documentation, setup instructions, and API endpoint references.</li>
    <li>Proof of production deployment (AWS EC2, Render, or Railway) with live domain or IP address link.</li>
  </ul>
</div>
""",
        "days": [
            {
                "day": 1,
                "title": "Modern Web Architecture, Semantic HTML5 & Modern CSS Systems",
                "subtopics": [
                    {
                        "title": "Client-Server Architecture & The HTTP Request Lifecycle",
                        "brief": "Explore the foundational mechanics of the modern internet. Analyze the complete lifecycle of a web request: DNS resolution, TCP three-way handshake, TLS cryptographic negotiation, and HTTP/1.1 vs HTTP/2 multiplexing. Examine REST protocol semantics, distinguishing idempotent idempotent operations (GET, PUT, DELETE) from non-idempotent operations (POST, PATCH), and master HTTP status code families (2xx success, 3xx redirection, 4xx client errors, 5xx server faults).",
                        "takeaways": [
                            "Trace the journey of a network packet from browser address bar to web server and back.",
                            "Leverage HTTP caching headers (Cache-Control, ETag, If-None-Match) to optimize network bandwidth.",
                            "Design RESTful URL paths adhering to uniform resource identification standards."
                        ],
                        "prompt_seed": "Explain the step-by-step lifecycle of an HTTP POST request from browser form submission to database commit."
                    },
                    {
                        "title": "Semantic HTML5, Accessibility (a11y) & The DOM Tree",
                        "brief": "Build web interfaces that are universally accessible and search-engine optimized. Replace unsemantic div-soup with semantic landmark tags (<header>, <nav>, <main>, <article>, <aside>, <footer>). Master WCAG 2.1 AA accessibility guidelines, color contrast ratios, keyboard tab navigation, and ARIA attributes (aria-label, aria-live). Understand how the browser parses markup into the Document Object Model (DOM) and accessibility tree.",
                        "takeaways": [
                            "Construct clean, accessible document outlines using HTML5 landmark elements.",
                            "Formulate form controls with explicitly paired <label> tags and accessible validation feedback.",
                            "Conduct browser accessibility audits using Lighthouse and keyboard navigation checks."
                        ],
                        "prompt_seed": "Contrast semantic HTML elements with generic <div> tags and explain their impact on accessibility and SEO."
                    },
                    {
                        "title": "Modern CSS Layouts, Design Tokens & Tailwind Fundamentals",
                        "brief": "Architect scalable, maintainable CSS systems. Master one-dimensional layouts with Flexbox and two-dimensional matrix grid systems with CSS Grid. Learn to build custom design systems using CSS Custom Properties (variables) for design tokens (colors, typography, spacing, shadows). Transition from rigid pixel values to fluid responsive units (rem, clamp(), min(), max()). Explore utility-first CSS principles as embodied by modern frameworks like Tailwind CSS.",
                        "takeaways": [
                            "Build complex multi-column responsive dashboard layouts with CSS Grid and Flexbox.",
                            "Create dynamic, zero-runtime theme switchers (light/dark mode) using CSS Custom Properties.",
                            "Apply mobile-first responsive design strategies without relying on bloated legacy frameworks."
                        ],
                        "prompt_seed": "How do CSS variables enable dynamic theming (light/dark mode) without reloading stylesheets?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "Which of the following HTTP methods is considered idempotent by REST standards?",
                        "options": ["POST", "PATCH", "PUT", "CONNECT"],
                        "correct_index": 2
                    },
                    {
                        "id": 2,
                        "question": "What is the primary architectural purpose of semantic HTML5 tags such as <main> and <nav>?",
                        "options": [
                            "They automatically apply built-in CSS styling animations to the page",
                            "They communicate structural meaning to search engines and assistive screen readers",
                            "They improve JavaScript execution speed by compiling into WebAssembly",
                            "They bypass browser Content Security Policy restrictions"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "In modern responsive CSS, what does the expression 'width: clamp(200px, 50vw, 800px)' do?",
                        "options": [
                            "It fixes the element width strictly at 50vw across all screens",
                            "It throws an error because clamp() only accepts pixel values",
                            "It sets a fluid width of 50vw bounded by a minimum of 200px and maximum of 800px",
                            "It centers the element horizontally inside its grid container"
                        ],
                        "correct_index": 2
                    },
                    {
                        "id": 4,
                        "question": "What is the difference between an HTTP 301 and an HTTP 302 redirect status code?",
                        "options": [
                            "301 indicates a permanent redirect that browsers cache; 302 indicates a temporary redirect",
                            "301 is an internal server error; 302 is an authentication error",
                            "301 is used only for image files; 302 is used for HTML pages",
                            "301 requires HTTPS; 302 only works over unencrypted HTTP"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 5,
                        "question": "In Flexbox, what does the property 'justify-content' control compared to 'align-items'?",
                        "options": [
                            "justify-content aligns items along the cross axis; align-items along the main axis",
                            "justify-content aligns items along the main axis; align-items along the cross axis",
                            "Both properties perform identical operations along the vertical axis",
                            "justify-content handles text justification inside paragraphs only"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 2,
                "title": "Modern JavaScript & Frontend Engineering with React",
                "subtopics": [
                    {
                        "title": "Modern JavaScript (ES6+), Event Loop & Asynchronous Control",
                        "brief": "Deepen your understanding of JavaScript fundamentals. Master ES6+ features: destructuring, rest/spread operators, arrow functions, template literals, and optional chaining (?.), nullish coalescing (??). Explore the V8 engine architecture: call stack, memory heap, microtask queue (Promises), and macrotask queue (setTimeout). Write robust asynchronous code with async/await, handling concurrency with Promise.all and Promise.allSettled.",
                        "takeaways": [
                            "Debug asynchronous timing bugs and race conditions using knowledge of the event loop.",
                            "Write clean, readable functional code using ES6+ syntax and immutability patterns.",
                            "Execute concurrent API calls safely using Promise.allSettled."
                        ],
                        "prompt_seed": "Explain how JavaScript's microtask queue processes Promises compared to setTimeout in the event loop."
                    },
                    {
                        "title": "React Fundamentals, JSX & Component Architecture",
                        "brief": "Transition from imperative DOM manipulation to declarative user interfaces. Understand how React's Virtual DOM computes diffs to minimize real DOM mutations. Build composable functional components, pass data via unidirectional props, handle synthetic events, and render lists efficiently using stable key attributes. Understand the build-time compilation of JSX to React.createElement using modern bundlers like Vite.",
                        "takeaways": [
                            "Break down UI mockups into composable, single-responsibility React components.",
                            "Manage data flow predictably from parent components to children via props.",
                            "Avoid re-rendering bugs by providing stable, unique keys to dynamic list elements."
                        ],
                        "prompt_seed": "Why must list items in React always have stable, unique keys rather than array indices?"
                    },
                    {
                        "title": "State Management with React Hooks (useState, useEffect, useRef)",
                        "brief": "Master React's official hook primitives. Manage local state with useState, ensuring state updates are treated immutably. Handle component side effects, asynchronous subscriptions, and DOM lifecycles with useEffect. Understand the role of dependency arrays in preventing infinite re-render loops and stale closures. Use useRef to persist mutable values across renders and interact directly with native DOM nodes.",
                        "takeaways": [
                            "Manage interactive UI state cleanly with functional updater functions in useState.",
                            "Correctly specify dependency arrays in useEffect to prevent stale closures and memory leaks.",
                            "Safely capture references to DOM elements using useRef."
                        ],
                        "prompt_seed": "What happens when you omit the dependency array in useEffect, and how do you prevent stale closures in React hooks?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "In the JavaScript event loop, which queue has higher execution priority after the current call stack clears?",
                        "options": [
                            "The Macrotask queue (setTimeout, setInterval)",
                            "The Microtask queue (Promise callbacks, queueMicrotask)",
                            "The RequestAnimationFrame queue",
                            "The Garbage Collection queue"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "Why should array indices generally be avoided as keys when rendering dynamic lists in React?",
                        "options": [
                            "React will throw a runtime syntax exception and crash",
                            "Array indices can cause component state bugs and incorrect DOM recycling when items are reordered or filtered",
                            "Array indices consume twice as much memory in the virtual DOM",
                            "Vite bundler cannot compile JSX containing numeric keys"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "What is the primary purpose of the cleanup function returned from a React useEffect hook?",
                        "options": [
                            "To delete the component from the browser history",
                            "To clear timers, cancel pending network subscriptions, and clean up resources before unmounting or re-running",
                            "To reset all useState variables back to their initial values",
                            "To force an immediate browser page reload"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What does the JavaScript nullish coalescing operator (??) evaluate?",
                        "options": [
                            "It returns the right-hand operand only if the left-hand operand is strictly null or undefined",
                            "It returns the right-hand operand if the left-hand operand is any falsy value (0, '', false)",
                            "It compares whether two objects have identical memory references",
                            "It performs a cryptographic hash comparison between two strings"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 5,
                        "question": "What distinguishes useRef from useState in React functional components?",
                        "options": [
                            "useRef can only store strings, whereas useState can store any type",
                            "Updating a ref value (.current) does not trigger a component re-render, whereas calling a state setter does",
                            "useRef cannot be used inside custom hooks",
                            "useState values persist across page reloads automatically"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 3,
                "title": "Backend Fundamentals & RESTful API Engineering with Python & Flask",
                "subtopics": [
                    {
                        "title": "WSGI Applications & The Flask Request/Response Lifecycle",
                        "brief": "Unpack Python web architectures. Understand the Web Server Gateway Interface (WSGI) standard that bridges production web servers (Nginx/Gunicorn) with Python web applications. Learn how Flask initializes application and request contexts. Explore Flask request objects (headers, form data, JSON payloads, query parameters) and response construction (jsonify, status codes, custom headers).",
                        "takeaways": [
                            "Understand the boundary between web servers (WSGI) and Python application logic.",
                            "Inspect inbound HTTP headers, cookies, and JSON payloads within Flask request contexts.",
                            "Construct consistent, standardized JSON HTTP responses with proper status codes."
                        ],
                        "prompt_seed": "Explain how WSGI allows web servers like Nginx/Gunicorn to communicate with Python frameworks like Flask."
                    },
                    {
                        "title": "Designing Idempotent RESTful APIs with JSON Payloads",
                        "brief": "Design production-grade REST APIs. Implement standard CRUD routing patterns, dynamic URL converters (<int:id>, <string:slug>), and query-string pagination (page, per_page). Enforce input validation, content-type verification (application/json), and handle errors with unified schema formats (e.g. {'status': 'error', 'message': '...'}). Master HTTP semantics for creation (201 Created with Location header) and validation failures (400 Bad Request, 422 Unprocessable Entity).",
                        "takeaways": [
                            "Implement URL parameter converters to enforce type safety at the routing layer.",
                            "Design uniform error response envelopes across all API endpoints.",
                            "Structure clean pagination metadata (total_count, page, total_pages) for client consumption."
                        ],
                        "prompt_seed": "What makes an HTTP method idempotent, and why are PUT and DELETE idempotent while POST is not?"
                    },
                    {
                        "title": "Modular Architecture with Flask Blueprints & Middleware",
                        "brief": "Scale web applications from monolithic scripts into organized, maintainable architectures. Structure backend systems using Flask Blueprints to separate authentication, administration, and resource endpoints into discrete modules. Implement application middleware hooks: before_request (authentication checks, rate limits), after_request (security headers, CSP nonces), and teardown_request (database connection cleanup).",
                        "takeaways": [
                            "Organize enterprise web applications into decoupled, testable Flask Blueprints.",
                            "Centralize cross-cutting concerns (authentication gates, audit logging) in before_request hooks.",
                            "Enforce security headers and clean up database connections in after_request hooks."
                        ],
                        "prompt_seed": "How do Flask Blueprints solve code duplication and route organization in enterprise web applications?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the primary role of WSGI (Web Server Gateway Interface) in Python web deployments?",
                        "options": [
                            "To compile Python bytecode into C++ for faster execution",
                            "To act as a standardized interface between web servers (e.g. Gunicorn/Nginx) and Python web applications",
                            "To provide browser-based CSS styling templates",
                            "To encrypt database passwords automatically"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "Which HTTP status code is the most semantically appropriate when a new resource is successfully created via POST?",
                        "options": ["200 OK", "201 Created", "204 No Content", "202 Accepted"],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "In Flask, what is the key advantage of using Blueprints?",
                        "options": [
                            "They replace the need for an underlying database",
                            "They modularize routes, templates, and static assets into independent logical components",
                            "They convert Flask synchronous routes into async Go routines",
                            "They automatically eliminate all CSS specificity conflicts"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What happens if a client submits a POST request with malformed JSON to a Flask route expecting request.get_json()?",
                        "options": [
                            "Flask re-routes the user to the homepage",
                            "Flask by default raises a 400 Bad Request HTTP exception unless silent=True is passed",
                            "The server crashes and terminates the WSGI worker process",
                            "The malformed JSON is automatically converted into an XML string"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "Which Flask hook executes after every request, allowing you to append security headers to the outgoing response?",
                        "options": ["@app.before_request", "@app.teardown_request", "@app.after_request", "@app.context_processor"],
                        "correct_index": 2
                    }
                ]
            },
            {
                "day": 4,
                "title": "Relational Database Modeling, SQL & Data Integrity",
                "subtopics": [
                    {
                        "title": "Schema Normalization & Entity-Relationship Design",
                        "brief": "Design robust database architectures. Walk through relational normalization rules from First Normal Form (1NF: atomic values) through Third Normal Form (3NF: eliminating transitive dependencies). Define primary keys, composite keys, and foreign key relationships (1:1, 1:N, N:M junction tables). Master integrity constraints: NOT NULL, UNIQUE, CHECK, and cascade behavior (ON DELETE CASCADE, ON DELETE SET NULL).",
                        "takeaways": [
                            "Eliminate data redundancy and update anomalies through relational normalization.",
                            "Model many-to-many business relationships using normalized join tables.",
                            "Enforce business rules directly in database DDL via CHECK constraints."
                        ],
                        "prompt_seed": "Walk through normalizing an unnormalized order invoice table with repeating items into 3rd Normal Form (3NF)."
                    },
                    {
                        "title": "Query Optimization, Multi-Table Joins & Indexing Strategies",
                        "brief": "Write high-performance SQL queries. Master relational joins: INNER JOIN, LEFT OUTER JOIN, and cross joins. Understand join cardinality and avoid cartesian explosion traps that duplicate financial data. Learn how B-tree indexes accelerate WHERE and ORDER BY lookups. Use EXPLAIN QUERY PLAN to detect full table scans (SCAN TABLE) and evaluate when covering indexes or composite indexes are warranted.",
                        "takeaways": [
                            "Analyze execution plans to optimize slow queries and eliminate full table scans.",
                            "Create composite B-tree indexes matching query predicate column ordering.",
                            "Audit join output row counts to prevent metric inflation from multi-table joins."
                        ],
                        "prompt_seed": "How do B-tree indexes accelerate WHERE and JOIN lookups, and why does over-indexing degrade write performance?"
                    },
                    {
                        "title": "ACID Transactions, Concurrency & SQLite WAL Mode",
                        "brief": "Protect data integrity under concurrent traffic. Master ACID guarantees: Atomicity, Consistency, Isolation, and Durability. Implement database transactions with BEGIN, COMMIT, and ROLLBACK blocks. Understand race conditions (dirty reads, non-repeatable reads, lost updates). Configure SQLite Write-Ahead Logging (PRAGMA journal_mode=WAL) to enable simultaneous readers and writers without lock contention.",
                        "takeaways": [
                            "Prevent financial race conditions using explicit database transactions with rollback safety.",
                            "Configure SQLite WAL mode and busy timeouts for high-throughput concurrent production apps.",
                            "Safely handle database deadlocks and concurrency locks in web services."
                        ],
                        "prompt_seed": "Explain how Write-Ahead Logging (WAL) allows concurrent readers while a transaction is actively writing in SQLite."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the primary condition required for a relational database table to satisfy Third Normal Form (3NF)?",
                        "options": [
                            "It must have at least five columns and an auto-incrementing integer ID",
                            "It must be in 2NF and contain no transitive functional dependencies of non-key attributes on the primary key",
                            "All columns must store binary serialized JSON objects",
                            "It must use a NoSQL key-value document store"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What does a LEFT JOIN return when a record in the left table has no matching row in the right table?",
                        "options": [
                            "The left row is completely omitted from the result set",
                            "The query throws a foreign key constraint violation error",
                            "The left row is returned with NULL values populated for all right table columns",
                            "The query halts and prompts the user to insert the missing record"
                        ],
                        "correct_index": 2
                    },
                    {
                        "id": 3,
                        "question": "In SQLite, what is the primary benefit of enabling Write-Ahead Logging (PRAGMA journal_mode=WAL)?",
                        "options": [
                            "It automatically encrypts the entire database file with AES-256",
                            "It permits multiple reading processes to read concurrently while a writing process writes changes",
                            "It compresses the database file to 10% of its original size",
                            "It replaces SQL syntax with Python dictionary lookups"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "Why does adding an index to every single column in a high-write database table harm overall performance?",
                        "options": [
                            "Indexes consume all CPU cache memory and prevent SQL queries from running",
                            "Every INSERT, UPDATE, or DELETE operation must synchronously update all associated B-tree index structures",
                            "Indexes only function properly when there are fewer than 100 rows in the table",
                            "Database connections cannot open when more than 3 indexes exist"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "Which property of ACID ensures that if any operation within a transaction fails, the entire transaction is rolled back leaving data unchanged?",
                        "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
                        "correct_index": 0
                    }
                ]
            },
            {
                "day": 5,
                "title": "Authentication, Authorization & Web Application Security",
                "subtopics": [
                    {
                        "title": "Secure Password Hashing & Salted Cryptographic Storage",
                        "brief": "Defend user credentials against credential stuffing and database dumps. Understand why plain text, MD5, and fast cryptographic hashes (SHA-256) are fundamentally unsafe for password storage due to high-speed GPU dictionary attacks. Master adaptive key-derivation functions (Argon2, bcrypt, PBKDF2). Implement salted hashing using Werkzeug/bcrypt and configure appropriate computational work factors.",
                        "takeaways": [
                            "Implement salted, slow hashing functions using generate_password_hash and check_password_hash.",
                            "Understand how unique salts defeat pre-computed rainbow table attacks.",
                            "Configure adaptive computational work factors to withstand evolving GPU brute-force hardware."
                        ],
                        "prompt_seed": "Explain why fast hash functions like SHA-256 are vulnerable to GPU brute-forcing and why memory-hard algorithms like bcrypt/Argon2 are necessary for passwords."
                    },
                    {
                        "title": "Session-Based Auth vs Stateless JWT Tokens & Cookie Security",
                        "brief": "Architect web authentication mechanisms. Compare stateful server-side sessions stored in databases/Redis against stateless JSON Web Tokens (JWT). Learn the anatomy of a JWT (Header, Payload, Signature) and token verification. Harden web cookies by configuring security flags: HttpOnly (mitigating XSS extraction), Secure (transmitting strictly over HTTPS), and SameSite=Strict/Lax (mitigating CSRF).",
                        "takeaways": [
                            "Configure hardened session cookies with HttpOnly, Secure, and SameSite attributes.",
                            "Implement signed JWT tokens with claims (sub, exp, iat) and refresh token rotation.",
                            "Choose between stateful sessions and stateless tokens based on application scale and revocation needs."
                        ],
                        "prompt_seed": "Compare session cookies and JWTs for web authentication, specifying the exact security flags required on auth cookies."
                    },
                    {
                        "title": "Defending the OWASP Top 10 (SQLi, XSS, CSRF & CSP)",
                        "brief": "Harden full-stack web applications against common web exploits. Eliminate SQL Injection (SQLi) using strictly parameterized database queries. Prevent Cross-Site Scripting (XSS) via context-aware output escaping and Content Security Policy (CSP) headers with cryptographic nonces. Defend against Cross-Site Request Forgery (CSRF) using synchronized anti-CSRF tokens. Secure file upload endpoints against directory traversal and remote code execution.",
                        "takeaways": [
                            "Eliminate SQL injection vulnerabilities by enforcing parameterized queries across all database drivers.",
                            "Deploy a strict Content Security Policy (CSP) header using dynamic nonces to block inline script injection.",
                            "Validate and sanitize user input and file uploads to prevent path traversal and execution exploits."
                        ],
                        "prompt_seed": "How does a Content Security Policy (CSP) with unique nonces stop stored and reflected XSS attacks?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the primary vulnerability of storing passwords using standard SHA-256 hashing without a salt?",
                        "options": [
                            "SHA-256 produces variable length hashes that crash databases",
                            "Attackers can instantly reverse identical passwords using precomputed rainbow tables and GPU brute-forcing",
                            "SHA-256 only works on ASCII characters",
                            "The algorithm expires after 10,000 uses"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What security protection does setting the 'HttpOnly' flag on an authentication session cookie provide?",
                        "options": [
                            "It forces the cookie to be sent only over unencrypted HTTP connections",
                            "It prevents client-side JavaScript (e.g. document.cookie) from accessing the cookie, protecting it from XSS theft",
                            "It ensures the cookie automatically deletes itself after 5 minutes",
                            "It encrypts the entire HTTP body payload with AES-128"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "Which of the following database queries is vulnerable to SQL Injection?",
                        "options": [
                            "cursor.execute('SELECT * FROM users WHERE email = ?', (user_email,))",
                            "cursor.execute(f'SELECT * FROM users WHERE email = \\'{user_email}\\'')",
                            "cursor.execute('SELECT * FROM users WHERE email = :email', {'email': user_email})",
                            "conn.execute('SELECT * FROM users WHERE id = ?', [user_id])"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What is the primary mechanism of a Cross-Site Request Forgery (CSRF) attack?",
                        "options": [
                            "An attacker reads your database password directly over the network",
                            "A malicious website tricks an authenticated user's browser into sending unauthorized requests to a trusted application",
                            "An attacker floods the server with UDP packets to knock it offline",
                            "An attacker injects malicious SQL into a search bar"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "In a modern Content Security Policy (CSP), what is the function of a 'nonce'?",
                        "options": [
                            "A static password hardcoded into the HTML head tag",
                            "A cryptographically random, single-use token generated per HTTP response that permits only authorized inline scripts to execute",
                            "An integer counter tracking the number of page views",
                            "A hash of the database connection string"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 6,
                "title": "Full-Stack Integration, State Management & Asynchronous Data Pipelines",
                "subtopics": [
                    {
                        "title": "Frontend-Backend Communication with Fetch/Axios & Error Boundaries",
                        "brief": "Bridge the gap between frontend clients and backend APIs. Build reusable API client abstractions using Fetch API or Axios with interceptors for token injection and automatic 401 redirect handling. Manage asynchronous loading states, empty collection states, and error toasts. Implement React Error Boundaries to catch unhandled JavaScript runtime exceptions and display graceful recovery interfaces.",
                        "takeaways": [
                            "Construct reusable HTTP client wrappers with request and response interceptors.",
                            "Manage loading, error, and data states cleanly in user interface components.",
                            "Isolate UI crashes using React Error Boundaries to protect user sessions."
                        ],
                        "prompt_seed": "Write a clean React data-fetching custom hook (useFetch) that handles loading, error, and cached data states."
                    },
                    {
                        "title": "Multipart Form Submissions, File Uploads & Asset Storage",
                        "brief": "Handle file uploads securely and reliably. Understand multipart/form-data encoding and boundary streams. Implement server-side validation: checking file size limits, validating allowed MIME types and file extensions, inspecting magic bytes/signatures, and generating secure random UUID filenames (preventing directory traversal attacks). Serve user-uploaded assets with proper Content-Disposition and security headers.",
                        "takeaways": [
                            "Accept and process multipart file streams safely on the web backend.",
                            "Validate file uploads using file signatures (magic bytes) rather than relying solely on file extensions.",
                            "Store uploads using randomized UUID paths to prevent filename collisions and traversal attacks."
                        ],
                        "prompt_seed": "What security vulnerabilities arise when accepting user file uploads, and how do you protect the server from directory traversal and remote code execution?"
                    },
                    {
                        "title": "Optimistic UI Updates & Real-Time State Synchronization",
                        "brief": "Deliver ultra-responsive user experiences. Implement optimistic UI patterns: immediately updating client-side state when a user triggers an action (e.g. toggling a task checkbox, liking a post), while simultaneously dispatching the asynchronous API mutation. Implement robust rollback handlers to revert UI state if the backend rejects the transaction. Explore real-time synchronization patterns via Server-Sent Events (SSE) and WebSockets.",
                        "takeaways": [
                            "Implement optimistic UI updates that provide zero-latency feedback to users.",
                            "Build rollback mechanisms that restore accurate state if backend operations fail.",
                            "Understand the trade-offs between polling, Server-Sent Events (SSE), and bidirectional WebSockets."
                        ],
                        "prompt_seed": "How does optimistic UI updating work in modern web applications, and how do you implement a rollback mechanism when a server request fails?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the primary UX advantage of implementing 'optimistic UI updates' in a web application?",
                        "options": [
                            "It eliminates the need for a backend database",
                            "The interface responds instantly to user interactions without waiting for network round-trip latency",
                            "It automatically encrypts user data before sending it over the wire",
                            "It decreases the size of bundle files generated by Vite"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "Why is checking only the file extension (e.g. .jpg) insufficient when validating user file uploads on the backend?",
                        "options": [
                            "File extensions cannot be read in Python",
                            "An attacker can rename a malicious executable script (.php, .sh, .exe) with a .jpg extension to bypass the check",
                            "Browsers automatically strip file extensions from uploads",
                            "File extensions are limited to 3 characters in modern operating systems"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "In Axios, what is the role of a 'response interceptor'?",
                        "options": [
                            "To inspect or transform responses, or globally handle HTTP error codes (like 401 Unauthorized), before .then() or .catch() execute",
                            "To compress outgoing request images into WebP format",
                            "To prevent the browser from closing during file downloads",
                            "To translate English error messages into foreign languages"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 4,
                        "question": "What HTTP encoding header is required when sending binary file data alongside text fields in an HTML form submission?",
                        "options": [
                            "application/x-www-form-urlencoded",
                            "text/plain",
                            "multipart/form-data",
                            "application/octet-stream-only"
                        ],
                        "correct_index": 2
                    },
                    {
                        "id": 5,
                        "question": "What is the primary role of a React Error Boundary?",
                        "options": [
                            "To prevent CSS layout shifts",
                            "To catch JavaScript runtime errors anywhere in its child component tree and display a fallback UI instead of crashing the whole app",
                            "To validate backend SQL schema migrations",
                            "To terminate user sessions when a network disconnects"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 7,
                "title": "Production Deployment, Linux/EC2 Infrastructure & DevOps",
                "subtopics": [
                    {
                        "title": "Linux Server Administration & AWS EC2 Instance Hardening",
                        "brief": "Deploy applications to cloud infrastructure. Navigate Linux servers over SSH. Manage system users, file permissions (chmod, chown), and isolate web app directories (/var/www/apps/). Configure firewall rules using Uncomplicated Firewall (ufw) and AWS Security Groups (exposing ports 22, 80, 443 only). Manage sensitive environment variables securely using isolated .env files with restricted permissions (chmod 600).",
                        "takeaways": [
                            "Secure and configure a cloud Ubuntu Linux server on AWS EC2.",
                            "Enforce least-privilege file permissions on web application root directories.",
                            "Configure UFW and AWS security group firewalls against port scanners and intrusion attempts."
                        ],
                        "prompt_seed": "Provide a checklist for hardening a fresh Ubuntu EC2 instance before deploying a public web service."
                    },
                    {
                        "title": "Reverse Proxying with Nginx & SSL/TLS Configuration",
                        "brief": "Configure Nginx as a high-performance reverse proxy and web server. Write robust Nginx server blocks that terminate SSL/TLS encryption, route traffic to internal application servers (http://127.0.0.1:5000), serve static files directly with gzip compression, buffer slow client requests, and enforce HTTP-to-HTTPS redirection. Obtain and automate free SSL/TLS certificates via Let's Encrypt and Certbot.",
                        "takeaways": [
                            "Write production Nginx configuration blocks for reverse proxying to Python WSGI backends.",
                            "Offload static asset delivery to Nginx to free up application worker processes.",
                            "Automate SSL/TLS certificate renewal using Certbot and Let's Encrypt."
                        ],
                        "prompt_seed": "Explain the architecture and configuration of an Nginx reverse proxy routing requests to a backend Python WSGI server."
                    },
                    {
                        "title": "Process Management with Gunicorn & Systemd Services",
                        "brief": "Run Python web applications continuously in production. Configure Gunicorn WSGI application servers: calculate worker pools based on CPU cores ((2 * CPU) + 1), handle request timeouts, and configure log file destinations. Write a Linux Systemd service unit (/etc/systemd/system/app.service) to daemonize the application, guarantee automatic restarts on failure or server reboot, and monitor health logs with journalctl.",
                        "takeaways": [
                            "Configure production Gunicorn worker processes and logging parameters.",
                            "Create and manage persistent Linux Systemd service units.",
                            "Monitor live production application logs and diagnose faults using journalctl."
                        ],
                        "prompt_seed": "Write a complete production Systemd service unit file for a Gunicorn web app, explaining ExecStart, Restart=always, and environment bindings."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the recommended rule of thumb for calculating the optimal number of Gunicorn worker processes on a dedicated server?",
                        "options": [
                            "1 worker per 1,000 users",
                            "(2 * Number of CPU Cores) + 1",
                            "Exactly 100 workers regardless of hardware",
                            "1 worker per database table"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "In production, why is Nginx placed in front of Gunicorn as a reverse proxy rather than exposing Gunicorn directly to the public internet?",
                        "options": [
                            "Nginx is required to execute Python code",
                            "Nginx efficiently handles slow clients, SSL termination, static file caching, and protects Gunicorn from connection exhaustion attacks",
                            "Gunicorn cannot bind to TCP ports",
                            "AWS EC2 blocks all traffic not originating from Nginx"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "In a Linux systemd service unit file, what does the directive 'Restart=always' ensure?",
                        "options": [
                            "The server restarts the entire operating system every 10 minutes",
                            "Systemd automatically relaunches the process if it crashes or terminates unexpectedly",
                            "The process is restarted every time a git push occurs",
                            "All database records are purged on startup"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "Which Linux command displays live, real-time log output for a systemd service named 'internship.service'?",
                        "options": [
                            "journalctl -u internship.service -f",
                            "cat /var/log/syslog --watch",
                            "systemctl status internship --tail",
                            "gunicorn --show-logs internship.service"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 5,
                        "question": "What permission setting represents 'chmod 600 .env' in Linux?",
                        "options": [
                            "Read, write, and execute permissions for everyone",
                            "Read and write permissions for the file owner only; no access for group or others",
                            "Read-only access for the entire operating system",
                            "Execute-only access for web server daemons"
                        ],
                        "correct_index": 1
                    }
                ]
            }
        ]
    }


def get_ai_agent_curriculum():
    return {
        "title": "Applied AI Agents: Production RAG, Tool Calling & Multi-Agent Orchestration",
        "slug": "ai-agent-development",
        "domain": "AI Agent Development",
        "level": "Intermediate to Advanced",
        "estimated_hours": 20,
        "banner_gradient": "linear-gradient(135deg, #8B5CF6, #6D28D9)",
        "project_brief": """
<div class="capstone-brief">
  <h2>Capstone Assignment: Autonomous Enterprise Research &amp; Intelligence Agent</h2>
  <p><strong>Goal:</strong> Architect, build, evaluate, and deploy an autonomous AI agent capable of breaking down high-level complex research goals, querying external APIs/search tools and internal vector knowledge stores, verifying facts, and compiling structured intelligence dossiers.</p>
  
  <h3>1. Core Architecture Requirements</h3>
  <ul>
    <li><strong>Agent Cognitive Architecture:</strong> ReAct (Reasoning + Acting) or Plan-and-Solve loop with dynamic task decomposition and termination conditions.</li>
    <li><strong>RAG Pipeline:</strong> Document ingestion (PDF, Markdown, HTML) with recursive chunking, dense vector embeddings (sentence-transformers / OpenAI), and high-performance vector indexing (FAISS or ChromaDB).</li>
    <li><strong>Tool Integration:</strong> At least 3 verified tools: (1) Live web search (DuckDuckGo or Tavily), (2) Vector store semantic search, and (3) Read-only SQL database querying.</li>
    <li><strong>Guardrails &amp; Safety:</strong> Strict system prompt boundaries, schema enforcement with Pydantic for structured outputs, and prompt injection defense.</li>
    <li><strong>Serving API:</strong> Async FastAPI service streaming agent thoughts and token outputs to clients via Server-Sent Events (SSE).</li>
  </ul>

  <h3>2. Functional Requirements</h3>
  <ol>
    <li><strong>Goal Ingestion &amp; Plan Generation:</strong> User provides a complex topic (e.g. 'Analyze competitor pricing and security compliance across top 3 European fintech APIs'). The agent drafts a multi-step investigation plan.</li>
    <li><strong>Autonomous Tool Execution:</strong> The agent invokes tools in sequence, analyzes tool observations, handles tool failures gracefully, and self-corrects without crashing.</li>
    <li><strong>Factual Verification &amp; Source Citations:</strong> Synthesized outputs must include verifiable inline source citations linked to source URLs or document chunk identifiers.</li>
    <li><strong>Episodic &amp; Working Memory:</strong> The agent maintains a sliding conversation context buffer while storing key factual findings in vector memory across queries.</li>
  </ol>

  <h3>3. Deliverables &amp; Evaluation Criteria</h3>
  <ul>
    <li>A public GitHub repository with comprehensive source code, modular structure, and automated unit/evaluation tests.</li>
    <li>Evaluation report using automated LLM-as-a-Judge metrics (Ragas / DeepEval) assessing Faithfulness and Answer Relevance.</li>
    <li>Live deployed API endpoint on AWS EC2 (Dockerized) with API documentation and sample curl / UI interactions.</li>
  </ul>
</div>
""",
        "days": [
            {
                "day": 1,
                "title": "LLM Architectures, Prompt Engineering & Structured Outputs",
                "subtopics": [
                    {
                        "title": "Foundation Models, Tokenomics & Inference Parameters",
                        "brief": "Deep dive into autoregressive transformer models (GPT-4, Gemini 1.5/2.0, Claude 3.5, and open-weight models like Qwen/Llama). Understand tokenization algorithms (Byte-Pair Encoding - BPE) and token-to-word ratios. Master LLM inference hyperparameters: Temperature (controlling probability entropy), Top-P (nucleus sampling), Frequency and Presence Penalties. Calculate operational cost and latency based on prompt and completion token counts.",
                        "takeaways": [
                            "Calculate token usage and API operational costs across frontier foundation models.",
                            "Tune temperature and top_p hyperparameters for deterministic extraction vs creative reasoning.",
                            "Manage context window limits and avoid prompt truncation errors."
                        ],
                        "prompt_seed": "How does temperature and top_p sampling mathematically alter the next-token probability distribution in an autoregressive LLM?"
                    },
                    {
                        "title": "Production Prompt Engineering & In-Context Learning",
                        "brief": "Move from ad-hoc prompting to robust prompt engineering. Master structural role formatting (System, User, Assistant). Implement Chain-of-Thought (CoT) reasoning to force models to 'think' step-by-step before answering. Construct Few-Shot exemplars to anchor output formatting and domain nuance. Implement prompt injection defenses: isolating untrusted user text inside XML/Markdown tags and instructing models to ignore embedded instructions.",
                        "takeaways": [
                            "Formulate Chain-of-Thought prompts that dramatically boost complex mathematical and reasoning accuracy.",
                            "Design few-shot demonstration exemplars that eliminate ambiguous formatting.",
                            "Harden system prompts against prompt injection and jailbreak exploits."
                        ],
                        "prompt_seed": "Write a robust system prompt with few-shot exemplars that extracts named entities and dates from unstructured email text without hallucination."
                    },
                    {
                        "title": "Structured Outputs & Schema Enforcement with Pydantic",
                        "brief": "Eliminate brittle regex parsing and hallucinated syntax. Force LLMs to generate 100% valid, type-safe JSON adhering strictly to JSON Schema definitions using native Structured Outputs (OpenAI, Gemini) and Pydantic models. Validate field types, optionality, string patterns, and value ranges. Build self-healing schema retry wrappers that pass validation error traces back to the model upon parsing failure.",
                        "takeaways": [
                            "Enforce strict JSON schema compliance using Pydantic data models.",
                            "Guarantee type-safe output ingestion directly into application databases and APIs.",
                            "Implement automated error-feedback retry loops for malformed schema payloads."
                        ],
                        "prompt_seed": "Demonstrate how to use Pydantic models with an LLM function calling API to extract strongly typed customer order data."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the mathematical effect of setting an LLM's 'temperature' parameter to 0.0 during text generation?",
                        "options": [
                            "The model stops generating text completely",
                            "The model behaves deterministically by greedily selecting the token with the highest log-probability at each step",
                            "The model samples uniformly at random across its entire vocabulary",
                            "The context window size is reduced by half"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "Why is Chain-of-Thought (CoT) prompting effective at solving multi-step mathematical or reasoning problems?",
                        "options": [
                            "It compiles the prompt into native C++ code",
                            "It grants the model additional compute and token steps to derive intermediate states before committing to a final answer",
                            "It bypasses the LLM's token rate limiter",
                            "It forces the model to search Google in the background"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "What distinguishes native LLM 'Structured Outputs' from naive prompt instructions like 'Respond in JSON'?",
                        "options": [
                            "Structured Outputs use grammar-constrained sampling at decoding time to mathematically guarantee schema adherence",
                            "Structured Outputs take 10x longer to generate tokens",
                            "Structured Outputs cannot validate string lengths or numbers",
                            "Structured Outputs work only with XML and not JSON"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 4,
                        "question": "What is the primary objective of an indirect prompt injection attack?",
                        "options": [
                            "To overheat the server GPU hardware",
                            "To embed malicious instructions within third-party data (like web pages or emails) that hijack the LLM's execution flow",
                            "To steal SSL certificates directly from the hosting Linux kernel",
                            "To force the model to decrease its context window"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "In tokenomics, approximately how many English words does a typical prompt containing 1,000 tokens represent?",
                        "options": ["100 words", "750 words", "3,000 words", "10,000 words"],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 2,
                "title": "Vector Embeddings, Semantic Search & Vector Database Architecture",
                "subtopics": [
                    {
                        "title": "Dense Embeddings & Vector Similarity Mathematics",
                        "brief": "Explore the mathematics of vector embeddings. Contrast sparse keyword vectors (TF-IDF, BM25) with dense semantic embeddings (OpenAI text-embedding-3, HuggingFace sentence-transformers). Understand how transformer encoders map textual semantics into high-dimensional geometric spaces (384 to 3072 dimensions). Calculate geometric distance metrics: Cosine Similarity, Dot Product, and Euclidean (L2) distance, and understand when each metric is appropriate.",
                        "takeaways": [
                            "Understand the mathematical principles governing dense vector embeddings.",
                            "Select appropriate distance metrics (Cosine vs L2) based on vector normalization.",
                            "Evaluate embedding models based on benchmark performance (MTEB) and latency."
                        ],
                        "prompt_seed": "Explain the geometric and mathematical differences between Cosine Similarity and Euclidean Distance when comparing normalized text embeddings."
                    },
                    {
                        "title": "Vector Databases & High-Performance Indexing (FAISS & Chroma)",
                        "brief": "Examine the architecture of dedicated vector storage engines: FAISS (Facebook AI Similarity Search), ChromaDB, Qdrant, and pgvector. Understand why exact k-Nearest Neighbors (k-NN) fails at scale. Dive into Approximate Nearest Neighbor (ANN) indexing structures: Inverted File Indexing (IVF) and Hierarchical Navigable Small World (HNSW) graphs. Benchmark trade-offs between search latency, index build time, and recall precision.",
                        "takeaways": [
                            "Build, persist, and query in-memory and disk-backed vector indexes with FAISS and ChromaDB.",
                            "Tune HNSW index parameters (M, efConstruction, efSearch) for optimal search speed and recall.",
                            "Persist and reload serialized vector index artifacts efficiently in production."
                        ],
                        "prompt_seed": "How does the HNSW (Hierarchical Navigable Small World) algorithm enable sub-linear search time across millions of high-dimensional vectors?"
                    },
                    {
                        "title": "Document Ingestion, Chunking Strategies & Metadata Tagging",
                        "brief": "Build the document ingestion pipeline. Extract raw text from diverse formats: PDFs (using pdfplumber and PyPDF2), Markdown, and HTML. Compare text chunking strategies: naive fixed-character chunking, recursive character chunking based on semantic boundaries (paragraphs, sentences), and document-structure chunking. Configure chunk overlap to preserve context across boundaries and attach rich metadata (source, page number, timestamp) for filtered retrieval.",
                        "takeaways": [
                            "Extract clean, tabular, and textual content from unstructured PDF documents.",
                            "Implement recursive character chunking that preserves semantic paragraph coherence.",
                            "Attach structured metadata to chunks to enable hybrid metadata-filtered vector queries."
                        ],
                        "prompt_seed": "Compare fixed-size chunking with recursive character chunking for technical PDF manuals containing tables and code blocks."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "Why does cosine similarity between two normalized vectors equal their dot product?",
                        "options": [
                            "Because normalized vectors have a magnitude (length) of exactly 1.0, simplifying the denominator to 1",
                            "Because cosine similarity is an obsolete metric that ignores vector direction",
                            "Because dot products are only calculated in 2-dimensional space",
                            "Because normalized vectors contain only positive integers"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 2,
                        "question": "What is the primary advantage of Approximate Nearest Neighbor (ANN) search algorithms like HNSW over exact flat k-NN search?",
                        "options": [
                            "ANN guarantees 100% mathematical recall accuracy across infinite datasets",
                            "ANN achieves sub-linear search latency (O(log N)) by navigating graph structures instead of comparing against every vector (O(N))",
                            "ANN eliminates the need for vector embeddings entirely",
                            "ANN compresses vectors into raw ASCII text"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "Why is chunk overlap (e.g. 50-100 characters) critical when splitting documents into smaller chunks for RAG?",
                        "options": [
                            "To make the vector database file as large as possible",
                            "To prevent loss of contextual meaning and split phrases that fall precisely across chunk boundaries",
                            "To trick the LLM into thinking it read multiple different documents",
                            "To ensure chunks always contain an even number of tokens"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What is the primary function of metadata filtering in a vector database query?",
                        "options": [
                            "To re-write the user's natural language question into SQL",
                            "To restrict the vector search space strictly to documents matching specific criteria (e.g. user_id, date, source) before or after similarity calculation",
                            "To delete outdated vector embeddings automatically",
                            "To translate vectors from one language to another"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "What does MTEB stand for in the context of evaluating vector embedding models?",
                        "options": [
                            "Massive Text Embedding Benchmark",
                            "Modern Transformer Evaluation Binary",
                            "Multi-Token Execution Budget",
                            "Modular Text Extraction Backend"
                        ],
                        "correct_index": 0
                    }
                ]
            },
            {
                "day": 3,
                "title": "Production Retrieval-Augmented Generation (RAG) Pipelines",
                "subtopics": [
                    {
                        "title": "Standard RAG vs Production RAG Architecture",
                        "brief": "Diagnose the core failure modes of basic naive RAG: irrelevant retrieval, context fragmentation, hallucination despite retrieval, and context dilution ('lost in the middle'). Architect end-to-end production RAG pipelines featuring query pre-processing, multi-vector indexing, contextual compression, and strict hallucination guardrails in the synthesis prompt.",
                        "takeaways": [
                            "Identify and diagnose common failure modes in basic retrieval-augmented generation.",
                            "Design grounding system prompts that prevent hallucinated extrapolation.",
                            "Structure modular RAG pipelines with clear retrieval, ranking, and synthesis boundaries."
                        ],
                        "prompt_seed": "What is the 'lost in the middle' phenomenon in large language models, and how does it impact retrieval-augmented generation?"
                    },
                    {
                        "title": "Query Transformation, Hybrid Search & Re-Ranking",
                        "brief": "Maximize retrieval precision. Implement query transformation techniques: Sub-Question Decomposition (breaking complex queries into distinct sub-queries) and Hypothetical Document Embeddings (HyDE). Combine dense semantic vector search with sparse keyword search (BM25) using Reciprocal Rank Fusion (RRF). Apply Cross-Encoder re-rankers (Cohere Re-rank, BGE-Reranker) to score document-query relevance with full self-attention.",
                        "takeaways": [
                            "Implement HyDE to retrieve relevant documents when user queries are terse or abstract.",
                            "Merge keyword search and vector search using Reciprocal Rank Fusion (RRF).",
                            "Filter out false-positive chunks by applying Cross-Encoder re-ranking models."
                        ],
                        "prompt_seed": "Explain how Reciprocal Rank Fusion (RRF) merges keyword search results (BM25) and semantic vector search results into a unified ranking."
                    },
                    {
                        "title": "Contextual Compression & Source Citation Synthesis",
                        "brief": "Optimize context window efficiency and auditable accuracy. Implement contextual compression to extract only the specific sentences relevant to the query from long retrieved chunks. Prompt the LLM to generate strict inline citations referencing specific document identifiers and page numbers. Build post-generation citation verification modules that verify every claimed quote exists verbatim in retrieved sources.",
                        "takeaways": [
                            "Compress retrieved context chunks to minimize prompt token bloat and inference latency.",
                            "Synthesize professional responses featuring verified inline citations.",
                            "Implement programmatic checks that audit LLM citations against ground-truth context chunks."
                        ],
                        "prompt_seed": "Design a prompt and post-processing pipeline that requires an LLM to cite specific source chunk IDs for every factual assertion made."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the 'Lost in the Middle' phenomenon observed in transformer LLMs during RAG synthesis?",
                        "options": [
                            "Models delete tokens in the middle of long words",
                            "Models show higher recall for information located at the very beginning or end of their input context, frequently ignoring relevant data placed in the middle",
                            "Vector databases lose 50% of embeddings during indexing",
                            "The middle layer of neural networks experiences zero gradient flow"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "How does Hypothetical Document Embeddings (HyDE) improve search retrieval?",
                        "options": [
                            "It generates a hypothetical answer to the question using an LLM, then uses that answer's embedding to search the vector space for real documents",
                            "It deletes hypothetical questions from the database",
                            "It encrypts document chunks with random salts",
                            "It forces the user to provide their own document embeddings"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 3,
                        "question": "What is the key structural difference between a Bi-Encoder (standard embedding model) and a Cross-Encoder (re-ranker)?",
                        "options": [
                            "Bi-encoders cannot process English text",
                            "Bi-encoders embed query and document independently into vectors; Cross-encoders process query and document simultaneously through all attention layers",
                            "Cross-encoders are 100x faster than Bi-encoders",
                            "Bi-encoders require GPU clusters while Cross-encoders run on calculators"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "In Reciprocal Rank Fusion (RRF), what does the formula RRF_Score = SUM(1 / (k + rank)) achieve?",
                        "options": [
                            "It calculates the exact cosine similarity between two documents",
                            "It combines rankings from multiple disparate search algorithms (e.g. BM25 and vector search) without requiring score normalization",
                            "It deletes duplicate records from a relational database table",
                            "It calculates token latency in seconds"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "What is the primary benefit of Contextual Compression in RAG pipelines?",
                        "options": [
                            "It compresses prompt context to reduce token costs, lower latency, and eliminate distracting irrelevant text",
                            "It converts text into zip files on disk",
                            "It replaces all vowels with asterisks",
                            "It forces the LLM to output 5-word summaries only"
                        ],
                        "correct_index": 0
                    }
                ]
            },
            {
                "day": 4,
                "title": "Tool Calling, Function Execution & Sandboxed Environments",
                "subtopics": [
                    {
                        "title": "Function Calling Protocols & Tool Declaration Schemas",
                        "brief": "Turn passive LLMs into active agents. Master the function calling protocol (OpenAI, Gemini). Define tool declarations using standard JSON Schema (tool name, description, parameter types, enums, required fields). Understand how the model decides when to return a standard text completion versus a structured tool call request. Parse tool call arguments, execute native code, and format tool results into tool-role messages.",
                        "takeaways": [
                            "Write clean, descriptive JSON Schema declarations for custom Python functions.",
                            "Handle LLM tool call payloads, argument parsing, and tool execution lifecycles.",
                            "Format tool observations correctly back into conversation context to resume generation."
                        ],
                        "prompt_seed": "Write an end-to-end Python script demonstrating an LLM invoking a custom get_weather(city, units) function call."
                    },
                    {
                        "title": "Building External Tool Integrations (Search, SQL & APIs)",
                        "brief": "Equip agents with real-world utility. Build production-grade tool integrations: live web search (DuckDuckGo, Tavily), read-only SQL query execution with automatic schema introspection, and external REST API consumers. Enforce strict safety guardrails on database tools: enforcing SELECT statements only, read-only database connections, statement execution timeouts, and result set row limits to protect server memory.",
                        "takeaways": [
                            "Integrate live internet search capabilities into autonomous agent loops.",
                            "Safely equip agents with read-only SQL querying tools with strict execution constraints.",
                            "Build robust API client tools that handle pagination and rate limits."
                        ],
                        "prompt_seed": "How do you design a database query tool for an AI agent that prevents destructive SQL operations (DROP, DELETE, UPDATE) while allowing analytical exploration?"
                    },
                    {
                        "title": "Error Recovery, Hallucinated Tool Handling & Sandboxing",
                        "brief": "Build resilient tool execution engines. Handle common real-world failures: models calling nonexistent functions, passing invalid arguments that fail Pydantic validation, or tools throwing network exceptions. Instead of crashing, capture exception tracebacks, format them into helpful natural language error messages, and feed them back to the agent so it can self-correct. Sandbox arbitrary code execution tools in isolated environments.",
                        "takeaways": [
                            "Implement self-healing tool execution wrappers that intercept exceptions and prompt the agent to self-correct.",
                            "Validate tool call arguments with Pydantic before invocation to block bad inputs.",
                            "Isolate untrusted code execution inside restricted containerized or subprocess sandboxes."
                        ],
                        "prompt_seed": "Explain the reflection loop where an agent encounters a Python execution error, analyzes the traceback, and corrects its code autonomously."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "In the OpenAI/Gemini function calling protocol, what actually executes the underlying Python tool code?",
                        "options": [
                            "The LLM neural network executes the Python code internally in its attention weights",
                            "The client application/server hosting the code receives the tool call schema from the model, executes the function locally, and returns the result",
                            "The cloud GPU cluster running the LLM executes the code in a remote sandbox",
                            "A browser extension running on the user's laptop"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What is the most effective defense against an AI agent executing destructive SQL queries (e.g. DROP TABLE) when given database querying tools?",
                        "options": [
                            "Asking the LLM politely in the system prompt to only run safe queries",
                            "Connecting the tool using a database user granted strictly read-only permissions (SELECT only) at the database engine level",
                            "Changing the database file extension from .db to .txt",
                            "Limiting user prompts to 10 words"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "Why is the 'description' field in a tool's JSON Schema declaration critical to agent performance?",
                        "options": [
                            "It is printed in the terminal console when the script boots",
                            "The LLM reads the description to determine what the tool does and decide whether calling it will help answer the user's request",
                            "It is used by the database to index the tool's source code",
                            "It sets the timeout duration of the function"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "When an agent passes invalid arguments to a tool, what is the best architectural recovery strategy?",
                        "options": [
                            "Immediately crash the entire backend service with an unhandled exception",
                            "Intercept the validation error and return a detailed error message as the tool's observation, allowing the model to correct its call",
                            "Guess random argument values and rerun the tool silently",
                            "Delete the conversation history and start from scratch"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "What is the primary risk of allowing an AI agent to execute arbitrary Python code via a native eval() or exec() tool without sandboxing?",
                        "options": [
                            "The script might print duplicate messages",
                            "An attacker could manipulate the agent via prompt injection to delete files, execute malicious shell commands, or exfiltrate private credentials",
                            "The agent might change the Python version installed on the computer",
                            "eval() only works on floating point numbers"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 5,
                "title": "Autonomous Agent Architectures: ReAct & Plan-and-Solve",
                "subtopics": [
                    {
                        "title": "The ReAct Framework (Reasoning + Acting)",
                        "brief": "Implement the classic autonomous agent pattern: ReAct. Explore the cognitive loop: Thought (verbal reasoning over current state) -> Action (selecting a tool) -> Action Input (providing tool parameters) -> Observation (ingesting tool output) -> Reflection -> Final Answer. Build a clean, dependency-free ReAct execution engine in pure Python. Enforce iteration limits to prevent infinite execution loops and runaway API costs.",
                        "takeaways": [
                            "Build a pure Python ReAct agent execution loop from scratch.",
                            "Parse reasoning thoughts and tool actions using robust string and schema parsers.",
                            "Implement iteration counters and cost guardrails to terminate runaway loops."
                        ],
                        "prompt_seed": "Provide a pure Python implementation of a ReAct agent loop that parses thoughts, executes tools, and stops when a final answer is reached."
                    },
                    {
                        "title": "Plan-and-Solve Prompting & Task Decomposition",
                        "brief": "Overcome myopic decision-making in complex multi-step objectives. Understand why step-by-step reaction often wanders off-track. Implement the Plan-and-Solve architecture: (1) Planner Agent decomposes a complex objective into an explicit list of sub-tasks, (2) Executor Agent iterates through the plan executing actions, (3) Re-planner updates remaining tasks based on intermediate findings. Contrast linear execution with tree-of-thought exploration.",
                        "takeaways": [
                            "Implement separate Planner and Executor cognitive roles for complex problem solving.",
                            "Decompose ambiguous high-level goals into ordered, testable sub-tasks.",
                            "Enable dynamic re-planning when intermediate tool executions produce unexpected data."
                        ],
                        "prompt_seed": "Contrast the ReAct pattern with the Plan-and-Solve pattern, specifying scenarios where planning ahead outperforms step-by-step reaction."
                    },
                    {
                        "title": "Agent Memory Architectures: Short-Term, Long-Term & Episodic",
                        "brief": "Endow agents with stateful persistence. Architect multi-tiered memory systems: Working Memory (current execution stack and tool observations), Short-Term Conversational Memory (sliding context buffers with automated LLM summarization of older dialogue turns), and Long-Term Episodic Memory (persisting past goals, user preferences, and solutions in vector databases for semantic retrieval across sessions).",
                        "takeaways": [
                            "Maintain multi-turn conversation memory without exceeding token context limits.",
                            "Implement automated conversation summarizers that compress historical dialogue.",
                            "Store and retrieve past agent experiences and user profiles using episodic vector memory."
                        ],
                        "prompt_seed": "How do you design an episodic memory system for an agent so it remembers user preferences and past project outcomes across weeks of interactions?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "In the ReAct agent framework, what is the specific purpose of the 'Thought' step before each 'Action'?",
                        "options": [
                            "It logs an error message to the system kernel",
                            "It forces the model to articulate verbal reasoning over previous observations and deliberate on which tool to invoke next",
                            "It renders the visual user interface in HTML",
                            "It charges the user's credit card"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What is the primary advantage of the Plan-and-Solve agent architecture over a basic ReAct loop for complex research tasks?",
                        "options": [
                            "Plan-and-Solve requires zero tokens to run",
                            "It decomposes the broad goal into an overarching roadmap first, avoiding myopic local decisions and looping behaviors",
                            "It eliminates the need for tool execution",
                            "It can only be used with local open-source models"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "Why is an iteration limit (e.g. max_steps = 10) essential in any autonomous agent execution loop?",
                        "options": [
                            "To comply with international Python programming laws",
                            "To prevent infinite loops from draining API token budgets and locking up server compute indefinitely",
                            "Because Python cannot count higher than 10",
                            "To ensure all answers contain exactly 10 words"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "How does a Conversation Summary Memory buffer maintain long dialogues within fixed context windows?",
                        "options": [
                            "It deletes all vowels from user messages",
                            "It progressively condenses older conversation turns into a running semantic summary while preserving recent messages verbatim",
                            "It stores messages on floppy disks",
                            "It forces the user to re-type their initial question"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "What is 'Episodic Memory' in an autonomous agent system?",
                        "options": [
                            "The RAM currently in use by the operating system",
                            "A persistent memory store (often in a vector DB) that preserves past experiences, task outcomes, and user preferences across multiple sessions",
                            "A memory that resets every 5 minutes",
                            "Memory dedicated solely to playing video clips"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 6,
                "title": "Multi-Agent Orchestration, State Graphs & Governance",
                "subtopics": [
                    {
                        "title": "Multi-Agent Collaboration Patterns",
                        "brief": "Scale single agents into specialized agent teams. Explore collaboration topologies: Supervisor-Worker (central router agent delegates subtasks to specialized researcher, writer, and coder agents), Sequential Handoff (assembly line pipeline), and Multi-Agent Debate (opposing agents critique and refine outputs to minimize hallucination). Define explicit agent communication schemas and data contracts.",
                        "takeaways": [
                            "Architect hierarchical Supervisor-Worker multi-agent teams.",
                            "Implement agent debate protocols that cross-examine findings before final delivery.",
                            "Design clear JSON data handoff contracts between specialized agents."
                        ],
                        "prompt_seed": "Diagram and explain a multi-agent software engineering team where a Product Manager agent, Developer agent, and QA agent collaborate to write code."
                    },
                    {
                        "title": "Stateful Agent Graphs with LangGraph / Finite State Machines",
                        "brief": "Tame non-deterministic LLMs with deterministic execution graphs. Model agent workflows as stateful graphs: State schemas (shared TypedDict context), Nodes (agent actions or tool invocations), and Conditional Edges (routing logic based on output evaluation). Implement cyclic loops (e.g. Code -> Test -> Fail -> Re-code -> Test -> Pass). Incorporate Human-in-the-Loop checkpoints to gate sensitive actions (e.g. sending emails or issuing payments).",
                        "takeaways": [
                            "Build deterministic cyclic state graphs with conditional routing logic.",
                            "Implement automated evaluation loops that iterate until quality criteria are met.",
                            "Integrate human-in-the-loop approval gates for mission-critical agent actions."
                        ],
                        "prompt_seed": "Explain how cycles and conditional edges in state graphs allow agents to iterate on code until automated unit tests pass."
                    },
                    {
                        "title": "Safety Guardrails, Content Moderation & Cost Governance",
                        "brief": "Deploy AI agents safely in enterprise settings. Implement multi-layered guardrails (NeMo Guardrails, Llama Guard): PII redaction (masking credit cards, phone numbers, emails), topic boundary enforcement (preventing agents from answering off-topic queries), and hallucination checks. Implement operational cost governance: tracking token expenditures per user, per-session rate limits, and hard budget circuit breakers.",
                        "takeaways": [
                            "Redact Personally Identifiable Information (PII) before passing text to cloud LLM APIs.",
                            "Implement dual-layer guardrails checking both inbound prompts and outbound answers.",
                            "Enforce token quotas and circuit breakers to prevent runaway billing spikes."
                        ],
                        "prompt_seed": "How do you implement a dual-layer guardrail that checks for PII leakage in user prompts and verifies factual consistency in model outputs?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "In a Supervisor-Worker multi-agent pattern, what is the primary role of the Supervisor agent?",
                        "options": [
                            "To execute all low-level code directly",
                            "To analyze the user request, break it down, route subtasks to specialized worker agents, and synthesize the final result",
                            "To monitor CPU hardware temperature",
                            "To act as a database backup service"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What is the key advantage of modeling an agentic workflow as a state graph (like LangGraph) rather than an unconstrained while-loop?",
                        "options": [
                            "State graphs allow deterministic control flow, explicit state schemas, conditional branching, and checkpointing",
                            "State graphs run without needing an internet connection",
                            "State graphs eliminate the need for API keys",
                            "State graphs convert Python code into assembly language"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 3,
                        "question": "What is a 'Human-in-the-Loop' (HITL) checkpoint in an agentic workflow?",
                        "options": [
                            "A requirement that a human manually types all LLM tokens",
                            "A designated state graph interrupt where execution pauses until a human operator approves, edits, or rejects a sensitive action",
                            "A captcha test shown to the LLM to verify it is human",
                            "A physical button on the EC2 server chassis"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What is the primary function of a PII redaction guardrail in enterprise AI deployments?",
                        "options": [
                            "To replace all numbers with emojis",
                            "To detect and mask sensitive user data (passwords, Aadhaar/SSN, payment cards) before prompts reach external cloud APIs",
                            "To increase the cost of API inference",
                            "To translate sensitive documents into Latin"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "In cost governance, what is an 'API circuit breaker'?",
                        "options": [
                            "A physical fuse in the datacenter electrical panel",
                            "An automated programmatic monitor that halts further LLM requests if a predefined monetary or token threshold is exceeded",
                            "A tool that breaks long words into syllables",
                            "A router that alternates between WiFi and Ethernet"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 7,
                "title": "Production Deployment, Observability & Evaluation of AI Agents",
                "subtopics": [
                    {
                        "title": "Automated Evaluation & LLM-as-a-Judge Frameworks",
                        "brief": "Establish rigorous quality benchmarks for stochastic AI agents. Move beyond manual inspection. Implement automated evaluation frameworks (Ragas, DeepEval). Master core quantitative metrics: Faithfulness (hallucination detection against retrieved context), Answer Relevance, Context Precision, and Tool Calling Accuracy. Set up automated regression test suites that run in CI/CD before deploying agent updates.",
                        "takeaways": [
                            "Evaluate RAG and agent systems quantitatively using Ragas and DeepEval metrics.",
                            "Implement LLM-as-a-Judge evaluation prompts with calibrated scoring rubrics.",
                            "Establish automated regression gates in CI/CD to prevent quality degradation across prompt updates."
                        ],
                        "prompt_seed": "Write an evaluation rubric and prompt for an LLM judge to grade the faithfulness and citation accuracy of an agent's answer against retrieved sources."
                    },
                    {
                        "title": "Observability, Tracing & Latency Optimization",
                        "brief": "Monitor multi-step agent reasoning in production. Instrument agent applications with distributed tracing (LangSmith, Phoenix/Arize, OpenTelemetry). Trace execution spans across nested tool calls, retrievals, and LLM calls. Measure token throughput and Time-to-First-Token (TTFT). Implement semantic caching (GPTCache, Redis) to serve instantaneous answers to recurring semantic queries, slashing API latency and cost.",
                        "takeaways": [
                            "Instrument production agent pipelines with full distributed execution traces.",
                            "Diagnose latency bottlenecks across vector retrieval, external tools, and model generation.",
                            "Deploy semantic caching to serve instant responses for semantically similar user queries."
                        ],
                        "prompt_seed": "What metrics are critical for monitoring an agent in production, and how does semantic caching reduce both API costs and latency?"
                    },
                    {
                        "title": "Serving Agentic APIs with FastAPI & Dockerized EC2 Deployment",
                        "brief": "Package and deploy autonomous agent applications. Build high-performance asynchronous web APIs using FastAPI. Implement Server-Sent Events (SSE) to stream real-time reasoning steps, tool execution statuses, and generated answer tokens to web clients. Containerize the application using Docker, secure API keys in production .env files, and deploy behind an Nginx reverse proxy on an AWS EC2 instance.",
                        "takeaways": [
                            "Build asynchronous FastAPI endpoints streaming agent thoughts and tokens via Server-Sent Events.",
                            "Containerize agent microservices with Docker for reproducible production deployment.",
                            "Deploy containerized AI agent APIs on AWS EC2 behind an Nginx reverse proxy."
                        ],
                        "prompt_seed": "Write a complete FastAPI route that streams agent execution steps and token output to a client using Server-Sent Events (SSE)."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "In RAG evaluation with frameworks like Ragas, what does the 'Faithfulness' metric measure?",
                        "options": [
                            "How quickly the model responds to queries in milliseconds",
                            "The proportion of claims in the generated answer that can be directly inferred from the retrieved context, penalizing hallucinations",
                            "Whether the user trusts the brand providing the service",
                            "How closely the output matches a standard dictionary definition"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What is the primary benefit of streaming agent progress to frontend users via Server-Sent Events (SSE)?",
                        "options": [
                            "It eliminates the need for an SSL certificate",
                            "It provides immediate visual feedback (showing intermediate thoughts and tokens) so users don't face a blank screen during long reasoning loops",
                            "It compresses video files faster than WebSockets",
                            "It allows the client to edit the backend database directly"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "How does 'Semantic Caching' differ from traditional HTTP key-value caching for LLM applications?",
                        "options": [
                            "Traditional caching matches exact string keys; semantic caching compares vector embeddings to return cached answers for semantically equivalent questions",
                            "Semantic caching only works on mobile devices",
                            "Traditional caching requires GPU hardware",
                            "Semantic caching deletes data every 60 seconds"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 4,
                        "question": "What does Time-to-First-Token (TTFT) measure in an LLM API service?",
                        "options": [
                            "The total time required to train the foundation model from scratch",
                            "The elapsed time between the client sending a request and receiving the very first token of the response stream",
                            "The time taken to save a prompt to an SQLite database",
                            "The duration of an SSL handshake"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "In distributed tracing for AI agents, what is a 'Span'?",
                        "options": [
                            "The total distance between the client laptop and the server",
                            "A single timed unit of work representing an individual operation (such as an LLM call, a tool execution, or a vector retrieval) within a trace tree",
                            "A memory leak in a Python script",
                            "The total character count of a system prompt"
                        ],
                        "correct_index": 1
                    }
                ]
            }
        ]
    }


def get_python_automation_curriculum():
    return {
        "title": "Python Automation & Web Scraping: Production Pipelines & Cloud Daemons",
        "slug": "python-automation-engineering",
        "domain": "Python Automation",
        "level": "Beginner to Intermediate",
        "estimated_hours": 16,
        "banner_gradient": "linear-gradient(135deg, #10B981, #047857)",
        "project_brief": """
<div class="capstone-brief">
  <h2>Capstone Assignment: Production Competitor Price &amp; Stock Intelligence Pipeline</h2>
  <p><strong>Goal:</strong> Engineer, automate, harden, and deploy an end-to-end autonomous competitor price and inventory monitoring daemon running 24/7 on an AWS EC2 instance.</p>
  
  <h3>1. Core Architecture Requirements</h3>
  <ul>
    <li><strong>Data Extraction:</strong> Resilient multi-target scraping engine utilizing <code>requests.Session</code> with backoff retries and headless browser automation (Playwright/Selenium) for JavaScript-rendered catalogs.</li>
    <li><strong>Data Pipeline &amp; Storage:</strong> Relational historical tracking in SQLite with Write-Ahead Logging (WAL) mode or PostgreSQL, storing product SKUs, historical prices, stock status, and timestamps.</li>
    <li><strong>Spreadsheet Reporting:</strong> Automated generation of professional multi-sheet Excel reports (<code>.xlsx</code>) using <code>openpyxl</code>, featuring summary KPI metrics, formulas (<code>AVERAGE</code>, <code>MIN</code>, <code>MAX</code>), and conditional formatting.</li>
    <li><strong>Multi-Channel Alerting:</strong> Real-time trigger notifications: HTML email via SMTP/cPanel API and webhook broadcasts (Slack, Discord, or Telegram) when a price drops >10% or items enter/exit stock.</li>
    <li><strong>Operational Hardening:</strong> Single-instance execution locking (preventing overlapping runs), structured rotating file logging, and autonomous Systemd daemonization on Linux.</li>
  </ul>

  <h3>2. Functional Requirements</h3>
  <ol>
    <li><strong>Autonomous Execution:</strong> The daemon executes automatically on an hourly or daily schedule without human intervention.</li>
    <li><strong>Self-Healing Error Isolation:</strong> Network dropouts or target site layout changes on one product do not crash the pipeline; failures are logged to an error dead-letter table.</li>
    <li><strong>Audit Logging:</strong> All execution passes, HTTP response codes, and item count deltas are recorded in rotating log files.</li>
    <li><strong>Executive Delivery:</strong> Generates and delivers the Excel report as an email attachment with a summary KPI dashboard in the email body.</li>
  </ol>

  <h3>3. Deliverables &amp; Evaluation Criteria</h3>
  <ul>
    <li>A public GitHub repository containing clean, documented Python automation code adhering to PEP 8 standards.</li>
    <li>Comprehensive <code>README.md</code> with system architecture diagram, configuration guide, and sample output artifacts.</li>
    <li>Active Systemd unit service configuration running live on an AWS EC2 instance with proof of automated alert delivery.</li>
  </ul>
</div>
""",
        "days": [
            {
                "day": 1,
                "title": "Modern Python Scripting, File I/O & OS-Level Automation",
                "subtopics": [
                    {
                        "title": "Pathlib, Cross-Platform File Systems & Directory Walks",
                        "brief": "Upgrade your filesystem automation skills. Replace legacy, fragile os.path string concatenations with object-oriented pathlib.Path. Navigate directory structures safely across Windows and Linux. Perform recursive file discovery with rglob(), batch file renaming, and extract file metadata (size, created/modified timestamps). Build automated file tidying scripts that organize chaotic directories by file extension and date stamps.",
                        "takeaways": [
                            "Write cross-platform filesystem scripts using object-oriented pathlib.Path.",
                            "Execute recursive directory walks and batch file operations with rglob().",
                            "Inspect and filter files based on system timestamps and byte sizes."
                        ],
                        "prompt_seed": "Write a Python script using pathlib that recursively organizes an unorganized downloads folder into categorized subfolders by file extension and creation date."
                    },
                    {
                        "title": "Structured Data Parsing: JSON, CSV, YAML & Config Management",
                        "brief": "Parse and manipulate diverse structured data feeds. Ingest and serialize nested JSON objects with proper encoding handling. Stream multi-gigabyte CSV transaction exports row-by-row using csv.DictReader to prevent server memory exhaustion. Parse YAML configuration files for automation settings, and isolate sensitive credentials using python-dotenv with strictly scoped environment variables.",
                        "takeaways": [
                            "Stream large CSV files without memory bloat using csv.DictReader.",
                            "Safely parse and format nested JSON and YAML configuration files.",
                            "Secure automation secrets using environment variables and python-dotenv."
                        ],
                        "prompt_seed": "How do you process a 5GB CSV transaction export in Python without exceeding a 512MB RAM server limit?"
                    },
                    {
                        "title": "Subprocess Management & Shell Command Orchestration",
                        "brief": "Command operating system utilities directly from Python. Use subprocess.run and subprocess.Popen safely: capture stdout and stderr streams, enforce non-zero exit code validation (check=True), and set execution timeouts to prevent hung processes from blocking servers. Eliminate critical shell injection vulnerabilities by passing command arguments as safe argument lists rather than raw strings with shell=True.",
                        "takeaways": [
                            "Orchestrate external CLI tools and shell utilities safely from Python scripts.",
                            "Capture and parse standard output and error streams programmatically.",
                            "Prevent shell injection vulnerabilities by avoiding unsanitized shell=True calls."
                        ],
                        "prompt_seed": "Contrast subprocess.run(shell=True) with subprocess.run(shell=False) and explain why passing unsanitized user inputs to shell=True is catastrophic."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the primary architectural advantage of using 'csv.DictReader' over 'csv.reader' when parsing enterprise CSV files?",
                        "options": [
                            "It automatically compresses the CSV file into a zip archive",
                            "It maps each row to a dictionary using header names as keys, preventing bugs when column orders change",
                            "It loads all rows into GPU memory at once",
                            "It translates text into French"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "In Python's pathlib module, what method recursively matches all files ending in '.log' across all nested subdirectories?",
                        "options": [
                            "Path.glob('*.log')",
                            "Path.rglob('*.log')",
                            "Path.find_all('*.log')",
                            "Path.scan_dir('.log')"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "Why is 'subprocess.run(..., shell=True)' considered dangerous when incorporating user-provided input?",
                        "options": [
                            "It runs 100x slower than shell=False",
                            "It passes input directly to the system shell interpreter, exposing the machine to arbitrary command injection exploits",
                            "It automatically deletes the user's home directory",
                            "It only works on 32-bit Windows machines"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What happens if a command executed via 'subprocess.run(cmd, check=True)' returns an exit code of 1?",
                        "options": [
                            "Python prints a warning and continues running silently",
                            "Python raises a CalledProcessError exception that can be caught in a try/except block",
                            "The operating system reboots immediately",
                            "The return code is converted to 0"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "What is the purpose of passing 'timeout=30' to a 'subprocess.run()' invocation in an automation worker?",
                        "options": [
                            "To make the script pause for 30 seconds before starting",
                            "To terminate the child process and raise a TimeoutExpired exception if it fails to finish within 30 seconds",
                            "To limit CPU usage to 30%",
                            "To set the process priority to low"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 2,
                "title": "Web Scraping & HTML Parsing with BeautifulSoup & Requests",
                "subtopics": [
                    {
                        "title": "HTTP Client Engineering: Sessions, Headers & Resilient Retries",
                        "brief": "Build industrial-strength HTTP scrapers. Use requests.Session to maintain persistent TCP connections (HTTP Keep-Alive) and manage cookies across requests. Configure realistic browser headers (User-Agent, Accept, Accept-Language) to avoid naive bot blockers. Mount custom HTTP adapters with urllib3.util.retry.Retry to implement automatic exponential backoff retries when facing 429 Too Many Requests or intermittent 502/503 server errors.",
                        "takeaways": [
                            "Maintain persistent TCP connections and session cookies using requests.Session.",
                            "Configure realistic browser request headers to avoid automated anti-bot triggers.",
                            "Implement exponential backoff retry adapters to survive intermittent network faults."
                        ],
                        "prompt_seed": "Write a Python snippet configuring a requests.Session with an exponential backoff retry adapter that handles 429 and 500-level HTTP errors."
                    },
                    {
                        "title": "DOM Parsing, CSS Selectors & XPath with BeautifulSoup",
                        "brief": "Extract structured data from raw HTML trees. Compare parsing engines (lxml vs html.parser). Master concise CSS selector syntax with soup.select() and soup.select_one(). Navigate complex DOM hierarchies using relative traversal: parent, next_sibling, and find_previous. Extract link hrefs, image sources, and parse nested tabular data into clean Python dictionaries and lists.",
                        "takeaways": [
                            "Extract target content accurately using concise CSS selectors in BeautifulSoup.",
                            "Traverse complex DOM hierarchies using relative parent/sibling navigation methods.",
                            "Parse structured HTML tables into standardized Python dictionaries."
                        ],
                        "prompt_seed": "Show how to extract all product titles, prices, and availability statuses from an HTML category page using BeautifulSoup CSS selectors."
                    },
                    {
                        "title": "Anti-Bot Defense Navigation: Headers, Proxies & Rate Governance",
                        "brief": "Scrape sustainably and responsibly. Navigate modern rate limiters and Web Application Firewalls (WAF). Implement randomized jitter delays (random.uniform) between requests to avoid predictable bot cadence. Configure HTTP and SOCKS5 proxy pools to distribute outbound traffic. Parse and honor target site robots.txt files, identify honeypot links, and manage ethical scraping boundaries.",
                        "takeaways": [
                            "Prevent automated IP bans using randomized jitter sleep intervals.",
                            "Route scraper requests through HTTP and SOCKS5 proxy pools.",
                            "Parse robots.txt directives and avoid hidden honeypot trap elements."
                        ],
                        "prompt_seed": "Explain how jittered exponential backoff and proxy rotation prevent IP bans when scraping e-commerce sites."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the primary network advantage of using 'requests.Session()' over standalone 'requests.get()' calls in a loop?",
                        "options": [
                            "It uses dark mode styling for HTTP responses",
                            "It reuses underlying TCP socket connections (Keep-Alive), eliminating repetitive TCP and TLS handshakes",
                            "It bypasses all internet firewall rules",
                            "It doubles the download speed of video files"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "In BeautifulSoup, what is the difference between 'soup.find()' and 'soup.select()'?",
                        "options": [
                            "find() uses tag name and keyword filters; select() accepts standard CSS selector strings",
                            "find() works only on XML; select() works only on JSON",
                            "select() is deprecated and should never be used",
                            "find() automatically executes JavaScript on the page"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 3,
                        "question": "What is a 'honeypot link' set by webmasters to detect scrapers?",
                        "options": [
                            "A link that gives users free coupons",
                            "A link hidden from visual users (via CSS display:none) that only automated bots crawling the raw HTML click, triggering an immediate IP ban",
                            "A link to an external honey-farming company",
                            "A link that encrypts the user's computer"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "Which HTTP response header indicates how many seconds a client must wait before making another request after receiving a 429 status code?",
                        "options": ["Retry-After", "X-Wait-Time", "Rate-Limit-Sleep", "Server-Pause"],
                        "correct_index": 0
                    },
                    {
                        "id": 5,
                        "question": "Why is adding randomized 'jitter' (e.g. sleep(random.uniform(1.5, 3.5))) superior to fixed sleep intervals (sleep(2)) in web scraping?",
                        "options": [
                            "It reduces CPU power consumption by 50%",
                            "Fixed timing patterns create recognizable periodic spikes that rate-limiting firewalls easily flag as automated bot traffic",
                            "Python cannot execute integer sleep durations",
                            "It allows the scraper to run without an IP address"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 3,
                "title": "Browser Automation & Dynamic SPAs with Playwright & Selenium",
                "subtopics": [
                    {
                        "title": "Headless Browser Architecture & Playwright Setup",
                        "brief": "Automate modern dynamic web applications (React, Angular, Vue) where target data is rendered asynchronously via client-side JavaScript. Understand headless browser architecture using the Chrome DevTools Protocol (CDP). Set up Playwright in Python on headless Linux EC2 servers without physical displays. Configure browser contexts, viewport sizes, and optimize memory footprints by blocking unnecessary image and font downloads.",
                        "takeaways": [
                            "Configure and launch headless Chromium browsers on Linux servers using Playwright.",
                            "Intercept and block image/font network traffic to reduce memory and accelerate scraping.",
                            "Manage isolated browser contexts and user storage states."
                        ],
                        "prompt_seed": "Write a Playwright Python script that launches a headless Chromium browser, navigates to a dynamic SPA, and intercepts network JSON responses."
                    },
                    {
                        "title": "Dynamic Form Interaction, Infinite Scroll & Explicit Waits",
                        "brief": "Interact with dynamic UI elements reliably. Learn why time.sleep() causes fragile, slow automation. Master Explicit Waits (wait_for_selector, wait_for_load_state) that wait for precise DOM conditions. Automate multi-step form submissions, dropdowns, modal dismissals, and infinite scroll pagination by evaluating JavaScript scroll positions until content loading terminates.",
                        "takeaways": [
                            "Eliminate flaky automation by replacing sleep timers with condition-based explicit waits.",
                            "Automate complex user workflows: multi-page forms, modals, and file uploads.",
                            "Implement infinite scroll loops that detect when dynamically loaded content terminates."
                        ],
                        "prompt_seed": "How do explicit waits differ from implicit waits in Selenium/Playwright, and why do explicit waits eliminate flakiness?"
                    },
                    {
                        "title": "Automated Screenshots, PDF Generation & File Interception",
                        "brief": "Capture visual and binary digital assets. Generate full-page screenshots of dashboards for visual monitoring and archival. Print dynamic web views into high-resolution, print-ready PDF reports. Automate binary file downloads (CSV reports, invoices), intercept download events with Playwright, and verify downloaded file integrity using MD5 checksums.",
                        "takeaways": [
                            "Capture full-page and element-specific high-resolution screenshots automatically.",
                            "Render dynamic web pages to professional PDF documents.",
                            "Intercept browser file downloads and verify data integrity with MD5 hashing."
                        ],
                        "prompt_seed": "Write a Playwright script that navigates to an internal dashboard, sets a custom viewport, and saves a full-page PDF report."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "Why is static HTML scraping with Requests and BeautifulSoup ineffective for single-page applications built with React or Vue?",
                        "options": [
                            "Because React websites do not use the HTTP protocol",
                            "The initial HTML response contains only an empty root div and JavaScript bundle script; content is rendered client-side after script execution",
                            "BeautifulSoup is blocked by all JavaScript frameworks",
                            "React requires WebAssembly to download"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What is the primary operational hazard of using 'time.sleep(10)' to wait for dynamic elements to appear in browser automation?",
                        "options": [
                            "It damages the server motherboard",
                            "It creates brittle, slow tests that fail when networks lag beyond 10 seconds and waste time when elements load in 1 second",
                            "It forces the browser to shut down",
                            "time.sleep() is forbidden in modern versions of Python"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "In Playwright, what is the benefit of routing network requests to abort image and font file loading (e.g. route.abort())?",
                        "options": [
                            "It turns the browser into a text terminal",
                            "It dramatically accelerates page load times and slashes server memory and bandwidth consumption",
                            "It bypasses all website authentication gates",
                            "It guarantees the browser will not crash on reboot"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What does a 'Headless' browser mode mean in server deployments?",
                        "options": [
                            "The browser operates without an internet connection",
                            "The browser runs in background memory without rendering a physical graphical user interface (GUI) or display window",
                            "The browser has no JavaScript engine",
                            "The browser cannot store cookies"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "Which Playwright method waits specifically until network activity has been idle for at least 500ms before continuing execution?",
                        "options": [
                            "page.wait_for_timeout(500)",
                            "page.wait_for_load_state('networkidle')",
                            "page.wait_for_server_quiet()",
                            "page.pause_until_ready()"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 4,
                "title": "Data Pipeline Automation with Pandas & Tabular Processing",
                "subtopics": [
                    {
                        "title": "Vectorized Data Transformation & ETL Pipelines",
                        "brief": "Process structured automation feeds at scale. Ingest messy tabular datasets into Pandas DataFrames. Implement vectorized data cleaning: handling missing null values (fillna, dropna), removing duplicate records, regex string standardization (formatting phone numbers, stripping currencies), type casting, and parsing heterogeneous datetime formats into standardized UTC timestamps.",
                        "takeaways": [
                            "Build automated Extract, Transform, Load (ETL) data pipelines in Python.",
                            "Execute vectorized cleaning operations orders of magnitude faster than iterative Python loops.",
                            "Normalize messy multi-source dates and numeric strings into standardized data schemas."
                        ],
                        "prompt_seed": "Write a Pandas ETL function that cleans a raw transactions export: normalizes phone numbers, converts date strings to UTC datetimes, and removes duplicate orders."
                    },
                    {
                        "title": "Excel Automation & Report Formatting with OpenPyXL",
                        "brief": "Automate corporate spreadsheet workflows. Read, create, and modify .xlsx workbooks using openpyxl. Populate multi-sheet workbooks, inject native Excel formulas (=SUM, =AVERAGE, =XLOOKUP), apply custom cell formatting (currency formats, font styling, borders, fill colors), configure conditional formatting rules, and auto-adjust column widths to fit content perfectly.",
                        "takeaways": [
                            "Generate professional, stylized multi-sheet Excel reports programmatically.",
                            "Inject dynamic spreadsheet formulas that recalculate upon opening in Excel.",
                            "Apply conditional styling rules and auto-fit column dimensions automatically."
                        ],
                        "prompt_seed": "Write a Python function using openpyxl that creates a multi-sheet financial workbook with custom header styles, auto-fitted columns, and a total summary formula."
                    },
                    {
                        "title": "Automated PDF Extraction & Document Processing",
                        "brief": "Extract structured data from unstructured corporate documents. Use pdfplumber and pypdf to inspect digital PDF invoices, statements, and receipts. Extract clean raw text, extract bounding box coordinates, and reconstruct complex tabular data grids into clean Pandas DataFrames. Automate text normalization across multi-page document archives.",
                        "takeaways": [
                            "Extract text and tabular grids from digital PDF documents into Pandas DataFrames.",
                            "Process multi-page invoice batches automatically without manual data entry.",
                            "Clean and sanitize extracted document text for downstream database storage."
                        ],
                        "prompt_seed": "How does pdfplumber reconstruct tabular grid structures from raw PDF text characters and lines?"
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "Why are vectorized Pandas operations significantly faster than using standard Python for-loops to iterate over DataFrame rows?",
                        "options": [
                            "Pandas operations run on quantum cloud computers",
                            "Vectorized operations are implemented in optimized, compiled C code that executes SIMD processor instructions over contiguous memory arrays",
                            "Python for-loops delete memory every 10 rows",
                            "Pandas converts all data into pure integer values"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "In openpyxl, how do you insert a native Excel formula into a cell rather than a static numeric value?",
                        "options": [
                            "ws['C10'] = '=SUM(C2:C9)' as a string",
                            "ws['C10'] = openpyxl.Formula('SUM', 'C2', 'C9')",
                            "ws['C10'].calculate('SUM(C2:C9)')",
                            "Excel formulas cannot be written using openpyxl"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 3,
                        "question": "What is the primary function of 'df.drop_duplicates(subset=['sku'], keep='last')' in a Pandas ETL pipeline?",
                        "options": [
                            "It drops the entire 'sku' column from the table",
                            "It keeps only the final occurrence of duplicate rows sharing identical 'sku' values, discarding earlier duplicates",
                            "It renames duplicate skus with numbers",
                            "It throws an error if any duplicate skus exist"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "What distinguishes 'pdfplumber' from basic PDF text extraction libraries like PyPDF2?",
                        "options": [
                            "pdfplumber is written in Java",
                            "pdfplumber inspects precise character coordinates, bounding boxes, and lines to reconstruct tabular tables visually",
                            "pdfplumber only works on encrypted files",
                            "pdfplumber converts PDFs into MP3 audio files"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "In Pandas, what does 'pd.to_datetime(df['date_str'], utc=True, errors='coerce')' do when encountering an invalid date string?",
                        "options": [
                            "It raises a ValueError and crashes the script",
                            "It converts valid strings to UTC datetimes and silently converts invalid date strings into NaT (Not a Time) missing values",
                            "It replaces invalid dates with today's date",
                            "It deletes the entire row from memory"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 5,
                "title": "API Integration, Webhooks & Automated Messaging Systems",
                "subtopics": [
                    {
                        "title": "Consuming Third-Party REST APIs & OAuth2 Workflows",
                        "brief": "Interface with external cloud services. Manage API authentication: Static API keys, Bearer tokens, and the OAuth2 Client Credentials flow. Handle cursor-based and offset-based pagination across long API collections. Inspect and respect rate-limiting headers (X-RateLimit-Remaining, X-RateLimit-Reset) and cache idempotent GET responses locally to avoid API quota burn.",
                        "takeaways": [
                            "Build robust, reusable API client classes for third-party platforms.",
                            "Implement automatic pagination to retrieve full enterprise collections.",
                            "Parse and respect provider rate-limiting headers with intelligent pauses."
                        ],
                        "prompt_seed": "Write a reusable Python API client class that automatically handles pagination and respects rate-limit headers."
                    },
                    {
                        "title": "Multi-Channel Alert Pipelines: Email (SMTP/cPanel), Slack & Telegram",
                        "brief": "Notify humans when critical events occur. Build multi-channel alerting engines: Dispatch rich HTML emails with embedded styles and PDF/Excel attachments using Python's smtplib and email.mime modules or transactional email APIs (cPanel/SES). Broadcast structured JSON alert webhooks to Slack channels (Block Kit formatting) and Telegram messaging bots.",
                        "takeaways": [
                            "Construct and dispatch multi-part MIME emails with attachments via SMTP.",
                            "Broadcast structured operational alert cards to Slack channels via webhooks.",
                            "Implement fallback alerting that switches to Telegram or SMS if email dispatch fails."
                        ],
                        "prompt_seed": "Write a Python alert utility that sends a formatted Slack webhook message and falls back to an SMTP email if the webhook fails."
                    },
                    {
                        "title": "Building Lightweight Webhook Receivers with Flask",
                        "brief": "Create inbound event listeners that trigger automation pipelines. Build a lightweight Flask webhook endpoint to receive inbound event notifications (e.g. Stripe payment succeeded, GitHub push, Typeform submission). Validate HMAC cryptographic signatures (SHA-256) to verify webhook authenticity and reject spoofed payloads. Return immediate 200 OK responses before dispatching asynchronous background tasks.",
                        "takeaways": [
                            "Build secure webhook receiver endpoints in Python with Flask.",
                            "Verify cryptographic HMAC SHA-256 signatures to reject forged payloads.",
                            "Return immediate 200 OK responses to avoid webhook sender timeouts."
                        ],
                        "prompt_seed": "Write a Flask webhook listener that verifies an incoming HMAC-SHA256 signature header before processing the request body."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "What is the primary purpose of verifying an HMAC SHA-256 signature header on incoming webhooks (e.g. Stripe-Signature)?",
                        "options": [
                            "To encrypt the outgoing response so the sender cannot read it",
                            "To cryptographically verify that the payload originated from the authentic sender and was not intercepted or forged by an attacker",
                            "To compress the payload size by 50%",
                            "To check whether the sender is running on Linux"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "Why should a webhook receiver return an HTTP 200 OK response immediately before executing long-running automation tasks?",
                        "options": [
                            "Webhook senders enforce strict timeouts (often 3-5 seconds); slow processing triggers automated retries and duplicate event deliveries",
                            "HTTP 200 is the only status code allowed by the Python language",
                            "Returning 200 saves electricity in the server rack",
                            "Webhooks fail if any other headers are returned"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 3,
                        "question": "In Python's standard 'email.mime' library, which class is required when sending an email containing both plain text, HTML, and an attached file?",
                        "options": ["MIMEMultipart", "MIMETextOnly", "MIMEAttachmentMaster", "MIMESingleStream"],
                        "correct_index": 0
                    },
                    {
                        "id": 4,
                        "question": "What does a Slack incoming webhook require in its JSON POST payload to display formatted text?",
                        "options": [
                            "A JSON object containing at minimum a 'text' key or 'blocks' array",
                            "An XML document containing a SOAP header",
                            "A binary raw image file",
                            "A zip file containing markdown"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 5,
                        "question": "In the OAuth2 Client Credentials grant flow, where does the application exchange its client_id and client_secret for an access_token?",
                        "options": [
                            "By writing them to a public GitHub repository",
                            "Via an encrypted HTTPS POST request to the authorization server's token endpoint",
                            "By sending an unencrypted email to the API provider",
                            "Through a DNS TXT record lookup"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 6,
                "title": "Scheduled Execution, Background Jobs & Process Daemons",
                "subtopics": [
                    {
                        "title": "Linux Cron Jobs & Systemd Timers",
                        "brief": "Automate recurring scheduled tasks on Linux servers. Understand the 5-field cron syntax (minute hour day month day-of-week). Troubleshoot classic cron failures: missing PATH environment variables, wrong working directories, and lost error logs. Transition from legacy cron to modern Linux Systemd Timers for centralized logging in journalctl, dependency chaining, and persistent miss handling across reboots.",
                        "takeaways": [
                            "Schedule automation scripts reliably using Linux crontab.",
                            "Capture scheduled job stdout and stderr into dedicated rotating log files.",
                            "Configure Systemd service and timer unit pairs for modern scheduling."
                        ],
                        "prompt_seed": "Explain why cron jobs frequently fail due to environment PATH issues, and write a systemd timer unit that runs an automation script daily at 2:00 AM."
                    },
                    {
                        "title": "In-Process Schedulers: APScheduler & Background Workers",
                        "brief": "Embed scheduling directly inside Python applications. Use APScheduler (Advanced Python Scheduler) for interval, date, and cron triggers. Configure persistent job stores (SQLite or PostgreSQL) so scheduled jobs survive process restarts. Configure misfire grace times, coalescing missed executions, and understand concurrency trade-offs between thread pools and process pools.",
                        "takeaways": [
                            "Embed background task schedulers directly within long-running Python services.",
                            "Persist job schedules across process reboots using SQLite job stores.",
                            "Configure misfire policies to handle jobs delayed by server load."
                        ],
                        "prompt_seed": "Write an APScheduler configuration using BackgroundScheduler with an SQLite job store and a misfire grace time of 60 seconds."
                    },
                    {
                        "title": "Concurrency Control, File Locks & Idempotency",
                        "brief": "Prevent catastrophic race conditions in automated workflows. What happens when a 5-minute scheduled scraper takes 12 minutes to run? Prevent overlapping concurrent executions using file locks (fcntl.flock on Linux, portalocker) and PID tracking files. Design idempotent database mutations that safely handle repeat executions without creating duplicate records or double-charging accounts.",
                        "takeaways": [
                            "Prevent overlapping script executions using operating system file locks.",
                            "Build idempotent data operations that safely handle retries and duplicate triggers.",
                            "Implement graceful shutdown signal handlers (SIGTERM, SIGINT) to finish transactions cleanly."
                        ],
                        "prompt_seed": "Implement a Python context manager using fcntl (file locking) that ensures only one instance of an automation script can run simultaneously."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "In standard Linux cron syntax, what schedule does '0 */2 * * 1-5' represent?",
                        "options": [
                            "Every 2 minutes on Monday through Friday",
                            "At minute 0 of every 2nd hour, Monday through Friday",
                            "At 2:00 AM on the 1st and 5th day of every month",
                            "Every 2 hours on weekends only"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What is the most frequent cause of a Python script working when run manually in bash, but failing when triggered via cron?",
                        "options": [
                            "Cron uses a minimal, restricted PATH environment variable that fails to locate the Python venv or system binaries",
                            "Cron cannot run Python 3 scripts",
                            "Cron requires a graphics monitor connected to the server",
                            "Cron only runs scripts written in C"
                        ],
                        "correct_index": 0
                    },
                    {
                        "id": 3,
                        "question": "Why is cross-process file locking (e.g. using fcntl.flock in non-blocking mode) essential for scheduled automation scripts?",
                        "options": [
                            "To encrypt the script source code from other users",
                            "To guarantee that if a prior scheduled execution is still running, the newly spawned instance exits immediately rather than causing overlapping race conditions",
                            "To speed up hard drive read speeds",
                            "To prevent the operating system from shutting down"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "In a Linux systemd timer unit, what does the setting 'Persistent=true' do?",
                        "options": [
                            "It keeps the timer running even when the server has no electrical power",
                            "If the server was powered off when the scheduled timer was due, the missed service triggers immediately when the machine boots back up",
                            "It prevents the service from ever being uninstalled",
                            "It writes timer logs to a persistent tape drive"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "What is the primary role of a SIGTERM signal handler in a long-running Python background worker daemon?",
                        "options": [
                            "To immediately kill the process without closing any files",
                            "To intercept graceful termination requests from systemd, finish current transactional work, release database locks, and exit cleanly",
                            "To restart the server kernel",
                            "To send a notification to Twitter"
                        ],
                        "correct_index": 1
                    }
                ]
            },
            {
                "day": 7,
                "title": "Production Hardening, Logging, Error Alerting & EC2 Deployment",
                "subtopics": [
                    {
                        "title": "Enterprise Logging Architecture & Rotating Handlers",
                        "brief": "Eliminate unmaintainable print() debugging statements. Configure Python's standard logging module for production: Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL), timestamp formatting, module attribution, and process IDs. Configure rotating file handlers (RotatingFileHandler by size, TimedRotatingFileHandler by day) to prevent log files from exhausting EC2 disk storage. Structure logs in JSON format for automated ingestion.",
                        "takeaways": [
                            "Configure production-grade file and console logging hierarchies in Python.",
                            "Prevent server disk exhaustion using size-based and time-based rotating log handlers.",
                            "Format logs into structured JSON payloads for centralized log collectors."
                        ],
                        "prompt_seed": "Write a standard Python logging configuration that writes colored output to the console and daily rotated logs (keeping 14 days) to /var/log/app.log."
                    },
                    {
                        "title": "Self-Healing Automation: Retries, Dead Letter Queues & Health Checks",
                        "brief": "Design automation pipelines that survive chaos. Build custom retry decorators with jittered exponential backoff. Implement failure isolation: an exception processing record #42 should not crash the batch of 1,000 records. Route failed records into an Error Dead Letter Queue (quarantine table or file) with full traceback details for later inspection. Implement heartbeat monitoring pings (e.g. Healthchecks.io, BetterStack) to detect silent task death.",
                        "takeaways": [
                            "Implement failure isolation patterns so single-item errors do not crash batch jobs.",
                            "Route unprocessable records to dead letter quarantine queues for post-incident inspection.",
                            "Integrate automated heartbeat healthcheck pings to alert on silent daemon failures."
                        ],
                        "prompt_seed": "Write a Python retry decorator with jittered exponential backoff and a dead-letter fallback handler for failed database inserts."
                    },
                    {
                        "title": "Headless Linux EC2 Deployment & Systemd Service Management",
                        "brief": "Deploy headless automation daemons to AWS EC2. Structure application code under /var/www/apps/automation. Configure virtual environments, isolate environment secrets, and assign restricted non-root service user ownership. Write and enable persistent Linux Systemd service unit files with Restart=always, manage automatic boot activation, and monitor real-time execution logs with journalctl.",
                        "takeaways": [
                            "Deploy Python automation suites to AWS EC2 Linux instances.",
                            "Daemonize automation workers using persistent Linux Systemd service units.",
                            "Inspect real-time execution logs and manage process lifecycles via journalctl and systemctl."
                        ],
                        "prompt_seed": "Provide a complete step-by-step deployment guide and Systemd service unit file for a headless Python scraper running 24/7 on Ubuntu EC2."
                    }
                ],
                "quiz": [
                    {
                        "id": 1,
                        "question": "Why is using print() statements instead of the standard 'logging' module considered bad practice in production background daemons?",
                        "options": [
                            "print() is removed in modern versions of Python",
                            "print() lacks severity levels, timestamp formatting, destination routing, and log rotation, risking disk exhaustion and lost debugging context",
                            "print() requires an active graphical desktop monitor",
                            "print() can only output strings shorter than 50 characters"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 2,
                        "question": "What does a TimedRotatingFileHandler with 'when=\"midnight\", backupCount=14' do?",
                        "options": [
                            "It deletes the application code every midnight",
                            "It rotates the log file every night at midnight, keeping exactly the 14 most recent daily log files and deleting older ones",
                            "It restarts the server at midnight every 14 days",
                            "It limits logs to 14 megabytes per day"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 3,
                        "question": "What is a 'Dead Letter Queue' (DLQ) in an automated data processing pipeline?",
                        "options": [
                            "A folder where deleted emails are permanently erased",
                            "A designated quarantine storage location where malformed or failed records are captured with error diagnostics without aborting the broader batch job",
                            "A queue that automatically shuts down the EC2 instance",
                            "An obsolete network protocol from the 1980s"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 4,
                        "question": "How does a 'heartbeat ping' (e.g. Healthchecks.io) detect that a scheduled cron job has silently stopped running?",
                        "options": [
                            "It sends a virus to the server",
                            "The script sends an HTTP GET ping upon successful completion; if the monitoring service fails to receive the ping within the expected window, it dispatches an alert",
                            "It measures the heartbeat of the human system administrator",
                            "It restarts the server if the CPU usage drops below 1%"
                        ],
                        "correct_index": 1
                    },
                    {
                        "id": 5,
                        "question": "Which Linux systemctl command both activates a service immediately AND configures it to launch automatically whenever the server boots up?",
                        "options": [
                            "systemctl start --now <service>",
                            "systemctl enable --now <service>",
                            "systemctl reboot <service>",
                            "systemctl persist <service>"
                        ],
                        "correct_index": 1
                    }
                ]
            }
        ]
    }

# =============================================================================
# 2. SEEDING ENGINE & DATABASE UPSERT
# =============================================================================

def seed_course(conn, curriculum_data):
    """
    Idempotently seeds a single course, its 7 chapters, 21 subtopics, 
    7 day quizzes, and 1 capstone project brief.
    """
    c_title = curriculum_data["title"]
    c_slug = curriculum_data["slug"]
    c_domain = curriculum_data["domain"]
    c_level = curriculum_data["level"]
    c_est_hours = curriculum_data["estimated_hours"]
    c_gradient = curriculum_data["banner_gradient"]
    c_project_brief = curriculum_data["project_brief"]
    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur = conn.cursor()

    # 1. Upsert into courses table
    cur.execute("SELECT id FROM courses WHERE slug = ?", (c_slug,))
    row = cur.fetchone()

    if row:
        course_id = row[0]
        cur.execute(
            """
            UPDATE courses SET
                title = ?, domain = ?, is_paid = 0, price_inr = 0,
                content_status = 'approved', source = 'custom', is_active = 1,
                level = ?, estimated_hours = ?, author_type = 'admin',
                requires_project = 1, banner_gradient = ?, updated_at = ?
            WHERE id = ?
            """,
            (c_title, c_domain, c_level, c_est_hours, c_gradient, now_ts, course_id)
        )
        action_desc = f"Updated existing course ID {course_id}"
    else:
        cur.execute(
            """
            INSERT INTO courses (
                title, slug, domain, is_paid, price_inr,
                content_status, source, is_active, level, estimated_hours,
                author_type, requires_project, banner_gradient, created_at, updated_at
            ) VALUES (?, ?, ?, 0, 0, 'approved', 'custom', 1, ?, ?, 'admin', 1, ?, ?, ?)
            """,
            (c_title, c_slug, c_domain, c_level, c_est_hours, c_gradient, now_ts, now_ts)
        )
        course_id = cur.lastrowid
        action_desc = f"Inserted new course ID {course_id}"

    # 2. In-place Upsert for Chapters, Subtopics, Quizzes, and Capstone Project
    total_subtopics = 0
    total_questions = 0

    for day_data in curriculum_data["days"]:
        day_num = day_data["day"]
        ch_title = f"Day {day_num}: {day_data['title']}"

        # Chapter upsert (by course_id, day_number)
        cur.execute(
            "SELECT id FROM course_chapters WHERE course_id = ? AND day_number = ?",
            (course_id, day_num)
        )
        ch_row = cur.fetchone()
        if ch_row:
            chapter_id = ch_row[0]
            cur.execute(
                "UPDATE course_chapters SET title = ? WHERE id = ?",
                (ch_title, chapter_id)
            )
        else:
            cur.execute(
                "INSERT INTO course_chapters (course_id, day_number, title, created_at) VALUES (?, ?, ?, ?)",
                (course_id, day_num, ch_title, now_ts)
            )
            chapter_id = cur.lastrowid

        # Subtopics upsert (3 per chapter, by chapter_id, sort_order)
        for idx, st in enumerate(day_data["subtopics"], 1):
            cur.execute(
                "SELECT id FROM course_subtopics WHERE chapter_id = ? AND sort_order = ?",
                (chapter_id, idx)
            )
            st_row = cur.fetchone()
            if st_row:
                cur.execute(
                    """
                    UPDATE course_subtopics SET
                        title = ?, brief = ?, key_takeaways_json = ?, prompt_seed = ?
                    WHERE id = ?
                    """,
                    (st["title"], st["brief"], json.dumps(st["takeaways"]), st["prompt_seed"], st_row[0])
                )
            else:
                cur.execute(
                    """
                    INSERT INTO course_subtopics (
                        chapter_id, sort_order, title, brief, key_takeaways_json, prompt_seed, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (chapter_id, idx, st["title"], st["brief"], json.dumps(st["takeaways"]), st["prompt_seed"], now_ts)
                )
            total_subtopics += 1

        # Day Quiz upsert (by course_id, day_number)
        quiz_json = json.dumps(day_data["quiz"])
        cur.execute(
            "SELECT id FROM course_day_quizzes WHERE course_id = ? AND day_number = ?",
            (course_id, day_num)
        )
        q_row = cur.fetchone()
        if q_row:
            cur.execute(
                "UPDATE course_day_quizzes SET questions_json = ? WHERE id = ?",
                (quiz_json, q_row[0])
            )
        else:
            cur.execute(
                "INSERT INTO course_day_quizzes (course_id, day_number, questions_json, created_at) VALUES (?, ?, ?, ?)",
                (course_id, day_num, quiz_json, now_ts)
            )
        total_questions += len(day_data["quiz"])

    # 3. Capstone Project Brief upsert (by course_id)
    cur.execute("SELECT id FROM course_projects WHERE course_id = ?", (course_id,))
    p_row = cur.fetchone()
    if p_row:
        cur.execute(
            "UPDATE course_projects SET brief = ? WHERE id = ?",
            (c_project_brief.strip(), p_row[0])
        )
    else:
        cur.execute(
            "INSERT INTO course_projects (course_id, brief, created_at) VALUES (?, ?, ?)",
            (course_id, c_project_brief.strip(), now_ts)
        )

    return {
        "course_id": course_id,
        "slug": c_slug,
        "domain": c_domain,
        "action": action_desc,
        "chapters": len(curriculum_data["days"]),
        "subtopics": total_subtopics,
        "quizzes": len(curriculum_data["days"]),
        "questions": total_questions,
        "project": 1
    }


def resolve_db_path(cli_db_path=None):
    """
    Resolves the SQLite database file path using:
    1. Explicit CLI argument --db-path
    2. DB_FILE variable from .env or .env.production
    3. Standard deployment locations (/var/www/apps/internship/internship.db or ./internship.db)
    """
    if cli_db_path and os.path.exists(cli_db_path):
        return os.path.abspath(cli_db_path)

    # Check EC2 production standard path
    ec2_prod_path = "/var/www/apps/internship/internship.db"
    if os.path.exists(ec2_prod_path):
        return ec2_prod_path

    # Check local workspace relative paths
    candidates = [
        "internship.db",
        "internship_live.db",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "internship.db")
    ]
    for p in candidates:
        if os.path.exists(p):
            return os.path.abspath(p)

    return os.path.abspath("internship.db")


# =============================================================================
# 3. CLI RUNNER & INTEGRITY VERIFICATION
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="DBERT LMS Multi-Domain Course Seeder (EC2 & Production Ready)")
    parser.add_argument("--db-path", type=str, default=None, help="Target SQLite database file path")
    parser.add_argument(
        "--domain",
        type=str,
        choices=["fullstack", "ai_agent", "automation", "all"],
        default="all",
        help="Specify which domain course to seed (default: all)"
    )
    parser.add_argument("--all", action="store_true", help="Seed all three courses simultaneously")

    args = parser.parse_args()

    target_db = resolve_db_path(args.db_path)
    print("=============================================================================")
    print(" DBERT LMS MULTI-DOMAIN ACCELERATED COURSE SEEDER")
    print("=============================================================================")
    print(f"[*] Target Database : {target_db}")
    print(f"[*] Timestamp       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if not os.path.exists(target_db):
        print(f"[!] Target database does not exist: {target_db}")
        sys.exit(1)

    # Connect to SQLite
    conn = sqlite3.connect(target_db)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")

    selected_domain = "all" if args.all else args.domain

    tasks = []
    if selected_domain in ("fullstack", "all"):
        tasks.append(("Full Stack Development", get_full_stack_curriculum))
    if selected_domain in ("ai_agent", "all"):
        tasks.append(("AI Agent Development", get_ai_agent_curriculum))
    if selected_domain in ("automation", "all"):
        tasks.append(("Python Automation", get_python_automation_curriculum))

    results = []
    try:
        with conn:
            for name, curriculum_func in tasks:
                print(f"[*] Seeding track: {name}...")
                data = curriculum_func()
                res = seed_course(conn, data)
                results.append(res)
                print(f"    [+] {res['action']}")
                print(f"        Chapters: {res['chapters']} | Subtopics: {res['subtopics']} | Quizzes: {res['quizzes']} ({res['questions']} MCQs) | Capstone: {res['project']}")

        print("\n=============================================================================")
        print(" SEEDING SUMMARY & INTEGRITY VERIFICATION")
        print("=============================================================================")
        print(f"{'Course Slug':<30} | {'Domain':<24} | {'Days':<4} | {'Subs':<4} | {'MCQs':<4} | {'Status'}")
        print("-" * 80)
        for r in results:
            print(f"{r['slug']:<30} | {r['domain']:<24} | {r['chapters']:<4} | {r['subtopics']:<4} | {r['questions']:<4} | SUCCESS")

        # Global Verification Query
        cur = conn.cursor()
        total_courses = cur.execute("SELECT COUNT(*) FROM courses WHERE is_active = 1").fetchone()[0]
        total_chapters = cur.execute("SELECT COUNT(*) FROM course_chapters").fetchone()[0]
        total_subtopics = cur.execute("SELECT COUNT(*) FROM course_subtopics").fetchone()[0]
        total_quizzes = cur.execute("SELECT COUNT(*) FROM course_day_quizzes").fetchone()[0]
        total_projects = cur.execute("SELECT COUNT(*) FROM course_projects").fetchone()[0]

        print("-" * 80)
        print(f"DATABASE TOTALS -> Courses: {total_courses} | Chapters: {total_chapters} | Subtopics: {total_subtopics} | Quizzes: {total_quizzes} | Projects: {total_projects}")
        print("=============================================================================")
        print("[OK] All requested courses seeded successfully and ready for production serving!")

    except Exception as e:
        import traceback
        print(f"\n[!] ERROR during course seeding: {e}")
        traceback.print_exc()
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
