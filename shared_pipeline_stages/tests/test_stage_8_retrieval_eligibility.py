from __future__ import annotations

from shared_pipeline_stages.stage_8.capability_derivation import (
    NO_REQUIRED_OVERLAP_PENALTY,
    PRIMARY_EXCLUSION_PENALTY,
    capability_domain_adjustment,
    derive_retrieval_request,
    runbook_derived_capabilities,
)
from shared_pipeline_stages.stage_8.link_scoring import boost_combined_score, build_retrieval_query_text
from shared_pipeline_stages.stage_8.normalize import (
    _surface_ids_from_text,
    evidence_domain_penalty,
    runbook_exact_fit_gaps,
    select_runbook_matches,
    total_domain_penalty,
)
from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch


# ---------------------------------------------------------------------------
# Fixtures mirroring case 228086's real nodes/runbooks (Section 9 regression
# target of the retrieval fix plan).
# ---------------------------------------------------------------------------

GATEWAY_HEALTH_NODE = {
    "node_id": "node_3",
    "node_type": "diagnostic_decision",
    "title": "Check whether Ignition gateway health is abnormal or merely a related observation",
    "intent": "Determine whether the Ignition gateway shows a current responsiveness problem or whether the memory observation is only follow-up context.",
    "runbook_placeholder": (
        "Procedure needed to inspect the Ignition gateway Systems Overview for gateway "
        "responsiveness, current response behavior, recent slow-response events, and "
        "available CPU or memory trend evidence."
    ),
}

RECOVERY_NODE = {
    "node_id": "node_4",
    "node_type": "procedure_reference",
    "title": "Perform authorized recovery of the affected gateway or OptiSweep service",
    "intent": "Use the approved role-specific recovery procedure for the service or gateway identified by the diagnostic evidence.",
    "runbook_placeholder": "Procedure needed for authorized recovery of the named Ignition gateway or OptiSweep service.",
}

AGV_STATE_NODE = {
    "node_id": "node_5",
    "node_type": "diagnostic_decision",
    "title": "Determine whether residual AGV state requires correction after service recovery",
    "intent": "Identify whether AGVs remain out of sync, unmapped, or otherwise abnormal after the service or gateway recovery.",
    "runbook_placeholder": (
        "Procedure needed to inspect the RMS fleet or map view for residual out-of-sync, "
        "unavailable, unmapped, or abnormal-state AGVs after service recovery."
    ),
}

VALIDATION_NODE = {
    "node_id": "node_7",
    "node_type": "validation_gate",
    "title": "Validate service responsiveness, AGV status, and resumed operation",
    "intent": (
        "Confirm that the recovered service and fleet state support stable automated "
        "operation before declaring the troubleshooting path complete."
    ),
}


def _runbook(procedure_id: str, title: str, summary: str, when_to_use: str = "", procedure_type: str = "diagnostic") -> dict:
    return {
        "procedure_id": procedure_id,
        "title": title,
        "summary": summary,
        "when_to_use": when_to_use,
        "procedure_type": procedure_type,
        "capability_tags": [],
        "access_surface": [],
        "audience_roles": [],
    }


OPC_TAG_FLOW_RUNBOOK = _runbook(
    "proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1",
    "Check OPC COM tag subscription updates flowing to Sorter Sweeper (Ignition tag provider to OPC server to Sorter Sweeper processing)",
    "Verify that OPC COM is actively subscribing to tags and that tag updates are being written to the OPC server and forwarded to the Sorter Sweeper module for processing; also confirm Ignition gateway health when needed.",
    "Use when you need to confirm the live tag flow: OPC COM subscribes to tags, tag updates are written via the OPC server/ignition tag provider, and Sorter Sweeper receives/acts on those updates.",
)

GATEWAY_RESTART_RUNBOOK = _runbook(
    "proc_ignition_gateway_restart_and_optisweep_response_validation_v1",
    "Ignition gateway restart and OptiSweep / WCS API response validation",
    "Use the Ignition gateway, Windows Event Viewer / services, and Apidog / WCS API surfaces to restart the Ignition gateway, verify the GetAgvStatuses response, and restart OptiSweep only if the API does not respond.",
    "Use when the Ignition gateway or OptiSweep / WCS API is not responding.",
    procedure_type="recovery",
)

HELIX_AGV_STATE_RUNBOOK = _runbook(
    "proc_wcs_helix_db_ssms_agv_state_inspection_v1",
    "WCS / Helix DB (SSMS) AGV state inspection",
    "Use the WCS / Helix DB (SSMS) live read-only database surface to inspect robotics-related AGV state records when the RMS / fleet status UI reports AGVs out of sync or the robotic system is stopped.",
    "Use the live WCS / Helix DB (SSMS) surface to inspect AGV state records when the RMS / fleet status UI reports AGVs out of sync.",
)

