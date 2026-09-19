# MCME-044 — VIETNAM OWNER ACCESS + CASH-OUT RESEARCH

**Task:** MCME-044  
**Observed at:** 2026-09-20  
**Owner residence:** Vietnam  
**Owner phone truth:** Owner controls one real Vietnam mobile number (+84); no foreign phone.  
**Five-Step:** QUESTION → DELETE → SIMPLIFY → ACCELERATE  
**Scope:** research + fail-closed planning only; no account action performed by Work.

## 1. Business question

Can at least one truthful affiliate route be opened by an Owner resident in Vietnam and eventually terminate in **real funds received** on an Owner-authorized Vietnam payout rail?

The economic endpoint is locked:

```text
commission
→ validated/payable
→ payout issued
→ payment rail
→ Vietnam bank / Owner-authorized rail
→ funds credited
→ reconciled payout evidence
→ CASH_SETTLED
```

A network status such as `paid`, a pending/approved commission, or a payout-issued record alone is not cash.

## 2. Evidence labels

- **DOCUMENTED FACT** — supported by official provider documentation.
- **OWNER_CONFIRMATION_REQUIRED** — official docs define the path but only the Owner's real account/bank/signup flow can prove the final fact.
- **PROVIDER_SPECIFIC_UNKNOWN** — provider-specific behavior is not published or not yet visible.
- **BLOCKED** — current official evidence contradicts a required first-cash condition.

No UNKNOWN is promoted to PASS.

---

# 3. Direct answers — foreign phone vs Vietnam +84

| Platform | Foreign phone required? | Can real Vietnam +84 be used? | Current classification |
|---|---|---|---|
| Pinterest | **No documented foreign-phone requirement.** New business-account docs require email, password, age. Phone is optional generally. | **Not required for initial business signup.** +84 support for optional SMS 2FA is not explicitly documented; 2FA is not available in every region. | Initial signup: DOCUMENTED FACT; +84 SMS 2FA: OWNER_CONFIRMATION_REQUIRED |
| Awin | **No documented requirement for US/UK/foreign phone.** | Awin user signup accepts telephone in international format, but retrieved publisher docs do not explicitly prove +84 or whether phone is mandatory in the Owner's exact publisher flow. | OWNER_CONFIRMATION_REQUIRED |
| impact.com | **No documented requirement for foreign phone.** Vietnam is explicitly included in impact.com's Southern/Southeast Asia contracting region. | Standard partner signup includes mobile verification, but official docs retrieved do not explicitly state +84 acceptance. | OWNER_CONFIRMATION_REQUIRED |
| Amazon Associates US | **No documented foreign-phone requirement.** Amazon says an account may exist without phone. | Payment-details access requires OTP by SMS or voice to a registered mobile; +84 is not explicitly proven. | OWNER_CONFIRMATION_REQUIRED |
| Payoneer | **No foreign phone required.** | **Yes — VERIFIED.** Payoneer's 2026 Vietnam guides explicitly say choose Vietnam, +84 is prefilled, omit the leading 0, receive OTP by WhatsApp/SMS. | VERIFIED |

### Core answer

**There is no official evidence that a foreign phone is required for the bounded first-cash routes.**  
**A real Vietnam +84 is explicitly documented by Payoneer.**  
For Awin and impact.com, +84 must still be proven in the Owner's real signup flow because the official docs do not state it explicitly.

---

# 4. Pinterest access

## DOCUMENTED FACT

Official Pinterest Business documentation for a new business account lists:

- email;
- password;
- age;
- profile/business description steps.

Pinterest separately states adding a phone number is optional.

Pinterest SMS 2FA requires a phone number and a country/region code. Pinterest also notes that 2FA is not available in all regions.

## OWNER_CONFIRMATION_REQUIRED

- Actual Owner Pinterest property has not yet been confirmed.
- +84 SMS behavior for optional 2FA is not explicitly documented.

## Decision

`PINTEREST_ACCESS = OWNER_CONFIRMATION_REQUIRED` only because the real Owner property is still unconfirmed. There is **no foreign-phone blocker** for initial business-account creation in the official flow.

MCME-010 remains the correct next real task.

