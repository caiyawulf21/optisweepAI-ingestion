# Stage 5 Playbook Candidate — Case 223554

- **Variant:** `prompt_b_multi_flow`
- **Title:** Hospital tote induction failure with AGV or service-state disruption
- **Candidate ID:** `playbook_candidate_incident_223554_hospital_induct_and_agv_state_recovery`

## Playbook Context

Restore safe, stable hospital tote induction and broader sort operation by coordinating symptom confirmation, service-state checks, AGV/tote-state checks, authorized recovery, and post-recovery validation without assuming a confirmed root cause.

## node_1 — Confirm hospital induction or site-operation symptom

- **Node type:** `diagnostic_decision`
- **Intent:** Confirm whether the reported problem is a hospital tote-add/induction failure, a broader inability to start or sustain sort, or a different symptom that should leave this path.
- **Expected result:** Site operator or L1 support observes the affected hospital station and asks whether totes can be added and removed, whether the hospital lane is accepting work, and whether sort is stopped or unstable. In the Hospital HMI or lane UI, unhealthy evidence is inability to add or induct totes or a visible station fault; healthy evidence is normal add and remove operation with no relevant alarm; inconclusive evidence is an unreadable display, contradictory reports, or no site confirmation.
- **Runbook placeholder:** Procedure needed to confirm with the site which affected hospital workflow is failing, whether totes can be added and removed, whether the hospital lane is accepting work, and whether sort is stopped or unstable; inspect the Hospital HMI or lane UI for station, lane, stacklight, or alarm indications. Use generic affected-zone or reported-station wording rather than incident-specific identifiers.
- **Expects capability:** hospital_diversion, lane_or_chute_state
- **Expects surface:** hospital_hmi, site_interview
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The case and chat repeatedly report that the hospital station could not add or induct totes, while later messages report inability to start or sustain sort."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_8",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "They can remove totes but cannot add them."
  },
  {
    "page_ref": "case_223554:page_6",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The site could not start sort or went down during sort."
  },
  {
    "page_ref": "case_223554:page_17",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Client unable to induct totes at the station."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_223554_page_008_nested_image_01",
  "artifact_incident_223554_page_014_nested_image_01"
]
```

### Related events

```json
[
  "incident_223554_event_019",
  "incident_223554_event_020",
  "incident_223554_event_036",
  "incident_223554_event_042"
]
```

## node_2 — Check hospital and fleet service health

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether an abnormal OptiSweep, AGV hospital service, or related server/service state correlates with the hospital or site-wide symptom.
- **Expected result:** L1 or L2 support checks Windows Event Viewer and Windows Services for service or application failure indicators, and checks the OptiSweep/WCS API for responsiveness. Healthy evidence is expected service availability, no relevant recent service termination indication, and a responsive API; unhealthy evidence is documented server/service trouble, service not running, API unresponsive, or relevant service-failure evidence; inconclusive evidence is that only a work-order note is available without live status.
- **Runbook placeholder:** Procedure needed to inspect Windows Event Viewer Application and System logs for relevant service or application failure evidence, check Windows Services for the affected OptiSweep or AGV hospital service state, and check the incident-evidenced OptiSweep/WCS API for responsiveness without making changes.
- **Expects capability:** windows_service_or_event_log, wcs_service_health, wcs_api_responsiveness
- **Expects surface:** event_viewer, wcs_api
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Work-order and repair notes report AGV hospital station server issues and a need to reset services; closure evidence reports resetting OptiSweep services, but does not identify all service names or prove the reset alone was causal."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_5",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "AGV hospital station is having server issues; services need to be reset."
  },
  {
    "page_ref": "case_223554:page_17",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Resolution details state that OptiSweep services were reset and Hospital Lane was restarted."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_223554_page_005_nested_image_01",
  "artifact_incident_223554_page_015_nested_image_01"
]
```

### Related events

```json
[
  "incident_223554_event_014",
  "incident_223554_event_037",
  "incident_223554_event_038",
  "incident_223554_event_043"
]
```

