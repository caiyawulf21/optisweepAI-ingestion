import json

from shared_pipeline_stages.stage_10.embedding_generator import generate_corpus_embeddings


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def test_stage10_generates_runbook_playbook_and_rag_embeddings(tmp_path) -> None:
    stage7 = tmp_path / "stage_7"
    stage8 = tmp_path / "stage_8_finalized_playbooks"
    source_root = tmp_path / "manual_optisweep_om_v3"
    procedure_id = "proc_canonical_v1"
    _write(
        stage7 / "canonical_runbooks.json",
        {
            "runbooks": [
                {
                    "procedure_id": procedure_id,
                    "title": "Restart ignition",
                    "summary": "Restart and verify AGV response.",
                    "when_to_use": "AGVs stopped after ignition restart.",
                    "procedure_type": "recovery",
                    "role_required": "operator",
                    "steps": [{"step_number": 1, "title": "Restart", "instruction": "Restart ignition service."}],
                    "metadata": {"source_type": "incident", "source_id": "228086"},
                    "validation_status": "needs_sme_review",
                }
            ]
        },
    )
    _write(
        stage8 / "prompt_a_one_per_incident/playbook_retrieval_cards.json",
        {
            "cards": [
                {
                    "playbook_id": "playbook_228086",
                    "playbook_candidate_id": "playbook_candidate_228086",
                    "case_id": "228086",
                    "extraction_mode": "one_playbook_candidate_per_incident",
                    "title": "AGVs stopped",
                    "retrieval_text": "AGVs stopped moving after ignition restart verify optisweep response",
                    "validation_status": "needs_sme_review",
                }
            ]
        },
    )
    _write(stage8 / "prompt_b_multi_flow/playbook_retrieval_cards.json", {"cards": []})
    _write(
        source_root / "stage_4_operational_context/operational_context.json",
        [
            {
                "context_id": "ctx_test_v1",
                "title": "AGV startup readiness",
                "summary": "Verify AGVs are in staging before restart.",
                "retrieval_text": "Verify AGV startup readiness and staging state before restart.",
                "context_type": "diagnostic",
                "source_type": "manual",
            }
        ],
    )
    _write(
        source_root / "stage_3_artifact_enrichment/source_artifacts_enriched.json",
        [
            {
                "artifact_id": "artifact_test_v1",
                "title": "AGV status screen",
                "summary": "Screenshot of AGV status screen with error codes.",
                "retrieval_text": "AGV status screen showing current AGV locations and error codes.",
                "artifact_type": "manual_figure",
                "source_type": "manual",
            }
        ],
    )

    result = generate_corpus_embeddings(
        stage7_dir=stage7,
        stage8_dir=stage8,
        output_dir=tmp_path / "shared",
        source_roots=[source_root],
        use_mock_embedder=True,
    )
    records = json.loads((tmp_path / "shared/stage_10_embeddings/embedding_records.json").read_text(encoding="utf-8"))
    assert result.record_count == 4
    assert result.runbook_record_count == 1
    assert result.playbook_prompt_a_count == 1
    assert result.operational_context_count == 1
    assert result.source_artifact_count == 1
    assert all(record["vector"] for record in records)
    assert (tmp_path / "shared/stage_10_embeddings/embedding_records_operational_context.json").exists()
