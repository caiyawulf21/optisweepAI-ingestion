# Site-wide robotic stoppage with AGVs out of sync after control-service disruption

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228086_site_stoppage_optisweep_recovery` |
| Case ID | `228086` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `high` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Nothing is moving at the site
- Robotic system is not responding
- Small sort is not running
- AGVs are reported out of sync
- Totes cannot be removed from hospital
- RMS/HMI shows a mostly blank page or abnormal message such as '.NET Control not created.'
- Question marks or abnormal HMI behavior are reported while the site is stopped

## Affected Systems

- OptiSweep service
- AGVs / robotic system
- RMS / HMI
- Ignition gateway
- Windows Event Viewer / Service Control Manager
- Windows Services
- OptiSweep / WCS API

## Nodes

### 1 — Confirm site-wide robotic stoppage pattern (`diagnostic_decision`)

**Intent:** Determine whether the reported issue matches a broad robotic stoppage pattern rather than a single-asset fault.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, hospital_hmi, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6605, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_review_visu_io_diag_screen_readings_for_operator_station_troubleshooting_v1` (high, support, score=0.5114, boosted=0.7614) — Review VISU_IO_DIAG Screen Readings For Operator Station Troubleshooting
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7609, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Evidence indicates movement is limited to a narrow area/asset rather than a site-wide stoppage.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Evidence supports a broad site-wide stoppage pattern.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Insufficient evidence to confirm site-wide stoppage vs localized faults.
- `escalate` (observer=remote; tool=RMS / AGV status UI): RMS/HMI access is unavailable or validation cannot be performed safely within role limits.

**Branches:**

- `healthy` → `node_9` when Diagnostic check does not indicate the fault condition
- `unhealthy` → `node_2` when Diagnostic check indicates the fault condition

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

<details><summary>Review VISU_IO_DIAG Screen Readings For Operator Station Troubleshooting (`proc_review_visu_io_diag_screen_readings_for_operator_station_troubleshooting_v1`)</summary>

##### Runbook: Review VISU_IO_DIAG Screen Readings For Operator Station Troubleshooting

- **Procedure ID:** `proc_review_visu_io_diag_screen_readings_for_operator_station_troubleshooting_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the read-only VISU_IO_DIAG screen on the Operator Station HMI to inspect alarms or informational messages, HMI temperatures, voltage levels, and displayed input states during troubleshooting.

**When To Use:**
Use this procedure when troubleshooting at the Operator Station and read-only diagnostic information is needed from the VISU_IO_DIAG screen, including banner messages, control temperatures, voltage levels, and station input states.

**Safety Notes:**

- The VISU_IO_DIAG screen is read-only and can be used for troubleshooting.
- Do not attempt control changes from this screen.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the VISU_IO_DIAG screen

**Responsible role:** L1_support

**Instruction:**
Open or navigate to the VISU_IO_DIAG screen using the HMI screen selection drop-down menu.

**Healthy condition:**
The VISU_IO_DIAG screen opens and its diagnostic sections are visible.

**Expected result:**
The VISU_IO_DIAG screen is displayed on the Operator Station HMI.

**Step Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/8a742ad9d3321d15.jpeg)

*VISU_IO_DIAG layout and the screen selection drop-down.*

![artifact_fig_4_18_operator_station_display_controls](assets/616114f839022c8e.png)

*Operator station display controls and navigation reference for accessing Visu_IO_Diag.*

---

###### Step 2 — Check the informational banner

**Responsible role:** L1_support

**Instruction:**
Check the informational banner for any displayed alarms or informational messages.

**Healthy condition:**
The banner is visible and messages can be read.

**Expected result:**
Any current banner message is visible for review.

**Step Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/8a742ad9d3321d15.jpeg)

*Informational banner area on the VISU_IO_DIAG screen.*

---

###### Step 3 — Navigate through banner messages

**Responsible role:** L1_support

**Instruction:**
Use the arrows on the right side of the banner to navigate through available banner messages and note the displayed messages.

**Healthy condition:**
The arrows allow message navigation and the displayed messages can be observed.

**Expected result:**
Available banner messages are reviewed and noted.

**Step Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/8a742ad9d3321d15.jpeg)

*Banner area and the message navigation arrows on the right side.*

---

###### Step 4 — Review control temperatures

**Responsible role:** L1_support

**Instruction:**
Review the "Control Temps" section and observe the CPU and motherboard (MB) temperature readings.

**Healthy condition:**
The Control Temps section is visible and both CPU and MB readings are displayed.

**Expected result:**
CPU and motherboard temperature readings are visible and noted.

**Step Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/8a742ad9d3321d15.jpeg)

*"Control Temps" section showing CPU and MB temperature readings.*

---

###### Step 5 — Verify voltage levels

**Responsible role:** L1_support

**Instruction:**
Review the "Voltage Levels" section and verify the internal controller voltage reading is 24 V.

**Healthy condition:**
The Voltage Levels section shows the internal controller voltage at 24 V.

**Expected result:**
The internal controller voltage reading is visible and compared to the expected 24 V value.

**Step Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/8a742ad9d3321d15.jpeg)

*"Voltage Levels" section showing the internal controller voltage reading.*

---

###### Step 6 — Inspect station switch input states

**Responsible role:** L1_support

**Instruction:**
Inspect the section corresponding to the switch mounted on the station and observe which inputs are shown as on and off.

**Healthy condition:**
The station switch section is visible and input states are clearly shown as on or off.

**Expected result:**
The displayed on/off states for the station switch inputs are visible and noted.

**Step Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/8a742ad9d3321d15.jpeg)

*Section corresponding to the switch mounted on the station and its displayed on/off input states.*

---

###### Step 7 — Open detailed input information

**Responsible role:** L1_support

**Instruction:**
Select one of the input sections to open the window with more information about what the inputs are.

**Healthy condition:**
Selecting an input section opens a window providing more information on what the inputs are.

**Expected result:**
A window opens with more information about the selected inputs.

**Step Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/8a742ad9d3321d15.jpeg)

*Input sections on the VISU_IO_DIAG screen and the selectable area used to open more input information.*

---

###### Step 8 — Record observed diagnostic information

**Responsible role:** L1_support

**Instruction:**
Record the observed messages, temperatures, voltage reading, and input states for troubleshooting.

**Healthy condition:**
Messages, temperatures, voltage reading, and input states have been captured.

**Expected result:**
Observed VISU_IO_DIAG information is documented for use in troubleshooting.

---

**Success Criteria:**

- The VISU_IO_DIAG screen is accessed successfully.
- Banner messages, CPU temperature, motherboard temperature, internal controller voltage, and displayed input states are reviewed.
- Any additional input detail window needed for troubleshooting is opened successfully.
- Observed diagnostic information is recorded for troubleshooting.

**Failure Conditions:**

- The VISU_IO_DIAG screen cannot be accessed.
- Expected diagnostic sections are not available.
- The internal controller voltage is not 24 V.
- Banner messages or input detail windows cannot be reviewed as described.


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

### 2 — Check for OptiSweep service failure evidence (`diagnostic_decision`)

**Intent:** Determine whether the robotic control path shows evidence of OptiSweep service termination or abnormal service state.

**Expects capability:** windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_verify_optsweep_wcs_windows_service_health_v1` (low, support, score=0.8377, boosted=1.0) — Verify OptiSweep/WCS Windows service health when RMS/logs appear silent
  - gaps: Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Windows Services / Event Viewer): No OptiSweep service failure evidence is found; service state appears stable.
