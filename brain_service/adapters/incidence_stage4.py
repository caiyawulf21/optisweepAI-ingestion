"""Adapter: incidence Stage 4 (create_stage4_canonical_incident_record_and_timeline)
output -> ingest_stage_output's generic `records` shape.

This is the ONLY place stage-4-specific field names are read. It performs
no judgment (no entity resolution, no text editing, no polarity) -- it
copies fields that already exist in a timeline event dict into the
{"text", "locator_hint", ...} shape extract_evidence expects, per the
plan's rule that all judgment stays inside the LLM-driven tools.
"""

from __future__ import annotations

from typing import Any


def timeline_events_to_records(timeline_events: dict[str, Any]) -> list[dict[str, Any]]:
    """`timeline_events` is the dict extract_timeline_events_from_chunks()
    returns: {"events": [...], "incident_id": ..., "source_case_id": ..., ...}."""
    records: list[dict[str, Any]] = []
    for event in timeline_events.get("events", []):
        records.append(
            {
                "event_id": event.get("event_id"),
                "event_order": event.get("event_order"),
                "text": event.get("details") or event.get("summary") or "",
                "summary": event.get("summary"),
                "event_type": event.get("event_type"),
                "actor_name": event.get("actor_name"),
                "systems": event.get("systems", []),
                "source_refs": event.get("source_refs", []),
                "locator_hint": {
                    "timeline_event_order": event.get("event_order"),
                    "page": (event.get("source_order") or {}).get("page_number"),
                },
            }
        )
    return records
