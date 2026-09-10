from __future__ import annotations

import json
from pathlib import Path

from brain_service.adapters.incidence_stage4 import timeline_events_to_records

CASE_228086_TIMELINE_EVENTS = (
    Path(__file__).resolve().parents[2]
    / "incidenceknowledgeingestion"
    / "data"
    / "output"
    / "incidents"
    / "case_228086"
    / "stage_4_canonical_incident_record"
    / "timeline_events.json"
)


def test_timeline_events_to_records_against_real_case_228086_data() -> None:
    """Regression coverage for the exact shape mismatch found while
    building this adapter: a timeline event's `details` field is NOT the
    same text that ended up in the Brain's EvidenceUnit for this event
    (the real corpus record dropped a trailing timestamp caveat) -- so this
    adapter must pass the RAW `details` field through unedited and let
    extract_evidence (an LLM call) do that editorial judgment, never
    attempt it here."""
    timeline_events = json.loads(CASE_228086_TIMELINE_EVENTS.read_text(encoding="utf-8"))

    records = timeline_events_to_records(timeline_events)

    assert len(records) == len(timeline_events["events"])
    first_record = records[0]
    first_event = timeline_events["events"][0]
    assert first_record["event_id"] == first_event["event_id"]
    assert first_record["text"] == first_event["details"]  # raw, unedited
    assert first_record["locator_hint"]["timeline_event_order"] == first_event["event_order"]


def test_timeline_events_to_records_handles_missing_events_key() -> None:
    assert timeline_events_to_records({}) == []


def test_timeline_events_to_records_falls_back_to_summary_when_no_details() -> None:
    timeline_events = {
        "events": [
            {"event_id": "evt_1", "event_order": 1, "summary": "short summary"},
        ]
    }
    records = timeline_events_to_records(timeline_events)
    assert records[0]["text"] == "short summary"
