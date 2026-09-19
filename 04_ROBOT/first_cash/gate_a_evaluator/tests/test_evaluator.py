from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
EVALUATOR_DIR = HERE.parents[1]
REPO_ROOT = HERE.parents[4]
FIXTURES = HERE.parent / "fixtures"
SCHEMA = REPO_ROOT / "07_EXPERIMENTS" / "gate_a" / "mcme_gate_a_evidence_v1.schema.json"

sys.path.insert(0, str(EVALUATOR_DIR))

from evaluator import (
    EvidenceValidationError,
    PrivacyValidationError,
    evaluate,
    load_schema,
)


def load_base():
    with (FIXTURES / "full_verified_pass.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


class GateAEvaluatorTests(unittest.TestCase):
    def test_schema_is_valid_and_full_verified_passes(self):
        schema = load_schema(SCHEMA)
        Draft202012Validator.check_schema(schema)
        result = evaluate(load_base(), SCHEMA)
        self.assertEqual(result["state"], "PASS")
        self.assertEqual(
            result["transition_trace"],
            [
                "NETWORK_READY",
                "MERCHANT_READY",
                "TRACKING_READY",
                "VALIDATION_TERMS_READY",
                "PAYOUT_READY",
                "RIGHTS_DISCLOSURE_READY",
            ],
        )

    def test_unknown_critical_never_passes(self):
        record = load_base()
        record["promotion"]["pinterest_social_allowed"].update(
            {"status": "UNKNOWN", "confidence": "LOW", "value": None, "source_reference_sanitized": None, "observed_at": None}
        )
        result = evaluate(record, SCHEMA)
        self.assertNotEqual(result["state"], "PASS")
        self.assertEqual(result["state"], "NETWORK_READY")

    def test_blocked_critical_never_passes(self):
        record = load_base()
        record["payout"]["feasibility"].update(
            {"status": "BLOCKED", "confidence": "HIGH", "value": None, "source_reference_sanitized": None, "observed_at": None}
        )
        result = evaluate(record, SCHEMA)
        self.assertEqual(result["state"], "WAIT_OWNER")

    def test_explicit_fail_is_fail(self):
        record = load_base()
        record["geography"]["us_allowed"].update(
            {"status": "FAIL", "confidence": "HIGH", "value": False, "source_reference_sanitized": "fixture:explicit-fail", "observed_at": "2026-09-20T00:00:00+07:00"}
        )
        result = evaluate(record, SCHEMA)
        self.assertEqual(result["state"], "FAIL")

    def test_sixth_slot_is_rejected(self):
        record = load_base()
        record["candidate_slot"] = "AWIN-03"
        with self.assertRaises(EvidenceValidationError):
            evaluate(record, SCHEMA)

    def test_repeated_evidence_is_stable_and_idempotent(self):
        record = load_base()
        first = evaluate(record, SCHEMA)
        second = evaluate(copy.deepcopy(record), SCHEMA)
        self.assertEqual(first, second)
        self.assertEqual(first["evaluation_id"], second["evaluation_id"])

    def test_pending_relationship_not_merchant_ready(self):
        record = load_base()
        record["merchant"]["relationship"]["value"] = "PENDING"
        result = evaluate(record, SCHEMA)
        self.assertEqual(result["state"], "WAIT_OWNER")
        self.assertNotIn("MERCHANT_READY", result["transition_trace"])

    def test_public_program_only_is_not_relationship_proof(self):
        record = load_base()
        record["merchant"]["relationship"]["value"] = "PUBLIC_PROGRAM_ONLY"
        result = evaluate(record, SCHEMA)
        self.assertEqual(result["state"], "WAIT_OWNER")
        self.assertNotEqual(result["state"], "PASS")

    def test_private_secret_like_value_is_rejected(self):
        record = load_base()
        record["property"]["public_reference_sanitized"] = "https://example.invalid/?token=SHOULD_NOT_BE_HERE"
        with self.assertRaises(PrivacyValidationError):
            evaluate(record, SCHEMA)

    def test_slot_network_binding_is_enforced(self):
        record = load_base()
        record["network"]["name"] = "impact.com"
        with self.assertRaises(EvidenceValidationError):
            evaluate(record, SCHEMA)


if __name__ == "__main__":
    unittest.main()
