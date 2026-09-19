# MCME-007 — FIRST-CASH IMPLEMENTATION BACKLOG

**Task:** MCME-007  
**Repository:** `magasincoffee/MAGASIN-CONTENT-MONEY-ENGINE`  
**Canonical input:** MCME-006 accepted by Brain at commit `df5d8701cd199f41736fc53d292b00aa987234bd`  
**Five-Step:** ACCELERATE  
**Current evidence level:** `L0_NO_REAL_COMMERCIAL_EVIDENCE`  
**Actual Gate A:** `OWNER_GATED_NOT_EXECUTED`  
**Cash truth sink:** `06_METRICS/mcme_cash_truth_v1.schema.json`

## 1. Acceleration law

The shortest path to FIRST REAL CASH is:

```text
REAL GATE A EVIDENCE
→ GATE A PASS
→ LOCK REAL OFFER + 3-PIN SPEC
→ PRODUCE EXACTLY 3 STATIC PINS
→ QA + LOCK OBSERVATION WINDOW
→ IDEMPOTENT PUBLISH
→ OBSERVE
→ INGEST CASH TRUTH EVENTS
→ KEEP/KILL/SCALE DECISION
→ VALIDATION/PAYABLE/PAYOUT
→ OWNER-AUTHORIZED FUNDS RECEIVED
→ FIRST REAL CASH
```

Current blocker is **not content production**. Current blocker is **real Gate A evidence**.

Hard invariant:

```text
NO GATE A PASS
=
NO PIN PRODUCTION
=
NO PUBLISH
=
NO CONTENT FACTORY
```

Anything that does not shorten the path above is deleted or deferred.

---

# 2. Fixed route and experiment

These are locked unless Brain records fatal evidence:

```text
Market: United States
Language: English
Distribution: Pinterest organic Pins
Monetization: Affiliate commerce
Niche: Small-space kitchen organization
First sub-problem: Fridge storage / fit
Format: Static 2:3 original checklist Pin
Gate B batch: exactly 3 Pins
Network order: Awin → impact.com → Amazon Associates conditional
SaydiVoice: DEFERRED / DELETED from first experiment
Video: DEFERRED / DELETED from first experiment
Paid media: DEFERRED
Cash truth: MCME Cash Truth Event Ledger V1
```

Canonical 3-Pin concepts after Gate A PASS:

1. Measure Before You Buy
2. Which Bin Shape Fits This Shelf?
3. Fridge Fit Mistakes to Check Before Ordering

No production asset is created in MCME-007.

---

# 3. Execution classes

Every future task carries one or more execution classes:

- `SAFE_PREP` — repository/read-only preparation with no protected account action.
- `OWNER_REQUIRED` — Owner must perform account/legal/payment/identity action.
- `READ_ONLY_EXTERNAL` — read/observe authorized external evidence without mutation.
- `REVERSIBLE_REPO_CHANGE` — bounded repository artifact/config change.
- `EXTERNAL_SIDE_EFFECT` — publishing or another real-world external mutation.
- `AUTOMATION_AFTER_PROOF` — automation explicitly blocked until evidence threshold is reached.

---

# 4. Ordered critical path IDs

The durable future IDs begin at `MCME-010`.

```text
MCME-010  Owner Pinterest property confirmation
MCME-011  Owner Awin network relationship evidence
MCME-012  Work Awin NETWORK_READY evaluation
MCME-013  Owner Awin merchant candidate 1 evidence
MCME-014  Work Awin candidate 1 Gate-A evaluation
MCME-015  Owner Awin merchant candidate 2 evidence       [only if candidate 1 fails]
MCME-016  Work Awin candidate 2 Gate-A evaluation         [only if candidate 1 fails]
MCME-017  Owner impact.com network relationship evidence  [only if Awin bounded path fails]
MCME-018  Work impact.com NETWORK_READY evaluation
MCME-019  Owner impact.com merchant candidate 1 evidence
MCME-020  Work impact.com candidate 1 Gate-A evaluation
MCME-021  Owner impact.com merchant candidate 2 evidence  [only if candidate 1 fails]
MCME-022  Work impact.com candidate 2 Gate-A evaluation
MCME-023  Owner Amazon conditional eligibility evidence   [only if Awin + impact fail]
MCME-024  Work Amazon conditional eligibility evaluation
MCME-025  Owner Amazon money-path evidence                [only if eligibility VERIFIED]
MCME-026  Work Amazon / terminal Gate-A evaluation
MCME-027  Owner winning-path KYC/tax/payment readiness    [only when actually required]
MCME-028  Work FINAL Gate-A PASS / WAIT_OWNER / FAIL decision
MCME-029  Work post-Gate-A minimum content specification
MCME-030  Work produce exactly 3 static Pins
MCME-031  Work QA + publish-readiness + observation-window lock
MCME-032  Work/Robot idempotent Pinterest publish
MCME-033  Robot/Work bounded observation collection
MCME-034  Work Cash Truth V1 ingestion + reconciliation
MCME-035  Brain KEEP / KILL / SCALE decision
MCME-036  Robot/Work validation/payable/payout observation
MCME-037  Owner settled-funds confirmation packet
MCME-038  Work FIRST REAL CASH reconciliation
```

