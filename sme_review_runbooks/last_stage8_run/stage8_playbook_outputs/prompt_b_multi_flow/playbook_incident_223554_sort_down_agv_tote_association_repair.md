# Site cannot start sort / reported down — validate AGV/tote association and correct mismatches via API-based recovery, then resume movement

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_sort_down_agv_tote_association_repair` |
| Case ID | `223554` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- “Site is down / unable to start sort.”
- “We went down in the middle of sort.”
- “We can remove totes but cannot add at the hospital.”
- “An AGV doesn’t belong in the shown location.”
- Discussion of disconnected tote / AGV location anomalies

## Affected Systems

- AGVs / robots
- Totes and tote associations
- ACB hospital station
- Hospital lane
- OptiSweep/WCS API-based correction path (API dog / Aveva endpoints as referenced)

## Nodes

### 1 — Confirm sort-down / hospital add failure correlates with AGV/tote association or location mismatch (`diagnostic_decision`)

**Intent:** Determine whether the site-down / inability to start sort and hospital add failure are consistent with AGV/tote association mismatches or AGV location anomalies.

**Expects capability:** agv_active_errors, device_roster_state, tote_lifecycle_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.5306, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `tote_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.7471, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `tote_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.
- `proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1` (low, support, score=0.3, boosted=0.2995) — Verify Robot Location model fields and location types/statuses used by RMS orange locations
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `tote_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `tote_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | Hospital HMI): No mismatch indicators; hospital add/sort failure does not correlate with abnormal AGV placement or disconnected/incorrect tote association.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | Hospital HMI): Evidence supports AGV/tote association mismatch or abnormal AGV placement correlating with hospital add failure and/or inability to start sort.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | Hospital HMI): Cannot confirm mismatch correlation due to missing/unclear telemetry or hospital state ambiguity.

**Branches:**

- `unhealthy` → `node_2` when Mismatch/abnormal AGV evidence supported
- `inconclusive` → `` when No supported evidence of mismatch

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View (`proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`)</summary>

##### Runbook: Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View

- **Procedure ID:** `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`
- **Procedure Type:** `operation`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Geek Plus RMS Robot Selection web view to add a robot by robot ID or remove an existing robot, and confirm success messages after each action.

**When To Use:**
When you need to manage the Geek Plus RMS robot roster using the Robot Selection Add/Remove workflow and verify the on-screen success confirmations.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open Geek Plus RMS web application from an authorized network path

**Responsible role:** L1_support

**Instruction:**
From an OT network device, open the Geek Plus RMS web application using the site/RMS address. If you are supporting remotely, ensure you are authorized to use the UPS VPN through Zscaler and can reach the site/RMS address.

**Healthy condition:**
You can access the Geek Plus RMS web application from your current network authorization path.

**Expected result:**
The Geek Plus RMS web application loads successfully and you can navigate to the Robot Selection screen.

---

###### Step 2 — Navigate to the Robot Selection screen with Add Robot and Remove Robot controls

**Responsible role:** L1_support

**Instruction:**
In the Geek Plus RMS web application, navigate to the Robot Selection screen that contains the Robot ID entry field and the Add Robot and Remove Robot controls.

**Healthy condition:**
You can see the Robot ID entry area and the Add/Remove controls on the Robot Selection screen.

**Expected result:**
The Robot Selection screen is visible with the Robot ID entry field and the Add and Remove controls.

---

###### Step 3 — Add a robot by robot ID

**Responsible role:** L1_support

**Instruction:**
In the Robot ID entry field, enter the corresponding robot ID. (If the robot is already introduced, partial numeric entry may surface matching robots.) Click the "Add" button.

**Healthy condition:**
The UI shows the success confirmation for the Add action after clicking "Add".

**Expected result:**
A confirmation message appears indicating the robot was added successfully ("adding was successful" / "robot was added successfully").

---

###### Step 4 — Remove a robot by robot ID or by selecting it from the list

**Responsible role:** L1_support

**Instruction:**
Enter the corresponding robot ID in the Robot ID entry field or select the robot from the list shown for that ID. Click the "Remove" button.

**Healthy condition:**
The UI shows the success confirmation for the Remove action after clicking "Remove".

**Expected result:**
A confirmation message appears indicating the robot was removed successfully ("removal was successful" / "remove what was successful").

---

**Success Criteria:**

- After clicking "Add", the Robot Selection screen displays an "adding was successful" confirmation message.
- After clicking "Remove", the Robot Selection screen displays a "removal was successful" confirmation message.

**Failure Conditions:**

- No success confirmation appears after clicking "Add".
- No success confirmation appears after clicking "Remove".


</details>

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

<details><summary>Verify Robot Location model fields and location types/statuses used by RMS orange locations (`proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1`)</summary>

##### Runbook: Verify Robot Location model fields and location types/statuses used by RMS orange locations

- **Procedure ID:** `proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Using the WCS / Helix DB (SSMS) read-only access surface, verify the Robot Location database model table includes the expected location attributes (station number, occupied, zone, closeout zone, location type, max AGVs, dwell-time tracking) and that the enumerated location types/statuses match the RMS orange location categories (sorter/tipper/hospital/shut down/GLD pre queue).

