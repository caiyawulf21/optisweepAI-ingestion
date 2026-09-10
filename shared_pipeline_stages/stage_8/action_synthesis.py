from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Any


REMOTE_ROLES = {"L1_support", "L2_support", "L3_support", "L4_support", "remote"}
DIAGNOSTIC_NODE_TYPES = {"diagnostic_decision", "branching_condition", "validation_gate"}
SURFACE_ORDER_REMOTE = ("wcs_sql", "wcs_api", "event_viewer", "aveva_hmi", "rms_ui", "site_interview")
SURFACE_ORDER_OPERATOR = ("aveva_hmi", "tipper_hmi", "hospital_hmi", "rms_ui", "physical_floor", "site_interview")
VALIDATED_SURFACES = {
    "wcs_sql",
    "wcs_api",
    "event_viewer",
    "ignition_gateway",
    "rms_ui",
    "aveva_hmi",
    "hospital_hmi",
    "tipper_hmi",
    "building_acb_hmi",
    "site_interview",
    "physical_floor",
}
MAX_ONTOLOGY_ENTITIES = 3
MAX_EVIDENCE_FIELDS = 8
ACTION_PLAN_FIELDS = (
    "diagnostic_classification",
    "question",
    "primary_action",
    "performed_by",
    "primary_surface",
    "optional_corroboration_surface",
    "evidence_to_collect",
    "healthy_interpretation",
    "unhealthy_interpretation",
    "inconclusive_interpretation",
    "optional_corroboration",
    "linked_primary_procedure",
    "generated_guidance",
    "ontology_evidence",
    "technical_field_mapping",
    "runbook_execution_result",
    "node_interpretation_mapping",
    "confidence",
    "requires_sme_review",
    "query_mode",
    "evidence_retrieval_success",
    "diagnostic_interpretation",
)