This is one critical path with **bounded conditional fallbacks**, not parallel strategies.

The first future task after `MCME-RUN-8H-01` is:

```text
MCME-010 — Owner Pinterest property confirmation
```

---

# 5. Task cards

## MCME-010 — Confirm real Pinterest property

**Objective:** establish the exact Owner-authorized Pinterest property that Gate A and Gate B will use.  
**Five-Step stage:** ACCELERATE.  
**Dependency/precondition:** MCME-007 accepted.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** account ownership only; no credentials returned to Work.  
**Input evidence/artifacts:** MCME-005 Gate A contract; fixed route.  
**Exact output:** sanitized property confirmation: property type, public handle/URL if safe, authorized=yes/no, checked_at.  
**Definition of Done:** one real Pinterest property is confirmed for MCME or a terminal property blocker is reported.  
**STOP/FAIL:** no property / property cannot be used → WAIT_OWNER or Brain review; do not advance.  
**Reversible:** yes.  
**External side effect:** no required mutation; confirmation only.  
**Idempotency/reconciliation:** property identity must be stable; repeated confirmation reconciles to the same public/sanitized property reference.  
**Next gate on PASS:** MCME-011.

---

## MCME-011 — Establish Awin network relationship evidence

**Objective:** obtain real sanitized evidence that Owner can use Awin with the confirmed property.  
**Five-Step stage:** ACCELERATE.  
**Dependency:** MCME-010 PASS.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** Owner performs join/login/legal/verification actions directly.  
**Input:** property confirmation + MCME-005 Owner Action Packet.  
**Exact output:** sanitized network status: active/pending/rejected/blocked, property accepted yes/no/unknown, observed_at.  
**DoD:** enough evidence exists for Work to classify Awin relationship.  
**STOP/FAIL:** pending → WAIT_OWNER; terminal incompatible → allow fallback only after MCME-012 records it.  
**Reversible:** account/legal actions may not be fully reversible; task record itself is reversible repo evidence.  
**External side effect:** yes, only when Owner performs account/legal setup.  
**Idempotency:** one network relationship record keyed by network + Owner/property sanitized identity; never duplicate account creation.  
**Next gate:** MCME-012.

---

## MCME-012 — Evaluate Awin NETWORK_READY

