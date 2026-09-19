# MCME-RUN-4H-02 — SAFE-PREP EXECUTION PLAN

Status: RUNNING
Mode: SINGLE_LANE_SEQUENTIAL
T0: 2026-09-20T03:21:04+07:00
Hard deadline: 2026-09-20T07:21:04+07:00
Duration: 4 hours wall-clock

## Purpose

Use the next four real hours to remove implementation friction **without crossing the Owner-gated Gate A boundary**.

The real first-cash critical path remains MCME-010→MCME-038.

This run does NOT replace or skip MCME-010.

## Highest-priority law

QUESTION → DELETE → SIMPLIFY → ACCELERATE → AUTOMATE

Every prep task must answer:
- Does this remove a real future blocker?
- Can it be smaller?
- Can it be proven locally/offline?
- Does it avoid external mutation?
- Does it preserve fail-closed boundaries?

## Single-lane invariant

Exactly one Work task may be active.

Brain:
- dispatches one task;
- reviews evidence/tests/commit;
- ACCEPT / FIX / DELETE / SIMPLIFY;
- only then dispatches the next task.

Work:
- performs the bounded task only;
- commits to main;
- stops for Brain review.

Robot:
- transports Brain↔Work;
- no autonomous Owner action.

## Owner / safety boundaries

Not authorized:
- Pinterest/Awin/Impact/Amazon account login or creation;
- merchant/network application;
- MFA/CAPTCHA;
- KYC/tax/banking/payment;
- production Pin creation;
- production publish;
- external spend;
- artificial clicks/test purchase/self-purchase;
- real affiliate link mutation;
- SaydiVoice/video reintroduction;
- changing the locked route/niche/format/batch.

## Current truth

- Evidence: L0_NO_REAL_COMMERCIAL_EVIDENCE
- Gate A: OWNER_GATED_NOT_EXECUTED
- Next real execution task: MCME-010 Owner Pinterest property confirmation
- Database required for MVP: NO
- MVP data architecture: local/private append-only JSONL + schemas + validators + deterministic reconciliation

---

# Sequential SAFE-PREP tasks

## MCME-039 — Materialize Gate A runtime contract
Five-Step: SIMPLIFY → ACCELERATE

Goal:
Convert MCME-005/009 prose contract into the smallest machine-validatable Gate A runtime package.

Required minimum:
- Gate A evidence JSON Schema;
- candidate-slot model AWIN-01/AWIN-02/IMPACT-01/IMPACT-02/AMAZON-01;
- fail-closed validator/evaluator;
- deterministic state transition logic;
- fixtures for PASS/UNKNOWN/BLOCKED/FAIL;
- tests proving UNKNOWN/BLOCKED never promote to PASS;
- sanitized evidence only.

No network/account calls.

Gate unlocked:
MCME-012 future Work can evaluate real Owner evidence without inventing schema at runtime.

## MCME-040 — Cash Truth local MVP runtime
Five-Step: SIMPLIFY → ACCELERATE

Dependency: MCME-039 ACCEPTED.

Goal:
Implement the minimum local/private Cash Truth runtime required before first publish.

Required minimum:
- validator for existing `mcme_cash_truth_v1.schema.json`;
- append-only JSONL writer/reader;
- deterministic dedupe/idempotency;
- conservative reconciliation for no-stable-ID cases;
- reversal/negative-adjustment handling;
- structural fictitious fixtures only;
- tests proving duplicate polling cannot double-count money;
- tests proving PAYOUT_ISSUED cannot become CASH_SETTLED without all settled-cash guards.

No DB/service unless tests prove local JSONL insufficient.

## MCME-041 — Pinterest publish safety harness
Five-Step: QUESTION → SIMPLIFY → ACCELERATE

Dependency: MCME-040 ACCEPTED.

Goal:
Implement/test the **side-effect safety state machine only**, not real Pinterest publishing.

Required minimum:
- deterministic publish key;
- PREPARED → SEND_STARTED → CONFIRMED;
- BLOCKED_AUTH / BLOCKED_AMBIGUOUS / FAILED_CONFIRMED;
- pre-action persisted latch abstraction;
- mock/dry-run backend only;
- reconciliation before retry;
- no blind resend;
- tests for timeout/ambiguous response/restart/repeated invocation;
- exactly-once intended publish semantics in fixtures.

No Pinterest login/browser/API mutation.

## MCME-042 — Launch-readiness + privacy gate
Five-Step: DELETE → SIMPLIFY

Dependency: MCME-041 ACCEPTED.

Goal:
Build the smallest deterministic pre-publish gate that can later answer READY / NOT_READY without manual ambiguity.

Must validate future requirements:
- Gate A PASS;
- merchant/link/commission/validation/payout evidence verified;
- rights/disclosure verified;
- exactly 3 deterministic content packages;
- QA PASS;
- observation window locked;
- publish latch/idempotency ready;
- Cash Truth sink ready;
- zero critical UNKNOWN;
- public/private leakage scan.

Use fixtures only; no real Pins or real private evidence.

## MCME-043 — SAFE-PREP integration/reconciliation
Five-Step: QUESTION → DELETE → ACCELERATE

Dependency: MCME-042 ACCEPTED.
Run only if time remains.

Goal:
Run the prep components together against fixtures and produce an exact delta for future MCME-010→038.

Required:
- Gate A fixture → evaluator;
- Gate B handoff fixture;
- launch-ready fixture;
- mock publish lifecycle;
- observation fixture;
- Cash Truth ingestion;
- reversal fixture;
- settled-cash guard fixture;
- privacy scan;
- identify any hidden dependency.

Artifact must say whether future MCME-012, MCME-031, MCME-032 and MCME-034 are implementation-ready or still need bounded changes.

No external actions.

---

# Timing policy

The task durations are NOT artificial quotas.

Brain dispatches the next task immediately after the prior task is ACCEPTED.

Hard stop at 2026-09-20T07:21:04+07:00.

If MCME-039→043 all finish before the deadline and no additional genuine SAFE_PREP blocker remains:
- stop early;
- do not invent work;
- status = EARLY_COMPLETE_WAIT_OWNER;
- next real task remains MCME-010.

If deadline arrives during a task:
- no new task is dispatched;
- current Work may return its current bounded result/state;
- Brain records the run as TIMEBOX_COMPLETE.

## Definition of success

Success is not number of commits.

Success means that before Owner begins MCME-010:
- Gate A real evidence has a machine-validatable fail-closed contract;
- Cash Truth sink can safely accept future evidence;
- publish side-effect safety has been proven locally;
- launch gate can fail closed;
- future implementation has less ambiguity;
- no external mutation or fake economics occurred.