ACTIVE_AGV_ERROR_RUNBOOK = _runbook(
    "proc_query_active_agv_errors_from_the_wcs_database_v1",
    "Query Active AGV Errors From the WCS Database",
    "Retrieve current active AGV error records from the WCS database by querying [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel].",
    "Use this procedure when active AGV error records need to be retrieved from the WCS database for investigation or visibility.",
)


def _match(runbook: dict, *, raw_score: float) -> RunbookSearchMatch:
    return RunbookSearchMatch(
        procedure_id=runbook["procedure_id"],
        title=runbook["title"],
        procedure_type=runbook["procedure_type"],
        cosine_score=raw_score,
        jaccard_score=raw_score,
        combined_score=raw_score,
    )


# ---------------------------------------------------------------------------
# Gateway health: OPC tag-flow must be penalized, not selected, for a generic
# gateway-health node -- but domain rules are score input now, not a hard
# veto, so a strong enough semantic match could still win against a weaker
# same-domain competitor (see the adversarial test below for the guarantee
# that a *normal* score gap still can't rescue it).
# ---------------------------------------------------------------------------


def test_gateway_health_node_penalizes_opc_tag_flow_without_tag_language() -> None:
    request = derive_retrieval_request(GATEWAY_HEALTH_NODE)
    penalty, reason = capability_domain_adjustment(request, OPC_TAG_FLOW_RUNBOOK)
    assert penalty <= PRIMARY_EXCLUSION_PENALTY
    assert "opc_tag_flow" in (reason or "")


def test_gateway_health_node_low_score_opc_candidate_scores_below_relevance() -> None:
    # A low raw-score OPC candidate combined with the domain penalty must
    # land at (or below) zero -- confirms the penalty is not merely present
    # but large enough to suppress a weak match entirely.
    match = _match(OPC_TAG_FLOW_RUNBOOK, raw_score=0.04)
    runbooks_by_id = {OPC_TAG_FLOW_RUNBOOK["procedure_id"]: OPC_TAG_FLOW_RUNBOOK}
    domain_penalty, _ = total_domain_penalty(GATEWAY_HEALTH_NODE, match, OPC_TAG_FLOW_RUNBOOK)
    boosted = boost_combined_score(
        match.combined_score,
        node=GATEWAY_HEALTH_NODE,
        node_text=build_retrieval_query_text(GATEWAY_HEALTH_NODE),
        match=match,
        runbook=OPC_TAG_FLOW_RUNBOOK,
        procedure_type_compatible=True,
        domain_penalty=domain_penalty,
    )
    assert boosted <= 0.05


def test_agv_state_node_does_not_select_opc_when_helix_state_competes_normally() -> None:
    # Adversarial regression guard: even with domain rules softened to score
    # input, OPC tag-flow (wrong domain entirely for an AGV-state node) must
    # still lose to the Helix AGV-state runbook under a normal score gap (not
    # an extreme one) -- proving the compounding domain penalties (excluded
    # capability + unrelated-equipment + wrong-domain-for-node, floored at
    # MAX_DOMAIN_PENALTY) reliably dominate ordinary competition.
    matches = [
        _match(OPC_TAG_FLOW_RUNBOOK, raw_score=0.55),
        _match(HELIX_AGV_STATE_RUNBOOK, raw_score=0.45),
    ]
    runbooks_by_id = {
        OPC_TAG_FLOW_RUNBOOK["procedure_id"]: OPC_TAG_FLOW_RUNBOOK,
        HELIX_AGV_STATE_RUNBOOK["procedure_id"]: HELIX_AGV_STATE_RUNBOOK,
    }
    selected = select_runbook_matches(AGV_STATE_NODE, matches, runbooks_by_id=runbooks_by_id)
    assert selected, "expected at least one selected runbook"
    assert selected[0][0].procedure_id == HELIX_AGV_STATE_RUNBOOK["procedure_id"]


# ---------------------------------------------------------------------------
# OPC tag flow: a node that actually asks about tag subscriptions must
# retrieve the OPC COM procedure with no domain-rule penalty.
# ---------------------------------------------------------------------------


def test_opc_tag_flow_node_accepts_opc_procedure_with_no_penalty() -> None:
    node = {
        "node_id": "node_opc",
        "node_type": "diagnostic_decision",
        "title": "Verify OPC COM tag subscriptions and Sorter Sweeper correlation",
        "intent": "Confirm tag updates are reaching Sorter Sweeper processing records via the OPC server.",
    }
    request = derive_retrieval_request(node)
    penalty, _ = capability_domain_adjustment(request, OPC_TAG_FLOW_RUNBOOK)
    assert penalty == 0.0
    assert request["action_family"] == "opc_tag_flow"


# ---------------------------------------------------------------------------
# AGV state: a state/synchronization query must rank the Helix state
# procedure above the active-error-only procedure (Section 8: primary vs
# corroborating, not a replacement).
# ---------------------------------------------------------------------------