**Objective:** ingest sanitized evidence into `mcme.gate-a-evidence.v1` and decide NETWORK_READY / WAIT_OWNER / FALLBACK-ELIGIBLE.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-011 evidence.  
**Executor:** WORK.  
**Execution class:** `SAFE_PREP`, `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Owner boundary:** no login/account mutation.  
**Input:** sanitized Awin relationship evidence.  
**Exact output:** Gate A evidence record + state transition.  
**DoD:** state is unambiguous and every material field is VERIFIED/UNKNOWN/BLOCKED/FAIL.  
**STOP/FAIL:** UNKNOWN/BLOCKED never becomes PASS.  
**Reversible:** repo record yes; external facts append-only.  
**External side effect:** no.  
**Idempotency:** same sanitized network evidence must reconcile, not create duplicate relationships.  
**Next gate:** NETWORK_READY → MCME-013; terminal network fail → MCME-017.

---

## MCME-013 — Awin merchant candidate 1 evidence

**Objective:** Owner checks exactly one US fridge-storage merchant program on Awin.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-012 NETWORK_READY.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** application/terms handled by Owner only.  
**Input:** merchant-qualification template.  
**Exact output:** sanitized merchant name/program, relationship state, US allowed, Pinterest/social allowed, direct/deep-link status, commissionable action known, validation/reversal known, payout feasibility, rights/disclosure status.  
**DoD:** candidate 1 has enough sanitized evidence for evaluation.  
**STOP/FAIL:** pending → WAIT_OWNER; no second candidate until MCME-014 decides.  
**Reversible:** merchant application may not be reversible; evidence record is append-only.  
**External side effect:** possible Owner application only.  
**Idempotency:** candidate slot = Awin/1; never blindly reapply.  
**Next gate:** MCME-014.

---

## MCME-014 — Evaluate Awin candidate 1

**Objective:** determine provisional Gate-A viability of Awin candidate 1.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-013.  
**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Owner boundary:** none crossed.  
**Input:** candidate 1 sanitized record.  
**Exact output:** PASS-TO-PAYOUT-READINESS / WAIT_OWNER / MERCHANT_FAIL.  
**DoD:** all non-protected merchant/tracking/terms evidence classified.  
**STOP/FAIL:** critical FAIL → candidate 1 rejected.  
**Reversible:** repo evaluation yes.  
**External side effect:** no.  
**Idempotency:** evaluation references candidate slot Awin/1 and evidence digest.  
**Next gate:** provisional viable → MCME-027; fail → MCME-015.

---

## MCME-015 — Awin merchant candidate 2 evidence

Same contract as MCME-013, but candidate slot = Awin/2.

**Dependency:** MCME-014 MERCHANT_FAIL.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Bound:** this is the final Awin merchant slot.  
**Next gate:** MCME-016.

---

## MCME-016 — Evaluate Awin candidate 2

Same evaluation contract as MCME-014.

**Dependency:** MCME-015.  
**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**STOP/FAIL:** candidate 2 fail exhausts Awin.  
**Next gate:** provisional viable → MCME-027; Awin exhausted → MCME-017.

---

## MCME-017 — Establish impact.com network relationship evidence

Same network-relationship pattern as MCME-011.

**Dependency:** Awin bounded path exhausted.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** Owner handles account/legal/identity.  
**Next gate:** MCME-018.

---

## MCME-018 — Evaluate impact.com NETWORK_READY

Same structure as MCME-012.

**Dependency:** MCME-017.  
**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Next gate:** ready → MCME-019; terminal impact incompatibility → MCME-023.

---

## MCME-019 — impact.com merchant candidate 1 evidence

Same merchant evidence contract as MCME-013.

**Dependency:** MCME-018 NETWORK_READY.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Candidate slot:** impact/1.  
**Public-path hint:** OXO may be evaluated, but approval must not be assumed.  
**Next gate:** MCME-020.

---

## MCME-020 — Evaluate impact.com candidate 1

Same evaluation contract as MCME-014.

**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Next gate:** provisional viable → MCME-027; fail → MCME-021.

---

## MCME-021 — impact.com merchant candidate 2 evidence

Same contract as MCME-019.

**Dependency:** MCME-020 fail.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Candidate slot:** impact/2.  
**Next gate:** MCME-022.

---

## MCME-022 — Evaluate impact.com candidate 2

Same evaluation contract as MCME-020.

**STOP/FAIL:** fail exhausts impact.com bounded merchant search.  
**Next gate:** provisional viable → MCME-027; exhausted → MCME-023.

---

## MCME-023 — Amazon conditional eligibility evidence

**Objective:** determine whether the real property/Owner configuration is eligible for the Amazon fallback at all.  
**Five-Step:** ACCELERATE.  
**Dependency:** Awin + impact.com exhausted.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** any Amazon account/legal action remains Owner-only.  
**Input:** MCME-002/005 conditional Amazon rules.  
**Exact output:** sanitized eligibility state: VERIFIED / UNKNOWN / BLOCKED / FAIL.  
**DoD:** eligibility is unambiguous.  
**STOP/FAIL:** anything other than VERIFIED blocks Amazon path.  
**Reversible:** evidence record yes; account actions may not be.  
**External side effect:** only Owner-side protected action if required.  
**Idempotency:** do not create duplicate Amazon relationships.  
**Next gate:** MCME-024.

---

## MCME-024 — Evaluate Amazon conditional eligibility

**Objective:** decide whether Amazon fallback may be attempted.  
**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Dependency:** MCME-023.  
**Exact output:** AMAZON_ELIGIBLE or TERMINAL_GATE_A_FAIL.  
**STOP/FAIL:** UNKNOWN/BLOCKED/FAIL → terminal Gate A FAIL; no workaround.  
**Next gate:** eligible → MCME-025; otherwise → MCME-028 terminal evaluation.

---

## MCME-025 — Amazon money-path evidence

**Objective:** Owner provides one bounded Amazon fallback money-path record.  
**Dependency:** MCME-024 AMAZON_ELIGIBLE.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** Owner handles account/legal/payment actions.  
**Exact output:** sanitized property/link/action/validation/payout/rights evidence.  
**DoD:** one path can be evaluated.  
**STOP/FAIL:** no second Amazon slot.  
**Idempotency:** one conditional Amazon path only.  
**Next gate:** MCME-026.

---

## MCME-026 — Evaluate Amazon / terminal Gate A path

**Objective:** evaluate the final allowed fallback.  
**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Dependency:** MCME-025.  
**Exact output:** provisional viable → MCME-027, or terminal FAIL.  
**STOP/FAIL:** fail → bounded fallback exhausted → Gate A FAIL → KILL niche → stop.  
**Next gate:** viable → MCME-027; fail → MCME-028 terminal record.

---

## MCME-027 — Winning-path KYC/tax/payment readiness

**Objective:** complete only the protected setup actually required for the one surviving merchant path.  
**Five-Step:** ACCELERATE.  
**Dependency:** one merchant path is provisionally viable.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** KYC, tax, bank/PayPal/Payoneer, legal acceptance are Owner-only.  
**Input:** winning network/merchant requirements.  
**Exact output:** sanitized statuses only: setup complete yes/no, payout rail type, threshold/cycle facts, checked_at.  
**DoD:** payout feasibility and protected prerequisites are either VERIFIED or clearly BLOCKED/FAIL.  
**STOP/FAIL:** no secrets/private identifiers returned; blocked → WAIT_OWNER; impossible → fail winning path and follow only remaining bounded fallback if one exists, otherwise terminal fail.  
**Reversible:** not necessarily.  
**External side effect:** yes, Owner-side only.  
**Idempotency:** setup relationship must be reconciled; never create duplicate payout rails.  
**Next gate:** MCME-028.

---

## MCME-028 — FINAL Gate A decision

**Objective:** ingest all sanitized winning-path evidence into `mcme.gate-a-evidence.v1` and decide PASS / WAIT_OWNER / FAIL.  
**Five-Step:** ACCELERATE.  
**Dependency:** all critical Gate A evidence for the surviving path.  
**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Owner boundary:** no protected action.  
**Input:** Gate A evidence contract + winning merchant qualification record.  
**Exact output:** canonical Gate A state + Gate B handoff fields if PASS.  
**DoD:** PASS only if every critical field is VERIFIED.  
**STOP/FAIL:** UNKNOWN/BLOCKED never PASS. Terminal FAIL → KILL niche → no content.  
**Reversible:** repo decision append-only; corrected evidence becomes new revision/evidence record.  
**External side effect:** no.  
**Idempotency:** deterministic Gate A evaluation keyed by evidence set/version.  
**Next gate:** PASS → MCME-029.

---

## MCME-029 — Post-Gate-A minimum content specification

**Objective:** only now lock the actual merchant/program, destination, link method, attribution key/sub-ID method, disclosure wording, asset rights and exact 3-Pin specification.  
**Five-Step:** SIMPLIFY → ACCELERATE.  
**Dependency:** MCME-028 PASS.  
**Executor:** WORK.  
**Execution class:** `SAFE_PREP`, `REVERSIBLE_REPO_CHANGE`.  
**Owner boundary:** none crossed.  
**Input:** sanitized Gate B handoff.  
**Exact output:** production-ready spec for exactly 3 static Pins; no additional batch.  
**DoD:** every Pin has deterministic content_id/framing_id, compliant CTA/link rules, disclosure and asset constraints.  
**STOP/FAIL:** missing tracking/disclosure/rights field → return to Gate A evidence; do not produce.  
**Reversible:** yes.  
**External side effect:** no.  
**Idempotency:** same Gate B handoff yields same deterministic 3-Pin spec version.  
**Next gate:** MCME-030.

---

## MCME-030 — Produce exactly 3 static Pins

**Objective:** produce only the three locked original static Pins.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-029 PASS.  
**Executor:** WORK.  
**Execution class:** `REVERSIBLE_REPO_CHANGE`.  
**Owner boundary:** no account action.  
**Input:** production spec.  
**Exact output:** exactly 3 production assets + metadata:
- Measure Before You Buy
- Which Bin Shape Fits This Shelf?
- Fridge Fit Mistakes to Check Before Ordering

**DoD:** 3 and only 3 static 2:3 original graphics; deterministic content IDs; original-graphics-only unless real rights explicitly allow merchant assets.  
**STOP/FAIL:** any rights/disclosure ambiguity → stop; no publish.  
**Reversible:** yes.  
**External side effect:** no.  
**Idempotency:** content build keyed by content_id + spec version; rerun must not create extra variants silently.  
**Next gate:** MCME-031.

---

## MCME-031 — QA + publish readiness + observation-window lock

**Objective:** certify the 3 assets and lock one fixed equal observation window before any publishing.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-030.  
**Executor:** WORK.  
**Execution class:** `SAFE_PREP`, `REVERSIBLE_REPO_CHANGE`.  
**Owner boundary:** none crossed.  
**Input:** 3 assets + Gate B handoff.  
**Exact output:** QA manifest containing dimensions, originality, rights, disclosure, destination, tracking/sub-ID, no-sensitive-data check, publish intent IDs, observation window start-rule/end-rule.  
**DoD:** all 3 PASS QA; observation window is fixed before publish.  
**STOP/FAIL:** any one Pin fails → fix only that asset, re-QA; do not publish partial batch unless Brain explicitly changes experiment.  
**Reversible:** yes.  
**External side effect:** no.  
**Idempotency:** QA manifest version bound to exact asset hashes/content IDs.  
**Next gate:** MCME-032.

---

## MCME-032 — Idempotent Pinterest publishing

**Objective:** publish each intended Pin exactly once.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-031 PASS + explicit authorization for external side effect.  
**Executor:** WORK/ROBOT.  
**Execution class:** `EXTERNAL_SIDE_EFFECT`.  
**Owner boundary:** authentication/MFA/CAPTCHA is Owner-only; fail closed.  
**Input:** publish manifest for exactly 3 content IDs.  
**Exact output:** Pinterest published Pin IDs reconciled to content IDs + `PIN_PUBLISHED` Cash Truth events.  
**DoD:** each intended content_id maps to exactly one confirmed published Pin ID.  
**STOP/FAIL:** auth/MFA/CAPTCHA, ambiguous prior send, missing confirmation, or conflict → stop and reconcile; never blind resend.  
**Reversible:** platform deletion may be possible but publishing itself is an external side effect and not treated as trivially reversible.  
**External side effect:** yes.  
**Idempotency requirement:**
- deterministic publish key = experiment_id + content_id + destination version;
- persist pre-action latch/state before send;
- one bounded publish action per intended Pin;
- after uncertain result, search/reconcile published Pin ID before any retry;
- no duplicate publish to "be safe".
**Next gate:** MCME-033.

---

## MCME-033 — Bounded observation collection

**Objective:** observe the pre-locked window without artificial interaction.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-032 reconciled publication + locked observation window.  
**Executor:** ROBOT/WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`.  
**Owner boundary:** no artificial clicks or purchases.  
**Input:** Pin IDs, tracking identifiers, observation window.  
**Exact output:** raw/sanitized Pinterest and network observations: impressions, Pin clicks, outbound clicks, network clicks, merchant actions, commission states if any.  
**DoD:** collection covers the fixed window and source timestamps; no fabricated missing values.  
**STOP/FAIL:** source unavailable → record UNKNOWN/BLOCKED; do not infer zero unless provider observation proves zero.  
**Reversible:** read-only.  
**External side effect:** no.  
**Idempotency:** repeated polling dedupes by provider stable ID/snapshot key.  
**Next gate:** MCME-034.

