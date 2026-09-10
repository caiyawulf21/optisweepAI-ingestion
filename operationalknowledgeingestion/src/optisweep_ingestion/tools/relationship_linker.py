"""Deterministic relationship linking for operational Stage 8."""

from __future__ import annotations

from typing import Any
import hashlib

LINK_TYPES = {
    "artifact_context",
    "artifact_runbook",
    "context_runbook",
    "context_runbook_shared_artifact",
    "context_candidate",
    "artifact_candidate",
}


def unique_sorted(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for raw in values:
        text = str(raw or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return sorted(ordered)


def artifact_ids_from_context(context: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for field in ("related_artifact_ids", "image_refs"):
        ids.extend(str(item) for item in context.get(field) or [] if str(item or "").strip())
    return unique_sorted(ids)


def artifact_ids_from_runbook(runbook: dict[str, Any]) -> list[str]:
    artifact_ids: set[str] = set()
    for ref in runbook.get("visual_references") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            artifact_ids.add(str(ref["artifact_id"]))
    for ref in runbook.get("screens_or_images") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            artifact_ids.add(str(ref["artifact_id"]))
    for ref in runbook.get("image_refs") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            artifact_ids.add(str(ref["artifact_id"]))
        elif isinstance(ref, str) and ref.strip():
            artifact_ids.add(ref.strip())
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        for ref in step.get("screens_or_images") or []:
            if isinstance(ref, dict) and ref.get("artifact_id"):
                artifact_ids.add(str(ref["artifact_id"]))
    return sorted(artifact_ids)


def build_candidate_to_procedure_map(
    runbooks: list[dict[str, Any]],
    candidates: list[dict[str, Any]] | None = None,
) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for runbook in runbooks:
        candidate_id = str(runbook.get("candidate_id") or "").strip()
        procedure_id = str(runbook.get("procedure_id") or "").strip()
        if candidate_id and procedure_id:
            mapping[candidate_id] = procedure_id
    for candidate in candidates or []:
        candidate_id = str(candidate.get("candidate_id") or "").strip()
        if candidate_id and candidate_id not in mapping:
            mapping[candidate_id] = candidate_id
    return mapping


def _link_id(link_type: str, source_id: str, target_id: str) -> str:
    digest = hashlib.sha1(f"{link_type}:{source_id}:{target_id}".encode("utf-8")).hexdigest()[:16]
    return f"link_{link_type}_{digest}"


def _append_link(
    links: list[dict[str, Any]],
    seen: set[tuple[str, str, str]],
    *,
    link_type: str,
    source_record_type: str,
    source_record_id: str,
    target_record_type: str,
    target_record_id: str,
    link_method: str,
    confidence: str = "high",
) -> None:
    if link_type not in LINK_TYPES:
        raise ValueError(f"Unsupported link_type: {link_type}")
    source_id = str(source_record_id or "").strip()
    target_id = str(target_record_id or "").strip()
    if not source_id or not target_id:
        return
    link_key = (link_type, source_id, target_id)
    if link_key in seen:
        return
    seen.add(link_key)
    links.append(
        {
            "link_id": _link_id(link_type, source_id, target_id),
            "link_type": link_type,
            "source_record_type": source_record_type,
            "source_record_id": source_id,
            "target_record_type": target_record_type,
            "target_record_id": target_id,
            "link_method": link_method,
            "confidence": confidence,
            "needs_sme_review": True,
        }
    )


def build_relationship_links(
    *,
    artifacts: list[dict[str, Any]],
    contexts: list[dict[str, Any]],
    runbooks: list[dict[str, Any]],
    candidates: list[dict[str, Any]] | None = None,
    infer_shared_artifact_links: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    links: list[dict[str, Any]] = []
    seen_links: set[tuple[str, str, str]] = set()
    candidate_map = build_candidate_to_procedure_map(runbooks, candidates)

    artifact_to_contexts: dict[str, list[str]] = {}
    artifact_to_runbooks: dict[str, list[str]] = {}
    context_to_runbooks: dict[str, list[str]] = {}
    context_to_candidates: dict[str, list[str]] = {}
    artifact_to_candidates: dict[str, list[str]] = {}

    known_artifact_ids = {str(item.get("artifact_id")) for item in artifacts if item.get("artifact_id")}
    known_context_ids = {str(item.get("context_id")) for item in contexts if item.get("context_id")}
    known_procedure_ids = {str(item.get("procedure_id")) for item in runbooks if item.get("procedure_id")}

    for context in contexts:
        context_id = str(context.get("context_id") or "").strip()
        if not context_id:
            continue
        for artifact_id in artifact_ids_from_context(context):
            if artifact_id not in known_artifact_ids:
                continue
            artifact_to_contexts.setdefault(artifact_id, []).append(context_id)
            _append_link(
                links,
                seen_links,
                link_type="artifact_context",
                source_record_type="source_artifact",
                source_record_id=artifact_id,
                target_record_type="operational_context",
                target_record_id=context_id,
                link_method="context_artifact_reference",
            )

    for runbook in runbooks:
        procedure_id = str(runbook.get("procedure_id") or "").strip()
        if not procedure_id:
            continue
        for context_id in unique_sorted([str(item) for item in runbook.get("related_context_ids") or []]):
            if context_id not in known_context_ids:
                continue
            context_to_runbooks.setdefault(context_id, []).append(procedure_id)
            _append_link(
                links,
                seen_links,
                link_type="context_runbook",
                source_record_type="operational_context",
                source_record_id=context_id,
                target_record_type="finalized_runbook",
                target_record_id=procedure_id,
                link_method="runbook_related_context",
            )
        for artifact_id in artifact_ids_from_runbook(runbook):
            if artifact_id not in known_artifact_ids:
                continue
            artifact_to_runbooks.setdefault(artifact_id, []).append(procedure_id)
            _append_link(
                links,
                seen_links,
                link_type="artifact_runbook",
                source_record_type="source_artifact",
                source_record_id=artifact_id,
                target_record_type="finalized_runbook",
                target_record_id=procedure_id,
                link_method="runbook_visual_reference",
            )

    for candidate in candidates or []:
        candidate_id = str(candidate.get("candidate_id") or "").strip()
        if not candidate_id:
            continue
        for context_id in unique_sorted([str(item) for item in candidate.get("related_context_ids") or []]):
            if context_id not in known_context_ids:
                continue
            context_to_candidates.setdefault(context_id, []).append(candidate_id)
            _append_link(
                links,
                seen_links,
                link_type="context_candidate",
                source_record_type="operational_context",
                source_record_id=context_id,
                target_record_type="runbook_candidate",
                target_record_id=candidate_id,
                link_method="candidate_related_context",
                confidence="medium",
            )
        for artifact_id in unique_sorted([str(item) for item in candidate.get("related_artifact_ids") or []]):
            if artifact_id not in known_artifact_ids:
                continue
            artifact_to_candidates.setdefault(artifact_id, []).append(candidate_id)
            _append_link(
                links,
                seen_links,
                link_type="artifact_candidate",
                source_record_type="source_artifact",
                source_record_id=artifact_id,
                target_record_type="runbook_candidate",
                target_record_id=candidate_id,
                link_method="candidate_related_artifact",
                confidence="medium",
            )

    if infer_shared_artifact_links:
        context_artifacts = {
            str(context.get("context_id")): set(artifact_ids_from_context(context))
            for context in contexts
            if context.get("context_id")
        }
        existing_context_runbook = {
            (link["source_record_id"], link["target_record_id"])
            for link in links
            if link["link_type"] == "context_runbook"
        }
        for runbook in runbooks:
            procedure_id = str(runbook.get("procedure_id") or "").strip()
            if not procedure_id:
                continue
            runbook_artifacts = set(artifact_ids_from_runbook(runbook))
            if not runbook_artifacts:
                continue
            for context_id, context_artifact_ids in context_artifacts.items():
                if not context_artifact_ids & runbook_artifacts:
                    continue
                if (context_id, procedure_id) in existing_context_runbook:
                    continue
                context_to_runbooks.setdefault(context_id, []).append(procedure_id)
                existing_context_runbook.add((context_id, procedure_id))
                _append_link(
                    links,
                    seen_links,
                    link_type="context_runbook_shared_artifact",
                    source_record_type="operational_context",
                    source_record_id=context_id,
                    target_record_type="finalized_runbook",
                    target_record_id=procedure_id,
                    link_method="shared_artifact_inference",
                    confidence="medium",
                )

    for key in artifact_to_contexts:
        artifact_to_contexts[key] = unique_sorted(artifact_to_contexts[key])
    for key in artifact_to_runbooks:
        artifact_to_runbooks[key] = unique_sorted(artifact_to_runbooks[key])
    for key in context_to_runbooks:
        context_to_runbooks[key] = unique_sorted(context_to_runbooks[key])
    for key in context_to_candidates:
        context_to_candidates[key] = unique_sorted(context_to_candidates[key])
    for key in artifact_to_candidates:
        artifact_to_candidates[key] = unique_sorted(artifact_to_candidates[key])

    unresolved_context_refs = sum(
        1
        for runbook in runbooks
        for context_id in runbook.get("related_context_ids") or []
        if str(context_id) not in known_context_ids
    )
    unresolved_artifact_refs = sum(
        1
        for runbook in runbooks
        for artifact_id in artifact_ids_from_runbook(runbook)
        if artifact_id not in known_artifact_ids
    )

    adjacency = {
        "artifact_to_contexts": artifact_to_contexts,
        "artifact_to_runbooks": artifact_to_runbooks,
        "context_to_runbooks": context_to_runbooks,
        "context_to_candidates": context_to_candidates,
        "artifact_to_candidates": artifact_to_candidates,
        "candidate_to_procedure": candidate_map,
    }
    stats = {
        "link_count": len(links),
        "artifact_context_links": sum(1 for link in links if link["link_type"] == "artifact_context"),
        "artifact_runbook_links": sum(1 for link in links if link["link_type"] == "artifact_runbook"),
        "context_runbook_links": sum(
            1 for link in links if link["link_type"] in {"context_runbook", "context_runbook_shared_artifact"}
        ),
        "context_candidate_links": sum(1 for link in links if link["link_type"] == "context_candidate"),
        "artifact_candidate_links": sum(1 for link in links if link["link_type"] == "artifact_candidate"),
        "artifacts_with_links": len({link["source_record_id"] for link in links if link["source_record_type"] == "source_artifact"}),
        "contexts_with_runbook_links": len(context_to_runbooks),
        "runbooks_with_context_links": len(
            {link["target_record_id"] for link in links if link["target_record_type"] == "finalized_runbook"}
        ),
        "unresolved_context_refs": unresolved_context_refs,
        "unresolved_artifact_refs": unresolved_artifact_refs,
        "known_procedure_ids": sorted(known_procedure_ids),
    }
    return links, {"adjacency": adjacency, "stats": stats}


def apply_relationship_links(
    *,
    artifacts: list[dict[str, Any]],
    contexts: list[dict[str, Any]],
    runbooks: list[dict[str, Any]],
    adjacency: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_to_contexts = adjacency.get("artifact_to_contexts") or {}
    artifact_to_runbooks = adjacency.get("artifact_to_runbooks") or {}
    context_to_runbooks = adjacency.get("context_to_runbooks") or {}
    candidate_map = adjacency.get("candidate_to_procedure") or {}

    updated_artifacts: list[dict[str, Any]] = []
    for artifact in artifacts:
        record = dict(artifact)
        artifact_id = str(record.get("artifact_id") or "").strip()
        procedure_ids = unique_sorted(artifact_to_runbooks.get(artifact_id, []))
        record["linked_context_ids"] = unique_sorted(artifact_to_contexts.get(artifact_id, []))
        record["linked_runbook_ids"] = procedure_ids
        record["linked_procedure_ids"] = procedure_ids
        updated_artifacts.append(record)

    updated_contexts: list[dict[str, Any]] = []
    for context in contexts:
        record = dict(context)
        context_id = str(record.get("context_id") or "").strip()
        direct_runbooks = unique_sorted(context_to_runbooks.get(context_id, []))
        candidate_ids = unique_sorted(record.get("related_runbook_candidate_ids") or [])
        candidate_runbooks = unique_sorted(
            candidate_map[candidate_id]
            for candidate_id in candidate_ids
            if candidate_id in candidate_map
        )
        record["related_runbook_ids"] = unique_sorted([*direct_runbooks, *candidate_runbooks])
        updated_contexts.append(record)

    updated_runbooks: list[dict[str, Any]] = []
    for runbook in runbooks:
        record = dict(runbook)
        record["linked_artifact_ids"] = artifact_ids_from_runbook(record)
        updated_runbooks.append(record)

    return updated_artifacts, updated_contexts, updated_runbooks