def test_agv_state_node_prefers_helix_state_over_active_error_only() -> None:
    runbooks_by_id = {
        HELIX_AGV_STATE_RUNBOOK["procedure_id"]: HELIX_AGV_STATE_RUNBOOK,
        ACTIVE_AGV_ERROR_RUNBOOK["procedure_id"]: ACTIVE_AGV_ERROR_RUNBOOK,
    }
    # Active-error procedure deliberately given a *stronger* raw score than
    # the state-inspection procedure -- selection must still prefer the
    # broader capability as primary per Section 8.
    matches = [
        _match(ACTIVE_AGV_ERROR_RUNBOOK, raw_score=0.55),
        _match(HELIX_AGV_STATE_RUNBOOK, raw_score=0.40),
    ]
    selected = select_runbook_matches(AGV_STATE_NODE, matches, runbooks_by_id=runbooks_by_id)
    assert selected, "expected at least one selected runbook"
    primary_id = selected[0][0].procedure_id
    assert primary_id == HELIX_AGV_STATE_RUNBOOK["procedure_id"]


def test_agv_state_node_still_allows_active_error_as_corroboration_no_penalty() -> None:
    request = derive_retrieval_request(AGV_STATE_NODE)
    penalty, _ = capability_domain_adjustment(request, ACTIVE_AGV_ERROR_RUNBOOK)
    assert penalty == 0.0


# ---------------------------------------------------------------------------
# Active errors: an active-error-specific query must retrieve the
# SystemActiveErrorModel procedure with no penalty.
# ---------------------------------------------------------------------------


def test_active_error_node_retrieves_active_error_procedure_no_penalty() -> None:
    node = {
        "node_id": "node_active_err",
        "node_type": "diagnostic_decision",
        "title": "Query current active AGV and system error records",
        "intent": "Query current active AGV and system error records from Helix2x_1Prod_Robotics SystemActiveErrorModel in SSMS.",
    }
    request = derive_retrieval_request(node)
    penalty, _ = capability_domain_adjustment(request, ACTIVE_AGV_ERROR_RUNBOOK)
    assert penalty == 0.0
    assert "agv_active_error_inspection" in request["required_capabilities"]


# ---------------------------------------------------------------------------
# Validation: the multi-signal validation node must penalize the AGV-state
# diagnostic procedure enough that it does not survive selection alongside a
# same-domain competitor.
# ---------------------------------------------------------------------------


def test_validation_node_penalizes_agv_state_procedure() -> None:
    request = derive_retrieval_request(VALIDATION_NODE)
    penalty, reason = capability_domain_adjustment(request, HELIX_AGV_STATE_RUNBOOK)
    assert penalty <= PRIMARY_EXCLUSION_PENALTY
    assert "agv_state_inspection" in (reason or "")


def test_validation_node_low_score_helix_candidate_scores_below_relevance() -> None:
    match = _match(HELIX_AGV_STATE_RUNBOOK, raw_score=0.33)
    domain_penalty, _ = total_domain_penalty(VALIDATION_NODE, match, HELIX_AGV_STATE_RUNBOOK)
    boosted = boost_combined_score(
        match.combined_score,
        node=VALIDATION_NODE,
        node_text=build_retrieval_query_text(VALIDATION_NODE),
        match=match,
        runbook=HELIX_AGV_STATE_RUNBOOK,
        procedure_type_compatible=True,
        domain_penalty=domain_penalty,
    )
    assert boosted < 0.28  # below MIN_RETRIEVAL_FLOOR -> unresolved


# ---------------------------------------------------------------------------
# Boost protection: a heavily-penalized candidate with a very low raw score
# must remain suppressed regardless of bonuses (the exact 0.04 -> 0.76 bug).
# ---------------------------------------------------------------------------


def test_heavily_penalized_candidate_not_rescued_by_boosting() -> None:
    match = _match(OPC_TAG_FLOW_RUNBOOK, raw_score=0.0423)
    domain_penalty, _ = total_domain_penalty(GATEWAY_HEALTH_NODE, match, OPC_TAG_FLOW_RUNBOOK)
    boosted = boost_combined_score(
        match.combined_score,
        node=GATEWAY_HEALTH_NODE,
        node_text=build_retrieval_query_text(GATEWAY_HEALTH_NODE),
        match=match,
        runbook=OPC_TAG_FLOW_RUNBOOK,
        procedure_type_compatible=True,
        domain_penalty=domain_penalty,
    )
    assert boosted <= 0.05, "domain penalty must still suppress this candidate's score near zero"


