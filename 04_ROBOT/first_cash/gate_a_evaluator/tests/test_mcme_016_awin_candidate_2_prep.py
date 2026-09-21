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

from candidate_runtime_guard import (
    RuntimePrerequisiteError,
    assert_awin_candidate_2_runtime_ready,
    awin_reconciliation_key,
)
from evaluator import EvidenceValidationError, evaluate


def load_awin02():
    with (FIXTURES / "full_verified_pass.json").open("r", encoding="utf-8") as handle:
        record = json.load(handle)
    record["candidate_slot"] = "AWIN-02"
    return record


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


class MCME016AwinCandidate2PrepTests(unittest.TestCase):
    def test_awin02_slot_binding_and_reconciliation_key_are_distinct(self):
        result = evaluate(load_awin02(), SCHEMA)
        self.assertEqual(result["candidate_slot"], "AWIN-02")
        self.assertEqual(result["network"], "Awin")
        self.assertEqual(awin_reconciliation_key("AWIN-02"), "MCME-FIRST-CASH-V1|AWIN-02")
        self.assertNotEqual(
            awin_reconciliation_key("AWIN-01"),
            awin_reconciliation_key("AWIN-02"),
        )

    def test_merchant_unknown_stays_network_ready(self):
        record = load_awin02()
        set_unknown(record["merchant"]["relationship"])
        set_unknown(record["geography"]["us_allowed"])
        set_unknown(record["promotion"]["pinterest_social_allowed"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "NETWORK_READY")
        self.assertEqual(result["reasons"], ["MERCHANT_CLASS_NOT_VERIFIED"])

    def test_pending_and_blocked_wait_owner(self):
        pending = load_awin02()
        pending["merchant"]["relationship"]["value"] = "PENDING"
        self.assertEqual(evaluate(pending, SCHEMA)["state"], "WAIT_OWNER")

        blocked = load_awin02()
        set_blocked(blocked["merchant"]["relationship"])
        self.assertEqual(evaluate(blocked, SCHEMA)["state"], "WAIT_OWNER")

    def test_rejected_and_explicit_critical_fail(self):
        rejected = load_awin02()
        rejected["merchant"]["relationship"]["value"] = "REJECTED"
        self.assertEqual(evaluate(rejected, SCHEMA)["state"], "FAIL")

        critical = load_awin02()
        critical["validation"]["locking_rule"].update(
            {
                "status": "FAIL",
                "confidence": "HIGH",
                "value": "TEST_ONLY_EXPLICIT_FAIL",
                "source_reference_sanitized": "fixture:mcme016-critical-fail",
                "observed_at": "2026-09-20T00:00:00+07:00",
            }
        )
        self.assertEqual(evaluate(critical, SCHEMA)["state"], "FAIL")

    def test_approved_or_joined_missing_downstream_stops_progressively(self):
        approved = load_awin02()
        set_unknown(approved["tracking"]["link_capability"])
        self.assertEqual(evaluate(approved, SCHEMA)["state"], "MERCHANT_READY")

        joined = load_awin02()
        joined["merchant"]["relationship"]["value"] = "JOINED"
        set_unknown(joined["commission"]["commissionable_action"])
        self.assertEqual(evaluate(joined, SCHEMA)["state"], "TRACKING_READY")

    def test_verified_critical_permissions_false_fail_closed(self):
        cases = [
            ("geography", "us_allowed", "US_GEOGRAPHY_NOT_ALLOWED"),
            ("promotion", "pinterest_social_allowed", "PINTEREST_SOCIAL_NOT_ALLOWED"),
            ("tracking", "link_capability", "TRACKING_LINK_UNAVAILABLE"),
            ("payout", "feasibility", "PAYOUT_NOT_FEASIBLE"),
        ]
        for group, field, reason in cases:
            with self.subTest(field=f"{group}.{field}"):
                record = load_awin02()
                record[group][field]["value"] = False
                result = evaluate(record, SCHEMA)
                self.assertEqual(result["state"], "FAIL")
                self.assertEqual(result["reasons"], [reason])

    def test_full_verified_path_and_deterministic_replay(self):
        record = load_awin02()
        first = evaluate(record, SCHEMA)
        second = evaluate(copy.deepcopy(record), SCHEMA)

        self.assertEqual(first, second)
        self.assertEqual(first["evaluation_id"], second["evaluation_id"])
        self.assertEqual(first["state"], "PASS")
        self.assertEqual(
            first["transition_trace"],
            [
                "NETWORK_READY",
                "MERCHANT_READY",
                "TRACKING_READY",
                "VALIDATION_TERMS_READY",
                "PAYOUT_READY",
                "RIGHTS_DISCLOSURE_READY",
            ],
        )

    def test_awin03_is_rejected_by_bounded_architecture_and_guard(self):
        record = load_awin02()
        record["candidate_slot"] = "AWIN-03"
        with self.assertRaises(EvidenceValidationError):
            evaluate(record, SCHEMA)
        with self.assertRaises(RuntimePrerequisiteError):
            awin_reconciliation_key("AWIN-03")

    def test_runtime_guard_requires_accepted_mcme014_merchant_fail(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_awin_candidate_2_runtime_ready(
                mcme_014_brain_accepted=False,
                mcme_014_runtime_result="MERCHANT_FAIL",
                mcme_015_real_sanitized_evidence_present=True,
            )
        with self.assertRaises(RuntimePrerequisiteError):
            assert_awin_candidate_2_runtime_ready(
                mcme_014_brain_accepted=True,
                mcme_014_runtime_result="PASS-TO-PAYOUT-READINESS",
                mcme_015_real_sanitized_evidence_present=True,
            )

    def test_runtime_guard_requires_real_mcme015_evidence(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_awin_candidate_2_runtime_ready(
                mcme_014_brain_accepted=True,
                mcme_014_runtime_result="MERCHANT_FAIL",
                mcme_015_real_sanitized_evidence_present=False,
            )

        assert_awin_candidate_2_runtime_ready(
            mcme_014_brain_accepted=True,
            mcme_014_runtime_result="MERCHANT_FAIL",
            mcme_015_real_sanitized_evidence_present=True,
        )


if __name__ == "__main__":
    unittest.main()
