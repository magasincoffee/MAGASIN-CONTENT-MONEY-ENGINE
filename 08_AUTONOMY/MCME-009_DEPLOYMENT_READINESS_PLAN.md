# MCME-009 — DEPLOYMENT READINESS PLAN

**Task:** MCME-009  
**Run:** `MCME-RUN-8H-01` — early-finish extension  
**Repository:** `magasincoffee/MAGASIN-CONTENT-MONEY-ENGINE`  
**Canonical input:** MCME-008 accepted at `1ee31a375aa82f8508252d2e4d1c2a6cca0848cc`  
**Mode:** PLANNING ONLY  
**Five-Step:** ACCELERATE → AUTOMATE (planning only; no deployment)  
**Current truth:** `L0_NO_REAL_COMMERCIAL_EVIDENCE`; Gate A = `OWNER_GATED_NOT_EXECUTED`

## 0. Locked decisions — DO NOT REOPEN

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

Format:
  Static 2:3 original problem-solution checklist Pin

Gate B batch:
  exactly 3 Pins

Network order:
  Awin → impact.com → Amazon Associates (conditional)

Gate A candidate cap:
  maximum 5 evaluations

Cash truth:
  06_METRICS/mcme_cash_truth_v1.schema.json

Current evidence:
  L0

Actual Gate A:
  OWNER_GATED_NOT_EXECUTED

SaydiVoice:
  DEFERRED

Video Composer:
  DEFERRED

Content Factory:
  BLOCKED until real evidence

Owner/privacy/payment boundaries:
  unchanged
```

MCME-009 prepares implementation/deployment contracts only. It does not create accounts, apply to programs, perform KYC/tax/payment work, generate Pins, publish, spend money, or deploy automation.

---

# 1. DEPLOYMENT TOPOLOGY

The first experiment should use the smallest reliable architecture. No database, message bus, orchestration platform, or 24/7 service is required for a three-Pin MVP unless real evidence later proves the simple implementation insufficient.

Paths marked **PROPOSED** are future implementation locations; MCME-009 does not create those modules.

| Component | Canonical / proposed repo path | Module owner | Input contract | Output contract | First-experiment mode | Private boundary | Side-effect class |
|---|---|---|---|---|---|---|---|
| Owner Action Packet | Canonical rules in `07_EXPERIMENTS/MCME-005_GATE_A_EXECUTION_READINESS.md`; future sanitized packet may live at **PROPOSED** `08_AUTONOMY/runtime_specs/OWNER_ACTION_PACKET_V1.md` | OWNER + WORK | fixed property/network order; sanitized fields only | sanitized Owner evidence statuses | MANUAL | credentials/MFA/KYC/tax/payment values never enter Git | OWNER_REQUIRED |
| Gate A evidence capture | MCME-005 contract; **PROPOSED** `07_EXPERIMENTS/gate_a/mcme_gate_a_evidence_v1.schema.json` and append-only sanitized records under `07_EXPERIMENTS/gate_a/evidence/` | WORK | Owner sanitized evidence + public/program terms | status fields VERIFIED/UNKNOWN/BLOCKED/FAIL | MANUAL FIRST; schema validation may be code | raw screenshots/private account data remain local/private | READ_ONLY_EXTERNAL + REVERSIBLE_REPO_CHANGE |
| Gate A evaluator | MCME-005 state machine; **PROPOSED** `04_ROBOT/first_cash/gate_a_evaluator/` | WORK; later ROBOT read-only | evidence record set | legal state transition + audit record | DETERMINISTIC CODE OR MANUAL RULE ENGINE | no account login/token handling | SAFE_PREP / READ_ONLY_EXTERNAL |
| Merchant handoff | **PROPOSED** `07_EXPERIMENTS/gate_a/gate_b_handoff_v1.json` | WORK | Gate A PASS evidence | sanitized merchant/program/destination/link/disclosure/rights/attribution contract | MANUAL + schema validation | raw affiliate URL/token can remain external reference | REVERSIBLE_REPO_CHANGE |
| 3-Pin spec / production package | **PROPOSED** `03_CONTENT/first_cash/MCME-029_THREE_PIN_SPEC.md`, assets under `03_CONTENT/first_cash/assets/` only after Gate A PASS | WORK | Gate B handoff | exactly 3 deterministic content specs/assets | MANUAL/ASSISTED FIRST | no private merchant secrets embedded in image or public metadata | REVERSIBLE_REPO_CHANGE |
| QA / publish readiness | **PROPOSED** `07_EXPERIMENTS/MCME-031_PUBLISH_READINESS.json` | WORK | asset hashes + Gate B handoff + observation plan | PASS/FAIL manifest, publish intents, locked observation window | CODE CHECKS + MANUAL RIGHTS/DISCLOSURE REVIEW | private link secret referenced externally | SAFE_PREP / REVERSIBLE_REPO_CHANGE |
| Pinterest publish adapter | **PROPOSED** `04_ROBOT/pinterest_publish_adapter/` + local/private latch store | WORK/ROBOT | one publish intent at a time | confirmed Pinterest Pin ID or BLOCKED_AMBIGUOUS | CONTROLLED ADAPTER; no blind retry | auth/session/MFA/browser state never Git | EXTERNAL_SIDE_EFFECT |
| Observation collector | **PROPOSED** `04_ROBOT/first_cash_observer/`; first run may be manual exports | ROBOT/WORK | Pin IDs + fixed observation window + network refs | sanitized source observations | MANUAL/READ-ONLY FIRST | raw account exports may stay private; Git gets sanitized facts only | READ_ONLY_EXTERNAL |
| Cash Truth ingestion | canonical schema `06_METRICS/mcme_cash_truth_v1.schema.json`; **PROPOSED** validator `06_METRICS/tools/cash_truth_ingest/` | WORK; later ROBOT | sanitized source observations | append-only validated events + reconciliation status | SIMPLE LOCAL JSONL + validator | real private ledger may remain outside public Git | REVERSIBLE_REPO_CHANGE / READ_ONLY_EXTERNAL |
| KEEP/KILL/SCALE package | **PROPOSED** `05_BRAIN/MCME-035_DECISION_PACKET.md` | BRAIN | canonical Cash Truth snapshot + Gate B hypotheses | KEEP / KILL / SCALE-ELIGIBLE | MANUAL BRAIN DECISION | no secrets required | SAFE_PREP |
| Payout / settled-cash reconciliation | Cash Truth V1 + **PROPOSED** `06_METRICS/MCME-038_FIRST_REAL_CASH_RECONCILIATION.md` | OWNER + WORK | payout-issued evidence + sanitized funds-received evidence + costs/time | CASH_SETTLED or unresolved; L-level | MANUAL FIRST | bank/payment statement details remain private | OWNER_REQUIRED + READ_ONLY_EXTERNAL |

## Topology principle

```text
PUBLIC GIT:
  contracts
  schemas
  sanitized state
  deterministic manifests
  hashes
  public merchant/program references
  redacted evidence metadata

