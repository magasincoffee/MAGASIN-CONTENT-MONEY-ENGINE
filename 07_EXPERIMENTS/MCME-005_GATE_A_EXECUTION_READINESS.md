# MCME-005 — GATE A EXECUTION READINESS + EVIDENCE CONTRACT

**Task:** MCME-005  
**Repository:** `magasincoffee/MAGASIN-CONTENT-MONEY-ENGINE`  
**Canonical input:** MCME-004 accepted by Brain at commit `29f203595afcd63a075d5f62f8638c22169b3c38`  
**Five-Step stage:** DELETE → SIMPLIFY → ACCELERATE  
**Scope:** execution-readiness contract only. No account creation/login/application, no credentials, no MFA/CAPTCHA, no KYC/tax/banking/payment action, no merchant contact, no production creative, no publishing, no spend, no fake/test/self-purchase, and **no Minimum Content Factory specification**.

---

# 1. Fixed experiment inputs

These inputs remain locked:

```text
Market:
  United States

Language:
  English

Distribution:
  Pinterest organic Pins

Monetization:
  Affiliate commerce

Niche:
  Small-space kitchen organization

First sub-problem:
  Fridge storage / fit

Canonical format:
  Static 2:3 original problem-solution checklist Pin

Gate B minimum:
  3 Pins

Network order:
  Awin
  → impact.com
  → Amazon Associates (conditional)

SaydiVoice:
  DELETED

Video:
  DELETED

Minimum Content Factory:
  BLOCKED until real Gate A + interaction evidence
```

MCME-005 changes only the **operational readiness** of Gate A.

---

# 2. Gate A state machine

## 2.1 State definitions

### `NOT_STARTED`

Gate A has not begun.

Invariant:
- no network relationship evidence has been collected for the current attempt;
- no merchant path is qualified;
- no content production may begin.

### `OWNER_ACTION_REQUIRED`

A required step can only be performed by Owner because it involves account ownership, legal acceptance, identity, tax, payment, or another protected boundary.

Examples:
- joining a network;
- accepting network/merchant terms;
- merchant application;
- KYC/tax/payment setup.

Work/Robot may describe the required action and required evidence, but may not perform it.

### `WAIT_OWNER`

A previously requested Owner action is pending, or the external platform is waiting on approval/review triggered by Owner.

Invariant:
- UNKNOWN/BLOCKED evidence stays non-PASS;
- Robot does not retry account actions;
- Robot does not create substitute accounts or alternate identities.

### `NETWORK_READY`

The current network attempt is real and usable enough to evaluate merchant programs.

Minimum evidence:
- publisher/network relationship is `VERIFIED`;
- actual Owner/property can use the network;
- network relationship is not merely a public-program assumption.

This does **not** mean a merchant is approved.

### `MERCHANT_READY`

Exactly one real merchant/program candidate for the selected sub-problem has a verified relationship state sufficient to evaluate promotion and tracking.

Minimum evidence:
- merchant/program identity known;
- relationship is joined/approved/otherwise actually usable;
- US geography fit verified;
- Pinterest/social promotional method verified as permitted.

### `TRACKING_READY`

The merchant path can generate a real trackable affiliate destination.

Minimum evidence:
- tracking-link capability verified;
- intended destination resolves to the merchant/category/product-family;
- direct/deep-link rule verified;
- Pin/sub-ID attribution capability marked `VERIFIED`, `UNKNOWN`, or `BLOCKED` explicitly;
- no UNKNOWN critical tracking field is treated as PASS.

### `VALIDATION_TERMS_READY`

The commissionable event and validation truth are known.

Minimum evidence:
- commissionable merchant action verified;
- pending/approved/validated state semantics known;
- locking/validation process known;
- reversal/return treatment known.

No commission rate or cookie duration must be invented; if relevant and not visible, status remains `UNKNOWN`.

### `PAYOUT_READY`

A real Owner-authorized payout path is feasible.

Minimum evidence:
- payout threshold/cycle known or explicitly evidenced as not applicable;
- required payout rail type known;
- Owner confirms the required legal/tax/payment setup is complete enough for payout;
- no bank/account/private payout identifiers are stored in GitHub.

