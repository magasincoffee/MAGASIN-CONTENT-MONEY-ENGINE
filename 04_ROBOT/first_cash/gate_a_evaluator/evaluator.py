"""Deterministic, fail-closed Gate A evaluator for MCME first-cash evidence.

No external calls. No account actions. No secret handling. Input must already be
sanitized and conform to mcme.gate-a-evidence.v1.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

SCHEMA_VERSION = "mcme.gate-a-evidence.v1"
ALLOWED_SLOTS = {
    "AWIN-01": "Awin",
    "AWIN-02": "Awin",
    "IMPACT-01": "impact.com",
    "IMPACT-02": "impact.com",
    "AMAZON-01": "Amazon Associates (conditional)",
}

READY_STATES = (
    "NETWORK_READY",
    "MERCHANT_READY",
    "TRACKING_READY",
    "VALIDATION_TERMS_READY",
    "PAYOUT_READY",
    "RIGHTS_DISCLOSURE_READY",
)

FORBIDDEN_KEY_FRAGMENTS = {
    "password",
    "passwd",
    "secret",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "session_cookie",
    "sessionid",
    "otp",
    "mfa",
    "recovery_code",
    "tax_id",
    "ssn",
    "tin",
    "bank_account",
    "account_number",
    "routing_number",
    "card_number",
    "identity_document",
    "private_tracking_token",
}

FORBIDDEN_VALUE_PATTERN = re.compile(
    r"(?i)(?:bearer\s+[A-Za-z0-9._~+/=-]{8,}|(?:password|passwd|token|api[_-]?key|"
    r"session(?:id)?|otp|mfa|tax[_-]?id|bank[_-]?account|routing[_-]?number|card[_-]?number)\s*[=:]\s*\S+)"
)


class GateAEvaluationError(ValueError):
    """Base class for deterministic Gate A validation errors."""


class EvidenceValidationError(GateAEvaluationError):
    """Schema or contract validation failed."""


class PrivacyValidationError(GateAEvaluationError):
    """Input appears to contain prohibited private/secret material."""


def default_schema_path() -> Path:
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "07_EXPERIMENTS" / "gate_a" / "mcme_gate_a_evidence_v1.schema.json"


def _walk(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, path + (str(key),))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from _walk(child, path + (str(idx),))


def assert_public_safe(record: dict[str, Any]) -> None:
    """Reject obvious secret/private material before evaluation.

    This is defense-in-depth, not a replacement for Owner-side sanitization.
    """

    for path, value in _walk(record):
        if path:
            key = path[-1].lower()
            if any(fragment in key for fragment in FORBIDDEN_KEY_FRAGMENTS):
                raise PrivacyValidationError(f"prohibited key at {'.'.join(path)}")
        if isinstance(value, str) and FORBIDDEN_VALUE_PATTERN.search(value):
            raise PrivacyValidationError(f"prohibited secret-like value at {'.'.join(path)}")


def load_schema(schema_path: Path | None = None) -> dict[str, Any]:
    path = schema_path or default_schema_path()
    with path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    return schema


def validate_record(record: dict[str, Any], schema_path: Path | None = None) -> None:
    assert_public_safe(record)
    schema = load_schema(schema_path)
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        ).iter_errors(record),
        key=lambda err: list(err.path),
    )
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, err.path)) or '<root>'}: {err.message}" for err in errors[:8]
        )
        raise EvidenceValidationError(details)

    slot = record["candidate_slot"]
    expected_network = ALLOWED_SLOTS.get(slot)
    if expected_network is None:
        raise EvidenceValidationError(f"candidate slot is outside bounded five-slot contract: {slot}")
    if record["network"]["name"] != expected_network:
        raise EvidenceValidationError(
            f"candidate slot {slot} is bound to network {expected_network}, got {record['network']['name']}"
        )


def canonical_digest(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _status(item: dict[str, Any]) -> str:
    return item["status"]


def _value(item: dict[str, Any]) -> Any:
    return item.get("value")


def _items(record: dict[str, Any], paths: list[tuple[str, str]]) -> list[dict[str, Any]]:
    return [record[group][name] for group, name in paths]


def _has_status(items: Iterable[dict[str, Any]], status: str) -> bool:
    return any(_status(item) == status for item in items)


def _all_verified(items: Iterable[dict[str, Any]]) -> bool:
    return all(_status(item) == "VERIFIED" for item in items)


def _result(record: dict[str, Any], state: str, trace: list[str], reasons: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "mcme.gate-a-evaluation.v1",
        "evaluation_id": canonical_digest(record),
        "candidate_slot": record["candidate_slot"],
        "network": record["network"]["name"],
        "state": state,
        "transition_trace": trace,
        "reasons": sorted(set(reasons)),
    }


def evaluate(record: dict[str, Any], schema_path: Path | None = None) -> dict[str, Any]:
    """Evaluate one sanitized candidate record deterministically and fail closed."""

    validate_record(record, schema_path)
    trace: list[str] = []

    critical_groups = [
        record["property"]["authorized"],
        record["property"]["network_property_accepted"],
        record["network"]["relationship"],
        record["merchant"]["relationship"],
        record["geography"]["us_allowed"],
        record["promotion"]["pinterest_social_allowed"],
        record["promotion"]["direct_link_allowed"],
        record["promotion"]["deep_link_allowed"],
        record["tracking"]["link_capability"],
        record["tracking"]["attribution_subid_capability"],
        record["commission"]["commissionable_action"],
        record["validation"]["locking_rule"],
        record["validation"]["reversal_return_rule"],
        record["payout"]["threshold_cycle"],
        record["payout"]["feasibility"],
        record["payout"]["rail_type"],
        record["rights_disclosure"]["creative_usage"],
        record["rights_disclosure"]["affiliate_disclosure"],
    ]
    if _has_status(critical_groups, "FAIL"):
        return _result(record, "FAIL", trace, ["EXPLICIT_CRITICAL_FAIL"])

    network_items = _items(
        record,
        [
            ("property", "authorized"),
            ("property", "network_property_accepted"),
            ("network", "relationship"),
        ],
    )
    if _has_status(network_items, "BLOCKED"):
        return _result(record, "WAIT_OWNER", trace, ["NETWORK_OR_PROPERTY_BLOCKED"])
    network_relationship = _value(record["network"]["relationship"])
    if _status(record["network"]["relationship"]) == "VERIFIED":
        if network_relationship == "PENDING":
            return _result(record, "WAIT_OWNER", trace, ["NETWORK_RELATIONSHIP_PENDING"])
        if network_relationship == "BLOCKED":
            return _result(record, "WAIT_OWNER", trace, ["NETWORK_RELATIONSHIP_BLOCKED"])
        if network_relationship == "REJECTED":
            return _result(record, "FAIL", trace, ["NETWORK_RELATIONSHIP_REJECTED"])
    if not _all_verified(network_items):
        return _result(record, "OWNER_ACTION_REQUIRED", trace, ["NETWORK_EVIDENCE_NOT_VERIFIED"])
    if _value(record["property"]["authorized"]) is not True:
        return _result(record, "FAIL", trace, ["PROPERTY_NOT_AUTHORIZED"])
    if _value(record["property"]["network_property_accepted"]) is not True:
        return _result(record, "FAIL", trace, ["PROPERTY_NOT_ACCEPTED_BY_NETWORK"])
    if network_relationship != "ACTIVE":
        return _result(record, "OWNER_ACTION_REQUIRED", trace, ["NETWORK_RELATIONSHIP_NOT_ACTIVE"])
    trace.append("NETWORK_READY")

    merchant_items = _items(
        record,
        [
            ("merchant", "relationship"),
            ("geography", "us_allowed"),
            ("promotion", "pinterest_social_allowed"),
        ],
    )
    if _has_status(merchant_items, "BLOCKED"):
        return _result(record, "WAIT_OWNER", trace, ["MERCHANT_EVIDENCE_BLOCKED"])
    merchant_relationship = _value(record["merchant"]["relationship"])
    if _status(record["merchant"]["relationship"]) == "VERIFIED":
        if merchant_relationship in {"PENDING", "PUBLIC_PROGRAM_ONLY", "BLOCKED"}:
            return _result(record, "WAIT_OWNER", trace, [f"MERCHANT_RELATIONSHIP_{merchant_relationship}"])
        if merchant_relationship == "REJECTED":
            return _result(record, "FAIL", trace, ["MERCHANT_RELATIONSHIP_REJECTED"])
    if not _all_verified(merchant_items):
        return _result(record, "NETWORK_READY", trace, ["MERCHANT_CLASS_NOT_VERIFIED"])
    if merchant_relationship not in {"APPROVED", "JOINED"}:
        return _result(record, "NETWORK_READY", trace, ["MERCHANT_RELATIONSHIP_NOT_USABLE"])
    if _value(record["geography"]["us_allowed"]) is not True:
        return _result(record, "FAIL", trace, ["US_GEOGRAPHY_NOT_ALLOWED"])
    if _value(record["promotion"]["pinterest_social_allowed"]) is not True:
        return _result(record, "FAIL", trace, ["PINTEREST_SOCIAL_NOT_ALLOWED"])
    trace.append("MERCHANT_READY")

    tracking_items = _items(
        record,
        [
            ("promotion", "direct_link_allowed"),
            ("promotion", "deep_link_allowed"),
            ("tracking", "link_capability"),
            ("tracking", "attribution_subid_capability"),
        ],
    )
    if _has_status(tracking_items, "BLOCKED"):
        return _result(record, "WAIT_OWNER", trace, ["TRACKING_EVIDENCE_BLOCKED"])
    if not _all_verified(tracking_items):
        return _result(record, "MERCHANT_READY", trace, ["TRACKING_CLASS_NOT_VERIFIED"])
    if _value(record["tracking"]["link_capability"]) is not True:
        return _result(record, "FAIL", trace, ["TRACKING_LINK_UNAVAILABLE"])
    if not (
        _value(record["promotion"]["direct_link_allowed"]) is True
        or _value(record["promotion"]["deep_link_allowed"]) is True
    ):
        return _result(record, "FAIL", trace, ["NO_ALLOWED_LINK_METHOD"])
    trace.append("TRACKING_READY")

    validation_items = _items(
        record,
        [
            ("commission", "commissionable_action"),
            ("validation", "locking_rule"),
            ("validation", "reversal_return_rule"),
        ],
    )
    if _has_status(validation_items, "BLOCKED"):
        return _result(record, "WAIT_OWNER", trace, ["VALIDATION_TERMS_BLOCKED"])
    if not _all_verified(validation_items):
        return _result(record, "TRACKING_READY", trace, ["VALIDATION_CLASS_NOT_VERIFIED"])
    if any(not isinstance(_value(item), str) or not _value(item).strip() for item in validation_items):
        return _result(record, "TRACKING_READY", trace, ["VALIDATION_VALUE_EMPTY"])
    trace.append("VALIDATION_TERMS_READY")

    payout_items = _items(
        record,
        [
            ("payout", "threshold_cycle"),
            ("payout", "feasibility"),
            ("payout", "rail_type"),
        ],
    )
    if _has_status(payout_items, "BLOCKED"):
        return _result(record, "WAIT_OWNER", trace, ["PAYOUT_EVIDENCE_BLOCKED"])
    if not _all_verified(payout_items):
        return _result(record, "VALIDATION_TERMS_READY", trace, ["PAYOUT_CLASS_NOT_VERIFIED"])
    if _value(record["payout"]["feasibility"]) is not True:
        return _result(record, "FAIL", trace, ["PAYOUT_NOT_FEASIBLE"])
    if not isinstance(_value(record["payout"]["threshold_cycle"]), str) or not _value(record["payout"]["threshold_cycle"]).strip():
        return _result(record, "VALIDATION_TERMS_READY", trace, ["PAYOUT_THRESHOLD_CYCLE_EMPTY"])
    if not isinstance(_value(record["payout"]["rail_type"]), str) or not _value(record["payout"]["rail_type"]).strip():
        return _result(record, "VALIDATION_TERMS_READY", trace, ["PAYOUT_RAIL_TYPE_EMPTY"])
    trace.append("PAYOUT_READY")

    rights_items = _items(
        record,
        [
            ("rights_disclosure", "creative_usage"),
            ("rights_disclosure", "affiliate_disclosure"),
        ],
    )
    if _has_status(rights_items, "BLOCKED"):
        return _result(record, "WAIT_OWNER", trace, ["RIGHTS_DISCLOSURE_BLOCKED"])
    if not _all_verified(rights_items):
        return _result(record, "PAYOUT_READY", trace, ["RIGHTS_DISCLOSURE_NOT_VERIFIED"])
    if any(not isinstance(_value(item), str) or not _value(item).strip() for item in rights_items):
        return _result(record, "PAYOUT_READY", trace, ["RIGHTS_DISCLOSURE_VALUE_EMPTY"])
    trace.append("RIGHTS_DISCLOSURE_READY")

    return _result(record, "PASS", trace, ["ALL_CRITICAL_GATE_A_CLASSES_VERIFIED"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate one sanitized MCME Gate A evidence JSON file.")
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--schema", type=Path, default=None)
    args = parser.parse_args()

    with args.evidence.open("r", encoding="utf-8") as handle:
        evidence = json.load(handle)
    print(json.dumps(evaluate(evidence, args.schema), indent=2, ensure_ascii=False))
