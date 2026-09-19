# MCME 8-HOUR AUTONOMOUS EXECUTION PLAN V1

Prepared: 2026-09-19 23:04 +07
Status: WAIT_OWNER_APPROVAL
Run ID: MCME-RUN-8H-01
Duration: 8 hours wall-clock from explicit Owner approval/start signal

## Purpose

Move MAGASIN CONTENT MONEY ENGINE from architecture lock to a fully evidence-backed first Minimum Viable Money Loop and an implementation-ready experiment package, without requiring Owner decisions during the run.

This run MUST NOT create accounts, enter credentials, accept KYC/tax/payment terms, spend money, publish production content, or cross legal/rights ambiguity.

## Control model

Owner:
- authorizes START once;
- is not required during the 8-hour run.

Brain:
- does NOT execute research/code/content tasks;
- dispatches bounded tasks;
- reviews Work evidence;
- rejects incomplete/weak outputs;
- applies Five-Step before each next dispatch;
- chooses between pre-authorized options using the decision policy below;
- updates canonical run state/checkpoints.

Work:
- executes bounded task;
- returns evidence, citations, artifacts, tests, risks and next facts.

Robot:
- transports Brain → Work → Brain;
- runs lanes independently;
- retries transient failures only;
- preserves state;
- never invents business decisions.

## Highest-priority law

Every task and every Brain review must explicitly apply:

QUESTION → DELETE → SIMPLIFY → ACCELERATE → AUTOMATE

AUTOMATE is prohibited until the relevant upstream economics/requirements are evidenced.

## Delegated decision authority for this run

Brain MAY decide without Owner:
- which countries to research deeper;
- which platform/monetization combinations to delete;
- which ONE first Minimum Viable Money Loop to recommend/select for the next experiment;
- which niche/content format to carry forward;
- research priorities;
- repo documentation/schema/test changes that are reversible and non-destructive;
- how to split work across lanes.

Brain MUST NOT decide/execute:
- account creation requiring legal acceptance/KYC;
- credentials/MFA/CAPTCHA;
- tax/banking/payment setup;
- platform appeals/suspensions;
- copyright/license ambiguity;
- production publishing;
- real ad/media spend;
- destructive repository/account actions;
- spend above zero unless separately authorized.

If a task hits one of those boundaries, mark that subtask WAIT_OWNER and continue other safe tasks. Do not stop the whole run unless no safe critical-path work remains.

## Parallel lane topology

### Lane 1 — PLATFORM MONEY
Focus:
- YouTube;
- TikTok;
- Facebook/Instagram/Meta;
- other platform-native monetization only if evidence justifies inclusion.

### Lane 2 — AFFILIATE / COMMERCE MONEY
Focus:
- Amazon Associates and major global affiliate networks/merchant ecosystems;
- market accessibility;
- payout/commission/EPC evidence where authoritative;
- conversion path and time-to-first-cash.

### Lane 3 — CONTENT / MARKET FIT
Focus:
- global niche discovery;
- content formats;
- demand signals;
- originality/rights burden;
- localization cost;
- source strategy;
- competition and production feasibility.

Lane isolation is mandatory. Brain merges results; lanes do not independently alter strategy.

---

# REAL-TIME SCHEDULE

T0 is the exact timestamp when Owner explicitly approves and Brain changes run state from WAIT_OWNER_APPROVAL to RUNNING.

Hard stop: T0 + 8:00:00.

## T+00:00 → T+00:20 — BOOTSTRAP / QUESTION

Brain:
- re-reads START_HERE, Five-Step law, architecture, PROJECT_STATE and this runbook;
- records exact start/deadline;
- verifies no Owner boundary is already active;
- dispatches MCME-001A/B/C in parallel.

No Work task may begin before run state is RUNNING.

### MCME-001A — Platform Monetization Evidence
Lane 1.
DoD:
- official eligibility/program availability by candidate market;
- originality/reused-content constraints;
- payout/threshold facts when official;
- facts separated from third-party estimates;
- timestamp/source for every material current claim.

