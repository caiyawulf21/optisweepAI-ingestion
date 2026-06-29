from operationalknowledgeingestion.src.optisweep_ingestion.schemas.source_lineage import SourceLineage
from operationalknowledgeingestion.src.optisweep_ingestion.tools.operational_context_extractor import (
    build_extraction_report,
    build_priority_context_check,
    parse_context_response,
    validate_context_record,
)


# --- parse_context_response ---


def test_parse_context_response_from_plain_json() -> None:
    raw = '{"contexts": [' + json.dumps(_valid_heartbeat_ctx()) + "]}"
    records = parse_context_response(raw)
    assert len(records) == 1
    assert records[0]["context_id"] == "ctx_manual_operator_station_heartbeat_stats_v1"


def test_parse_context_response_from_json_fence() -> None:
    raw = "```json\n" + '{"contexts": [' + json.dumps(_valid_heartbeat_ctx()) + "]}\n```"
    records = parse_context_response(raw)
    assert len(records) == 1


def test_parse_context_response_returns_empty_for_no_contexts() -> None:
    records = parse_context_response('{"contexts": []}')
    assert records == []


def test_parse_context_response_skips_non_dict_entries() -> None:
    raw = '{"contexts": [null, "bad", ' + json.dumps(_valid_heartbeat_ctx()) + "]}"
    records = parse_context_response(raw)
    assert len(records) == 1


# --- validate_context_record ---


def test_valid_record_passes_validation() -> None:
    errors = validate_context_record(_valid_heartbeat_ctx(), {"artifact_manual_manual_optisweep_om_v3_fig_4_22_heartbeat"})
    assert errors == []


def test_invalid_context_type_fails() -> None:
    record = {**_valid_heartbeat_ctx(), "context_type": "runbook"}
    errors = validate_context_record(record, set())
    assert any("context_type" in e for e in errors)


def test_missing_context_id_fails() -> None:
    record = {**_valid_heartbeat_ctx(), "context_id": ""}
    errors = validate_context_record(record, set())
    assert any("context_id" in e for e in errors)


def test_missing_source_id_fails() -> None:
    record = {**_valid_heartbeat_ctx(), "source_id": ""}
    errors = validate_context_record(record, set())
    assert any("source_id" in e for e in errors)


def test_missing_source_refs_fails() -> None:
    record = {**_valid_heartbeat_ctx(), "source_refs": []}
    errors = validate_context_record(record, set())
    assert any("source_refs" in e for e in errors)


def test_unknown_artifact_id_fails() -> None:
    record = {**_valid_heartbeat_ctx(), "related_artifact_ids": ["artifact_nonexistent"]}
    errors = validate_context_record(record, {"artifact_fig_4_22"})
    assert any("artifact_nonexistent" in e for e in errors)


def test_known_artifact_id_passes() -> None:
    record = {
        **_valid_heartbeat_ctx(),
        "related_artifact_ids": ["artifact_fig_4_22"],
        "image_refs": ["artifact_fig_4_22"],
    }
    errors = validate_context_record(record, {"artifact_fig_4_22"})
    assert errors == []


def test_forbidden_field_rejected() -> None:
    record = {**_valid_heartbeat_ctx(), "trigger_conditions": ["alarm active"]}
    errors = validate_context_record(record, set())
    assert any("trigger_conditions" in e for e in errors)


def test_all_forbidden_fields_rejected() -> None:
    from operationalknowledgeingestion.src.optisweep_ingestion.schemas.operational_context import FORBIDDEN_FIELDS

    for field in FORBIDDEN_FIELDS:
        record = {**_valid_heartbeat_ctx(), field: "some value"}
        errors = validate_context_record(record, set())
        assert any(field in e for e in errors), f"Expected '{field}' to be rejected"


def test_wrong_validation_status_fails() -> None:
    record = {**_valid_heartbeat_ctx(), "validation_status": "approved"}
    errors = validate_context_record(record, set())
    assert any("validation_status" in e for e in errors)


# --- build_priority_context_check ---


def test_heartbeat_context_check_detects_all_terms() -> None:
    contexts = [_valid_heartbeat_ctx()]
    check = build_priority_context_check(contexts)
    hb = check["heartbeat_stats"]
    assert hb["found"] is True
    assert hb["has_artifact_ref"] is True
    assert hb["mentions_last_max_min"] is True
    assert hb["mentions_10_seconds"] is True


def test_heartbeat_context_check_not_found_when_missing() -> None:
    check = build_priority_context_check([])
    assert check["heartbeat_stats"]["found"] is False
    assert check["heartbeat_stats"]["has_artifact_ref"] is False
    assert check["heartbeat_stats"]["mentions_last_max_min"] is False
    assert check["heartbeat_stats"]["mentions_10_seconds"] is False


def test_operator_station_context_found() -> None:
    ctx = {
        **_valid_heartbeat_ctx(),
        "context_id": "ctx_op_station_v1",
        "title": "Operator Station HMI Overview",
        "retrieval_text": "The Operator Station HMI provides monitoring controls.",
        "related_artifact_ids": ["artifact_fig_3_1"],
    }
    check = build_priority_context_check([ctx])
    assert check["operator_station_hmi"]["found"] is True
    assert check["operator_station_hmi"]["has_artifact_ref"] is True