**When To Use:**
When you need to confirm that RMS orange location categories are backed by the expected Robot Location model/table definition in the WCS/Robotics database (fields present and location type/status enumerations match the expected categories).

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open WCS / Helix DB (SSMS) read-only access surface

**Responsible role:** L2_support

**Instruction:**
Use the WCS / Helix DB (SSMS) access surface to connect to the OptiSweep/WCS database that contains the Robotics database model table definitions for the Robot Location model.

**Healthy condition:**
You can browse the database objects needed to locate the Robot Location database model table definition.

**Expected result:**
SSMS is connected to the OptiSweep/WCS database that contains the Robotics database model table definitions for the Robot Location model.

---

###### Step 2 — Locate Robot Location database model table and verify required location attributes

**Responsible role:** L2_support

**Instruction:**
In SSMS, locate the Robot Location database model table definition and verify it includes fields/attributes for: station number, occupied (occupied or not), zone, closeout zone, location type, Max number of AGVs allowed at that location, and whether the location should be tracked for dwell time there.

**Healthy condition:**
All required attributes are present in the Robot Location model/table definition with names/meaning consistent with the expected set (station number, occupied, zone, closeout zone, location type, max AGVs, dwell tracking).

**Expected result:**
The Robot Location database model table definition shows the expected location attributes: station number, occupied, zone, closeout zone, location type, Max number of AGVs allowed, and dwell-time tracking (tracked vs not tracked).

---

###### Step 3 — Verify Robot Location model includes expected location types/statuses for RMS orange categories

**Responsible role:** L2_support

**Instruction:**
In the same Robot Location model/table definition, verify the listed location types/statuses include the categories: sorter entrance queue, sorter queue, sorter exit queue; tipper, tipper queue, tipper exit queue; hospital drop off, hospital entrance queue, hospital pickup, hospital exit queue; queue shut down, off the end shut down queue; GLD pre queue entrance, GLD pre queue exit.

**Healthy condition:**
All listed categories appear in the Robot Location model/table definition (as location types/statuses) with names consistent with the expected set.

**Expected result:**
The Robot Location model/table definition includes the named location types/statuses for sorter/tipper/hospital/shut down/GLD pre queue categories.

---

###### Step 4 — Cross-check RMS orange location categories map to the same Robot Location types/statuses

**Responsible role:** L2_support

**Instruction:**
Using the Robot Location model/table definition you verified, confirm that the segment’s RMS orange location categories correspond to the same named location types/statuses you see in the Robot Location model/table definition.

**Healthy condition:**
The set of location types/statuses in the Robot Location model/table definition matches the expected RMS orange categories (sorter/tipper/hospital/shut down/GLD pre queue).

**Expected result:**
The RMS orange location categories map consistently to the location types/statuses present in the Robot Location model/table definition.

---

**Success Criteria:**

- Robot Location model/table definition includes required location attributes: station number, occupied, zone, closeout zone, location type, max AGVs, dwell-time tracking.
- Robot Location model/table definition includes expected location types/statuses: sorter entrance/queue/exit; tipper/tipper queue/tipper exit; hospital drop off/entrance queue/pickup/exit queue; queue shut down/off-the-end shut down; GLD pre queue entrance/exit.
- RMS orange location categories map consistently to the same named location types/statuses in the Robot Location model/table definition.

**Failure Conditions:**

- One or more required Robot Location attributes are missing or named differently such that the expected set cannot be confirmed.
- One or more expected location types/statuses are missing from the Robot Location model/table definition.
- RMS orange location categories cannot be mapped consistently to the Robot Location model/table definition.


</details>

</details>

---

### 2 — Perform approved API-based correction for disconnected/inducted tote and AGV mismatch (`procedure_reference`)

