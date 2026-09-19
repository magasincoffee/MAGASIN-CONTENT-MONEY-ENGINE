# MCME-006 — CASH TRUTH + EVENT LEDGER V1

**Task:** MCME-006  
**Canonical input:** MCME-005 accepted by Brain at commit b731207531d4b235e04956cd8b592d333f9435b4  
**Five-Step:** SIMPLIFY → ACCELERATE  
**Scope:** cash-truth/event-ledger specification only. Actual Gate A remains OWNER_GATED_NOT_EXECUTED.

## 1. Non-negotiable cash truth

Canonical money path:

Pinterest Pin → outbound click → network/merchant action → pending commission → validated/approved commission → payable commission → payout issued → funds received / settled cash

Invariant:

**click != sale != pending commission != validated revenue != payable != payout issued != settled cash**

### FIRST REAL CASH — locked definition

**FIRST REAL CASH** exists only when all of the following are true:

1. the payout is attributable to the experiment through reconciled commission/payout evidence;
2. funds are actually received on an Owner-authorized payout rail;
3. the received funds can be reconciled to the payable commission / payout record;
4. the settlement evidence is VERIFIED.

A network status such as "paid", "sent", "completed" or equivalent is **not enough by itself**. That status proves, at most, PAYOUT_ISSUED until the Owner-authorized payout rail shows funds actually received.

Anything before CASH_SETTLED is not real cash.

---

## 2. Source-of-truth hierarchy

Use the narrowest authoritative source for each fact. A lower layer must never overwrite a stronger layer silently.

| Truth domain | Primary source of truth | Secondary evidence | Forbidden inference |
|---|---|---|---|
| Pin publication | Pinterest publication record / authorized account record | sanitized internal publication record | existence of a draft does not mean published |
| Pinterest impressions / Pin clicks / outbound clicks | Pinterest Analytics/API/export for the exact Pin and observation window | sanitized UI capture | network click count cannot be substituted for Pinterest impressions |
| Affiliate network clicks | affiliate network click/reporting record | merchant/network diagnostic report | Pinterest outbound clicks are not automatically network clicks |
| Merchant action | network/merchant tracked action record with provider identity | authorized merchant/network report | click does not imply action/sale |
| Pending commission | affiliate network transaction/commission record | merchant transaction status if officially linked | merchant action does not imply commission |
| Validation / approval / reversal | network/merchant canonical transaction status and revision history | sanitized program record | pending cannot be promoted to validated by elapsed time alone |
| Payable commission | network payable/balance record | payout statement | validated does not imply payable |
| Payout issued | network/payout-provider payout record | payout statement/reference | issued does not imply funds received |
| Settled cash | **Owner-authorized payout rail posted/settled funds evidence** | reconciled bank/payment-provider statement metadata | network "paid" alone never means cash settled |
| Direct cash cost | actual receipt/invoice/authorized payment evidence or explicit measured zero where structurally applicable | sanitized cost ledger | tool list price does not equal experiment cost |
| Time | measured timer/log/timestamp record | Owner/Work measured attestation | do not assign a labor rate automatically |

### Conflict rule

If two sources conflict:

1. keep both observations append-only;
2. mark the lower-confidence item BLOCKED if the conflict is material;
3. prefer the domain-specific authoritative source above for derived truth;
4. never delete the losing observation;
5. emit a reconciliation note/event reference.

---

## 3. Canonical event ontology V1

The ledger supports these event types:

1. PIN_PUBLISHED
2. PIN_IMPRESSION_OBSERVED
3. PIN_CLICK_OBSERVED
4. OUTBOUND_CLICK_OBSERVED
5. NETWORK_CLICK_OBSERVED
6. MERCHANT_ACTION_TRACKED
7. COMMISSION_PENDING
8. COMMISSION_VALIDATED
9. COMMISSION_REVERSED
10. COMMISSION_PAYABLE
11. PAYOUT_ISSUED
12. CASH_SETTLED
13. NEGATIVE_ADJUSTMENT_RECORDED
14. COST_RECORDED
15. TIME_RECORDED

### Event meaning

