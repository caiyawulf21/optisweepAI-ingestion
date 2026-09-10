# Hospital station cannot induct/add totes; site reports shut down / sort disruption

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_totes_server_reset` |
| Case ID | `223554` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital station cannot induct/add totes
- “Robot is in a shut down state” (site-reported)
- Site reports it can’t start sort or is down / disrupted during sort
- Operators can remove totes but cannot add totes at the hospital
- Backlog builds in the hospital area; tote flow to hospital is disrupted

## Affected Systems

- ACB hospital station
- AGV hospital station
- Hospital lane
- OptiSweep services
- Robots / AGVs
- Totes
- Tippers (operator station context during recovery)

## Nodes

### 1 — Confirm hospital tote induction/add failure and whether it aligns with abnormal hospital/AGV state (`diagnostic_decision`)

**Intent:** Determine whether the reported hospital station inability to induct/add totes is currently reproducible and whether RMS/WCS/HMI shows abnormal hospital lane/tote/AGV state that would explain the induction failure.

**Expects capability:** agv_active_errors, hospital_diversion, zone_pairing_state
**Expects surface:** hospital_hmi, rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.7151, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (low, support, score=0.7336, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_disconnected_agv_count_cause_v1` (low, support, score=0.6857, boosted=1.0) — Check RMS disconnected AGV count and identify likely disconnect cause (lost RMS comms vs turned off)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (read-only where available)): Hospital lane can accept induct/add requests and shows no active hospital obstruction/alarms; fleet/hospital indicators do not corroborate abnormal hospital/AGV/tote state.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (read-only where available)): Hospital lane is stuck/paused for induct/add or shows abnormal hospital state consistent with the symptom pattern; fleet/WCS corroborate the anomaly.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (attempt)): Hospital HMI state is unclear or evidence cannot be corroborated due to missing/unavailable RMS/WCS views.
- `escalate` (observer=remote; tool=Hospital HMI / RMS / WCS (attempt)): Safety-critical abnormality or required evidence surfaces are unavailable to make a safe call within scope.

**Branches:**

- `unhealthy` → `node_2` when Symptom corroborated as abnormal hospital/AGV/tote state
- `healthy` → `` when Pattern not corroborated
- `inconclusive` → `node_2` when Evidence inconclusive

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Check Overall System AGV Status popup for AGVs with destination errors (`proc_check_overall_system_agv_status_popup_agv_destination_errors_v1`)</summary>

##### Runbook: Check Overall System AGV Status popup for AGVs with destination errors

