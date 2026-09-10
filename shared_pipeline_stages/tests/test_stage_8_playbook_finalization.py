from __future__ import annotations

from pathlib import Path

from shared_pipeline_stages.stage_6_5.embedder import MockRunbookEmbedder
from shared_pipeline_stages.stage_6_5.json_utils import read_json
from shared_pipeline_stages.stage_8.comparison_report import build_comparison_report, build_variant_report
from shared_pipeline_stages.stage_8.link_scoring import (
    build_retrieval_query_text,
    node_expects_capabilities,
    surface_hint_adjustment,
    node_is_site_interview,
    normalize_placeholder_text,
    procedure_type_boost,
    rank_matches_for_node,
)
from shared_pipeline_stages.stage_8.normalize import (
    build_branches_from_hints,
    build_decision_outcomes,
    evaluate_link_confidence,
    evidence_domain_penalty,
    filter_compatible_matches,
    intent_domain_penalty,
    reconcile_llm_runbook_links,
    repair_playbook_graph_cycles,
    runbook_exact_fit_gaps,
    select_runbook_matches,
    validate_finalized_playbook,
)
from shared_pipeline_stages.stage_8.playbook_builder import (
    Stage8BuildConfig,
    _merge_llm_node,
    _load_playbook_candidates,
    _load_runbooks_for_linking,
    build_stage8_finalized_playbooks,
)
from shared_pipeline_stages.stage_8.playbook_retrieval import build_playbook_retrieval_card, build_playbook_retrieval_index
from shared_pipeline_stages.stage_8.review_markdown import _render_node_markdown
from shared_pipeline_stages.stage_8.action_synthesis import (
    _technical_field_mapping,
    synthesize_diagnostic_action_plan,
)
from shared_pipeline_stages.stage_8.runbook_search import RunbookCatalogSearch
from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch

from providers.local_storage import LocalStorageProvider


class _FakeBrainEmbeddingProvider:
    """Zero-network stand-in for EmbeddingProvider, matching the
    MockRunbookEmbedder pattern already used for Stage 6.5's own embedder
    in this test module -- ontology-snippet retrieval in
    brain_snippets_for_stage5_playbook needs an embedder, but this test
    only exercises Stage 8's linking/finalization logic, not real semantic
    grounding."""

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]

    def embedding_model_id(self) -> str:
        return "fake"


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
    assert card.title in card.retrieval_text
    assert card.user_facing_summary not in card.retrieval_text
    for system in card.affected_systems_or_components:
        assert system not in card.retrieval_text
    for symptom in card.observed_entry_symptoms:
        assert symptom in card.retrieval_text


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


def test_intent_alignment_does_not_prefer_rms_over_wcs_sql_for_system_state() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import intent_alignment_adjustment

    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm fleet / system down state",
        "intent": "Determine whether the system is down and AGVs show faults.",
        "runbook_placeholder": "Check RMS Overall System and/or SSMS SystemDatabaseModel / active errors.",
        "expects_capability": ["fleet_system_status"],
        "expects_surface": ["rms_ui"],
    }
    rms_runbook = {
        "procedure_id": "proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
        "title": "Check Overall System RMS For System Faults And Active AGV Faults",
        "procedure_type": "diagnostic",
        "summary": "Use Overall System RMS for system faults and active AGV faults.",
        "access_surface": ["rms_ui"],
        "capability_tags": ["fleet_system_status", "agv_active_errors"],
    }
    sql_runbook = {
        "procedure_id": "proc_query_system_state_from_the_wcs_database_v1",
        "title": "Query System State From The WCS Database",
        "procedure_type": "diagnostic",
        "summary": "Query SystemDatabaseModel / SystemStateModel in SSMS for system state.",
        "access_surface": ["wcs_sql"],
        "capability_tags": ["fleet_system_status"],
    }
    rms_match = RunbookSearchMatch(
        procedure_id=rms_runbook["procedure_id"],
        title=rms_runbook["title"],
        procedure_type="diagnostic",
        cosine_score=0.50,
        jaccard_score=0.20,
        combined_score=0.50,
    )
    sql_match = RunbookSearchMatch(
        procedure_id=sql_runbook["procedure_id"],
        title=sql_runbook["title"],
        procedure_type="diagnostic",
        cosine_score=0.50,
        jaccard_score=0.20,
        combined_score=0.50,
    )
    rms_adj = intent_alignment_adjustment(node, rms_match, rms_runbook)
    sql_adj = intent_alignment_adjustment(node, sql_match, sql_runbook)
    assert sql_adj >= rms_adj - 0.02


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


def test_recovery_prep_only_yields_no_link_for_check_node() -> None:
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
    }
    matches = [
        RunbookSearchMatch(
            procedure_id=gather_runbook["procedure_id"],
            title=gather_runbook["title"],
            procedure_type="diagnostic",
            cosine_score=0.62,
            jaccard_score=0.25,
            combined_score=0.62,
        )
    ]
    assert select_runbook_matches(node, matches, runbooks_by_id={gather_runbook["procedure_id"]: gather_runbook}) == []
    assert reconcile_llm_runbook_links(
        node,
        [{"procedure_id": gather_runbook["procedure_id"], "link_confidence": "high"}],
        matches,
        runbooks_by_id={gather_runbook["procedure_id"]: gather_runbook},
    ) == []


def test_pairing_gap_caps_confidence_to_low() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm zone pairing failure pattern",
        "intent": "Determine whether pairing failure is present.",
        "runbook_placeholder": "Procedure needed to validate zone pairing failure and hospital diversion in RMS.",
    }
    runbook = {
        "procedure_id": "proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
        "title": "Check Overall System RMS For System Faults And Active AGV Faults",
        "procedure_type": "diagnostic",
        "summary": "Use Overall System RMS for system and AGV faults.",
    }
    match = RunbookSearchMatch(
        procedure_id=runbook["procedure_id"],
        title=runbook["title"],
        procedure_type="diagnostic",
        cosine_score=0.55,
        jaccard_score=0.2,
        combined_score=0.55,
    )
    confidence, _, gaps = evaluate_link_confidence(node, match, runbook=runbook, llm_confidence="high")
    assert any("pairing" in gap.lower() or "hospital" in gap.lower() for gap in gaps)
    assert confidence == "low"


def test_synthesized_outcomes_include_observer_and_tool() -> None:
    node = {
        "node_id": "node_1",
        "node_type": "diagnostic_decision",
        "title": "Confirm active AGV errors",
        "intent": "Determine whether AGVs show active errors.",
        "runbook_placeholder": "Procedure needed to confirm active AGV errors via RMS and/or WCS/SSMS read-only query.",
        "expects_capability": ["agv_active_errors"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["L2_support"],
        "expected_or_observed_result": "Remote L2 checks RMS and SSMS; healthy when no active errors.",
    }
    outcomes = build_decision_outcomes(node, {}, linked_runbook_ids=[], branch_hints=[])
    assert outcomes
    assert all(item.get("observer") == "remote" for item in outcomes)
    assert all("WCS/SSMS" in str(item.get("tool_or_view") or "") for item in outcomes)


def test_site_interview_node_skips_runbook_links() -> None:
    node = {
        "node_type": "branching_condition",
        "title": "Check whether recent remove/add activity is part of the incident context",
        "intent": "Choose direction based on recent robot handling.",
        "runbook_placeholder": (
            "Procedure needed to confirm with the site whether the site recently replaced, added, or removed any AMRs."
        ),
    }
    assert node_is_site_interview(node)
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_gather_required_fault_information_before_entering_the_grid_for_agv_recovery_v1",
            title="Gather Required Fault Information Before Entering the Grid for AGV Recovery",
            procedure_type="diagnostic",
            cosine_score=0.6,
            jaccard_score=0.2,
            combined_score=0.6,
        )
    ]
    assert select_runbook_matches(node, matches) == []
    assert reconcile_llm_runbook_links(
        node,
        [{"procedure_id": matches[0].procedure_id, "link_confidence": "high"}],
        matches,
        runbooks_by_id={},
    ) == []


def test_site_history_branch_skips_runbook_links() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import node_is_site_history_branch

    node = {
        "node_type": "branching_condition",
        "title": "Check whether recent remove/add or replacement activity is part of the incident context",
        "intent": "Choose the next troubleshooting direction.",
        "runbook_placeholder": (
            "Procedure needed to review recent site-reported robot handling history and any RMS evidence "
            "of recent add, remove, replacement, or hospital-flow activity for specific robot IDs."
        ),
    }
    assert node_is_site_history_branch(node)
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_verify_which_metrics_are_present_on_the_acb_system_statistics_screen_v1",
            title="Verify Which Metrics Are Present on the ACB System Statistics Screen",
            procedure_type="reference",
            cosine_score=0.6,
            jaccard_score=0.2,
            combined_score=0.6,
        )
    ]
    assert select_runbook_matches(node, matches) == []


def test_orchestration_rubric_branch_skips_runbook_links() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import node_is_site_history_branch

    node = {
        "node_type": "branching_condition",
        "title": "Check for recent AGV replacement or remove/add history",
        "intent": "Decide whether to prioritize RMS roster or mapping investigation.",
        "runbook_placeholder": (
            "Procedure needed for a branching rubric that uses incident questioning guidance and RMS / fleet "
            "status context to determine whether recent AGV replacement, add, remove, or return-through-hospital "
            "activity should shift troubleshooting toward roster or mapping abnormalities."
        ),
    }
    assert node_is_site_history_branch(node)
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
            title="Check Overall System RMS For System Faults And Active AGV Faults",
            procedure_type="diagnostic",
            cosine_score=0.6,
            jaccard_score=0.2,
            combined_score=0.6,
        )
    ]
    assert select_runbook_matches(node, matches) == []


def test_symptom_pattern_diagnostic_gets_unhealthy_and_healthy_branches() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import node_is_symptom_pattern_confirmation

    node = {
        "node_id": "node_1",
        "node_order": 1,
        "node_type": "diagnostic_decision",
        "title": "Confirm the pairing-failure and hospital-diversion symptom pattern",
        "intent": "Determine whether the reported issue matches zone-level pairing failure with hospital diversion.",
        "runbook_placeholder": (
            "Procedure needed to confirm the reported pairing failure and hospital-lane diversion pattern using "
            "RMS / fleet status views that show current AGV routing or abnormal-state indicators."
        ),
    }
    all_nodes = [
        node,
        {
            "node_id": "node_2",
            "node_order": 2,
            "node_type": "diagnostic_decision",
            "title": "Inspect RMS roster state",
        },
        {
            "node_id": "node_6",
            "node_order": 6,
            "node_type": "escalation_gate",
            "title": "Escalate when unsupported",
        },
    ]
    assert node_is_symptom_pattern_confirmation(node)
    branch_hints = [
        {
            "from_node_id": "node_1",
            "condition_or_signal": "Reported zone cannot get a pair and AMRs are diverting to hospital lane",
            "suggested_next_node_id": "node_2",
        },
        {
            "from_node_id": "node_3",
            "condition_or_signal": "RMS evidence is unreadable, inconclusive, or does not identify a supported suspect AGV path",
            "suggested_next_node_id": "node_6",
        },
    ]
    branches = build_branches_from_hints(node, branch_hints, all_nodes=all_nodes)
    outcomes = {branch["outcome"] for branch in branches}
    assert outcomes == {"healthy", "unhealthy"}
    unhealthy = next(branch for branch in branches if branch["outcome"] == "unhealthy")
    healthy = next(branch for branch in branches if branch["outcome"] == "healthy")
    assert unhealthy["next_node_id"] == "node_2"
    assert healthy["next_node_id"] == "node_6"


