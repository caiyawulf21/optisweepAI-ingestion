# Restore hospital station tote induction and resume sort after hospital/AGV-tote association disruption

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_tote_and_site_sort_recovery` |
| Case ID | `223554` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- “Hospital station can’t induct/add totes.”
- “We can remove totes but we can’t add totes at the hospital.”
- “The robot/system is in a shut down state.”
- “The site is down / we can’t start sort.”
- “Sort went down in the middle of sorting.”

## Affected Systems

- ACB hospital station / hospital lane
- AGVs / robots in hospital area
- totes and tote association state
- OptiSweep services (OptiSweep reset mentioned in resolution evidence)
- sort workflow (site unable to start sort / went down mid-sort)

## Nodes

### 1 — Confirm whether the issue is hospital induct/add failure with abnormal hospital-area state (and whether it is fleet-wide or localized) (`diagnostic_decision`)

**Intent:** Determine the observable scope: hospital station cannot induct/add totes (possibly while removal works), and whether the site is down/unable to start sort; then decide whether to focus on hospital-area tote/AGV association anomalies versus broader fleet/system health.

**Expects capability:** agv_active_errors, fleet_system_status, zone_pairing_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1` (low, operator, score=0.677, boosted=1.0) — Stop the OptiSweep System Using the System HMI API Screen (SYSTEM SHUTDOWN)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_agv_api_controls_remove_recover_pause_resume_v1` (low, operator, score=0.729, boosted=1.0) — Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_hospital_hmi_remove_tote_screen_to_remove_tote_v1` (low, operator, score=0.3875, boosted=0.5622) — Use Hospital HMI "Remove Tote" screen to remove a tote from the system
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI + WCS/SSMS (read-only) + Hospital HMI): Hospital induct/add works (or failure is limited/localized) and broader fleet/system indicators do not show persistent abnormal conditions.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI + WCS/SSMS (read-only) + Hospital HMI): Hospital induct/add fails and there are active fleet/system indicators consistent with shutdown/sort-halting.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI + WCS/SSMS (read-only) + Hospital HMI): Symptoms are reported but RMS/WCS evidence is missing, ambiguous, or not available to corroborate scope.
- `escalate` (observer=site_or_remote; tool=Hospital HMI + RMS / WCS visibility): Evidence is insufficient to proceed safely (e.g., no remote visibility and site cannot provide clear scope facts).

**Branches:**

- `unhealthy` → `node_2` when Hospital add/induct fails and sort down/halts with abnormal fleet/system indicators
- `inconclusive` → `node_2` when Hospital add/induct fails but fleet/system looks normal (localized pattern)

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

### 2 — Check for active fleet/AGV faults and hospital-area association anomalies that block tote induction (`diagnostic_decision`)

**Intent:** Identify whether active AGV errors/faults or abnormal roster/association state in the hospital area correlates with the inability to add/induct totes.

**Expects capability:** agv_active_errors, device_roster_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.5549, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.7664, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.3, boosted=1.1) — Query Active AGV Errors From the WCS Database
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=WCS/SSMS (read-only) + RMS / AGV status UI): No active AGV faults and hospital-area state appears normal enough that tote/induct blocking is not explained by current active errors.
- `unhealthy` (observer=remote; tool=WCS/SSMS (read-only) + RMS / AGV status UI): Active AGV faults/errors exist and/or hospital-area related state looks abnormal, matching a blocking condition for tote induction.
- `inconclusive` (observer=remote; tool=WCS/SSMS (read-only) + RMS / AGV status UI): RMS/WCS evidence does not clearly correlate with hospital induction behavior (missing, blank, or ambiguous results).
- `escalate` (observer=site_or_remote; tool=RMS / WCS/Hospital HMI): Unable to obtain sufficient diagnostic evidence to choose safe recovery actions.

**Branches:**