---

# 5. Awin access

## DOCUMENTED FACT

Awin's current publisher signup flow requests:

- tax residency;
- name;
- email;
- password;
- primary region / promotional type;
- promotional space.

Awin explicitly allows a social-media profile as promotional space.

A separate Awin user-account signup page requests a telephone number in international format.

Awin's current 2SV process:

- begins with email verification;
- uses an authenticator app;
- is required to access Payment Details.

This means a foreign SMS number is **not** the documented Awin 2SV mechanism for payment settings.

## OWNER_CONFIRMATION_REQUIRED

Official text retrieved does not prove:

- Vietnam appears as an accepted tax-residency value in the Owner's live publisher flow;
- whether telephone is mandatory in that exact publisher onboarding flow;
- whether a Vietnam +84 is accepted if telephone is requested.

## Decision

`AWIN_ACCESS = OWNER_CONFIRMATION_REQUIRED`.

This is not BLOCKED. It is a bounded Owner test.

---

# 6. Awin cash-out to Vietnam

## DOCUMENTED FACT

Awin states that international publisher payments are handled via Payoneer.

Awin's current payment-method documentation says:

- USD to banks outside the US → Payoneer;
- GBP outside UK → Payoneer;
- EUR outside EU/UK → Payoneer;
- international transfers may be local-currency transfer or international wire/SWIFT;
- publisher must set up Payoneer **through the Awin account**.

Important architecture fact:

> Awin's Payoneer setup does not mean a normal standalone Payoneer balance is necessarily used. Awin's guide says the integration saves payment details so Awin can transfer to the publisher's bank; an existing standalone Payoneer account cannot simply be linked as a substitute.

Awin minimum threshold documentation currently states:

- USD: $20 minimum;
- GBP: £20;
- EUR: €20;
- other currencies: equivalent rules;
- payments are processed twice per month.

Awin terms state FX/conversion or third-party conversion costs can be borne by the publisher.

## OWNER_CONFIRMATION_REQUIRED

The following are not yet observed in the Owner's live Awin payment setup:

- destination country Vietnam;
- exact destination currency;
- exact Payoneer route offered;
- actual Owner Vietnam bank compatibility;
- actual route-specific fee/FX.

## Decision

`AWIN_PAYOUT_TO_VN = OWNER_CONFIRMATION_REQUIRED`.

The route is credible and bounded, not proven end-to-end yet.

---

# 7. impact.com access

## DOCUMENTED FACT

impact.com's partner signup is not email-only.

Current official flow:

1. signup by email or supported social sign-in;
2. **verify mobile number**;
3. choose business category;
4. add/verify promotion method;
5. provide account information including Country/Region;
6. verify email.

impact.com also explicitly states that partners in **Southern and South East Asia including Vietnam** contract under Impact Tech Singapore PTE. Ltd.

For account 2FA, impact.com states:

- email is the default authentication method for applicable account-user flow;
- authenticator app is recommended;
- unusual device/activity can trigger additional verification.

## OWNER_CONFIRMATION_REQUIRED

- The docs do not explicitly say "+84 is accepted."
- Therefore real SMS delivery to Owner's +84 must be tested truthfully.

## Decision

`IMPACT_ACCESS = OWNER_CONFIRMATION_REQUIRED`.

Vietnam residency itself is documented; the remaining critical test is practical +84 verification and actual account approval.

---

# 8. impact.com payout to Vietnam

## DOCUMENTED FACT

impact.com payment docs require:

- applicable tax documentation;
- phone/security verification where prompted;
- verified bank details;
- sometimes identity verification.

Payment methods include:

- ACH where applicable;
- international wire;
- PayPal.

For this route, **bank wire/EFT is the intended path**; PayPal is not required.

impact.com currently documents:

- minimum Autopay threshold: **$10 USD or equivalent**;
- threshold-based payout or fixed-day schedule;
- bank wire processing normally 3–5 business days after paystub clears;
- wire fee is currency-specific;
- PayPal costs 2% when used;
- bank detail changes impose a 48-hour payment hold;
- intermediary-bank routing can fail and return if the user tries to send to an intermediary rather than the final destination account.