LOCAL / PRIVATE:
  credentials
  account exports containing private data
  private screenshots
  raw tracking tokens/URLs if sensitive
  identity/KYC/tax documents
  bank/payment records
  private payout identifiers
  browser/session state
```

No private system is required to expose raw secrets to Brain/Work. A sanitized fact is sufficient whenever it proves the required state.

---

# 2. MCME-010 → MCME-038 EXECUTION MAP

The existing numbering is preserved. No competing numbering system is introduced.

## A. Owner/Gate-A path

| Task | Exact precondition | Executor | Required artifact/evidence | Test / review gate | Rollback / recovery | Forbidden inference | PASS → | FAIL / WAIT_OWNER |
|---|---|---|---|---|---|---|---|---|
| MCME-010 | MCME-009 accepted; fixed route unchanged | OWNER | sanitized Pinterest property reference + authorization status | one real property unambiguously identified | correct evidence by new sanitized record; no credential transfer | a known handle does not prove Owner authorization | MCME-011 | no usable property → WAIT_OWNER / Brain review |
| MCME-011 | MCME-010 PASS | OWNER | Awin relationship active/pending/rejected/blocked + property acceptance | enough evidence for network evaluation | do not create duplicate Awin account; resolve existing relationship first | public Awin availability != Owner acceptance | MCME-012 | pending → WAIT_OWNER; rejected recorded for fallback |
| MCME-012 | MCME-011 evidence | WORK | `mcme.gate-a-evidence.v1` record; materialize schema/template if needed | NETWORK_READY only if critical network/property evidence VERIFIED | append corrected evidence; evaluator rerun by evidence version | UNKNOWN/BLOCKED != READY | MCME-013 | terminal network fail → MCME-017 |
| MCME-013 | MCME-012 NETWORK_READY | OWNER | Awin candidate slot 1 sanitized qualification evidence | candidate record complete enough for evaluation | do not blind reapply; wait if pending | program listing != approval; link page != social permission | MCME-014 | pending → WAIT_OWNER |
| MCME-014 | MCME-013 evidence | WORK | candidate 1 evaluation | all critical merchant/link/terms fields classified | append new evidence and re-evaluate same slot | missing field != favorable default | MCME-027 if provisional winner | candidate fail → MCME-015 |
| MCME-015 | MCME-014 merchant fail | OWNER | Awin candidate slot 2 evidence | final Awin merchant slot complete | no third Awin candidate | candidate 1 failure does not imply network failure until slot 2 evaluated | MCME-016 | pending → WAIT_OWNER |
| MCME-016 | MCME-015 evidence | WORK | candidate 2 evaluation | explicit provisional winner or Awin exhausted | same-slot evidence revision only | UNKNOWN != fail-safe PASS | MCME-027 if winner | exhausted → MCME-017 |
| MCME-017 | Awin exhausted | OWNER | impact.com relationship + property status | enough evidence for network evaluation | reconcile existing account first; no duplicate account | OXO public path != Owner impact acceptance | MCME-018 | pending → WAIT_OWNER |
| MCME-018 | MCME-017 evidence | WORK | impact network evidence record | NETWORK_READY only with verified critical fields | append corrected evidence | network availability != merchant approval | MCME-019 | terminal impact fail → MCME-023 |
| MCME-019 | MCME-018 NETWORK_READY | OWNER | impact candidate slot 1 evidence | merchant record complete | no blind reapply | public affiliate page != joined relationship | MCME-020 | pending → WAIT_OWNER |
| MCME-020 | MCME-019 evidence | WORK | impact candidate 1 evaluation | provisional winner or explicit candidate fail | re-evaluate by evidence version | unknown direct/deep-link rule cannot be assumed allowed | MCME-027 if winner | fail → MCME-021 |
| MCME-021 | MCME-020 candidate fail | OWNER | impact candidate slot 2 evidence | final impact merchant slot complete | no third impact candidate | first candidate failure does not unlock Amazon yet | MCME-022 | pending → WAIT_OWNER |
| MCME-022 | MCME-021 evidence | WORK | impact candidate 2 evaluation | winner or impact exhausted | append-only evaluation history | UNKNOWN != PASS | MCME-027 if winner | exhausted → MCME-023 |
| MCME-023 | Awin + impact exhausted | OWNER | Amazon conditional eligibility sanitized evidence | eligibility must be VERIFIED before money-path attempt | resolve real existing property/account status | Amazon program existence != eligible Pinterest property | MCME-024 | UNKNOWN/BLOCKED/FAIL captured |
| MCME-024 | MCME-023 evidence | WORK | eligibility evaluation | AMAZON_ELIGIBLE only if verified | re-evaluate only with new evidence | no alternate identity/property invented | MCME-025 | otherwise terminal path → MCME-028 |
| MCME-025 | MCME-024 AMAZON_ELIGIBLE | OWNER | one Amazon money-path evidence packet | one and only one conditional Amazon slot | reconcile existing path; no second Amazon slot | association/account existence != trackable permitted path | MCME-026 | pending → WAIT_OWNER |
| MCME-026 | MCME-025 evidence | WORK | final Amazon path evaluation | provisional winner or bounded fallback exhausted | evidence revision only | missing validation/payout rule != acceptable | MCME-027 if winner | terminal FAIL → MCME-028 |
| MCME-027 | one provisional winning merchant path | OWNER | only required winning-path KYC/tax/payment readiness; sanitized output | payout feasibility + protected requirements either complete or blocked | complete existing setup; no duplicate payout rails | payment-rail name != payout readiness | MCME-028 | blocked → WAIT_OWNER; impossible → fallback only if bounded slot remains |
| MCME-028 | winning-path evidence complete or terminal exhaustion | WORK | final Gate A evidence set + audit trail | PASS iff every critical item VERIFIED | new evidence produces a new evaluation revision; never mutate history | UNKNOWN/BLOCKED/marketing claim != PASS | MCME-029 | FAIL → KILL niche; WAIT_OWNER → stop |

### Gate A candidate identities

Use stable internal slots:

```text
AWIN-01
AWIN-02
IMPACT-01
IMPACT-02
AMAZON-01
```

These are **evaluation slots**, not merchant IDs and not evidence of approval.

---

## B. Post-Gate-A production/publish path

| Task | Exact precondition | Executor | Artifact/evidence | Test/review gate | Rollback/recovery | Forbidden inference | PASS → | FAIL / WAIT_OWNER |
|---|---|---|---|---|---|---|---|---|
| MCME-029 | MCME-028 = PASS | WORK | Gate B handoff; real merchant/program/destination/link/disclosure/rights/attribution facts | exactly 3 content specs; no critical placeholder unresolved | revise spec before production | public merchant page != approved asset usage | MCME-030 | missing critical field → back to Gate A evidence |
| MCME-030 | MCME-029 PASS | WORK | exactly 3 static production assets + metadata/hashes | asset count = 3; deterministic IDs; original graphics default | regenerate only failed content version; preserve version history | visually correct != rights/disclosure compliant | MCME-031 | rights/spec ambiguity → STOP |
| MCME-031 | 3 assets exist | WORK | QA manifest + publish intents + locked observation window + tested publish latch contract + Cash Truth sink readiness | all 3 QA PASS; zero critical UNKNOWN; dry-run adapter no side effect | fix failed asset/config; re-hash/re-QA | a working URL != trackable/allowed URL | MCME-032 | any critical fail → no publish |
| MCME-032 | MCME-031 PASS + explicit publish authorization + browser/auth ready | WORK/ROBOT | three persisted publish intents/latches | exactly one confirmed published Pin ID per intended content version | ambiguous result → reconcile before retry; no blind resend | missing response != failed send | MCME-033 | auth/MFA/CAPTCHA → WAIT_OWNER; unresolved send → STOP |
| MCME-033 | all intended Pin IDs reconciled; observation window already locked | ROBOT/WORK | Pinterest/network observations with source timestamps | source-bound observation complete for fixed window | retry reads safely with dedupe; source unavailable remains UNKNOWN | absent data != zero unless source proves zero | MCME-034 | source blocked → WAIT/STOP, no fabricated metric |
| MCME-034 | MCME-033 evidence | WORK | events valid under Cash Truth V1 + reconciliation status | schema-valid, append-only, deduped, no inferred money state | correction = new event; never overwrite | click != sale; provider "paid" != settled cash | MCME-035 | ambiguous join → UNKNOWN/CONSERVATIVE_RECONCILIATION |
| MCME-035 | canonical evidence snapshot | BRAIN | KEEP/KILL/SCALE package | decision references exact evidence level/version | later evidence may supersede decision | views/clicks != SCALE eligibility | MCME-036 only if L2+ survives | L0/L1 → KEEP/REVISE/KILL, not scale |
| MCME-036 | L2+ and MCME-035 keeps path | ROBOT/WORK | lifecycle observations for commission provider record(s) | pending/validated/reversed/payable/payout-issued states source-backed | repeated read deduped; reversal appended | elapsed time != validation; payout issued != cash | MCME-037 when payout path exists | reversal/blocked recorded honestly |
| MCME-037 | payable/payout-issued evidence exists | OWNER | sanitized funds-received confirmation + fees if visible | actual Owner-authorized rail observation | correction append-only; no banking secret copied | network "paid" != funds received | MCME-038 | funds absent → remain below L4 / WAIT |
| MCME-038 | MCME-037 evidence + measured cost/time | WORK | CASH_SETTLED event/reconciliation or unresolved result | funds actually received + reconciled + costs/time measured | append negative/correction events if later evidence changes economics | payout issued != settled cash | FIRST REAL CASH / future economics review | unresolved → no L4 claim |

---

# 3. OWNER SETUP PACKAGE — ONE-SITTING FLOW

MCME-009 does not ask Owner to do this now. This is the future execution packet.

## Step 1 — Pinterest property

Owner returns only:

```text
property_authorized: YES | NO
property_public_reference: <safe public/sanitized reference>
checked_at: <timestamp>
```

No password, cookie, device/session data, private phone/email, OTP, or recovery code.

## Step 2 — Awin first

Owner handles login/join/legal/account steps directly.

Return:

```text
network: Awin
relationship: ACTIVE | PENDING | REJECTED | BLOCKED
property_accepted: YES | NO | UNKNOWN
checked_at: <timestamp>
```

If ACTIVE, Owner evaluates only candidate slot `AWIN-01`. Candidate `AWIN-02` is touched only after Work rejects slot 1.

Candidate packet:

```text
slot:
network:
merchant_public_name:
relationship: APPROVED | JOINED | PENDING | REJECTED | BLOCKED
us_allowed: YES | NO | UNKNOWN
pinterest_social_allowed: YES | NO | UNKNOWN
direct_link_allowed: YES | NO | UNKNOWN
deep_link_allowed: YES | NO | UNKNOWN
tracking_link_capability: VERIFIED | UNKNOWN | BLOCKED | FAIL
commissionable_action: VERIFIED | UNKNOWN | BLOCKED | FAIL
validation_locking: VERIFIED | UNKNOWN | BLOCKED | FAIL
reversal_return_rule: VERIFIED | UNKNOWN | BLOCKED | FAIL
payout_feasible: YES | NO | UNKNOWN
asset_rights: VERIFIED | UNKNOWN | BLOCKED | FAIL
disclosure_rule: VERIFIED | UNKNOWN | BLOCKED | FAIL
checked_at:
```

## Step 3 — impact.com fallback

Only after Awin is formally exhausted.

Same packet, slots:

```text
IMPACT-01
IMPACT-02
```

## Step 4 — Amazon conditional fallback

Only after Awin and impact.com are exhausted.

First return:

```text
amazon_conditional_eligibility:
  VERIFIED | UNKNOWN | BLOCKED | FAIL
