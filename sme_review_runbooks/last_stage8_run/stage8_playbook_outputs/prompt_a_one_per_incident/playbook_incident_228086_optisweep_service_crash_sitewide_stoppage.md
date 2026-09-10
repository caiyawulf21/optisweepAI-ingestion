# Site-wide motion stoppage with abnormal RMS/HMI state; verify OptiSweep/WCS application health and resynchronize AGVs

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228086_optisweep_service_crash_sitewide_stoppage` |
| Case ID | `228086` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Nothing is moving at the site
- Robotic system is reported as not responding
- Small sort is not running
- AGVs are reported out of sync
- RMS/HMI shows a mostly blank screen or abnormal message (e.g., “.NET Control not created.”)
- WCS web application/application errors appear around the same time as the stoppage

## Affected Systems

- OptiSweep service
- AGVs / robotic system
- RMS / HMI (ACB System 1 - RMS / map monitor)
- Ignition gateway (status page / gateway restart activity)
- WCSWebApplication
- Windows Event Viewer / Service Control Manager
- OptiSweep API (GetAgvStatuses / Get Statuses pattern)

## Nodes

### 1 — Confirm the observable site-wide stoppage pattern and capture which control surfaces are abnormal (`diagnostic_decision`)

**Intent:** Determine whether the reported “nothing is moving” aligns with an abnormal control-plane presentation (RMS/HMI blank/abnormal message) and whether backend error evidence is likely present to justify service/app health checks.

**Expects capability:** agv_active_errors
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (medium, support, score=0.8421, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_ui_confirm_rms_up_v1` (low, support, score=0.3957, boosted=0.5299) — Check RMS fleet status UI to confirm RMS is up and running
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.
- `proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1` (high, support, score=0.8114, boosted=1.41) — Corroborate AGV Active Errors Using AGV Active Error Database Model + Error Code Dictionary + Sort GUID
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Site-wide stoppage confirmed and RMS/HMI abnormal presentation is observed (blank/abnormal/NET-control-like state) with correlated control-plane error evidence; enough pattern match to justify backend/service/app health checks.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Pattern indicates control-plane unhealthiness is likely, but evidence is incomplete or contradictory; still sufficient to proceed to service/app health checks.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Either RMS/HMI appears normal or the abnormal/NET-control-like presentation is not observed; WCS correlation is absent.
- `escalate` (observer=site; tool=RMS / AGV status UI): Unable to verify stoppage scope or control-plane surface state remotely; low evidence quality after attempts.

**Branches:**

- `healthy` → `node_2` when Pattern matched: site-wide stoppage + abnormal RMS/HMI + (reported/visible) WCS errors near same time
- `inconclusive` → `` when Pattern not matched / localized issue / RMS normal

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

<details><summary>Check RMS fleet status UI to confirm RMS is up and running (`proc_check_rms_fleet_status_ui_confirm_rms_up_v1`)</summary>

##### Runbook: Check RMS fleet status UI to confirm RMS is up and running

