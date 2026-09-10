# Stage 5 Playbook Candidate — Case 228086

- **Variant:** `prompt_a_one_per_incident`
- **Title:** Robotic system stops responding with AGV state disruption
- **Candidate ID:** `playbook_candidate_incident_228086_service_crash_agv_resynchronization`

## Playbook Context

Determine whether the stoppage correlates with a failed OptiSweep or related WCS application state, perform only authorized recovery through the applicable procedure, correct residual AGV state discrepancies, and validate stable service and automated operation.

## node_1 — Confirm broad stoppage and affected workflow

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether the report represents a broad automated-operation stoppage rather than an isolated robot or local equipment issue.
- **Expected result:** The site operator or L1 support observes the reported area and, when available, the RMS overall or fleet status view. Unhealthy-style evidence is that multiple AGVs or a broad workflow are stopped, the small sort or hospital workflow is unavailable, or RMS is blank or abnormal. Healthy-style evidence is that operation is moving normally or the issue is limited to one local asset. Inconclusive evidence is a conflicting site report, unavailable RMS view, or insufficient information about scope.
- **Runbook placeholder:** Procedure needed to question the site about whether nothing is moving, which broad workflow is stopped, whether hospital or small-sort activity is affected, and whether any AGV alarms are visible; also check the RMS overall or fleet status view for broad stopped, blank, or abnormal presentation without assuming the displayed message is a confirmed fault.
- **Expects capability:** fleet_system_status
- **Expects surface:** site_interview, rms_ui
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The incident included reports that nothing was moving, the small sort was not running, hospital totes could not be removed, and RMS/HMI appeared blank or abnormal."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_2",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "support_type": "teams_message",
    "quote_or_summary": "Nothing was moving; no fault or failed AGVs were reported."
  },
  {
    "page_ref": "case_228086:page_25",
    "artifact_id": "artifact_incident_228086_page_025_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "artifact_visual",
    "quote_or_summary": "Robotic system not responding and small sort not running."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_005_embedded_image_01",
  "artifact_incident_228086_page_025_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_002",
  "incident_228086_event_003",
  "incident_228086_event_030",
  "incident_228086_event_035"
]
```

## node_2 — Check named service and application failure evidence

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether Windows logs or service state show an OptiSweep or WCSWebApplication failure correlated with the stoppage.
- **Expected result:** L1 or L2 support observes Windows Event Viewer and Windows Services. Unhealthy-style evidence includes a System-log Service Control Manager termination event for OptiSweep, Application-log WCSWebApplication or Application Error entries clustered with the event, or OptiSweep not running. Healthy-style evidence is no correlated service termination or application-error cluster and OptiSweep is running. Inconclusive evidence is missing logs, ambiguous timestamps, or a Running service state without correlation to application and operational status.
- **Runbook placeholder:** Procedure needed to inspect Windows Event Viewer System and Application logs for OptiSweep Service Control Manager termination events, WCSWebApplication errors, and related Application Error entries, and to check OptiSweep status in Windows Services. The procedure should distinguish observed failure evidence from a later Running state and should not infer root cause from correlation alone.
- **Expects capability:** windows_service_or_event_log, wcs_service_health
- **Expects surface:** event_viewer
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Event Viewer showed WCSWebApplication errors around 6:35-6:36 AM and Event 7031 stating that the OptiSweep service terminated unexpectedly; Windows Services later showed OptiSweep running."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_29",
    "artifact_id": "artifact_incident_228086_page_029_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "system_log",
    "quote_or_summary": "Event 7031 states that the OptiSweep service terminated unexpectedly and a restart action was scheduled."
  },
  {
    "page_ref": "case_228086:page_28",
    "artifact_id": "artifact_incident_228086_page_028_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "system_log",
    "quote_or_summary": "WCSWebApplication Event 20102 reported a failed database command."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_027_embedded_image_01",
  "artifact_incident_228086_page_028_embedded_image_01",
  "artifact_incident_228086_page_029_embedded_image_01",
  "artifact_incident_228086_page_019_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_044",
  "incident_228086_event_045",
  "incident_228086_event_046",
  "incident_228086_event_049",
  "incident_228086_event_050",
  "incident_228086_event_029"
]
```

## node_3 — Perform authorized OptiSweep or gateway recovery

