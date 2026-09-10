from __future__ import annotations

from shared_pipeline_stages.stage_8.normalize import (
    ensure_backend_evidence_pairing,
    node_needs_backend_pairing,
)
from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch


# ---------------------------------------------------------------------------
# Guaranteed backend-vs-UI completion pass (docs/design_decisions/
# stage_8_playbook_finalization.md, "Backend-vs-UI evidence rule"): for
# diagnostic nodes investigating system state, ensure a WCS/SSMS backend link
# is present alongside at most one RMS/UI link -- as an unconditional
# post-selection step, not a probabilistic scoring outcome.
# ---------------------------------------------------------------------------


def _rms_link(procedure_id: str = "proc_rms_roster_v1") -> dict:
    return {
        "procedure_id": procedure_id,
        "link_confidence": "high",
        "link_role": "primary",
        "link_rank": 1,
    }


ROSTER_MAPPING_NODE = {
    "node_id": "node_roster",
    "node_type": "diagnostic_decision",
    "title": "Identify the abnormal or unmapped robot",
    "intent": "Inspect the RMS fleet or robot status view for roster membership, mapping, location abnormalities.",
    "runbook_placeholder": "Procedure needed to inspect RMS fleet, roster, and mapping-related views.",
}

RMS_ROSTER_RUNBOOK = {
    "procedure_id": "proc_rms_roster_v1",
    "title": "Check RMS Robot Roster And Map Monitor",
    "procedure_type": "diagnostic",
    "capability_tags": ["device_roster_state"],
    "access_surface": ["rms_ui"],
    "audience_roles": ["operator", "L1_support"],
    "role_required": "operator",
}

SQL_ROSTER_RUNBOOK = {
    "procedure_id": "proc_wcs_helix_db_ssms_agv_state_inspection_v1",
    "title": "WCS / Helix DB (SSMS) AGV state inspection",
    "summary": "Use the WCS / Helix DB (SSMS) live read-only database surface to inspect robotics-related AGV state records when the RMS / fleet status UI reports AGVs out of sync.",
    "procedure_type": "diagnostic",
    "capability_tags": ["device_roster_state"],
    "access_surface": ["wcs_sql"],
    "audience_roles": ["L2_support", "L3_support"],
    "role_required": "L2_support",
}

SECOND_RMS_RUNBOOK = {
    "procedure_id": "proc_rms_secondary_v1",
    "title": "Check RMS Map Monitor Station IDs",
    "procedure_type": "diagnostic",
    "capability_tags": ["device_roster_state"],
    "access_surface": ["rms_ui"],
    "audience_roles": ["operator"],
    "role_required": "operator",
}


def _match(runbook: dict, *, raw_score: float = 0.5) -> RunbookSearchMatch:
    return RunbookSearchMatch(
        procedure_id=runbook["procedure_id"],
        title=runbook["title"],
        procedure_type=runbook["procedure_type"],
        cosine_score=raw_score,
        jaccard_score=raw_score,
        combined_score=raw_score,
    )


def test_node_needs_backend_pairing_true_for_roster_mapping_node() -> None:
    assert node_needs_backend_pairing(ROSTER_MAPPING_NODE) is True


def test_node_needs_backend_pairing_false_for_gateway_health_exception() -> None:
    node = {
        "node_id": "node_gateway",
        "node_type": "diagnostic_decision",
        "title": "Check Ignition gateway health and responsiveness",
        "intent": "Determine whether the Ignition gateway shows a current responsiveness problem.",
        "runbook_placeholder": "Procedure needed to inspect Ignition gateway Systems Overview for responsiveness.",
    }
    assert node_needs_backend_pairing(node) is False


def test_node_needs_backend_pairing_false_for_service_restart_exception() -> None:
    node = {
        "node_id": "node_restart",
        "node_type": "procedure_reference",
        "title": "Perform authorized recovery of the affected OptiSweep service",
        "intent": "Use the approved role-specific recovery procedure for the service identified by diagnostic evidence.",
    }
    assert node_needs_backend_pairing(node) is False


def test_node_needs_backend_pairing_false_for_event_viewer_exception() -> None:
    node = {
        "node_id": "node_event_viewer",
        "node_type": "diagnostic_decision",
        "title": "Check Windows Event Viewer / services for OptiSweep-WCSWebApplication",
        "intent": "Confirm the OptiSweep / WCSWebApplication service state using Event Viewer and services.",
    }
    assert node_needs_backend_pairing(node) is False


