# MCME publish side-effect safety — mock/dry-run only

SAFE_PREP runtime for future **MCME-032**. This package proves idempotency/recovery mechanics only. It contains **no Pinterest implementation**, no login/browser/API/network calls, no account action, no production Pin, and no external side effect.

## Five-Step

- **QUESTION:** minimum mechanism preventing duplicate Pin publication = deterministic identity + durable pre-action latch + reconciliation-before-retry.
- **DELETE:** real Pinterest code, browser/API automation, scheduler, queue, distributed lock, DB.
- **SIMPLIFY:** deterministic key + local/private JSON latch + mock send + mock reconciliation + bounded retry.
- **ACCELERATE:** future MCME-032 can plug an explicitly authorized backend into already-tested safety semantics.
- **AUTOMATE:** local state-machine mechanics only.

## Deterministic identity

```text
publish_key = SHA-256(canonical JSON {
  experiment_id,
  content_id,
  content_version,
  destination_version
})
```

Same intended publish => same key across restart. Changing `content_version` or `destination_version` => different key.

Intent fields must be opaque sanitized identifiers. URLs, credentials, cookies, tokens, MFA/OTP/CAPTCHA, bank/tax/identity data are rejected/not persisted.

## Local/private latch

Default directory:

```text
~/.mcme_private/publish_safety/
```

Override for a private runtime location:

```bash
export MCME_PUBLISH_SAFETY_DIR=/private/path/publish_safety
```

One JSON file per `publish_key`, user-only mode where supported. Persisted operational metadata only:

- publish key;
- experiment/content/version/destination version;
- state;
- bounded attempt count;
- sanitized mock published ID;
- reconciliation status;
- timestamps/transition history.

Never commit a future real latch store to Git.

## States

```text
PREPARED
SEND_STARTED
CONFIRMED
BLOCKED_AUTH
BLOCKED_AMBIGUOUS
FAILED_CONFIRMED
```

Before any mock send, `PREPARED` is persisted; immediately before the side-effect boundary, `SEND_STARTED` plus attempt count is persisted.

## Exactly-once intended semantics

- `CONFIRMED` invoked again => zero additional send.
- restart in `SEND_STARTED` / `BLOCKED_AMBIGUOUS` => reconcile before any retry.
- reconciliation `CONFIRMED_PRESENT` => `CONFIRMED`, zero resend.
- reconciliation `UNKNOWN` / `AMBIGUOUS` => `BLOCKED_AMBIGUOUS`, zero resend.
- reconciliation `CONFIRMED_ABSENT` may unlock **one** bounded retry.
- total sends per intended publish are capped at **2** (initial + one retry).
- after cap is exhausted and absence is reconciled => `FAILED_CONFIRMED`.
- auth/MFA/CAPTCHA-like mock result => `BLOCKED_AUTH`; Owner resolution is outside this task.

No blind resend is implemented.

## Mock backend outcomes

Tests can simulate:

- `success`
- `timeout_after_create`
- `timeout_no_create`
- `ambiguous_no_create`
- `auth_block`
- `confirmed_failure`

The mock backend is a local JSON file only and performs no platform/network call.

## Offline tests

From repository root:

```bash
python -m unittest discover -s 04_ROBOT/first_cash/publish_safety/tests -v
```

Future MCME-032 must separately obtain explicit external-side-effect authorization and an authorized backend.