- `unhealthy` → `node_3` when Active faults/errors or abnormal hospital-area roster/association state present
- `healthy` → `node_3` when No active faults and hospital-area state appears normal

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

<details><summary>Query Active AGV Errors From the WCS Database (`proc_query_active_agv_errors_from_the_wcs_database_v1`)</summary>

##### Runbook: Query Active AGV Errors From the WCS Database

- **Procedure ID:** `proc_query_active_agv_errors_from_the_wcs_database_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Retrieve current active AGV error records from the WCS database by logging into the WCS primary server, opening the WCS database, creating a new query tab, entering the documented SQL query against [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel], executing it, and reviewing the returned results.

**When To Use:**
Use this procedure when active AGV error records need to be retrieved from the WCS database for investigation or visibility.

**Safety Notes:**

- This is a source-backed diagnostic retrieval procedure.
- The source does not provide corrective actions for returned errors; use the output for investigation only.

- **Source:** `manual` / `active_agv_error_query_1`

**Procedure Steps:**

###### Step 1 — Log into the WCS primary server

**Responsible role:** L2_support

**Instruction:**
Log into the WCS primary server.

**Healthy condition:**
The WCS primary server is accessible and the session is opened successfully.

**Expected result:**
You are logged into the WCS primary server and can continue to the database access step.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_1_image_1](assets/dd374953acdb3906.png)

*Initial server access or login entry point associated with the first procedure step.*

![artifact_manual_active_agv_error_query_1_page_1_image_2](assets/14ea52d1bb1ce1b4.jpeg)

*Initial server access or login entry point associated with the first procedure step.*

---

###### Step 2 — Open the WCS database

**Responsible role:** L2_support

**Instruction:**
Open the WCS database.

**Healthy condition:**
The WCS database opens successfully and the query interface can be accessed.

**Expected result:**
The WCS database is open and ready for query entry.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_1_image_1](assets/dd374953acdb3906.png)

*Database access point or initial database selection area after server login.*

![artifact_manual_active_agv_error_query_1_page_1_image_2](assets/14ea52d1bb1ce1b4.jpeg)

*Database access point or initial database selection area after server login.*

---

###### Step 3 — Open a new query tab

**Responsible role:** L2_support

**Instruction:**
Open a new query tab by clicking the indicated control.

**Healthy condition:**
The new query tab appears in the database interface.

**Expected result:**
A new query tab opens and is ready for SQL entry.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_2_image_1](assets/d1aaf4391764bc2d.jpeg)

*UI control used to open a new query tab and where the new tab appears.*

![artifact_manual_active_agv_error_query_1_page_2_image_2](assets/a3cb4c312665a8da.png)

*UI control used to open a new query tab and where the new tab appears.*

---

###### Step 4 — Paste the documented SQL query into the new tab

**Responsible role:** L2_support

**Instruction:**
Copy and paste the provided SQL query into the newly opened query tab.

**Healthy condition:**
The full SQL query is visible in the new query tab.

**Expected result:**
The query editor contains the documented SQL statement.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_2_image_1](assets/d1aaf4391764bc2d.jpeg)

*Query editor area where the SQL statement should be entered.*

![artifact_manual_active_agv_error_query_1_page_2_image_2](assets/a3cb4c312665a8da.png)

*Query editor area where the SQL statement should be entered.*

---

###### Step 5 — Use the documented active AGV error query text

**Responsible role:** L2_support

**Instruction:**
Use the provided query text exactly as documented: SELECT TOP (1000) [Id], [EntityInserted], [EntityLastUpdate], [Name], [Area], [Error], [LastSeen], [SystemErrorDescription], [SystemErrorResolution] FROM [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel].

**Healthy condition:**
The query includes Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution from [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel].

**Expected result:**
The query text references the documented fields and the [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel] table.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_2_image_1](assets/d1aaf4391764bc2d.jpeg)

*Query editor area containing the pasted SQL statement.*

![artifact_manual_active_agv_error_query_1_page_2_image_2](assets/a3cb4c312665a8da.png)

*Query editor area containing the pasted SQL statement.*

---

###### Step 6 — Execute the query

**Responsible role:** L2_support

**Instruction:**
Right click on the query and click execute.

**Healthy condition:**
The query executes without blocking the results display.

**Expected result:**
The query runs and the interface proceeds to display returned results.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_2_image_1](assets/d1aaf4391764bc2d.jpeg)

*Query area where the execute action is initiated.*

![artifact_manual_active_agv_error_query_1_page_2_image_2](assets/a3cb4c312665a8da.png)

*Query area where the execute action is initiated.*

---

###### Step 7 — Review the results area

**Responsible role:** L2_support

**Instruction:**
Review the results area where the active errors appear.

**Healthy condition:**
The results panel or table is visible and populated with active error records.

**Expected result:**
A results area displays the active AGV errors returned by the query.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_4_image_1](assets/bd0e5496db114110.jpeg)

*Results panel or table where active AGV errors are shown after execution.*

![artifact_manual_active_agv_error_query_1_page_4_image_2](assets/8770cb52c8e0fa23.png)

*Results panel or table where active AGV errors are shown after execution.*

---

###### Step 8 — Check the returned fields in the results

**Responsible role:** L2_support

**Instruction:**
Check the returned fields in the results, including Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution.

**Healthy condition:**
Returned records show Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution.

**Expected result:**
The results include the documented identifier, timestamp, area, error, description, and resolution fields.

**Step Images:**

![artifact_manual_active_agv_error_query_1_page_4_image_1](assets/bd0e5496db114110.jpeg)

*Returned results table and the displayed columns for active AGV errors.*

![artifact_manual_active_agv_error_query_1_page_4_image_2](assets/8770cb52c8e0fa23.png)

*Returned results table and the displayed columns for active AGV errors.*

---

**Success Criteria:**

- The WCS primary server is accessed successfully.
- The WCS database is opened successfully.
- A new query tab is opened.
- The documented SQL query against [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel] is entered.
- The query executes successfully.
- The results area displays active AGV error records.
- Returned results include Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution.

**Failure Conditions:**

- Access to the WCS primary server is not available.
- Access to the WCS database is not available.
- A new query tab cannot be opened.
- The query cannot be executed.
- The results area does not display returned active errors.
- Expected fields are missing from the returned results.


</details>

</details>

---

### 3 — Perform authorized recovery actions to restore hospital induction and clear blocking association state (`procedure_reference`)

**Intent:** If hospital add/induct is blocked by abnormal association state or server/service issues, execute the approved recovery procedure(s) for the hospital lane/station and related OptiSweep services and/or API-based state correction as authorized.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1` (low, support, score=0.621, boosted=0.791) — Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1` (low, operator, score=0.5321, boosted=0.7021) — Start OptiSweep AGV System From Shut-down Mode (Reset Metrics → Start → Close out/Bag Out → Running)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI + RMS/WCS corroboration): Recovery restores hospital induction/add functionality and site can start sort.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI + RMS/WCS): Recovery does not restore hospital induction; site remains unable to start sort.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI + RMS/WCS): Partial improvement without clear stabilization; further evidence needed to decide continuation vs escalate.

**Branches:**

- `healthy` → `node_4` when Authorized recovery executed (OptiSweep restart and/or AGV/API corrections) and hospital add behavior changes

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

<details><summary>Start OptiSweep AGV System From Shut-down Mode (Reset Metrics → Start → Close out/Bag Out → Running) (`proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1`)</summary>

##### Runbook: Start OptiSweep AGV System From Shut-down Mode (Reset Metrics → Start → Close out/Bag Out → Running)

- **Procedure ID:** `proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the OptiSweep system screen to bring the AGV system from Shut-down Mode into the normal “Running” state by verifying the required number of empty AGVs, resetting metrics, starting the system, performing close out (Bag Out) until the system returns to “Running,” and then shutting down when finished.