def test_add_tote_context_found() -> None:
    ctx = {
        **_valid_heartbeat_ctx(),
        "context_id": "ctx_add_tote_v1",
        "title": "Hospital Add Tote Screen",
        "retrieval_text": "The Add Tote screen allows operators to add tote containers.",
        "related_artifact_ids": [],
    }
    check = build_priority_context_check([ctx])
    assert check["hospital_add_tote"]["found"] is True
    assert check["hospital_add_tote"]["has_artifact_ref"] is False


def test_agv_bump_context_found() -> None:
    ctx = {
        **_valid_heartbeat_ctx(),
        "context_id": "ctx_agv_bump_v1",
        "title": "AGV Bump Fault Screen",
        "retrieval_text": "The AGV Bump Fault screen shows details when an AGV bump sensor triggers.",
        "related_artifact_ids": ["artifact_agv_bump"],
    }
    check = build_priority_context_check([ctx])
    assert check["agv_bump_fault"]["found"] is True
    assert check["agv_bump_fault"]["has_artifact_ref"] is True


# --- build_extraction_report ---


def test_extraction_report_counts() -> None:
    contexts = [_valid_heartbeat_ctx()]
    report = build_extraction_report(
        source_bundle_path="data/output/manual_optisweep_om_v3/source_bundle.json",
        source_artifacts_path="data/output/manual_optisweep_om_v3/source_artifacts_enriched.json",
        contexts=contexts,
        lineage=_lineage(),
        llm_used=True,
        failed_packets=[],
        warnings=[],
    )
    assert report["context_count"] == 1
    assert report["llm_used"] is True
    assert report["records_with_artifacts"] == 1
    assert report["records_without_artifacts"] == 0
    assert report["records_missing_source_refs"] == 0
    assert report["context_counts_by_type"]["hmi_metric_reference"] == 1


def test_extraction_report_records_missing_source_refs() -> None:
    ctx = {**_valid_heartbeat_ctx(), "source_refs": []}
    ctx["source_refs"] = []
    report = build_extraction_report(
        source_bundle_path="bundle.json",
        source_artifacts_path="artifacts.json",
        contexts=[ctx],
        lineage=_lineage(),
        llm_used=True,
        failed_packets=[],
        warnings=[],
    )
    assert report["records_missing_source_refs"] == 1


def test_extraction_report_failed_packets_logged() -> None:
    report = build_extraction_report(
        source_bundle_path="bundle.json",
        source_artifacts_path="artifacts.json",
        contexts=[],
        lineage=_lineage(),
        llm_used=True,
        failed_packets=[{"section_id": "sec_1", "error": "timeout"}],
        warnings=["dropped a record"],
    )
    assert len(report["failed_packets"]) == 1
    assert len(report["warnings"]) == 1


# --- helpers ---


import json


def _valid_heartbeat_ctx() -> dict:
    return {
        "context_id": "ctx_manual_operator_station_heartbeat_stats_v1",
        "title": "Operator Station Heartbeat Stats",
        "context_type": "hmi_metric_reference",
        "summary": "Heartbeat Stats show timing values for heartbeat signals between the tipper and WCS.",
        "details": (
            "The Heartbeat section provides Last, Max, and Min timing values in milliseconds. "
            "Last is the most recent signal timing. Max is the longest. Min is the shortest. "
            "A heartbeat signal longer than 10 seconds can cause operational issues with the tipper."
        ),
        "applies_to": ["Operator Station HMI", "Tipper", "WCS"],
        "key_terms": ["Heartbeat", "Last", "Max", "Min", "10 seconds", "mis-synchronization"],
        "related_artifact_ids": ["artifact_manual_manual_optisweep_om_v3_fig_4_22_heartbeat"],
        "image_refs": ["artifact_manual_manual_optisweep_om_v3_fig_4_22_heartbeat"],
        "related_runbook_candidate_ids": [],
        "source_id": "manual_optisweep_om_v3",
        "source_type": "manual",
        "source_title": "OptiSweep Operation and Maintenance Manual",
        "ingestion_batch_id": "batch_test",
        "source_refs": [
            {
                "source_id": "manual_optisweep_om_v3",
                "source_type": "manual",
                "source_title": "OptiSweep Operation and Maintenance Manual",
                "source_document_id": "optisweep_operation_and_maintenance_manual_final_1",
                "page": 52,
                "section_id": "optisweep_operation_and_maintenance_manual_final_1_4_1_2_2_visu_data_screen",
                "figure_id": "fig_4_22",
                "figure_number": "Figure 4-22",
                "quote_or_summary": "The Heartbeat section provides Last, Max, and Min heartbeat timing values.",
            }
        ],
        "retrieval_text": (
            "Operator Station Heartbeat Stats on the VISU_DATA screen show Last, Max, and Min "
            "heartbeat timing values between the tipper and WCS. A heartbeat signal longer than "
            "10 seconds can cause tipper operational issues due to mis-synchronization."
        ),
        "validation_status": "needs_review",
        "metadata": {
            "created_by": "operational_context_extraction_agent",
            "source_quality": "manual",
        },
    }


def _lineage() -> SourceLineage:
    return SourceLineage(
        source_id="manual_optisweep_om_v3",
        source_type="manual",
        source_title="OptiSweep Operation and Maintenance Manual",
        source_version="3",
        ingestion_batch_id="batch_test",
        source_document_id="optisweep_operation_and_maintenance_manual_final_1",
    )
