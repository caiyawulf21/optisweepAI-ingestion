# Hospital tote-induct or site-flow disruption with AGV state anomalies

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_flow` |
| Case ID | `223554` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital station cannot add or induct totes.
- Totes can be removed but cannot be added at the hospital area.
- A robot or AGV is reported in a shut down state.
- The site cannot start sort or goes down during sort.
- Hospital backlog or abnormal tote flow to the hospital area is reported.

## Affected Systems

- ACB hospital station
- Hospital Lane
- AGV hospital station
- AGVs and robot locations
- Totes and tote associations
- OptiSweep services
- Tippers
- Sort operation

## Nodes

### 1 — Confirm the observable hospital and site-flow impact (`diagnostic_decision`)

**Objective:** Determine whether the current report is an active hospital tote-induct problem, a broader sort disruption, or a localized condition that does not match this response path.

**Why this check is next:** The case subject and closure summary describe inability to induct totes, while Teams messages describe inability to add totes and a later site-down or sort-start failure.

**Action:**

Confirm with the site and, when available, the Hospital HMI whether totes can currently be added/inducted and removed at the affected hospital station, whether the reported robot/station is in a shut down state, and whether sort can start and remain running.

**Suggested database check:**

- **Database:** robotics
  - **Model:** HospitalDatabaseModel
  - **Inspect:** Hospital entrance and exit queue locations.
  - **Inspect:** Hospital tote drop-off location.
- **Database:** sorter_sweeper
  - **Model:** HospitalTagsModel
  - **Inspect:** Whether tag is in or out; drives action.
  - **Inspect:** List of hospital controller tags.
  - **Inspect:** Modular typed value columns (string/bool) selected by variable type.
- **Database:** robotics
  - **Model:** RobotDatabaseModel
  - **Inspect:** Robot state enum (Tipper/Hospital/Charger/Sorter/GLD/ShutDown family).
  - **Inspect:** Tote currently associated with robot.
  - **Inspect:** Assigned sorter side.

**Healthy:** Totes can be added/inducted and removed at the hospital station, and sort starts and remains running normally.

**Unhealthy:** Hospital tote addition/induction is unavailable, the station/robot reports a shut down condition, or sort cannot start and/or stops during operation; hospital backlog continues to increase.

**Inconclusive:** The site cannot identify the affected workflow and/or the Hospital HMI/status evidence is unreadable or missing.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** operator, L1_support

**Runbook Links:**

- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.

**Source Evidence:**

- They can remove totes but cannot add; surrounding HMI-style evidence is discussed.
- Client unable to induct totes at the station; robot in a shut down state.
- Site reported down and unable to start sort or went down during sort.

**Branches:**

- `unhealthy` → `node_2` when Hospital induct blocked or sort cannot start/sustain
- `healthy` → `` when Hospital add/remove works and sort operating normally
- `inconclusive` → `` when Cannot confirm current state

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Check for AGV location, roster, and tote-association anomalies (`diagnostic_decision`)

**Objective:** Determine whether the reported hospital-flow problem coincides with an AGV in an unexpected location, duplicate occupancy, disconnected tote, or residual tote association.

**Why this check is next:** Teams messages and annotated HMI-style images describe an AGV in an unexpected location, two AGVs under a rack, and possible disconnected or residual tote associations.

**Action:**

Compare the affected hospital/expected AGV locations and station/rack occupancy with the displayed HMI evidence and the system/fleet/API evidence to identify whether anomalies exist (unexpected location, duplicate rack occupancy, missing expected AGV, residual/disconnected tote association).

**Suggested database check:**

- **Database:** robotics
  - **Model:** RobotDatabaseModel
  - **Inspect:** Robot state enum (Tipper/Hospital/Charger/Sorter/GLD/ShutDown family).
  - **Inspect:** Tote currently associated with robot.
- **Database:** robotics
  - **Model:** RobotLocationDatabaseModel
  - **Inspect:** Station / workstation number for the location.
  - **Inspect:** Whether the location is currently occupied.
  - **Inspect:** Zone associated with the location (sorter-side zones).
- **Database:** robotics
  - **Model:** AgvActiveErrorDatabaseModel
  - **Inspect:** Robot code.
  - **Inspect:** Active error code.
  - **Inspect:** Error description.

**Healthy:** AGVs occupy expected locations and no disconnected/residual tote association is reported; hospital station tote state matches physical/operational intent.

**Unhealthy:** AGVs are in unexpected locations, duplicate rack occupancy appears, an expected rack/location is missing AGV presence, or a disconnected/residual tote association persists; hospital tote state cannot be reconciled with displayed AGV state.

**Inconclusive:** Identifiers/locations/tote associations cannot be confirmed due to unreadable legends or inability to compare physical vs displayed states.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.

**Source Evidence:**

- This AGV doesn't belong here; two AGVs were under the rack in the same zone.
- AGV with disconnected tote was in the system; other AGVs were under the rack.
- Aveva was used to remove an AGV from a zone and add a tote to a station.

**Branches:**

- `unhealthy` → `node_4` when Unexpected AGV location or residual/disconnected tote association indicated
- `inconclusive` → `node_3` when No anomaly / evidence cannot confirm anomaly

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 3 — Determine whether the hospital-station service condition is contributing (`diagnostic_decision`)

**Objective:** Determine whether the reported AGV hospital-station server or OptiSweep service condition is present and sufficiently correlated with the hospital or site-flow symptoms.

**Why this check is next:** The source documents AGV hospital-station server issues, a need to reset services, and a closure statement that OptiSweep services were reset before Hospital Lane was restarted.

**Action:**

Review the current health of the hospital-station server and OptiSweep/WCS services using Windows Events/Services (when authorized) and correlate that with current Hospital Lane/HMI responsiveness; do not assume historical reset implies current fault.

**Suggested database check:**

- **Database:** robotics
  - **Model:** HospitalDatabaseModel
  - **Inspect:** Hospital entrance and exit queue locations.
  - **Inspect:** Hospital tote drop-off location.
- **Database:** sorter_sweeper
  - **Model:** HospitalTagsModel
  - **Inspect:** Whether tag is in or out; drives action.
  - **Inspect:** List of hospital controller tags.
  - **Inspect:** Modular typed value columns (string/bool) selected by variable type.
- **Database:** robotics
  - **Model:** RobotDatabaseModel
  - **Inspect:** Robot state enum (Tipper/Hospital/Charger/Sorter/GLD/ShutDown family).
  - **Inspect:** Tote currently associated with robot.
  - **Inspect:** Assigned sorter side.

**Healthy:** The relevant service and the hospital interface respond normally; no current abnormal service condition is evident.

**Unhealthy:** Current evidence shows an AGV hospital-station server / OptiSweep service abnormality, and Hospital Lane/HMI is unresponsive or aligns with the reported disruption.

**Inconclusive:** Only a historical note says services need reset; current service health and named service/host details are not available.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1` (low, support, score=0.5705, boosted=0.7705) — Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.