def test_validation_gate_gets_recovery_branches() -> None:
    node = {
        "node_id": "node_5",
        "node_order": 5,
        "node_type": "validation_gate",
        "title": "Validate that pairing and routing behavior have normalized",
        "intent": "Confirm recovery after suspect AGV isolation.",
        "runbook_placeholder": "Procedure needed to validate recovery in RMS / fleet status.",
    }
    all_nodes = [
        node,
        {
            "node_id": "node_6",
            "node_order": 6,
            "node_type": "escalation_gate",
            "title": "Escalate unsupported recovery",
        },
    ]
    branch_hints = [
        {
            "from_node_id": "node_4",
            "condition_or_signal": "Suspect AGV has been isolated from active operation",
            "suggested_next_node_id": "node_5",
        },
        {
            "from_node_id": "node_3",
            "condition_or_signal": "No supported abnormal robot state is identified, or the needed correction is outside role authority",
            "suggested_next_node_id": "node_6",
        },
    ]
    branches = build_branches_from_hints(node, branch_hints, all_nodes=all_nodes)
    outcomes = {branch["outcome"] for branch in branches}
    assert "healthy" in outcomes
    assert "unhealthy" in outcomes
    assert any(branch["outcome"] == "unhealthy" and branch["next_node_id"] == "node_6" for branch in branches)


def test_roster_mapping_node_blocks_hospital_hmi_alarms() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Inspect RMS for abnormal robot roster or mapping state tied to the incident",
        "intent": "Determine whether robots appear not mapped or improperly rostered in RMS.",
        "runbook_placeholder": "Procedure needed to inspect RMS fleet, roster, and mapping-related views.",
    }
    hospital_alarms = RunbookSearchMatch(
        procedure_id="proc_review_active_alarms_on_the_hospital_hmi_alarms_screen_v1",
        title="Review Active Alarms On the Hospital HMI Alarms Screen",
        procedure_type="diagnostic",
        cosine_score=0.52,
        jaccard_score=0.18,
        combined_score=0.52,
    )
    fleet = RunbookSearchMatch(
        procedure_id="proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
        title="Check Overall System RMS For System Faults And Active AGV Faults",
        procedure_type="diagnostic",
        cosine_score=0.48,
        jaccard_score=0.16,
        combined_score=0.48,
        source_type="training_video",
    )
    hospital_penalty, _ = intent_domain_penalty(node, hospital_alarms, None)
    fleet_penalty, _ = intent_domain_penalty(node, fleet, None)
    assert hospital_penalty < 0.0
    assert fleet_penalty == 0.0


def test_roster_mapping_node_filters_bump_exception_reference() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Inspect RMS for abnormal robot roster or mapping state tied to the incident",
        "intent": "Determine whether robots appear not mapped or improperly rostered in RMS.",
        "runbook_placeholder": "Procedure needed to inspect RMS fleet, roster, and mapping-related views.",
    }
    bump = RunbookSearchMatch(
        procedure_id="proc_interpret_agv_bump_exception_codes_on_the_bump_fault_screen_v1",
        title="Interpret AGV BUMP Exception Codes On The Bump Fault Screen",
        procedure_type="reference",
        cosine_score=0.52,
        jaccard_score=0.18,
        combined_score=0.52,
    )
    fleet = RunbookSearchMatch(
        procedure_id="proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
        title="Check Overall System RMS For System Faults And Active AGV Faults",
        procedure_type="diagnostic",
        cosine_score=0.48,
        jaccard_score=0.16,
        combined_score=0.48,
        source_type="training_video",
    )
    bump_penalty, _ = intent_domain_penalty(node, bump, None)
    fleet_penalty, _ = intent_domain_penalty(node, fleet, None)
    assert bump_penalty < 0.0
    assert fleet_penalty == 0.0


def test_isolation_node_blocks_bump_fault_recovery() -> None:
    node = {
        "node_type": "procedure_reference",
        "title": "Perform approved isolation or removal of the suspect robot from the active system",
        "intent": "Perform the authorized robot-isolation or removal action.",
        "runbook_placeholder": (
            "Procedure needed for authorized isolation or removal of a specific robot from the active RMS-managed fleet."
        ),
    }
    bump = RunbookSearchMatch(
        procedure_id="proc_recover_an_agv_from_a_bump_fault_code_v1",
        title="Recover An AGV From A BUMP Fault Code",
        procedure_type="recovery",
        cosine_score=0.58,
        jaccard_score=0.18,
        combined_score=0.58,
    )
    penalty, _ = intent_domain_penalty(node, bump, None)
    assert penalty < 0.0


