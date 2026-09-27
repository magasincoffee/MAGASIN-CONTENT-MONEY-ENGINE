# SOT — CORE DATA CONTRACTS

## Canonical IDs

source_item_id
opportunity_id
lane_id
product_id
affiliate_link_id
creative_id
hook_id
experiment_id
publish_key
platform_post_id
commerce_event_id
cash_event_id
task_id
run_id

IDs must be stable and joinable across the loop.

## Core entities

SourceItem — observed trend/reference.
Opportunity — scored hypothesis joining topic/problem/product potential.
ContentLane — audience/content portfolio unit.
ProductCandidate — mapped Shopee opportunity.
AffiliateLink — tracked monetization path.
Creative — publishable artifact + provenance.
Experiment — hypothesis and variants.
PublishAttempt — external side-effect state.
PerformanceSnapshot — platform observations.
CommerceEvent — Shopee commercial evidence.
CashEvent — canonical money ledger entry.
Decision — KILL/KEEP/REVISE/SCALE.
OwnerBlocker — bounded exception.

## Time

Persist observed_at, effective_at/provider time when available, and ingested_at separately.

## Provenance

Every generated creative must trace to:
- source/reference signals;
- asset provenance;
- rights classification;
- script/render version;
- product/link;
- experiment.

## Append-only evidence

Provider observations and Cash Truth are append-only. Derived current state may be recomputed but must not destroy the event trail.

## Unknown handling

Unknown is explicit. Missing fields are never silently coerced to PASS/zero/success.