**Evidence Collection Procedures:**

- `proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1` — Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures (L2_support): Use Windows Event Viewer / services to inspect the live Windows Application and System logs, then verify the current OptiSweep service state. Correlate WCSWebApplication database-command errors around 6:35-6:36 AM with OptiSweep Service Control Manager Event 7031 and the current Windows Services status before further recovery.

**Source Evidence:**

- AGV hospital station is having server issues; services need to be reset.
- Resolution details say OptiSweep services were reset and the site restarted Hospital Lane.

**Branches:**

- `unhealthy` → `node_4` when Current service or hospital-lane abnormality indicated
- `healthy` → `None` when Service/hospital-lane checks healthy or evidence historical/inconclusive

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures (`proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1`)</summary>

##### Runbook: Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures

- **Procedure ID:** `proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use Windows Event Viewer / services to inspect the live Windows Application and System logs, then verify the current OptiSweep service state. Correlate WCSWebApplication database-command errors around 6:35-6:36 AM with OptiSweep Service Control Manager Event 7031 and the current Windows Services status before further recovery.

**When To Use:**
Use Windows Event Viewer / services when the live OptiSweep or WCS-backed system is unresponsive, when clustered WCSWebApplication errors are suspected, or when a service crash or restart must be correlated with the incident. Inspect the live Windows Application and System logs and current Windows Services state before performing further recovery.

**Safety Notes:**

- This is an inspection and diagnostic procedure; do not infer root cause from clustered errors.
- Automatic restart configuration records an intended Windows action, not confirmed service recovery.
- Do not perform further recovery based only on the historical service-state screenshot.

- **Source:** `incident_case` / `source_case_228086`

**Procedure Steps:**

###### Step 1 — Inspect the Windows Event Viewer Application log

**Responsible role:** L2_support

**Instruction:**
In Windows Event Viewer / services, open Windows Logs > Application and inspect entries around 2/20/2026 6:35:24-6:36:07 AM. Open the WCSWebApplication error details, including Event ID 20102, and check nearby Application Error or Windows Error Reporting entries.

**Healthy condition:**
No new or repeated WCSWebApplication or related application errors appear in the current inspection window.

**Expected result:**
The Application log shows whether WCSWebApplication Event ID 20102 with 'Failed executing DbCommand (1,840ms)' and nearby clustered application errors are present in the inspected time window.

**Step Images:**

![artifact_incident_228086_page_027_embedded_image_01](assets/abd43e133aa30f1d.jpeg)

*Windows Event Viewer Application log showing Windows Error Reporting Event 1001 and clustered WCSWebApplication and Application Error entries around 6:36 AM.*

![artifact_incident_228086_page_028_embedded_image_01](assets/d4f3abbd8bd09df2.jpeg)

*Windows Event Viewer Application log showing WCSWebApplication Event ID 20102 and the 'Failed executing DbCommand (1,840ms)' message.*

---

###### Step 2 — Inspect the OptiSweep termination event

**Responsible role:** L2_support

**Instruction:**
In Windows Event Viewer / services, select Windows Logs > System and open the Service Control Manager event for OptiSweep. Check for Event ID 7031, Level Error, and inspect whether the message states that OptiSweep terminated unexpectedly and Windows planned to restart it after 60000 milliseconds.

**Healthy condition:**
No new or repeated OptiSweep Event ID 7031 termination is present in the current System log inspection.

**Expected result:**
The System log identifies whether an OptiSweep Event ID 7031 termination is present and whether the event contains the 60000-millisecond restart message.

**Step Images:**

![artifact_incident_228086_page_029_embedded_image_01](assets/dabb6bbd62f07c7c.png)

*Windows Event Viewer System log showing OptiSweep Service Control Manager Event 7031, unexpected termination, and the planned 60000-millisecond restart.*

---

###### Step 3 — Verify the current OptiSweep service state

**Responsible role:** L2_support

**Instruction:**
In Windows Event Viewer / services, open Windows Services, select OptiSweep, and inspect the current Status and Startup Type.

**Healthy condition:**
OptiSweep is currently shown as Running and its Startup Type is shown as Automatic.

**Expected result:**
Windows Services displays the current OptiSweep Status and Startup Type, allowing the live service state to be compared with the Event Viewer evidence.

**Step Images:**

![artifact_incident_228086_page_019_embedded_image_01](assets/3832c5ce44b05a86.png)

*Windows Services showing OptiSweep selected with Status Running and Startup Type Automatic.*

---

###### Step 4 — Correlate Windows Event Viewer / services evidence with the live incident state

**Responsible role:** L2_support

**Instruction:**
Compare the timestamps and live entries in Windows Event Viewer / services with the current incident state and the current OptiSweep status in Windows Services. Do not treat the configured automatic restart as proof that recovery completed.

**Healthy condition:**
The current Windows Services state is Running and the current Event Viewer inspection shows no new or repeated relevant errors.

**Expected result:**
The diagnostic conclusion separately identifies the observed WCSWebApplication errors, any OptiSweep Event 7031 termination, and the current OptiSweep service state.

---

**Success Criteria:**

- Windows Event Viewer / services inspection identifies whether current Application log evidence includes WCSWebApplication Event ID 20102 or clustered related errors.
- Windows Event Viewer / services inspection identifies whether an OptiSweep Event ID 7031 termination is present and whether a 60000-millisecond restart was configured.
- Windows Services shows the current OptiSweep Status and Startup Type.
- The diagnostic conclusion does not claim recovery or root cause without live supporting evidence.

**Failure Conditions:**

- WCSWebApplication Event ID 20102 or clustered application errors are present or repeating in the current inspection.
- OptiSweep Event ID 7031 is present or repeating in the current System log inspection.
- OptiSweep is not shown as Running in Windows Services.
- The available evidence only shows a configured restart and does not establish that recovery completed.
- The evidence is insufficient to establish a definitive root cause.


</details>

</details>

---

### 4 — Apply authorized high-level recovery for the identified condition (`procedure_reference`)

**Objective:** Use the approved recovery procedure appropriate to the confirmed condition: service or lane recovery, correction of supported AGV/tote state, or controlled physical AGV handling.

**Why this check is next:** Historical evidence describes service reset and Hospital Lane restart, API dog removal of tote state, Aveva-based AGV/tote state correction, and removal of several AGVs during recovery. These actions are preserved as high-level source evidence, not procedural instructions.

**Action:**

Execute the authorized high-level recovery corresponding to the confirmed condition (either service/lane recovery, or authorized AGV/tote state correction) using the approved procedure; do not perform any unsupported reset or any physical AGV handling unless role limits and safety/authorization conditions are satisfied and the responsible recovery procedure is selected.

**Healthy:** The selected authorized recovery completes and the affected service/lane or AGV/tote state is corrected without introducing additional discrepancies.

**Unhealthy:** Recovery cannot be completed or the abnormal state persists; recovery introduces additional tote/AGV discrepancies.

**Inconclusive:** The incident packet does not identify exact service names, authorization boundaries, or safe physical conditions needed for recovery.

**Procedure Reference:**

- **Trigger condition:** Authorized support or site personnel complete the applicable approved recovery and record whether it completed. Recovery signal: the source-supported service or lane recovery is completed, or the affected AGV/tote state is corrected through the approved API/Aveva or physical procedure. Unsuccessful signal: the action cannot be completed, the state remains abnormal, or the action introduces additional tote or AGV discrepancies. Inconclusive: the source does not identify the exact service, authorization, or safe physical conditions required.
- **Selected procedure:** Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV) (`proc_recover_from_agv_fault_during_exchange_recovery_v1`)
- **Selection rationale:** Retrieval match (0.6764, boosted 0.8464).
- **Success confirmation:** Faulted AGV is removed from RMS.
- **Failure boundary:** Trailing AGV does not backfill and cannot be removed/cleared as described.

**Prerequisites:**

- rms_ui

**Safety checks:**

- Perform an RMS E-stop as the first recovery action for this fault scenario.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support, operator

**Runbook Links:**

- `proc_recover_from_agv_fault_during_exchange_recovery_v1` (low, support, score=0.6764, boosted=0.8464) — Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Evidence Collection Procedures:**

- `proc_recover_from_agv_fault_during_exchange_recovery_v1` — Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV) (L2_support): Restore exchange flow after an AGV faults while leaving by stopping RMS, removing the faulted AGV from the RMS, optionally removing the trailing AGV if it does not backfill, then introducing a new tote and placing an empty AGV in the affected zone.

**Source Evidence:**

- API dog was used to remove inducted and hospital tote state; several AGVs were taken out to restore operation.
- Aveva was used to remove an AGV from a zone and add a tote to a station.
- OptiSweep services were reset and Hospital Lane was restarted.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Recovery control surfaces + post-recovery read-only verification): Approved recovery completed and appropriate state restored.
- `unhealthy` (observer=remote; tool=Hospital HMI + RMS/fleet view read-only evidence): Recovery unsuccessful; abnormal state persists or new discrepancies appear.
- `inconclusive` (observer=remote; tool=Notes + authorization check): Cannot safely execute/verify due to missing authorization/service/physical safety details.

**Branches:**

- `healthy` → `node_5` when Authorized recovery completed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV) (`proc_recover_from_agv_fault_during_exchange_recovery_v1`)</summary>

##### Runbook: Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV)

- **Procedure ID:** `proc_recover_from_agv_fault_during_exchange_recovery_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Restore exchange flow after an AGV faults while leaving by stopping RMS, removing the faulted AGV from the RMS, optionally removing the trailing AGV if it does not backfill, then introducing a new tote and placing an empty AGV in the affected zone.