```

Proceed to `AMAZON-01` only if eligibility is VERIFIED.

## Step 5 — winning-path protected setup only

Only after one path is provisionally viable:

```text
kyc_tax_setup_complete: YES | NO
payment_setup_complete: YES | NO
payout_rail_type: BANK | PAYPAL | PAYONEER | OTHER_ALLOWED
payout_threshold_cycle: <sanitized fact if visible>
checked_at:
```

### Never return

- passwords;
- session cookies;
- API keys/secrets;
- MFA/OTP/recovery codes;
- CAPTCHA material;
- tax IDs;
- account/routing/card numbers;
- identity documents;
- raw private payout IDs;
- raw sensitive affiliate tracking token/URL;
- browser/session storage.

This one-sitting packet minimizes Owner interruptions while preserving fail-closed boundaries.

---

# 4. REPOSITORY ARTIFACT LAYOUT

## 4.1 PUBLIC SAFE — allowed in Git

Recommended categories:

```text
00_PROJECT/
  canonical state/backlog/contracts

03_CONTENT/first_cash/
  public-safe specs
  deterministic content IDs
  future final assets if approved for public repository

06_METRICS/
  schemas
  validators
  sanitized event examples
  sanitized reconciliation summaries

07_EXPERIMENTS/gate_a/
  schemas/templates
  sanitized evidence status records
  merchant qualification outcomes
  Gate B handoff without raw secrets