def test_boost_cannot_lift_eligible_low_score_past_relevance() -> None:
    # Even for a domain-compatible candidate, raw 0.04 should not reach ~0.76
    # -- MAX_ADDITIVE_BOOST caps the total positive contribution.
    match = _match(GATEWAY_RESTART_RUNBOOK, raw_score=0.04)
    boosted = boost_combined_score(
        match.combined_score,
        node=RECOVERY_NODE,
        node_text=build_retrieval_query_text(RECOVERY_NODE),
        match=match,
        runbook=GATEWAY_RESTART_RUNBOOK,
        procedure_type_compatible=True,
    )
    assert boosted <= 0.04 + 0.20 + 1e-6


# ---------------------------------------------------------------------------
# Empty explicit metadata: a node with no explicit expects_capability must
# use derived capability metadata to penalize the wrong candidate, rather
# than letting a high raw score alone decide.
# ---------------------------------------------------------------------------


def test_empty_explicit_metadata_uses_derived_request_not_unrestricted_passage() -> None:
    # AGV_STATE_NODE (diagnostic_decision, "determine whether residual AGV
    # state requires correction") has no expects_capability / expects_surface
    # either -- the derived request must still penalize the unrelated OPC
    # tag-flow procedure enough that it loses selection despite a much higher
    # raw score. (A normal, not maximal, score gap is used -- see the
    # adversarial test above for how large a gap the penalty can overcome;
    # a sufficiently extreme raw-score gap can still win, by design, since
    # domain rules are score input, not an absolute veto.)
    assert AGV_STATE_NODE.get("expects_capability") in (None, [])
    assert AGV_STATE_NODE.get("expects_surface") in (None, [])
    matches = [
        _match(OPC_TAG_FLOW_RUNBOOK, raw_score=0.55),  # would win on raw score alone
        _match(HELIX_AGV_STATE_RUNBOOK, raw_score=0.45),
    ]
    runbooks_by_id = {
        OPC_TAG_FLOW_RUNBOOK["procedure_id"]: OPC_TAG_FLOW_RUNBOOK,
        HELIX_AGV_STATE_RUNBOOK["procedure_id"]: HELIX_AGV_STATE_RUNBOOK,
    }
    selected = select_runbook_matches(AGV_STATE_NODE, matches, runbooks_by_id=runbooks_by_id)
    assert selected, "expected at least one selected runbook"
    assert selected[0][0].procedure_id == HELIX_AGV_STATE_RUNBOOK["procedure_id"]


# ---------------------------------------------------------------------------
# Capability taxonomy: related concepts must not collapse into synonyms.
# ---------------------------------------------------------------------------


def test_opc_and_gateway_health_are_distinct_capabilities() -> None:
    caps = runbook_derived_capabilities(OPC_TAG_FLOW_RUNBOOK)
    assert "opc_tag_flow" in caps


def test_active_error_and_state_inspection_are_distinct_capabilities() -> None:
    state_caps = runbook_derived_capabilities(HELIX_AGV_STATE_RUNBOOK)
    error_caps = runbook_derived_capabilities(ACTIVE_AGV_ERROR_RUNBOOK)
    assert "agv_state_inspection" in state_caps
    assert "agv_active_error_inspection" not in state_caps
    assert "agv_active_error_inspection" in error_caps
    assert "agv_state_inspection" not in error_caps


# ---------------------------------------------------------------------------
# Surface-text parsing: compound "RMS/WCS/API"-style fields must yield every
# named surface, not just the first alias that happens to match as a whole
# phrase (case 228086 node_7 regression -- this previously collapsed to just
# {"rms_ui"} and hard-rejected every candidate on a false "surface does not
# match" gap).
# ---------------------------------------------------------------------------


def test_surface_ids_from_text_parses_slash_separated_surfaces() -> None:
    assert _surface_ids_from_text("Site confirmation + RMS/WCS/API corroboration") == {
        "rms_ui",
        "wcs_api",
    }


def test_surface_ids_from_text_parses_plus_separated_surfaces() -> None:
    assert _surface_ids_from_text("Event Viewer+Ignition Gateway") == {
        "event_viewer",
        "ignition_gateway",
    }


def test_validation_node_with_compound_surface_accepts_wcs_api_runbook() -> None:
    # VALIDATION_NODE's primary_surface is "Site confirmation + RMS/WCS/API
    # corroboration". A runbook that only offers the wcs_api surface must not
    # be hard-rejected merely because the compound surface string was parsed
    # down to rms_ui alone.
    node = {**VALIDATION_NODE, "primary_surface": "Site confirmation + RMS/WCS/API corroboration"}
    runbook = {
        **OPC_TAG_FLOW_RUNBOOK,
        "access_surface": ["wcs_api"],
    }
    gaps = runbook_exact_fit_gaps(node, runbook)
    assert not any("surface does not match" in gap.lower() for gap in gaps)


