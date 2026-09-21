"""dbert-mailer tests:
Covers auth (401), validation (400), multi-sender pool rotation,
failover, rate limits (429), and DBERT identity preservation.
"""
import app as mailer_module


def test_health():
    with mailer_module.app.test_client() as c:
        r = c.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert data["pool_size"] >= 1
    assert data["available_senders"] >= 1


def test_send_requires_api_key(client):
    r = client.post("/send", json={"to": "x@example.com", "subject": "S", "html": "<p>hi</p>"})
    assert r.status_code == 401


def test_send_rejects_wrong_api_key(client):
    r = client.post("/send", headers={"X-API-Key": "wrong"},
                     json={"to": "x@example.com", "subject": "S", "html": "<p>hi</p>"})
    assert r.status_code == 401


def test_send_validates_missing_to(client):
    r = client.post("/send", headers={"X-API-Key": "test-api-key"},
                     json={"subject": "S", "html": "<p>hi</p>"})
    assert r.status_code == 400


def test_send_validates_missing_subject(client):
    r = client.post("/send", headers={"X-API-Key": "test-api-key"},
                     json={"to": "x@example.com", "html": "<p>hi</p>"})
    assert r.status_code == 400


def test_send_validates_missing_body(client):
    r = client.post("/send", headers={"X-API-Key": "test-api-key"},
                     json={"to": "x@example.com", "subject": "S"})
    assert r.status_code == 400


def test_send_2xx_happy_path_ssl_port_465(client, monkeypatch):
    captured = {}

    class FakeSMTP_SSL:
        def __init__(self, host, port, timeout=None, context=None):
            captured["host"] = host
            captured["port"] = port
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def login(self, user, pw):
            captured["login"] = (user, pw)
        def sendmail(self, from_addr, to_addr, msg_str):
            captured["from_addr"] = from_addr
            captured["to_addr"] = to_addr
            captured["msg_str"] = msg_str

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", FakeSMTP_SSL)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP_SSL)

    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com",
        "subject": "DBERT Internship Offer",
        "html": "<p>Welcome to DBERT</p>",
        "text": "Welcome to DBERT",
    })
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "sent"
    assert captured["to_addr"] == "candidate@example.com"
    assert "From: DBERT Careers <" in captured["msg_str"]
    assert f"Reply-To: {data['sender']}" in captured["msg_str"]
    assert "Subject: DBERT Internship Offer" in captured["msg_str"]


def test_dbert_identity_and_custom_branding(client, monkeypatch):
    captured = {}

    class FakeSMTP_SSL:
        def __init__(self, host, port, timeout=None, context=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, pw): pass
        def sendmail(self, from_addr, to_addr, msg_str):
            captured["msg_str"] = msg_str

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", FakeSMTP_SSL)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP_SSL)

    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com",
        "subject": "DBERT Task Verification",
        "html": "<p>Approved</p>",
        "from_name": "DBERT Verification Team",
        "reply_to": "support@dbert.online",
    })
    assert r.status_code == 200
    assert "From: DBERT Verification Team <" in captured["msg_str"]
    assert "Reply-To: support@dbert.online" in captured["msg_str"]
    assert "X-Sender-Brand: DBERT" in captured["msg_str"]


def test_round_robin_rotation_across_pool(client, monkeypatch):
    senders_used = []

    class FakeSMTP_SSL:
        def __init__(self, host, port, timeout=None, context=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, pw): pass
        def sendmail(self, from_addr, to_addr, msg_str):
            senders_used.append(from_addr)

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", FakeSMTP_SSL)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP_SSL)

    pool_size = len(mailer_module.pool.senders)
    # Send enough emails to rotate through the pool
    for i in range(pool_size * 2):
        r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
            "to": f"user{i}@example.com",
            "subject": f"Test {i}",
            "html": "<p>Test</p>",
        })
        assert r.status_code == 200

    # Ensure all senders in the pool participated
    unique_senders = set(senders_used)
    expected_senders = {s.email for s in mailer_module.pool.senders}
    assert unique_senders == expected_senders


