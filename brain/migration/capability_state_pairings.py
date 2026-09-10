"""Hand-judged state/symptom pairings for docs/ontology/catalogs/capability_catalog.json.

Every one of the 27 real (non-stub) capabilities was read individually —
its id, label, job, description, and when_to_use — and judged against the
Entity/Capability boundary locked in brain/AGENT_DESIGN_NOTES.md §2: an
Entity is a thing or a STATE of a thing that exists whether or not anyone
is checking it; a Capability is something a human does to diagnose/verify/
act on that state. This is not a mechanical transform (no keyword rule
produced this mapping) — each entry below is a individually-considered
judgment call, made while reading the actual catalog content, not derived
from the capability's slug/label text.

Finding: 25 of 27 are pure VERIFICATION capabilities (their job is "confirm
whether X is true"), and needed a paired state/symptom entity that mostly
did not exist. 2 are genuinely different in kind, not just naming:

- rms_soft_stop ("Pause/resume AGVs via RMS soft stop") CONTROLS a state
  rather than verifying it — it changes whether the fleet is paused.
- agv_physical_recovery ("Coordinate on-site AGV add/remove/bump recovery")
  is a recovery action that resolves a symptom, not a check of one.

Both were misclassified capability_kind=diagnostic before this pass (traced
to a keyword-matching function, CAPABILITY_KIND_BY_PREFIX in
migrate_ontology_catalogs.py, that only recognized "verify"/"check"/
"restart"/"recover"/"clear" as substrings of the SLUG — "rms_soft_stop"
and "agv_physical_recovery" matched none of those and silently fell
through to the DIAGNOSTIC default despite their own job fields already
describing a control/recovery action). See brain/AGENT_DESIGN_NOTES.md for
the full account of why this needed to be a judged pass, not a better
keyword list.

Each entry:
    "<capability_slug>": {
        "state_entity_type": EntityType — "state" or "symptom", judged per
            capability (a symptom is an anomaly/problem condition; a state
            is a neutral condition that can be healthy or not, e.g.
            "current zone pairing state" vs. "hospital diversion is
            occurring unexpectedly").
        "state_entity_name": the paired entity's name (a real noun phrase
            naming the condition, independent of the checking action).
        "new_capability_id_suffix": the capability's corrected, verb-first
            identity (id becomes "confirm_..."/"pause_or_resume_..." etc,
            replacing the old state-shaped slug).
        "new_capability_label": a human-readable action-shaped label to
            replace the old state-shaped one.
        "capability_kind": the corrected CapabilityKind.
        "relationship_type": VERIFIES for diagnostic capabilities, CONTROLS
            for capabilities that change the state rather than check it.
    }
"""

