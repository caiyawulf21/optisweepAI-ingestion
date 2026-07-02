from operationalknowledgeingestion.src.optisweep_ingestion.tools.artifact_linker import (
    IMAGE_NOTE_MARKER,
    collect_candidate_artifact_ids,
    enrich_context_record,
    enrich_runbook_candidate,
    find_matching_artifact_ids,
)


def _artifacts() -> list[dict]:
    return [
        {
            "artifact_id": "artifact_fig_3_1_operator_station",
            "figure_id": "fig_3_1",
            "page_number": 24,
            "image_type": "photo",
            "short_description": "Operator station with panels removed for clarity.",
            "retrieval_text": "Figure 3-1 operator station overview with stacklights and HMI.",
            "tags": ["operator_station", "stacklight"],
        },
        {
            "artifact_id": "artifact_page_83_image_10",
            "page_number": 83,
            "image_type": "operator_station_screen",
            "short_description": "Visu_Dual_MCP jogging screen with axis controls.",
            "retrieval_text": "Navigate to the Visu_Dual_MCP screen and press JOG to open axis controls.",
            "tags": ["visu_dual_mcp", "jog"],
        },
    ]


def test_find_matching_artifact_ids_by_figure_and_screen_name() -> None:
    record = {
        "title": "Lock Out And Tag Out From Visu_Dual_MCP",
        "summary": "Navigate to the Visu_Dual_MCP screen and press CYCLE STOP.",
        "source_refs": [
            {"page": 18, "figure_id": "fig_3_1", "figure_number": "Figure 3-1"},
        ],
    }

    matched = find_matching_artifact_ids(record, _artifacts(), max_results=4)

    assert "artifact_fig_3_1_operator_station" in matched
    assert "artifact_page_83_image_10" in matched


def test_enrich_context_record_backfills_image_refs() -> None:
    context = {
        "context_id": "ctx_visu_dual_mcp_screen_reference_v1",
        "context_type": "hmi_screen_reference",
        "title": "Visu_Dual_MCP HMI screen reference",
        "summary": "Navigate to the Visu_Dual_MCP screen on the operator station HMI.",
        "details": "The operator station HMI includes a screen named Visu_Dual_MCP.",
        "key_terms": ["Visu_Dual_MCP", "operator station HMI"],
        "related_artifact_ids": [],
        "image_refs": [],
        "source_refs": [{"page": 18}],
    }

    enriched, notes = enrich_context_record(context, _artifacts())

    assert enriched["related_artifact_ids"]
    assert enriched["image_refs"] == enriched["related_artifact_ids"]
    assert notes


def test_enrich_runbook_candidate_links_artifacts_and_image_notes() -> None:
    candidate = {
        "candidate_id": "candidate_l2_operator_station_lockout_tagout_from_visu_dual_mcp",
        "title": "Lock Out And Tag Out From Visu_Dual_MCP",
        "summary": "Navigate to the Visu_Dual_MCP screen and press CYCLE STOP.",
        "rough_steps": [
            'At the operator station HMI, navigate to the "Visu_Dual_MCP" screen.',
            "Press CYCLE STOP.",
        ],
        "related_context_ids": ["ctx_visu_dual_mcp_screen_reference_v1"],
        "related_artifact_ids": [],
        "source_refs": [{"page": 18}],
    }
    contexts = [
        {
            "context_id": "ctx_visu_dual_mcp_screen_reference_v1",
            "title": "Visu_Dual_MCP HMI screen reference",
            "summary": "Navigate to the Visu_Dual_MCP screen.",
            "related_artifact_ids": [],
            "image_refs": [],
            "source_refs": [{"page": 18}],
        }
    ]

    enriched, notes = enrich_runbook_candidate(candidate, _artifacts(), {contexts[0]["context_id"]: contexts[0]})

    assert enriched["related_artifact_ids"]
    assert any(IMAGE_NOTE_MARKER in step for step in enriched["rough_steps"])
    assert notes


def test_collect_candidate_artifact_ids_uses_context_image_refs() -> None:
    candidate = {
        "candidate_id": "candidate_manual_start_operator_station",
        "title": "Start Operator Station",
        "summary": "Use the operator station control panel.",
        "related_artifact_ids": [],
        "related_context_ids": ["ctx_operator_station_overview_v1"],
        "source_refs": [{"page": 24}],
    }
    contexts = {
        "ctx_operator_station_overview_v1": {
            "context_id": "ctx_operator_station_overview_v1",
            "image_refs": ["artifact_fig_3_1_operator_station"],
            "related_artifact_ids": ["artifact_fig_3_1_operator_station"],
        }
    }

    artifact_ids = collect_candidate_artifact_ids(candidate, _artifacts(), contexts)

    assert "artifact_fig_3_1_operator_station" in artifact_ids