- **Procedure ID:** `proc_check_rms_fleet_status_ui_confirm_rms_up_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI as a quick health check to confirm RMS is reachable and displaying current fleet/status information so the OptiSweep system can be considered up and running.

**When To Use:**
Use after system events or when you need a fast confirmation that RMS is reachable and presenting fleet/status content.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open the RMS / fleet status UI

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui).

**Healthy condition:**
The RMS page loads and shows fleet/status content (not blank/unreachable).

**Expected result:**
The RMS / fleet status UI is reachable and begins loading (i.e., you can view the page rather than seeing a blank/unreachable state).

---

###### Step 2 — Confirm RMS page loads and shows current fleet/status content

**Responsible role:** L1_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), confirm the page loads successfully and shows current fleet/status content (i.e., not blank/unreachable).

**Healthy condition:**
You can see fleet/status content on the RMS page.

**Expected result:**
RMS / fleet status UI displays current fleet/status information.

---

###### Step 3 — Interpret RMS health/error indicator (if present)

**Responsible role:** L1_support

**Instruction:**
If the RMS / fleet status UI shows an errors/health indicator, note whether it indicates normal operation versus an outage/unreachable condition.

**Healthy condition:**
RMS health/error indicator (if shown) aligns with normal operation (not outage/unhealthy/unreachable).

**Expected result:**
You can classify the RMS health/error indicator as normal operation or outage/unhealthy/unreachable.

---

**Success Criteria:**

- RMS / fleet status UI is reachable and displays current fleet/status information (not blank/unreachable).

**Failure Conditions:**

- RMS / fleet status UI is blank/unreachable.
- RMS / fleet status UI health/error indicator (if present) indicates outage/unhealthy/unreachable.


</details>

<details><summary>Corroborate AGV Active Errors Using AGV Active Error Database Model + Error Code Dictionary + Sort GUID (`proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1`)</summary>

##### Runbook: Corroborate AGV Active Errors Using AGV Active Error Database Model + Error Code Dictionary + Sort GUID

- **Procedure ID:** `proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use WCS / Helix DB (SSMS) to corroborate which AGVs currently have active errors by cross-checking the active-error model (robot code/name, error code, description, SortGuid) against the AGV error dictionary model (error code → description and critical vs non-critical classification). Use SortGuid to identify which sort occurrence the active error is associated with.

**When To Use:**
When you need to confirm which AGVs currently have active errors and map each active error code to its description/classification, including which sort occurrence (SortGuid) the error is tied to.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open WCS / Helix DB (SSMS) and connect to the OptiSweep database containing the Robotics / AGV error models

**Responsible role:** L2_support

**Instruction:**
Using WCS / Helix DB (SSMS), connect to the OptiSweep database that contains the Robotics / AGV error models.

**Healthy condition:**
You can browse/select the Robotics/AGV model tables needed for the active-error model and the error-code dictionary model.

**Expected result:**
SSMS is connected to the OptiSweep database that contains the Robotics/AGV error model tables.

---

###### Step 2 — Open the AGV Active Error Database model table (AgvActiveErrorDatabaseModel)

**Responsible role:** L2_support

**Instruction:**
In SSMS, open the “AGV Active Error Database model table” (AgvActiveErrorDatabaseModel).

**Healthy condition:**
Active error rows are visible and include: Name (robot code), Error code, Description, and SortGuid.

**Expected result:**
The AgvActiveErrorDatabaseModel table view/query results show active error rows with fields including robot code (Name), error code, description, and SortGuid.

---

###### Step 3 — Verify active error rows include Name, Error code, Description, and SortGuid; record error code and SortGuid for one or more rows

**Responsible role:** L2_support

**Instruction:**
Verify the table shows active error rows that include robot code (Name), error code (Error code), description (Description), and SortGuid (Sort id). For one or more active error rows, note the error code and SortGuid values.

**Healthy condition:**
For each recorded row, the Error code and SortGuid values are populated and the row also shows the Description and robot code (Name).

**Expected result:**
You have at least one active error instance recorded with its Error code and SortGuid (and can see the corresponding Description and robot Name in the same row).

---

###### Step 4 — Open the AGV error model table (error code dictionary) and locate matching error code

**Responsible role:** L2_support

**Instruction:**
Open the “AGV error model table” (AgvErrorModel / error dictionary) and locate the matching error code to confirm the error description and critical vs non-critical classification.

**Healthy condition:**
The dictionary entry for the active error’s Error code shows a description consistent with the active-error row’s Description, and includes critical vs non-critical classification.

**Expected result:**
The matching error code is found in the AgvErrorModel dictionary and provides the description and critical vs non-critical classification for that error code.

---

###### Step 5 — Use SortGuid to identify which sort the error occurred during

**Responsible role:** L2_support

