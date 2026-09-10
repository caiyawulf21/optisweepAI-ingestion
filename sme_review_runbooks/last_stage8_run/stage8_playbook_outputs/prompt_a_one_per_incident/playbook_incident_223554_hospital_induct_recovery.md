# Hospital tote induction failure with AGV or service-state recovery

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_recovery` |
| Case ID | `223554` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital station cannot add or induct totes, although tote removal may still work.
- A robot or AGV is reported in a shut down or abnormal state.
- The site cannot start sort, or sort stops during operation.
- Hospital backlog or abnormal tote flow is reported.
- AGVs appear in unexpected locations, duplicated under a rack, or associated with disconnected totes.

## Affected Systems

- ACB hospital station
- AGV hospital station
- AGVs and robot roster/location state
- Tote associations and hospital tote flow
- OptiSweep services
- Hospital Lane
- RMS / fleet status
- WCS / SSMS
- Hospital HMI / lane UI
- Tipper HMI / VISU

## Nodes

### 1 — Confirm hospital induction or broader sort disruption (`diagnostic_decision`)

**Intent:** Determine whether the reported issue is an observable hospital tote-induction failure with possible wider operational impact, before selecting the technical investigation path.

**Expects capability:** fleet_system_status
**Expects surface:** hospital_hmi, site_interview, rms_ui
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1` (medium, operator, score=0.5328, boosted=1.0) — Stop the OptiSweep System Using the System HMI API Screen (SYSTEM SHUTDOWN)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_tote_from_system_hospital_hmi_remove_tote_v1` (low, operator, score=0.6852, boosted=0.8152) — Remove Tote from System using Hospital HMI (Remove Tote screen)
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (high, support, score=0.3, boosted=1.15) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital add/induct and removal work normally; no active hospital disruption indicated.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Induction/add fails or backlog/disruption indicators are present.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Symptom cannot be reproduced or HMI evidence is unavailable.

**Branches:**

- `unhealthy` → `node_2` when Hospital induction or broader sort disruption confirmed
- `healthy` → `` when Normal add/induct and removal; no broader disruption

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (2)</summary>

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

<details><summary>Remove Tote from System using Hospital HMI (Remove Tote screen) (`proc_remove_tote_from_system_hospital_hmi_remove_tote_v1`)</summary>

##### Runbook: Remove Tote from System using Hospital HMI (Remove Tote screen)

- **Procedure ID:** `proc_remove_tote_from_system_hospital_hmi_remove_tote_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the Hospital HMI “Remove Tote” screen to scan the tote barcode into the Tote ID and Barcode fields, verify the extract-side position information from WCS (AGV#, Tote ID, Bar Code, Status), ensure the tote is positioned properly on the extract side, and then press CONFIRM & EXECUTE to remove the tote from the system.

**When To Use:**
When a station operator needs to remove a tote from the OptiSweep system at the Hospital Station so the required task can be performed.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the Hospital HMI “Remove Tote” screen

**Responsible role:** operator

**Instruction:**
On the Hospital HMI, open the “Remove Tote” screen.

**Healthy condition:**
Extract Position Information panel is visible and ready to display WCS-provided extract-side data (AGV#, Tote ID, Bar Code, Status).

**Expected result:**
The Hospital HMI “Remove Tote” screen is displayed with the Tote ID field, Barcode field, CONFIRM & EXECUTE button, and the Extract Position Information panel.

---

###### Step 2 — Scan tote barcode into the Tote ID field

**Responsible role:** operator

**Instruction:**
In the Tote ID area, use the green scanner to scan the tote bar code to populate the Tote ID field.

**Healthy condition:**
Tote ID field contains the scanned tote identifier.

**Expected result:**
The Tote ID field is populated after scanning.

---

###### Step 3 — Scan tote barcode into the Barcode field

**Responsible role:** operator

**Instruction:**
In the Barcode area, press the green scanner button and then scan the tote bar code to populate the Barcode field.

**Healthy condition:**
Barcode field contains the scanned bar code information.

**Expected result:**
The Barcode field is populated with the scanned information.

---

###### Step 4 — Verify Extract Position Information from WCS (extract side)

**Responsible role:** operator

**Instruction:**
Verify the “Extract Position Information” panel shows WCS data for the extract side, including AGV#, Tote ID, Bar Code, and Status.

**Healthy condition:**
Extract Position Information panel shows WCS-provided extract-side data (AGV#, Tote ID, Bar Code, Status) consistent with the tote you scanned.

**Expected result:**
Extract Position Information panel displays AGV# (AGV ID), Tote ID (tote ID), Bar Code (scanned information), and Status (status messages from WCS).

---

###### Step 5 — Ensure tote is positioned properly on the extract side

**Responsible role:** operator

**Instruction:**
Ensure the tote is positioned properly on the extract side.

**Healthy condition:**
Tote is correctly placed on the extract side so the removal action can be executed.

**Expected result:**
The tote is physically positioned properly on the extract side of the Hospital Station.

---

###### Step 6 — Press CONFIRM & EXECUTE to remove the tote

**Responsible role:** operator

**Instruction:**
Press CONFIRM & EXECUTE to remove the tote from the system.

**Healthy condition:**
Removal completes successfully and the workflow proceeds for the station operator’s task.

**Expected result:**
The tote is removed from the system after pressing CONFIRM & EXECUTE (with the tote positioned properly on the extract side).

---

###### Step 7 — Use the “1.1 Add Tote” shortcut only if you need to navigate

**Responsible role:** operator

**Instruction:**
Use the “1.1 Add Tote” shortcut button only if you need to navigate to the Add Tote screen.

**Healthy condition:**
You remain on the Remove Tote screen unless navigation is necessary.

**Expected result:**
You navigate to the “Add Tote” screen only when required.

---

**Success Criteria:**

- Tote is removed from the system after pressing CONFIRM & EXECUTE with the tote positioned properly on the extract side.
- Extract Position Information panel shows WCS-provided extract-side data (AGV#, Tote ID, Bar Code, Status) for the tote/AGV being removed.

**Failure Conditions:**

- Extract Position Information (AGV#, Tote ID, Bar Code, Status) does not reflect the expected extract-side tote/AGV.
- Tote ID and/or Barcode fields do not populate correctly after scanning.


</details>

</details>

<details><summary><strong>Support runbooks</strong> (1)</summary>

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

</details>

---

### 2 — Check AGV roster, location, active errors, and tote association state (`diagnostic_decision`)

**Intent:** Determine whether the hospital symptom correlates with an AGV in an unexpected location, duplicate occupancy, disconnected tote, or other abnormal fleet or association state.

**Expects capability:** device_roster_state, agv_active_errors
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.6543, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.
- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.6436, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.3, boosted=1.2437) — Query Active AGV Errors From the WCS Database
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI + WCS/SSMS (read-only)): AGV roster/location, active-error state, and tote associations are normal; no disconnected/inconsistent association evidence.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI + WCS/SSMS (read-only)): Unexpected AGV location/duplicate occupancy/shutdown state or disconnected/inconsistent tote association is indicated.
- `inconclusive` (observer=remote; tool=RMS / WCS-SSMS read-only): RMS, WCS/SSMS, and site observations disagree or required records are unavailable.

**Branches:**

- `unhealthy` → `node_4` when Unexpected AGV/tote association state indicated
- `healthy` → `node_3` when Fleet/association checks normal

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed) (`proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`)</summary>

##### Runbook: Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)

- **Procedure ID:** `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Get AGV Status view (RMS / fleet status UI) to confirm the current AGV state, current command vitals (described as “teal vitals”), and whether the HMI error alert flag is set to true and bubbles to the top when an AGV error or system error is active.

**When To Use:**
Use when you need to verify whether any AGV errors or system errors are currently active and are being surfaced by the Get AGV Status HMI error alert behavior (alert becomes true and bubbles to the top).

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open Get AGV Status view and locate AGV state, teal command vitals, and error sections

**Responsible role:** L1_support

**Instruction:**
Open the live Get AGV Status view/screen in the RMS / fleet status UI that shows: (1) AGV state, (2) current command vitals (described as “teal vitals”), and (3) sections for AGV errors and system errors.

**Healthy condition:**
For the AGV(s) shown, the screen is populated with AGV state and teal vitals, and the AGV errors/system errors sections are present for evaluation.

**Expected result:**
The Get AGV Status screen displays AGV state, current command vitals (“teal vitals”), and areas where AGV errors and system errors are shown.

---

###### Step 2 — Verify displayed AGV state and current command vitals (teal vitals) for a selected AGV entry

**Responsible role:** L1_support

**Instruction:**
Select an AGV row/entry on the Get AGV Status screen and verify the displayed AGV state and the current command vitals (described as “teal vitals”).

**Healthy condition:**
AGV state and teal vitals are present for the selected AGV entry.

**Expected result:**
For the selected AGV entry, the AGV state and teal vitals are populated and visible on the Get AGV Status screen.

---

###### Step 3 — Check error alert flag behavior (must be true and bubble to the top when an error exists)

**Responsible role:** L1_support

**Instruction:**
On the Get AGV Status screen, check whether an error alert is present and whether it is set to true when there is an error (system error or “geek error”). Confirm that the alert bubbles to the top in the HMI when errors exist.

**Healthy condition:**
With an active error condition, the error alert changes to true and appears at the top (bubbles up).

**Expected result:**
When an AGV error or system error exists, the error alert flag is set to true and bubbles to the top in the HMI.

---

###### Step 4 — Confirm AGV errors and/or system errors sections are populated when the alert indicates an error

**Responsible role:** L1_support

**Instruction:**
If the error alert indicates an error, confirm the Get AGV Status screen is showing AGV errors and/or system errors (described as being populated from the system faults table / active faults).

**Healthy condition:**
AGV errors and/or system errors lists/fields contain entries consistent with the active error condition.

**Expected result:**
When the error alert indicates an error, the AGV errors and/or system errors sections on the Get AGV Status screen are populated.

---

**Success Criteria:**

- When an AGV error or system error exists, the Get AGV Status HMI error alert flag is set to true and bubbles to the top.
- For the selected AGV entry, AGV state and current command vitals (“teal vitals”) are populated.
- When the error alert indicates an error, the AGV errors and/or system errors sections are populated.

**Failure Conditions:**

- Error alert is not set to true while an active AGV/system error condition is observed.
- Error alert does not bubble to the top in the HMI despite an observed AGV/system error.
- Error alert indicates an error but AGV errors/system errors sections are not populated as expected.


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

### 3 — Check OptiSweep service and related host health (`diagnostic_decision`)

**Intent:** Determine whether an abnormal OptiSweep or AGV hospital-station service state is contributing to the induction or sort disruption.

**Expects capability:** windows_service_or_event_log, wcs_api_responsiveness
**Expects surface:** event_viewer, wcs_api
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.5038, boosted=1.0) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_current_tote_task_and_resend_tote_task_v1` (low, support, score=0.3274, boosted=0.5474) — Check current tote task and resend tote task command using the Tote Management API page (Obeyba/Aveva API features)
  - gaps: Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Retrieval score 0.3274 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.4803, boosted=0.5303) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Windows Services + Event Viewer (and WCS/OptiSweep API)): OptiSweep/WCS services are healthy and API responsiveness is normal; no service termination evidence.