### `RIGHTS_DISCLOSURE_READY`

The first static-Pin experiment can comply with rights and disclosure rules.

Minimum evidence:
- affiliate disclosure requirement known;
- Pinterest/social promotional disclosure requirement known;
- merchant logo/photo/creative rights known;
- if merchant asset rights are uncertain, experiment is constrained to original graphics/text only.

### `PASS`

Gate A has one real qualified merchant money path.

PASS requires all of:

```text
NETWORK_READY
+ MERCHANT_READY
+ TRACKING_READY
+ VALIDATION_TERMS_READY
+ PAYOUT_READY
+ RIGHTS_DISCLOSURE_READY
```

**No critical evidence item may be UNKNOWN, BLOCKED or FAIL.**

PASS authorizes only the Gate B handoff contract.  
PASS does not authorize publishing by itself.

### `FAIL`

Terminal Gate A failure for the current niche after bounded fallback is exhausted, or a fatal condition invalidates the route.

Examples:
- all allowed network attempts exhausted without one qualified path;
- no feasible payout rail exists within Owner boundaries;
- Pinterest/social promotion is prohibited across surviving merchant paths;
- tracking/validation truth cannot be established;
- compliance/rights burden invalidates the minimum static format.

FAIL means:
- **KILL/DELETE the niche before Pin production**;
- return to Brain;
- no automatic niche switch.

---

## 2.2 Legal transitions

```text
NOT_STARTED
  → OWNER_ACTION_REQUIRED

OWNER_ACTION_REQUIRED
  → WAIT_OWNER
  → NETWORK_READY
  → FAIL

WAIT_OWNER
  → OWNER_ACTION_REQUIRED
  → NETWORK_READY
  → MERCHANT_READY
  → FAIL

NETWORK_READY
  → OWNER_ACTION_REQUIRED
  → WAIT_OWNER
  → MERCHANT_READY
  → FAIL
  → OWNER_ACTION_REQUIRED   # next bounded network fallback

MERCHANT_READY
  → OWNER_ACTION_REQUIRED
  → WAIT_OWNER
  → TRACKING_READY
  → FAIL
  → NETWORK_READY          # try alternate merchant inside same network, if bounded slot remains
  → OWNER_ACTION_REQUIRED  # fallback network

TRACKING_READY
  → VALIDATION_TERMS_READY
  → WAIT_OWNER
  → FAIL
  → NETWORK_READY
  → OWNER_ACTION_REQUIRED

VALIDATION_TERMS_READY
  → OWNER_ACTION_REQUIRED
  → WAIT_OWNER
  → PAYOUT_READY
  → FAIL
  → NETWORK_READY
  → OWNER_ACTION_REQUIRED

PAYOUT_READY
  → RIGHTS_DISCLOSURE_READY
  → WAIT_OWNER
  → FAIL

RIGHTS_DISCLOSURE_READY
  → PASS
  → FAIL

PASS
  → terminal for MCME-005 contract
  → Gate B handoff only after Brain authorization

FAIL
  → terminal for Gate A
  → Brain review
```

### Illegal transitions

The following are prohibited:

```text
NOT_STARTED → PASS
NETWORK_READY → PASS
MERCHANT_READY → PASS
TRACKING_READY → PASS
UNKNOWN → VERIFIED without evidence
BLOCKED → PASS
FAIL → PASS without a new Brain-authorized Gate A run
PASS → production/publish automatically
```

---

## 2.3 Fail-closed behavior

1. **UNKNOWN is not PASS.**
2. **BLOCKED is not PASS.**
3. Missing evidence is `UNKNOWN`, never inferred.
4. Public program existence does not equal Owner/network/merchant approval.
5. A pending merchant application is `WAIT_OWNER`, not `MERCHANT_READY`.
6. A generated link without verified commissionable action/validation/payout is not Gate A PASS.
7. A payout method name without Owner-confirmed feasibility is not `PAYOUT_READY`.
8. If evidence sources conflict, mark the field `BLOCKED` and request resolution; do not choose the favorable source silently.
9. Robot/Work may not cross an Owner boundary to convert UNKNOWN/BLOCKED into VERIFIED.