**Instruction:**
Use the SortGuid value from the active-error row to identify which sort the error occurred during (SortGuid is the identifier for the sort occurrence).

**Healthy condition:**
SortGuid values are present in the active-error rows and are used as the sort-occurrence identifier for those errors.

**Expected result:**
For each recorded active error row, you can associate the error instance with the corresponding sort occurrence using its SortGuid value.

---

**Success Criteria:**

- AgvActiveErrorDatabaseModel shows active error rows with Name (robot code), Error code, Description, and SortGuid.
- For each sampled active error row, the Error code exists in AgvErrorModel and provides a description and critical vs non-critical classification.
- Each active error instance can be associated to a sort occurrence using SortGuid.

**Failure Conditions:**

- AgvActiveErrorDatabaseModel returns no active error rows.
- An active-error row contains an Error code that cannot be found in AgvErrorModel.
- SortGuid is missing/blank for an active-error row.


</details>

</details>

---

### 2 — Check OptiSweep service termination and related WCS web application errors (`diagnostic_decision`)

**Intent:** Determine whether the control-plane is unhealthy by checking Windows Event Viewer for OptiSweep termination events and checking WCSWebApplication/application error evidence.

**Expects capability:** fleet_system_status
**Expects surface:** event_viewer
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_check_overall_system_state_on_aveva_api_page_v1` (medium, support, score=0.7003, boosted=1.0) — Check Overall System state on the AVEVA API page (System State / System Startup / Bag Out / Shutdown / Purge)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_verify_optsweep_wcs_windows_service_health_v1` (low, support, score=0.46, boosted=0.401) — Verify OptiSweep/WCS Windows service health when RMS/logs appear silent
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1` (high, operator, score=0.7643, boosted=1.0) — Start OptiSweep AGV System From Shut-down Mode (Reset Metrics → Start → Close out/Bag Out → Running)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Event Viewer / Service Control Manager (desired)): OptiSweep termination and clustered WCSWebApplication/app errors are confirmed around the incident window; proceed to approved recovery.
- `unhealthy` (observer=remote; tool=OptiSweep/WCS Windows service health (desired) + RMS fault/screen as corroboration): Partial evidence suggests the control-plane is unhealthy but Event Viewer evidence is incomplete; proceed to recovery if safety/authorization allows.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI and (later) API validation): No supporting Event Viewer evidence found for OptiSweep termination/WCS web errors (or evidence unclear). Pivot to validation gate using API/RMS synchronization checks.
- `escalate` (observer=remote; tool=Event Viewer (desired) / RMS): Service/app health cannot be assessed and validation gate is unlikely to succeed due to access limitations.

**Branches:**

- `healthy` → `node_3` when Event Viewer supports OptiSweep termination + WCS app errors
- `inconclusive` → `node_4` when No supporting Event Viewer evidence found / inconclusive

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

<details><summary><strong>Support runbooks</strong> (2)</summary>

<details><summary>Check Overall System state on the AVEVA API page (System State / System Startup / Bag Out / Shutdown / Purge) (`proc_check_overall_system_state_on_aveva_api_page_v1`)</summary>

##### Runbook: Check Overall System state on the AVEVA API page (System State / System Startup / Bag Out / Shutdown / Purge)

- **Procedure ID:** `proc_check_overall_system_state_on_aveva_api_page_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the AVEVA HMI “Overall System” / “API page” to verify the current OptiSweep system lifecycle state shown in the “System State” field, and confirm the presence/meaning of the system-level lifecycle actions: System Startup, System Bag Out, System Shutdown, and System Purge.

**When To Use:**
When you need to confirm the current OptiSweep system lifecycle phase and verify that the AVEVA “API page” is showing the expected system-level lifecycle controls (System Startup / Bag Out / Shutdown / Purge) and the “System State” value.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the AVEVA HMI Overall System / API page view

**Responsible role:** L1_support