- PIN_PUBLISHED — the content became public on Pinterest.
- PIN_IMPRESSION_OBSERVED — provider-reported Pinterest impression observation for a defined scope/window.
- PIN_CLICK_OBSERVED — provider-reported Pin click observation.
- OUTBOUND_CLICK_OBSERVED — provider-reported off-Pinterest outbound click observation.
- NETWORK_CLICK_OBSERVED — affiliate network saw a click or aggregate click observation.
- MERCHANT_ACTION_TRACKED — merchant/network recorded the commissionable or candidate merchant action.
- COMMISSION_PENDING — a commission record exists but is not yet validated.
- COMMISSION_VALIDATED — commission is approved/validated under provider rules.
- COMMISSION_REVERSED — commission/action was reversed, cancelled, refunded, returned, rejected or clawed back at commission layer.
- COMMISSION_PAYABLE — provider marks the commission as eligible for payout.
- PAYOUT_ISSUED — provider says payout was issued/sent. This is not cash.
- CASH_SETTLED — actual funds received on Owner-authorized payout rail and reconciled.
- NEGATIVE_ADJUSTMENT_RECORDED — explicit negative adjustment at commission/payout accounting layer when the provider exposes a separate adjustment rather than a normal reversal.
- COST_RECORDED — measured attributable cash cost.
- TIME_RECORDED — measured attributable time.

No event name is allowed to imply more economic truth than its source proves.

---

## 4. Append-only ledger contract

The ledger is immutable history.

### Required rule

**Never overwrite, mutate or delete a historical event to make current totals look correct.**

Corrections are new events:

- a refunded sale → COMMISSION_REVERSED;
- a provider correction → new observation/correction event with reference to the prior record;
- a negative payout adjustment → NEGATIVE_ADJUSTMENT_RECORDED;
- a later bank debit/chargeback that actually changes settled funds → CASH_SETTLED with a negative amount and reconciliation reference, if and only if the payout rail proves the debit.

### Provider snapshots vs event deltas

Pinterest/network analytics may expose cumulative or windowed counters rather than individual click rows.

For observation events, record:

- metric name;
- metric value;
- aggregation mode;
- observation window start/end;
- observed_at;
- provider/source reference.

Allowed aggregation modes:

- SNAPSHOT_CUMULATIVE
- WINDOW_TOTAL
- PROVIDER_DELTA
- INDIVIDUAL_EVENT

Repeated snapshots must not be summed blindly.

---

## 5. Minimum identity carried by every ledger event

Every event must contain:

- schema_version;
- event_id;
- event_type;
- experiment_id;
- content_id when applicable;
- pin_id when applicable;
- framing_id when applicable;
- network when applicable;
- merchant/program identifier when applicable;
- source_system;
- sanitized source_record_id if available;
- sanitized source reference;
- attribution key/sub-ID metadata if available and safe;
- occurred_at;
- observed_at;
- evidence status;
- evidence confidence;
- sanitized evidence reference;
- currency and amount when applicable.

Private tracking tokens are never stored in the public ledger.

---

## 6. Idempotency and dedupe

### 6.1 Preferred deterministic identity

When a provider supplies a stable record ID, use a deterministic idempotency key derived from:

provider/source_system + source_record_id + canonical event_type + provider state/version/effective timestamp when necessary

Store only a sanitized provider ID/reference.

A repeated poll that returns the same provider record/state must resolve to the same idempotency identity and must not create duplicate revenue/cash.

### 6.2 State changes on one provider record

If one provider record changes state:

PENDING → VALIDATED → PAYABLE

that is not one mutable ledger row. Emit separate append-only canonical events, each tied to the same provider record identity and its observed state/effective time.

### 6.3 No stable provider ID

If the provider does not expose a stable ID:

- set idempotency.strategy = CONSERVATIVE_RECONCILIATION;
- do not invent uniqueness;
- compare the narrowest available tuple such as source + merchant + content/attribution key + event type + amount/currency + provider timestamp/window;
- mark ambiguous joins/repeats for manual reconciliation;
- do not double-count a record merely because polling returned it again;
- do not manufacture a unique source ID from random values and call it provider truth.

### 6.4 Aggregate metric snapshots

