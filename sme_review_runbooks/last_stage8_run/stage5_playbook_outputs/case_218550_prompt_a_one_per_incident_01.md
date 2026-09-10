# Stage 5 Playbook Candidate — Case 218550

- **Variant:** `prompt_a_one_per_incident`
- **Title:** Bag-out stoppage with inactive or out-of-sequence AGV symptoms
- **Candidate ID:** `playbook_candidate_incident_218550_bagout_agv_sequence`

## Playbook Context

Determine whether the bag-out stoppage is associated with an observable AGV, system-error, task, or HMI condition; use an authorized recovery procedure when a supported path is identified; and validate stable robot operation and bag-out progress.

## node_1 — Confirm an active automated bag-out stoppage and observable AGV impact

- **Node type:** `diagnostic_decision`
- **Intent:** Establish whether automated bag-out is currently stalled and whether the site can identify an inactive, faulted, or sequencing-related AGV symptom without assuming the cause.
- **Expected result:** The site/operator reports that automated bag-out is stopped, stalled, or requiring manual handling, and identifies whether robots are moving. In RMS fleet status, a healthy indication is normal fleet activity with no corresponding stoppage; an unhealthy indication is an inactive or faulted AGV, abnormal fleet overview, or activity gap consistent with the reported stoppage; inconclusive means the site cannot reproduce the symptom or RMS is blank or lacks enough status detail.
- **Runbook placeholder:** Procedure needed to confirm with the site whether automated bag-out is stopped or requiring manual handling, whether AGVs are moving in the affected area, and whether the symptom is repeatable. In RMS fleet status, inspect the overall fleet view and AGV activity/status view for normal operation, inactive assets, alarms, or an unavailable display. Do not rely on AVEVA if the site cannot see the relevant screen.
- **Expects capability:** fleet_system_status, agv_active_errors
- **Expects surface:** rms_ui, site_interview
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The case reported that the system stopped at bag-out, manual bagging was required, and an AGV had not moved for three hours."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_2",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The system had stopped at the bag-out stage after sorting."
  },
  {
    "page_ref": "case_218550:page_9",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "System is not going into bagout. Manual bagging out reported."
  },
  {
    "page_ref": "case_218550:page_11",
    "artifact_id": "artifact_incident_218550_page_011_nested_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "An AGV did not move for 3 hours."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_218550_page_011_nested_image_01"
]
```

### Related events

```json
[
  "incident_218550_event_002",
  "incident_218550_event_016",
  "incident_218550_event_023"
]
```

## node_2 — Check for active AGV or system error evidence

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether current AGV or system active-error evidence supports continuing into an AGV recovery or sequencing path.
- **Expected result:** An operator or L1 observer may see AGV alarms or abnormal status in RMS. L2/L3 may corroborate through WCS/SSMS read-only views of AGV active-error and system active-error records. Healthy evidence is no relevant active alarms or cleared error rows with normal AGV status; unhealthy evidence is a faulted or blocked AGV, active error code or description, or recent system error associated with the stoppage; inconclusive means RMS is blank, the identifiers cannot be correlated, or RMS and WCS/SSMS disagree.
- **Runbook placeholder:** Procedure needed to inspect RMS AGV status and fleet error indicators, and to corroborate the same active-error check through WCS database / SSMS read-only views for AGV active errors and SystemActiveError records. The procedure should capture the affected robot or area, current error description, and whether the error is active, cleared, or ambiguous without making database changes.
- **Expects capability:** agv_active_errors, wcs_system_faults
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Support advised checking system active error, and the incident evidence reported an AGV that had not moved for three hours."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_11",
    "artifact_id": "artifact_incident_218550_page_011_nested_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Support suggested checking system active error after observing that an AGV had not moved for three hours."
  },
  {
    "page_ref": "case_218550:page_11",
    "artifact_id": "artifact_incident_218550_page_011_nested_image_02",
    "chunk_id": "stage4_artifact_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The technical screenshot was too small and garbled to identify detailed error values."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_218550_page_011_nested_image_01",
  "artifact_incident_218550_page_011_nested_image_02"
]
```

### Related events

```json
[
  "incident_218550_event_022",
  "incident_218550_event_023"
]
```