---

## MCME-034 — Cash Truth V1 ingestion + reconciliation

**Objective:** append real events into Cash Truth V1.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-033 evidence.  
**Executor:** WORK.  
**Execution class:** `REVERSIBLE_REPO_CHANGE`, `READ_ONLY_EXTERNAL`.  
**Owner boundary:** no private payment identifiers.  
**Input:** sanitized source observations.  
**Exact output:** append-only canonical events validated against `mcme_cash_truth_v1.schema.json`; reconciliation status.  
**DoD:** no double-count; no inferred sale/revenue/cash; money states separated.  
**STOP/FAIL:** ambiguous source identity → CONSERVATIVE_RECONCILIATION / UNKNOWN; never fabricate join.  
**Reversible:** event ledger itself is append-only; corrections are new events, not destructive edits.  
**External side effect:** no.  
**Idempotency:** stable provider IDs preferred; otherwise conservative reconciliation.  
**Next gate:** MCME-035.

---

## MCME-035 — KEEP / KILL / SCALE decision

**Objective:** Brain decides experiment path using L0/L1/L2/L3/L4 evidence and measured economics only.  
**Five-Step:** QUESTION → DELETE → ACCELERATE.  
**Dependency:** MCME-034.  
**Executor:** BRAIN.  
**Execution class:** `SAFE_PREP`.  
**Owner boundary:** none.  
**Input:** Cash Truth V1 evidence + Gate-B hypotheses.  
**Exact output:** KEEP / KILL / SCALE-ELIGIBLE decision with reason.  
**DoD rules:**
- L0/no distribution → revise distribution mechanics, not merchant economics;
- distribution but zero qualified outbound clicks → KILL/REVISE framing;
- L1 click → KEEP as learning only;
- SCALE is forbidden unless at least tracked merchant action + attributed commission (L2);
- views/clicks alone never SCALE.
**STOP/FAIL:** insufficient evidence → KEEP OBSERVING or STOP, not SCALE.  
**Reversible:** decision can be superseded by later evidence.  
**External side effect:** no.  
**Idempotency:** decision references exact ledger/evidence version.  
**Next gate:** if L2+ path survives → MCME-036; if KILL → stop/Brain redesign.