**Instruction:**
Open the AVEVA HMI “Overall System” / “API page” view that shows the left-side items labeled: System State, System Startup, System Bag Out, System Shutdown, and System Purge.

**Healthy condition:**
All five left-side labels/sections are present on the AVEVA “API page”.

**Expected result:**
The AVEVA “API page” is visible with the left-side panel containing the labeled sections for System State, System Startup, System Bag Out, System Shutdown, and System Purge.

---

###### Step 2 — Read the System State value

**Responsible role:** L1_support

**Instruction:**
On the AVEVA “API page”, locate the “System State” field and read the value shown there.

**Healthy condition:**
A “System State” value is displayed (i.e., the field is present and populated).

**Expected result:**
The “System State” field shows the current system lifecycle state.

---

###### Step 3 — Confirm lifecycle action sections are present (Startup / Bag Out / Shutdown / Purge)

**Responsible role:** L1_support

**Instruction:**
Confirm the AVEVA “API page” left-side panel displays the labeled sections for: System Startup, System Bag Out, System Shutdown, and System Purge.

**Healthy condition:**
All four lifecycle action labels/sections are visible on the left side.

**Expected result:**
The left-side panel contains the labeled sections for System Startup, System Bag Out, System Shutdown, and System Purge.

---

###### Step 4 — Sanity-check lifecycle context using the displayed lifecycle meanings

**Responsible role:** L1_support

**Instruction:**
Using the lifecycle meanings shown for each section on the AVEVA “API page”, sanity-check the lifecycle context implied by the current “System State” value:

**Healthy condition:**
The “System State” value aligns with the lifecycle context implied by the meanings (e.g., Startup relates to staging AGVs for exchanges; Shutdown relates to putting AGVs into a shutdown state for charger rotation; Purge exchanges all totes and does not print a label at the tipper; Bag Out/close-out closes chutes and exchanges totes with items at end of sort).

**Expected result:**
You can map the current “System State” to the lifecycle context described for System Startup / Bag Out / Shutdown / Purge.

---

###### Step 5 — Stop and escalate on missing fields/labels or unexpected lifecycle state

**Responsible role:** L1_support

**Instruction:**
If any of the following conditions occur, stop the check and escalate.

**Healthy condition:**
No escalation triggers are met.

**Expected result:**
Escalation is triggered when the AVEVA “API page” is missing expected UI elements or when “System State” appears inconsistent with the operational lifecycle phase.

---

**Success Criteria:**

- On the AVEVA “API page”, the “System State” field is present and shows a current system lifecycle state value.
- The left-side panel contains the labeled sections for System Startup, System Bag Out, System Shutdown, and System Purge.
- The current “System State” value can be sanity-checked against the lifecycle meanings without indicating an unexpected lifecycle phase for the operational moment.

**Failure Conditions:**

- AVEVA “API page” missing the “System State” field.
- AVEVA “API page” missing one or more left-side lifecycle labels/sections (System Startup / Bag Out / Shutdown / Purge).
- System State value appears inconsistent with the expected lifecycle phase for the current operational moment.


</details>

<details><summary>Verify OptiSweep/WCS Windows service health when RMS/logs appear silent (`proc_verify_optsweep_wcs_windows_service_health_v1`)</summary>

##### Runbook: Verify OptiSweep/WCS Windows service health when RMS/logs appear silent

