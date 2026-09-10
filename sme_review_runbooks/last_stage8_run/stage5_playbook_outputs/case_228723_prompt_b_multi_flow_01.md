# Stage 5 Playbook Candidate — Case 228723

- **Variant:** `prompt_b_multi_flow`
- **Title:** Zone pairing failure with abnormal AMR routing
- **Candidate ID:** `playbook_candidate_incident_228723_zone_pairing_roster_recovery`

## Playbook Context

Determine whether the reported pairing failure is associated with abnormal fleet membership, mapping, or AGV state, apply only an authorized recovery path when supported, and confirm that normal pairing and AMR operation resume.

## node_1 — Confirm the zone pairing failure and current routing symptom

- **Node type:** `diagnostic_decision`
- **Intent:** Establish whether the reported issue is an active zone pairing failure and whether AMRs are being routed to an unexpected destination such as the hospital lane.
- **Expected result:** The site operator or L1 support observes the affected zone and reports whether pair requests fail, whether the zone is otherwise active, and whether AMRs are being directed toward the hospital. In RMS pairing or fleet views, an unhealthy signal is a pair-fail or unable-to-pair indication, while a healthy signal is normal pairing with no active pairing alarm. Inconclusive means the site report is unavailable or RMS does not expose a readable pairing state.
- **Runbook placeholder:** Procedure needed to confirm with the site whether the affected zone cannot obtain a pair, whether AMRs are actively routing to the hospital lane, and whether the symptom began after recent AGV replacement or remove/add activity. In RMS, inspect the affected zone's pairing or fleet-status view for pair-fail indicators and the visible routing or destination state.
- **Expects capability:** zone_pairing_state
- **Expects surface:** rms_ui, site_interview
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The site reported that the zone could not get a pair, and support discussion linked the symptom with AMRs going to the hospital lane."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_1",
    "quote_or_summary": "Site reports under zone 5, they're unable to get a pair."
  },
  {
    "page_ref": "case_228723:page_2",
    "quote_or_summary": "Earlier low-battery AMR issues were reported, and attempted replacement AMRs were going to the hospital lane."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_012_embedded_image_01",
  "artifact_incident_228723_page_010_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228723_event_002",
  "incident_228723_event_003",
  "incident_228723_event_020",
  "incident_228723_event_021"
]
```

## node_2 — Check fleet roster and mapping consistency

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether one or more AGVs have abnormal roster membership, mapping, location, or zone state that could explain the pairing failure.
- **Expected result:** L1 or L2 support observes RMS fleet and roster views and, when remotely attainable, corroborates them through read-only WCS/SSMS robotics and mapping state. Unhealthy signals include an AGV missing from the expected roster, shown as unmapped, inconsistent zone or location state, or red or exception entries associated with fleet membership. Healthy signals are a coherent roster, mapped AGVs, and consistent zone and location state. Inconclusive means the RMS table is unreadable or RMS and WCS/SSMS evidence disagree.
- **Runbook placeholder:** Procedure needed to inspect RMS roster and map views for missing, unmapped, or abnormal AGVs and to corroborate robot, location, cell-code, and zone state through read-only WCS/SSMS robotics data. The procedure should identify whether the fleet membership and mapping state are coherent without changing database or configuration state.
- **Expects capability:** device_roster_state
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Support suspected that AGVs had not been removed and added correctly, and the case resolution stated that a removed robot was shown as not mapped."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_2",
    "quote_or_summary": "Support suggested the robots may not have been removed and added properly, causing tasking problems."
  },
  {
    "page_ref": "case_228723:page_12",
    "quote_or_summary": "Resolution details state that the removed robot was shown as not mapped."
  },
  {
    "page_ref": "case_228723:page_6",
    "artifact_id": "artifact_incident_228723_page_006_embedded_image_01",
    "quote_or_summary": "RMS screenshot contains red-highlighted table entries, but exact values are unreadable."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_006_embedded_image_01",
  "artifact_incident_228723_page_012_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228723_event_004",
  "incident_228723_event_005",
  "incident_228723_event_008",
  "incident_228723_event_022",
  "incident_228723_event_023"
]
```

## node_3 — Perform authorized AGV isolation or roster recovery