---

# 3. Minimum Owner action sequence

The sequence is designed to minimize back-and-forth and avoid unnecessary setup on a network that may fail early.

## Step 0 — Confirm the Pinterest property once

**Why needed**  
Gate A must evaluate the real promotional property, not an abstract Pinterest account.

**Owner does/sees**
- confirm the Pinterest account/property that would be used;
- confirm it is Owner-authorized for MCME;
- if a network asks for promotional properties, add the real Pinterest property as required.

**Sanitized evidence Owner may return**
- `property_type = Pinterest`;
- `property_authorized = true`;
- sanitized profile URL/handle if it is intended to be public;
- date/time checked.

**Never return/commit**
- password;
- session cookie;
- MFA/OTP;
- recovery codes;
- private device/session data.

---

# 4. Network attempt 1 — Awin

## A1 — Establish real network relationship

**Why needed**  
Awin is the first network in the locked order. Public advertiser listings alone cannot prove Owner eligibility.

**Owner does/sees**
- join/sign in to Awin using Owner-controlled credentials;
- complete any account/legal steps required by Awin;
- if Awin requires identity/tax/payment steps at this stage, Owner completes them directly.

**Sanitized evidence**
- `network = Awin`;
- `network_relationship = active | pending | rejected | blocked`;
- `publisher_property_accepted = true/false/unknown`;
- `checked_at`;
- sanitized screenshot/text summary with private fields redacted, if needed.

**Never commit**
- username/email if not intentionally public;
- password;
- API secret;
- tax ID;
- identity document;
- bank details;
- payout account identifier.

**State**
- active → `NETWORK_READY`;
- pending → `WAIT_OWNER`;
- rejected/terminal incompatible → advance fallback algorithm.

## A2 — Qualify merchant candidate 1, then at most candidate 2

**Why needed**  
Gate A requires one real fridge-storage merchant path, not generic network access.

**Owner does/sees**
- search/join/apply to a relevant US merchant program;
- verify whether Pinterest/social promotion is allowed;
- verify geography and relationship state.

**Sanitized evidence**
- merchant/program public name;
- program/network identifier if non-sensitive;
- relationship state;
- Pinterest/social permission status;
- US geography status;
- source timestamp.

**Never commit**
- private application notes containing personal data;
- private messages;
- internal merchant contact details not intended for publication.

## A3 — Owner completes payout/legal setup only after a viable merchant path exists, unless Awin requires it earlier

**Why needed**  
Avoid unnecessary payment setup before merchant feasibility is known.

**Owner does/sees**
- complete KYC/tax/payment requirements directly;
- confirm payout method is accepted and setup is complete enough for future payout.

**Sanitized evidence**
- `payout_setup_complete = true/false`;
- `payout_rail_type = bank | PayPal | Payoneer | other_allowed`;
- threshold/cycle facts if visible;
- checked timestamp.

**Never commit**
- bank/account number;
- routing number;
- PayPal/Payoneer private ID;
- tax number;
- identity document.

---

# 5. Network attempt 2 — impact.com fallback

Use this only if Awin cannot produce Gate A PASS within its bounded candidate slots.

## I1 — Establish real impact.com relationship

**Owner does/sees**
- join/sign in;
- accept required terms;
- complete protected verification if required.

**Sanitized evidence**
- same network-relationship fields as Awin.

## I2 — Qualify merchant candidate 1, then at most candidate 2

Public evidence from MCME-003/004 identifies OXO as a plausible public Impact path, but **approval must not be pre-filled**.

Owner verifies:
- real program relationship;
- Pinterest/social permission;
- US availability;
- tracking-link capability;
- validation/reversal terms;
- payout feasibility;
- asset/disclosure rules.

## I3 — Complete payout/legal setup only when needed

Same privacy and evidence rules as Awin.

---

# 6. Network attempt 3 — Amazon Associates conditional fallback

Attempt only if:

```text
Awin failed bounded qualification
AND
impact.com failed bounded qualification
AND
the actual Owner property/traffic configuration is eligible for Amazon under current terms
```

If Amazon eligibility itself is UNKNOWN/BLOCKED and cannot be resolved without disallowed workaround, Gate A does not PASS.

