# Stage 5 Playbook Candidate — Case 228086

- **Variant:** `prompt_b_multi_flow`
- **Title:** Robotic system stopped responding with AGVs not moving
- **Candidate ID:** `playbook_candidate_incident_228086_sitewide_robotic_stoppage`

## Playbook Context

Restore and validate robotic-system responsiveness for a site-wide or broad AGV stoppage without assuming a confirmed root cause.

## node_1 — Confirm the stoppage pattern and affected scope

- **Node type:** `diagnostic_decision`
- **Intent:** Confirm that the reported condition is a broad robotic-system or AGV stoppage rather than an isolated robot or local equipment issue.
- **Expected result:** The site operator or L1 support observes the affected zone or fleet and reports whether multiple AGVs are stationary, whether the small sort or robotic workflow is stopped, and whether hospital or HMI symptoms are present. In RMS fleet or overall status, a healthy or unrelated condition is a normal populated view with expected movement or no broad stop indication; an unhealthy pattern is a blank/abnormal overview or broad non-movement; inconclusive means the site cannot confirm scope or RMS is unavailable.
- **Runbook placeholder:** Procedure needed to confirm with the site which affected area or workflow is stopped, whether multiple AGVs are stationary, whether the small sort or hospital workflow is affected, and whether any local safety stop is active. In RMS fleet or overall status, check the generic affected-area overview for a populated normal view versus a blank, unavailable, or broad stopped presentation; do not rely on the incident-specific zone or robot identifiers.
- **Expects capability:** fleet_system_status
- **Expects surface:** rms_ui, site_interview
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The packet reports nothing moving, multiple bots not moving in various areas, a stopped small sort, hospital tote removal problems, and an abnormal mostly blank RMS/HMI presentation."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_2",
    "artifact_id": null,
    "quote_or_summary": "Reports included 4-6 bots not moving, inability to remove hospital totes, question marks on HMI, and nothing moving with no obvious failed AGV."
  },
  {
    "page_ref": "case_228086:page_5",
    "artifact_id": "artifact_incident_228086_page_005_embedded_image_01",
    "quote_or_summary": "RMS page appeared mostly blank and displayed an apparent .NET control message."
  },
  {
    "page_ref": "case_228086:page_25",
    "artifact_id": "artifact_incident_228086_page_025_embedded_image_01",
    "quote_or_summary": "Work order described the robotic system as not responding and the small sort as not running."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_005_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_001",
  "incident_228086_event_002",
  "incident_228086_event_003",
  "incident_228086_event_030",
  "incident_228086_event_035"
]
```

## node_2 — Check for OptiSweep or WCS application failure evidence

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether a service termination or correlated WCS application error provides a supported direction for service recovery.
- **Expected result:** L1 or L2 support observes Windows Event Viewer. An unhealthy pattern is a System-log Service Control Manager error showing OptiSweep terminated unexpectedly, or clustered Application-log WCSWebApplication/Application Error entries such as the reported database-command failure. A healthy-style result is no relevant service or application errors in the incident time window; inconclusive means logs are unavailable, timestamps cannot be correlated, or only informational events are present.
- **Runbook placeholder:** Procedure needed to inspect Windows Event Viewer for the OptiSweep service in the System log, including Service Control Manager termination events, and to review the Application log for correlated WCSWebApplication or Application Error entries around the reported stoppage. Capture whether the service termination and application-error pattern is present, absent, or inconclusive without treating it as confirmed root cause.
- **Expects capability:** windows_service_or_event_log, wcs_service_health
- **Expects surface:** event_viewer
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Event Viewer evidence showed OptiSweep Event 7031 and clustered WCSWebApplication/Application Error events around the reported stoppage."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_28",
    "artifact_id": "artifact_incident_228086_page_028_embedded_image_01",
    "quote_or_summary": "WCSWebApplication Event ID 20102 reported a failed database command in the Application log."
  },
  {
    "page_ref": "case_228086:page_29",
    "artifact_id": "artifact_incident_228086_page_029_embedded_image_01",
    "quote_or_summary": "Service Control Manager Event 7031 stated that OptiSweep terminated unexpectedly and that an automatic restart was scheduled."
  },
  {
    "page_ref": "case_228086:page_27",
    "artifact_id": "artifact_incident_228086_page_027_embedded_image_01",
    "quote_or_summary": "Application log showed clustered WCSWebApplication and Application Error entries around the same period."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_027_embedded_image_01",
  "artifact_incident_228086_page_028_embedded_image_01",
  "artifact_incident_228086_page_029_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_044",
  "incident_228086_event_045",
  "incident_228086_event_046",
  "incident_228086_event_049",
  "incident_228086_event_050"
]
```