08_AUTONOMY/
  planning/deployment docs
```

Allowed public fields:

- public merchant/network names;
- sanitized relationship statuses;
- sanitized public property reference;
- evidence status/confidence;
- timestamps;
- public program references;
- deterministic content IDs;
- content hashes;
- Pin IDs if intended to be public;
- sanitized payout/cash summary if Owner explicitly permits it.

## 4.2 LOCAL / PRIVATE — never Git by default

Use a symbolic local root such as:

```text
<MCME_PRIVATE_ROOT>/
  gate_a/raw_captures/
  gate_a/account_exports/
  tracking/
  pinterest_session/
  analytics/raw_exports/
  payout/raw_evidence/
  cash_truth/ledger.jsonl
  temp/
```

The exact machine path is environment-specific and must not be hard-coded in public docs.

Private evidence includes:

- unredacted screenshots;
- raw account exports;
- confidential program terms if applicable;
- raw affiliate tracking URLs/tokens if sensitive;
- browser state/session;
- bank/payment evidence;
- KYC/tax/identity data.

## 4.3 Secrets

Secrets belong only in the platform/browser credential store or another Owner-controlled secret store.

They do not belong in:

- Git;
- commit messages;
- issue text;
- JSON manifests;
- content metadata;
- logs;
- screenshots committed to the repo.

## 4.4 Temporary files

Temporary screenshots/downloads/exports should remain under local temporary/private storage and be deleted after sanitized facts are extracted, subject to any Owner audit-retention choice.

---

# 5. GATE A IMPLEMENTATION CONTRACT

Canonical contract:

`07_EXPERIMENTS/MCME-005_GATE_A_EXECUTION_READINESS.md`

## 5.1 Machine-readable extraction

Before MCME-012 needs deterministic validation, materialize the MCME-005 inline contract into **PROPOSED**:

```text
07_EXPERIMENTS/gate_a/mcme_gate_a_evidence_v1.schema.json
07_EXPERIMENTS/gate_a/merchant_qualification_v1.schema.json
```

This is a safe-prep implementation detail, not new strategy.

## 5.2 Legal states

```text
NOT_STARTED
OWNER_ACTION_REQUIRED
WAIT_OWNER
NETWORK_READY
MERCHANT_READY
TRACKING_READY
VALIDATION_TERMS_READY
PAYOUT_READY
RIGHTS_DISCLOSURE_READY
PASS
FAIL
```

No direct shortcut to PASS.

## 5.3 Evidence statuses

Every material field:

```text
VERIFIED
UNKNOWN
BLOCKED
FAIL
```

Rules:

- no source → UNKNOWN;
- Owner action required → BLOCKED or WAIT_OWNER;
- incompatible real term → FAIL;
- source-backed compatible truth → VERIFIED;
- UNKNOWN/BLOCKED never satisfies PASS.

## 5.4 Audit trail

Each evaluation record should include:

- evaluation_id;
- task_id;
- network slot;
- merchant slot;
- evidence version/digest;
- prior state;
- new state;
- decision reason;
- observed_at/evaluated_at;
- sanitized evidence refs.

Do not overwrite prior evaluations.

## 5.5 Bounded candidate slots

```text
AWIN-01
AWIN-02
IMPACT-01
IMPACT-02
AMAZON-01
```

Maximum = 5.

The first viable path stops further merchant searching and proceeds to winning-path protected setup.

---

# 6. THREE-PIN PRODUCTION READINESS — ONLY AFTER GATE A PASS

Invariant:

```text
NO GATE A PASS = NO PRODUCTION
```

## 6.1 Deterministic content identities

Use stable IDs independent of filename:

```text
MCME-FC1-FRIDGE-FIT-P01-MEASURE
MCME-FC1-FRIDGE-FIT-P02-SHAPE
MCME-FC1-FRIDGE-FIT-P03-MISTAKES
```

Version separately:

```text
content_version: v1
```

A visual revision increments version; it does not silently replace the identity/history.

## 6.2 Canonical concepts

1. **Measure Before You Buy**
2. **Which Bin Shape Fits This Shelf?**
3. **Fridge Fit Mistakes to Check Before Ordering**

## 6.3 Graphic rules

Default:

- original graphics only;
- original copy;
- no merchant photo/logo unless Gate A rights explicitly allow it;
- no unsupported food-safety/health/freshness/environmental claim;
- vertical 2:3;
- preferred implementation target `1000 × 1500` or exact 2:3 equivalent;
- no SaydiVoice;
- no video.

## 6.4 Spec inputs from Gate B handoff

Each content record must receive:

- merchant/program public identifier;
- destination/category/product-family;
- allowed link method;
- tracking generation method;
- attribution/sub-ID method if available;
- disclosure requirement/wording;
- asset-rights constraint;
- geography;
- any reporting/attribution constraints.

Use placeholders only in the pre-production spec. Production cannot start while a **critical** placeholder remains unresolved.

## 6.5 Proposed outputs

```text
03_CONTENT/first_cash/
  MCME-029_THREE_PIN_SPEC.md
  manifests/
    MCME-FC1-FRIDGE-FIT-P01-MEASURE.v1.json
    MCME-FC1-FRIDGE-FIT-P02-SHAPE.v1.json
    MCME-FC1-FRIDGE-FIT-P03-MISTAKES.v1.json
  assets/
    <content_id>.v1.png
