# BRAIN ↔ WORK PROTOCOL

## Brain responsibility

Brain decides the next highest-value bounded task after applying Five-Step.

A valid task must contain:
- task_id;
- objective;
- context;
- constraints;
- expected artifact/result;
- Definition of Done;
- test/evidence requirement;
- Owner/security boundary.

## Work responsibility

Work executes the task. Work must not invent a new strategic direction.

Work returns:
- status;
- what changed;
- evidence/tests;
- economics impact if relevant;
- risks/blockers;
- next facts Brain needs.

## Robot responsibility

Robot transports task/result, preserves lane/project identity and prevents duplicate side effects.

## Suggested machine directive

```text
<<<MCME_DIRECTIVE_V1>>>
{
  "action":"WORK",
  "task_id":"MCME-001",
  "instruction":"Self-contained bounded instruction"
}
<<<END_MCME_DIRECTIVE_V1>>>
```

Idle:

```text
<<<MCME_DIRECTIVE_V1>>>
{"action":"IDLE"}
<<<END_MCME_DIRECTIVE_V1>>>
```

## Task selection law

Brain prioritizes:

```text
Expected Cash Impact
× Probability of Learning/Success
÷ Time + Cost + Risk
```

with Owner/safety constraints as hard gates.

## Five-Step requirement

Every directive should make clear which current step is being applied:
QUESTION, DELETE, SIMPLIFY, ACCELERATE or AUTOMATE.

AUTOMATE tasks are invalid unless upstream economics are already proven.