**Intent:** Execute the approved API-based recovery actions to remove/correct the mismatched tote/AGV state so the system can resume movement/sort.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_recover_from_agv_fault_during_exchange_recovery_v1` (medium, support, score=0.6733, boosted=0.8433) — Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1` (high, support, score=0.6295, boosted=0.7995) — Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1` (high, support, score=0.6284, boosted=0.7984) — Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI | RMS / AGV status UI | WCS/SSMS (read-only)): API-based correction successfully removes the mismatch that was blocking flow.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI | RMS / AGV status UI | WCS/SSMS (read-only)): Mismatch persists or correction triggers additional errors.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI | RMS / AGV status UI | WCS/SSMS (read-only)): Partial recovery; unclear whether corrected state is fully effective.
- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | Hospital HMI): Recovery actions did not restore movement/sort/hospital add/remove; deeper ownership required.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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

---

**Success Criteria:**

- Faulted AGV is removed from RMS.
- If the AGV behind did not backfill, the trailing AGV is also removed.
- Affected exchange location has a newly introduced tote and an empty AGV placed in the correct zone so exchange can proceed.

**Failure Conditions:**

- Trailing AGV does not backfill and cannot be removed/cleared as described.
- New tote and/or empty AGV cannot be introduced into the correct zone.


</details>

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

<details><summary>Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice) (`proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1`)</summary>

##### Runbook: Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice)

- **Procedure ID:** `proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
If empty AGVs lose their tasks after an RMS restart, stop RMS, remove and re-add the affected empty AGVs without totes twice, verify each AGV is in the "szonestaging" state on the HMI, press E-stop again when ready, then resume RMS.

**When To Use:**
Use when empty AGVs have lost their tasks because the RMS was restarted, and the recovery guidance calls for removing and re-adding the AGVs twice and confirming "szonestaging" before resuming RMS.

**Safety Notes:**

- Do not resume RMS until the affected AGVs are confirmed in the "szonestaging" state on the HMI.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), press the E-stop for RMS.

**Healthy condition:**
The RMS E-stop control is engaged/active on the RMS / fleet status UI.

**Expected result:**
RMS is in an E-stopped state on the RMS / fleet status UI.

---

###### Step 2 — Remove and re-add empty AGVs without totes twice using Tote API Controls

**Responsible role:** L2_support

**Instruction:**
Using the Tote API Controls flow within the RMS / fleet status UI (rms_ui), remove and re-add the affected empty AGVs without totes twice.

**Healthy condition:**
The AGVs proceed through the expected post-add state progression (next step will verify "szonestaging").

**Expected result:**
Each affected empty AGV has been removed and re-added twice via the RMS Tote API Controls flow.

---

###### Step 3 — Verify AGVs are in "szonestaging" on the HMI

**Responsible role:** L2_support

**Instruction:**
If the system needs to be restarted, verify on the HMI (hospital_hmi) that the affected AGVs are in the "szonestaging" state by referencing the AGV state/value on the HMI.

**Healthy condition:**
AGV status is "szonestaging" for the affected empty AGVs.

**Expected result:**
The affected empty AGVs show AGV status/state value "szonestaging" on the HMI.

---

###### Step 4 — Press E-stop again when ready to resume

**Responsible role:** L2_support

**Instruction:**
When the affected empty AGVs are confirmed in "szonestaging" on the HMI, press the E-stop again on the RMS / fleet status UI (rms_ui) when ready to resume.

**Healthy condition:**
E-stop again action is accepted and the system is ready for RMS resumption.

**Expected result:**
The RMS E-stop control is pressed again (as indicated by the RMS / fleet status UI).

---

###### Step 5 — Resume RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), resume RMS.

**Healthy condition:**
RMS is resumed and the affected empty AGVs are no longer in the lost-task condition.

**Expected result:**
RMS resumes/starts successfully on the RMS / fleet status UI.

---

**Success Criteria:**

- RMS is resumed on the RMS / fleet status UI.
- Affected empty AGVs are no longer in the lost-task condition after the remove/re-add cycle and "szonestaging" verification.

**Failure Conditions:**

- Any affected empty AGV cannot be brought to "szonestaging".
- Lost-task condition persists after the twice remove/re-add process and RMS resumption.


</details>

</details>

---

### 3 — Validate movement/sort resumes and hospital add/remove works after mismatch correction (`validation_gate`)

**Intent:** Confirm that the site can start sort again and that hospital tote add/remove behavior is restored.