- `unhealthy` (observer=remote; tool=Windows Services / Event Viewer): OptiSweep termination/unsteady state evidence is present.
- `inconclusive` (observer=remote; tool=Windows Services / Event Viewer): Service evidence is unclear; proceed to gateway decision rubric or additional checks.
- `escalate` (observer=remote; tool=Windows Services / Event Viewer): Cannot safely inspect service health or proceed within authorized role limits.

**Branches:**

- `inconclusive` → `node_4` when OptiSweep termination evidence or unstable service state is found
- `healthy` → `node_9` when Diagnostic check does not indicate the fault condition
- `unhealthy` → `node_4` when Diagnostic check indicates the fault condition

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

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

### 3 — Decide whether gateway recovery is also needed (`branching_condition`)

**Intent:** Choose whether to continue with gateway-health recovery checks when site symptoms or prior checks suggest Ignition may also be part of the stoppage path.

**Expects capability:** gateway_health
**Expects surface:** ignition_gateway
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Ignition Gateway UI): Gateway appears responsive/healthy; continue with control-service recovery first.
- `unhealthy` (observer=remote; tool=Ignition Gateway UI): Gateway health concerns exist; enter gateway recovery flow.
- `inconclusive` (observer=remote; tool=Ignition Gateway UI): Gateway status cannot be conclusively determined.
- `escalate` (observer=remote; tool=Ignition Gateway UI): Gateway recovery cannot be authorized/performed safely.

**Branches:**

- `unhealthy` → `node_4` when Ignition crash suspicion or gateway unresponsiveness present
- `healthy` → `node_4` when Gateway health appears normal

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 4 — Perform approved service or gateway recovery (`procedure_reference`)

**Intent:** Carry out the supported recovery action for the affected control service or gateway if the prior checks indicate it is needed and the role is authorized.

**Runbook Links:**

- `proc_recover_an_agv_from_a_bump_fault_code_v1` (medium, support, score=0.5765, boosted=0.7465) — Recover An AGV From A BUMP Fault Code
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Windows Services / Ignition Gateway UI / WCS API): Recovery completes and downstream control path becomes operational for validation.
- `unhealthy` (observer=remote; tool=Windows Services / Ignition Gateway UI): Recovery fails or completes incompletely; cannot validate responsiveness.
- `inconclusive` (observer=remote; tool=WCS API): Recovery performed but results are ambiguous; proceed to validation gate.
- `escalate` (observer=remote; tool=N/A (authorization constraint)): Responder not authorized to restart or safety preconditions are not met.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Recover An AGV From A BUMP Fault Code (`proc_recover_an_agv_from_a_bump_fault_code_v1`)</summary>