def test_failover_when_first_sender_fails(client, monkeypatch):
    attempts = []

    class MockSMTP_SSL:
        def __init__(self, host, port, timeout=None, context=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, pw):
            attempts.append(user)
            # Fail on first attempt, succeed on second
            if len(attempts) == 1:
                raise ConnectionRefusedError("smtp connection timed out")
        def sendmail(self, from_addr, to_addr, msg_str):
            pass

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", MockSMTP_SSL)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", MockSMTP_SSL)

    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com",
        "subject": "Failover Test",
        "html": "<p>Failover</p>",
    })
    assert r.status_code == 200
    assert r.get_json()["status"] == "sent"
    # Verify that failover attempted more than 1 sender
    assert len(attempts) >= 2


def test_all_senders_fail_returns_502(client, monkeypatch):
    class AlwaysFailingSMTP:
        def __init__(self, host, port, timeout=None, context=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, pw):
            raise ConnectionResetError("network is unreachable")
        def sendmail(self, *a): pass

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", AlwaysFailingSMTP)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", AlwaysFailingSMTP)

    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com",
        "subject": "502 Test",
        "html": "<p>fail</p>",
    })
    assert r.status_code == 502
    assert "send failed across pool" in r.get_json()["message"]


def test_rate_limit_blocks_when_pool_exhausted(client, monkeypatch):
    class FakeSMTP_SSL:
        def __init__(self, host, port, timeout=None, context=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, pw): pass
        def sendmail(self, *a): pass

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", FakeSMTP_SSL)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP_SSL)

    # Set artificially low limits for all senders to test exhaustion
    for s in mailer_module.pool.senders:
        s.hourly_limit = 1

    total_capacity = len(mailer_module.pool.senders)
    for _ in range(total_capacity):
        r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
            "to": "candidate@example.com", "subject": "Test", "html": "<p>hi</p>"
        })
        assert r.status_code == 200

    # Next send should be rejected as all senders are exhausted
    r_blocked = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com", "subject": "Test", "html": "<p>hi</p>"
    })
    assert r_blocked.status_code == 429
    assert r_blocked.get_json()["message"] == "all senders currently rate limited"


def test_reply_to_defaults_to_sending_mailbox_across_rotation(client, monkeypatch):
    captured_messages = []

    class FakeSMTP_SSL:
        def __init__(self, host, port, timeout=None, context=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, pw): pass
        def sendmail(self, from_addr, to_addr, msg_str):
            captured_messages.append((from_addr, msg_str))

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", FakeSMTP_SSL)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP_SSL)

    pool_size = len(mailer_module.pool.senders)
    for i in range(pool_size):
        r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
            "to": f"applicant{i}@example.com",
            "subject": f"Offer #{i}",
            "html": "<p>Offer</p>",
        })
        assert r.status_code == 200
        sender_email = r.get_json()["sender"]
        from_addr, msg_str = captured_messages[-1]
        assert from_addr == sender_email
        assert f"Reply-To: {sender_email}" in msg_str


def test_reply_to_explicit_override_is_honored(client, monkeypatch):
    captured = {}

    class FakeSMTP_SSL:
        def __init__(self, host, port, timeout=None, context=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, pw): pass
        def sendmail(self, from_addr, to_addr, msg_str):
            captured["msg_str"] = msg_str

    monkeypatch.setattr(mailer_module.smtplib, "SMTP_SSL", FakeSMTP_SSL)
    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP_SSL)

    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "applicant@example.com",
        "subject": "Interview Scheduling",
        "html": "<p>Select slot</p>",
        "reply_to": "interviews@customdomain.com",
    })
    assert r.status_code == 200
    assert "Reply-To: interviews@customdomain.com" in captured["msg_str"]
