"""Deterministic relationship linking for incident per-source Stage 8."""

from __future__ import annotations

from typing import Any
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
OPERATIONAL_SRC = REPO_ROOT / "operationalknowledgeingestion" / "src"
if str(OPERATIONAL_SRC) not in sys.path:
    sys.path.insert(0, str(OPERATIONAL_SRC))

from optisweep_ingestion.tools.relationship_linker import (
    artifact_ids_from_runbook,
    build_candidate_to_procedure_map,
    unique_sorted,
)

LINK_TYPES = {
    "artifact_incident",
    "artifact_timeline",
    "incident_timeline",
    "artifact_runbook",
    "timeline_runbook",
    "incident_runbook",
    "incident_runbook_shared_artifact",
    "artifact_candidate",
    "timeline_candidate",
}


def artifact_ids_from_incident_record(record: dict[str, Any]) -> list[str]:
    ids = [str(item) for item in record.get("supporting_artifact_ids") or [] if str(item or "").strip()]
    for ref in record.get("source_refs") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            ids.append(str(ref["artifact_id"]))
    for ref in (record.get("kpi_tracking") or {}).get("source_refs") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            ids.append(str(ref["artifact_id"]))
    return unique_sorted(ids)


def event_ids_from_timeline_container(timeline: dict[str, Any]) -> list[str]:
    return unique_sorted(
        str(event.get("event_id"))
        for event in timeline.get("events") or []
        if isinstance(event, dict) and event.get("event_id")
    )


def artifact_ids_from_timeline_event(event: dict[str, Any]) -> list[str]:
    ids = [str(item) for item in event.get("artifact_refs") or [] if str(item or "").strip()]
    for ref in event.get("source_refs") or []:
        if isinstance(ref, dict) and ref.get("artifact_id"):
            ids.append(str(ref["artifact_id"]))
    return unique_sorted(ids)


def event_ids_from_runbook(runbook: dict[str, Any]) -> list[str]:
    event_ids: set[str] = set()
    for event_id in runbook.get("related_event_ids") or []:
        text = str(event_id or "").strip()
        if text:
            event_ids.add(text)
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        for event_id in step.get("related_event_ids") or []:
            text = str(event_id or "").strip()
            if text:
                event_ids.add(text)
        for ref in step.get("source_evidence") or []:
            if isinstance(ref, dict) and ref.get("event_id"):
                event_ids.add(str(ref["event_id"]))
    for ref in runbook.get("source_refs") or []:
        if isinstance(ref, dict) and ref.get("event_id"):
            event_ids.add(str(ref["event_id"]))
    return sorted(event_ids)


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


