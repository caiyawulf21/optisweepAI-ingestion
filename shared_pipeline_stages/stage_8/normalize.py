from __future__ import annotations

import re
from typing import Any

from shared_pipeline_stages.stage_8.capability_derivation import (
    capability_domain_adjustment,
    derive_retrieval_request,
    runbook_derived_capabilities,
)
from shared_pipeline_stages.stage_8.link_scoring import (
    anchor_overlap,
    boost_combined_score,
    build_retrieval_query_text,
    capability_tag_overlap,
    normalize_placeholder_text,
    node_allows_active_agv_error_sql,
    node_expects_capabilities,
    node_expects_surfaces,
    node_is_check_phase,
    node_is_site_interview,
    node_is_site_interview_only,
    node_is_site_history_branch,
    node_is_escalation_handoff_only,
    node_is_symptom_pattern_confirmation,
    node_check_text,
    node_mentions_grid_entry,
    node_mentions_motionless_floor,
    node_needs_agv_fleet_domain,
    node_needs_hospital_flow_check,
    node_needs_isolation_or_removal,
    node_needs_pairing_validation,
    node_needs_roster_mapping_check,
    node_needs_sequence_backfill_check,
    node_preferred_audience,
    rank_matches_for_node,
    runbook_access_surfaces,
    runbook_as_match,
    runbook_audience_roles,
    runbook_capability_tags,
    runbook_is_active_agv_error_sql,
    runbook_is_agv_isolation_or_removal,
    runbook_is_bump_exception_reference,
    runbook_is_bump_fault_recovery,
    runbook_is_fleet_rms_status_check,
    runbook_is_agv_fleet_related,
    runbook_is_generic_agv_removal,
    runbook_is_hospital_ui_reference,
    runbook_is_motionless_floor_removal,
    runbook_is_unrelated_equipment,
    runbook_is_recovery_prep,
    runbook_is_status_check,
    runbook_is_wcs_sql_diagnostic_state,
    runbook_match_text,
    runbook_supports_symptom_corroboration,
    runbook_is_wrong_domain_for_node,
    text_contains_incident_specific_detail,
    intent_mismatch_gaps,
    unresolved_catalog_gaps,
    INTENT_OVERRIDE_MARGIN,
    DOMAIN_ANCHORS,
    USE_CAPABILITY_TAG_CONSTRAINTS,
)
from shared_pipeline_stages.stage_8.schemas import FinalizedNode, RunbookSearchMatch

MAX_RUNBOOKS_PER_NODE = 3
MIN_RETRIEVAL_FLOOR = 0.28
HIGH_CONFIDENCE_SCORE = 0.48
MEDIUM_CONFIDENCE_SCORE = 0.38
ANCHOR_MEDIUM_OVERLAP = 0.18
ANCHOR_HIGH_OVERLAP = 0.28

CONFIDENCE_RANK = {"unresolved": 0, "low": 1, "medium": 2, "high": 3}

DIAGNOSTIC_NODE_TYPES = {"diagnostic_decision", "branching_condition", "validation_gate"}
OUTCOME_NODE_TYPES = DIAGNOSTIC_NODE_TYPES

PROCEDURE_TYPE_ALLOWED: dict[str, set[str]] = {
    "diagnostic_decision": {"diagnostic", "reference", "monitoring"},
    "branching_condition": {"diagnostic", "reference", "monitoring"},
    "validation_gate": {"diagnostic", "monitoring", "reference"},
    "procedure_reference": {"diagnostic", "reference", "monitoring", "operation", "recovery"},
    "escalation_gate": {"reference", "diagnostic", "monitoring", "operation"},
    "recovery_phase_marker": {"reference", "diagnostic", "monitoring", "operation", "recovery"},
}

PROCEDURE_TYPE_BLOCKED: dict[str, set[str]] = {
    "diagnostic_decision": {"recovery"},
    "branching_condition": {"recovery"},
    "validation_gate": set(),
    "procedure_reference": set(),
    "escalation_gate": set(),
    "recovery_phase_marker": set(),
}

COMPOUND_PLACEHOLDER_PATTERN = re.compile(
    r"\b(then also|as well as|both .+ and|;\s|\. then\b|\band then\b)",
    re.IGNORECASE,
)

SECONDARY_RUNBOOK_MIN_BOOSTED = 0.42
SECONDARY_RUNBOOK_MIN_ANCHOR_OVERLAP = 0.15
MAX_ALTERNATE_RUNBOOKS = 2
SEVERE_GAP_CONFIDENCE_CAP = "low"
SURFACE_COVERAGE_PRIORITY = (
    "wcs_sql",
    "wcs_api",
    "event_viewer",
    "rms_ui",
    "hospital_hmi",
    "tipper_hmi",
)
SURFACE_COVERAGE_SYNTHETIC_SCORE = 0.30
SURFACE_COVERAGE_RELATED_CAPABILITIES: dict[str, frozenset[str]] = {
    "device_roster_state": frozenset({"device_roster_state", "zone_config_state"}),
    "zone_config_state": frozenset({"zone_config_state", "device_roster_state"}),
    "agv_active_errors": frozenset({"agv_active_errors"}),
    "fleet_system_status": frozenset({"fleet_system_status", "wcs_service_health", "sort_lifecycle_state"}),
    "wcs_service_health": frozenset({"wcs_service_health", "fleet_system_status"}),
    "sort_lifecycle_state": frozenset({"sort_lifecycle_state", "fleet_system_status"}),
    "robot_command_or_task_state": frozenset({"robot_command_or_task_state"}),
    "robot_dwell_or_shutdown_staging": frozenset({"robot_dwell_or_shutdown_staging"}),
}


def runbook_exact_fit_gaps(
    node: dict[str, Any],
    runbook: dict[str, Any] | None,
    *,
    match: RunbookSearchMatch | None = None,
) -> list[str]:
    if not isinstance(runbook, dict):
        return ["Runbook is not present in the canonical catalog."]
    node_text = node_check_text(node).lower()
    runbook_text = " ".join(
        [
            str(runbook.get("title") or ""),
            str(runbook.get("summary") or ""),
            str(runbook.get("purpose") or ""),
            str(runbook.get("when_to_use") or ""),
            " ".join(str(item) for item in runbook.get("not_for") or []),
            " ".join(
                str(step.get(key) or "")
                for step in runbook.get("steps") or []
                if isinstance(step, dict)
                for key in ("title", "purpose", "instruction", "expected_result", "failure_condition")
            ),
        ]
    ).lower()
    gaps: list[str] = []
    node_type = str(node.get("node_type") or "")
    rb_type = str(runbook.get("procedure_type") or "").lower()
    if (
        node_type in DIAGNOSTIC_NODE_TYPES
        and str(node.get("ontology_contract_status") or "") == "missing"
    ):
        gaps.append("Node is missing its ontology capability contract.")
    if not procedure_type_compatible(node_type, rb_type):
        gaps.append(f"Node type '{node_type}' is incompatible with procedure type '{rb_type}'.")
    if node_type in DIAGNOSTIC_NODE_TYPES and rb_type in {"recovery", "operation"}:
        gaps.append("Diagnostic node requires an evidence-collection procedure, not a state-changing procedure.")
    if node_is_site_interview_only(node):
        gaps.append("This node requires site confirmation and cannot be satisfied by a catalog procedure.")
    if _runbook_trigger_is_unestablished(node_text, runbook_text):
        gaps.append("Runbook trigger or incident condition is not established by the node.")
    if _runbook_requires_unstated_safety(node, runbook, node_text, runbook_text=runbook_text):
        gaps.append("Runbook safety precondition is not established by the node.")
    expected_surfaces = node_expects_surfaces(node)
    selected_surface = str(node.get("primary_surface") or "").strip()
    if selected_surface:
        # A selected surface is the preferred path, not the only valid path.
        # Ontology contracts may authorize a complementary diagnostic surface,
        # such as Ignition gateway health beside a WCS API check.
        expected_surfaces |= _surface_ids_from_text(selected_surface) or {selected_surface}
    runbook_surfaces = runbook_access_surfaces(runbook)
    if (
        expected_surfaces
        and runbook_surfaces
        and not expected_surfaces & runbook_surfaces
        and not _allows_conditional_l2_evidence(node, runbook)
    ):
        gaps.append("Runbook surface does not match the selected support surface.")
    expected_roles = node_preferred_audience(node)
    runbook_roles = runbook_audience_roles(runbook)
    if (
        expected_roles
        and runbook_roles
        and not expected_roles & runbook_roles
        and not _allows_conditional_l2_evidence(node, runbook)
    ):
        gaps.append("Executing role is not authorized by the node/runbook role contract.")
    if match is not None:
        gaps.extend(intent_mismatch_gaps(node, match, runbook))
    gaps.extend(_ontology_contract_gaps(node, runbook))
    if node_type in DIAGNOSTIC_NODE_TYPES and rb_type == "diagnostic":
        if node_expects_capabilities(node) & runbook_capability_tags(runbook):
            gaps = [
                gap.replace("Missing corroboration", "Optional corroboration")
                for gap in gaps
            ]
    return list(dict.fromkeys(gap for gap in gaps if gap))


def _ontology_contract_gaps(
    node: dict[str, Any],
    runbook: dict[str, Any],
) -> list[str]:
    contracts = [
        item for item in node.get("ontology_capabilities") or [] if isinstance(item, dict)
    ]
    if not contracts:
        return []
    node_capabilities = {
        _normalize_contract_capability_id(item.get("id") or item.get("capability"))
        for item in contracts
        if _normalize_contract_capability_id(item.get("id") or item.get("capability"))
    }
    runbook_capabilities = runbook_capability_tags(runbook)
    gaps: list[str] = []
    if node_capabilities and runbook_capabilities and not node_capabilities & runbook_capabilities:
        gaps.append("Runbook does not match the ontology capability contract.")
    for contract in contracts:
        support_contract = contract.get("support_contract")
        if not isinstance(support_contract, dict):
            continue
        forbidden = {
            str(item).strip()
            for item in support_contract.get("forbidden_capabilities") or []
            if str(item).strip()
        }
        forbidden_overlap = forbidden & runbook_capabilities
        if forbidden_overlap:
            gaps.append(
                "Runbook capability is forbidden by the ontology contract: "
                + ", ".join(sorted(forbidden_overlap))
            )
        allowed_surfaces = {
            str(item).strip()
            for item in (
                support_contract.get("diagnostic_surfaces")
                or support_contract.get("control_surfaces")
                or []
            )
            if str(item).strip()
        }
        runbook_surfaces = runbook_access_surfaces(runbook)
        if allowed_surfaces and runbook_surfaces and not allowed_surfaces & runbook_surfaces:
            gaps.append("Runbook surface is outside the ontology contract.")
    return gaps


def _normalize_contract_capability_id(value: Any) -> str:
    normalized = str(value or "").strip()
    return normalized.split(":", 1)[1] if normalized.startswith("capability:") else normalized


def _allows_conditional_l2_evidence(
    node: dict[str, Any],
    runbook: dict[str, Any],
) -> bool:
    """Permit explicitly conditional, read-only L2 evidence beside an L1 path."""
    if str(node.get("node_type") or "") not in DIAGNOSTIC_NODE_TYPES:
        return False
    if str(runbook.get("procedure_type") or "").lower() != "diagnostic":
        return False
    if "wcs_sql" not in runbook_access_surfaces(runbook):
        return False
    runbook_roles = runbook_audience_roles(runbook)
    if not runbook_roles or not runbook_roles <= {"L2_support", "L3_support", "L4_support", "L2_L3_support"}:
        return False
    text = " ".join(
        [
            node_check_text(node),
            *[str(item) for item in node.get("inconclusive_indicators") or []],
            *[str(item) for item in node.get("evidence_required") or []],
        ]
    ).lower()
    return bool(
        re.search(
            r"\b(where|when|if)\s+available\b|\bsupport role\b|"
            r"\bsystem\s+active[- ]error(?:s)?\b",
            text,
        )
    )


# Structural/schema facts: a runbook literally cannot satisfy these (wrong
# procedure type for the node's schema; no catalog procedure can substitute
# for a pure site-interview step). These remain true hard filters -- this is
# not the RAG-vs-domain-knowledge tension the soft-scoring rework addresses.
HARD_STRUCTURAL_GAP_MARKERS = (
    "incompatible with procedure type",
    "state-changing procedure",
    "site confirmation",
)

# Domain-knowledge judgment calls: these used to also hard-drop the candidate,
# but they are inferences from text/ontology matching (not schema facts), so
# they now cost a penalty (EXACT_FIT_GAP_PENALTY) instead of eliminating the
# candidate outright -- a strong enough semantic match can still overcome one.
SOFT_EXACT_FIT_GAP_MARKERS = (
    "trigger or incident condition",
    "safety precondition",
    "surface does not match",
    "executing role is not authorized",
    "runbook does not match the ontology capability contract",
    "runbook capability is forbidden",
    "runbook surface is outside the ontology contract",
    "wrong catalog family",
)

# Same magnitude as capability_derivation.PRIMARY_EXCLUSION_PENALTY -- these
# are comparably strong domain-conflict signals.
EXACT_FIT_GAP_PENALTY = -0.35


def has_structural_gap(gaps: list[str]) -> bool:
    """True hard filter: schema-level incompatibility, not a domain-rule call."""
    return any(any(marker in gap.lower() for marker in HARD_STRUCTURAL_GAP_MARKERS) for gap in gaps)


def exact_fit_gap_penalty(gaps: list[str]) -> float:
    """Score penalty for the domain-knowledge-inference gap markers."""
    has_soft_gap = any(any(marker in gap.lower() for marker in SOFT_EXACT_FIT_GAP_MARKERS) for gap in gaps)
    return EXACT_FIT_GAP_PENALTY if has_soft_gap else 0.0


def _has_hard_exact_fit_gap(gaps: list[str]) -> bool:
    """Deprecated: use has_structural_gap() (hard) + exact_fit_gap_penalty()
    (soft) instead. Kept temporarily for any lingering internal callers during
    the soft-scoring migration; treats both marker tiers as hard, matching the
    old pre-migration behavior exactly, so any remaining caller does not
    silently change behavior until it is migrated."""
    return has_structural_gap(gaps) or bool(exact_fit_gap_penalty(gaps))


# Floor on the SUM of all domain-rule penalties for one candidate (capability
# domain adjustment + intent domain penalty + evidence domain penalty +
# exact-fit-gap penalty). Without a floor, multiple rules firing on the same
# candidate could compound to zero out even a very strong raw semantic score;
# this keeps one strong rule (e.g. -0.35) able to dominate a normal
# same-domain score gap, while preventing runaway compounding.
MAX_DOMAIN_PENALTY = -0.45


def total_domain_penalty(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
) -> tuple[float, list[str]]:
    """Unified domain-rule score adjustment for one candidate against one
    node: sums capability_domain_adjustment + intent_domain_penalty +
    evidence_domain_penalty + exact_fit_gap_penalty, floored at
    MAX_DOMAIN_PENALTY. This is the single function score_candidate()-style
    callers should use rather than calling the four sources individually.
    """
    retrieval_request = derive_retrieval_request(node)
    cap_penalty, cap_reason = capability_domain_adjustment(retrieval_request, runbook)
    intent_penalty, intent_reasons = intent_domain_penalty(node, match, runbook)
    evidence_penalty, evidence_reasons = evidence_domain_penalty(node, match, runbook)
    gap_penalty = exact_fit_gap_penalty(runbook_exact_fit_gaps(node, runbook, match=match))
    total = max(cap_penalty + intent_penalty + evidence_penalty + gap_penalty, MAX_DOMAIN_PENALTY)
    reasons = [r for r in ([cap_reason] if cap_reason else []) + intent_reasons + evidence_reasons if r]
    if gap_penalty:
        reasons.append("exact-fit gap")
    return total, reasons


def _surface_ids_from_text(text: str) -> set[str]:
    # Compound fields like "RMS/WCS/API" or "Event Viewer+Ignition Gateway" join
    # multiple surface names with punctuation rather than spaces. Normalize those
    # separators to spaces so each surface's alias markers can match individually
    # instead of only matching a single, fully space-separated surface phrase.
    lowered = re.sub(r"[/+,;|]", " ", str(text or "").lower())
    aliases: dict[str, tuple[str, ...]] = {
        "wcs_sql": ("wcs_sql", "ssms", "sql", "database"),
        "wcs_api": ("wcs_api", "wcs api", "api dog", "apidog", "getagvstatuses"),
        "event_viewer": ("event_viewer", "event viewer", "windows services", "services.msc", "windows_services"),
        "ignition_gateway": ("ignition_gateway", "ignition gateway", "systems overview"),
        "rms_ui": ("rms_ui", "rms ui", "rms"),
        "aveva_hmi": ("aveva_hmi", "aveva"),
        "hospital_hmi": ("hospital_hmi", "hospital hmi", "hospital lane"),
        "tipper_hmi": ("tipper_hmi", "webvisu", "visu", "tipper hmi"),
        "physical_floor": ("physical_floor", "physical floor", "e-stop", "estop"),
        "site_interview": ("site_interview", "site interview", "site observation"),
    }
    return {
        surface
        for surface, markers in aliases.items()
        if any(marker in lowered for marker in markers)
    }


def _runbook_trigger_is_unestablished(node_text: str, runbook_text: str) -> bool:
    if re.search(r"\bbump\b|21057|21060", runbook_text) and not re.search(
        r"\bbump\b|21057|21060", node_text
    ):
        return True
    if re.search(r"lost task|lost-task", runbook_text) and re.search(r"\brms restart|\brestart rms", runbook_text):
        if not re.search(r"lost task|lost-task", node_text) or not re.search(
            r"\brms restart|\brestart rms", node_text
        ):
            return True
    if re.search(r"\badd\s+(?:an?\s+)?agv\b|\badd\s+(?:an?\s+)?robot\b", runbook_text):
        if re.search(r"disconnected tote|service reset|after service recovery", node_text) and not re.search(
            r"\badd\s+(?:an?\s+)?agv\b|\badd\s+(?:an?\s+)?robot\b", node_text
        ):
            return True
    if re.search(r"\bignition\b.{0,40}\brestart\b|\brestart\b.{0,40}\bignition\b", runbook_text):
        if not re.search(r"\bignition\b|\bgateway\b", node_text) or not re.search(
            r"\brestart\b|\breset\b", node_text
        ):
            return True
    if re.search(r"\bservice reset\b|\brestart optisweep\b", runbook_text) and re.search(
        r"\bagv\b|\brobot\b", node_text
    ) and re.search(r"after (?:the )?service recovery|state correction", node_text):
        return True
    return False


