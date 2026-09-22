# 24/7 AUTONOMY ARCHITECTURE — V2

Status: TARGET PROPERTY / NOT YET AUTHORIZED FOR FULL PRODUCTION  
Date: 2026-09-22

## Principle

24/7 automation is a destination, not the starting point.

The first requirement is to prove:

```text
trend → product → content → click → order → commission → cash
```

Only then automate the steps that demonstrably shorten time-to-cash.

## Control topology

```text
OWNER
  ↓ authority / boundaries
BRAIN
  ↓ bounded task / thresholds
ROBOT
  ↓
COLLECTORS / EDIT / QUEUES / SERVICES
  ↓
RESULT + EVIDENCE
  ↓
BRAIN
```

## Target autonomous loops

### Social Radar loop
Douyin ingestion → normalize → snapshot → growth metrics → trend score.

Xiaohongshu is initially a confirmation input and becomes automated only if its incremental value is proven.

### Product Mapping loop
Trend/product signal → Shopee Vietnam equivalent candidates → affiliate/listing evidence → opportunity score.

### Production loop
Reference intelligence → rights/source gate → Vietnamese hook/script → edit plan → render → QA.

### Distribution loop
Queue → authorized publish → reconcile publication → persist platform content ID.

### Measurement loop
Collect views/clicks/orders/commission/cash → normalize into Cash Truth.

### Learning loop
Compare products/hooks → KILL / KEEP / SCALE → update next bounded experiment.

## Suggested states

```text
DISCOVERED
SNAPSHOT_PENDING
SCORED
PRODUCT_MAPPING
AFFILIATE_CHECK
RIGHTS_CHECK
CREATIVE_READY
QA
READY_TO_PUBLISH
PUBLISHING
LIVE
MEASURING
ORDER_ATTRIBUTED
COMMISSION_PENDING
COMMISSION_APPROVED
CASH_SETTLED
SCALE
KILL
WAIT_OWNER
FAILED_RETRYABLE
FAILED_TERMINAL
```

## Owner-only boundaries

Robot stops for:
- login credentials;
- MFA/OTP/CAPTCHA;
- Shopee signup/contractual acceptance;
- KYC/tax identity;
- bank/payment setup;
- unclear copyright/license rights;
- account suspension/appeal;
- destructive actions;
- spend outside explicit budget.

## Side-effect safety

For publishing, spend, messages, account mutations or deletion:
- deterministic idempotency/reconciliation key;
- pre-action persisted state;
- bounded retry;
- no blind duplicate side effect;
- evidence after action.

## Economic circuit breaker

Stop or reduce scale when:
- cash attribution breaks;
- product mapping becomes unreliable;
- affiliate eligibility becomes unknown;
- rights evidence is missing;
- clicks do not progress to orders;
- approved commission reverses materially;
- platform policy warnings appear;
- spend exceeds approval.

## Automation admission rule

Full automation is forbidden merely because code can be written.

Minimum admission sequence:

```text
FIRST ATTRIBUTED ORDER
→ REPEATABLE ORDER EVIDENCE
→ RELIABLE ATTRIBUTION
→ BRAIN AUTHORIZATION
→ AUTOMATION V1
```

Priority is expected marginal net cash adjusted by confidence, time and risk — not FIFO and not content volume.
