import json

from shared_pipeline_stages.stage_8_5.link_aggregator import build_stage8_5_corpus_relationship_links


def test_stage8_5_aggregates_per_source_and_playbook_links(tmp_path) -> None:
    manual_root = tmp_path / "manual_optisweep_om_v3"
    incident_root = tmp_path / "case_228086"
    stage7_dir = tmp_path / "stage_7_merged_runbooks"
    stage8_dir = tmp_path / "stage_8_finalized_playbooks"

    manual_links = [
        {
            "link_id": "link_artifact_context_1",
            "link_type": "artifact_context",
            "source_record_type": "source_artifact",
            "source_record_id": "artifact_a",
            "target_record_type": "operational_context",
            "target_record_id": "ctx_a",
            "link_method": "context_artifact_reference",
            "confidence": "high",
            "needs_sme_review": True,
        }
    ]
    incident_links = [
        {
            "link_id": "link_artifact_incident_1",
            "link_type": "artifact_incident",
            "source_record_type": "source_artifact",
            "source_record_id": "artifact_b",
            "target_record_type": "canonical_incident_record",
            "target_record_id": "incident_228086",
            "link_method": "incident_supporting_artifact",
            "confidence": "high",
            "needs_sme_review": True,
        }
    ]

    def write(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    write(manual_root / "stage_8_relationship_linking/relationship_links.json", manual_links)
    write(
        manual_root / "stage_8_relationship_linking/relationship_linking_report.json",
        {"source_id": "manual_optisweep_om_v3"},
    )
    write(incident_root / "stage_8_relationship_linking/relationship_links.json", incident_links)
    write(
        incident_root / "stage_8_relationship_linking/relationship_linking_report.json",
        {"incident_id": "incident_228086", "source_case_id": "228086"},
    )
    write(
        stage7_dir / "candidate_to_procedure_mapping.json",
        {
            "mappings": [
                {
                    "candidate_id": "candidate_x",
                    "source_procedure_id": "proc_source_v1",
                    "canonical_procedure_id": "proc_canonical_v1",
                }
            ]
        },
    )
    write(
        stage8_dir / "prompt_a_one_per_incident/playbook_runbook_links.json",
        {
            "links": [
                {
                    "case_id": "228086",
                    "playbook_id": "playbook_a",
                    "node_id": "node_1",
                    "procedure_id": "proc_canonical_v1",
                    "link_confidence": "high",
                    "link_rank": 1,
                    "extraction_mode": "prompt_a_one_per_incident",
                }
            ]
        },
    )

    result = build_stage8_5_corpus_relationship_links(
        source_roots=[manual_root, incident_root],
        output_dir=tmp_path / "shared",
        stage7_dir=stage7_dir,
        stage8_dir=stage8_dir,
    )
    corpus = json.loads((tmp_path / "shared/stage_8_5_relationship_linking/relationship_links.json").read_text(encoding="utf-8"))

    assert result.link_count == 3
    assert result.per_source_link_count == 2
    assert result.playbook_link_count == 1
    assert any(link["link_type"] == "playbook_runbook" for link in corpus)
    assert any(link["link_scope"] == "per_source" for link in corpus)