Owner actions/evidence/privacy rules are the same:
- account/legal relationship;
- eligible property;
- permitted traffic/link method;
- commissionable action/validation;
- payout feasibility;
- rights/disclosure.

---

# 7. Implementation-ready evidence schema

The contract below is normative.

```yaml
schema_version: mcme.gate-a-evidence.v1

gate:
  task_id: MCME-005
  experiment_id: string
  state: NOT_STARTED | OWNER_ACTION_REQUIRED | NETWORK_READY | MERCHANT_READY | TRACKING_READY | VALIDATION_TERMS_READY | PAYOUT_READY | RIGHTS_DISCLOSURE_READY | PASS | FAIL | WAIT_OWNER
  network_attempt_index: 1 | 2 | 3
  network_name: Awin | impact.com | Amazon Associates
  merchant_candidate_index: 1 | 2
  updated_at: ISO-8601
  decision_reason: sanitized string

status_enum:
  - VERIFIED
  - UNKNOWN
  - BLOCKED
  - FAIL

evidence_item:
  status: VERIFIED | UNKNOWN | BLOCKED | FAIL
  value_sanitized: scalar | enum | null
  source_type: public_doc | account_ui | program_terms | network_report | owner_attestation | sanitized_capture
  source_reference_sanitized: string | null
  observed_at: ISO-8601 | null
  confidence: HIGH | MEDIUM | LOW
  notes_sanitized: string | null

publisher_property:
  property_type: evidence_item
  property_authorized: evidence_item
  property_public_reference: evidence_item
  network_property_accepted: evidence_item

network_relationship:
  network_name: evidence_item
  publisher_relationship_state: evidence_item
  network_usable_for_owner: evidence_item

merchant_relationship:
  merchant_name: evidence_item
  program_public_identifier: evidence_item
  relationship_state: evidence_item
  merchant_usable_now: evidence_item

promotion_permissions:
  allowed_geography_us: evidence_item
  pinterest_social_allowed: evidence_item
  organic_social_allowed: evidence_item
  direct_link_allowed: evidence_item
  deep_link_allowed: evidence_item
  bridge_page_required: evidence_item

tracking:
  tracking_link_capability: evidence_item
  tracking_link_method: evidence_item
  destination_type: evidence_item
  pin_subid_supported: evidence_item
  attribution_key_method: evidence_item
  reporting_clicks_available: evidence_item
  reporting_actions_available: evidence_item
  secret_link_reference_external: evidence_item

commission_truth:
  commissionable_action: evidence_item
  pending_state_defined: evidence_item
  validated_state_defined: evidence_item
  payable_state_defined: evidence_item
  validation_locking_rule: evidence_item
  reversal_return_rule: evidence_item
  cookie_attribution_rule: evidence_item
  commission_rate: evidence_item

payout:
  payout_threshold: evidence_item
  payout_cycle: evidence_item
  payout_rail_type: evidence_item
  owner_payout_setup_feasible: evidence_item
  owner_payout_setup_complete: evidence_item
  payout_fees_known: evidence_item

rights_disclosure:
  merchant_photo_rights: evidence_item
  merchant_logo_rights: evidence_item
  approved_creative_rights: evidence_item
  original_graphics_allowed: evidence_item
  affiliate_disclosure_requirement: evidence_item
  required_disclosure_wording: evidence_item
  pinterest_disclosure_compatible: evidence_item

gate_b_handoff:
  merchant_program_public_id: string | null
  destination_category_public_ref: string | null
  tracking_link_generation_method: string | null
  secret_tracking_link_ref_external: string | null
  allowed_link_method: direct | deep | bridge_required | unknown
  disclosure_requirement_sanitized: string | null
  asset_rights_constraint_sanitized: string | null
  attribution_key_method: string | null
  observation_constraints_sanitized: string | null
```

## Schema rules

