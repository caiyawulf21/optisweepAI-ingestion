from optisweep_incidence_ingestion.stage6_runbook_finalization import build_incident_finalization_packet


def test_build_incident_finalization_packet_includes_related_evidence() -> None:
    candidate = {
        "candidate_id": "candidate_incident_228086_restart_ignition",
        "title": "Restart Ignition",
        "related_artifact_ids": ["artifact_incident_228086_page_015_embedded_image_01"],
        "related_event_ids": ["incident_228086_event_019"],
        "source_refs": [{"chunk_id": "stage4_page_chunk_002"}],
    }
    artifacts = {
        "artifact_incident_228086_page_015_embedded_image_01": {
            "artifact_id": "artifact_incident_228086_page_015_embedded_image_01",
            "short_description": "Ignition restart command prompt",
        }
    }
    events = {
        "incident_228086_event_019": {
            "event_id": "incident_228086_event_019",
            "summary": "Restart Ignition",
        }
    }
    evidence_handoff = {
        "page_text_chunks": [
            {
                "chunk_id": "stage4_page_chunk_002",
                "page_refs": ["case_228086:page_15"],
                "text": "gwcmd -r",
            }
        ],
        "artifact_evidence_chunks": [],
    }

    packet = build_incident_finalization_packet(
        candidate=candidate,
        artifacts=artifacts,
        events=events,
        canonical_record={"source_case_id": "228086", "title": "Case 228086"},
        evidence_handoff=evidence_handoff,
        source_package={"source_id": "source_case_228086", "source_case_id": "228086"},
    )

    assert packet["packet_type"] == "stage_6_incident_runbook_finalization_packet"
    assert len(packet["related_artifacts"]) == 1
    assert len(packet["timeline_events"]) == 1
    assert len(packet["evidence_chunks"]["page_text_chunks"]) == 1
