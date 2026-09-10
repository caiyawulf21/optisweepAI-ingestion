# Stage 5 Playbook Candidate — Case 223554

- **Variant:** `prompt_a_one_per_incident`
- **Title:** Hospital tote induction failure with AGV or service-state recovery
- **Candidate ID:** `playbook_candidate_incident_223554_hospital_induct_recovery`

## Playbook Context

Restore safe hospital tote induction and stable automated operation by distinguishing station or fleet-state symptoms from AGV/tote association anomalies and abnormal OptiSweep service state, then validating recovery.

## node_1 — Confirm hospital induction or broader sort disruption

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether the reported issue is an observable hospital tote-induction failure with possible wider operational impact, before selecting the technical investigation path.
- **Expected result:** The site operator or L1 support observes the Hospital HMI or lane UI and confirms whether totes cannot be added or inducted, whether removal still works, whether a robot is shown shut down, and whether sort is stopped or unable to start. Healthy signal: normal add and remove behavior and no active hospital disruption. Unhealthy signal: add or induct fails, hospital backlog is present, or sort is stopped. Inconclusive: the site cannot reproduce the symptom, the HMI is unavailable, or the report is only second-hand.
- **Runbook placeholder:** Procedure needed to confirm with the site which affected hospital workflow is failing, whether totes can be added and removed, whether a reported robot is shut down, and whether sort is stopped. Check the Hospital HMI or lane UI for the observable induction state and use RMS fleet status for the high-level system-down or AGV overview; do not assume the cause from the initial report.
- **Expects capability:** fleet_system_status
- **Expects surface:** hospital_hmi, site_interview, rms_ui
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The case reports inability to induct or add totes at the hospital, a robot in a shut down state, and later inability to start or sustain sort."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_14",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "case_comment",
    "quote_or_summary": "Case subject: acb hospital unable to induct."
  },
  {
    "page_ref": "case_223554:page_17",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "page_ocr",
    "quote_or_summary": "Client unable to induct totes at the station and robot is in a shut down state."
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

## node_2 — Check AGV roster, location, active errors, and tote association state

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether the hospital symptom correlates with an AGV in an unexpected location, duplicate occupancy, disconnected tote, or other abnormal fleet or association state.
- **Expected result:** The operator or L1 support checks RMS fleet status, while L1/L2 support may corroborate through WCS/SSMS read-only data. Healthy signal: expected AGV roster, locations, active-error state, and tote associations with no duplicate or disconnected association. Unhealthy signal: an AGV is mapped to an unexpected location, multiple AGVs appear in one position or zone, a robot is shut down, or a tote association is disconnected or inconsistent. Inconclusive: RMS, WCS/SSMS, and site observations disagree or required asset records are unavailable.
- **Runbook placeholder:** Procedure needed to inspect the affected fleet and hospital-area state in RMS fleet status, including AGV location and roster views, and to corroborate active AGV or system errors and association state through WCS database / SSMS read-only diagnostics when available. The procedure should explain how to distinguish a normal location from an unexpected, duplicate, shut-down, or disconnected AGV/tote state without changing database records.
- **Expects capability:** device_roster_state, agv_active_errors
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"Chat evidence describes an AGV in an unexpected location, two AGVs under one rack, and a disconnected tote; the incident summary also describes AGV and tote state corrections."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_8",
    "chunk_id": "stage4_page_chunk_003",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "teams_message",
    "quote_or_summary": "This AGV does not belong here; two AGVs are under the rack in the same zone."
  },
  {
    "page_ref": "case_223554:page_11",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "teams_message",
    "quote_or_summary": "AGV with a disconnected tote was in the system; other AGVs were under the rack."
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
  "incident_223554_event_031"
]
```

## node_3 — Check OptiSweep service and related host health

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether an abnormal OptiSweep or AGV hospital-station service state is contributing to the induction or sort disruption.
- **Expected result:** L1/L2 support observes Windows Services and Windows Event Viewer, and may use the OptiSweep or WCS API for responsiveness. Healthy signal: relevant services are running without recent service-termination evidence and the API responds with expected system or AGV data. Unhealthy signal: a relevant service is stopped or repeatedly restarting, Event Viewer shows service termination or application errors, or the API is unavailable or returns an abnormal response. Inconclusive: service names are not identified, logs are unavailable, or API and host evidence disagree.
- **Runbook placeholder:** Procedure needed to inspect the named OptiSweep or AGV hospital-station service state in Windows Services, review Windows Event Viewer System and Application logs for relevant service-control or application errors, and check OptiSweep / WCS API responsiveness without making configuration changes. The procedure should identify what evidence is sufficient to treat service health as normal, abnormal, or inconclusive.
- **Expects capability:** windows_service_or_event_log, wcs_api_responsiveness
- **Expects surface:** event_viewer, wcs_api
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Repair and case notes report AGV hospital-station server issues and a need to reset services; the packet does not identify exact service names or show live service status."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_5",
    "chunk_id": "stage4_artifact_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "artifact_visual",
    "quote_or_summary": "AGV hospital station is having server issues; services need to be reset."
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
  "incident_223554_event_038"
]
```

## node_4 — Perform approved service or state recovery