- `unhealthy` (observer=remote; tool=Windows Services + Event Viewer (and WCS/OptiSweep API)): Relevant OptiSweep/WCS service is stopped/restarting or API responsiveness is abnormal.
- `inconclusive` (observer=remote; tool=Windows Services + Event Viewer (and WCS/OptiSweep API)): Service names/logs unavailable or service/API evidence disagrees.

**Branches:**

- `unhealthy` → `node_4` when OptiSweep/WCS service abnormality indicated
- `inconclusive` → `node_4` when Service checks healthy but symptom persists/inconclusive evidence

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests (`proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1`)</summary>

##### Runbook: Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests

- **Procedure ID:** `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1`
- **Procedure Type:** `operation`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the OptiSweep / WCS API client to send a Geek request to remove a specified AGV from the system (RemoveAgv) or re-add it (RecoverAGV). Both API actions require the target robot ID.

**When To Use:**
When you need to remove a specific AGV from the system roster (RemoveAgv) or re-add it (RecoverAGV) by sending the correct OptiSweep→Geek API request using the required robot ID.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Identify the target AGV robot ID for the API request

**Responsible role:** L2_support

**Instruction:**
Obtain the target AGV's robot ID that you will enter into the OptiSweep / WCS API request.

**Healthy condition:**
The robot ID you plan to use corresponds to the intended AGV you are trying to remove/recover.