- **Node type:** `procedure_reference`
- **Intent:** Use the approved recovery procedure for the affected service or gateway when the diagnostic evidence supports that path and the role is authorized.
- **Expected result:** L2 or L3 support observes completion of the approved recovery procedure and the resulting service or gateway state. Recovery is complete only when the responsible role confirms that the procedure finished without an unsafe condition and the affected service or gateway is available for validation. Inconclusive evidence includes a restart still in progress, no final status, or a service that appears Running without responsiveness validation.
- **Runbook placeholder:** Procedure needed for authorized recovery of the OptiSweep service or related Ignition gateway, including safety preconditions, any required site operational state, role limits, and completion criteria. The procedure must avoid relying on the incident's exact command text and must define how to determine that recovery has completed before post-recovery checks.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The incident records an OptiSweep reset and an Ignition gateway restart activity, but the exact command sequence and final restart outcome are not suitable for playbook instructions."
```

### Stop or escalation note

```json
"Do not continue with mutating recovery outside the authorized role or while site safety conditions are not satisfied."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "case_comment",
    "quote_or_summary": "After resetting OptiSweep, RMS was used to locate and correct out-of-sync AGVs."
  },
  {
    "page_ref": "case_228086:page_15",
    "artifact_id": "artifact_incident_228086_page_015_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "artifact_visual",
    "quote_or_summary": "Ignition gateway restart was initiated and the console showed that it was waiting for restart."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_012_nested_image_02",
  "artifact_incident_228086_page_015_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_018",
  "incident_228086_event_022",
  "incident_228086_event_039"
]
```

## node_4 — Check AGV and system error state when service failure is not indicated

- **Node type:** `diagnostic_decision`
- **Intent:** Use fleet and backend state evidence to identify an alternate AGV, system-error, or state-distribution condition when the service-failure pattern is not confirmed.
- **Expected result:** The operator or L1 support observes RMS fleet status, while L2 or L3 support may corroborate the same error and system state through read-only WCS/SSMS. Unhealthy-style evidence includes active AGV or system error rows, stopped or faulted system state, or a conflict between RMS and backend state. Healthy-style evidence is a normal overall system state with no relevant active errors and no broad stoppage. Inconclusive evidence is a blank RMS view, unavailable backend data, or state values whose operational meaning cannot be established.
- **Runbook placeholder:** Procedure needed to inspect RMS fleet or AGV status and, for remote support, corroborate active AGV and system errors and overall system state through read-only WCS database / SSMS views using the documented robotics models. The procedure should identify whether the state is a true active error, a normal transitional state, or an RMS/backend disagreement.
- **Expects capability:** agv_active_errors, fleet_system_status
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"The evidence included RMS AGV views, read-only SSMS state inspection, reports of no visible AGV faults, and investigation of a potentially removed or out-of-sync AGV."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_24",
    "artifact_id": "artifact_incident_228086_page_024_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_002",
    "support_type": "artifact_visual",
    "quote_or_summary": "SSMS results displayed multiple robotics-related AGV state values."
  },
  {
    "page_ref": "case_228086:page_21",
    "artifact_id": "artifact_incident_228086_page_021_full_page_01",
    "chunk_id": "stage4_artifact_chunk_002",
    "support_type": "case_comment",
    "quote_or_summary": "A possibly removed AGV was being investigated."
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
  "incident_228086_event_034"
]
```

## node_5 — Check for residual AGV synchronization issues after recovery

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether AGVs remain out of sync or otherwise require authorized state correction after service or gateway recovery.
- **Expected result:** The operator or L1 support observes the RMS fleet or map status, and L2 or L3 support may corroborate active errors or roster/state information through read-only WCS/SSMS. Unhealthy-style evidence includes AGVs still marked out of sync, abnormal roster or mapping state, active AGV/system errors, or a discrepancy between RMS and backend state. Healthy-style evidence is a consistent normal fleet view with no relevant active errors and expected AGV status. Inconclusive evidence is an unavailable or blank RMS view, incomplete roster data, or conflicting RMS and SSMS results.
- **Runbook placeholder:** Procedure needed to inspect the RMS fleet or map view for out-of-sync, unmapped, or abnormal-state AGVs and to corroborate the same fleet error or roster condition through read-only WCS database / SSMS where remotely attainable. If correction is authorized, the linked operational procedure must define the safe state-correction boundary without embedding the correction steps here.
- **Expects capability:** agv_active_errors, device_roster_state
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"After the OptiSweep reset, RMS was used to locate and fix AGVs reported as out of sync one by one."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "case_comment",
    "quote_or_summary": "RMS was used to locate AGVs that were out of sync and fix them."
  },
  {
    "page_ref": "case_228086:page_24",
    "artifact_id": "artifact_incident_228086_page_024_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_002",
    "support_type": "artifact_visual",
    "quote_or_summary": "SSMS displayed robotics-related AGV state results for diagnostic review."
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
  "incident_228086_event_039",
  "incident_228086_event_040"
]
```

## node_6 — Apply authorized AGV state correction

- **Node type:** `procedure_reference`
- **Intent:** Use the approved RMS or fleet-state procedure to correct identified out-of-sync AGV state when the responsible role confirms that correction is safe and supported.
- **Expected result:** The authorized support role observes that the identified AGV state correction procedure has completed and that the affected assets are available for validation. Inconclusive evidence includes a correction that did not complete, an unidentified asset, or conflicting RMS and backend state.
- **Runbook placeholder:** Procedure needed for authorized correction of an out-of-sync or otherwise abnormal AGV state through the supported RMS or fleet-management workflow, including asset identification, safety preconditions, role limits, and completion criteria. Exact UI actions and state-changing instructions belong in the linked runbook, not in this orchestration node.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The case states that out-of-sync AGVs were located and fixed in RMS after the OptiSweep service was reset."
```

