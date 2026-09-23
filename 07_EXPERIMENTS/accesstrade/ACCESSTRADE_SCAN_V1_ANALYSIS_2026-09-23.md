# ACCESSTRADE Scan V1 Analysis — 2026-09-23

Source: Owner-provided sanitized Browser Explorer V1 output.

## Scan result

- Pages mapped: 20
- Navigation failures: 0
- Sensitive pages mapped structurally: 4
- Network endpoints observed: 159
- ACCESSTRADE API endpoints observed on `pub2-api.accesstrade.vn`: 54
- API methods observed: overwhelmingly GET; one POST observed at `/v1/product_link/`

## Proven money surfaces

### Campaign discovery
Observed API surface includes:

- `GET /v1/campaign/best_for_me`
- `GET /v1/campaign/check_aff`
- `GET /v1/campaign/detail`
- `GET /v1/campaign/similar`
- `GET /v2/campaign/collections`
- `GET /v2/campaign/seeding`

The campaign listing visibly surfaced multiple Shopee-related opportunities, including:

- Shopee Việt Nam Smartlink cho tất cả thiết bị
- Shopee KOL NEW
- OZOVN Shopee PUB
- KEYSHU Shopee PUB

Do not infer eligibility, payout, traffic permission or exact economics from listing text alone. Campaign detail/rules remain authoritative.

### Affiliate/product-link surface

Observed:

- `POST /v1/product_link/`

This proves a product-link API surface exists, but V1 intentionally stripped request body/query values and did not capture response bodies. Therefore request schema is still UNKNOWN and no automated deeplink creation is authorized yet.

### Click / traffic measurement

Observed:

- `GET /v1/click/total`
- `GET /v1/click/qualify-total`
- `GET /v1/click/histogram`
- `GET /v1/click/unique-active-user`
- `GET /v1/click/utm_agg`
- `GET /v1/click/top_browsers`
- `GET /v1/click/top_platform`

This is sufficient evidence that click and traffic telemetry can likely be read from a browser-authenticated adapter after exact request parameters are learned.

### Conversion / order measurement

Observed:

- `GET /v2/conversion/`
- `GET /v2/conversion/statistic`
- `GET /v2/statistics/conversion`
- `GET /v1/statistic/transactions_agg`

This is the critical source for ATTRIBUTED_ORDER / commission-state evidence.

### Campaign performance

Observed:

- `GET /v2/statistics/top-campaign`
- `GET /v1/statistic/top_merchants`
- `GET /v1/statistic/top_products`
- `GET /v1/statistic/utm_agg`

### Payment / cash evidence

Observed:

- `GET /v1/payment/cross_check`
- `GET /v1/payment/cross_check/income_campaigns_by_month`
- `GET /v1/payment/invoice_history`
- `GET /v1/payment/payment_rule`

These routes are sensitive and were intentionally not body-captured. They are candidates for a later read-only Cash Truth adapter with stricter redaction.

## Coverage limitation

This was the 20-page smoke scan, not a complete website crawl.

Important gap:
- `/tool` was not visited by this batch even though the Owner has confirmed the Tools UI exists.
- SPA navigation elements are not always anchor links.
- Exact request query keys/body schema/response JSON shape for `POST /v1/product_link/` remain unknown.

Therefore the system must not claim “whole site mapped” yet.

## Five-Step decision

### QUESTION
What additional evidence directly shortens time-to-cash?

Answer:
1. Full/deep money-surface coverage.
2. Exact sanitized schema for product-link generation.
3. Exact sanitized schema for click/conversion report filters.

### DELETE
Do not:
- reverse-engineer unrelated agency/referral features;
- automate payment mutations;
- automate campaign registration;
- scrape identity/profile bodies;
- build a generic browser agent.

### SIMPLIFY
Add:
1. explicit money/full seed presets to Browser Explorer;
2. a schema-only money-flow recorder attached to Owner Chrome.

### ACCELERATE
Owner demonstrates once:

```text
Shopee campaign
→ Create Link / Product Link
→ one normal affiliate link if Owner chooses
→ Click report
→ Conversion report
→ Campaign report
```

Recorder stores only field names/types and endpoint paths.

### AUTOMATE
Only after the above schema is captured and Brain verifies:
- campaign eligibility/rules;
- exact deeplink request schema;
- attribution/report semantics;
- no sensitive values are required in persisted config.

## Target V2 money path

```text
TREND PRODUCT
→ ACCESSTRADE CAMPAIGN MATCH
→ SHOPEE PRODUCT / SMARTLINK
→ AFFILIATE LINK
→ UTM/CONTENT ID
→ CLICK OBSERVED
→ ATTRIBUTED ORDER
→ COMMISSION STATE
→ PAYMENT / CASH TRUTH
```

Status: V1 scan PASS / full coverage PARTIAL / money adapter NOT YET AUTHORIZED.
