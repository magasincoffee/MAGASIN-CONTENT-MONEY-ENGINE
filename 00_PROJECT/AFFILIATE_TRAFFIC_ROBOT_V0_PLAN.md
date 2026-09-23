# AFFILIATE TRAFFIC ROBOT V0 — REAL-TIME BUILD PLAN

Status: PLANNED / READY_TO_BUILD  
Repository: magasincoffee/MAGASIN-CONTENT-MONEY-ENGINE  
Baseline main: `64a6246299e6387ad59f816c9f08e2f54aa8f051`  
Plan anchored at: 2026-09-24 00:24 +07:00  
Runtime relation: independent product; MAGASIN Supervisor/Work may be used to build/test it, but Affiliate Traffic Robot must run independently after deployment.

## V0 mission

Build the smallest end-to-end robot that can:

```text
FIND VIDEO
→ RANK
→ COLLECT/DOWNLOAD
→ LOCALIZE/EDIT
→ QUEUE
→ PUBLISH
→ VERIFY LIVE
```

Do not expand into dashboards, multi-network monetization, advanced analytics, paid traffic, or broad infrastructure before the end-to-end path passes.

## Hard principles

1. Five-Step: QUESTION → DELETE → SIMPLIFY → ACCELERATE → AUTOMATE.
2. Local-first / free-first.
3. Video/media bytes stay local or in approved media storage, not Git.
4. Git stores code, schemas, configs, tests, and sanitized evidence.
5. Publishing must be exact-once/reconciled to avoid duplicate posts.
6. Login credentials, OTP/MFA/CAPTCHA, KYC/tax, banking, destructive account actions, spend, and ambiguous legal/rights decisions remain Owner boundaries.
7. Collection for analysis is separate from publication authority.
8. Unknown rights never silently becomes publishable.

## V0 scope

Primary discovery source: Douyin.  
Secondary source: deferred until V0 proves value.  
Initial publishing target: ONE platform only.  
Media processing: Python + FFmpeg first.  
State: local SQLite/JSONL acceptable for V0.  
Paid traffic: disabled.  
Target daily volume after stabilization: 5–10 videos/day before scaling.

## Real-time execution plan

| Vietnam time | Task | Required output |
|---|---|---|
| 00:30–01:00 | Freeze baseline + audit existing runner/collector code | Reuse map, no direct-main development |
| 01:00–03:00 | AR-01 Trend Scanner V1 | Douyin candidate metadata collected automatically |
| 03:00–04:30 | AR-02 Viral Ranker V1 | Candidates scored/ranked automatically |
| 04:30–06:00 | AR-03 Media Collector V1 | Eligible media collected with source metadata |
| 06:00–09:00 | AR-04/05 Localizer + Video Editor V1 | 9:16 MP4 rendered automatically |
| 09:00–11:00 | Chinese speech → Vietnamese subtitle flow | Dialogue videos localized automatically |
| 11:00–13:00 | AR-06 Publish Queue V1 | READY_TO_PUBLISH queue + duplicate guard |
| 13:00–16:00 | AR-07 Publisher V1 for one platform | Automated upload/caption/publish path |
| 16:00–18:00 | Reconciliation + retry safety | Timeout/restart cannot blindly duplicate |
| 18:00–20:00 | AR-08 single-video E2E | discover → edit → publish → verify LIVE |
| 20:00–22:00 | E2E batch 3–5 videos | Repeatable batch proof |
| 22:00–00:30 | Fixes, tests, evidence, PR | V0 candidate ready for acceptance |

These are execution targets, not guarantees. External platform/login/CAPTCHA/policy changes may extend the schedule.

## Task sequence

### AR-01 — TREND_SCANNER
Goal:
- collect candidate video metadata;
- normalize platform, source id/url, creator, caption/hashtags, view/like/comment/share counts, published time, first/last seen.

DoD:
- at least 20 real candidates in a bounded smoke test;
- deterministic normalized schema;
- no manual candidate entry.

### AR-02 — VIRAL_RANKER
Initial HOT_SCORE inputs:
- view signal;
- comment signal;
- share signal;
- freshness;
- observed growth;
- Vietnam adaptability.

