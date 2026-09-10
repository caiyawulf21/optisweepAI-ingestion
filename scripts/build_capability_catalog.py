"""Build docs/ontology/catalogs/capability_catalog.json from adjacency + SQL/API catalogs."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TAX = REPO / "docs/ontology/taxonomy/runbook_capability_taxonomy.json"
SQL = REPO / "docs/ontology/catalogs/wcs_sql_catalog.json"
API = REPO / "docs/ontology/catalogs/wcs_api_catalog.json"
CROSS = REPO / "docs/ontology/catalogs/cross_links.json"
OUT = REPO / "docs/ontology/catalogs/capability_catalog.json"

SUPPORT_CONTRACTS: dict[str, dict] = {
    "wcs_service_health": {
        "diagnostic_surfaces": ["wcs_sql", "event_viewer", "ignition_gateway", "wcs_api"],
        "control_surfaces": ["windows_services", "ignition_gateway", "wcs_api"],
        "required_evidence": [
            "windows_service_or_event_log",
            "wcs_api_responsiveness",
        ],
        "forbidden_capabilities": [
            "agv_physical_recovery",
            "tote_lifecycle_state",
            "rms_map_reposition",
        ],
        "availability_rules": {
            "wcs_sql": "available_when_site_has_rms_aveva_hmi_or_other_wcs_backed_interface",
            "vpn_exception": "vpn_or_connectivity_unavailable",
            "service_down": "prefer_ignition_host_service_event_log_api_and_sql_when_site_ui_is_unavailable",
        },
    },
    "windows_service_or_event_log": {
        "diagnostic_surfaces": ["wcs_sql", "event_viewer", "windows_services"],
        "control_surfaces": ["windows_services"],
        "required_evidence": ["windows_service_or_event_log"],
        "forbidden_capabilities": ["agv_physical_recovery", "tote_lifecycle_state"],
    },
    "gateway_health": {
        "diagnostic_surfaces": ["wcs_sql", "ignition_gateway", "event_viewer", "wcs_api"],
        "control_surfaces": ["ignition_gateway"],
        "required_evidence": ["gateway_health"],
        "forbidden_capabilities": ["agv_physical_recovery", "tote_lifecycle_state"],
    },
    "wcs_api_responsiveness": {
        "diagnostic_surfaces": ["wcs_sql", "wcs_api", "event_viewer"],
        "control_surfaces": ["wcs_api"],
        "required_evidence": ["wcs_api_responsiveness"],
        "forbidden_capabilities": ["agv_physical_recovery", "tote_lifecycle_state"],
    },
    "device_roster_state": {
        "diagnostic_surfaces": ["wcs_sql", "wcs_api", "rms_ui"],
        "control_surfaces": ["aveva_hmi", "wcs_api", "approved_system_hmi"],
        "required_evidence": ["device_roster_state", "robot_location_state"],
        "forbidden_capabilities": ["optisweep_service_restart", "ignition_restart"],
        "backend_mappings": [
            {
                "operational_concept": "robot_location_state",
                "site_ui_sources": ["rms_ui", "aveva_hmi", "hospital_hmi"],
                "support_read_sources": [
                    {
                        "surface": "wcs_sql",
                        "database": "robotics",
                        "model": "RobotDatabaseModel",
                        "fields": ["State", "CurrentLocationId", "DestinationLocationId"],
                    },
                    {
                        "surface": "wcs_sql",
                        "database": "robotics",
                        "model": "RobotLocationDatabaseModel",
                        "fields": ["StationNumber"],
                    },
                ],
                "correlation_keys": ["robot_id", "location_id"],
                "freshness_field": "EntityLastUpdate",
                "preferred_support_surface": "wcs_sql",
                "approved_control_surfaces": ["aveva_hmi", "wcs_api", "approved_system_hmi"],
            }
        ],
    },
    "tote_lifecycle_state": {
        "diagnostic_surfaces": ["wcs_sql", "wcs_api"],
        "control_surfaces": ["aveva_hmi", "wcs_api", "approved_system_hmi"],
        "required_evidence": ["tote_association_state"],
        "forbidden_capabilities": ["optisweep_service_restart", "ignition_restart"],
        "backend_mappings": [
            {
                "operational_concept": "tote_robot_association",
                "site_ui_sources": ["aveva_hmi", "hospital_hmi", "rms_ui"],
                "support_read_sources": [
                    {
                        "surface": "wcs_sql",
                        "database": "robotics",
                        "model": "RobotDatabaseModel",
                        "fields": ["ToteName", "CurrentLocationId", "DestinationLocationId"],
                    },
                    {
                        "surface": "wcs_sql",
                        "database": "robotics",
                        "model": "RobotToteDatabseModel",
                        "fields": ["ToteId", "RobotId"],
                    },
                ],
                "correlation_keys": ["robot_id", "tote_id"],
                "freshness_field": "EntityLastUpdate",
                "preferred_support_surface": "wcs_sql",
                "approved_control_surfaces": ["aveva_hmi", "wcs_api", "approved_system_hmi"],
            }
        ],
    },
    "robot_command_or_task_state": {
        "diagnostic_surfaces": ["wcs_sql", "wcs_api"],
        "control_surfaces": ["wcs_api", "approved_system_hmi"],
        "required_evidence": ["robot_command_or_task_state"],
        "forbidden_capabilities": ["optisweep_service_restart", "ignition_restart"],
    },
    "hospital_diversion": {
        "diagnostic_surfaces": ["wcs_sql", "wcs_api", "hospital_hmi"],
        "control_surfaces": ["hospital_hmi", "aveva_hmi", "wcs_api"],
        "required_evidence": ["hospital_diversion"],
    },
}

# Full enrichment for every taxonomy capability (Stage 6 mini-RAG cards).
ENRICH: dict[str, dict] = {
    "agv_active_errors": {
        "job": "Confirm whether AGVs/robots currently have active error or fault state.",
        "when_to_use": "Site reports AGV stopped, alarms, bump, path lost, or software showing robot faults; corroborate RMS overview vs WCS truth.",
        "not_for": "Physical bump recovery steps (use agv_physical_recovery); Ignition OPC alone; tote NoRead.",
        "primary_access_surfaces": ["rms_ui", "wcs_sql", "wcs_api"],
        "secondary_access_surfaces": ["site_interview", "apidog"],
        "primary_databases": ["robotics"],
        "secondary_databases": ["sorter_sweeper"],
        "primary_models": [
            "AgvActiveErrorDatabaseModel",
            "SystemActiveErrorModel",
            "AGVErrorActivityDatabaseModel",
            "AgvErrorModel",
        ],
        "api_checks": ["GetAGVStatuses", "GetAGVFaultStats"],
        "activities": [
            {
                "id": "rms_overview_agv_status",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "Open RMS overview / AGV status; note alarms present vs clear vs blank UI.",
            },
            {
                "id": "ssms_robotics_active_agv_error",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS Helix/Robotics: AgvActiveError / SystemActiveError (+ activity history).",
            },
            {
                "id": "apidog_get_agv_statuses",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "GetAGVStatuses (and GetAGVFaultStats if needed) via Apidog.",
            },
        ],
        "observables": {
            "healthy": [
                "RMS AGV overview shows no active alarms for the robots in question",
                "AgvActiveError / SystemActiveError rows empty or cleared",
                "GetAGVStatuses shows robots not in active error",
            ],
            "degraded": [
                "RMS shows AGV alarms / fault codes",
                "Active error rows with ErrorCode / SystemErrorDescription",
                "API status reports faulted or blocked AGVs",
            ],
            "escalate": [
                "RMS blank while site running — check wcs_service_health",
                "RMS vs SQL/API conflict — deepen L2/L3, consider L4",
            ],
        },
        "role_paths": {
            "operator": "Primary RMS overview / AGV status on site; report floor symptoms; no SSMS",
            "L1_support": "Remote RMS overview + optional site_interview; not SSMS how-to",
            "L2_support": "Deeper RMS + Robotics active-error models + GetAGVStatuses",
            "L3_support": "Same as L2; own resolve/RCA when persistent",
        },
    },
    "device_roster_state": {
        "job": "Confirm robot roster, mapping, locations, cell codes, or abnormal fleet membership.",
        "when_to_use": "Robots missing on map, wrong zone, mapping abnormal, roster vs floor mismatch.",
        "not_for": "Active error code triage alone (agv_active_errors); physical remove without system-side steps.",
        "primary_access_surfaces": ["rms_ui", "wcs_sql", "wcs_api"],
        "secondary_access_surfaces": ["site_interview", "physical_floor", "apidog"],
        "primary_databases": ["robotics"],
        "secondary_databases": ["geek_agv", "sorter_sweeper"],
        "primary_models": [
            "RobotDatabaseModel",
            "RobotLocationDatabaseModel",
            "CellCodeDatabaseModel",
            "LatticeCodeModel",
            "AgvStatusModel",
        ],
        "api_checks": ["GetAGVStatuses", "RecoverAGV", "RemoveAgv"],
        "activities": [
            {
                "id": "rms_map_monitor",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "RMS roster/map monitor; ask site if robots missing visually.",
            },
            {
                "id": "ssms_robot_location_cellcode",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS Robotics Robot / RobotLocation / CellCode; GeekAgv LatticeCode if mapping.",
            },
            {
                "id": "api_recover_remove_agv",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "RecoverAGV / RemoveAgv when system-side roster repair is required.",
            },
        ],
        "observables": {
            "healthy": [
                "Roster matches expected robots on RMS",
                "RobotLocation Occupied/Zone/LocationType coherent",
                "Cell/lattice codes match mapped fleet",
            ],
            "degraded": [
                "Robot missing on map or disconnected",
                "Zone / LocationType mismatch",
                "CellCode or LatticeCode abnormal",
            ],
            "escalate": ["Cannot reconcile roster vs floor after RMS+DB+API"],
        },
        "role_paths": {
            "operator": "Primary RMS roster/map on site; confirm visual presence / missing robots",
            "L1_support": "Remote RMS roster/map + site visual confirm",
            "L2_support": "Robot/RobotLocation/CellCode + Recover/Remove APIs",
            "L3_support": "Same as L2 for persistent mapping issues",
        },
    },
    "fleet_system_status": {
        "job": "Confirm overall fleet / system-down vs running from overview surfaces.",
        "when_to_use": "Blank RMS, site-wide stoppage report, overall system page down.",
        "not_for": "Single-AGV active error deep dive without overall context.",
        "primary_access_surfaces": ["rms_ui", "aveva_hmi"],
        "secondary_access_surfaces": ["event_viewer", "wcs_sql", "site_interview"],
        "primary_databases": ["robotics", "sorter_sweeper"],
        "secondary_databases": [],
        "primary_models": ["SystemDatabaseModel", "SystemStateModel", "SortModel"],
        "api_checks": ["SystemState"],
        "activities": [
            {
                "id": "rms_overall_system",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "Check RMS overall / fleet overview blank or down.",
            },
            {
                "id": "aveva_overall_system",
                "access_surface": "aveva_hmi",
                "role": "operator",
                "action": "Aveva Overall System page if site can view; FORTNA may coach only.",
            },
            {
                "id": "ssms_system_state",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS SystemDatabaseModel / SystemStateModel; corroborate Event Viewer services.",
            },
        ],
        "observables": {
            "healthy": ["Overview shows system running", "SystemState consistent with running sort"],
            "degraded": ["RMS/Aveva blank or system-down indicators", "SystemState shows stopped/faulted"],
            "escalate": ["Unplanned restart — wcs_service_health / Ignition / Stunnel host trio"],
        },
        "role_paths": {
            "operator": "Primary RMS / Aveva overall on site when reachable",
            "L1_support": "Remote RMS overview + site report",
            "L2_support": "Services + SystemState / system DB + deeper RMS",
        },
    },
    "sort_lifecycle_state": {
        "job": "Confirm sort / system lifecycle: running, starting, shutting down, SortGuid continuity.",
        "when_to_use": "Site unsure if sort is running vs shutting down; lifecycle stuck between states.",
        "not_for": "Bag-out stuck alone (bag_out_or_closeout_state); single AGV fault.",
        "primary_access_surfaces": ["wcs_sql", "wcs_api", "rms_ui"],
        "secondary_access_surfaces": ["aveva_hmi", "apidog", "site_interview"],
        "primary_databases": ["robotics", "sorter_sweeper"],
        "secondary_databases": [],
        "primary_models": ["SystemDatabaseModel", "SystemStateModel", "SortModel"],
        "api_checks": ["SystemState", "SystemStartup", "SystemShutdown", "ResetMetrics"],
        "activities": [
            {
                "id": "ask_sort_running",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Ask site/RMS whether system is running vs shutting down.",
            },
            {
                "id": "ssms_sort_lifecycle",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS SystemDatabaseModel / SystemStateModel / SortModel (SortGuid).",
            },
            {
                "id": "api_system_state",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "SystemState (and Startup/Shutdown only when playbook authorizes).",
            },
        ],
        "observables": {
            "healthy": ["Lifecycle matches expected running/idle", "SortGuid stable for active sort"],
            "degraded": ["Stuck between start/shutdown", "SortGuid missing or inconsistent"],
            "escalate": ["Cannot advance lifecycle after documented SystemState checks"],
        },
        "role_paths": {
            "L1_support": "Ask site + RMS high-level running vs shutdown",
            "L2_support": "SSMS + SystemState APIs",
            "L3_support": "Authorize startup/shutdown mutations per playbook",
            "operator": "Report floor state / Aveva if available",
        },
    },
    "hospital_diversion": {
        "job": "Confirm hospital diversion path: lanes, stacklight, hospital tags/locations, AGV routing to hospital.",
        "when_to_use": "Hospital diversion active or suspected; stacklight/lane alarms; robots diverting unexpectedly.",
        "not_for": "Generic tipper fault without hospital context.",
        "primary_access_surfaces": ["rms_ui", "hospital_hmi", "wcs_sql"],
        "secondary_access_surfaces": ["site_interview", "building_acb_hmi"],
        "primary_databases": ["robotics", "sorter_sweeper"],
        "secondary_databases": [],
        "primary_models": [
            "HospitalDatabaseModel",
            "HosptialSorterSideDatabaseModel",
            "HospitalTagsModel",
            "LocationModel",
            "CellCodeDatabaseModel",
            "AgvStatusModel",
        ],
        "api_checks": [],
        "activities": [
            {
                "id": "rms_hospital_routing",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "RMS fleet routing toward hospital; ask stacklight color.",
            },
            {
                "id": "hospital_hmi_lane",
                "access_surface": "hospital_hmi",
                "role": "operator",
                "action": "Hospital HMI / lane UI / stacklight; FORTNA coaches or views if remote.",
            },
            {
                "id": "ssms_hospital_models",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS Hospital* / HospitalTags / Location / CellCode for diversion state.",
            },
        ],
        "observables": {
            "healthy": ["No unexpected hospital diversion", "Hospital tags/lanes idle as expected"],
            "degraded": ["Stacklight divert color", "Hospital tags/locations active", "AGVs routed to hospital"],
            "escalate": ["Diversion persists after lane/HMI+DB corroboration"],
        },
        "role_paths": {
            "L1_support": "RMS + site stacklight/lane report",
            "L2_support": "Hospital HMI remote + SSMS hospital models",
            "operator": "Hospital HMI / stacklight primary on floor",
        },
    },
    "zone_pairing_state": {
        "job": "Confirm zone pairing health (pair fail / unable to get a pair).",
        "when_to_use": "Pairing failure symptoms on RMS or site report of zone pair issues.",
        "not_for": "Zone config mutation (zone_config_state); tote exchange pairing.",
        "primary_access_surfaces": ["rms_ui", "site_interview"],
        "secondary_access_surfaces": ["wcs_sql", "aveva_hmi"],
        "primary_databases": [],
        "secondary_databases": ["robotics"],
        "primary_models": [],
        "api_checks": [],
        "activities": [
            {
                "id": "rms_pairing_symptoms",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "RMS pairing symptoms; ask site what they see on zone/pair UI.",
            },
            {
                "id": "deeper_rms_pair",
                "access_surface": "rms_ui",
                "role": "L2_support",
                "action": "Deeper RMS pairing views; related DB only if source-backed rows exist.",
            },
        ],
        "observables": {
            "healthy": ["Zones paired as expected", "No pair-fail alarms"],
            "degraded": ["Unable to get a pair", "Pairing failure alarms"],
            "escalate": ["Persistent pair fail after RMS deep dive — L3/L4"],
        },
        "role_paths": {
            "L1_support": "RMS symptoms + site_interview",
            "L2_support": "Deeper RMS / related DB if present",
            "operator": "Report zone/pair UI symptoms",
        },
        "gaps": ["Thin SQL model mapping for pairing — expand when Day1/OM evidence lands"],
    },
    "zone_config_state": {
        "job": "Confirm zone configuration / staging via Aveva overview and GetZoneConfig.",
        "when_to_use": "Zone config mismatch, staging wrong zone settings, need read of zone config.",
        "not_for": "UpdateZoneConfig mutate unless playbook explicitly authorizes (slides: rarely customer-used).",
        "primary_access_surfaces": ["aveva_hmi", "wcs_api", "apidog"],
        "secondary_access_surfaces": ["wcs_sql", "rms_ui"],
        "primary_databases": [],
        "secondary_databases": [],
        "primary_models": [],
        "api_checks": ["GetZoneConfig", "UpdateZoneConfig"],
        "activities": [
            {
                "id": "aveva_zone_config",
                "access_surface": "aveva_hmi",
                "role": "operator",
                "action": "Aveva Zone Config overview if available on site.",
            },
            {
                "id": "apidog_get_zone_config",
                "access_surface": "apidog",
                "role": "L2_support",
                "action": "GetZoneConfig via Apidog; treat UpdateZoneConfig as high-risk mutate.",
            },
        ],
        "observables": {
            "healthy": ["Zone config matches expected staging", "GetZoneConfig returns expected payload"],
            "degraded": ["Zone config mismatch", "Staging not applied"],
            "escalate": ["Need UpdateZoneConfig beyond playbook — SME/L4"],
        },
        "role_paths": {
            "L1_support": "Coach Aveva overview if reachable; else escalate",
            "L2_support": "GetZoneConfig primary; mutate only if authorized",
            "operator": "Aveva Zone Config primary on floor",
        },
    },
    "tipper_station_fault": {
        "job": "Confirm tipper station faults via WebVisu/VISU screens and tipper/tag/bits models.",
        "when_to_use": "Tipper alarms, pneumatic/feedrate faults, station not releasing, need VISU_ALARM / IO diag.",
        "not_for": "OPC connection faulted alone (opc_connection_or_tipper_heartbeat); Aveva pages; LOTO without capability intent.",
        "primary_access_surfaces": ["tipper_hmi", "wcs_sql"],
        "secondary_access_surfaces": ["site_interview", "ignition_gateway"],
        "primary_databases": ["robotics", "sorter_sweeper"],
        "secondary_databases": ["opc_comms"],
        "primary_models": [
            "TipperStationDatabaseModel",
            "TipperDatabaseModel",
            "TipperStationModel",
            "TipperModel",
            "BitsModel",
            "TagModel",
            "TipperDepartureActivityModel",
        ],
        "api_checks": [],
        "activities": [
            {
                "id": "visu_read_alarm",
                "access_surface": "tipper_hmi",
                "role": "operator",
                "action": "VISU_ALARM — read active tipper alarms + SHOW HISTORY (last 1500); FORTNA asks text/photo if not remote.",
            },
            {
                "id": "visu_data_banner",
                "access_surface": "tipper_hmi",
                "role": "L1_support",
                "action": "VISU_DATA banner / station data, or coach site for alarm text/color/photo.",
            },
            {
                "id": "visu_io_diag_troubleshoot",
                "access_surface": "tipper_hmi",
                "role": "L2_support",
                "action": "VISU_IO_DIAG read-only IO + VISU_MCP_DUAL fault reset as appropriate.",
            },
            {
                "id": "ssms_tipper_bits_tags",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS Tipper* models + Tag/Bits; guide LOTO only when physical work required (operator executes).",
            },
        ],
        "observables": {
            "healthy": ["No tipper alarms on VISU_ALARM", "Bits/tags show healthy station state", "MCP controls normal"],
            "degraded": ["VISU alarm text/timestamp", "IO diag mismatch", "Tipper fault bits set", "Departure activity stuck"],
            "escalate": ["Needs LOTO / mechanical — operator + L2 coach; safety SME if unclear"],
        },
        "role_paths": {
            "operator": "Primary VISU user (MCP/DATA/ALARM/IO); physical tipper actions",
            "L1_support": "Remote VISU if available else ask alarm text/photo — not SSMS how-to",
            "L2_support": "VISU_IO_DIAG / alarm history + SSMS tipper/tag/bits",
            "L3_support": "Persistent tipper + VISU_MDS axis params per OM",
        },
    },
    "e_stop_or_safety_stop": {
        "job": "Confirm physical E-stop / safety stop state and coordinate on-site reset.",
        "when_to_use": "Emergency stop depressed, safety circuit, master E-stop clear prep.",
        "not_for": "RMS soft stop / PauseAGVs (rms_soft_stop).",
        "primary_access_surfaces": ["physical_floor", "site_interview", "rms_ui"],
        "secondary_access_surfaces": ["wcs_sql", "aveva_hmi"],
        "primary_databases": ["sorter_sweeper"],
        "secondary_databases": [],
        "primary_models": ["EstopModel"],
        "api_checks": [],
        "activities": [
            {
                "id": "ask_physical_estop",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Ask site if any E-stop depressed; note remote cues on RMS map.",
            },
            {
                "id": "rms_before_master_estop_clear",
                "access_surface": "rms_ui",
                "role": "L2_support",
                "action": "Confirm robotControl loads before master E-stop clear coaching.",
            },
            {
                "id": "ssms_estop_model",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "EstopModel + HMI corroboration; operator performs physical reset only.",
            },
        ],
        "observables": {
            "healthy": ["No E-stop depressed; safety clear", "EstopModel clear"],
            "degraded": ["E-stop active", "Map emergency stop trigger", "EstopModel set"],
            "escalate": ["Safety uncertainty — do not clear remotely"],
        },
        "role_paths": {
            "operator": "Only role that performs physical E-stop reset",
            "L1_support": "Ask/confirm; never perform E-stop",
            "L2_support": "Remote status + coach operator; never perform E-stop",
            "L3_support": "Same hard rule — no remote E-stop",
        },
    },
    "rms_soft_stop": {
        "job": "Pause/resume AGVs via RMS soft stop (not physical E-stop).",
        "when_to_use": "Need fleet pause without E-stop.",
        "not_for": "Physical E-stop; L1 mutate.",
        "primary_access_surfaces": ["rms_ui", "wcs_api", "apidog"],
        "secondary_access_surfaces": [],
        "primary_databases": [],
        "secondary_databases": [],
        "primary_models": [],
        "api_checks": ["PauseAGVs", "ResumeAGVs"],
        "activities": [
            {
                "id": "rms_pause_agvs",
                "access_surface": "rms_ui",
                "role": "L2_support",
                "action": "RMS pause UI — L2/L3 only.",
            },
            {
                "id": "api_pause_resume_agvs",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "PauseAGVs / ResumeAGVs via Apidog when authorized.",
            },
        ],
        "observables": {
            "healthy": ["AGVs paused or resumed as intended"],
            "degraded": ["Pause/resume not taking effect"],
            "escalate": ["Confused with E-stop — stop and clarify capability"],
        },
        "role_paths": {
            "L1_support": "No access to soft-stop mutate",
            "L2_support": "Pause/Resume only",
            "L3_support": "Pause/Resume + resolve if stuck",
            "operator": "Use physical E-stop path if safety requires",
        },
    },
    "gateway_health": {
        "job": "Confirm Ignition gateway health / role in the host stack.",
        "when_to_use": "Suspect Ignition down, performance issues, or unplanned restart host path.",
        "not_for": "Tipper alarm text alone without gateway/OPC context.",
        "primary_access_surfaces": ["ignition_gateway"],
        "secondary_access_surfaces": ["event_viewer", "wcs_api", "site_interview"],
        "primary_databases": [],
        "secondary_databases": [],
        "primary_models": [],
        "api_checks": [],
        "activities": [
            {
                "id": "identify_ignition_role",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Identify Ignition role / symptoms only; do not admin-recover as L1 how-to.",
            },
            {
                "id": "gateway_performance",
                "access_surface": "ignition_gateway",
                "role": "L2_support",
                "action": "Ignition Gateway performance UI + connectivity; host restart path with OptiSweep/Stunnel.",
            },
        ],
        "observables": {
            "healthy": ["Gateway up; performance acceptable"],
            "degraded": ["Gateway slow/unreachable", "Related Aveva/tag feed unhealthy"],
            "escalate": ["Product defect → L4"],
        },
        "role_paths": {
            "L1_support": "Identify role / symptoms only",
            "L2_support": "Gateway UI + restart path with host trio",
            "L3_support": "Own recovery; escalate L4 if product defect",
            "operator": "Report site symptoms; no Ignition admin",
        },
    },
    "wcs_service_health": {
        "job": "Confirm OptiSweep / WCS Windows service health and related host recovery signals.",
        "when_to_use": "Blank RMS, service crash, unplanned restart, need OptiSweep service + SQL Agent checks.",
        "not_for": "Single AGV active error without service-down evidence.",
        "primary_access_surfaces": ["event_viewer", "rms_ui"],
        "secondary_access_surfaces": ["wcs_sql", "ignition_gateway", "stunnel", "site_interview"],
        "primary_databases": [],
        "secondary_databases": [],
        "primary_models": [],
        "api_checks": [],
        "activities": [
            {
                "id": "rms_blank_check",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "Note blank/unreachable RMS as system-down symptom.",
            },
            {
                "id": "services_optisweep",
                "access_surface": "event_viewer",
                "role": "L2_support",
                "action": "Services MMC / Event Viewer for OptiSweep + WCSWebApplication; SQL Agent on backup after unplanned restart.",
            },
            {
                "id": "host_trio_unplanned_restart",
                "access_surface": "ignition_gateway",
                "role": "L2_support",
                "action": "Unplanned restart host path: Ignition → Stunnel → OptiSweep (+ tipper heartbeat, RMS loads).",
            },
        ],
        "observables": {
            "healthy": ["OptiSweep service running", "RMS reachable", "SQL Agent running on backup when expected"],
            "degraded": ["Service stopped/crashed", "7031 / restart storms", "RMS blank"],
            "escalate": ["Repeated crashes after restart path — L3/L4"],
        },
        "role_paths": {
            "L1_support": "High-level system down / blank RMS; escalate tooling",
            "L2_support": "Event Viewer / Services + host trio",
            "L3_support": "Own restore/RCA",
            "operator": "Report site outage symptoms",
        },
    },
    "wcs_api_responsiveness": {
        "job": "Confirm OptiSweep/WCS API responds (GetAGVStatuses and related) via Apidog.",
        "when_to_use": "Suspect API dead; Ignition/Aveva fed by same APIs unhealthy; remote AGV/system corroboration.",
        "not_for": "Operator HMI-only checks; mutating APIs beyond playbook.",
        "primary_access_surfaces": ["apidog", "wcs_api"],
        "secondary_access_surfaces": ["ignition_gateway", "rms_ui"],
        "primary_databases": [],
        "secondary_databases": [],
        "primary_models": [],
        "api_checks": ["GetAGVStatuses", "GetAGVFaultStats", "SystemState"],
        "activities": [
            {
                "id": "apidog_get_agv_statuses",
                "access_surface": "apidog",
                "role": "L2_support",
                "action": "Run GetAGVStatuses on primary Apidog; note latency/errors.",
            },
            {
                "id": "apidog_system_state",
                "access_surface": "apidog",
                "role": "L2_support",
                "action": "SystemState / related read APIs if AGV status alone is inconclusive.",
            },
        ],
        "observables": {
            "healthy": ["API returns timely success payload"],
            "degraded": ["Timeouts, 5xx, empty unexpected payloads"],
            "escalate": ["API down with services up — L4 / product defect"],
        },
        "role_paths": {
            "L1_support": "Rarely primary; escalate to L2 Apidog",
            "L2_support": "Apidog / WCS API primary",
            "L3_support": "Same + deeper API diagnostics",
            "operator": "No access",
        },
    },
    "windows_service_or_event_log": {
        "job": "Confirm Windows Event Viewer / Services evidence for OptiSweep or related host faults.",
        "when_to_use": "7031 crashes, service restarts, need host log proof.",
        "not_for": "Substitute for RMS AGV status when service is healthy.",
        "primary_access_surfaces": ["event_viewer"],
        "secondary_access_surfaces": ["wcs_service_health"],
        "primary_databases": [],
        "secondary_databases": [],
        "primary_models": [],
        "api_checks": [],
        "activities": [
            {
                "id": "event_viewer_optisweep",
                "access_surface": "event_viewer",
                "role": "L2_support",
                "action": "Event Viewer Application/System logs for OptiSweep/WCSWebApplication crash/restart evidence (incl. 7031).",
            },
            {
                "id": "services_mmc_optisweep",
                "access_surface": "event_viewer",
                "role": "L2_support",
                "action": "Services MMC: confirm OptiSweep / related services Running vs Stopped; note restart storms.",
            },
        ],
        "observables": {
            "healthy": ["No crash/restart storm for OptiSweep services", "Services Running"],
            "degraded": ["7031 / unexpected restarts", "Service stopped"],
            "escalate": ["Catalog gap for deep runbooks — honest unresolved if no procedure"],
        },
        "role_paths": {
            "L1_support": "No Event Viewer how-to; escalate",
            "L2_support": "Event Viewer / Services primary",
            "L3_support": "Same + RCA packaging",
            "operator": "No access",
        },
        "gaps": ["Thin procedure catalog historically — allow unresolved in playbooks"],
    },
    "agv_physical_recovery": {
        "job": "Coordinate on-site AGV add/remove/bump recovery with system-side roster repair.",
        "when_to_use": "Floor recovery, bump codes, motionless robot handling, remove/add AGV.",
        "not_for": "SQL-only active error query without floor action when physical recovery is required.",
        "primary_access_surfaces": ["physical_floor", "rms_ui", "wcs_api"],
        "secondary_access_surfaces": ["site_interview", "apidog"],
        "primary_databases": [],
        "secondary_databases": ["robotics"],
        "primary_models": [],
        "api_checks": ["RemoveAgv", "RecoverAGV", "GetAGVStatuses"],
        "activities": [
            {
                "id": "coach_floor_recovery",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Coach site add/remove/bump; confirm RMS status first when possible.",
            },
            {
                "id": "operator_floor_recovery",
                "access_surface": "physical_floor",
                "role": "operator",
                "action": "Execute physical AGV recovery / bump handling.",
            },
            {
                "id": "api_remove_recover",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "RemoveAgv / RecoverAGV + RMS corroboration after floor work.",
            },
        ],
        "observables": {
            "healthy": ["Robot recovered on floor and roster/map healthy"],
            "degraded": ["Bump/object blocking persists", "Remove/Recover API fails"],
            "escalate": ["Repeated physical faults — mechanical SME / L3"],
        },
        "role_paths": {
            "operator": "Executes floor recovery",
            "L1_support": "Coaches site + RMS pre-check",
            "L2_support": "System-side Remove/Recover + RMS",
            "L3_support": "Persistent recovery ownership",
        },
    },
    "robot_dwell_or_shutdown_staging": {
        "job": "Confirm robots stuck in dwell tracking or shutdown staging queues/locations.",
        "when_to_use": "Shutdown/dwell stuck on floor; robots piled in shutdown queues.",
        "not_for": "Normal charging state (agv_charging_state).",
        "primary_access_surfaces": ["wcs_sql", "rms_ui"],
        "secondary_access_surfaces": ["site_interview"],
        "primary_databases": ["robotics"],
        "secondary_databases": [],
        "primary_models": ["LocationActiveDwellModel", "ShutDownStaging", "RobotLocationDatabaseModel"],
        "api_checks": [],
        "activities": [
            {
                "id": "ask_dwell_stuck",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Ask if shutdown/dwell stuck on floor; RMS location cues if visible.",
            },
            {
                "id": "ssms_dwell_shutdown",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS LocationActiveDwell + ShutDownStaging (+ RobotLocation LocationType shutdown queues).",
            },
        ],
        "observables": {
            "healthy": ["No abnormal dwell; shutdown staging clear when expected"],
            "degraded": ["Active dwell rows", "Robots in ShutDownQueue / staging LocationTypes"],
            "escalate": ["Cannot clear staging after documented recoveries"],
        },
        "role_paths": {
            "L1_support": "Ask floor/RMS symptoms",
            "L2_support": "LocationActiveDwell + ShutDownStaging",
            "L3_support": "Persistent staging ownership",
            "operator": "Report floor pile-up / shutdown queue visuals",
        },
    },
    "agv_charging_state": {
        "job": "Confirm charging areas, charger locations, thresholds, or charge-related robot state.",
        "when_to_use": "Charge-related stops, charger unavailable, threshold misbehavior.",
        "not_for": "Shutdown staging queues (robot_dwell_or_shutdown_staging).",
        "primary_access_surfaces": ["wcs_sql", "rms_ui", "wcs_api"],
        "secondary_access_surfaces": ["apidog"],
        "primary_databases": ["robotics"],
        "secondary_databases": [],
        "primary_models": [
            "ChargingDatabaseModel",
            "ChargingLocationDatabaseModel",
            "ChargingThresholdsDatabaseModel",
            "RobotDatabaseModel",
        ],
        "api_checks": ["GetChargersStatus"],
        "activities": [
            {
                "id": "rms_charge_indicators",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "RMS charge indicators if visible.",
            },
            {
                "id": "ssms_charging_models",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS Charging* models + robot charge-related fields.",
            },
            {
                "id": "api_chargers_status",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "GetChargersStatus via Apidog.",
            },
        ],
        "observables": {
            "healthy": ["Chargers available", "Thresholds as expected", "Robots charging normally"],
            "degraded": ["Charger unavailable", "Threshold/location abnormal", "API charger fault"],
            "escalate": ["Persistent charging abnormal after DB+API"],
        },
        "role_paths": {
            "L1_support": "RMS indicators if visible",
            "L2_support": "Charging* models + GetChargersStatus",
            "operator": "Report floor charger / robot charge symptoms",
        },
    },
    "sorter_item_or_scan_state": {
        "job": "Confirm sorter item/scan path: miss-scans, dimensions, destinations, lane activity.",
        "when_to_use": "Miss-scans, odd dimensions, recirculation, lane scan anomalies.",
        "not_for": "Chute open/closed alone without item evidence (lane_or_chute_state).",
        "primary_access_surfaces": ["wcs_sql", "site_interview"],
        "secondary_access_surfaces": ["aveva_hmi", "rms_ui"],
        "primary_databases": ["sorter_sweeper"],
        "secondary_databases": [],
        "primary_models": [
            "ItemModels",
            "ItemDefaultDimModel",
            "ItemCubeAdjustmentModel",
            "IgnitionLaneActivityModel",
            "DestinationModel",
            "RecircDestinationsModel",
            "SorterModel",
        ],
        "api_checks": [],
        "activities": [
            {
                "id": "ask_miss_scans",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Ask about miss-scans / odd dimensions / recirculation symptoms.",
            },
            {
                "id": "ssms_item_lane_activity",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS Item* / IgnitionLaneActivity / Destination / Recirc models.",
            },
        ],
        "observables": {
            "healthy": ["Scans succeed", "Dimensions in expected range", "Destinations coherent"],
            "degraded": ["Miss-scan / NoRead pattern", "Default-dim fallback", "Lane activity anomalies"],
            "escalate": ["Persistent missort after item+lane DB checks"],
        },
        "role_paths": {
            "L1_support": "Site symptoms + high-level RMS/Aveva cues",
            "L2_support": "SorterSweeper item/lane models",
            "operator": "Report scanner/HMI miss-scan symptoms",
        },
    },
    "tote_exchange_sequence": {
        "job": "Confirm tote exchange sequence / hot-bin or missort exchange path.",
        "when_to_use": "Exchange stuck, hot-bin/missort exchange, exchange settings wrong.",
        "not_for": "Initialize tote alone (tote_lifecycle_state).",
        "primary_access_surfaces": ["wcs_sql", "wcs_api", "aveva_hmi"],
        "secondary_access_surfaces": ["apidog", "rms_ui"],
        "primary_databases": ["sorter_sweeper", "robotics"],
        "secondary_databases": [],
        "primary_models": [
            "ActiveExchangeModel",
            "ToteConfigModel",
            "ToteModel",
            "RobotToteDatabseModel",
            "TipperDepartureActivityModel",
        ],
        "api_checks": [
            "ExchangeTote",
            "ExchangeLane",
            "ExchangeSorterSideZone",
            "GetExchangeSettings",
            "UpdateExchange",
            "GetToteTask",
            "Purge",
        ],
        "activities": [
            {
                "id": "aveva_exchange_indicators",
                "access_surface": "aveva_hmi",
                "role": "operator",
                "action": "Verify normal exchange indicators on Aveva when available.",
            },
            {
                "id": "ssms_active_exchange",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS ActiveExchange + ToteConfig + related tote/robot-tote rows.",
            },
            {
                "id": "api_exchange",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "GetExchangeSettings / Exchange* APIs when authorized.",
            },
        ],
        "observables": {
            "healthy": ["Exchange completes", "ActiveExchange clear when idle", "Settings match expected"],
            "degraded": ["ActiveExchange stuck", "Hot-bin/missort exchange pattern", "Settings mismatch"],
            "escalate": ["Exchange APIs fail after DB corroboration"],
        },
        "role_paths": {
            "L1_support": "Verify remote indicators; escalate DB/API",
            "L2_support": "ActiveExchange + exchange APIs",
            "operator": "Aveva exchange UI when on floor",
        },
    },
    "bag_out_or_closeout_state": {
        "job": "Confirm bag-out / closeout state vs service-down.",
        "when_to_use": "Bag-out stuck, closeout not completing, cancel closeout needed.",
        "not_for": "Generic site stoppage without bag-out evidence.",
        "primary_access_surfaces": ["wcs_sql", "wcs_api", "apidog"],
        "secondary_access_surfaces": ["rms_ui", "site_interview"],
        "primary_databases": ["sorter_sweeper"],
        "secondary_databases": [],
        "primary_models": ["ActiveBagOutModel", "SystemStateModel"],
        "api_checks": ["CloseOut", "CancelCloseout", "OpenAllChutes"],
        "activities": [
            {
                "id": "ask_bag_out",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Confirm bag-out vs service-down symptoms.",
            },
            {
                "id": "ssms_active_bag_out",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS ActiveBagOutModel (+ SystemState if needed).",
            },
            {
                "id": "api_closeout",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "CloseOut / CancelCloseout when authorized; OpenAllChutes if chute-related.",
            },
        ],
        "observables": {
            "healthy": ["No stuck ActiveBagOut", "Closeout completes"],
            "degraded": ["ActiveBagOut stuck", "Closeout fails"],
            "escalate": ["CancelCloseout required repeatedly — L3"],
        },
        "role_paths": {
            "L1_support": "Symptom triage bag-out vs service-down",
            "L2_support": "ActiveBagOut + CloseOut APIs",
            "operator": "Report bag-out floor/HMI symptoms",
        },
    },
    "robot_command_or_task_state": {
        "job": "Confirm robot command/task lifecycle and Geek translation path.",
        "when_to_use": "Commands stuck, Geek task not progressing, OptiSweep vs Geek ownership of a command.",
        "not_for": "Training-study fluff without live SSMS/API checks.",
        "primary_access_surfaces": ["wcs_sql", "wcs_api", "apidog"],
        "secondary_access_surfaces": [],
        "primary_databases": ["robotics", "audit", "geek_agv"],
        "secondary_databases": ["sorter_sweeper"],
        "primary_models": [
            "RobotCommandDatabaseModel",
            "RobotTaskDatabaseModel",
            "TaskIdToRequestId",
            "GeekAgvActionLoggingModel",
            "TaskModel",
        ],
        "api_checks": ["ResendGeekCommand", "ExecutedAgvCommand", "ResendToteTask"],
        "activities": [
            {
                "id": "ssms_robot_command_task",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS RobotCommand/RobotTask; Audit TaskIdToRequestId; GeekAgv action logs.",
            },
            {
                "id": "api_resend_geek",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "ResendGeekCommand / ExecutedAgvCommand when source-backed after unplanned restart miss.",
            },
        ],
        "observables": {
            "healthy": ["Commands complete", "GUID mapping present", "Geek actions progress"],
            "degraded": ["Stuck RobotTask/Command", "Missing Audit mapping", "Geek log gap"],
            "escalate": ["ResendGeekCommand fails repeatedly"],
        },
        "role_paths": {
            "L1_support": "Usually not L1 primary",
            "L2_support": "SSMS + ResendGeekCommand as documented",
            "L3_support": "Persistent command-path ownership",
            "operator": "No SSMS/API access",
        },
    },
    "wcs_system_faults": {
        "job": "Confirm WCS/system-level active faults (SystemActiveError / system fault tables).",
        "when_to_use": "High-level software fault report; system errors distinct from single-AGV bump.",
        "not_for": "Ignore AGV-specific active errors when both present — link both capabilities.",
        "primary_access_surfaces": ["wcs_sql", "rms_ui", "wcs_api"],
        "secondary_access_surfaces": ["apidog"],
        "primary_databases": ["robotics"],
        "secondary_databases": [],
        "primary_models": ["SystemActiveErrorModel", "SystemErrorActivityModel"],
        "api_checks": ["GetAGVStatuses", "GetAGVFaultStats"],
        "activities": [
            {
                "id": "rms_system_fault_cues",
                "access_surface": "rms_ui",
                "role": "operator",
                "action": "High-level software fault cues on RMS.",
            },
            {
                "id": "ssms_system_active_error",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS SystemActiveError / SystemErrorActivity.",
            },
        ],
        "observables": {
            "healthy": ["No system active errors"],
            "degraded": ["SystemActiveError rows present", "System error activity recent"],
            "escalate": ["System faults + service down — join wcs_service_health"],
        },
        "role_paths": {
            "L1_support": "High-level fault report",
            "L2_support": "SystemActiveError tables + API corroboration",
            "operator": "Report site software-fault symptoms",
        },
    },
    "lane_or_chute_state": {
        "job": "Confirm lane/chute open-closed / bypass state.",
        "when_to_use": "Chute stuck closed, bypassed, OpenAllChutes needed, lane status wrong.",
        "not_for": "Item miss-scan root cause without lane evidence.",
        "primary_access_surfaces": ["aveva_hmi", "wcs_sql", "wcs_api"],
        "secondary_access_surfaces": ["apidog", "site_interview"],
        "primary_databases": ["sorter_sweeper"],
        "secondary_databases": [],
        "primary_models": ["LocationModel", "SorterModel", "IgnitionLaneActivityModel"],
        "api_checks": ["OpenAllChutes", "ExchangeLane"],
        "activities": [
            {
                "id": "ask_chute_state",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Ask chute open/closed; Aveva lane/zone if available.",
            },
            {
                "id": "ssms_lane_status",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS LocationModel LaneStatus / SorterModel / lane activity.",
            },
            {
                "id": "api_open_all_chutes",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "OpenAllChutes when authorized for closed chutes.",
            },
        ],
        "observables": {
            "healthy": ["Chutes open as expected", "LaneStatus healthy"],
            "degraded": ["Chute stuck closed/bypassed", "LaneStatus abnormal"],
            "escalate": ["OpenAllChutes ineffective — physical/HMI path"],
        },
        "role_paths": {
            "L1_support": "Ask chute state + Aveva overview if reachable",
            "L2_support": "LocationModel + OpenAllChutes",
            "operator": "Physical/HMI chute confirmation",
        },
    },
    "tote_lifecycle_state": {
        "job": "Confirm tote lifecycle: initialize, tasks, NoRead/MissMatch errors, remove tote.",
        "when_to_use": "Initialize tote / tote tasks issues; tote error NoRead or MissMatch.",
        "not_for": "Exchange sequence alone (tote_exchange_sequence).",
        "primary_access_surfaces": ["aveva_hmi", "wcs_sql", "wcs_api"],
        "secondary_access_surfaces": ["apidog"],
        "primary_databases": ["sorter_sweeper"],
        "secondary_databases": ["robotics"],
        "primary_models": ["ToteModel", "RobotToteDatabseModel"],
        "api_checks": ["GetToteTask", "InitializeTote", "RemoveTote", "ResendToteTask"],
        "activities": [
            {
                "id": "aveva_initialize_tote",
                "access_surface": "aveva_hmi",
                "role": "operator",
                "action": "Aveva Initialize Tote / Tote Tasks pages.",
            },
            {
                "id": "ssms_tote_model",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "SSMS ToteModel (+ RobotTote) for lifecycle/error enums.",
            },
            {
                "id": "api_tote_lifecycle",
                "access_surface": "wcs_api",
                "role": "L2_support",
                "action": "GetToteTask / InitializeTote / RemoveTote as authorized.",
            },
        ],
        "observables": {
            "healthy": ["Tote tasks progress", "No NoRead/MissMatch", "Initialize succeeds"],
            "degraded": ["Tote error NoRead/MissMatch", "Stuck tote task", "Initialize fails"],
            "escalate": ["Repeated tote errors after API+DB"],
        },
        "role_paths": {
            "L1_support": "Coach Aveva if reachable; else escalate",
            "L2_support": "ToteModel + tote APIs",
            "operator": "Aveva tote pages primary",
        },
    },
    "ups_chat_or_stunnel_health": {
        "job": "Confirm UPS Chat / Stunnel message path (AI01, AI02, SortationChat).",
        "when_to_use": "Scan/sort/hot-bin messages not flowing; Stunnel/Chat down after restart.",
        "not_for": "RMS AGV alarm as substitute for message-path health.",
        "primary_access_surfaces": ["stunnel", "site_interview"],
        "secondary_access_surfaces": ["event_viewer", "wcs_service_health"],
        "primary_databases": [],
        "secondary_databases": [],
        "primary_models": [],
        "api_checks": [],
        "activities": [
            {
                "id": "ask_chat_flowing",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Ask if Chat/sort messages are flowing.",
            },
            {
                "id": "stunnel_connections",
                "access_surface": "stunnel",
                "role": "L2_support",
                "action": "Stunnel connection list AI01/AI02/SortationChat on primary.",
            },
        ],
        "observables": {
            "healthy": ["Stunnel connections up", "Chat/sort messages flowing"],
            "degraded": ["Stunnel/Chat down", "Messages not flowing"],
            "escalate": ["Down after host restart path — join wcs_service_health"],
        },
        "role_paths": {
            "L1_support": "Ask if messages flowing (not overview-only pretend check)",
            "L2_support": "Stunnel connection check primary",
            "L3_support": "Persistent Stunnel/Chat ownership",
            "operator": "Report message-flow symptoms from site tools if any",
        },
    },
    "opc_connection_or_tipper_heartbeat": {
        "job": "Confirm Ignition OPC connections and tipper WebVisu heartbeat.",
        "when_to_use": "OPC Connections faulted; tipper HMI dead; heartbeat flatline after unplanned restart.",
        "not_for": "RMS AGV alarm list as substitute for OPC faulted; Aveva as tipper HMI.",
        "primary_access_surfaces": ["ignition_gateway", "tipper_hmi"],
        "secondary_access_surfaces": ["wcs_sql", "site_interview", "event_viewer"],
        "primary_databases": ["opc_comms"],
        "secondary_databases": ["sorter_sweeper"],
        "primary_models": ["OpcConfiguration", "OpcTags", "TagModel"],
        "api_checks": [],
        "activities": [
            {
                "id": "ask_tipper_hmi_alive",
                "access_surface": "site_interview",
                "role": "L1_support",
                "action": "Ask if tipper HMI/WebVisu alive and whether heartbeats look flat.",
            },
            {
                "id": "opc_connections_view",
                "access_surface": "ignition_gateway",
                "role": "L2_support",
                "action": "Ignition Config → OPC → OPC Connections (Day2: tippers powered off show Faulted).",
            },
            {
                "id": "webvisu_heartbeat_check",
                "access_surface": "tipper_hmi",
                "role": "L2_support",
                "action": "Confirm tipper heartbeats; if flatlined after Ignition late start, restart OptiSweep (OPC path).",
            },
            {
                "id": "ssms_opc_tags",
                "access_surface": "wcs_sql",
                "role": "L2_support",
                "action": "OPCComms OpcConfiguration/OpcTags (+ SorterSweeper TagModel) when needed.",
            },
        ],
        "observables": {
            "healthy": ["OPC connected", "WebVisu heartbeat alive", "Tipper tags readable"],
            "degraded": ["OPC tipper Faulted", "Heartbeat flatline", "Tipper HMI not responding"],
            "escalate": ["OPC faulted → OptiSweep restart path; LOTO if physical; L4 if product OPC defect"],
        },
        "role_paths": {
            "L1_support": "Ask tipper HMI alive / heartbeat symptoms",
            "L2_support": "OPC Connections + WebVisu heartbeat + OptiSweep restart when documented",
            "L3_support": "Persistent OPC/heartbeat ownership with host trio",
            "operator": "Confirm tipper HMI/local alarms on station",
        },
    },
}


def _apis_by_capability(api_doc: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for group in ("system", "agvs", "totes"):
        for row in api_doc.get(group) or []:
            name = str(row.get("name") or "")
            if not name:
                continue
            for cap in row.get("capability_hints") or []:
                if name not in out[str(cap)]:
                    out[str(cap)].append(name)
    return out


def _field_highlights(sql_doc: dict, model_names: list[str], limit: int = 12) -> list[dict]:
    by_name = {str(m.get("name")): m for m in sql_doc.get("models") or []}
    highlights: list[dict] = []
    for name in model_names:
        model = by_name.get(name)
        if not model:
            continue
        for field in model.get("fields") or []:
            fname = field.get("name")
            if not fname:
                continue
            highlights.append(
                {
                    "model": name,
                    "database": model.get("database"),
                    "field": fname,
                    "meaning": field.get("meaning"),
                    "needs_sme": bool(field.get("needs_sme")),
                }
            )
            if len(highlights) >= limit:
                return highlights
    return highlights


def _merge_unique(seq: list, extra: list) -> list:
    out: list = []
    for item in list(seq or []) + list(extra or []):
        if item not in out:
            out.append(item)
    return out


def main() -> None:
    tax = json.loads(TAX.read_text(encoding="utf-8"))
    sql = json.loads(SQL.read_text(encoding="utf-8"))
    api = json.loads(API.read_text(encoding="utf-8"))
    cross = json.loads(CROSS.read_text(encoding="utf-8"))
    api_by_cap = _apis_by_capability(api)

    models_by_cap: dict[str, list[dict]] = defaultdict(list)
    for model in sql.get("models") or []:
        for cap in model.get("capability_hints") or []:
            models_by_cap[str(cap)].append(
                {
                    "database": model.get("database"),
                    "model": model.get("name"),
                    "purpose": model.get("purpose"),
                }
            )

    fail_by_cap = {
        str(e.get("capability")): list(e.get("failure_patterns") or [])
        for e in cross.get("capability_failure_edges") or []
    }

    activities_by_cap: dict[str, list[dict]] = defaultdict(list)
    for act in cross.get("surface_activities") or []:
        for cap in act.get("capability_hints") or []:
            activities_by_cap[str(cap)].append(
                {
                    "id": act.get("activity_id"),
                    "access_surface": act.get("access_surface"),
                    "label": act.get("label"),
                    "observables": act.get("observables") or [],
                }
            )

    ordered = []
    missing_enrich = []
    for cap in tax.get("capabilities") or []:
        cid = str(cap.get("id"))
        rich = ENRICH.get(cid)
        if not rich:
            missing_enrich.append(cid)
            rich = {
                "job": cap.get("description"),
                "when_to_use": f"Source-backed checks related to {cap.get('label')}.",
                "not_for": "Different job/capability with similar wording.",
                "primary_access_surfaces": [],
                "secondary_access_surfaces": [],
                "primary_databases": [],
                "secondary_databases": [],
                "primary_models": [],
                "api_checks": [],
                "activities": [],
                "observables": {"healthy": [], "degraded": [], "escalate": []},
                "role_paths": {},
            }

        linked = models_by_cap.get(cid) or []
        primary_models = list(rich.get("primary_models") or [])
        if not primary_models and linked:
            primary_models = [m["model"] for m in linked[:8]]
        primary_dbs = list(rich.get("primary_databases") or [])
        if not primary_dbs and linked:
            primary_dbs = sorted({m["database"] for m in linked if m.get("database")})

        api_checks = _merge_unique(list(rich.get("api_checks") or []), api_by_cap.get(cid) or [])
        activities = list(rich.get("activities") or [])
        if len(activities) < 1 and activities_by_cap.get(cid):
            activities = [
                {
                    "id": a["id"],
                    "access_surface": a["access_surface"],
                    "role": None,
                    "action": a.get("label"),
                }
                for a in activities_by_cap[cid]
            ]

        ordered.append(
            {
                "id": cid,
                "label": cap.get("label"),
                "job": rich.get("job") or cap.get("description"),
                "description": cap.get("description"),
                "when_to_use": rich.get("when_to_use"),
                "not_for": rich.get("not_for"),
                "primary_access_surfaces": rich.get("primary_access_surfaces") or [],
                "secondary_access_surfaces": rich.get("secondary_access_surfaces") or [],
                "primary_databases": primary_dbs,
                "secondary_databases": rich.get("secondary_databases") or [],
                "primary_models": primary_models,
                "sql_model_links": linked,
                "field_highlights": _field_highlights(sql, primary_models),
                "api_checks": api_checks,
                "activities": activities,
                "cross_link_activities": activities_by_cap.get(cid) or [],
                "observables": rich.get("observables") or {},
                "failure_patterns": fail_by_cap.get(cid) or [],
                "role_paths": rich.get("role_paths") or {},
                "support_contract": SUPPORT_CONTRACTS.get(cid) or {},
                "backend_mappings": (
                    rich.get("backend_mappings")
                    or (SUPPORT_CONTRACTS.get(cid) or {}).get("backend_mappings")
                    or []
                ),
                "gaps": rich.get("gaps") or [],
                "source_refs": [
                    "docs/ontology/support_roles_components_and_adjacency.md",
                    "docs/ontology/catalogs/wcs_sql_catalog.json",
                    "docs/ontology/catalogs/wcs_api_catalog.json",
                    "docs/ontology/catalogs/cross_links.json",
                ],
            }
        )

    if missing_enrich:
        raise SystemExit(f"Missing ENRICH for capabilities: {missing_enrich}")

    payload = {
        "schema_version": "0.4",
        "catalog_id": "capabilities",
        "description": (
            "Rich capability cards for Stage 6 mini-RAG: each job links to access surfaces, "
            "SQL databases/models/key fields, API checks, activities, observables, failures, and role paths. "
            "Constrained tag IDs remain the taxonomy capability id list; this file is reference enrichment."
        ),
        "capabilities": ordered,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    thin = []
    for c in ordered:
        obs = c.get("observables") or {}
        n_obs = sum(len(obs.get(k) or []) for k in ("healthy", "degraded", "escalate"))
        if (
            len(c.get("activities") or []) < 2
            or n_obs < 3
            or len(c.get("role_paths") or {}) < 2
            or len(c.get("primary_access_surfaces") or []) < 1
        ):
            thin.append(c["id"])
    print(f"Wrote {OUT} ({len(ordered)} capabilities); thin={thin or 'none'}")


if __name__ == "__main__":
    main()