1. Every material field carries its own status.
2. A field with no evidence is `UNKNOWN`.
3. A field that cannot proceed until Owner acts is `BLOCKED`.
4. A field contradicted by real terms is `FAIL`.
5. `VERIFIED` requires a source and observation timestamp.
6. `confidence=LOW` cannot satisfy a critical PASS field unless Brain explicitly accepts the evidence source.
7. Secret/private values are never stored directly in `value_sanitized`.
8. The evidence record may reference an external secret handle, but the secret itself is outside GitHub.

---

# 8. Evidence privacy / redaction contract

## Never store in GitHub

Absolute prohibition:

- passwords;
- passphrases;
- session cookies;
- bearer tokens;
- API secrets;
- affiliate private tracking tokens if not intended to be public yet;
- MFA codes;
- OTPs;
- recovery codes;
- CAPTCHA artifacts;
- tax IDs / SSN / TIN / EIN where private;
- bank account numbers;
- routing numbers;
- card numbers;
- private PayPal/Payoneer/banking identifiers;
- identity documents;
- selfies/video verification;
- date of birth;
- home address unless intentionally public and necessary;
- private phone number;
- private email unless explicitly intended for repository publication;
- private merchant messages containing personal data.

## Allowed sanitized evidence

Examples:

```text
network_relationship = active
merchant_relationship = approved
pinterest_social_allowed = true
direct_link_allowed = true
validation_rule_known = true
payout_rail_type = bank
payout_setup_complete = true
checked_at = 2026-...
source = sanitized account UI capture
```

## Redaction rules

- redact personal identifiers before saving a capture;
- crop to the smallest relevant UI fragment;
- store factual status, not full account pages;
- do not store partial bank/tax/ID values as "proof";
- do not hash passwords/tokens and commit the hash — secret digests are still prohibited;
- a digest may be used only for a **sanitized evidence artifact** whose contents are already safe to store.

---

# 9. Bounded network fallback algorithm

The fallback algorithm is finite by design.

## Limits

```text
Awin:
  max merchant candidates evaluated = 2

impact.com:
  max merchant candidates evaluated = 2

Amazon Associates:
  max merchant paths evaluated = 1
  only if conditional eligibility is VERIFIED

Total automatic Gate A candidate evaluations:
  maximum = 5
```

These are process-control caps, not market-performance estimates.

## Algorithm

```text
START
  network = Awin
  merchant_slot = 1

FOR current network:
  if Owner/network relationship is pending:
    WAIT_OWNER

  if Owner/network relationship is terminally rejected/incompatible:
    FALLBACK_NETWORK

  evaluate merchant candidate

  if merchant relationship pending:
    WAIT_OWNER

  if merchant candidate has a critical FAIL:
    if another merchant slot remains in same network:
      evaluate next candidate
    else:
      FALLBACK_NETWORK

  if any critical evidence is UNKNOWN because Owner must act:
    OWNER_ACTION_REQUIRED / WAIT_OWNER

  if all critical evidence becomes VERIFIED:
    PASS

FALLBACK_NETWORK:
  Awin → impact.com → Amazon conditional

  if Amazon conditional eligibility is not VERIFIED:
    FAIL

  if all bounded attempts are exhausted:
    FAIL
    KILL NICHE
    STOP

NO automatic search beyond the caps.
NO infinite retry.
NO silent expansion to a new network.
NO niche switch without Brain.
```

## When to continue in the same network

Continue only when:
- network relationship is usable;
- current candidate failed for merchant-specific reasons;
- one bounded candidate slot remains.

## When to fallback

Fallback when:
- network relationship is terminally incompatible;
- both merchant slots fail;
- tracking/validation/payout rules make all evaluated merchant paths unusable.

## When to `WAIT_OWNER`

Use `WAIT_OWNER` when:
- application/review is pending;
- Owner must accept terms;
- Owner must complete KYC/tax/payment;
- Owner must resolve a protected account question.

## When Gate A is `FAIL`

Gate A FAIL when:
- bounded fallback exhausted;
- Amazon conditional path is unavailable after Awin/impact fail;
- a fatal policy/payment/rights issue invalidates all allowed paths.

## When to KILL niche

KILL `Fridge storage / fit` when Gate A reaches terminal `FAIL`.

Do not produce Pins first and "see what happens."

---

# 10. Real merchant qualification record template

Copy this template for exactly one merchant candidate at a time.