**When To Use:**
Use when an AGV faults during exchange while leaving and you need to restore exchange flow by removing the faulted AGV from RMS, handling backfill behavior, and reintroducing the correct tote + empty-AGV state in the affected zone.

**Safety Notes:**

- Perform an RMS E-stop as the first recovery action for this fault scenario.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), perform an E-stop of the RMS.

**Healthy condition:**
RMS remains stopped (no exchange movement continuing) while you proceed with AGV removal actions.

**Expected result:**
RMS is in an E-stopped state (fleet movement is stopped) on the RMS / fleet status UI.

---

###### Step 2 — Remove the faulted AGV that is lifted and faulted out while leaving

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), identify the AGV that is lifted and has faulted out while leaving, then remove that AGV from the RMS using the AGV API Controls flow referenced by the manual.

**Healthy condition:**
Only the faulted AGV is removed; the RMS remains stopped while you confirm the removal is reflected in the RMS UI.

**Expected result:**
The faulted AGV is removed from the RMS (it no longer appears as an active AGV in the RMS fleet context for the affected zone).

**Step Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/d87070d22301b81d.jpeg)

*HMI screenshot showing the faulted AGV with tote state (used as visual context for the faulted condition during exchange recovery).*

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*RMS screen showing an AGV fault example (visual context for RMS fault screens; not specific to this exact exchange-fault step).*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*AGV API Controls screen showing controls such as Remove AGV / Recover AGV / Pause All AGVs / Resume All AGVs (used for the AGV removal action referenced by the recovery procedure).*

