# SOT — PUBLISHER & RECONCILIATION

## State machine

DRAFT
-> QA_PASS
-> QUEUED
-> PRE_ACTION_LATCHED
-> PUBLISHING
-> PUBLISHED
-> RECONCILED

Failure states:
BLOCKED, FAILED_RETRYABLE, FAILED_TERMINAL, UNKNOWN_SIDE_EFFECT.

## Idempotency

publish_key = deterministic(page_id + creative_id + scheduled_slot/version)

Before external action, persist PRE_ACTION_LATCHED.

After action, persist provider post ID and reconcile.

Never blindly retry UNKNOWN_SIDE_EFFECT.

## Retry policy

Retries are bounded and classified by failure type.

Auth/MFA/CAPTCHA ambiguity -> Owner exception.
Duplicate/unknown provider state -> reconcile before any resend.

## Scheduling

Cadence is an experiment variable, not a fixed vanity target.

Avoid spam behavior and preserve page health.

## Evidence

Every publish attempt writes:
request identity, timestamp, result, provider post ID if known, error classification, retry count, reconciliation status.

Control must expose stuck/failed publishing immediately.
