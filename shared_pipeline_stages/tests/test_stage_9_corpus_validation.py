import json

from shared_pipeline_stages.stage_9.corpus_validator import validate_corpus


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _minimal_runbook(procedure_id: str) -> dict:
    return {
        "procedure_id": procedure_id,
        "title": "Inspect RMS",
        "summary": "Check RMS roster state.",
        "procedure_type": "diagnostic",
        "role_required": "operator",
        "steps": [{"step_number": 1, "title": "Open RMS", "instruction": "Review roster."}],
        "metadata": {"merge_status": "pass_through", "source_type": "incident", "source_id": "228086"},
        "merged_from_procedure_ids": [procedure_id],
        "validation_status": "needs_sme_review",
    }


def _minimal_playbook(playbook_id: str, procedure_id: str) -> dict:
    return {
        "playbook_id": playbook_id,
        "case_id": "228086",
        "title": "AGVs stopped",
        "nodes": [
            {
                "node_id": "node_1",
                "node_type": "diagnostic_decision",
                "title": "Check RMS",
                "runbook_links": [{"procedure_id": procedure_id, "link_confidence": "high", "link_rank": 1}],
                "decision_outcomes": [{"outcome_label": "healthy"}, {"outcome_label": "unhealthy"}],
                "branches": [],
            }
        ],
        "branches": [],
    }


def test_stage9_passes_valid_corpus(tmp_path) -> None:
    stage7 = tmp_path / "stage_7"
    stage8 = tmp_path / "stage_8_finalized_playbooks"
    stage85 = tmp_path / "stage_8_5_relationship_linking"
    procedure_id = "proc_canonical_v1"
    playbook_id = "playbook_228086"
    _write(stage7 / "canonical_runbooks.json", {"runbooks": [_minimal_runbook(procedure_id)]})
    _write(
        stage8 / "prompt_a_one_per_incident/canonical_playbooks.json",
        {"playbooks": [_minimal_playbook(playbook_id, procedure_id)]},
    )
    _write(
        stage8 / "prompt_a_one_per_incident/playbook_runbook_links.json",
        {
            "links": [
                {
                    "case_id": "228086",
                    "playbook_id": playbook_id,
                    "node_id": "node_1",
                    "procedure_id": procedure_id,
                    "link_confidence": "high",
                    "link_rank": 1,
                    "extraction_mode": "prompt_a_one_per_incident",
                }
            ]
        },
    )
    _write(
        stage8 / "prompt_b_multi_flow/canonical_playbooks.json",
        {"playbooks": []},
    )
    _write(
        stage85 / "relationship_links.json",
        [
            {
                "link_type": "playbook_runbook",
                "source_record_id": playbook_id,
                "target_record_id": procedure_id,
                "link_scope": "shared_playbook",
            }
        ],
    )
    result = validate_corpus(
        stage7_dir=stage7,
        stage8_dir=stage8,
        stage85_dir=stage85,
        output_dir=tmp_path / "shared",
    )
    assert result.passed
    assert result.error_count == 0
    assert (tmp_path / "shared/stage_9_validation/validation_report.json").exists()


def test_stage9_fails_on_unresolved_playbook_link(tmp_path) -> None:
    stage7 = tmp_path / "stage_7"
    stage8 = tmp_path / "stage_8_finalized_playbooks"
    procedure_id = "proc_canonical_v1"
    _write(stage7 / "canonical_runbooks.json", {"runbooks": [_minimal_runbook(procedure_id)]})
    _write(
        stage8 / "prompt_a_one_per_incident/canonical_playbooks.json",
        {
            "playbooks": [
                {
                    "playbook_id": "playbook_228086",
                    "nodes": [
                        {
                            "node_id": "node_1",
                            "node_type": "diagnostic_decision",
                            "runbook_links": [{"procedure_id": "", "link_confidence": "unresolved"}],
                        }
                    ],
                }
            ]
        },
    )
    _write(stage8 / "prompt_b_multi_flow/canonical_playbooks.json", {"playbooks": []})
    result = validate_corpus(stage7_dir=stage7, stage8_dir=stage8)
    assert not result.passed
    assert result.error_count >= 1