## node_3 — Perform authorized OptiSweep service recovery

- **Node type:** `procedure_reference`
- **Intent:** Restore the affected robotic-control service using an approved recovery procedure when the role is authorized and the safety state permits continuation.
- **Expected result:** L1 or L2 support observes that the approved service-recovery procedure has completed and that OptiSweep is not left in a stopped or repeatedly failing state. A successful recovery indication is a stable service state suitable for validation; an unsuccessful indication is a failed, stopped, or repeatedly terminating service; inconclusive means completion or service state cannot be verified.
- **Runbook placeholder:** Procedure needed for authorized recovery of the OptiSweep service through Windows Services or the approved service-recovery mechanism, including safety prerequisites, role limits, and criteria for stopping if the service cannot be recovered. Do not assume the Event Viewer automatic restart completed successfully.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"Case comments state that OptiSweep was reset after the service crash; Windows Services later showed OptiSweep running, but the screenshot did not prove when or how recovery occurred."
```

### Stop or escalation note

```json
"Do not continue with unsupported service or database changes. Stop if the approved recovery cannot be performed safely or the service repeatedly fails."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "quote_or_summary": "Chat states that the OptiSweep service was reset before RMS follow-up."
  },
  {
    "page_ref": "case_228086:page_19",
    "artifact_id": "artifact_incident_228086_page_019_embedded_image_01",
    "quote_or_summary": "Windows Services showed OptiSweep in a Running state."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_019_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_039",
  "incident_228086_event_040",
  "incident_228086_event_049",
  "incident_228086_event_050"
]
```

## node_4 — Validate gateway and OptiSweep responsiveness

- **Node type:** `validation_gate`
- **Intent:** Confirm that the recovered service and supporting gateway are responding before investigating or correcting residual AGV state.
- **Expected result:** L1 or L2 support observes Windows Services with OptiSweep Running, the Ignition gateway Systems Overview responding with a current response value and no recent slow-response events, and the OptiSweep/WCS API GetAgvStatuses request returning HTTP 200 with AGV records. Healthy evidence is stable service state, responsive Ignition status, and returned AGV data; unhealthy evidence is a stopped service, unavailable gateway, no API response, or repeated service failure; inconclusive evidence is a successful HTTP response with unusable or ambiguous payload, such as the reported schema warning.
- **Runbook placeholder:** Procedure needed to validate OptiSweep in Windows Services, inspect Ignition gateway health in the Systems Overview including response time and recent slow-response indicators, and call the incident-evidenced OptiSweep/WCS API GetAgvStatuses endpoint through the approved API client to confirm response status and usable AGV records. Treat schema-validation warnings separately from transport success.
- **Expects capability:** wcs_service_health, gateway_health, wcs_api_responsiveness
- **Expects surface:** event_viewer, ignition_gateway, wcs_api
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"The packet contains evidence of OptiSweep Running, Ignition Systems Overview responsiveness, and a GetAgvStatuses HTTP 200 response with returned AGV records, while noting a schema-validation warning."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_16",
    "artifact_id": "artifact_incident_228086_page_016_embedded_image_01",
    "quote_or_summary": "Ignition Systems Overview showed current response time and no recent slow response events."
  },
  {
    "page_ref": "case_228086:page_17",
    "artifact_id": "artifact_incident_228086_page_017_embedded_image_01",
    "quote_or_summary": "GetAgvStatuses returned HTTP 200 with AGV records, although the API client reported a schema mismatch."
  },
  {
    "page_ref": "case_228086:page_19",
    "artifact_id": "artifact_incident_228086_page_019_embedded_image_01",
    "quote_or_summary": "OptiSweep was displayed as Running in Windows Services."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_016_embedded_image_01",
  "artifact_incident_228086_page_017_embedded_image_01",
  "artifact_incident_228086_page_019_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_023",
  "incident_228086_event_024",
  "incident_228086_event_025",
  "incident_228086_event_026",
  "incident_228086_event_027",
  "incident_228086_event_029"
]
```

