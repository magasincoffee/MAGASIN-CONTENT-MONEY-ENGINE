# SOT — GLOBAL TREND RADAR

## Purpose

Discover rising content, product, problem, hook, and audience signals early enough to create commercially useful Vietnamese content.

## Source policy

Global and modular. Candidate sources:
- Douyin;
- Xiaohongshu;
- TikTok;
- YouTube / Shorts;
- Instagram / Reels;
- Facebook public surfaces;
- marketplaces and public trend surfaces;
- future sources with compliant access.

A source is kept only if its incremental signal improves decisions.

## Canonical candidate fields

source_platform, source_id, source_url, creator_ref, observed_at, published_at, language/country, caption/tags, engagement snapshot, growth snapshot, media/reference pointers, discovered product/problem/topic, rights_classification, commercial_match_status.

## Scoring

Trend score is not popularity alone.

Combine:
- velocity;
- recency;
- repeated cross-source confirmation;
- visual demonstrability;
- problem-solution clarity;
- novelty/saturation;
- Vietnam relevance;
- Shopee mappability;
- rights/production feasibility.

## Dedupe

Cluster duplicate/reposted source material before scoring so one viral asset does not create fake multi-source confirmation.

## Output

A bounded ranked opportunity queue, not an infinite crawler archive.

## Delete rule

Remove a source adapter if it consumes meaningful resources without improving selected opportunities or commercial outcomes.
