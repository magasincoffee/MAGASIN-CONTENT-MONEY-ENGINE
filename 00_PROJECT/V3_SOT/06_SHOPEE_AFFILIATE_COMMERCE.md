# SOT — SHOPEE AFFILIATE COMMERCE

## Role

Shopee Vietnam Affiliate is the primary monetization engine.

## Verified starting state

- affiliate program approval: verified from prior execution;
- publisher access: verified;
- affiliate link smoke test: pending;
- final payout/tax/banking state: verify only when required.

## Product mapping

A product opportunity requires:
- real Shopee listing;
- affiliate eligibility where observable;
- acceptable seller/listing quality;
- product/content fit;
- viable commission/economics;
- low policy/claim burden;
- evidence that the audience problem maps to the product.

## Link contract

Each bound affiliate link stores:
- product/listing ID;
- canonical destination;
- affiliate/tracking link reference;
- created_at;
- link status;
- redirect smoke-test result;
- campaign/content/experiment IDs;
- click telemetry capability.

## Commerce events

AFFILIATE_CLICK
ATTRIBUTED_ORDER
COMMISSION_PENDING
COMMISSION_APPROVED
COMMISSION_REVERSED
PAYOUT_ISSUED
CASH_RECEIVED
CASH_RECONCILED

## D01 priority

Prove one real link redirect/tracking path before content volume.

## Truth rule

Orders/commission/cash must come from provider evidence or reconciled payout evidence, never inferred from Facebook clicks.
