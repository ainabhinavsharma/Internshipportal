# DBERT Internship Portal — Razorpay Payment Gateway & Dynamic Fallback Architecture (PAY-004 to PAY-010)

**Document Date:** 2026-09-23  
**Status:** Core Architectural Specification  
**Objective:** Seamless integration of Razorpay online payment gateway across all checkout touchpoints with automatic zero-downtime fallback to manual UPI QR code and screenshot verification when gateway keys are unconfigured.

---

## 1. Executive Summary & Dynamic Flow

The DBERT Internship Portal collects deposits and fees across multiple touchpoints:
1. **Internship Free Track Security Deposit** (₹499)
2. **Onboarding Data Completion Wizard** (Step 3: Deposit Verification)
3. **Post-Hire Job Offer Guarantee Deposit** (₹499)
4. **Paid Fast-Track Program Seat Fee** (₹1,599)
5. **Standalone LMS Course Purchases** (variable INR)
6. **Company Workshops / Cohort Registrations** (variable INR)

### Dynamic Detection Principle:
```python
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "").strip()
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "").strip()
RAZORPAY_ENABLED = bool(RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and os.environ.get("RAZORPAY_ENABLED", "1") == "1")
```

- **When `RAZORPAY_ENABLED == True`**:
  - The frontend hides the static QR code (`/static/img/qrcode.jpeg` / `/static/qr.jpg`) and screenshot upload controls.
  - The user clicks **"Pay Online (UPI / Cards / Netbanking)"**, launching Razorpay Standard Checkout (`Checkout.js`).
  - Upon successful payment signature verification on the server, the user's enrollment/purchase status transitions **instantly to `Enrolled` / `Paid`** without manual admin approval delays.
- **When `RAZORPAY_ENABLED == False`**:
  - The application automatically falls back to the existing manual UPI QR code and screenshot upload workflow.
  - The transaction enters the `/admin/enrollments` manual review queue.
  - Zero disruption to active operations if keys are absent or temporarily revoked.

---

## 2. Payment Touchpoints & UX Mapping

| Touchpoint | Current Amount | Location in UI | Razorpay Action | Fallback (Keys Absent) |
|---|---|---|---|---|
| **1. Internship Security Deposit** | ₹499 | `templates/portal.html` (`#ovSelected`) | Razorpay Modal popup -> instant enrollment activation | Static QR Code + Screenshot Upload |
| **2. Onboarding Wizard Step 3** | ₹499 | `templates/portal.html` (`#onboardingWizardModal` Step 3) | One-click Razorpay payment -> automatically advances wizard to Step 4 | Static QR Code + Screenshot Upload |
| **3. Post-Hire Guarantee Deposit** | ₹499 | `templates/portal.html` (`#ovJobDeposit`) | Razorpay Modal popup -> logs deposit in `post_hire_deposits` | Static QR Code + Screenshot Upload |
| **4. Paid Fast-Track Program** | ₹1,599 | `templates/program.html` (`#ctaForm`) | Direct Razorpay checkout -> immediate course and placement track access | Static UPI ID + Screenshot Upload |
| **5. LMS Standalone Courses** | `course.price_inr` | `templates/course_pay.html` | Direct Razorpay checkout -> instant chapter unlock | Static QR Code + Screenshot Upload |
| **6. Company Cohort Seats** | `cohort.fee_inr` | `/cohorts/<cohort_id>/enroll` | Instant cohort seat reservation | Offline review |

---

## 3. Backend Architecture & API Specifications

### 3.1 Order Creation Endpoint
`POST /api/payment/razorpay/create-order`

**Request Headers**: Cookie session required (authenticated intern or candidate).  
**Request Payload**:
```json
{
  "product_type": "security_deposit", // "security_deposit" | "paid_program" | "post_hire_deposit" | "course"
  "product_id": null,                // course_id or post_id if applicable
  "domain": "AI Agent Development",  // optional domain selection
  "joining_date": "2026-10-05"       // selected Monday
}
```

**Security Validation**:
- Backend validates the user's eligibility and determines the canonical price from database/config (`UPI_AMOUNT`, `PAID_PROGRAM_AMOUNT`, or `courses.price_inr`). **Clients never dictate the payment amount.**
- Calls Razorpay API:
  ```text
  POST https://api.razorpay.com/v1/orders
  Auth: Basic (RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
  Payload: {
    "amount": amount_in_paise, // e.g. 49900 for ₹499
    "currency": "INR",
    "receipt": "rcpt_user_{user_id}_{timestamp}",
    "notes": { "user_id": ..., "product": ... }
  }
  ```
- Returns:
  ```json
  {
    "status": "success",
    "order_id": "order_EKwxwAgituvdik",
    "amount": 49900,
    "currency": "INR",
    "key_id": "rzp_live_..."
  }
  ```

---

### 3.2 Payment Verification Endpoint
`POST /api/payment/razorpay/verify-payment`

