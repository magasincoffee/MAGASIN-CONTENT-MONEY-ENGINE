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

_IMPACT_RECONCILIATION_KEYS = {
    "IMPACT-01": "MCME-FIRST-CASH-V1|IMPACT-01",
    "IMPACT-02": "MCME-FIRST-CASH-V1|IMPACT-02",
}


def impact_candidate_reconciliation_key(candidate_slot: str) -> str:
    """Return the fixed bounded reconciliation key for an allowed impact.com merchant slot."""
    try:
        return _IMPACT_RECONCILIATION_KEYS[candidate_slot]
    except KeyError as exc:
        raise RuntimePrerequisiteError(
            f"unsupported bounded impact.com candidate slot: {candidate_slot}"
        ) from exc


def assert_impact_candidate_1_runtime_ready(
    *,
    candidate_slot: str,
    network_name: str,
    mcme_018_brain_accepted: bool,
    mcme_018_runtime_result: str | None,
    mcme_019_real_sanitized_evidence_present: bool,
) -> None:
    """Fail closed unless canonical IMPACT-01 merchant evaluation is unlocked."""
    if candidate_slot != "IMPACT-01":
        raise RuntimePrerequisiteError(
            "MCME-020 runtime is bound exclusively to candidate_slot IMPACT-01"
        )
    if network_name != "impact.com":
        raise RuntimePrerequisiteError(
            "MCME-020 runtime is bound exclusively to network.name impact.com"
        )
    if not mcme_018_brain_accepted:
        raise RuntimePrerequisiteError(
            "Brain-accepted real MCME-018 NETWORK_READY is required before MCME-020 runtime"
        )
    if mcme_018_runtime_result != "NETWORK_READY":
        raise RuntimePrerequisiteError(
            "MCME-018 accepted real runtime result must be NETWORK_READY before MCME-020 runtime"
        )
    if not mcme_019_real_sanitized_evidence_present:
        raise RuntimePrerequisiteError(
            "MCME-019 real sanitized IMPACT-01 merchant evidence is required before execution"
        )


def assert_impact_candidate_1_identity_reconciles(
    *,
    bound_public_name: str | None,
    bound_program_public_identifier: str | None,
    incoming_public_name: str,
    incoming_program_public_identifier: str,
) -> None:
    """Reject a silent merchant/program identity swap on the fixed IMPACT-01 slot."""
    incoming_name = incoming_public_name.strip() if isinstance(incoming_public_name, str) else ""
    incoming_program = (
        incoming_program_public_identifier.strip()
        if isinstance(incoming_program_public_identifier, str)
        else ""
    )
    if not incoming_name or not incoming_program:
        raise RuntimePrerequisiteError(
            "IMPACT-01 identity reconciliation requires non-empty sanitized merchant/program identity"
        )

    if bound_public_name is None and bound_program_public_identifier is None:
        return

    bound_name = bound_public_name.strip() if isinstance(bound_public_name, str) else ""
    bound_program = (
        bound_program_public_identifier.strip()
        if isinstance(bound_program_public_identifier, str)
        else ""
    )
    if not bound_name or not bound_program:
        raise RuntimePrerequisiteError(
            "existing IMPACT-01 identity binding is incomplete and requires Brain review"
        )
    if (bound_name, bound_program) != (incoming_name, incoming_program):
        raise RuntimePrerequisiteError(
            "IMPACT-01 merchant/program identity conflict requires Brain review"
        )

