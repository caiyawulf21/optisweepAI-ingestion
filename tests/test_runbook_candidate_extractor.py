import json

from optisweep_ingestion.schemas.source_lineage import SourceLineage
from optisweep_ingestion.tools.runbook_candidate_extractor import (
    build_backfill_candidate,
    build_extraction_report,
    build_missing_priority_candidates,
    build_priority_candidate_check,
    dedupe_candidates,
    find_missing_candidate_sections,
    identify_procedural_sections,
    parse_candidate_response,
    validate_candidate_record,
)


def test_parse_candidate_response_from_json_fence() -> None:
    raw = "```json\n" + json.dumps({"candidates": [_valid_candidate()]}) + "\n```"

    candidates = parse_candidate_response(raw)

    assert len(candidates) == 1
    assert candidates[0]["candidate_id"] == "candidate_manual_check_tipper_heartbeat_stats"


def test_validate_allowed_procedure_type() -> None:
    record = {**_valid_candidate(), "likely_procedure_type": "maintenance"}

    errors = validate_candidate_record(record, {"artifact_manual_fig_4_22"}, {"ctx_manual_heartbeat_stats_v1"})

    assert any("likely_procedure_type" in error for error in errors)


def test_validate_allowed_role_value() -> None:
    record = {**_valid_candidate(), "likely_role_required": "maintenance"}

    errors = validate_candidate_record(record, {"artifact_manual_fig_4_22"}, {"ctx_manual_heartbeat_stats_v1"})

    assert any("likely_role_required" in error for error in errors)


def test_forbidden_fields_are_rejected() -> None:
    record = {**_valid_candidate(), "trigger_conditions": ["alarm"]}

    errors = validate_candidate_record(record, {"artifact_manual_fig_4_22"}, {"ctx_manual_heartbeat_stats_v1"})

    assert any("trigger_conditions" in error for error in errors)


def test_source_refs_are_required() -> None:
    record = {**_valid_candidate(), "source_refs": []}

    errors = validate_candidate_record(record, {"artifact_manual_fig_4_22"}, {"ctx_manual_heartbeat_stats_v1"})

    assert any("source_refs" in error for error in errors)


def test_related_artifact_ids_must_exist() -> None:
    record = {**_valid_candidate(), "related_artifact_ids": ["missing"]}

    errors = validate_candidate_record(record, {"artifact_manual_fig_4_22"}, {"ctx_manual_heartbeat_stats_v1"})

    assert any("related_artifact_id not found" in error for error in errors)


def test_related_context_ids_must_exist() -> None:
    record = {**_valid_candidate(), "related_context_ids": ["missing"]}

    errors = validate_candidate_record(record, {"artifact_manual_fig_4_22"}, {"ctx_manual_heartbeat_stats_v1"})

    assert any("related_context_id not found" in error for error in errors)


def test_dedupe_removes_exact_duplicate_candidate_ids_only() -> None:
    first = _valid_candidate()
    second = {
        **_valid_candidate(),
        "title": "Different title",
        "candidate_goal": "Different goal",
    }

    deduped, count = dedupe_candidates([first, second])

    assert count == 1
    assert len(deduped) == 1


def test_dedupe_keeps_distinct_candidates_with_different_ids() -> None:
    first = _valid_candidate()
    second = {
        **_valid_candidate(),
        "candidate_id": "candidate_manual_other_procedure",
        "title": "Different title",
        "candidate_goal": "Different goal",
    }

    deduped, count = dedupe_candidates([first, second])

    assert count == 0
    assert len(deduped) == 2


def test_priority_candidate_report_logic() -> None:
    checks = build_priority_candidate_check([_valid_candidate()])

    heartbeat = checks["check_tipper_heartbeat_stats"]
    assert heartbeat["found"] is True
    assert heartbeat["has_artifact_ref"] is True
    assert heartbeat["has_context_ref"] is True
    assert heartbeat["mentions_last_max_min"] is True
    assert heartbeat["mentions_10_seconds"] is True


def test_identify_procedural_sections_detects_starting_and_stopping() -> None:
    bundle = _fake_bundle()

    sections = identify_procedural_sections(bundle)

    titles = {section["title"] for section in sections}
    assert "5.1: Starting the System" in titles
    assert "5.2: Stopping the System" in titles
    assert "3.1: System Overview" not in titles


def test_missing_candidate_sections_reports_uncovered_procedural_section() -> None:
    sections = identify_procedural_sections(_fake_bundle())
    candidates = [
        {
            **_valid_candidate(),
            "title": "Starting the System",
            "candidate_goal": "Start OptiSweep.",
            "source_refs": [{"section_id": "sec_starting_system"}],
        }
    ]

    missing = find_missing_candidate_sections(sections, candidates)

    assert any(section["section_id"] == "sec_stopping_system" for section in missing)
    assert not any(section["section_id"] == "sec_starting_system" for section in missing)


