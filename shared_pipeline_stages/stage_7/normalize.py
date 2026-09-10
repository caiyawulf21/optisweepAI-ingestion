from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from shared_pipeline_stages.runbook_tags import union_runbook_tags


ALLOWED_PROCEDURE_TYPES = {"operation", "diagnostic", "recovery", "reference"}
ALLOWED_ROLES = {"operator", "L1_support", "L2_support", "L3_support"}


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def canonical_procedure_id(title: str, *, suffix: str = "v1") -> str:
    slug = slugify(title) or "procedure"
    return f"proc_{slug}_canonical_{suffix}"


def normalize_merged_runbook(
    runbook: dict[str, Any],
    *,
    source_runbooks: list[dict[str, Any]],
    merge_cluster_id: str,
    sub_cluster_id: str,
    merge_decision: str,
) -> dict[str, Any]:
    normalized = dict(runbook)
    title = str(normalized.get("title") or _best_title(source_runbooks)).strip()
    normalized["title"] = title
    normalized["procedure_id"] = str(
        normalized.get("procedure_id") or canonical_procedure_id(title)
    ).strip()
    normalized["procedure_type"] = _allowed(
        normalized.get("procedure_type"),
        ALLOWED_PROCEDURE_TYPES,
        _most_common([str(item.get("procedure_type") or "") for item in source_runbooks]) or "operation",
    )
    normalized["role_required"] = _allowed(
        normalized.get("role_required"),
        ALLOWED_ROLES,
        _most_common([str(item.get("role_required") or item.get("responsible_role") or "") for item in source_runbooks])
        or "operator",
    )
    normalized["responsible_role"] = _allowed(
        normalized.get("responsible_role") or normalized["role_required"],
        ALLOWED_ROLES,
        normalized["role_required"],
    )
    normalized["supporting_roles"] = [
        role for role in _string_list(normalized.get("supporting_roles")) if role in ALLOWED_ROLES
    ]
    union_runbook_tags(normalized, source_runbooks)
    normalized["summary"] = str(normalized.get("summary") or _best_summary(source_runbooks)).strip()
    normalized["when_to_use"] = str(normalized.get("when_to_use") or normalized["summary"]).strip()
    normalized["not_for"] = _string_list(normalized.get("not_for"))
    normalized["safety_notes"] = _dedupe_strings(
        _string_list(normalized.get("safety_notes"))
        + _collect_strings(source_runbooks, "safety_notes")
    )
    normalized["access_or_tools_needed"] = _dedupe_strings(
        _string_list(normalized.get("access_or_tools_needed"))
        + _collect_strings(source_runbooks, "access_or_tools_needed")
    )
    normalized["related_context_ids"] = _dedupe_strings(
        _string_list(normalized.get("related_context_ids"))
        + _collect_strings(source_runbooks, "related_context_ids")
    )
    normalized["steps"] = _normalize_steps(normalized.get("steps") or [])
    normalized["success_criteria"] = _dedupe_strings(_string_list(normalized.get("success_criteria")))
    normalized["healthy_conditions"] = _dedupe_strings(_string_list(normalized.get("healthy_conditions")))
    normalized["failure_conditions"] = _dedupe_strings(_string_list(normalized.get("failure_conditions")))
    normalized["escalation_guidance"] = _dedupe_strings(_string_list(normalized.get("escalation_guidance")))
    normalized["commands"] = _dict_list(normalized.get("commands"))
    normalized["screens_or_images"] = _dict_list(normalized.get("screens_or_images"))
    normalized["visual_references"] = _dict_list(normalized.get("visual_references"))
    normalized["source_refs"] = _dict_list(normalized.get("source_refs")) or _collect_dicts(
        source_runbooks, "source_refs"
    )
    normalized["image_refs"] = _dict_list(normalized.get("image_refs"))
    source_candidate_ids = _dedupe_strings(
        _string_list(normalized.get("source_candidate_ids"))
        + [str(item.get("candidate_id") or "") for item in source_runbooks]
    )
    normalized["source_candidate_ids"] = [item for item in source_candidate_ids if item]
    explicit_merged_from = _dedupe_strings(_string_list(normalized.get("merged_from_procedure_ids")))
    if explicit_merged_from:
        merged_from = explicit_merged_from
    else:
        merged_from = sorted(
            {
                str(item.get("procedure_id") or "")
                for item in source_runbooks
                if str(item.get("procedure_id") or "").strip()
            }
        )
    normalized["merged_from_procedure_ids"] = merged_from
    normalized["canonical_source_procedure_ids"] = merged_from
    source_lookup = {
        str(item.get("procedure_id") or ""): item for item in source_runbooks if str(item.get("procedure_id") or "")
    }
    normalized["source_lineage"] = _dict_list(normalized.get("source_lineage")) or _collect_dicts(
        [source_lookup[item] for item in merged_from if item in source_lookup],
        "source_lineage",
    )
    normalized["known_gaps"] = _dedupe_strings(_string_list(normalized.get("known_gaps")))
    normalized["missing_details"] = _dedupe_strings(
        _string_list(normalized.get("missing_details")) + normalized["known_gaps"]
    )
    normalized["validation_status"] = str(normalized.get("validation_status") or "needs_sme_review")
    timestamp = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    metadata = dict(normalized.get("metadata") or {})
    metadata.update(
        {
            "product": metadata.get("product") or "OptiSweep",
            "version": metadata.get("version") or 1,
            "merge_status": "canonical",
            "created_by": "stage_7_runbook_merge",
            "created_at": metadata.get("created_at") or timestamp,
            "updated_at": timestamp,
            "merge_cluster_id": merge_cluster_id,
            "sub_cluster_id": sub_cluster_id,
            "merge_decision": merge_decision,
        }
    )
    normalized["metadata"] = metadata
    normalized["merge_history"] = _dict_list(normalized.get("merge_history")) + [
        {
            "merge_cluster_id": merge_cluster_id,
            "sub_cluster_id": sub_cluster_id,
            "merge_decision": merge_decision,
            "merged_from_procedure_ids": merged_from,
            "merged_at": timestamp,
        }
    ]
    return normalized