## node_3 — Check AGV roster, location, and tote association state

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether AGV location, roster, task, or tote-association anomalies are present and may be blocking hospital induction or broader flow.
- **Expected result:** Operator or L2 support checks the RMS fleet or roster view and, when remotely attainable, WCS/SSMS read-only state or the OptiSweep/WCS API. Unhealthy evidence includes an AGV in an unexpected location, duplicate occupancy under a rack or in a zone, a disconnected or stranded tote association, shutdown state, or abnormal task state; healthy evidence is a coherent roster, expected locations, and no relevant disconnected tote or task anomaly; inconclusive evidence is an unreadable map, incomplete asset state, or disagreement between RMS and read-only backend evidence.
- **Runbook placeholder:** Procedure needed to inspect AGV roster, location, task, and tote-association state in RMS fleet status and corroborate the same state through WCS/SSMS read-only data or the OptiSweep/WCS API. The procedure should identify abnormal-state assets and distinguish a live state from an annotated or historical screenshot without changing database state.
- **Expects capability:** device_roster_state, agv_active_errors, robot_command_or_task_state
- **Expects surface:** rms_ui, wcs_sql, wcs_api
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"Chat and incident summary report AGVs in unexpected locations, two AGVs under one rack, disconnected tote associations, shutdown state, and removal or re-addition of several robots."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_8",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "An AGV did not belong in the shown location and two AGVs were under the rack in the same zone."
  },
  {
    "page_ref": "case_223554:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Summary describes an AGV with a disconnected tote and several AGVs being removed to restore operation."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_223554_page_008_nested_image_01",
  "artifact_incident_223554_page_009_nested_image_01"
]
```

### Related events

```json
[
  "incident_223554_event_021",
  "incident_223554_event_023",
  "incident_223554_event_024",
  "incident_223554_event_031",
  "incident_223554_event_032"
]
```

## node_4 — Check tipper station contribution when hospital flow follows tipping

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether a tipper alarm, station state, or operator-station condition is contributing to totes being directed incorrectly or the hospital workflow not progressing.
- **Expected result:** Operator or L1 support observes the tipper HMI/WebVisu and reports active alarm or station state; L2 may inspect read-only tipper or OPC evidence. Healthy evidence is no relevant VISU alarm, normal station state, and readable heartbeat or tag state; unhealthy evidence is a tipper alarm, station not releasing, abnormal station state, or a flat or unavailable heartbeat; inconclusive evidence is only a second-hand tipper report or an unreadable screen.
- **Runbook placeholder:** Procedure needed to inspect the relevant tipper HMI/WebVisu VISU_ALARM and station-state indicators, and when appropriate corroborate tipper or OPC heartbeat state through Ignition or WCS/SSMS read-only diagnostics. Keep this as an evidence check; do not include physical recovery, E-stop, or exact HMI navigation steps.
- **Expects capability:** tipper_station_fault, opc_connection_or_tipper_heartbeat
- **Expects surface:** tipper_hmi, ignition_gateway, wcs_sql
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"The packet contains second-hand reports of tipper issues and notes that operators should pause the station during recovery to avoid sending everything to hospital."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_2",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Second-hand report mentions tipper issues."
  },
  {
    "page_ref": "case_223554:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Summary notes that operators at tippers should pause the station during recovery."
  }
]
```

### Related events

```json
[
  "incident_223554_event_003",
  "incident_223554_event_009",
  "incident_223554_event_031"
]
```

## node_5 — Select supported recovery direction

