# Bag-out stops after sorting; restore correct AGV/robot sequencing and clear active faults

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_218550_bagout_stopped_after_sorting_sequence_check` |
| Case ID | `218550` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- System stops at bag-out after sorting
- Manual bagging out is required
- An AGV/robot appears not to move for an extended period (e.g., hours)
- Hospital-area HMI shows a fault during the stoppage
- Site suspects a robot/AGV is out of sequence/position

## Affected Systems

- bag-out stage
- AGV / robots
- RMS
- AVEVA (screen visibility context only)
- Hospital HMI
- WCS / Helix DB (SSMS) active error views (diagnostic target)

## Nodes

### 1 — Confirm the stoppage pattern and determine whether active AGV/system faults are present (`diagnostic_decision`)

**Intent:** Determine whether the bag-out stoppage correlates with active AGV errors and/or system-level active faults that would explain why bag-out cannot progress.

**Expects capability:** agv_active_errors, fleet_system_status, wcs_system_faults
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.7556, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.8675, boosted=1.0) — Query Active AGV Errors From the WCS Database
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.7821, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): No relevant active AGV errors or system active faults found while bag-out is stuck.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Active AGV/system faults are present and consistent with the bag-out stoppage pattern.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Faults cannot be confirmed via RMS/WCS/SSMS or views are unavailable/blank while the site reports bag-out is stuck.

**Branches:**

- `unhealthy` → `node_2` when Active AGV/system faults present
- `inconclusive` → `node_2` when No active faults found / inconclusive

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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

### 2 — Restore correct AGV/robot sequence/roster state to restart bag-out (`procedure_reference`)

**Intent:** Apply the supported recovery approach to re-establish proper AGV/robot sequencing/roster state so bag-out can progress.

**Expects capability:** agv_physical_recovery, agv_active_errors
**Expects surface:** physical_floor, rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1` (medium, operator, score=1.0, boosted=1.0) — Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_agv_api_controls_remove_recover_pause_resume_v1` (high, operator, score=0.9463, boosted=1.0) — Use AGV API Controls to Remove/Recover an AGV and Pause/Resume All AGVs
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Sequence/roster restoration succeeded; bag-out progresses beyond the previously stuck stage.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Bag-out still does not progress; manual bagging out is still required.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Recovery action was performed but site cannot yet confirm progression or faults due to access/visibility limits.

**Branches:**

- `healthy` → `node_3` when Bag-out progression resumes
- `unhealthy` → `node_1` when Bag-out stops again / manual bagging still required

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (2)</summary>

<details><summary>Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET (`proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1`)</summary>

##### Runbook: Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET

- **Procedure ID:** `proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1`
- **Procedure Type:** `recovery`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
For an AGV motionless on the floor (fault), locate the faulted AGV (optionally using RMS to identify the AGV error), stop the appropriate E-stop zone using the E-stop zone map, remove the faulted AGV, pull the E-STOP, and press the blue RESET button to resume operation.

**When To Use:**
Use when an AGV is motionless on the floor and the issue is identified as a fault, requiring physical removal of the faulted AGV and an E-stop zone reset to resume system operation.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Locate the faulted AGV (use RMS if needed)

**Responsible role:** operator

**Instruction:**
If the faulted AGV is not immediately obvious, use the RMS / fleet status UI to identify the AGV error/faulted unit.

**Healthy condition:**
RMS indicates the faulted AGV/error state for the unit you are targeting for removal.

**Expected result:**
You have identified the faulted AGV that is motionless on the floor.

---

###### Step 2 — Stop the appropriate E-stop zone using the E-stop zone map

**Responsible role:** operator

**Instruction:**
Reference the E-stop zone map and press the E-STOP for the appropriate E-stop zone.

**Healthy condition:**
The E-stop you pressed corresponds to the zone for the faulted AGV identified in Step 1.

**Expected result:**
The appropriate E-stop zone is stopped.

---

###### Step 3 — Remove the faulted AGV

**Responsible role:** operator

**Instruction:**
Remove the faulted AGV from the floor/system area.

**Healthy condition:**
The faulted AGV is no longer present in the faulted location/zone.

**Expected result:**
The faulted AGV has been removed.

---

###### Step 4 — Pull the E-STOP

**Responsible role:** operator

**Instruction:**
Pull the E-STOP.

**Healthy condition:**
E-STOP is in the pulled state as part of the reset procedure.

**Expected result:**
The E-STOP has been pulled (reset sequence is ready for blue RESET).

---

###### Step 5 — Press the blue RESET button

**Responsible role:** operator

**Instruction:**
Press the blue RESET button.

**Healthy condition:**
System operation resumes (no longer remains in the faulted/stopped state).

**Expected result:**
The system resumes operation after the reset.

---

###### Step 6 — Confirm the system resumes operation

**Responsible role:** operator

**Instruction:**
Confirm that the system resumes operation following the blue RESET.

**Healthy condition:**
System is running/operational after reset.

**Expected result:**
Operation resumes.

---

**Success Criteria:**

- After pulling the E-STOP and pressing the blue RESET button, the system resumes operation.

**Failure Conditions:**

- System does not resume operation after pressing the blue RESET button.
- RMS does not clearly identify the faulted AGV.


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

</details>

---

### 3 — Validate bag-out progression and fault clearance after sequence restoration (`validation_gate`)

**Intent:** Confirm that bag-out can proceed normally and that the relevant active fault indicators are cleared or no longer blocking progression.

**Expects capability:** agv_active_errors, fleet_system_status, wcs_system_faults
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.7217, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.8404, boosted=1.0) — Query Active AGV Errors From the WCS Database
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.7801, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Bag-out progresses normally and relevant active faults are cleared.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Recovery not stable; bag-out still blocks or faults remain active.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI; WCS/SSMS (read-only)): Conflicting evidence: faults cleared but bag-out still blocks, or tools unavailable.

**Branches:**

- `healthy` → `` when Validation pass: bag-out proceeds
- `unhealthy` → `node_1` when Validation fail / inconclusive

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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
| `node_1` | `unhealthy` | Active AGV/system faults present | `node_2` |
| `node_1` | `inconclusive` | No active faults found / inconclusive | `node_2` |
| `node_2` | `healthy` | Bag-out progression resumes | `node_3` |
| `node_2` | `unhealthy` | Bag-out stops again / manual bagging still required | `node_1` |
| `node_3` | `healthy` | Validation pass: bag-out proceeds | `` |
| `node_3` | `unhealthy` | Validation fail / inconclusive | `node_1` |

## Unresolved / Low-Confidence Links

- node_1: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_1: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_1: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
- node_3: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_3: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_3: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
