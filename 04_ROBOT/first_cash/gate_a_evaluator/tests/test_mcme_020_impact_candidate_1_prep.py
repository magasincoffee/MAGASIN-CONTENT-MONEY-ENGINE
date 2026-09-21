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
    assert_impact_candidate_1_identity_reconciles,
    assert_impact_candidate_1_runtime_ready,
    impact_candidate_reconciliation_key,
)
from evaluator import EvidenceValidationError, evaluate


def load_impact01():
    with (FIXTURES / "full_verified_pass.json").open("r", encoding="utf-8") as handle:
        record = json.load(handle)
    record["candidate_slot"] = "IMPACT-01"
    record["network"]["name"] = "impact.com"
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


class MCME020ImpactCandidate1PrepTests(unittest.TestCase):
    def test_impact01_binding_is_valid(self):
        result = evaluate(load_impact01(), SCHEMA)
        self.assertEqual(result["candidate_slot"], "IMPACT-01")
        self.assertEqual(result["network"], "impact.com")

    def test_cross_network_mixing_fails_closed(self):
        record = load_impact01()
        record["network"]["name"] = "Awin"
        with self.assertRaises(EvidenceValidationError):
            evaluate(record, SCHEMA)

    def test_runtime_guard_requires_real_brain_accepted_mcme018_network_ready(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_candidate_1_runtime_ready(
                candidate_slot="IMPACT-01",
                network_name="impact.com",
                mcme_018_brain_accepted=False,
                mcme_018_runtime_result="NETWORK_READY",
                mcme_019_real_sanitized_evidence_present=True,
            )
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_candidate_1_runtime_ready(
                candidate_slot="IMPACT-01",
                network_name="impact.com",
                mcme_018_brain_accepted=True,
                mcme_018_runtime_result="PREPARED_ONLY",
                mcme_019_real_sanitized_evidence_present=True,
            )

    def test_runtime_guard_requires_real_mcme019_evidence(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_candidate_1_runtime_ready(
                candidate_slot="IMPACT-01",
                network_name="impact.com",
                mcme_018_brain_accepted=True,
                mcme_018_runtime_result="NETWORK_READY",
                mcme_019_real_sanitized_evidence_present=False,
            )

        assert_impact_candidate_1_runtime_ready(
            candidate_slot="IMPACT-01",
            network_name="impact.com",
            mcme_018_brain_accepted=True,
            mcme_018_runtime_result="NETWORK_READY",
            mcme_019_real_sanitized_evidence_present=True,
        )

    def test_merchant_unknown_stays_network_ready_non_terminal(self):
        record = load_impact01()
        set_unknown(record["merchant"]["relationship"])
        set_unknown(record["geography"]["us_allowed"])
        set_unknown(record["promotion"]["pinterest_social_allowed"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "NETWORK_READY")
        self.assertEqual(result["reasons"], ["MERCHANT_CLASS_NOT_VERIFIED"])

    def test_pending_and_blocked_wait_owner(self):
        pending = load_impact01()
        pending["merchant"]["relationship"]["value"] = "PENDING"
        self.assertEqual(evaluate(pending, SCHEMA)["state"], "WAIT_OWNER")

        blocked = load_impact01()
        set_blocked(blocked["merchant"]["relationship"])
        self.assertEqual(evaluate(blocked, SCHEMA)["state"], "WAIT_OWNER")

    def test_rejected_and_explicit_critical_fail(self):
        rejected = load_impact01()
        rejected["merchant"]["relationship"]["value"] = "REJECTED"
        rejected_result = evaluate(rejected, SCHEMA)
        self.assertEqual(rejected_result["state"], "FAIL")
        self.assertEqual(
            rejected_result["reasons"], ["MERCHANT_RELATIONSHIP_REJECTED"]
        )

        critical = load_impact01()
        critical["validation"]["locking_rule"].update(
            {
                "status": "FAIL",
                "confidence": "HIGH",
                "value": "TEST_ONLY_EXPLICIT_FAIL",
                "source_reference_sanitized": "fixture:mcme020-critical-fail",
                "observed_at": "2026-09-20T00:00:00+07:00",
            }
        )
        critical_result = evaluate(critical, SCHEMA)
        self.assertEqual(critical_result["state"], "FAIL")
        self.assertEqual(critical_result["reasons"], ["EXPLICIT_CRITICAL_FAIL"])

    def test_approved_or_joined_missing_downstream_stops_progressively(self):
        approved = load_impact01()
        set_unknown(approved["tracking"]["link_capability"])
        approved_result = evaluate(approved, SCHEMA)
        self.assertEqual(approved_result["state"], "MERCHANT_READY")
        self.assertEqual(
            approved_result["transition_trace"],
            ["NETWORK_READY", "MERCHANT_READY"],
        )

        joined = load_impact01()
        joined["merchant"]["relationship"]["value"] = "JOINED"
        set_unknown(joined["commission"]["commissionable_action"])
        joined_result = evaluate(joined, SCHEMA)
        self.assertEqual(joined_result["state"], "TRACKING_READY")
        self.assertEqual(
            joined_result["transition_trace"],
            ["NETWORK_READY", "MERCHANT_READY", "TRACKING_READY"],
        )

    def test_verified_critical_false_values_fail_closed(self):
        cases = [
            ("geography", "us_allowed", "US_GEOGRAPHY_NOT_ALLOWED"),
            ("promotion", "pinterest_social_allowed", "PINTEREST_SOCIAL_NOT_ALLOWED"),
            ("tracking", "link_capability", "TRACKING_LINK_UNAVAILABLE"),
            ("payout", "feasibility", "PAYOUT_NOT_FEASIBLE"),
        ]
        for group, field, reason in cases:
            with self.subTest(field=f"{group}.{field}"):
                record = load_impact01()
                record[group][field]["value"] = False
                result = evaluate(record, SCHEMA)
                self.assertEqual(result["state"], "FAIL")
                self.assertEqual(result["reasons"], [reason])

    def test_complete_verified_path_follows_canonical_trace(self):
        result = evaluate(load_impact01(), SCHEMA)
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

    def test_deterministic_replay_matches_twice(self):
        record = load_impact01()
        first = evaluate(record, SCHEMA)
        second = evaluate(copy.deepcopy(record), SCHEMA)
        self.assertEqual(first, second)
        self.assertEqual(first["evaluation_id"], second["evaluation_id"])

    def test_impact_candidate_reconciliation_keys_are_stable_and_distinct(self):
        first = impact_candidate_reconciliation_key("IMPACT-01")
        second = impact_candidate_reconciliation_key("IMPACT-01")
        candidate_2 = impact_candidate_reconciliation_key("IMPACT-02")
        self.assertEqual(first, "MCME-FIRST-CASH-V1|IMPACT-01")
        self.assertEqual(first, second)
        self.assertNotEqual(first, candidate_2)

    def test_impact03_is_forbidden(self):
        record = load_impact01()
        record["candidate_slot"] = "IMPACT-03"
        with self.assertRaises(EvidenceValidationError):
            evaluate(record, SCHEMA)
        with self.assertRaises(RuntimePrerequisiteError):
            impact_candidate_reconciliation_key("IMPACT-03")

    def test_mcme020_runtime_rejects_impact02(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_candidate_1_runtime_ready(
                candidate_slot="IMPACT-02",
                network_name="impact.com",
                mcme_018_brain_accepted=True,
                mcme_018_runtime_result="NETWORK_READY",
                mcme_019_real_sanitized_evidence_present=True,
            )

    def test_mcme020_runtime_rejects_wrong_network(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_candidate_1_runtime_ready(
                candidate_slot="IMPACT-01",
                network_name="Awin",
                mcme_018_brain_accepted=True,
                mcme_018_runtime_result="NETWORK_READY",
                mcme_019_real_sanitized_evidence_present=True,
            )

    def test_merchant_identity_binding_accepts_first_and_same_identity(self):
        assert_impact_candidate_1_identity_reconciles(
            bound_public_name=None,
            bound_program_public_identifier=None,
            incoming_public_name="TEST_ONLY_MERCHANT",
            incoming_program_public_identifier="TEST_ONLY_PROGRAM",
        )
        assert_impact_candidate_1_identity_reconciles(
            bound_public_name="TEST_ONLY_MERCHANT",
            bound_program_public_identifier="TEST_ONLY_PROGRAM",
            incoming_public_name="TEST_ONLY_MERCHANT",
            incoming_program_public_identifier="TEST_ONLY_PROGRAM",
        )

    def test_merchant_identity_conflict_fails_closed(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_candidate_1_identity_reconciles(
                bound_public_name="TEST_ONLY_MERCHANT",
                bound_program_public_identifier="TEST_ONLY_PROGRAM",
                incoming_public_name="DIFFERENT_TEST_ONLY_MERCHANT",
                incoming_program_public_identifier="DIFFERENT_TEST_ONLY_PROGRAM",
            )


if __name__ == "__main__":
    unittest.main()
