from optisweep_incidence_ingestion.stage8_relationship_linking import link_incident_relationships
from optisweep_incidence_ingestion.tools.incident_relationship_linker import (
    apply_incident_relationship_links,
    build_incident_relationship_links,
)


def _fixture() -> tuple[list[dict], dict, dict, list[dict]]:
    incident_id = "incident_228086"
    artifact_id = "artifact_incident_228086_page_015_embedded_image_01"
    event_id = "incident_228086_event_018"
    procedure_id = "proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1"
    candidate_id = "candidate_incident_228086_restart_ignition_and_verify_optisweep_response"

    artifacts = [{"artifact_id": artifact_id, "linked_runbook_candidate_ids": []}]
    canonical = {
        "incident_id": incident_id,
        "supporting_artifact_ids": [artifact_id],
        "supporting_timeline_event_ids": [event_id],
        "source_refs": [{"artifact_id": artifact_id}],
    }
    timeline = {
        "incident_id": incident_id,
        "events": [
            {
                "event_id": event_id,
                "artifact_refs": [artifact_id],
                "source_refs": [{"artifact_id": artifact_id}],
            }
        ],
    }
    runbooks = [
        {
            "procedure_id": procedure_id,
            "candidate_id": candidate_id,
            "related_event_ids": [event_id],
            "visual_references": [{"artifact_id": artifact_id}],
            "steps": [],
        }
    ]
    return artifacts, canonical, timeline, runbooks


def test_incident_relationship_links_connect_artifact_incident_timeline_and_runbook() -> None:
    artifacts, canonical, timeline, runbooks = _fixture()
    links, payload = build_incident_relationship_links(
        artifacts=artifacts,
        canonical_incident_record=canonical,
        timeline_events=timeline,
        runbooks=runbooks,
        candidates=[{"candidate_id": runbooks[0]["candidate_id"], "related_artifact_ids": [artifacts[0]["artifact_id"]]}],
    )
    linked_artifacts, linked_incident, linked_timeline, linked_runbooks = apply_incident_relationship_links(
        artifacts=artifacts,
        canonical_incident_record=canonical,
        timeline_events=timeline,
        runbooks=runbooks,
        adjacency=payload["adjacency"],
    )

    incident_id = canonical["incident_id"]
    event_id = timeline["events"][0]["event_id"]
    procedure_id = runbooks[0]["procedure_id"]
    artifact_id = artifacts[0]["artifact_id"]
    assert linked_artifacts[0]["linked_incident_id"] == incident_id
    assert event_id in linked_artifacts[0]["linked_timeline_event_ids"]
    assert procedure_id in linked_artifacts[0]["linked_runbook_ids"]
    assert artifact_id in linked_incident["linked_artifact_ids"]
    assert procedure_id in linked_incident["linked_runbook_ids"]
    assert linked_timeline["events"][0]["linked_runbook_ids"] == [procedure_id]
    assert artifact_id in linked_runbooks[0]["linked_artifact_ids"]
    assert any(link["link_type"] == "artifact_incident" for link in links)
    assert any(link["link_type"] == "timeline_runbook" for link in links)


def test_incident_stage8_end_to_end_writes_outputs(tmp_path) -> None:
    from pathlib import Path
    import json

    artifacts, canonical, timeline, runbooks = _fixture()
    output_dir = tmp_path / "case_228086"

    def write(path: Path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    write(output_dir / "stage_3_artifact_enrichment/source_artifacts_enriched.json", artifacts)
    write(output_dir / "stage_4_canonical_incident_record/canonical_incident_record.json", canonical)
    write(output_dir / "stage_4_canonical_incident_record/timeline_events.json", timeline)
    write(
        output_dir / "stage_6_finalized_runbooks/finalized_runbooks/candidate_incident_228086_restart_ignition_and_verify_optisweep_response.json",
        runbooks[0],
    )
    write(
        output_dir / "stage_5_runbook_candidates/runbook_candidates.json",
        [{"candidate_id": runbooks[0]["candidate_id"], "related_artifact_ids": [artifacts[0]["artifact_id"]]}],
    )

    report = link_incident_relationships(output_dir=output_dir)
    stage8_dir = output_dir / "stage_8_relationship_linking"
    assert (stage8_dir / "relationship_links.json").exists()
    assert (stage8_dir / "canonical_incident_record_linked.json").exists()
    assert report["link_stats"]["link_count"] >= 4


def test_incident_stage8_without_runbooks_links_artifact_incident_and_timeline() -> None:
    artifacts = [{"artifact_id": "artifact_incident_228723_page_001_embedded_image_01", "linked_runbook_candidate_ids": []}]
    canonical = {
        "incident_id": "incident_228723",
        "supporting_artifact_ids": ["artifact_incident_228723_page_001_embedded_image_01"],
        "supporting_timeline_event_ids": ["incident_228723_event_001"],
        "source_refs": [],
    }
    timeline = {
        "incident_id": "incident_228723",
        "events": [
            {
                "event_id": "incident_228723_event_001",
                "artifact_refs": ["artifact_incident_228723_page_001_embedded_image_01"],
                "source_refs": [],
            }
        ],
    }
    links, payload = build_incident_relationship_links(
        artifacts=artifacts,
        canonical_incident_record=canonical,
        timeline_events=timeline,
        runbooks=[],
        candidates=[],
    )
    linked_artifacts, linked_incident, linked_timeline, linked_runbooks = apply_incident_relationship_links(
        artifacts=artifacts,
        canonical_incident_record=canonical,
        timeline_events=timeline,
        runbooks=[],
        adjacency=payload["adjacency"],
    )

    assert linked_runbooks == []
    assert linked_artifacts[0]["linked_runbook_ids"] == []
    assert linked_incident["linked_runbook_ids"] == []
    assert any(link["link_type"] == "artifact_incident" for link in links)
    assert any(link["link_type"] == "incident_timeline" for link in links)
    assert not any(link["link_type"] == "artifact_runbook" for link in links)