def test_surface_ids_from_text_maps_rms_wcs_api_to_full_canonical_set() -> None:
    # RMS/WCS/API must resolve to exactly the canonical surface ids it names.
    # "api" alone is not a registered alias (only "wcs api"/"wcs_api"/etc are),
    # so RMS/WCS/API correctly yields {rms_ui, wcs_api}, matching every real
    # compound-surface field observed in the corpus (e.g. node_5's "RMS
    # fleet/map (site) + WCS/SSMS robotics read-only evidence").
    assert _surface_ids_from_text("RMS/WCS/API") == {"rms_ui", "wcs_api"}
    assert _surface_ids_from_text("Evidence collection surfaces (event_viewer, ignition_gateway, wcs_api, rms_ui)") == {
        "event_viewer",
        "ignition_gateway",
        "wcs_api",
        "rms_ui",
    }


# ---------------------------------------------------------------------------
# OPC-COM tag-flow isolation: fixing the compound-surface parser must not
# let OPC-tag-flow leak onto validation or gateway-health nodes that never
# established tag-flow evidence. The domain-rule penalty, not the surface
# parser, is what must keep OPC-COM disfavored on these nodes.
# ---------------------------------------------------------------------------


def test_opc_tag_flow_penalized_on_validation_node_without_tag_evidence() -> None:
    # VALIDATION_NODE's intent never mentions tags/OPC/subscriptions -- only
    # service responsiveness, AGV status, and resumed operation. Even with a
    # compound multi-surface field, OPC-COM must carry a domain penalty here.
    # (validation_gate nodes discard agv_state_inspection/agv_active_error_inspection
    # rather than excluding opc_tag_flow specifically -- OPC-COM lands in the
    # milder "no required-capability overlap" vocabulary-gap tier here, not
    # the primary-exclusion tier, since it was never actively excluded.)
    node = {**VALIDATION_NODE, "primary_surface": "Site confirmation + RMS/WCS/API corroboration"}
    request = derive_retrieval_request(node)
    penalty, reason = capability_domain_adjustment(request, OPC_TAG_FLOW_RUNBOOK)
    assert penalty <= NO_REQUIRED_OVERLAP_PENALTY, (
        "OPC-COM tag-flow must be penalized without explicit tag-flow language in the node; "
        f"got penalty={penalty!r} reason={reason!r}"
    )
    assert penalty < 0.0


def test_opc_tag_flow_penalized_on_gateway_health_node_via_compound_surface() -> None:
    # Even if a gateway-health node's surface field were compound (e.g. it
    # also lists wcs_api), OPC-COM must stay penalized -- capability exclusion
    # governs the penalty, independent of how many surfaces the node accepts.
    node = {**GATEWAY_HEALTH_NODE, "primary_surface": "Ignition Gateway/WCS API"}
    request = derive_retrieval_request(node)
    penalty, reason = capability_domain_adjustment(request, OPC_TAG_FLOW_RUNBOOK)
    assert penalty <= PRIMARY_EXCLUSION_PENALTY
    assert "opc_tag_flow" in (reason or "")


# ---------------------------------------------------------------------------
# Validation-node scope discipline: accepting several surfaces must not by
# itself pull in an unrelated new diagnostic procedure. Surface compatibility
# is necessary but not sufficient to avoid a domain penalty.
# ---------------------------------------------------------------------------


def test_validation_node_penalizes_unrelated_diagnostic_despite_broad_surfaces() -> None:
    # A node that accepts RMS, WCS, and API surfaces broadly must still
    # penalize a procedure whose actual subject (OPC tag subscriptions) the
    # node's own text never raises -- multi-surface acceptance is not a
    # green light for arbitrary diagnostics that merely happen to expose one
    # of those surfaces.
    node = {
        "node_id": "node_broad_surface",
        "node_type": "validation_gate",
        "title": "Validate stable automated operation",
        "intent": "Confirm service responsiveness, AGV state, and resumed operation before declaring recovery complete.",
        "primary_surface": "RMS/WCS/API",
    }
    request = derive_retrieval_request(node)
    penalty, _ = capability_domain_adjustment(request, OPC_TAG_FLOW_RUNBOOK)
    assert penalty <= NO_REQUIRED_OVERLAP_PENALTY
    assert penalty < 0.0


# ---------------------------------------------------------------------------
# Penalty persistence: correcting the surface parser must not remove the
# domain penalty for a previously-penalized-for-non-surface-reasons
# candidate. Surface compatibility is one signal among several.
# ---------------------------------------------------------------------------


def test_penalized_candidate_stays_penalized_after_surface_parsing_fix() -> None:
    # HELIX_AGV_STATE_RUNBOOK is penalized for VALIDATION_NODE on capability
    # grounds (agv_state_inspection), not on surface grounds. Widening the
    # surface parser must not accidentally remove that penalty.
    node = {**VALIDATION_NODE, "primary_surface": "Site confirmation + RMS/WCS/API corroboration"}
    request = derive_retrieval_request(node)
    penalty, reason = capability_domain_adjustment(request, HELIX_AGV_STATE_RUNBOOK)
    assert penalty <= PRIMARY_EXCLUSION_PENALTY
    assert "agv_state_inspection" in (reason or "")