**Expects capability:** fleet_system_status, hospital_diversion, agv_active_errors
**Expects surface:** rms_ui, hospital_hmi, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.6754, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.7427, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_hospital_hmi_operations_menu_induct_extract_status_v1` (low, operator, score=0.8884, boosted=1.0) — Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI | RMS / AGV status UI | WCS/SSMS (read-only)): Movement/sort resumes and hospital add/remove works after mismatch correction.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI | RMS / AGV status UI | WCS/SSMS (read-only)): Recovery did not restore normal sort start or hospital add/remove behavior.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI | WCS/SSMS (read-only) | RMS / AGV status UI): Partial restoration or ambiguous telemetry; unclear if movement/sort will sustain.

**Branches:**

- `healthy` → `` when Sort and hospital add/remove restored
- `escalate` → `` when Not restored after correction

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

<details><summary>Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages (`proc_check_hospital_hmi_operations_menu_induct_extract_status_v1`)</summary>

##### Runbook: Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages

- **Procedure ID:** `proc_check_hospital_hmi_operations_menu_induct_extract_status_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the Hospital HMI / lane UI Operations Menu screen to read the WCS-fed induct and extract position fields (AGV#, Tote ID, Bar Code, Status). Confirm the Status messages explain why the tote is there and what station operator menu/action to use.

**When To Use:**
When a tote arrives at the hospital station and you need to determine what tote/AGV is at the induct and extract positions and what the WCS status message requires the station operator to do next.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open Hospital HMI Operations Menu and locate Induct Position / Extract Position sections

**Responsible role:** operator

**Instruction:**
On the Hospital HMI / lane UI, navigate to the Operations Menu screen that contains the "Induct Position" and "Extract Position" sections.

**Healthy condition:**
"Induct Position" and "Extract Position" sections are visible on the Operations Menu screen.

**Expected result:**
The screen shows both "Induct Position" and "Extract Position" sections.

---

###### Step 2 — Read Induct Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Induct Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Healthy condition:**
AGV#, Tote ID, Bar Code, and Status are present in the "Induct Position" section as read-only WCS data.

**Expected result:**
The "Induct Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

---

###### Step 3 — Read Extract Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Extract Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Healthy condition:**
AGV#, Tote ID, Bar Code, and Status are present in the "Extract Position" section as read-only WCS data.

**Expected result:**
The "Extract Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

---

###### Step 4 — Confirm both Status messages are present and provide WCS explanation/action guidance

**Responsible role:** operator

**Instruction:**
Verify that the "Induct Position" Status and "Extract Position" Status messages are present and written as messages received from the WCS that explain why the tote is there and what menu/action the station operator needs to use.

**Healthy condition:**
Induct Position Status and Extract Position Status each provide a clear WCS message describing why the tote is there and what menu/action to perform.

**Expected result:**
Both Status fields contain non-blank WCS messages that provide explanation and action/menu guidance.

---

**Success Criteria:**

- Induct Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
- Extract Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
- Both Status messages explain why the tote is there and what menu/action the station operator needs to use.

**Failure Conditions:**

- Induct Position Status is blank/missing.
- Extract Position Status is blank/missing.
- Either Status message does not provide explanation/action guidance (why the tote is there and what menu/action to use).


</details>

</details>

<details><summary><strong>Support runbooks</strong> (2)</summary>

<details><summary>Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up (`proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1`)</summary>

##### Runbook: Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up

- **Procedure ID:** `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI pop-up titled “Overall System AGV Status” to confirm the current overall AGV/AUV system status is populated and capture the displayed overall status wording/values for troubleshooting context.

**When To Use:**
When you need a first confirmation of whether the overall AGV/AUV system status page is populated and what overall status it reports (e.g., to establish whether the system appears reachable vs overall-down/unreachable).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS / fleet status UI and navigate to the “Overall System AGV Status” pop-up

**Responsible role:** L1_support

**Instruction:**
In the RMS / fleet status UI (rms_ui), open the pop-up/page titled “Overall System AGV Status”.

**Healthy condition:**
The pop-up/page titled “Overall System AGV Status” is reachable and displayed.

**Expected result:**
The “Overall System AGV Status” pop-up/page is opened and visible.

---

###### Step 2 — Verify the “Overall System AGV Status” page is populated (not blank/unavailable)

**Responsible role:** L1_support

**Instruction:**
On the “Overall System AGV Status” page, confirm the page shows current status details (i.e., the status content is present rather than blank/unreachable).

**Healthy condition:**
Status content is present on the “Overall System AGV Status” page (the page is not blank/unreachable).

**Expected result:**
The “Overall System AGV Status” page shows current overall AGV/AUV status details (not blank/unavailable).

---

###### Step 3 — Record the displayed overall status value(s) from the pop-up

**Responsible role:** L1_support

**Instruction:**
Record the displayed overall status value(s) shown on the “Overall System AGV Status” page using the exact on-screen wording/fields present.

**Healthy condition:**
The recorded values match the on-screen overall status details currently shown on the page.

**Expected result:**
You have captured the displayed overall status value(s)/wording from the “Overall System AGV Status” pop-up.

---

**Success Criteria:**

- The “Overall System AGV Status” pop-up/page is reachable and populated with current status details.
- The displayed overall status value(s)/wording are recorded from the pop-up.

**Failure Conditions:**

- “Overall System AGV Status” pop-up/page is blank or unavailable (overall system-down/unreachable symptom).


</details>

<details><summary>Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall) (`proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1`)</summary>

##### Runbook: Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)

- **Procedure ID:** `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Geek+ RMS / fleet status web UI to confirm the overall page is reachable and that it correctly separates fault categories: “system faults” on the left and “AGV system faults” on the right. If the RMS page is blank, treat it as a reachability/firewall symptom. Use the left/right placement to interpret whether the issue is communication loss vs an AGV that was commanded to move but is not in progress.

**When To Use:**
When you need to verify that the Geek+ RMS overall/fleet status page is reachable and that it is showing the expected fault panels (left system faults vs right AGV system faults), including the specific symptom where the page appears blank due to firewall not being open.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the Geek+ RMS / fleet status web UI (RMS overall page)

**Responsible role:** L1_support

**Instruction:**
Open the Geek+ RMS / fleet status web UI (RMS / fleet status UI).

**Healthy condition:**
The RMS overall page is visible and fault panels can be observed.

**Expected result:**
The RMS overall page loads (or you observe that it is blank).

---

###### Step 2 — Confirm the RMS page is not blank; if blank, treat as firewall/reachability symptom

**Responsible role:** L1_support

**Instruction:**
Check whether the RMS overall page shows content/fault panels. If it is blank, treat it as the firewall-not-open symptom described by the source.

**Healthy condition:**
Fault panels are visible (not blank).

**Expected result:**
Either (a) fault panels are visible, or (b) the page is blank consistent with firewall not being open.

---

###### Step 3 — Check left-side “system faults” panel

**Responsible role:** L1_support

**Instruction:**
On the RMS overall page, check the left side labeled area for “system faults”.

**Healthy condition:**
The left “system faults” panel is visible (fault rows/entries can be observed if present).

**Expected result:**
The left-side “system faults” area is visible and can be reviewed for any listed faults.

---

###### Step 4 — Check right-side “AGV system faults” panel

**Responsible role:** L1_support

**Instruction:**
On the RMS overall page, check the right side labeled area for “AGV system faults” (active AGV faults).

**Healthy condition:**
The right “AGV system faults” panel is visible (fault rows/entries can be observed if present).

**Expected result:**
The right-side “AGV system faults” area is visible and can be reviewed for any listed faults.

---

###### Step 5 — Interpret left/right fault placement for communication loss vs commanded-but-not-in-progress movement

**Responsible role:** L1_support

**Instruction:**
Use the source mapping: if you lose communication with a chat, expect it on the left “system faults”; if you told an AGV to move but it hasn’t moved, expect it on the right “AGV system faults”.

**Healthy condition:**
Observed faults align with the expected left/right meaning (left = communication loss; right = commanded move not in progress).

**Expected result:**
You can map the observed fault placement to either communication-loss (left) or commanded-but-not-in-progress movement (right).

---

**Success Criteria:**

- RMS overall page is reachable and not blank (fault panels visible).
- Left “system faults” and right “AGV system faults” areas are observable on the RMS overall page.
- Observed fault placement can be interpreted as communication loss (left) vs commanded-but-not-in-progress movement (right) using the source mapping.

**Failure Conditions:**

- RMS remains blank (no visible system/AGV fault panels).
- Left/right fault separation is not observable or does not align with the expected meaning (left = communication loss; right = commanded move not in progress).


</details>

</details>

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Mismatch/abnormal AGV evidence supported | `node_2` |
| `node_1` | `inconclusive` | No supported evidence of mismatch | `` |
| `node_3` | `healthy` | Sort and hospital add/remove restored | `` |
| `node_3` | `escalate` | Not restored after correction | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_1: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_1: proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1 (low)
- node_3: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_3: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
- node_3: proc_check_hospital_hmi_operations_menu_induct_extract_status_v1 (low)