- **Procedure ID:** `proc_verify_optsweep_wcs_windows_service_health_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
When the system appears to have a crash/restart period and logs may be silent, verify whether the relevant OptiSweep/WCS Windows service(s) are actually Running vs Stopped in the Windows Services MMC. Use the service state as the primary observable when log activity is missing.

**When To Use:**
Use when RMS and/or other log-based signals appear silent during a suspected OptiSweep/WCS crash/restart window, and you need host-level evidence that the service is Running vs Stopped.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open Windows Services MMC on the OptiSweep/WCS host

**Responsible role:** L2_support

**Instruction:**
On the OptiSweep/WCS host, open the Windows Services MMC / Windows Services view (the Services list).

**Healthy condition:**
You can clearly see the Services list and the Status values (Running/Stopped) for services.

**Expected result:**
The Services list is visible with a Status column that can show Running vs Stopped for services.

---

###### Step 2 — Locate OptiSweep/WCS-related service(s) and check Running vs Stopped

**Responsible role:** L2_support

**Instruction:**
In the Services list, locate the OptiSweep/WCS-related service(s) (the segment notes there are about 10 services) and check the Status column for Running vs Stopped.

**Healthy condition:**
The OptiSweep/WCS-related service(s) show Status = Running during normal operation.

**Expected result:**
You identify the relevant OptiSweep/WCS-related service(s) and observe their Status as Running or Stopped.

---

###### Step 3 — Interpret Stopped/restarting service state as evidence consistent with the silent crash window

**Responsible role:** L2_support

**Instruction:**
If the relevant OptiSweep/WCS service(s) are Stopped (or show restart behavior), treat that as evidence consistent with the segment’s “service must stop” / “service was just like … gone” period during the suspected crash window.

**Healthy condition:**
During normal operation, the OptiSweep/WCS-related service(s) are Running.

**Expected result:**
Your conclusion matches the observed Status: Stopped/restarting supports the suspected crash/restart period; Running supports normal operation.

---

###### Step 4 — Stop and escalate when service identification/status is unclear

**Responsible role:** L2_support

**Instruction:**
If you cannot identify the relevant OptiSweep/WCS service(s) in the Services list, or if the Services view does not show clear Running/Stopped status, stop and escalate.

**Healthy condition:**
The relevant service(s) are identifiable and show clear Running/Stopped status.

**Expected result:**
Escalation is initiated with the evidence that the relevant service(s) could not be identified or status was unclear.

---

**Success Criteria:**

- You can identify the relevant OptiSweep/WCS-related service(s) in the Windows Services MMC and observe clear Status values (Running vs Stopped).
- During the suspected crash window, the observed service state (Stopped/restarting) aligns with the segment’s described “service must stop” / “logs may be silent” behavior.

**Failure Conditions:**

- OptiSweep/WCS-related service(s) show Status = Stopped during the suspected crash window.
- OptiSweep/WCS-related service(s) show restart behavior consistent with an unplanned crash/restart period.
- Relevant service(s) cannot be identified among the ~10 services, or Running/Stopped status is unclear.


</details>

</details>

---

### 3 — Perform approved recovery for OptiSweep control-plane health (service/app/gateway) if unhealthy (`procedure_reference`)

**Intent:** If OptiSweep termination and/or WCS web application errors are confirmed, follow approved recovery procedures to restore service responsiveness (without embedding exact restart commands here).

**Expects capability:** fleet_system_status
**Expects surface:** event_viewer, rms_ui
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_check_rms_fleet_status_ui_confirm_rms_up_v1` (medium, support, score=0.7019, boosted=1.0) — Check RMS fleet status UI to confirm RMS is up and running
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=OptiSweep/WCS API (GetAgvStatuses) + RMS / AGV status UI): OptiSweep control-plane recovered: services responsive; RMS/HMI is no longer blank/abnormal; API endpoints respond.
- `unhealthy` (observer=remote; tool=OptiSweep/WCS API (GetAgvStatuses) + RMS / AGV status UI): Recovery did not restore responsiveness; control-plane remains unhealthy.
- `inconclusive` (observer=remote; tool=OptiSweep/WCS API (GetAgvStatuses) + RMS / AGV status UI): Recovery partially restored some surfaces but not enough to confirm full responsiveness/sync.
- `escalate` (observer=remote; tool=Control-plane access): Cannot perform approved recovery due to role restrictions or safety preconditions; must escalate.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Check RMS fleet status UI to confirm RMS is up and running (`proc_check_rms_fleet_status_ui_confirm_rms_up_v1`)</summary>