# ---------------------------------------------------------------------------
# Cross-case regression guard: the surface-normalization fix must not alter
# the *filtering* outcome for candidates in the other three cases that were
# already linked correctly. These mirror real pool records (see
# shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool) so a
# future change to _surface_ids_from_text can't silently start rejecting
# already-correct links elsewhere in the corpus.
# ---------------------------------------------------------------------------


HOSPITAL_HMI_INDUCT_RUNBOOK = _runbook(
    "proc_check_hospital_hmi_operations_menu_induct_extract_status_v1",
    "Check Hospital HMI operations menu induct/extract status",
    "Use the Hospital HMI operations menu to check tote induct/extract availability, AGV number, tote ID, and status messages.",
    "Use when Hospital HMI tote induct or extract status needs to be checked.",
)
HOSPITAL_HMI_INDUCT_RUNBOOK["access_surface"] = ["hospital_hmi"]

EVENT_VIEWER_RUNBOOK = _runbook(
    "proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1",
    "Windows Event Viewer / services OptiSweep-WCSWebApplication diagnostic",
    "Use Windows Event Viewer and Services to check the OptiSweep / WCSWebApplication service state and recent errors.",
    "Use when the OptiSweep / WCSWebApplication service state needs to be checked via Event Viewer / services.",
)
EVENT_VIEWER_RUNBOOK["access_surface"] = ["event_viewer"]


def test_hospital_hmi_node_still_accepts_hospital_hmi_runbook_after_fix() -> None:
    node = {
        "node_id": "node_hospital_induct",
        "node_type": "diagnostic_decision",
        "title": "Check Hospital HMI tote induct/extract status",
        "intent": "Confirm whether tote induct/extract is available on the Hospital HMI and inspect status messages.",
        "primary_surface": "Hospital HMI",
    }
    gaps = runbook_exact_fit_gaps(node, HOSPITAL_HMI_INDUCT_RUNBOOK)
    assert not any("surface does not match" in gap.lower() for gap in gaps)


def test_event_viewer_node_still_accepts_event_viewer_runbook_after_fix() -> None:
    node = {
        "node_id": "node_event_viewer",
        "node_type": "diagnostic_decision",
        "title": "Check Windows Event Viewer / services for OptiSweep-WCSWebApplication",
        "intent": "Confirm the OptiSweep / WCSWebApplication service state using Event Viewer and services.",
        "primary_surface": "Event Viewer",
    }
    gaps = runbook_exact_fit_gaps(node, EVENT_VIEWER_RUNBOOK)
    assert not any("surface does not match" in gap.lower() for gap in gaps)


# ---------------------------------------------------------------------------
# Case 228723 targeted regression: roster/mapping vs shutdown-queue-cycling
# vs remove/recover vs unrelated map-monitor micro-procedures. Both
# candidates below previously shared only the coarse "device_roster_state"
# tag with no fine-grained text distinction, so the wrong one could win on
# score alone with no eligibility gate to stop it. Under the softened
# scoring model, the same distinction must now survive as a score penalty
# large enough to lose under normal (not just extreme) score competition --
# this is the central regression guard for the whole soft-scoring migration.
# ---------------------------------------------------------------------------

ROSTER_MAPPING_NODE_228723 = {
    "node_id": "node_2",
    "node_type": "diagnostic_decision",
    "title": "Identify the abnormal or unmapped robot",
    "intent": (
        "Inspect the RMS fleet or robot status view for roster membership, mapping, "
        "location, and exception indicators associated with the affected workflow, and "
        "interpret whether the data supports a specific unmapped or abnormal robot."
    ),
}

RECOVERY_NODE_228723 = {
    "node_id": "node_3",
    "node_type": "procedure_reference",
    "title": "Use an authorized site-side robot isolation or removal path",
    "intent": (
        "If an abnormal roster or mapping condition is supported, use the approved site "
        "procedure to isolate or remove the affected robot from the operating system and "
        "place it in a safe non-operational state."
    ),
    "runbook_placeholder": (
        "Procedure needed for authorized site-side AGV physical isolation and system "
        "removal, including safety prerequisites, handling of a robot in an abnormal "
        "location, charger placement, and confirmation of the corresponding RMS state."
    ),
}

VALIDATION_NODE_228723 = {
    "node_id": "node_4",
    "node_type": "validation_gate",
    "title": "Validate pairing and routing recover",
    "intent": (
        "Ask the site to confirm the affected zone can obtain a pair, confirm replacement "
        "AMRs route to the intended workflow rather than hospital, recheck the affected "
        "robot/fleet state in RMS, and confirm any earlier L2 backend evidence no longer "
        "shows the inconsistent active state."
    ),
}

