# MCME 8-HOUR SINGLE-LANE EXECUTION PLAN V2

Prepared: 2026-09-19
Status: WAIT_OWNER_APPROVAL
Run ID: MCME-RUN-8H-01
Mode: SINGLE_LANE_SEQUENTIAL
Duration: 8 hours wall-clock from explicit Owner approval

## Objective

Use ONE Brain ↔ ONE Work lane only.

The 8-hour run exists for one purpose:

> Move the project as close as possible to the first real cash transaction, using evidence instead of speculation.

This is not a broad research sprint and not a generic Robot-building sprint.

The run must finish with ONE selected money loop and the minimum implementation/experiment package needed to test it for real money.

## Operating roles

### Owner
Approves START once.
No routine decision is required during the 8-hour run.

### Brain
Brain does NOT perform Work tasks.

Brain only:
1. applies Five-Step;
2. sends ONE bounded task to the single Work chat;
3. waits for Work result;
4. verifies evidence and Definition of Done;
5. accepts, repairs, deletes or simplifies;
6. updates run state;
7. sends the NEXT task only after the previous task is accepted.

### Work
Executes exactly ONE active task at a time.

### Robot
Transports Brain → Work → Brain, preserves state, performs bounded recovery and exact-once delivery where supported.

## Single-lane invariant

At any moment:

```text
Brain
  ↓ exactly one directive
Work
  ↓ one completed result
Brain review
  ↓
next directive
```

There is NEVER:
- 3-lane parallel execution;
- concurrent strategic tasks;
- multiple active Work tasks;
- Work choosing its own next task.

## Highest-priority law

For EVERY task:

QUESTION → DELETE → SIMPLIFY → ACCELERATE → AUTOMATE

AUTOMATE is not allowed before the money loop and experiment economics are explicit.

## Cash-first decision rule

Brain prioritizes the next task by:

```text
Expected contribution to first real cash
× confidence / learning value
× speed
──────────────────────────────────────
cost + complexity + policy risk + Owner dependency
```

Raw views, follower growth and content volume are secondary.

## Run boundaries

Allowed without Owner:
- public research;
- comparing countries/platforms/niches;
- deleting weak options;
- choosing one provisional market/money loop;
- writing reversible repo docs/specs/tests;
- defining experiments;
- defining affiliate/content funnel;
- defining SaydiVoice/video requirements.

Not allowed:
- credentials;
- MFA/CAPTCHA;
- KYC/tax/banking;
- legal/license ambiguity;
- production publishing;
- paid advertising;
- real external spend;
- destructive account/repository action.

If a task hits a boundary, Brain records it and immediately asks Work for the next safe critical-path task. Only stop if no safe work remains.

---

# 8-HOUR REAL-TIME SEQUENCE

T0 = exact Owner approval/start timestamp.
Hard stop = T0 + 8 hours.

## STEP 1 — T+00:00 → T+01:15
### MCME-001 — FIND THE SHORTEST CREDIBLE PATH TO FIRST CASH
Five-Step: QUESTION

Brain dispatches ONE task to Work:

Research current global monetization routes and determine which path is most capable of producing the FIRST REAL CASH with the least Owner dependency.

Work must compare only:
1. Affiliate commerce
2. Platform monetization
3. Lead generation

Work must evaluate:
- country availability;
- platform/network eligibility;
- time-to-first-cash;
- whether a new creator can start immediately;
- audience purchase intent;
- payout/settlement friction;
- content originality requirements;
- account/Owner dependencies;
- ability to measure actual cash.

Required output:
- evidence table;
- VERIFIED vs ASSUMPTION vs UNKNOWN;
- top 3 candidate combinations;
- explicit reasons to DELETE weaker paths.

Brain acceptance gate:
No invented RPM/CPM.
Current claims must have reliable sources.
Result must answer: "Which route can reach cash fastest?"

Checkpoint: C1_PATHS_EVIDENCED

---

## STEP 2 — T+01:15 → T+02:15
### MCME-002 — DELETE TO ONE MONEY MODEL
Five-Step: DELETE

After Brain accepts MCME-001, Brain sends one new task:

Take the accepted evidence and aggressively eliminate options until only ONE primary monetization model remains for the first experiment.

Work must produce:
- selected monetization model;
- selected candidate market/language;
- selected platform/distribution surface;
- why alternatives were deleted;
- Owner actions eventually required;
- evidence still missing.

Selection rule:
Choose the option with the shortest credible path to real settled cash, not the option with the biggest theoretical audience.

Expected likely candidates may include affiliate-led content because it can generate commerce revenue before native creator monetization thresholds, but Work must prove this rather than assume it.

Checkpoint: C2_ONE_MONEY_MODEL

---

