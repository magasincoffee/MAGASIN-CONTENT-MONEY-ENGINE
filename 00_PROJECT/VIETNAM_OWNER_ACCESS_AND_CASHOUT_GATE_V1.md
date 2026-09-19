# VIETNAM OWNER ACCESS + CASH-OUT HARD GATE V1

Status: MCME-044 RESEARCH COMPLETE — WAITING BRAIN ACCEPTANCE  
Owner residence: Vietnam  
Owner phone truth: Owner controls a real Vietnam mobile number (+84); no foreign phone.  
Observed official-source review: 2026-09-20

Business goal:

> FIRST REAL CASH means funds actually received on an Owner-authorized payout rail and reconciled to the affiliate payout record.

A commission, provider balance, payable status, or network `paid` flag is not sufficient.

## Canonical supporting artifacts

- `02_MONETIZATION/MCME-044_VIETNAM_ACCESS_CASHOUT_RESEARCH.md`
- `02_MONETIZATION/MCME-044_VIETNAM_CASHOUT_MATRIX.json`
- `00_PROJECT/MCME-044_OWNER_ACTION_PACKET.md`

## Hard questions

Before first-cash execution, the system must know:

1. Can truthful Vietnam identity/residency open the required platform/network?
2. Is a mobile phone required?
3. Does real Vietnam +84 work when phone verification is required?
4. Is any foreign phone required?
5. What KYC/tax/security steps are required?
6. What payout rail can actually reach an Owner-authorized Vietnam bank/payment rail?
7. What threshold/cycle/fees/FX/rejection behavior applies?
8. What later evidence proves funds actually arrived?

Unknown never becomes PASS.

## Evidence labels

- `DOCUMENTED FACT`
- `OWNER_CONFIRMATION_REQUIRED`
- `PROVIDER_SPECIFIC_UNKNOWN`
- `BLOCKED`

## MCME-044 verified findings

### Pinterest

**DOCUMENTED FACT**

- New business-account documentation uses email, password and age.
- Adding a phone number is optional generally.
- SMS 2FA requires a phone number.
- Pinterest notes 2FA is not available in all regions.

**Conclusion**

- Foreign phone: **not documented as required**.
- Vietnam +84: **not needed for initial business signup**.
- +84 for optional SMS 2FA: `OWNER_CONFIRMATION_REQUIRED`.
- Real Owner property remains unconfirmed until MCME-010.

### Awin

**DOCUMENTED FACT**

- Publisher signup collects tax residency, identity/account fields and promotional space.
- Social-media profiles may be supplied as promotional space.
- Awin user signup accepts telephone in international format.
- Awin payment settings require Awin two-step verification using email initiation + authenticator app.
- International payouts use Awin's Payoneer integration.

**OWNER_CONFIRMATION_REQUIRED**

- Vietnam tax-residency availability in Owner's exact publisher signup.
- Whether phone is mandatory in that exact flow.
- Whether +84 is accepted if requested.
- Whether Payment Details offers Vietnam destination/currency and Owner bank route.

**Conclusion**

`AWIN_ACCESS = OWNER_CONFIRMATION_REQUIRED`  
`AWIN_PAYOUT_TO_VN = OWNER_CONFIRMATION_REQUIRED`

No official evidence requires a foreign phone.

### impact.com

**DOCUMENTED FACT**

- Standard partner signup requires mobile verification.
- Country/Region is collected.
- Vietnam is explicitly included in impact.com's Southern/Southeast Asia contracting region.
- Email 2FA is the default for applicable account-user flows; authenticator app is recommended.
- Payments require tax/bank details and can require identity verification.
- Bank withdrawal supports international wire.
- USD bank-account location support is documented as "all locations".
- Minimum Autopay threshold is USD 10 equivalent.

**OWNER_CONFIRMATION_REQUIRED**

- Real +84 SMS verification.
- Owner's exact Vietnam bank/currency/wire compatibility.

**Conclusion**

`IMPACT_ACCESS = OWNER_CONFIRMATION_REQUIRED`  
`IMPACT_PAYOUT_TO_VN = OWNER_CONFIRMATION_REQUIRED`

No official evidence requires a foreign phone.

### Amazon Associates conditional

**DOCUMENTED FACT**

- Non-US Associates are supported in tax documentation.
- Account may exist without phone, but payment-details access requires OTP by SMS or voice to a registered mobile.
- Non-US payment requires tax information.
- Current international direct-deposit list does **not** include Vietnam.
- International paper check and gift card exist; gift card is not cash.

**Conclusion**

`AMAZON_ACCESS_CONDITIONAL = OWNER_CONFIRMATION_REQUIRED`  
`AMAZON_PAYOUT_TO_VN_CONDITIONAL = BLOCKED`

Reason: current official evidence does not establish direct deposit to a Vietnam bank, and Amazon does not establish that an international paper check can be converted into Owner Vietnam-bank `CASH_SETTLED`.