- **Procedure ID:** `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the live RMS / fleet status UI popup titled “Overall System AGV Status” to identify which AGVs currently have errors and review their Destination and Errors details. The popup shows a top section for all AGVs and a bottom section filtered to only AGVs with errors.

**When To Use:**
When you need to quickly determine which AGVs have active errors related to destination/error conditions and view their Destination and Errors details in the RMS fleet status UI.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS “Overall System AGV Status” popup

**Responsible role:** L1_support

**Instruction:**
In the RMS / fleet status UI (rms_ui), navigate to the popup/screen titled “Overall System AGV Status”.

**Healthy condition:**
The popup title “Overall System AGV Status” is visible and the popup is rendered with both top and bottom sections.

**Expected result:**
The “Overall System AGV Status” popup is displayed.

---

###### Step 2 — Confirm top section fields for all AGVs (ID, Status, Destination, Errors)

**Responsible role:** L1_support

**Instruction:**
In the “Overall System AGV Status” popup, check the top section table/list to confirm it includes fields/columns for ID, Status, Destination, and Errors.

**Healthy condition:**
The top section shows a detailed table/list for all AGVs with visible column headers/fields: ID, Status, Destination, Errors.

**Expected result:**
The top section displays the fields/columns “ID”, “Status”, “Destination”, and “Errors”.

---

###### Step 3 — Confirm bottom section is filtered to AGVs with errors

**Responsible role:** L1_support

**Instruction:**
In the “Overall System AGV Status” popup, check the bottom section to confirm it lists only AGVs with errors and includes additional error/destination detail for those AGVs.

**Healthy condition:**
The bottom section contains only error AGVs and additional detail is present for those error cases.

**Expected result:**
The bottom section lists only AGVs with errors (error cases) and shows additional detail for those error AGVs.

---

###### Step 4 — Record AGV IDs and their Destination/Errors from the error-only bottom section

**Responsible role:** L1_support

**Instruction:**
For each AGV listed in the bottom (error-only) section, record/verify the AGV ID and the associated Destination and Errors details displayed in the popup.

**Healthy condition:**
Each bottom-section row corresponds to an error case and includes the AGV ID plus Destination and Errors details.

**Expected result:**
You have a list of AGV IDs from the bottom section along with their displayed Destination and Errors values.

---

###### Step 5 — Escalate if popup fields are missing or error-only list behavior is inconsistent

**Responsible role:** L1_support

**Instruction:**
If the popup does not show the expected “Overall System AGV Status” title/fields (ID, Status, Destination, Errors) or if the bottom section does not correctly show only AGVs with errors, stop and escalate.

**Healthy condition:**
No escalation is required because the popup title/fields are present and the bottom section correctly reflects error-only AGVs.

**Expected result:**
Escalation is initiated when UI evidence is inconsistent with expected fields or filtering behavior.

---

**Success Criteria:**

- The “Overall System AGV Status” popup displays the expected fields: ID, Status, Destination, Errors in the top section.
- The bottom section lists only AGVs with errors and shows additional detail for those error AGVs.
- For each AGV in the bottom (error-only) section, the AGV ID and its Destination and Errors values are captured.

**Failure Conditions:**

- Popup fails to display expected fields (ID/Status/Destination/Errors).
- Bottom section is empty while the top section indicates any AGV has a non-empty Errors value.
- Bottom section does not behave as an error-only list.


</details>

<details><summary>Check Overall System Faults and Active AGV Faults on the Overall System RMS Page (`proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1`)</summary>

##### Runbook: Check Overall System Faults and Active AGV Faults on the Overall System RMS Page

- **Procedure ID:** `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Perform a first-pass live check on the RMS / fleet status UI (Geek+ RMS web page) to determine whether the system has any system faults (left side) and whether any AGVs have active faults (right side).

**When To Use:**
Use when a caller reports a potential fleet/system issue and you need a quick overview of (1) system faults and (2) any active AGV faults visible on the Overall System RMS page.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the Overall System RMS page in the RMS / fleet status UI

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (Geek+ RMS web page) for the site and navigate to the Overall System RMS page.

**Healthy condition:**
Both left and right fault areas are visible on the Overall System RMS page.

**Expected result:**
The Overall System RMS page loads and shows the two fault areas: system faults on the left and active AGV faults on the right.

---

###### Step 2 — Check the left-side “system faults” area

**Responsible role:** L1_support

**Instruction:**
On the Overall System RMS page, look at the left-side “system faults” area and determine whether any system faults are listed/present.

**Healthy condition:**
The left-side “system faults” area shows no system faults (empty/not showing faults).

**Expected result:**
You can state whether the left-side “system faults” area shows one or more fault entries or is empty/not showing faults at the time of the check.

---

###### Step 3 — Check the right-side “active AGV faults” area

**Responsible role:** L1_support

**Instruction:**
On the same Overall System RMS page, look at the right-side “active AGV faults” area and determine whether any active AGV faults are listed/present.

**Healthy condition:**
The right-side “active AGV faults” area shows no active AGV faults (empty/not showing faults).

**Expected result:**
You can state whether the right-side “active AGV faults” area shows one or more fault entries or is empty/not showing faults at the time of the check.

---

###### Step 4 — Report the displayed fault indications (or confirm none are displayed)

**Responsible role:** L1_support

**Instruction:**
If the left “system faults” area and/or the right “active AGV faults” area shows entries, report those fault indications to support. If both areas are empty/not showing faults, report that no system faults/active AGV faults are currently displayed on this page.

**Healthy condition:**
Report indicates both sides show no fault entries (no system faults and no active AGV faults displayed).

**Expected result:**
A clear statement is provided indicating whether system faults are present on the left and whether active AGV faults are present on the right at the time of the check.