- **Node type:** `procedure_reference`
- **Intent:** Use the authorized recovery path indicated by the diagnostic evidence, which may include OptiSweep service recovery and correction of supported AGV or tote state through the approved operational interface.
- **Expected result:** L2/L3 support or an authorized site operator observes that the approved recovery action has completed without safety or authorization exceptions. Progress signal: the relevant service or gateway is responsive, supported AGV/tote state corrections are accepted, and the affected workflow can proceed. Unhealthy signal: the action is rejected, state remains inconsistent, service remains unavailable, or recovery would require an undocumented mutation or unsafe physical intervention. Inconclusive: completion cannot be confirmed from the responsible tool or interface.
- **Runbook placeholder:** Procedure needed for authorized recovery of the affected OptiSweep services or related hospital lane service state, plus the approved API or AVEVA operational procedure for correcting supported AGV and tote associations when those states are confirmed abnormal. The procedure must define safety preconditions, role limits, required state checks, and prohibited database or configuration changes without specifying click paths, commands, or exact mutation steps.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, operator

### Source-supported description

```json
"Source-reported recovery included resetting OptiSweep services, restarting Hospital Lane, removing disconnected or inducted totes through an API-based tool, taking selected AGVs out, and using Aveva to add a tote to a station. Exact procedures are not supplied."
```

### Stop or escalation note

```json
"Do not continue if the required recovery is not covered by an approved procedure, requires unsupported database/configuration mutation, or requires physical intervention beyond the executing role."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_17",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "case_comment",
    "quote_or_summary": "Resolution details say OptiSweep services were reset and the site restarted Hospital Lane."
  },
  {
    "page_ref": "case_223554:page_11",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "teams_message",
    "quote_or_summary": "API-based actions removed inducted or disconnected totes and selected AGVs were taken out to restore flow."
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

## node_5 — Validate induction, fleet state, and stable operation

- **Node type:** `validation_gate`
- **Intent:** Confirm that hospital tote handling and broader automated operation have recovered and remain stable after the approved recovery path.
- **Expected result:** The site operator observes the Hospital HMI or lane UI and confirms totes can be added and removed; RMS shows the expected AGV roster and normal fleet state; L1/L2 support may confirm OptiSweep / WCS API responsiveness and service state in Windows Services. Healthy signal: tote induction and removal work, AGVs are re-added or shown in expected state, movement or sort resumes, and no immediate recurrence is reported. Unhealthy signal: induction still fails, AGVs remain abnormal, the site cannot start sort, or service/API health degrades again. Inconclusive: only a general statement that the system is running is available without workflow or fleet confirmation.
- **Runbook placeholder:** Procedure needed to validate the Hospital HMI or lane UI for successful tote add and remove behavior, confirm expected AGV roster and status in RMS, verify relevant service state in Windows Services, and check OptiSweep / WCS API responsiveness. The validation procedure should include a short stability observation and distinguish workflow recovery from a general report that the system is running.
- **Expects capability:** fleet_system_status, wcs_api_responsiveness
- **Expects surface:** hospital_hmi, rms_ui, wcs_api, event_viewer
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"The source reports that the site could add and remove totes again, all robots were re-added and running, movement started, and the system was running."
```

### Stop or escalation note

```json
"Failure or recurrence after the approved recovery path requires the escalation gate rather than repeated unsupported recovery."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_16",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "case_comment",
    "quote_or_summary": "Site could add and remove totes; all robots were re-added and back up and running."
  },
  {
    "page_ref": "case_223554:page_11",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "teams_message",
    "quote_or_summary": "Movement started and the system was running."
  }
]
```

### Related events

```json
[
  "incident_223554_event_029",
  "incident_223554_event_030",
  "incident_223554_event_039",
  "incident_223554_event_040"
]
```

## node_6 — Stop and escalate when supported recovery or validation fails

- **Node type:** `escalation_gate`
- **Intent:** Hand off when the evidence does not support a safe authorized recovery path, when required access or procedures are unavailable, or when the incident remains unresolved after recovery and validation.
- **Expected result:** L1/L2 support observes that diagnostics are inconclusive, an approved recovery procedure is unavailable, service or fleet abnormalities persist, or validation fails after recovery. Healthy exit for this gate is not applicable; this gate is entered only when the path cannot continue safely or the issue remains unresolved.
- **Runbook placeholder:** Procedure needed to prepare an escalation handoff containing Hospital HMI and RMS evidence, WCS/SSMS read-only findings when used, Windows Services and Event Viewer evidence, OptiSweep / WCS API response evidence, affected workflow symptoms, recovery actions attempted, and validation results. The procedure should define stop criteria and the required technical owner without creating a communication or case-management workflow.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The packet documents unresolved uncertainty, missing service detail, and discussion that persistent OptiSweep-related incidents need a faster technical escalation path."
```

### Stop or escalation note

```json
"Escalate if the cause remains uncertain after supported checks, if service or state correction requires an unavailable role or undocumented procedure, or if tote induction, fleet state, API/service health, or stable sort validation fails."
```

### Source references

```json
[
  {
    "page_ref": "case_223554:page_3",
    "chunk_id": "stage4_page_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "teams_message",
    "quote_or_summary": "If technical support cannot determine the issue, a path to the project execution team was requested."
  },
  {
    "page_ref": "case_223554:page_11",
    "chunk_id": "stage4_page_chunk_004",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "support_type": "teams_message",
    "quote_or_summary": "The summary states the cause was not certain."
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
  "incident_223554_event_011",
  "incident_223554_event_031"
]
```