##### Runbook: Recover An AGV From A BUMP Fault Code

- **Procedure ID:** `proc_recover_an_agv_from_a_bump_fault_code_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Recover a documented AGV BUMP fault when Geek+ cannot recover the AGV by gathering required fault details, confirming the BUMP fault information on the AGV Bump Fault Screen, stopping RMS, removing the obstruction, resetting the AGV, and resuming RMS.

**When To Use:**
Use this procedure for the documented AGV BUMP fault recovery case in the OptiSweep manual when Geek+ cannot recover the AGV.

**Safety Notes:**

- The source states to gather information before going inside the grid (the Dance Floor).
- This procedure includes going inside the grid and physically removing an obstruction.
- Safety controls beyond the documented E-stop actions are not specified in the supplied source excerpt.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Gather required fault information before entering the grid

**Responsible role:** L2_support

**Instruction:**
Before going inside the grid (the Dance Floor), gather the Robot ID, the fault description from RMS, whether RMS indicates the faulted AGV is holding a bin and the tote ID if present, and if the faulted AGV is under a rack, determine whether that AGV is the empty AGV for that zone.

**Healthy condition:**
Robot ID, RMS fault description, tote/bin status, tote ID if present, and under-rack empty-AGV status are known before entering the grid.

**Expected result:**
The responder has the AGV identity and required RMS fault context needed for the recovery.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*AGV identification and fault information relevant to the faulted robot.*

---

###### Step 2 — Confirm the documented BUMP fault case

**Responsible role:** L2_support

**Instruction:**
Identify that the AGV is in the documented BUMP fault case and check the exception information shown for code 21057 or 21060 if displayed on the AGV Bump Fault Screen.

**Healthy condition:**
The AGV Bump Fault Screen shows the documented BUMP fault context, with exception information matching code 21057 or 21060 when displayed.

**Expected result:**
The responder confirms the AGV fault matches the documented BUMP fault context and reviews the displayed exception information.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*Fault or exception display area, exception code area, and AGV identification on the AGV Bump Fault Screen.*

---

###### Step 3 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Healthy condition:**
RMS is in the stopped state required for the recovery sequence.

**Expected result:**
RMS is E-stopped.

---

###### Step 4 — Remove the obstruction

**Responsible role:** L2_support

**Instruction:**
Remove the obstruction.

**Healthy condition:**
The obstruction is no longer present and the AGV is clear of the bump condition.

**Expected result:**
The obstruction is removed from the AGV path or contact point.

---

###### Step 5 — Reset the AGV to clear the fault

**Responsible role:** L2_support

**Instruction:**
Click the AGV RESET button for two seconds to clear the fault.

**Healthy condition:**
The BUMP fault clears after the AGV RESET button is held for two seconds.

**Expected result:**
The AGV fault is cleared.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*AGV RESET button location on the AGV Bump Fault Screen.*

---

###### Step 6 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
Press E-stop again.

**Healthy condition:**
The second E-stop action is completed as specified by the manual.

**Expected result:**
The documented second E-stop action is completed.

---

###### Step 7 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
Resume RMS.

**Healthy condition:**
RMS resumes and the AGV BUMP fault remains cleared.

**Expected result:**
RMS is resumed and the documented recovery sequence is complete.

---

**Success Criteria:**

- The obstruction is removed.
- The AGV fault is cleared using the AGV RESET button.
- RMS is resumed.
- The documented BUMP recovery sequence completes without the fault persisting.

**Failure Conditions:**

- Required pre-entry fault information cannot be gathered.
- The fault does not match the documented BUMP fault case.
- RMS cannot be E-stopped or resumed as documented.
- The obstruction cannot be removed.
- The AGV fault does not clear after the documented reset sequence.


</details>

</details>

---

### 5 — Validate control-path responsiveness after recovery (`validation_gate`)

**Intent:** Confirm that the service and gateway path are responsive before moving on to fleet-state correction.

**Expects capability:** gateway_health, windows_service_or_event_log, wcs_api_responsiveness
**Expects surface:** wcs_api, ignition_gateway
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_check_ignition_gateway_sys_perf_localhost_v1` (low, support, score=0.7162, boosted=1.0) — Check Ignition Gateway system performance status via localhost sys.perf page
  - gaps: Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1` (high, support, score=0.7207, boosted=1.0) — Check OPC COM tag subscription updates flowing to Sorter Sweeper (Ignition tag provider → OPC server → Sorter Sweeper processing)
  - gaps: Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (high, support, score=0.6509, boosted=1.0) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=WCS/SSMS (read-only) / WCS API / Ignition Systems Overview): Control-path responsiveness validated after recovery.
- `unhealthy` (observer=remote; tool=WCS API / Windows Services / Ignition Gateway UI): Control-path validation fails (API/service not responsive).
- `inconclusive` (observer=remote; tool=WCS API / Windows Services / Ignition Gateway UI): Validation cannot be completed (intermittent responses).
- `escalate` (observer=remote; tool=WCS API / Windows Services / Ignition Gateway UI): Cannot restore or validate control-path; stop and escalate.

**Branches:**

- `unhealthy` → `` when Service and API responsiveness are restored but AGVs remain abnormal in RMS
- `inconclusive` → `node_9` when Service, gateway, or API validation remains failed or inconclusive
- `healthy` → `` when Recovery validation criteria are met

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Check Ignition Gateway system performance status via localhost sys.perf page (`proc_check_ignition_gateway_sys_perf_localhost_v1`)</summary>

##### Runbook: Check Ignition Gateway system performance status via localhost sys.perf page

- **Procedure ID:** `proc_check_ignition_gateway_sys_perf_localhost_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Ignition Gateway web UI on the host to open the system performance status page at http://localhost:8088/web/status/sys.perf. Confirm the page loads and that system performance/health indicators are visible (not a connection/refused/unreachable error).

