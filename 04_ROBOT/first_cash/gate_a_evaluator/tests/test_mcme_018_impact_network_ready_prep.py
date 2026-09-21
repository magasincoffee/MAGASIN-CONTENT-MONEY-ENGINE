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
    assert_impact_network_runtime_ready,
    impact_network_reconciliation_key,
)
from evaluator import EvidenceValidationError, evaluate


DOWNSTREAM_ITEMS = [
    ("merchant", "relationship"),
    ("geography", "us_allowed"),
    ("promotion", "pinterest_social_allowed"),
    ("promotion", "direct_link_allowed"),
    ("promotion", "deep_link_allowed"),
    ("tracking", "link_capability"),
    ("tracking", "attribution_subid_capability"),
    ("commission", "commissionable_action"),
    ("validation", "locking_rule"),
    ("validation", "reversal_return_rule"),
    ("payout", "threshold_cycle"),
    ("payout", "feasibility"),
    ("payout", "rail_type"),
    ("rights_disclosure", "creative_usage"),
    ("rights_disclosure", "affiliate_disclosure"),
]


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


def load_impact_network(candidate_slot="IMPACT-01"):
    with (FIXTURES / "full_verified_pass.json").open("r", encoding="utf-8") as handle:
        record = json.load(handle)
    record["candidate_slot"] = candidate_slot
    record["network"]["name"] = "impact.com"
    record["merchant"]["public_name"] = None
    record["merchant"]["program_public_identifier"] = None
    for group, field in DOWNSTREAM_ITEMS:
        set_unknown(record[group][field])
    return record


class MCME018ImpactNetworkReadyPrepTests(unittest.TestCase):
    def test_impact_candidate_bindings_are_valid(self):
        for slot in ("IMPACT-01", "IMPACT-02"):
            with self.subTest(slot=slot):
                result = evaluate(load_impact_network(slot), SCHEMA)
                self.assertEqual(result["candidate_slot"], slot)
                self.assertEqual(result["network"], "impact.com")
                self.assertEqual(result["state"], "NETWORK_READY")

    def test_cross_network_mixing_fails_closed(self):
        impact = load_impact_network()
        impact["network"]["name"] = "Awin"
        with self.assertRaises(EvidenceValidationError):
            evaluate(impact, SCHEMA)

        awin = load_impact_network()
        awin["candidate_slot"] = "AWIN-01"
        with self.assertRaises(EvidenceValidationError):
            evaluate(awin, SCHEMA)

    def test_runtime_guard_requires_brain_accepted_awin_exhaustion(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_network_runtime_ready(
                awin_bounded_path_brain_accepted_exhausted=False,
                mcme_016_runtime_result="MERCHANT_FAIL",
                mcme_017_real_sanitized_evidence_present=True,
            )

    def test_runtime_guard_requires_mcme016_terminal_merchant_fail(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_network_runtime_ready(
                awin_bounded_path_brain_accepted_exhausted=True,
                mcme_016_runtime_result="PASS-TO-PAYOUT-READINESS",
                mcme_017_real_sanitized_evidence_present=True,
            )

    def test_runtime_guard_requires_real_mcme017_evidence(self):
        with self.assertRaises(RuntimePrerequisiteError):
            assert_impact_network_runtime_ready(
                awin_bounded_path_brain_accepted_exhausted=True,
                mcme_016_runtime_result="MERCHANT_FAIL",
                mcme_017_real_sanitized_evidence_present=False,
            )

        assert_impact_network_runtime_ready(
            awin_bounded_path_brain_accepted_exhausted=True,
            mcme_016_runtime_result="MERCHANT_FAIL",
            mcme_017_real_sanitized_evidence_present=True,
        )

    def test_relationship_reconciliation_key_is_stable_and_network_scoped(self):
        ref = "https://www.pinterest.com/example-safe-property/"
        first = impact_network_reconciliation_key(ref)
        second = impact_network_reconciliation_key(f"  {ref}  ")
        other = impact_network_reconciliation_key(
            "https://www.pinterest.com/another-safe-property/"
        )

        self.assertEqual(first, second)
        self.assertNotEqual(first, other)
        self.assertIn("|impact.com|property-sha256:", first)
        with self.assertRaises(RuntimePrerequisiteError):
            impact_network_reconciliation_key("   ")

    def test_unknown_network_relationship_is_owner_action_required(self):
        record = load_impact_network()
        set_unknown(record["network"]["relationship"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "OWNER_ACTION_REQUIRED")
        self.assertNotEqual(result["state"], "PASS")
        self.assertNotIn("NETWORK_READY", result["transition_trace"])

    def test_pending_and_blocked_network_relationship_wait_owner(self):
        pending = load_impact_network()
        pending["network"]["relationship"]["value"] = "PENDING"
        pending_result = evaluate(pending, SCHEMA)
        self.assertEqual(pending_result["state"], "WAIT_OWNER")

        blocked = load_impact_network()
        blocked["network"]["relationship"].update(
            {
                "status": "BLOCKED",
                "confidence": "HIGH",
                "value": None,
                "source_reference_sanitized": None,
                "observed_at": None,
            }
        )
        blocked_result = evaluate(blocked, SCHEMA)
        self.assertEqual(blocked_result["state"], "WAIT_OWNER")

    def test_rejected_network_relationship_fails(self):
        record = load_impact_network()
        record["network"]["relationship"]["value"] = "REJECTED"

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["NETWORK_RELATIONSHIP_REJECTED"])

    def test_property_acceptance_unknown_is_not_network_ready(self):
        record = load_impact_network()
        set_unknown(record["property"]["network_property_accepted"])

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "OWNER_ACTION_REQUIRED")
        self.assertNotIn("NETWORK_READY", result["transition_trace"])

    def test_property_acceptance_false_fails_closed(self):
        record = load_impact_network()
        record["property"]["network_property_accepted"]["value"] = False

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["PROPERTY_NOT_ACCEPTED_BY_NETWORK"])

    def test_property_authorization_false_fails_closed(self):
        record = load_impact_network()
        record["property"]["authorized"]["value"] = False

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "FAIL")
        self.assertEqual(result["reasons"], ["PROPERTY_NOT_AUTHORIZED"])

    def test_active_accepted_network_reaches_only_network_ready(self):
        record = load_impact_network()

        result = evaluate(record, SCHEMA)

        self.assertEqual(result["state"], "NETWORK_READY")
        self.assertEqual(result["transition_trace"], ["NETWORK_READY"])
        self.assertEqual(result["reasons"], ["MERCHANT_CLASS_NOT_VERIFIED"])
        self.assertIsNone(record["merchant"]["public_name"])
        self.assertIsNone(record["merchant"]["program_public_identifier"])
        for group, field in DOWNSTREAM_ITEMS:
            self.assertEqual(record[group][field]["status"], "UNKNOWN")
            self.assertIsNone(record[group][field]["value"])

    def test_deterministic_replay_matches_twice(self):
        record = load_impact_network()

        first = evaluate(record, SCHEMA)
        second = evaluate(copy.deepcopy(record), SCHEMA)

        self.assertEqual(first, second)
        self.assertEqual(first["evaluation_id"], second["evaluation_id"])


if __name__ == "__main__":
    unittest.main()
