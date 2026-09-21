# dbert-mailer — Multi-Domain Email Relay (cPanel / Passenger Deploy)

A lightweight standalone Flask microservice that relays emails through a rotating, rate-limited pool of SMTP accounts (Titan Email, cPanel, Gmail, etc.) while enforcing consistent **DBERT identity and branding** (Display Name: `DBERT Careers`, Reply-To: `careers@dbert.online`).

The portal (`internship` app on EC2, `EMAIL_PROVIDER=cpanel_api`) does all HTML rendering, open tracking, and unsubscribe generation, then POSTs the finished message here over HTTPS (port 443 — bypassing EC2 outbound port 25/587 blocks).

---

## 1. Multi-Sender Pool Architecture

Senders are loaded with the following priority:
1. **`SENDER_POOL_JSON`** environment variable (ideal for cPanel's "Setup Python App" configuration UI).
2. **`senders.json`** file in the app root directory.
3. Fallback to legacy single-mailbox env vars (`MAIL_HOST`, `MAIL_USER`, `MAIL_PASS`).

### Active Senders (Titan Email - Port 465 SSL):
- `contactus@aivaratech.online`
- `humanresource@aivaratech.online`
- `support@aivaratech.info`
- `hr@aivaratech.info`

### How to Add Senders in the Future:
Simply append a new sender object to `senders.json` or your `SENDER_POOL_JSON` env:
```json
{
  "id": "new_account_id",
  "email": "name@yourdomain.com",
  "password": "MailboxPasswordOrAppPassword",
  "name": "DBERT Careers",
  "server": "smtp.titan.email",
  "port": 465,
  "ssl": true,
  "hourly_limit": 28,
  "daily_limit": 280,
  "enabled": true
}
```
*For Gmail/Google Workspace, use `"server": "smtp.gmail.com"`, `"port": 587`, `"ssl": false`.*

---

## 2. cPanel Subdomain & AutoSSL

If you are hosting this on `mailer.dbert.online`:
1. In cPanel → **Domains** → create `mailer.dbert.online` with document root (e.g. `~/mailer.dbert.online`).
2. In cPanel → **SSL/TLS Status** → select `mailer.dbert.online` → **Run AutoSSL**. Wait for the green padlock before routing production traffic.

---

## 3. Setup Python App in cPanel

1. In cPanel → **Setup Python App** → **Create Application**:
   - **Python version**: 3.9+ (e.g., 3.11 or 3.12)
   - **Application root**: folder containing `dbert-mailer` files (e.g. `mailer.dbert.online`)
   - **Application URL**: `mailer.dbert.online`
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`
2. Click **Create**.
3. Upload the files from `dbert-mailer/` into the Application root on cPanel:
   - `app.py`
   - `passenger_wsgi.py`
   - `requirements.txt`
   - `senders.json`
4. Under **Configuration files**, set the environment variables:
   ```env
   API_KEY=c04e1ba5f674a53ce6b9c5e291ce2fdd91d8781c832a9bf195300dab5745e6e6
   DEFAULT_FROM_NAME=DBERT Careers
   DEFAULT_REPLY_TO=careers@dbert.online
   GLOBAL_RATE_LIMIT_PER_MIN=120
   ```
5. Run `pip install -r requirements.txt` via cPanel's "Run Pip Install" button.
6. Click **Restart** on the Python App page.

---

## 4. Testing & Verification

### A. Health Check (No Auth Required)
```bash
curl -s https://mailer.dbert.online/health
```
**Expected Response:**
```json
{
  "status": "ok",
  "pool_size": 4,
  "available_senders": 4,
  "senders": [ ... ]
}
```

### B. Send a Live Test Email
```bash
curl -s -X POST https://mailer.dbert.online/send \
  -H "X-API-Key: c04e1ba5f674a53ce6b9c5e291ce2fdd91d8781c832a9bf195300dab5745e6e6" \
  -H "Content-Type: application/json" \
  -d '{
        "to": "your-email@example.com",
        "subject": "DBERT Mailer Test",
        "html": "<p>This is a test email sent via multi-domain dbert-mailer.</p>",
        "text": "This is a test email sent via multi-domain dbert-mailer."
      }'
```
**Expected Response:**
```json
{"status": "sent", "sender": "contactus@aivaratech.online"}
```

---

## 5. Pointing the EC2 Internship Portal at the Mailer

In your EC2 portal's `.env` (`/var/www/apps/internship/.env`):
```env
EMAIL_PROVIDER=cpanel_api
CPANEL_EMAIL_API_URL=https://mailer.dbert.online/send
CPANEL_EMAIL_API_KEY=c04e1ba5f674a53ce6b9c5e291ce2fdd91d8781c832a9bf195300dab5745e6e6
FROM_NAME=DBERT Careers
FROM_EMAIL=careers@dbert.online
```
Restart the portal on EC2:
```bash
sudo systemctl restart dbert-internship
```
All transactional emails, interview invitations, enrollment receipts, and cohort updates will now relay seamlessly through the multi-sender pool.