**When To Use:**
When Ignition Gateway reachability or performance is suspected on the Ignition Gateway host, and you need a quick local check that the /web/status/sys.perf page is reachable and shows performance/health indicators.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open the Ignition Gateway sys.perf status page on localhost

**Responsible role:** L2_support

**Instruction:**
On the Ignition Gateway host, open a web browser and navigate to http://localhost:8088/web/status/sys.perf.

**Healthy condition:**
The sys.perf page loads with visible page content rather than an unreachable/error state.

**Expected result:**
The browser successfully loads the Ignition Gateway system performance status page at /web/status/sys.perf (page content visible; not a connection/refused/unreachable error).

---

###### Step 2 — Verify sys.perf performance/health indicators are visible

**Responsible role:** L2_support

**Instruction:**
On the loaded /web/status/sys.perf page, observe the system performance status indicators/readouts shown on the page.

**Healthy condition:**
Performance/health indicators/readouts are visible on the sys.perf page.

**Expected result:**
System performance/health information is displayed on the sys.perf page (not blank and not replaced by an error/unavailable state).

---

**Success Criteria:**

- http://localhost:8088/web/status/sys.perf loads successfully in a browser
- The sys.perf page displays system performance/health indicators (no connection/refused/unreachable error)

**Failure Conditions:**

- sys.perf page does not load due to unreachable/error state (e.g., connection refused/unreachable)
- sys.perf page loads but performance indicators show degraded/unacceptable status


</details>

<details><summary>Check OPC COM tag subscription updates flowing to Sorter Sweeper (Ignition tag provider → OPC server → Sorter Sweeper processing) (`proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1`)</summary>

##### Runbook: Check OPC COM tag subscription updates flowing to Sorter Sweeper (Ignition tag provider → OPC server → Sorter Sweeper processing)