def build_incident_relationship_links(
    *,
    artifacts: list[dict[str, Any]],
    canonical_incident_record: dict[str, Any],
    timeline_events: dict[str, Any],
    runbooks: list[dict[str, Any]],
    candidates: list[dict[str, Any]] | None = None,
    infer_shared_artifact_links: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    links: list[dict[str, Any]] = []
    seen_links: set[tuple[str, str, str]] = set()
    candidate_map = build_candidate_to_procedure_map(runbooks, candidates)

    incident_id = str(canonical_incident_record.get("incident_id") or "").strip()
    events = [event for event in timeline_events.get("events") or [] if isinstance(event, dict)]
    known_artifact_ids = {str(item.get("artifact_id")) for item in artifacts if item.get("artifact_id")}
    known_event_ids = {str(event.get("event_id")) for event in events if event.get("event_id")}
    known_procedure_ids = {str(item.get("procedure_id")) for item in runbooks if item.get("procedure_id")}

    artifact_to_incidents: dict[str, list[str]] = {}
    artifact_to_timeline: dict[str, list[str]] = {}
    artifact_to_runbooks: dict[str, list[str]] = {}
    timeline_to_runbooks: dict[str, list[str]] = {}
    incident_to_runbooks: dict[str, list[str]] = {}
    artifact_to_candidates: dict[str, list[str]] = {}
    timeline_to_candidates: dict[str, list[str]] = {}

    if incident_id:
        for artifact_id in artifact_ids_from_incident_record(canonical_incident_record):
            if artifact_id not in known_artifact_ids:
                continue
            artifact_to_incidents.setdefault(artifact_id, []).append(incident_id)
            _append_link(
                links,
                seen_links,
                link_type="artifact_incident",
                source_record_type="source_artifact",
                source_record_id=artifact_id,
                target_record_type="canonical_incident_record",
                target_record_id=incident_id,
                link_method="incident_supporting_artifact",
            )
        for event_id in unique_sorted(canonical_incident_record.get("supporting_timeline_event_ids") or []):
            if event_id not in known_event_ids:
                continue
            _append_link(
                links,
                seen_links,
                link_type="incident_timeline",
                source_record_type="canonical_incident_record",
                source_record_id=incident_id,
                target_record_type="timeline_event",
                target_record_id=event_id,
                link_method="incident_supporting_timeline_event",
            )

    for event in events:
        event_id = str(event.get("event_id") or "").strip()
        if not event_id:
            continue
        if incident_id:
            _append_link(
                links,
                seen_links,
                link_type="incident_timeline",
                source_record_type="canonical_incident_record",
                source_record_id=incident_id,
                target_record_type="timeline_event",
                target_record_id=event_id,
                link_method="timeline_event_membership",
            )
        for artifact_id in artifact_ids_from_timeline_event(event):
            if artifact_id not in known_artifact_ids:
                continue
            artifact_to_timeline.setdefault(artifact_id, []).append(event_id)
            _append_link(
                links,
                seen_links,
                link_type="artifact_timeline",
                source_record_type="source_artifact",
                source_record_id=artifact_id,
                target_record_type="timeline_event",
                target_record_id=event_id,
                link_method="timeline_artifact_reference",
            )

    for runbook in runbooks:
        procedure_id = str(runbook.get("procedure_id") or "").strip()
        if not procedure_id:
            continue
        for event_id in event_ids_from_runbook(runbook):
            if event_id not in known_event_ids:
                continue
            timeline_to_runbooks.setdefault(event_id, []).append(procedure_id)
            _append_link(
                links,
                seen_links,
                link_type="timeline_runbook",
                source_record_type="timeline_event",
                source_record_id=event_id,
                target_record_type="finalized_runbook",
                target_record_id=procedure_id,
                link_method="runbook_related_event",
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
        if incident_id and (event_ids_from_runbook(runbook) or artifact_ids_from_runbook(runbook)):
            incident_to_runbooks.setdefault(incident_id, []).append(procedure_id)
            _append_link(
                links,
                seen_links,
                link_type="incident_runbook",
                source_record_type="canonical_incident_record",
                source_record_id=incident_id,
                target_record_type="finalized_runbook",
                target_record_id=procedure_id,
                link_method="runbook_incident_evidence",
            )

    for candidate in candidates or []:
        candidate_id = str(candidate.get("candidate_id") or "").strip()
        if not candidate_id:
            continue
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
        for event_id in unique_sorted([str(item) for item in candidate.get("related_event_ids") or []]):
            if event_id not in known_event_ids:
                continue
            timeline_to_candidates.setdefault(event_id, []).append(candidate_id)
            _append_link(
                links,
                seen_links,
                link_type="timeline_candidate",
                source_record_type="timeline_event",
                source_record_id=event_id,
                target_record_type="runbook_candidate",
                target_record_id=candidate_id,
                link_method="candidate_related_event",
                confidence="medium",
            )

    if infer_shared_artifact_links and incident_id:
        incident_artifacts = set(artifact_ids_from_incident_record(canonical_incident_record))
        existing_incident_runbook = {
            (link["source_record_id"], link["target_record_id"])
            for link in links
            if link["link_type"] == "incident_runbook"
        }
        for runbook in runbooks:
            procedure_id = str(runbook.get("procedure_id") or "").strip()
            if not procedure_id:
                continue
            runbook_artifacts = set(artifact_ids_from_runbook(runbook))
            if not incident_artifacts or not runbook_artifacts or not (incident_artifacts & runbook_artifacts):
                continue
            if (incident_id, procedure_id) in existing_incident_runbook:
                continue
            incident_to_runbooks.setdefault(incident_id, []).append(procedure_id)
            existing_incident_runbook.add((incident_id, procedure_id))
            _append_link(
                links,
                seen_links,
                link_type="incident_runbook_shared_artifact",
                source_record_type="canonical_incident_record",
                source_record_id=incident_id,
                target_record_type="finalized_runbook",
                target_record_id=procedure_id,
                link_method="shared_artifact_inference",
                confidence="medium",
            )

    for mapping in (
        artifact_to_incidents,
        artifact_to_timeline,
        artifact_to_runbooks,
        timeline_to_runbooks,
        incident_to_runbooks,
        artifact_to_candidates,
        timeline_to_candidates,
    ):
        for key in mapping:
            mapping[key] = unique_sorted(mapping[key])

    unresolved_event_refs = sum(
        1
        for runbook in runbooks
        for event_id in event_ids_from_runbook(runbook)
        if event_id not in known_event_ids
    )
    unresolved_artifact_refs = sum(
        1
        for runbook in runbooks
        for artifact_id in artifact_ids_from_runbook(runbook)
        if artifact_id not in known_artifact_ids
    )

    adjacency = {
        "artifact_to_incidents": artifact_to_incidents,
        "artifact_to_timeline_events": artifact_to_timeline,
        "artifact_to_runbooks": artifact_to_runbooks,
        "timeline_to_runbooks": timeline_to_runbooks,
        "incident_to_runbooks": incident_to_runbooks,
        "artifact_to_candidates": artifact_to_candidates,
        "timeline_to_candidates": timeline_to_candidates,
        "candidate_to_procedure": candidate_map,
        "incident_id": incident_id,
        "timeline_event_ids": sorted(known_event_ids),
    }
    stats = {
        "link_count": len(links),
        "artifact_incident_links": sum(1 for link in links if link["link_type"] == "artifact_incident"),
        "artifact_timeline_links": sum(1 for link in links if link["link_type"] == "artifact_timeline"),
        "incident_timeline_links": sum(1 for link in links if link["link_type"] == "incident_timeline"),
        "artifact_runbook_links": sum(1 for link in links if link["link_type"] == "artifact_runbook"),
        "timeline_runbook_links": sum(
            1 for link in links if link["link_type"] in {"timeline_runbook", "incident_runbook_shared_artifact"}
        ),
        "incident_runbook_links": sum(
            1 for link in links if link["link_type"] in {"incident_runbook", "incident_runbook_shared_artifact"}
        ),
        "context_candidate_links": sum(1 for link in links if link["link_type"] == "timeline_candidate"),
        "artifact_candidate_links": sum(1 for link in links if link["link_type"] == "artifact_candidate"),
        "artifacts_with_links": len({link["source_record_id"] for link in links if link["source_record_type"] == "source_artifact"}),
        "timeline_events_with_runbook_links": len(timeline_to_runbooks),
        "incidents_with_runbook_links": len(incident_to_runbooks),
        "unresolved_event_refs": unresolved_event_refs,
        "unresolved_artifact_refs": unresolved_artifact_refs,
        "known_procedure_ids": sorted(known_procedure_ids),
    }
    return links, {"adjacency": adjacency, "stats": stats}


def apply_incident_relationship_links(
    *,
    artifacts: list[dict[str, Any]],
    canonical_incident_record: dict[str, Any],
    timeline_events: dict[str, Any],
    runbooks: list[dict[str, Any]],
    adjacency: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    artifact_to_incidents = adjacency.get("artifact_to_incidents") or {}
    artifact_to_timeline = adjacency.get("artifact_to_timeline_events") or {}
    artifact_to_runbooks = adjacency.get("artifact_to_runbooks") or {}
    timeline_to_runbooks = adjacency.get("timeline_to_runbooks") or {}
    incident_to_runbooks = adjacency.get("incident_to_runbooks") or {}
    artifact_to_candidates = adjacency.get("artifact_to_candidates") or {}
    candidate_map = adjacency.get("candidate_to_procedure") or {}
    incident_id = str(adjacency.get("incident_id") or canonical_incident_record.get("incident_id") or "").strip()

    updated_artifacts: list[dict[str, Any]] = []
    for artifact in artifacts:
        record = dict(artifact)
        artifact_id = str(record.get("artifact_id") or "").strip()
        procedure_ids = unique_sorted(artifact_to_runbooks.get(artifact_id, []))
        record["linked_incident_id"] = incident_id or None
        record["linked_timeline_event_ids"] = unique_sorted(artifact_to_timeline.get(artifact_id, []))
        record["linked_runbook_candidate_ids"] = unique_sorted(artifact_to_candidates.get(artifact_id, []))
        record["linked_runbook_ids"] = procedure_ids
        record["linked_procedure_ids"] = procedure_ids
        updated_artifacts.append(record)

    updated_incident = dict(canonical_incident_record)
    updated_incident["linked_artifact_ids"] = artifact_ids_from_incident_record(updated_incident)
    updated_incident["linked_timeline_event_ids"] = event_ids_from_timeline_container(timeline_events)
    procedure_ids = unique_sorted(incident_to_runbooks.get(incident_id, [])) if incident_id else []
    updated_incident["linked_runbook_ids"] = procedure_ids
    updated_incident["linked_procedure_ids"] = procedure_ids

    updated_timeline = dict(timeline_events)
    updated_events: list[dict[str, Any]] = []
    for event in timeline_events.get("events") or []:
        if not isinstance(event, dict):
            continue
        record = dict(event)
        event_id = str(record.get("event_id") or "").strip()
        record["linked_artifact_ids"] = artifact_ids_from_timeline_event(record)
        record["linked_runbook_ids"] = unique_sorted(timeline_to_runbooks.get(event_id, []))
        record["linked_procedure_ids"] = record["linked_runbook_ids"]
        updated_events.append(record)
    updated_timeline["events"] = updated_events

    updated_runbooks: list[dict[str, Any]] = []
    for runbook in runbooks:
        record = dict(runbook)
        record["linked_artifact_ids"] = artifact_ids_from_runbook(record)
        record["linked_event_ids"] = event_ids_from_runbook(record)
        updated_runbooks.append(record)

    return updated_artifacts, updated_incident, updated_timeline, updated_runbooks
