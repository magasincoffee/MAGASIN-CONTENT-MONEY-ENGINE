# MCME-044 — OWNER ACTION PACKET

**Purpose:** resolve only the remaining Vietnam-access / +84 / payout facts that official docs cannot prove.  
**Do not send Work any secret or private financial/identity value.**

## Decision order

1. **MCME-010 — Pinterest property**
2. **MCME-011 — Awin access**
3. Awin merchant path
4. impact.com only if bounded Awin path fails
5. Amazon Associates remains conditional and currently cash-out BLOCKED

---

# Step 1 — MCME-010 Pinterest property confirmation

Owner action:

- use or create one truthful Pinterest property/business account;
- use real Vietnam identity/contact data;
- no foreign phone is required by the documented initial business-account flow;
- do not enable SMS 2FA merely for this test unless you actually want it.

Return only:

```text
platform=PINTEREST
status=SUCCESS | PENDING | BLOCKED
property_type=BUSINESS | PERSONAL_CONVERTED_TO_BUSINESS
public_or_sanitized_property_ref=<safe ref>
phone_requested_during_initial_signup=YES | NO
observed_at=<timestamp>
```

Never return password, cookies, SMS code, backup code, browser profile, or private account IDs.

---

# Step 2 — MCME-011 Awin access test

This is the **minimum unresolved proof** for Route A.

Owner action:

1. Open the official Awin Publisher Sign-Up.
2. Enter truthful:
   - Vietnam tax residency if offered;
   - real name/business name;
   - email;
   - real Pinterest/social promotional property.
3. If the flow asks for telephone:
   - use only the Owner's real Vietnam +84 number;
   - do not use rented SMS/foreign number/fake residency.
4. If the flow reaches email activation or account-status result, complete only what is necessary to learn the status.
5. **STOP** before returning any password, OTP, recovery code, tax ID, bank details, identity document, or payment data to Work.

Return only:

```text
platform=AWIN
country_or_tax_residency_vietnam_available=YES | NO | NOT_SEEN
phone_requested=YES | NO
plus84_result=SUCCESS | BLOCKED | NOT_TESTED
account_status=SUCCESS | PENDING | REJECTED | BLOCKED
pinterest_property_accepted=YES | NO | UNKNOWN
observed_at=<timestamp>
safe_reference=<public/sanitized reference if any>
```

### Interpretation

- Vietnam available + account SUCCESS/PENDING + no phone blocker → continue Awin bounded path.
- +84 rejected or Vietnam unavailable → Work records failure; do not fake another country/number.
- terminal Awin incompatibility → Brain can advance bounded fallback to impact.com.

---

# Step 3 — Awin payout route, only after an Awin relationship exists

Owner action is private:

1. Open Awin Payment Details.
2. Enable required Awin authenticator-app 2SV privately.
3. Check whether:
   - Destination Country = Vietnam is available;
   - a usable destination currency is offered;
   - Payoneer/GBT route appears;
   - Owner's real Vietnam bank can be entered/verified.
4. Do not send bank/account/tax/KYC values to Work.

Return only:

```text
platform=AWIN
payment_destination_vietnam=YES | NO
payment_provider=PAYONEER_GBT | OTHER | NONE
route=LOCAL_TRANSFER | SWIFT | UNKNOWN
currency=<safe code if visible>
bank_setup_status=SUCCESS | PENDING | BLOCKED | NOT_STARTED
fees_or_fx_visible=YES | NO
observed_at=<timestamp>
```

---

# Step 4 — impact.com fallback only if Awin bounded path fails

Owner action:

1. Sign up as a Partner using truthful Vietnam Country/Region.
2. When mobile verification appears, use real +84 only.
3. Complete the minimum account step needed to see SUCCESS/PENDING/BLOCKED.
4. Do not provide private values to Work.

Return:

```text
platform=IMPACT
country=Vietnam
mobile_verification_required=YES
plus84_result=SUCCESS | BLOCKED
account_status=SUCCESS | PENDING | REJECTED | BLOCKED
observed_at=<timestamp>
```

If the account later reaches payment setup, return only:

```text
bank_location_vietnam=AVAILABLE | BLOCKED | NOT_TESTED
withdrawal_method=WIRE | EFT | PAYPAL | UNKNOWN
currency=<safe code>
bank_setup_status=SUCCESS | PENDING | BLOCKED | NOT_STARTED
observed_at=<timestamp>
```

---

# Step 5 — Payoneer, only when winning path requires it

Official Vietnam guidance already verifies +84.

If a real Payoneer setup is required:

- choose Vietnam truthfully;
- use Owner's real +84;
- receive OTP privately via WhatsApp/SMS;
- perform KYC privately;
- link only Owner-authorized Vietnam bank.

Return only:

```text
platform=PAYONEER
country=Vietnam
plus84_verified=SUCCESS | BLOCKED
kyc_status=SUCCESS | PENDING | BLOCKED
vn_bank_link_status=SUCCESS | PENDING | BLOCKED
withdrawal_currency=<safe code>
observed_at=<timestamp>
```

Do not return OTP, identity document, tax ID, bank account number, private payout ID, or screenshots containing them.

---

# CASH_SETTLED evidence to keep later

When the first real payout eventually occurs, retain privately and report sanitized facts:

```text
network=<provider>
commission_ref_sanitized=<ref>
payable_amount=<amount>
payout_issued_amount=<amount>
payout_currency=<code>
payout_issued_at=<timestamp>
payout_ref_sanitized=<ref>
rail_type=<wire/local-transfer/etc>
amount_received=<amount>
received_currency=<code>
posted_at=<timestamp>
fees_visible=<amount/null>
fx_visible=<rate-or-null>
receiving_ref_sanitized=<ref>
funds_actually_received=true
owner_authorized_payout_rail=true
reconciled_to_payout=true
```

Only this final reconciled receiving evidence permits `CASH_SETTLED`.

---

# Prohibited

Do **not** use or return:

- fake/borrowed foreign phone;
- rented SMS/OTP service;
- fake residency/country;
- VPN identity trick;
- password;
- OTP/MFA/recovery code;
- CAPTCHA artifact;
- cookie/session;
- tax ID;
- bank account/routing/card number;
- identity document;
- private payout ID;
- raw affiliate/tracking token.

## Current Owner action required now

**None inside MCME-044 itself.**

After Brain accepts MCME-044, the next real action remains **MCME-010 Pinterest property confirmation**.  
The first unresolved +84/network test is **MCME-011 Awin signup**.