---

**Success Criteria:**

- You verify the presence/absence of system faults in the left-side “system faults” area on the Overall System RMS page.
- You verify the presence/absence of active AGV faults in the right-side “active AGV faults” area on the Overall System RMS page.
- You report whether each side shows fault entries or is empty/not showing faults.

**Failure Conditions:**

- Left-side “system faults” area lists one or more system faults.
- Right-side “active AGV faults” area lists one or more active AGV faults.
- Overall System RMS page cannot be reached or does not load the content needed to view the left/right fault areas.


</details>

<details><summary>Check RMS disconnected AGV count and identify likely disconnect cause (lost RMS comms vs turned off) (`proc_check_rms_disconnected_agv_count_cause_v1`)</summary>

##### Runbook: Check RMS disconnected AGV count and identify likely disconnect cause (lost RMS comms vs turned off)

- **Procedure ID:** `proc_check_rms_disconnected_agv_count_cause_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
On the RMS / fleet status UI map monitor summary, read the “count of AGVs disconnected” metric. Use the training’s definition to interpret “disconnected” as AGVs that have lost communication from RMS (RMS runs on the server; AGVs are on Wi‑Fi), then correlate the disconnected count with likely causes: Wi‑Fi/RMS communication loss vs AGVs being turned off.

**When To Use:**
When you need a first-pass diagnostic using RMS’s disconnected AGV count to understand whether AGVs are likely disconnected due to lost RMS/Wi‑Fi communication versus being turned off.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI map monitor summary area

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the map monitor summary/message panel area that includes the “count of AGVs disconnected” metric.

**Healthy condition:**
The map monitor summary/message panel is visible and the disconnected AGV count metric is readable.

**Expected result:**
The RMS UI shows the map monitor summary/message panel with a visible “count of AGVs disconnected” value.

---

###### Step 2 — Read the “count of AGVs disconnected” value

**Responsible role:** L1_support

**Instruction:**
In the RMS map monitor summary/message panel, locate and read the “count of AGVs disconnected” value.

**Healthy condition:**
A single disconnected count value is displayed in the metric list.

**Expected result:**
You have the numeric value for “count of AGVs disconnected” as shown in the RMS UI.

---

###### Step 3 — Interpret “disconnected” as lost RMS communication (RMS server + AGVs on Wi‑Fi)

**Responsible role:** L1_support

**Instruction:**
Use the definition: treat “disconnected” as AGVs that have lost communication from RMS (RMS is the application running on the server; AGVs are on the Wi‑Fi).

**Healthy condition:**
You can state that “disconnected” means lost communication from RMS to AGVs (RMS server application; AGVs on Wi‑Fi).

**Expected result:**
Your interpretation of the disconnected count is explicitly tied to lost communication from RMS to AGVs over Wi‑Fi.

---

###### Step 4 — Correlate disconnected count with likely causes: Wi‑Fi/RMS comms loss vs AGV turned off

**Responsible role:** L1_support

**Instruction:**
Correlate the disconnected count with likely causes: (1) AGVs lost communication with the Wi‑Fi on site, or (2) the AGV was turned off.

**Healthy condition:**
Your hypothesis aligns with the observed situation (e.g., if AGVs were turned off, you expect to see disconnect; if not, you consider Wi‑Fi/RMS communication loss).

**Expected result:**
You produce a likely cause hypothesis that matches one of the two causes explicitly described: Wi‑Fi/RMS communication loss or AGV turned off.

---

**Success Criteria:**

- You can read the RMS “count of AGVs disconnected” metric from the RMS / fleet status UI.
- You interpret “disconnected” as lost communication from RMS to AGVs over Wi‑Fi.
- You correlate the disconnected count to one of the two explicitly described likely causes: Wi‑Fi/RMS communication loss or AGV turned off.

**Failure Conditions:**

- Disconnected count is high and you cannot determine whether the cause is communication loss vs AGVs being turned off using only this metric.


</details>

</details>

---

### 2 — Apply approved recovery actions for hospital lane / related OptiSweep services and reconcile problematic AGV/tote state (`procedure_reference`)

**Intent:** Perform the supported recovery actions that restore hospital lane operation and reconcile any problematic AGV/tote state that prevents induction/add.

**Expects capability:** agv_physical_recovery, agv_active_errors
**Expects surface:** hospital_hmi, rms_ui, wcs_api
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1` (low, support, score=0.7964, boosted=1.0) — Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_agv_api_controls_remove_recover_pause_resume_v1` (high, operator, score=0.8774, boosted=1.0) — Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (if checked)): Hospital lane operation is restored; hospital accepts tote induction/add again and sort can resume.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / RMS): Recovery actions do not restore induction/add; induction still blocked and sort cannot start/continues disrupted.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (attempt)): Recovery partially applied but evidence of success cannot be confirmed due to missing access or unclear station indicators.
- `escalate` (observer=remote; tool=Hospital HMI / RMS / WCS): Cannot proceed safely within approved scope (e.g., evidence unavailable or recovery cannot be safely completed).

**Branches:**

- `healthy` → `node_3` when Recovery successful; hospital accepts induction again / sort can start
- `escalate` → `` when Recovery unsuccessful

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

<details><summary>Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs (`proc_use_agv_api_controls_remove_recover_pause_resume_v1`)</summary>

##### Runbook: Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs

- **Procedure ID:** `proc_use_agv_api_controls_remove_recover_pause_resume_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the System HMI API screen’s AGVs section to remove a problematic AGV by ID, recover (add back) the AGV by ID after physical recovery, and pause/resume all AGV movement fleet-wide.