---

###### Step 3 — Check backfill; remove trailing AGV if it does not backfill

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), check whether the AGV behind the faulted AGV backfills into the expected position. If it does not backfill, remove that trailing AGV as well using the same AGV API Controls flow referenced by the manual.

**Healthy condition:**
Backfill occurs as expected, or the trailing AGV is successfully removed so the zone can be re-established with the correct tote + empty AGV state.

**Expected result:**
Either (a) the AGV behind backfills into the expected position, or (b) the trailing AGV is removed from RMS when it does not backfill.

---

###### Step 4 — Introduce new tote and place an empty AGV in the affected zone

**Responsible role:** L2_support

**Instruction:**
Introduce a new tote at the faulted location and place an empty AGV in that zone using the RMS UI actions referenced by the manual.

**Healthy condition:**
The affected exchange location shows the newly introduced tote and an empty AGV in the zone (exchange can resume).

**Expected result:**
A newly introduced tote is present at the affected location, and an empty AGV is placed in that zone so exchange can proceed.

**Step Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/ec83d895fff08cd8.jpeg)

*RMS screen for adding an AGV to a zone when no empty AGV is present (visual support for re-establishing empty AGV state in the affected zone).*

---

**Success Criteria:**

- Faulted AGV is removed from RMS.
- If the AGV behind did not backfill, the trailing AGV is also removed.
- Affected exchange location has a newly introduced tote and an empty AGV placed in the correct zone so exchange can proceed.