def test_fleet_status_bundle_can_select_primary_and_alternate() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Inspect RMS for abnormal robot roster or mapping state tied to the incident",
        "intent": "Determine whether robots appear abnormal in RMS roster or mapping views.",
        "runbook_placeholder": "Procedure needed to inspect RMS fleet, roster, and mapping-related views for named robot IDs.",
    }
    runbooks_by_id = {
        "proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1": {
            "procedure_id": "proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
            "title": "Check Overall System RMS For System Faults And Active AGV Faults",
            "procedure_type": "diagnostic",
            "summary": "Use the Overall System RMS page to determine whether system faults or active AGV faults are present.",
            "when_to_use": "Use during support troubleshooting when determining whether faults are currently visible in RMS.",
            "metadata": {"source_type": "training_video"},
        },
        "proc_open_the_agv_status_screen_and_check_agv_locations_and_current_error_codes_v1": {
            "procedure_id": "proc_open_the_agv_status_screen_and_check_agv_locations_and_current_error_codes_v1",
            "title": "Open the AGV Status Screen and Check AGV Locations and Current Error Codes",
            "procedure_type": "diagnostic",
            "summary": "Access the AGV Status screen from the system HMI and review AGV locations and current error codes.",
            "when_to_use": "Use when AGV location information or currently displayed AGV error codes need to be checked.",
            "metadata": {"source_type": "manual"},
        },
        "proc_review_fleet_status_on_the_overall_system_agv_status_screen_v1": {
            "procedure_id": "proc_review_fleet_status_on_the_overall_system_agv_status_screen_v1",
            "title": "Review Fleet Status On the Overall System AGV Status Screen",
            "procedure_type": "diagnostic",
            "summary": "Use the Overall System AGV Status screen to review fleet-wide AGV information.",
            "when_to_use": "Use when reviewing fleet-level AGV status and identifying AGVs currently shown with errors.",
            "metadata": {"source_type": "training_video"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
            title=runbooks_by_id["proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.55,
            jaccard_score=0.14,
            combined_score=0.55,
            source_type="training_video",
        ),
        RunbookSearchMatch(
            procedure_id="proc_open_the_agv_status_screen_and_check_agv_locations_and_current_error_codes_v1",
            title=runbooks_by_id["proc_open_the_agv_status_screen_and_check_agv_locations_and_current_error_codes_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.5,
            jaccard_score=0.12,
            combined_score=0.5,
            source_type="manual",
        ),
        RunbookSearchMatch(
            procedure_id="proc_review_fleet_status_on_the_overall_system_agv_status_screen_v1",
            title=runbooks_by_id["proc_review_fleet_status_on_the_overall_system_agv_status_screen_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.49,
            jaccard_score=0.11,
            combined_score=0.49,
            source_type="training_video",
        ),
    ]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    assert len(selected) >= 2
    fleet_ids = {
        "proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1",
        "proc_open_the_agv_status_screen_and_check_agv_locations_and_current_error_codes_v1",
        "proc_review_fleet_status_on_the_overall_system_agv_status_screen_v1",
    }
    assert selected[0][0].procedure_id in fleet_ids
    assert {item[0].procedure_id for item in selected}.issubset(fleet_ids)
    assert len({item[0].procedure_id for item in selected}) >= 2


def test_synthesized_outcomes_cover_healthy_unhealthy_inconclusive() -> None:
    node = {
        "node_id": "node_1",
        "node_type": "diagnostic_decision",
        "title": "Confirm the pairing-failure and hospital-diversion symptom pattern",
        "intent": "Determine whether the current incident matches the observable pattern.",
        "expected_or_observed_result": "Some symptoms are present but not fully confirmed.",
    }
    branch_hints = [
        {
            "from_node_id": "node_1",
            "condition_or_signal": "Zone cannot get a pair and AMRs are going to the hospital after recent robot replacement or add/remove activity",
            "suggested_next_node_id": "node_2",
        }
    ]
    outcomes = build_decision_outcomes(
        node,
        {},
        linked_runbook_ids=[],
        branch_hints=branch_hints,
    )
    labels = {item["outcome_label"] for item in outcomes}
    assert labels >= {"healthy", "unhealthy", "inconclusive"}
    unhealthy = next(item for item in outcomes if item["outcome_label"] == "unhealthy")
    assert "zone 5" not in unhealthy["descriptor"].lower()
    assert "robot 158" not in unhealthy["descriptor"].lower()
    assert "pairing failure" in unhealthy["descriptor"].lower() or "hospital-diversion" in unhealthy["descriptor"].lower()


def test_domain_filter_blocks_bump_on_event_viewer_node() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import runbook_is_wrong_domain_for_node

    node = {
        "node_type": "diagnostic_decision",
        "title": "Inspect Windows Event Viewer for clustered application faults",
        "intent": "Determine whether application log faults correlate with service instability.",
        "runbook_placeholder": "Procedure needed to inspect Windows Event Viewer Application and System logs for clustered faults.",
    }
    bump = RunbookSearchMatch(
        procedure_id="proc_interpret_agv_bump_exception_codes_on_the_bump_fault_screen_v1",
        title="Interpret AGV BUMP Exception Codes On The Bump Fault Screen",
        procedure_type="reference",
        cosine_score=0.5,
        jaccard_score=0.2,
        combined_score=0.5,
    )
    assert runbook_is_wrong_domain_for_node(node, {}, bump)


def test_branching_node_gets_complementary_branch() -> None:
    node = {
        "node_id": "node_2",
        "node_order": 2,
        "node_type": "branching_condition",
        "title": "Check whether recent remove/add or replacement activity is part of the incident context",
        "intent": "Choose the next troubleshooting direction.",
    }
    all_nodes = [
        node,
        {
            "node_id": "node_3",
            "node_order": 3,
            "node_type": "diagnostic_decision",
            "title": "Inspect RMS for abnormal robot state",
        },
        {
            "node_id": "node_6",
            "node_order": 6,
            "node_type": "escalation_gate",
            "title": "Escalate when outside role",
        },
    ]
    branch_hints = [
        {
            "from_node_id": "node_2",
            "condition_or_signal": "Recent robot handling changes are confirmed",
            "suggested_next_node_id": "node_3",
        },
        {
            "from_node_id": "node_3",
            "condition_or_signal": "No supported abnormal robot state is identified, or the needed correction is outside role authority",
            "suggested_next_node_id": "node_6",
        },
    ]
    branches = build_branches_from_hints(node, branch_hints, all_nodes=all_nodes)
    outcomes = {branch["outcome"] for branch in branches}
    next_nodes = {branch["next_node_id"] for branch in branches}
    assert "unhealthy" in outcomes
    assert "healthy" in outcomes
    assert "node_3" in next_nodes
    assert "node_6" in next_nodes


def test_inferred_healthy_does_not_skip_to_post_recovery_node() -> None:
    all_nodes = [
        {
            "node_id": "node_1",
            "node_order": 1,
            "node_type": "diagnostic_decision",
            "title": "Confirm site-wide stoppage and abnormal control-system presentation",
            "intent": "Determine whether the reported issue matches a broad robotic-system stoppage pattern.",
            "runbook_placeholder": "Confirm site-wide stoppage and abnormal HMI presentation.",
        },
        {
            "node_id": "node_2",
            "node_order": 2,
            "node_type": "diagnostic_decision",
            "title": "Confirm OptiSweep service failure evidence",
        },
        {
            "node_id": "node_5",
            "node_order": 5,
            "node_type": "procedure_reference",
            "title": "Perform approved recovery for the affected service or gateway",
            "intent": "Carry out the authorized recovery action.",
            "runbook_placeholder": "Authorized recovery of the OptiSweep service or Ignition gateway.",
        },
        {
            "node_id": "node_6",
            "node_order": 6,
            "node_type": "diagnostic_decision",
            "title": "Check for residual AGV desynchronization after service recovery",
            "intent": "Identify out-of-sync AGVs after recovery.",
            "runbook_placeholder": "Inspect AGV fleet for out-of-sync assets after service or gateway recovery.",
        },
        {
            "node_id": "node_9",
            "node_order": 9,
            "node_type": "escalation_gate",
            "title": "Escalate unsupported recovery",
        },
    ]
    branch_hints = [
        {
            "from_node_id": "node_5",
            "condition_or_signal": "Primary service or gateway recovery completed",
            "suggested_next_node_id": "node_6",
        },
        {
            "from_node_id": "node_6",
            "condition_or_signal": "Out-of-sync or abnormal AGVs are present in RMS",
            "suggested_next_node_id": "node_7",
        },
    ]
    node_1 = all_nodes[0]
    branches = build_branches_from_hints(node_1, branch_hints, all_nodes=all_nodes)
    healthy = next(branch for branch in branches if branch["outcome"] == "healthy")
    unhealthy = next(branch for branch in branches if branch["outcome"] == "unhealthy")
    assert healthy["next_node_id"] != "node_6"
    assert unhealthy["next_node_id"] == "node_2"
    assert not any(
        branch["branch_id"].endswith("inferred_healthy") and branch["next_node_id"] == "node_6"
        for branch in branches
    )

    node_5 = all_nodes[2]
    recovery_branches = build_branches_from_hints(node_5, branch_hints, all_nodes=all_nodes)
    recovery_completed = next(
        branch for branch in recovery_branches if "recovery completed" in branch["condition_label"].lower()
    )
    assert recovery_completed["outcome"] == "healthy"
    assert recovery_completed["next_node_id"] == "node_6"

    node_6 = all_nodes[3]
    node_6_branches = build_branches_from_hints(node_6, branch_hints, all_nodes=all_nodes)
    healthy_6 = next(branch for branch in node_6_branches if branch["outcome"] == "healthy")
    assert healthy_6["next_node_id"] != "node_6"


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
    assert selected == []


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
        # Ontology grounding now comes from Brain (brain_ontology_bridge.py)
        # -- an isolated, empty LocalStorageProvider plus a zero-network
        # fake embedder keep this test exercising Stage 8's own
        # linking/finalization logic without touching the real local
        # corpus or making real Azure embedding calls.
        brain_storage=LocalStorageProvider(root=tmp_path / "_brain_storage"),
        brain_embeddings=_FakeBrainEmbeddingProvider(),
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


def test_capability_overlap_boosts_matching_runbook() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import (
        boost_combined_score,
        capability_overlap_adjustment,
    )

    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm active AGV errors",
        "intent": "Determine whether AGVs show active errors.",
        "runbook_placeholder": "Procedure needed to confirm active AGV errors via RMS and/or WCS/SSMS.",
        "expects_capability": ["agv_active_errors"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["L1_support", "L2_support"],
    }
    rms = {
        "procedure_id": "proc_rms_agv_errors",
        "title": "Check Overall System RMS For Active AGV Faults",
        "procedure_type": "diagnostic",
        "capability_tags": ["agv_active_errors"],
        "access_surface": ["rms_ui"],
        "audience_roles": ["L1_support"],
        "role_required": "L1_support",
    }
    sql = {
        "procedure_id": "proc_ssms_agv_errors",
        "title": "Query SystemActiveErrorModel in WCS Robotics DB",
        "procedure_type": "diagnostic",
        "capability_tags": ["agv_active_errors"],
        "access_surface": ["wcs_sql"],
        "audience_roles": ["L2_support"],
        "role_required": "L2_support",
    }
    tipper = {
        "procedure_id": "proc_tipper_visu",
        "title": "Check Tipper VISU Alarm Screen",
        "procedure_type": "diagnostic",
        "capability_tags": ["tipper_station_fault"],
        "access_surface": ["tipper_hmi"],
        "audience_roles": ["operator"],
        "role_required": "operator",
    }
    assert capability_overlap_adjustment(node, rms) > 0.15
    assert capability_overlap_adjustment(node, sql) > 0.15
    assert capability_overlap_adjustment(node, tipper) < 0

    rms_match = RunbookSearchMatch(
        procedure_id=rms["procedure_id"],
        title=rms["title"],
        procedure_type="diagnostic",
        cosine_score=0.4,
        jaccard_score=0.1,
        combined_score=0.4,
    )
    tipper_match = RunbookSearchMatch(
        procedure_id=tipper["procedure_id"],
        title=tipper["title"],
        procedure_type="diagnostic",
        cosine_score=0.45,
        jaccard_score=0.12,
        combined_score=0.45,
    )
    rms_boosted = boost_combined_score(
        0.4, node=node, node_text="agv errors", match=rms_match, runbook=rms, procedure_type_compatible=True
    )
    tipper_boosted = boost_combined_score(
        0.45,
        node=node,
        node_text="agv errors",
        match=tipper_match,
        runbook=tipper,
        procedure_type_compatible=True,
    )
    assert rms_boosted > tipper_boosted


def test_capability_multilink_selects_rms_and_ssms() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm active AGV errors",
        "intent": "Determine whether AGVs show active errors remotely.",
        "runbook_placeholder": "Procedure needed to confirm active AGV errors via RMS fleet status and/or WCS/SSMS read-only query.",
        "expects_capability": ["agv_active_errors"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["operator", "L1_support", "L2_support"],
    }
    runbooks_by_id = {
        "proc_rms_agv_errors_v1": {
            "procedure_id": "proc_rms_agv_errors_v1",
            "title": "Check Overall System RMS For System Faults And Active AGV Faults",
            "procedure_type": "diagnostic",
            "summary": "Use Overall System RMS to determine whether active AGV faults are present.",
            "when_to_use": "Use when checking AGV active faults in RMS.",
            "capability_tags": ["agv_active_errors", "fleet_system_status"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support", "operator"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_ssms_agv_errors_v1": {
            "procedure_id": "proc_ssms_agv_errors_v1",
            "title": "Query Active AGV Errors in WCS Robotics Database",
            "procedure_type": "diagnostic",
            "summary": "Use SSMS read-only query against SystemActiveErrorModel.",
            "when_to_use": "Use when corroborating AGV active errors remotely via WCS SQL.",
            "capability_tags": ["agv_active_errors"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_agv_errors_v1",
            title=runbooks_by_id["proc_rms_agv_errors_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.55,
            jaccard_score=0.2,
            combined_score=0.55,
            source_type="manual",
        ),
        RunbookSearchMatch(
            procedure_id="proc_ssms_agv_errors_v1",
            title=runbooks_by_id["proc_ssms_agv_errors_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.42,
            jaccard_score=0.12,
            combined_score=0.42,
            source_type="manual",
        ),
    ]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    ids = {item[0].procedure_id for item in selected}
    assert "proc_rms_agv_errors_v1" in ids
    assert "proc_ssms_agv_errors_v1" in ids
    assert len(selected) >= 2


def test_surface_coverage_replaces_duplicate_rms_when_slots_full() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm active AGV errors",
        "intent": "Determine whether AGVs show active errors remotely.",
        "runbook_placeholder": "Procedure needed to confirm active AGV errors via RMS fleet status and/or WCS/SSMS read-only query.",
        "expects_capability": ["agv_active_errors"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["operator", "L1_support", "L2_support"],
    }
    runbooks_by_id = {
        "proc_rms_agv_errors_v1": {
            "procedure_id": "proc_rms_agv_errors_v1",
            "title": "Check Overall System RMS For System Faults And Active AGV Faults",
            "procedure_type": "diagnostic",
            "summary": "Use Overall System RMS to determine whether active AGV faults are present.",
            "when_to_use": "Use when checking AGV active faults in RMS.",
            "capability_tags": ["agv_active_errors", "fleet_system_status"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support", "operator"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_rms_disconnected_agv_v1": {
            "procedure_id": "proc_rms_disconnected_agv_v1",
            "title": "Check RMS Disconnected AGV Count Cause",
            "procedure_type": "diagnostic",
            "summary": "Use Overall System RMS to review disconnected AGV counts.",
            "when_to_use": "Use when checking disconnected AGVs in RMS.",
            "capability_tags": ["agv_active_errors", "fleet_system_status"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_rms_fleet_status_v1": {
            "procedure_id": "proc_rms_fleet_status_v1",
            "title": "Check RMS Fleet Status AGVs Exchange Waiting",
            "procedure_type": "diagnostic",
            "summary": "Use RMS fleet status to confirm AGV exchange waiting states.",
            "when_to_use": "Use when checking fleet/RMS status.",
            "capability_tags": ["fleet_system_status", "agv_active_errors"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_ssms_agv_errors_v1": {
            "procedure_id": "proc_ssms_agv_errors_v1",
            "title": "Query Active AGV Errors in WCS Robotics Database",
            "procedure_type": "diagnostic",
            "summary": "Use SSMS read-only query against SystemActiveErrorModel.",
            "when_to_use": "Use when corroborating AGV active errors remotely via WCS SQL.",
            "capability_tags": ["agv_active_errors"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_agv_errors_v1",
            title=runbooks_by_id["proc_rms_agv_errors_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.55,
            jaccard_score=0.2,
            combined_score=0.55,
            source_type="manual",
        ),
        RunbookSearchMatch(
            procedure_id="proc_rms_disconnected_agv_v1",
            title=runbooks_by_id["proc_rms_disconnected_agv_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.52,
            jaccard_score=0.18,
            combined_score=0.52,
            source_type="manual",
        ),
        RunbookSearchMatch(
            procedure_id="proc_rms_fleet_status_v1",
            title=runbooks_by_id["proc_rms_fleet_status_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.50,
            jaccard_score=0.17,
            combined_score=0.50,
            source_type="manual",
        ),
    ]
    llm_links = [
        {"procedure_id": "proc_rms_agv_errors_v1", "link_confidence": "high", "link_rationale": "llm"},
        {"procedure_id": "proc_rms_disconnected_agv_v1", "link_confidence": "medium", "link_rationale": "llm"},
        {"procedure_id": "proc_rms_fleet_status_v1", "link_confidence": "medium", "link_rationale": "llm"},
    ]
    # SQL peer is absent from retrieval matches; coverage should still pull it from catalog.
    reconciled = reconcile_llm_runbook_links(
        node,
        llm_links,
        matches,
        runbooks_by_id=runbooks_by_id,
    )
    ids = [link["procedure_id"] for link in reconciled]
    assert "proc_ssms_agv_errors_v1" in ids
    assert any(
        "wcs_sql" in (runbooks_by_id[pid].get("access_surface") or []) for pid in ids
    )
    assert len(ids) <= 3


def test_surface_coverage_prefers_exclusive_wcs_sql_over_dual_surface() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm active AGV errors",
        "intent": "Determine whether AGVs show active errors remotely.",
        "runbook_placeholder": "Procedure needed to confirm active AGV errors via RMS and/or WCS/SSMS.",
        "expects_capability": ["agv_active_errors"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["L1_support", "L2_support"],
    }
    runbooks_by_id = {
        "proc_rms_agv_errors_v1": {
            "procedure_id": "proc_rms_agv_errors_v1",
            "title": "Check Overall System RMS For Active AGV Faults",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "fleet_system_status"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_rms_disconnected_agv_v1": {
            "procedure_id": "proc_rms_disconnected_agv_v1",
            "title": "Check RMS Disconnected AGV Count Cause",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "fleet_system_status"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_dual_rms_wcs_backfill_v1": {
            "procedure_id": "proc_dual_rms_wcs_backfill_v1",
            "title": "Diagnose AGV exchange/backfill gap when an AGV moves out without a replacement",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "fleet_system_status"],
            "access_surface": ["rms_ui", "wcs_sql"],
            "audience_roles": ["L1_support", "L2_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_query_active_agv_errors_from_the_wcs_database_v1": {
            "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
            "title": "Query Active AGV Errors From the WCS Database",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "wcs_service_health"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_agv_errors_v1",
            title=runbooks_by_id["proc_rms_agv_errors_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.7,
            jaccard_score=0.25,
            combined_score=0.7,
            source_type="manual",
        ),
        RunbookSearchMatch(
            procedure_id="proc_rms_disconnected_agv_v1",
            title=runbooks_by_id["proc_rms_disconnected_agv_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.65,
            jaccard_score=0.22,
            combined_score=0.65,
            source_type="manual",
        ),
        RunbookSearchMatch(
            procedure_id="proc_dual_rms_wcs_backfill_v1",
            title=runbooks_by_id["proc_dual_rms_wcs_backfill_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.68,
            jaccard_score=0.24,
            combined_score=0.68,
            source_type="manual",
        ),
    ]
    llm_links = [
        {"procedure_id": "proc_rms_agv_errors_v1", "link_confidence": "high", "link_rationale": "llm"},
        {"procedure_id": "proc_rms_disconnected_agv_v1", "link_confidence": "medium", "link_rationale": "llm"},
        {"procedure_id": "proc_dual_rms_wcs_backfill_v1", "link_confidence": "medium", "link_rationale": "llm"},
    ]
    reconciled = reconcile_llm_runbook_links(node, llm_links, matches, runbooks_by_id=runbooks_by_id)
    ids = [link["procedure_id"] for link in reconciled]
    assert "proc_query_active_agv_errors_from_the_wcs_database_v1" in ids
    assert "proc_dual_rms_wcs_backfill_v1" not in ids or ids.count("proc_dual_rms_wcs_backfill_v1") == 0


def test_surface_coverage_rejects_active_agv_sql_without_capability() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm fleet system-down status",
        "intent": "Determine whether the overall system is down.",
        "runbook_placeholder": "Procedure needed to confirm fleet/system-down status via RMS and WCS/SSMS.",
        "expects_capability": ["fleet_system_status"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["L1_support", "L2_support"],
    }
    runbooks_by_id = {
        "proc_rms_fleet_status_v1": {
            "procedure_id": "proc_rms_fleet_status_v1",
            "title": "Check Overall System RMS For System Faults",
            "procedure_type": "diagnostic",
            "capability_tags": ["fleet_system_status"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_query_active_agv_errors_from_the_wcs_database_v1": {
            "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
            "title": "Query Active AGV Errors From the WCS Database",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "wcs_service_health"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_check_systemdatabasemodel_lifecycle_staging_status_ssms_v1": {
            "procedure_id": "proc_check_systemdatabasemodel_lifecycle_staging_status_ssms_v1",
            "title": "Check SystemDatabaseModel Lifecycle Staging Status in SSMS",
            "procedure_type": "diagnostic",
            "capability_tags": ["sort_lifecycle_state", "fleet_system_status"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_fleet_status_v1",
            title=runbooks_by_id["proc_rms_fleet_status_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.6,
            jaccard_score=0.2,
            combined_score=0.6,
            source_type="manual",
        ),
    ]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    ids = [item[0].procedure_id for item in selected]
    assert "proc_query_active_agv_errors_from_the_wcs_database_v1" not in ids
    assert "proc_check_systemdatabasemodel_lifecycle_staging_status_ssms_v1" in ids


def test_surface_coverage_prefers_location_sql_for_roster_nodes() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm robot roster mapping",
        "intent": "Determine whether robot roster/mapping is abnormal.",
        "runbook_placeholder": "Procedure needed to confirm roster/mapping via RMS map monitor and WCS robot-location models.",
        "expects_capability": ["device_roster_state"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["operator", "L2_support"],
    }
    runbooks_by_id = {
        "proc_rms_roster_v1": {
            "procedure_id": "proc_rms_roster_v1",
            "title": "Check RMS Robot Roster And Map Monitor",
            "procedure_type": "diagnostic",
            "capability_tags": ["device_roster_state"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["operator", "L1_support"],
            "role_required": "operator",
            "metadata": {"source_type": "manual"},
        },
        "proc_query_active_agv_errors_from_the_wcs_database_v1": {
            "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
            "title": "Query Active AGV Errors From the WCS Database",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "wcs_service_health"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1": {
            "procedure_id": "proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1",
            "title": "Verify Robot Location Model Fields And RMS Orange Location Types",
            "procedure_type": "diagnostic",
            "capability_tags": ["zone_config_state"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_roster_v1",
            title=runbooks_by_id["proc_rms_roster_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.58,
            jaccard_score=0.2,
            combined_score=0.58,
            source_type="manual",
        ),
    ]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    ids = [item[0].procedure_id for item in selected]
    assert "proc_query_active_agv_errors_from_the_wcs_database_v1" not in ids
    assert "proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1" in ids


def test_active_agv_sql_gap_when_capability_not_expected() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import intent_mismatch_gaps

    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm hospital diversion",
        "intent": "Determine whether hospital diversion is active.",
        "runbook_placeholder": "Procedure needed to confirm hospital diversion pattern.",
        "expects_capability": ["hospital_diversion", "zone_pairing_state"],
        "expects_surface": ["rms_ui", "wcs_sql"],
    }
    runbook = {
        "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
        "title": "Query Active AGV Errors From the WCS Database",
        "capability_tags": ["agv_active_errors", "wcs_service_health"],
        "access_surface": ["wcs_sql"],
    }
    match = RunbookSearchMatch(
        procedure_id=runbook["procedure_id"],
        title=runbook["title"],
        procedure_type="diagnostic",
        cosine_score=0.4,
        jaccard_score=0.1,
        combined_score=0.4,
    )
    gaps = intent_mismatch_gaps(node, match, runbook)
    assert any("active agv error sql" in gap.lower() or "wrong catalog family" in gap.lower() for gap in gaps)
    # The active-error-SQL-vs-expected-capability mismatch is now penalized in
    # link_scoring.py's intent_alignment_adjustment (unconditionally, not
    # gated behind USE_CAPABILITY_TAG_CONSTRAINTS as it previously was here),
    # plus intent_domain_penalty's own symptom-corroboration check.
    from shared_pipeline_stages.stage_8.link_scoring import intent_alignment_adjustment

    domain_penalty, _ = intent_domain_penalty(node, match, runbook)
    link_adjustment = intent_alignment_adjustment(node, match, runbook)
    assert domain_penalty < 0.0
    assert link_adjustment < 0.0


def test_mixed_expects_without_error_language_rejects_active_agv_sql() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm hospital induct and pairing scope",
        "intent": "Determine whether hospital station can add/induct totes and whether zone pairing failed.",
        "runbook_placeholder": (
            "Procedure needed to confirm with the site what the hospital station is doing right now "
            "(can they add/induct totes) and whether the zone is unable to get a pair."
        ),
        "expects_capability": ["agv_active_errors", "hospital_diversion", "zone_pairing_state"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["operator", "L2_support"],
    }
    runbooks_by_id = {
        "proc_rms_fleet_status_v1": {
            "procedure_id": "proc_rms_fleet_status_v1",
            "title": "Check Overall System RMS For System Faults",
            "procedure_type": "diagnostic",
            "capability_tags": ["fleet_system_status", "agv_active_errors"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_query_active_agv_errors_from_the_wcs_database_v1": {
            "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
            "title": "Query Active AGV Errors From the WCS Database",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "wcs_service_health"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_check_systemdatabasemodel_lifecycle_staging_status_ssms_v1": {
            "procedure_id": "proc_check_systemdatabasemodel_lifecycle_staging_status_ssms_v1",
            "title": "Check SystemDatabaseModel Lifecycle Staging Status in SSMS",
            "procedure_type": "diagnostic",
            "capability_tags": ["sort_lifecycle_state", "fleet_system_status"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_fleet_status_v1",
            title=runbooks_by_id["proc_rms_fleet_status_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.55,
            jaccard_score=0.18,
            combined_score=0.55,
            source_type="manual",
        ),
    ]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    ids = [item[0].procedure_id for item in selected]
    assert "proc_query_active_agv_errors_from_the_wcs_database_v1" not in ids


def test_active_agv_sql_allowed_for_system_error_state_title() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import node_allows_active_agv_error_sql

    node = {
        "node_type": "diagnostic_decision",
        "title": "Check AGV and system error state when service failure is not indicated",
        "intent": (
            "Use fleet and backend state evidence to identify an alternate AGV, system-error, "
            "or state-distribution condition when the service path is not indicated."
        ),
        "runbook_placeholder": (
            "Procedure needed to inspect RMS fleet or AGV status and, for remote support, "
            "corroborate active AGV errors via WCS/SSMS."
        ),
        "expects_capability": ["agv_active_errors", "fleet_system_status"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["operator", "L1_support", "L2_support"],
    }
    assert node_allows_active_agv_error_sql(node) is True
    runbooks_by_id = {
        "proc_rms_fleet_status_v1": {
            "procedure_id": "proc_rms_fleet_status_v1",
            "title": "Check Overall System RMS For System Faults",
            "procedure_type": "diagnostic",
            "capability_tags": ["fleet_system_status"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_query_active_agv_errors_from_the_wcs_database_v1": {
            "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
            "title": "Query Active AGV Errors From the WCS Database",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "wcs_service_health"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_check_systemdatabasemodel_state_and_sortguid_helix2x_1prod_robotics_v1": {
            "procedure_id": "proc_check_systemdatabasemodel_state_and_sortguid_helix2x_1prod_robotics_v1",
            "title": "Check SystemDatabaseModel state and SortGuid in Helix2x_1Prod_Robotics",
            "procedure_type": "diagnostic",
            "capability_tags": ["sort_lifecycle_state"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "training_video"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_fleet_status_v1",
            title=runbooks_by_id["proc_rms_fleet_status_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.55,
            jaccard_score=0.18,
            combined_score=0.55,
            source_type="manual",
        ),
    ]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    ids = [item[0].procedure_id for item in selected]
    assert "proc_query_active_agv_errors_from_the_wcs_database_v1" in ids
    assert "proc_check_systemdatabasemodel_state_and_sortguid_helix2x_1prod_robotics_v1" not in ids


def test_active_agv_sql_still_allowed_when_node_asks_for_errors() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm active AGV errors and roster state",
        "intent": "Determine whether AGVs show active errors and abnormal roster state.",
        "runbook_placeholder": (
            "Procedure needed to inspect RMS fleet status for active AGV errors/faults and abnormal "
            "roster/device state, including WCS/SSMS corroboration."
        ),
        "expects_capability": ["agv_active_errors", "device_roster_state"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["L1_support", "L2_support"],
    }
    runbooks_by_id = {
        "proc_rms_agv_errors_v1": {
            "procedure_id": "proc_rms_agv_errors_v1",
            "title": "Check Overall System RMS For Active AGV Faults",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors"],
            "access_surface": ["rms_ui"],
            "audience_roles": ["L1_support"],
            "role_required": "L1_support",
            "metadata": {"source_type": "manual"},
        },
        "proc_query_active_agv_errors_from_the_wcs_database_v1": {
            "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
            "title": "Query Active AGV Errors From the WCS Database",
            "procedure_type": "diagnostic",
            "capability_tags": ["agv_active_errors", "wcs_service_health"],
            "access_surface": ["wcs_sql"],
            "audience_roles": ["L2_support"],
            "role_required": "L2_support",
            "metadata": {"source_type": "manual"},
        },
    }
    matches = [
        RunbookSearchMatch(
            procedure_id="proc_rms_agv_errors_v1",
            title=runbooks_by_id["proc_rms_agv_errors_v1"]["title"],
            procedure_type="diagnostic",
            cosine_score=0.6,
            jaccard_score=0.2,
            combined_score=0.6,
            source_type="manual",
        ),
    ]
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id)
    ids = [item[0].procedure_id for item in selected]
    assert "proc_query_active_agv_errors_from_the_wcs_database_v1" in ids


def test_pairing_hospital_gaps_are_actionable_evidence_paths() -> None:
    from shared_pipeline_stages.stage_8.link_scoring import intent_mismatch_gaps, unresolved_catalog_gaps
    from shared_pipeline_stages.stage_8.normalize import attach_catalog_gaps

    node = {
        "node_type": "diagnostic_decision",
        "title": "Confirm pairing failure and hospital diversion",
        "intent": "Determine whether zone pairing failed with hospital diversion.",
        "runbook_placeholder": "Procedure needed to confirm zone pairing failure and hospital diversion pattern.",
        "expects_capability": ["zone_pairing_state", "hospital_diversion"],
        "expects_surface": ["rms_ui", "hospital_hmi", "wcs_sql"],
    }
    runbook = {
        "procedure_id": "proc_rms_only",
        "title": "Check Overall System RMS For System Faults",
        "capability_tags": ["fleet_system_status"],
        "access_surface": ["rms_ui"],
    }
    match = RunbookSearchMatch(
        procedure_id="proc_rms_only",
        title=runbook["title"],
        procedure_type="diagnostic",
        cosine_score=0.5,
        jaccard_score=0.15,
        combined_score=0.5,
    )
    gaps = intent_mismatch_gaps(node, match, runbook)
    assert any("zone_pairing_state" in gap and "ask site" in gap.lower() for gap in gaps)
    assert any("hospital_diversion" in gap and "hospital" in gap.lower() for gap in gaps)

    unresolved = attach_catalog_gaps({"node_id": "node_2", "node_type": "branching_condition", **node, "runbook_links": []})
    assert unresolved.get("catalog_gaps")
    assert any("Catalog gap" in gap for gap in unresolved["catalog_gaps"])
    assert unresolved_catalog_gaps({"node_type": "escalation_gate"})[0].startswith("No runbook link expected")


def test_sanitize_playbook_branch_graph_drops_empty_and_duplicate_rows() -> None:
    from shared_pipeline_stages.stage_8.normalize import sanitize_playbook_branch_graph
    from shared_pipeline_stages.stage_8.review_markdown import write_playbook_review_markdown

    playbook = {
        "playbook_id": "pb_test",
        "title": "Branch cleanup",
        "case_id": "228723",
        "extraction_mode": "one_or_more_playbook_candidates_when_separable",
        "nodes": [
            {
                "node_id": "node_2",
                "node_order": 2,
                "node_type": "branching_condition",
                "title": "Recent handling?",
                "branches": [
                    {
                        "outcome": "unhealthy",
                        "condition_label": "Recent AGV replacement",
                        "next_node_id": "node_3",
                    }
                ],
                "runbook_links": [],
            },
            {
                "node_id": "node_3",
                "node_order": 3,
                "node_type": "diagnostic_decision",
                "title": "Inspect RMS",
                "branches": [],
                "runbook_links": [],
            },
            {
                "node_id": "node_6",
                "node_order": 6,
                "node_type": "escalation_gate",
                "title": "Escalate",
                "branches": [],
                "runbook_links": [],
                "decision_outcomes": [{"outcome_label": "escalate", "descriptor": "Escalate"}],
            },
        ],
        "branches": [
            {
                "from_node_id": "node_2",
                "outcome": "unhealthy",
                "condition_label": "Recent AGV replacement",
                "next_node_id": "node_3",
            },
            {
                "from_node_id": "",
                "outcome": "unhealthy",
                "condition_label": "pattern_confirmed",
                "next_node_id": "node_2",
            },
            {
                "outcome": "unhealthy",
                "condition_label": "orphan_llm_branch",
                "next_node_id": "node_3",
            },
        ],
    }
    cleaned = sanitize_playbook_branch_graph(playbook)
    assert cleaned["branches"] == []
    md = write_playbook_review_markdown(cleaned, runbooks_by_id={})
    assert "pattern_confirmed" not in md
    assert md.count("`node_2`") >= 1
    assert "no branch outcomes — proceed / escalate" in md
    assert "| `` |" not in md


def test_linked_runbooks_group_into_operator_and_support_dropdowns() -> None:
    from shared_pipeline_stages.stage_8.linked_runbook_surface import (
        render_linked_runbooks_html,
        render_linked_runbooks_markdown,
        runbook_audience_bucket,
    )

    operator_rb = {
        "procedure_id": "proc_operator_hmi_v1",
        "title": "Check Tipper VISU Alarm",
        "procedure_type": "diagnostic",
        "role_required": "operator",
        "audience_roles": ["operator"],
        "summary": "Operator station check.",
        "when_to_use": "When tipper alarm is present.",
        "steps": [],
    }
    support_rb = {
        "procedure_id": "proc_l2_ssms_v1",
        "title": "Query AGV Errors in SSMS",
        "procedure_type": "diagnostic",
        "role_required": "L2_support",
        "audience_roles": ["L2_support"],
        "summary": "Remote SQL corroboration.",
        "when_to_use": "When L2 confirms active errors.",
        "steps": [],
    }
    assert runbook_audience_bucket(operator_rb) == "operator"
    assert runbook_audience_bucket(support_rb) == "support"
    node = {
        "node_id": "node_1",
        "runbook_links": [
            {"procedure_id": "proc_operator_hmi_v1", "link_rank": 1},
            {"procedure_id": "proc_l2_ssms_v1", "link_rank": 2},
        ],
        "resolved_runbook_ids": ["proc_operator_hmi_v1", "proc_l2_ssms_v1"],
        "linked_runbooks": [operator_rb, support_rb],
    }
    runbooks_by_id = {
        "proc_operator_hmi_v1": operator_rb,
        "proc_l2_ssms_v1": support_rb,
    }
    md = "\n".join(
        render_linked_runbooks_markdown(
            node,
            runbooks_by_id=runbooks_by_id,
            artifact_index=None,
            review_markdown_path=None,
            repo_root=Path("."),
            asset_link_cache={},
        )
    )
    html = "\n".join(
        render_linked_runbooks_html(
            node,
            runbooks_by_id=runbooks_by_id,
            artifact_index=None,
            review_html_path=None,
            repo_root=Path("."),
            asset_link_cache={},
        )
    )
    assert "Operator runbooks" in md
    assert "Support runbooks" in md
    assert "Alternate supporting runbooks" not in md
    assert "Operator runbooks" in html
    assert "Support runbooks" in html
    assert "linked-runbook-operator" in html
    assert "linked-runbook-support" in html


def test_stage8_procedure_references_do_not_embed_runbook_bodies() -> None:
    from shared_pipeline_stages.stage_8.linked_runbook_surface import attach_linked_runbooks

    node = {"resolved_runbook_ids": ["proc_1"]}
    runbook = {
        "procedure_id": "proc_1",
        "title": "Check AGV status",
        "procedure_type": "diagnostic",
        "summary": "Collect current AGV state.",
        "role_required": "L1_support",
        "audience_roles": ["L1_support"],
        "steps": [{"step_number": 1, "instruction": "Open the status screen."}],
        "healthy_conditions": ["No active faults."],
    }
    attach_linked_runbooks(node, runbooks_by_id={"proc_1": runbook})
    assert node["linked_runbooks"] == [
        {
            "procedure_id": "proc_1",
            "title": "Check AGV status",
            "procedure_type": "diagnostic",
            "purpose": "Collect current AGV state.",
            "role_required": "L1_support",
            "audience_roles": ["L1_support"],
        }
    ]
    assert node["evidence_collection_procedures"][0]["procedure_id"] == "proc_1"
    assert "steps" not in node["linked_runbooks"][0]


def test_stage8_node_structure_preserves_stage5_reasoning_and_indicators() -> None:
    from shared_pipeline_stages.stage_8.normalize import enrich_node_structure

    node = {
        "node_id": "node_1",
        "node_type": "diagnostic_decision",
        "title": "Check fleet state",
        "intent": "Determine whether fleet state is abnormal.",
        "source_supported_description": "The incident showed broad fleet disruption.",
        "source_refs": [{"page_ref": "case_1:page_2"}],
    }
    enriched = enrich_node_structure(
        node,
        decision_outcomes=[
            {"outcome_label": "healthy", "descriptor": "Fleet is operating normally."},
            {"outcome_label": "unhealthy", "descriptor": "Fleet shows abnormal state."},
            {"outcome_label": "inconclusive", "descriptor": "The status view is unavailable."},
        ],
        branches=[],
    )
    assert enriched["title"] == node["title"]
    assert enriched["diagnostic_reasoning"] == node["source_supported_description"]
    assert enriched["healthy_indicators"] == ["Fleet is operating normally."]
    assert enriched["unhealthy_indicators"] == ["Fleet shows abnormal state."]
    assert enriched["inconclusive_indicators"] == ["The status view is unavailable."]
    assert enriched["source_evidence"] == node["source_refs"]


def test_stage5_preservation_validator_detects_changed_workflow_fields() -> None:
    from shared_pipeline_stages.stage_8.normalize import stage5_node_preservation_warnings

    source = [{"node_id": "node_1", "title": "Original", "intent": "Determine state."}]
    finalized = [{"node_id": "node_1", "title": "Changed", "intent": "Determine state."}]
    warnings = stage5_node_preservation_warnings(source, finalized)
    assert warnings == ["node_1: Stage 5 field changed: title"]


def test_validation_warns_when_outcome_coverage_is_incomplete() -> None:
    playbook = {
        "nodes": [
            {
                "node_id": "node_1",
                "node_type": "diagnostic_decision",
                "decision_outcomes": [{"outcome_label": "healthy", "descriptor": "Normal"}],
                "branches": [],
            }
        ]
    }
    warnings = validate_finalized_playbook(playbook, runbooks_by_id={})
    assert any("missing healthy/unhealthy decision outcomes" in warning for warning in warnings)


def test_validation_requires_gaps_for_low_confidence_links() -> None:
    playbook = {
        "nodes": [
            {
                "node_id": "node_1",
                "node_type": "procedure_reference",
                "runbook_links": [
                    {"procedure_id": "proc_1", "link_confidence": "low", "match_gaps": []}
                ],
            }
        ]
    }
    warnings = validate_finalized_playbook(
        playbook,
        runbooks_by_id={"proc_1": {"procedure_type": "reference"}},
    )
    assert any("must include match_gaps" in warning for warning in warnings)


def test_diagnostic_action_plan_separates_evidence_retrieval_from_health() -> None:
    from shared_pipeline_stages.stage_8.action_synthesis import synthesize_diagnostic_action_plan

    node = {
        "node_type": "diagnostic_decision",
        "title": "Inspect stalled bag-out task and tote state",
        "intent": "Determine whether the bag-out task is stale or inconsistent.",
        "preferred_audience": ["L2_support"],
        "expects_surface": ["wcs_sql", "aveva_hmi"],
        "decision_outcomes": [
            {"outcome_label": "healthy", "descriptor": "Task is current and identifiers agree."},
            {"outcome_label": "unhealthy", "descriptor": "Task is stale or identifiers conflict."},
            {"outcome_label": "inconclusive", "descriptor": "Required mappings are unavailable."},
        ],
    }
    plan = synthesize_diagnostic_action_plan(
        node,
        ontology_evidence=[
            {
                "id": "model:BagOutTaskModel",
                "text": "Model BagOutTaskModel (db): task state. Key fields: ToteId: tote; AgvId: AGV; TaskState: state; LastUpdate: timestamp.",
            }
        ],
        links=[
            {
                "procedure_id": "proc_sql",
                "link_confidence": "high",
            }
        ],
        runbooks_by_id={
            "proc_sql": {
                "procedure_id": "proc_sql",
                "title": "Inspect bag-out task state",
                "summary": "Read-only task inspection.",
                "procedure_type": "diagnostic",
                "access_surface": ["wcs_sql"],
            }
        },
    )
    assert plan["primary_surface"] == "wcs_sql"
    assert any("ToteId" in item for item in plan["evidence_to_collect"])
    assert "retrieval" in plan["evidence_retrieval_success"].lower()
    assert "unhealthy" in plan["diagnostic_interpretation"].lower()
    assert plan["query_mode"] == "ontology_generated_read_only"


def test_capability_mismatch_penalizes_candidate() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "expects_capability": ["device_roster_state"],
        "expects_surface": ["wcs_sql"],
    }
    match = RunbookSearchMatch(
        procedure_id="proc_active_errors",
        title="Query active errors",
        procedure_type="diagnostic",
        cosine_score=0.9,
        jaccard_score=0.9,
        combined_score=0.9,
    )
    runbook = {
        "capability_tags": ["agv_active_errors"],
        "access_surface": ["wcs_sql"],
    }
    penalty, reasons = evidence_domain_penalty(node, match, runbook)
    assert penalty < 0.0
    assert any("expected-capability" in reason for reason in reasons)


def test_diagnostic_procedure_limits_keep_primary_and_distinct_corroboration() -> None:
    from shared_pipeline_stages.stage_8.normalize import enforce_procedure_limits

    node = {
        "node_type": "diagnostic_decision",
        "expects_capability": ["device_roster_state"],
        "expects_surface": ["wcs_sql", "rms_ui"],
    }
    links = [
        {"procedure_id": "proc_sql", "link_confidence": "high"},
        {"procedure_id": "proc_rms", "link_confidence": "medium"},
        {"procedure_id": "proc_sql_duplicate", "link_confidence": "medium"},
    ]
    runbooks = {
        "proc_sql": {
            "procedure_type": "diagnostic",
            "capability_tags": ["device_roster_state"],
            "access_surface": ["wcs_sql"],
        },
        "proc_rms": {
            "procedure_type": "diagnostic",
            "capability_tags": ["device_roster_state"],
            "access_surface": ["rms_ui"],
        },
        "proc_sql_duplicate": {
            "procedure_type": "diagnostic",
            "capability_tags": ["device_roster_state"],
            "access_surface": ["wcs_sql"],
        },
    }
    selected = enforce_procedure_limits(node, links, runbooks_by_id=runbooks)
    assert [item["procedure_id"] for item in selected] == ["proc_sql", "proc_rms"]
    assert selected[0]["link_role"] == "primary"
    assert selected[1]["link_role"] == "optional_corroboration"


def test_remote_diagnostic_does_not_promote_rms_over_sql_by_source_mention() -> None:
    from shared_pipeline_stages.stage_8.action_synthesis import synthesize_diagnostic_action_plan

    plan = synthesize_diagnostic_action_plan(
        {
            "node_type": "diagnostic_decision",
            "title": "Check AGV fleet status in RMS",
            "preferred_audience": ["L2_support"],
            "expects_surface": ["rms_ui"],
            "evidence_required": ["AGV identifier", "current lifecycle state"],
        }
    )
    assert plan["primary_surface"] == "wcs_sql"


def test_remote_rms_only_expectation_rejects_rms_procedure_without_authority() -> None:
    from shared_pipeline_stages.stage_8.normalize import enforce_procedure_limits

    selected = enforce_procedure_limits(
        {
            "node_type": "diagnostic_decision",
            "preferred_audience": ["L2_support"],
            "expects_surface": ["rms_ui"],
        },
        [{"procedure_id": "rms_check"}],
        runbooks_by_id={
            "rms_check": {
                "procedure_type": "diagnostic",
                "access_surface": ["rms_ui"],
            }
        },
    )
    assert selected == []


def test_llm_action_plan_fields_are_preserved_without_deterministic_repair() -> None:
    llm_plan = {
        "primary_action": "Inspect the exact WCS task fields for the affected tote.",
        "performed_by": "L2 Support",
        "primary_surface": "wcs_sql",
        "evidence_to_collect": ["TaskId", "TaskState"],
        "healthy_interpretation": "Task is current.",
        "unhealthy_interpretation": "Task is stale.",
        "inconclusive_interpretation": "Records are unavailable.",
        "optional_corroboration": [],
        "linked_primary_procedure": None,
        "generated_guidance": "Use the validated read-only task mapping.",
        "ontology_evidence": [],
        "confidence": "medium",
        "requires_sme_review": True,
        "query_mode": "conceptual_inspection_only",
        "evidence_retrieval_success": "Evidence was obtained.",
        "diagnostic_interpretation": "Interpret values separately from retrieval success.",
    }
    node = _merge_llm_node(
        {"node_id": "node_1", "node_type": "diagnostic_decision"},
        llm_plan,
        runbooks_by_id={},
        retrieval_matches=[],
    )
    assert node["primary_action"] == llm_plan["primary_action"]
    assert node["evidence_to_collect"] == ["TaskId", "TaskState"]
    assert node["query_mode"] == "conceptual_inspection_only"


def test_missing_and_malformed_llm_action_plan_fields_are_warnings() -> None:
    warnings = validate_finalized_playbook(
        {
            "playbook_id": "pb_1",
            "case_id": "case_1",
            "nodes": [
                {
                    "node_id": "node_1",
                    "node_type": "diagnostic_decision",
                    "primary_action": 123,
                    "requires_sme_review": "yes",
                }
            ],
        },
        runbooks_by_id={},
    )
    assert any("diagnostic action plan missing" in warning for warning in warnings)
    assert any("diagnostic action plan malformed" in warning for warning in warnings)


def test_ontology_contract_rejects_service_health_link_to_agv_state_procedure() -> None:
    node = {
        "node_type": "procedure_reference",
        "title": "Recover OptiSweep service after health diagnosis",
        "intent": "Restart the OptiSweep service only after health is abnormal.",
        "ontology_capabilities": [
            {
                "id": "wcs_service_health",
                "support_contract": {
                    "forbidden_capabilities": ["tote_lifecycle_state", "agv_physical_recovery"],
                    "control_surfaces": ["windows_services", "ignition_gateway"],
                },
            }
        ],
        "prerequisites": ["Service health is confirmed abnormal."],
    }
    runbook = {
        "procedure_id": "proc_wrong_state_mutation",
        "procedure_type": "recovery",
        "capability_tags": ["tote_lifecycle_state"],
        "access_surface": ["wcs_api"],
        "steps": [{"instruction": "Mutate AGV and tote state."}],
    }
    gaps = runbook_exact_fit_gaps(node, runbook)
    assert any("forbidden" in gap.lower() for gap in gaps)


def test_service_restart_requires_health_prerequisite() -> None:
    node = {
        "node_type": "procedure_reference",
        "title": "Restart OptiSweep service",
        "intent": "Restart the service.",
        "prerequisites": [],
    }
    runbook = {
        "procedure_id": "proc_restart_optisweep_service",
        "title": "Restart OptiSweep Windows service",
        "procedure_type": "recovery",
        "access_surface": ["windows_services"],
        "steps": [{"instruction": "Restart the OptiSweep Windows service."}],
    }
    gaps = runbook_exact_fit_gaps(node, runbook)
    assert any("safety precondition" in gap.lower() for gap in gaps)


def test_review_rendering_omits_redundant_decision_question() -> None:
    lines = _render_node_markdown(
        {
            "node_order": 1,
            "title": "Confirm service health",
            "node_type": "diagnostic_decision",
            "purpose": "Confirm whether the OptiSweep service is healthy.",
            "intent": "Confirm whether the OptiSweep service is healthy.",
        "question": "Confirm whether the OptiSweep service is healthy.",
        },
        runbooks_by_id={},
    )
    rendered = "\n".join(lines)
    assert "**Objective:** Confirm whether the OptiSweep service is healthy." in rendered
    assert "**Decision Question:**" not in rendered
    assert "**Intent:**" not in rendered


def test_graph_cycle_is_repaired_to_terminal_escalation() -> None:
    playbook = {
        "nodes": [
            {
                "node_id": "node_1",
                "node_order": 1,
                "node_type": "diagnostic_decision",
                "decision_outcomes": [
                    {
                        "outcome_label": "unhealthy",
                        "next_node_id": "node_2",
                    }
                ],
            },
            {
                "node_id": "node_2",
                "node_order": 2,
                "node_type": "procedure_reference",
                "decision_outcomes": [
                    {
                        "outcome_label": "complete",
                        "next_node_id": "node_1",
                    }
                ],
            },
        ]
    }
    repaired = repair_playbook_graph_cycles(playbook)
    assert repaired == ["node_2->node_1"]
    assert playbook["nodes"][1]["decision_outcomes"][0]["next_node_id"] is None
    assert playbook["nodes"][1]["decision_outcomes"][0]["terminal_result"]


def test_ontology_capability_prefix_matches_pool_tags() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "ontology_capabilities": [
            {
                "id": "capability:wcs_service_health",
                "support_contract": {"diagnostic_surfaces": ["wcs_sql", "event_viewer"]},
            }
        ],
    }
    runbook = {
        "procedure_type": "diagnostic",
        "capability_tags": ["wcs_service_health"],
        "access_surface": ["wcs_sql"],
    }
    assert node_expects_capabilities(node) == {"wcs_service_health"}
    assert not any(
        "ontology capability contract" in gap
        for gap in runbook_exact_fit_gaps(node, runbook)
    )
    assert surface_hint_adjustment(node, runbook) >= 0.18


def test_system_surface_keeps_read_only_wcs_field_suggestions() -> None:
    mapping = _technical_field_mapping(
        {
            "node_type": "diagnostic_decision",
            "backend_observability": [
                {
                    "support_read_sources": [
                        {
                            "surface": "wcs_sql",
                            "database": "robotics",
                            "model": "RobotDatabaseModel",
                            "fields": ["ToteName", "CurrentLocationId"],
                        }
                    ]
                }
            ],
        },
        [],
        "rms_ui",
    )
    assert mapping["entities"] == []
    assert mapping["suggested_database_checks"][0]["entity"] == "RobotDatabaseModel"
    assert "ToteName" in mapping["suggested_database_checks"][0]["fields"][0]["name"]


def test_stage8_resolves_hmi_evidence_without_runbook() -> None:
    plan = synthesize_diagnostic_action_plan(
        {
            "node_type": "diagnostic_decision",
            "title": "Check fleet roster and mapping state",
            "intent": "Determine whether an incorrect robot membership, location, zone assignment, or mapping state prevents pairing.",
            "diagnostic_reasoning": "The incident followed robot replacement activity and the removed robot was not mapped.",
            "preferred_audience": ["L2_support"],
            "expects_surface": ["rms_ui"],
            "healthy_interpretation": "The robot is present once and its location and zone are current.",
            "unhealthy_interpretation": "The robot is missing, duplicated, stale, or assigned to the wrong zone.",
        }
    )
    checks = plan["technical_field_mapping"]["suggested_database_checks"]
    assert checks
    assert any(check["entity"] == "RobotDatabaseModel" for check in checks)
    assert any(
        "location" in str(field.get("meaning") or "").lower()
        for check in checks
        for field in check["fields"]
    )
    assert plan["internal_resolution_status"] == "missing_validated_procedure"


def test_service_health_node_keeps_day2_service_runbook_as_companion() -> None:
    service_diag = RunbookSearchMatch(
        procedure_id="proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1",
        title="Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures",
        procedure_type="diagnostic",
        cosine_score=0.0,
        jaccard_score=0.27,
        combined_score=0.27,
    )
    day2_service = RunbookSearchMatch(
        procedure_id="proc_verify_optsweep_wcs_windows_service_health_v1",
        title="Verify OptiSweep / WCS Windows service health",
        procedure_type="diagnostic",
        cosine_score=0.0,
        jaccard_score=0.17,
        combined_score=0.17,
    )
    node = {
        "node_type": "diagnostic_decision",
        "title": "Determine whether a named service or application failure correlates with the stoppage",
        "intent": "Check Event Viewer, Windows Services, and OptiSweep service health.",
        "primary_surface": "event_viewer / windows_services",
        "expects_capability": ["wcs_service_health", "windows_service_or_event_log"],
    }
    selected = select_runbook_matches(
        node,
        [service_diag, day2_service],
        runbooks_by_id={
            service_diag.procedure_id: {
                "procedure_type": "diagnostic",
                "access_surface": ["event_viewer"],
                "capability_tags": ["wcs_service_health", "windows_service_or_event_log"],
            },
            day2_service.procedure_id: {
                "procedure_type": "diagnostic",
                "access_surface": ["event_viewer"],
                "capability_tags": ["wcs_service_health"],
            },
        },
    )
    assert [item[0].procedure_id for item in selected] == [
        service_diag.procedure_id,
        day2_service.procedure_id,
    ]


def test_service_recovery_node_prefers_ignition_optisweep_restart_runbook() -> None:
    restart = RunbookSearchMatch(
        procedure_id="proc_ignition_gateway_restart_and_optisweep_response_validation_v1",
        title="Ignition gateway restart and OptiSweep / WCS API response validation",
        procedure_type="recovery",
        cosine_score=0.0,
        jaccard_score=0.04,
        combined_score=0.04,
    )
    diagnostic = RunbookSearchMatch(
        procedure_id="proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1",
        title="Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures",
        procedure_type="diagnostic",
        cosine_score=0.0,
        jaccard_score=0.13,
        combined_score=0.13,
    )
    node = {
        "node_type": "procedure_reference",
        "title": "Perform authorized recovery of the affected gateway or OptiSweep service",
        "intent": "Use the approved recovery procedure for the service or gateway identified by diagnostic evidence.",
        "runbook_placeholder": "Restart Ignition or reset OptiSweep and verify GetAgvStatuses response.",
        "primary_surface": "ignition_gateway / windows_services",
    }
    selected = select_runbook_matches(
        node,
        [diagnostic, restart],
        runbooks_by_id={
            restart.procedure_id: {
                "title": restart.title,
                "procedure_type": "recovery",
                "access_surface": ["ignition_gateway", "event_viewer", "wcs_api", "physical_floor"],
                "capability_tags": ["gateway_health", "wcs_api_responsiveness", "e_stop_or_safety_stop"],
                "safety_notes": ["Do not release the E-stop until API response is confirmed."],
            },
            diagnostic.procedure_id: {
                "title": diagnostic.title,
                "procedure_type": "diagnostic",
                "access_surface": ["event_viewer"],
                "capability_tags": ["wcs_service_health", "windows_service_or_event_log"],
            },
        },
    )
    assert selected[0][0].procedure_id == restart.procedure_id


def test_service_api_health_node_does_not_emit_adjacent_agv_database_checks() -> None:
    mapping = _technical_field_mapping(
        {
            "node_type": "diagnostic_decision",
            "title": "Validate API responsiveness after service recovery",
            "intent": "Determine whether GetAgvStatuses is responding and the OptiSweep service is healthy.",
            "backend_observability": [
                {
                    "support_read_sources": [
                        {
                            "surface": "wcs_sql",
                            "database": "robotics",
                            "model": "RobotLocationDatabaseModel",
                            "fields": ["StationNumber", "Occupied"],
                        }
                    ]
                }
            ],
        },
        [],
        "wcs_api",
    )
    assert mapping["suggested_database_checks"] == []


def test_roster_mapping_database_guidance_includes_identity_location_zone_tote_and_errors() -> None:
    mapping = _technical_field_mapping(
        {
            "node_type": "diagnostic_decision",
            "title": "Check fleet roster and mapping state",
            "intent": "Determine robot membership, mapped or unmapped state, location, destination, zone, tote association, freshness, and active errors.",
        },
        [],
        "wcs_sql",
    )
    checks = {check["entity"]: check for check in mapping["suggested_database_checks"]}
    assert "RobotDatabaseModel" in checks
    assert "RobotLocationDatabaseModel" in checks
    assert "AgvActiveErrorDatabaseModel" in checks or "SystemActiveErrorModel" in checks
    robot_fields = {field["name"] for field in checks["RobotDatabaseModel"]["fields"]}
    location_fields = {field["name"] for field in checks["RobotLocationDatabaseModel"]["fields"]}
    assert {"State", "CurrentLocationId", "DestinationLocationId", "AssignedSorterSide", "ToteName"} & robot_fields
    assert {"StationNumber", "Zone", "Occupied", "LocationStatus"} & location_fields


def test_hospital_hmi_database_guidance_uses_hospital_robot_tote_task_models() -> None:
    mapping = _technical_field_mapping(
        {
            "node_type": "diagnostic_decision",
            "title": "Map Hospital HMI and AVEVA tote induction state to backend records",
            "intent": "Determine hospital induction availability, pickup, drop-off, robot location, tote association, active task, and lane state.",
        },
        [],
        "wcs_sql",
    )
    entities = {check["entity"] for check in mapping["suggested_database_checks"]}
    assert "HospitalDatabaseModel" in entities
    assert "HospitalTagsModel" in entities
    assert "RobotDatabaseModel" in entities
    assert len(entities) <= 3


def test_active_error_sql_is_retained_as_composite_diagnostic_evidence() -> None:
    pool_dir = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool"
    stage7_dir = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks"
    runbooks = _load_runbooks_for_linking(stage7_dir, pool_dir)
    runbooks_by_id = {str(item.get("procedure_id")): item for item in runbooks}
    target_id = "proc_query_active_agv_errors_from_the_wcs_database_v1"
    assert target_id in runbooks_by_id
    assert runbooks_by_id[target_id]["source_id"] == "active_agv_error_query_1"
    assert runbooks_by_id[target_id]["source_type"] == "manual"
    assert runbooks_by_id[target_id]["access_surface"] == ["wcs_sql"]
    assert runbooks_by_id[target_id]["capability_tags"] == ["agv_active_errors", "wcs_service_health"]

    candidate = _load_playbook_candidates(
        REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents",
        "228086",
        "playbook_prompt_a_one_per_incident",
    )[0]
    node = next(item for item in candidate["nodes"] if item.get("node_id") == "node_5")
    cards = read_json(pool_dir / "retrieval_cards.json")
    index = read_json(pool_dir / "runbook_retrieval_index.json")
    assert target_id in {item.get("finalized_runbook_id") for item in cards}
    assert target_id in {item.get("finalized_runbook_id") for item in index}
    assert "proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1" in {
        item.get("finalized_runbook_id") for item in cards
    }
    catalog = RunbookCatalogSearch.from_pool_artifacts(cards, index, runbooks)
    query = build_retrieval_query_text(node, affected_systems=candidate.get("affected_systems_or_components"))
    matches = catalog.search_for_node(
        node,
        query_vector=MockRunbookEmbedder().embed_texts([query])[0],
        top_k=150,
        case_id="228086",
        affected_systems=candidate.get("affected_systems_or_components"),
    )
    selected = select_runbook_matches(node, matches, runbooks_by_id=runbooks_by_id, max_runbooks=2)
    selected_ids = [item[0].procedure_id for item in selected]
    assert target_id in selected_ids
    assert len(selected_ids) <= 2


def test_runbook_step_conditions_do_not_become_node_outcomes() -> None:
    node = {
        "node_id": "node_1",
        "node_type": "diagnostic_decision",
        "title": "Check active errors",
        "intent": "Determine whether an active error remains.",
        "healthy_indicators": ["No active error remains."],
        "unhealthy_indicators": ["An active error remains."],
        "inconclusive_indicators": ["The error view is unavailable."],
    }
    outcomes = build_decision_outcomes(
        node,
        {
            "proc_diag": {
                "procedure_type": "diagnostic",
                "steps": [{"expected_result": "The detail panel expands successfully."}],
                "healthy_conditions": [{"healthy_condition": "The alarm list is empty."}],
                "failure_conditions": ["The procedure cannot be completed."],
            }
        },
        linked_runbook_ids=["proc_diag"],
        branch_hints=[],
    )
    assert len(outcomes) == 3
    assert all(not item.get("linked_runbook_id") for item in outcomes)


def test_diagnostic_render_has_single_status_surface_and_database_limits() -> None:
    node = {
        "node_order": 1,
        "node_type": "diagnostic_decision",
        "title": "Check robot state",
        "purpose": "Determine whether the robot is healthy.",
        "primary_action": "Inspect the affected robot state and compare it with the observed state.",
        "healthy_interpretation": "Robot state and location agree with the expected physical state.",
        "unhealthy_interpretation": "The robot is missing, stale, or in an unexpected state.",
        "inconclusive_interpretation": "The robot ID or backend state is unavailable.",
        "healthy_indicators": ["A step-level success must not render here."],
        "unhealthy_indicators": ["A step-level failure must not render here."],
        "inconclusive_indicators": ["A step-level ambiguity must not render here."],
        "decision_outcomes": [
            {"outcome_label": "healthy", "descriptor": "Robot state and location agree."},
            {"outcome_label": "unhealthy", "descriptor": "The robot is missing."},
            {"outcome_label": "inconclusive", "descriptor": "The backend state is unavailable."},
        ],
        "technical_field_mapping": {
            "suggested_database_checks": [
                {"database": "robotics", "entity": "RobotDatabaseModel", "fields": [{"name": "State", "meaning": "State"}]},
            ]
        },
    }
    rendered = "\n".join(_render_node_markdown(node, runbooks_by_id={}))
    assert rendered.count("**Healthy:**") == 1
    assert rendered.count("**Unhealthy:**") == 1
    assert rendered.count("**Inconclusive:**") == 1
    assert "Healthy Indicators" not in rendered
    assert "Decision Outcomes" not in rendered
    assert "A step-level success" not in rendered


def test_distribute_visual_references_assigns_images_to_matching_steps() -> None:
    from shared_pipeline_stages.stage_8.linked_runbook_surface import _distribute_visual_references_to_steps

    runbook = {
        "visual_references": [
            {
                "artifact_id": "artifact_gwcmd",
                "description": "Windows Administrator Command Prompt showing the Ignition directory, gwcmd -r, and Waiting for Gateway restart.",
            },
            {
                "artifact_id": "artifact_systems_overview",
                "description": "Ignition gateway Status Systems Overview showing Current Response Time and Recent Slow Response Events.",
            },
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Restart the Ignition gateway",
                "instruction": "Open a Windows Administrator Command Prompt and run gwcmd -r in the Ignition directory.",
                "screens_or_images": [],
            },
            {
                "step_number": 2,
                "title": "Verify the Ignition gateway Systems Overview",
                "instruction": "Open Status Systems Overview and check Current Response Time and Recent Slow Response Events.",
                "screens_or_images": [],
            },
        ],
    }
    steps = _distribute_visual_references_to_steps(runbook)
    assert [ref["artifact_id"] for ref in steps[0]["screens_or_images"]] == ["artifact_gwcmd"]
    assert [ref["artifact_id"] for ref in steps[1]["screens_or_images"]] == ["artifact_systems_overview"]


def test_distribute_visual_references_leaves_existing_step_images_untouched() -> None:
    from shared_pipeline_stages.stage_8.linked_runbook_surface import _distribute_visual_references_to_steps

    runbook = {
        "visual_references": [{"artifact_id": "artifact_a", "description": "gwcmd Ignition directory"}],
        "steps": [
            {"step_number": 1, "title": "Restart", "instruction": "run gwcmd", "screens_or_images": [{"artifact_id": "artifact_existing"}]},
            {"step_number": 2, "title": "Verify", "instruction": "check overview", "screens_or_images": []},
        ],
    }
    steps = _distribute_visual_references_to_steps(runbook)
    assert steps[0]["screens_or_images"] == [{"artifact_id": "artifact_existing"}]


# ---------------------------------------------------------------------------
# Explicit retrieval mode: missing Azure OpenAI embedding credentials must
# fail loudly by default rather than silently degrading to lexical-only
# scoring. Callers must opt in explicitly (allow_lexical_fallback=True /
# --lexical-only) to accept that degradation.
# ---------------------------------------------------------------------------


def test_resolve_embedder_fails_loud_without_credentials_by_default(monkeypatch) -> None:
    from shared_pipeline_stages.stage_8 import playbook_builder
    from shared_pipeline_stages.stage_8.playbook_builder import (
        EmbeddingCredentialsUnavailableError,
        Stage8BuildConfig,
        _resolve_embedder,
    )

    def _raise_missing_credentials() -> None:
        raise RuntimeError("Azure OpenAI embedding credentials are not configured.")

    monkeypatch.setattr(playbook_builder, "_default_embedder", _raise_missing_credentials)
    config = Stage8BuildConfig(use_mock_embedder=False, allow_lexical_fallback=False)
    try:
        _resolve_embedder(config)
        assert False, "expected EmbeddingCredentialsUnavailableError"
    except EmbeddingCredentialsUnavailableError:
        pass


def test_resolve_embedder_allows_lexical_fallback_when_explicitly_enabled(monkeypatch) -> None:
    from shared_pipeline_stages.stage_8 import playbook_builder
    from shared_pipeline_stages.stage_8.playbook_builder import (
        Stage8BuildConfig,
        _resolve_embedder,
        retrieval_mode_for_embedder,
    )

    def _raise_missing_credentials() -> None:
        raise RuntimeError("Azure OpenAI embedding credentials are not configured.")

    monkeypatch.setattr(playbook_builder, "_default_embedder", _raise_missing_credentials)
    config = Stage8BuildConfig(use_mock_embedder=False, allow_lexical_fallback=True)
    embedder = _resolve_embedder(config)
    assert retrieval_mode_for_embedder(embedder) == "lexical"


def test_resolve_embedder_reports_semantic_mode_when_credentials_available(monkeypatch) -> None:
    from shared_pipeline_stages.stage_6_5.embedder import MockRunbookEmbedder
    from shared_pipeline_stages.stage_8 import playbook_builder
    from shared_pipeline_stages.stage_8.playbook_builder import (
        Stage8BuildConfig,
        _resolve_embedder,
        retrieval_mode_for_embedder,
    )

    monkeypatch.setattr(playbook_builder, "_default_embedder", lambda: MockRunbookEmbedder(dimensions=8))
    config = Stage8BuildConfig(use_mock_embedder=False, allow_lexical_fallback=False)
    embedder = _resolve_embedder(config)
    assert retrieval_mode_for_embedder(embedder) == "semantic"
