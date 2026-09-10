from __future__ import annotations

import re
import os
from typing import Any

from shared_pipeline_stages.stage_8.capability_derivation import (
    capability_domain_adjustment,
    derive_retrieval_request,
)
from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch

USE_CAPABILITY_TAG_CONSTRAINTS = (
    str(os.getenv("STAGE8_USE_CAPABILITY_TAG_CONSTRAINTS", "0")).strip().lower()
    in {"1", "true", "yes", "on"}
)

# Reduced from the original +0.45/+0.18 flat keyword bonus (Section 5 of the
# fix plan): a single keyword-overlap bonus must not dominate the score, and
# is only granted when capability_domain_adjustment() finds no domain-rule
# objection for this candidate.
INTENT_KEYWORD_BONUS = 0.10
INTENT_KEYWORD_RECOVERY_BONUS = 0.06

PLACEHOLDER_BOILERPLATE = re.compile(
    r"^(procedure needed to|runbook needed to|steps needed to|check needed to)\s+",
    re.IGNORECASE,
)

CHECK_NODE_PATTERN = re.compile(
    r"\b(determine|check|whether|verify|inspect|review|confirm|assess|identify whether)\b",
    re.IGNORECASE,
)

RECOVERY_PREP_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"before entering|entering the grid|inside the grid|for agv recovery|"
    r"gather.*fault|prepare.*recovery|physical agv recovery|dance floor"
    r")\b",
    re.IGNORECASE,
)

STATUS_CHECK_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"check overall system|system fault|active agv fault|inspect.*rms|"
    r"review.*rms|determine whether.*fault|roster|map monitor|system errors|"
    r"fleet status|agv status screen|agv locations|error codes"
    r")\b",
    re.IGNORECASE,
)

FLEET_RMS_STATUS_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"overall system rms|overall system agv status|agv status screen|"
    r"fleet status|active agv fault|agv locations|current error codes"
    r")\b",
    re.IGNORECASE,
)

BUMP_EXCEPTION_RUNBOOK_PATTERN = re.compile(
    r"\b(bump exception|exception code 21057|exception code 21060|bump fault screen)\b",
    re.IGNORECASE,
)

SITE_INTERVIEW_PLACEHOLDER_PATTERN = re.compile(
    r"\b("
    r"confirm with the site|site-reported|site reported|ask the site|"
    r"from the site|site symptom|site handling history|site confirmation"
    r")\b",
    re.IGNORECASE,
)

FLEET_INSPECTION_NODE_PATTERN = re.compile(
    r"\b("
    r"inspect.*rms|rms.*inspect|fleet|roster|mapping|agv status|"
    r"overall system rms|overall system agv|error codes|robot roster"
    r")\b",
    re.IGNORECASE,
)

AGV_FLEET_NODE_PATTERN = re.compile(
    r"\b("
    r"agv|amr|robot|rms|roster|mapping|pair|hospital lane|hospital workflow|"
    r"fleet status|fleet overview|fleet rms|agv status|agv fleet|robot roster|"
    r"unable to get a pair|hospital diversion|hospital lane"
    r")\b",
    re.IGNORECASE,
)

AGV_RECOVERY_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"remove.*agv|agv.*remove|recover agv|add.*agv|remove.*robot|"
    r"agv from the system|agv from the floor|hospital.*agv"
    r")\b",
    re.IGNORECASE,
)

UNRELATED_EQUIPMENT_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"tipper|operator station|clink|clearlink|z-axis|axis fault|visu_data|"
    r"cable carrier|end stop|teknic|hospital hmi alarm|stacklight|sorter|"
    r"acb system statistics|hospital station status"
    r")\b",
    re.IGNORECASE,
)

HOSPITAL_UI_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"hospital hmi|hospital.*diagnostics|io diagnostics|"
    r"stacklight|hospital hmi alarm|hospital.*alarms screen|"
    r"acb system statistics|hospital station status|hospital station and its stacklight"
    r")\b",
    re.IGNORECASE,
)

BUMP_FAULT_RECOVERY_RUNBOOK_PATTERN = re.compile(
    r"\b(bump fault|recover an agv from a bump|bump exception code 21057|bump exception code 21060)\b",
    re.IGNORECASE,
)

AGV_ISOLATION_REMOVAL_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"remove.*agv|agv.*remov|remove.*robot|robot.*remov|isolation|out of service|"
    r"remove.*from the active|remove.*from the floor|remove.*from the system"
    r")\b",
    re.IGNORECASE,
)

SITE_HISTORY_BRANCH_PATTERN = re.compile(
    r"\b("
    r"site-reported|site reported|site handling history|recent site-reported|"
    r"incident questioning|branching rubric|decision rubric|"
    r"recent agv replacement|remove/add history|recent robot handling|"
    r"return-through-hospital activity"
    r")\b",
    re.IGNORECASE,
)

ESCALATION_HANDOFF_PATTERN = re.compile(
    r"\b(escalation handoff|prepare an escalation|escalate if|stop and escalate)\b",
    re.IGNORECASE,
)

SYMPTOM_PATTERN_CONFIRMATION_PATTERN = re.compile(
    r"\b("
    r"pairing.?failure|hospital.?diversion|unable to get a pair|"
    r"zone.*pair|amrs.*hospital|hospital lane"
    r")\b.*\b(pattern|symptom)\b|\b(confirm|corroborate)\b.*\b("
    r"pairing.?failure|hospital.?diversion|unable to get a pair|"
    r"zone.*pair|amrs.*hospital|hospital lane"
    r")\b",
    re.IGNORECASE,
)

ISOLATION_REMOVAL_NODE_PATTERN = re.compile(
    r"\b(isolation|removal|remove from the active|remove.*robot)\b",
    re.IGNORECASE,
)

MOTIONLESS_FLOOR_NODE_PATTERN = re.compile(
    r"\b(motionless|on the floor|faulted.*floor)\b",
    re.IGNORECASE,
)

MOTIONLESS_FLOOR_RUNBOOK_PATTERN = re.compile(
    r"\b(motionless|on the floor|faulted.*floor)\b",
    re.IGNORECASE,
)

GENERIC_AGV_REMOVAL_RUNBOOK_PATTERN = re.compile(
    r"\b(remove.*agv.*system|remove.*robot.*selection|remove an agv from the system|api screen)\b",
    re.IGNORECASE,
)

PAIRING_VALIDATION_NODE_PATTERN = re.compile(
    r"\b(pair|pairing|hospital lane|hospital diversion|hospital workflow|fleet behavior)\b",
    re.IGNORECASE,
)