---

## MCME-036 — Validation / payable / payout observation

**Objective:** continue bounded read-only observation for commission lifecycle after an attributed action exists.  
**Five-Step:** ACCELERATE.  
**Dependency:** L2 evidence and MCME-035 KEEP/SCALE-ELIGIBLE.  
**Executor:** ROBOT/WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`.  
**Owner boundary:** no payout modification.  
**Input:** distinct commission/provider IDs.  
**Exact output:** append-only PENDING/VALIDATED/REVERSED/PAYABLE/PAYOUT_ISSUED evidence.  
**DoD:** provider lifecycle observed without promoting missing states.  
**STOP/FAIL:** reversal → record reversal; payout-issued alone is not cash.  
**Reversible:** read-only; ledger append-only.  
**External side effect:** no.  
**Idempotency:** provider record + canonical state/version prevents duplicate revenue.  
**Next gate:** PAYOUT_ISSUED or payable path ready → MCME-037.

---

## MCME-037 — Owner settled-funds confirmation packet

**Objective:** obtain minimum sanitized evidence that funds actually arrived on the Owner-authorized payout rail.  
**Five-Step:** ACCELERATE.  
**Dependency:** PAYOUT_ISSUED evidence or provider payout reference.  
**Executor:** OWNER.  
**Execution class:** `OWNER_REQUIRED`.  
**Owner boundary:** bank/payment account remains private.  
**Input:** payout reference/amount/currency/date sanitized from ledger.  
**Exact output:** sanitized confirmation:
- funds_received yes/no;
- Owner-authorized rail yes/no;
- received amount/currency;
- settled/posted timestamp;
- sanitized reconciliation reference;
- measured payout/payment fees if visible.

**DoD:** enough evidence exists to prove or reject CASH_SETTLED.  
**STOP/FAIL:** network "paid" without rail evidence → not settled cash; WAIT_OWNER.  
**Reversible:** evidence correction append-only.  
**External side effect:** no new financial action required; observation only.  
**Idempotency:** confirmation reconciles to the specific payout ID/reference, never counted twice.  
**Next gate:** MCME-038.

---

## MCME-038 — FIRST REAL CASH reconciliation

**Objective:** prove the locked FIRST REAL CASH definition and measured net economics.  
**Five-Step:** ACCELERATE.  
**Dependency:** MCME-037 + measured direct cost/time.  
**Executor:** WORK.  
**Execution class:** `READ_ONLY_EXTERNAL`, `REVERSIBLE_REPO_CHANGE`.  
**Owner boundary:** no raw bank/payment identifiers stored.  
**Input:** payout record, settled-funds evidence, direct cost/time events.  
**Exact output:** `CASH_SETTLED` event(s), payout-to-funds reconciliation, evidence level decision, measured net settled cash/direct cash cost/net cash contribution where currencies/scopes are valid.  
**DoD:** FIRST REAL CASH only if funds are actually received on Owner-authorized payout rail and reconciled to payable/payout record; cost/time measured.  
**STOP/FAIL:** missing rail evidence or unresolved reconciliation → remain below L4; do not claim cash.  
**Reversible:** append-only correction model.  
**External side effect:** no.  
**Idempotency:** payout ID + settlement evidence must reconcile one-to-one/one-to-many without double counting.  
**Next gate:** L4 reached → future economics review; 24/7 automation may be considered only after Brain explicitly authorizes it.

---

# 6. Bounded Gate A fallback algorithm

The path is deliberately finite:

```text
Awin:
  network relationship
  → candidate 1
  → candidate 2
  → exhausted