PAIRINGS = {
    "agv_active_errors": {
        "state_entity_type": "symptom",
        "state_entity_name": "AGV has an active error or fault",
        "new_capability_id_suffix": "confirm_agv_active_error_state",
        "new_capability_label": "Confirm AGV active error state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "device_roster_state": {
        "state_entity_type": "state",
        "state_entity_name": "Device roster, mapping, and fleet membership state",
        "new_capability_id_suffix": "confirm_device_roster_state",
        "new_capability_label": "Confirm device roster and mapping state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "fleet_system_status": {
        "state_entity_type": "state",
        "state_entity_name": "Overall fleet/system running-vs-down status",
        "new_capability_id_suffix": "confirm_fleet_system_status",
        "new_capability_label": "Confirm overall fleet/system status",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "sort_lifecycle_state": {
        "state_entity_type": "state",
        "state_entity_name": "Sort/system lifecycle state (running, starting, shutting down)",
        "new_capability_id_suffix": "confirm_sort_lifecycle_state",
        "new_capability_label": "Confirm sort lifecycle state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "hospital_diversion": {
        "state_entity_type": "symptom",
        "state_entity_name": "AGVs diverting to hospital unexpectedly",
        "new_capability_id_suffix": "confirm_hospital_diversion_path",
        "new_capability_label": "Confirm hospital diversion path",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "zone_pairing_state": {
        "state_entity_type": "state",
        "state_entity_name": "Zone pairing health state",
        "new_capability_id_suffix": "confirm_zone_pairing_state",
        "new_capability_label": "Confirm zone pairing state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "zone_config_state": {
        "state_entity_type": "state",
        "state_entity_name": "Zone configuration/staging state",
        "new_capability_id_suffix": "confirm_zone_configuration_state",
        "new_capability_label": "Confirm zone configuration state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "tipper_station_fault": {
        "state_entity_type": "symptom",
        "state_entity_name": "Tipper station fault",
        "new_capability_id_suffix": "confirm_tipper_station_fault",
        "new_capability_label": "Confirm tipper station fault",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "e_stop_or_safety_stop": {
        "state_entity_type": "state",
        "state_entity_name": "Physical E-stop / safety stop active state",
        "new_capability_id_suffix": "confirm_e_stop_or_safety_stop_state",
        "new_capability_label": "Confirm E-stop / safety stop state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "rms_soft_stop": {
        "state_entity_type": "state",
        "state_entity_name": "AGV fleet pause (soft stop) state",
        "new_capability_id_suffix": "pause_or_resume_agv_fleet",
        "new_capability_label": "Pause or resume AGV fleet (RMS soft stop)",
        "capability_kind": "operation",
        "relationship_type": "controls",
    },
    "gateway_health": {
        "state_entity_type": "state",
        "state_entity_name": "Ignition gateway health state",
        "new_capability_id_suffix": "confirm_ignition_gateway_health",
        "new_capability_label": "Confirm Ignition gateway health",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "wcs_service_health": {
        "state_entity_type": "state",
        "state_entity_name": "WCS/OptiSweep Windows service health state",
        "new_capability_id_suffix": "confirm_wcs_service_health",
        "new_capability_label": "Confirm WCS service health",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "wcs_api_responsiveness": {
        "state_entity_type": "state",
        "state_entity_name": "WCS/OptiSweep API responsiveness state",
        "new_capability_id_suffix": "confirm_wcs_api_responsiveness",
        "new_capability_label": "Confirm WCS API responsiveness",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "windows_service_or_event_log": {
        "state_entity_type": "state",
        "state_entity_name": "Windows service/event-log evidence of a host fault",
        "new_capability_id_suffix": "confirm_windows_service_and_event_log_evidence",
        "new_capability_label": "Confirm Windows service and event log evidence",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "agv_physical_recovery": {
        "state_entity_type": "symptom",
        "state_entity_name": "AGV stuck, bump-faulted, or otherwise needing physical recovery",
        "new_capability_id_suffix": "recover_agv_physically",
        "new_capability_label": "Recover AGV physically (add/remove/bump)",
        "capability_kind": "recovery",
        "relationship_type": "controls",
    },
    "robot_dwell_or_shutdown_staging": {
        "state_entity_type": "state",
        "state_entity_name": "Robot dwell / shutdown staging queue state",
        "new_capability_id_suffix": "confirm_robot_dwell_or_shutdown_staging_state",
        "new_capability_label": "Confirm robot dwell or shutdown staging state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "agv_charging_state": {
        "state_entity_type": "state",
        "state_entity_name": "AGV charging state",
        "new_capability_id_suffix": "confirm_agv_charging_state",
        "new_capability_label": "Confirm AGV charging state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "sorter_item_or_scan_state": {
        "state_entity_type": "state",
        "state_entity_name": "Sorter item/scan path state",
        "new_capability_id_suffix": "confirm_sorter_item_or_scan_state",
        "new_capability_label": "Confirm sorter item or scan state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "tote_exchange_sequence": {
        "state_entity_type": "state",
        "state_entity_name": "Tote exchange sequence state",
        "new_capability_id_suffix": "confirm_tote_exchange_sequence_state",
        "new_capability_label": "Confirm tote exchange sequence state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "bag_out_or_closeout_state": {
        "state_entity_type": "state",
        "state_entity_name": "Bag-out / closeout state",
        "new_capability_id_suffix": "confirm_bag_out_or_closeout_state",
        "new_capability_label": "Confirm bag-out or closeout state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "robot_command_or_task_state": {
        "state_entity_type": "state",
        "state_entity_name": "Robot command/task lifecycle state",
        "new_capability_id_suffix": "confirm_robot_command_or_task_state",
        "new_capability_label": "Confirm robot command or task state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "wcs_system_faults": {
        "state_entity_type": "symptom",
        "state_entity_name": "WCS/system-level active fault",
        "new_capability_id_suffix": "confirm_wcs_system_faults",
        "new_capability_label": "Confirm WCS system faults",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "lane_or_chute_state": {
        "state_entity_type": "state",
        "state_entity_name": "Lane/chute open-closed or bypass state",
        "new_capability_id_suffix": "confirm_lane_or_chute_state",
        "new_capability_label": "Confirm lane or chute state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "tote_lifecycle_state": {
        "state_entity_type": "state",
        "state_entity_name": "Tote lifecycle / inventory state",
        "new_capability_id_suffix": "confirm_tote_lifecycle_state",
        "new_capability_label": "Confirm tote lifecycle state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "ups_chat_or_stunnel_health": {
        "state_entity_type": "state",
        "state_entity_name": "UPS Chat / Stunnel message path health",
        "new_capability_id_suffix": "confirm_ups_chat_or_stunnel_health",
        "new_capability_label": "Confirm UPS Chat or Stunnel health",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "opc_connection_or_tipper_heartbeat": {
        "state_entity_type": "state",
        "state_entity_name": "Ignition OPC connection / tipper heartbeat state",
        "new_capability_id_suffix": "confirm_opc_connection_and_tipper_heartbeat",
        "new_capability_label": "Confirm OPC connection and tipper heartbeat",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "robot_location_state": {
        "state_entity_type": "state",
        "state_entity_name": "Robot/AGV current and destination location",
        "new_capability_id_suffix": "confirm_robot_location_state",
        "new_capability_label": "Confirm robot location state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
    "tote_association_state": {
        "state_entity_type": "state",
        "state_entity_name": "Tote-robot association (pairing) state",
        "new_capability_id_suffix": "confirm_tote_robot_association_state",
        "new_capability_label": "Confirm tote-robot association state",
        "capability_kind": "verification",
        "relationship_type": "verifies",
    },
}


# Found during the §6.12 sample-based re-judge pass, a separate case from
# PAIRINGS above: 3 capability slugs (optisweep_service_restart,
# ignition_restart, rms_map_reposition) are never independently defined in
# capability_catalog.json — they exist ONLY as bare id-strings inside other
# capabilities' support_contract.forbidden_capability_ids, so Pass 0
# auto-creates a minimal stub for each (see migrate_ontology_catalogs.py's
# "referenced_only" stub creation) with no description/when_to_use/job
# content to judge a state/symptom pairing from. Unlike PAIRINGS, these
# don't need re-identifying — "restart"/"reposition" already read as
# actions, not states, so their id/label are fine as they are. The only
# real defect is capability_kind: _capability_kind_for() (the same
# CAPABILITY_KIND_BY_PREFIX keyword bug documented in PAIRINGS' own
# docstring above) checks the slug for "restart"/"recover"/"clear"/
# "verify"/"check"/"query" substrings only. "restart" matches for the first
# two (correctly landing on RECOVERY by coincidence), but "reposition"
# matches nothing and silently defaulted to DIAGNOSTIC — wrong:
# repositioning something on a map is a control action, not a diagnostic
# check. Judged fix below; the other two are left alone since RECOVERY is
# already correct for them (documented here anyway so the stub-kind
# question doesn't need re-deriving next time someone looks).
STUB_CAPABILITY_KIND_FIXES: dict[str, str] = {
    "rms_map_reposition": "operation",
}
