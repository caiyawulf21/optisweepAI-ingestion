from optisweep_incidence_ingestion.stage4_canonical_incident_record import (
    deduplicate_symptoms,
    extract_early_failure_signals,
    finalize_canonical_incident_record,
    link_supporting_timeline_event_ids,
    sync_kpi_tracking_fields,
)


def _canonical_record() -> dict:
    return {
        "record_type": "canonical_incident_record",
        "source_case_id": "228086",
        "reported_at": "2026-02-20T07:19:00",
        "resolved_at": "2026-02-20T14:58:00",
        "title": "UPS Haslet robotic system not responding",
        "incident_description": "OptiSweep service terminated and AGVs went out of sync.",
        "what_resolved_it": "OptiSweep service was reset and RMS was used to correct out-of-sync AGVs.",
        "customer_operational_impact": "Nothing was moving and the small sort stopped.",
        "symptoms": [
            "Nothing was moving at the site.",
            "Nothing was moving.",
            "AGVs were reported out of sync.",
        ],
        "systems_involved": ["OptiSweep service", "AGVs / robotic system", "RMS / HMI"],
        "kpi_tracking": {
            "tracking_start_at": "2026-02-20T07:19:00",
            "tracking_end_at": "2026-02-20T14:58:00",
            "elapsed_minutes": 459,
            "basis": "Work-order entry to case close.",
            "confidence": "medium",
            "notes": [],
        },
        "supporting_artifact_ids": [
            "artifact_incident_228086_page_029_embedded_image_01",
            "artifact_missing",
        ],
        "evidence_summary": {
            "conflicts_or_ambiguities": [],
            "unsupported_or_missing_details": [],
        },
    }


def _timeline_events() -> dict:
    return {
        "events": [
            {
                "event_id": "incident_228086_event_001",
                "event_type": "system_event",
                "timestamp": "2026-02-20T06:36:02",
                "summary": "OptiSweep service terminated unexpectedly.",
                "details": "",
                "confidence": "high",
            },
            {
                "event_id": "incident_228086_event_010",
                "event_type": "action_taken",
                "timestamp": "2026-02-20T12:00:00",
                "summary": "OptiSweep service was reset.",
                "details": "",
                "confidence": "medium",
            },
            {
                "event_id": "incident_228086_event_020",
                "event_type": "validation_result",
                "timestamp": "2026-02-20T13:00:00",
                "summary": "RMS used to correct out-of-sync AGVs.",
                "details": "",
                "confidence": "high",
            },
        ]
    }


def test_deduplicate_symptoms_removes_near_duplicates():
    symptoms = deduplicate_symptoms(
        [
            "Nothing was moving at the site.",
            "Nothing was moving.",
            "AGVs were reported out of sync.",
        ]
    )
    assert len(symptoms) == 2


def test_sync_kpi_tracking_fields_recomputes_duration():
    record = sync_kpi_tracking_fields(
        {
            "reported_at": "2026-02-20T07:19:00",
            "resolved_at": "2026-02-20T14:58:00",
            "kpi_tracking": {},
        }
    )
    assert record["downtime_minutes"] == 459
    assert record["resolution_time"] == "7h 39m"
    assert record["kpi_tracking"]["elapsed_minutes"] == 459


def test_extract_early_failure_signals_finds_pre_kpi_events():
    signals = extract_early_failure_signals(_canonical_record(), _timeline_events()["events"])
    assert len(signals) == 1
    assert signals[0]["event_id"] == "incident_228086_event_001"


def test_link_supporting_timeline_event_ids_prefers_recovery_events():
    linked = link_supporting_timeline_event_ids(_canonical_record(), _timeline_events()["events"])
    assert "incident_228086_event_020" in linked
    assert "incident_228086_event_010" in linked


def test_finalize_canonical_incident_record_adds_links_and_signals():
    record, report = finalize_canonical_incident_record(
        _canonical_record(),
        {"warnings": [], "notes": []},
        _timeline_events(),
        known_artifact_ids={"artifact_incident_228086_page_029_embedded_image_01"},
    )
    assert len(record["symptoms"]) == 2
    assert record["early_failure_signals"]
    assert record["supporting_timeline_event_ids"]
    assert "artifact_missing" not in record["supporting_artifact_ids"]
    assert any("physical failure" in item.lower() for item in record["evidence_summary"]["conflicts_or_ambiguities"])
    assert "Finalized canonical record" in " ".join(report.get("notes") or [])