impact.com:
  network relationship
  → candidate 1
  → candidate 2
  → exhausted

Amazon:
  conditional eligibility must first be VERIFIED
  → one money path
  → exhausted

Total merchant/path candidate slots:
  maximum 5
```

Rules:

- no fourth network;
- no infinite advertiser search;
- no repeated blind application;
- a pending application is WAIT_OWNER, not failure and not PASS;
- UNKNOWN/BLOCKED never PASS;
- the first provisionally viable merchant path stops further candidate search and moves to MCME-027;
- terminal exhaustion → Gate A FAIL → KILL niche → no content;
- no automatic niche switch.

---

# 7. OWNER ACTION PACKET — one-sitting design

The goal is minimum interruptions.

## What Owner must do

### Phase A — property

Return only:

```text
Pinterest property authorized: YES/NO
Public/sanitized property reference: <safe value>
Checked at: <timestamp>
```

### Phase B — Awin first

Owner joins/signs in and handles legal/identity steps directly.

Return:

```text
Network: Awin
Relationship: ACTIVE / PENDING / REJECTED / BLOCKED
Property accepted: YES / NO / UNKNOWN
Checked at: <timestamp>
```

If ACTIVE, evaluate candidate 1, then candidate 2 only if Brain/Work asks after candidate 1 fails.

For each candidate return only:

```text
Network:
Merchant public name:
Relationship: APPROVED / JOINED / PENDING / REJECTED / BLOCKED
US allowed: YES / NO / UNKNOWN
Pinterest/social allowed: YES / NO / UNKNOWN
Direct link allowed: YES / NO / UNKNOWN
Deep link allowed: YES / NO / UNKNOWN
Commissionable action: VERIFIED / UNKNOWN / BLOCKED / FAIL
Validation/reversal rules: VERIFIED / UNKNOWN / BLOCKED / FAIL
Payout feasible: YES / NO / UNKNOWN
Asset rights: VERIFIED / UNKNOWN / BLOCKED / FAIL
Disclosure rule: VERIFIED / UNKNOWN / BLOCKED / FAIL
Checked at:
```

### Phase C — fallback

Only when Work records Awin exhaustion:

```text
impact.com:
  same packet
  max 2 merchant candidates