## node_5 — Determine whether AGV state remains out of sync

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether residual AGV errors, roster state, or inconsistent operational states remain after service responsiveness is restored.
- **Expected result:** An operator or L1 support observes RMS fleet status, while L2 support may corroborate through read-only WCS/SSMS. Healthy evidence is a populated RMS view with no relevant active AGV/system alarms and consistent normal roster or state information; unhealthy evidence is out-of-sync, unmapped, abnormal, or active-error AGV state; inconclusive evidence is a blank RMS view, conflicting RMS and SSMS/API results, or unreadable state data.
- **Runbook placeholder:** Procedure needed to inspect AGV fleet status and roster state in RMS and, for remote corroboration, read-only WCS database/SSMS models for active AGV or system errors and robot state. Compare the same fleet condition across RMS and WCS/SSMS without making database changes, and identify whether residual out-of-sync or abnormal-state assets remain.
- **Expects capability:** agv_active_errors, device_roster_state
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"After service reset, the incident record states that RMS was used to locate AGVs that were out of sync; the packet also contains SSMS evidence of AGV state inspection and ontology support for active-error and roster checks."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "quote_or_summary": "Chat states that RMS was used to locate and fix AGVs that were out of sync after OptiSweep reset."
  },
  {
    "page_ref": "case_228086:page_24",
    "artifact_id": "artifact_incident_228086_page_024_embedded_image_01",
    "quote_or_summary": "SSMS view showed robotics-related AGV state values during troubleshooting."
  },
  {
    "page_ref": "case_228086:page_14",
    "artifact_id": "artifact_incident_228086_page_014_embedded_image_01",
    "quote_or_summary": "RMS Map Monitor showed an AGV state and control area, but the screenshot did not establish whether the displayed state was abnormal."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_014_embedded_image_01",
  "artifact_incident_228086_page_024_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_021",
  "incident_228086_event_033",
  "incident_228086_event_034",
  "incident_228086_event_039"
]
```

## node_6 — Correct residual AGV synchronization state

- **Node type:** `procedure_reference`
- **Intent:** Use an authorized RMS procedure to correct identified out-of-sync or otherwise supported abnormal AGV states after service responsiveness is established.
- **Expected result:** The authorized operator or support role observes that identified AGV records have been processed according to the approved RMS procedure and that the affected fleet state is eligible for revalidation. Successful progress is a corrected or normal state for the identified assets; unsuccessful progress is persistence, recurrence, or inability to identify the affected assets; inconclusive means RMS and WCS/SSMS disagree or the state cannot be safely interpreted.
- **Runbook placeholder:** Procedure needed for authorized RMS handling of identified out-of-sync AGVs, including asset-selection criteria, safety prerequisites, role limits, and post-action state checks. Keep the exact RMS controls and per-AGV actions in the runbook; do not infer or generalize the incident-specific robot identifiers.
- **Expects capability:** None
- **Expects surface:** rms_ui
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"Case comments state that individual out-of-sync AGVs were located and fixed in RMS after the OptiSweep service was reset."
```

### Stop or escalation note

```json
"Stop if the affected asset cannot be safely identified, if the approved RMS action is unavailable, or if the action would require unsupported database or configuration changes."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "quote_or_summary": "After resetting OptiSweep, RMS was used to locate and fix out-of-sync AGVs one by one."
  }
]
```

### Related events

```json
[
  "incident_228086_event_039",
  "incident_228086_event_040"
]
```

## node_7 — Confirm stable fleet operation and workflow recovery

