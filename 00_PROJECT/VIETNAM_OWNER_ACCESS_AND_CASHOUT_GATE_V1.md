# VIETNAM OWNER ACCESS + CASH-OUT HARD GATE V1

Status: LOCKED AS PRE-EXECUTION HARD GATE
Owner residence: Vietnam
Business goal: FIRST REAL CASH means funds actually received on an Owner-authorized payout rail and reconciled to the affiliate payout record.

## Why this gate exists

A commission that cannot be withdrawn to the Owner in Vietnam is not a successful money loop.

Before real content production or scale, MCME must verify both:

1. ACCOUNT ACCESS FEASIBILITY
2. VIETNAM CASH-OUT FEASIBILITY

This gate does not change the selected market (United States), language (English), Pinterest route, niche, format, or affiliate strategy.

## New critical questions

### Account access
For every platform/network used in the first-cash path, verify:

- Can an Owner resident in Vietnam register using truthful Vietnam identity/contact information?
- Is a foreign-country phone number required?
- Is any valid mobile phone required?
- Can a Vietnam +84 mobile number be used?
- Can email or authenticator-app 2FA substitute for SMS after account creation?
- Are phone/SMS checks required again for financial actions?
- Are phone, identity, KYC, tax or payout checks mandatory before funds can be received?

### Cash-out
For every candidate money network, verify:

- Vietnam residence eligibility
- payout method available to Vietnam
- supported currency
- receiving bank requirements
- Payoneer/PayPal/SWIFT dependency if any
- KYC/tax requirements
- payout threshold
- payout cycle
- fees / intermediary fees
- FX conversion behavior
- rejected-payout behavior
- exact evidence required to prove CASH_SETTLED

## Current verified facts from official docs — planning truth only

### Pinterest
- Current Pinterest Business account creation documentation lists email, password and age for account creation.
- Adding a phone number is optional for the account in general.
- Pinterest 2FA by SMS requires a phone number.
- Therefore: foreign phone number is not a prerequisite for initial business-account creation based on current docs.
- Actual Owner property remains unverified until MCME-010.

### impact.com
- Current partner sign-up documentation includes mobile-number verification as Step 2.
- impact.com supports 2FA by email, authenticator app or SMS in account security settings.
- Phone information is also associated with many financial/security activities.
- Therefore: email-only must NOT be assumed sufficient for the standard new-partner sign-up flow.
- Whether a Vietnam +84 number works in the Owner's real flow must be VERIFIED, not assumed.

### Amazon Associates
- Amazon states an Associates account can exist without a phone number, but access/edit of payment details uses OTP to a registered mobile number; a number can be added at that point.
- Therefore: no phone at all can block payment setup even if initial account access is possible.

### Awin
- Current public publisher sign-up documentation does not provide enough evidence to conclude that phone verification is or is not mandatory.
- Treat Awin phone requirement as UNKNOWN until real registration flow or official support evidence confirms it.

### Payoneer
- Payoneer official registration FAQ says a valid phone number is required and the mobile number is validated.
- Payoneer's Vietnam guidance explicitly instructs Vietnamese users to enter a mobile number and receive OTP by WhatsApp/SMS.
- Payoneer also documents withdrawal to local bank accounts and has Vietnam-specific withdrawal/support pages.
- Therefore: if the selected Awin payout route requires Payoneer, an Owner with no mobile number at all has a real payout-access blocker.

## Locked policy

DO NOT:
- buy or borrow a fake foreign identity/phone number;
- use false country/residency data;
- use temporary SMS services for KYC/payment security;
- claim phone feasibility without real verification.

Prefer:
- the Owner's truthful Vietnam residency;
- a real Vietnam +84 mobile number owned/controlled by Owner;
- authenticator app or email 2FA where officially supported;
- sanitized evidence only in Git.

## Decision states

Each platform/network must be classified:

- VERIFIED_VN_EMAIL_ONLY
- VERIFIED_VN_PHONE_REQUIRED
- VERIFIED_VN_PHONE_OPTIONAL
- VERIFIED_AUTHENTICATOR_OR_EMAIL_FALLBACK
- UNKNOWN
- BLOCKED

No UNKNOWN is treated as PASS.

## CASH-OUT PASS

Vietnam cash-out feasibility is PASS only when at least one selected affiliate path has:

1. Owner/residency accepted
2. required phone/security path available
3. merchant relationship available
4. payout method to Vietnam available
5. KYC/tax/payment setup feasible
6. payout terms understood
7. no critical unresolved blocker

Ultimate Proof-of-Cash-Out remains:
commission → validated/payable → payout issued → funds actually received in Owner-authorized bank/payment rail → CASH_SETTLED.

## Sequencing change

A new Brain task is inserted before real Gate A execution:

MCME-044 — Vietnam Owner Access + Cash-Out Feasibility Gate

MCME-010 remains the first Pinterest-property task, but it must not be treated as sufficient to start production until MCME-044 is PASS or its remaining UNKNOWNs are explicitly Owner-resolvable.

No content production, publish, or scale is authorized by this document.