INFRA_DOMAIN_PATTERNS: dict[str, re.Pattern[str]] = {
    "event_viewer": re.compile(
        r"\b(event viewer|application log|system log|7031|service control manager|clustered application)\b",
        re.IGNORECASE,
    ),
    "ignition": re.compile(
        r"\b(ignition|gateway health|systems overview|memory trend|gateway responsiveness)\b",
        re.IGNORECASE,
    ),
    "optisweep": re.compile(
        r"\b(optisweep|wcswebapp|wcs web app|getagvstatuses|get agv status)\b",
        re.IGNORECASE,
    ),
    "windows_services": re.compile(
        r"\b(windows services|services\.msc|service failure|service recovery)\b",
        re.IGNORECASE,
    ),
}

RUNBOOK_INFRA_DOMAIN_PATTERNS = INFRA_DOMAIN_PATTERNS

VISU_OPERATOR_RUNBOOK_PATTERN = re.compile(
    r"\b(visu_io|visu_data|operator station|tipper fault)\b",
    re.IGNORECASE,
)

INCIDENT_SPECIFIC_DETAIL_PATTERN = re.compile(
    r"\b("
    r"zone\s*\d+|robot\s*\d+|amr\s*\d+|agv\s*\d+|"
    r"in this incident|this incident,|the site reported zone"
    r")\b",
    re.IGNORECASE,
)

GRID_ENTRY_NODE_PATTERN = re.compile(
    r"\b("
    r"entering the grid|inside the grid|before entering|dance floor|grid entry|"
    r"physical agv recovery|remove from the floor"
    r")\b",
    re.IGNORECASE,
)

ROSTER_MAPPING_NODE_PATTERN = re.compile(
    r"\b("
    r"roster|mapping|not mapped|map monitor|fleet roster|robot roster|"
    r"abnormal.*robot|mapping state"
    r")\b",
    re.IGNORECASE,
)

HOSPITAL_FLOW_NODE_PATTERN = re.compile(
    r"\b("
    r"hospital lane|hospital diversion|hospital workflow|hospital induct|"
    r"hospital extract|hospital tote|hospital station|hospital queue|"
    r"tote induct|tote extract|induct.*flow|hospital flow"
    r")\b",
    re.IGNORECASE,
)

SEQUENCE_BACKFILL_NODE_PATTERN = re.compile(
    r"\b("
    r"backfill|out of sequence|sequence.*(pair|gap)|exchange.*sequence|"
    r"bag.?out.*sequence|trailing agv|shutdown queue sequence|"
    r"exchange.*backfill|tote association"
    r")\b",
    re.IGNORECASE,
)

MANUAL_SOURCE_TYPES = frozenset({"manual", "sop", "sme"})

DOMAIN_ANCHORS: dict[str, tuple[str, ...]] = {
    "event viewer": ("event viewer", "7031", "service control manager", "application log", "system log"),
    "optisweep": ("optisweep", "getagvstatuses", "get agv status"),
    "ignition": ("ignition", "gateway", "systems overview"),
    "rms": ("rms", "geek+", "overall system", "robot roster", "agv fault", "system fault"),
    "hmi": ("hmi", ".net control", "question mark", "blank state"),
    "windows services": ("windows services", "services.msc", "service state"),
    "agv": ("agv", "robot", "fleet", "out of sync", "roster", "mapping"),
    "hospital": ("hospital", "tote", "hospital lane"),
    "api": ("api", "endpoint", "http", "response", "getagvstatuses"),
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "whether",
    "needed",
    "procedure",
    "runbook",
    "using",
    "approved",
    "support",
    "site",
    "check",
    "confirm",
    "inspect",
    "review",
    "determine",
}

PROCEDURE_TYPE_PREFERRED: dict[str, tuple[str, ...]] = {
    "diagnostic_decision": ("diagnostic", "reference", "monitoring"),
    "branching_condition": ("diagnostic", "reference", "monitoring"),
    "validation_gate": ("diagnostic", "monitoring", "reference"),
    "procedure_reference": ("recovery", "operation", "diagnostic"),
    "escalation_gate": ("reference", "diagnostic"),
    "recovery_phase_marker": ("reference", "monitoring", "recovery"),
}

INTENT_OVERRIDE_MARGIN = 0.08

CANONICAL_SOURCE_BOOST: dict[str, float] = {
    "manual": 0.08,
    "sop": 0.07,
    "sme": 0.06,
}

TRAINING_SOURCE_TYPES = frozenset(
    {"training_video", "training_slide", "training_transcript"}
)
TRAINING_SOURCE_PENALTY = -0.06