**Expected result:**
You have a specific robot ID value ready to use for the RemoveAgv and RecoverAGV requests.

---

###### Step 2 — Select RemoveAgv in the OptiSweep / WCS API client and confirm it targets Geek removal by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RemoveAgv and confirm it is described as requiring the robot ID and sending a request to Geek to remove the specified AGV from the system.

**Healthy condition:**
RemoveAgv is the selected action and its description matches: requires robot ID; sends request to Geek to remove the specified AGV from the system.

**Expected result:**
The RemoveAgv action is selected in the API client and is associated with the robot ID input requirement.

---

###### Step 3 — Submit RemoveAgv request with the target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RemoveAgv request in the Apidog / WCS API client using the target robot ID you identified.

**Healthy condition:**
The API client response indicates the request was accepted/executed for RemoveAgv.

**Expected result:**
The RemoveAgv request is submitted and you receive an observable API client response indicating acceptance/execution (success or error).

---

###### Step 4 — Verify RemoveAgv request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RemoveAgv request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Healthy condition:**
Response indicates the request was accepted/executed for RemoveAgv.

**Expected result:**
The API client response for RemoveAgv shows an observable success/acceptance indicator (or an error indicator if it failed).

---

###### Step 5 — Select RecoverAGV in the OptiSweep / WCS API client and confirm it targets Geek add by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RecoverAGV and confirm it is described as requiring the robot ID and sending a request to Geek to add the specified AGV to the system.