**Request Payload**:
```json
{
  "razorpay_order_id": "order_EKwxwAgituvdik",
  "razorpay_payment_id": "pay_29QQoUBi66xm2f",
  "razorpay_signature": "9ef4dff3509376374f941825d34484ab819cd050edce385f0b0ee6e75dcd3268",
  "product_type": "security_deposit",
  "product_id": null,
  "domain": "AI Agent Development",
  "joining_date": "2026-10-05"
}
```

**Signature Verification Algorithm**:
```python
import hmac
import hashlib

expected_sig = hmac.new(
    RAZORPAY_KEY_SECRET.encode(),
    f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
    hashlib.sha256
).hexdigest()

if not hmac.compare_digest(expected_sig, razorpay_signature):
    return jsonify({"status": "error", "message": "Invalid payment signature"}), 400
```

**Atomic State Transition**:
Within a single database transaction:
1. Verify `razorpay_payment_id` has not been credited previously (`SELECT count(*) FROM payments WHERE razorpay_payment_id = ?`).
2. Insert audit record in `payments`:
   ```sql
   INSERT INTO payments (
       intern_id, amount, payment_status, gateway,
       razorpay_order_id, razorpay_payment_id, razorpay_signature,
       created_at
   ) VALUES (?, ?, 'Accepted', 'razorpay', ?, ?, ?, ?)
   ```
3. Update `enrollments`:
   - Set `payment_status = 'Accepted'`, `status = 'Enrolled'`, `payment_id = ?`.
4. Update `intern_accounts`:
   - Sync selected domain and joining date.
5. Create notification event for the user and admin.
6. Commit transaction and return `{ "status": "success", "redirect": "/portal" }`.

---

### 3.3 Asynchronous Webhook Endpoint
`POST /api/payment/razorpay/webhook`

- Protects against user drop-off (e.g. user pays on Razorpay but closes browser tab before redirect).
- Validates `X-Razorpay-Signature` against `RAZORPAY_WEBHOOK_SECRET`.
- Handles `payment.captured` event by looking up the order in `payments` or notes, and ensuring enrollment activation is executed idempotently.

---

## 4. Frontend Integration Template (`RazorpayCheckout` Helper)

Create shared client utility in `static/js/razorpay-checkout.js`:
```javascript
async function initiateRazorpayPayment(productType, metadata = {}) {
    const res = await fetch("/api/payment/razorpay/create-order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ product_type: productType, ...metadata })
    });
    const orderData = await res.json();
    if (orderData.status !== "success") {
        alert(orderData.message || "Could not initialize payment");
        return;
    }

    const options = {
        key: orderData.key_id,
        amount: orderData.amount,
        currency: orderData.currency,
        name: "DBERT Internship Portal",
        description: orderData.description || "Program Payment",
        image: "/static/img/hero_student.jpg",
        order_id: orderData.order_id,
        handler: async function (response) {
            const verifyRes = await fetch("/api/payment/razorpay/verify-payment", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({
                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_signature: response.razorpay_signature,
                    product_type: productType,
                    ...metadata
                })
            });
            const result = await verifyRes.json();
            if (result.status === "success") {
                window.location.reload();
            } else {
                alert("Payment verification failed: " + result.message);
            }
        },
        prefill: orderData.prefill || {},
        theme: { color: "#6366f1" }
    };
    const rzp = new Razorpay(options);
    rzp.open();
}
```

---

## 5. Content Security Policy (CSP) Updates

In `app.py`, update `csp_policy_for(nonce)` to allow Razorpay Checkout assets:
```python
_CSP_SCRIPT_ORIGINS = (
    "https://cdn.onesignal.com "
    "https://challenges.cloudflare.com https://www.googletagmanager.com "
    "https://checkout.razorpay.com"
)

# Frame source must allow Razorpay 3D Secure modal:
"frame-src 'self' https://challenges.cloudflare.com https://api.razorpay.com;"

# Connect source must allow Razorpay telemetry and order verification:
"connect-src 'self' ... https://api.razorpay.com https://lumberjack.razorpay.com;"
```

---

## 6. Migration & Database Schema Changes

Using the **Expand → Migrate → Verify → Switch → Monitor → Contract** cycle:
1. `EXPAND`: Add gateway columns to `payments`, `enrollments`, `post_hire_deposits`, and `course_payments`:
   - `gateway` (`TEXT DEFAULT 'manual_upi'`)
   - `razorpay_order_id` (`TEXT`)
   - `razorpay_payment_id` (`TEXT`)
   - `razorpay_signature` (`TEXT`)
   - `webhook_event_id` (`TEXT`)
2. `INDEX`: Add unique index on `payments(razorpay_payment_id)` where `razorpay_payment_id IS NOT NULL`.
3. `TEST`: Verify with `scripts/verify_backup_restore.py`.