**When To Use:**
Use this procedure when the OptiSweep AGV system is in Shut-down Mode and you need to start it into normal “Running” operation using the documented start-up sequence (Reset metrics → Start → Close out/Bag Out → Running).

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Verify nine (9) empty AGVs are present (5 north, 4 south)

**Responsible role:** operator

**Instruction:**
Confirm there are nine (9) AGVs without totes in the system: five (5) under the north rack and four (4) under the south rack. If not, move an AGV into the zone missing an empty AGV, then add that AGV to RMS after moving it.

**Healthy condition:**
The empty-AGV counts match the required distribution: 5 north and 4 south.

**Expected result:**
You have five (5) empty AGVs under the north rack and four (4) empty AGVs under the south rack (total nine (9) empty AGVs).

---

###### Step 2 — Open the System in Shut-down Mode screen and verify Shut-down Mode

**Responsible role:** operator

**Instruction:**
Open the system screen shown as “System in Shut-down Mode” (Figure 5-1) and verify the system mode indicates Shut-down.

**Healthy condition:**
System mode is displayed as Shut-down on the referenced system screen.

**Expected result:**
The system mode indicator on the “System in Shut-down Mode” screen shows Shut-down.

---

###### Step 3 — Reset metrics

**Responsible role:** operator

**Instruction:**
On the “System in Shut-down Mode” screen (Figure 5-1), use the control option to Reset metrics.

