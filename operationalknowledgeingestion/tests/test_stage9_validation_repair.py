from optisweep_ingestion.stage9_validation_repair import validate_source_knowledge_outputs


def test_validator_rejects_forbidden_candidate_fields() -> None:
    candidate = _candidate()
    candidate["trigger_conditions"] = ["alarm active"]

    result = validate_source_knowledge_outputs(candidates=[candidate])

    assert any("forbidden field 'trigger_conditions'" in failure for failure in result["schema_validation_failures"])


def test_validator_checks_missing_lineage() -> None:
    artifact = _artifact()
    artifact.pop("source_id")

    result = validate_source_knowledge_outputs(artifacts=[artifact])

    assert any("missing source lineage fields" in failure for failure in result["schema_validation_failures"])


def test_validator_checks_missing_artifact_refs() -> None:
    candidate = _candidate()
    candidate["related_artifact_ids"] = ["missing_artifact"]

    result = validate_source_knowledge_outputs(
        artifacts=[_artifact()],
        candidates=[candidate],
    )

    assert result["missing_artifact_reference_count"] == 1


def _artifact() -> dict:
    return {
        "artifact_id": "artifact_manual_manual_optisweep_om_v3_fig_4_22",
        "source_id": "manual_optisweep_om_v3",
        "source_type": "manual",
        "ingestion_batch_id": "batch_test",
        "source_refs": [{"page": 52}],
    }


def _candidate() -> dict:
    return {
        "candidate_id": "candidate_manual_check_heartbeat",
        "title": "Check Heartbeat",
        "candidate_goal": "Check heartbeat values.",
        "likely_procedure_type": "diagnostic",
        "likely_role_required": "operator",
        "summary": "Review heartbeat values.",
        "source_id": "manual_optisweep_om_v3",
        "source_type": "manual",
        "ingestion_batch_id": "batch_test",
        "source_refs": [{"page": 52}],
        "rough_steps": ["Review heartbeat values."],
        "candidate_status": "needs_review",
    }
