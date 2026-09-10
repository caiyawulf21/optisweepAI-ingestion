# Stage 5 Playbook Candidate — Case 218550

- **Variant:** `prompt_b_multi_flow`
- **Title:** Bag-out stoppage with immobile or out-of-sequence AGVs
- **Candidate ID:** `playbook_candidate_incident_218550_bagout_agv_sequence`

## Playbook Context

Determine whether the stoppage is associated with abnormal fleet or AGV state, sequence or roster inconsistency, or a related task state; guide authorized recovery; and validate that bag-out and AGV operation resume.

## node_1 — Confirm bag-out stoppage and fleet-level operating scope

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether the reported symptom is an active bag-out interruption with an associated fleet or AGV operating abnormality rather than an isolated normal pause.
- **Expected result:** The site or L1 support observes the bag-out state through the site report and RMS overall or fleet view. Unhealthy evidence is bag-out stopped or partially progressed together with an RMS down, fault, inactive, or abnormal AGV indication. Healthy evidence is bag-out operating normally and RMS showing a running fleet without abnormal indicators. Inconclusive evidence is an unavailable RMS view, unclear bag-out state, or a symptom that is localized without a confirmed operational impact.
- **Runbook placeholder:** Procedure needed to confirm with the site whether the affected bag-out workflow is stopped, partially progressed, or operating, and to inspect the RMS overall or fleet status view for running, stopped, blank, or abnormal AGV indicators. Use generic affected-zone and reported-robot references rather than incident-specific identifiers.
- **Expects capability:** fleet_system_status
- **Expects surface:** rms_ui
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The case reports that the system stopped at bag-out after sorting and that production was seriously impacted. RMS-style evidence later showed an AGV had not moved for three hours."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_1",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The system stopped at bag-out after sorting; production seriously impacted."
  },
  {
    "page_ref": "case_218550:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "An AGV did not move for 3 hours."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_218550_page_001_nested_image_01",
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

## node_2 — Check for active AGV or system fault evidence

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether active AGV or system-level errors correlate with the bag-out stoppage or immobile robot symptom.
- **Expected result:** L1 or L2 support observes RMS AGV status and, where available, WCS or SSMS read-only active-error state. Unhealthy evidence is an RMS alarm or fault, an active AGV error row, a SystemActiveError row, or API/status evidence of a faulted or blocked AGV. Healthy evidence is no active AGV or system errors and normal AGV status. Inconclusive evidence is a blank RMS view, unreadable error detail, conflicting RMS and WCS/SSMS results, or no identifiable affected asset.
- **Runbook placeholder:** Procedure needed to inspect active AGV and system errors through the RMS fleet or AGV status view and WCS/SSMS read-only active-error models, including robot status, error code or description, affected area, and recent activity; use the OptiSweep or WCS API only when needed to corroborate status.
- **Expects capability:** agv_active_errors, wcs_system_faults
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Support advised checking system active errors, and the incident included an RMS-style observation that an AGV had not moved for three hours. No specific error code is confirmed."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_11",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Support suggested checking system active error and reported that an AGV had not moved for three hours."
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

## node_3 — Determine whether AGV sequence or roster state is inconsistent

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether a robot, AGV pair, or roster position is preventing the bag-out workflow from progressing.
- **Expected result:** The site observes the physical or HMI position when needed, while L1 or L2 support compares the RMS fleet or roster view with available WCS/SSMS state. Unhealthy evidence is a robot reported out of sequence, an AGV pair that does not correspond to expected roster or position state, an inactive or removed AGV without a replacement, or a task blocked behind abnormal AGV state. Healthy evidence is a consistent roster and sequence with AGVs assigned and positioned normally. Inconclusive evidence is an unreadable HMI, unavailable roster data, unclear pair identity, or conflicting physical and system views.
- **Runbook placeholder:** Procedure needed to inspect AGV roster, mapping, pairing, and position consistency in RMS fleet status and WCS/SSMS read-only state, and to compare the system view with the site-reported physical or HMI position without making database or configuration changes.
- **Expects capability:** device_roster_state, agv_active_errors
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"The site believed a robot was out of sequence or position. Support explained that removing an AGV without a tote requires replacing it with another one, and later reported that AGV pair removal and addition was attempted."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_3",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The site was trying to find a robot believed to be out of sequence or position."
  },
  {
    "page_ref": "case_218550:page_5",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Removing an AGV without a tote from the grid requires replacing it with another one."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_218550_page_003_nested_image_01"
]
```

### Related events

```json
[
  "incident_218550_event_003",
  "incident_218550_event_009",
  "incident_218550_event_019",
  "incident_218550_event_020"
]
```

## node_4 — Perform authorized AGV sequence or roster recovery

- **Node type:** `procedure_reference`
- **Intent:** Use an approved, role-authorized AGV recovery procedure when the diagnostic path indicates an inconsistent or blocked AGV sequence, pair, or roster state.
- **Expected result:** The authorized site operator or L2 support observes that the affected AGV or pair has been handled according to the approved procedure and that RMS or WCS status reflects the intended roster or sequence state. Progress evidence is an AGV or pair becoming available and bag-out beginning or continuing. Failure evidence is the AGV remaining inactive, the pair remaining inconsistent, or bag-out stopping again.
- **Runbook placeholder:** Procedure needed for authorized AGV physical and system-side recovery, including safe remove or add handling, replacement requirements for removed AGVs, role limits, and RMS or WCS status confirmation after the recovery action. Exact physical steps and API operations belong in the supporting runbook.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"The incident records AGV pair removal and addition attempts, discussion of AGV replacement after removal, and later confirmation that robots in proper sequence were functional."
```

