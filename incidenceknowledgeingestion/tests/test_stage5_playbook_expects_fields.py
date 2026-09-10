from __future__ import annotations

from optisweep_incidence_ingestion.stage5_runbook_candidates import (
    _normalize_playbook_node,
    _scrub_unknown_playbook_refs,
    validate_and_dedupe_playbook_candidates,
)


def test_normalize_playbook_node_keeps_source_evidence_fields() -> None:
    node = _normalize_playbook_node(
        {
            "node_id": "node_1",
            "node_order": 1,
            "node_type": "diagnostic_decision",
            "title": "Confirm active AGV errors",
            "intent": "Check AGV active errors remotely or on site.",
            "runbook_placeholder": "Procedure needed to confirm active AGV errors via RMS and/or WCS/SSMS.",
            "allowed_roles": ["L2_support", "operator"],
            "required_evidence_concepts": ["agv_active_errors", "not_a_real_capability"],
            "observed_surfaces": ["rms_ui"],
            "source_used_surfaces": [
                {
                    "surface": "rms_ui",
                    "provenance": "explicit_source",
                    "source_evidence": "The incident states RMS showed the active errors.",
                }
            ],
            "recommended_diagnostic_surfaces": ["rms_ui"],
            "preferred_audience": ["L2_support"],
            "expected_or_observed_result": "Remote L2 sees no active errors in RMS/SSMS.",
        },
        1,
        source_text="The incident states RMS showed the active errors.",
    )
    assert node["required_evidence_concepts"] == ["agv_active_errors"]
    assert node["observed_surfaces"] == ["rms_ui"]
    assert node["source_used_surfaces"][0]["provenance"] == "explicit_source"
    assert node["recommended_diagnostic_surfaces"] == ["rms_ui"]
    assert node["expects_surface"] == ["rms_ui"]
    assert node["preferred_audience"] == ["L2_support"]


def test_normalize_playbook_node_keeps_llm_expects_without_rewrite() -> None:
    node = _normalize_playbook_node(
        {
            "node_id": "node_1",
            "node_order": 1,
            "node_type": "diagnostic_decision",
            "title": "Confirm active AGV faults",
            "intent": "Check whether AGVs show active faults.",
            "runbook_placeholder": "Procedure needed to confirm active AGV errors via RMS and/or WCS/SSMS.",
            "expects_capability": ["fleet_system_status"],
            "expects_surface": ["rms_ui"],
            "preferred_audience": ["L2_support"],
            "expected_or_observed_result": "Remote L2 sees active error rows clear in RMS/SSMS.",
        },
        1,
    )
    # Taxonomy filter only — do not rewrite capability or auto-fill a surface.
    assert node["expects_capability"] == ["fleet_system_status"]
    assert node["expects_surface"] == []


def test_normalize_does_not_force_pairing_capability_shortlist() -> None:
    node = _normalize_playbook_node(
        {
            "node_id": "node_1",
            "node_order": 1,
            "node_type": "diagnostic_decision",
            "title": "Confirm zone pairing failure",
            "intent": "Determine whether the zone is unable to get a pair.",
            "runbook_placeholder": (
                "Procedure needed to confirm with the site which zone cannot get a pair, "
                "then check RMS and/or WCS/SSMS for active errors."
            ),
            "expects_capability": ["agv_active_errors", "device_roster_state"],
            "expects_surface": ["rms_ui"],
            "preferred_audience": ["operator", "L2_support"],
            "expected_or_observed_result": "Site or remote sees pairing restored for the affected zone.",
        },
        1,
    )
    assert node["expects_capability"] == ["agv_active_errors", "device_roster_state"]
    assert node["expects_surface"] == []


def test_normalize_does_not_autofill_surfaces() -> None:
    node = _normalize_playbook_node(
        {
            "node_id": "node_1",
            "node_order": 1,
            "node_type": "diagnostic_decision",
            "title": "Confirm hospital induct failure",
            "intent": "Determine whether hospital lane induct/add is failing.",
            "runbook_placeholder": "Procedure needed to confirm hospital station behavior.",
            "expects_capability": ["hospital_diversion"],
            "expects_surface": ["hospital_hmi"],
            "preferred_audience": ["operator"],
            "expected_or_observed_result": "Site sees hospital stacklight/lane routing return to normal induct.",
        },
        1,
    )
    assert node["expects_capability"] == ["hospital_diversion"]
    assert node["expects_surface"] == []


def test_normalize_drops_surfaces_not_present_in_source() -> None:
    node = _normalize_playbook_node(
        {
            "node_id": "node_1",
            "node_type": "diagnostic_decision",
            "title": "Confirm fleet state",
            "intent": "Determine whether RMS reports an abnormal fleet state.",
            "observed_surfaces": ["rms_ui"],
            "source_used_surfaces": [
                {
                    "surface": "rms_ui",
                    "provenance": "strongly_implied_by_source",
                    "source_evidence": "AGVs are involved.",
                }
            ],
            "recommended_diagnostic_surfaces": ["rms_ui"],
            "stage8_candidate_surfaces": ["wcs_sql"],
        },
        1,
        source_text="AGVs are involved and the fleet is unavailable.",
    )
    assert node["observed_surfaces"] == []
    assert node["source_used_surfaces"] == []
    assert node["recommended_diagnostic_surfaces"] == []
    assert node["stage8_candidate_surfaces"] == ["wcs_sql"]
    assert "RMS" not in node["intent"]