For cumulative/window snapshots, the deterministic identity includes:

source_system + metric_name + content scope + window_start + window_end + aggregation_mode + provider snapshot/effective timestamp if available

Derived metrics select the correct latest/authoritative observation for a scope/window; they do not sum duplicate snapshots.

---

## 7. Canonical money-state machine

Canonical states:

NO_REVENUE → PENDING → VALIDATED → PAYABLE → PAYOUT_ISSUED → CASH_SETTLED

Provider labels are mapped into these states; providers are **not required** to use the same words.

### Normalization

- no commission-bearing merchant action yet → NO_REVENUE
- commission exists but awaits provider validation → PENDING
- provider approves/validates commission → VALIDATED
- provider makes commission eligible for payout → PAYABLE
- provider issues payout → PAYOUT_ISSUED
- Owner payout rail proves funds received → CASH_SETTLED

### Reversals and cancellations

Reversal is a truth event, not an edit.

Possible paths include:

- PENDING → COMMISSION_REVERSED
- VALIDATED → COMMISSION_REVERSED
- PAYABLE → COMMISSION_REVERSED or NEGATIVE_ADJUSTMENT_RECORDED
- PAYOUT_ISSUED → later negative payout adjustment
- CASH_SETTLED → later actual debit/chargeback evidenced by payout rail, represented as a new negative CASH_SETTLED event plus linked adjustment evidence

The current canonical balance/state is computed from the event history; it is never preserved as "gross fantasy revenue" after a reversal.

---

## 8. Reversal truth and net economics

### Commission record truth

For each distinct provider commission/action record:

- preserve every observed lifecycle event;
- determine current valid amount after reversals/adjustments;
- never sum PENDING + VALIDATED + PAYABLE for the same commission as three revenues.

### Settled cash truth

Net settled cash is derived only from VERIFIED CASH_SETTLED events on Owner-authorized payout rails, including verified negative cash settlement/debit events where applicable.

A commission reversal that never affected the payout rail changes commission economics but does not retroactively create a bank debit.

### Negative adjustments

NEGATIVE_ADJUSTMENT_RECORDED must contain:

- adjustment scope: COMMISSION or PAYOUT;
- negative amount when monetary;
- source record/reference;
- related provider record/payout reference when available;
- reason category if provider exposes it.

It cannot be used as a substitute for CASH_SETTLED unless actual funds moved on the authorized payout rail.

---

## 9. Cost truth and time truth

Cash cost and time are separate dimensions.

### Measured time fields

At minimum:

- production_minutes
- qa_minutes
- owner_minutes

Additional measured categories may include:

- research_minutes
- publishing_minutes
- monitoring_minutes
- reconciliation_minutes
- work_minutes

TIME_RECORDED stores measured minutes only.

**Do not assign a labor rate automatically.**

### Measured cash-cost categories

At minimum:

- tool_api_cash_cost
- direct_creative_cost
- paid_media
- payment_fee
- fx_fee
- other_attributable_variable_cost

Current experiment rule:

**paid_media = 0 by design unless a future Brain/Owner authorization explicitly changes it.**

Do not infer cash cost from catalog pricing if no attributable payment occurred.

---

## 10. Derived metrics — observed data only

No KPI target is defined in MCME-006.

All derived metrics require:

1. source events with acceptable evidence;
2. compatible time/scope;
3. denominator > 0 where division is used;
4. no double-counted provider records.

### Allowed derived metrics

- outbound CTR = outbound clicks / Pinterest impressions, only when denominator > 0 and scopes match;
- merchant action rate = distinct tracked merchant actions / qualified network or outbound clicks, only with defensible attribution and denominator > 0;
- attributed revenue = current attributed commission amount from distinct commission records at or beyond PENDING, net of applicable commission reversals; do not add the same commission across states;
- validated revenue = current amount of distinct validated commissions net of reversals;
- payable revenue = current amount of distinct payable commissions net of reversals/adjustments;
- reversals = sum/classification of verified reversal/negative-adjustment events at their applicable layer;
- settled cash = sum of VERIFIED CASH_SETTLED amounts for the experiment/currency scope;
- net settled cash = settled cash after verified negative settlement/debit events;
- direct cash cost = sum of VERIFIED COST_RECORDED cash amounts attributable to the experiment;
- net cash contribution = net settled cash - direct cash cost, only inside a defined same-currency or explicitly reconciled FX scope;
- NCC/1000 = net cash contribution / qualified-view denominator × 1000 only when the denominator definition is explicitly locked and observed.

