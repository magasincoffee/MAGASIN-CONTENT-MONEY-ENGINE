"""Pure runtime guards/reconciliation helpers for bounded Gate A candidates.

This module does not evaluate evidence and performs no external calls. Canonical Gate A
semantics remain in evaluator.py.
"""

from __future__ import annotations

import hashlib


class RuntimePrerequisiteError(ValueError):
    """Runtime evidence/prerequisite gate failed closed."""


_AWIN_RECONCILIATION_KEYS = {
    "AWIN-01": "MCME-FIRST-CASH-V1|AWIN-01",
    "AWIN-02": "MCME-FIRST-CASH-V1|AWIN-02",
}


def awin_reconciliation_key(candidate_slot: str) -> str:
    """Return the fixed bounded reconciliation key for an allowed Awin slot."""
    try:
        return _AWIN_RECONCILIATION_KEYS[candidate_slot]
    except KeyError as exc:
        raise RuntimePrerequisiteError(
            f"unsupported bounded Awin candidate slot: {candidate_slot}"
        ) from exc


def assert_awin_candidate_2_runtime_ready(
    *,
    mcme_014_brain_accepted: bool,
    mcme_014_runtime_result: str | None,
    mcme_015_real_sanitized_evidence_present: bool,
) -> None:
    """Fail closed unless both canonical AWIN-02 runtime prerequisites are proven."""
    if not mcme_014_brain_accepted:
        raise RuntimePrerequisiteError(
            "MCME-014 accepted runtime result is required before AWIN-02 execution"
        )
    if mcme_014_runtime_result != "MERCHANT_FAIL":
        raise RuntimePrerequisiteError(
            "MCME-014 accepted runtime result must be MERCHANT_FAIL before AWIN-02 execution"
        )
    if not mcme_015_real_sanitized_evidence_present:
        raise RuntimePrerequisiteError(
            "MCME-015 real sanitized AWIN-02 merchant evidence is required before execution"
        )


def impact_network_reconciliation_key(property_public_reference_sanitized: str) -> str:
    """Return one stable impact.com relationship key for the accepted sanitized property."""
    if not isinstance(property_public_reference_sanitized, str):
        raise RuntimePrerequisiteError(
            "impact.com reconciliation requires a sanitized property reference"
        )
    normalized = property_public_reference_sanitized.strip()
    if not normalized:
        raise RuntimePrerequisiteError(
            "impact.com reconciliation requires a non-empty sanitized property reference"
        )
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"MCME-FIRST-CASH-V1|impact.com|property-sha256:{digest}"


def assert_impact_network_runtime_ready(
    *,
    awin_bounded_path_brain_accepted_exhausted: bool,
    mcme_016_runtime_result: str | None,
    mcme_017_real_sanitized_evidence_present: bool,
) -> None:
    """Fail closed unless impact.com fallback runtime is canonically unlocked."""
    if not awin_bounded_path_brain_accepted_exhausted:
        raise RuntimePrerequisiteError(
            "Brain-accepted real Awin bounded-path exhaustion is required before impact.com runtime"
        )
    if mcme_016_runtime_result != "MERCHANT_FAIL":
        raise RuntimePrerequisiteError(
            "MCME-016 accepted real runtime result must be MERCHANT_FAIL before impact.com runtime"
        )
    if not mcme_017_real_sanitized_evidence_present:
        raise RuntimePrerequisiteError(
            "MCME-017 real sanitized impact.com network evidence is required before execution"
        )
