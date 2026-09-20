# MCME SAFE-PREP WAVES V1

**Project:** MAGASIN CONTENT MONEY ENGINE  
**Repository:** `magasincoffee/MAGASIN-CONTENT-MONEY-ENGINE`  
**Plan owner:** Brain — lane-2 ROBOT AUTO GIAO VIỆC KIẾM TIỀN  
**Status:** LOCKED PLAN / READY FOR SEQUENTIAL DISPATCH  
**Five-Step:** QUESTION → DELETE → SIMPLIFY → ACCELERATE → AUTOMATE  
**Canonical purpose:** Move as much future work as safely possible into `PREPARED` state before Owner performs merchant/KYC/payment actions, without fabricating evidence or bypassing dependency gates.

---

## 1. Owner decision

Owner has explicitly chosen the following operating mode:

> Robot/Work should complete all safe preparatory work first. Owner-required account, merchant, legal, KYC, tax, payment, MFA/OTP/CAPTCHA and settled-funds actions will be performed later by Owner.

This plan does **not** authorize Work/Robot to perform protected Owner actions.

---

## 2. Hard operating law

Every future task must distinguish preparation from execution:

```text
PREPARED
→ WAIT_REAL_EVIDENCE
→ EXECUTED
→ BRAIN_ACCEPTED
```

Definitions:

- `PREPARED`: code, schema, template, evaluator, tests, adapters, reconciliation logic or documentation is ready.
- `WAIT_REAL_EVIDENCE`: task cannot advance without real provider/account/merchant/payment evidence.
- `EXECUTED`: canonical task has actually run on real evidence or performed its explicitly authorized external action.
- `BRAIN_ACCEPTED`: Brain has verified the result against canonical repo state.

A task may reach `PREPARED` before its runtime dependency exists. It may **not** reach `EXECUTED`, `PASS`, `READY` or equivalent merely because preparation is complete.

### Non-negotiable guardrails

1. UNKNOWN never becomes VERIFIED/PASS without real evidence.
2. No fabricated merchant, account, tracking, commission, payout or cash evidence.
3. No merchant application without Owner action/authorization.
4. No KYC/tax/payment setup by Robot.
5. No credential, OTP, MFA, CAPTCHA, bank/account number or identity-document handling by Robot.
6. No commercial publish before canonical Gate A PASS.
7. No duplicate/blind publish retry.
8. Historical evidence is append-only/superseding; do not erase prior WAIT/FAIL truth.
9. Current critical-path semantics in `MCME-007_FIRST_CASH_IMPLEMENTATION_BACKLOG.md` remain authoritative.
10. If prep discovers a semantic bug in canonical runtime/evaluator, stop and report exact evidence; do not silently redefine the contract.

---

## 3. WAVE 0 — Close current Awin network reevaluation

### Active task

`MCME-012/AWIN-NETWORK-REEVALUATION-01`

This task remains ahead of the SAFE-PREP waves because it is already active.

Expected decision boundary:

- If canonical evaluator returns `NETWORK_READY`: record real network-layer result and stop for Brain acceptance.
- If not: fail closed and preserve exact reasons.
- Do not run MCME-013 automatically.

The SAFE-PREP waves below may begin only after Brain receives a coherent result from the current active task, unless Brain explicitly dispatches a preparation-only task that cannot conflict with current files.

---

# 4. WAVE 1 — Gate-A evaluator and evidence preparation

**Goal:** make future merchant/network evaluation tasks require only real sanitized evidence + deterministic execution.

## 4.1 Tasks covered

Preparation targets:

```text
MCME-014
MCME-016
MCME-018
MCME-020
MCME-022
MCME-024
MCME-026
MCME-028
```

### MCME-014 PREP — Awin candidate 1 evaluator readiness

Prepare only:

- candidate-slot `AWIN-01` evidence input template;
- field mapping for merchant relationship;
- US geography permission;
- Pinterest/social permission;
- direct/deep-link permission;
- tracking capability;
- commissionable action;
- validation/reversal terms;
- payout fields;
- rights/disclosure fields;
- deterministic evaluator replay;
- fail-closed test cases;
- output artifact schema/template;
- evidence digest/reconciliation rules.

Do not invent a merchant. Do not apply to a merchant.

### MCME-016 PREP — Awin candidate 2 evaluator readiness

Prepare the same deterministic machinery for bounded slot `AWIN-02`.

Hard invariant:

```text
AWIN-02 runtime execution is forbidden until MCME-014 records candidate 1 terminal MERCHANT_FAIL.
```

Preparation itself is allowed.

### MCME-018 PREP — impact.com NETWORK_READY evaluator readiness

Prepare:

- impact network/property evidence mapping;
- candidate slots `IMPACT-01` / `IMPACT-02` compatibility;
- network READY / WAIT_OWNER / FAIL classifications;
- deterministic test fixtures;
- output template.

Do not create or modify a real impact.com account.

### MCME-020 PREP — impact candidate 1 evaluator readiness

Prepare deterministic merchant candidate evaluator for `IMPACT-01`.

### MCME-022 PREP — impact candidate 2 evaluator readiness

Prepare deterministic merchant candidate evaluator for `IMPACT-02`.

### MCME-024 PREP — Amazon conditional eligibility evaluator readiness

Prepare eligibility-only contract and fail-closed evaluation.

Amazon remains conditional fallback only.

### MCME-026 PREP — Amazon terminal money-path evaluator readiness

Prepare the bounded terminal evaluation logic without account creation or application.

### MCME-028 PREP — Final Gate-A decision readiness

Prepare deterministic final decision package:

```text
PASS
WAIT_OWNER
FAIL
```

The final runtime decision must consume only accepted real upstream evidence.

### WAVE 1 Definition of Done

Wave 1 is prepared only when:

- all preparation artifacts are clearly marked `PREPARED_ONLY`;
- all tests are deterministic;
- no real account mutation occurred;
- no UNKNOWN was promoted;
- future runtime tasks can consume sanitized evidence without redesign;
- repo QA passes.

---

# 5. WAVE 2 — Production and publish preparation

**Goal:** prepare the complete post-Gate-A production/publishing machinery while keeping real commercial output blocked.

## 5.1 Tasks covered

```text
MCME-029
MCME-030
MCME-031
MCME-032
```

### MCME-029 PREP — Minimum content specification framework

Prepare:

- canonical 3-Pin specification template;
- merchant/offer binding placeholders;
- title/hook/body/CTA constraints;
- original-content/rights fields;
- affiliate disclosure slot;
- destination/tracking fields;
- deterministic content IDs.

Do not lock a fake merchant-specific offer.

### MCME-030 PREP — Exactly 3 static Pins production pipeline

Prepare:

- deterministic input/output contract;
- static 2:3 Pin generation pipeline;
- three canonical concepts:
  1. Measure Before You Buy
  2. Which Bin Shape Fits This Shelf?
  3. Fridge Fit Mistakes to Check Before Ordering
- content ID/version rules;
- asset manifest;
- regeneration/reconciliation rules.

Commercial final assets remain blocked until Gate A PASS and real merchant/offer binding exist.

### MCME-031 PREP — QA + publish-readiness + observation-window lock

Prepare:

- visual/content QA checklist;
- disclosure QA;
- rights QA;
- destination validation;
- tracking validation;
- duplicate/content-version check;
- fixed observation-window contract;
- launch readiness result schema.

### MCME-032 PREP — Idempotent Pinterest publish harness

Prepare only:

- publish adapter;
- pre-action persisted latch;
- deterministic publish key;
- duplicate prevention;
- uncertain-result reconciliation;
- post-action Pin ID reconciliation;
- no-blind-retry rule;
- auth/MFA/CAPTCHA stop rules.

Hard invariant:

```text
NO FINAL GATE A PASS
= NO REAL COMMERCIAL PUBLISH
```

### WAVE 2 Definition of Done

Wave 2 is prepared only when the path from accepted merchant/offer → 3 assets → QA → idempotent publish can execute without new architecture work.

No real commercial Pin must be published during preparation.

---

# 6. WAVE 3 — Observation, Cash Truth and economics preparation

**Goal:** make post-publish measurement and first-real-cash reconciliation ready before traffic exists.

## 6.1 Tasks covered

```text
MCME-033
MCME-034
MCME-035
MCME-036
MCME-038
```

### MCME-033 PREP — Bounded observation collector

Prepare collectors/adapters for:

- Pinterest impressions;
- Pin clicks;
- outbound clicks;
- network clicks if available;
- merchant actions;
- commission status observations;
- source timestamps;
- stable provider IDs.

Missing observation must remain UNKNOWN unless provider evidence proves zero.

### MCME-034 PREP — Cash Truth V1 ingestion + reconciliation

Prepare:

- normalization into `06_METRICS/mcme_cash_truth_v1.schema.json`;
- append-only event writer;
- provider-ID dedupe;
- conservative reconciliation;
- correction/reversal event logic;
- no inferred revenue/cash;
- deterministic validation.

### MCME-035 PREP — KEEP / KILL / SCALE decision package

Prepare the decision engine and evidence thresholds.

Hard rules:

- views alone never SCALE;
- clicks alone never SCALE;
- L1 = learning only;
- SCALE requires at least tracked merchant action + attributed commission (L2);
- decisions reference exact evidence/ledger version.

Runtime Brain decision remains a Brain responsibility.