### Stop or escalation note

```json
"Do not perform state-changing fleet correction without an authorized role and a clearly identified affected asset."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "case_comment",
    "quote_or_summary": "Out-of-sync AGVs were corrected in RMS."
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

## node_7 — Validate service, API, fleet state, and automated operation

- **Node type:** `validation_gate`
- **Intent:** Confirm that the recovered service is responsive, AGV state is usable, and the site can resume stable automated operation.
- **Expected result:** L1 or L2 support observes OptiSweep in Windows Services and validates the GetAgvStatuses endpoint through the OptiSweep/WCS API client; the operator observes RMS fleet status and reports whether automated movement and the affected workflow have resumed. Healthy evidence includes a responsive service, successful API response with usable AGV records, no unresolved relevant AGV errors, a normal RMS fleet view, and resumed automated operation. Unhealthy evidence includes no API response, non-usable or persistently faulted AGV records, unresolved out-of-sync state, blank or abnormal RMS, or continued stoppage. Inconclusive evidence includes HTTP success with a schema warning, a Running service without operational movement, or missing site confirmation.
- **Runbook placeholder:** Procedure needed to confirm OptiSweep state in Windows Services, validate the incident-evidenced GetAgvStatuses endpoint through the OptiSweep/WCS API client, inspect RMS fleet status and active AGV/system errors, and obtain site confirmation that automated movement or bag-out has resumed and remains stable. The procedure must distinguish API reachability from full operational recovery.
- **Expects capability:** wcs_api_responsiveness, fleet_system_status, agv_active_errors
- **Expects surface:** wcs_api, rms_ui, wcs_sql
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"The packet records GetAgvStatuses returning HTTP 200 with AGV records, OptiSweep shown as Running, RMS follow-up, and site resumption of auto bag-out, while also documenting an API schema warning that should not be treated as full recovery by itself."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_17",
    "artifact_id": "artifact_incident_228086_page_017_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_002",
    "support_type": "validation_evidence",
    "quote_or_summary": "GetAgvStatuses returned HTTP 200 with AGV records, including visible NORMAL values, alongside a schema-validation warning."
  },
  {
    "page_ref": "case_228086:page_19",
    "artifact_id": "artifact_incident_228086_page_019_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_002",
    "support_type": "diagnostic_evidence",
    "quote_or_summary": "OptiSweep was shown as Running in Windows Services."
  },
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "case_comment",
    "quote_or_summary": "The site resumed auto bag-out after AGV correction."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_017_embedded_image_01",
  "artifact_incident_228086_page_019_embedded_image_01",
  "artifact_incident_228086_page_016_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_023",
  "incident_228086_event_025",
  "incident_228086_event_026",
  "incident_228086_event_029",
  "incident_228086_event_041"
]
```

## node_8 — Stop and escalate unresolved or unsafe recovery

- **Node type:** `escalation_gate`
- **Intent:** Hand off when the supported diagnostic and recovery path cannot safely establish a recovery state or validation fails.
- **Expected result:** L1 or L2 support observes unresolved service or application errors, conflicting RMS and WCS/SSMS state, failed or incomplete recovery, persistent API non-responsiveness, unresolved AGV synchronization issues, or continued site stoppage. Escalation is not required merely because another team participated historically.
- **Runbook placeholder:** Procedure needed to prepare the escalation handoff with Windows Event Viewer System and Application evidence, Windows Services state, RMS fleet or map evidence, WCS/SSMS read-only diagnostic results, API response evidence, recovery actions attempted, validation outcomes, safety status, and the precise reason the supported path cannot continue.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The evidence contains unresolved uncertainty around the web application, memory/log behavior, incomplete restart outcomes, and API schema validation, supporting an evidence-based stop boundary when validation fails."
```

### Stop or escalation note

```json
"Escalate for unsafe, unauthorized, unsupported, conflicting, or unresolved conditions; do not treat historical unfamiliarity or communication handoff as the escalation reason."
```

### Source references

```json
[
  {
    "page_ref": "case_228086:page_17",
    "artifact_id": "artifact_incident_228086_page_017_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_002",
    "support_type": "validation_evidence",
    "quote_or_summary": "The API response was HTTP 200 but did not match the endpoint specification."
  },
  {
    "page_ref": "case_228086:page_26",
    "artifact_id": "artifact_incident_228086_page_026_full_page_01",
    "chunk_id": "stage4_artifact_chunk_003",
    "support_type": "case_comment",
    "quote_or_summary": "Investigation continued into a faulted web application and memory or log-size concerns."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228086_page_017_embedded_image_01",
  "artifact_incident_228086_page_027_embedded_image_01",
  "artifact_incident_228086_page_028_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228086_event_026",
  "incident_228086_event_027",
  "incident_228086_event_042",
  "incident_228086_event_043"
]
```