**Healthy condition:**
Reset metrics control is executed as part of the start-up sequence.

**Expected result:**
Metrics are reset using the Reset metrics control on the system screen.

---

###### Step 4 — Start the system

**Responsible role:** operator

**Instruction:**
On the “System in Shut-down Mode” screen (Figure 5-1), use the control to Start the system.

**Healthy condition:**
System Startup is initiated from the Shut-down Mode screen.

**Expected result:**
The system start control is executed as part of the start-up sequence.

---

###### Step 5 — Perform close out (Bag Out) until system returns to Running

**Responsible role:** operator

**Instruction:**
Perform close out (Bag Out) and continue until the system status returns to “Running.”

**Healthy condition:**
System status transitions back to “Running” after Bag Out completes.

**Expected result:**
After close out (Bag Out) is completed, the system status returns to “Running.”

---

###### Step 6 — Shut down when the start-up process is complete and you are done

**Responsible role:** operator

**Instruction:**
When the start-up process is complete and you are done with the procedure, shut down using the documented shut down step/control.

**Healthy condition:**
System Shutdown is executed after the system has returned to Running and you are done with the procedure.

**Expected result:**
System shutdown is initiated using the documented shut down control/step.

---

**Success Criteria:**

- After close out (Bag Out) is completed, the system status returns to “Running”.

**Failure Conditions:**

- System does not return to “Running” after Bag Out (Step 5).
- Precondition not met: fewer than nine (9) empty AGVs (5 north, 4 south) before starting (Step 1).


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

### 4 — Validate hospital induction and sort stability after recovery (`validation_gate`)

**Intent:** Confirm that the hospital station can add/induct totes again and that the site can start sort and remain stable.

**Expects capability:** fleet_system_status, agv_active_errors
**Expects surface:** rms_ui, wcs_sql, hospital_hmi
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6437, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.7522, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.7453, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI + RMS / AGV status UI + WCS/SSMS (read-only)): Hospital induction/add and sort stability are restored.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI + RMS / AGV status UI + WCS/SSMS (read-only)): Validation fails: hospital add remains blocked or sort cannot start/keeps going down.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI + RMS/WCS): Mixed/partial validation signals; need additional evidence or stop/escalate depending on availability.

**Branches:**

- `healthy` → `` when Validation confirms recovery completed
- `unhealthy` → `node_5` when Validation fails; escalate

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Access RMS web application via site Argus server IP and verify the RMS overview screen loads (`proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1`)</summary>