Do not spend Owner time here while Route A/B remain viable.

### Payoneer

**DOCUMENTED FACT — VERIFIED**

Payoneer's 2026 Vietnam-specific documentation explicitly supports:

- Country = Vietnam;
- real Vietnam mobile;
- +84 prefilled;
- omit leading zero;
- OTP by WhatsApp or SMS;
- Vietnam identity/address verification;
- Vietnam bank linkage;
- VND or eligible supported bank currency;
- withdrawal to local bank.

**Conclusion**

`PAYONEER_VN_ACCESS = VERIFIED`  
`PAYONEER_TO_VN_BANK = VERIFIED`

Specific Owner bank, exact fee and FX remain real-account observations.

### SWIFT / bank rail

Awin/Payoneer and impact.com document international wire/SWIFT paths.

The specific receiving capability of Owner's Vietnam bank/currency account remains:

`OWNER_CONFIRMATION_REQUIRED`

No bank detail may be committed to Git.

## Route decisions

### ROUTE_A — KEEP FIRST ATTEMPT

```text
Pinterest
→ Awin
→ Awin Payoneer / Global Bank Transfer
→ Vietnam bank
→ funds credited
→ CASH_SETTLED
```

Status: `OWNER_CONFIRMATION_REQUIRED`

Remaining proof is bounded and Owner-executable with truthful Vietnam information.

### ROUTE_B — KEEP FALLBACK 1

```text
Pinterest
→ impact.com
→ USD wire/EFT
→ Vietnam bank
→ funds credited
→ CASH_SETTLED
```

Status: `OWNER_CONFIRMATION_REQUIRED`

Vietnam residence is explicitly supported in impact.com's regional model; +84 and exact bank route remain Owner proof.

### ROUTE_C — BLOCKED FOR FIRST-CASH CASH-OUT

```text
Pinterest
→ Amazon Associates conditional
→ Vietnam cash rail
```

Status: `BLOCKED`

Do not treat gift cards or unsupported direct-deposit assumptions as cash.

## Direct phone answers

| Platform | Foreign phone needed? | Real +84 status |
|---|---|---|
| Pinterest | No documented requirement | Not required for initial signup; SMS 2FA unverified |
| Awin | No documented requirement | Owner confirmation required |
| impact.com | No documented requirement | Owner confirmation required |
| Amazon Associates | No documented requirement | Owner confirmation required for payment OTP |
| Payoneer | No | **Verified +84** |

## Cash-out proof contract

Future `CASH_SETTLED` requires:

- payout reference sanitized;
- payout amount/currency;
- payout issued timestamp;
- rail type;
- received amount/currency;
- receiving-rail posted timestamp;
- fee/FX if visible;
- sanitized receiving reference;
- `funds_actually_received=true`;
- `owner_authorized_payout_rail=true`;
- `reconciled_to_payout=true`.

## Five-Step reconciliation

### QUESTION
The issue is not generic international support; it is truthful Vietnam access plus actual cash arrival.

### DELETE
Delete:

- fake foreign phone;
- rented SMS/OTP;
- false residency;
- VPN identity tricks;
- unsupported Amazon cash-out assumptions;
- unnecessary PayPal dependency;
- fourth affiliate network;
- infinite research.

### SIMPLIFY
Keep:

1. Awin first.
2. impact.com fallback.
3. Amazon conditional but cash-out blocked under current evidence.

### ACCELERATE
After Brain accepts MCME-044:

`MCME-010 — Owner Pinterest property confirmation`

then:

`MCME-011 — Owner Awin access evidence`

Awin failure is recorded before impact.com fallback.

No AUTOMATE yet.

## MCME-044 recommendation

`PASS_TO_MCME_010`

Rationale:

At least two bounded routes have official Vietnam-compatible cash-out architecture, and remaining critical items are explicit Owner-action proofs using truthful Vietnam information. No route requires a fake/foreign phone under current official evidence.

This recommendation does **not** assert:

- Awin account already exists;
- impact.com account already exists;
- merchant approval exists;
- payment setup exists;
- any real commission/payout/cash exists.

## Locked policy

DO NOT:

- buy/borrow a foreign identity or phone;
- use fake country/residency;
- use temporary SMS service;
- send secrets to Work;
- infer +84 support where docs do not prove it;
- infer Vietnam payout from generic "international" language alone.

Allowed Owner return is sanitized status only:

`SUCCESS / PENDING / BLOCKED / REJECTED + observed_at + safe reference`.

## Current truth

```text
evidence = L0_NO_REAL_COMMERCIAL_EVIDENCE
Gate A = OWNER_GATED_NOT_EXECUTED
real account approvals = NONE VERIFIED
real click/sale/commission/cash = NONE VERIFIED
MCME-044 = COMPLETE_WAITING_BRAIN_ACCEPTANCE
recommended next real task after acceptance = MCME-010
```

No content production, publish, spend, account automation, KYC automation or payment automation is authorized by this gate.