**When To Use:**
When an AGV needs to be removed from the system (e.g., it has an issue) and later recovered after physical removal/recovery, and you need to pause/resume all AGV movement using the AGV API Controls.

**Safety Notes:**

- If the AGV has a tote, take the tote to the hospital where the tote is removed; the tote is recovered when it is put back in the system.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the System HMI API screen and navigate to the AGVs section

**Responsible role:** operator

**Instruction:**
Open the System HMI API screen and navigate to the AGVs section (AGV API Controls).

**Healthy condition:**
AGV API Controls are visible and ready for input (Remove AGV / Recover AGV fields and Pause/Resume buttons are present).

**Expected result:**
The AGVs section is visible with controls including Remove AGV, Recover AGV, Pause All AGVs, and Resume All AGVs.

---

###### Step 2 — Remove an AGV from the system by AGV ID

**Responsible role:** operator

**Instruction:**
In the AGVs section, enter the target AGV ID in the Remove AGV input field, then click the Remove AGV control/button.

**Healthy condition:**
After clicking Remove AGV, you can proceed with physical removal of the AGV from the system (and tote handling if applicable).

**Expected result:**
The Remove AGV action is accepted for the entered AGV ID, and the AGV is removed from the system after the required physical removal step.

---

###### Step 3 — Recover (add back) the AGV by AGV ID after physical recovery

**Responsible role:** operator

**Instruction:**
After the physical recovery/add-back step, enter the same (or correct) AGV ID in the Recover AGV input field, then click the Recover AGV control/button.

**Healthy condition:**
The AGV is successfully re-added to the system and you can proceed to fleet pause/resume actions as needed.

**Expected result:**
The Recover AGV action is accepted for the entered AGV ID, and the AGV is added back into the system after physical recovery.

---

###### Step 4 — Pause all AGV movement

**Responsible role:** operator

**Instruction:**
Click Pause All AGVs in the AGVs section of the API screen.

**Healthy condition:**
AGV movement is stopped fleet-wide (pause state is in effect).

**Expected result:**
Fleet-wide AGV movement is paused after clicking Pause All AGVs.

---

###### Step 5 — Resume all AGV movement

**Responsible role:** operator

**Instruction:**
Click Resume All AGVs in the AGVs section of the API screen.

**Healthy condition:**
AGV movement is running fleet-wide (resume state is in effect).

**Expected result:**
Fleet-wide AGV movement resumes after clicking Resume All AGVs.

---

**Success Criteria:**