## node_3 — Check for task, tote, or HMI evidence associated with the stalled flow

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether the affected workflow has a visible HMI fault, stuck task, tote-location discrepancy, or other task-state evidence that provides a supported next direction.
- **Expected result:** The site/operator may observe a fault or stuck-task indication on the hospital HMI or related lane UI. A healthy indication is no relevant HMI fault and a task or tote progressing normally; an unhealthy indication is a visible fault, a task that remains stuck, or a tote/location mismatch reported by the site; inconclusive means the HMI text is unreadable, the relevant screen is unavailable, or the reported task cannot be correlated to the stopped workflow.
- **Runbook placeholder:** Procedure needed to inspect the Hospital HMI / lane UI for the current fault or stuck-task indication and to compare the displayed tote or task context with the site's physical observation. The procedure should provide a decision rubric for distinguishing a recoverable acknowledge/retry condition from an unresolved task or tote-state condition without prescribing click sequences or screen navigation.
- **Expects capability:** robot_command_or_task_state, sorter_item_or_scan_state
- **Expects surface:** hospital_hmi, site_interview
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The source reported a hospital HMI fault, a tote read at the hospital while physically elsewhere, and a stuck task visible only on that HMI."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_9",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "A tote had been mixed around at the hospital, read at the hospital while actually elsewhere, and bag-out entered request but did not progress."
  },
  {
    "page_ref": "case_218550:page_12",
    "artifact_id": "artifact_incident_218550_page_012_nested_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The hospital HMI was reported to be showing a fault."
  },
  {
    "page_ref": "case_218550:page_13",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_002",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "A stuck task was reported as visible only on that HMI."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_218550_page_012_nested_image_01"
]
```

### Related events

```json
[
  "incident_218550_event_017",
  "incident_218550_event_024",
  "incident_218550_event_028",
  "incident_218550_event_029"
]
```

## node_4 — Use an authorized AGV sequencing or roster recovery procedure

- **Node type:** `procedure_reference`
- **Intent:** Apply the approved recovery path for an identified AGV sequencing, pairing, availability, or task-state condition within the executing role's authority.
- **Expected result:** The authorized operator or support role completes the approved recovery activity without unsafe or unsupported changes. Progress evidence is that affected robots are available, represented consistently in RMS, and able to participate in the expected sequence; failure evidence is that the robot remains unavailable, the sequence remains inconsistent, or the procedure cannot be completed within role limits.
- **Runbook placeholder:** Procedure needed for authorized AGV sequencing, pairing, roster, or physical recovery when the diagnostic path identifies a supported condition. It should define safety preconditions, role limits, required RMS confirmation, any site-side AGV handling or remove/add coordination, and the evidence to capture after recovery. Do not infer or prescribe a specific sequence from the incident.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"The incident records AGV pair remove/add activity, guidance that a removed AGV without a tote needs replacement, robots being turned back on, and resolution after robots were in proper sequence."
```

### Stop or escalation note

```json
"Do not continue if the required action is outside the authorized role, requires unsupported database or configuration changes, or presents an unresolved physical safety condition."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_5",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "A removed AGV without a tote needs to be replaced with another one; the customer later confirmed robots were in proper sequence and functional."
  },
  {
    "page_ref": "case_218550:page_10",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_002",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Support asked the site to remove and add AGV pairs; bag-out started but later stopped again."
  }
]
```

### Related events

```json
[
  "incident_218550_event_006",
  "incident_218550_event_008",
  "incident_218550_event_009",
  "incident_218550_event_019",
  "incident_218550_event_020"
]
```

## node_5 — Validate stable AGV operation and resumed bag-out

- **Node type:** `validation_gate`
- **Intent:** Confirm that the affected workflow has recovered rather than relying only on a temporary change in screen state.
- **Expected result:** The site/operator observes that robots remain powered and in proper sequence, AGVs resume expected movement, and automated bag-out progresses without immediately stopping. RMS should show a normal fleet or relevant AGV state; L2/L3 may corroborate through WCS/SSMS that active errors are cleared or no longer active. Healthy evidence is stable robot operation and continued bag-out progress; unhealthy evidence is recurrence of the stoppage, inactive AGV, active error, or renewed HMI/task fault; inconclusive evidence is a temporary acknowledgement without observed workflow progress or conflicting RMS and WCS/SSMS state.
- **Runbook placeholder:** Procedure needed to validate recovery through site observation and RMS fleet status, with WCS database / SSMS read-only corroboration of AGV and system active-error state when available. The validation should confirm that robots remain available and in sequence, bag-out progresses beyond the prior stall, and no relevant fault immediately recurs before recovery is declared.
- **Expects capability:** fleet_system_status, agv_active_errors, robot_command_or_task_state
- **Expects surface:** rms_ui, wcs_sql, site_interview
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"The customer confirmed that robots were functional when all were in proper sequence, and later reported that the HMI condition was all good."
```

### Stop or escalation note

```json
"A temporary acknowledgement or brief robot movement is not sufficient if bag-out remains stalled or the fault recurs."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_5",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "With all robots in proper sequence, the customer confirmed they were functional."
  },
  {
    "page_ref": "case_218550:page_13",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_002",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The site confirmed the tote condition was good."
  }
]
```

### Related events

```json
[
  "incident_218550_event_010",
  "incident_218550_event_026"
]
```

## node_6 — Stop and escalate when no supported recovery path or validation exists

- **Node type:** `escalation_gate`
- **Intent:** Hand off when diagnostics are inconclusive, required access or authorization is unavailable, or the approved recovery path fails to restore stable operation.
- **Expected result:** L1/L2 identifies missing or conflicting evidence, an unresolved AGV or task condition, a recurring bag-out stoppage, or a failed validation gate. Healthy continuation is not applicable; this node is reached only when the current role cannot safely continue or the available recovery path did not restore operation.
- **Runbook placeholder:** Procedure needed to prepare an escalation handoff with the observed bag-out state, RMS fleet and AGV status, WCS/SSMS read-only active-error evidence when available, HMI or task evidence, affected asset identifiers if known, recovery actions attempted, and validation results. Include stop criteria for unresolved safety, authorization, or repeated operational failure.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The incident records that available troubleshooting options were exhausted and that further investigation was needed after bag-out restarted and stopped again."
```

### Stop or escalation note

```json
"Escalate for unresolved or repeated faults, RMS versus WCS/SSMS conflicts, unavailable required access, unsupported changes, or failed recovery validation."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_10",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_002",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Support reported that available troubleshooting options had been exhausted."
  },
  {
    "page_ref": "case_218550:page_10",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_002",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Bag-out started, processed most items, and stopped again."
  }
]
```

### Related events

```json
[
  "incident_218550_event_020",
  "incident_218550_event_021"
]
```

