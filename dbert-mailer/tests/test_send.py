"""dbert-mailer: auth (401), payload validation, sender-lock, rate limit, 2xx happy
path with a mocked SMTP. Live SMTP delivery is owner-verified manually post-deploy."""
import app as mailer_module


def test_health():
    with mailer_module.app.test_client() as c:
        r = c.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


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


def test_send_2xx_happy_path_with_mocked_smtp(client, monkeypatch):
    captured = {}

    class FakeSMTP:
        def __init__(self, host, port, timeout=None):
            captured["host"] = host
            captured["port"] = port
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def ehlo(self):
            pass
        def starttls(self):
            pass
        def login(self, user, pw):
            captured["login"] = (user, pw)
        def sendmail(self, from_addr, to_addr, msg_str):
            captured["from_addr"] = from_addr
            captured["to_addr"] = to_addr
            captured["msg_str"] = msg_str

    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP)
    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com", "subject": "Hello", "html": "<p>Hi <b>there</b></p>",
        "text": "Hi there", "from_name": "DBERT",
    })
    assert r.status_code == 200
    assert r.get_json() == {"status": "sent"}
    assert captured["to_addr"] == "candidate@example.com"
    assert captured["from_addr"] == "careers@dbert.info"  # default, no from_email given
    assert "Hello" in captured["msg_str"]


def test_sender_lock_allows_on_domain_from_email(client, monkeypatch):
    captured = {}

    class FakeSMTP:
        def __init__(self, host, port, timeout=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def ehlo(self): pass
        def starttls(self): pass
        def login(self, *a): pass
        def sendmail(self, from_addr, to_addr, msg_str):
            captured["from_addr"] = from_addr

    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP)
    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com", "subject": "Hello", "html": "<p>hi</p>",
        "from_email": "notifications@dbert.online",
    })
    assert r.status_code == 200
    assert captured["from_addr"] == "notifications@dbert.online"


def test_sender_lock_rejects_off_domain_from_email(client, monkeypatch):
    captured = {}

    class FakeSMTP:
        def __init__(self, host, port, timeout=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def ehlo(self): pass
        def starttls(self): pass
        def login(self, *a): pass
        def sendmail(self, from_addr, to_addr, msg_str):
            captured["from_addr"] = from_addr

    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP)
    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com", "subject": "Hello", "html": "<p>hi</p>",
        "from_email": "attacker@evil.com",
    })
    assert r.status_code == 200
    # off-domain From is silently overridden to the configured default, never relayed
    assert captured["from_addr"] == "careers@dbert.info"


def test_smtp_failure_returns_502(client, monkeypatch):
    class FailingSMTP:
        def __init__(self, host, port, timeout=None): pass
        def __enter__(self): raise ConnectionRefusedError("smtp down")
        def __exit__(self, *a): return False

    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FailingSMTP)
    r = client.post("/send", headers={"X-API-Key": "test-api-key"}, json={
        "to": "candidate@example.com", "subject": "Hello", "html": "<p>hi</p>",
    })
    assert r.status_code == 502


def test_rate_limit_blocks_after_threshold(client, monkeypatch):
    monkeypatch.setattr(mailer_module, "RATE_LIMIT_PER_MIN", 2)

    class FakeSMTP:
        def __init__(self, host, port, timeout=None): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def ehlo(self): pass
        def starttls(self): pass
        def login(self, *a): pass
        def sendmail(self, *a): pass

    monkeypatch.setattr(mailer_module.smtplib, "SMTP", FakeSMTP)
    payload = {"to": "candidate@example.com", "subject": "Hello", "html": "<p>hi</p>"}
    headers = {"X-API-Key": "test-api-key"}
    assert client.post("/send", headers=headers, json=payload).status_code == 200
    assert client.post("/send", headers=headers, json=payload).status_code == 200
    r3 = client.post("/send", headers=headers, json=payload)
    assert r3.status_code == 429