impact.com's currency table states:

- **USD: supported bank-account locations = all locations**;
- USD is supported for wire withdrawal.

The same documentation set explicitly includes Vietnam in impact.com's contracting region.

## OWNER_CONFIRMATION_REQUIRED

- Owner's specific Vietnam bank and selected currency/SWIFT capability must be verified in the real account/bank setup.
- +84 mobile verification must still pass.

## Decision

`IMPACT_PAYOUT_TO_VN = OWNER_CONFIRMATION_REQUIRED`.

This is the best documented fallback cash-out route if Awin cannot be established.

---

# 9. Amazon Associates conditional fallback

## Access

### DOCUMENTED FACT

Amazon Associates official tax docs explicitly address non-US Associates.

Amazon states an Associates account can exist without a phone number, but payment-detail access requires OTP to a registered mobile by SMS or voice.

Non-US Associates must complete applicable tax information; Amazon's US docs reference W-8BEN/tax interview requirements for non-US persons.

### OWNER_CONFIRMATION_REQUIRED

- Vietnam-specific signup acceptance is not explicitly stated.
- +84 OTP support is not explicitly stated.

## Cash-out

### DOCUMENTED FACT

Amazon's current international direct-deposit help lists supported bank/currency regions. **Vietnam is not in the documented list.**

Amazon still offers international:

- gift card;
- paper check.

But gift card is not cash.

The international paper-check path does not prove a Vietnam bank can cash/collect the check into Owner funds.

### BLOCKED

For the required first-cash definition:

`AMAZON_PAYOUT_TO_VN_CONDITIONAL = BLOCKED`

under current official evidence.

Amazon is not allowed to rescue the first-cash path via an unsupported assumption about Vietnam direct deposit, Payoneer, or check cashability.

---

# 10. Payoneer Vietnam access

## DOCUMENTED FACT — VERIFIED

Payoneer's 2026 Vietnam-specific guides cover both business and individual registration.

For an individual in Vietnam, official guidance states:

- choose Country = Vietnam;
- provide email;
- add mobile number;
- +84 is prefilled;
- omit leading zero from a domestic 09... number;
- receive OTP via WhatsApp or SMS;
- continue identity/address verification;
- link a Vietnam bank account.

The same guidance describes:

- Vietnam-issued identity documents;
- proof of address;
- selfie/identity verification;
- Vietnam bank linkage;
- VND or eligible foreign-currency bank account depending actual setup.

Payoneer security docs also state 2-step verification may be used for account actions.

## Decision

`PAYONEER_VN_ACCESS = VERIFIED`

and:

`PAYONEER_TO_VN_BANK = VERIFIED`

at generic provider capability level.

The Owner's exact bank/fee/FX remains a real-account observation, not an assumption.

---

# 11. Payoneer → Vietnam bank

## DOCUMENTED FACT

Payoneer Vietnam documentation states withdrawals can be made to local bank accounts.

Current official materials describe:

- bank country, bank name, account type and currency setup;
- local-currency withdrawal;
- fee/FX shown before confirmation;
- most withdrawals arriving same day or within about two business days depending route;
- supported local-bank withdrawals in many countries including Vietnam.

Payoneer's public pricing varies by:

- currency;
- country;
- conversion;
- route.

Therefore no single fee should be invented for the future experiment.

## CASH_SETTLED proof

Payoneer "sent" or Awin "paid" is not enough.

Required later:

- affiliate payout reference;
- amount/currency sent;
- Payoneer/rail transfer reference sanitized;
- amount/currency received;
- receiving-bank posted timestamp;
- fees/FX if visible;
- reconciliation link between payout and received funds.

---

# 12. SWIFT / bank rail

SWIFT is relevant because:

- Awin/Payoneer may use SWIFT for cross-border USD/EUR/GBP;
- impact.com supports international wire.

Provider support does not prove a specific Vietnamese bank/currency account will accept the transfer.

Therefore:

`SWIFT_BANK_RAIL_VN = OWNER_CONFIRMATION_REQUIRED`.

The Owner must verify the final bank/currency route privately when the winning network is known.