- **Procedure ID:** `proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Verify that OPC COM is actively subscribing to tags and that tag updates are being written to the OPC server and forwarded to the Sorter Sweeper module for processing by checking live WCS/Helix DB (SSMS) tables/models for OPC COM activity and correlating it to Sorter Sweeper processing records; also confirm Ignition gateway health when needed.

**When To Use:**
Use when you need to confirm the live tag flow: OPC COM subscribes to tags, tag updates are written via the OPC server/ignition tag provider, and Sorter Sweeper receives/acts on those updates.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open WCS/Helix DB (SSMS) and connect to the live OptiSweep/WCS database catalog

**Responsible role:** L2_support

**Instruction:**
Using SSMS / Helix DB (wcs_sql), connect to the live OptiSweep/WCS database catalog that includes the OPC Comms and Sorter Sweeper modules.

**Healthy condition:**
You can access the live database objects needed to query OPC Comms and Sorter Sweeper-related models/tables.

**Expected result:**
SSMS connection is established and you can browse the live database objects for the OPC Comms and Sorter Sweeper modules.

---

###### Step 2 — Locate live OPC COM communications and Sorter Sweeper processing models/tables

**Responsible role:** L2_support

**Instruction:**
In SSMS / Helix DB (wcs_sql), locate the live tables/models for OPC COM communications and for Sorter Sweeper processing.

**Healthy condition:**
The identified objects correspond to OPC Comms and Sorter Sweeper databases/models used for tag subscription/update and processing.

**Expected result:**
You have identified the live OPC COM communications objects and the live Sorter Sweeper processing objects that will be used for correlation.

---

###### Step 3 — Check for recent OPC COM tag update activity in OPC COM communications objects

**Responsible role:** L2_support

**Instruction:**
Using the OPC COM communications objects you identified in SSMS / Helix DB (wcs_sql), check for recent tag update activity (e.g., recently updated records/timestamps) for the relevant subscribed tags.

**Healthy condition:**
OPC COM shows continuous/recent tag update activity (recent rows/records with updated timestamps for relevant tags).

**Expected result:**
There are recent records showing tag update activity (updated timestamps/entries) in the OPC COM communications objects.

---

###### Step 4 — Correlate OPC COM tag updates to Sorter Sweeper processing records

**Responsible role:** L2_support

**Instruction:**
In SSMS / Helix DB (wcs_sql), correlate the timeframe of the recent OPC COM tag update activity to Sorter Sweeper processing records; if available, match tag identifiers between the two.

**Healthy condition:**
For recent OPC COM updates, Sorter Sweeper shows corresponding processing entries in the same timeframe.

**Expected result:**
Sorter Sweeper has corresponding processing entries for the same tag update timeframe (and, if available, matching tag identifiers).

---

###### Step 5 — If applicable, verify Ignition gateway health for tag provider connectivity

**Responsible role:** L2_support

**Instruction:**
Using Ignition gateway (ignition_gateway), perform a basic health check to confirm the gateway is not in a failed/unreachable state.

**Healthy condition:**
Ignition gateway is not in a failed/unreachable state; performance indicators do not show obvious crash behavior (e.g., memory spiked then dropped to 0).

**Expected result:**
Ignition gateway status indicates it is reachable/healthy enough to provide tag updates.

---

###### Step 6 — Stop and escalate based on correlation results

**Responsible role:** L2_support

**Instruction:**
Based on your findings from Steps 3–4, stop and escalate using the failure mode that matches the observed evidence.

**Healthy condition:**
OPC COM shows recent tag updates and Sorter Sweeper shows corresponding processing entries for the same timeframe.

**Expected result:**
Escalation is triggered only when the evidence indicates missing tag updates or missing Sorter Sweeper processing correlation.

---

**Success Criteria:**

- Live evidence shows recent OPC COM tag update activity (recent records with updated timestamps for relevant tags).
- Sorter Sweeper has corresponding processing entries for the same tag update timeframe (and, if available, matching tag identifiers).

**Failure Conditions:**

- No recent tag update activity in OPC COM communications objects.
- OPC COM updates exist but Sorter Sweeper processing records are missing for the same timeframe.


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

### 6 — Check for remaining out-of-sync AGVs in RMS (`diagnostic_decision`)

**Intent:** Determine whether fleet synchronization issues remain after service responsiveness is restored.

**Expects capability:** fleet_system_status, agv_physical_recovery
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6965, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (high, support, score=0.8249, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.8054, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): No remaining synchronization/blocking exceptions in RMS.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Remaining out-of-sync fleet state exists in RMS.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): RMS indicates anomalies but mapping/sync interpretation is unclear.
- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI): RMS evidence suggests deeper data/model or access issues beyond allowed correction.

**Branches:**

- `unhealthy` → `node_7` when Service/API responsiveness restored but AGVs remain abnormal in RMS
- `healthy` → `node_8` when No remaining synchronization exceptions

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

### 7 — Perform approved AGV resynchronization or correction (`procedure_reference`)

**Intent:** Apply the supported fleet-state correction for AGVs identified as out of sync or otherwise abnormal in RMS.

**Runbook Links:**

- `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (low, support, score=0.6231, boosted=0.8931) — Recover an AGV That Lost a Tote Without Faulting
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_execute_agv_command_for_system_recovery_v1` (high, support, score=0.6215, boosted=0.8915) — Use Execute AGV Command For System Recovery
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1` (high, support, score=0.6178, boosted=0.8878) — Recover an AGV That Lost a Tote Without an AGV Fault
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Fleet-state correction completes and assets return to synchronized operation in RMS.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Fleet correction cannot complete within authorized support procedures.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Correction partially applied; requires further diagnosis/correction loops.
- `escalate` (observer=remote; tool=RMS / AGV status UI): Requested correction exceeds responder authorization or requires unsupported intervention.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Recover an AGV That Lost a Tote Without Faulting (`proc_recover_an_agv_that_lost_a_tote_without_faulting_v1`)</summary>

##### Runbook: Recover an AGV That Lost a Tote Without Faulting

