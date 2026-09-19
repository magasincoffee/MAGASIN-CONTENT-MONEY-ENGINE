# MCME Gate A evaluator V1

Small, offline, fail-closed runtime package for future MCME-012/014/016/018/020/022/024/026/028.

It does **not** log in, call external services, create accounts, apply to merchants, handle KYC/payment, generate Pins, or publish.

## Contract

- Evidence schema: `07_EXPERIMENTS/gate_a/mcme_gate_a_evidence_v1.schema.json`
- Allowed candidate slots only: `AWIN-01`, `AWIN-02`, `IMPACT-01`, `IMPACT-02`, `AMAZON-01`
- `UNKNOWN` and `BLOCKED` never promote to `PASS`
- Public-program existence does not prove merchant relationship
- Pending relationships return `WAIT_OWNER`
- `PASS` requires every critical Gate A class to be verified and usable
- Evaluation is deterministic: identical sanitized evidence produces the same `evaluation_id`

## Offline test

From repository root:

```bash
python -m unittest discover -s 04_ROBOT/first_cash/gate_a_evaluator/tests -v
```

Runtime/test dependency: Python 3 + `jsonschema` (Draft 2020-12 support). No network access is used.

## Evaluate one sanitized record

```bash
python 04_ROBOT/first_cash/gate_a_evaluator/evaluator.py path/to/sanitized-evidence.json
```

Never place passwords, tokens, cookies, MFA/OTP, tax IDs, bank details, identity documents, raw private payout IDs, or sensitive tracking URLs in the evidence JSON.