- **Node type:** `procedure_reference`
- **Intent:** Use the approved recovery path for an AGV that is confirmed to be unmapped, incorrectly rostered, or otherwise preventing normal fleet operation.
- **Expected result:** The authorized site operator or L2 support observes the affected AGV's physical and RMS state before and after the approved action. Progress is indicated when the AGV is safely isolated or recovered, its RMS roster state is coherent, and the affected workflow can begin normal pairing. Failure is indicated by an unsuccessful remove or recovery action, persistent abnormal roster state, or continued unsafe physical obstruction. Inconclusive means the action outcome or system-side state cannot be verified.
- **Runbook placeholder:** Procedure needed for authorized AGV isolation, removal, or recovery using the physical-floor process and the applicable RMS or OptiSweep/WCS API capability, including safety preconditions, role limits, system-side roster expectations, and post-action RMS confirmation. Exact physical handling and API operations belong in the supporting runbook.
- **Expects capability:** agv_physical_recovery, device_roster_state
- **Expects surface:** physical_floor, rms_ui, wcs_api
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"The site removed an AGV from the system and placed it on a charger; the system was later reported to function again."
```

### Stop or escalation note

```json
"Stop if the AGV cannot be handled safely, authorization is unclear, the system-side operation fails, or the roster remains inconsistent after the approved recovery path."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_10",
    "artifact_id": "artifact_incident_228723_page_010_embedded_image_01",
    "quote_or_summary": "Site removed an AGV from the system and placed it on charger; the system reportedly began functioning again."
  },
  {
    "page_ref": "case_228723:page_3",
    "quote_or_summary": "Support noted that remove/add handling may require moving the robot through the hospital."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_010_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228723_event_006",
  "incident_228723_event_007",
  "incident_228723_event_009",
  "incident_228723_event_016",
  "incident_228723_event_022"
]
```

## node_4 — Investigate hospital-lane diversion when roster state appears healthy

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether unexpected hospital routing remains the active observable symptom after no clear roster or mapping mismatch is found.
- **Expected result:** The site operator observes the hospital lane UI and the AMR routing behavior, while L1 or L2 support compares the RMS destination or fleet view. An unhealthy signal is repeated AMR diversion to the hospital or a hospital-lane alarm while the affected zone still cannot obtain a pair. A healthy signal is normal routing and no hospital diversion. Inconclusive means the site cannot observe the lane or the destination state is not visible in RMS.
- **Runbook placeholder:** Procedure needed to inspect the Hospital HMI or lane UI for diversion, alarm, or station-state indicators and to compare the affected AMR destination or fleet state in RMS. The procedure should distinguish normal hospital routing from persistent unexpected diversion without changing routing configuration.
- **Expects capability:** hospital_diversion
- **Expects surface:** hospital_hmi, rms_ui
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The incident description and support messages reported that replacement AMRs or every AMR were going to the hospital lane."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_2",
    "quote_or_summary": "Attempted replacement AMRs were reported as going to the hospital lane."
  },
  {
    "page_ref": "case_228723:page_12",
    "quote_or_summary": "Case description states that every AMR goes to the hospital."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_012_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228723_event_003",
  "incident_228723_event_020",
  "incident_228723_event_021"
]
```

## node_5 — Validate normal pairing and stable fleet operation

- **Node type:** `validation_gate`
- **Intent:** Confirm that the affected workflow has recovered and remains operational after the diagnostic or recovery path.
- **Expected result:** The site observes that the affected zone can obtain a pair and that AMRs resume expected routing. RMS should show coherent fleet and pairing state without active pair-fail or unmapped-robot indicators; when remotely attainable, WCS/SSMS should corroborate normal system or roster state. Healthy validation is successful pairing and stable operation during monitoring. Unhealthy validation is recurring pair failure, continued hospital diversion, or a new abnormal roster state. Inconclusive means recovery is reported but no live RMS or WCS/SSMS evidence is available.
- **Runbook placeholder:** Procedure needed to validate the affected zone's pairing state in RMS, confirm expected fleet and destination behavior, and corroborate system or roster state through read-only WCS/SSMS where available. Include a short stability-monitoring check and distinguish reported recovery from independently observable technical recovery.
- **Expects capability:** zone_pairing_state, fleet_system_status
- **Expects surface:** rms_ui, wcs_sql, site_interview
- **Preferred audience:** operator, L1_support, L2_support

### Source-supported description

```json
"The site reported that the system began functioning after AGV removal and remained operational during approximately ten minutes of monitoring."
```

### Stop or escalation note

```json
"Do not declare recovery when pairing remains unavailable, abnormal routing continues, or only case-closure status is available without operational confirmation."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_10",
    "artifact_id": "artifact_incident_228723_page_010_embedded_image_01",
    "quote_or_summary": "System reportedly began functioning and remained operational during approximately ten minutes of monitoring."
  },
  {
    "page_ref": "case_228723:page_12",
    "quote_or_summary": "Case summary reports that the system was functional again after robot removal."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_010_embedded_image_01",
  "artifact_incident_228723_page_012_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228723_event_011",
  "incident_228723_event_016",
  "incident_228723_event_024"
]
```

## node_6 — Stop when the supported recovery path does not restore operation

- **Node type:** `escalation_gate`
- **Intent:** Hand off when the pairing failure, roster inconsistency, unsafe physical condition, or abnormal hospital routing persists after the available supported checks and authorized recovery path.
- **Expected result:** L1 or L2 support observes persistent pair failure or abnormal routing in RMS and, where available, corroborates unresolved fleet or system state through WCS/SSMS. Escalation is warranted when recovery cannot be performed safely or authorizedly, RMS and WCS/SSMS disagree materially, or validation fails after the approved path. A healthy result is not expected at this stop gate; inconclusive evidence should also be handed off with the evidence package.
- **Runbook placeholder:** Procedure needed to prepare an escalation handoff containing RMS pairing and roster views, read-only WCS/SSMS corroboration when available, Hospital HMI observations, physical AGV state, recovery actions attempted, and validation outcomes. The procedure should define stop criteria and the responsible higher-level technical role without prescribing case-management or communication workflow.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The incident shows persistent issues during intermediate remove/add attempts and later support involvement before reported recovery; it does not establish a universal recovery outcome."
```

### Stop or escalation note

```json
"Escalate for unsafe or unauthorized physical handling, unresolved roster or mapping state, persistent pairing failure after supported recovery, or insufficient evidence to continue safely."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_7",
    "quote_or_summary": "Zone issues were still reported at one point after robot removal, before later recovery was reported."
  },
  {
    "page_ref": "case_228723:page_6",
    "artifact_id": "artifact_incident_228723_page_006_embedded_image_01",
    "quote_or_summary": "RMS evidence showed abnormal-looking entries, but exact details were unreadable."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_006_embedded_image_01",
  "artifact_incident_228723_page_010_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228723_event_008",
  "incident_228723_event_010",
  "incident_228723_event_015"
]
```

