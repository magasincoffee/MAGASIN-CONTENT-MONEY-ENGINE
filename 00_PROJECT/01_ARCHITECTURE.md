# MONEY V3 — AUTONOMOUS FACEBOOK -> SHOPEE ARCHITECTURE

Status: OWNER APPROVED / CANONICAL ACTIVE ARCHITECTURE
Effective: 2026-09-27
Supersedes Architecture V2 as active authority.

## Mission

Autonomously discover global content/product opportunities, produce compliant Vietnamese Facebook content, distribute it through an authorized Fanpage, learn from performance and commerce telemetry, and maximize real Shopee Affiliate cash contribution.

## Topology

GLOBAL TREND SOURCES
-> TREND RADAR
-> NORMALIZER / DEDUPE
-> TREND + COMMERCIAL SCORER
-> CONTENT LANE ROUTER
-> SHOPEE PRODUCT MAPPER
-> RIGHTS / POLICY GATE
-> CONTENT BRAIN
-> EDIT / RENDER ROBOT
-> CREATIVE QA
-> AFFILIATE LINK BINDER
-> FACEBOOK PUBLISH QUEUE
-> FACEBOOK FANPAGE
-> PERFORMANCE COLLECTOR
-> SHOPEE COMMERCE COLLECTOR
-> CASH TRUTH
-> EXPERIMENT BRAIN
-> KILL / KEEP / SCALE
-> next cycle

CONTROL WEBAPP observes and controls the full loop.

## Distribution lock

Primary V1 surface: Facebook Fanpage.

Do not use a personal Facebook profile as the canonical Shopee Affiliate distribution surface.

A second page or additional platform is opened only after the first page produces enough evidence to justify it.

## Trend intelligence

The system is global-source, not China-only.

Sources may include Douyin, Xiaohongshu, TikTok, YouTube/Shorts, Instagram/Reels, Facebook, marketplaces, public trend surfaces, and future sources.

Every source adapter must obey its terms, access rules, and content rights constraints.

## Content model

Import proven signals and ideas, not stolen finished content.

Allowed inputs to production include original, licensed, creator-authorized, supplier-authorized, platform-permitted, public-domain, or otherwise rights-verified assets.

Reference-only content may inform:
- hooks;
- angles;
- pacing;
- product discovery;
- topic selection;
- audience questions;
- scene concepts.

Pure download -> minor edit -> repost is not the business model.

## Content lanes

The system may run multiple content lanes, but each lane must have:
- audience promise;
- topic boundary;
- monetization hypothesis;
- success metric;
- stop condition.

The first Fanpage must remain coherent enough for audience and platform understanding.

## Monetization

Primary:
SHOPEE VIETNAM AFFILIATE

Secondary:
Facebook/platform monetization when eligible, without compromising affiliate economics or policy compliance.

## Automation model

Safe automation starts immediately for:
- ingestion;
- normalization;
- dedupe;
- scoring;
- research queues;
- script generation;
- edit plans;
- rendering;
- QA;
- telemetry;
- dashboards;
- experiment analysis.

External side effects such as publishing, destructive changes, spend, payment, or contractual actions use explicit authorization boundaries and fail-closed controls.

## Autonomy

Target operating mode:
ZERO-TOUCH NORMAL OPERATION + MINIMAL OWNER EXCEPTION HANDOFF

Owner-only exceptions:
credentials, MFA/OTP/CAPTCHA, KYC/tax, bank/payout, legal/rights ambiguity, appeals/suspensions, destructive account action, spend approval.

## Economic truth

Cash stages:
QUALIFIED_VIEW
-> AFFILIATE_CLICK
-> ATTRIBUTED_ORDER
-> COMMISSION_PENDING
-> COMMISSION_APPROVED
-> PAYOUT_ISSUED
-> CASH_RECEIVED
-> CASH_RECONCILED

Only CASH_RECONCILED is FIRST REAL CASH.

## North Star

NET CASH CONTRIBUTION / 1,000 QUALIFIED VIEWS

Supporting diagnostics:
- qualified reach;
- retention/watch time;
- share/save/comment quality;
- outbound CTR;
- affiliate click quality;
- order CVR;
- approved commission per 1,000 qualified views;
- cost/time per creative;
- cash settlement.

## Reliability laws

- deterministic content/experiment/publish IDs;
- append-only event history;
- idempotent external side effects;
- bounded retries;
- no blind resend;
- reconcile provider IDs after side effects;
- unknown != pass;
- blocked != pass;
- policy/rights ambiguity fails closed;
- every failure visible in Control.

## System-of-record split

Strategy/state: `00_PROJECT/*` and `00_PROJECT/V3_SOT/*`
Operational data: runtime database/event store
Economic truth: Cash Truth ledger
Owner view: Control Webapp
Historical evidence: Git history and non-canonical legacy artifacts