```

Each final asset receives:

- SHA-256 or equivalent content hash;
- deterministic content ID;
- version;
- source spec version;
- creation timestamp;
- no secret URL embedded in public manifest.

## 6.6 QA artifact

**PROPOSED** `07_EXPERIMENTS/MCME-031_PUBLISH_READINESS.json`

Must bind:

- asset hashes;
- dimensions/aspect ratio;
- originality review;
- rights review;
- disclosure review;
- destination/link config version;
- attribution config version;
- sensitive-data scan result;
- observation-window definition;
- publish intent IDs.

---

# 7. PINTEREST PUBLISH ADAPTER CONTRACT — PLANNING ONLY

No adapter is deployed in MCME-009.

## 7.1 One intended publish per content/version

Publish identity:

```text
publish_intent_id =
  deterministic(
    experiment_id,
    content_id,
    content_version,
    destination_config_version
  )
```

A cryptographic hash may implement the deterministic key; the unhashed canonical inputs must also be recorded in the local/private latch record.

## 7.2 Persisted pre-action latch

Minimum states:

```text
PREPARED
SEND_STARTED
CONFIRMED
BLOCKED_AUTH
BLOCKED_AMBIGUOUS
FAILED_CONFIRMED
```

Before any external send:

1. persist `PREPARED`;
2. verify content/version/link/disclosure hash;
3. mark `SEND_STARTED`;
4. perform at most one bounded send attempt;
5. if Pinterest returns a confirmed Pin ID, store `CONFIRMED`;
6. if result is ambiguous, store `BLOCKED_AMBIGUOUS` and reconcile before any retry.

## 7.3 No blind retry

An error, timeout, UI ambiguity, or missing response does not prove no Pin was created.

Recovery:

1. search/reconcile Pinterest account for the intended content/version;
2. if a matching Pin exists, bind its Pin ID and mark CONFIRMED;
3. if no result can be proven, escalate rather than blindly resend.

## 7.4 Auth fail-closed

If login, password, MFA, CAPTCHA, identity, suspension, or account recovery is required:

```text
STOP
→ OWNER
```

Robot must not bypass or solve protected authentication.

## 7.5 External side-effect truth

Publishing is not treated as trivially reversible.

Deletion/unpublish, if later considered, is a separate external side effect and requires explicit authorization.

---

# 8. OBSERVATION / ANALYTICS CONTRACT

## 8.1 Observation window

The observation window must be locked in MCME-031 **before** MCME-032 publishes.

Required fields:

- window definition;
- start rule;
- end rule;
- same comparison rule for all 3 Pins;
- source systems to observe.

Duration is currently **UNKNOWN** and must not be invented by MCME-009.

## 8.2 Sources

Pinterest:

- Pin ID;
- impressions;
- Pin clicks;
- outbound clicks;
- source timestamps/window.

Affiliate network / merchant:

- network click if available;
- merchant action;
- commission lifecycle states;
- source record IDs when available.

## 8.3 Cadence

Polling/read cadence remains:

```text
UNKNOWN UNTIL SOURCE CAPABILITY / OBSERVATION CONTRACT IS KNOWN
```

For the 3-Pin MVP, manual/read-only snapshots are acceptable. Automation is not required merely because polling could be automated.

## 8.4 Dedupe

- stable provider record ID where available;
- snapshot key for cumulative/window metrics;
- no summing repeated cumulative snapshots;
- conservative reconciliation where stable ID is absent.

## 8.5 Prohibited behavior

- no artificial clicks;
- no Owner/Robot affiliate-click testing that contaminates experiment metrics;
- no fake save/engagement;
- no self/test purchase;
- no missing-value fabrication.

---

# 9. CASH TRUTH DEPLOYMENT

Canonical schema:

`06_METRICS/mcme_cash_truth_v1.schema.json`

Canonical semantic contract:

`06_METRICS/MCME-006_CASH_TRUTH_EVENT_LEDGER.md`

## 9.1 Does the three-Pin MVP need a database?

**QUESTION:** Is a database required before first cash?

**Answer:** **NO, not currently.**

For exactly three Pins and one merchant path, the smallest reliable implementation is:

```text
local/private append-only JSONL
+ JSON Schema validator
+ deterministic idempotency key
+ reconciliation command/report
+ sanitized public summary if needed
```

A database becomes justified only if observed operational needs such as concurrency, recurring multi-source ingestion, query/reconciliation burden, or audit reliability exceed the simple ledger. No artificial event-volume threshold is invented.

## 9.2 Proposed MVP implementation

**Private source ledger:**

```text
<MCME_PRIVATE_ROOT>/cash_truth/ledger.jsonl
```

**Public code/schema:**

```text
06_METRICS/mcme_cash_truth_v1.schema.json
06_METRICS/tools/cash_truth_ingest/   # PROPOSED
```

Validator responsibilities:

- schema validate;
- reject invalid `CASH_SETTLED`;
- calculate/verify idempotency key;
- append only if not duplicate;
- preserve source/evidence refs in sanitized form;
- never infer missing money state.

## 9.3 Adapter → event mapping

| Adapter/source | Allowed canonical events |
|---|---|
| Pinterest publication | PIN_PUBLISHED |
| Pinterest analytics | PIN_IMPRESSION_OBSERVED, PIN_CLICK_OBSERVED, OUTBOUND_CLICK_OBSERVED |
| Affiliate network click report | NETWORK_CLICK_OBSERVED |
| Merchant/network action report | MERCHANT_ACTION_TRACKED |
| Commission report | COMMISSION_PENDING, COMMISSION_VALIDATED, COMMISSION_REVERSED, COMMISSION_PAYABLE |
| Payout provider/network | PAYOUT_ISSUED, NEGATIVE_ADJUSTMENT_RECORDED |
| Owner-authorized payout rail | CASH_SETTLED |
| receipts/payment evidence | COST_RECORDED |
| measured timers/logs | TIME_RECORDED |

## 9.4 Append-only/reversal

Never mutate prior events.

Refund/return/clawback:

- append COMMISSION_REVERSED or NEGATIVE_ADJUSTMENT_RECORDED;
- if actual settled money is later debited, append a negative CASH_SETTLED event only when payout-rail evidence proves the debit.

## 9.5 Settlement privacy

Raw bank/payment statement never needs to enter Git.

Cash-settlement public-safe record may contain only:

- amount/currency if Owner permits;
- posted timestamp;
- sanitized payout/reference digest/handle;
- `funds_actually_received=true`;
- `owner_authorized_payout_rail=true`;
- `reconciled_to_payout=true`.

---

# 10. TEST STRATEGY

Testing precedes any real Pin publication.

## 10.1 Schema tests

Required fixtures:

- valid Gate A VERIFIED record;
- UNKNOWN critical field must fail PASS evaluation;
- BLOCKED field must fail PASS evaluation;
- invalid state transition rejected;
- valid Cash Truth event;
- malformed currency/amount rejected;
- CASH_SETTLED missing any required settlement truth rejected.

## 10.2 Gate A fail-closed tests

Must prove:

```text
UNKNOWN → cannot PASS
BLOCKED → cannot PASS
pending merchant → WAIT_OWNER
candidate FAIL → bounded next slot only
5 slots exhausted → FAIL/KILL
```

## 10.3 Publish idempotency tests — no real side effect

Use a fake/mock publish sink or dry-run interface.

Test:

1. same publish intent twice → one logical intent;
2. simulated timeout after mock side effect → adapter enters BLOCKED_AMBIGUOUS;
3. reconcile finds existing mock Pin → no second send;
4. auth-required condition → STOP/OWNER;
5. content version change → new explicit intent, not hidden overwrite.

A dry run must not call the real Pinterest publish action.

## 10.4 Cash dedupe tests

- repeated same provider record does not double-count;
- PENDING → VALIDATED is two lifecycle events on one commission record, not two revenues;
- repeated aggregate snapshot not summed blindly.

## 10.5 Reversal tests

- pending commission reversed;
- validated commission reversed;
- negative payout adjustment;
- settled cash later debited with real settlement evidence.

Net economics must reflect the reversal.

## 10.6 Privacy leak tests

Before Git commit/public artifact:

scan/review for:

- passwords/tokens;
- cookies;
- OTP/MFA;
- tax IDs;
- bank/account/card/routing numbers;
- identity docs;
- raw payout identifiers;
- sensitive affiliate URLs/tokens;
- browser session state.

Automated pattern scanning is helpful but does not replace manual review.

## 10.7 Production launch checklist

Before MCME-032:

- Gate A PASS;
- all 3 QA PASS;
- link/disclosure/rights verified;
- content hashes fixed;
- observation window locked;
- publish latches initialized;
- mock/dry-run idempotency tests PASS;
- Cash Truth validator/sink ready;
- browser/auth prerequisites ready;
- zero critical UNKNOWN.

---

# 11. ROLLBACK / RECOVERY

| Operation | Reversibility | Recovery rule | STOP / Owner escalation |
|---|---|---|---|
| Repo contract/schema change | reversible through later commit; history preserved | fix forward; never erase accepted history | conflicting canonical truth → Brain review |
| Gate A sanitized evidence | append-only truth record | new evidence supersedes prior interpretation | private evidence ambiguity → WAIT_OWNER |
| Network/merchant application | may be non-reversible | do not duplicate; wait/reconcile existing state | rejection/pending/protected verification → Owner |
| KYC/tax/payment setup | protected; not treated as reversible | Owner manages provider account | any identity/payment ambiguity → Owner |
| Pin asset generation | reversible before publish | increment version; preserve prior hash | rights/disclosure ambiguity → STOP |
| Real Pin publish | external side effect, not safely reversible | reconcile Pin ID before any retry | ambiguous result/auth/MFA/CAPTCHA → STOP |
| Observation read | read-only | re-read with dedupe | source unavailable → UNKNOWN |
| Ledger append | append-only | correction/reversal as new event | invalid schema/source identity → reject append |
| Payout | external financial process | observe/reconcile only | payment changes/problems → Owner |
| Settled-cash evidence | observation only | corrected evidence appended | insufficient rail evidence → no L4 |

Principle:

```text
SAFE RETRY requires either:
  proven no side effect