def synthesize_diagnostic_action_plan(
    node: dict[str, Any],
    *,
    ontology_evidence: list[dict[str, Any]] | None = None,
    links: list[dict[str, Any]] | None = None,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if str(node.get("node_type") or "") not in DIAGNOSTIC_NODE_TYPES:
        return {}
    snippets = [item for item in ontology_evidence or [] if isinstance(item, dict)]
    linked = [item for item in links or [] if isinstance(item, dict) and item.get("procedure_id")]
    catalog = runbooks_by_id or {}
    classification = classify_diagnostic_node(node)
    surfaces = _surfaces(node, snippets, classification=classification)
    performed_by = _performed_by(node)
    field_mapping = _technical_field_mapping(node, snippets, surfaces[0] if surfaces else "")
    evidence = _evidence_to_collect(node, snippets, field_mapping)
    primary_surface = surfaces[0] if surfaces else "unspecified"
    fields = [
        str(field.get("name") or "")
        for entity in field_mapping.get("entities") or []
        for field in entity.get("fields") or []
        if str(field.get("name") or "")
    ]
    action = _primary_action(node, primary_surface, evidence, field_mapping)
    interpretations = _interpretations(node)
    primary = (
        _procedure_reference(linked[0], catalog, node=node, surface=primary_surface)
        if linked and classification == "technical_diagnosis"
        else None
    )
    corroboration = [
        reference
        for link in linked[1:]
        for reference in [_procedure_reference(link, catalog, node=node, surface=primary_surface)]
        if reference and _distinct_evidence_surface(primary, reference)
    ]
    corroboration = corroboration[:1]
    optional_surface = _surface_for_procedure(corroboration[0], catalog) if corroboration else ""
    query_mode = _query_mode(primary_surface, snippets, fields)
    suggested_checks = field_mapping.get("suggested_database_checks") or []
    ontology_resolution_status = (
        "complete" if suggested_checks or field_mapping.get("entities") else "missing"
    )
    guidance = _generated_guidance(
        primary_surface,
        action=action,
        evidence=evidence,
        fields=fields,
        snippets=snippets,
        query_mode=query_mode,
    )
    confidence = str((linked[0] if linked else {}).get("link_confidence") or "unresolved")
    requires_review = (
        not primary
        or confidence in {"low", "unresolved"}
        or not snippets
        or not evidence
        or bool(node.get("catalog_gaps"))
    )
    return {
        "diagnostic_classification": classification,
        "question": str(node.get("intent") or node.get("goal") or node.get("title") or "").strip(),
        "primary_action": action,
        "performed_by": performed_by,
        "primary_surface": primary_surface,
        "optional_corroboration_surface": optional_surface,
        "evidence_to_collect": evidence,
        "healthy_interpretation": interpretations["healthy"],
        "unhealthy_interpretation": interpretations["unhealthy"],
        "inconclusive_interpretation": interpretations["inconclusive"],
        "optional_corroboration": corroboration,
        "linked_primary_procedure": primary,
        "generated_guidance": guidance,
        "ontology_evidence": _selected_ontology_entities(snippets, field_mapping),
        "technical_field_mapping": field_mapping,
        "ontology_resolution_status": ontology_resolution_status,
        "internal_resolution_status": (
            "linked_procedure"
            if primary
            else "missing_validated_procedure"
            if ontology_resolution_status != "missing"
            else "missing_ontology_guidance"
        ),
        "runbook_execution_result": _runbook_execution_result(primary, catalog),
        "node_interpretation_mapping": _node_interpretation_mapping(interpretations),
        "confidence": confidence,
        "requires_sme_review": requires_review,
        "query_mode": query_mode,
        "evidence_retrieval_success": (
            "Evidence retrieval succeeded when the referenced records, screen values, or API response are obtained; "
            "retrieval success alone does not indicate system health."
        ),
        "diagnostic_interpretation": (
            "Interpret the collected values against the healthy, unhealthy, and inconclusive conditions below; "
            "a populated result can still indicate an unhealthy system state."
        ),
    }


def synthesize_node_type_output(
    node: dict[str, Any],
    *,
    links: list[dict[str, Any]] | None = None,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    node_type = str(node.get("node_type") or "")
    catalog = runbooks_by_id or {}
    link = next((item for item in links or [] if isinstance(item, dict)), None)
    procedure_id = str((link or {}).get("procedure_id") or "")
    runbook = catalog.get(procedure_id) or {}
    if node_type == "procedure_reference":
        return {
            "trigger_condition": _node_trigger_condition(node),
            "selected_procedure": _compact_procedure_reference(link, runbook),
            "selection_rationale": str((link or {}).get("link_rationale") or ""),
            "prerequisites": _list_values((runbook.get("prerequisites") or {}).get("system_preconditions"))
            + _list_values((runbook.get("prerequisites") or {}).get("access_required")),
            "safety_checks": _list_values(runbook.get("safety_notes")),
            "success_confirmation": _first_text_value(runbook.get("success_criteria")),
            "failure_boundary": _first_text_value(runbook.get("failure_conditions"))
            or "Stop at the documented failure condition and escalate; do not invent a recovery path.",
            "runbook_execution_result": _runbook_execution_result(
                _compact_procedure_reference(link, runbook), catalog
            ),
        }
    if node_type == "validation_gate":
        surfaces = _surfaces(node, [], classification="technical_diagnosis")
        checklist = [
            "Confirm the owning service remains running and stable.",
            "Confirm the supported API or control endpoint responds.",
            "Compare database or fleet state with the live HMI or site-observed state.",
            "Observe the affected workflow for recurrence during the stated observation window.",
        ]
        if surfaces and surfaces[0] in {"site_interview", "aveva_hmi", "hospital_hmi", "tipper_hmi"}:
            checklist[2] = "Confirm the source-observed HMI state and ask the site to repeat the affected workflow."
        return {
            "validation_checklist": checklist,
            "required_evidence_sources": [_surface_label(surface) for surface in surfaces[:2]]
            or ["Service state", "API response", "fleet or database state", "site observation"],
            "stable_operation_observation": (
                "Observe the affected workflow for recurrence during the defined observation window; "
                "a reachable screen or successful request alone is not recovery."
            ),
            "healthy_interpretation": str(node.get("healthy_interpretation") or "")
            or "All relevant signals agree and the workflow completes without recurrence.",
            "unhealthy_interpretation": str(node.get("unhealthy_interpretation") or "")
            or "One or more operational signals remain abnormal or the workflow fails again.",
            "inconclusive_interpretation": str(node.get("inconclusive_interpretation") or "")
            or "Signals disagree, the observation window is incomplete, or the required source is unavailable.",
        }
    if node_type == "escalation_gate":
        return {
            "escalation_reason": str(
                node.get("escalation_reason")
                or node.get("purpose")
                or node.get("intent")
                or "The condition remains unresolved or outside the executing role."
            ),
            "evidence_package": _values_from_node(node, "evidence_required", "evidence_to_collect", "source_refs"),
            "actions_attempted": _values_from_node(node, "actions_attempted", "completed_actions"),
            "unresolved_questions": _values_from_node(node, "unresolved_questions", "open_questions"),
            "required_next_team": str(
                node.get("required_next_team")
                or node.get("next_team")
                or "The owning L2/L3 service or controls team"
            ),
            "technical_field_mapping": {},
            "ontology_evidence": [],
        }
    return {
        "technical_field_mapping": {},
        "ontology_evidence": [],
    }


def _compact_procedure_reference(
    link: dict[str, Any] | None,
    runbook: dict[str, Any],
) -> dict[str, Any] | None:
    if not link or not str(link.get("procedure_id") or ""):
        return None
    return {
        "procedure_id": str(link.get("procedure_id") or ""),
        "title": str(runbook.get("title") or ""),
        "purpose": str(runbook.get("purpose") or runbook.get("summary") or runbook.get("when_to_use") or ""),
        "role_required": str(runbook.get("role_required") or runbook.get("responsible_role") or ""),
        "link_confidence": str(link.get("link_confidence") or "unresolved"),
    }


def _node_trigger_condition(node: dict[str, Any]) -> str:
    return str(
        node.get("trigger_condition")
        or node.get("expected_or_observed_result")
        or node.get("intent")
        or node.get("purpose")
        or ""
    ).strip()


def _list_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        values = [item for nested in value.values() for item in (nested if isinstance(nested, list) else [nested])]
    else:
        values = value if isinstance(value, list) else [value]
    return _dedupe([str(item).strip() for item in values if str(item).strip()])


def _values_from_node(node: dict[str, Any], *keys: str) -> list[str]:
    values: list[str] = []
    for key in keys:
        values.extend(_list_values(node.get(key)))
    return _dedupe(values)


def _performed_by(node: dict[str, Any]) -> str:
    roles = {
        str(item).strip()
        for item in (node.get("preferred_audience") or node.get("allowed_roles") or [])
        if str(item).strip()
    }
    if roles & {"operator", "on_site"} and not roles & REMOTE_ROLES:
        return "Site operator"
    if "L3_support" in roles:
        return "L3 support"
    if "L2_support" in roles:
        return "L2 support"
    if "L1_support" in roles:
        return "L1 support"
    return "Support engineer"


def classify_diagnostic_node(node: dict[str, Any]) -> str:
    text = " ".join(
        str(node.get(key) or "")
        for key in (
            "title",
            "intent",
            "goal",
            "runbook_placeholder",
            "expected_or_observed_result",
        )
    )
    if re.search(
        r"\b(confirm|corroborate|reported|symptom|pattern|site interview|ask the site|"
        r"what is happening|currently happening)\b",
        text,
        re.IGNORECASE,
    ) and not re.search(
        r"\b(model|database|sql|ssms|api|service state|lifecycle|timestamp|field|"
        r"recorded state|technical diagnosis)\b",
        text,
        re.IGNORECASE,
    ):
        return "symptom_confirmation"
    if re.search(r"\b(site interview|ask the site|site observation)\b", text, re.IGNORECASE):
        return "symptom_confirmation"
    return "technical_diagnosis"


def _surfaces(
    node: dict[str, Any],
    snippets: list[dict[str, Any]],
    *,
    classification: str,
) -> list[str]:
    if classification == "symptom_confirmation":
        source_surfaces = [
            str(item.get("surface") or "").strip()
            for item in node.get("observed_surfaces") or node.get("source_used_surfaces") or []
            if isinstance(item, dict) and str(item.get("surface") or "").strip()
        ]
        for surface in source_surfaces:
            if surface in VALIDATED_SURFACES and surface not in {"wcs_sql", "wcs_api"}:
                return [surface]
        return ["site_interview"]
    expected = [str(item).strip() for item in node.get("expects_surface") or [] if str(item).strip()]
    source_required = [
        str(item).strip()
        for item in node.get("recommended_diagnostic_surfaces") or []
        if str(item).strip()
    ]
    role_text = " ".join(
        str(item) for item in (node.get("preferred_audience") or node.get("allowed_roles") or [])
    )
    roles = {
        str(item).strip()
        for item in (node.get("preferred_audience") or node.get("allowed_roles") or [])
        if str(item).strip()
    }
    remote = bool(roles & REMOTE_ROLES) or "support" in role_text.lower()
    sql_authorized = bool(roles & {"L2_support", "L3_support", "L4_support", "L2_L3_support"})
    order = SURFACE_ORDER_REMOTE if remote else SURFACE_ORDER_OPERATOR
    backend_mappings = [
        item for item in node.get("backend_observability") or [] if isinstance(item, dict)
    ]
    mapped_support_surfaces = [
        str(item.get("preferred_support_surface") or "").strip()
        for item in backend_mappings
        if str(item.get("preferred_support_surface") or "").strip()
    ]
    if remote and sql_authorized and "wcs_sql" in mapped_support_surfaces:
        return ["wcs_sql"]
    if remote and not sql_authorized:
        observed = [
            str(item.get("surface") or "").strip()
            for item in (node.get("source_used_surfaces") or node.get("observed_surfaces") or [])
            if isinstance(item, dict) and str(item.get("surface") or "").strip() in VALIDATED_SURFACES
        ]
        if observed:
            return [observed[0]]
    node_text = " ".join(
        str(node.get(key) or "")
        for key in ("title", "intent", "goal", "runbook_placeholder", "purpose")
    )
    required_concepts = {
        str(item).strip().lower()
        for item in node.get("required_evidence_concepts") or node.get("expects_capability") or []
        if str(item).strip()
    }
    rms_is_authoritative = bool(
        re.search(r"\b(rms|rms_ui)\b.*\b(only|authoritative|unique|owns)\b", node_text, re.I)
        or re.search(r"\b(unique|authoritative|owns)\b.*\b(rms|rms_ui)\b", node_text, re.I)
    )
    if remote and source_required:
        return [surface for surface in source_required if surface in VALIDATED_SURFACES]
    if remote and required_concepts and not source_required and not re.search(
        r"\b(ignition|gateway|system health|service health)\b",
        node_text,
        re.I,
    ):
        return ["wcs_sql"]
    if remote and expected and set(expected) <= {"rms_ui", "rms"} and not rms_is_authoritative:
        return ["wcs_sql"]
    chosen = [surface for surface in order if surface in expected]
    if chosen:
        return chosen
    snippet_ids = " ".join(str(item.get("id") or "") for item in snippets)
    if "model:" in snippet_ids or "db:" in snippet_ids:
        return ["wcs_sql"]
    for surface in order:
        if surface in snippet_ids:
            return [surface]
    return [surface for surface in expected if surface in VALIDATED_SURFACES]


def _evidence_to_collect(
    node: dict[str, Any],
    snippets: list[dict[str, Any]],
    field_mapping: dict[str, Any],
) -> list[str]:
    values: list[str] = []
    for key in (
        "evidence_required",
        "required_evidence",
        "required_observations",
        "required_evidence_concepts",
        "evidence_to_collect",
    ):
        raw = node.get(key) or []
        if isinstance(raw, str):
            raw = [raw]
        values.extend(str(item).strip() for item in raw if str(item).strip())
    for entity in field_mapping.get("entities") or []:
        for field in entity.get("fields") or []:
            name = str(field.get("name") or "").strip()
            meaning = str(field.get("meaning") or "").strip()
            if name:
                values.append(f"{meaning or name} ({name})")
    for entity in field_mapping.get("suggested_database_checks") or []:
        model = str(entity.get("entity") or "WCS model")
        database = str(entity.get("database") or "WCS database")
        fields = ", ".join(
            str(field.get("name") or "")
            for field in entity.get("fields") or []
            if isinstance(field, dict) and str(field.get("name") or "").strip()
        )
        if fields:
            values.append(f"Suggested read-only {database}.{model} fields: {fields}")
    if not values:
        expected = str(node.get("expected_or_observed_result") or "").strip()
        if expected:
            values.append(f"Observed result described by Stage 5: {expected}")
    if not values:
        values.append("Required evidence mapping is unresolved; record the missing ontology or catalog capability.")
    values = _dedupe(values)
    if len(values) < 3:
        values.extend(
            item
            for item in (
                "Affected asset or workflow identifier",
                "Current observed state and timing",
                "Visible error or reason the state cannot be confirmed",
            )
            if item.casefold() not in {value.casefold() for value in values}
        )
    return values[:MAX_EVIDENCE_FIELDS]


def _ontology_fields(snippets: list[dict[str, Any]]) -> list[str]:
    fields: list[str] = []
    for snippet in snippets:
        text = str(snippet.get("text") or "")
        match = re.search(
            r"(?:Key fields|Fields):\s*(.*?)(?:\.\s*(?:Activities|Healthy|Degraded|Escalate|Roles|Failures|Select template):|$)",
            text,
            re.IGNORECASE,
        )
        if not match:
            continue
        for item in match.group(1).split(";"):
            value = item.strip(" .")
            if value:
                fields.append(value)
    return _dedupe(fields)


def _primary_action(
    node: dict[str, Any],
    surface: str,
    evidence: list[str],
    field_mapping: dict[str, Any],
) -> str:
    title = str(node.get("title") or node.get("intent") or "the diagnostic condition").strip()
    fields = [
        str(field.get("meaning") or field.get("name") or "").strip()
        for entity in field_mapping.get("entities") or []
        for field in entity.get("fields") or []
        if str(field.get("meaning") or field.get("name") or "").strip()
    ]
    if surface == "site_interview":
        return (
            f"Ask the site to describe the affected workflow, asset identifiers, current behavior, timing, "
            f"and any visible error so you can confirm {title.lower()}."
        )
    if fields:
        surface_label = _surface_label(surface)
        subject = _subject_for_node(node)
        return f"In {surface_label}, inspect {subject} and compare the backend evidence with the physical or reported state."
    if evidence:
        return f"On {_surface_label(surface)}, inspect {_subject_for_node(node)} and compare the backend evidence with the physical or reported state."
    return f"On {_surface_label(surface)}, collect the minimum operational evidence needed to determine {title.lower()}."


def _interpretations(node: dict[str, Any]) -> dict[str, str]:
    outcomes = {
        str(item.get("outcome_label") or "").lower(): str(
            item.get("descriptor") or item.get("observable_signal") or ""
        ).strip()
        for item in node.get("decision_outcomes") or []
        if isinstance(item, dict)
    }
    return {
        "healthy": outcomes.get("healthy") or _first_text(node, "healthy_indicators", "healthy_conditions"),
        "unhealthy": outcomes.get("unhealthy") or _first_text(node, "unhealthy_indicators", "unhealthy_conditions"),
        "inconclusive": outcomes.get("inconclusive")
        or _first_text(node, "inconclusive_indicators", "inconclusive_conditions"),
    }


def _first_text(node: dict[str, Any], *keys: str) -> str:
    values: list[str] = []
    for key in keys:
        raw = node.get(key) or []
        if isinstance(raw, str):
            raw = [raw]
        values.extend(str(item).strip() for item in raw if str(item).strip())
    return "; ".join(_dedupe(values))


def _procedure_reference(
    link: dict[str, Any],
    runbooks_by_id: dict[str, dict[str, Any]],
    *,
    node: dict[str, Any],
    surface: str,
) -> dict[str, Any] | None:
    procedure_id = str(link.get("procedure_id") or "")
    if not procedure_id:
        return None
    runbook = runbooks_by_id.get(procedure_id) or {}
    return {
        "procedure_id": procedure_id,
        "title": str(runbook.get("title") or ""),
        "purpose": str(
            runbook.get("purpose") or runbook.get("summary") or runbook.get("when_to_use") or ""
        ),
        "role_required": str(runbook.get("role_required") or ""),
        "link_confidence": str(link.get("link_confidence") or "unresolved"),
        "selection_rationale": str(link.get("link_rationale") or ""),
        "surface": surface,
    }


def _surface_for_procedure(
    reference: dict[str, Any] | None,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> str:
    if not reference:
        return ""
    runbook = runbooks_by_id.get(str(reference.get("procedure_id") or "")) or {}
    surfaces = [str(item) for item in runbook.get("access_surface") or [] if str(item).strip()]
    return surfaces[0] if surfaces else str(reference.get("surface") or "")


def _runbook_execution_result(
    reference: dict[str, Any] | None,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if not reference:
        return {}
    runbook = runbooks_by_id.get(str(reference.get("procedure_id") or "")) or {}
    success = _first_text_value(runbook.get("success_criteria"))
    failure = _first_text_value(runbook.get("failure_conditions"))
    return {
        "success": success or "The procedure's documented completion condition is observed.",
        "failure": failure or "The procedure's documented failure condition is observed.",
    }


def _node_interpretation_mapping(interpretations: dict[str, str]) -> dict[str, Any]:
    return {
        "success": interpretations.get("healthy") or "",
        "failure": interpretations.get("unhealthy") or "",
        "inconclusive": interpretations.get("inconclusive") or "",
    }


def _technical_field_mapping(
    node: dict[str, Any],
    snippets: list[dict[str, Any]],
    surface: str,
) -> dict[str, Any]:
    outcome_text = " ".join(
        str(node.get(key) or "")
        for key in (
            "title",
            "intent",
            "purpose",
            "diagnostic_reasoning",
            "evidence_required",
            "healthy_indicators",
            "unhealthy_indicators",
            "inconclusive_indicators",
        )
    ).lower()
    suggested_database_checks: list[dict[str, Any]] = []
    for mapping in node.get("backend_observability") or []:
        if not isinstance(mapping, dict):
            continue
        for source in mapping.get("support_read_sources") or []:
            if not isinstance(source, dict) or str(source.get("surface") or "") != "wcs_sql":
                continue
            fields = [
                {"name": str(field), "meaning": ""}
                for field in source.get("fields") or []
                if str(field).strip()
            ][:MAX_EVIDENCE_FIELDS]
            if fields:
                suggested_database_checks.append(
                    {
                        "entity": str(source.get("model") or ""),
                        "database": str(source.get("database") or ""),
                        "fields": fields,
                        "correlation_keys": list(mapping.get("correlation_keys") or []),
                        "freshness_field": str(mapping.get("freshness_field") or ""),
                        "source_refs": ["ontology.backend_mappings"],
                    }
                )
    if _service_or_api_health_text(outcome_text):
        suggested_database_checks = []
    if _should_resolve_wcs_database(outcome_text, surface):
        catalog = _load_json_catalog("wcs_sql_catalog.json")
        seeded = {str(check.get("entity") or "") for check in suggested_database_checks}
        for check in _intent_database_checks(outcome_text, catalog):
            entity = str(check.get("entity") or "")
            if entity and entity not in seeded:
                suggested_database_checks.append(check)
                seeded.add(entity)
    if suggested_database_checks:
        suggested_database_checks = _limit_suggested_checks(suggested_database_checks)
    if not suggested_database_checks and _should_resolve_wcs_database(outcome_text, surface):
        catalog = _load_json_catalog("wcs_sql_catalog.json")
        scored_models: list[tuple[int, dict[str, Any]]] = []
        tokens = set(re.findall(r"[a-z0-9]+", outcome_text))
        for model in catalog.get("models") or []:
            model_text = " ".join(
                [
                    str(model.get("name") or ""),
                    str(model.get("purpose") or ""),
                    " ".join(
                        f"{field.get('name', '')} {field.get('meaning', '')}"
                        for field in model.get("fields") or []
                        if isinstance(field, dict)
                    ),
                ]
            ).lower()
            score = len(tokens & set(re.findall(r"[a-z0-9]+", model_text)))
            model_name = str(model.get("name") or "").lower()
            hints = " ".join(str(item) for item in model.get("capability_hints") or []).lower()
            if re.search(r"\b(robot|agv|amr|roster|pairing|mapping)\b", outcome_text):
                if "robotdatabasemodel" in model_name or "device_roster_state" in hints:
                    score += 8
                if "robotlocation" in model_name:
                    score += 6
            if re.search(r"\b(error|fault|alarm)\b", outcome_text) and "activeerror" in model_name:
                score += 7
            if "hospital" in outcome_text and "hospital" in model_name:
                score += 7
            if re.search(r"\b(tote|bag.?out)\b", outcome_text) and "tote" in model_name:
                score += 7
            if re.search(r"\b(task|workflow)\b", outcome_text) and "task" in model_name:
                score += 7
            if score:
                scored_models.append((score, model))
        selected_models = sorted(
            scored_models,
            key=lambda item: (-item[0], str(item[1].get("name") or "")),
        )[:MAX_ONTOLOGY_ENTITIES]
        fields_left = MAX_EVIDENCE_FIELDS
        for model_index, (_, model) in enumerate(selected_models):
            fields = [
                {
                    "name": str(field.get("name") or ""),
                    "meaning": str(field.get("meaning") or field.get("name") or ""),
                }
                for field in model.get("fields") or []
                if isinstance(field, dict) and str(field.get("name") or "").strip()
            ]
            fields.sort(
                key=lambda field: (
                    -len(tokens & set(re.findall(r"[a-z0-9]+", field["meaning"].lower()))),
                    field["name"],
                )
            )
            if fields:
                remaining_models = len(selected_models) - model_index
                field_limit = max(2, fields_left // remaining_models)
                suggested_database_checks.append(
                    {
                        "entity": str(model.get("name") or ""),
                        "database": str(model.get("database") or ""),
                        "fields": fields[:field_limit],
                        "correlation_keys": list(model.get("relationship_keys") or []),
                        "freshness_field": next(
                            (
                                field["name"]
                                for field in fields
                                if re.search(r"updated|timestamp|last.?seen|date", field["name"], re.I)
                            ),
                            "",
                        ),
                        "source_refs": list(model.get("source_refs") or []),
                    }
                )
        suggested_database_checks = _limit_suggested_checks(suggested_database_checks)
    if surface != "wcs_sql":
        suggested_database_checks = _limit_suggested_checks(suggested_database_checks)
        return {
            "primary_surface": surface,
            "entities": [],
            "suggested_database_checks": suggested_database_checks,
            "field_count": 0,
            "availability": (
                "Validated read-only WCS SQL suggestions are available as corroboration."
                if suggested_database_checks
                else "No ontology field mapping is emitted for this surface."
            ),
        }
    outcome_text = " ".join(
        str(node.get(key) or "")
        for key in (
            "title",
            "intent",
            "expected_or_observed_result",
            "healthy_interpretation",
            "unhealthy_interpretation",
            "inconclusive_interpretation",
            "healthy_indicators",
            "unhealthy_indicators",
            "inconclusive_indicators",
            "evidence_required",
        )
    ).lower()
    entities: list[dict[str, Any]] = []
    for snippet in snippets:
        snippet_id = str(snippet.get("id") or "")
        if not snippet_id.startswith(("model:", "capability:")):
            continue
        entity_name = snippet_id.split(":", 1)[1]
        parsed = _parse_field_entries(str(snippet.get("text") or ""))
        if not parsed:
            continue
        scored = sorted(
            parsed,
            key=lambda item: (
                -_field_relevance(item, outcome_text),
                str(item.get("name") or ""),
            ),
        )
        chosen = [item for item in scored[:MAX_EVIDENCE_FIELDS] if _field_is_available(entity_name, item["name"])]
        if not chosen:
            continue
        entities.append(
            {
                "entity": entity_name,
                "database": str(snippet.get("database") or _database_for_model(entity_name)),
                "fields": chosen,
                "source_refs": list(snippet.get("source_refs") or []),
            }
        )
        if len(entities) >= MAX_ONTOLOGY_ENTITIES:
            break
    fields_used = sum(len(item.get("fields") or []) for item in entities)
    if fields_used > MAX_EVIDENCE_FIELDS:
        remaining = MAX_EVIDENCE_FIELDS
        for entity in entities:
            entity["fields"] = list(entity.get("fields") or [])[:remaining]
            remaining -= len(entity["fields"])
        entities = [entity for entity in entities if entity.get("fields")]
        fields_used = sum(len(item.get("fields") or []) for item in entities)
    return {
        "primary_surface": surface,
        "entities": entities,
        "suggested_database_checks": _limit_suggested_checks(suggested_database_checks),
        "field_count": fields_used,
        "availability": (
            "Validated against the WCS SQL model catalog."
            if entities
            else "No validated WCS SQL entity/field mapping is available for this node."
        ),
    }


def _should_resolve_wcs_database(outcome_text: str, surface: str) -> bool:
    if _service_or_api_health_text(outcome_text):
        return False
    if re.search(r"\b(service|gateway|api)\b", outcome_text) and not re.search(
        r"\b(robot|agv|amr|tote|task|roster|location|hospital|sort|system state)\b",
        outcome_text,
    ):
        return False
    if surface == "wcs_sql":
        return True
    return bool(
        re.search(
            r"\b(rms|aveva|hmi|webvisu|robot|agv|amr|tote|task|roster|"
            r"location|hospital|sort|system|mapping|pairing|fleet)\b",
            outcome_text,
        )
    )


def _service_or_api_health_text(text: str) -> bool:
    return bool(
        re.search(r"\b(service|gateway|ignition|api responsiveness|getagvstatuses|wcswebapplication)\b", text)
        and not re.search(r"\b(robot|agv|amr|tote|task|roster|location|hospital|sort|bag.?out|system state)\b", text)
    )


def _intent_database_checks(outcome_text: str, catalog: dict[str, Any]) -> list[dict[str, Any]]:
    model_names: list[str] = []
    if re.search(r"\b(roster|mapping|mapped|unmapped|membership|pairing)\b", outcome_text) or re.search(
        r"\bout of sync\b.*\b(roster|map|mapping|robot|agv|amr)\b", outcome_text
    ):
        model_names.extend(
            [
                "RobotDatabaseModel",
                "RobotLocationDatabaseModel",
                "AgvActiveErrorDatabaseModel",
                "SystemActiveErrorModel",
            ]
        )
    hospital_intent = bool(
        re.search(r"\b(hospital|induct|induction|pickup|drop.?off)\b", outcome_text)
        or (
            re.search(r"\b(aveva|hmi|lane)\b", outcome_text)
            and re.search(r"\b(hospital|induct|tote)\b", outcome_text)
        )
    )
    if hospital_intent:
        model_names.extend(
            [
                "HospitalDatabaseModel",
                "HospitalTagsModel",
                "RobotDatabaseModel",
                "RobotLocationDatabaseModel",
                "RobotToteDatabseModel",
                "TaskModel",
                "ToteModel",
                "CellCodeDatabaseModel",
                "AgvActiveErrorDatabaseModel",
            ]
        )
    if not hospital_intent and re.search(
        r"\b(bag.?out|closeout|task|task-state|workflow progression|stuck task|tote-location mismatch|sequence|sequencing|tote)\b",
        outcome_text,
    ):
        model_names.extend(
            [
                "ActiveBagOutModel",
                "RobotTaskDatabaseModel",
                "TaskModel",
                "RobotDatabaseModel",
                "RobotToteDatabseModel",
                "ToteModel",
                "AgvActiveErrorDatabaseModel",
            ]
        )
    checks: list[dict[str, Any]] = []
    seen: set[str] = set()
    for name in model_names:
        if name in seen:
            continue
        seen.add(name)
        check = _model_check(catalog, name)
        if check:
            checks.append(check)
    return checks


def _model_check(catalog: dict[str, Any], model_name: str) -> dict[str, Any] | None:
    for model in catalog.get("models") or []:
        if str(model.get("name") or "") != model_name:
            continue
        fields = [
            {
                "name": str(field.get("name") or ""),
                "meaning": str(field.get("meaning") or field.get("name") or ""),
            }
            for field in model.get("fields") or []
            if isinstance(field, dict) and str(field.get("name") or "").strip()
        ]
        if not fields:
            return None
        return {
            "entity": model_name,
            "database": str(model.get("database") or ""),
            "fields": fields,
            "correlation_keys": list(model.get("relationship_keys") or []),
            "freshness_field": next(
                (
                    field["name"]
                    for field in fields
                    if re.search(r"updated|timestamp|last.?seen|date", field["name"], re.I)
                ),
                "",
            ),
            "source_refs": list(model.get("source_refs") or []),
        }
    return None


def _limit_suggested_checks(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    limited: list[dict[str, Any]] = []
    fields_left = MAX_EVIDENCE_FIELDS
    seen: set[str] = set()
    unique_checks = [
        check
        for check in checks
        if str(check.get("entity") or "") and str(check.get("entity") or "") not in seen
    ][:MAX_ONTOLOGY_ENTITIES]
    seen = set()
    for index, check in enumerate(unique_checks):
        entity = str(check.get("entity") or "")
        if not entity or entity in seen or fields_left <= 0:
            continue
        remaining_checks = max(1, len(unique_checks) - index)
        field_limit = max(1, fields_left // remaining_checks)
        fields = list(check.get("fields") or [])[:field_limit]
        if not fields:
            continue
        copied = dict(check)
        copied["fields"] = fields
        limited.append(copied)
        seen.add(entity)
        fields_left -= len(fields)
    return limited


def _selected_ontology_entities(
    snippets: list[dict[str, Any]],
    mapping: dict[str, Any],
) -> list[dict[str, Any]]:
    entities = {str(item.get("entity") or "") for item in mapping.get("entities") or []}
    selected: list[dict[str, Any]] = []
    for snippet in snippets:
        if len(selected) >= MAX_ONTOLOGY_ENTITIES:
            break
        snippet_id = str(snippet.get("id") or "")
        if not entities or snippet_id.split(":", 1)[-1] in entities:
            compact = {
                key: snippet[key]
                for key in ("id", "title", "score", "source_refs")
                if key in snippet
            }
            compact["text"] = str(snippet.get("text") or "")[:500]
            selected.append(compact)
    return selected


def _parse_field_entries(text: str) -> list[dict[str, str]]:
    match = re.search(
        r"(?:Key fields|Fields):\s*(.*?)(?:\.\s*(?:Activities|Healthy|Degraded|Escalate|Roles|Failures|Select template):|$)",
        text,
        re.IGNORECASE,
    )
    if not match:
        return []
    entries: list[dict[str, str]] = []
    for raw in match.group(1).split(";"):
        value = raw.strip(" .")
        if not value:
            continue
        name, _, meaning = value.partition(":")
        name = name.strip()
        if "." in name:
            name = name.rsplit(".", 1)[-1]
        clean_meaning = re.split(r"\bselect\s+template\b|\bselect\s+top\b|\bfrom\s+\[", meaning, maxsplit=1, flags=re.IGNORECASE)[0]
        entries.append({"name": name, "meaning": clean_meaning.strip(" .") or name})
    return entries


def _field_relevance(field: dict[str, str], text: str) -> int:
    words = set(re.findall(r"[a-z0-9]+", text))
    return len(words & set(re.findall(r"[a-z0-9]+", f"{field.get('name')} {field.get('meaning')}")))


def _field_is_available(entity: str, field: str) -> bool:
    catalog = _load_json_catalog("wcs_sql_catalog.json")
    for model in catalog.get("models") or []:
        if str(model.get("name") or "").casefold() != entity.casefold():
            continue
        return any(str(item.get("name") or "").casefold() == field.casefold() for item in model.get("fields") or [])
    return entity.casefold() in {"bagouttaskmodel", "systemactiveerrormodel"}


def _database_for_model(entity: str) -> str:
    catalog = _load_json_catalog("wcs_sql_catalog.json")
    for model in catalog.get("models") or []:
        if str(model.get("name") or "").casefold() == entity.casefold():
            return str(model.get("database") or "")
    return ""


def _load_json_catalog(name: str) -> dict[str, Any]:
    path = Path(__file__).resolve().parents[2] / "docs" / "ontology" / "catalogs" / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _surface_label(surface: str) -> str:
    return {
        "wcs_sql": "SSMS",
        "wcs_api": "the OptiSweep/WCS API",
        "rms_ui": "RMS",
        "site_interview": "a site interview",
        "event_viewer": "Windows Event Viewer and Services",
        "ignition_gateway": "the Ignition gateway",
        "aveva_hmi": "the AVEVA HMI",
        "hospital_hmi": "the Hospital HMI",
        "tipper_hmi": "the Tipper HMI",
    }.get(surface, surface or "the selected support surface")


def _subject_for_node(node: dict[str, Any]) -> str:
    text = " ".join(str(node.get(key) or "") for key in ("title", "intent", "purpose")).lower()
    if re.search(r"\b(tote|bag.?out)\b", text):
        return "the affected tote or task"
    if re.search(r"\b(robot|agv|amr|fleet|roster)\b", text):
        return "the affected robot and its fleet record"
    if re.search(r"\b(service|gateway|api)\b", text):
        return "the affected service or gateway"
    return "the affected record or asset"


def _join_human_fields(fields: list[str]) -> str:
    values = _dedupe([field.lower() for field in fields if field])
    if len(values) <= 1:
        return values[0] if values else "the recorded state"
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return ", ".join(values[:-1]) + f", and {values[-1]}"


def _first_text_value(values: Any) -> str:
    for value in values or []:
        if isinstance(value, dict):
            text = str(value.get("description") or value.get("condition") or "").strip()
        else:
            text = str(value).strip()
        if text:
            return text
    return ""


def _distinct_evidence_surface(primary: dict[str, Any] | None, corroboration: dict[str, Any]) -> bool:
    if not primary:
        return True
    return primary.get("purpose") != corroboration.get("purpose")


def _query_mode(surface: str, snippets: list[dict[str, Any]], fields: list[str]) -> str:
    if surface != "wcs_sql":
        return "none"
    has_model = any(str(item.get("id") or "").startswith("model:") for item in snippets)
    if has_model and fields:
        return "ontology_generated_read_only"
    return "conceptual_inspection_only"


def _generated_guidance(
    surface: str,
    *,
    action: str,
    evidence: list[str],
    fields: list[str],
    snippets: list[dict[str, Any]],
    query_mode: str,
) -> str:
    if surface != "wcs_sql":
        return action
    if query_mode == "ontology_generated_read_only":
        return (
            f"{action}. Use only validated ontology entities and fields: "
            f"{'; '.join(fields)}. Restrict any generated query to SELECT-only read access. "
            "Do not infer health from query completion or row count alone."
        )
    return (
        f"{action}. No complete validated ontology mapping is available for the required evidence "
        f"({'; '.join(evidence) or 'the requested state'}); provide conceptual read-only inspection guidance "
        "and record the missing mapping instead of generating executable SQL."
    )


def _dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.casefold()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result