##### Runbook: Check RMS fleet status UI to confirm RMS is up and running

- **Procedure ID:** `proc_check_rms_fleet_status_ui_confirm_rms_up_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI as a quick health check to confirm RMS is reachable and displaying current fleet/status information so the OptiSweep system can be considered up and running.

**When To Use:**
Use after system events or when you need a fast confirmation that RMS is reachable and presenting fleet/status content.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open the RMS / fleet status UI

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui).

**Healthy condition:**
The RMS page loads and shows fleet/status content (not blank/unreachable).

**Expected result:**
The RMS / fleet status UI is reachable and begins loading (i.e., you can view the page rather than seeing a blank/unreachable state).

---

###### Step 2 — Confirm RMS page loads and shows current fleet/status content

**Responsible role:** L1_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), confirm the page loads successfully and shows current fleet/status content (i.e., not blank/unreachable).

**Healthy condition:**
You can see fleet/status content on the RMS page.

**Expected result:**
RMS / fleet status UI displays current fleet/status information.

---

###### Step 3 — Interpret RMS health/error indicator (if present)

**Responsible role:** L1_support

**Instruction:**
If the RMS / fleet status UI shows an errors/health indicator, note whether it indicates normal operation versus an outage/unreachable condition.

**Healthy condition:**
RMS health/error indicator (if shown) aligns with normal operation (not outage/unhealthy/unreachable).

**Expected result:**
You can classify the RMS health/error indicator as normal operation or outage/unhealthy/unreachable.

---

**Success Criteria:**

- RMS / fleet status UI is reachable and displays current fleet/status information (not blank/unreachable).

**Failure Conditions:**

- RMS / fleet status UI is blank/unreachable.
- RMS / fleet status UI health/error indicator (if present) indicates outage/unhealthy/unreachable.


</details>

</details>

---

### 4 — Validate OptiSweep responsiveness and correct out-of-sync AGVs in RMS (`validation_gate`)

**Intent:** Confirm that the control-plane is responsive (API and/or RMS) and that AGVs are no longer out of sync; then validate that motion can resume.

**Expects capability:** agv_active_errors, device_roster_state
**Expects surface:** rms_ui, wcs_sql, wcs_api
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.575, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.7467, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (low, support, score=0.7513, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=WCS/OptiSweep API + RMS / AGV status UI): Control-plane responsive and fleet synchronization corrected; motion/workflow can resume.
- `unhealthy` (observer=remote; tool=WCS/OptiSweep API + RMS / AGV status UI): Validation fails: API doesn’t respond and/or RMS remains abnormal; AGVs cannot be corrected to synchronized state.
- `inconclusive` (observer=site_or_remote; tool=WCS/OptiSweep API + RMS / AGV status UI): Some indicators improve but not enough to declare stable motion resume.
- `escalate` (observer=remote; tool=WCS/OptiSweep API + RMS / AGV status UI): Stop orchestration due to validation failure per escalation gate.

**Branches:**

- `healthy` → `` when Recovery validation criteria are met

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

</details>

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `healthy` | Pattern matched: site-wide stoppage + abnormal RMS/HMI + (reported/visible) WCS errors near same time | `node_2` |
| `node_1` | `inconclusive` | Pattern not matched / localized issue / RMS normal | `` |
| `node_2` | `healthy` | Event Viewer supports OptiSweep termination + WCS app errors | `node_3` |
| `node_2` | `inconclusive` | No supporting Event Viewer evidence found / inconclusive | `node_4` |
| `node_4` | `healthy` | Recovery validation criteria are met | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_check_rms_fleet_status_ui_confirm_rms_up_v1 (low)
- node_2: proc_verify_optsweep_wcs_windows_service_health_v1 (low)
- node_4: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_4: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_4: proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1 (low)