```yaml
merchant_qualification_record:
  record_version: mcme.merchant-qualification.v1
  network: null
  merchant_name: null
  program_public_identifier: null
  merchant_candidate_index: null

  relationship:
    status: UNKNOWN
    relationship_state_sanitized: null
    source_reference_sanitized: null
    observed_at: null

  geography:
    status: UNKNOWN
    us_allowed: null
    source_reference_sanitized: null

  promotion:
    pinterest_social_allowed:
      status: UNKNOWN
      value_sanitized: null
    direct_link_allowed:
      status: UNKNOWN
      value_sanitized: null
    deep_link_allowed:
      status: UNKNOWN
      value_sanitized: null

  tracking:
    tracking_link_capability:
      status: UNKNOWN
      value_sanitized: null
    pin_subid_supported:
      status: UNKNOWN
      value_sanitized: null
    destination_type:
      status: UNKNOWN
      value_sanitized: null

  commission:
    commissionable_action:
      status: UNKNOWN
      value_sanitized: null
    validation_locking:
      status: UNKNOWN
      value_sanitized: null
    reversals_returns:
      status: UNKNOWN
      value_sanitized: null

  payout:
    threshold_cycle:
      status: UNKNOWN
      value_sanitized: null
    payout_feasible:
      status: UNKNOWN
      value_sanitized: null

  rights_disclosure:
    merchant_asset_rights:
      status: UNKNOWN
      value_sanitized: null
    original_graphics_allowed:
      status: UNKNOWN
      value_sanitized: null
    disclosure_requirement:
      status: UNKNOWN
      value_sanitized: null

  decision:
    result: UNKNOWN   # PASS | FAIL | UNKNOWN | BLOCKED
    reason_sanitized: null
    decided_at: null
```

**Do not pre-fill approval.**

---

# 11. Zero-production preflight invariant

This invariant is absolute:

```text
NO GATE A PASS
=
NO PIN PRODUCTION
=
NO PIN PUBLISHING
=
NO GATE B EXECUTION
```

Allowed before PASS:
- read public documentation;
- receive sanitized Owner evidence;
- validate schema completeness;
- determine PASS / WAIT_OWNER / fallback / FAIL.

Not allowed before PASS:
- create production Pin assets;
- create merchant-specific production copy;
- publish;
- schedule;
- spend;
- generate fake traffic;
- test purchase/self-purchase.

---

# 12. Gate B handoff contract

If and only if Gate A reaches `PASS`, Brain/Work receives this sanitized handoff.

Required fields:

```yaml
gate_b_handoff:
  gate_a_state: PASS
  gate_a_passed_at: ISO-8601

  network:
    name: string
    relationship_state: verified_sanitized_value

  merchant:
    public_name: string
    program_public_identifier: string_or_null
    relationship_state: verified_sanitized_value

  destination:
    market: United States
    sub_problem: Fridge storage / fit
    destination_type: category | product_family | product
    destination_public_reference: string_or_null

  linking:
    tracking_link_generation_method: sanitized_string
    allowed_link_method: direct | deep | bridge_required
    secret_tracking_link_ref_external: external_reference_only
    pin_subid_supported: true | false
    attribution_key_method: sanitized_string_or_null

  compliance:
    disclosure_requirement_sanitized: string
    required_disclosure_wording_sanitized: string_or_null
    merchant_asset_rights_constraint_sanitized: string
    original_graphics_required: true | false

  merchant_truth:
    commissionable_action_sanitized: string
    validation_locking_rule_sanitized: string
    reversal_return_rule_sanitized: string
    payout_cycle_sanitized: string
    payout_threshold_sanitized: string_or_null

  observation_constraints:
    reporting_delay_notes_sanitized: string_or_null
    attribution_window_notes_sanitized: string_or_null
    link_expiry_notes_sanitized: string_or_null
    product_availability_notes_sanitized: string_or_null
```

## Gate B restrictions remain

The handoff does **not**:
- create the 3 Pins;
- authorize publishing;
- reveal private affiliate tokens in GitHub;
- authorize paid traffic;
- authorize self/test purchase;
- re-enable SaydiVoice/video.

---