**Healthy condition:**
RecoverAGV is the selected action and its description matches: requires robot ID; sends request to Geek to add the specified AGV to the system.

**Expected result:**
The RecoverAGV action is selected in the API client and is associated with the robot ID input requirement.

---

###### Step 6 — Submit RecoverAGV request with the same target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RecoverAGV request in the Apidog / WCS API client using the same robot ID used for RemoveAgv.

**Healthy condition:**
The API client response indicates the request was accepted/executed for RecoverAGV.

**Expected result:**
The RecoverAGV request is submitted and you receive an observable API client response indicating acceptance/success (or error).

---

###### Step 7 — Verify RecoverAGV request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RecoverAGV request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Healthy condition:**
Response indicates the request was accepted/executed for RecoverAGV.

**Expected result:**
The API client response for RecoverAGV shows an observable success/acceptance indicator (or an error indicator if it failed).

---

**Success Criteria:**

- RemoveAgv request is accepted/executed for the specified robot ID (observable success/acceptance in the API client response).
- RecoverAGV request is accepted/executed for the same robot ID (observable success/acceptance in the API client response).

**Failure Conditions:**

- API client response indicates RemoveAgv failed/error.
- API client response indicates RecoverAGV failed/error.
- Robot ID is incorrect or missing (request cannot target intended AGV).


</details>

<details><summary>Check current tote task and resend tote task command using the Tote Management API page (Obeyba/Aveva API features) (`proc_check_current_tote_task_and_resend_tote_task_v1`)</summary>

##### Runbook: Check current tote task and resend tote task command using the Tote Management API page (Obeyba/Aveva API features)