No bank account number or SWIFT credentials belong in Git.

---

# 13. Route decisions

## ROUTE_A — KEEP FIRST ATTEMPT

```text
Pinterest
→ Awin
→ Awin Payoneer / Global Bank Transfer
→ Vietnam bank
→ funds credited
→ CASH_SETTLED
```

Status: **OWNER_CONFIRMATION_REQUIRED**

Remaining proof is bounded:

1. Awin truthful Vietnam tax-residency/signup works;
2. real +84 works if phone requested;
3. payment setup offers Vietnam destination and Owner bank route.

No foreign number is documented as required.

## ROUTE_B — KEEP FALLBACK 1

```text
Pinterest
→ impact.com
→ USD wire/EFT
→ Vietnam bank
→ funds credited
→ CASH_SETTLED
```

Status: **OWNER_CONFIRMATION_REQUIRED**

This has stronger official Vietnam residence evidence than Awin:

- Vietnam is explicitly included in impact.com's regional contracting model;
- USD is documented for all bank-account locations;
- international wire is a documented withdrawal method.

Remaining proof:

1. real +84 signup verification;
2. actual Owner bank/currency route.

## ROUTE_C — BLOCK FOR FIRST-CASH CASH-OUT

```text
Pinterest
→ Amazon Associates conditional
→ ??? Vietnam cash rail
```

Status: **BLOCKED**

Reason:

- current official direct-deposit country list excludes Vietnam;
- gift card is not cash;
- check-to-Vietnam-bank settlement is not proven.

Do not spend Owner time on Route C while A/B remain viable.

---

# 14. Five-Step

## QUESTION

The real question was not "Can a Vietnamese person see these signup pages?" It was:

> Can truthful Vietnam identity/contact details produce an affiliate account and a credible path to funds actually credited to a Vietnam Owner-authorized rail?

## DELETE

Deleted from first-cash path:

- fake foreign phone;
- rented SMS/OTP;
- foreign-residency fiction;
- VPN identity tricks;
- Amazon as a cash-out rescue assumption;
- PayPal as an unnecessary extra dependency;
- fourth affiliate network;
- any "international payout" claim without Vietnam-specific or all-location official evidence.

## SIMPLIFY

Keep only:

1. **Route A:** Awin → Payoneer/GBT → Vietnam bank.
2. **Route B:** impact.com → bank wire/EFT → Vietnam bank.
3. Amazon remains conditional but is currently cash-out BLOCKED.

## ACCELERATE

The first real account/property step should remain:

`MCME-010 — Owner Pinterest property confirmation`.

Then:

`MCME-011 — Owner Awin access evidence`.

Only if Awin's bounded path fails do we test impact.com.

---

# 15. MCME-044 gate decision

## Result

**PASS_TO_MCME_010**

Why PASS is allowed:

- no bounded route requires a fake/foreign phone under current official evidence;
- Pinterest initial access has no mandatory phone in documented signup;
- Payoneer explicitly supports Vietnam +84 and Vietnam bank linkage;
- Awin's international payout architecture is Payoneer-based and has a bounded Owner verification path;
- impact.com explicitly includes Vietnam in its regional model and documents USD withdrawal to all bank locations by wire-capable methods;
- all remaining critical gaps are explicit Owner-action items that can be answered truthfully during the existing MCME-010→028 critical path.

This PASS does **not** mean Awin or impact.com account approval already exists.

---

# 16. Owner evidence format

When an Owner step occurs, return only sanitized facts such as:

```text
platform=AWIN
step=publisher_signup
status=SUCCESS | PENDING | BLOCKED
country=Vietnam
phone_requested=YES | NO
plus84_result=SUCCESS | NOT_TESTED | BLOCKED
observed_at=<timestamp>
safe_reference=<public/sanitized reference if available>
```

Never return:

- password;
- OTP/MFA/recovery code;
- cookie/session;
- CAPTCHA artifact;
- bank account number;
- tax ID;
- identity document;
- private payout ID;
- raw affiliate/tracking token.

---

# 17. Future CASH_SETTLED proof fields

Required evidence later:

- network/program;
- sanitized commission record;
- validated/payable amount;
- payout-issued amount and currency;
- payout-issued timestamp;
- sanitized payout reference;
- rail type;
- amount received;
- currency received;
- bank/payment-rail posted timestamp;
- visible fee;
- visible FX rate/converted amount;
- sanitized receiving-rail reference;
- `funds_actually_received=true`;
- `owner_authorized_payout_rail=true`;
- `reconciled_to_payout=true`.

Only then may MCME emit `CASH_SETTLED`.

---

# 18. Official source register

Observed 2026-09-20.

### Pinterest
- https://help.pinterest.com/en/business/article/get-a-business-account
- https://help.pinterest.com/en/article/how-pinterest-uses-your-phone-number
- https://help.pinterest.com/en/article/two-factor-authentication

### Awin
- https://success.awin.com/articles/en_US/Knowledge/How-do-I-join-Awin-as-a-Publisher
- https://ui.awin.com/publisher-signup/en/awin/step1
- https://ui.awin.com/user-signup?setLocale=en_GB
- https://success.awin.com/articles/en_US/Knowledge/How-to-activate-and-deactivate-the-Two-Step-Verification
- https://success.awin.com/articles/en_US/Knowledge/what-are-the-available-payment-methods
- https://success.awin.com/articles/en_US/Knowledge/International-Payment-Method-FAQs
- https://success.awin.com/articles/en_US/Knowledge/How-to-set-up-a-Payoneer-Account
- https://success.awin.com/articles/en_US/Knowledge/What-are-the-payment-thresholds
- https://success.awin.com/articles/en_US/Knowledge/When-will-I-receive-payment

### impact.com
- https://help.impact.com/partner/what-would-you-like-to-learn-about/getting-started/sign-up-as-a-partner-on-impactcom
- https://help.impact.com/other/reference-documentation/understanding-impactcoms-trading-models
- https://help.impact.com/partner/what-would-you-like-to-learn-about/account-management/account-settings/manage-2fa-for-partner-accounts
- https://help.impact.com/partner/what-would-you-like-to-learn-about/account-management/account-settings/user-management/verify-your-identity-as-a-partner
- https://help.impact.com/partner/what-would-you-like-to-learn-about/platform-features/finance/payments-withdrawals-and-balance/how-do-partners-get-paid
- https://help.impact.com/partner/what-would-you-like-to-learn-about/platform-features/finance/payments-withdrawals-and-balance/withdraw-funds-to-your-bank-account
- https://help.impact.com/other/reference-documentation/supported-currencies-and-timezones
- https://help.impact.com/partner/what-would-you-like-to-learn-about/platform-features/finance/payment-requirements-explained-for-partners
- https://help.impact.com/partner/what-would-you-like-to-learn-about/platform-features/finance/payments-withdrawals-and-balance/limitations-of-withdrawals-via-intermediary-banks

### Amazon Associates
- https://affiliate-program.amazon.com/help/node/topic/GP75GP58NT9U34YH
- https://affiliate-program.amazon.com/help/node/topic/G8VUMS6GTBCR9RGV
- https://affiliate-program.amazon.com/help/node/topic/GGD9H76RMDDNEWAE
- https://affiliate-program.amazon.com/help/operating/policies
- https://affiliate-program.amazon.com/help/topic/t3/a3
- https://affiliate-program.amazon.com/help/node/topic/GYJB2LE2AB473W2L

### Payoneer
- https://www.payoneer.com/vi/resources/how-to-use-payoneer/payoneer-registration-guide-for-individual-entrepreneurs/
- https://www.payoneer.com/vi/resources/instructions-for-registering-to-a-payoneer-account/
- https://www.payoneer.com/vi/about/security-center/
- https://www.payoneer.com/vi/withdraw-funds/
- https://www.payoneer.com/vi/resources/business/cach-rut-tien-tu-payoneer-ve-tai-khoan-ngan-hang-cua-ban/
- https://www.payoneer.com/vi/about/pricing/

## Hard stop

MCME-044 does not create any account, submit OTP, complete KYC/tax/payment setup, create Pins, publish, click, buy, or spend.

Do not auto-run MCME-010. Brain acceptance is still required.