or
  successful reconciliation of prior side effect
```

No "retry because uncertain."

---

# 12. LAUNCH GATE — BEFORE FIRST REAL PIN PUBLISH

MCME-032 cannot execute unless all conditions are true:

```text
[ ] Gate A state = PASS
[ ] Real merchant/program relationship VERIFIED
[ ] US geography VERIFIED
[ ] Pinterest/social promotion VERIFIED
[ ] link method VERIFIED
[ ] tracking capability VERIFIED
[ ] commissionable action VERIFIED
[ ] validation/reversal rule VERIFIED
[ ] payout feasibility VERIFIED
[ ] disclosure requirement VERIFIED
[ ] asset-rights constraint VERIFIED
[ ] exactly 3 deterministic Pin packages ready
[ ] all 3 assets QA PASS
[ ] original-graphics-only default satisfied unless explicit rights allow otherwise
[ ] observation window locked before publish
[ ] deterministic publish idempotency key/latch ready
[ ] ambiguous publish recovery tested
[ ] Cash Truth V1 validator + append-only sink ready
[ ] privacy scan/review PASS
[ ] Owner/browser/auth prerequisite ready
[ ] explicit external-side-effect authorization present
[ ] zero unresolved critical UNKNOWN
```

If any item fails:

```text
NO PUBLISH
```

---

# 13. POST-LAUNCH DECISION CADENCE — EVIDENCE-DRIVEN, NOT INVENTED TIME

No KPI target or polling interval is invented.

## L0

Truth:

- no qualified commercial signal yet.

Possible actions:

- if no distribution, inspect publication/indexing/distribution mechanics;
- if distribution but no outbound click, revise/kill framing after bounded observation.

Not allowed:

- scale;
- new platform;
- large batch;
- 24/7 automation.

## L1 — qualified outbound click

Action:

- KEEP as learning signal if genuine;
- inspect which framing created intent;
- do not call it revenue.

Not allowed:

- scale from views/clicks alone.

## L2 — tracked merchant action / attributed commission

Action:

- first SCALE-eligibility discussion may occur;
- continue validation;
- consider only minimal repetitive/read-only automation if it reduces evidence-handling friction.

Still not cash.

## L3 — validated / payable commission

Action:

- stronger economics review;
- monitor reversals/payout;
- measure production/cost/time carefully.

Still not settled cash.

## L4 — settled cash + measured direct cost/time

Action:

- first real cash claim is permitted;
- calculate measured net economics;
- Brain may reconsider automation architecture.

### Gate for 24/7 automation reconsideration

24/7 content/publishing automation may be reconsidered only when:

```text
L4 exists
AND
observed workflow is repeatable enough for Brain to identify stable inputs/outputs/failures
AND
Owner explicitly authorizes external-side-effect automation
```

L4 does not automatically authorize automation.

---

# 14. FIVE-STEP IMPLEMENTATION AUDIT

| Component | QUESTION | DELETE | SIMPLIFY | ACCELERATE | AUTOMATE plan | First experiment mode |
|---|---|---|---|---|---|---|
| Owner packet | Does Work need raw account data? No. | secrets/screenshots from public workflow | sanitized statuses only | one-sitting packet | none until proven repetitive | MANUAL OWNER |
| Gate A evaluator | Need a service/DB? No. | heavy workflow engine | schema + deterministic transitions | bounded slots | later automate validation/read-only | MANUAL + SIMPLE VALIDATOR |
| Merchant handoff | Need full merchant data model? No. | noncritical marketing detail | one winning-path handoff | stop search at first viable path | later generated from validated evidence | MANUAL |
| Content spec | Need many variants? No. | large batch/video/voice | 3 deterministic specs | reuse one template structure | template generation only after proof | WORK MANUAL/ASSISTED |
| Graphics | Need video? No. | SaydiVoice/video/merchant photos by default | 1000×1500 original static | deterministic manifests/hashes | later template rendering after evidence | MANUAL/ASSISTED |
| QA | Need giant QA platform? No. | cosmetic noncritical checks | checklist + hashes + privacy scan | deterministic prepublish manifest | automate mechanical checks only | HYBRID |
| Publish | Can blind retries be tolerated? No. | generic browser-loop automation | one-intent latch + reconcile | bounded single send | automate only with explicit authorization/proof | CONTROLLED / MANUAL-FIRST |
| Observation | Need continuous polling? Unknown. | arbitrary frequency | fixed-window snapshots | read-only source capture | automate only if repetitive burden appears | MANUAL/READ-ONLY |
| Cash truth | Need database? No for current 3-Pin MVP. | DB/event bus/dashboard | private JSONL + schema validator | append/dedupe/reconcile | adapter automation after source proof | SIMPLE CODE |
| Decision | Should an algorithm auto-scale? No. | auto-scale rules from vanity metrics | L0-L4 evidence packet | one Brain decision | decision support later; not autonomous spend/publish | MANUAL BRAIN |
| Payout reconciliation | Need bank integration now? No. | raw bank-data ingestion | sanitized Owner confirmation | one payout-to-settlement reconcile | read-only automation only if safe/proven | MANUAL OWNER + WORK |

## Components that should remain manual in the first experiment

- Owner property/account/network setup;
- merchant application/legal acceptance;
- KYC/tax/payment;
- rights/disclosure judgment;
- final QA judgment;
- first external publish authorization;
- KEEP/KILL/SCALE Brain decision;
- settled-funds confirmation.

Automation is only justified after the workflow becomes repetitive and source-backed.

---

# 15. DEPLOYMENT BACKLOG READINESS

## 15.1 Is MCME-010 operationally ready?

```text
YES
```

MCME-010 needs only:

- accepted canonical route;
- Owner Action Packet;
- privacy contract;
- one sanitized Pinterest property confirmation.

All of those contracts already exist.

MCME-010 does **not** depend on publish adapter code, analytics collectors, a database, or content production.

## 15.2 Biggest remaining blocker

```text
REAL OWNER-GATED GATE A EVIDENCE
```

Specifically, the first blocker is:

```text
MCME-010:
  confirm real Owner-authorized Pinterest property