- Remove AGV is followed by physical removal of the AGV from the system; if a tote is present, the tote is taken to the hospital where the tote is removed.
- Recover AGV is performed after physical recovery/add-back, resulting in the AGV being added back into the system.
- Pause All AGVs stops fleet-wide AGV movement, and Resume All AGVs resumes fleet-wide AGV movement.

**Failure Conditions:**

- Cannot physically remove/recover the AGV/tote as required after using Remove AGV.
- System does not reflect expected fleet behavior after Pause All AGVs (verify AGV state using Get AGV Status pop-up).


</details>

</details>

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery) (`proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1`)</summary>

##### Runbook: Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)

- **Procedure ID:** `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Recover operation by stopping RMS, physically placing an AGV into the zone under the tote rack, adding the AGV in RMS using Tote API Controls, verifying the AGV turns blue and reaches AGV status/state "szonestaging" on the Hospital HMI/lane UI, then stopping again and resuming RMS.

**When To Use:**
Use when there is no empty AGV available for a zone and you must recover by adding an AGV into the zone under the tote rack, ensuring it reaches the required "szonestaging" state before resuming RMS.

**Safety Notes:**

- E-stop RMS before making the AGV add/recovery changes in RMS.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), press the E-stop for RMS.

**Healthy condition:**
E-stop control shows RMS is stopped (not running).

**Expected result:**
RMS is in an E-stopped state on the RMS / fleet status UI.

---

###### Step 2 — Move an AGV into the zone under the tote rack

**Responsible role:** L2_support

**Instruction:**
Move an AGV into the zone under the tote rack (physical_floor).

**Healthy condition:**
AGV is placed in the intended zone location under the tote rack (no mismatch between intended zone and physical placement).

**Expected result:**
An AGV is physically positioned in the zone under the tote rack.

---

###### Step 3 — Add the AGV in RMS using Tote API Controls

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), add the AGV using the "Tote API Controls" function.

**Healthy condition:**
After adding, the AGV begins the transition that results in the AGV turning blue.

**Expected result:**
The AGV is added in RMS via Tote API Controls (AGV appears in RMS roster/map context for the add operation).

---

###### Step 4 — Wait for the AGV to turn blue on the RMS UI

**Responsible role:** L2_support

**Instruction:**
Wait for the AGV to turn blue on the RMS / fleet status UI (rms_ui).

**Healthy condition:**
AGV indicator on RMS transitions to blue after the add action.

**Expected result:**
The added AGV changes to blue on the RMS UI.

---

###### Step 5 — Verify AGV status/state is exactly "szonestaging" on the Hospital HMI

**Responsible role:** L2_support

**Instruction:**
On the Hospital HMI / lane UI (hospital_hmi), verify the AGV status/state is exactly "szonestaging".

**Healthy condition:**
AGV state/status equals exactly "szonestaging".

**Expected result:**
Hospital HMI shows the AGV state/status value "szonestaging".

---

###### Step 6 — If AGV is moving to the Hospital, remove and add it again

**Responsible role:** L2_support

**Instruction:**
If the AGV is moving to the Hospital (Hospital HMI shows Hospital destination/state), remove the AGV and add it again (repeat the add step).

**Healthy condition:**
After remove/re-add, the AGV can reach "szonestaging" on the Hospital HMI.

**Expected result:**
AGV is removed from the system and then re-added so it can transition back toward "szonestaging".

---

###### Step 7 — Press E-stop again on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
Press the E-stop again on the RMS / fleet status UI (rms_ui).

**Healthy condition:**
E-stop control indicates RMS is stopped (not running).

**Expected result:**
RMS reflects the E-stopped state again on the RMS / fleet status UI.

---

###### Step 8 — Resume RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
Resume RMS on the RMS / fleet status UI (rms_ui) (Starting the System procedure reference).

**Healthy condition:**
RMS shows resumed/started state after the second E-stop press.

**Expected result:**
RMS is resumed/started on the RMS / fleet status UI.

---

**Success Criteria:**

- The selected AGV appears as blue on the RMS UI.
- The Hospital HMI shows the AGV status/state exactly "szonestaging".
- RMS is resumed after the second E-stop press.

**Failure Conditions:**

- AGV does not reach "szonestaging" after being added.
- AGV repeatedly moves to the Hospital instead of staging.
- RMS cannot be resumed after the second E-stop press.


</details>

</details>

---

### 3 — Validate hospital induction/add and sort operation stability after recovery (`validation_gate`)

**Intent:** Confirm that the hospital station can add/induct totes again and that the site can start/continue sort without the reported disruption recurring.

**Expects capability:** agv_active_errors, hospital_diversion, fleet_system_status
**Expects surface:** hospital_hmi, rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1` (low, operator, score=0.698, boosted=1.0) — Stop the OptiSweep System Using the System HMI API Screen (SYSTEM SHUTDOWN)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_agv_api_controls_remove_recover_pause_resume_v1` (low, operator, score=0.7633, boosted=1.0) — Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_hospital_hmi_remove_tote_screen_to_remove_tote_v1` (low, operator, score=0.396, boosted=0.576) — Use Hospital HMI "Remove Tote" screen to remove a tote from the system
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (read-only where available)): Hospital induction/add and sort operation are stable after recovery; backlog condition clears.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (attempt)): Induction/add remains blocked and/or sort cannot start; abnormal indicators persist.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / RMS / WCS (attempt)): Cannot confirm stability due to missing evidence access or ambiguous UI state.
- `escalate` (observer=remote; tool=Hospital HMI / RMS / WCS): Validation fails and additional authorized troubleshooting beyond this playbook candidate is needed.