### Stop or escalation note

```json
"Stop if physical handling, roster correction, or system-side recovery is outside the authorized role or safety conditions."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_9",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "AGV pairs were removed and added in an attempt to start bag-out."
  },
  {
    "page_ref": "case_218550:page_5",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "With all robots in proper sequence, the customer confirmed they were functional."
  }
]
```

### Related events

```json
[
  "incident_218550_event_009",
  "incident_218550_event_019",
  "incident_218550_event_020",
  "incident_218550_event_010"
]
```

## node_5 — Validate bag-out progress and stable AGV operation

- **Node type:** `validation_gate`
- **Intent:** Confirm that the recovery restored the affected workflow and that AGVs remain operational rather than only showing a temporary improvement.
- **Expected result:** The site observes bag-out completing or progressing normally and confirms that AGVs are moving and remain available. RMS should show normal AGV activity and roster state; WCS/SSMS may corroborate cleared active errors and normal system state. Healthy evidence is continued bag-out progress, functional robots, and no recurring active fault. Unhealthy evidence is bag-out stopping again, an AGV remaining inactive, or active errors returning. Inconclusive evidence is only a temporary start, missing RMS/WCS visibility, or inability to confirm the next operating cycle.
- **Runbook placeholder:** Procedure needed to validate bag-out workflow progress through site observation, confirm AGV movement and roster state in RMS, and corroborate cleared active errors or normal system state through WCS/SSMS read-only checks before declaring stable recovery.
- **Expects capability:** fleet_system_status, agv_active_errors
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"Bag-out reportedly restarted after AGV pair handling but stopped again; later, the customer confirmed operation when robots were in proper sequence."
```

### Stop or escalation note

```json
"Do not declare recovery from a single bag-out restart if the workflow stops again or AGV activity remains abnormal."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_9",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Bag-out started, processed most items, and stopped again after AGV pair handling."
  },
  {
    "page_ref": "case_218550:page_5",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "The customer confirmed the robots were functional when in proper sequence."
  }
]
```

### Related events

```json
[
  "incident_218550_event_019",
  "incident_218550_event_010",
  "incident_218550_event_026"
]
```

## node_6 — Stop and escalate when the supported recovery path does not stabilize operation

- **Node type:** `escalation_gate`
- **Intent:** Hand off when diagnostics remain inconclusive, recovery is unauthorized or unsafe, or bag-out or AGV operation fails validation after the supported path.
- **Expected result:** L1 or L2 support observes unresolved bag-out stoppage, repeated AGV inactivity, conflicting RMS and WCS/SSMS state, an unavailable required HMI or diagnostic surface, or failure after authorized recovery. A supported resolution is not established when the workflow cannot be validated as stable.
- **Runbook placeholder:** Procedure needed to prepare an escalation evidence package containing RMS fleet or roster views, WCS/SSMS active-error and system-state evidence, relevant HMI fault or task observations, AGV handling and recovery outcomes, bag-out progress, and validation results, with clear safety and authorization boundaries.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The incident records that available troubleshooting options were exhausted and that the bag-out problem could recur after partial progress."
```

### Stop or escalation note

```json
"Escalate for repeated physical faults, unresolved roster or sequence inconsistency, conflicting diagnostic surfaces, or failed validation; do not infer a confirmed root cause."
```

### Source references

```json
[
  {
    "page_ref": "case_218550:page_10",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "Support reported that available troubleshooting options had been exhausted."
  },
  {
    "page_ref": "case_218550:page_13",
    "site_code": "ups_haslet_tx",
    "site_label": "UPS Haslet TX (TXRTH)",
    "quote_or_summary": "A process to recover from a stuck task was needed before the next sort."
  }
]
```

### Related events

```json
[
  "incident_218550_event_021",
  "incident_218550_event_019",
  "incident_218550_event_027"
]
```

