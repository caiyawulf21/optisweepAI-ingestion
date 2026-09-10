# Bag-out after sorting stops; restore AGV/robot sequencing and motion

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_218550_bagout_after_sorting_agv_sequence_or_inactive` |
| Case ID | `218550` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- “The system stopped at bag-out after sorting.”
- “We had to manually bag out.”
- “An AGV hasn’t moved for hours.”
- “It looks like a robot/AGV is out of sequence.”

## Affected Systems

- bag-out stage
- AGV / robots
- RMS
- WCS database / SSMS (read-only diagnostic surface)
- Aveva screen visibility context (as a constraint on what can be observed)

## Nodes

### 1 — Confirm the stoppage pattern and whether AGVs/robots show abnormal active errors or inactivity (`diagnostic_decision`)

**Intent:** Decide whether the bag-out stoppage is accompanied by observable AGV/robot abnormal state (active errors/faults) or prolonged inactivity that would plausibly block bag-out progression.

**Expects capability:** agv_active_errors
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L2_support, operator

**Runbook Links:**

- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (medium, support, score=0.8388, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (high, support, score=0.8443, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (high, support, score=0.3, boosted=1.21) — Query Active AGV Errors From the WCS Database
  - gaps: Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): No relevant active AGV/robot faults and no evidence of prolonged inactivity that would plausibly block bag-out.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Active AGV/robot errors and/or a clearly abnormal inactivity pattern is present.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): RMS/WCS evidence is unavailable, inaccessible, or ambiguous.

**Branches:**

- `unhealthy` → `node_2` when RMS and/or WCS evidence shows active errors and/or prolonged inactivity
- `inconclusive` → `` when No relevant active errors/inactivity found

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

### 2 — Restore correct AGV/robot sequencing and resume automatic bag-out (`procedure_reference`)

**Intent:** Apply the incident-evidenced orchestration approach to restore proper sequence/motion so bag-out can continue automatically (without embedding exact runbook steps in the playbook).

**Expects capability:** agv_active_errors
**Expects surface:** n/a
**Preferred audience:** n/a

**Runbook Links:**

- `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1` (medium, support, score=0.7058, boosted=1.0) — Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger
  - gaps: Limited domain-term overlap between placeholder and runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Bag-out progresses beyond the previously stuck point and sequence/membership state becomes consistent.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Recovery did not resolve the abnormal state; bag-out stops again quickly.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Behavior changes but evidence is insufficient/ambiguous.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger (`proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1`)</summary>

##### Runbook: Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger

- **Procedure ID:** `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI to determine whether AGVs are not progressing due to state-transition failure visibility patterns: (1) AGVs waiting to do an exchange during shutdown, and/or (2) startup delay while waiting for an AGV on the charger. The system is described as exposing this via system faults and visible waiting conditions.

**When To Use:**
Use when lifecycle progression appears delayed during shutdown/startup and you need to check whether RMS is showing AGVs in the documented waiting/fault visibility patterns (exchange-waiting during shutdown; charger-waiting startup delay).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI and navigate to AGV status/errors overview

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV status/errors overview area.

**Healthy condition:**
The RMS AGV status/errors overview area is populated and ready for inspection (not blank/unreachable).

**Expected result:**
You are viewing the RMS AGV status/errors overview area where AGV waiting conditions and system fault/alert visibility can be checked.

---

###### Step 2 — Check for AGVs waiting to do an exchange during shutdown

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, look for AGVs showing a waiting condition consistent with “waiting to do an exchange” during shutdown.

**Healthy condition:**
No widespread exchange-waiting indications are present when shutdown is expected to complete normally.

**Expected result:**
At least one AGV is indicated in RMS as waiting to do an exchange during shutdown (or you determine none are indicated).

---

###### Step 3 — Check for startup delay waiting for an AGV on the charger

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, look for startup delay evidence consistent with “waiting … for an AGV on the charger.”

**Healthy condition:**
No charger-waiting startup delay indications are present when startup proceeds normally.

**Expected result:**
At least one AGV is indicated in RMS as contributing to startup delay by waiting for an AGV on the charger (or you determine none are indicated).

---

###### Step 4 — Confirm system faults/alerts align with the waiting conditions

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, confirm whether system faults/alerts are visible and align with the exchange-waiting and/or charger-waiting conditions you observed.

**Healthy condition:**
Fault/alert visibility is consistent with normal operation (no fault entries that match the described waiting patterns).

**Expected result:**
RMS shows visible system fault/alert entries that align with the waiting conditions (or you determine there are no aligning fault/alert entries).

---

###### Step 5 — Stop and escalate on repeated or widespread waiting/fault indications

**Responsible role:** L1_support

**Instruction:**
If you see repeated or widespread waiting/fault indications that prevent lifecycle progression (e.g., multiple AGVs stuck in exchange-waiting or charger-waiting states), stop and escalate for deeper investigation.

**Healthy condition:**
No repeated/widespread waiting/fault indications are present; lifecycle progression is not blocked by the described patterns.

**Expected result:**
Escalation is initiated when the RMS evidence shows repeated/widespread waiting/fault indications consistent with the described patterns.

---

**Success Criteria:**

- RMS / fleet status UI shows either (a) AGVs indicated as waiting to do an exchange during shutdown and/or (b) startup delay evidence consistent with waiting for an AGV on the charger.
- RMS also shows visible system faults/alerts that align with the observed waiting conditions (when present).

**Failure Conditions:**

- RMS shows repeated/widespread AGVs waiting to do an exchange during shutdown.
- RMS shows repeated/widespread startup delay evidence consistent with waiting for an AGV on the charger.
- RMS shows system faults/alerts that align with the above waiting conditions.


</details>

</details>

---

### 3 — Validate bag-out progression and that AGV/robot abnormal state is cleared (`validation_gate`)

**Intent:** Confirm that the system is no longer stuck at bag-out and that the abnormal AGV/robot state (active errors/inactivity) is resolved or no longer blocking.

**Expects capability:** agv_active_errors
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L2_support, operator

**Runbook Links:**

- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (medium, support, score=0.8324, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (high, support, score=0.8473, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (high, support, score=0.3, boosted=1.21) — Query Active AGV Errors From the WCS Database
  - gaps: Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Bag-out progresses automatically and active/inactivity abnormal state is cleared.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Bag-out stops again and active/inactivity abnormal state persists.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Validation evidence is insufficient or ambiguous.
- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): After sequence restoration, bag-out still stops and evidence persists; handoff/escalate required.

**Branches:**

- `escalate` → `` when Validation fails: bag-out stops again and abnormal state persists

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

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | RMS and/or WCS evidence shows active errors and/or prolonged inactivity | `node_2` |
| `node_1` | `inconclusive` | No relevant active errors/inactivity found | `` |
| `node_3` | `escalate` | Validation fails: bag-out stops again and abnormal state persists | `` |
