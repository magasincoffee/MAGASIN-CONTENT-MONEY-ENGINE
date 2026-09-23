# Traffic Robot V0

This directory is reserved for the first independent Affiliate Traffic Robot runtime.

Target loop:

```text
Douyin discovery
→ normalized metadata
→ viral ranking
→ media collection
→ rights/reuse state
→ Chinese/Vietnamese localization
→ FFmpeg render
→ publish queue
→ one-platform publisher
→ LIVE reconciliation
```

The runtime must remain independent from MAGASIN Supervisor after deployment. Supervisor/Work may build or test this code, but must not be a production dependency.

See:
- `00_PROJECT/AFFILIATE_TRAFFIC_ROBOT_V0_PLAN.md`
- `00_PROJECT/AFFILIATE_TRAFFIC_ROBOT_V0_PLAN.json`

Implementation starts at AR-01 and may not skip AR-08 end-to-end acceptance.