- **Procedure ID:** `proc_check_current_tote_task_and_resend_tote_task_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the AVEVA/Obeyba “API Features for Tote Management” page to retrieve the current tote task (“Get Tote Task”) and, when a tote command previously errored or failed to execute, resend it (“Resend Tote Task”). Confirm the “Get Tote Task” output updates after resending.

**When To Use:**
When a tote task command encountered an error or failed to execute and you need to verify the current tote task and resend the tote task command using the Tote Management API features page.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the Tote Management API features page (Obeyba/Aveva)

**Responsible role:** L2_support

**Instruction:**
Open the AVEVA/Obeyba page titled like “API Features for Tote Management” that contains the controls “Get Tote Task” and “Resend Tote Task”.

**Healthy condition:**
Both “Get Tote Task” and “Resend Tote Task” are visible on the Tote Management API features page.

**Expected result:**
The page shows the “Get Tote Task” and “Resend Tote Task” controls.

---

###### Step 2 — Confirm you are logged in to Obeyba

**Responsible role:** L2_support

**Instruction:**
On the Tote Management API features page, confirm the login state indicates you are logged in to Obeyba before using “Get Tote Task” or “Resend Tote Task”.

**Healthy condition:**
No “not logged in” condition is present; API controls can be used.

**Expected result:**
You are logged in to Obeyba (login indicator/prompt is not blocking API actions).

---

###### Step 3 — Retrieve the current tote task using “Get Tote Task”

**Responsible role:** L2_support

**Instruction:**
Use the “Get Tote Task” function on the Tote Management API features page to retrieve the current tote task.

**Healthy condition:**
“Get Tote Task” returns current tote task data (not blank/no data).

**Expected result:**
The “Get Tote Task” output populates with the current tote task information.

---

###### Step 4 — Resend the tote task command using “Resend Tote Task” (only when needed)

**Responsible role:** L2_support

**Instruction:**
If the tote task previously encountered an error or failed to execute, use “Resend Tote Task” on the same Tote Management API features page to resend the command.

**Healthy condition:**
Resend is performed for the tote task that needs re-issuing.

**Expected result:**
The “Resend Tote Task” action is executed (command resent) for the tote that previously errored/failed.

---

###### Step 5 — Verify “Get Tote Task” output updates after resending

**Responsible role:** L2_support

**Instruction:**
Run “Get Tote Task” again and compare the output to the prior “Get Tote Task” results to confirm the tote task information updates after resending.

**Healthy condition:**
The “Get Tote Task” output changes to reflect the resent command (observable update in the output fields).

**Expected result:**
After “Resend Tote Task”, the “Get Tote Task” output reflects the current tote task (task state/values update rather than remaining unchanged in the prior failed/error state).

---

**Success Criteria:**

- “Get Tote Task” returns current tote task data (not blank/no data).
- After “Resend Tote Task”, a subsequent “Get Tote Task” shows observable updates (task state/values change rather than remaining in the prior failed/error state).

**Failure Conditions:**

- “Get Tote Task” returns blank/no data or does not return a current task.
- “Resend Tote Task” produces no observable change in the subsequent “Get Tote Task” output.
- The page indicates you are not logged in to Obeyba.


</details>

<details><summary>Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed) (`proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`)</summary>

##### Runbook: Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)

- **Procedure ID:** `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Get AGV Status view (RMS / fleet status UI) to confirm the current AGV state, current command vitals (described as “teal vitals”), and whether the HMI error alert flag is set to true and bubbles to the top when an AGV error or system error is active.

**When To Use:**
Use when you need to verify whether any AGV errors or system errors are currently active and are being surfaced by the Get AGV Status HMI error alert behavior (alert becomes true and bubbles to the top).

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open Get AGV Status view and locate AGV state, teal command vitals, and error sections

**Responsible role:** L1_support

**Instruction:**
Open the live Get AGV Status view/screen in the RMS / fleet status UI that shows: (1) AGV state, (2) current command vitals (described as “teal vitals”), and (3) sections for AGV errors and system errors.

**Healthy condition:**
For the AGV(s) shown, the screen is populated with AGV state and teal vitals, and the AGV errors/system errors sections are present for evaluation.

**Expected result:**
The Get AGV Status screen displays AGV state, current command vitals (“teal vitals”), and areas where AGV errors and system errors are shown.

---

###### Step 2 — Verify displayed AGV state and current command vitals (teal vitals) for a selected AGV entry

**Responsible role:** L1_support

**Instruction:**
Select an AGV row/entry on the Get AGV Status screen and verify the displayed AGV state and the current command vitals (described as “teal vitals”).