### MCME-001B — Affiliate/Commerce Evidence
Lane 2.
DoD:
- major affiliate networks/programs accessible across candidate markets;
- merchant/product depth;
- commission/EPC evidence only when authoritative or clearly marked estimate;
- payout/settlement constraints;
- fastest plausible affiliate path.

### MCME-001C — Global Content Opportunity Evidence
Lane 3.
DoD:
- candidate niches/formats that can be produced originally or with verified rights;
- demand/competition proxies;
- localization complexity;
- product/monetization adjacency;
- reject pure reupload as a default strategy.

Checkpoint C1 at T+00:20:
3 valid dispatches, no duplicate task IDs.

## T+00:20 → T+02:20 — PARALLEL RESEARCH / QUESTION

Work executes 001A/B/C.

Brain behavior:
- poll/review only;
- do not micromanage active Work;
- if one lane finishes early, review and either ACCEPT or return one bounded FIX task;
- do not create new strategic scope yet.

Checkpoint C2 at T+02:20:
Expected artifacts:
- platform matrix;
- affiliate matrix;
- content opportunity matrix.

Acceptance:
- evidence-backed;
- current-date aware;
- no invented RPM;
- no uncited material eligibility claim;
- no policy-unsafe recommendation.

If one lane is incomplete:
- Brain may grant one repair pass ≤30 minutes while other lanes continue.

## T+02:20 → T+03:00 — DELETE

Brain reviews all three matrices and produces an evidence ledger:
- VERIFIED;
- ASSUMPTION;
- UNKNOWN;
- REJECTED.

Brain deletes:
- markets with weak monetization coverage and no compensating advantage;
- monetization paths with long/blocked time-to-first-cash;
- niches requiring unclear third-party rights;
- formats likely to violate originality/reused-content policies;
- research dimensions that do not affect the first cash experiment.

Brain then dispatches MCME-002A/B/C.

### MCME-002A — Market Score V1
Lane 1.
Build a transparent scoring model using current evidence.
No false precision.

### MCME-002B — Money Loop Economics V1
Lane 2.
Compare:
- Affiliate;
- Platform monetization;
- Lead generation.
Estimate time-to-first-cash, measurement path, owner dependencies, cash attribution.

### MCME-002C — Production Feasibility V1
Lane 3.
For top candidate markets/niches:
- script/localization;
- SaydiVoice suitability;
- visual sourcing;
- video complexity;
- rights/policy risk;
- estimated unit production burden.

Checkpoint C3: Five-Step DELETE log committed.

## T+03:00 → T+04:30 — SIMPLIFY

Workers complete 002A/B/C.

Brain must select ONE provisional Minimum Viable Money Loop using:

Expected Net Cash Potential
× Evidence Confidence
× Speed to Cash
× Automation Fit
÷ Cost + Policy Risk + Owner Dependency

The selection is not a permanent global strategy; it is the cheapest credible first experiment.

Brain records:
- selected market;
- language;
- primary platform;
- niche;
- format;
- primary monetization;
- secondary monetization if zero extra complexity;
- why alternatives were deleted.

Checkpoint C4 at T+04:30:
ONE loop only.
If evidence is tied, choose the cheaper/faster falsification path, not a larger research project.

## T+04:30 → T+05:50 — ACCELERATE: EXPERIMENT PACKAGE

Brain dispatches in parallel:

### MCME-003A — Experiment Design
Lane 1.
Define:
- target audience;
- 3–5 content hypotheses;
- batch size using cheapest falsification logic;
- success/kill criteria;
- CTA;
- monetization attribution path.

### MCME-003B — Content Factory Minimum Spec
Lane 2.
Define only what first loop needs:
- research input;
- script schema;
- voice requirements;
- SaydiVoice boundary;
- video template requirements;
- subtitles/captions;
- output package.

No generic media platform design.

### MCME-003C — Measurement + Rights Spec
Lane 3.
Define:
- qualified view;
- click;
- conversion;
- approved revenue;
- settled cash;
- cost attribution;
- rights evidence record;
- policy QA checklist.

Checkpoint C5:
Experiment can be explained end-to-end as:
Opportunity → Content → Publish → Click/Revenue → Cash evidence.