then MCME-011:
  establish real Awin relationship evidence
```

Until real Gate A evidence exists:

- no merchant is qualified;
- no production is allowed;
- no publishing is allowed;
- no commercial event can be observed.

## 15.3 Safe-prep gaps — do not block MCME-010

These are implementation gaps that should be absorbed into existing tasks rather than creating a competing task-number system.

### Gap A — machine-readable Gate A schema is still embedded in Markdown

Resolve by/before MCME-012:

- materialize `mcme_gate_a_evidence_v1.schema.json`;
- materialize merchant-qualification schema/template;
- add transition validator tests.

### Gap B — publish adapter/latch is not implemented

Resolve by MCME-031 readiness:

- implement deterministic publish-intent/latch store;
- implement dry-run/mock sink;
- pass duplicate/ambiguous-result tests.

No real Pinterest publish occurs during this prep.

### Gap C — Cash Truth ingest validator/private sink is not implemented

Resolve by MCME-031 launch readiness:

- validate against existing `mcme_cash_truth_v1.schema.json`;
- use local/private append-only JSONL;
- test dedupe/reversal/CASH_SETTLED rules.

A database is not needed.

### Gap D — observation capture method is not yet source-instantiated

Resolve in MCME-031/033:

- identify actual Pinterest/network read method after account access exists;
- keep cadence UNKNOWN until real source capability is known.

Manual exports/snapshots are acceptable for first experiment.

## 15.4 Hidden dependencies

Known hidden dependencies, now explicit:

1. Pinterest/browser/account access must exist before real publish.
2. Network/merchant reporting must expose enough identifiers for attribution/reconciliation; if not, evidence stays at the strongest defensible scope.
3. Merchant terms may require a specific link/deep-link/bridge method; Gate A must resolve this before production.
4. Actual reporting delay/validation windows remain UNKNOWN and cannot be replaced with invented observation durations.
5. Public Git cannot be assumed safe for raw real-economics/account evidence; private ledger/reference layer is required.
6. External publish ambiguity must be reconciled before retry.
7. Cash Truth sink and idempotency tests must be ready before first publish so events are not reconstructed from memory later.

None of these require reopening MCME-001→008 strategy.

---

# 16. Deployment readiness conclusion

```text
strategy_ready:
  YES

MCME-010_operationally_ready:
  YES

actual_Gate_A_executed:
  NO

current_evidence:
  L0

production_ready_now:
  NO

publish_ready_now:
  NO

first_real_cash_proven:
  NO

biggest_blocker:
  Owner-gated real Gate A evidence

safe_prep_remaining:
  machine-readable Gate A schema
  publish latch/dry-run adapter
  Cash Truth validator/private JSONL sink
  source-specific observation capture contract

database_required_for_3_pin_MVP:
  NO

24_7_automation_ready:
  NO
```

The smallest reliable next real action remains:

```text
MCME-010 — Owner Pinterest property confirmation
```

No MCME-010 action is executed in MCME-009.

---

# 17. Hard stop

MCME-009 is planning-only.

It does **not**:

- reopen market/language/platform/model/niche/sub-problem/format;
- create any account;
- login/apply;
- handle credentials/MFA/CAPTCHA;
- perform KYC/tax/payment;
- generate a Pin;
- publish a Pin;
- contact merchants;
- spend money;
- create fake/test traffic/purchases;
- reintroduce SaydiVoice/video;
- deploy 24/7 automation;
- build a Content Factory;
- execute MCME-010.

**STOP after MCME-009.**
