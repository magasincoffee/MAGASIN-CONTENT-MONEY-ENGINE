# MAGASIN CONTENT MONEY ENGINE — ARCHITECTURE V1

Status: OWNER APPROVED
Date: 2026-09-19

## Mission

Build a globally scalable, policy-compliant, autonomous Content-to-Cash operating system that can run continuously and optimize for real net cash.

## System topology

```text
GLOBAL SIGNALS
     ↓
01 OPPORTUNITY ENGINE
     ↓
02 MARKET INTELLIGENCE
     ↓
03 RIGHTS / POLICY GATE
     ↓
04 CONTENT INTELLIGENCE
     ↓
05 SCRIPT + LOCALIZATION
     ↓
06 VOICE ENGINE (SaydiVoice provider first)
     ↓
07 VIDEO COMPOSER
     ↓
08 DISTRIBUTION ENGINE
     ↓
09 MONETIZATION ENGINE
     ↓
10 PROFIT & CASH ENGINE
     ↓
11 LEARNING ENGINE
     └──────────────→ BRAIN
```

## Responsibilities

### Owner
Authority for:
- platform/account creation;
- credentials, MFA, CAPTCHA;
- tax/KYC;
- payment and banking;
- legal/rights ambiguity;
- capital allocation above configured limits;
- destructive or irreversible account actions.

### Brain
Responsible for:
- strategy;
- market selection;
- niche selection;
- monetization hypothesis;
- experiment design;
- KPI interpretation;
- task priority;
- KEEP / KILL / SCALE decisions.

### Work
Executes one bounded, self-contained task at a time.

### Robot
Responsible for:
- transport;
- scheduling;
- persisted operational state;
- exact-once/idempotent dispatch where possible;
- bounded retries;
- recovery;
- monitoring;
- approved automated execution.

Robot does not own business strategy.

## Core rule

Content is not the product objective.

```text
CONTENT → ATTENTION → INTENT → TRANSACTION → CASH
```

A view without a monetization hypothesis is not sufficient reason to produce a video.

## Global-first design

The project is not Vietnam-only.

Market selection is dynamic and must consider:
- platform monetization availability;
- audience purchasing power;
- advertiser demand;
- affiliate program depth;
- e-commerce maturity;
- language/localization cost;
- competition;
- content supply;
- policy risk;
- payout feasibility;
- time-to-first-cash.

## Provider boundaries

SaydiVoice is a Voice Provider, not the business core.

```text
Content Factory
   ↓
Voice Engine
   ├── SaydiVoiceProvider
   └── future providers
```

The same rule applies to video sources, publishing platforms, analytics sources and affiliate networks.

## Non-negotiable invariants

1. Five-Step precedes automation.
2. Optimize for net cash, not view count.
3. No pure reupload business model.
4. Rights/policy gate runs before publication.
5. One source of truth for economic metrics.
6. Every production side effect should be idempotent or reconciled.
7. Retry loops are bounded.
8. Unknown safety/account/payment states fail closed.
9. Real experiments precede scaling.
10. Losing experiments are deleted quickly.