If currencies differ and no verified FX conversion evidence exists, do not collapse them into one money total.

---

## 11. Evidence levels

### L0 — no commercial evidence

No genuine qualified outbound click attributable to the experiment.

### L1 — qualified outbound click

At least one genuine qualified outbound click is evidenced.

This is commercial intent evidence, not revenue.

### L2 — tracked merchant action / attributed commission

At least one genuine merchant action/commission record attributable to experiment traffic is evidenced.

Pending revenue may exist. It is not validated revenue or cash.

### L3 — validated / payable commission

At least one attributed commission reaches VALIDATED or PAYABLE with source evidence.

This is stronger revenue evidence, still not settled cash.

### L4 — settled cash + measured direct cost/time

At least one attributable payout is reconciled to funds actually received on the Owner-authorized payout rail, and direct cost/time records for the experiment are measured sufficiently for economics analysis.

### Promotion rules

- promotion is monotonic only when source evidence exists;
- views, saves or impressions cannot promote above L0;
- outbound click can promote only to L1;
- merchant action/pending commission can promote only to L2;
- validated/payable commission can promote only to L3;
- payout issued alone remains L3;
- only reconciled CASH_SETTLED plus measured cost/time can promote to L4;
- UNKNOWN/BLOCKED/FAIL evidence never promotes a level.

A later reversal can reduce economics without erasing the historical fact that a prior evidence level was once observed. Current-economics status must separately reflect reversal impact.

---

## 12. Bounded reconciliation

Reconciliation chain:

Pinterest outbound clicks ↔ network clicks ↔ merchant actions ↔ commission records ↔ payout records ↔ settled funds

### Rules

1. Counts are not expected to match exactly.
2. Pinterest outbound clicks and network clicks can differ because of tracking loss, blocking, redirects, attribution rules or observation windows.
3. A network click without a stable join to a Pin must remain unattributed/partially attributed.
4. A merchant action without an attribution key must not be fabricated into a Pin-level join.
5. A commission can be attributed to an experiment without being attributable to an individual Pin if that is the strongest defensible evidence.
6. Payouts may aggregate many commissions; reconciliation may be one-to-many.
7. Settled bank/payment-rail transactions may aggregate payouts/fees; retain explicit reconciliation references.
8. No "balancing event" may be invented merely to force counts or money totals to match.
9. Reconciliation attempts are bounded to available stable identifiers and documented provider windows; unresolved items remain UNKNOWN/BLOCKED.

---

## 13. Privacy contract

The public repository stores only sanitized metadata.

Never store:

- credentials/passwords;
- MFA/OTP/CAPTCHA data;
- session cookies;
- bearer/API secrets;
- raw sensitive affiliate tracking tokens;
- tax IDs;
- bank/card/account/routing numbers;
- identity documents;
- private payout identifiers;
- private payment-provider IDs if sensitive;
- personal identity data not required for public evidence.

Allowed:

- sanitized provider/program names;
- sanitized source record IDs when safe;
- external secret-reference placeholders;
- event timestamps;
- evidence status/confidence;
- non-sensitive public URLs;
- redacted evidence references.

If a stable provider ID itself is sensitive, store a safe external-reference handle and keep the raw value outside GitHub.

---

## 14. Structural examples — EXAMPLE / NOT REAL ECONOMICS

**These examples are fictitious structure only. They do not report a real click, sale, commission, payout or cash event.**

Example A — outbound observation shape:

- event_type: OUTBOUND_CLICK_OBSERVED
- experiment_id: EXAMPLE-NOT-REAL
- pin_id: EXAMPLE-PIN
- source_system: PINTEREST
- evidence.status: VERIFIED
- metric.aggregation_mode: WINDOW_TOTAL
- metric.value: EXAMPLE_PLACEHOLDER