def validate_canonical_runbook(runbook: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ["procedure_id", "title", "summary"]:
        if not str(runbook.get(field) or "").strip():
            errors.append(f"missing {field}")
    if runbook.get("procedure_type") not in ALLOWED_PROCEDURE_TYPES:
        errors.append("invalid procedure_type")
    if runbook.get("role_required") not in ALLOWED_ROLES:
        errors.append("invalid role_required")
    if not runbook.get("steps"):
        errors.append("missing steps")
    metadata = runbook.get("metadata") or {}
    if metadata.get("merge_status") not in {"canonical", "pass_through"}:
        errors.append("invalid metadata.merge_status")
    if not runbook.get("merged_from_procedure_ids"):
        errors.append("missing merged_from_procedure_ids")
    return errors


def _normalize_steps(raw_steps: list[Any]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, step in enumerate(raw_steps, start=1):
        if not isinstance(step, dict):
            continue
        record = dict(step)
        record["step_number"] = int(record.get("step_number") or index)
        record["title"] = str(record.get("title") or f"Step {index}").strip()
        record["instruction"] = str(record.get("instruction") or "").strip()
        record["expected_result"] = str(record.get("expected_result") or "").strip()
        record["actions"] = _dict_list(record.get("actions"))
        record["commands"] = _dict_list(record.get("commands"))
        record["screens_or_images"] = _dict_list(record.get("screens_or_images"))
        record["stop_or_escalate_if"] = _string_list(record.get("stop_or_escalate_if"))
        record["source_evidence"] = _dict_list(record.get("source_evidence"))
        normalized.append(record)
    return normalized


def _best_title(source_runbooks: list[dict[str, Any]]) -> str:
    ranked = sorted(source_runbooks, key=lambda item: (-len(str(item.get("title") or "")), str(item.get("title") or "")))
    return str(ranked[0].get("title") or "Untitled Procedure")


def _best_summary(source_runbooks: list[dict[str, Any]]) -> str:
    ranked = sorted(
        source_runbooks,
        key=lambda item: (-len(str(item.get("summary") or "")), str(item.get("summary") or "")),
    )
    return str(ranked[0].get("summary") or "")


def _allowed(value: Any, allowed: set[str], default: str) -> str:
    text = str(value or "").strip()
    return text if text in allowed else default


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _collect_strings(source_runbooks: list[dict[str, Any]], field: str) -> list[str]:
    values: list[str] = []
    for runbook in source_runbooks:
        values.extend(_string_list(runbook.get(field)))
    return values


def _collect_dicts(source_runbooks: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for runbook in source_runbooks:
        values.extend(_dict_list(runbook.get(field)))
    return values


def _most_common(values: list[str]) -> str:
    counts: dict[str, int] = {}
    for value in values:
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        return ""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