```

Only when both Awin and impact.com fail:

```text
Amazon:
  first return conditional eligibility
  proceed only if VERIFIED
  max 1 path
```

### Phase D — protected winning-path setup

Only after one merchant path survives:

```text
KYC/tax setup complete: YES/NO
Payment setup complete: YES/NO
Payout rail TYPE: BANK / PAYPAL / PAYONEER / OTHER_ALLOWED
Payout threshold/cycle: <sanitized fact if visible>
Checked at:
```

## Never requested from Owner

Never provide or commit:

- passwords;
- session cookies;
- API secrets;
- MFA/OTP/recovery codes;
- CAPTCHA artifacts;
- tax IDs;
- bank/account/routing/card numbers;
- identity documents;
- private payout identifiers;
- raw sensitive affiliate tracking tokens;
- private payment-provider identifiers.

Owner may provide a redacted screenshot only when the smallest relevant fragment is safe and contains no private value.

---

# 8. Time ordering / unblock map

## (1) Critical path order

```text
MCME-010
→ 011 → 012
→ 013 → 014
→ [015 → 016 if needed]
→ [017 → 018 → 019 → 020 → 021 → 022 if Awin exhausted]
→ [023 → 024 → 025 → 026 if impact exhausted]
→ 027
→ 028 PASS
→ 029
→ 030
→ 031
→ 032
→ 033
→ 034
→ 035
→ 036
→ 037
→ 038 FIRST REAL CASH
```

No durations are invented.

## (2) Safe prep before Owner

Already complete:

- Gate A contract;
- Cash Truth V1 ontology/schema;
- experiment design;
- owner privacy/redaction rules;
- this dependency-correct backlog.

Permitted additional safe prep is limited to validating repository artifacts and deterministic IDs/templates. It must not drift into content production.

## (3) Blocked on Owner

Blocked now:

- MCME-010 Pinterest property;
- all real network relationships/applications;
- legal acceptance;
- merchant applications;
- MFA/CAPTCHA/identity;
- KYC/tax/payment setup.

## (4) Unblocked only after Gate A PASS

- MCME-029 actual merchant-specific 3-Pin spec;
- MCME-030 production;
- MCME-031 QA/publish readiness;
- MCME-032 publish;
- observation and commercial testing.

## (5) Unblocked after evidence levels

### After L1

Allowed:
- keep/revise learning decision;
- diagnose click behavior.

Not allowed:
- scale based on views/clicks;
- 24/7 production factory.

### After L2

Allowed:
- first SCALE-eligibility discussion;
- continue validation/payable observation;
- design minimal conversion-aware improvements if Brain approves.

### After L3

Allowed:
- stronger economics review;
- continue payout reconciliation.

Still not real cash unless funds received.

### After L4

Allowed:
- first real cash claim;
- measured net economics;
- Brain may consider automation/scale architecture.

24/7 automation is still not automatic; it requires a separate Brain-authorized task.

---

# 9. Deferred / deleted from first-cash critical path

Explicitly DEFER until evidence justifies:

- SaydiVoice;
- Video Composer;
- video Pins;
- multi-platform distribution;
- multilingual/localization;
- dashboard polish;
- 24/7 autonomous content factory;
- paid traffic;
- generic AI agents;
- large content batches;
- brand-building work unrelated to first cash;
- broad merchant/network expansion;
- sponsorship;
- platform-native monetization;
- lead-generation restart;
- SEO website/bridge page unless real merchant rules require it;
- sophisticated forecasting;
- invented RPM/CPM/EPC models.

These items do not shorten the current path from Gate A to FIRST REAL CASH.

---

# 10. Cash Truth V1 as mandatory future evidence sink

Every real event after publish must normalize into:

`06_METRICS/mcme_cash_truth_v1.schema.json`

Minimum truth sequence:

```text
PIN_PUBLISHED
→ impressions/click observations
→ OUTBOUND_CLICK_OBSERVED
→ NETWORK_CLICK_OBSERVED if available
→ MERCHANT_ACTION_TRACKED
→ COMMISSION_PENDING
→ COMMISSION_VALIDATED / REVERSED
→ COMMISSION_PAYABLE
→ PAYOUT_ISSUED
→ CASH_SETTLED
```

Rules:

- append-only;
- deterministic provider IDs when available;
- conservative reconciliation when absent;
- no missing-state inference;
- network "paid" != CASH_SETTLED;
- no double-counting from repeated polling;
- costs and time recorded separately;
- corrections/reversals are new events.

---

# 11. STOP / KILL matrix

### Gate A STOP

- Owner action pending → WAIT_OWNER.
- auth/MFA/CAPTCHA required → Owner only.
- critical evidence UNKNOWN/BLOCKED → no PASS.
- bounded network fallback exhausted → FAIL.

### Gate A KILL

Terminal Gate A FAIL:

```text
KILL fridge storage/fit niche
NO Pin production
NO automatic niche switch
RETURN TO BRAIN
```

### Production STOP

- no Gate A PASS;
- missing disclosure;
- unclear rights;
- broken destination/tracking;
- sensitive data detected.

### Publishing STOP

- missing explicit external-side-effect authorization;
- uncertain previous publish result;
- auth/MFA/CAPTCHA;
- publish latch conflict;
- duplicate content_id already reconciled to a Pin.

### Observation STOP

Do not manufacture traffic. Missing data remains UNKNOWN/BLOCKED.

### Economics STOP

- click != sale;
- pending != validated;
- payout-issued != cash;
- no settled-funds evidence → no L4 / no FIRST REAL CASH.

---

# 12. Definition of Done — MCME-007

MCME-007 is complete only if:

- one dependency-correct path exists from current L0 to FIRST REAL CASH;
- durable future task IDs begin at MCME-010;
- Gate A fallback is bounded Awin → impact.com → Amazon conditional;
- Owner interruptions are minimized through one sanitized packet design;
- every future task has objective, stage, dependency, executor, boundary, inputs, output, DoD, stop/fail, reversibility, side-effect, idempotency/reconciliation and next gate;
- content production is blocked until Gate A PASS;
- publishing is a separate external-side-effect task with pre-action latch and reconciliation;
- observation window is locked before publish;
- Cash Truth V1 is the canonical evidence sink;
- SCALE requires at least tracked merchant action + attributed commission;
- FIRST REAL CASH requires funds actually received and reconciled;
- SaydiVoice/video/multi-platform/multilingual/paid traffic/24-7 automation/large batches remain deferred;
- no account action, content production, publishing or spend is executed in MCME-007.

---

# 13. MCME-007 handoff

**Status:** COMPLETE — backlog only; no external actions executed.

**First future task after current run:**

```text
MCME-010 — Owner Pinterest property confirmation
```

**Current blocker:**

```text
Actual Gate A has not been executed.
Current evidence level remains L0.
```

**FIRST REAL CASH endpoint:**

```text
MCME-038 PASS
=
payout attributable to experiment
+ funds actually received on Owner-authorized payout rail
+ reconciliation to payable/payout record
+ measured direct cost/time
```

**Hard stop:** Do not start MCME-008 automatically.
