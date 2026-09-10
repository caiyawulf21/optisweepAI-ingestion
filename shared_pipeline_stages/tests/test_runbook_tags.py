from __future__ import annotations

from shared_pipeline_stages.runbook_tags import infer_runbook_tags, normalize_runbook_tags, union_runbook_tags
from shared_pipeline_stages.stage_prompts import compose_stage6_system_prompt


def test_normalize_filters_invalid_and_canonicalizes_ssms() -> None:
    runbook = {
        "capability_tags": ["agv_active_errors", "not_real"],
        "access_surface": ["ssms", "rms_ui"],
        "audience_roles": ["L2_support"],
        "failure_pattern_tags": ["pairing_failure", "bogus"],
        "role_required": "L2_support",
    }
    normalize_runbook_tags(runbook)
    assert runbook["capability_tags"] == ["agv_active_errors"]
    assert runbook["access_surface"] == ["wcs_sql", "rms_ui"]
    assert runbook["failure_pattern_tags"] == ["pairing_failure"]


def test_infer_active_agv_sql_runbook() -> None:
    runbook = {
        "title": "Query Active AGV Errors From the WCS Database",
        "summary": "Retrieve active AGV errors via SSMS against SystemActiveErrorModel in Helix.",
        "role_required": "L2_support",
        "access_or_tools_needed": ["WCS database", "SSMS"],
    }
    infer_runbook_tags(runbook)
    assert "agv_active_errors" in runbook["capability_tags"]
    assert "wcs_sql" in runbook["access_surface"]
    assert "L2_support" in runbook["audience_roles"]


def test_infer_rms_fleet_check() -> None:
    runbook = {
        "title": "Check Overall System RMS For System Faults And Active AGV Faults",
        "summary": "Use Overall System RMS to inspect fleet status and AGV faults.",
        "role_required": "L1_support",
    }
    infer_runbook_tags(runbook)
    assert set(runbook["capability_tags"]) & {"agv_active_errors", "fleet_system_status"}
    assert "rms_ui" in runbook["access_surface"]


def test_union_tags_from_sources() -> None:
    primary = {"capability_tags": ["fleet_system_status"], "access_surface": ["rms_ui"]}
    sources = [
        {"capability_tags": ["agv_active_errors"], "access_surface": ["wcs_sql"], "audience_roles": ["L2_support"]},
    ]
    union_runbook_tags(primary, sources)
    assert "agv_active_errors" in primary["capability_tags"]
    assert "wcs_sql" in primary["access_surface"]
    assert "L2_support" in primary["audience_roles"]


def test_compose_stage6_includes_taxonomy_appendix() -> None:
    composed = compose_stage6_system_prompt("Task prompt body.")
    assert "Appended Capability Taxonomy" in composed
    assert "agv_active_errors" in composed
    assert "wcs_sql" in composed