## STEP 3 — T+02:15 → T+03:20
### MCME-003 — SELECT ONE NICHE + ONE CONTENT FORMAT
Five-Step: SIMPLIFY

Brain sends one task only after MCME-002 is accepted.

Work finds ONE niche and ONE content format aligned with the chosen money model.

Required evaluation:
- buyer pain/problem;
- product or offer availability;
- search/social demand;
- content supply/competition;
- visual sourcing feasibility;
- originality/rights burden;
- SaydiVoice suitability;
- localization cost;
- repeatability;
- expected CTA clarity.

Work must return:
- 3–5 candidates;
- delete all but ONE;
- selected niche;
- selected audience;
- selected format;
- sample content concept set;
- why this can produce money, not just views.

Prohibited default:
download → minor edit → repost.

Checkpoint: C3_ONE_NICHE_FORMAT

---

## STEP 4 — T+03:20 → T+04:30
### MCME-004 — DESIGN THE FIRST REAL-MONEY EXPERIMENT
Five-Step: SIMPLIFY → ACCELERATE

Brain sends Work a task to define the smallest experiment capable of producing or falsifying real revenue.

Work must define:

```text
Market
× Platform
× Niche
× Format
× Monetization
× CTA
```

Required:
- content count: smallest justified batch, not automatically 30;
- 3–5 hypotheses;
- CTA;
- destination/affiliate/lead path;
- qualified view definition;
- click definition;
- conversion definition;
- approved revenue;
- settled cash;
- production cost ceiling;
- KEEP criteria;
- KILL criteria;
- SCALE criteria;
- what evidence means "we are wrong."

Checkpoint: C4_REAL_MONEY_EXPERIMENT

---

## STEP 5 — T+04:30 → T+05:30
### MCME-005 — BUILD THE MINIMUM CONTENT FACTORY CONTRACT
Five-Step: DELETE → SIMPLIFY

Work must define only what the selected experiment needs.

Pipeline:

```text
Opportunity
→ Script
→ SaydiVoice
→ Visual assets
→ Video assembly
→ Subtitle/caption
→ QA
→ Publish package
```

Work must specify:
- script schema;
- language;
- voice style;
- SaydiVoice functions actually required;
- visual source classes;
- video duration/aspect ratio;
- hook structure;
- CTA placement;
- subtitle requirements;
- rights evidence;
- output file/package.

Delete:
- generic features;
- multi-platform abstractions not required now;
- fancy editor features;
- AI features with no effect on first-cash experiment.

Checkpoint: C5_FACTORY_MINIMUM

---

## STEP 6 — T+05:30 → T+06:30
### MCME-006 — MONEY ATTRIBUTION + ECONOMICS
Five-Step: QUESTION → SIMPLIFY

Work defines the minimum truth model required to know whether money was actually made.

Required fields:
- content_id;
- market;
- platform;
- niche;
- monetization method;
- qualified views;
- clicks;
- conversions;
- pending revenue;
- approved revenue;
- settled cash;
- refunds/reversals;
- variable production cost;
- net cash contribution;
- NCC per 1,000 qualified views.

Work must define how each number will be sourced and which values are UNKNOWN until real platform/account data exists.

No synthetic revenue.
No assumed cash settlement.

Checkpoint: C6_CASH_TRUTH_MODEL

---

## STEP 7 — T+06:30 → T+07:20
### MCME-007 — IMPLEMENTATION BACKLOG TO FIRST CASH
Five-Step: ACCELERATE

Work converts the accepted experiment into an ordered execution backlog.

Priority must be:
1. blockers to first publish;
2. blockers to first click/conversion;
3. blockers to revenue attribution;
4. only then automation.

Required backlog:
- exact next SaydiVoice task;
- exact minimum Video Composer task;
- exact distribution/publish task;
- exact tracking task;
- Owner setup checklist;
- estimated dependency order;
- which tasks Robot can perform autonomously;
- which task must wait for Owner.

No 24/7 automation task may precede real experiment readiness.

Checkpoint: C7_FIRST_CASH_BACKLOG

---

## STEP 8 — T+07:20 → T+08:00
### MCME-008 — BRAIN FINAL REVIEW / RUN REPORT
Five-Step: full cycle

Brain does NOT ask Work for a broad new research task.

Brain reviews all accepted Work results and writes canonical state.

Required final decision package:

1. ONE selected country/market.
2. ONE language.
3. ONE primary platform.
4. ONE niche.
5. ONE content format.
6. ONE primary monetization method.
7. Exact path from content → transaction → settled cash.
8. First experiment.
9. KEEP/KILL/SCALE thresholds.
10. SaydiVoice minimum scope.
11. Video minimum scope.
12. Cash attribution schema.
13. Rights/policy constraints.
14. Ordered next implementation tasks.
15. Owner actions required before real launch.
16. Deleted alternatives and why.
17. Remaining UNKNOWNs.

