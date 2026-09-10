# Stage 5 Playbook Candidate — Case 228723

- **Variant:** `prompt_a_one_per_incident`
- **Title:** AGV pairing failure with abnormal fleet roster or mapping state
- **Candidate ID:** `playbook_candidate_incident_228723_agv_pairing_roster_recovery`

## Playbook Context

Confirm the reported pairing and fleet symptoms, determine whether the fleet roster or mapping state is abnormal, use an authorized AGV isolation or removal procedure when supported, and validate that pairing and automated operation remain stable.

## node_1 — Confirm pairing failure and fleet behavior

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether the reported issue is an active zone pairing failure accompanied by abnormal AGV or AMR behavior.
- **Expected result:** The site or L1 support observes the affected zone and pairing behavior through site interview and RMS pairing or fleet views. Unhealthy evidence is an inability to obtain a pair, pairing-failure indication, or replacement robots routing unexpectedly to the hospital lane. Healthy evidence is normal pairing and normal robot routing. Inconclusive evidence is an unclear site description, unavailable RMS view, or symptoms that are localized to a physical obstruction without a confirmed pairing failure.
- **Runbook placeholder:** Procedure needed to confirm with the site which affected zone cannot obtain a pair, whether AMRs are actively routing to the hospital lane or remaining unavailable, and whether the issue followed recent robot replacement or add/remove activity. In RMS, inspect the affected zone pairing view and fleet status overview for pairing-failure or abnormal-routing indicators.
- **Expects capability:** zone_pairing_state, fleet_system_status
- **Expects surface:** rms_ui, site_interview
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The site reported that a zone was unable to get a pair, that replacement AMRs were going to the hospital lane, and that the ACB system was down."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_1",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "support_type": "teams_message",
    "quote_or_summary": "Site reports under zone 5, they're unable to get a pair."
  },
  {
    "page_ref": "case_228723:page_12",
    "artifact_id": "artifact_incident_228723_page_012_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "support_type": "artifact_ocr",
    "quote_or_summary": "Description says zone 5 unable to get a pair; replacement AMRs go to the hospital."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_012_embedded_image_01",
  "artifact_incident_228723_page_012_full_page_01"
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

## node_2 — Check AGV roster and mapping consistency

- **Node type:** `diagnostic_decision`
- **Intent:** Determine whether an AGV roster, mapping, location, or membership inconsistency is present after replacement or add/remove activity.
- **Expected result:** L1 support or L2 support observes the RMS roster and map state, with L2 support optionally corroborating through read-only WCS database / SSMS views. Unhealthy evidence is an unmapped or missing robot, a zone or location mismatch, abnormal fleet membership, or red exception entries associated with roster state. Healthy evidence is a roster that matches the expected fleet and coherent robot location, zone, and mapping state. Inconclusive evidence is unreadable RMS detail, unavailable SSMS data, or inability to distinguish a roster issue from a physical or mechanical issue.
- **Runbook placeholder:** Procedure needed to inspect the AGV roster, map membership, robot location, zone, and cell or lattice mapping in RMS, with read-only WCS database / SSMS corroboration of robot and robot-location state when remotely attainable. The procedure should distinguish an unmapped or mismatched robot from a normal low-battery or charging condition.
- **Expects capability:** device_roster_state
- **Expects surface:** rms_ui, wcs_sql
- **Preferred audience:** L1_support, L2_support

### Source-supported description

```json
"Internal discussion suggested that robots may not have been removed and added properly, and the case resolution stated that the removed robot was shown as not mapped. The RMS screenshots showed unreadable red-highlighted exception entries."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_2",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "support_type": "teams_message",
    "quote_or_summary": "Support discussion suggested the robots may not have been removed and added properly."
  },
  {
    "page_ref": "case_228723:page_12",
    "artifact_id": "artifact_incident_228723_page_012_full_page_01",
    "chunk_id": "stage4_artifact_chunk_002",
    "support_type": "artifact_ocr",
    "quote_or_summary": "Resolution details state that the removed robot was shown to not be mapped."
  },
  {
    "page_ref": "case_228723:page_6",
    "artifact_id": "artifact_incident_228723_page_006_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "support_type": "artifact_visual",
    "quote_or_summary": "RMS status tables contain red-highlighted entries, but exact fields are unreadable."
  }
]
```

### Related artifacts

```json
[
  "artifact_incident_228723_page_006_embedded_image_01",
  "artifact_incident_228723_page_010_embedded_image_01",
  "artifact_incident_228723_page_012_embedded_image_01"
]
```

### Related events

```json
[
  "incident_228723_event_004",
  "incident_228723_event_008",
  "incident_228723_event_022",
  "incident_228723_event_023"
]
```

## node_3 — Use authorized AGV isolation or removal recovery when roster state is abnormal

- **Node type:** `procedure_reference`
- **Intent:** Perform an approved site-side or system-side AGV isolation or removal action when an abnormal roster or mapping state is supported and the responsible role is authorized.
- **Expected result:** The operator observes that the affected AGV is physically safe and isolated or placed in an appropriate charging or holding state. L1 or L2 support observes the corresponding RMS roster state and, where authorized, the WCS API or RMS state after the action. Recovery-completed evidence is that the abnormal robot is no longer interfering with fleet operation and the roster reflects the intended state. Unhealthy evidence is that the robot remains active in an abnormal state, the remove or recovery action fails, or the fleet remains unable to pair. Inconclusive evidence is missing site confirmation or unavailable RMS status.
- **Runbook placeholder:** Procedure needed for authorized AGV isolation, removal, or recovery involving the physical floor and RMS or OptiSweep / WCS API state, including safety preconditions, role limits, and confirmation that the affected robot is placed in an appropriate charger or holding state. Do not make database or configuration changes without an approved procedure.
- **Expects capability:** agv_physical_recovery, device_roster_state
- **Expects surface:** physical_floor, rms_ui, wcs_api
- **Preferred audience:** operator, L2_support

### Source-supported description

```json
"The site removed an AGV from the system and placed it on a charger; the source later reported that operation began working again. The packet does not provide exact removal steps."
```

### Stop or escalation note

```json
"Stop if physical conditions are unsafe, the required authorization is unavailable, or the robot cannot be safely isolated or removed using an approved procedure."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_10",
    "artifact_id": "artifact_incident_228723_page_010_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "support_type": "teams_message",
    "quote_or_summary": "Site removed the robot from the system, placed it on charger, and reported that the system began functioning again."
  },
  {
    "page_ref": "case_228723:page_12",
    "artifact_id": "artifact_incident_228723_page_012_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "support_type": "artifact_visual",
    "quote_or_summary": "Resolution details report removal of a robot shown as not mapped."
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
  "incident_228723_event_007",
  "incident_228723_event_009",
  "incident_228723_event_016",
  "incident_228723_event_022"
]
```

## node_4 — Validate pairing and stable automated operation

- **Node type:** `validation_gate`
- **Intent:** Confirm that the affected workflow has recovered after the AGV isolation or removal action and remains stable during observation.
- **Expected result:** The site observes successful pairing and normal AMR movement through the affected workflow, while L1 or L2 support checks RMS fleet and pairing views. Healthy evidence is normal pairing, expected robot routing, no persistent abnormal roster indicator, and continued operation during a short monitoring period. Unhealthy evidence is recurring pair failure, robots continuing to divert unexpectedly to the hospital, or a robot remaining in an abnormal state. Inconclusive evidence is only a case-status update or verbal recovery report without direct operational or RMS confirmation.
- **Runbook placeholder:** Procedure needed to validate pairing and fleet recovery through the RMS pairing and fleet-status views, confirm the affected workflow with the site, and monitor for recurrence after an AGV isolation or removal action. The procedure should distinguish direct operational confirmation from an administrative case closure or narrative recovery report.
- **Expects capability:** zone_pairing_state, fleet_system_status, device_roster_state
- **Expects surface:** rms_ui, site_interview
- **Preferred audience:** operator, L1_support

### Source-supported description

```json
"The site reported that the system began functioning after robot removal and remained operational during approximately ten minutes of monitoring, but readable live RMS details were not available."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_10",
    "artifact_id": "artifact_incident_228723_page_010_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "support_type": "validation_evidence",
    "quote_or_summary": "After robot removal, the system reportedly began functioning and remained operational during approximately ten minutes of monitoring."
  },
  {
    "page_ref": "case_228723:page_12",
    "artifact_id": "artifact_incident_228723_page_012_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "support_type": "artifact_visual",
    "quote_or_summary": "The system was reported functional again after removal of the unmapped robot."
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
  "incident_228723_event_011",
  "incident_228723_event_016",
  "incident_228723_event_024"
]
```

## node_5 — Stop when the supported recovery path is incomplete or validation fails

- **Node type:** `escalation_gate`
- **Intent:** Hand off when safe authorization, reliable diagnostic evidence, or stable recovery is unavailable.
- **Expected result:** L1 or L2 support identifies that the pairing failure persists, the roster or mapping state cannot be interpreted, the approved AGV recovery action cannot be completed safely, or validation fails after recovery. A complete handoff contains the site-observed symptoms, RMS roster or pairing evidence, any available read-only WCS database / SSMS corroboration, the action attempted, and the resulting operational state.
- **Runbook placeholder:** Procedure needed to prepare an escalation handoff for unresolved AGV pairing or roster recovery, including RMS pairing and fleet evidence, read-only WCS database / SSMS findings when available, physical safety status, recovery actions attempted, validation results, and explicit stop criteria.
- **Expects capability:** None
- **Expects surface:** None
- **Preferred audience:** L2_support, L3_support

### Source-supported description

```json
"The incident evidence shows incomplete and conflicting diagnostic detail, unreadable RMS status fields, and a reported recovery that required site-side action and monitoring."
```

### Stop or escalation note

```json
"Escalate for unresolved pairing failure, unsafe or unauthorized physical action, failed system-side recovery, or persistent abnormal roster or mapping state."
```

### Source references

```json
[
  {
    "page_ref": "case_228723:page_6",
    "artifact_id": "artifact_incident_228723_page_006_embedded_image_01",
    "chunk_id": "stage4_artifact_chunk_001",
    "support_type": "artifact_visual",
    "quote_or_summary": "RMS table details were unreadable and exact abnormal states could not be confirmed."
  },
  {
    "page_ref": "case_228723:page_7",
    "artifact_id": null,
    "chunk_id": "stage4_page_chunk_001",
    "support_type": "teams_message",
    "quote_or_summary": "The issue was still reported at one point after robot removal, before later recovery was reported."
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
  "incident_228723_event_016"
]
```