- **Procedure ID:** `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Restore an AGV and tote to service after an AGV loses a tote without faulting by stopping RMS, manually moving the AGV to the Hospital, removing and re-adding the AGV at the Hospital station PC, power cycling the AGV, positioning it over the QR code in front of the Inbound Hospital Station, and removing and re-adding the missing tote so the AGV can return the tote to the sorter.

**When To Use:**
Use when an AGV has lost a tote without faulting and must be restored to service through the Hospital workflow described in section 5.8.2.6.

**Safety Notes:**

- This procedure is not marked support-safe in the candidate.
- The procedure includes E-stop use, brake release use, manual AGV movement, and AGV power cycling.
- Only maintenance or a supervisor should remove an AGV from the system, per the Add/Remove AGV source reference attached to the Hospital HMI screen artifact.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS before beginning recovery of the AGV that lost a tote without faulting.

**Healthy condition:**
The system is stopped and recovery actions can proceed.

**Expected result:**
RMS is in an E-stopped or shut-down state suitable for recovery work.

**Step Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/597651fff1a13999.jpeg)

*System shut-down mode visual context for stopped system state.*

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/d87070d22301b81d.jpeg)

*Recovery-related screen context showing E-stop use in AGV/tote recovery.*

---

###### Step 2 — Release the AGV brake

**Responsible role:** L2_support

**Instruction:**
Press the brake release on the AGV that lost a tote.

**Healthy condition:**
The brake release can be used and the AGV is movable.

**Expected result:**
The AGV brake is released so the AGV can be rolled manually.

---

###### Step 3 — Move the AGV to the Hospital

**Responsible role:** L2_support

**Instruction:**
Push the AGV over to the Hospital.

**Healthy condition:**
The AGV reaches the Hospital area and is available for Hospital station PC actions.

**Expected result:**
The AGV is physically positioned at the Hospital.

**Step Images:**

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Hospital station area context for tote handling and AGV arrival.*

---

###### Step 4 — Remove and re-add the AGV at the Hospital station PC

**Responsible role:** L2_support

**Instruction:**
At the Hospital station PC, remove the AGV and then add the AGV back into the system.

**Healthy condition:**
The Hospital station PC/Hospital HMI accepts the AGV removal and add-back actions.

**Expected result:**
The AGV is removed and then reinserted into the system through the Hospital station interface.

**Step Images:**

![artifact_fig_4_37_hospital_hmi_add_remove_agv_screen](assets/2c21ae93aa1bc610.png)

*AGV ID entry and the Hospital HMI controls used to remove an AGV and INSERT INTO SYSTEM.*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*Related AGV Remove AGV and Recover AGV controls context.*

---

###### Step 5 — Power cycle the AGV

**Responsible role:** L2_support

**Instruction:**
Turn the AGV off, then turn it on again.

**Healthy condition:**
After the power cycle, the AGV lights turn green.

**Expected result:**
The AGV powers back on and proceeds toward a normal status indication.

---

###### Step 6 — Position the AGV over the Inbound Hospital Station QR code

**Responsible role:** L2_support

**Instruction:**
When the AGV lights turn green, roll it over the QR code in front of the Inbound Hospital Station.

**Healthy condition:**
AGV lights are green and the AGV is correctly positioned over the QR code.

**Expected result:**
The AGV is positioned over the QR code in front of the Inbound Hospital Station.

---

###### Step 7 — Locate the missing tote and remove it from the system

**Responsible role:** L2_support

**Instruction:**
Locate the missing tote and bring it to the Hospital to remove it from the system.

**Healthy condition:**
The tote is found, brought to the Hospital, and successfully removed from the system.

**Expected result:**
The missing tote is at the Hospital and has been removed from the system using the documented tote-removal process.

**Step Images:**

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/1612450530188bc6.png)

*Hospital HMI tote scan fields and REMOVE TOTE button.*

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Hospital station tote handling flow, including scanning tote barcode and extracting tote from the system.*

---

###### Step 8 — Add the tote back into the system

**Responsible role:** L2_support

**Instruction:**
Add the tote back into the system. The AGV should then take the tote back to the sorter.

**Healthy condition:**
The tote add-back is accepted and the AGV returns the tote to the sorter.

**Expected result:**
The tote is added back into the system and the AGV takes the tote back to the sorter.

**Step Images:**

![artifact_page_93_image_2](assets/d1045eabc9fd3587.png)

*Add Tote screen workflow: scan tote barcode, verify Tote ID, and press Confirm & Execute.*

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Hospital station tote placement context if the tote is going back into the system.*

---

**Success Criteria:**

- The AGV has been removed and added back into the system at the Hospital station PC.
- The AGV lights turn green after the power cycle.
- The AGV is rolled over the QR code in front of the Inbound Hospital Station.
- The missing tote is located, removed from the system, and added back into the system.
- The AGV takes the tote back to the sorter.

**Failure Conditions:**

- Brake release cannot be used.
- AGV cannot be moved to the Hospital.
- AGV cannot be removed and added back at the Hospital station PC.
- AGV lights do not turn green after the power cycle.
- Missing tote cannot be located.
- Missing tote cannot be removed and re-added using the documented tote procedures.
- After tote add-back, the AGV does not take the tote back to the sorter.


</details>

<details><summary>Use Execute AGV Command For System Recovery (`proc_use_execute_agv_command_for_system_recovery_v1`)</summary>

##### Runbook: Use Execute AGV Command For System Recovery

- **Procedure ID:** `proc_use_execute_agv_command_for_system_recovery_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Execute AGV Command control in the AGVs section of the System HMI API screen for system recovery when the system has gone down and messages were missed. The source documents the control and its purpose, but does not provide the command inputs, parameters, or confirmation behavior.

**When To Use:**
Use this procedure during system recovery when the system went down and messages were missed, and the recovery action involves the Execute AGV Command control in the AGVs section of the API screen.

**Safety Notes:**

- This is a recovery-related control with potential system-wide impact.
- The source does not provide command inputs, parameters, or confirmation behavior; do not improvise unsupported recovery commands.
- Escalate if approved site documentation or support personnel cannot provide the required recovery command details.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the AGVs section of the API screen

**Responsible role:** L2_support

**Instruction:**
Open the System HMI API screen and navigate to the AGVs section.

**Healthy condition:**
The AGV API Controls area is displayed and the AGV controls are available for review.

