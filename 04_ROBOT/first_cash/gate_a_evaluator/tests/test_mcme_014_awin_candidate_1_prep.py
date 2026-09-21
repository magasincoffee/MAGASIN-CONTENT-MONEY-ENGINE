from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
EVALUATOR_DIR = HERE.parents[1]
REPO_ROOT = HERE.parents[4]
FIXTURES = HERE.parent / "fixtures"
SCHEMA = REPO_ROOT / "07_EXPERIMENTS" / "gate_a" / "mcme_gate_a_evidence_v1.schema.json"

sys.path.insert(0, str(EVALUATOR_DIR))

from evaluator import evaluate


def load_base():
    with (FIXTURES / "full_verified_pass.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def set_unknown(item):
    item.update(
        {
            "status": "UNKNOWN",
            "confidence": "HIGH",
            "value": None,
            "source_reference_sanitized": None,
            "observed_at": None,
        }
    )


def set_blocked(item):
    item.update(
        {
            "status": "BLOCKED",
            "confidence": "HIGH",
            "value": None,
            "source_reference_sanitized": None,
            "observed_at": None,
        }
    )


class MCME014AwinCandidate1PrepTests(unittest.TestCase):
    def test_merchant_unknown_stays_network_ready(self):
        record = load_base()
        set_unknown(record["merchant"]["relationship"])
        set_unknown(record["geography"]["us_allowed"])
        set_unknown(record["promotion"]["pinterest_social_allowed"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "NETWORK_READY")
        self.assertEqual(result["reasons"], ["MERCHANT_CLASS_NOT_VERIFIED"])

    def test_merchant_pending_waits_owner(self):
        record = load_base()
        record["merchant"]["relationship"]["value"] = "PENDING"

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "WAIT_OWNER")
        self.assertEqual(result["reasons"], ["MERCHANT_RELATIONSHIP_PENDING"])

    def test_merchant_blocked_waits_owner(self):
        record = load_base()
        set_blocked(record["merchant"]["relationship"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "WAIT_OWNER")
        self.assertEqual(result["reasons"], ["MERCHANT_EVIDENCE_BLOCKED"])

    def test_merchant_rejected_fails(self):
        record = load_base()
        record["merchant"]["relationship"]["value"] = "REJECTED"

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["MERCHANT_RELATIONSHIP_REJECTED"])

    def test_explicit_critical_fail_fails(self):
        record = load_base()
        record["validation"]["locking_rule"].update(
            {
                "status": "FAIL",
                "confidence": "HIGH",
                "value": "TEST_ONLY_EXPLICIT_FAIL",
                "source_reference_sanitized": "fixture:critical-fail",
                "observed_at": "2026-09-20T00:00:00+07:00",
            }
        )

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["EXPLICIT_CRITICAL_FAIL"])

    def test_approved_missing_tracking_stops_at_merchant_ready(self):
        record = load_base()
        for group, field in [
            ("promotion", "direct_link_allowed"),
            ("promotion", "deep_link_allowed"),
            ("tracking", "link_capability"),
            ("tracking", "attribution_subid_capability"),
        ]:
            set_unknown(record[group][field])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "MERCHANT_READY")
        self.assertEqual(
            result["transition_trace"],
            ["NETWORK_READY", "MERCHANT_READY"],
        )

    def test_joined_missing_tracking_stops_at_merchant_ready(self):
        record = load_base()
        record["merchant"]["relationship"]["value"] = "JOINED"
        set_unknown(record["tracking"]["link_capability"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "MERCHANT_READY")

    def test_verified_geography_false_fails_closed(self):
        record = load_base()
        record["geography"]["us_allowed"]["value"] = False

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["US_GEOGRAPHY_NOT_ALLOWED"])

    def test_verified_pinterest_permission_false_fails_closed(self):
        record = load_base()
        record["promotion"]["pinterest_social_allowed"]["value"] = False

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["PINTEREST_SOCIAL_NOT_ALLOWED"])

    def test_no_allowed_link_method_fails_closed(self):
        record = load_base()
        record["promotion"]["direct_link_allowed"]["value"] = False
        record["promotion"]["deep_link_allowed"]["value"] = False

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["NO_ALLOWED_LINK_METHOD"])

    def test_tracking_link_false_fails_closed(self):
        record = load_base()
        record["tracking"]["link_capability"]["value"] = False

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["TRACKING_LINK_UNAVAILABLE"])

    def test_missing_validation_stops_at_tracking_ready(self):
        record = load_base()
        set_unknown(record["commission"]["commissionable_action"])
        set_unknown(record["validation"]["locking_rule"])
        set_unknown(record["validation"]["reversal_return_rule"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "TRACKING_READY")
        self.assertEqual(
            result["transition_trace"],
            ["NETWORK_READY", "MERCHANT_READY", "TRACKING_READY"],
        )

    def test_missing_payout_stops_at_validation_terms_ready(self):
        record = load_base()
        set_unknown(record["payout"]["threshold_cycle"])
        set_unknown(record["payout"]["feasibility"])
        set_unknown(record["payout"]["rail_type"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "VALIDATION_TERMS_READY")

    def test_payout_feasibility_false_fails_closed(self):
        record = load_base()
        record["payout"]["feasibility"]["value"] = False

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["PAYOUT_NOT_FEASIBLE"])

    def test_missing_rights_stops_at_payout_ready(self):
        record = load_base()
        set_unknown(record["rights_disclosure"]["creative_usage"])
        set_unknown(record["rights_disclosure"]["affiliate_disclosure"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "PAYOUT_READY")

    def test_complete_valid_classes_follow_full_canonical_trace(self):
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

    def test_replay_is_deterministic_and_idempotent(self):
        record = load_base()

        first = evaluate(record, SCHEMA)
        second = evaluate(copy.deepcopy(record), SCHEMA)

        self.assertEqual(first, second)
        self.assertEqual(first["evaluation_id"], second["evaluation_id"])


if __name__ == "__main__":
    unittest.main()
