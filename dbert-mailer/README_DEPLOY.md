# dbert-mailer — cPanel deploy

A tiny standalone Flask app that relays one email per request to a cPanel mailbox over
**localhost SMTP** (port 587/25 — not blocked the way outbound SMTP is on EC2). The
portal (`internship` app, `EMAIL_PROVIDER=cpanel_api`) does all the rendering — subject,
HTML, text, footer, unsubscribe link, open pixel, UTM tags — and just POSTs the
finished message here. This app never renders anything; it only relays + sends.

## 1. Create the mailbox

In cPanel → **Email Accounts**, create the mailbox you want mail to come from, e.g.
`careers@dbert.info`. Note its password — that's `MAIL_PASS` below.

## 2. AutoSSL on the mail subdomain (optional, if you expose one)

If you're putting this app on its own subdomain (e.g. `mailer.dbert.info`):
1. cPanel → **Domains** → create the subdomain `mailer.dbert.info` pointed at a new
   document root (e.g. `~/mailer.dbert.info`).
2. cPanel → **SSL/TLS Status** → select the subdomain → **Run AutoSSL**. Wait for the
   green padlock before sending real traffic to it.
3. Confirm `https://mailer.dbert.online/health` returns `{"status":"ok"}` once deployed.

## 3. Setup Python App

cPanel → **Setup Python App**:
1. **Create Application**
   - Python version: 3.9+ (whatever's available)
   - Application root: the folder you uploaded this `dbert-mailer/` content into
     (e.g. `mailer.dbert.info` or a subfolder under it)
   - Application URL: the subdomain/path from step 2
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application` (cPanel usually infers this from the file)
2. Click **Create**. cPanel generates a virtualenv and shows you an "Enter to the
   virtual environment" command.
3. Upload (or `git clone`/SCP) the contents of this `dbert-mailer/` folder into the
   Application root cPanel created.
4. In the cPanel Python App page, under **Configuration files**, set the environment
   variables from `.env.example` (cPanel's UI lets you add them directly — you do NOT
   need a real `.env` file in production; `.env` is only read for local dev, and only if
   `python-dotenv` happens to be installed):
   ```
   API_KEY=<a long random secret — same value the portal's CPANEL_EMAIL_API_KEY uses>
   MAIL_HOST=localhost
   MAIL_PORT=587
   MAIL_USER=careers@dbert.info
   MAIL_PASS=<the mailbox password from step 1>
   ALLOWED_SENDER_DOMAINS=dbert.info,dbert.online
   DEFAULT_FROM_EMAIL=careers@dbert.info
   DEFAULT_FROM_NAME=DBERT Careers
   RATE_LIMIT_PER_MIN=60
   ```
5. Run `pip install -r requirements.txt` via the "Run Pip Install" button (or the venv
   command cPanel gave you) — it's just `flask`.
6. Click **Restart** on the Python App page after any env/code change.

## 4. Test it

```bash
# health check (no auth)
curl -s https://mailer.dbert.online/health
# -> {"status":"ok"}

# send a real test email
curl -s -X POST https://mailer.dbert.online/send \
  -H "X-API-Key: <your API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
        "to": "you@example.com",
        "subject": "dbert-mailer test",
        "html": "<p>It works.</p>",
        "text": "It works."
      }'
# -> {"status":"sent"}  (check your inbox)

# missing/bad key -> 401
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://mailer.dbert.online/send \
  -H "Content-Type: application/json" -d '{"to":"x@example.com","subject":"S","html":"<p>hi</p>"}'
# -> 401
```

If `/send` returns `502`, the SMTP send itself failed — check `MAIL_HOST`/`MAIL_PORT`/
`MAIL_USER`/`MAIL_PASS`, and the app's log (cPanel Python App page → **Log**, or the
file Passenger writes under the app's `logs/` directory).

## 5. Point the portal at it

In the **portal's** `.env` (the `internship` app, not this one):
```
EMAIL_PROVIDER=cpanel_api
CPANEL_EMAIL_API_URL=https://mailer.dbert.online/send
CPANEL_EMAIL_API_KEY=<the same API_KEY you set above>
```
Restart the portal (`systemctl restart dbert-internship`). Trigger any status-change
notification and confirm `email_log.email_sent = 'YES'` on the portal side, and that the
message lands (check spam too — SPF/DKIM for the mailbox's domain is whatever cPanel's
mail server already has configured; this app doesn't change that).

## Notes

- **Stateless / cheap cold start**: no DB, no background workers — fine for Passenger's
  restart-on-file-touch model.
- **Shared-host SMTP throttling**: cPanel mail servers commonly cap outbound volume per
  hour/day. `RATE_LIMIT_PER_MIN` is a simple in-process guard so a portal bug can't burst
  past your host's own limits and get the mailbox suspended; tune it to what your host
  allows.
- **Sender-lock**: `from_email` in the request body is only honoured if its domain is in
  `ALLOWED_SENDER_DOMAINS` — anything else (including a missing value) silently falls
  back to `DEFAULT_FROM_EMAIL`. This app will never relay mail claiming to be from a
  domain you don't control.
- **Logging**: only recipient + subject + status are logged — never message bodies.