SHUTDOWN_QUEUE_RUNBOOK = _runbook(
    "proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1",
    "Check RMS fleet status for AGVs in shutdown queues and zone cycling",
    "Use when you need to confirm that AGVs are in the shutdown state (shutdown queues) "
    "and then transition into their assigned zones (4 zones) after startup, using the "
    "live fleet status view in RMS.",
    "When you need to confirm that AGVs are in the shutdown state and then transition "
    "into their assigned zones after startup.",
)
SHUTDOWN_QUEUE_RUNBOOK["capability_tags"] = ["device_roster_state"]
SHUTDOWN_QUEUE_RUNBOOK["access_surface"] = ["rms_ui"]

SELECTED_ROBOT_DETAILS_RUNBOOK = _runbook(
    "proc_check_selected_robot_details_robot_id_location_node_code_tote_v1",
    "Check Selected Robot Details (Robot ID, Location, Node Code/Cell Code, Tote ID) in Robot Selection Overview",
    "Use Robot Selection to inspect a specific robot ID, its location/node code, tote "
    "state, and status/color/error indicators to determine whether the robot appears "
    "missing, unmapped, or abnormal.",
    "When you need to inspect a specific robot selected in RMS for roster/mapping "
    "abnormalities.",
)
SELECTED_ROBOT_DETAILS_RUNBOOK["capability_tags"] = ["device_roster_state"]
SELECTED_ROBOT_DETAILS_RUNBOOK["access_surface"] = ["rms_ui"]

AGV_API_REMOVE_RECOVER_RUNBOOK = _runbook(
    "proc_use_agv_api_controls_remove_recover_pause_resume_v1",
    "Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs",
    "Use the AGV API Controls to remove a specific AGV from the system when it has an "
    "issue, later recover it after physical removal, and pause/resume all AGV movement.",
    "When an AGV needs to be removed from the system and later recovered after physical "
    "removal/recovery.",
    procedure_type="operation",
)
AGV_API_REMOVE_RECOVER_RUNBOOK["capability_tags"] = ["agv_physical_recovery", "agv_active_errors"]
AGV_API_REMOVE_RECOVER_RUNBOOK["access_surface"] = ["tipper_hmi"]

STATION_IDS_RUNBOOK = _runbook(
    "proc_display_station_ids_on_map_monitor_quick_select_v1",
    "Display Station IDs on the Map Using Map Monitor Quick Select",
    "Visually confirm station locations and their unique station IDs on the RMS Map "
    "Monitor map (stations are special locations distinct from cells) to support "
    "station-related identification/debugging.",
    "When you need to visually confirm station locations and IDs on the RMS map.",
)
STATION_IDS_RUNBOOK["capability_tags"] = ["device_roster_state"]
STATION_IDS_RUNBOOK["access_surface"] = ["rms_ui"]


def test_shutdown_queue_runbook_penalized_for_roster_mapping_node() -> None:
    request = derive_retrieval_request(ROSTER_MAPPING_NODE_228723)
    penalty, reason = capability_domain_adjustment(request, SHUTDOWN_QUEUE_RUNBOOK)
    assert penalty <= PRIMARY_EXCLUSION_PENALTY
    assert "shutdown_queue_transition" in (reason or "")


def test_selected_robot_details_no_penalty_for_roster_mapping_node() -> None:
    request = derive_retrieval_request(ROSTER_MAPPING_NODE_228723)
    penalty, _ = capability_domain_adjustment(request, SELECTED_ROBOT_DETAILS_RUNBOOK)
    assert penalty == 0.0


def test_agv_api_remove_recover_no_penalty_for_recovery_node() -> None:
    request = derive_retrieval_request(RECOVERY_NODE_228723)
    penalty, _ = capability_domain_adjustment(request, AGV_API_REMOVE_RECOVER_RUNBOOK)
    assert penalty == 0.0


def test_station_ids_runbook_penalized_for_validation_node() -> None:
    request = derive_retrieval_request(VALIDATION_NODE_228723)
    penalty, _ = capability_domain_adjustment(request, STATION_IDS_RUNBOOK)
    assert penalty < 0.0


def test_shutdown_queue_and_roster_mapping_are_distinct_capabilities() -> None:
    shutdown_caps = runbook_derived_capabilities(SHUTDOWN_QUEUE_RUNBOOK)
    roster_caps = runbook_derived_capabilities(SELECTED_ROBOT_DETAILS_RUNBOOK)
    assert "shutdown_queue_transition" in shutdown_caps
    assert "agv_roster_mapping_validation" not in shutdown_caps
    assert "agv_roster_mapping_validation" in roster_caps
    assert "shutdown_queue_transition" not in roster_caps


