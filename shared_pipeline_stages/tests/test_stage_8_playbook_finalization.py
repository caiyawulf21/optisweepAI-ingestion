from __future__ import annotations

from pathlib import Path

from shared_pipeline_stages.stage_6_5.embedder import MockRunbookEmbedder
from shared_pipeline_stages.stage_6_5.json_utils import read_json
from shared_pipeline_stages.stage_8.comparison_report import build_comparison_report, build_variant_report
from shared_pipeline_stages.stage_8.link_scoring import (
    build_retrieval_query_text,
    normalize_placeholder_text,
    procedure_type_boost,
    rank_matches_for_node,
)
from shared_pipeline_stages.stage_8.normalize import (
    filter_compatible_matches,
    reconcile_llm_runbook_links,
    select_runbook_matches,
    validate_finalized_playbook,
)
from shared_pipeline_stages.stage_8.playbook_builder import Stage8BuildConfig, build_stage8_finalized_playbooks
from shared_pipeline_stages.stage_8.playbook_retrieval import build_playbook_retrieval_card, build_playbook_retrieval_index
from shared_pipeline_stages.stage_8.runbook_search import RunbookCatalogSearch
from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_build_playbook_retrieval_card_from_sample() -> None:
    candidates = read_json(
        REPO_ROOT
        / "incidenceknowledgeingestion/data/output/incidents/case_228086/stage_5_runbook_candidates/playbook_prompt_a_one_per_incident/playbook_candidates.json"
    )
    card = build_playbook_retrieval_card(candidates[0], case_id="228086", extraction_mode="one_playbook_candidate_per_incident")
    assert card.playbook_id
    assert card.node_retrieval_summaries
    assert card.retrieval_text


def test_normalize_placeholder_strips_boilerplate() -> None:
    raw = "Procedure needed to inspect RMS roster and mapping state."
    assert normalize_placeholder_text(raw) == "inspect RMS roster and mapping state."


def test_build_retrieval_query_includes_node_type_and_systems() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Check RMS faults",
        "runbook_placeholder": "Procedure needed to inspect RMS roster.",
    }
    query = build_retrieval_query_text(node, affected_systems=["RMS", "AGV fleet"])
    assert "diagnostic_decision" in query
    assert "RMS" in query
    assert "Procedure needed to" not in query


def test_procedure_type_boost_prefers_diagnostic_on_diagnostic_node() -> None:
    assert procedure_type_boost("diagnostic_decision", "diagnostic") == 0.08
    assert procedure_type_boost("diagnostic_decision", "recovery") == 0.0


def test_filter_compatible_matches_blocks_recovery_on_diagnostic_node() -> None:
    node = {"node_type": "diagnostic_decision"}
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_diag_v1",
            title="Inspect RMS",
            procedure_type="diagnostic",
            cosine_score=0.4,
            jaccard_score=0.2,
            combined_score=0.35,
        ),
        RunbookSearchMatch(
            procedure_id="proc_recovery_v1",
            title="Restart service",
            procedure_type="recovery",
            cosine_score=0.5,
            jaccard_score=0.2,
            combined_score=0.45,
        ),
    ]
    filtered = filter_compatible_matches(node, matches)
    assert [item.procedure_id for item in filtered] == ["proc_diag_v1"]


def test_intent_alignment_prefers_status_check_over_recovery_prep() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Determine whether AGVs remain out of sync after service recovery",
        "intent": "Check whether service recovery alone restored fleet consistency.",
        "runbook_placeholder": "Procedure needed to inspect RMS roster and AGV error views after recovery.",
    }
    gather_runbook = {
        "procedure_id": "proc_gather_required_fault_information_before_entering_the_grid_for_agv_recovery_v1",
        "title": "Gather Required Fault Information Before Entering the Grid for AGV Recovery",
        "procedure_type": "diagnostic",
        "summary": "Collect AGV and RMS details before going inside the grid for fault recovery.",
        "when_to_use": "Use before going inside the grid for AGV fault recovery.",
        "not_for": ["Do not use as the physical AGV recovery procedure inside the grid."],
    }
    check_runbook = {
        "procedure_id": "proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
        "title": "Check Overall System RMS For System Faults And Active AGV Faults",
        "procedure_type": "diagnostic",
        "summary": "Use the Overall System RMS page to determine whether system faults or active AGV faults are present.",
        "when_to_use": "Use during support troubleshooting when determining whether faults are currently visible in RMS.",
    }
    matches = [
        RunbookSearchMatch(
            procedure_id=gather_runbook["procedure_id"],
            title=gather_runbook["title"],
            procedure_type="diagnostic",
            cosine_score=0.52,
            jaccard_score=0.22,
            combined_score=0.5889,
        ),
        RunbookSearchMatch(
            procedure_id=check_runbook["procedure_id"],
            title=check_runbook["title"],
            procedure_type="diagnostic",
            cosine_score=0.48,
            jaccard_score=0.20,
            combined_score=0.5472,
        ),
    ]
    runbooks_by_id = {
        gather_runbook["procedure_id"]: gather_runbook,
        check_runbook["procedure_id"]: check_runbook,
    }
    ranked = rank_matches_for_node(node, matches, runbooks_by_id=runbooks_by_id)
    assert ranked[0][0].procedure_id == check_runbook["procedure_id"]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    assert selected[0][0].procedure_id == check_runbook["procedure_id"]
    corrected = reconcile_llm_runbook_links(
        node,
        [{"procedure_id": gather_runbook["procedure_id"], "link_confidence": "high"}],
        matches,
        runbooks_by_id=runbooks_by_id,
    )
    assert corrected[0]["procedure_id"] == check_runbook["procedure_id"]


