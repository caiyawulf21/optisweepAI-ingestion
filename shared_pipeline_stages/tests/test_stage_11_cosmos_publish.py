import json

from shared_pipeline_stages.stage_10.embedding_generator import generate_corpus_embeddings
from shared_pipeline_stages.stage_11.cosmos_publisher import publish_corpus_to_cosmos


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def test_stage11_writes_multi_container_bundle_and_sme_review_sheet(tmp_path) -> None:
    stage7 = tmp_path / "stage_7"
    stage8 = tmp_path / "stage_8_finalized_playbooks"
    stage85 = tmp_path / "stage_8_5_relationship_linking"
    stage9 = tmp_path / "stage_9_validation"
    source_root = tmp_path / "case_228086"
    procedure_id = "proc_canonical_v1"
    playbook_id = "playbook_228086"
    artifact_id = "artifact_smoke_screenshot"
    image_path = source_root / "stage_3_artifact_enrichment" / "images" / f"{artifact_id}.png"
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    _write(
        source_root / "stage_3_artifact_enrichment/source_artifacts_enriched.json",
        [
            {
                "artifact_id": artifact_id,
                "artifact_type": "rms_screenshot",
                "short_description": "Smoke screenshot",
                "detailed_description": "Test image for Stage 11 canonical_images publish.",
                "storage_path": str(image_path),
                "case_id": "228086",
            }
        ],
    )
    _write(
        stage7 / "canonical_runbooks.json",
        {
            "runbooks": [
                {
                    "procedure_id": procedure_id,
                    "title": "Restart ignition",
                    "summary": "Restart and verify.",
                    "procedure_type": "recovery",
                    "role_required": "operator",
                    "steps": [
                        {
                            "step_number": 1,
                            "title": "Restart",
                            "instruction": "Restart service.",
                            "screens_or_images": [{"artifact_id": artifact_id, "what_to_look_at": "RMS state"}],
                        }
                    ],
                    "metadata": {"merge_status": "pass_through", "source_type": "incident"},
                    "merged_from_procedure_ids": [procedure_id],
                }
            ]
        },
    )
    _write(
        stage8 / "prompt_a_one_per_incident/canonical_playbooks.json",
        {"playbooks": [{"playbook_id": playbook_id, "case_id": "228086", "title": "AGVs stopped", "nodes": []}]},
    )
    _write(stage8 / "prompt_b_multi_flow/canonical_playbooks.json", {"playbooks": []})
    _write(
        stage8 / "prompt_a_one_per_incident/playbook_retrieval_cards.json",
        {
            "cards": [
                {
                    "playbook_id": playbook_id,
                    "case_id": "228086",
                    "extraction_mode": "one_playbook_candidate_per_incident",
                    "retrieval_text": "AGVs stopped after ignition restart",
                }
            ]
        },
    )
    _write(stage8 / "prompt_b_multi_flow/playbook_retrieval_cards.json", {"cards": []})
    _write(
        stage85 / "relationship_links.json",
        [
            {
                "link_type": "playbook_runbook",
                "source_record_id": f"{playbook_id}:node_1",
                "target_record_id": procedure_id,
                "link_confidence": "high",
                "link_rank": 1,
            },
            {
                "link_type": "artifact_runbook",
                "source_record_id": artifact_id,
                "target_record_id": procedure_id,
                "link_method": "runbook_visual_reference",
                "confidence": "high",
            },
        ],
    )
    _write(
        stage9 / "validation_report.json",
        {"passed": True, "summary": {"error_count": 0, "warning_count": 0}, "warnings": []},
    )

    generate_corpus_embeddings(
        stage7_dir=stage7,
        stage8_dir=stage8,
        output_dir=tmp_path / "shared",
        source_roots=[source_root],
        use_mock_embedder=True,
    )
    result = publish_corpus_to_cosmos(
        stage7_dir=stage7,
        stage8_dir=stage8,
        stage10_dir=tmp_path / "shared/stage_10_embeddings",
        stage85_dir=stage85,
        stage9_dir=stage9,
        source_roots=[source_root],
        output_dir=tmp_path / "shared",
        upload_image_blobs=False,
    )
    stage11_dir = tmp_path / "shared/stage_11_cosmos_publish"
    manifest = json.loads((stage11_dir / "publish_manifest.json").read_text(encoding="utf-8"))
    images = json.loads((stage11_dir / "publish_bundle/canonical_images/documents.json").read_text(encoding="utf-8"))
    assert result.runbook_count == 1
    assert result.playbook_prompt_a_count == 1
    assert result.playbook_prompt_b_count == 0
    assert result.embedding_count == 3
    assert result.operational_context_count == 0
    assert result.source_artifact_count == 1
    assert result.relationship_link_count == 2
    assert result.canonical_image_count == 1
    assert not result.uploaded
    assert manifest["record_counts"]["playbooks_prompt_a"] == 1
    assert manifest["record_counts"]["canonical_images"] == 1
    assert manifest["record_counts"]["embeddings_source_artifacts"] == 1
    assert manifest["containers"]["canonical_images"] == "publish_canonical_images"
    assert manifest["containers"]["source_artifacts"] == "publish_source_artifacts"
    assert images[0]["image_id"] == artifact_id
    assert images[0]["linked_procedure_ids"] == [procedure_id]
    assert images[0]["storage_uri"] == ""
    assert (stage11_dir / "publish_bundle/playbooks_prompt_a/documents.json").exists()
    assert (stage11_dir / "publish_bundle/playbooks_prompt_b/documents.json").exists()
    artifact_embeddings = json.loads(
        (stage11_dir / "publish_bundle/source_artifacts/embeddings.json").read_text(encoding="utf-8")
    )
    artifact_rag = json.loads(
        (stage11_dir / "publish_bundle/source_artifacts/rag_records.json").read_text(encoding="utf-8")
    )
    assert artifact_embeddings[0]["doc_type"] == "embedding"
    assert artifact_embeddings[0]["record_type"] == "source_artifact"
    assert artifact_embeddings[0]["vector"]
    assert artifact_rag[0]["doc_type"] == "rag_record"
    assert artifact_rag[0]["id"].startswith("rag_")
    assert (stage11_dir / "sme_review_sheet.md").exists()
    assert (stage11_dir / "sme_review_sheet.json").exists()