def test_section_coverage_does_not_match_summary_only() -> None:
    sections = identify_procedural_sections(_fake_bundle())
    candidates = [
        {
            **_valid_candidate(),
            "title": "Perform Operator Station Lockout/Tagout",
            "candidate_goal": "Place the operator station into a stopped and powered off state.",
            "summary": "This mentions stopping the system, but it is not the Stopping the System section.",
            "source_refs": [{"section_id": "sec_loto"}],
        }
    ]

    missing = find_missing_candidate_sections(sections, candidates)

    assert any(section["section_id"] == "sec_stopping_system" for section in missing)


def test_backfill_candidate_is_conservative_and_validator_compatible() -> None:
    bundle = _fake_bundle()
    section = identify_procedural_sections(bundle)[0]

    candidate = build_backfill_candidate(_fake_bundle(), section, _lineage())
    errors = validate_candidate_record(candidate, set(), set())

    assert errors == []
    assert candidate["candidate_id"] == "candidate_manual_backfill_starting_the_system"
    assert candidate["confidence"] == "low"
    assert candidate["metadata"]["created_by"] == "stage_5_candidate_coverage_backfill"


def test_report_includes_missing_candidate_sections_and_priority_candidates() -> None:
    missing_sections = [{"section_id": "sec_stopping_system", "title": "5.2: Stopping the System", "page_start": 82}]

    report = build_extraction_report(
        source_bundle_path="source_bundle.json",
        source_artifacts_path="source_artifacts.json",
        operational_context_path="operational_context.json",
        candidates=[_valid_candidate()],
        lineage=_lineage(),
        llm_used=True,
        failed_packets=[],
        warnings=[],
        missing_candidate_sections=missing_sections,
    )

    assert report["missing_candidate_sections"] == missing_sections
    assert "Stop OptiSweep System" in report["missing_priority_candidates"]


def test_missing_priority_candidates_lists_required_gaps() -> None:
    missing = build_missing_priority_candidates([_valid_candidate()])

    assert "Check Tipper Heartbeat Stats" not in missing
    assert "Start OptiSweep System" in missing


def _valid_candidate() -> dict:
    return {
        "candidate_id": "candidate_manual_check_tipper_heartbeat_stats",
        "title": "Check Tipper Heartbeat Stats",
        "candidate_goal": "Check heartbeat timing values on the Operator Station HMI Data screen.",
        "likely_procedure_type": "diagnostic",
        "likely_role_required": "operator",
        "support_safe": True,
        "summary": "Review Last, Max, and Min heartbeat timing values and note whether values exceed 10 seconds.",
        "rough_steps": [
            "Open the Operator Station HMI Data screen.",
            "Locate the Heartbeat section.",
            "Review Last, Max, and Min values.",
        ],
        "expected_result": "Heartbeat timing values are visible.",
        "failure_or_escalation_notes": ["Escalate if heartbeat values exceed 10 seconds."],
        "access_or_tools_needed": ["Operator Station HMI access"],
        "related_context_ids": ["ctx_manual_heartbeat_stats_v1"],
        "related_artifact_ids": ["artifact_manual_fig_4_22"],
        "source_refs": [{"page": 52, "section_id": "sec_heartbeat"}],
        "evidence_source_refs": [{"page": 52, "section_id": "sec_heartbeat"}],
        "source_id": "manual_optisweep_om_v3",
        "source_type": "manual",
        "source_title": "OptiSweep Operation and Maintenance Manual",
        "source_version": "3",
        "ingestion_batch_id": "batch_test",
        "confidence": "high",
        "candidate_status": "needs_review",
        "extraction_notes": [],
        "metadata": {"created_by": "runbook_candidate_discovery_agent", "source_quality": "manual"},
    }


def _lineage() -> SourceLineage:
    return SourceLineage(
        source_id="manual_optisweep_om_v3",
        source_type="manual",
        source_title="OptiSweep Operation and Maintenance Manual",
        source_version="3",
        ingestion_batch_id="batch_test",
        source_document_id="manual_1",
    )


def _fake_bundle() -> dict:
    return {
        "source_metadata": {
            "source_id": "manual_optisweep_om_v3",
            "source_type": "manual",
            "source_title": "OptiSweep Operation and Maintenance Manual",
            "source_version": "3",
            "ingestion_batch_id": "batch_test",
            "source_document_id": "manual_1",
        },
        "source_document": {"source_document_id": "manual_1", "source_type": "manual"},
        "sections": [
            {
                "section_id": "sec_overview",
                "title": "3.1: System Overview",
                "page_start": 23,
                "page_end": 23,
            },
            {
                "section_id": "sec_starting_system",
                "title": "5.1: Starting the System",
                "page_start": 81,
                "page_end": 81,
            },
            {
                "section_id": "sec_stopping_system",
                "title": "5.2: Stopping the System",
                "page_start": 82,
                "page_end": 82,
            },
        ],
    }