# 13. Future automation boundary

## May later be automated read-only after proof and explicit authorization

- parse sanitized network/program status exports;
- check whether required evidence fields are present;
- detect `UNKNOWN/BLOCKED/FAIL`;
- compare evidence timestamps;
- detect link-status changes using non-secret public endpoints where permitted;
- reconcile sanitized merchant/program identifiers;
- ingest Pinterest analytics;
- ingest network click/action/commission reports through authorized connectors/APIs;
- reconcile money states;
- flag payout/report discrepancies;
- verify that no production starts unless Gate A state is PASS;
- produce KEEP/KILL reports.

## Must remain Owner/legal/payment-only

- creating network accounts;
- logging in with credentials;
- entering passwords;
- MFA/OTP/CAPTCHA;
- identity verification;
- accepting legal/network/merchant contracts;
- merchant applications where Owner representation/attestation is required;
- KYC;
- tax forms;
- bank/PayPal/Payoneer setup;
- payout-account changes;
- policy appeals/suspension disputes;
- merchant negotiation;
- regulated/legal judgments;
- approving spend.

No account automation is authorized by MCME-005.

---

# 14. Time-to-first-cash critical path

No duration is invented.

```text
T0
Owner begins Gate A
  duration: UNKNOWN

→ network relationship usable
  duration: UNKNOWN

→ merchant relationship usable
  duration: UNKNOWN

→ tracking + validation terms ready
  duration: UNKNOWN

→ payout ready
  duration: UNKNOWN

→ rights/disclosure ready
  duration: UNKNOWN

→ GATE A PASS
  duration from T0: UNKNOWN

→ Gate B 3-Pin publish readiness
  duration: UNKNOWN

→ first Pin published
  duration: future task / not authorized here

→ FIRST COMMERCIAL SIGNAL
  first genuine qualified outbound click
  duration: UNKNOWN

→ FIRST ATTRIBUTED REVENUE
  first commission-bearing tracked merchant action / pending commission
  duration: UNKNOWN

→ FIRST VALIDATED REVENUE
  validated/approved commission
  duration: UNKNOWN

→ FIRST SETTLED CASH
  reconciled funds received on Owner-authorized payout rail
  duration: UNKNOWN
```

Every timestamp must be measured from real events.

---

# 15. Concise Owner handoff card

## Goal

Complete Gate A with minimum back-and-forth while keeping private data private.

## Owner checklist

```text
[ ] 1. Confirm the Pinterest property to use.

[ ] 2. AWIN FIRST
      Join/sign in and complete required Owner-only setup.
      Return only:
        - network active/pending/rejected
        - property accepted yes/no/unknown

[ ] 3. AWIN MERCHANT
      Check up to 2 relevant fridge-storage merchant programs.
      For each, return only:
        - merchant public name
        - joined/approved/pending/rejected
        - US allowed?
        - Pinterest/social allowed?
        - direct/deep link allowed?
        - commissionable action known?
        - validation/reversal known?
        - payout feasible?
        - asset/disclosure rules known?

[ ] 4. If Awin cannot pass, repeat the same checklist on impact.com
      for up to 2 merchant candidates.

[ ] 5. Use Amazon only if Awin + impact fail and Amazon property eligibility is VERIFIED.

[ ] 6. Complete KYC/tax/payment directly with the chosen network when required.
      Return only:
        - setup complete yes/no
        - payout rail TYPE only
        - threshold/cycle facts if visible

[ ] 7. Never send:
      password, OTP, cookie, tax ID, bank number, identity document,
      private payout identifier, private tracking token.
```

### What Owner can paste back safely

A compact answer can look like:

```text
Network: Awin
Network relationship: ACTIVE
Pinterest property accepted: YES
Merchant: <public merchant name>
Merchant relationship: APPROVED
US allowed: YES
Pinterest/social allowed: YES
Direct link: YES
Deep link: UNKNOWN
Commissionable action: VERIFIED
Validation/reversal: VERIFIED
Payout setup complete: YES
Payout rail type: BANK
Asset rights: ORIGINAL-GRAPHICS-ONLY
Disclosure rule: VERIFIED
```

No private values are needed.

---