def _runbook_requires_unstated_safety(
    node: dict[str, Any],
    runbook: dict[str, Any],
    node_text: str,
    *,
    runbook_text: str | None = None,
) -> bool:
    if str(runbook.get("procedure_type") or "").lower() not in {"recovery", "operation"}:
        return False
    runbook_text = (runbook_text or node_check_text(runbook)).lower()
    is_service_restart = bool(
        re.search(r"\b(restart|reset|recycle)\b", runbook_text)
        and re.search(r"\b(optisweep|ignition|windows service|service|gateway|getagvstatuses)\b", runbook_text)
    )
    if (
        is_service_restart
        and re.search(r"\b(service|gateway|ignition|optisweep|api)\b", node_text)
        and re.search(r"\b(diagnos\w*|abnormal|unhealthy|not respond|nonresponsive|no response)\b", node_text)
    ):
        return False
    prerequisites = runbook.get("prerequisites") if isinstance(runbook.get("prerequisites"), dict) else {}
    safety_text = " ".join(
        str(item)
        for item in (
            runbook.get("safety_notes") or [],
            prerequisites.get("system_preconditions") or [],
        )
    ).lower()
    if re.search(r"\bestop\b|\bE-stop\b", safety_text) and not re.search(r"\bestop\b|\be-stop\b", node_text):
        return True
    if re.search(r"\bloto\b|lockout|tagout", safety_text) and not re.search(r"\bloto\b|lockout|tagout", node_text):
        return True
    if runbook.get("requires_loto") is True and not re.search(r"\bloto\b|lockout|tagout", node_text):
        return True
    if is_service_restart:
        prerequisite_text = " ".join(
            str(item)
            for item in (
                node.get("prerequisites") or [],
                node.get("safety_checks") or [],
            )
        ).lower()
        if not re.search(r"\b(health|diagnos|healthy|abnormal|service status)\b", prerequisite_text + " " + node_text):
            return True
    if re.search(r"\b(agv|robot|tote|task)\b", runbook_text) and re.search(
        r"\b(service|ignition|gateway)\b.{0,40}\b(restart|reset|recover)\b", node_text
    ):
        return True
    return False


def reconcile_link_confidence(
    *,
    llm_confidence: str | None,
    retrieval_score: float | None,
    boosted_score: float | None = None,
    node: dict[str, Any] | None = None,
    match: RunbookSearchMatch | None = None,
    runbook: dict[str, Any] | None = None,
    link_rank: int = 1,
    type_compatible: bool = True,
) -> str:
    effective_score = boosted_score if boosted_score is not None else (retrieval_score or 0.0)
    score_confidence = confidence_for_score(effective_score)
    if (
        node
        and match
        and runbook
        and node_needs_roster_mapping_check(node)
        and runbook_is_fleet_rms_status_check(runbook, match)
        and score_confidence == "unresolved"
        and effective_score >= 0.20
    ):
        score_confidence = "low"
    if (
        node
        and match
        and runbook
        and score_confidence == "unresolved"
        and effective_score >= 0.08
        and str(node.get("primary_surface") or "").lower().find("wcs_sql") >= 0
        and "wcs_sql" in runbook_access_surfaces(runbook)
        and type_compatible
    ):
        # An explicitly requested WCS/SSMS surface is meaningful evidence even
        # when the node wording is broad and lexical retrieval is sparse.
        score_confidence = "low"
    if (
        node
        and match
        and runbook
        and node_is_symptom_pattern_confirmation(node)
        and runbook_supports_symptom_corroboration(node, runbook, match)
        and score_confidence == "unresolved"
        and effective_score >= 0.20
    ):
        score_confidence = "low"
    llm_value = str(llm_confidence or "").strip().lower()
    if llm_value not in CONFIDENCE_RANK:
        llm_value = score_confidence

    overlap = 0.0
    if node and match:
        node_text = build_retrieval_query_text(node)
        overlap = anchor_overlap(node_text, runbook_match_text(match, runbook))

    elevated = score_confidence
    if link_rank == 1 and type_compatible:
        if overlap >= ANCHOR_HIGH_OVERLAP or effective_score >= HIGH_CONFIDENCE_SCORE:
            elevated = "high"
        elif overlap >= ANCHOR_MEDIUM_OVERLAP or effective_score >= MEDIUM_CONFIDENCE_SCORE or match and match.jaccard_score >= 0.20:
            elevated = "medium"

    if llm_value == "high" and link_rank == 1 and type_compatible and elevated != "unresolved":
        elevated = "high"
    if llm_value == "medium" and CONFIDENCE_RANK[elevated] < CONFIDENCE_RANK["medium"]:
        elevated = "medium"

    result = elevated if CONFIDENCE_RANK[elevated] >= CONFIDENCE_RANK[llm_value] else llm_value
    return _cap_confidence_from_gaps(result, node=node, match=match, runbook=runbook, link_rank=link_rank)


def evaluate_link_confidence(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    *,
    runbook: dict[str, Any] | None = None,
    llm_confidence: str | None = None,
    link_rank: int = 1,
) -> tuple[str, float, list[str]]:
    node_type = str(node.get("node_type") or "")
    type_ok = procedure_type_compatible(node_type, match.procedure_type)
    node_text = build_retrieval_query_text(node)
    domain_penalty, domain_reasons = total_domain_penalty(node, match, runbook)
    boosted = boost_combined_score(
        match.combined_score,
        node=node,
        node_text=node_text,
        match=match,
        runbook=runbook,
        procedure_type_compatible=type_ok,
        domain_penalty=domain_penalty,
    )
    confidence = reconcile_link_confidence(
        llm_confidence=llm_confidence,
        retrieval_score=match.combined_score,
        boosted_score=boosted,
        node=node,
        match=match,
        runbook=runbook,
        link_rank=link_rank,
        type_compatible=type_ok,
    )
    gaps = _match_gaps(
        node,
        match,
        confidence,
        overlap=anchor_overlap(node_text, runbook_match_text(match, runbook)),
        runbook=runbook,
    )
    gaps.extend(domain_reasons)
    gaps = _dedupe_gaps(gaps)
    confidence = _cap_confidence_from_gaps(confidence, gaps=gaps, link_rank=link_rank)
    if not type_ok:
        gaps.append(f"Procedure type '{match.procedure_type}' is not ideal for node type '{node_type}'.")
        if CONFIDENCE_RANK[confidence] > CONFIDENCE_RANK["low"]:
            confidence = "low"
    return confidence, boosted, gaps


def confidence_for_score(score: float) -> str:
    if score >= HIGH_CONFIDENCE_SCORE:
        return "high"
    if score >= MEDIUM_CONFIDENCE_SCORE:
        return "medium"
    if score >= MIN_RETRIEVAL_FLOOR:
        return "low"
    return "unresolved"


def procedure_type_compatible(node_type: str, procedure_type: str) -> bool:
    normalized_node = str(node_type or "").strip()
    normalized_type = str(procedure_type or "").strip().lower()
    if not normalized_type:
        return True
    blocked = PROCEDURE_TYPE_BLOCKED.get(normalized_node, set())
    if normalized_type in blocked:
        return False
    allowed = PROCEDURE_TYPE_ALLOWED.get(normalized_node)
    if allowed is None:
        return True
    return normalized_type in allowed


def filter_compatible_matches(node: dict[str, Any], matches: list[RunbookSearchMatch]) -> list[RunbookSearchMatch]:
    node_type = str(node.get("node_type") or "")
    return [
        match
        for match in matches
        if procedure_type_compatible(node_type, match.procedure_type)
    ]


def intent_domain_penalty(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
) -> tuple[float, list[str]]:
    """Domain-rule score adjustment for one candidate against one node.

    Mirrors every condition that used to hard-drop a candidate in the former
    filter_intent_compatible_matches -- but accumulates a penalty and a reason
    list instead of dropping it. Multiple simultaneous domain-rule violations
    sum (a candidate wrong on several axes is a worse fit than one wrong on
    one axis), then the caller (score_candidate via evaluate_link_confidence)
    applies the shared MAX_DOMAIN_PENALTY floor across all domain-penalty
    sources so compounding rules cannot alone zero out a very strong raw
    score. The soft exact-fit-gap check (runbook_exact_fit_gaps) is scored
    separately via exact_fit_gap_penalty -- not duplicated here.
    """
    penalty = 0.0
    reasons: list[str] = []
    node_type = str(node.get("node_type") or "")

    def _add(amount: float, reason: str) -> None:
        nonlocal penalty
        penalty += amount
        reasons.append(reason)

    if node_is_check_phase(node) and runbook_is_recovery_prep(runbook, match) and not node_mentions_grid_entry(node):
        _add(-0.30, "recovery-prep runbook on check-only node")
    if node_is_check_phase(node) and node_needs_roster_mapping_check(node) and runbook_is_bump_exception_reference(runbook, match):
        _add(-0.30, "bump-exception runbook does not corroborate roster/mapping")
    if node_is_check_phase(node) and node_needs_roster_mapping_check(node) and runbook_is_hospital_ui_reference(runbook, match):
        _add(-0.25, "hospital-UI runbook does not corroborate roster/mapping")
    if node_is_check_phase(node) and node_needs_roster_mapping_check(node) and not (
        runbook_is_fleet_rms_status_check(runbook, match)
        or runbook_is_wcs_sql_diagnostic_state(runbook, match)
        or (
            runbook_is_status_check(runbook, match)
            and re.search(r"\b(rms|fleet|roster|mapping|agv status)\b", runbook_match_text(match, runbook), re.I)
        )
    ):
        _add(-0.20, "no roster/mapping-shaped evidence path")
    if node_is_symptom_pattern_confirmation(node) and not runbook_supports_symptom_corroboration(node, runbook, match):
        _add(-0.20, "does not support symptom-pattern corroboration")
    if node_needs_pairing_validation(node) and (
        runbook_is_bump_exception_reference(runbook, match) or runbook_is_bump_fault_recovery(runbook, match)
    ):
        _add(-0.30, "bump-exception/recovery runbook does not corroborate pairing validation")
    if node_needs_pairing_validation(node) and not (
        runbook_is_fleet_rms_status_check(runbook, match)
        or runbook_is_wcs_sql_diagnostic_state(runbook, match)
        or (
            runbook_is_status_check(runbook, match)
            and re.search(r"\b(rms|fleet|agv status|pair|hospital)\b", runbook_match_text(match, runbook), re.I)
        )
    ):
        _add(-0.20, "no pairing-validation-shaped evidence path")
    if node_is_check_phase(node) and node_needs_hospital_flow_check(node) and runbook_is_bump_exception_reference(runbook, match):
        _add(-0.30, "bump-exception runbook does not corroborate hospital flow")
    if node_is_check_phase(node) and node_needs_hospital_flow_check(node) and not (
        runbook_is_fleet_rms_status_check(runbook, match)
        or runbook_is_hospital_ui_reference(runbook, match)
        or runbook_is_wcs_sql_diagnostic_state(runbook, match)
        or (
            runbook_is_status_check(runbook, match)
            and re.search(r"\b(rms|fleet|hospital|tote|induct|extract)\b", runbook_match_text(match, runbook), re.I)
        )
    ):
        _add(-0.20, "no hospital-flow-shaped evidence path")
    if node_is_check_phase(node) and node_needs_sequence_backfill_check(node) and runbook_is_bump_exception_reference(runbook, match):
        _add(-0.30, "bump-exception runbook does not corroborate sequence backfill")
    if node_is_check_phase(node) and node_needs_sequence_backfill_check(node) and not (
        runbook_is_fleet_rms_status_check(runbook, match)
        or runbook_is_wcs_sql_diagnostic_state(runbook, match)
        or (
            runbook_is_status_check(runbook, match)
            and re.search(r"\b(rms|fleet|agv|exchange|sequence|backfill|tote)\b", runbook_match_text(match, runbook), re.I)
        )
    ):
        _add(-0.20, "no sequence-backfill-shaped evidence path")
    if node_needs_isolation_or_removal(node) and runbook_is_bump_fault_recovery(runbook, match):
        _add(-0.30, "bump-fault-recovery runbook does not corroborate isolation/removal")
    if (
        node_needs_isolation_or_removal(node)
        and node_type not in DIAGNOSTIC_NODE_TYPES
        and not runbook_is_agv_isolation_or_removal(runbook, match)
    ):
        _add(-0.25, "not an isolation/removal runbook")
    if node_needs_agv_fleet_domain(node) and runbook_is_unrelated_equipment(runbook, match):
        _add(-0.30, "unrelated equipment for AGV/fleet domain node")
    if runbook_is_wrong_domain_for_node(node, runbook, match):
        _add(-0.30, "wrong domain for node")
    if node_type == "procedure_reference" and node_needs_agv_fleet_domain(node):
        if not runbook_is_agv_fleet_related(runbook, match):
            _add(-0.30, "not AGV/fleet-related for procedure_reference node")
        elif str(match.procedure_type or "").lower() not in {"recovery", "operation", "diagnostic"}:
            _add(-0.20, "procedure type not recovery/operation/diagnostic for procedure_reference node")
    return penalty, reasons


