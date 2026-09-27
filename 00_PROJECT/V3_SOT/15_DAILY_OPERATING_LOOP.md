# SOT — DAILY OPERATING LOOP

## Start of day

1. Read START_HERE.
2. Read PROJECT_STATE.
3. Read CURRENT_STATE.
4. Read TASK_QUEUE.
5. Read relevant subsystem SOT.
6. Inspect runtime/control evidence.
7. Identify highest dependency-correct bottleneck.

## Plan

Apply Five-Step.
Create one primary daily objective and only bounded parallel work that cannot invalidate it.

## Execute

Robot/Executor:
- performs safe internal work autonomously;
- records deterministic IDs;
- persists state before external side effects;
- reconciles side effects;
- captures evidence;
- stops only at true Owner boundaries.

## Review

Brain/Planner checks:
- DoD;
- evidence quality;
- money funnel movement;
- system reliability;
- policy/rights status;
- cost/time;
- what should be deleted.

Decision:
ACCEPT / REJECT-CORRECT / BLOCKED-OWNER / KILL / KEEP / REVISE / SCALE.

## End of day state update

Update:
- PROJECT_STATE current task/phase/evidence;
- CURRENT_STATE actual reality;
- TASK_QUEUE next dependency-correct task;
- experiment decision;
- Cash Truth events;
- Control status.

## Never

- mark planned work as observed;
- mark click as order;
- mark order as approved commission;
- mark payout as cash received;
- protect a weak strategy because code has already been built.
