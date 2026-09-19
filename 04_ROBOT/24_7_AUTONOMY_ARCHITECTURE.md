# 24/7 AUTONOMY ARCHITECTURE

Status: REQUIRED SYSTEM PROPERTY

## Objective

Run proven Content-to-Cash loops continuously with minimal Owner intervention while preserving safety, policy compliance and economic controls.

## Control topology

```text
OWNER
  ↓ authority / boundaries
BRAIN
  ↓ machine-readable bounded task
SUPERVISOR / ROBOT
  ↓
WORK / SERVICES
  ↓
RESULT + EVIDENCE
  ↓
BRAIN
```

Reuse lessons from MAGASIN Supervisor Three-Lane:
- explicit Brain target;
- deterministic task identity;
- persisted latches;
- exact-once reconciliation markers where side effects are uncertain;
- bounded retry;
- local/private credentials;
- fail-closed security boundaries.

Do not copy implementation blindly. Reuse proven invariants.

## Autonomous loops

### Opportunity loop
Discover → normalize → score → queue.

### Production loop
Research → rights gate → script → voice → video → QA.

### Distribution loop
Schedule → publish → verify publication → capture content ID.

### Measurement loop
Fetch analytics → fetch monetization/affiliate data → normalize → attribute.

### Learning loop
Update priors → compare experiments → KEEP/KILL/SCALE.

## State model

Suggested job states:

```text
DISCOVERED
SCORED
APPROVED_AUTOMATIC
PRODUCING
QA
READY_TO_PUBLISH
PUBLISHING
LIVE
MEASURING
EVALUATING
SCALE
KILL
WAIT_OWNER
FAILED_RETRYABLE
FAILED_TERMINAL
```

## Side-effect safety

For publish, delete, spend, message, account action or external mutation:
- deterministic idempotency key;
- pre-action persisted latch;
- server/platform reconciliation;
- no blind resend;
- bounded retry;
- evidence of confirmation.

## Owner-only boundaries

Robot must stop for:
- login credentials;
- MFA/OTP/CAPTCHA;
- KYC/tax identity;
- bank/payment setup;
- contractual acceptance with material legal/financial impact;
- copyright/license ambiguity;
- platform suspension/appeal decisions;
- destructive account deletion;
- spending outside an approved budget;
- ambiguous business decisions above delegated thresholds.

## Health requirements

24/7 does not mean never failing.

It means:
- failures are classified;
- transient failures recover automatically;
- loops do not duplicate side effects;
- deadlocks are detected;
- retries are bounded;
- state survives restart;
- watchdog can restart components;
- Owner gets a concise escalation only when needed.

## Economic circuit breaker

Autonomy must stop scaling when:
- cash attribution is broken;
- spend exceeds budget;
- conversion materially degrades;
- refund/reversal rate breaches threshold;
- platform policy warnings appear;
- rights evidence is missing;
- analytics source becomes untrusted.

## Scheduling principle

Priority queue is based on expected marginal net cash, adjusted by confidence and risk.

Not FIFO by default.
