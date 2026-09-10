from __future__ import annotations

from scripts.backfill_playbook_expects import _infer_audience, backfill_node


def test_infer_audience_rms_prefers_operator() -> None:
    assert _infer_audience("check rms overview", ["rms_ui"], []) == ["operator", "L1_support"]


def test_infer_audience_wcs_sql_prefers_l2_l3() -> None:
    assert _infer_audience("query ssms", ["wcs_sql"], []) == ["L2_support", "L3_support"]


def test_infer_audience_dual_surface_includes_operator_and_l2() -> None:
    out = _infer_audience("active agv errors", ["rms_ui", "wcs_sql"], [])
    assert out[0] == "operator"
    assert "L2_support" in out


def test_backfill_forces_operator_for_rms_surface() -> None:
    node = {
        "node_type": "diagnostic_decision",
        "title": "Check active AGV errors",
        "expects_capability": ["agv_active_errors"],
        "expects_surface": ["rms_ui", "wcs_sql"],
        "preferred_audience": ["L1_support"],
    }
    assert backfill_node(node, force=True) is True
    preferred = node["preferred_audience"]
    assert "operator" in preferred
    assert "L2_support" in preferred