## T+05:50 → T+06:40 — BRAIN REVIEW / REPAIR

Brain checks all 003 outputs against Five-Step.

Mandatory questions:
- What can be deleted?
- What is still assumption?
- Can first cash test be smaller?
- Does any requirement secretly require Owner?
- Is every external side effect reversible/idempotent?
- Can SaydiVoice remain a provider rather than a business subsystem?

Brain may issue one repair task per lane.
No new module unless required for the selected experiment.

Checkpoint C6:
First experiment package ACCEPTED.

## T+06:40 → T+07:30 — IMPLEMENTATION-READY BACKLOG

Brain dispatches bounded documentation/engineering planning tasks only; no production publishing.

Outputs:
1. SaydiVoice gap list for selected experiment.
2. Minimum Video Composer acceptance contract.
3. Distribution adapter contract for selected platform.
4. Money Attribution schema.
5. 24/7 state machine deltas needed after validation.
6. ordered next-task queue by cash impact.

If a small reversible code/test change is necessary to prove feasibility, Work may implement it only if:
- no credentials;
- no external production mutation;
- no spend;
- no destructive migration;
- unit/offline tests exist.

Checkpoint C7:
Next implementation sequence is ready without architectural ambiguity.

## T+07:30 → T+08:00 — FINAL RECONCILIATION / HARD STOP

Brain:
- reviews all accepted artifacts;
- reconciles contradictions;
- updates PROJECT_STATE, CURRENT_STATE and TASK_QUEUE;
- writes final run report;
- records unresolved UNKNOWNs;
- records Owner boundaries separately;
- creates the next bounded task, but DOES NOT continue beyond 8-hour deadline.

Final report must contain:
- Five-Step decisions;
- evidence gathered;
- deleted markets/paths and why;
- selected first Money Loop;
- first experiment definition;
- expected money path;
- SaydiVoice requirements;
- Video requirements;
- measurement schema;
- risks;
- next 3–5 tasks;
- exact start/end timestamps;
- tasks accepted/rejected/repaired;
- whether next run can proceed without Owner.

At T0+8h:
RUNNING → COMPLETE_8H
No automatic overtime.

---

# TRACKING CONTRACT

Canonical files during run:
- `00_PROJECT/PROJECT_STATE.json`
- `00_PROJECT/TASK_QUEUE.md`
- `08_AUTONOMY/MCME_RUN_8H_01_STATE.json`
- `08_AUTONOMY/MCME_RUN_8H_01_LOG.md`
- `08_AUTONOMY/MCME_RUN_8H_01_FINAL_REPORT.md`

Brain updates run state after every accepted/rejected Work result.

## Checkpoint states

WAIT_OWNER_APPROVAL
RUNNING
C1_DISPATCHED
C2_RESEARCH_ACCEPTED
C3_DELETE_COMPLETE
C4_MONEY_LOOP_SELECTED
C5_EXPERIMENT_DRAFTED
C6_EXPERIMENT_ACCEPTED
C7_BACKLOG_READY
COMPLETE_8H
WAIT_OWNER
FAILED_TERMINAL

## Review rule

A Work result is not complete merely because Work says DONE.

Brain must verify:
- DoD;
- source quality;
- consistency with architecture;
- Five-Step;
- no scope creep;
- no unsupported factual claims;
- no Owner boundary crossed.

Only Brain may mark a checkpoint ACCEPTED.

## Failure policy

Transient technical failure:
- Robot bounded retry/recovery.

Weak/incomplete Work:
- Brain returns one bounded FIX task.

Repeated weak result:
- Brain deletes/simplifies the task and continues with available evidence.

Owner boundary:
- mark affected branch WAIT_OWNER;
- continue independent safe critical-path work.

No remaining safe work:
- stop run early with a report; never fabricate progress.

## Budget

Default external spend authorization for this run: ZERO.

Research and repository work only.

## Approval trigger

The plan remains inert until Owner explicitly approves starting MCME-RUN-8H-01.

After approval, Brain must:
1. capture exact T0;
2. set deadline T0 + 8h;
3. change run state to RUNNING;
4. dispatch only the first three bounded tasks.
