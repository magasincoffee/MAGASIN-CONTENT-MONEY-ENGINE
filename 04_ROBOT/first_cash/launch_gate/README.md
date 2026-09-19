# MCME Launch Readiness + Privacy Gate V1

Offline SAFE_PREP gate for future MCME-031/032. It reads a sanitized snapshot and returns only:

- `READY`
- `NOT_READY`

`READY` means **mechanical prerequisites are satisfied for a separately authorized future publish task**. It does not publish, call Pinterest, log in, or independently authorize a side effect.

## Five-Step

- **QUESTION:** what exact prerequisites are required before first real Pin publish?
- **DELETE:** dashboard, workflow engine, account automation, content generator, network integrations.
- **SIMPLIFY:** one strict schema + one deterministic evaluator + one privacy scanner + fixtures/tests.
- **ACCELERATE:** future MCME-031 can evaluate launch readiness without redesign.
- **AUTOMATE:** deterministic local readiness evaluation only.

## Critical READY checks

READY requires all critical Gate A classes verified/usable, exactly three deterministic 2:3 Pin records with QA PASS, locked observation window/source plan, publish-safety mechanics ready, Cash Truth local sink ready, future authorized browser/account prerequisite verified, and an explicit side-effect authorization field verified `true`.

Any critical `UNKNOWN`, `BLOCKED`, `FAIL`, missing/false required value, wrong Pin count, duplicate content ID, QA failure, privacy finding, or missing launch prerequisite results in `NOT_READY` or validation rejection.

## Privacy scanner

Fail-closed scanner flags obvious:

- passwords/secrets/API or bearer tokens;
- cookies/session values;
- OTP/MFA/recovery/CAPTCHA artifacts;
- tax IDs;
- bank/routing/card/account fields;
- identity-document fields;
- private payout/tracking-token fields;
- browser profile/session paths exposing private state;
- URLs containing risky secret/auth/token query parameters.

It allows public merchant identifiers, deterministic internal IDs, hashes/status flags, safe metadata, safe public URLs, and opaque placeholders such as `PRIVATE_REF:affiliate-destination-v1`.

The scanner is defense-in-depth, **not a guarantee that every possible secret format can be detected**. Owner-side sanitization remains mandatory; uncertain data must remain private.

## Fixtures

- `current_realistic_l0.json` — mirrors current project truth: Gate A not executed and no side-effect authorization; must be `NOT_READY`.
- `hypothetical_ready.json` — **HYPOTHETICAL TEST ONLY**, all fields mechanically verified including a test-only authorization flag; proves evaluator mechanics, not real launch authorization.

Neither fixture represents real merchant approval, real Pin assets, real authorization, or real economics.

## Offline tests

From repository root:

```bash
python -m unittest discover -s 04_ROBOT/first_cash/launch_gate/tests -v
```

Dependency: Python 3 + `jsonschema` Draft 2020-12 support. No network/browser/API calls are used.

## Evaluate a sanitized snapshot

```bash
python 04_ROBOT/first_cash/launch_gate/launch_gate.py snapshot.json
```

No external side effect is performed.