Example B — commission lifecycle shape:

- source_record_id: EXAMPLE-COMMISSION
- COMMISSION_PENDING event observed first
- COMMISSION_VALIDATED event later if provider validates
- COMMISSION_REVERSED event later if provider reverses
- history remains append-only

Example C — cash rule:

- PAYOUT_ISSUED from network: **not cash**
- CASH_SETTLED only after Owner-authorized payout rail proves funds received
- values intentionally omitted because this is NOT REAL ECONOMICS

---

## 15. Robot ingestion readiness — future only

MCME-006 does **not** build polling automation.

A future authorized read-only adapter must output normalized candidate events containing at least:

- provider/source system;
- source record ID if available;
- canonical event type candidate;
- raw provider state label stored only if non-sensitive;
- occurred_at;
- observed_at;
- experiment/content/Pin attribution identifiers when defensible;
- money amount/currency when applicable;
- metric snapshot/window when applicable;
- evidence reference;
- adapter version;
- idempotency inputs.

### Adapter must never infer

- a sale from a click;
- a commission from a merchant action unless provider reports it;
- validation from elapsed time;
- payable from validation;
- payout issued from payable;
- cash settled from network "paid";
- Pin-level attribution when the stable join is absent;
- a unique provider ID when none exists;
- revenue/cash by filling missing values;
- a labor rate.

Adapters emit evidence; the ledger/reconciliation layer determines canonical truth.

---

## 16. JSON Schema contract

Implementation schema:

06_METRICS/mcme_cash_truth_v1.schema.json

The schema validates one append-only ledger event. Storage systems may wrap these event objects in JSONL, database rows or immutable event-stream envelopes, but the event payload semantics remain canonical.

Key requirements enforced in schema:

- canonical event_type enum;
- event/source/evidence identity;
- timestamps;
- evidence status/confidence;
- idempotency strategy;
- optional metric/money/cost/time/adjustment/reconciliation structures;
- CASH_SETTLED requires settlement evidence indicating actual funds received and Owner-authorized rail;
- TIME_RECORDED requires a time payload;
- COST_RECORDED requires cost + money payload;
- monetary values use decimal strings to avoid binary floating-point money errors.

---

## 17. Remaining UNKNOWNs

Because actual Gate A is still OWNER_GATED_NOT_EXECUTED, the following remain unknown:

- real network;
- real merchant/program;
- stable provider IDs available from that network;
- Pin/sub-ID attribution capability;
- provider event labels and lifecycle semantics;
- exact validation/reversal rules;
- payout grouping behavior;
- payout threshold/cycle;
- actual payout rail;
- whether payout reports expose stable payout IDs;
- settlement reference granularity;
- reporting latency;
- currency/FX behavior;
- actual click/action/commission events;
- actual costs/time;
- any real revenue or cash.

No UNKNOWN above may be converted to economic truth without source evidence.

---

## 18. Owner boundaries

MCME-006 performs none of the following:

- account creation/login/application;
- credentials/MFA/CAPTCHA;
- KYC/tax/banking/payment setup;
- merchant contact;
- affiliate link creation in real accounts;
- Pin generation/publishing;
- external spend;
- fake/test/self-purchase;
- SaydiVoice/video work;
- Content Factory specification;
- polling automation;
- MCME-007.

---

## 19. MCME-006 handoff

Status: **COMPLETE — specification only; no real economics claimed.**

Canonical ontology:
PIN_PUBLISHED, PIN_IMPRESSION_OBSERVED, PIN_CLICK_OBSERVED, OUTBOUND_CLICK_OBSERVED, NETWORK_CLICK_OBSERVED, MERCHANT_ACTION_TRACKED, COMMISSION_PENDING, COMMISSION_VALIDATED, COMMISSION_REVERSED, COMMISSION_PAYABLE, PAYOUT_ISSUED, CASH_SETTLED, NEGATIVE_ADJUSTMENT_RECORDED, COST_RECORDED, TIME_RECORDED.

Highest cash truth:
**Owner-authorized payout rail evidence of funds actually received.**

Hard stop:
**Do not start MCME-007 automatically. Brain acceptance is required.**