def test_canonical_source_adjustment_prefers_manual_over_training() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import canonical_source_adjustment

    manual = RunbookSearchMatch(
        procedure_id="proc_manual_v1",
        title="Manual RMS check",
        procedure_type="diagnostic",
        cosine_score=0.4,
        jaccard_score=0.2,
        combined_score=0.5,
        source_type="manual",
    )
    training = RunbookSearchMatch(
        procedure_id="proc_training_v1",
        title="Training RMS check",
        procedure_type="diagnostic",
        cosine_score=0.4,
        jaccard_score=0.2,
        combined_score=0.5,
        source_type="training_video",
    )
    assert canonical_source_adjustment(manual) > canonical_source_adjustment(training)


def test_select_low_confidence_when_only_weak_match() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "runbook_placeholder": "Procedure needed to inspect RMS roster and mapping state.",
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_example_v1",
            title="Unrelated manual task",
            procedure_type="diagnostic",
            cosine_score=0.2,
            jaccard_score=0.1,
            combined_score=0.38,
        )
    ]
    selected = select_runbook_matches(node, matches)
    assert len(selected) == 1
    assert selected[0][1] in {"low", "medium"}


def test_stage8_pilot_build_without_llm(tmp_path: Path) -> None:
    pool_dir = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool"
    stage7_dir = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks"
    incidents_root = REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents"
    if not (pool_dir / "retrieval_cards.json").is_file():
        return
    if not (stage7_dir / "canonical_runbooks.json").is_file():
        return

    result = build_stage8_finalized_playbooks(
        pool_dir=pool_dir,
        stage7_dir=stage7_dir,
        incidents_root=incidents_root,
        output_dir=tmp_path,
        config=Stage8BuildConfig(case_ids=["228086", "228723"], use_mock_embedder=True),
        embedder=MockRunbookEmbedder(dimensions=8),
    )
    stage_dir = tmp_path / "stage_8_finalized_playbooks"
    assert result.playbook_count >= 4
    prompt_a = read_json(stage_dir / "prompt_a_one_per_incident/canonical_playbooks.json")
    assert prompt_a["playbooks"]
    comparison = read_json(stage_dir / "stage_8_comparison_report.json")
    assert comparison["case_ids"] == ["228086", "228723"]
    html_files = list((stage_dir / "prompt_a_one_per_incident/review_markdown/playbooks").glob("*.html"))
    assert html_files


def test_validate_rejects_unknown_procedure_id() -> None:
    playbook = {
        "nodes": [
            {
                "node_id": "node_1",
                "node_type": "procedure_reference",
                "runbook_links": [{"procedure_id": "proc_does_not_exist", "link_confidence": "high"}],
            }
        ]
    }
    warnings = validate_finalized_playbook(playbook, runbooks_by_id={})
    assert any("unknown procedure_id" in warning for warning in warnings)


def test_comparison_report_includes_both_variants() -> None:
    reports = [
        build_variant_report([], extraction_mode="one_playbook_candidate_per_incident", case_ids=["228086"], warnings=[]),
        build_variant_report([], extraction_mode="one_or_more_playbook_candidates_when_separable", case_ids=["228086"], warnings=[]),
    ]
    payload = build_comparison_report(reports, case_ids=["228086"], generated_at="2026-01-01T00:00:00Z")
    assert len(payload["variant_reports"]) == 2