# 16. Definition of Ready — future real Gate A execution task

A future Gate A execution task is READY only when all of the following are true:

## Governance

- [ ] Brain explicitly authorizes real Gate A execution.
- [ ] Fixed route/niche/sub-problem remains unchanged or Brain records an approved change.
- [ ] Network order remains Awin → impact.com → Amazon conditional.
- [ ] The privacy contract in this artifact is loaded.

## Owner readiness

- [ ] Owner knows which Pinterest property is authorized.
- [ ] Owner agrees to perform protected account/legal/payment steps directly.
- [ ] Owner understands that no credentials/private values should be pasted into GitHub/chat artifacts.
- [ ] Owner can return sanitized evidence statuses.

## Work/Robot readiness

- [ ] Evidence schema `mcme.gate-a-evidence.v1` is available.
- [ ] Merchant qualification template is available.
- [ ] Current state begins at `NOT_STARTED`.
- [ ] Fallback counters are initialized:
  - Awin merchant slots = 2;
  - impact.com merchant slots = 2;
  - Amazon conditional slots = 1.
- [ ] No production task can execute unless Gate A state is exactly `PASS`.
- [ ] No Minimum Content Factory task is active.

## Decision readiness

- [ ] PASS criteria are explicit.
- [ ] FAIL criteria are explicit.
- [ ] WAIT_OWNER criteria are explicit.
- [ ] KILL-niche action after terminal FAIL is explicit.
- [ ] No UNKNOWN can satisfy a PASS field.

If any checkbox is false, execution remains `NOT_STARTED` or `OWNER_ACTION_REQUIRED`.

---

# 17. Remaining UNKNOWNs

MCME-005 intentionally does not resolve these:

1. Whether Owner already has the intended Pinterest property.
2. Whether Owner can join/use Awin.
3. Whether Awin accepts the actual Pinterest property.
4. Which Awin fridge-storage merchants are available.
5. Whether any of the first two Awin candidates approve the Owner.
6. Whether impact.com accepts the Owner/property if needed.
7. Whether OXO or another Impact merchant approves the Owner.
8. Whether Amazon conditional eligibility is available if needed.
9. Real Pinterest/social promotion permissions in joined merchant terms.
10. Direct-link/deep-link permissions.
11. Pin/sub-ID attribution support.
12. Commissionable action for the finally selected merchant.
13. Commission rate.
14. Cookie/attribution window.
15. Validation/locking period.
16. Return/reversal treatment.
17. Payout threshold.
18. Payout cycle.
19. Payout rail feasibility and fees.
20. Merchant creative/logo/photo rights.
21. Exact affiliate disclosure wording.
22. Reporting delays.
23. Product availability at Gate B launch.
24. Any duration from Gate A start to settled cash.

All remain `UNKNOWN` until real evidence exists.

---

# 18. Owner boundaries

MCME-005 does **not** perform:

- account creation;
- account login;
- affiliate network application;
- merchant application;
- legal-term acceptance;
- credentials handling;
- MFA/OTP/CAPTCHA;
- KYC;
- tax setup;
- bank/PayPal/Payoneer setup;
- payout changes;
- merchant contact;
- product purchase;
- external spend;
- production creative generation;
- Pin publishing;
- fake/test/self-purchase;
- fake traffic/clicks;
- SaydiVoice;
- video;
- bridge-page construction;
- Minimum Content Factory specification;
- MCME-006.

---

# 19. MCME-005 handoff

## Status

**COMPLETE — Gate A contract is execution-ready, but actual Gate A remains Owner-gated.**

## Core decision rule

```text
PASS =
  one real qualified merchant money path
  with every critical evidence item VERIFIED

UNKNOWN/BLOCKED =
  NOT PASS

FAIL current merchant =
  continue within bounded slot or fallback

FAIL all bounded network paths =
  GATE A FAIL
  → KILL NICHE
  → NO PIN PRODUCTION
```

## Critical invariant

```text
NO GATE A PASS
=
NO PIN PRODUCTION
=
NO GATE B
=
NO CONTENT FACTORY
```

## Hard stop

**Do not start MCME-006 automatically. Brain acceptance is required.**