def test_ensure_backend_evidence_pairing_adds_sql_link_when_missing() -> None:
    runbooks_by_id = {
        RMS_ROSTER_RUNBOOK["procedure_id"]: RMS_ROSTER_RUNBOOK,
        SQL_ROSTER_RUNBOOK["procedure_id"]: SQL_ROSTER_RUNBOOK,
    }
    links = [_rms_link()]
    candidates = [_match(SQL_ROSTER_RUNBOOK, raw_score=0.6)]
    result = ensure_backend_evidence_pairing(
        ROSTER_MAPPING_NODE, links, runbooks_by_id=runbooks_by_id, candidates=candidates
    )
    ids = [link["procedure_id"] for link in result]
    assert SQL_ROSTER_RUNBOOK["procedure_id"] in ids
    assert RMS_ROSTER_RUNBOOK["procedure_id"] in ids


def test_ensure_backend_evidence_pairing_finds_sql_via_full_catalog_fallback() -> None:
    # The SQL runbook is NOT in candidates (simulating it scoring below the
    # node's normal top-K retrieval cutoff) -- the guarantee must still hold
    # via the full-catalog fallback over runbooks_by_id.
    runbooks_by_id = {
        RMS_ROSTER_RUNBOOK["procedure_id"]: RMS_ROSTER_RUNBOOK,
        SQL_ROSTER_RUNBOOK["procedure_id"]: SQL_ROSTER_RUNBOOK,
    }
    links = [_rms_link()]
    result = ensure_backend_evidence_pairing(
        ROSTER_MAPPING_NODE, links, runbooks_by_id=runbooks_by_id, candidates=[]
    )
    ids = [link["procedure_id"] for link in result]
    assert SQL_ROSTER_RUNBOOK["procedure_id"] in ids


def test_ensure_backend_evidence_pairing_noop_when_sql_already_present() -> None:
    runbooks_by_id = {
        RMS_ROSTER_RUNBOOK["procedure_id"]: RMS_ROSTER_RUNBOOK,
        SQL_ROSTER_RUNBOOK["procedure_id"]: SQL_ROSTER_RUNBOOK,
    }
    links = [_rms_link(), {"procedure_id": SQL_ROSTER_RUNBOOK["procedure_id"], "link_confidence": "medium"}]
    result = ensure_backend_evidence_pairing(
        ROSTER_MAPPING_NODE, links, runbooks_by_id=runbooks_by_id, candidates=[]
    )
    assert len(result) == 2
    ids = [link["procedure_id"] for link in result]
    assert ids.count(SQL_ROSTER_RUNBOOK["procedure_id"]) == 1


def test_ensure_backend_evidence_pairing_does_not_force_pairing_on_exception_node() -> None:
    gateway_node = {
        "node_id": "node_gateway",
        "node_type": "diagnostic_decision",
        "title": "Check Ignition gateway health and responsiveness",
        "intent": "Determine whether the Ignition gateway shows a current responsiveness problem.",
        "runbook_placeholder": "Procedure needed to inspect Ignition gateway Systems Overview for responsiveness.",
    }
    runbooks_by_id = {
        RMS_ROSTER_RUNBOOK["procedure_id"]: RMS_ROSTER_RUNBOOK,
        SQL_ROSTER_RUNBOOK["procedure_id"]: SQL_ROSTER_RUNBOOK,
    }
    links = [_rms_link()]
    result = ensure_backend_evidence_pairing(
        gateway_node, links, runbooks_by_id=runbooks_by_id, candidates=[]
    )
    assert result == links


def test_cap_rms_ui_links_drops_second_rms_only_link() -> None:
    runbooks_by_id = {
        RMS_ROSTER_RUNBOOK["procedure_id"]: RMS_ROSTER_RUNBOOK,
        SECOND_RMS_RUNBOOK["procedure_id"]: SECOND_RMS_RUNBOOK,
        SQL_ROSTER_RUNBOOK["procedure_id"]: SQL_ROSTER_RUNBOOK,
    }
    links = [
        _rms_link(),
        _rms_link(SECOND_RMS_RUNBOOK["procedure_id"]),
        {"procedure_id": SQL_ROSTER_RUNBOOK["procedure_id"], "link_confidence": "medium"},
    ]
    result = ensure_backend_evidence_pairing(
        ROSTER_MAPPING_NODE, links, runbooks_by_id=runbooks_by_id, candidates=[]
    )
    ids = [link["procedure_id"] for link in result]
    assert ids.count(RMS_ROSTER_RUNBOOK["procedure_id"]) == 1
    assert SECOND_RMS_RUNBOOK["procedure_id"] not in ids
    assert SQL_ROSTER_RUNBOOK["procedure_id"] in ids


def test_ensure_backend_evidence_pairing_passthrough_when_no_sql_runbook_exists() -> None:
    # Genuine catalog gap: no wcs_sql runbook exists anywhere. Links must pass
    # through unchanged rather than fabricating a pairing.
    runbooks_by_id = {RMS_ROSTER_RUNBOOK["procedure_id"]: RMS_ROSTER_RUNBOOK}
    links = [_rms_link()]
    result = ensure_backend_evidence_pairing(
        ROSTER_MAPPING_NODE, links, runbooks_by_id=runbooks_by_id, candidates=[]
    )
    assert result == links