DoD:
- deterministic ranking;
- top-N selection without Owner hand-picking.

### AR-03 — MEDIA_COLLECTOR
Goal:
- collect/download source media for processing;
- retain source id/url and provenance;
- dedupe by source/content fingerprint.

DoD:
- repeat call does not duplicate the same source asset;
- failed downloads are retryable with bounded retry.

### AR-04 — LOCALIZER
Dialogue path:
```text
extract audio
→ Chinese speech-to-text
→ Vietnamese adaptation
→ subtitle file
```

No-dialogue path:
```text
skip ASR
→ Vietnamese hook/caption metadata
```

DoD:
- machine-readable transcript/subtitle artifact;
- no manual subtitle authoring required for the smoke test.

### AR-05 — VIDEO_EDITOR
V0 transform:
- normalize dimensions;
- 9:16 output;
- trim;
- subtitle burn-in;
- hook text;
- optional outro;
- audio normalization;
- H.264/AAC MP4.

DoD:
- valid playable output;
- rendering reproducible from job manifest;
- no GUI editor required.

### AR-06 — PUBLISH_QUEUE
Core states:
```text
DISCOVERED
SCORED
COLLECTED
RIGHTS_CHECK
LOCALIZED
RENDERED
READY_TO_PUBLISH
PUBLISHING
LIVE
WAIT_OWNER
FAILED_RETRYABLE
FAILED_TERMINAL
```

DoD:
- idempotency key persisted before external publish;
- one source/render cannot create blind duplicate publish jobs.

### AR-07 — PUBLISHER
V0:
- exactly one target platform;
- authorized logged-in account/session;
- upload;
- caption;
- publish;
- reconcile platform result.

DoD:
- save platform content id/url when available;
- ambiguous timeout requires reconciliation before retry;
- Owner gate for login/MFA/CAPTCHA/platform warnings.

### AR-08 — END-TO-END ACCEPTANCE
Required proof:
```text
source discovery
→ automatic ranking
→ collection
→ localization/edit
→ queue
→ publish
→ LIVE verification
```

Acceptance:
- 1 real video E2E PASS;
- then 3–5 video bounded batch PASS;
- sanitized evidence retained.

### AR-09 — AUTONOMOUS SCHEDULER
Only after AR-08 passes.

Initial cadence:
- scan periodically;
- rank after each scan;
- process approved queue;
- publish at configured times;
- reconcile outstanding jobs.

DoD:
- robot continues independently after Supervisor/Work is stopped;
- restart-safe local state.

## Proposed code layout

```text
04_ROBOT/
└── traffic_robot/
    ├── scanner/
    │   └── douyin_scanner.py
    ├── ranker/
    │   └── viral_ranker.py
    ├── collector/
    │   └── media_collector.py
    ├── localizer/
    │   ├── transcribe.py
    │   ├── zh_to_vi.py
    │   └── subtitles.py
    ├── editor/
    │   ├── ffmpeg_pipeline.py
    │   └── templates/
    ├── publisher/
    │   ├── queue.py
    │   ├── browser_publisher.py
    │   └── reconcile.py
    ├── state/
    │   └── jobs.sqlite
    ├── orchestrator.py
    └── tests/
```

## V0 technical targets

Single simple video:
- collection: 10–60 s typical;
- localization/edit/render: target 1–5 min depending on media and hardware;
- publish: target 0.5–2 min excluding external login/CAPTCHA gates.

Bounded batch target after stabilization:
- 5–10 videos/day fully automated;
- only scale beyond this after account health and pipeline stability are proven.

## Explicitly deferred

- Shopee product matching as a prerequisite for every traffic video;
- multi-platform publishing in V0;
- multi-China-platform crawler;
- dashboard;
- paid ads;
- 20–50 videos/day scale;
- advanced ML ranking;
- 24/7 production before AR-08 proves the basic loop.

## Acceptance rule

No task after AR-08 may be called production-ready merely because code exists.

Canonical V0 success means:

```text
A REAL VIDEO
was discovered automatically
→ selected automatically
→ processed automatically
→ published through an authorized path
→ verified LIVE
without manual editing/upload.
```