def test_bare_zone_word_alone_does_not_trigger_shutdown_queue_capability() -> None:
    # "zone" alone (e.g. "affected zone", "assigned zone") must not be
    # sufficient to classify text as shutdown-queue-transition -- only
    # explicit shutdown-queue/startup-lifecycle language should. Use a
    # roster/pairing node (real signal present, unlike a no-signal node)
    # so the exclusion has something to bite on.
    penalty, reason = capability_domain_adjustment(
        derive_retrieval_request(ROSTER_MAPPING_NODE_228723), SHUTDOWN_QUEUE_RUNBOOK
    )
    assert penalty <= PRIMARY_EXCLUSION_PENALTY
    assert "shutdown_queue_transition" in (reason or "")

    # Confirm the exclusion is earned by explicit shutdown-queue language,
    # not by "zone" alone: a runbook whose only zone-adjacent text has no
    # shutdown/startup-lifecycle wording must not classify as
    # shutdown_queue_transition in the first place.
    zone_only_runbook = _runbook(
        "proc_check_current_zone_configuration_get_zone_configuration_v1",
        "Check current zone configuration",
        "Use GetZoneConfiguration to review the zones an AGV is currently assigned to.",
        "When you need to confirm current zone assignment for an AGV.",
    )
    assert "shutdown_queue_transition" not in runbook_derived_capabilities(zone_only_runbook)


def test_roster_mapping_node_selects_correct_runbook_even_when_shutdown_queue_scores_higher() -> None:
    # THE central adversarial regression test: give the wrong-domain
    # shutdown-queue runbook a deliberately HIGHER raw semantic score than
    # the correct roster-mapping runbook. Under the old hard-gate
    # architecture this distinction was enforced by dropping the wrong
    # candidate outright; under the new soft-scoring architecture it must be
    # enforced by the -0.35 domain penalty reliably outweighing a realistic
    # score advantage. This proves the softened mechanism does not silently
    # reintroduce the case-228723 false-positive class of bug.
    runbooks_by_id = {
        SHUTDOWN_QUEUE_RUNBOOK["procedure_id"]: SHUTDOWN_QUEUE_RUNBOOK,
        SELECTED_ROBOT_DETAILS_RUNBOOK["procedure_id"]: SELECTED_ROBOT_DETAILS_RUNBOOK,
    }
    matches = [
        _match(SHUTDOWN_QUEUE_RUNBOOK, raw_score=0.75),  # deliberately higher raw score
        _match(SELECTED_ROBOT_DETAILS_RUNBOOK, raw_score=0.60),
    ]
    selected = select_runbook_matches(ROSTER_MAPPING_NODE_228723, matches, runbooks_by_id=runbooks_by_id)
    assert selected, "expected at least one selected runbook"
    assert selected[0][0].procedure_id == SELECTED_ROBOT_DETAILS_RUNBOOK["procedure_id"]


# ---------------------------------------------------------------------------
# Vocabulary-gap tolerance: a runbook with correct capability_tags but no
# fine-grained regex coverage (the SSMS-runbook-linking bug from this
# session) must only carry the mild NO_REQUIRED_OVERLAP_PENALTY, not be
# eliminated -- a strong semantic match should still clear the high/medium
# confidence threshold despite the penalty.
# ---------------------------------------------------------------------------


def test_vocabulary_gap_runbook_carries_mild_penalty_not_elimination() -> None:
    node = {
        "node_id": "node_wcs_system_fault",
        "node_type": "diagnostic_decision",
        "title": "Check WCS system fault state",
        "intent": "Confirm whether a WCS-level system fault is active beyond per-AGV errors.",
    }
    # capability_tags carries a real, correctly-assigned taxonomy capability
    # (wcs_system_faults) that has no corresponding entry in
    # capability_derivation.py's fine-grained CAPABILITIES vocabulary.
    runbook = _runbook(
        "proc_check_robotics_systemdatabasemodel_state_v1",
        "Check Robotics SystemDatabaseModel State in SSMS",
        "Use SSMS to inspect SystemDatabaseModel state for WCS system faults.",
    )
    runbook["capability_tags"] = ["wcs_system_faults"]
    runbook["access_surface"] = ["wcs_sql"]
    request = derive_retrieval_request(node)
    penalty, reason = evidence_domain_penalty(node, _match(runbook, raw_score=0.87), runbook)
    assert penalty >= NO_REQUIRED_OVERLAP_PENALTY - 1e-9, (
        f"vocabulary-gap penalty must stay mild (>= {NO_REQUIRED_OVERLAP_PENALTY}), got {penalty}"
    )
    boosted = boost_combined_score(
        0.87,
        node=node,
        node_text=build_retrieval_query_text(node),
        match=_match(runbook, raw_score=0.87),
        runbook=runbook,
        procedure_type_compatible=True,
        domain_penalty=penalty,
    )
    assert boosted >= 0.60, "a strong semantic match must survive a mild vocabulary-gap penalty"
