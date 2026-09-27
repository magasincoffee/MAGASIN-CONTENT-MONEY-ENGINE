# SOT — CASH TRUTH

## Purpose

Be the canonical economic evidence sink.

## Event model

Append-only. Corrections are new events.

Events:
QUALIFIED_VIEW_OBSERVED
AFFILIATE_CLICK_OBSERVED
ATTRIBUTED_ORDER_OBSERVED
COMMISSION_PENDING
COMMISSION_APPROVED
COMMISSION_REVERSED
PAYOUT_ISSUED
CASH_RECEIVED
CASH_RECONCILED
NEGATIVE_ADJUSTMENT
COST_RECORDED
TIME_RECORDED

## Evidence levels

L0 no commercial evidence
L1 verified affiliate click
L2 attributed order
L3 approved commission
L4 cash received + reconciled with cost/time measured

## First real cash

FIRST REAL CASH = funds actually received on an Owner-authorized payout rail and reconciled to the related Shopee payout/commission evidence.

## Dedupe

Prefer provider IDs + event type + provider state/version/effective time.

If no stable provider ID exists, use conservative reconciliation and never invent uniqueness.

## Reporting

Control must display each money stage separately.

No dashboard field named revenue may silently combine pending, approved, payable, payout, or cash.