**Healthy condition:**
AGV state and teal vitals are present for the selected AGV entry.

**Expected result:**
For the selected AGV entry, the AGV state and teal vitals are populated and visible on the Get AGV Status screen.

---

###### Step 3 — Check error alert flag behavior (must be true and bubble to the top when an error exists)

**Responsible role:** L1_support

**Instruction:**
On the Get AGV Status screen, check whether an error alert is present and whether it is set to true when there is an error (system error or “geek error”). Confirm that the alert bubbles to the top in the HMI when errors exist.

**Healthy condition:**
With an active error condition, the error alert changes to true and appears at the top (bubbles up).

**Expected result:**
When an AGV error or system error exists, the error alert flag is set to true and bubbles to the top in the HMI.

---

###### Step 4 — Confirm AGV errors and/or system errors sections are populated when the alert indicates an error

**Responsible role:** L1_support

**Instruction:**
If the error alert indicates an error, confirm the Get AGV Status screen is showing AGV errors and/or system errors (described as being populated from the system faults table / active faults).

**Healthy condition:**
AGV errors and/or system errors lists/fields contain entries consistent with the active error condition.

**Expected result:**
When the error alert indicates an error, the AGV errors and/or system errors sections on the Get AGV Status screen are populated.

---

**Success Criteria:**

- When an AGV error or system error exists, the Get AGV Status HMI error alert flag is set to true and bubbles to the top.
- For the selected AGV entry, AGV state and current command vitals (“teal vitals”) are populated.
- When the error alert indicates an error, the AGV errors and/or system errors sections are populated.

**Failure Conditions:**

- Error alert is not set to true while an active AGV/system error condition is observed.
- Error alert does not bubble to the top in the HMI despite an observed AGV/system error.
- Error alert indicates an error but AGV errors/system errors sections are not populated as expected.


</details>

</details>

---

### 4 — Perform approved service or state recovery (`procedure_reference`)

**Intent:** Use the authorized recovery path indicated by the diagnostic evidence, which may include OptiSweep service recovery and correction of supported AGV or tote state through the approved operational interface.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, operator

**Runbook Links:**

- `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1` (low, support, score=0.7056, boosted=0.8756) — Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=WCS/OptiSweep API + relevant service interfaces): Approved recovery completed safely; supported state corrections accepted; affected workflow can proceed.
- `unhealthy` (observer=remote; tool=WCS/OptiSweep API + service interfaces): Recovery action rejected or state remains inconsistent; recovery requires unsupported mutation or unsafe physical intervention.
- `inconclusive` (observer=remote; tool=WCS/OptiSweep API / service interfaces): Cannot confirm recovery completion from responsible interface.

**Branches:**

- `healthy` → `node_5` when Approved recovery completed
- `unhealthy` → `node_6` when Recovery/confirmation fails

**Linked Runbook Procedures:**

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

### 5 — Validate induction, fleet state, and stable operation (`validation_gate`)

**Intent:** Confirm that hospital tote handling and broader automated operation have recovered and remain stable after the approved recovery path.

**Expects capability:** fleet_system_status, wcs_api_responsiveness
**Expects surface:** hospital_hmi, rms_ui, wcs_api, event_viewer
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.4722, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.6272, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.4834, boosted=1.09) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI + RMS / services + WCS/OptiSweep API): Induction/removal works; expected fleet state restored; operation remains stable with no immediate recurrence.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI + RMS / Windows Services / WCS-OptiSweep API): Induction still fails and/or fleet/service/API health degrades or sort fails again during validation.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / RMS): Only generic statement that system is running; cannot confirm workflow/fleet confirmation.

**Branches:**

- `healthy` → `` when Stable recovery validated
- `unhealthy` → `node_6` when Validation failure/reoccurrence

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

<details><summary>Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed) (`proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`)</summary>

##### Runbook: Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)