**Expected result:**
The AGVs section of the API screen is visible.

**Step Images:**

![artifact_fig_4_8_acb_api_screen](assets/b192077f772ce5cd.jpeg)

*The ACB API screen interface used to access AGV controls.*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*The AGV API Controls area within the AGVs section of the API screen.*

---

###### Step 2 — Locate the Execute AGV Command control

**Responsible role:** L2_support

**Instruction:**
In the AGVs section, locate the Execute AGV Command control.

**Healthy condition:**
The Execute AGV Command control is visible in the AGV API Controls area.

**Expected result:**
The Execute AGV Command control is identified on the AGV API Controls screen.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*The Execute AGV Command control listed among the AGV API Controls.*

---

###### Step 3 — Use Execute AGV Command for documented recovery purpose

**Responsible role:** L2_support

**Instruction:**
Use Execute AGV Command as part of system recovery when the system went down and messages were missed. If the required command details are not available from approved site documentation or support personnel, stop and escalate.

**Healthy condition:**
The control is used only in the documented recovery scenario and the operator has approved recovery command details from site documentation or support personnel.

**Expected result:**
The Execute AGV Command control is used for the documented system recovery purpose related to missed messages.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*The Execute AGV Command control used for system recovery in the AGV API Controls screen.*

---

**Success Criteria:**

- The AGVs section of the API screen is accessed.
- The Execute AGV Command control is identified.
- The control is used only for the documented recovery case where the system went down and messages were missed.

**Failure Conditions:**

- The API screen or AGVs section cannot be accessed.
- The Execute AGV Command control cannot be located.
- The source does not provide enough detail to safely determine command inputs, parameters, or confirmation behavior.


</details>

<details><summary>Recover an AGV That Lost a Tote Without an AGV Fault (`proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1`)</summary>

##### Runbook: Recover an AGV That Lost a Tote Without an AGV Fault