def normalize_placeholder_text(text: str) -> str:
    cleaned = PLACEHOLDER_BOILERPLATE.sub("", str(text or "").strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _id_set(values: Any) -> set[str]:
    return {str(item).strip() for item in (values or []) if str(item or "").strip()}


def node_expects_capabilities(node: dict[str, Any]) -> set[str]:
    # `required_evidence_concepts` and `expects_capability` are independent
    # fields (see stage5 normalization: expects_capability is a passthrough
    # of required_evidence_concepts historically, but a node can carry
    # capability ids in one that never made it into the other) -- `or`
    # between them previously dropped one entirely whenever the other was
    # populated, even when they held different values. Union both.
    values = set(node.get("required_evidence_concepts") or []) | set(node.get("expects_capability") or [])
    values.update(
        str(item.get("id") or item.get("capability") or "")
        for item in node.get("ontology_capabilities") or []
        if isinstance(item, dict)
    )
    return {
        value.split(":", 1)[1] if value.startswith("capability:") else value
        for value in _id_set(values)
    }


def node_expects_surfaces(node: dict[str, Any]) -> set[str]:
    surfaces = _id_set(node.get("expects_surface"))
    for item in node.get("ontology_capabilities") or []:
        if not isinstance(item, dict):
            continue
        contract = item.get("support_contract")
        if not isinstance(contract, dict):
            continue
        surfaces.update(
            str(surface)
            for surface in contract.get("diagnostic_surfaces") or []
            if str(surface).strip()
        )
    return surfaces


def node_preferred_audience(node: dict[str, Any]) -> set[str]:
    preferred = _id_set(node.get("preferred_audience"))
    if preferred:
        return preferred
    return _id_set(node.get("allowed_roles"))


def runbook_capability_tags(runbook: dict[str, Any] | None) -> set[str]:
    if not isinstance(runbook, dict):
        return set()
    return _id_set(runbook.get("capability_tags"))


def runbook_access_surfaces(runbook: dict[str, Any] | None) -> set[str]:
    if not isinstance(runbook, dict):
        return set()
    return _id_set(runbook.get("access_surface"))


def runbook_audience_roles(runbook: dict[str, Any] | None) -> set[str]:
    if not isinstance(runbook, dict):
        return set()
    roles = _id_set(runbook.get("audience_roles"))
    primary = str(runbook.get("role_required") or runbook.get("responsible_role") or "").strip()
    if primary:
        roles.add(primary)
    return roles


def capability_tag_overlap(node: dict[str, Any], runbook: dict[str, Any] | None) -> set[str]:
    return node_expects_capabilities(node) & runbook_capability_tags(runbook)


def capability_overlap_adjustment(
    node: dict[str, Any],
    runbook: dict[str, Any] | None,
) -> float:
    expects = node_expects_capabilities(node)
    caps = runbook_capability_tags(runbook)
    if not expects or not caps:
        return 0.0
    overlap = expects & caps
    if not overlap:
        penalty = -0.14
        if runbook_is_active_agv_error_sql(runbook, None) and "agv_active_errors" not in expects:
            penalty -= 0.12
        return penalty
    coverage_ratio = len(overlap) / max(len(expects), 1)
    adjustment = 0.10 + (0.12 * coverage_ratio)
    if runbook_is_active_agv_error_sql(runbook, None) and "agv_active_errors" not in expects:
        adjustment -= 0.22
    node_surfaces = node_expects_surfaces(node)
    rb_surfaces = runbook_access_surfaces(runbook)
    if node_surfaces and rb_surfaces:
        if node_surfaces & rb_surfaces:
            adjustment += 0.10
        else:
            adjustment += 0.02
    preferred = node_preferred_audience(node)
    audience = runbook_audience_roles(runbook)
    if preferred and audience and (preferred & audience):
        adjustment += 0.05
    if (
        "physical_floor" in rb_surfaces
        and "physical_floor" not in node_surfaces
        and preferred
        and not (preferred & {"operator", "on_site"})
    ):
        adjustment -= 0.18
    return adjustment


def surface_hint_adjustment(
    node: dict[str, Any],
    runbook: dict[str, Any] | None,
) -> float:
    node_surfaces = node_expects_surfaces(node)
    rb_surfaces = runbook_access_surfaces(runbook)
    adjustment = 0.0
    if node_surfaces and rb_surfaces:
        adjustment += 0.08 if node_surfaces & rb_surfaces else -0.02
    preferred_surfaces = [
        str(surface).strip()
        for item in node.get("ontology_capabilities") or []
        if isinstance(item, dict)
        and isinstance(item.get("support_contract"), dict)
        for surface in (
            item.get("support_contract", {}).get("preferred_support_surfaces")
            or item.get("support_contract", {}).get("diagnostic_surfaces")
            or []
        )
        if str(surface).strip()
    ]
    if preferred_surfaces and "wcs_sql" in rb_surfaces:
        adjustment += 0.10 if preferred_surfaces[0] == "wcs_sql" else 0.04
    preferred = node_preferred_audience(node)
    audience = runbook_audience_roles(runbook)
    if preferred and audience and preferred & audience:
        adjustment += 0.03
    if (
        "physical_floor" in rb_surfaces
        and "physical_floor" not in node_surfaces
        and preferred
        and not preferred & {"operator", "on_site"}
    ):
        adjustment -= 0.12
    return adjustment


def runbook_is_active_agv_error_sql(
    runbook: dict[str, Any] | None,
    match: RunbookSearchMatch | None = None,
) -> bool:
    caps = runbook_capability_tags(runbook)
    surfaces = runbook_access_surfaces(runbook)
    if "wcs_sql" not in surfaces:
        return False
    text = runbook_match_text(match, runbook).lower() if match is not None else " ".join(
        [
            str((runbook or {}).get("title") or ""),
            str((runbook or {}).get("summary") or ""),
            str((runbook or {}).get("when_to_use") or ""),
        ]
    ).lower()
    return bool(
        re.search(
            r"\b(active\s+agv\s+errors?|agv\s+active\s+errors?|"
            r"systemactiveerrormodel|agvactiveerrordatabasemodel)\b",
            text,
        )
    )


ACTIVE_AGV_ERROR_EVIDENCE_PATTERN = re.compile(
    r"\b("
    r"active (?:agv |robot )?(?:error|fault)s?|"
    r"agv (?:active )?(?:error|fault)s?|"
    r"agv(?:s)?(?:\s+\w+){0,4}\s+(?:error|fault)s?|"
    r"(?:system|fleet)\s+(?:error|fault)\s*state|"
    r"system(?:\s+\w+){0,3}\s+(?:error|fault)s?|"
    r"systemactiveerror|agvactiveerror|"
    r"active faults?|error codes"
    r")\b",
    re.IGNORECASE,
)


def node_allows_active_agv_error_sql(node: dict[str, Any]) -> bool:
    caps = node_expects_capabilities(node)
    if "agv_active_errors" not in caps:
        return False
    other_caps = caps - {"agv_active_errors"}
    core_text = " ".join(
        part
        for part in [
            str(node.get("title") or ""),
            str(node.get("intent") or node.get("goal") or ""),
        ]
        if part
    ).lower()
    mentions_in_core = bool(ACTIVE_AGV_ERROR_EVIDENCE_PATTERN.search(core_text))
    if other_caps:
        if mentions_in_core:
            return True
        # A composite diagnostic may name the SQL model only in its evidence
        # contract or runbook placeholder.  That is still a valid partial
        # active-error evidence source when the node explicitly requests it.
        evidence_text = " ".join(
            str(node.get(key) or "")
            for key in (
                "runbook_placeholder",
                "evidence_required",
                "healthy_indicators",
                "unhealthy_indicators",
                "inconclusive_indicators",
            )
        ).lower()
        if re.search(
            r"\b(systemactiveerrormodel|agvactiveerrormodel|active agv errors?|agv errors?|error codes?)\b",
            evidence_text,
        ):
            return True
        # Stage 5 may preserve the active-error capability in the ontology
        # contract while the human wording focuses on residual AGV state. In a
        # diagnostic AGV/robot node that explicit capability is sufficient to
        # retain the read-only SQL evidence; service/API-only nodes do not pass
        # this domain guard.
        if (
            str(node.get("node_type") or "") in {"diagnostic_decision", "branching_condition", "validation_gate"}
            and re.search(r"\b(agv|robot|amr|fleet|roster|mapping)\b", core_text)
            and not re.search(r"\b(service|gateway|ignition|api|event viewer)\b", core_text)
        ):
            return True
        # Placeholder often carries Stage 5 SSMS boilerplate; only use it when the
        # title/intent already signals an error/fault check and wcs_sql is expected.
        surfaces = node_expects_surfaces(node)
        if "wcs_sql" not in surfaces or not re.search(r"\b(?:error|fault)s?\b", core_text):
            return False
        placeholder = normalize_placeholder_text(str(node.get("runbook_placeholder") or "")).lower()
        return bool(ACTIVE_AGV_ERROR_EVIDENCE_PATTERN.search(placeholder))
    placeholder = normalize_placeholder_text(str(node.get("runbook_placeholder") or "")).lower()
    return mentions_in_core or bool(ACTIVE_AGV_ERROR_EVIDENCE_PATTERN.search(placeholder)) or True


def build_retrieval_query_text(
    node: dict[str, Any],
    *,
    affected_systems: list[str] | None = None,
) -> str:
    node_type = str(node.get("node_type") or "").strip()
    title = str(node.get("title") or "").strip()
    intent = str(node.get("intent") or node.get("goal") or "").strip()
    placeholder = normalize_placeholder_text(
        str(node.get("runbook_placeholder") or node.get("needed_runbook_capability") or "")
    )
    systems = " ".join(affected_systems or [])
    tag_bits = [
        " ".join(sorted(node_expects_capabilities(node))),
        *(
            [" ".join(sorted(node_expects_capabilities(node)))]
            if USE_CAPABILITY_TAG_CONSTRAINTS
            else []
        ),
        " ".join(sorted(node_expects_surfaces(node))),
        " ".join(sorted(node_preferred_audience(node))),
    ]
    outcome_bits: list[str] = []
    for key in ("expected_or_observed_result", "healthy_condition", "unhealthy_condition", "inconclusive_condition"):
        value = str(node.get(key) or "").strip()
        if value:
            outcome_bits.append(value)
    for key in (
        "evidence_required",
        "healthy_indicators",
        "unhealthy_indicators",
        "inconclusive_indicators",
        "decision_outcomes",
        "outcomes",
        "branches",
        "branch_hints",
    ):
        for item in node.get(key) or []:
            if isinstance(item, dict):
                outcome_bits.extend(
                    str(item.get(field) or "").strip()
                    for field in (
                        "outcome_label",
                        "descriptor",
                        "observable_signal",
                        "condition",
                        "condition_descriptor",
                        "outcome",
                        "tool_or_view",
                    )
                    if str(item.get(field) or "").strip()
                )
            elif item:
                outcome_bits.append(str(item).strip())
    return re.sub(
        r"\s+",
        " ",
        " ".join(
            part
            for part in [node_type, title, intent, placeholder, systems, *tag_bits, *outcome_bits]
            if part
        ),
    ).strip()


def node_check_text(node: dict[str, Any]) -> str:
    return " ".join(
        part
        for part in [
            str(node.get("title") or ""),
            str(node.get("intent") or node.get("goal") or ""),
            normalize_placeholder_text(str(node.get("runbook_placeholder") or "")),
        ]
        if part
    )


def node_is_check_phase(node: dict[str, Any]) -> bool:
    node_type = str(node.get("node_type") or "")
    if node_type not in {"diagnostic_decision", "branching_condition", "validation_gate"}:
        return False
    text = node_check_text(node)
    return bool(CHECK_NODE_PATTERN.search(text))


def runbook_is_recovery_prep(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook)
    return bool(RECOVERY_PREP_RUNBOOK_PATTERN.search(text))


def runbook_is_status_check(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook)
    return bool(STATUS_CHECK_RUNBOOK_PATTERN.search(text))


def runbook_is_wcs_sql_diagnostic_state(
    runbook: dict[str, Any] | None,
    match: RunbookSearchMatch,
) -> bool:
    """Recognize read-only Helix/SSMS state evidence even without RMS wording."""
    if "wcs_sql" not in runbook_access_surfaces(runbook):
        return False
    if str((runbook or {}).get("procedure_type") or match.procedure_type or "").lower() not in {
        "diagnostic",
        "reference",
        "monitoring",
    }:
        return False
    text = runbook_match_text(match, runbook).lower()
    return bool(re.search(r"\b(agv|amr|robot|location|roster|mapping|state|tote|task|helix|ssms)\b", text))


def runbook_is_fleet_rms_status_check(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook)
    return bool(FLEET_RMS_STATUS_RUNBOOK_PATTERN.search(text))


def runbook_is_bump_exception_reference(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook)
    return bool(BUMP_EXCEPTION_RUNBOOK_PATTERN.search(text))


def node_is_site_interview(node: dict[str, Any]) -> bool:
    return node_is_site_interview_only(node)


def node_is_site_interview_only(node: dict[str, Any]) -> bool:
    text = node_check_text(node)
    if not SITE_INTERVIEW_PLACEHOLDER_PATTERN.search(text):
        return False
    return not FLEET_INSPECTION_NODE_PATTERN.search(text)


def node_needs_agv_fleet_domain(node: dict[str, Any]) -> bool:
    return bool(AGV_FLEET_NODE_PATTERN.search(node_check_text(node)))


def node_is_site_history_branch(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") != "branching_condition":
        return False
    return bool(SITE_HISTORY_BRANCH_PATTERN.search(node_check_text(node)))


def node_is_escalation_handoff_only(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") != "escalation_gate":
        return False
    return bool(ESCALATION_HANDOFF_PATTERN.search(node_check_text(node)))


def node_is_symptom_pattern_confirmation(node: dict[str, Any]) -> bool:
    return bool(SYMPTOM_PATTERN_CONFIRMATION_PATTERN.search(node_check_text(node)))


def node_needs_isolation_or_removal(node: dict[str, Any]) -> bool:
    return bool(ISOLATION_REMOVAL_NODE_PATTERN.search(node_check_text(node)))


def node_needs_pairing_validation(node: dict[str, Any]) -> bool:
    if str(node.get("node_type") or "") != "validation_gate":
        return False
    return bool(PAIRING_VALIDATION_NODE_PATTERN.search(node_check_text(node)))


def node_mentions_motionless_floor(node: dict[str, Any]) -> bool:
    return bool(MOTIONLESS_FLOOR_NODE_PATTERN.search(node_check_text(node)))


def runbook_is_motionless_floor_removal(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook).lower()
    return bool(MOTIONLESS_FLOOR_RUNBOOK_PATTERN.search(text))


def runbook_is_generic_agv_removal(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook).lower()
    return bool(GENERIC_AGV_REMOVAL_RUNBOOK_PATTERN.search(text))


def runbook_supports_symptom_corroboration(
    node: dict[str, Any],
    runbook: dict[str, Any] | None,
    match: RunbookSearchMatch,
) -> bool:
    if runbook_is_hospital_ui_reference(runbook, match):
        return False
    if runbook_is_recovery_prep(runbook, match) and not node_mentions_grid_entry(node):
        return False
    if runbook_is_bump_fault_recovery(runbook, match) or runbook_is_bump_exception_reference(runbook, match):
        return False
    if runbook_is_fleet_rms_status_check(runbook, match):
        return True
    text = runbook_match_text(match, runbook).lower()
    if runbook_is_status_check(runbook, match) and re.search(
        r"\b(rms|fleet|agv status|agv locations|overall system agv|map monitor|not mapped|roster|pair|hospital)\b",
        text,
        re.I,
    ):
        return True
    if str(match.procedure_type or "").lower() in {"diagnostic", "reference", "monitoring"} and re.search(
        r"\b(agv status|fleet status|overall system agv|agv locations|map monitor|not mapped)\b",
        text,
        re.I,
    ):
        return True
    return False


def runbook_is_hospital_ui_reference(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook).lower()
    if runbook_is_fleet_rms_status_check(runbook, match):
        return False
    return bool(HOSPITAL_UI_RUNBOOK_PATTERN.search(text))


def runbook_is_bump_fault_recovery(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook).lower()
    return bool(BUMP_FAULT_RECOVERY_RUNBOOK_PATTERN.search(text))


def runbook_is_agv_isolation_or_removal(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook).lower()
    if runbook_is_bump_fault_recovery(runbook, match):
        return False
    if re.search(r"\brecover.*tote\b|\blost a tote\b", text) and not re.search(
        r"\bremove.*agv\b|\bremove.*robot\b|\bremove an agv\b",
        text,
        re.I,
    ):
        return False
    if runbook_is_generic_agv_removal(runbook, match):
        return True
    return bool(AGV_ISOLATION_REMOVAL_RUNBOOK_PATTERN.search(text))


def detect_link_domains(text: str) -> set[str]:
    domains: set[str] = set()
    for name, pattern in INFRA_DOMAIN_PATTERNS.items():
        if pattern.search(text):
            domains.add(name)
    if AGV_FLEET_NODE_PATTERN.search(text):
        domains.add("agv_fleet")
    return domains


def node_link_domains(node: dict[str, Any]) -> set[str]:
    return detect_link_domains(node_check_text(node))


def runbook_link_domains(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> set[str]:
    text = runbook_match_text(match, runbook)
    domains = detect_link_domains(text)
    if runbook_is_bump_fault_recovery(runbook, match) or runbook_is_bump_exception_reference(runbook, match):
        domains.add("agv_bump_recovery")
    if VISU_OPERATOR_RUNBOOK_PATTERN.search(text):
        domains.add("visu_operator")
    if runbook_is_hospital_ui_reference(runbook, match):
        domains.add("hospital_ui")
    return domains


def runbook_is_wrong_domain_for_node(
    node: dict[str, Any],
    runbook: dict[str, Any] | None,
    match: RunbookSearchMatch,
) -> bool:
    node_domains = node_link_domains(node)
    runbook_domains = runbook_link_domains(runbook, match)
    if not node_domains:
        return False

    infra = node_domains & set(INFRA_DOMAIN_PATTERNS)
    agv = "agv_fleet" in node_domains

    if not runbook_domains:
        return bool(infra and not agv)

    if infra and not agv:
        if runbook_domains & {"agv_bump_recovery", "visu_operator", "hospital_ui"} and not (runbook_domains & infra):
            return True
        if runbook_domains == {"agv_fleet"} or runbook_domains == {"agv_fleet", "agv_bump_recovery"}:
            return True

    if "event_viewer" in node_domains and "visu_operator" in runbook_domains and "event_viewer" not in runbook_domains:
        return True
    if "event_viewer" in node_domains and "hospital_ui" in runbook_domains:
        return True
    if "ignition" in node_domains and "visu_operator" in runbook_domains and not (runbook_domains & {"ignition", "event_viewer"}):
        return True
    if "ignition" in node_domains and "hospital_ui" in runbook_domains and "ignition" not in runbook_domains:
        return True
    if "optisweep" in node_domains and runbook_domains <= {"agv_bump_recovery", "visu_operator", "hospital_ui"}:
        return True

    if agv and infra:
        return not bool(node_domains & runbook_domains)

    if node_domains and not (node_domains & runbook_domains):
        if agv and runbook_is_fleet_rms_status_check(runbook, match):
            return False
        if agv and runbook_is_agv_fleet_related(runbook, match) and not infra:
            return False
        if infra:
            return True
    return False


def text_contains_incident_specific_detail(text: str) -> bool:
    return bool(INCIDENT_SPECIFIC_DETAIL_PATTERN.search(text or ""))


def runbook_is_agv_fleet_related(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook).lower()
    if runbook_is_hospital_ui_reference(runbook, match):
        return False
    if AGV_RECOVERY_RUNBOOK_PATTERN.search(text):
        return True
    if runbook_is_fleet_rms_status_check(runbook, match):
        return True
    if runbook_is_status_check(runbook, match) and any(term in text for term in ("agv", "rms", "robot", "fleet")):
        return True
    return bool(re.search(r"\b(agv|amr|robot|rms|fleet)\b", text))


def runbook_is_unrelated_equipment(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook).lower()
    if runbook_is_agv_fleet_related(runbook, match):
        return False
    return bool(UNRELATED_EQUIPMENT_RUNBOOK_PATTERN.search(text))


def node_mentions_grid_entry(node: dict[str, Any]) -> bool:
    text = node_check_text(node)
    return bool(GRID_ENTRY_NODE_PATTERN.search(text))


def node_needs_roster_mapping_check(node: dict[str, Any]) -> bool:
    text = node_check_text(node)
    return bool(ROSTER_MAPPING_NODE_PATTERN.search(text))


def node_needs_hospital_flow_check(node: dict[str, Any]) -> bool:
    """True for hospital tote induct/extract/lane-flow diagnostic or validation nodes.

    Mirrors node_needs_roster_mapping_check's SQL-allowance role: these nodes
    concern backend hospital/tote state (HospitalDatabaseModel,
    HospitalTagsModel) and must not be restricted to RMS/HMI-only candidates.
    """
    text = node_check_text(node)
    return bool(HOSPITAL_FLOW_NODE_PATTERN.search(text))


def node_needs_sequence_backfill_check(node: dict[str, Any]) -> bool:
    """True for AGV exchange-sequence/backfill/tote-association diagnostic or validation nodes.

    Covers the "front AGV moves out without a trailing AGV backfilling"
    pattern and related tote-association checks (RobotCommandDatabaseModel,
    RobotToteDatabseModel, ActiveExchangeModel) so these nodes are not
    restricted to RMS-only candidates.
    """
    text = node_check_text(node)
    return bool(SEQUENCE_BACKFILL_NODE_PATTERN.search(text))


def canonical_source_adjustment(match: RunbookSearchMatch) -> float:
    source = str(match.source_type or "").strip().lower()
    if source in CANONICAL_SOURCE_BOOST:
        return CANONICAL_SOURCE_BOOST[source]
    if source in TRAINING_SOURCE_TYPES:
        return TRAINING_SOURCE_PENALTY
    return 0.0


def intent_alignment_adjustment(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
) -> float:
    adjustment = 0.0
    node_surfaces = node_expects_surfaces(node)
    primary_surface = str(node.get("primary_surface") or "").lower()
    if "wcs_sql" in primary_surface or re.search(r"\b(ssms|sql|database)\b", primary_surface):
        node_surfaces.add("wcs_sql")
    node_caps = node_expects_capabilities(node)
    rb_surfaces = runbook_access_surfaces(runbook)
    # SSMS holds system state + errors — do not prefer RMS fleet checks over WCS/SQL peers.
    remote_state_job = bool(
        node_caps
        & {
            "fleet_system_status",
            "agv_active_errors",
            "wcs_service_health",
            "wcs_system_faults",
        }
    )
    wants_sql = "wcs_sql" in node_surfaces or remote_state_job
    if runbook_is_active_agv_error_sql(runbook, match) and node_allows_active_agv_error_sql(node):
        # Prefer the explicit active-error procedure over a broader fleet/state
        # neighbor when the node names active-error evidence directly.
        roles = node_preferred_audience(node)
        adjustment += 0.12 if roles & {"L2_support", "L3_support", "L4_support", "L2_L3_support"} else 0.05
    if node_is_check_phase(node):
        if runbook_is_fleet_rms_status_check(runbook, match):
            adjustment += 0.10
            if node_needs_roster_mapping_check(node):
                adjustment += 0.08
        elif runbook_is_status_check(runbook, match):
            adjustment += 0.10
            if node_needs_roster_mapping_check(node):
                adjustment += 0.08
        if wants_sql and "wcs_sql" in rb_surfaces:
            adjustment += 0.10
        if runbook_is_recovery_prep(runbook, match):
            adjustment += -0.28 if not node_mentions_grid_entry(node) else -0.18
        if node_needs_roster_mapping_check(node) and runbook_is_bump_exception_reference(runbook, match):
            adjustment -= 0.22
        if node_is_symptom_pattern_confirmation(node) and runbook_supports_symptom_corroboration(node, runbook, match):
            adjustment += 0.12
            if runbook_is_fleet_rms_status_check(runbook, match):
                adjustment += 0.06
            placeholder = normalize_placeholder_text(str(node.get("runbook_placeholder") or "")).lower()
            if "rms" in placeholder and "map monitor" in runbook_match_text(match, runbook).lower():
                adjustment -= 0.06
    if node_needs_isolation_or_removal(node):
        if runbook_is_bump_fault_recovery(runbook, match):
            adjustment -= 0.22
        if runbook_is_motionless_floor_removal(runbook, match):
            adjustment += -0.22 if not node_mentions_motionless_floor(node) else 0.04
        if runbook_is_generic_agv_removal(runbook, match):
            adjustment += 0.10 if not node_mentions_motionless_floor(node) else 0.0
    node_text = node_check_text(node).lower()
    rb_text = runbook_match_text(match, runbook).lower()
    if (
        str(node.get("node_type") or "") == "procedure_reference"
        and re.search(r"\b(service|gateway|ignition|optisweep)\b", node_text)
        and re.search(r"\b(restart|reset|recover)\b", node_text)
    ):
        if re.search(r"\b(ignition|gateway|optisweep|getagvstatuses|windows service)\b", rb_text):
            # Bare keyword co-occurrence is not sufficient to grant this bonus:
            # it must not be reachable by a capability the domain-rule
            # adjustment would penalize for this node (e.g. opc_tag_flow
            # bleeding onto a gateway-restart/health node merely because both
            # mention "Ignition"/"gateway"). This local check is a second,
            # cheaper guard against the same failure mode elsewhere in scoring.
            retrieval_request = derive_retrieval_request(node)
            domain_penalty, _ = capability_domain_adjustment(retrieval_request, runbook)
            if domain_penalty == 0.0:
                adjustment += INTENT_KEYWORD_BONUS
                if str(match.procedure_type or "").lower() == "recovery":
                    adjustment += INTENT_KEYWORD_RECOVERY_BONUS
                elif str(match.procedure_type or "").lower() == "diagnostic":
                    adjustment -= 0.18
        if re.search(r"\b(agv bump|motionless|tipper|operator station|pneumatic|z-axis|loto)\b", rb_text):
            adjustment -= 0.30
    if runbook_is_active_agv_error_sql(runbook, match) and not node_allows_active_agv_error_sql(node):
        adjustment -= 0.28
    return adjustment


def manual_fleet_status_check_in_matches(
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> bool:
    for match in matches:
        source = str(match.source_type or "").strip().lower()
        if source not in MANUAL_SOURCE_TYPES:
            runbook = (runbooks_by_id or {}).get(match.procedure_id)
            metadata = runbook.get("metadata") if isinstance(runbook, dict) and isinstance(runbook.get("metadata"), dict) else {}
            source = str(metadata.get("source_type") or "").strip().lower()
        if source not in MANUAL_SOURCE_TYPES:
            continue
        runbook = (runbooks_by_id or {}).get(match.procedure_id)
        if runbook_is_fleet_rms_status_check(runbook, match) or runbook_is_status_check(runbook, match):
            return True
    return False


def effective_canonical_source_adjustment(
    match: RunbookSearchMatch,
    *,
    runbook: dict[str, Any] | None = None,
    peer_matches: list[RunbookSearchMatch] | None = None,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> float:
    adjustment = canonical_source_adjustment(match)
    if adjustment >= 0:
        return adjustment
    source = str(match.source_type or "").strip().lower()
    if source not in TRAINING_SOURCE_TYPES:
        return adjustment
    if runbook_is_fleet_rms_status_check(runbook, match) or runbook_is_status_check(runbook, match):
        if not manual_fleet_status_check_in_matches(peer_matches or [], runbooks_by_id=runbooks_by_id):
            return 0.0
    return adjustment


def extract_anchor_terms(text: str) -> set[str]:
    lowered = text.lower()
    anchors: set[str] = set()
    for group in DOMAIN_ANCHORS.values():
        for term in group:
            if term in lowered:
                anchors.add(term)
    for token in re.findall(r"[a-z0-9]+", lowered):
        if len(token) > 2 and token not in STOPWORDS:
            anchors.add(token)
    return anchors


def anchor_overlap(node_text: str, runbook_text: str) -> float:
    node_anchors = extract_anchor_terms(node_text)
    runbook_anchors = extract_anchor_terms(runbook_text)
    if not node_anchors or not runbook_anchors:
        return 0.0
    return len(node_anchors & runbook_anchors) / len(node_anchors | runbook_anchors)


def runbook_match_text(match: RunbookSearchMatch, runbook: dict[str, Any] | None = None) -> str:
    parts = [match.title, match.procedure_type]
    if runbook:
        parts.extend(
            [
                str(runbook.get("summary") or ""),
                str(runbook.get("when_to_use") or ""),
                " ".join(str(item) for item in runbook.get("not_for") or []),
                " ".join(str(step.get("title") or "") for step in runbook.get("steps") or [] if isinstance(step, dict)),
            ]
        )
    return " ".join(parts)


def procedure_type_boost(node_type: str, procedure_type: str) -> float:
    preferred = PROCEDURE_TYPE_PREFERRED.get(str(node_type or "").strip())
    if not preferred:
        return 0.0
    normalized_type = str(procedure_type or "").strip().lower()
    if normalized_type == preferred[0]:
        return 0.08
    if normalized_type in preferred:
        return 0.05
    return 0.0


MAX_ADDITIVE_BOOST = 0.20


def boost_combined_score(
    base_score: float,
    *,
    node: dict[str, Any] | None = None,
    node_text: str = "",
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
    procedure_type_compatible: bool,
    peer_matches: list[RunbookSearchMatch] | None = None,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
    domain_penalty: float = 0.0,
) -> float:
    """Rerank a structurally-compatible candidate (procedure-type compatible,
    no hard structural gap -- see normalize.has_structural_gap). `domain_penalty`
    is the caller-computed sum of domain-rule adjustments (capability_domain_adjustment,
    intent_domain_penalty, evidence_domain_penalty, exact_fit_gap_penalty --
    all defined in normalize.py/capability_derivation.py, which this module
    cannot import without a cycle) and is summed in directly, uncapped, same
    as the other penalty sources below. These domain rules used to be a hard
    pre-scoring filter; they are now score input only, so a strong enough
    semantic match can still win despite a domain-rule mismatch. The net
    positive contribution of all bonuses combined is capped (MAX_ADDITIVE_BOOST)
    so a weak raw/base score cannot be boosted past relevance; penalties
    (including domain_penalty) are never capped.
    """
    overlap = anchor_overlap(node_text, runbook_match_text(match, runbook))
    bonus = 0.0
    penalty = domain_penalty
    if overlap >= 0.12:
        bonus += min(0.12, overlap * 0.35)
    if overlap >= 0.25:
        bonus += 0.06
    if match.jaccard_score >= 0.18:
        bonus += 0.04
    if procedure_type_compatible:
        bonus += 0.05
    if match.cosine_score >= 0.50:
        bonus += 0.04
    if node is not None:
        intent_adj = intent_alignment_adjustment(node, match, runbook)
        capability_adj = capability_overlap_adjustment(node, runbook)
        bonus += max(0.0, intent_adj) + max(0.0, capability_adj)
        penalty += min(0.0, intent_adj) + min(0.0, capability_adj)
    source_adj = effective_canonical_source_adjustment(
        match,
        runbook=runbook,
        peer_matches=peer_matches,
        runbooks_by_id=runbooks_by_id,
    )
    bonus += max(0.0, source_adj)
    penalty += min(0.0, source_adj)
    boosted = base_score + min(bonus, MAX_ADDITIVE_BOOST) + penalty
    return round(min(max(boosted, 0.0), 1.0), 4)


def runbook_as_match(runbook: dict[str, Any]) -> RunbookSearchMatch:
    return RunbookSearchMatch(
        procedure_id=str(runbook.get("procedure_id") or ""),
        title=str(runbook.get("title") or ""),
        procedure_type=str(runbook.get("procedure_type") or ""),
        cosine_score=0.0,
        jaccard_score=0.0,
        combined_score=0.0,
    )


def rank_matches_for_node(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
    domain_penalty_fn: Any = None,
) -> list[tuple[RunbookSearchMatch, float]]:
    """domain_penalty_fn, if given, is a callable(node, match, runbook) -> (float, list[str])
    -- normally normalize.total_domain_penalty, passed in by the caller since
    link_scoring.py cannot import normalize.py without a cycle. Ranking order
    should reflect domain-rule adjustments the same way final link scoring
    does, so a same-domain competitor with a normal score gap still wins even
    at the ranking stage, not only at final confidence evaluation."""
    node_text = build_retrieval_query_text(node)
    ranked: list[tuple[RunbookSearchMatch, float]] = []
    for match in matches:
        runbook = (runbooks_by_id or {}).get(match.procedure_id)
        domain_penalty = 0.0
        if domain_penalty_fn is not None:
            domain_penalty, _ = domain_penalty_fn(node, match, runbook)
        boosted = boost_combined_score(
            match.combined_score,
            node=node,
            node_text=node_text,
            match=match,
            runbook=runbook,
            procedure_type_compatible=True,
            peer_matches=matches,
            runbooks_by_id=runbooks_by_id,
            domain_penalty=domain_penalty,
        )
        ranked.append((match, boosted))
    ranked.sort(key=lambda item: (-item[1], item[0].procedure_id))
    return ranked


def intent_mismatch_gaps(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
) -> list[str]:
    gaps: list[str] = []
    if node_is_site_interview_only(node):
        gaps.append(
            "Missing evidence path: site interview/confirmation only — ask the site for the reported "
            "symptom timeline; no catalog runbook replaces a site interview."
        )
    if node_is_check_phase(node) and runbook_is_recovery_prep(runbook, match) and not node_mentions_grid_entry(node):
        gaps.append(
            "Wrong catalog family: pre-grid-entry AGV recovery prep cannot corroborate this check-only node "
            "(need RMS/fleet or remote DB status views, not grid-entry prep)."
        )
    if node_needs_roster_mapping_check(node) and runbook_is_bump_exception_reference(runbook, match):
        gaps.append(
            "Wrong catalog family: BUMP exception codes do not corroborate RMS roster/mapping state "
            "(need Overall System RMS / map monitor / robot roster views)."
        )
    if node_needs_roster_mapping_check(node) and runbook_is_recovery_prep(runbook, match):
        gaps.append(
            "Missing evidence path: runbook lacks RMS roster/mapping inspection "
            "(check map monitor / robot roster; optionally WCS robot-location models for L2)."
        )
    if node_needs_roster_mapping_check(node) and runbook_is_hospital_ui_reference(runbook, match):
        gaps.append(
            "Wrong catalog family: hospital HMI/stacklight does not corroborate RMS roster/mapping "
            "(use RMS map/roster views; hospital UI is secondary diversion corroboration only)."
        )
    if node_is_symptom_pattern_confirmation(node) and runbook_is_hospital_ui_reference(runbook, match):
        gaps.append(
            "Incomplete corroboration: hospital UI alone cannot confirm pairing+hospital diversion pattern "
            "(need RMS fleet/status plus hospital lane view or site-reported diversion)."
        )
    if node_needs_isolation_or_removal(node) and runbook_is_bump_fault_recovery(runbook, match):
        gaps.append(
            "Wrong catalog family: BUMP fault recovery is not authorized robot isolation/removal "
            "(need remove/add AGV or out-of-service isolation procedure)."
        )
    if runbook_is_active_agv_error_sql(runbook, match) and not node_allows_active_agv_error_sql(node):
        gaps.append(
            "Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate "
            "this node's expected capabilities — pick the WCS/SSMS model that matches roster, "
            "lifecycle, hospital, pairing, or service-health intent."
        )
    gaps.extend(capability_corroboration_gaps(node, match, runbook))
    return gaps


CAPABILITY_EVIDENCE_PATHS: dict[str, str] = {
    "zone_pairing_state": (
        "zone pairing failure — ask site whether the zone can obtain a pair; "
        "check RMS zone/AGV status and/or remote WCS pairing-related views (L2)"
    ),
    "hospital_diversion": (
        "hospital-lane diversion — ask site about hospital stacklight/lane routing; "
        "check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2)"
    ),
    "device_roster_state": (
        "roster/mapping abnormality — check RMS map monitor / robot roster "
        "(optionally WCS robot-location models for L2)"
    ),
    "agv_active_errors": (
        "AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2)"
    ),
    "fleet_system_status": (
        "fleet/system-down status — check Overall System RMS / AGV status "
        "(optionally WCS system-state models for L2)"
    ),
}


def capability_corroboration_gaps(
    node: dict[str, Any],
    match: RunbookSearchMatch | None = None,
    runbook: dict[str, Any] | None = None,
) -> list[str]:
    """Actionable gaps when expects_* capabilities are not corroborated by the linked runbook/catalog."""
    expects = node_expects_capabilities(node)
    if not expects:
        expects = _infer_expected_capabilities_from_text(node)
    if not expects:
        return []

    rb_caps = runbook_capability_tags(runbook)
    rb_text = ""
    if match is not None:
        rb_text = runbook_match_text(match, runbook).lower()
    elif runbook:
        rb_text = " ".join(
            [
                str(runbook.get("title") or ""),
                str(runbook.get("summary") or ""),
                str(runbook.get("when_to_use") or ""),
            ]
        ).lower()

    gaps: list[str] = []
    for cap in sorted(expects):
        covered = cap in rb_caps if rb_caps else _capability_mentioned_in_text(cap, rb_text)
        if covered:
            continue
        path = CAPABILITY_EVIDENCE_PATHS.get(cap)
        if path:
            gaps.append(f"Missing corroboration for `{cap}`: {path}.")
        else:
            gaps.append(
                f"Missing corroboration for `{cap}`: no linked runbook covers this capability; "
                f"prefer catalog peers with matching capability_tags / expects_surface."
            )
    return gaps


def unresolved_catalog_gaps(node: dict[str, Any]) -> list[str]:
    """Node-level gaps when Stage 8 leaves the node without a runbook link."""
    node_type = str(node.get("node_type") or "")
    if node_type in {"escalation_gate", "exit"}:
        return [
            "No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; "
            "no branch outcomes required beyond escalate."
        ]
    if node_is_site_interview_only(node) or node_is_site_history_branch(node):
        return [
            "Missing evidence path: site interview/history branch — confirm with the site; "
            "do not substitute a fleet diagnostic runbook."
        ]
    if node_is_escalation_handoff_only(node):
        return [
            "No runbook link expected for escalation handoff — document evidence and escalate."
        ]

    expects = node_expects_capabilities(node) or _infer_expected_capabilities_from_text(node)
    surfaces = node_expects_surfaces(node)
    gaps: list[str] = []
    if expects:
        for cap in sorted(expects):
            path = CAPABILITY_EVIDENCE_PATHS.get(cap)
            if path:
                gaps.append(f"Catalog gap for `{cap}`: {path}.")
            else:
                gaps.append(
                    f"Catalog gap for `{cap}`: no compatible runbook survived filters; "
                    "keep unresolved rather than linking a wrong-domain neighbor."
                )
    else:
        gaps.append(
            "Catalog gap: no compatible runbook survived intent filters; "
            "keep unresolved rather than nearest-neighbor substitution."
        )
    if surfaces:
        gaps.append(
            "Preferred surfaces for a future SME gap runbook: "
            + ", ".join(f"`{item}`" for item in sorted(surfaces))
            + "."
        )
    return gaps


def _infer_expected_capabilities_from_text(node: dict[str, Any]) -> set[str]:
    text = node_check_text(node).lower()
    inferred: set[str] = set()
    if "pair" in text:
        inferred.add("zone_pairing_state")
    if "hospital" in text:
        inferred.add("hospital_diversion")
    if re.search(r"\b(roster|mapping|not mapped)\b", text):
        inferred.add("device_roster_state")
    if re.search(
        r"active\s+(agv\s+)?(error|fault)s?|agv\s+(active\s+)?(error|fault)s?|systemactiveerror",
        text,
    ):
        inferred.add("agv_active_errors")
    if re.search(r"\b(fleet|overall system|system[- ]down|system fault)\b", text):
        inferred.add("fleet_system_status")
    return inferred


def _capability_mentioned_in_text(capability: str, text: str) -> bool:
    if not text:
        return False
    markers = {
        "zone_pairing_state": ("pair", "pairing"),
        "hospital_diversion": ("hospital",),
        "device_roster_state": ("roster", "mapping", "map monitor", "not mapped"),
        "agv_active_errors": ("active agv", "active error", "systemactiveerror", "agv fault"),
        "fleet_system_status": ("overall system", "fleet status", "system fault", "agv status"),
    }
    return any(token in text for token in markers.get(capability, (capability.replace("_", " "),)))
