# MCME Cash Truth local/private MVP

Small offline runtime for future MCME-034. It validates the canonical schema at `06_METRICS/mcme_cash_truth_v1.schema.json`, writes immutable JSONL events, dedupes provider observations, replays explicit states, and computes only mechanically safe totals.

## Five-Step

- **QUESTION:** the 3-Pin MVP needs an evidence sink, not a database or service.
- **DELETE:** DB, web service, API adapters, scheduler, dashboard, cloud infrastructure.
- **SIMPLIFY:** canonical JSON Schema + append-only local/private JSONL + deterministic dedupe/reconciliation + replay/tests.
- **ACCELERATE:** future MCME-034 can ingest evidence without redesigning money truth.
- **AUTOMATE:** only deterministic local validation/append/replay mechanics. No external automation.

## Privacy / location

The runtime ledger is **LOCAL/PRIVATE**. Do not commit a real ledger containing future account, tracking, payout, or private evidence.

Default path:

```text
~/.mcme_private/cash_truth/ledger.jsonl
```

Override explicitly:

```bash
export MCME_CASH_TRUTH_LEDGER=/private/path/ledger.jsonl
```

The runtime creates the ledger with user-only file mode where supported. Public Git contains only code, schema, and fictitious structural fixtures.

Never place passwords, cookies, API secrets, MFA/OTP, tax IDs, bank/account/card data, identity documents, raw private payout identifiers, or sensitive tracking tokens in event payloads.

## Contract

The existing Cash Truth V1 schema remains canonical.

Hard truths:

```text
click != sale != pending != validated != payable != payout issued != settled cash
```

The runtime never promotes one state into the next based on elapsed time or missing data.

`CASH_SETTLED` is additionally fail-closed at runtime and requires:

- schema-valid settlement flags;
- `source.source_system = OWNER_PAYOUT_RAIL`;
- `evidence.status = VERIFIED`;
- `funds_actually_received = true`;
- `owner_authorized_payout_rail = true`;
- `reconciled_to_payout = true`;
- a sanitized payout source reference **or** a `MATCHED` reconciliation linking a payout event.

A `PAYOUT_ISSUED` event never becomes cash automatically.

## Idempotency

Stable provider identity is preferred:

```text
source_system + network + merchant + program + source_record_id + canonical event type (+ provider state/version when required)
```

Repeated stable source events return `DUPLICATE_SOURCE_EVENT` and are not appended again.

If the provider has no stable ID, use `CONSERVATIVE_RECONCILIATION`. A first unique narrow fingerprint may be appended, but a later fingerprint collision returns `REQUIRES_RECONCILIATION` and does **not** append silently.

`MANUAL_REVIEW` never auto-appends.

## Append-only

Historical JSONL lines are never edited or deleted by this runtime. Corrections, reversals, negative adjustments, and genuine later cash debits are new events.

For a genuine debit/clawback after settlement, append a **negative `CASH_SETTLED` event** only when Owner-authorized payout-rail evidence satisfies the same settlement guards.

## Cost and time

- Cash costs remain monetary events (`COST_RECORDED`).
- Time remains minutes (`TIME_RECORDED`).
- No labor rate is assigned.
- Time is never converted into cash automatically.

## Replay totals

Replay reports only explicit observed data:

- event counts;
- current pending/validated/payable commission amounts for provider records with stable source IDs;
- reversal/negative-adjustment observations;
- positive/negative/net settled cash;
- direct cash cost;
- net cash contribution by currency;
- measured time minutes.

It does not infer a sale/commission/cash state, does not convert currencies, and does not create KPI targets.

## Offline tests

From repository root:

```bash
python -m unittest discover -s 06_METRICS/tools/cash_truth_ingest/tests -v
```

Dependency: Python 3 + `jsonschema` with Draft 2020-12 support. No network access is used.

## CLI

Validate one event:

```bash
python 06_METRICS/tools/cash_truth_ingest/cash_truth.py validate event.json
```

Append to default private ledger:

```bash
python 06_METRICS/tools/cash_truth_ingest/cash_truth.py append event.json
```

Replay:

```bash
python 06_METRICS/tools/cash_truth_ingest/cash_truth.py replay
```

Use `--ledger /private/path/ledger.jsonl` to override the ledger location.
