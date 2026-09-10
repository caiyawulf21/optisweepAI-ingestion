# Bag-out stoppage with immobile or out-of-sequence AGVs

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_218550_bagout_agv_sequence` |
| Case ID | `218550` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Bag-out stops after sorting or does not complete.
- The site must manually bag out or bag-out starts and later stops.
- An AGV or robot has not moved for an extended period.
- The site reports that a robot may be out of sequence or in the wrong position.
- A hospital-area HMI shows a fault or a task appears stuck.

## Affected Systems

- Bag-out workflow
- AGV or robot fleet
- RMS fleet status
- WCS or Helix database state
- Hospital-area HMI
- Tote and task state

## Nodes

### 1 — Confirm bag-out stoppage and fleet-level operating scope (`diagnostic_decision`)

**Intent:** Determine whether the reported symptom is an active bag-out interruption with an associated fleet or AGV operating abnormality rather than an isolated normal pause.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.4725, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (high, support, score=0.596, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.6323, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Bag-out is operating normally and RMS overview shows a running/normal fleet without abnormal indicators.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Active bag-out interruption with associated fleet/AGV abnormality evidence.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Cannot confirm bag-out scope or RMS overall view is unavailable/unclear.

**Branches:**

- `unhealthy` → `node_2` when Bag-out stopped or partially progressed AND RMS shows fleet/AGV abnormality
- `inconclusive` → `` when Bag-out and RMS fleet status are normal, or symptom is localized without confirmed operational impact

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

</details>

---

### 2 — Check for active AGV or system fault evidence (`diagnostic_decision`)

**Intent:** Determine whether active AGV or system-level errors correlate with the bag-out stoppage or immobile robot symptom.

**Expects capability:** agv_active_errors, wcs_system_faults
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.6698, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.7434, boosted=1.0) — Query Active AGV Errors From the WCS Database
  - gaps: Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.
- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.646, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): No active AGV/system fault evidence; AGVs appear normal and no active errors correlate with the stoppage.
- `unhealthy` (observer=remote; tool=WCS/SSMS (read-only)): Active AGV or system fault evidence present and correlated with immobile/blocked symptoms.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Fault/error details unreadable, RMS blank/unavailable, or RMS/WCS conflict without a clear affected asset.

**Branches:**

- `unhealthy` → `node_3` when Active AGV or system fault/blocked status evidence is present
- `healthy` → `` when No active AGV or system fault present and status is normal

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

</details>

---

### 3 — Determine whether AGV sequence or roster state is inconsistent (`diagnostic_decision`)

**Intent:** Determine whether a robot, AGV pair, or roster position is preventing the bag-out workflow from progressing.

**Expects capability:** device_roster_state, agv_active_errors
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.5879, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.
- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.5731, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.3, boosted=0.9200000000000002) — Query Active AGV Errors From the WCS Database
  - gaps: Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.; Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI): Roster/sequence are consistent; suspected out-of-sequence/pairing problem is not indicated by system state.
- `unhealthy` (observer=remote; tool=WCS/SSMS (read-only)): Roster/pairing/position inconsistency indicated (missing replacement, inactive/removed AGV, abnormal pair identity), consistent with blocking bag-out sequence.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Unable to reconcile due to unreadable HMI/roster data or conflicting views.

**Branches:**

- `unhealthy` → `` when Roster, pairing, position, or sequence inconsistency is indicated
- `healthy` → `` when Roster and sequence are consistent, or suspected pattern is not indicated

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

### 4 — Perform authorized AGV sequence or roster recovery (`procedure_reference`)

**Intent:** Use an approved, role-authorized AGV recovery procedure when the diagnostic path indicates an inconsistent or blocked AGV sequence, pair, or roster state.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1` (low, support, score=0.7323, boosted=0.9953) — Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1` (low, support, score=0.753, boosted=0.9667) — Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_from_agv_fault_during_exchange_recovery_v1` (low, support, score=0.7238, boosted=0.9398) — Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Authorized AGV recovery completed and system state reflects intended roster/sequence; bag-out begins/continues.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): Recovery does not stabilize operation: AGV remains inactive/inconsistent and bag-out stops again.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Recovery cannot be completed safely/authorized or system-side state is unclear.

**Branches:**

- `healthy` → `node_5` when Recovery completed and RMS/WCS state reflects intended sequence/roster
- `unhealthy` → `node_6` when Recovery is not authorized / cannot be completed safely / system state remains inconsistent

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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

</details>

---

### 5 — Validate bag-out progress and stable AGV operation (`validation_gate`)

**Intent:** Confirm that the recovery restored the affected workflow and that AGVs remain operational rather than only showing a temporary improvement.

**Expects capability:** fleet_system_status, agv_active_errors
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.4687, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (high, support, score=0.6038, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Limited domain-term overlap between placeholder and runbook.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.3, boosted=0.9200000000000002) — Query Active AGV Errors From the WCS Database
  - gaps: Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Stable recovery confirmed: bag-out progresses normally and AGVs remain operational; no recurring active faults.
- `unhealthy` (observer=remote; tool=WCS/SSMS (read-only)): Validation failure: bag-out stops again, an AGV remains inactive, or active errors recur.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Only a temporary restart or inability to confirm next operating cycle/diagnostic visibility.

**Branches:**

- `healthy` → `` when Bag-out continues and RMS/WCS evidence remains healthy
- `unhealthy` → `node_6` when Bag-out stops again OR AGV remains inactive OR active errors recur

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

### 6 — Stop and escalate when the supported recovery path does not stabilize operation (`escalation_gate`)

**Intent:** Hand off when diagnostics remain inconclusive, recovery is unauthorized or unsafe, or bag-out or AGV operation fails validation after the supported path.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=RMS / AGV status UI): Supported recovery path fails to stabilize; diagnostics inconclusive, unauthorized/unsafe recovery, or validation failed.

**Branches:**

- `escalate` → `` when Escalate: diagnostics inconclusive or bag-out/AGV operation fails validation after recovery

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Bag-out stopped or partially progressed AND RMS shows fleet/AGV abnormality | `node_2` |
| `node_1` | `inconclusive` | Bag-out and RMS fleet status are normal, or symptom is localized without confirmed operational impact | `` |
| `node_2` | `unhealthy` | Active AGV or system fault/blocked status evidence is present | `node_3` |
| `node_2` | `healthy` | No active AGV or system fault present and status is normal | `` |
| `node_3` | `unhealthy` | Roster, pairing, position, or sequence inconsistency is indicated | `` |
| `node_3` | `healthy` | Roster and sequence are consistent, or suspected pattern is not indicated | `` |
| `node_4` | `healthy` | Recovery completed and RMS/WCS state reflects intended sequence/roster | `node_5` |
| `node_4` | `unhealthy` | Recovery is not authorized / cannot be completed safely / system state remains inconsistent | `node_6` |
| `node_5` | `healthy` | Bag-out continues and RMS/WCS evidence remains healthy | `` |
| `node_5` | `unhealthy` | Bag-out stops again OR AGV remains inactive OR active errors recur | `node_6` |
| `node_6` | `escalate` | Escalate: diagnostics inconclusive or bag-out/AGV operation fails validation after recovery | `` |

## Unresolved / Low-Confidence Links

- node_2: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_2: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_2: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_3: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_3: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_3: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_4: proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1 (low)
- node_4: proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1 (low)
- node_4: proc_recover_from_agv_fault_during_exchange_recovery_v1 (low)
- node_5: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_5: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_6: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
