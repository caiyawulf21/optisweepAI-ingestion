import json
import hashlib

from optisweep_ingestion.stage6_runbook_finalization import (
    build_operational_finalization_packet,
    normalize_runbook,
    validate_runbook,
    write_runbook_review_markdown,
    _procedure_id_from_candidate,
)
from shared_pipeline_stages.stage_prompts import compose_stage6_system_prompt


class _Lineage:
    source_id = "manual_optisweep_om_v3"
    source_type = "manual"
    source_title = "OptiSweep Operation and Maintenance Manual"
    source_version = "3"
    ingestion_batch_id = "batch_test"


def _candidate() -> dict:
    return {
        "candidate_id": "candidate_manual_start_operator_station",
        "title": "Start Operator Station",
        "candidate_goal": "Start the Operator Station after power off.",
        "likely_procedure_type": "operation",
        "likely_role_required": "operator",
        "support_safe": True,
        "summary": "Verify prerequisites and start the operator station.",
        "rough_steps": [
            "Verify AGVs are powered on.",
            "Verify the main disconnect is ON.",
            "Press AUTO REF.",
        ],
        "expected_result": "Operator station is in AUTO mode.",
        "failure_or_escalation_notes": ["Escalate if AUTO mode cannot be enabled."],
        "access_or_tools_needed": ["Access to the Operator Station HMI"],
        "related_context_ids": ["ctx_operator_station_overview_v1"],
        "related_artifact_ids": ["artifact_manual_fig_4_19_operator_station_control_panel"],
        "source_refs": [
            {
                "section_id": "manual_section_5_3",
                "page": 82,
                "quote_or_summary": "Starting the Operator Station",
            }
        ],
        "source_id": "manual_optisweep_om_v3",
        "source_type": "manual",
        "ingestion_batch_id": "batch_test",
        "metadata": {"source_quality": "manual"},
    }


def test_stage6_task_prompt_is_composed_with_structure_reference() -> None:
    composed = compose_stage6_system_prompt("Operational Stage 6 task prompt.")
    assert "Operational Stage 6 task prompt." in composed
    assert "Step Template" in composed
    assert '"procedure_type": "operation"' in composed


def test_procedure_id_from_candidate() -> None:
    assert _procedure_id_from_candidate("candidate_manual_start_operator_station", "Start Operator Station") == (
        "proc_manual_start_operator_station_v1"
    )


def test_build_operational_finalization_packet_selects_related_records() -> None:
    candidate = _candidate()
    artifacts = {
        "artifact_manual_fig_4_19_operator_station_control_panel": {
            "artifact_id": "artifact_manual_fig_4_19_operator_station_control_panel",
            "short_description": "Control panel",
        }
    }
    contexts = {
        "ctx_operator_station_overview_v1": {
            "context_id": "ctx_operator_station_overview_v1",
            "title": "Operator Station Overview",
        }
    }
    sections = {
        "manual_section_5_3": {
            "section_id": "manual_section_5_3",
            "heading": "5.3 Starting the Operator Station",
            "text": "Verify AGVs are powered on.",
        }
    }

    packet = build_operational_finalization_packet(
        candidate=candidate,
        artifacts=artifacts,
        contexts=contexts,
        sections=sections,
        lineage=_Lineage(),
    )

    assert packet["packet_type"] == "stage_6_operational_runbook_finalization_packet"
    assert len(packet["related_artifacts"]) == 1
    assert len(packet["related_context_records"]) == 1
    assert len(packet["source_sections"]) == 1


def test_normalize_runbook_applies_defaults() -> None:
    candidate = _candidate()
    response = {
        "runbook": {
            "title": "Start Operator Station",
            "steps": [
                {
                    "step_number": 1,
                    "title": "Verify AGVs are powered on",
                    "instruction": "Verify that the AGVs are powered on.",
                    "expected_result": "AGVs are powered on.",
                }
            ],
        }
    }

    runbook = normalize_runbook(response, candidate, _Lineage())

    assert runbook["candidate_id"] == candidate["candidate_id"]
    assert runbook["procedure_type"] == "operation"
    assert runbook["role_required"] == "operator"
    assert runbook["metadata"]["merge_status"] == "source_finalized"
    assert candidate["candidate_id"] in runbook["source_candidate_ids"]


def test_validate_runbook_rejects_unknown_artifact() -> None:
    runbook = normalize_runbook(
        {
            "runbook": {
                "title": "Start Operator Station",
                "steps": [
                    {
                        "step_number": 1,
                        "title": "Verify AGVs",
                        "instruction": "Verify AGVs are powered on.",
                        "screens_or_images": [{"artifact_id": "missing_artifact"}],
                    }
                ],
            }
        },
        _candidate(),
        _Lineage(),
    )

    errors = validate_runbook(runbook, {"artifact_manual_fig_4_19_operator_station_control_panel"}, {"ctx_operator_station_overview_v1"})

    assert any("unknown artifact_id" in error for error in errors)


def test_write_runbook_review_markdown_includes_header_and_steps() -> None:
    runbook = normalize_runbook(
        {
            "runbook": {
                "title": "Start Operator Station",
                "steps": [
                    {
                        "step_number": 1,
                        "title": "Verify AGVs are powered on",
                        "instruction": "Verify that the AGVs are powered on.",
                        "expected_result": "AGVs are powered on.",
                    }
                ],
            }
        },
        _candidate(),
        _Lineage(),
    )

    markdown = write_runbook_review_markdown(runbook)

    assert "# Start Operator Station" in markdown
    assert "## Runbook Header" in markdown
    assert "### Step 1 — Verify AGVs are powered on" in markdown


def test_write_runbook_review_markdown_embeds_step_images(tmp_path) -> None:
    image_path = tmp_path / "artifacts" / "artifact_test_panel.png"
    image_path.parent.mkdir(parents=True)
    image_path.write_bytes(b"png")
    review_path = tmp_path / "review" / "runbook.md"
    review_path.parent.mkdir(parents=True)
    artifact_index = {
        "artifact_test_panel": {
            "artifact_id": "artifact_test_panel",
            "storage_path": str(image_path),
            "short_description": "Operator panel screenshot",
        }
    }
    runbook = {
        "title": "Open Panel",
        "procedure_id": "proc_open_panel_v1",
        "procedure_type": "operation",
        "role_required": "operator",
        "supporting_roles": [],
        "support_safe": True,
        "validation_status": "needs_sme_review",
        "metadata": {"merge_status": "source_finalized"},
        "summary": "Open the panel.",
        "when_to_use": "Use when opening the panel.",
        "steps": [
            {
                "step_number": 1,
                "title": "Locate panel",
                "instruction": "Locate the operator panel.",
                "expected_result": "Panel is visible.",
                "screens_or_images": [
                    {
                        "artifact_id": "artifact_test_panel",
                        "what_to_look_at": "Operator panel power button in the upper-right corner.",
                    }
                ],
            }
        ],
    }

    markdown = write_runbook_review_markdown(
        runbook,
        artifact_index=artifact_index,
        review_markdown_path=review_path,
        repo_root=tmp_path,
    )

    assert "**Screens / Images:**" in markdown
    assert "assets/" in markdown
    copied = list((review_path.parent / "assets").glob("*"))
    assert copied
    assert copied[0].name == hashlib.sha1(b"artifact_test_panel").hexdigest()[:16] + ".png"
    assert "*Operator panel power button in the upper-right corner.*" in markdown
