from optisweep_ingestion.tools.artifact_enricher import (
    build_artifact_enrichment_report,
    heartbeat_check,
    merge_enrichment,
    parse_llm_response,
    priority_artifact_check,
)


def test_llm_response_parsing_from_json_fence() -> None:
    parsed = parse_llm_response(
        """```json
{"short_description":"Figure showing heartbeat stats.","detailed_description":"Grounded details.","what_to_look_at":["Heartbeat section"],"tags":["heartbeat"],"retrieval_text":"Heartbeat Last Max Min 10 seconds","enrichment_notes":[]}
```"""
    )

    assert parsed["short_description"] == "Figure showing heartbeat stats."
    assert parsed["what_to_look_at"] == ["Heartbeat section"]
    assert parsed["tags"] == ["heartbeat"]


def test_merge_enrichment_preserves_existing_fields_artifact_id_and_source_refs() -> None:
    artifact = _artifact()
    merged = merge_enrichment(
        artifact,
        {
            "short_description": "Heartbeat stats screen.",
            "detailed_description": "Shows heartbeat timing values.",
            "what_to_look_at": ["Heartbeat section"],
            "tags": ["heartbeat"],
            "retrieval_text": "Heartbeat Last Max Min 10 seconds",
            "enrichment_notes": [],
        },
    )

    assert merged["artifact_id"] == artifact["artifact_id"]
    assert merged["source_refs"] == artifact["source_refs"]
    assert merged["existing_field"] == "kept"
    assert merged["short_description"] == "Heartbeat stats screen."


def test_merge_keeps_linked_ids_empty() -> None:
    artifact = _artifact()
    artifact["linked_context_ids"] = ["ctx_1"]
    artifact["linked_runbook_ids"] = ["rb_1"]
    artifact["linked_procedure_ids"] = ["proc_1"]

    merged = merge_enrichment(artifact, _enrichment())

    assert merged["linked_context_ids"] == []
    assert merged["linked_runbook_ids"] == []
    assert merged["linked_procedure_ids"] == []


def test_heartbeat_check_logic() -> None:
    check = heartbeat_check([{**_artifact(), **_enrichment()}])

    assert check["artifact_found"] is True
    assert check["enriched"] is True
    assert check["retrieval_text_contains_heartbeat"] is True
    assert check["retrieval_text_contains_last"] is True
    assert check["retrieval_text_contains_max"] is True
    assert check["retrieval_text_contains_min"] is True
    assert check["retrieval_text_contains_10_seconds"] is True


def test_priority_artifact_report_logic() -> None:
    checks = priority_artifact_check([{**_artifact(), **_enrichment()}])

    assert checks["fig_4_22"]["artifact_found"] is True
    assert checks["fig_4_22"]["enriched"] is True
    assert checks["fig_5_2"]["artifact_found"] is False


def test_enrichment_report_counts() -> None:
    report = build_artifact_enrichment_report([_artifact()], [{**_artifact(), **_enrichment()}], llm_used=True)

    assert report["input_artifact_count"] == 1
    assert report["enriched_artifact_count"] == 1
    assert report["llm_used"] is True
    assert report["failed_artifact_count"] == 0


def _artifact() -> dict:
    return {
        "artifact_id": "artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats",
        "figure_id": "fig_4_22",
        "title": "Operator Station HMI Data Screen-Heartbeat Stats",
        "source_refs": [{"figure_id": "fig_4_22"}],
        "existing_field": "kept",
    }


def _enrichment() -> dict:
    return {
        "short_description": "Heartbeat stats screen.",
        "detailed_description": "Shows heartbeat timing values between the tipper and WCS.",
        "what_to_look_at": ["Heartbeat section", "Last value", "Max value", "Min value", "RESET button"],
        "tags": ["heartbeat", "tipper", "wcs"],
        "retrieval_text": "Heartbeat Last Max Min 10 seconds tipper WCS mis-synchronization RESET button.",
        "enrichment_notes": [],
    }