**Failure Conditions:**

- Trailing AGV does not backfill and cannot be removed/cleared as described.
- New tote and/or empty AGV cannot be introduced into the correct zone.


</details>

</details>

---

### 5 — Validate hospital flow, AGV state, and sustained sort recovery (`validation_gate`)

**Objective:** Confirm that recovery restored the affected workflow without leaving residual AGV, tote, or station-state anomalies.

**Why this check is next:** The source reports that totes could again be added and removed, robots were re-added and running, movement started, and the system was running by the later recovery updates.

**Validate:**

Validate that hospital tote flow is restored and remains stable, that AGV roster/location and tote association are consistent, and that sort resumes and sustains operation (not just transient movement).

**Success:** Totes can be added/removed; Hospital Lane accepts normal flow; AGVs are consistent with expected locations; movement resumes and sort starts and remains stable; no disconnected/residual tote association persists.

**Failure:** Hospital tote addition remains blocked, AGVs remain stopped/misplaced, disconnected tote state persists, or sort fails again during monitoring.

**Inconclusive:** Only generic 'system is running' is available without confirming hospital tote-flow behavior and residual AGV/tote consistency or without stable observation period.

**Validation Gate:**

**Validation checklist:**

- Confirm the owning service remains running and stable.
- Confirm the supported API or control endpoint responds.
- Compare database or fleet state with the live HMI or site-observed state.
- Observe the affected workflow for recurrence during the stated observation window.

**Required evidence sources:** Service state, API response, fleet or database state, site observation

**Stable-operation observation:** Observe the affected workflow for recurrence during the defined observation window; a reachable screen or successful request alone is not recovery.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.

**Source Evidence:**

- Site could add and remove totes again; all robots were re-added and back up and running.
- Movement had started.
- System was running; incident summary states issue resolved by approximately 9 PM ET.

**Branches:**

- `healthy` → `` when Totes add/remove works and stable sort recovery confirmed
- `unhealthy` → `` when Tote add remains blocked or anomalies persist or sort fails again

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Hospital induct blocked or sort cannot start/sustain | `node_2` |
| `node_1` | `healthy` | Hospital add/remove works and sort operating normally | `` |
| `node_1` | `inconclusive` | Cannot confirm current state | `` |
| `node_2` | `unhealthy` | Unexpected AGV location or residual/disconnected tote association indicated | `node_4` |
| `node_2` | `inconclusive` | No anomaly / evidence cannot confirm anomaly | `node_3` |
| `node_3` | `unhealthy` | Current service or hospital-lane abnormality indicated | `node_4` |
| `node_3` | `healthy` | Service/hospital-lane checks healthy or evidence historical/inconclusive | `` |
| `node_4` | `healthy` | Authorized recovery completed | `node_5` |
| `node_5` | `healthy` | Totes add/remove works and stable sort recovery confirmed | `` |
| `node_5` | `unhealthy` | Tote add remains blocked or anomalies persist or sort fails again | `` |
