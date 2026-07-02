from operationalknowledgeingestion.src.optisweep_ingestion.tools.context_id_resolver import (
    normalize_context_slug,
    resolve_context_id,
    resolve_context_ids,
    resolve_candidate_context_ids,
    build_context_resolution_index,
)


def _contexts() -> list[dict]:
    return [
        {
            "context_id": "ctx_manual_visu_dual_mcp_hmi_screen_reference_v1",
            "title": "Visu_Dual_MCP HMI screen reference",
        },
        {
            "context_id": "ctx_manual_operator_station_stacklight_statuses_v1",
            "title": "Operator station stacklight statuses",
        },
        {
            "context_id": "ctx_manual_lift_connecting_rod_safety_v1",
            "title": "Lift connecting rod safety",
        },
    ]


def test_normalize_context_slug_strips_manual_prefix() -> None:
    assert normalize_context_slug("ctx_manual_visu_dual_mcp_hmi_screen_reference_v1") == (
        "visu_dual_mcp_hmi_screen_reference"
    )
    assert normalize_context_slug("ctx_visu_dual_mcp_screen_reference_v1") == "visu_dual_mcp_screen_reference"


def test_resolve_context_id_maps_legacy_id_to_manual_id() -> None:
    index = build_context_resolution_index(_contexts())
    resolved = resolve_context_id("ctx_visu_dual_mcp_screen_reference_v1", index)
    assert resolved == "ctx_manual_visu_dual_mcp_hmi_screen_reference_v1"


def test_resolve_context_ids_deduplicates_and_drops_unknown() -> None:
    contexts = _contexts()
    resolved, notes = resolve_context_ids(
        [
            "ctx_visu_dual_mcp_screen_reference_v1",
            "ctx_manual_visu_dual_mcp_hmi_screen_reference_v1",
            "ctx_missing_context_v1",
        ],
        contexts,
    )
    assert resolved == ["ctx_manual_visu_dual_mcp_hmi_screen_reference_v1"]
    assert any("Unresolved" in note for note in notes)


def test_resolve_candidate_context_ids_updates_candidate() -> None:
    candidate = {
        "candidate_id": "candidate_l2_operator_station_lockout_tagout_from_visu_dual_mcp",
        "related_context_ids": [
            "ctx_visu_dual_mcp_screen_reference_v1",
            "ctx_lift_connecting_rod_safety_v1",
        ],
    }
    updated, notes = resolve_candidate_context_ids(candidate, _contexts())
    assert "ctx_manual_visu_dual_mcp_hmi_screen_reference_v1" in updated["related_context_ids"]
    assert "ctx_manual_lift_connecting_rod_safety_v1" in updated["related_context_ids"]
    assert notes