### MCME-036 PREP — Commission lifecycle observation

Prepare state observation/reconciliation for:

```text
COMMISSION_PENDING
COMMISSION_VALIDATED
COMMISSION_REVERSED
COMMISSION_PAYABLE
PAYOUT_ISSUED
```

Do not equate `PAYOUT_ISSUED` with cash received.

### MCME-038 PREP — FIRST REAL CASH reconciliation

Prepare deterministic reconciliation for:

```text
provider payout
→ Owner sanitized settled-funds evidence
→ CASH_SETTLED
→ direct cash cost/time
→ measured net cash contribution
```

FIRST REAL CASH remains impossible until Owner supplies MCME-037 settled-funds evidence.

### WAVE 3 Definition of Done

The system is ready to ingest real post-publish observations and reconcile through first settled cash without redesign or manual spreadsheet improvisation.

---

# 7. Owner-required tasks intentionally deferred

These tasks are **not delegated to Robot for execution**:

```text
MCME-013 — Awin merchant candidate 1 evidence/application
MCME-015 — Awin merchant candidate 2 evidence/application if required
MCME-017 — impact.com relationship/account action if fallback required
MCME-019 — impact merchant candidate 1
MCME-021 — impact merchant candidate 2
MCME-023 — Amazon conditional eligibility/account action if fallback required
MCME-025 — Amazon money-path evidence if eligible
MCME-027 — winning-path KYC/tax/payment readiness
MCME-037 — settled-funds confirmation
```

Owner also retains all interventions involving:

- credentials;
- MFA;
- OTP;
- CAPTCHA;
- KYC;
- tax declarations;
- identity documents;
- legal acceptance;
- payout account setup;
- banking/payment rails;
- platform appeal/suspension;
- destructive account actions.

---

# 8. Dispatch order

Brain should dispatch **one Work task at a time**.

Preferred order after current MCME-012 reevaluation is coherently closed:

```text
WAVE 1
014-PREP
→ 016-PREP
→ 018-PREP
→ 020-PREP
→ 022-PREP
→ 024-PREP
→ 026-PREP
→ 028-PREP

WAVE 2
→ 029-PREP
→ 030-PREP
→ 031-PREP
→ 032-PREP

WAVE 3
→ 033-PREP
→ 034-PREP
→ 035-PREP
→ 036-PREP
→ 038-PREP
```

Brain may delete a prep task if canonical code already proves the required capability exists. Five-Step `DELETE` applies before adding new code.

---

# 9. Preparation audit matrix

For every SAFE-PREP task Work must return:

```text
task_id
status=COMPLETE|BLOCKED
result=PREPARED_ONLY|ALREADY_SATISFIED|BLOCKED
exact_commit_sha
branch
files_changed
canonical_inputs
what_was_prepared
tests_run
repo_qa
real_evidence_consumed=false unless explicitly authorized
external_side_effect=false
owner_action_performed=false
unknown_promoted=false
historical_evidence_preserved=true
runtime_dependency_still_required
recommendation_for_brain
```

If any of the last four safety assertions are false, Brain must review before acceptance.

---

# 10. Owner return path

When Owner is ready to perform the real account steps, execution resumes at the earliest unmet Owner gate.

If Awin network is NETWORK_READY, expected first Owner task is:

```text
MCME-013 — Awin merchant candidate 1 evidence
```

After Owner supplies real sanitized evidence, the already-prepared Work evaluator executes immediately.

This pattern repeats:

```text
OWNER REAL ACTION
→ SANITIZED EVIDENCE
→ PREPARED EVALUATOR EXECUTES
→ BRAIN ACCEPT/REJECT
→ NEXT DEPENDENCY
```

---

# 11. Commercial launch boundary

The system is considered commercially live only after:

```text
MCME-028 = FINAL GATE A PASS
→ MCME-029 runtime spec bound to real merchant/offer
→ MCME-030 final 3 Pin assets
→ MCME-031 publish readiness PASS
→ MCME-032 real idempotent Pinterest publish
```

SAFE-PREP completion does not equal launch.

---

# 12. FIRST REAL CASH boundary

```text
FIRST REAL CASH
=
real commission lifecycle
+ payout issued
+ Owner confirms funds actually received on authorized rail
+ MCME-038 reconciliation records CASH_SETTLED
```

Network dashboards, clicks, sales, pending commission or payout-issued state alone are not settled cash.

---

# 13. Plan lock

This plan is the canonical Brain operating plan for the Owner-approved period in which Robot performs safe preparation first and Owner performs protected real-world actions later.

Changes require a new Brain decision and a superseding committed plan or explicit amendment.

**Do not reinterpret this plan as authorization to bypass the existing critical-path dependencies.**
