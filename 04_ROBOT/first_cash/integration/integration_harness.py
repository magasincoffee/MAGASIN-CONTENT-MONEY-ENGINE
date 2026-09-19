"""MCME-043 fixture-only composition helpers. No external calls or side effects."""
from __future__ import annotations
import copy, json, sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
GATE_DIR = REPO_ROOT / "04_ROBOT" / "first_cash" / "gate_a_evaluator"
PUBLISH_DIR = REPO_ROOT / "04_ROBOT" / "first_cash" / "publish_safety"
LAUNCH_DIR = REPO_ROOT / "04_ROBOT" / "first_cash" / "launch_gate"
CASH_DIR = REPO_ROOT / "06_METRICS" / "tools" / "cash_truth_ingest"
for p in (GATE_DIR, PUBLISH_DIR, LAUNCH_DIR, CASH_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from evaluator import evaluate as evaluate_gate_a
from launch_gate import evaluate as evaluate_launch, NOT_READY, READY
from publish_safety import PublishIntent, PublishSafetyMachine, LatchStore, MockBackend, MockReconciler, RECON_UNKNOWN
from cash_truth import CashTruthLedger

GATE_FIXTURE = GATE_DIR / "tests" / "fixtures" / "full_verified_pass.json"
CURRENT_LAUNCH_FIXTURE = LAUNCH_DIR / "tests" / "fixtures" / "current_realistic_l0.json"
READY_LAUNCH_FIXTURE = LAUNCH_DIR / "tests" / "fixtures" / "hypothetical_ready.json"
GATE_SCHEMA = REPO_ROOT / "07_EXPERIMENTS" / "gate_a" / "mcme_gate_a_evidence_v1.schema.json"
CASH_SCHEMA = REPO_ROOT / "06_METRICS" / "mcme_cash_truth_v1.schema.json"

PROVIDER_SPECIFIC_UNKNOWN = "PROVIDER_SPECIFIC_UNKNOWN"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def launch_item(value: Any, source: str) -> dict[str, Any]:
    return {"status": "VERIFIED", "value": value, "source_reference_sanitized": source}


def gate_a_to_launch_fields(evidence: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Map only facts Gate A actually proves; do not invent provider runtime details."""
    direct = evidence["promotion"]["direct_link_allowed"]["value"] is True
    deep = evidence["promotion"]["deep_link_allowed"]["value"] is True
    link_method = "DIRECT_AND_DEEP" if direct and deep else "DIRECT" if direct else "DEEP" if deep else None
    rel = evidence["merchant"]["relationship"]
    return {
        "state": result["state"],
        "merchant_public_identifier": evidence["merchant"]["public_name"],
        "program_public_identifier": evidence["merchant"]["program_public_identifier"],
        "relationship": launch_item(rel["value"] in {"APPROVED", "JOINED"}, rel["source_reference_sanitized"]),
        "us_allowed": launch_item(evidence["geography"]["us_allowed"]["value"], evidence["geography"]["us_allowed"]["source_reference_sanitized"]),
        "pinterest_social_allowed": launch_item(evidence["promotion"]["pinterest_social_allowed"]["value"], evidence["promotion"]["pinterest_social_allowed"]["source_reference_sanitized"]),
        "link_method": launch_item(link_method, "mapping:gate-a-link-permission"),
        "tracking_link_capability": launch_item(evidence["tracking"]["link_capability"]["value"], evidence["tracking"]["link_capability"]["source_reference_sanitized"]),
        "commissionable_action": launch_item(evidence["commission"]["commissionable_action"]["value"], evidence["commission"]["commissionable_action"]["source_reference_sanitized"]),
        "validation_locking": launch_item(evidence["validation"]["locking_rule"]["value"], evidence["validation"]["locking_rule"]["source_reference_sanitized"]),
        "reversal_return": launch_item(evidence["validation"]["reversal_return_rule"]["value"], evidence["validation"]["reversal_return_rule"]["source_reference_sanitized"]),
        "payout_threshold_cycle": launch_item(evidence["payout"]["threshold_cycle"]["value"], evidence["payout"]["threshold_cycle"]["source_reference_sanitized"]),
        "payout_feasibility": launch_item(evidence["payout"]["feasibility"]["value"], evidence["payout"]["feasibility"]["source_reference_sanitized"]),
        "rights_creative": launch_item(evidence["rights_disclosure"]["creative_usage"]["value"], evidence["rights_disclosure"]["creative_usage"]["source_reference_sanitized"]),
        "disclosure_requirements": launch_item(evidence["rights_disclosure"]["affiliate_disclosure"]["value"], evidence["rights_disclosure"]["affiliate_disclosure"]["source_reference_sanitized"]),
    }


def hypothetical_launch_from_gate_a() -> tuple[dict[str, Any], dict[str, Any]]:
    evidence = load_json(GATE_FIXTURE)
    result = evaluate_gate_a(evidence, GATE_SCHEMA)
    snapshot = load_json(READY_LAUNCH_FIXTURE)
    snapshot["gate_a"] = gate_a_to_launch_fields(evidence, result)
    return snapshot, result


def current_reality_result() -> dict[str, Any]:
    snapshot = load_json(CURRENT_LAUNCH_FIXTURE)
    return {
        "gate_a_state": snapshot["gate_a"]["state"],
        "launch": evaluate_launch(snapshot),
        "commercial_events_created": 0,
        "publish_invoked": False,
    }


def publish_intents(snapshot: dict[str, Any]) -> list[PublishIntent]:
    return [
        PublishIntent(
            snapshot["experiment_id"],
            pin["content_id"],
            pin["content_version"],
            pin["destination_version"],
        )
        for pin in snapshot["three_pin_package"]["pins"]
    ]


def base_event(event_type: str, event_id: str, *, content_id: str | None = None, pin_id: str | None = None,
               source_system: str = "AFFILIATE_NETWORK", source_type: str = "TRANSACTION_RECORD",
               source_record_id: str | None = None, network: str | None = "Awin", merchant: str | None = "EXAMPLE MERCHANT — NOT REAL",
               program_id: str | None = "EXAMPLE-PROGRAM", provider_state: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": "mcme.cash-truth-event.v1",
        "event_id": event_id,
        "event_type": event_type,
        "experiment_id": "EXAMPLE-NOT-REAL",
        "content_id": content_id,
        "pin_id": pin_id,
        "network": network,
        "merchant": merchant,
        "program_id_sanitized": program_id,
        "source": {
            "source_system": source_system,
            "source_type": source_type,
            "source_record_id_sanitized": source_record_id,
            "source_reference_sanitized": f"fixture:{event_id}",
            "provider_state_label_sanitized": provider_state,
        },
        "occurred_at": "2026-09-20T00:00:00+07:00",
        "observed_at": "2026-09-20T00:00:01+07:00",
        "evidence": {
            "status": "VERIFIED",
            "confidence": "HIGH",
            "evidence_reference_sanitized": "fixture:HYPOTHETICAL-TEST-ONLY",
            "notes_sanitized": "HYPOTHETICAL / TEST ONLY / NOT REAL ECONOMICS",
        },
        "idempotency": {
            "strategy": "PROVIDER_STABLE_ID",
            "key_sanitized": None,
            "provider_effective_at": None,
        },
    }


def hypothetical_cash_events(pin_id: str, content_id: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    pub = base_event("PIN_PUBLISHED", "E-PUB", content_id=content_id, pin_id=pin_id, source_system="PINTEREST", source_type="ACCOUNT_UI", source_record_id=pin_id, network=None, merchant=None, program_id=None)
    events.append(pub)
    out = base_event("OUTBOUND_CLICK_OBSERVED", "E-OUT", content_id=content_id, pin_id=pin_id, source_system="PINTEREST", source_type="EXPORT", source_record_id="PIN-OUT-1", network=None, merchant=None, program_id=None)
    out["metric"] = {"name": "OUTBOUND_CLICKS", "value": 1, "aggregation_mode": "INDIVIDUAL_EVENT"}
    events.append(out)
    net = base_event("NETWORK_CLICK_OBSERVED", "E-NET", content_id=content_id, pin_id=pin_id, source_record_id="NETCLICK-1")
    net["metric"] = {"name": "NETWORK_CLICKS", "value": 1, "aggregation_mode": "INDIVIDUAL_EVENT"}
    events.append(net)
    act = base_event("MERCHANT_ACTION_TRACKED", "E-ACT", content_id=content_id, pin_id=pin_id, source_record_id="ACTION-1", provider_state="TRACKED")
    events.append(act)
    state_map = [
        ("COMMISSION_PENDING", "E-PENDING", "PENDING", "2026-09-20T00:01:00+07:00"),
        ("COMMISSION_VALIDATED", "E-VALID", "VALIDATED", "2026-09-20T00:02:00+07:00"),
        ("COMMISSION_PAYABLE", "E-PAYABLE", "PAYABLE", "2026-09-20T00:03:00+07:00"),
    ]
    for typ, eid, state, effective in state_map:
        e = base_event(typ, eid, content_id=content_id, pin_id=pin_id, source_record_id="COMM-1", provider_state=state)
        e["canonical_money_state"] = state
        e["money"] = {"amount_decimal": "10.50", "currency": "USD"}
        e["idempotency"]["strategy"] = "PROVIDER_STATE_VERSION"
        e["idempotency"]["provider_effective_at"] = effective
        events.append(e)
    payout = base_event("PAYOUT_ISSUED", "E-PAYOUT", source_system="PAYOUT_PROVIDER", source_type="TRANSACTION_RECORD", source_record_id="PAYOUT-1", provider_state="ISSUED")
    payout["canonical_money_state"] = "PAYOUT_ISSUED"
    payout["money"] = {"amount_decimal": "10.50", "currency": "USD"}
    events.append(payout)
    return events


def reversal_event() -> dict[str, Any]:
    e = base_event("COMMISSION_REVERSED", "E-REV", source_record_id="COMM-1", provider_state="REVERSED")
    e["canonical_money_state"] = "REVERSED"
    e["money"] = {"amount_decimal": "-10.50", "currency": "USD"}
    e["idempotency"]["strategy"] = "PROVIDER_STATE_VERSION"
    e["idempotency"]["provider_effective_at"] = "2026-09-20T00:04:00+07:00"
    return e


def guarded_cash_event() -> dict[str, Any]:
    e = base_event("CASH_SETTLED", "E-CASH", source_system="OWNER_PAYOUT_RAIL", source_type="STATEMENT", source_record_id="SETTLE-1", network=None, merchant=None, program_id=None, provider_state="SETTLED")
    e["canonical_money_state"] = "CASH_SETTLED"
    e["money"] = {"amount_decimal": "10.50", "currency": "USD"}
    e["settlement"] = {
        "funds_actually_received": True,
        "owner_authorized_payout_rail": True,
        "reconciled_to_payout": True,
        "payout_source_record_id_sanitized": "PAYOUT-1",
        "settlement_reference_external": "PRIVATE_REF:TEST-ONLY-SETTLEMENT",
    }
    return e


def cross_contract_mapping() -> dict[str, str]:
    return {
        "gate_a_candidate_slot_to_launch": "candidate slot selects evaluated path; winning merchant/program public identifiers map to launch.gate_a identifiers",
        "gate_a_link_permissions_to_launch": "direct/deep verified permissions map to launch link_method; real link generation remains PROVIDER_SPECIFIC_UNKNOWN",
        "gate_a_rights_to_launch": "creative_usage -> rights_creative; affiliate_disclosure -> disclosure_requirements",
        "launch_content_to_publish": "experiment_id + content_id + content_version + destination_version -> PublishIntent/publish_key",
        "mock_pin_to_cash_truth": "mock published_id -> PIN_PUBLISHED.pin_id/source_record_id_sanitized in TEST ONLY flow",
        "network_source_to_cash_identity": "source_system + network + merchant + program + provider source_record_id + event type/state version",
        "private_refs_to_public": "raw private values stay local/private; public artifacts carry sanitized IDs or PRIVATE_REF placeholders",
        "real_attribution_subid_method": PROVIDER_SPECIFIC_UNKNOWN,
        "real_tracking_link_generation": PROVIDER_SPECIFIC_UNKNOWN,
        "real_pinterest_reconciliation_lookup": PROVIDER_SPECIFIC_UNKNOWN,
        "real_network_source_record_semantics": PROVIDER_SPECIFIC_UNKNOWN,
    }
