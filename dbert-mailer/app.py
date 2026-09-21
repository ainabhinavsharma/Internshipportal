"""dbert-mailer: standalone email relay for cPanel shared hosting.

Sends through the cPanel mailbox over localhost SMTP (not blocked like EC2 egress).
Does no rendering of its own -- the portal (internship app, EMAIL_PROVIDER=cpanel_api)
sends already-rendered HTML+text (footer/unsubscribe/pixel/UTM already baked in); this
app just relays it. Stateless, cheap cold-start for Passenger.
"""
import hmac
import logging
import os
import smtplib
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
# Anti-open-relay: From addresses are only ever honoured when their domain is on this
# allowlist; anything else silently falls back to DEFAULT_FROM_EMAIL.
ALLOWED_SENDER_DOMAINS = {
    d.strip().lower() for d in os.environ.get("ALLOWED_SENDER_DOMAINS", "").split(",") if d.strip()
}
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
DEFAULT_FROM_NAME = os.environ.get("DEFAULT_FROM_NAME", "DBERT")
MAIL_HOST = os.environ.get("MAIL_HOST", "localhost")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
MAIL_USER = os.environ.get("MAIL_USER", "")
MAIL_PASS = os.environ.get("MAIL_PASS", "")
RATE_LIMIT_PER_MIN = int(os.environ.get("RATE_LIMIT_PER_MIN", "60"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("dbert-mailer")

_rate_lock = threading.Lock()
_rate_window = deque()  # send timestamps in the trailing 60s window, shared per-process


def _rate_check():
    """Simple in-proc sliding-window counter -- good enough for a single small
    shared-host process; not distributed, by design (volume here is low)."""
    now = time.time()
    with _rate_lock:
        while _rate_window and now - _rate_window[0] > 60:
            _rate_window.popleft()
        if len(_rate_window) >= RATE_LIMIT_PER_MIN:
            return False
        _rate_window.append(now)
        return True


def _valid_api_key(provided):
    if not API_KEY or not provided:
        return False
    return hmac.compare_digest(provided, API_KEY)  # constant-time compare


def _resolve_from_email(requested):
    """Sender-lock: a requested From is only honoured if its domain is on
    ALLOWED_SENDER_DOMAINS; otherwise (or if none was given) fall back to
    DEFAULT_FROM_EMAIL. Never relays an arbitrary off-domain sender."""
    requested = (requested or "").strip()
    if requested and "@" in requested:
        domain = requested.rsplit("@", 1)[-1].lower()
        if domain in ALLOWED_SENDER_DOMAINS:
            return requested
    return DEFAULT_FROM_EMAIL


def _build_message(to_email, subject, html, text, from_name, from_email):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email
    msg["Date"] = formatdate(localtime=True)
    try:
        msg["Message-ID"] = make_msgid(domain=from_email.split("@")[-1])
    except Exception:
        pass
    if text:
        msg.attach(MIMEText(text, "plain", "utf-8"))
    if html:
        msg.attach(MIMEText(html, "html", "utf-8"))
    return msg


def _send_via_smtp(msg, from_email, to_email):
    with smtplib.SMTP(MAIL_HOST, MAIL_PORT, timeout=15) as s:
        s.ehlo()
        if MAIL_PORT != 25:
            try:
                s.starttls()
                s.ehlo()
            except smtplib.SMTPNotSupportedError:
                pass  # plain port 25 / a host that doesn't offer TLS
        if MAIL_USER and MAIL_PASS:
            s.login(MAIL_USER, MAIL_PASS)
        s.sendmail(from_email, to_email, msg.as_string())


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/send", methods=["POST"])
def send():
    if not _valid_api_key(request.headers.get("X-API-Key", "")):
        return jsonify({"status": "error", "message": "unauthorized"}), 401

    if not _rate_check():
        return jsonify({"status": "error", "message": "rate limit exceeded"}), 429

    data = request.get_json(silent=True) or {}
    to_email = (data.get("to") or "").strip()
    subject = (data.get("subject") or "").strip()
    html = data.get("html") or ""
    text = data.get("text") or ""
    from_name = (data.get("from_name") or DEFAULT_FROM_NAME).strip()

    if not to_email or "@" not in to_email:
        return jsonify({"status": "error", "message": "invalid 'to'"}), 400
    if not subject:
        return jsonify({"status": "error", "message": "missing 'subject'"}), 400
    if not html and not text:
        return jsonify({"status": "error", "message": "missing 'html' or 'text'"}), 400

    from_email = _resolve_from_email(data.get("from_email"))
    if not from_email:
        return jsonify({"status": "error", "message": "server misconfigured: no sender domain"}), 500

    msg = _build_message(to_email, subject, html, text, from_name, from_email)
    try:
        _send_via_smtp(msg, from_email, to_email)
    except Exception as e:
        log.error("send failed to=%s subject=%r err=%s", to_email, subject, e)
        return jsonify({"status": "error", "message": "send failed"}), 502

    log.info("sent to=%s subject=%r", to_email, subject)  # recipient + subject only, no body
    return jsonify({"status": "sent"}), 200


application = app  # Passenger looks for this name

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))