##### Runbook: Access RMS web application via site Argus server IP and verify the RMS overview screen loads

- **Procedure ID:** `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Verify that the RMS / fleet status web UI is reachable from a supported workstation using the site-provided unique IP, that login succeeds with the provided username/password, and that the RMS overview screen loads. Use this as the first connectivity/login check when troubleshooting RMS web availability.

**When To Use:**
Use when you need a first-pass check that the RMS web application is reachable and that authentication leads to the RMS overview screen (the initial landing/overview page).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS web location using the site-provided unique IP

**Responsible role:** L1_support

**Instruction:**
From a supported workstation, open a web browser and navigate to the site-provided RMS web location using the unique IP address for the RMS service.

**Healthy condition:**
The RMS web application page is reachable and displays the RMS login flow.

**Expected result:**
The RMS web application landing page loads (i.e., the browser reaches the RMS web location).

---

###### Step 2 — Authenticate on the RMS login page

**Responsible role:** L1_support

**Instruction:**
On the RMS login page, enter the username and password provided for RMS access, then submit/login.

**Healthy condition:**
After submitting credentials, the RMS overview screen is reached.

**Expected result:**
Login succeeds and the session proceeds to the RMS overview screen.

---

###### Step 3 — Verify the RMS overview screen is displayed

**Responsible role:** L1_support

**Instruction:**
After login, verify you are on the RMS overview screen (the screen described as “this is what you will see… the overview screen”).

**Healthy condition:**
The overview screen loads successfully after login.

**Expected result:**
The RMS overview screen is displayed.

---

**Success Criteria:**

- RMS web application is reachable using the site’s unique IP.
- Login succeeds using the provided username/password.
- The RMS overview screen is displayed after login.

**Failure Conditions:**

- RMS web application is unreachable (page won’t load).
- Login does not lead to the RMS overview screen.


</details>

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

### 5 — Escalate if hospital induction and sort stability cannot be restored (`escalation_gate`)

**Intent:** Stop the playbook when recovery/validation fails or evidence is insufficient to continue safely within role limits.

**Expects capability:** agv_active_errors
**Expects surface:** n/a
**Preferred audience:** n/a

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=site_or_remote; tool=Hospital HMI + RMS / WCS evidence (read-only) + site observations): Stop playbook and escalate with an evidence package because validation failed or evidence is insufficient to proceed safely.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI + RMS/WCS): Validation failure evidence exists but is incomplete; partial escalation evidence should still be prepared based on available RMS/WCS and hospital HMI indicators.

**Branches:**

- `escalate` → `` when Escalate (validation failure or insufficient evidence)

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Hospital add/induct fails and sort down/halts with abnormal fleet/system indicators | `node_2` |
| `node_1` | `inconclusive` | Hospital add/induct fails but fleet/system looks normal (localized pattern) | `node_2` |
| `node_2` | `unhealthy` | Active faults/errors or abnormal hospital-area roster/association state present | `node_3` |
| `node_2` | `healthy` | No active faults and hospital-area state appears normal | `node_3` |
| `node_3` | `healthy` | Authorized recovery executed (OptiSweep restart and/or AGV/API corrections) and hospital add behavior changes | `node_4` |
| `node_4` | `healthy` | Validation confirms recovery completed | `` |
| `node_4` | `unhealthy` | Validation fails; escalate | `node_5` |
| `node_5` | `escalate` | Escalate (validation failure or insufficient evidence) | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1 (low)
- node_1: proc_use_agv_api_controls_remove_recover_pause_resume_v1 (low)
- node_1: proc_use_hospital_hmi_remove_tote_screen_to_remove_tote_v1 (low)
- node_2: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_2: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_2: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_3: proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1 (low)
- node_3: proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1 (low)
- node_4: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_4: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_4: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
- node_5: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