## CONDITIONAL EARLY-FINISH EXTENSION — USE REMAINING WALL-CLOCK TIME

If C7_FIRST_CASH_BACKLOG and the MCME-008 final decision package are accepted **before T0+8h**, Brain MUST NOT idle.

Brain uses the remaining authorized wall-clock time to prepare deployment readiness, still in the same single lane.

### MCME-009 — IMPLEMENTATION / DEPLOYMENT PLAN TO FIRST CASH
Five-Step: ACCELERATE → AUTOMATE (planning only)

Brain dispatches ONE bounded task to Work only after MCME-008 is accepted.

Work prepares an implementation-ready deployment plan for the selected money loop.

Required output:
- exact repository/module ownership for each component;
- ordered code/document/config changes;
- SaydiVoice integration sequence;
- minimum Video Composer implementation sequence;
- distribution/publishing integration sequence;
- tracking/attribution implementation sequence;
- local/CI test gates;
- staging/dry-run gate;
- production launch gate;
- rollback/recovery strategy;
- idempotency requirements for external side effects;
- credentials/KYC/payment/Owner setup checklist;
- exact tasks Robot can perform autonomously;
- exact tasks requiring Owner;
- first-launch checklist;
- post-launch measurement schedule;
- STOP conditions;
- ordered implementation task IDs ready for future Brain dispatch.

Constraints:
- planning only;
- no production publish;
- no credentials/KYC/payment actions;
- no external spend;
- no destructive change;
- do not build speculative infrastructure not required by the selected first-cash loop.

Checkpoint: C8_DEPLOYMENT_PLAN_READY

### Remaining-time rule

If MCME-009 finishes with time still remaining:
- Brain reviews it against Five-Step;
- Work may receive ONE bounded FIX task if required;
- Brain may refine the ordered task queue and launch gates;
- Brain does NOT start speculative features merely to consume time.

The run always stops at the original hard deadline T0+8h.

At T0+8h:
status → COMPLETE_8H
No automatic overtime.

---

# BRAIN REVIEW CONTRACT

After every Work result, Brain must answer internally:

### QUESTION
Did Work answer the exact business question?

### DELETE
What in the result can be removed?

### SIMPLIFY
Can the next experiment/task be smaller?

### ACCELERATE
What is the next action that most reduces time-to-first-cash?

### AUTOMATE
Is this already proven enough to automate?
Default answer during this run: NO, unless evidence says otherwise.

A Work result saying DONE is not sufficient.

Brain accepts only if:
- DoD met;
- evidence is current enough;
- assumptions identified;
- no unsupported economic claim;
- no rights/policy shortcut;
- no scope creep.

If rejected:
Brain sends ONE bounded FIX task.
It does not start a second unrelated task.

---

# TRACKING STATE

Canonical files:

- `08_AUTONOMY/MCME_8_HOUR_EXECUTION_PLAN_V1.md`
- `08_AUTONOMY/MCME_RUN_8H_01_STATE.json`
- `08_AUTONOMY/MCME_RUN_8H_01_LOG.md`
- `08_AUTONOMY/MCME_RUN_8H_01_FINAL_REPORT.md`
- `00_PROJECT/PROJECT_STATE.json`
- `00_PROJECT/TASK_QUEUE.md`

Checkpoint sequence:

```text
WAIT_OWNER_APPROVAL
→ RUNNING
→ C1_PATHS_EVIDENCED
→ C2_ONE_MONEY_MODEL
→ C3_ONE_NICHE_FORMAT
→ C4_REAL_MONEY_EXPERIMENT
→ C5_FACTORY_MINIMUM
→ C6_CASH_TRUTH_MODEL
→ C7_FIRST_CASH_BACKLOG
→ [if early] C8_DEPLOYMENT_PLAN_READY
→ COMPLETE_8H
```

There is only ONE active Work task.

## Success definition for this run

Success does NOT mean:
- most documents;
- most research;
- most video features;
- most automation.

Success means:

> We know exactly what first real-money experiment to execute, why it was selected, how money will be measured, and what minimum product/Robot work must happen next.

If the core sequence finishes early, success is extended to:

> An implementation/deployment plan is ready down to ordered task IDs, test gates, Owner boundaries, launch gates, rollback conditions and the exact path to first real cash.

## Approval trigger

This plan remains inert until Owner explicitly approves MCME-RUN-8H-01.

After approval:
1. record exact T0;
2. calculate T0 + 8h;
3. change state to RUNNING;
4. dispatch MCME-001 only;
5. never dispatch MCME-002 before MCME-001 is reviewed and accepted;
6. if the core sequence completes early, use remaining wall-clock time for MCME-009 deployment planning rather than stopping early.