**Branches:**

- `healthy` → `` when Validation success
- `unhealthy` → `node_2` when Validation failure

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (3)</summary>

<details><summary>Stop the OptiSweep System Using the System HMI API Screen (SYSTEM SHUTDOWN) (`proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1`)</summary>

##### Runbook: Stop the OptiSweep System Using the System HMI API Screen (SYSTEM SHUTDOWN)

- **Procedure ID:** `proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the system HMI API screen to initiate SYSTEM SHUTDOWN and confirm the AGVs transition to a shutdown queue between sorts.

**When To Use:**
When you need to stop the OptiSweep system between sorts so AGVs move to a shutdown queue.

**Safety Notes:**

- The system should be shutdown between sorts to allow AGVs to charge.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Navigate to the system API screen on the system HMI

**Responsible role:** operator

**Instruction:**
On the system HMI, navigate to the system API screen.

**Healthy condition:**
The system API screen is displayed with the System API controls available.

**Expected result:**
The system API screen is open and ready for the SYSTEM SHUTDOWN action.

---

###### Step 2 — Press SYSTEM SHUTDOWN

**Responsible role:** operator

**Instruction:**
Press SYSTEM SHUTDOWN on the system API screen.

**Healthy condition:**
The SYSTEM SHUTDOWN action is accepted by the system (shutdown sequence begins).

**Expected result:**
SYSTEM SHUTDOWN is initiated.

---

###### Step 3 — Confirm AGVs transition to the shutdown queue

**Responsible role:** operator

**Instruction:**
Observe that the AGVs go to a shutdown queue after SYSTEM SHUTDOWN.

**Healthy condition:**
AGVs transition into the shutdown queue after SYSTEM SHUTDOWN.

**Expected result:**
AGVs are in a shutdown queue state.

---

**Success Criteria:**

- After pressing SYSTEM SHUTDOWN, AGVs are in a shutdown queue state.

**Failure Conditions:**

- AGVs do not transition to the shutdown queue after SYSTEM SHUTDOWN.


</details>

<details><summary>Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs (`proc_use_agv_api_controls_remove_recover_pause_resume_v1`)</summary>

##### Runbook: Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs

- **Procedure ID:** `proc_use_agv_api_controls_remove_recover_pause_resume_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the System HMI API screen’s AGVs section to remove a problematic AGV by ID, recover (add back) the AGV by ID after physical recovery, and pause/resume all AGV movement fleet-wide.

**When To Use:**
When an AGV needs to be removed from the system (e.g., it has an issue) and later recovered after physical removal/recovery, and you need to pause/resume all AGV movement using the AGV API Controls.

**Safety Notes:**

- If the AGV has a tote, take the tote to the hospital where the tote is removed; the tote is recovered when it is put back in the system.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the System HMI API screen and navigate to the AGVs section

