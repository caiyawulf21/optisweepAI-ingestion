from optisweep_incidence_ingestion.stage5_runbook_candidates import (
    build_stage5_packet,
    validate_candidate,
)


def test_build_stage5_packet_includes_access_surfaces_and_ontology() -> None:
    packet = build_stage5_packet(
        package={
            "source_id": "source_case_228086",
            "source_case_id": "228086",
            "source_title": "Case 228086",
            "ingestion_batch_id": "batch_test",
            "site_location": {"site_code": "ups_haslet_tx"},
            "source_bundle": {},
        },
        canonical_record={
            "source_case_id": "228086",
            "title": "Site stoppage",
            "summary": "Ignition restart and GetAgvStatuses validation",
            "affected_systems": ["Ignition", "OptiSweep API"],
        },
        timeline={"events": [{"event_id": "e1", "summary": "Restart Ignition gateway"}]},
        evidence_handoff={
            "chunk_index": [],
            "page_text_chunks": [{"chunk_id": "c1", "text": "Open SSMS Helix DB and check AGV active errors"}],
            "artifact_evidence_chunks": [],
        },
        artifacts=[
            {
                "artifact_id": "a1",
                "short_description": "SSMS query of SystemActiveErrorModel",
                "ocr_text": "SELECT * FROM SystemActiveErrorModel",
            }
        ],
    )

    assert packet["packet_type"] == "stage_5_incident_runbook_candidate_discovery_packet"
    assert isinstance(packet["allowed_access_surfaces"], list)
    assert any(item.get("id") == "wcs_sql" for item in packet["allowed_access_surfaces"])
    assert isinstance(packet["ontology_snippets"], list)
    assert any("allowed_access_surfaces" in item for item in packet["instructions"])


def test_validate_candidate_rejects_missing_live_surface() -> None:
    candidate = {
        "candidate_id": "candidate_incident_1_vague",
        "title": "Investigate the issue",
        "candidate_goal": "Look at evidence and document findings",
        "summary": "Review case evidence and document findings",
        "rough_steps": [
            "Review evidence from the case.",
            "Investigate the issue further.",
            "Document findings for later review.",
        ],
        "expected_result": "Findings are documented",
        "failure_or_escalation_notes": ["Escalate if unclear"],
        "access_or_tools_needed": ["case evidence"],
        "source_id": "source_case_1",
        "ingestion_batch_id": "batch_1",
        "source_refs": [{"page_ref": "case_1:page_1"}],
        "evidence_source_refs": [{"page_ref": "case_1:page_1"}],
        "related_artifact_ids": [],
        "related_event_ids": [],
    }
    errors = validate_candidate(
        candidate,
        {
            "artifact_ids": set(),
            "event_ids": set(),
            "page_refs": {"case_1:page_1"},
            "chunk_ids": set(),
        },
    )
    assert any("live access surface" in error or "operational target" in error for error in errors)
