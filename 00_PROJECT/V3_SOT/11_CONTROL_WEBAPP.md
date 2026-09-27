# SOT — CONTROL WEBAPP

## Role

Control is a first-class operational interface, not a later vanity dashboard.

It answers:
- what is the system doing;
- why;
- what is winning/losing;
- where is the bottleneck;
- what money stage has been reached;
- what needs Owner action;
- what happens next.

## Required V0 panels

1. Mission / current phase / current task.
2. Robot health and worker state.
3. Owner blockers.
4. Trend opportunity queue.
5. Content production/publish queue.
6. Facebook performance summary.
7. Shopee commerce funnel.
8. Cash Truth stages.
9. Experiments and KILL/KEEP/SCALE decisions.
10. Event/error/retry feed.

## V1 enhancements

- lane portfolio;
- product economics;
- creative comparison;
- source health;
- payout reconciliation;
- task/source-of-truth links;
- strategy decision log.

## Control actions

Actions that mutate external systems must reflect authorization boundaries.

The UI never labels an action complete until runtime/provider evidence is reconciled.

## Data rule

Control reads canonical operational state; it must not become a separate conflicting source of truth.