**Responsible role:** operator

**Instruction:**
Open the System HMI API screen and navigate to the AGVs section (AGV API Controls).

**Healthy condition:**
AGV API Controls are visible and ready for input (Remove AGV / Recover AGV fields and Pause/Resume buttons are present).

**Expected result:**
The AGVs section is visible with controls including Remove AGV, Recover AGV, Pause All AGVs, and Resume All AGVs.

---

###### Step 2 — Remove an AGV from the system by AGV ID

**Responsible role:** operator

**Instruction:**
In the AGVs section, enter the target AGV ID in the Remove AGV input field, then click the Remove AGV control/button.

**Healthy condition:**
After clicking Remove AGV, you can proceed with physical removal of the AGV from the system (and tote handling if applicable).

**Expected result:**
The Remove AGV action is accepted for the entered AGV ID, and the AGV is removed from the system after the required physical removal step.

---

###### Step 3 — Recover (add back) the AGV by AGV ID after physical recovery

**Responsible role:** operator

**Instruction:**
After the physical recovery/add-back step, enter the same (or correct) AGV ID in the Recover AGV input field, then click the Recover AGV control/button.

**Healthy condition:**
The AGV is successfully re-added to the system and you can proceed to fleet pause/resume actions as needed.

**Expected result:**
The Recover AGV action is accepted for the entered AGV ID, and the AGV is added back into the system after physical recovery.

---

###### Step 4 — Pause all AGV movement

**Responsible role:** operator

**Instruction:**
Click Pause All AGVs in the AGVs section of the API screen.

**Healthy condition:**
AGV movement is stopped fleet-wide (pause state is in effect).

**Expected result:**
Fleet-wide AGV movement is paused after clicking Pause All AGVs.

---

###### Step 5 — Resume all AGV movement

**Responsible role:** operator

**Instruction:**
Click Resume All AGVs in the AGVs section of the API screen.

**Healthy condition:**
AGV movement is running fleet-wide (resume state is in effect).

**Expected result:**
Fleet-wide AGV movement resumes after clicking Resume All AGVs.

---

**Success Criteria:**

- Remove AGV is followed by physical removal of the AGV from the system; if a tote is present, the tote is taken to the hospital where the tote is removed.
- Recover AGV is performed after physical recovery/add-back, resulting in the AGV being added back into the system.
- Pause All AGVs stops fleet-wide AGV movement, and Resume All AGVs resumes fleet-wide AGV movement.

**Failure Conditions:**

- Cannot physically remove/recover the AGV/tote as required after using Remove AGV.
- System does not reflect expected fleet behavior after Pause All AGVs (verify AGV state using Get AGV Status pop-up).


</details>

<details><summary>Use Hospital HMI "Remove Tote" screen to remove a tote from the system (`proc_use_hospital_hmi_remove_tote_screen_to_remove_tote_v1`)</summary>

##### Runbook: Use Hospital HMI "Remove Tote" screen to remove a tote from the system