def filter_evidence_compatible_matches(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> list[RunbookSearchMatch]:
    """Deprecated shim: use evidence_domain_penalty() (per-candidate score
    adjustment) instead. Retained temporarily for callers not yet migrated
    onto the unified score_candidate path; behaves as a soft-domain-only
    filter (never drops on the retired "no required-capability overlap"
    vocabulary-gap case, since that is no longer a real conflict signal)."""
    retrieval_request = derive_retrieval_request(node)
    compatible: list[RunbookSearchMatch] = []
    for match in matches:
        runbook = (runbooks_by_id or {}).get(match.procedure_id) or {}
        penalty, reason = capability_domain_adjustment(retrieval_request, runbook)
        if reason and reason.startswith("excluded capability"):
            continue
        compatible.append(match)
    return compatible


def evidence_domain_penalty(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
) -> tuple[float, list[str]]:
    """Domain-rule score adjustment for the explicit expects_capability/
    expects_surface overlap check, replacing the former hard eligibility gate
    (filter_evidence_compatible_matches). A strong semantic/RAG match can now
    win despite a domain-rule mismatch here, and a weak match can still lose
    even when domain-rule-compatible.

    Explicit node metadata (expects_capability/expects_surface) is rarely
    populated by Stage 5 by design (Stage 5 stays source-grounded and does not
    know the runbook catalog); when absent, this contributes no penalty --
    the derived-request capability check is capability_domain_adjustment's
    job (called separately by total_domain_penalty, not duplicated here).

    No fail-open exception is needed here (unlike the former hard-filter
    version): a mild per-candidate penalty can never wipe out the whole
    candidate pool the way a hard drop could, so the "vocabulary gap" escape
    hatch that used to guard against that is retired -- NO_REQUIRED_OVERLAP_PENALTY
    already keeps that case mild on its own (see capability_derivation.py).
    """
    reasons: list[str] = []
    penalty = 0.0

    expected_capabilities = {
        str(item).strip()
        for item in node.get("required_evidence_concepts") or node.get("expects_capability") or []
        if str(item).strip()
    }
    expected_surfaces = {
        str(item).strip()
        for item in node.get("expects_surface") or []
        if str(item).strip()
    }
    expected_surfaces = _apply_remote_surface_preference(node, expected_surfaces)
    if expected_capabilities or expected_surfaces:
        runbook_capabilities = runbook_capability_tags(runbook)
        runbook_surfaces = runbook_access_surfaces(runbook)
        if expected_capabilities and runbook_capabilities and not expected_capabilities & runbook_capabilities:
            penalty += -0.15
            reasons.append("no expected-capability overlap")
        if expected_surfaces and runbook_surfaces and not expected_surfaces & runbook_surfaces:
            penalty += -0.15
            reasons.append("no expected-surface overlap")
    return penalty, reasons


def evidence_eligibility_rejections(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """Deprecated: domain rules no longer drop candidates, so there is no
    "rejected" set distinct from the scored candidate list. Retained only for
    the excluded-capability case (a runbook whose primary function directly
    conflicts with the node, e.g. the 228723-class MUTUALLY_EXCLUSIVE_GROUPS
    case) so downstream telemetry can still call out that specific signal;
    see build_retrieval_decision_telemetry for the full per-candidate scoring
    breakdown (domain_penalty/domain_reasons on every scored candidate)."""
    retrieval_request = derive_retrieval_request(node)
    rejections: list[dict[str, str]] = []
    for match in matches:
        runbook = (runbooks_by_id or {}).get(match.procedure_id) or {}
        _penalty, reason = capability_domain_adjustment(retrieval_request, runbook)
        if reason and reason.startswith("excluded capability"):
            rejections.append({"procedure_id": match.procedure_id, "reason": reason})
    return rejections


def build_retrieval_eligibility_trace(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    runbooks = runbooks_by_id or {}
    trace: list[dict[str, Any]] = []
    for match in matches:
        runbook = runbooks.get(match.procedure_id) or {}
        exact_gaps = runbook_exact_fit_gaps(node, runbook, match=match)
        type_ok = procedure_type_compatible(
            str(node.get("node_type") or ""),
            match.procedure_type,
        )
        trace.append(
            {
                "procedure_id": match.procedure_id,
                "procedure_type": match.procedure_type,
                "raw_scores": {
                    "cosine": match.cosine_score,
                    "jaccard": match.jaccard_score,
                    "combined": match.combined_score,
                },
                "capabilities": sorted(runbook_capability_tags(runbook)),
                "surfaces": sorted(runbook_access_surfaces(runbook)),
                "roles": sorted(runbook_audience_roles(runbook)),
                "procedure_type_match": type_ok,
                "exact_fit_gaps": exact_gaps,
                "structurally_compatible": type_ok and not has_structural_gap(exact_gaps),
                "exact_fit_gap_penalty": exact_fit_gap_penalty(exact_gaps),
            }
        )
    return trace


def build_retrieval_decision_telemetry(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
    selected: list[tuple[RunbookSearchMatch, str, list[str], float]] | None = None,
) -> dict[str, Any]:
    """Per-node retrieval decision record (Section 10 of the fix plan).

    Debug-only telemetry meant to make retrieval failures directly
    diagnosable -- not rendered into the finalized playbook. Domain-rule
    penalties are score input, not a hard filter, so every structurally-
    compatible candidate (procedure-type compatible, no hard structural gap)
    is included in scored_candidates with its domain_penalty/domain_reasons
    visible -- a strong semantic match with a domain penalty is now visible
    here instead of silently vanishing into a separate rejected-candidates
    list. rejected_candidates is retained narrowly for the true structural
    exclusions (excluded-capability primary hits) as a quick-scan signal.
    """
    runbooks = runbooks_by_id or {}
    retrieval_request = derive_retrieval_request(node)
    rejected = evidence_eligibility_rejections(node, matches, runbooks_by_id=runbooks)
    structurally_compatible = [
        match
        for match in matches
        if not has_structural_gap(runbook_exact_fit_gaps(node, runbooks.get(match.procedure_id), match=match))
    ]
    ranked = [
        match
        for match, _ in rank_matches_for_node(node, structurally_compatible, runbooks_by_id=runbooks, domain_penalty_fn=total_domain_penalty)
    ] if structurally_compatible else []
    scored_candidates = []
    for match in ranked:
        runbook = runbooks.get(match.procedure_id)
        domain_penalty, domain_reasons = total_domain_penalty(node, match, runbook)
        boosted = boost_combined_score(
            match.combined_score,
            node=node,
            node_text=build_retrieval_query_text(node),
            match=match,
            runbook=runbook,
            procedure_type_compatible=True,
            peer_matches=structurally_compatible,
            runbooks_by_id=runbooks,
            domain_penalty=domain_penalty,
        )
        scored_candidates.append(
            {
                "procedure_id": match.procedure_id,
                "raw_score": match.combined_score,
                "boosted_score": boosted,
                "domain_penalty": domain_penalty,
                "domain_reasons": domain_reasons,
            }
        )
    selected_ids = [match.procedure_id for match, *_ in (selected or [])]
    return {
        "node_id": str(node.get("node_id") or ""),
        "derived_retrieval_request": retrieval_request,
        "candidate_count_before_eligibility": len(matches),
        "eligible_candidates": [match.procedure_id for match in structurally_compatible],
        "rejected_candidates": rejected,
        "scored_candidates": scored_candidates,
        "selected_primary": selected_ids[0] if selected_ids else None,
        "selected_corroborating": selected_ids[1:] if len(selected_ids) > 1 else [],
    }


def filter_evidence_compatible_links(
    node: dict[str, Any],
    links: list[dict[str, Any]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Last line of defense for the LLM-merged node path (_merge_llm_node can
    populate runbook_links without going through select_runbook_matches).

    Only drops on has_structural_gap (true schema-level incompatibility, e.g.
    procedure-type mismatch or a site-interview-only node) or on the
    remote-role RMS-authority check below. Other domain-rule penalties
    (capability/intent/evidence/exact-fit-gap) no longer drop a link here --
    an LLM-selected link with a domain-rule mismatch should surface at lower
    confidence with visible match_gaps, not vanish silently, matching the
    "soft signal, not hard veto" decision even for the LLM-merge path.
    Callers that render match_gaps onto the link (e.g. reconcile_llm_runbook_links)
    are responsible for attaching total_domain_penalty's reasons.

    The RMS-authority check stays a real filter here (rather than a score
    penalty) because this function operates on already-built link dicts with
    no combined_score to soften against -- a remote support role (L1-L4)
    should not receive an RMS-only procedure unless the node explicitly marks
    RMS as the authoritative/unique surface (_apply_remote_surface_preference);
    otherwise a remote role would be handed a site-only UI with no backend
    corroboration, which is a genuine access-authority gap, not a fuzzy
    semantic-fit question.
    """
    expected_surfaces = _apply_remote_surface_preference(
        node,
        {str(item).strip() for item in node.get("expects_surface") or [] if str(item).strip()},
    )
    filtered: list[dict[str, Any]] = []
    for link in links:
        if not isinstance(link, dict):
            continue
        runbook = runbooks_by_id.get(str(link.get("procedure_id") or "")) or {}
        if has_structural_gap(runbook_exact_fit_gaps(node, runbook)):
            continue
        runbook_surfaces = runbook_access_surfaces(runbook)
        if expected_surfaces and runbook_surfaces and not expected_surfaces & runbook_surfaces:
            continue
        filtered.append(link)
    return filtered


def _apply_remote_surface_preference(
    node: dict[str, Any],
    expected_surfaces: set[str],
) -> set[str]:
    roles = {
        str(item).strip().lower()
        for item in (node.get("preferred_audience") or node.get("allowed_roles") or [])
        if str(item).strip()
    }
    if not roles & {"l1_support", "l2_support", "l3_support", "l4_support", "remote"}:
        return expected_surfaces
    if not expected_surfaces or not expected_surfaces <= {"rms_ui", "rms"}:
        return expected_surfaces
    text = " ".join(
        str(node.get(key) or "")
        for key in ("title", "intent", "goal", "runbook_placeholder", "purpose")
    )
    if re.search(r"\b(rms|rms_ui)\b.*\b(only|authoritative|unique|owns)\b", text, re.I):
        return expected_surfaces
    if re.search(r"\b(unique|authoritative|owns)\b.*\b(rms|rms_ui)\b", text, re.I):
        return expected_surfaces
    return {"wcs_sql", "wcs_api", "event_viewer", "aveva_hmi"}


def enforce_procedure_limits(
    node: dict[str, Any],
    links: list[dict[str, Any]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    node_type = str(node.get("node_type") or "")
    if node_type in {"diagnostic_decision", "branching_condition", "validation_gate"}:
        allowed_types = PROCEDURE_TYPE_ALLOWED.get(node_type, set())
        eligible = [
            link
            for link in filter_evidence_compatible_links(node, links, runbooks_by_id=runbooks_by_id)
            if str((runbooks_by_id.get(str(link.get("procedure_id") or "")) or {}).get("procedure_type") or "")
            in allowed_types
            and not has_structural_gap(
                runbook_exact_fit_gaps(
                    node,
                    runbooks_by_id.get(str(link.get("procedure_id") or "")),
                )
            )
        ]
        if node_type == "validation_gate":
            return eligible[:1]
        result: list[dict[str, Any]] = []
        surfaces: set[str] = set()
        for link in eligible:
            runbook = runbooks_by_id.get(str(link.get("procedure_id") or "")) or {}
            link_surfaces = runbook_access_surfaces(runbook)
            if result and link_surfaces and link_surfaces & surfaces and not _is_distinct_capability_companion_link(
                node,
                result,
                link,
                runbooks_by_id=runbooks_by_id,
            ):
                continue
            link_copy = dict(link)
            link_copy["link_role"] = "primary" if not result else "optional_corroboration"
            link_copy["link_rank"] = len(result) + 1
            result.append(link_copy)
            surfaces.update(link_surfaces)
            if len(result) == 2:
                break
        return result
    if _is_recovery_action_node(node):
        recovery = [
            link
            for link in links
            if str((runbooks_by_id.get(str(link.get("procedure_id") or "")) or {}).get("procedure_type") or "")
            == "recovery"
            and not has_structural_gap(
                runbook_exact_fit_gaps(
                    node,
                    runbooks_by_id.get(str(link.get("procedure_id") or "")),
                )
            )
        ]
        return recovery[:1]
    return links[:1] if node_type == "recovery_phase_marker" else links


def _is_recovery_action_node(node: dict[str, Any]) -> bool:
    text = " ".join(
        str(node.get(key) or "")
        for key in ("title", "intent", "goal", "runbook_placeholder")
    ).lower()
    return str(node.get("node_type") or "") in {"recovery_action", "recovery_phase_marker"} or bool(
        re.search(r"\b(recover|restart|remove|isolate|restore|perform approved)\b", text)
    )


# docs/design_decisions/stage_8_playbook_finalization.md, "Backend-vs-UI
# evidence rule (2026-08-07)": nodes in these documented exception categories
# are source-supported by a different surface, so forcing a SQL/SSMS pairing
# onto them would be a fabricated evidence path, not corroboration.
BACKEND_PAIRING_EXCEPTION_PATTERN = re.compile(
    r"\b("
    r"ignition|gateway|optisweep.*service|wcswebapplication|"
    r"windows service|event viewer|application log|service control manager|"
    r"api.*respons|getagvstatuses"
    r")\b",
    re.IGNORECASE,
)


def _is_backend_pairing_exception(node: dict[str, Any]) -> bool:
    text = node_check_text(node).lower()
    if re.search(r"\b(rms|rms_ui)\b.*\b(only|authoritative|unique|owns)\b", text):
        return True
    if re.search(r"\b(unique|authoritative|owns)\b.*\b(rms|rms_ui)\b", text):
        return True
    return bool(BACKEND_PAIRING_EXCEPTION_PATTERN.search(text))


def _is_post_recovery_validation_node(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") != "validation_gate":
        return False
    text = node_check_text(node).lower()
    return bool(
        re.search(
            r"\b(after|post)[- ]?(recovery|correction|restart)\b|resumed operation|stable[- ]operation",
            text,
        )
    )


def node_needs_backend_pairing(node: dict[str, Any]) -> bool:
    """True for diagnostic nodes in scope for the Backend-vs-UI evidence rule
    (docs/design_decisions/stage_8_playbook_finalization.md): pairing,
    roster, tote, task, hospital, tipper, sequence, or post-recovery
    validation state -- excluding the rule's documented exceptions
    (operator-required-by-source, ignition/service-health, service-restart,
    gateway-health, Event Viewer/Windows Services/API-responsiveness).
    """
    if str(node.get("node_type") or "") not in DIAGNOSTIC_NODE_TYPES:
        return False
    if _is_backend_pairing_exception(node):
        return False
    return bool(
        node_needs_roster_mapping_check(node)
        or node_needs_hospital_flow_check(node)
        or node_needs_sequence_backfill_check(node)
        or node_needs_pairing_validation(node)
        or node_is_symptom_pattern_confirmation(node)
        or _is_post_recovery_validation_node(node)
    )


def _link_is_rms_ui_only(link: dict[str, Any], *, runbooks_by_id: dict[str, dict[str, Any]]) -> bool:
    runbook = runbooks_by_id.get(str(link.get("procedure_id") or ""))
    surfaces = runbook_access_surfaces(runbook)
    return bool(surfaces) and surfaces <= {"rms_ui"}


def _link_has_wcs_sql_surface(link: dict[str, Any], *, runbooks_by_id: dict[str, dict[str, Any]]) -> bool:
    runbook = runbooks_by_id.get(str(link.get("procedure_id") or ""))
    return "wcs_sql" in runbook_access_surfaces(runbook)


def _cap_rms_ui_links(
    links: list[dict[str, Any]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """At most one RMS/UI-only link per the Backend-vs-UI evidence rule.
    Keeps the first (highest-ranked, since input is already rank-ordered)
    RMS/UI-only link and drops any additional ones."""
    kept: list[dict[str, Any]] = []
    rms_seen = False
    for link in links:
        if _link_is_rms_ui_only(link, runbooks_by_id=runbooks_by_id):
            if rms_seen:
                continue
            rms_seen = True
        kept.append(link)
    return kept


def ensure_backend_evidence_pairing(
    node: dict[str, Any],
    links: list[dict[str, Any]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    candidates: list[RunbookSearchMatch] | None = None,
) -> list[dict[str, Any]]:
    """Guaranteed post-selection completion step (not probabilistic): if the
    node needs backend pairing (node_needs_backend_pairing) and the current
    links have no wcs_sql-surfaced runbook, attach the best-scoring wcs_sql
    candidate as corroborating evidence. Falls back to a full-catalog scan
    when the node's normal top-K retrieval candidates didn't include a
    qualifying wcs_sql runbook, so the guarantee holds even if the SQL
    runbook scored below the node's normal retrieval cutoff. If truly no
    wcs_sql runbook exists anywhere in the catalog, links pass through
    unchanged -- a genuine catalog gap should be visible via match_gaps/
    telemetry, not silently invented.

    Also caps RMS/UI-only links at one per the same rule (_cap_rms_ui_links),
    applied whether or not a new backend link was added.
    """
    if not node_needs_backend_pairing(node):
        return links
    if any(_link_has_wcs_sql_surface(link, runbooks_by_id=runbooks_by_id) for link in links if isinstance(link, dict)):
        return _cap_rms_ui_links(links, runbooks_by_id=runbooks_by_id)

    node_text = build_retrieval_query_text(node)
    pool = list(candidates or [])
    sql_candidates = [
        match
        for match in pool
        if "wcs_sql" in runbook_access_surfaces(runbooks_by_id.get(match.procedure_id))
        and runbook_is_wcs_sql_diagnostic_state(runbooks_by_id.get(match.procedure_id), match)
    ]
    if not sql_candidates:
        # Full-catalog fallback: the guarantee must hold even when the
        # qualifying SQL runbook never surfaced in this node's normal
        # top-K retrieval results.
        sql_candidates = [
            runbook_as_match(runbook)
            for runbook in runbooks_by_id.values()
            if "wcs_sql" in runbook_access_surfaces(runbook)
            and runbook_is_wcs_sql_diagnostic_state(runbook, runbook_as_match(runbook))
        ]
    if not sql_candidates:
        return _cap_rms_ui_links(links, runbooks_by_id=runbooks_by_id)

    scored = [
        (match, evaluate_link_confidence(node, match, runbook=runbooks_by_id.get(match.procedure_id), link_rank=len(links) + 1))
        for match in sql_candidates
    ]
    scored.sort(key=lambda item: -item[1][1])
    best_match, (confidence, boosted, gaps) = scored[0]
    new_link = {
        "procedure_id": best_match.procedure_id,
        "link_confidence": confidence if confidence != "unresolved" else "low",
        "link_rationale": (
            "Backend-vs-UI completion pass: WCS/SSMS is the authoritative backend "
            "state source for this node; attached as corroborating evidence."
        ),
        "match_gaps": gaps,
        "retrieval_combined_score": best_match.combined_score,
        "boosted_score": boosted,
        "link_role": "backend_corroboration",
    }
    combined = _cap_rms_ui_links([*links, new_link], runbooks_by_id=runbooks_by_id)
    return combined[:MAX_RUNBOOKS_PER_NODE]


def select_runbook_matches(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
    max_runbooks: int = MAX_RUNBOOKS_PER_NODE,
) -> list[tuple[RunbookSearchMatch, str, list[str], float]]:
    if node_is_site_interview_only(node):
        return []
    if node_is_site_history_branch(node):
        return []
    if node_is_escalation_handoff_only(node):
        return []
    if not matches:
        return []
    # Only true structural filters remain hard drops here: procedure-type
    # compatibility and schema-level exact-fit gaps (has_structural_gap).
    # Domain-rule penalties (capability/intent/evidence/exact-fit-gap) are
    # score input only from here on -- see total_domain_penalty, applied
    # inside evaluate_link_confidence/rank_matches_for_node below.
    compatible = filter_compatible_matches(node, matches)
    compatible = [
        match
        for match in compatible
        if not has_structural_gap(
            runbook_exact_fit_gaps(node, (runbooks_by_id or {}).get(match.procedure_id), match=match)
        )
    ]
    if not compatible:
        return []
    ranked = [match for match, _ in rank_matches_for_node(node, compatible, runbooks_by_id=runbooks_by_id, domain_penalty_fn=total_domain_penalty)]
    ranked = _prefer_broader_primary_capability(node, ranked, runbooks_by_id=runbooks_by_id)
    top = ranked[0]
    top_runbook = (runbooks_by_id or {}).get(top.procedure_id)
    top_confidence, top_boosted, top_gaps = evaluate_link_confidence(
        node,
        top,
        runbook=top_runbook,
        link_rank=1,
    )
    if top_confidence == "unresolved":
        return []
    # A same-rank jaccard-based confidence elevation (reconcile_link_confidence)
    # can label a candidate "medium"/"low" even when its actual boosted score
    # (raw semantic score + domain-rule penalties) sits below the retrieval
    # floor -- that elevation heuristic looks at jaccard_score directly, not
    # the domain-penalized score. Since domain rules are no longer a
    # pre-scoring hard filter, a severely domain-penalized top candidate must
    # not survive selection purely on a confidence-label technicality.
    top_domain_penalty, _ = total_domain_penalty(node, top, top_runbook)
    if top_domain_penalty <= MAX_DOMAIN_PENALTY and top_boosted < MIN_RETRIEVAL_FLOOR:
        return []

    selected: list[tuple[RunbookSearchMatch, str, list[str], float]] = [
        (top, top_confidence, top_gaps, top_boosted)
    ]
    placeholder = str(node.get("runbook_placeholder") or "")
    allow_multiple = (
        _allows_multiple_runbooks(node, placeholder)
        or _allows_fleet_status_bundle(node)
        or _allows_isolation_removal_bundle(node)
        or _allows_symptom_corroboration_bundle(node)
        or _allows_capability_multilink(node)
        or _allows_service_health_bundle(node)
    )
    max_links = min(max_runbooks, 1 + MAX_ALTERNATE_RUNBOOKS if allow_multiple else 1)

    for match in ranked[1:]:
        if len(selected) >= max_links:
            break
        if match.procedure_id == top.procedure_id:
            continue
        if _too_similar_to_selected(match, selected):
            continue
        if allow_multiple and not _is_valid_companion_link(node, top, match, runbooks_by_id=runbooks_by_id):
            continue
        confidence, boosted, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=(runbooks_by_id or {}).get(match.procedure_id),
            link_rank=len(selected) + 1,
        )
        if confidence == "unresolved":
            continue
        node_text = build_retrieval_query_text(node)
        runbook = (runbooks_by_id or {}).get(match.procedure_id)
        overlap = anchor_overlap(node_text, runbook_match_text(match, runbook))
        has_capability_overlap = (
            bool(capability_tag_overlap(node, runbook))
            if USE_CAPABILITY_TAG_CONSTRAINTS
            else False
        )
        min_boosted = 0.35 if has_capability_overlap else SECONDARY_RUNBOOK_MIN_BOOSTED
        min_anchor = 0.05 if has_capability_overlap else SECONDARY_RUNBOOK_MIN_ANCHOR_OVERLAP
        if len(selected) > 1 and (boosted < min_boosted or overlap < min_anchor):
            continue
        selected.append((match, confidence, gaps, boosted))
        if len(selected) >= max_links:
            break
    return _ensure_surface_coverage_selected(
        node,
        selected,
        ranked,
        runbooks_by_id=runbooks_by_id or {},
        max_links=max_links,
    )


def reconcile_llm_runbook_links(
    node: dict[str, Any],
    links: list[dict[str, Any]],
    retrieval_matches: list[Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if node_is_site_interview_only(node):
        return []
    if node_is_site_history_branch(node):
        return []
    if node_is_escalation_handoff_only(node):
        return []
    if not links:
        return []
    if not retrieval_matches:
        return filter_evidence_compatible_links(
            node,
            links,
            runbooks_by_id=runbooks_by_id,
        )
    # Only the true structural filter remains a hard drop here; domain-rule
    # penalties are score input via rank_matches_for_node's domain_penalty_fn
    # below, not a pre-ranking filter.
    compatible = [
        match
        for match in retrieval_matches
        if not has_structural_gap(
            runbook_exact_fit_gaps(node, runbooks_by_id.get(match.procedure_id), match=match)
        )
    ]
    if not compatible:
        return []
    ranked = rank_matches_for_node(
        node,
        compatible,
        runbooks_by_id=runbooks_by_id,
        domain_penalty_fn=total_domain_penalty,
    )
    if not ranked:
        return links
    best_match, best_boosted = ranked[0]
    first = links[0]
    procedure_id = str(first.get("procedure_id") or "")
    chosen_match = next((match for match, _ in ranked if match.procedure_id == procedure_id), None)
    if not chosen_match:
        return _build_links_from_ranked(node, ranked, runbooks_by_id=runbooks_by_id)
    chosen_runbook = runbooks_by_id.get(procedure_id)
    chosen_is_mismatch = bool(intent_mismatch_gaps(node, chosen_match, chosen_runbook))
    best_runbook = runbooks_by_id.get(best_match.procedure_id)
    best_is_better_fit = (
        runbook_is_fleet_rms_status_check(best_runbook, best_match)
        or runbook_is_status_check(best_runbook, best_match)
    ) and (
        runbook_is_recovery_prep(chosen_runbook, chosen_match)
        or runbook_is_bump_exception_reference(chosen_runbook, chosen_match)
        or chosen_is_mismatch
    )
    if not best_is_better_fit:
        _, chosen_boosted = next((item for item in ranked if item[0].procedure_id == procedure_id), (None, 0.0))
        if chosen_boosted > best_boosted + INTENT_OVERRIDE_MARGIN:
            return _annotate_link_roles(links)
    confidence, boosted, gaps = evaluate_link_confidence(
        node,
        best_match,
        runbook=best_runbook,
        link_rank=1,
    )
    # Same floor as select_runbook_matches: a severely domain-penalized top
    # candidate must not survive purely because reconcile_link_confidence's
    # jaccard-based elevation heuristic labeled it "low"/"medium" despite a
    # boosted score below the retrieval floor.
    best_domain_penalty, _ = total_domain_penalty(node, best_match, best_runbook)
    if confidence == "unresolved" or (best_domain_penalty <= MAX_DOMAIN_PENALTY and boosted < MIN_RETRIEVAL_FLOOR):
        return []
    corrected = dict(first)
    corrected.update(
        {
            "procedure_id": best_match.procedure_id,
            "link_confidence": confidence,
            "link_rationale": (
                "Retrieval realigned to fleet/status-check runbook; prior link penalized for intent mismatch."
            ),
            "match_gaps": gaps,
            "retrieval_combined_score": best_match.combined_score,
            "boosted_score": boosted,
            "link_rank": 1,
            "link_role": "primary",
        }
    )
    remaining = []
    for link in links[1:]:
        if not isinstance(link, dict):
            continue
        alt_id = str(link.get("procedure_id") or "")
        if alt_id == best_match.procedure_id:
            continue
        alt_match = next((match for match, _ in ranked if match.procedure_id == alt_id), None)
        if not alt_match:
            continue
        alt_confidence, alt_boosted, alt_gaps = evaluate_link_confidence(
            node,
            alt_match,
            runbook=runbooks_by_id.get(alt_id),
            link_rank=len(remaining) + 2,
        )
        if alt_confidence == "unresolved":
            continue
        remaining.append(
            {
                **link,
                "link_confidence": alt_confidence,
                "match_gaps": alt_gaps,
                "retrieval_combined_score": alt_match.combined_score,
                "boosted_score": alt_boosted,
                "link_role": "alternate",
            }
        )
    companion_links = _companion_links_from_ranked(
        node,
        ranked[1:],
        runbooks_by_id=runbooks_by_id,
        exclude_ids={best_match.procedure_id, *(str(item.get("procedure_id") or "") for item in remaining)},
        start_rank=len(remaining) + 2,
    )
    combined = _annotate_link_roles([corrected, *remaining, *companion_links][:MAX_RUNBOOKS_PER_NODE])
    return _ensure_surface_coverage_links(
        node,
        combined,
        ranked,
        runbooks_by_id=runbooks_by_id,
        max_links=MAX_RUNBOOKS_PER_NODE,
    )


def build_decision_outcomes(
    node: dict[str, Any],
    runbooks_by_id: dict[str, dict[str, Any]],
    *,
    linked_runbook_ids: list[str],
    branch_hints: list[dict[str, Any]],
    playbook_context: dict[str, Any] | None = None,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    node_type = str(node.get("node_type") or "")
    if node_type not in OUTCOME_NODE_TYPES:
        return []
    synthesized = _synthesize_node_decision_outcomes(
        node,
        branch_hints,
        playbook_context=playbook_context,
        all_nodes=all_nodes,
    )
    # Node outcomes belong to the Stage 5 diagnostic question.  Linked
    # runbooks provide collection steps and criteria, but their step results
    # must remain inside the linked procedure surface.
    return _mark_terminal_outcomes(synthesized)


def enrich_node_structure(
    node: dict[str, Any],
    *,
    decision_outcomes: list[dict[str, Any]] | None = None,
    branches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    enriched = dict(node)
    enriched.setdefault("purpose", str(node.get("intent") or node.get("goal") or ""))
    enriched.setdefault(
        "diagnostic_reasoning",
        str(node.get("source_supported_description") or node.get("intent") or node.get("goal") or ""),
    )
    enriched.setdefault(
        "evidence_required",
        list(node.get("evidence_required") or node.get("required_evidence") or []),
    )
    enriched.setdefault(
        "healthy_indicators",
        list(node.get("healthy_indicators") or node.get("healthy_conditions") or []),
    )
    enriched.setdefault(
        "unhealthy_indicators",
        list(node.get("unhealthy_indicators") or node.get("unhealthy_conditions") or []),
    )
    enriched.setdefault(
        "inconclusive_indicators",
        list(node.get("inconclusive_indicators") or node.get("inconclusive_conditions") or []),
    )
    outcomes = decision_outcomes if decision_outcomes is not None else list(node.get("decision_outcomes") or [])
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            continue
        label = str(outcome.get("outcome_label") or "").strip()
        descriptor = str(outcome.get("descriptor") or outcome.get("observable_signal") or "").strip()
        if label == "healthy" and descriptor and not enriched["healthy_indicators"]:
            enriched["healthy_indicators"] = [descriptor]
        elif label == "unhealthy" and descriptor and not enriched["unhealthy_indicators"]:
            enriched["unhealthy_indicators"] = [descriptor]
        elif label == "inconclusive" and descriptor and not enriched["inconclusive_indicators"]:
            enriched["inconclusive_indicators"] = [descriptor]
    enriched.setdefault("evidence_collection_procedures", [])
    enriched.setdefault("catalog_gaps", [])
    enriched.setdefault("next_branches", branches if branches is not None else list(node.get("branches") or []))
    enriched.setdefault("source_evidence", list(node.get("source_refs") or []))
    return enriched


def stage5_node_preservation_warnings(
    stage5_nodes: list[dict[str, Any]],
    finalized_nodes: list[dict[str, Any]],
) -> list[str]:
    finalized_by_id = {
        str(node.get("node_id") or ""): node
        for node in finalized_nodes
        if isinstance(node, dict)
    }
    warnings: list[str] = []
    source_ids = [str(node.get("node_id") or "") for node in stage5_nodes if isinstance(node, dict)]
    finalized_ids = [str(node.get("node_id") or "") for node in finalized_nodes if isinstance(node, dict)]
    if source_ids != finalized_ids:
        warnings.append("Stage 8 changed Stage 5 node order or node IDs.")
    preserved_fields = (
        "node_order",
        "node_type",
        "title",
        "intent",
        "goal",
        "runbook_placeholder",
        "expected_or_observed_result",
        "observed_surfaces",
        "source_used_surfaces",
        "required_evidence_concepts",
        "recommended_diagnostic_surfaces",
        "stage8_candidate_surfaces",
        "healthy_indicators",
        "unhealthy_indicators",
        "inconclusive_indicators",
        "source_supported_description",
        "source_refs",
        "related_artifact_ids",
        "related_event_ids",
        "stop_or_escalation_note",
    )
    for source in stage5_nodes:
        if not isinstance(source, dict):
            continue
        node_id = str(source.get("node_id") or "")
        finalized = finalized_by_id.get(node_id)
        if not finalized:
            continue
        for field in preserved_fields:
            if field in source and finalized.get(field) != source.get(field):
                warnings.append(f"{node_id}: Stage 5 field changed: {field}")
    return warnings


def build_branches_from_hints(
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    llm_branches: list[dict[str, Any]] | None = None,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    node_id = str(node.get("node_id") or "")
    if llm_branches:
        return _sanitize_branches(node, llm_branches, branch_hints, all_nodes=all_nodes)
    seeded = [
        hint
        for hint in branch_hints
        if str(hint.get("from_node_id") or "") == node_id
    ]
    branches: list[dict[str, Any]] = []
    for index, hint in enumerate(seeded, start=1):
        condition = str(hint.get("condition_or_signal") or "")
        next_node_id = str(hint.get("suggested_next_node_id") or "")
        if not _transition_allowed(node, next_node_id, branch_hints, all_nodes=all_nodes):
            next_node_id = ""
        outcome = _branch_outcome_for_hint(node, condition)
        branches.append(
            {
                "branch_id": f"{node_id}_branch_{index}",
                "condition_label": condition,
                "condition_descriptor": condition,
                "outcome": outcome,
                "next_node_id": next_node_id,
                "terminal_result": _terminal_result(outcome, condition) if not next_node_id else "",
                "source_branch_hint_ids": [f"branch_hint_{index}"],
                "linked_runbook_step_ref": "",
                "source_refs": hint.get("source_refs") or [],
            }
        )
    branches.extend(
        _infer_complementary_branches(node, branches, branch_hints, all_nodes=all_nodes)
    )
    return _sanitize_branches(node, branches, branch_hints, all_nodes=all_nodes)


def validate_finalized_playbook(
    playbook: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    max_runbooks_per_node: int = MAX_RUNBOOKS_PER_NODE,
) -> list[str]:
    warnings: list[str] = []
    node_ids = {str(node.get("node_id") or "") for node in playbook.get("nodes") or [] if isinstance(node, dict)}
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        try:
            FinalizedNode.model_validate(node)
        except Exception as exc:
            warnings.append(f"{node.get('node_id') or 'node'}: invalid finalized node shape: {exc}")
        links = node.get("runbook_links") or []
        procedure_ids = [str(link.get("procedure_id") or "") for link in links if isinstance(link, dict)]
        if len(procedure_ids) > max_runbooks_per_node:
            warnings.append(f"{node.get('node_id')}: more than {max_runbooks_per_node} runbook links")
        for procedure_id in procedure_ids:
            if procedure_id and procedure_id not in runbooks_by_id:
                warnings.append(f"{node.get('node_id')}: unknown procedure_id {procedure_id}")
            elif procedure_id and node_is_check_phase(node) and runbook_is_recovery_prep(
                runbooks_by_id.get(procedure_id),
                runbook_as_match(runbooks_by_id[procedure_id]),
            ):
                warnings.append(
                    f"{node.get('node_id')}: recovery-prep runbook linked to check-only node {procedure_id}"
                )
            elif procedure_id and not procedure_type_compatible(str(node.get("node_type") or ""), str(runbooks_by_id[procedure_id].get("procedure_type") or "")):
                warnings.append(
                    f"{node.get('node_id')}: procedure_type mismatch for {procedure_id}"
                )
        for link in links:
            if not isinstance(link, dict):
                continue
            if str(link.get("link_confidence") or "").lower() in {"low", "unresolved"} and not [
                gap for gap in link.get("match_gaps") or [] if str(gap).strip()
            ]:
                warnings.append(
                    f"{node.get('node_id')}: low-confidence link {link.get('procedure_id') or 'unresolved'} "
                    "must include match_gaps"
                )
            linked_procedure_id = str(link.get("procedure_id") or "")
            if linked_procedure_id and linked_procedure_id in runbooks_by_id:
                exact_gaps = runbook_exact_fit_gaps(
                    node,
                    runbooks_by_id[linked_procedure_id],
                )
                if has_structural_gap(exact_gaps) or exact_fit_gap_penalty(exact_gaps):
                    warnings.append(
                        f"{node.get('node_id')}: exact-fit gap on linked runbook {linked_procedure_id}: "
                        + "; ".join(exact_gaps)
                    )
        for reference in node.get("linked_runbooks") or []:
            if not isinstance(reference, dict):
                continue
            embedded_fields = set(reference) & {
                "steps",
                "healthy_conditions",
                "failure_conditions",
                "visual_references",
                "screens_or_images",
            }
            if embedded_fields:
                warnings.append(
                    f"{node.get('node_id')}: linked runbook reference embeds catalog fields "
                    f"{sorted(embedded_fields)}"
                )
        node_type = str(node.get("node_type") or "")
        if node_type == "diagnostic_decision":
            required_action_fields = (
                "primary_action",
                "performed_by",
                "primary_surface",
                "evidence_to_collect",
                "healthy_interpretation",
                "unhealthy_interpretation",
                "inconclusive_interpretation",
                "generated_guidance",
                "ontology_evidence",
                "confidence",
                "requires_sme_review",
            )
            missing_action_fields = [
                field
                for field in required_action_fields
                if field not in node
                or (
                    field != "ontology_evidence"
                    and node.get(field) in (None, "", [])
                )
            ]
            if missing_action_fields:
                warnings.append(
                    f"{node.get('node_id')}: diagnostic action plan missing "
                    f"{', '.join(missing_action_fields)}"
                )
            expected_action_types = {
                "primary_action": str,
                "performed_by": str,
                "primary_surface": str,
                "evidence_to_collect": list,
                "healthy_interpretation": str,
                "unhealthy_interpretation": str,
                "inconclusive_interpretation": str,
                "optional_corroboration": list,
                "linked_primary_procedure": (dict, type(None)),
                "generated_guidance": str,
                "ontology_evidence": list,
                "confidence": str,
                "requires_sme_review": bool,
                "query_mode": str,
                "evidence_retrieval_success": str,
                "diagnostic_interpretation": str,
            }
            malformed_action_fields = [
                field
                for field, expected_type in expected_action_types.items()
                if field in node
                and node.get(field) not in (None, "", [])
                and not isinstance(node.get(field), expected_type)
            ]
            for field in ("evidence_to_collect",):
                if (
                    isinstance(node.get(field), list)
                    and any(not isinstance(item, str) for item in node.get(field))
                ):
                    malformed_action_fields.append(field)
            for field in ("optional_corroboration", "ontology_evidence"):
                if (
                    isinstance(node.get(field), list)
                    and any(not isinstance(item, dict) for item in node.get(field))
                ):
                    malformed_action_fields.append(field)
            malformed_action_fields = list(dict.fromkeys(malformed_action_fields))
            if malformed_action_fields:
                warnings.append(
                    f"{node.get('node_id')}: diagnostic action plan malformed "
                    f"{', '.join(malformed_action_fields)}"
                )
            evidence = node.get("evidence_to_collect")
            if isinstance(evidence, list) and not 3 <= len(evidence) <= 8:
                warnings.append(
                    f"{node.get('node_id')}: diagnostic evidence must contain 3–8 items"
                )
            if len(links) > 2:
                warnings.append(
                    f"{node.get('node_id')}: diagnostic node exceeds one primary plus one corroboration procedure"
                )
            mapping = node.get("technical_field_mapping") or {}
            entities = (mapping.get("entities") if isinstance(mapping, dict) else []) or []
            field_count = sum(
                len(entity.get("fields") or [])
                for entity in entities
                if isinstance(entity, dict)
            )
            if len(entities) > 3 or field_count > 8:
                warnings.append(
                    f"{node.get('node_id')}: ontology evidence exceeds 3 entities or 8 fields"
                )
            if node.get("optional_corroboration") and len(node.get("optional_corroboration")) > 1:
                warnings.append(
                    f"{node.get('node_id')}: more than one optional corroboration procedure"
                )
        if node_type in {"procedure_reference", "recovery_action", "recovery_phase_marker", "escalation_gate"}:
            field_mapping = node.get("technical_field_mapping")
            if node.get("ontology_evidence") or (
                isinstance(field_mapping, dict) and field_mapping.get("entities")
            ):
                warnings.append(f"{node.get('node_id')}: recovery/escalation node must not contain ontology fields")
        if node_type == "procedure_reference":
            required = (
                "trigger_condition",
                "selected_procedure",
                "selection_rationale",
                "prerequisites",
                "safety_checks",
                "success_confirmation",
                "failure_boundary",
            )
            missing = [field for field in required if field not in node]
            if missing:
                warnings.append(f"{node.get('node_id')}: procedure reference schema missing {', '.join(missing)}")
        if node_type == "validation_gate":
            required = (
                "validation_checklist",
                "required_evidence_sources",
                "stable_operation_observation",
                "healthy_interpretation",
                "unhealthy_interpretation",
                "inconclusive_interpretation",
            )
            missing = [field for field in required if field not in node]
            if missing:
                warnings.append(f"{node.get('node_id')}: validation gate schema missing {', '.join(missing)}")
        if node_type == "escalation_gate":
            required = (
                "escalation_reason",
                "evidence_package",
                "actions_attempted",
                "unresolved_questions",
                "required_next_team",
            )
            missing = [field for field in required if field not in node]
            if missing:
                warnings.append(f"{node.get('node_id')}: escalation gate schema missing {', '.join(missing)}")
        if node_type in OUTCOME_NODE_TYPES:
            outcomes = node.get("decision_outcomes") or []
            labels = {str(item.get("outcome_label") or "") for item in outcomes if isinstance(item, dict)}
            if "healthy" not in labels or not {"unhealthy", "inconclusive"} & labels:
                warnings.append(f"{node.get('node_id')}: missing healthy/unhealthy decision outcomes")
            branch_outcomes = {
                str(branch.get("outcome") or "")
                for branch in (node.get("branches") or [])
                if isinstance(branch, dict)
            }
            if node_type == "diagnostic_decision" and (
                "healthy" not in branch_outcomes or "unhealthy" not in branch_outcomes
            ):
                warnings.append(
                    f"{node.get('node_id')}: diagnostic node missing healthy and/or unhealthy branch coverage"
                )
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            next_node_id = str(branch.get("next_node_id") or "")
            if next_node_id and next_node_id not in node_ids:
                warnings.append(f"{node.get('node_id')}: branch next_node_id not found: {next_node_id}")
            if next_node_id and next_node_id == str(node.get("node_id") or ""):
                label = str(branch.get("condition_label") or "").lower()
                if "wait" not in label and "retry" not in label and "monitor" not in label:
                    warnings.append(
                        f"{node.get('node_id')}: unexpected self-loop branch {branch.get('branch_id')}"
                    )
            if next_node_id and not _transition_allowed(
                node,
                next_node_id,
                playbook.get("branch_hints") or [],
                all_nodes=[item for item in playbook.get("nodes") or [] if isinstance(item, dict)],
            ):
                warnings.append(
                    f"{node.get('node_id')}: branch to {next_node_id} skips required recovery prerequisite"
                )
        warnings.extend(_validate_outcome_labels(node, node_ids))
    for branch in playbook.get("branches") or []:
        if not isinstance(branch, dict):
            continue
        from_id = str(branch.get("from_node_id") or "").strip()
        if not from_id:
            warnings.append("playbook branch missing from_node_id")
            continue
        if from_id not in node_ids:
            warnings.append(f"playbook branch from_node_id not found: {from_id}")
        next_node_id = str(branch.get("next_node_id") or "")
        if next_node_id and next_node_id not in node_ids:
            warnings.append(f"playbook branch next_node_id not found: {next_node_id}")
    seen_edges: set[tuple[str, str, str, str]] = set()
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        from_id = str(node.get("node_id") or "")
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            key = (
                from_id,
                str(branch.get("outcome") or ""),
                str(branch.get("next_node_id") or ""),
                str(branch.get("condition_label") or branch.get("condition_descriptor") or "").strip().lower(),
            )
            if key in seen_edges:
                warnings.append(f"{from_id}: duplicate branch edge {key[1]} → {key[2]}")
            seen_edges.add(key)
    return warnings


def _validate_outcome_labels(node: dict[str, Any], node_ids: set[str]) -> list[str]:
    """Report deterministic outcome/branch contradictions without LLM repair."""
    node_id = str(node.get("node_id") or "node")
    node_type = str(node.get("node_type") or "")
    warnings: list[str] = []
    branches = [item for item in node.get("branches") or [] if isinstance(item, dict)]
    branch_labels = [str(item.get("outcome") or "").lower() for item in branches]
    duplicate_labels = sorted({label for label in branch_labels if label and branch_labels.count(label) > 1})
    if duplicate_labels:
        warnings.append(f"{node_id}: duplicate branch outcome labels: {', '.join(duplicate_labels)}")
    failure_terms = re.compile(r"\b(fail|failed|fault|error|abnormal|missing|remain|cannot|does not|not restored|unavailable)\b", re.I)
    success_terms = re.compile(r"\b(success|successful|completed|normal|restored|running|passes|passed|no residual)\b", re.I)
    for outcome in node.get("decision_outcomes") or []:
        if not isinstance(outcome, dict):
            continue
        label = str(outcome.get("outcome_label") or "").lower()
        descriptor = str(outcome.get("descriptor") or outcome.get("observable_signal") or "")
        if label == "healthy" and failure_terms.search(descriptor):
            warnings.append(f"{node_id}: healthy outcome contains failure language")
        if label == "unhealthy" and success_terms.search(descriptor):
            warnings.append(f"{node_id}: unhealthy outcome contains successful-completion language")
    for branch in branches:
        label = str(branch.get("outcome") or "").lower()
        condition = str(branch.get("condition_label") or branch.get("condition_descriptor") or "")
        next_node = str(branch.get("next_node_id") or "")
        if next_node and next_node not in node_ids:
            warnings.append(f"{node_id}: branch next_node_id not found: {next_node}")
        if node_type in {"recovery_action", "recovery_phase_marker", "procedure_reference"} and label == "inconclusive" and success_terms.search(condition):
            warnings.append(f"{node_id}: recovery success branch labeled inconclusive")
        if node_type == "validation_gate" and label == "unhealthy" and success_terms.search(condition):
            warnings.append(f"{node_id}: validation success branch labeled unhealthy")
        if label == "unhealthy" and not next_node and re.search(r"\b(correct|recover|restart|restore|remove|repair|escalat)", condition, re.I):
            warnings.append(f"{node_id}: unhealthy corrective branch has no next node")
    return list(dict.fromkeys(warnings))


class StructuralValidationError(ValueError):
    def __init__(self, playbook_id: str, errors: list[str]) -> None:
        self.playbook_id = playbook_id
        self.errors = errors
        super().__init__(f"Stage 8 workflow graph validation failed for {playbook_id}: " + "; ".join(errors))


def validate_workflow_graph(playbook: dict[str, Any]) -> list[str]:
    nodes = [node for node in playbook.get("nodes") or [] if isinstance(node, dict)]
    node_ids = [str(node.get("node_id") or "").strip() for node in nodes]
    errors: list[str] = []
    if not nodes:
        return ["playbook has no nodes"]
    if any(not node_id for node_id in node_ids):
        errors.append("every node must have a node_id")
    if len(node_ids) != len(set(node_ids)):
        errors.append("node_id values must be unique")
    node_by_id = {node_id: node for node_id, node in zip(node_ids, nodes) if node_id}
    edges: list[tuple[str, str, str]] = []

    def terminal(value: dict[str, Any]) -> bool:
        return bool(
            value.get("terminal_result")
            or value.get("is_terminal")
            or value.get("terminal") is True
        )

    for node in nodes:
        node_id = str(node.get("node_id") or "")
        for outcome in node.get("decision_outcomes") or []:
            if not isinstance(outcome, dict):
                continue
            next_node = str(outcome.get("next_node_id") or "").strip()
            if next_node:
                if next_node not in node_by_id:
                    errors.append(f"{node_id}: outcome targets missing node {next_node}")
                else:
                    edges.append((node_id, next_node, str(outcome.get("outcome_label") or "")))
            elif not terminal(outcome):
                errors.append(f"{node_id}: outcome {outcome.get('outcome_label') or 'unnamed'} has no next node or terminal result")
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            next_node = str(branch.get("next_node_id") or "").strip()
            label = str(branch.get("outcome") or "")
            if next_node:
                if next_node not in node_by_id:
                    errors.append(f"{node_id}: branch targets missing node {next_node}")
                else:
                    edges.append((node_id, next_node, label))
            elif not terminal(branch):
                errors.append(f"{node_id}: branch {branch.get('branch_id') or label} has no next node or terminal result")
    for branch in playbook.get("branches") or []:
        if not isinstance(branch, dict):
            continue
        from_node = str(branch.get("from_node_id") or "").strip()
        next_node = str(branch.get("next_node_id") or "").strip()
        label = str(branch.get("outcome") or "")
        if not from_node or from_node not in node_by_id:
            errors.append(f"playbook branch has missing from_node_id {from_node or '<empty>'}")
        if next_node and next_node not in node_by_id:
            errors.append(f"playbook branch targets missing node {next_node}")
        if not next_node and not terminal(branch):
            errors.append("playbook branch has no next node or terminal result")
        if from_node and next_node and from_node in node_by_id and next_node in node_by_id:
            edges.append((from_node, next_node, label))

    incoming: dict[str, int] = {node_id: 0 for node_id in node_by_id}
    outgoing: dict[str, list[tuple[str, str]]] = {node_id: [] for node_id in node_by_id}
    for from_node, next_node, label in edges:
        if from_node == next_node:
            errors.append(f"{from_node}: accidental self-cycle")
        incoming[next_node] = incoming.get(next_node, 0) + 1
        outgoing.setdefault(from_node, []).append((next_node, label))
    if _has_cycle(outgoing):
        errors.append("workflow graph contains an accidental cycle")

    entry = min(
        nodes,
        key=lambda node: (
            int(node.get("node_order") or 0),
            str(node.get("node_id") or ""),
        ),
    )
    reachable = _walk_graph(str(entry.get("node_id") or ""), outgoing)
    for node_id in node_by_id:
        if node_id not in reachable:
            errors.append(f"orphaned or unreachable node {node_id}")

    recovery_ids = {
        node_id for node_id, node in node_by_id.items() if _is_recovery_node(node)
    }
    validation_ids = {
        node_id for node_id, node in node_by_id.items() if str(node.get("node_type") or "") == "validation_gate"
    }
    if recovery_ids:
        for recovery_id in recovery_ids:
            if recovery_id not in reachable:
                errors.append(f"recovery node {recovery_id} is unreachable")
        for validation_id in validation_ids:
            if not any(validation_id in _walk_graph(recovery_id, outgoing) for recovery_id in recovery_ids):
                errors.append(f"validation node {validation_id} is not reachable after recovery")

    escalation_ids = {
        node_id
        for node_id, node in node_by_id.items()
        if str(node.get("node_type") or "") == "escalation_gate"
    }
    for escalation_id in escalation_ids:
        if not any(
            target == escalation_id
            and label.lower() in {"unhealthy", "inconclusive", "failure", "escalate"}
            for _, target, label in edges
        ):
            errors.append(f"escalation node {escalation_id} is not reachable from failure or inconclusive outcomes")

    for node_id, node in node_by_id.items():
        if str(node.get("node_type") or "") != "diagnostic_decision":
            continue
        declared = [
            str(item.get("outcome_label") or "").lower()
            for item in node.get("decision_outcomes") or []
            if isinstance(item, dict)
        ]
        targets = [target for source, target, _ in edges if source == node_id]
        if (
            declared
            and targets
            and all(target in escalation_ids for target in targets)
            and not (
                node.get("source_requires_escalation") is True
                or node.get("requires_escalation") is True
            )
        ):
            errors.append(f"{node_id}: diagnostic outcomes all route to escalation")

    return list(dict.fromkeys(errors))


def _walk_graph(start: str, outgoing: dict[str, list[tuple[str, str]]]) -> set[str]:
    seen: set[str] = set()
    stack = [start] if start else []
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(target for target, _ in outgoing.get(current, []))
    return seen


def _has_cycle(outgoing: dict[str, list[tuple[str, str]]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        if any(visit(target) for target, _ in outgoing.get(node_id, [])):
            return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node_id) for node_id in outgoing)


def needs_graph_repair(playbook: dict[str, Any]) -> bool:
    hints = playbook.get("branch_hints") or []
    confirmed: set[tuple[str, str]] = set()
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        for branch in node.get("branches") or []:
            if isinstance(branch, dict):
                confirmed.add((node_id, str(branch.get("next_node_id") or "")))
    for hint in hints:
        if not isinstance(hint, dict):
            continue
        edge = (str(hint.get("from_node_id") or ""), str(hint.get("suggested_next_node_id") or ""))
        if edge[0] and edge[1] and edge not in confirmed:
            return True
    return False


def _allows_multiple_runbooks(node: dict[str, Any], placeholder: str) -> bool:
    node_type = str(node.get("node_type") or "")
    normalized = normalize_placeholder_text(placeholder)
    if node_type == "validation_gate":
        return bool(re.search(r"\b(and|also|both|;\s|then)\b", normalized, re.IGNORECASE))
    if not COMPOUND_PLACEHOLDER_PATTERN.search(normalized):
        return False
    distinct_domains = sum(1 for terms in DOMAIN_ANCHORS.values() if any(term in normalized.lower() for term in terms))
    return distinct_domains >= 2


def _allows_fleet_status_bundle(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") not in DIAGNOSTIC_NODE_TYPES:
        return False
    text = node_check_text(node).lower()
    fleet_terms = ("rms", "agv", "robot", "fleet", "roster", "mapping", "hospital")
    hits = sum(1 for term in fleet_terms if term in text)
    return hits >= 2 or node_needs_roster_mapping_check(node)


def _allows_symptom_corroboration_bundle(node: dict[str, Any]) -> bool:
    return node_is_symptom_pattern_confirmation(node)


def _allows_isolation_removal_bundle(node: dict[str, Any]) -> bool:
    return str(node.get("node_type") or "") == "procedure_reference" and node_needs_isolation_or_removal(node)


# Capability pairs where the first is the broader/primary evidence source and
# the second is a valid but narrower corroborating source. A narrower-capability
# candidate must not outrank the broader one as *primary* purely on retrieval
# score -- e.g. an active-error-only SQL query should corroborate, not replace,
# a general AGV-state inspection procedure (Section 8 of the fix plan).
_PRIMARY_CAPABILITY_PREFERENCE: tuple[tuple[str, str], ...] = (
    ("agv_state_inspection", "agv_active_error_inspection"),
)
_PRIMARY_PREFERENCE_SCORE_MARGIN = 0.20


def _prefer_broader_primary_capability(
    node: dict[str, Any],
    ranked: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> list[RunbookSearchMatch]:
    if len(ranked) < 2:
        return ranked
    top = ranked[0]
    top_runbook = (runbooks_by_id or {}).get(top.procedure_id)
    top_caps = runbook_derived_capabilities(top_runbook)
    for broad_cap, narrow_cap in _PRIMARY_CAPABILITY_PREFERENCE:
        if narrow_cap not in top_caps or broad_cap in top_caps:
            continue
        for index, candidate in enumerate(ranked[1:], start=1):
            candidate_runbook = (runbooks_by_id or {}).get(candidate.procedure_id)
            candidate_caps = runbook_derived_capabilities(candidate_runbook)
            if broad_cap not in candidate_caps:
                continue
            if top.combined_score - candidate.combined_score > _PRIMARY_PREFERENCE_SCORE_MARGIN:
                break
            reordered = list(ranked)
            reordered.pop(index)
            reordered.insert(0, candidate)
            return reordered
    return ranked


def _allows_capability_multilink(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") not in DIAGNOSTIC_NODE_TYPES:
        return False
    caps = node_expects_capabilities(node)
    if not caps:
        return False
    surfaces = node_expects_surfaces(node)
    return len(surfaces) >= 2 or bool(surfaces & {"wcs_sql", "wcs_api", "event_viewer", "rms_ui"})


def _allows_service_health_bundle(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") not in DIAGNOSTIC_NODE_TYPES:
        return False
    return bool(re.search(r"\b(service|gateway|ignition|optisweep|wcswebapplication)\b", node_check_text(node), re.I))


def _is_distinct_capability_companion_link(
    node: dict[str, Any],
    selected_links: list[dict[str, Any]],
    candidate_link: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> bool:
    """Allow same-surface diagnostic evidence when it adds a missing capability.

    WCS SQL is a single support surface, but separate Helix/SSMS procedures can
    answer different evidence questions. Surface uniqueness alone must not erase
    the second procedure after retrieval has already established that it is valid.
    """
    if str(node.get("node_type") or "") not in DIAGNOSTIC_NODE_TYPES:
        return False
    candidate_id = str(candidate_link.get("procedure_id") or "")
    candidate_runbook = (runbooks_by_id or {}).get(candidate_id) or {}
    if str(candidate_runbook.get("procedure_type") or "").lower() != "diagnostic":
        return False
    node_caps = node_expects_capabilities(node)
    candidate_caps = node_caps & runbook_capability_tags(candidate_runbook)
    if not candidate_caps:
        return False
    covered_caps: set[str] = set()
    has_diagnostic_primary = False
    for selected in selected_links:
        selected_runbook = (runbooks_by_id or {}).get(str(selected.get("procedure_id") or "")) or {}
        if str(selected_runbook.get("procedure_type") or "").lower() == "diagnostic":
            has_diagnostic_primary = True
        covered_caps |= node_caps & runbook_capability_tags(selected_runbook)
    if not has_diagnostic_primary:
        return False
    selected_surfaces: set[str] = set()
    for selected in selected_links:
        selected_runbook = (runbooks_by_id or {}).get(str(selected.get("procedure_id") or "")) or {}
        selected_surfaces |= runbook_access_surfaces(selected_runbook)
    candidate_surfaces = runbook_access_surfaces(candidate_runbook)
    if candidate_caps and candidate_surfaces - selected_surfaces:
        return True
    if candidate_caps - covered_caps:
        return True
    # A specialized active-error query is still useful beside a broader Helix
    # state/status procedure even when both advertise agv_active_errors.  The
    # node contract and earlier filters still keep this scoped to diagnostics
    # that explicitly request active-error evidence.
    candidate_is_specialized_active_error = _is_specialized_active_error_runbook(candidate_runbook)
    if candidate_is_specialized_active_error and node_allows_active_agv_error_sql(node):
        candidate_source = str(candidate_runbook.get("source_id") or "").strip().lower()
        for selected in selected_links:
            selected_runbook = (runbooks_by_id or {}).get(str(selected.get("procedure_id") or "")) or {}
            if not _is_specialized_active_error_runbook(selected_runbook):
                continue
            selected_source = str(selected_runbook.get("source_id") or "").strip().lower()
            if candidate_source and selected_source and candidate_source != selected_source:
                return True
        return any(
            not _is_specialized_active_error_runbook(
                (runbooks_by_id or {}).get(str(selected.get("procedure_id") or ""))
            )
            for selected in selected_links
        )
    return False


def _is_specialized_active_error_runbook(runbook: dict[str, Any] | None) -> bool:
    if not runbook_is_active_agv_error_sql(runbook, None):
        return False
    source_id = str(runbook.get("source_id") or "").strip().lower()
    title = str(runbook.get("title") or "").lower()
    return source_id in {"active_agv_error_query_1", "training_video_day2"} or bool(
        re.search(r"\b(query|corroborat)\w*\b.*\bactive\s+agv\s+error", title)
    )


def _is_capability_surface_companion(
    node: dict[str, Any],
    primary: RunbookSearchMatch,
    candidate: RunbookSearchMatch,
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> bool:
    if candidate.procedure_id == primary.procedure_id:
        return False
    primary_runbook = (runbooks_by_id or {}).get(primary.procedure_id)
    candidate_runbook = (runbooks_by_id or {}).get(candidate.procedure_id)
    node_caps = node_expects_capabilities(node)
    if not node_caps:
        return False
    if not (node_caps & runbook_capability_tags(primary_runbook)):
        return False
    if not (node_caps & runbook_capability_tags(candidate_runbook)):
        return False
    if _is_distinct_capability_companion_link(
        node,
        [{"procedure_id": primary.procedure_id}],
        {"procedure_id": candidate.procedure_id},
        runbooks_by_id=runbooks_by_id,
    ):
        return True
    primary_surfaces = runbook_access_surfaces(primary_runbook)
    candidate_surfaces = runbook_access_surfaces(candidate_runbook)
    if primary_surfaces and candidate_surfaces and not (primary_surfaces & candidate_surfaces):
        return True
    primary_roles = runbook_audience_roles(primary_runbook)
    candidate_roles = runbook_audience_roles(candidate_runbook)
    preferred = node_preferred_audience(node)
    if preferred:
        primary_roles = primary_roles & preferred if primary_roles else preferred
        candidate_roles = candidate_roles & preferred if candidate_roles else preferred
    if primary_roles and candidate_roles and not (primary_roles & candidate_roles):
        return True
    if primary_surfaces != candidate_surfaces:
        return True
    return False


def _is_valid_companion_link(
    node: dict[str, Any],
    primary: RunbookSearchMatch,
    candidate: RunbookSearchMatch,
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> bool:
    if _is_capability_surface_companion(node, primary, candidate, runbooks_by_id=runbooks_by_id):
        return True
    runbook = (runbooks_by_id or {}).get(candidate.procedure_id)
    if runbook_is_fleet_rms_status_check(runbook, candidate):
        return True
    if _allows_isolation_removal_bundle(node) and runbook_is_agv_isolation_or_removal(runbook, candidate):
        return candidate.procedure_id != primary.procedure_id
    if node_is_symptom_pattern_confirmation(node) and runbook_supports_symptom_corroboration(node, runbook, candidate):
        return candidate.procedure_id != primary.procedure_id
    if node_needs_roster_mapping_check(node) and runbook_is_status_check(runbook, candidate):
        return candidate.procedure_id != primary.procedure_id
    if _allows_service_health_bundle(node):
        caps = runbook_capability_tags(runbook)
        text = runbook_match_text(candidate, runbook).lower()
        if caps & {"wcs_service_health", "gateway_health", "windows_service_or_event_log"}:
            return True
        if re.search(r"\b(optisweep|wcswebapplication|windows service|event viewer|ignition gateway)\b", text):
            return True
    return _allows_multiple_runbooks(node, str(node.get("runbook_placeholder") or ""))


def _synthetic_match_from_runbook(
    procedure_id: str,
    runbook: dict[str, Any],
    *,
    combined_score: float = SURFACE_COVERAGE_SYNTHETIC_SCORE,
) -> RunbookSearchMatch:
    metadata = runbook.get("metadata") if isinstance(runbook.get("metadata"), dict) else {}
    return RunbookSearchMatch(
        procedure_id=procedure_id,
        title=str(runbook.get("title") or ""),
        procedure_type=str(runbook.get("procedure_type") or ""),
        cosine_score=0.0,
        jaccard_score=0.0,
        combined_score=combined_score,
        source_type=str(metadata.get("source_type") or ""),
        source_id=str(metadata.get("source_id") or ""),
    )


def _surface_coverage_capability_sets(node: dict[str, Any]) -> tuple[set[str], set[str]]:
    exact = set(node_expects_capabilities(node))
    related = set(exact)
    for cap in exact:
        related |= set(SURFACE_COVERAGE_RELATED_CAPABILITIES.get(cap, frozenset({cap})))
    return exact, related


def _surface_coverage_capability_set(node: dict[str, Any]) -> set[str]:
    _, related = _surface_coverage_capability_sets(node)
    return related


def _surface_coverage_specificity_bonus(
    *,
    surface: str,
    runbook: dict[str, Any] | None,
    node_caps: set[str],
    exact_overlap: bool,
) -> float:
    surfaces = runbook_access_surfaces(runbook)
    if surface not in surfaces:
        return -1.0
    rb_caps = runbook_capability_tags(runbook)
    if runbook_is_active_agv_error_sql(runbook, None) and "agv_active_errors" not in node_caps:
        return -1.0
    if not exact_overlap and not (rb_caps & node_caps):
        if not (rb_caps & _surface_coverage_capability_set({"expects_capability": list(node_caps)})):
            return -1.0
    bonus = 0.0
    if surfaces == {surface}:
        bonus += 0.15
    elif surfaces - {surface}:
        bonus -= 0.04
    overlap = node_caps & rb_caps
    if overlap:
        bonus += 0.08 + (0.10 * (len(overlap) / max(len(node_caps), 1)))
    else:
        bonus -= 0.06
    title = str((runbook or {}).get("title") or "").lower()
    if surface == "wcs_sql" and "agv_active_errors" in node_caps and "active" in title and "error" in title:
        bonus += 0.08
    elif surface == "wcs_sql" and "agv_active_errors" not in node_caps and "active" in title and "error" in title:
        bonus -= 0.20
    return bonus


def _find_surface_coverage_match(
    node: dict[str, Any],
    surface: str,
    *,
    ranked: list[tuple[RunbookSearchMatch, float]] | list[RunbookSearchMatch],
    runbooks_by_id: dict[str, dict[str, Any]],
    exclude_ids: set[str],
) -> tuple[RunbookSearchMatch, float] | None:
    node_caps, related_caps = _surface_coverage_capability_sets(node)
    if not related_caps:
        return None

    ranked_pairs: list[tuple[RunbookSearchMatch, float]] = []
    for item in ranked:
        if isinstance(item, tuple):
            ranked_pairs.append(item)
        else:
            ranked_pairs.append((item, item.combined_score))

    exact_candidates: list[tuple[RunbookSearchMatch, float, bool]] = []
    related_candidates: list[tuple[RunbookSearchMatch, float, bool]] = []
    seen_ids = set(exclude_ids)

    def _consider(match: RunbookSearchMatch, boosted: float) -> None:
        if match.procedure_id in seen_ids:
            return
        runbook = runbooks_by_id.get(match.procedure_id)
        surfaces = runbook_access_surfaces(runbook)
        if surface not in surfaces:
            return
        rb_caps = runbook_capability_tags(runbook)
        exact_overlap = bool(node_caps & rb_caps)
        related_overlap = bool(related_caps & rb_caps)
        if not exact_overlap and not related_overlap:
            return
        if (
            USE_CAPABILITY_TAG_CONSTRAINTS
            and runbook_is_active_agv_error_sql(runbook, match)
            and not node_allows_active_agv_error_sql(node)
        ):
            return
        if runbook_is_wrong_domain_for_node(node, runbook, match):
            return
        confidence, scored, _ = evaluate_link_confidence(
            node,
            match,
            runbook=runbook,
            link_rank=2,
        )
        if confidence == "unresolved":
            if not (exact_overlap or related_overlap):
                return
            confidence = "low"
            scored = max(scored, SURFACE_COVERAGE_SYNTHETIC_SCORE)
        specificity = _surface_coverage_specificity_bonus(
            surface=surface,
            runbook=runbook,
            node_caps=node_caps or related_caps,
            exact_overlap=exact_overlap,
        )
        if specificity < 0:
            return
        score = max(boosted, scored) + specificity
        if not exact_overlap:
            score -= 0.12
        exclusive = surfaces == {surface}
        entry = (match, score, exclusive)
        seen_ids.add(match.procedure_id)
        if exact_overlap:
            exact_candidates.append(entry)
        else:
            related_candidates.append(entry)

    for match, boosted in ranked_pairs:
        _consider(match, boosted)

    for procedure_id, runbook in runbooks_by_id.items():
        if procedure_id in seen_ids or not isinstance(runbook, dict):
            continue
        if surface not in runbook_access_surfaces(runbook):
            continue
        rb_caps = runbook_capability_tags(runbook)
        if not ((node_caps & rb_caps) or (related_caps & rb_caps)):
            continue
        match = _synthetic_match_from_runbook(procedure_id, runbook)
        _consider(match, SURFACE_COVERAGE_SYNTHETIC_SCORE)

    if exact_candidates:
        candidates = exact_candidates
    elif related_candidates and not (
        surface == "wcs_sql" and "agv_active_errors" in node_caps
    ):
        candidates = related_candidates
    else:
        candidates = []
    if not candidates:
        return None
    exclusive = [item for item in candidates if item[2]]
    pool = exclusive or candidates
    best_match, best_score, _ = max(pool, key=lambda item: item[1])
    return best_match, best_score


def _ordered_uncovered_surfaces(expected: set[str], covered: set[str]) -> list[str]:
    uncovered = {surface for surface in expected if surface not in covered}
    ordered = [surface for surface in SURFACE_COVERAGE_PRIORITY if surface in uncovered]
    ordered.extend(sorted(surface for surface in uncovered if surface not in SURFACE_COVERAGE_PRIORITY))
    return ordered


def _covered_surfaces_for_ids(
    procedure_ids: list[str],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> set[str]:
    covered: set[str] = set()
    for procedure_id in procedure_ids:
        covered |= runbook_access_surfaces(runbooks_by_id.get(procedure_id))
    return covered


def _replaceable_alternate_index(
    selected_ids: list[str],
    *,
    expected_surfaces: set[str],
    runbooks_by_id: dict[str, dict[str, Any]],
) -> int | None:
    if len(selected_ids) < 2:
        return None
    surface_owners: dict[str, list[int]] = {}
    for index, procedure_id in enumerate(selected_ids):
        for surface in runbook_access_surfaces(runbooks_by_id.get(procedure_id)) & expected_surfaces:
            surface_owners.setdefault(surface, []).append(index)
    for index in range(len(selected_ids) - 1, 0, -1):
        unique = False
        for owners in surface_owners.values():
            if owners == [index]:
                unique = True
                break
        if not unique:
            return index
    return len(selected_ids) - 1


def _ensure_surface_coverage_selected(
    node: dict[str, Any],
    selected: list[tuple[RunbookSearchMatch, str, list[str], float]],
    ranked: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    max_links: int,
) -> list[tuple[RunbookSearchMatch, str, list[str], float]]:
    if not selected or not _allows_capability_multilink(node):
        return selected
    expected = node_expects_surfaces(node)
    if not expected:
        return selected

    working = list(selected)
    ranked_pairs = [(match, match.combined_score) for match in ranked]
    for _ in range(len(expected)):
        selected_ids = [match.procedure_id for match, _, _, _ in working]
        covered = _covered_surfaces_for_ids(selected_ids, runbooks_by_id=runbooks_by_id)
        uncovered = _ordered_uncovered_surfaces(expected, covered)
        if not uncovered:
            break
        surface = uncovered[0]
        found = _find_surface_coverage_match(
            node,
            surface,
            ranked=ranked_pairs,
            runbooks_by_id=runbooks_by_id,
            exclude_ids=set(selected_ids),
        )
        if found is None:
            break
        match, coverage_score = found
        confidence, boosted, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=runbooks_by_id.get(match.procedure_id),
            link_rank=len(working) + 1,
        )
        # _find_surface_coverage_match already made a considered decision to
        # surface this candidate (its own internal evaluate_link_confidence
        # call applies the surface-coverage synthetic-score floor -- see
        # SURFACE_COVERAGE_SYNTHETIC_SCORE -- when the candidate has real
        # capability overlap, even if the raw/domain-penalized score alone
        # would be unresolved). Don't let this second, independent re-scoring
        # silently discard that decision: trust coverage_score as the floor.
        if confidence == "unresolved":
            confidence = "low"
            boosted = max(boosted, coverage_score)
        entry = (match, confidence, gaps, boosted)
        if len(working) < max_links:
            working.append(entry)
            continue
        replace_at = _replaceable_alternate_index(
            selected_ids,
            expected_surfaces=expected,
            runbooks_by_id=runbooks_by_id,
        )
        if replace_at is None or replace_at <= 0:
            break
        working[replace_at] = entry
    return _upgrade_to_exclusive_surface_selected(
        node,
        working,
        ranked_pairs,
        runbooks_by_id=runbooks_by_id,
        expected=expected,
    )


def _upgrade_to_exclusive_surface_selected(
    node: dict[str, Any],
    selected: list[tuple[RunbookSearchMatch, str, list[str], float]],
    ranked: list[tuple[RunbookSearchMatch, float]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    expected: set[str],
) -> list[tuple[RunbookSearchMatch, str, list[str], float]]:
    working = list(selected)
    for surface in _ordered_uncovered_surfaces(expected, set()):
        selected_ids = [match.procedure_id for match, _, _, _ in working]
        exclusive_present = any(
            runbook_access_surfaces(runbooks_by_id.get(procedure_id)) == {surface}
            for procedure_id in selected_ids
        )
        if exclusive_present:
            continue
        covering = [
            index
            for index, procedure_id in enumerate(selected_ids)
            if surface in runbook_access_surfaces(runbooks_by_id.get(procedure_id))
        ]
        if not covering:
            continue
        found = _find_surface_coverage_match(
            node,
            surface,
            ranked=ranked,
            runbooks_by_id=runbooks_by_id,
            exclude_ids=set(selected_ids),
        )
        if found is None:
            continue
        match, _ = found
        if runbook_access_surfaces(runbooks_by_id.get(match.procedure_id)) != {surface}:
            continue
        replace_at = _exclusive_upgrade_replace_index(
            selected_ids,
            covering_indexes=covering,
            surface=surface,
            expected_surfaces=expected,
            runbooks_by_id=runbooks_by_id,
        )
        if replace_at is None:
            continue
        confidence, boosted, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=runbooks_by_id.get(match.procedure_id),
            link_rank=replace_at + 1,
        )
        if confidence == "unresolved":
            continue
        working[replace_at] = (match, confidence, gaps, boosted)
    return working


def _exclusive_upgrade_replace_index(
    selected_ids: list[str],
    *,
    covering_indexes: list[int],
    surface: str,
    expected_surfaces: set[str],
    runbooks_by_id: dict[str, dict[str, Any]],
) -> int | None:
    for index in reversed(covering_indexes):
        other_ids = [pid for i, pid in enumerate(selected_ids) if i != index]
        other_covered = _covered_surfaces_for_ids(other_ids, runbooks_by_id=runbooks_by_id)
        peer_surfaces = runbook_access_surfaces(runbooks_by_id.get(selected_ids[index]))
        required_from_peer = (peer_surfaces & expected_surfaces) - {surface}
        if required_from_peer and not required_from_peer <= other_covered:
            continue
        return index
    return None


def _ensure_surface_coverage_links(
    node: dict[str, Any],
    links: list[dict[str, Any]],
    ranked: list[tuple[RunbookSearchMatch, float]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    max_links: int,
) -> list[dict[str, Any]]:
    if not links or not _allows_capability_multilink(node):
        return links
    expected = node_expects_surfaces(node)
    if not expected:
        return links

    working = [dict(link) for link in links if isinstance(link, dict)]
    for _ in range(len(expected)):
        selected_ids = [
            str(link.get("procedure_id") or "") for link in working if str(link.get("procedure_id") or "")
        ]
        covered = _covered_surfaces_for_ids(selected_ids, runbooks_by_id=runbooks_by_id)
        uncovered = _ordered_uncovered_surfaces(expected, covered)
        if not uncovered:
            break
        surface = uncovered[0]
        found = _find_surface_coverage_match(
            node,
            surface,
            ranked=ranked,
            runbooks_by_id=runbooks_by_id,
            exclude_ids=set(selected_ids),
        )
        if found is None:
            break
        match, boosted = found
        confidence, scored, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=runbooks_by_id.get(match.procedure_id),
            link_rank=len(working) + 1,
        )
        if confidence == "unresolved":
            break
        entry = {
            "procedure_id": match.procedure_id,
            "link_confidence": confidence,
            "link_rationale": (
                f"Surface coverage companion for `{surface}` "
                f"({match.combined_score:.4f}, boosted {max(boosted, scored):.4f})."
            ),
            "match_gaps": gaps,
            "retrieval_combined_score": match.combined_score,
            "boosted_score": max(boosted, scored),
            "link_rank": len(working) + 1,
            "link_role": "alternate",
        }
        if len(working) < max_links:
            working.append(entry)
            continue
        replace_at = _replaceable_alternate_index(
            selected_ids,
            expected_surfaces=expected,
            runbooks_by_id=runbooks_by_id,
        )
        if replace_at is None or replace_at <= 0:
            break
        working[replace_at] = entry
    working = _upgrade_to_exclusive_surface_links(
        node,
        working,
        ranked,
        runbooks_by_id=runbooks_by_id,
        expected=expected,
    )
    return _annotate_link_roles(working[:max_links])


def _upgrade_to_exclusive_surface_links(
    node: dict[str, Any],
    links: list[dict[str, Any]],
    ranked: list[tuple[RunbookSearchMatch, float]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    expected: set[str],
) -> list[dict[str, Any]]:
    working = [dict(link) for link in links]
    for surface in _ordered_uncovered_surfaces(expected, set()):
        selected_ids = [
            str(link.get("procedure_id") or "") for link in working if str(link.get("procedure_id") or "")
        ]
        exclusive_present = any(
            runbook_access_surfaces(runbooks_by_id.get(procedure_id)) == {surface}
            for procedure_id in selected_ids
        )
        if exclusive_present:
            continue
        covering = [
            index
            for index, procedure_id in enumerate(selected_ids)
            if surface in runbook_access_surfaces(runbooks_by_id.get(procedure_id))
        ]
        if not covering:
            continue
        found = _find_surface_coverage_match(
            node,
            surface,
            ranked=ranked,
            runbooks_by_id=runbooks_by_id,
            exclude_ids=set(selected_ids),
        )
        if found is None:
            continue
        match, boosted = found
        if runbook_access_surfaces(runbooks_by_id.get(match.procedure_id)) != {surface}:
            continue
        replace_at = _exclusive_upgrade_replace_index(
            selected_ids,
            covering_indexes=covering,
            surface=surface,
            expected_surfaces=expected,
            runbooks_by_id=runbooks_by_id,
        )
        if replace_at is None:
            continue
        confidence, scored, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=runbooks_by_id.get(match.procedure_id),
            link_rank=replace_at + 1,
        )
        if confidence == "unresolved":
            continue
        working[replace_at] = {
            "procedure_id": match.procedure_id,
            "link_confidence": confidence,
            "link_rationale": (
                f"Exclusive `{surface}` companion "
                f"({match.combined_score:.4f}, boosted {max(boosted, scored):.4f})."
            ),
            "match_gaps": gaps,
            "retrieval_combined_score": match.combined_score,
            "boosted_score": max(boosted, scored),
            "link_rank": replace_at + 1,
            "link_role": "alternate" if replace_at else "primary",
        }
    return working


def _build_links_from_ranked(
    node: dict[str, Any],
    ranked: list[tuple[RunbookSearchMatch, float]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    links: list[dict[str, Any]] = []
    for rank, (match, boosted) in enumerate(ranked[:MAX_RUNBOOKS_PER_NODE], start=1):
        confidence, _, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=runbooks_by_id.get(match.procedure_id),
            link_rank=rank,
        )
        if confidence == "unresolved":
            continue
        links.append(
            {
                "procedure_id": match.procedure_id,
                "link_confidence": confidence,
                "link_rationale": f"Retrieval match ({match.combined_score:.4f}, boosted {boosted:.4f}).",
                "match_gaps": gaps,
                "retrieval_combined_score": match.combined_score,
                "boosted_score": boosted,
                "link_rank": rank,
            }
        )
    annotated = _annotate_link_roles(links)
    return _ensure_surface_coverage_links(
        node,
        annotated,
        ranked,
        runbooks_by_id=runbooks_by_id,
        max_links=MAX_RUNBOOKS_PER_NODE,
    )


def _companion_links_from_ranked(
    node: dict[str, Any],
    ranked: list[tuple[RunbookSearchMatch, float]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    exclude_ids: set[str],
    start_rank: int,
) -> list[dict[str, Any]]:
    allow_fleet = _allows_fleet_status_bundle(node)
    allow_capability = _allows_capability_multilink(node)
    if not allow_fleet and not allow_capability:
        return []
    primary_match = None
    for match, _ in ranked:
        if match.procedure_id not in exclude_ids:
            primary_match = match
            break
    links: list[dict[str, Any]] = []
    for match, boosted in ranked:
        if match.procedure_id in exclude_ids:
            continue
        runbook = runbooks_by_id.get(match.procedure_id)
        is_fleet = allow_fleet and runbook_is_fleet_rms_status_check(runbook, match)
        is_capability = False
        if allow_capability and primary_match is not None:
            is_capability = _is_capability_surface_companion(
                node,
                primary_match,
                match,
                runbooks_by_id=runbooks_by_id,
            )
        elif allow_capability and capability_tag_overlap(node, runbook):
            is_capability = True
        if not is_fleet and not is_capability:
            continue
        confidence, _, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=runbook,
            link_rank=start_rank + len(links),
        )
        if confidence == "unresolved":
            continue
        rationale = (
            f"Capability/surface alternate ({match.combined_score:.4f}, boosted {boosted:.4f})."
            if is_capability and not is_fleet
            else f"Alternate fleet/RMS status reference ({match.combined_score:.4f}, boosted {boosted:.4f})."
        )
        links.append(
            {
                "procedure_id": match.procedure_id,
                "link_confidence": confidence,
                "link_rationale": rationale,
                "match_gaps": gaps,
                "retrieval_combined_score": match.combined_score,
                "boosted_score": boosted,
                "link_rank": start_rank + len(links),
            }
        )
        if len(links) >= MAX_ALTERNATE_RUNBOOKS:
            break
    return links


def _annotate_link_roles(links: list[dict[str, Any]]) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    for index, link in enumerate(links):
        if not isinstance(link, dict):
            continue
        updated = dict(link)
        updated.setdefault("link_role", "primary" if index == 0 else "alternate")
        updated["link_rank"] = index + 1
        annotated.append(updated)
    return annotated


def _cap_confidence_from_gaps(
    confidence: str,
    *,
    node: dict[str, Any] | None = None,
    match: RunbookSearchMatch | None = None,
    runbook: dict[str, Any] | None = None,
    gaps: list[str] | None = None,
    link_rank: int = 1,
) -> str:
    gap_list = list(gaps or [])
    if node is not None and match is not None and not gap_list:
        gap_list = intent_mismatch_gaps(node, match, runbook)
    if not gap_list:
        return confidence
    if node_is_site_interview_only(node or {}):
        return "unresolved"
    severe = any(
        phrase in gap.lower()
        for gap in gap_list
        for phrase in (
            "site confirmation",
            "site interview",
            "pre-grid-entry",
            "bump exception",
            "not this check-only node",
            "no explicit zone pairing",
            "hospital-diversion",
            "hospital-flow",
            "hospital-lane diversion",
            "no explicit rms roster",
            "roster/mapping",
            "roster or mapping",
            "hospital ui",
            "not symptom-pattern confirmation",
            "pairing validation",
            "zone_pairing_state",
            "hospital_diversion",
            "missing corroboration",
            "catalog gap",
            "wrong catalog family",
            "active agv error sql",
        )
    )
    if severe:
        return SEVERE_GAP_CONFIDENCE_CAP if CONFIDENCE_RANK[confidence] > CONFIDENCE_RANK["low"] else confidence
    if link_rank != 1:
        return confidence
    if CONFIDENCE_RANK[confidence] >= CONFIDENCE_RANK["high"]:
        return "medium"
    return confidence


def _dedupe_gaps(gaps: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for gap in gaps:
        normalized = str(gap).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def node_check_text(node: dict[str, Any]) -> str:
    from shared_pipeline_stages.stage_8.link_scoring import node_check_text as _node_check_text

    return _node_check_text(node)


def _too_similar_to_selected(
    match: RunbookSearchMatch,
    selected: list[tuple[RunbookSearchMatch, str, list[str], float]],
) -> bool:
    for existing, _, _, _ in selected:
        if existing.procedure_id == match.procedure_id:
            return True
        title_a = existing.title.lower()
        title_b = match.title.lower()
        if title_a and title_b and (title_a in title_b or title_b in title_a):
            return True
    return False


def _match_gaps(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    confidence: str,
    *,
    overlap: float = 0.0,
    runbook: dict[str, Any] | None = None,
) -> list[str]:
    gaps = intent_mismatch_gaps(node, match, runbook)
    if match.combined_score < MEDIUM_CONFIDENCE_SCORE:
        gaps.append(f"Retrieval score {match.combined_score:.4f} below medium threshold.")
    if overlap < ANCHOR_MEDIUM_OVERLAP:
        gaps.append("Limited domain-term overlap between placeholder and runbook.")
    placeholder = normalize_placeholder_text(str(node.get("runbook_placeholder") or "")).lower()
    title = match.title.lower()
    if placeholder and title and token_overlap_ratio(placeholder, title) < 0.12:
        gaps.append("Placeholder wording differs materially from matched runbook title.")
    return _dedupe_gaps(gaps)


def token_overlap_ratio(first: str, second: str) -> float:
    first_tokens = set(re.findall(r"[a-z0-9]+", first.lower()))
    second_tokens = set(re.findall(r"[a-z0-9]+", second.lower()))
    if not first_tokens or not second_tokens:
        return 0.0
    return len(first_tokens & second_tokens) / len(first_tokens | second_tokens)


def _terminal_result(outcome_label: str, condition: str) -> str:
    label = str(outcome_label or "").strip().lower()
    text = str(condition or "").strip().lower()
    if "escalat" in label or "escalat" in text or "stop and hand off" in text:
        return "escalation_required"
    if any(term in text for term in ("retriage", "re-triage", "localized", "normal movement", "exit")):
        return "retriage"
    if label in {"unhealthy", "inconclusive", "failure"}:
        return "unresolved"
    return "workflow_complete"


def _mark_terminal_outcomes(outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    marked: list[dict[str, Any]] = []
    seen_node_labels: set[str] = set()
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            continue
        item = dict(outcome)
        label = str(item.get("outcome_label") or "").strip().lower()
        if label in {"healthy", "unhealthy", "inconclusive"}:
            if label in seen_node_labels:
                continue
            seen_node_labels.add(label)
            descriptor = _compact_node_outcome_text(
                str(item.get("descriptor") or item.get("observable_signal") or "")
            )
            item["descriptor"] = descriptor
            item["observable_signal"] = descriptor
        next_node_id = str(item.get("next_node_id") or "").strip()
        if not next_node_id:
            item["terminal_result"] = str(item.get("terminal_result") or "").strip() or _terminal_result(
                str(item.get("outcome_label") or ""),
                str(item.get("descriptor") or item.get("observable_signal") or ""),
            )
        else:
            item["terminal_result"] = ""
        marked.append(item)
    return marked


def _compact_node_outcome_text(text: str, *, max_words: int = 35) -> str:
    normalized = re.sub(r"\s+", " ", str(text or "")).strip()
    if not normalized:
        return "Required evidence is unavailable or cannot be interpreted."
    first_sentence = re.split(r"(?<=[.!?])\s+", normalized, maxsplit=1)[0].strip()
    words = first_sentence.split()
    if len(words) <= max_words:
        return first_sentence
    return " ".join(words[:max_words]).rstrip(" ,;:") + "."


def _outcomes_from_runbook(
    node: dict[str, Any],
    runbook: dict[str, Any],
    procedure_id: str,
    branch_hints: list[dict[str, Any]],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []
    observer, tool_or_view = _evidence_observer_and_tool(node)
    targets = _branch_targets_for_node(
        str(node.get("node_id") or ""),
        branch_hints,
        node=node,
        all_nodes=all_nodes,
    )
    next_node_id = targets.get("unhealthy") or targets.get("healthy") or _next_node_from_hints(
        str(node.get("node_id") or ""), branch_hints
    )
    for condition in runbook.get("healthy_conditions") or []:
        if not isinstance(condition, dict):
            continue
        descriptor = str(condition.get("healthy_condition") or condition.get("description") or "").strip()
        if descriptor:
            outcomes.append(
                {
                    "outcome_label": "healthy",
                    "descriptor": descriptor,
                    "observable_signal": descriptor,
                    "observer": observer,
                    "tool_or_view": tool_or_view,
                    "source": "runbook_healthy_condition",
                    "linked_runbook_id": procedure_id,
                    "linked_step_number": condition.get("step_number"),
                    "next_node_id": targets.get("healthy", next_node_id),
                }
            )
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        healthy = str(step.get("healthy_condition") or "").strip()
        expected = str(step.get("expected_result") or "").strip()
        descriptor = healthy or expected
        if not descriptor or text_contains_incident_specific_detail(descriptor):
            continue
        outcomes.append(
            {
                "outcome_label": "healthy" if healthy else "inconclusive",
                "descriptor": descriptor,
                "observable_signal": descriptor,
                "observer": observer,
                "tool_or_view": tool_or_view,
                "source": "runbook_step",
                "linked_runbook_id": procedure_id,
                "linked_step_number": step.get("step_number"),
                "next_node_id": targets.get("healthy" if healthy else "inconclusive", next_node_id),
            }
        )
    failure_conditions = runbook.get("failure_conditions") or []
    for item in failure_conditions[:3]:
        text = str(item).strip()
        if text:
            outcomes.append(
                {
                    "outcome_label": "unhealthy",
                    "descriptor": text,
                    "observable_signal": text,
                    "observer": observer,
                    "tool_or_view": tool_or_view,
                    "source": "runbook_step",
                    "linked_runbook_id": procedure_id,
                    "linked_step_number": None,
                    "next_node_id": targets.get("unhealthy", next_node_id),
                }
            )
    return outcomes


def _fallback_outcomes_from_node(
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    playbook_context: dict[str, Any] | None = None,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    return _synthesize_node_decision_outcomes(
        node,
        branch_hints,
        playbook_context=playbook_context,
        all_nodes=all_nodes,
    )


def _node_allows_wcs_sql(node: dict[str, Any]) -> bool:
    surfaces = {str(item).strip().lower() for item in node.get("expects_surface") or []}
    if surfaces & {"wcs_sql", "ssms", "helix_db", "wcs_db", "wcs_database"}:
        return True
    text = node_check_text(node).lower()
    return bool(re.search(r"\b(wcs\s*/\s*ssms|ssms|wcs\s+database|helix\s+db|read-only query)\b", text, re.I))


def _evidence_observer_and_tool(node: dict[str, Any]) -> tuple[str, str]:
    surfaces = [str(item).strip().lower() for item in node.get("expects_surface") or [] if str(item).strip()]
    audience = {str(item).strip() for item in node.get("preferred_audience") or [] if str(item).strip()}
    audience |= {str(item).strip() for item in node.get("allowed_roles") or [] if str(item).strip()}
    text = node_check_text(node).lower()

    tools: list[str] = []
    surface_labels = {
        "rms_ui": "RMS / AGV status UI",
        "wcs_sql": "WCS/SSMS (read-only)",
        "wcs_api": "OptiSweep / WCS API",
        "event_viewer": "Windows Event Viewer / services",
        "ignition_gateway": "Ignition gateway",
        "hospital_hmi": "Hospital HMI / lane UI",
        "tipper_hmi": "Tipper HMI / WebVisu",
        "building_acb_hmi": "Building / ACB overview HMI",
        "aveva_hmi": "AVEVA HMI",
        "site_interview": "site interview",
        "physical_floor": "on-site floor / grid",
    }
    for surface in surfaces:
        label = surface_labels.get(surface)
        if label and label not in tools:
            tools.append(label)
    if not tools:
        if re.search(r"\b(event viewer|windows services)\b", text, re.I):
            tools.append("Windows Event Viewer / services")
        if re.search(r"\bignition\b", text, re.I):
            tools.append("Ignition gateway")
        if _node_allows_wcs_sql(node):
            tools.append("WCS/SSMS (read-only)")
        if re.search(r"\b(rms|agv status|fleet|roster|mapping)\b", text, re.I):
            tools.append("RMS / AGV status UI")
        if re.search(r"\b(confirm with the site|site interview|ask the site|site-reported)\b", text, re.I):
            tools.append("site interview")
    if not tools:
        tools.append("named diagnostic tool/view from the node placeholder")

    fortna = audience & {"L1_support", "L2_support", "L3_support", "L4_support"}
    site = "operator" in audience or bool(re.search(r"\b(site|operator|floor)\b", text, re.I))
    if fortna and site:
        observer = "site_or_remote"
    elif fortna:
        observer = "remote"
    elif site:
        observer = "site"
    elif _node_allows_wcs_sql(node) or re.search(r"\b(rms|event viewer|ignition|api)\b", text, re.I):
        observer = "remote"
    else:
        observer = "site_or_remote"
    return observer, " / ".join(tools)


def _synthesize_node_decision_outcomes(
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    playbook_context: dict[str, Any] | None = None,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    node_id = str(node.get("node_id") or "")
    node_type = str(node.get("node_type") or "")
    title = str(node.get("title") or "")
    intent = str(node.get("intent") or node.get("goal") or "")
    expected = str(node.get("expected_or_observed_result") or "").strip()
    if text_contains_incident_specific_detail(expected):
        expected = ""
    outcomes: list[dict[str, Any]] = []
    observer, tool_or_view = _evidence_observer_and_tool(node)

    def add_outcome(label: str, descriptor: str, *, next_node_id: str = "") -> None:
        if not descriptor:
            return
        outcomes.append(
            {
                "outcome_label": label,
                "descriptor": descriptor,
                "observable_signal": descriptor,
                "observer": observer,
                "tool_or_view": tool_or_view,
                "source": "playbook_expected_result",
                "linked_runbook_id": "",
                "linked_step_number": None,
                "next_node_id": next_node_id,
                "terminal_result": "workflow_complete" if not next_node_id else "",
            }
        )

    branch_targets = _branch_targets_for_node(
        node_id,
        branch_hints,
        node=node,
        all_nodes=all_nodes,
    )
    status_views = tool_or_view or "RMS or AGV status views"
    remote_clause = " and/or WCS/SSMS read-only query" if _node_allows_wcs_sql(node) else ""

    if node_type == "diagnostic_decision":
        if node_is_symptom_pattern_confirmation(node):
            uses_site_interview = bool(
                re.search(r"\b(confirm with the site|site interview|ask the site|site-reported)\b", node_check_text(node), re.I)
            )
            healthy_text = (
                f"Site interview and available {status_views} do not corroborate the target pattern "
                "(zone unable to get a pair, AMRs broadly routing to the hospital lane, and recent robot add/remove or replacement activity)."
                if uses_site_interview
                else f"Available {status_views} do not corroborate the target pattern "
                "(zone unable to get a pair, AMRs broadly routing to the hospital lane, and recent robot add/remove or replacement activity)."
            )
            unhealthy_text = (
                f"Site and/or {status_views} corroborate the target symptom pattern: zone pairing failure, hospital-diversion behavior, "
                "and recent robot add/remove or replacement activity."
                if uses_site_interview
                else f"{status_views} corroborate the target symptom pattern: zone pairing failure, hospital-diversion behavior, "
                "and recent robot add/remove or replacement activity."
            )
            add_outcome(
                "healthy",
                healthy_text,
                next_node_id=branch_targets.get("healthy", ""),
            )
            add_outcome(
                "unhealthy",
                unhealthy_text,
                next_node_id=branch_targets.get("unhealthy", branch_targets.get("inconclusive", "")),
            )
            add_outcome(
                "inconclusive",
                expected
                or f"Some symptoms are reported but site confirmation or {status_views} corroboration is incomplete for the full pattern.",
                next_node_id=branch_targets.get("inconclusive", branch_targets.get("unhealthy", "")),
            )
        elif node_needs_roster_mapping_check(node):
            add_outcome(
                "healthy",
                f"No supported abnormal robot roster or mapping state is identified in available {status_views}.",
                next_node_id=branch_targets.get("healthy", ""),
            )
            add_outcome(
                "unhealthy",
                f"A specific robot appears abnormal in {status_views} and is a plausible blocker to normal pairing or fleet behavior.",
                next_node_id=branch_targets.get("unhealthy", ""),
            )
            add_outcome(
                "inconclusive",
                expected
                or f"{status_views} evidence is incomplete or ambiguous and does not yet support a safe corrective action.",
                next_node_id=branch_targets.get("inconclusive", branch_targets.get("unhealthy", "")),
            )
        else:
            add_outcome(
                "healthy",
                f"Checks for '{title}' via {status_views} do not indicate the fault condition being evaluated.",
                next_node_id=branch_targets.get("healthy", ""),
            )
            add_outcome(
                "unhealthy",
                f"Checks for '{title}' via {status_views} indicate the fault condition being evaluated.",
                next_node_id=branch_targets.get("unhealthy", ""),
            )
            add_outcome(
                "inconclusive",
                expected or f"Evidence for '{title}' via {status_views} is incomplete or ambiguous.",
                next_node_id=branch_targets.get("inconclusive", ""),
            )
    elif node_type == "branching_condition":
        add_outcome(
            "healthy",
            "The branch condition is not confirmed; choose the alternate troubleshooting direction.",
            next_node_id=branch_targets.get("healthy", ""),
        )
        add_outcome(
            "unhealthy",
            "The branch condition is confirmed and the flow should continue in the primary direction.",
            next_node_id=branch_targets.get("unhealthy", ""),
        )
        add_outcome(
            "inconclusive",
            expected or "The branch condition is suspected but not yet firmly established.",
            next_node_id=branch_targets.get("inconclusive", branch_targets.get("unhealthy", "")),
        )
    elif node_type == "validation_gate":
        add_outcome(
            "healthy",
            "Recovery validation criteria are met and normal operation appears restored.",
            next_node_id=branch_targets.get("healthy", ""),
        )
        add_outcome(
            "unhealthy",
            "Recovery validation criteria are not met and troubleshooting or escalation should continue.",
            next_node_id=branch_targets.get("unhealthy", ""),
        )
        add_outcome(
            "inconclusive",
            expected or "Recovery cannot yet be confirmed because monitoring is incomplete or observations conflict.",
            next_node_id=branch_targets.get("inconclusive", branch_targets.get("unhealthy", "")),
        )

    labels = {str(item.get("outcome_label") or "") for item in outcomes}
    if "inconclusive" not in labels and expected:
        add_outcome("inconclusive", expected, next_node_id=branch_targets.get("inconclusive", ""))
    return outcomes


def _branch_targets_for_node(
    node_id: str,
    branch_hints: list[dict[str, Any]],
    *,
    node: dict[str, Any] | None = None,
    all_nodes: list[dict[str, Any]] | None = None,
) -> dict[str, str]:
    targets: dict[str, str] = {}
    source_node = node or {"node_id": node_id, "node_type": ""}
    for hint in branch_hints:
        if str(hint.get("from_node_id") or "") != node_id:
            continue
        condition = str(hint.get("condition_or_signal") or "")
        next_node_id = str(hint.get("suggested_next_node_id") or "")
        if not next_node_id:
            continue
        if not _transition_allowed(source_node, next_node_id, branch_hints, all_nodes=all_nodes):
            continue
        outcome = _branch_outcome_for_hint(source_node, condition)
        targets.setdefault(outcome, next_node_id)
    if "unhealthy" not in targets:
        sequential = _next_sequential_diagnostic(source_node, all_nodes=all_nodes)
        if sequential and _transition_allowed(source_node, sequential, branch_hints, all_nodes=all_nodes):
            targets["unhealthy"] = sequential
    if "healthy" not in targets:
        healthy_dest = _infer_healthy_destination(source_node, branch_hints, all_nodes=all_nodes)
        if healthy_dest is not None:
            targets["healthy"] = healthy_dest
    return targets


def _branch_outcome_for_hint(node: dict[str, Any], condition: str) -> str:
    lowered = condition.lower()
    node_type = str(node.get("node_type") or "")
    if _RECOVERY_COMPLETED_PATTERN.search(lowered) or any(
        term in lowered
        for term in [
            "correction completed",
            "no residual",
            "recovery completed",
            "validation criteria are met",
        ]
    ):
        return "healthy"
    if any(
        term in lowered
        for term in [
            "not confirmed",
            "not identified",
            "not clearly",
            "do not match",
            "outside role",
            "no supported",
            "remain unexplained",
        ]
    ):
        return "healthy"
    if any(term in lowered for term in ["unreadable", "does not identify", "inconclusive"]):
        return "inconclusive"
    if node_type == "diagnostic_decision" and node_is_symptom_pattern_confirmation(node):
        if any(
            term in lowered
            for term in [
                "reported",
                "cannot get a pair",
                "diverting",
                "hospital lane",
                "hospital diversion",
            ]
        ):
            return "unhealthy"
    if node_type == "branching_condition" and any(
        term in lowered
        for term in [
            "confirmed or strongly suspected",
            "recent agv replacement",
            "remove activity is confirmed",
        ]
    ):
        return "unhealthy"
    if any(
        term in lowered
        for term in [
            "confirmed",
            "abnormal",
            "persists",
            "unable",
            "cannot",
            "failure",
            "not mapped",
            "isolated",
            "are present",
        ]
    ):
        return "unhealthy"
    if any(term in lowered for term in ["escalat", "unauthorized", "unsafe"]):
        return "escalate"
    if any(term in lowered for term in ["restored", "responsive", "functioning again", "monitoring", "normalized"]):
        return "healthy"
    if any(
        term in lowered
        for term in [
            "cannot get a pair",
            "going to the hospital",
            "hospital diversion",
            "symptom pattern",
            "after recent",
        ]
    ):
        return "inconclusive"
    return _infer_outcome_label(condition)


_AFTER_RECOVERY_PATTERN = re.compile(
    r"\bafter\b.{0,80}\brecovery\b|\bpost[-\s]?recovery\b|\bresidual\b.{0,60}\bafter\b",
    re.IGNORECASE,
)
_RECOVERY_COMPLETED_PATTERN = re.compile(
    r"\brecovery\b.{0,40}\bcompleted\b|\bcompleted\b.{0,40}\brecovery\b|"
    r"\bcorrection completed\b|\bno residual\b",
    re.IGNORECASE,
)
_EXIT_HINT_PATTERN = re.compile(
    r"outside role|escalat|hand ?off|pattern (does )?not (match|indicated)|"
    r"not (this|the) pattern|retriage|unsupported|not confirmed",
    re.IGNORECASE,
)


def _node_text_blob(node: dict[str, Any]) -> str:
    return " ".join(
        str(node.get(key) or "")
        for key in ("title", "intent", "goal", "runbook_placeholder", "needed_runbook_capability")
    )


def _node_requires_recovery_prerequisite(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") == "escalation_gate":
        return False
    return bool(_AFTER_RECOVERY_PATTERN.search(_node_text_blob(node)))


def _is_recovery_node(node: dict[str, Any]) -> bool:
    node_type = str(node.get("node_type") or "")
    text = _node_text_blob(node).lower()
    if node_type == "recovery_phase_marker":
        return True
    if node_type == "procedure_reference" and any(
        term in text for term in ("recover", "restart", "reset", "restore", "correct")
    ):
        return True
    return False


def _is_exit_or_escalation_node(node: dict[str, Any]) -> bool:
    return str(node.get("node_type") or "") == "escalation_gate"


def _nodes_by_id(all_nodes: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    return {
        str(node.get("node_id") or ""): node
        for node in (all_nodes or [])
        if isinstance(node, dict) and str(node.get("node_id") or "")
    }


def _transition_allowed(
    from_node: dict[str, Any],
    next_node_id: str,
    branch_hints: list[dict[str, Any]],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> bool:
    if not next_node_id:
        return True
    from_id = str(from_node.get("node_id") or "")
    if next_node_id == from_id:
        return False
    nodes = _nodes_by_id(all_nodes)
    target = nodes.get(next_node_id)
    if not target:
        return True
    if not _node_requires_recovery_prerequisite(target):
        return True
    if _is_recovery_node(from_node):
        return True
    for hint in branch_hints:
        if str(hint.get("from_node_id") or "") != from_id:
            continue
        if str(hint.get("suggested_next_node_id") or "") != next_node_id:
            continue
        if _RECOVERY_COMPLETED_PATTERN.search(str(hint.get("condition_or_signal") or "")):
            return _is_recovery_node(from_node)
    return False


def _next_sequential_diagnostic(
    node: dict[str, Any],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> str:
    if not all_nodes:
        return ""
    node_id = str(node.get("node_id") or "")
    ordered = sorted(
        [item for item in all_nodes if isinstance(item, dict)],
        key=lambda item: int(item.get("node_order") or 0),
    )
    passed = False
    for item in ordered:
        item_id = str(item.get("node_id") or "")
        if item_id == node_id:
            passed = True
            continue
        if not passed:
            continue
        if str(item.get("node_type") or "") in {
            "diagnostic_decision",
            "branching_condition",
            "procedure_reference",
            "validation_gate",
        }:
            return item_id
    return ""


def _infer_healthy_destination(
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> str:
    node_id = str(node.get("node_id") or "")
    for hint in branch_hints:
        if str(hint.get("from_node_id") or "") != node_id:
            continue
        condition = str(hint.get("condition_or_signal") or "")
        outcome = _branch_outcome_for_hint(node, condition)
        next_node_id = str(hint.get("suggested_next_node_id") or "")
        if outcome == "healthy" and next_node_id and _transition_allowed(
            node, next_node_id, branch_hints, all_nodes=all_nodes
        ):
            return next_node_id

    exit_node = _default_exit_or_escalation_node(branch_hints, all_nodes=all_nodes)
    if exit_node and _transition_allowed(node, exit_node, branch_hints, all_nodes=all_nodes):
        return exit_node

    sequential = _next_sequential_diagnostic(node, all_nodes=all_nodes)
    if sequential and _transition_allowed(node, sequential, branch_hints, all_nodes=all_nodes):
        if str(node.get("node_type") or "") == "branching_condition":
            return sequential
    return ""


def _infer_unhealthy_destination(
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> str:
    node_id = str(node.get("node_id") or "")
    for hint in branch_hints:
        if str(hint.get("from_node_id") or "") != node_id:
            continue
        condition = str(hint.get("condition_or_signal") or "")
        outcome = _branch_outcome_for_hint(node, condition)
        next_node_id = str(hint.get("suggested_next_node_id") or "")
        if outcome in {"unhealthy", "inconclusive"} and next_node_id:
            # _transition_allowed's recovery-prerequisite gate must never be
            # bypassed here -- a keyword match on the hint's condition text
            # (residual/abnormal/fault/recover/...) previously routed into a
            # recovery-gated node anyway when the gate said no, which is
            # exactly the branch (unhealthy/inconclusive) most likely to
            # describe a fault in language that matches those keywords
            # without recovery actually having happened yet. Fall through to
            # the sequential-diagnostic fallback below instead, same as when
            # no hint matches at all.
            if _transition_allowed(node, next_node_id, branch_hints, all_nodes=all_nodes):
                return next_node_id
    sequential = _next_sequential_diagnostic(node, all_nodes=all_nodes)
    if sequential and _transition_allowed(node, sequential, branch_hints, all_nodes=all_nodes):
        return sequential
    return ""


def _infer_complementary_branches(
    node: dict[str, Any],
    existing: list[dict[str, Any]],
    branch_hints: list[dict[str, Any]],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    node_id = str(node.get("node_id") or "")
    node_type = str(node.get("node_type") or "")
    complementary: list[dict[str, Any]] = []
    existing_keys = {
        (str(branch.get("outcome") or ""), str(branch.get("next_node_id") or ""))
        for branch in existing
        if isinstance(branch, dict)
    }
    existing_outcomes = {str(branch.get("outcome") or "") for branch in existing if isinstance(branch, dict)}

    def add_branch(
        *,
        branch_id: str,
        condition_label: str,
        outcome: str,
        next_node_id: str,
        source_refs: list[Any] | None = None,
    ) -> None:
        key = (outcome, next_node_id)
        if key in existing_keys:
            return
        complementary.append(
            {
                "branch_id": branch_id,
                "condition_label": condition_label,
                "condition_descriptor": condition_label,
                "outcome": outcome,
                "next_node_id": next_node_id,
                "terminal_result": "workflow_complete" if not next_node_id else "",
                "source_branch_hint_ids": [],
                "linked_runbook_step_ref": "",
                "source_refs": source_refs or [],
            }
        )
        existing_keys.add(key)
        existing_outcomes.add(outcome)

    if node_type in {"diagnostic_decision", "branching_condition"} and "healthy" not in existing_outcomes:
        healthy_dest = _infer_healthy_destination(node, branch_hints, all_nodes=all_nodes)
        label = (
            "Branch condition is not confirmed"
            if node_type == "branching_condition"
            else "Diagnostic check does not indicate the fault condition"
        )
        add_branch(
            branch_id=f"{node_id}_branch_inferred_healthy",
            condition_label=label,
            outcome="healthy",
            next_node_id=healthy_dest,
        )

    if node_type in {"diagnostic_decision", "branching_condition"} and "unhealthy" not in existing_outcomes:
        unhealthy_dest = _infer_unhealthy_destination(node, branch_hints, all_nodes=all_nodes)
        if unhealthy_dest:
            label = (
                "Branch condition is confirmed"
                if node_type == "branching_condition"
                else "Diagnostic check indicates the fault condition"
            )
            add_branch(
                branch_id=f"{node_id}_branch_inferred_unhealthy",
                condition_label=label,
                outcome="unhealthy",
                next_node_id=unhealthy_dest,
            )

    if node_type == "validation_gate":
        exit_node = _default_exit_or_escalation_node(branch_hints, all_nodes=all_nodes)
        if exit_node and "unhealthy" not in existing_outcomes:
            add_branch(
                branch_id=f"{node_id}_branch_inferred_unhealthy",
                condition_label="Recovery validation criteria are not met",
                outcome="unhealthy",
                next_node_id=exit_node,
            )
        if "healthy" not in existing_outcomes:
            add_branch(
                branch_id=f"{node_id}_branch_inferred_healthy",
                condition_label="Recovery validation criteria are met",
                outcome="healthy",
                next_node_id="",
            )

    if node_type in {"diagnostic_decision", "validation_gate", "procedure_reference"}:
        for hint in branch_hints:
            if str(hint.get("from_node_id") or "") != node_id:
                continue
            outcome = _branch_outcome_for_hint(node, str(hint.get("condition_or_signal") or ""))
            next_node_id = str(hint.get("suggested_next_node_id") or "")
            if not next_node_id:
                continue
            if not _transition_allowed(node, next_node_id, branch_hints, all_nodes=all_nodes):
                continue
            add_branch(
                branch_id=f"{node_id}_branch_hint_{len(complementary) + 1}",
                condition_label=str(hint.get("condition_or_signal") or ""),
                outcome=outcome,
                next_node_id=next_node_id,
                source_refs=hint.get("source_refs") or [],
            )
    return complementary


def _default_exit_or_escalation_node(
    branch_hints: list[dict[str, Any]],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> str:
    nodes = _nodes_by_id(all_nodes)
    for hint in branch_hints:
        condition = str(hint.get("condition_or_signal") or "")
        next_node_id = str(hint.get("suggested_next_node_id") or "")
        if not next_node_id:
            continue
        if not _EXIT_HINT_PATTERN.search(condition) and "outside role" not in condition.lower():
            continue
        target = nodes.get(next_node_id)
        if target is None:
            return next_node_id
        if _is_exit_or_escalation_node(target) or not _node_requires_recovery_prerequisite(target):
            return next_node_id
    for node in all_nodes or []:
        if isinstance(node, dict) and _is_exit_or_escalation_node(node):
            return str(node.get("node_id") or "")
    return ""


def _sanitize_branches(
    node: dict[str, Any],
    branches: list[dict[str, Any]],
    branch_hints: list[dict[str, Any]],
    *,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    node_id = str(node.get("node_id") or "")
    cleaned: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for branch in branches:
        if not isinstance(branch, dict):
            continue
        item = dict(branch)
        next_node_id = str(item.get("next_node_id") or "")
        if next_node_id == node_id:
            label = str(item.get("condition_label") or "").lower()
            if "wait" not in label and "retry" not in label and "monitor" not in label:
                item["next_node_id"] = ""
                next_node_id = ""
        if next_node_id and not _transition_allowed(node, next_node_id, branch_hints, all_nodes=all_nodes):
            if str(item.get("outcome") or "") == "healthy":
                item["next_node_id"] = _infer_healthy_destination(node, branch_hints, all_nodes=all_nodes)
            else:
                item["next_node_id"] = _infer_unhealthy_destination(node, branch_hints, all_nodes=all_nodes)
                if item["next_node_id"] == next_node_id:
                    item["next_node_id"] = ""
            next_node_id = str(item.get("next_node_id") or "")
        if not next_node_id:
            if str(item.get("outcome") or "").lower() == "unhealthy":
                inferred = _infer_unhealthy_destination(node, branch_hints, all_nodes=all_nodes)
                if inferred and inferred != node_id:
                    item["next_node_id"] = inferred
                    next_node_id = inferred
        if not next_node_id:
            item["terminal_result"] = str(item.get("terminal_result") or "").strip() or _terminal_result(
                str(item.get("outcome") or ""),
                str(item.get("condition_label") or item.get("condition_descriptor") or ""),
            )
        else:
            item["terminal_result"] = ""
        key = (
            str(item.get("outcome") or ""),
            str(item.get("next_node_id") or ""),
            str(item.get("condition_label") or item.get("condition_descriptor") or "").strip().lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
    return cleaned


def sanitize_playbook_branch_graph(playbook: dict[str, Any]) -> dict[str, Any]:
    """Drop empty/duplicate playbook-level branch rows; keep node-level branches authoritative."""
    node_ids = {
        str(node.get("node_id") or "")
        for node in playbook.get("nodes") or []
        if isinstance(node, dict) and str(node.get("node_id") or "")
    }
    node_edge_keys: set[tuple[str, str, str, str]] = set()
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        from_id = str(node.get("node_id") or "")
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            node_edge_keys.add(
                (
                    from_id,
                    str(branch.get("outcome") or ""),
                    str(branch.get("next_node_id") or ""),
                    str(branch.get("condition_label") or branch.get("condition_descriptor") or "").strip().lower(),
                )
            )

    cleaned_playbook_branches: list[dict[str, Any]] = []
    seen_playbook: set[tuple[str, str, str, str]] = set()
    for branch in playbook.get("branches") or []:
        if not isinstance(branch, dict):
            continue
        from_id = str(branch.get("from_node_id") or "").strip()
        if not from_id or from_id not in node_ids:
            continue
        key = (
            from_id,
            str(branch.get("outcome") or ""),
            str(branch.get("next_node_id") or ""),
            str(branch.get("condition_label") or branch.get("condition_descriptor") or "").strip().lower(),
        )
        if key in node_edge_keys or key in seen_playbook:
            continue
        seen_playbook.add(key)
        cleaned_branch = dict(branch)
        next_node_id = str(cleaned_branch.get("next_node_id") or "").strip()
        if not next_node_id:
            cleaned_branch["terminal_result"] = str(cleaned_branch.get("terminal_result") or "").strip() or _terminal_result(
                str(cleaned_branch.get("outcome") or ""),
                str(cleaned_branch.get("condition_label") or cleaned_branch.get("condition_descriptor") or ""),
            )
        else:
            cleaned_branch["terminal_result"] = ""
        cleaned_playbook_branches.append(cleaned_branch)
    playbook["branches"] = cleaned_playbook_branches
    return playbook


def repair_playbook_graph_cycles(playbook: dict[str, Any]) -> list[str]:
    nodes = [
        node for node in playbook.get("nodes") or []
        if isinstance(node, dict) and str(node.get("node_id") or "").strip()
    ]
    node_ids = {str(node.get("node_id")) for node in nodes}
    edges: dict[str, list[tuple[str, dict[str, Any]]]] = {node_id: [] for node_id in node_ids}
    for node in nodes:
        node_id = str(node.get("node_id"))
        for field in ("decision_outcomes", "branches"):
            for edge in node.get(field) or []:
                if not isinstance(edge, dict):
                    continue
                target = str(edge.get("next_node_id") or "").strip()
                if target in node_ids:
                    edges[node_id].append((target, edge))
    repaired: list[str] = []
    while True:
        visiting: set[str] = set()
        visited: set[str] = set()
        back_edge: tuple[str, dict[str, Any]] | None = None

        def visit(node_id: str) -> bool:
            nonlocal back_edge
            visiting.add(node_id)
            for target, edge in edges.get(node_id, []):
                if target in visiting:
                    back_edge = (node_id, edge)
                    return True
                if target not in visited and visit(target):
                    return True
            visiting.remove(node_id)
            visited.add(node_id)
            return False

        if not any(node_id not in visited and visit(node_id) for node_id in sorted(node_ids)):
            break
        if back_edge is None:
            break
        from_node, edge = back_edge
        target = str(edge.get("next_node_id") or "")
        edge["next_node_id"] = None
        edge["terminal_result"] = (
            str(edge.get("terminal_result") or "").strip()
            or "Stop this branch and escalate for SME review; the workflow would otherwise cycle."
        )
        repaired.append(f"{from_node}->{target}")
        edges[from_node] = [
            (candidate, item)
            for candidate, item in edges.get(from_node, [])
            if item is not edge
        ]
    return repaired


def attach_catalog_gaps(node: dict[str, Any]) -> dict[str, Any]:
    """Attach node-level catalog_gaps when unresolved or when links still miss expected capabilities."""
    links = [link for link in (node.get("runbook_links") or []) if isinstance(link, dict)]
    if not links:
        node["catalog_gaps"] = unresolved_catalog_gaps(node)
        return node
    aggregated: list[str] = []
    seen: set[str] = set()
    for link in links:
        for gap in link.get("match_gaps") or []:
            text = str(gap).strip()
            if not text or text in seen:
                continue
            if "missing corroboration" in text.lower() or "catalog gap" in text.lower() or "wrong catalog" in text.lower():
                seen.add(text)
                aggregated.append(text)
    if aggregated:
        node["catalog_gaps"] = aggregated
    elif "catalog_gaps" in node and not node.get("catalog_gaps"):
        node.pop("catalog_gaps", None)
    return node

def _linked_runbooks_support_outcomes(
    node: dict[str, Any],
    linked_runbook_ids: list[str],
    runbooks_by_id: dict[str, dict[str, Any]],
) -> bool:
    if node_is_site_interview_only(node):
        return False
    for procedure_id in linked_runbook_ids:
        runbook = runbooks_by_id.get(procedure_id, {})
        match = runbook_as_match(runbook) if runbook else None
        if not match:
            continue
        if runbook_is_hospital_ui_reference(runbook, match) and (
            node_needs_roster_mapping_check(node) or node_is_symptom_pattern_confirmation(node)
        ):
            return False
        if node_needs_isolation_or_removal(node) and runbook_is_bump_fault_recovery(runbook, match):
            return False
        if node_needs_roster_mapping_check(node) and not runbook_is_agv_fleet_related(runbook, match):
            return False
        if node_needs_agv_fleet_domain(node) and runbook_is_unrelated_equipment(runbook, match):
            return False
    return bool(linked_runbook_ids)


def _merge_outcome_sets(primary: list[dict[str, Any]], secondary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = list(primary)
    primary_labels = {str(item.get("outcome_label") or "") for item in primary}
    seen = {(str(item.get("outcome_label") or ""), str(item.get("descriptor") or "")) for item in primary}
    for item in secondary:
        label = str(item.get("outcome_label") or "")
        descriptor = str(item.get("descriptor") or "")
        if text_contains_incident_specific_detail(descriptor):
            continue
        if label in primary_labels and str(item.get("source") or "") == "playbook_expected_result":
            continue
        key = (label, descriptor)
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return merged


def _ensure_outcome_coverage(
    outcomes: list[dict[str, Any]],
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
    linked_runbook_ids: list[str] | None = None,
    all_nodes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    labels = {str(item.get("outcome_label") or "") for item in outcomes}
    targets = _branch_targets_for_node(
        str(node.get("node_id") or ""),
        branch_hints,
        node=node,
        all_nodes=all_nodes,
    )
    next_node_id = targets.get("unhealthy") or targets.get("healthy") or _next_node_from_hints(
        str(node.get("node_id") or ""), branch_hints
    )
    if "healthy" not in labels:
        for procedure_id in linked_runbook_ids or []:
            runbook = (runbooks_by_id or {}).get(procedure_id, {})
            for item in runbook.get("success_criteria") or []:
                text = str(item).strip()
                if text:
                    outcomes.append(
                        {
                            "outcome_label": "healthy",
                            "descriptor": text,
                            "observable_signal": text,
                            "source": "runbook_step",
                            "linked_runbook_id": procedure_id,
                            "linked_step_number": None,
                            "next_node_id": targets.get("healthy", next_node_id),
                        }
                    )
                    labels.add("healthy")
                    break
            if "healthy" in labels:
                break
    if "unhealthy" not in labels:
        for procedure_id in linked_runbook_ids or []:
            runbook = (runbooks_by_id or {}).get(procedure_id, {})
            for item in runbook.get("failure_conditions") or []:
                text = str(item).strip()
                if text:
                    outcomes.append(
                        {
                            "outcome_label": "unhealthy",
                            "descriptor": text,
                            "observable_signal": text,
                            "source": "runbook_step",
                            "linked_runbook_id": procedure_id,
                            "linked_step_number": None,
                            "next_node_id": targets.get("unhealthy", next_node_id),
                        }
                    )
                    labels.add("unhealthy")
                    break
            if "unhealthy" in labels:
                break
    if "inconclusive" not in labels:
        expected = str(node.get("expected_or_observed_result") or "").strip()
        if text_contains_incident_specific_detail(expected):
            expected = ""
        descriptor = expected or "Observed state is unclear or cannot be confirmed from available evidence."
        outcomes.append(
            {
                "outcome_label": "inconclusive",
                "descriptor": descriptor,
                "observable_signal": descriptor,
                "source": "playbook_expected_result",
                "linked_runbook_id": "",
                "linked_step_number": None,
                "next_node_id": targets.get("inconclusive", next_node_id),
            }
        )
    return outcomes


def _next_node_from_hints(node_id: str, branch_hints: list[dict[str, Any]]) -> str:
    for hint in branch_hints:
        if str(hint.get("from_node_id") or "") == node_id:
            return str(hint.get("suggested_next_node_id") or "")
    return ""


def _infer_outcome_label(condition: str) -> str:
    lowered = condition.lower()
    if any(term in lowered for term in ["fail", "not responsive", "abnormal", "error", "blocked", "unable"]):
        return "unhealthy"
    if any(term in lowered for term in ["escalat", "unauthorized", "unsafe"]):
        return "escalate"
    if any(term in lowered for term in ["confirm", "healthy", "responsive", "recovered", "visible"]):
        return "healthy"
    return "inconclusive"