- **Node type:** `branching_condition`
- **Intent:** Select service recovery, AGV/tote-state correction, tipper-state handling, or a combined authorized path based on observed evidence rather than the tentative hypothesis alone.
- **Expected result:** L1/L2 support compares live evidence from Event Viewer, Windows Services, OptiSweep/WCS API, RMS, WCS/SSMS, Hospital HMI, and tipper HMI. A service-related branch is indicated by service or API health evidence; an AGV/tote branch by roster, location, task, or association inconsistency; a tipper branch by an active tipper or heartbeat condition; a combined branch is used when more than one condition is observed; healthy or absent patterns require leaving this recovery path or retriaging rather than assuming recovery is needed; inconclusive evidence requires escalation or additional authorized diagnostics.
- **Runbook placeholder:** Decision rubric needed to compare named evidence from Windows Event Viewer and Windows Services, OptiSweep/WCS API, RMS fleet status, WCS/SSMS read-only state, Hospital HMI, and tipper HMI, and choose only an authorized recovery direction supported by the observed signals. The rubric must distinguish confirmed observations from tentative internal patterns.
- **Expects capability:** wcs_service_health, device_roster_state, tipper_station_fault
- **Expects surface:** event_viewer, wcs_api, rms_ui, wcs_sql, tipper_hmi
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"The incident evidence contains multiple possible contributors and multiple recovery statements, including service reset, AGV/tote correction, robot removal or re-addition, and tipper pause handling."
```

### Stop or escalation note

```json
"Do not select a mutating database, configuration, or unsupported API action from this rubric."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Source summary identifies two possible issues and states the exact cause was not known."
  },
  {
    "page_ref": "case_223554:page_5",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "AGV hospital station server issue and need to reset services."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_223554_page_005_nested_image_01",
  "artifact_incident_223554_page_008_nested_image_01"
]
```

### Related events

```json
[
  "incident_223554_event_014",
  "incident_223554_event_023",
  "incident_223554_event_031",
  "incident_223554_event_043"
]
```

## node_6 — Perform authorized recovery for service and operational state

- **Node type:** `procedure_reference`
- **Intent:** Apply the approved recovery path for the observed service, AGV/tote state, or tipper condition within role and safety limits.
- **Expected result:** Authorized L1/L2 support or site operator observes recovery completion through the applicable procedure. Healthy progress is a returned service/API response, corrected AGV or tote state, or restored tipper station condition; unhealthy progress is continued service failure, unresolved state inconsistency, or renewed alarm; inconclusive progress is no reliable post-action evidence. Any physical AGV handling or safety action remains site-controlled and must follow its approved procedure.
- **Runbook placeholder:** Procedure needed for authorized recovery of the named OptiSweep or AGV hospital service, supported AGV/tote-state correction through the approved OptiSweep/WCS API or AVEVA path, and any authorized tipper-state recovery. The procedure must define safety preconditions, role limits, evidence capture, and whether site operators must pause the relevant station; it must not be replaced by exact commands or API mutations in this playbook.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, operator

### Source-supported description

```json
"Source-reported recovery includes resetting OptiSweep services, restarting Hospital Lane, removing or correcting disconnected tote associations through an API-based tool, taking some AGVs out, and re-adding robots."
```

### Stop or escalation note

```json
"Do not perform unsupported database changes, configuration changes, physical AGV removal, or safety actions outside the authorized procedure."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_17",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "OptiSweep services were reset and Hospital Lane was restarted."
  },
  {
    "page_ref": "case_223554:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "API-based tote removal, AGV removal, and subsequent restoration were reported."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_223554_page_015_nested_image_01"
]
```

### Related events

```json
[
  "incident_223554_event_031",
  "incident_223554_event_032",
  "incident_223554_event_043"
]
```

## node_7 — Validate hospital induction and stable site operation

- **Node type:** `validation_gate`
- **Intent:** Confirm that the hospital workflow and broader sort operation have recovered and remain stable before declaring the troubleshooting path successful.
- **Expected result:** Site operator observes that the Hospital HMI or lane UI accepts tote additions and removals, hospital backlog is progressing, and tippers are in the expected operating state. L1/L2 support corroborates service/API responsiveness and RMS or WCS/SSMS roster and task state where available. Healthy evidence is successful tote add and remove, AGV movement, normal roster/state, and sort starting or continuing; unhealthy evidence is inability to add, renewed shutdown or location inconsistency, continued site-down state, or recurring alarms; inconclusive evidence is a general statement that the system is running without workflow-specific confirmation.
- **Runbook placeholder:** Procedure needed to validate Hospital HMI or lane UI tote add and remove behavior, confirm AGV movement and roster state in RMS with WCS/SSMS or OptiSweep/WCS API corroboration, check service responsiveness in Windows Services, and verify that sort starts or remains stable. Include monitoring duration and evidence expectations without prescribing exact screen sequences.
- **Expects capability:** hospital_diversion, device_roster_state, wcs_api_responsiveness, fleet_system_status
- **Expects surface:** hospital_hmi, rms_ui, wcs_sql, wcs_api, event_viewer
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"The source reports that totes could again be added and removed, robots were re-added and running, movement resumed, and the system was running."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_4",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Site could add and remove totes again and later reported all robots re-added and running."
  },
  {
    "page_ref": "case_223554:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Movement started and the system was reported running."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_223554_page_003_nested_image_01"
]
```

### Related events

```json
[
  "incident_223554_event_008",
  "incident_223554_event_013",
  "incident_223554_event_029",
  "incident_223554_event_030",
  "incident_223554_event_039",
  "incident_223554_event_040"
]
```

## node_8 — Stop and escalate when supported recovery or validation fails

- **Node type:** `escalation_gate`
- **Intent:** Stop the playbook when evidence is insufficient, recovery is unauthorized or unsafe, or the hospital or site-wide operation remains unstable after the supported path.
- **Expected result:** L1/L2 support observes unresolved service failure in Event Viewer or Windows Services, nonresponsive OptiSweep/WCS API, unresolved AGV/tote state in RMS or WCS/SSMS, active HMI alarms, unsafe physical conditions, or failed validation after authorized recovery. Healthy evidence for this gate is that escalation is not required because validation passed; inconclusive evidence is missing logs, unreadable screens, contradictory state, or inability to confirm safe role access.
- **Runbook placeholder:** Procedure needed to prepare an escalation handoff with Event Viewer and Windows Services evidence, OptiSweep/WCS API response evidence, RMS and WCS/SSMS read-only fleet or tote-state evidence, Hospital HMI or tipper alarm evidence, safety stop criteria, recovery actions attempted, and validation results. Do not use this gate merely because the historical case involved collaboration or unfamiliarity.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The packet documents unresolved uncertainty, severe production impact, and source concerns that a faster technical escalation path may be needed, but this gate is based on reusable stop conditions rather than the historical handoff itself."
```

### Stop or escalation note

```json
"Escalate when the path is unsafe, outside role authorization, lacks sufficient source-supported evidence to continue, or remains unresolved after authorized diagnostics and validation."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Source states the exact cause was not known and describes recovery attempts."
  },
  {
    "page_ref": "case_223554:page_6",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Site was reported down and unable to start or sustain sort."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_223554_page_006_nested_image_01"
]
```

### Related events

```json
[
  "incident_223554_event_019",
  "incident_223554_event_031",
  "incident_223554_event_043"
]
```