def test_playbook_discovery_packet_uses_ontology_for_support_contracts() -> None:
    from optisweep_incidence_ingestion.stage5_runbook_candidates import _packet_for_playbook_discovery

    packet = _packet_for_playbook_discovery(
        {
            "packet_type": "stage_5_incident_runbook_candidate_discovery_packet",
            "canonical_incident_record": {"title": "AGVs stopped with active errors", "summary": "System down"},
            "timeline_events": [],
            "artifact_evidence": [],
            "evidence_chunk_index": [],
            "page_text_chunks": [],
            "ontology_snippets": [{"id": "capability:agv_active_errors"}],
            "instructions": ["old"],
        },
        "playbook_prompt_a_one_per_incident",
    )
    assert packet["packet_type"] == "stage_5_incident_playbook_candidate_discovery_packet"
    joined = " ".join(packet["instructions"])
    assert packet["ontology_snippets"] == [{"id": "capability:agv_active_errors"}]
    assert "source_used_surfaces" in joined
    assert "recommended_diagnostic_surfaces" in joined
    assert "backend mappings" in joined


def test_playbook_validation_warns_when_expects_capability_missing() -> None:
    packet = {
        "source_package": {"source_id": "src", "source_case_id": "228086", "ingestion_batch_id": "batch"},
        "canonical_incident_record": {},
        "timeline_events": [],
        "enriched_artifacts": [],
    }
    known = {"artifact_ids": set(), "event_ids": set(), "page_refs": set(), "chunk_ids": set()}
    candidates = [
        {
            "playbook_candidate_id": "playbook_candidate_test",
            "title": "Test playbook",
            "playbook_goal": "Test goal",
            "user_facing_summary": "Summary",
            "source_id": "src",
            "ingestion_batch_id": "batch",
            "source_refs": [{"page_ref": "case_228086:page_1", "support_type": "page_ocr", "quote_or_summary": "x"}],
            "nodes": [
                {
                    "node_id": "node_1",
                    "node_order": 1,
                    "node_type": "diagnostic_decision",
                    "title": "Check status",
                    "intent": "Check status",
                    "goal": "Check status",
                    "runbook_placeholder": "Procedure needed to inspect RMS fleet status.",
                    "source_refs": [{"page_ref": "case_228086:page_1", "support_type": "page_ocr", "quote_or_summary": "x"}],
                },
                {
                    "node_id": "node_2",
                    "node_order": 2,
                    "node_type": "escalation_gate",
                    "title": "Escalate",
                    "intent": "Escalate",
                    "goal": "Escalate",
                    "runbook_placeholder": "Procedure needed to escalate unsupported changes.",
                    "source_refs": [{"page_ref": "case_228086:page_1", "support_type": "page_ocr", "quote_or_summary": "x"}],
                },
            ],
        }
    ]
    # page_refs must be known for validation
    known["page_refs"].add("case_228086:page_1")
    accepted, report = validate_and_dedupe_playbook_candidates(candidates, packet, known)
    assert len(accepted) == 1
    assert report["nodes_missing_expects_capability"] >= 1
    assert any("expects_capability" in warning for warning in report["warnings"])


def test_scrub_unknown_playbook_refs_keeps_candidate() -> None:
    candidate = {
        "playbook_candidate_id": "pb_1",
        "title": "Test",
        "playbook_goal": "Goal",
        "user_facing_summary": "Summary",
        "source_id": "src",
        "ingestion_batch_id": "batch",
        "related_event_ids": ["7031", "evt_real"],
        "related_artifact_ids": ["case_x:page_1", "art_real"],
        "source_refs": [{"page_ref": "case_x:page_1", "support_type": "page_ocr", "quote_or_summary": "x"}],
        "nodes": [
            {
                "node_id": "n1",
                "node_order": 1,
                "node_type": "diagnostic_decision",
                "title": "Check",
                "goal": "Check",
                "runbook_placeholder": "Procedure needed to check RMS.",
                "related_event_ids": ["7031"],
                "related_artifact_ids": ["bogus"],
                "source_refs": [{"page_ref": "case_x:page_1", "support_type": "page_ocr", "quote_or_summary": "x"}],
            },
            {
                "node_id": "n2",
                "node_order": 2,
                "node_type": "escalation_gate",
                "title": "Escalate",
                "goal": "Escalate",
                "runbook_placeholder": "Procedure needed to escalate.",
                "source_refs": [{"page_ref": "case_x:page_1", "support_type": "page_ocr", "quote_or_summary": "x"}],
            },
        ],
    }
    known = {
        "artifact_ids": {"art_real"},
        "event_ids": {"evt_real"},
        "page_refs": {"case_x:page_1"},
        "chunk_ids": set(),
    }
    warnings = _scrub_unknown_playbook_refs(candidate, known)
    assert candidate["related_event_ids"] == ["evt_real"]
    assert candidate["related_artifact_ids"] == ["art_real"]
    assert candidate["nodes"][0]["related_event_ids"] == []
    assert candidate["nodes"][0]["related_artifact_ids"] == []
    assert any("7031" in w for w in warnings)
    packet = {"source_package": {"source_id": "src", "source_case_id": "x", "ingestion_batch_id": "batch"}}
    accepted, report = validate_and_dedupe_playbook_candidates([candidate], packet, known)
    assert len(accepted) == 1
    assert report["dropped_candidate_count"] == 0
