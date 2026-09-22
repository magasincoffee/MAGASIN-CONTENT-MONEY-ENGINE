# MAGASIN CONTENT MONEY ENGINE — ARCHITECTURE V2

Status: OWNER APPROVED / CANONICAL ACTIVE ARCHITECTURE  
Date: 2026-09-22  
Supersedes active Architecture V1 routing. Historical evidence remains append-only.

## Mission

Create real, measurable cash in Vietnam by detecting fast-rising social-commerce demand from Chinese social platforms, mapping that demand to Shopee Vietnam affiliate products, producing compliant Vietnamese content, distributing it, and measuring the path from qualified view to settled cash.

## North Star

**NET CASH CONTRIBUTION / 1,000 QUALIFIED VIEWS**

Vanity metrics are diagnostic only.

## Five-Step Operating Law

Every material action follows, in order:

1. QUESTION — challenge every requirement and assumption.
2. DELETE — remove work not required to reach first cash.
3. SIMPLIFY — use the smallest money loop that can be tested.
4. ACCELERATE — shorten signal → content → click → order → cash.
5. AUTOMATE — automate only after the loop has demonstrated real economic evidence.

## Canonical V2 topology

```text
DOUYIN ─────────────┐
XIAOHONGSHU ────────┤
                    ↓
            SOCIAL RADAR
                    ↓
             TREND SCORER
                    ↓
           PRODUCT MAPPER
                    ↓
            SHOPEE VIETNAM
                    ↓
          AFFILIATE ELIGIBILITY
                    ↓
          SOURCE / RIGHTS GATE
                    ↓
            CONTENT BRAIN
                    ↓
             EDIT ROBOT
                    ↓
            PUBLISH QUEUE
                    ↓
       TIKTOK / FACEBOOK REELS
       / SHOPEE-COMPATIBLE SURFACES
                    ↓
        PERFORMANCE COLLECTOR
                    ↓
          ANALYTICS BRAIN
                    ↓
          KILL / KEEP / SCALE
                    ↓
             CASH TRUTH
```

## Initial source set — locked for V1

1. Douyin — primary trend discovery source.
2. Xiaohongshu / RED — secondary confirmation source for repeated product/content signals.
3. Evil0ctal/Douyin_TikTok_Download_API — first technical collector candidate for Douyin/TikTok metadata and bounded ingestion.

Xiaohongshu automation is deferred until Douyin proves commercial value. Manual/limited XHS confirmation is enough for Proof-of-Money V1.

## Market and monetization lock

For V1:

```text
MARKET = VIETNAM
MONETIZATION = SHOPEE AFFILIATE
TRAFFIC = ORGANIC SHORT-FORM CONTENT
AD SPEND = 0
```

The prior US/Pinterest/Awin/impact.com route is no longer the active first-cash architecture. Its evidence is historical and must not be deleted or rewritten.

## Proof-of-Money loop

```text
TREND
→ PRODUCT
→ VIETNAMESE CREATIVE
→ PUBLICATION
→ AFFILIATE CLICK
→ ATTRIBUTED ORDER
→ APPROVED COMMISSION
→ CASH RECEIVED
```

Success is not “Robot installed” or “video got views.” Success progresses through:

- CASH GATE 0 — affiliate click;
- CASH GATE 1 — attributed Shopee order;
- CASH GATE 2 — approved commission;
- CASH GATE 3 — funds actually received and reconciled.

## V1 operating constraints

Before the first attributed order:

- scan a bounded initial set, approximately 50–100 candidate videos;
- select no more than 3 products for the first batch;
- create 3 differentiated creatives per product, maximum 9 initial videos;
- publish manually or through the simplest authorized path;
- no paid traffic;
- no generic dashboard build;
- no multi-source crawler platform;
- no full auto-publishing system;
- no automation of an unproven loop.

## Product selection criteria

A candidate product should be favored when it has:

- strong visual demonstration;
- problem → solution understandable within seconds;
- evidence of rising/repeated social interest;
- an equivalent product available on Shopee Vietnam;
- affiliate eligibility that can be verified;
- acceptable seller/listing quality;
- low factual/safety claim burden;
- source material that can be used compliantly.

The system is niche-agnostic. Trend evidence selects the product category.

## Content rule

**Import proven ideas, not stolen finished content.**

Chinese social content may be used for:

- trend discovery;
- hook discovery;
- product discovery;
- pacing/angle analysis;
- reference-only scene understanding.

Publication must use original, licensed, supplier-authorized, creator-authorized, platform-permitted, public-domain, or otherwise rights-verified material.

```text
Download → minor edit → repost
```

is explicitly not the business model.

## Core roles

### Owner
Controls credentials, MFA/CAPTCHA, Shopee registration, KYC/tax, banking/payment setup, legal/rights ambiguity, spend, destructive account actions and any contractual decision requiring human authority.

### Brain
Chooses trend/product hypotheses, experiment priorities, thresholds, economic interpretation and KILL / KEEP / SCALE decisions.

### Work
Executes one bounded task and stops.

### Robot
Handles collection, normalization, scoring, state, rendering, scheduling, retries, reconciliation and later automation. Robot does not own strategy.

## Automation gate

Automation becomes valid only after the loop demonstrates economic evidence.

Recommended sequence:

```text
FIRST CLICK
→ FIRST ATTRIBUTED ORDER
→ REPEAT ORDERS
→ AUTOMATE PROVEN STEPS
→ SCALE
```

## Non-negotiable invariants

1. Five-Step precedes automation.
2. First real cash outranks architecture elegance.
3. Unknown rights/account/payment state never silently becomes PASS.
4. No pure-reupload model.
5. No paid traffic before explicit Owner approval and proven economics.
6. Historical Awin/impact/Pinterest evidence remains immutable history.
7. Cash Truth remains the canonical economic evidence sink.
8. Weak products and creatives are deleted quickly.
9. Publish/account/payment side effects remain fail-closed.
10. Automation must reduce time-to-cash, not merely increase system complexity.
