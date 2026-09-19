"""Deterministic MCME launch readiness + privacy gate. Offline only."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse, parse_qsl
from jsonschema import Draft202012Validator

READY = "READY"
NOT_READY = "NOT_READY"
CRITICAL_BAD = {"UNKNOWN", "BLOCKED", "FAIL"}
RISKY_QUERY_KEYS = {"token", "access_token", "refresh_token", "api_key", "apikey", "key", "secret", "signature", "sig", "auth", "session", "sessionid", "cookie", "code", "otp", "mfa"}
FORBIDDEN_KEY_FRAGMENTS = {
    "password", "passwd", "secret", "api_key", "apikey", "access_token", "refresh_token",
    "session_cookie", "sessionid", "cookie", "otp", "mfa", "recovery_code", "captcha",
    "tax_id", "ssn", "tin", "bank_account", "account_number", "routing_number", "card_number",
    "identity_document", "private_payout_id", "private_tracking_token", "browser_profile", "browser_session"
}
SECRET_VALUE = re.compile(r"(?i)(bearer\s+[A-Za-z0-9._~+/=-]{8,}|(?:password|passwd|token|api[_-]?key|secret|session(?:id)?|cookie|otp|mfa|tax[_-]?id|routing[_-]?number|card[_-]?number)\s*[=:]\s*\S+)")
PRIVATE_PATH = re.compile(r"(?i)(AppData[/\\].*(Chrome|Chromium|Edge)[/\\].*User Data|\.config[/\\](google-chrome|chromium)|[/\\](Cookies|Session Storage|Local Storage)[/\\]?)")

class LaunchGateError(ValueError): pass
class SchemaError(LaunchGateError): pass
class PrivacyLeakError(LaunchGateError): pass

def default_schema_path() -> Path:
    return Path(__file__).resolve().with_name("launch_readiness.schema.json")

def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def _walk(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, path + (str(key),))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from _walk(child, path + (str(idx),))

def privacy_scan(record: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    for path, value in _walk(record):
        dotted = ".".join(path) or "<root>"
        if path:
            key = path[-1].lower()
            if any(key == fragment or key.startswith(fragment + "_") or key.endswith("_" + fragment) for fragment in FORBIDDEN_KEY_FRAGMENTS):
                findings.append(f"FORBIDDEN_KEY:{dotted}")
        if not isinstance(value, str):
            continue
        if SECRET_VALUE.search(value):
            findings.append(f"SECRET_LIKE_VALUE:{dotted}")
        if PRIVATE_PATH.search(value):
            findings.append(f"PRIVATE_BROWSER_PATH:{dotted}")
        parsed = urlparse(value)
        if parsed.scheme in {"http", "https"} and parsed.query:
            risky = sorted({k.lower() for k, _ in parse_qsl(parsed.query, keep_blank_values=True)} & RISKY_QUERY_KEYS)
            if risky:
                findings.append(f"SENSITIVE_URL_QUERY:{dotted}:{','.join(risky)}")
    return sorted(set(findings))

def validate(record: dict[str, Any], schema_path: Path | None = None) -> None:
    findings = privacy_scan(record)
    if findings:
        raise PrivacyLeakError("; ".join(findings))
    path = schema_path or default_schema_path()
    with path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
    if errors:
        raise SchemaError("; ".join(f"{'.'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors[:12]))

def _verified_true(item: dict[str, Any]) -> bool:
    return item["status"] == "VERIFIED" and item.get("value") is True

def _verified_nonempty(item: dict[str, Any]) -> bool:
    return item["status"] == "VERIFIED" and isinstance(item.get("value"), str) and bool(item["value"].strip())

def evaluate(record: dict[str, Any], schema_path: Path | None = None) -> dict[str, Any]:
    validate(record, schema_path)
    reasons: list[str] = []
    gate = record["gate_a"]
    if gate["state"] != "PASS": reasons.append(f"GATE_A_NOT_PASS:{gate['state']}")
    if not gate.get("merchant_public_identifier"): reasons.append("MERCHANT_IDENTIFIER_MISSING")
    if not gate.get("program_public_identifier"): reasons.append("PROGRAM_IDENTIFIER_MISSING")

    bool_checks = [
        ("MERCHANT_RELATIONSHIP", gate["relationship"]),
        ("US_ALLOWED", gate["us_allowed"]),
        ("PINTEREST_SOCIAL_ALLOWED", gate["pinterest_social_allowed"]),
        ("TRACKING_LINK_CAPABILITY", gate["tracking_link_capability"]),
        ("PAYOUT_FEASIBILITY", gate["payout_feasibility"]),
    ]
    for name, item in bool_checks:
        if not _verified_true(item): reasons.append(f"{name}_NOT_VERIFIED_TRUE:{item['status']}")

    text_checks = [
        ("LINK_METHOD", gate["link_method"]),
        ("COMMISSIONABLE_ACTION", gate["commissionable_action"]),
        ("VALIDATION_LOCKING", gate["validation_locking"]),
        ("REVERSAL_RETURN", gate["reversal_return"]),
        ("PAYOUT_THRESHOLD_CYCLE", gate["payout_threshold_cycle"]),
        ("RIGHTS_CREATIVE", gate["rights_creative"]),
        ("DISCLOSURE_REQUIREMENTS", gate["disclosure_requirements"]),
    ]
    for name, item in text_checks:
        if not _verified_nonempty(item): reasons.append(f"{name}_NOT_VERIFIED_NONEMPTY:{item['status']}")
    if gate["link_method"].get("value") not in {"DIRECT", "DEEP", "DIRECT_AND_DEEP"}:
        reasons.append("LINK_METHOD_NOT_ALLOWED")

    pins = record["three_pin_package"]["pins"]
    if len(pins) != 3: reasons.append(f"PIN_COUNT_NOT_3:{len(pins)}")
    ids = [pin["content_id"] for pin in pins]
    if len(ids) != len(set(ids)): reasons.append("DUPLICATE_CONTENT_ID")
    for idx, pin in enumerate(pins, 1):
        prefix = f"PIN_{idx}"
        if pin["width_px"] * 3 != pin["height_px"] * 2: reasons.append(f"{prefix}_NOT_2_BY_3")
        if not _verified_true(pin["original_right_safe"]): reasons.append(f"{prefix}_RIGHTS_NOT_VERIFIED")
        if not _verified_nonempty(pin["attribution_method"]): reasons.append(f"{prefix}_ATTRIBUTION_NOT_VERIFIED")
        if not _verified_true(pin["qa"]): reasons.append(f"{prefix}_QA_NOT_PASS")
        for field in ("output_reference", "disclosure_ref", "destination_link_ref", "content_version", "destination_version"):
            if not isinstance(pin.get(field), str) or not pin[field].strip(): reasons.append(f"{prefix}_{field.upper()}_MISSING")

    obs = record["observation"]
    for name in ("window_locked", "no_artificial_clicks", "no_test_purchase"):
        if not _verified_true(obs[name]): reasons.append(f"OBS_{name.upper()}_NOT_VERIFIED_TRUE:{obs[name]['status']}")
    if not obs.get("window_reference"): reasons.append("OBS_WINDOW_REFERENCE_MISSING")
    if not _verified_nonempty(obs["measurement_source_plan"]): reasons.append(f"OBS_MEASUREMENT_PLAN_NOT_VERIFIED:{obs['measurement_source_plan']['status']}")

    ps = record["publish_safety"]
    for name in ("deterministic_key_ready", "persisted_latch_private_boundary", "reconciliation_before_retry", "bounded_retry_ready", "auth_block_ready"):
        if not _verified_true(ps[name]): reasons.append(f"PUBLISH_{name.upper()}_NOT_READY:{ps[name]['status']}")

    cash = record["cash_truth"]
    for name in ("schema_validator_ready", "local_private_jsonl_ready", "append_only_replay_ready", "dedupe_ready", "cash_settled_guard_ready", "privacy_boundary_ready"):
        if not _verified_true(cash[name]): reasons.append(f"CASH_{name.upper()}_NOT_READY:{cash[name]['status']}")

    auth = record["auth_browser"]["future_authorized_prerequisite"]
    if not _verified_true(auth): reasons.append(f"AUTH_BROWSER_NOT_READY:{auth['status']}")
    side = record["side_effect_authorization"]
    if not _verified_true(side): reasons.append(f"SIDE_EFFECT_AUTHORIZATION_NOT_READY:{side['status']}")

    result = READY if not reasons else NOT_READY
    return {
        "schema_version": "mcme.launch-readiness-evaluation.v1",
        "evaluation_id": digest(record),
        "result": result,
        "reasons": sorted(set(reasons)),
        "ready_semantics": "READY means mechanical prerequisites are satisfied; it does not execute or independently authorize publishing.",
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    with args.snapshot.open("r", encoding="utf-8") as handle:
        snapshot = json.load(handle)
    print(json.dumps(evaluate(snapshot), indent=2, ensure_ascii=False))