- **Node type:** `validation_gate`
- **Intent:** Confirm that the robotic workflow has resumed and remains stable after service recovery and any AGV-state correction.
- **Expected result:** The site operator observes resumed automated movement or the affected workflow, including normal handling of the small sort or bag-out process as applicable. L1/L2 support corroborates RMS fleet status and the OptiSweep/WCS API response; WCS/SSMS may corroborate that active-error and roster-state evidence is normal. Healthy evidence is resumed operation, a populated RMS view, usable API records, and no relevant active AGV/system errors; unhealthy evidence is renewed stoppage, persistent out-of-sync state, failed API/service response, or active errors; inconclusive evidence is only a case-status update or a partial snapshot without live operational confirmation.
- **Runbook placeholder:** Procedure needed to confirm stable recovery through the site-observed workflow, RMS fleet status, the OptiSweep/WCS API GetAgvStatuses response, and read-only WCS/SSMS corroboration of active errors or roster state when needed. Include monitoring duration or repeat-check criteria and distinguish resumed bag-out from full restoration of all site functions.
- **Expects capability:** fleet_system_status, wcs_api_responsiveness, agv_active_errors
- **Expects surface:** site_interview, rms_ui, wcs_api, wcs_sql
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"The packet reports that the site resumed auto bag-out after AGV correction and later case evidence stated the site was running; API and service checks were also documented."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "quote_or_summary": "Site reportedly resumed auto bag-out after the out-of-sync AGVs were corrected."
  },
  {
    "page_ref": "case_228086:page_17",
    "artifact_id": "artifact_incident_228086_page_017_embedded_image_01",
    "quote_or_summary": "GetAgvStatuses returned HTTP 200 with AGV records and visible normal status values."
  },
  {
    "page_ref": "case_228086:page_19",
    "artifact_id": "artifact_incident_228086_page_019_embedded_image_01",
    "quote_or_summary": "OptiSweep was shown as Running in Windows Services."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_017_embedded_image_01",
  "artifact_incident_228086_page_019_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_025",
  "incident_228086_event_029",
  "incident_228086_event_041"
]
```

## node_8 — Stop and escalate when recovery cannot be safely validated

- **Node type:** `escalation_gate`
- **Intent:** Hand off when the approved diagnostic and recovery path does not restore stable operation or when evidence remains conflicting or insufficient to continue safely.
- **Expected result:** L1 or L2 support observes one or more of the following: OptiSweep repeatedly terminates, Event Viewer shows unresolved correlated errors, the API remains unavailable or unusable, RMS and WCS/SSMS disagree, AGVs remain out of sync, or the site cannot confirm stable automated operation. A healthy result does not enter this gate; an inconclusive result requires an evidence-based handoff rather than an assumed resolution.
- **Runbook placeholder:** Procedure needed to prepare an escalation handoff with Event Viewer System and Application evidence, Windows Services state, Ignition gateway status, OptiSweep/WCS API response evidence, RMS fleet or AGV-state evidence, WCS/SSMS read-only findings, recovery actions attempted, and explicit stop criteria.
- **Expects capability:** None
- **Expects surface:** event_viewer, ignition_gateway, wcs_api, rms_ui, wcs_sql
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The packet documents unresolved uncertainty around service restart completion, API schema interpretation, memory/log follow-up, and the need to distinguish resumed bag-out from complete restoration."
```

### Stop or escalation note

```json
"Escalate for unresolved, unsafe, unauthorized, or conflicting conditions; do not escalate solely because the historical case involved collaboration or unfamiliarity."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_17",
    "artifact_id": "artifact_incident_228086_page_017_embedded_image_01",
    "quote_or_summary": "API returned HTTP 200 but the response differed from the endpoint specification."
  },
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "quote_or_summary": "Follow-up investigation concerned a faulted web application, memory usage, and log size without confirmed causal resolution."
  },
  {
    "page_ref": "case_228086:page_29",
    "artifact_id": "artifact_incident_228086_page_029_embedded_image_01",
    "quote_or_summary": "Event Viewer documented OptiSweep termination and configured restart action without confirming successful recovery."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_016_embedded_image_01",
  "artifact_incident_228086_page_017_embedded_image_01",
  "artifact_incident_228086_page_027_embedded_image_01",
  "artifact_incident_228086_page_028_embedded_image_01",
  "artifact_incident_228086_page_029_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_026",
  "incident_228086_event_027",
  "incident_228086_event_042",
  "incident_228086_event_043",
  "incident_228086_event_049"
]
```

