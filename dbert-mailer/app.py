"""dbert-mailer: multi-domain email relay for cPanel shared hosting.

Sends through an extensible, rotating, rate-limited pool of SMTP accounts
(Titan Email, cPanel, Gmail, etc.) while enforcing consistent DBERT branding and identity.
Stateless, cheap cold-start for Phusion Passenger.
"""
import hmac
import json
import logging
import os
import smtplib
import ssl
import threading
import time
from collections import deque
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

from flask import Flask, jsonify, request

try:  # optional: cPanel's "Setup Python App" sets env vars directly; .env is for local dev
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "")
DEFAULT_FROM_NAME = os.environ.get("DEFAULT_FROM_NAME", "DBERT Careers")
DEFAULT_REPLY_TO = os.environ.get("DEFAULT_REPLY_TO", "").strip()
GLOBAL_RATE_LIMIT_PER_MIN = int(os.environ.get("GLOBAL_RATE_LIMIT_PER_MIN", "120"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("dbert-mailer")


# ============================================================
# SENDER ACCOUNT & POOL MANAGEMENT
# ============================================================

class SenderAccount:
    """Represents a single mailbox with independent hourly/daily rate limiting."""

    def __init__(self, config):
        self.id = config.get("id", config.get("email"))
        self.email = (config.get("email") or "").strip().lower()
        self.password = config.get("password") or ""
        self.name = config.get("name") or DEFAULT_FROM_NAME
        self.server = config.get("server") or "smtp.titan.email"
        self.port = int(config.get("port", 465))
        self.ssl = bool(config.get("ssl", self.port == 465))
        self.hourly_limit = int(config.get("hourly_limit", config.get("rate_limit_per_hour", 28)))
        self.daily_limit = int(config.get("daily_limit", config.get("rate_limit_per_day", 280)))
        self.enabled = bool(config.get("enabled", True))
        self.reply_to = config.get("reply_to") or self.email

        self.hourly_window = deque()
        self.daily_window = deque()
        self.lock = threading.Lock()

    def purge_windows(self, now=None):
        if now is None:
            now = time.time()
        with self.lock:
            while self.hourly_window and now - self.hourly_window[0] > 3600:
                self.hourly_window.popleft()
            while self.daily_window and now - self.daily_window[0] > 86400:
                self.daily_window.popleft()

    def is_available(self, now=None):
        if not self.enabled:
            return False
        if now is None:
            now = time.time()
        self.purge_windows(now)
        with self.lock:
            return len(self.hourly_window) < self.hourly_limit and len(self.daily_window) < self.daily_limit

    def record_send(self, now=None):
        if now is None:
            now = time.time()
        with self.lock:
            self.hourly_window.append(now)
            self.daily_window.append(now)

    def to_dict(self):
        self.purge_windows()
        with self.lock:
            return {
                "id": self.id,
                "email": self.email,
                "server": self.server,
                "port": self.port,
                "ssl": self.ssl,
                "hourly_usage": len(self.hourly_window),
                "hourly_limit": self.hourly_limit,
                "daily_usage": len(self.daily_window),
                "daily_limit": self.daily_limit,
                "enabled": self.enabled,
            }


class SenderPool:
    """Manages pool rotation, failover, and rate limits across multiple senders."""

    def __init__(self):
        self.senders = []
        self._index = 0
        self._lock = threading.Lock()
        self._global_window = deque()
        self.load_senders()

    def load_senders(self):
        loaded = []

        # Priority 1: SENDER_POOL_JSON env var (ideal for cPanel App Configuration)
        raw_json = os.environ.get("SENDER_POOL_JSON", "").strip()
        if raw_json:
            try:
                data = json.loads(raw_json)
                if isinstance(data, list):
                    loaded = [SenderAccount(c) for c in data if isinstance(c, dict) and "email" in c and "password" in c]
            except Exception as e:
                log.error("Failed to parse SENDER_POOL_JSON: %s", e)

        # Priority 2: senders.json file in app directory
        if not loaded:
            json_file = os.path.join(os.path.dirname(__file__), "senders.json")
            if os.path.exists(json_file):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        loaded = [SenderAccount(c) for c in data if isinstance(c, dict) and "email" in c and "password" in c]
                except Exception as e:
                    log.error("Failed to load senders.json: %s", e)

        # Priority 3: Fallback to single sender env vars
        if not loaded:
            mail_user = os.environ.get("MAIL_USER", "").strip()
            mail_pass = os.environ.get("MAIL_PASS", "").strip()
            if mail_user and mail_pass:
                port = int(os.environ.get("MAIL_PORT", "587"))
                loaded.append(SenderAccount({
                    "id": "default",
                    "email": mail_user,
                    "password": mail_pass,
                    "name": os.environ.get("DEFAULT_FROM_NAME", DEFAULT_FROM_NAME),
                    "server": os.environ.get("MAIL_HOST", "localhost"),
                    "port": port,
                    "ssl": port == 465,
                    "hourly_limit": 60,
                    "daily_limit": 500,
                }))

        with self._lock:
            self.senders = loaded
            self._index = 0
        log.info("SenderPool initialized with %d sender accounts", len(self.senders))

    def check_global_rate(self):
        now = time.time()
        with self._lock:
            while self._global_window and now - self._global_window[0] > 60:
                self._global_window.popleft()
            if len(self._global_window) >= GLOBAL_RATE_LIMIT_PER_MIN:
                return False
            self._global_window.append(now)
            return True

    def get_candidate_senders(self):
        now = time.time()
        with self._lock:
            n = len(self.senders)
            if n == 0:
                return []
            # Order senders starting from the current round-robin index
            ordered = [self.senders[(self._index + i) % n] for i in range(n)]
            # Advance index for subsequent calls
            self._index = (self._index + 1) % n

        # Return senders that are currently within their rate limit caps
        return [s for s in ordered if s.is_available(now)]


pool = SenderPool()


# ============================================================
# HELPERS
# ============================================================

def _valid_api_key(provided):
    if not API_KEY or not provided:
        return False
    return hmac.compare_digest(provided, API_KEY)


def _build_message(to_email, subject, html, text, from_name, sender_email, reply_to=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{sender_email}>"
    msg["To"] = to_email
    # Reply-To defaults to the sending mailbox itself unless explicitly overridden
    msg["Reply-To"] = reply_to or sender_email
    msg["Date"] = formatdate(localtime=True)
    try:
        domain = sender_email.split("@")[-1]
        msg["Message-ID"] = make_msgid(domain=domain)
    except Exception:
        pass
    msg["X-Sender-Brand"] = "DBERT"
    if text:
        msg.attach(MIMEText(text, "plain", "utf-8"))
    if html:
        msg.attach(MIMEText(html, "html", "utf-8"))
    return msg


def _send_via_smtp(sender, msg, to_email):
    """Sends using SMTP_SSL (port 465) or STARTTLS (port 587/25)."""
    context = ssl.create_default_context()
    if sender.ssl:
        with smtplib.SMTP_SSL(sender.server, sender.port, context=context, timeout=20) as s:
            s.login(sender.email, sender.password)
            s.sendmail(sender.email, to_email, msg.as_string())
    else:
        with smtplib.SMTP(sender.server, sender.port, timeout=20) as s:
            s.ehlo()
            if sender.port != 25:
                try:
                    s.starttls(context=context)
                    s.ehlo()
                except smtplib.SMTPNotSupportedError:
                    pass
            if sender.password:
                s.login(sender.email, sender.password)
            s.sendmail(sender.email, to_email, msg.as_string())
    sender.record_send()


# ============================================================
# ROUTES
# ============================================================

@app.route("/health")
def health():
    candidates = [s for s in pool.senders if s.is_available()]
    return jsonify({
        "status": "ok",
        "pool_size": len(pool.senders),
        "available_senders": len(candidates),
        "senders": [s.to_dict() for s in pool.senders]
    })


@app.route("/send", methods=["POST"])
def send():
    if not _valid_api_key(request.headers.get("X-API-Key", "")):
        return jsonify({"status": "error", "message": "unauthorized"}), 401

    if not pool.check_global_rate():
        return jsonify({"status": "error", "message": "global rate limit exceeded"}), 429

    data = request.get_json(silent=True) or {}
    to_email = (data.get("to") or "").strip()
    subject = (data.get("subject") or "").strip()
    html = data.get("html") or ""
    text = data.get("text") or ""
    from_name = (data.get("from_name") or DEFAULT_FROM_NAME).strip()
    custom_reply_to = (data.get("reply_to") or "").strip()

    if not to_email or "@" not in to_email:
        return jsonify({"status": "error", "message": "invalid 'to'"}), 400
    if not subject:
        return jsonify({"status": "error", "message": "missing 'subject'"}), 400
    if not html and not text:
        return jsonify({"status": "error", "message": "missing 'html' or 'text'"}), 400

    candidates = pool.get_candidate_senders()
    if not candidates:
        log.warning("All senders in pool are currently rate limited or exhausted")
        return jsonify({"status": "error", "message": "all senders currently rate limited"}), 429

    last_err = None
    for sender in candidates:
        effective_reply_to = custom_reply_to or sender.reply_to or sender.email
        msg = _build_message(to_email, subject, html, text, from_name, sender.email, effective_reply_to)
        try:
            _send_via_smtp(sender, msg, to_email)
            log.info("sent to=%s subject=%r via sender=%s reply_to=%s", to_email, subject, sender.email, effective_reply_to)
            return jsonify({"status": "sent", "sender": sender.email}), 200
        except Exception as e:
            last_err = e
            log.warning("send failed via sender=%s to=%s: %s (trying next sender in pool)", sender.email, to_email, e)

    log.error("all candidates failed for to=%s subject=%r err=%s", to_email, subject, last_err)
    return jsonify({"status": "error", "message": f"send failed across pool: {last_err}"}), 502


application = app  # Passenger looks for this name

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))