- **Procedure ID:** `proc_use_hospital_hmi_remove_tote_screen_to_remove_tote_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
On the Hospital HMI, scan the tote barcode to populate Tote ID/Barcode fields, verify extract-side position information from WCS (AGV#, Tote ID, Bar Code, Status), ensure the tote is positioned properly on the extract side, then press CONFIRM & EXECUTE to remove the tote from the system.

**When To Use:**
Use when a tote is at the Hospital Station extract side and the station operator needs to remove that tote from the system so the required task can be performed.

**Safety Notes:**

- Do not press CONFIRM & EXECUTE until the tote is positioned properly on the extract side.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the Hospital HMI "Remove Tote" screen

**Responsible role:** operator

**Instruction:**
Open the Hospital HMI screen labeled "Remove Tote".

**Healthy condition:**
The screen shows the Remove Tote workflow elements (Tote ID scan, Barcode scan, CONFIRM & EXECUTE, and Extract Position Information from WCS).

**Expected result:**
The Hospital HMI "Remove Tote" screen is displayed with fields/controls for Tote ID, Barcode, CONFIRM & EXECUTE, and the Extract Position Information panel.

---

###### Step 2 — Scan tote barcode to populate the Tote ID field

**Responsible role:** operator

**Instruction:**
In the Tote ID area, use the green scanner to scan the tote bar code to populate the Tote ID field.

**Healthy condition:**
Tote ID field updates from the scanned tote bar code.

**Expected result:**
The Tote ID field is populated after scanning the tote bar code.

---

###### Step 3 — Scan tote barcode to populate the Barcode field

**Responsible role:** operator

**Instruction:**
In the Barcode area, press the Barcode scan control and then use the green scanner to scan the tote bar code to populate the Barcode field.

**Healthy condition:**
Barcode field updates from the scanned tote bar code.

**Expected result:**
The Barcode field is populated after scanning the tote bar code.

---

###### Step 4 — Verify Extract Position Information for the extract side (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
Verify the "Extract Position Information" panel shows WCS data for the extract side, including AGV# (ID of the AGV at the extract side), Tote ID (ID of the tote at the extract side), Bar Code (scanned information), and Status (status messages received from the WCS about the tote).

**Healthy condition:**
The Extract Position Information values correspond to the tote you intend to remove (and the Status messages are consistent with the tote at the extract side).

**Expected result:**
Extract Position Information panel displays AGV#, Tote ID, Bar Code, and Status values for the extract side.

---

###### Step 5 — Ensure the tote is positioned properly on the extract side

**Responsible role:** operator

**Instruction:**
Ensure the tote is positioned properly on the extract side of the Hospital Station.

**Healthy condition:**
Tote is correctly placed on the extract side (consistent with the Extract Position Information panel).

**Expected result:**
The tote is physically located on the extract side, ready for removal.

---

###### Step 6 — Press CONFIRM & EXECUTE to remove the tote from the system

**Responsible role:** operator

**Instruction:**
Press the CONFIRM & EXECUTE button to remove the tote from the system.

**Healthy condition:**
Removal is executed after the tote is positioned properly on the extract side (per the workflow), and the Extract Position Information panel continues to show WCS-provided extract-side details.

**Expected result:**
The tote is removed from the system using the Remove Tote screen workflow; the screen reflects the removal action and the Extract Position Information panel reflects the WCS-provided extract-side details.

---

###### Step 7 — Use Add Tote shortcut if needed

**Responsible role:** operator

**Instruction:**
If needed, use the "Add Tote" shortcut button to navigate to the "Add Tote" screen.

**Healthy condition:**
Add Tote shortcut is available on the Remove Tote screen and navigation succeeds.

**Expected result:**
The Hospital HMI navigates to the "Add Tote" screen.

---

**Success Criteria:**

- Tote removal is executed via the Hospital HMI Remove Tote screen workflow (CONFIRM & EXECUTE pressed after tote is positioned properly on the extract side).
- Extract Position Information panel shows WCS-provided extract-side details including AGV#, Tote ID, Bar Code, and Status.

**Failure Conditions:**

- Extract Position Information (AGV#, Tote ID, Bar Code, Status) does not match the tote intended for removal.
- Tote is not positioned properly on the extract side when attempting removal.


</details>

</details>

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Symptom corroborated as abnormal hospital/AGV/tote state | `node_2` |
| `node_1` | `healthy` | Pattern not corroborated | `` |
| `node_1` | `inconclusive` | Evidence inconclusive | `node_2` |
| `node_2` | `healthy` | Recovery successful; hospital accepts induction again / sort can start | `node_3` |
| `node_2` | `escalate` | Recovery unsuccessful | `` |
| `node_3` | `healthy` | Validation success | `` |
| `node_3` | `unhealthy` | Validation failure | `node_2` |

## Unresolved / Low-Confidence Links

- node_1: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_1: proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1 (low)
- node_1: proc_check_rms_disconnected_agv_count_cause_v1 (low)
- node_2: proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1 (low)
- node_3: proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1 (low)
- node_3: proc_use_agv_api_controls_remove_recover_pause_resume_v1 (low)
- node_3: proc_use_hospital_hmi_remove_tote_screen_to_remove_tote_v1 (low)