- **Procedure ID:** `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Restore the AGV and the missing tote to the system after an AGV loses a tote without the AGV itself faulting. The source sequence stops RMS, manually releases and moves the AGV to the Hospital, removes and re-adds the AGV at the Hospital station PC, power-cycles the AGV, repositions it at the Inbound Hospital Station QR code after its lights turn green, then removes and re-adds the missing tote.

**When To Use:**
Use when the AGV LOST TOTE NO FAULT recovery scenario applies and the AGV has lost a tote without the AGV itself faulting, using the recovery sequence documented in section 5.8.2.6.

**Safety Notes:**

- This procedure is not marked support-safe in the candidate.
- The recovery includes E-stop use, brake release, manual AGV movement, and AGV/tote removal and re-addition actions.
- Only maintenance or a supervisor should remove an AGV from the system, per the Add/Remove AGV screen reference.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Healthy condition:**
RMS is in the E-stopped state and the recovery can proceed.

**Expected result:**
RMS is E-stopped for recovery.

---

###### Step 2 — Release the AGV brake

**Responsible role:** L2_support

**Instruction:**
Press the brake release on the AGV that lost a tote.

**Healthy condition:**
The AGV can be moved after the brake release is pressed.

**Expected result:**
The AGV brake is released so the AGV can be rolled manually.

---

###### Step 3 — Move the AGV to the Hospital

**Responsible role:** L2_support

**Instruction:**
Push the AGV over to the Hospital.

**Healthy condition:**
The AGV is at the Hospital and ready for Hospital station PC actions.

**Expected result:**
The AGV is physically moved to the Hospital area.

**Step Images:**

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Hospital station area and tote handling location that may help identify the Hospital destination for the moved AGV.*

---

###### Step 4 — Remove and re-add the AGV at the Hospital station PC

**Responsible role:** L2_support

**Instruction:**
At the Hospital station PC, remove the AGV, then add the AGV back into the system. Use the documented Add/Remove AGV procedure reference on page 52.

**Healthy condition:**
The AGV has been successfully removed and re-added using the documented Add/Remove AGV procedure.

**Expected result:**
The AGV is removed and then added back into the system at the Hospital station PC.

**Step Images:**

![artifact_fig_4_37_hospital_hmi_add_remove_agv_screen](assets/2c21ae93aa1bc610.png)

*Hospital HMI Add/Remove AGV screen used to remove an AGV from the system and insert it back into the system.*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*AGV API controls reference showing Remove AGV and Recover AGV controls in the system context.*

---

###### Step 5 — Power-cycle the AGV

**Responsible role:** L2_support

**Instruction:**
Turn the AGV off, then turn it on again.

**Healthy condition:**
The AGV restarts and proceeds toward the documented green-light status.

**Expected result:**
The AGV has been power-cycled.

---

###### Step 6 — Wait for green lights and position the AGV at the Inbound Hospital Station QR code

**Responsible role:** L2_support

**Instruction:**
Wait until the AGV lights turn green, then roll the AGV over the QR code in front of the Inbound Hospital Station.

**Healthy condition:**
Green AGV lights are observed and the AGV is positioned over the referenced QR code.

**Expected result:**
The AGV lights turn green and the AGV is rolled over the QR code in front of the Inbound Hospital Station.

**Step Images:**

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Hospital station area that may help orient the Inbound Hospital Station location.*

![artifact_page_93_image_2](assets/d1045eabc9fd3587.png)

*Related hospital/add-tote context artifact that may help identify the station area used after AGV repositioning.*

---

###### Step 7 — Remove the missing tote from the system at the Hospital

**Responsible role:** L2_support

**Instruction:**
Locate the missing tote and bring it to the Hospital to remove it from the system using the documented Remove Tote procedure reference on page 47.

**Healthy condition:**
The tote has been removed from the system using the documented Remove Tote procedure.

**Expected result:**
The missing tote is located, brought to the Hospital, and removed from the system.

**Step Images:**

![artifact_fig_4_32_hospital_hmi_remove_tote_screen](assets/2ade24bb590cf243.png)

*Hospital HMI Remove Tote screen used to scan the tote barcode and confirm removal from the system.*

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Hospital station tote handling area where the tote is brought for removal.*

---

###### Step 8 — Add the tote back into the system

**Responsible role:** L2_support

**Instruction:**
Add the tote back into the system using the documented Add Tote procedure reference on page 46.

**Healthy condition:**
The tote is successfully added back into the system and the AGV should then take the tote back to the sorter.

**Expected result:**
The tote is added back into the system.

**Step Images:**

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/12f351ab67fe300a.png)

*Hospital HMI Add Tote screen used to scan the tote barcode and confirm execution.*

![artifact_page_93_image_2](assets/d1045eabc9fd3587.png)

*Add Tote flow showing tote barcode scan, tote ID verification, and Confirm & Execute.*

---

**Success Criteria:**

- The AGV is restored to the system.
- The missing tote is removed and re-added in the system.
- The AGV should then take the tote back to the sorter.

**Failure Conditions:**

- The AGV lights do not turn green after power cycling.
- The AGV cannot be moved with the brake release.
- The AGV cannot be re-added at the Hospital station PC.
- The documented Add/Remove AGV procedure cannot be completed.
- The documented Remove Tote procedure cannot be completed.
- The documented Add Tote procedure cannot be completed.


</details>

</details>

---

### 8 — Confirm site operations have resumed (`validation_gate`)

**Intent:** Verify that robotic movement and site workflow have returned sufficiently to close the troubleshooting path.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.691, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7655, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.7394, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Site operations have resumed and fleet state is normal after correction.
- `unhealthy` (observer=site; tool=RMS / AGV status UI): Operations did not resume or faults recur.
- `inconclusive` (observer=site_or_remote; tool=Site operational confirmation): RMS looks improved but site workflow confirmation is not yet obtained.
- `escalate` (observer=remote; tool=RMS / AGV status UI): Closure cannot be supported due to recurring abnormalities or inability to validate.

**Branches:**

- `unhealthy` → `node_9` when Recovery validation criteria are not met
- `healthy` → `` when Recovery validation criteria are met

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

### 9 — Escalate if supported recovery does not restore stable operation (`escalation_gate`)

**Intent:** Stop and escalate when the supported service, gateway, and fleet-correction path does not identify a safe or effective recovery.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=Windows Event Viewer / Windows Services / Ignition Systems Overview / WCS API / RMS): Supported recovery/validation did not restore stable operation; escalation required with full evidence.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `healthy` | Diagnostic check does not indicate the fault condition | `node_9` |
| `node_1` | `unhealthy` | Diagnostic check indicates the fault condition | `node_2` |
| `node_2` | `inconclusive` | OptiSweep termination evidence or unstable service state is found | `node_4` |
| `node_2` | `healthy` | Diagnostic check does not indicate the fault condition | `node_9` |
| `node_2` | `unhealthy` | Diagnostic check indicates the fault condition | `node_4` |
| `node_3` | `unhealthy` | Ignition crash suspicion or gateway unresponsiveness present | `node_4` |
| `node_3` | `healthy` | Gateway health appears normal | `node_4` |
| `node_5` | `unhealthy` | Service and API responsiveness are restored but AGVs remain abnormal in RMS | `` |
| `node_5` | `inconclusive` | Service, gateway, or API validation remains failed or inconclusive | `node_9` |
| `node_5` | `healthy` | Recovery validation criteria are met | `` |
| `node_6` | `unhealthy` | Service/API responsiveness restored but AGVs remain abnormal in RMS | `node_7` |
| `node_6` | `healthy` | No remaining synchronization exceptions | `node_8` |
| `node_8` | `unhealthy` | Recovery validation criteria are not met | `node_9` |
| `node_8` | `healthy` | Recovery validation criteria are met | `` |

## Unresolved / Low-Confidence Links

- node_2: proc_verify_optsweep_wcs_windows_service_health_v1 (low)
- node_3: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_5: proc_check_ignition_gateway_sys_perf_localhost_v1 (low)
- node_6: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_7: proc_recover_an_agv_that_lost_a_tote_without_faulting_v1 (low)
- node_9: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