- **Procedure ID:** `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Get AGV Status view (RMS / fleet status UI) to confirm the current AGV state, current command vitals (described as “teal vitals”), and whether the HMI error alert flag is set to true and bubbles to the top when an AGV error or system error is active.

**When To Use:**
Use when you need to verify whether any AGV errors or system errors are currently active and are being surfaced by the Get AGV Status HMI error alert behavior (alert becomes true and bubbles to the top).

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open Get AGV Status view and locate AGV state, teal command vitals, and error sections

**Responsible role:** L1_support

**Instruction:**
Open the live Get AGV Status view/screen in the RMS / fleet status UI that shows: (1) AGV state, (2) current command vitals (described as “teal vitals”), and (3) sections for AGV errors and system errors.

**Healthy condition:**
For the AGV(s) shown, the screen is populated with AGV state and teal vitals, and the AGV errors/system errors sections are present for evaluation.

**Expected result:**
The Get AGV Status screen displays AGV state, current command vitals (“teal vitals”), and areas where AGV errors and system errors are shown.

---

###### Step 2 — Verify displayed AGV state and current command vitals (teal vitals) for a selected AGV entry

**Responsible role:** L1_support

**Instruction:**
Select an AGV row/entry on the Get AGV Status screen and verify the displayed AGV state and the current command vitals (described as “teal vitals”).

**Healthy condition:**
AGV state and teal vitals are present for the selected AGV entry.

**Expected result:**
For the selected AGV entry, the AGV state and teal vitals are populated and visible on the Get AGV Status screen.

---

###### Step 3 — Check error alert flag behavior (must be true and bubble to the top when an error exists)

**Responsible role:** L1_support

**Instruction:**
On the Get AGV Status screen, check whether an error alert is present and whether it is set to true when there is an error (system error or “geek error”). Confirm that the alert bubbles to the top in the HMI when errors exist.

**Healthy condition:**
With an active error condition, the error alert changes to true and appears at the top (bubbles up).

**Expected result:**
When an AGV error or system error exists, the error alert flag is set to true and bubbles to the top in the HMI.

---

###### Step 4 — Confirm AGV errors and/or system errors sections are populated when the alert indicates an error

**Responsible role:** L1_support

**Instruction:**
If the error alert indicates an error, confirm the Get AGV Status screen is showing AGV errors and/or system errors (described as being populated from the system faults table / active faults).

**Healthy condition:**
AGV errors and/or system errors lists/fields contain entries consistent with the active error condition.

**Expected result:**
When the error alert indicates an error, the AGV errors and/or system errors sections on the Get AGV Status screen are populated.

---

**Success Criteria:**

- When an AGV error or system error exists, the Get AGV Status HMI error alert flag is set to true and bubbles to the top.
- For the selected AGV entry, AGV state and current command vitals (“teal vitals”) are populated.
- When the error alert indicates an error, the AGV errors and/or system errors sections are populated.

**Failure Conditions:**

- Error alert is not set to true while an active AGV/system error condition is observed.
- Error alert does not bubble to the top in the HMI despite an observed AGV/system error.
- Error alert indicates an error but AGV errors/system errors sections are not populated as expected.


</details>

<details><summary>Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests (`proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1`)</summary>

##### Runbook: Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests

- **Procedure ID:** `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1`
- **Procedure Type:** `operation`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the OptiSweep / WCS API client to send a Geek request to remove a specified AGV from the system (RemoveAgv) or re-add it (RecoverAGV). Both API actions require the target robot ID.

**When To Use:**
When you need to remove a specific AGV from the system roster (RemoveAgv) or re-add it (RecoverAGV) by sending the correct OptiSweep→Geek API request using the required robot ID.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Identify the target AGV robot ID for the API request

**Responsible role:** L2_support

**Instruction:**
Obtain the target AGV's robot ID that you will enter into the OptiSweep / WCS API request.

**Healthy condition:**
The robot ID you plan to use corresponds to the intended AGV you are trying to remove/recover.

**Expected result:**
You have a specific robot ID value ready to use for the RemoveAgv and RecoverAGV requests.

---

###### Step 2 — Select RemoveAgv in the OptiSweep / WCS API client and confirm it targets Geek removal by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RemoveAgv and confirm it is described as requiring the robot ID and sending a request to Geek to remove the specified AGV from the system.

**Healthy condition:**
RemoveAgv is the selected action and its description matches: requires robot ID; sends request to Geek to remove the specified AGV from the system.

**Expected result:**
The RemoveAgv action is selected in the API client and is associated with the robot ID input requirement.

---

###### Step 3 — Submit RemoveAgv request with the target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RemoveAgv request in the Apidog / WCS API client using the target robot ID you identified.

**Healthy condition:**
The API client response indicates the request was accepted/executed for RemoveAgv.

**Expected result:**
The RemoveAgv request is submitted and you receive an observable API client response indicating acceptance/execution (success or error).

---

###### Step 4 — Verify RemoveAgv request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RemoveAgv request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Healthy condition:**
Response indicates the request was accepted/executed for RemoveAgv.

**Expected result:**
The API client response for RemoveAgv shows an observable success/acceptance indicator (or an error indicator if it failed).

---

###### Step 5 — Select RecoverAGV in the OptiSweep / WCS API client and confirm it targets Geek add by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RecoverAGV and confirm it is described as requiring the robot ID and sending a request to Geek to add the specified AGV to the system.

**Healthy condition:**
RecoverAGV is the selected action and its description matches: requires robot ID; sends request to Geek to add the specified AGV to the system.

**Expected result:**
The RecoverAGV action is selected in the API client and is associated with the robot ID input requirement.

---

###### Step 6 — Submit RecoverAGV request with the same target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RecoverAGV request in the Apidog / WCS API client using the same robot ID used for RemoveAgv.

**Healthy condition:**
The API client response indicates the request was accepted/executed for RecoverAGV.

**Expected result:**
The RecoverAGV request is submitted and you receive an observable API client response indicating acceptance/success (or error).

---

###### Step 7 — Verify RecoverAGV request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RecoverAGV request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Healthy condition:**
Response indicates the request was accepted/executed for RecoverAGV.

**Expected result:**
The API client response for RecoverAGV shows an observable success/acceptance indicator (or an error indicator if it failed).

---

**Success Criteria:**

- RemoveAgv request is accepted/executed for the specified robot ID (observable success/acceptance in the API client response).
- RecoverAGV request is accepted/executed for the same robot ID (observable success/acceptance in the API client response).

**Failure Conditions:**

- API client response indicates RemoveAgv failed/error.
- API client response indicates RecoverAGV failed/error.
- Robot ID is incorrect or missing (request cannot target intended AGV).


</details>

</details>

---

### 6 — Stop and escalate when supported recovery or validation fails (`escalation_gate`)

**Intent:** Hand off when the evidence does not support a safe authorized recovery path, when required access or procedures are unavailable, or when the incident remains unresolved after recovery and validation.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=N/A (handoff preparation)): Diagnostics are inconclusive or approved recovery/validation cannot be completed safely; handoff to technical owner required.

**Branches:**

- `escalate` → `` when Enter escalation handoff

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Hospital induction or broader sort disruption confirmed | `node_2` |
| `node_1` | `healthy` | Normal add/induct and removal; no broader disruption | `` |
| `node_2` | `unhealthy` | Unexpected AGV/tote association state indicated | `node_4` |
| `node_2` | `healthy` | Fleet/association checks normal | `node_3` |
| `node_3` | `unhealthy` | OptiSweep/WCS service abnormality indicated | `node_4` |
| `node_3` | `inconclusive` | Service checks healthy but symptom persists/inconclusive evidence | `node_4` |
| `node_4` | `healthy` | Approved recovery completed | `node_5` |
| `node_4` | `unhealthy` | Recovery/confirmation fails | `node_6` |
| `node_5` | `healthy` | Stable recovery validated | `` |
| `node_5` | `unhealthy` | Validation failure/reoccurrence | `node_6` |
| `node_6` | `escalate` | Enter escalation handoff | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_remove_tote_from_system_hospital_hmi_remove_tote_v1 (low)
- node_2: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_2: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_2: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_3: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_3: proc_check_current_tote_task_and_resend_tote_task_v1 (low)
- node_3: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_4: proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1 (low)
- node_5: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_5: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_5: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_6: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
