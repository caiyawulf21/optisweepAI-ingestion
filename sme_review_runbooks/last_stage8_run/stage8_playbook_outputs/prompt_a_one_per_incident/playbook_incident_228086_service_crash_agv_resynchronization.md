# Robotic system stops responding with AGV state disruption

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228086_service_crash_agv_resynchronization` |
| Case ID | `228086` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `high` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Nothing is moving or multiple robots are not moving in different areas.
- The robotic system is reported as not responding.
- The small sort or automated bag-out workflow is not running.
- AGVs are reported as out of sync or unavailable.
- RMS or HMI is blank, shows question marks, or displays an apparent control-rendering message.
- Hospital totes cannot be removed or related material-handling workflow is stopped.

## Affected Systems

- OptiSweep service
- AGVs and robotic system
- RMS / fleet status UI
- WCSWebApplication
- Ignition gateway
- Windows Event Viewer and Windows Services
- OptiSweep / WCS API
- WCS database / SSMS
- Hospital workflow and small sort

## Nodes

### 1 — Confirm broad stoppage and affected workflow (`diagnostic_decision`)

**Intent:** Determine whether the report represents a broad automated-operation stoppage rather than an isolated robot or local equipment issue.

**Expects capability:** fleet_system_status
**Expects surface:** site_interview, rms_ui
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.5274, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (high, support, score=0.6086, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.6473, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Operation is normal or limited to a local asset; the broad site-wide stoppage pattern is not confirmed.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Broad automated-operation stoppage and affected workflow(s) are confirmed by site report and/or abnormal RMS presentation.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Conflicting or insufficient evidence about scope; RMS may be temporarily unavailable or site report conflicts with what can be observed.

**Branches:**

- `unhealthy` → `node_2` when Broad stoppage confirmed
- `healthy` → `node_4` when Localized/normal operation

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

### 2 — Check named service and application failure evidence (`diagnostic_decision`)

**Intent:** Determine whether Windows logs or service state show an OptiSweep or WCSWebApplication failure correlated with the stoppage.

**Expects capability:** windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_verify_optsweep_wcs_windows_service_health_v1` (low, support, score=0.7305, boosted=1.0) — Verify OptiSweep/WCS Windows service health when RMS/logs appear silent
  - gaps: Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `unhealthy` (observer=remote; tool=Windows Event Viewer / Windows Services): Service failure evidence correlates with stoppage (OptiSweep terminated unexpectedly and/or WCSWebApplication errors clustered).
- `healthy` (observer=remote; tool=Windows Event Viewer / Windows Services): No correlated service failure; OptiSweep service is running and evidence does not support service-failure path.
- `inconclusive` (observer=remote; tool=Windows Event Viewer / Windows Services): Missing/ambiguous logs or evidence only shows a running service state without correlation to operational symptoms.

**Branches:**

- `unhealthy` → `node_4` when Correlated service/application failure indicated
- `healthy` → `node_4` when No correlated failure; OptiSweep running

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

### 3 — Perform authorized OptiSweep or gateway recovery (`procedure_reference`)

**Intent:** Use the approved recovery procedure for the affected service or gateway when the diagnostic evidence supports that path and the role is authorized.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- `proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1` (medium, support, score=0.6556, boosted=0.7456) — Restart Ignition and verify OptiSweep service response with GetAgvStatuses
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Windows Services / Ignition gateway status + API validation (GetAgvStatuses)): Authorized recovery completed with safe end state and affected service/gateway available for validation.
- `unhealthy` (observer=remote; tool=Windows Services / Ignition gateway status): Recovery incomplete/unsafe/unauthorized or no confirmed end state.
- `inconclusive` (observer=remote; tool=Windows Services / Ignition gateway status): Recovery appears to start but final validation outcome is unclear.

**Branches:**

- `healthy` → `node_5` when Recovery completed (authorized)
- `unhealthy` → `node_8` when Recovery incomplete/unsafe/no confirmed end state

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Restart Ignition and verify OptiSweep service response with GetAgvStatuses (`proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1`)</summary>

##### Runbook: Restart Ignition and verify OptiSweep service response with GetAgvStatuses

- **Procedure ID:** `proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Conditional incident-derived recovery guidance for restarting Ignition and confirming OptiSweep service responsiveness before releasing the E-stop. The source instructs the operator to first E-stop the system, restart Ignition with `gwcmd -r`, wait until the gateway is back up and login is possible, then verify OptiSweep by sending a GetAgvStatuses request. If no response is returned, restart OptiSweep, send the request again, and only then release the E-stop.

**When To Use:**
Use when the incident-specific guidance indicates Ignition may need to be restarted and you need to confirm the OptiSweep service is responding again before releasing the E-stop.

**Safety Notes:**

- First E-stop the system before attempting the restart.
- Do not release the E-stop until OptiSweep response is confirmed.
- If Ignition does not come back up to a login-capable state, stop and do not perform undocumented changes beyond the source-shared restart sequence.
- If response still cannot be confirmed after the documented restart steps, stop and escalate rather than inventing additional recovery actions.

- **Source:** `incident_case` / `source_case_228086`

**Procedure Steps:**

###### Step 1 — E-stop the system before restart

**Responsible role:** L2_support

**Instruction:**
First E-stop the system before attempting the restart.

**Healthy condition:**
The system is in E-stop and restart activity has not yet begun.

**Expected result:**
The system is placed in E-stop before any Ignition restart action is taken.

**Step Images:**

![artifact_incident_228086_page_014_embedded_image_01](assets/0d41c4115fc03143.png)

*Emergency stop control area highlighted in the RMS/system control context.*

---

###### Step 2 — Restart Ignition from the Ignition directory

**Responsible role:** L2_support

**Instruction:**
Open a Windows command prompt on the Ignition host, navigate to the Ignition installation directory, and run `gwcmd -r` from `C:\Program Files\Inductive Automation\Ignition>`. Observe the console message `Waiting for Gateway restart...`.

**Healthy condition:**
The command prompt shows `gwcmd -r` executed from the Ignition directory and displays `Waiting for Gateway restart...`.

**Expected result:**
The Ignition gateway restart command is accepted and the console shows `Waiting for Gateway restart...`.

**Step Images:**

![artifact_incident_228086_page_015_embedded_image_01](assets/30dd5b0a07803c56.png)

*Command prompt in `C:\Program Files\Inductive Automation\Ignition>` showing `gwcmd -r` and `Waiting for Gateway restart...`.*

![artifact_incident_228086_page_012_nested_image_02](assets/9326afd07f2ffe67.png)

*Restart-instruction screenshot context showing the Ignition restart command sequence.*

---

###### Step 3 — Wait for Ignition to come back up

**Responsible role:** L2_support

**Instruction:**
Wait for Ignition to come back up, meaning it lets you log in and does not show the gateway starting up. Use the Ignition status/login page to confirm the gateway is reachable.

**Healthy condition:**
The Ignition Status > Systems > Overview page is reachable, with visible system widgets and no gateway-starting-up screen.

**Expected result:**
Ignition is reachable again and presents a login-capable or status page rather than a startup screen.

**Step Images:**

![artifact_incident_228086_page_016_embedded_image_01](assets/6e057be40744620d.png)

*Ignition Status > Systems > Overview page reachable in the browser, with Current Response Time and no startup screen.*

---

###### Step 4 — Send GetAgvStatuses request after Ignition restart

**Responsible role:** L2_support

**Instruction:**
Open the API client identified in the source as api dog and send a GetAgvStatuses request to `http://10.27.80.165:5000/GetAgvStatuses`.

**Healthy condition:**
The API client shows the GetAgvStatuses request executed successfully against the documented endpoint.

**Expected result:**
The request executes against the shown endpoint and returns a response from the OptiSweep service.

**Step Images:**

![artifact_incident_228086_page_017_embedded_image_01](assets/8625154eb02b186c.png)

*API client showing GET request to `http://10.27.80.165:5000/GetAgvStatuses`.*

---

###### Step 5 — Confirm HTTP 200 and returned AGV records

**Responsible role:** L2_support

**Instruction:**
Check that the GetAgvStatuses request returns HTTP 200 and returned AGV records. Visible records in the source include status values such as `NORMAL`. Do not treat the visible schema validation warning alone as a service outage if the request still returns HTTP 200 with data.

**Healthy condition:**
The response panel shows Success (200) / Status: 200 and returned JSON records with visible AGV status values such as `NORMAL`.

**Expected result:**
The API response shows Success/Status 200 and returned AGV records, including visible status values such as `NORMAL`.

**Step Images:**

![artifact_incident_228086_page_017_embedded_image_01](assets/8625154eb02b186c.png)

*Response panel showing Success/Status 200 and returned records with visible `NORMAL` values; note the validation warning but do not treat it alone as outage proof.*

---

###### Step 6 — If no response, restart OptiSweep and retry GetAgvStatuses

**Responsible role:** L2_support

**Instruction:**
If no response is given, restart OptiSweep, then send another GetAgvStatuses request to confirm response. The source supports this at a high level only; use the Windows Services console context shown for OptiSweep and do not invent additional click-by-click steps not present in the source.

**Healthy condition:**
The follow-up request returns a confirmed response after the OptiSweep restart.

**Expected result:**
OptiSweep is restarted and a follow-up GetAgvStatuses request is sent to confirm response.

**Step Images:**

![artifact_incident_228086_page_019_embedded_image_01](assets/3832c5ce44b05a86.png)

*Windows Services console with OptiSweep selected, showing Running state and restart control visible.*

![artifact_incident_228086_page_017_embedded_image_01](assets/8625154eb02b186c.png)

*Use the same GetAgvStatuses request view to retry and confirm response.*

---

###### Step 7 — Release the E-stop after response is confirmed

**Responsible role:** L2_support

**Instruction:**
Once the response is confirmed, release the E-stop.

**Healthy condition:**
A confirmed GetAgvStatuses response exists before the E-stop is released.

**Expected result:**
The E-stop is released only after OptiSweep response has been confirmed.

**Step Images:**

![artifact_incident_228086_page_014_embedded_image_01](assets/0d41c4115fc03143.png)

*System control context with emergency stop control area relevant to release after confirmation.*

---

**Success Criteria:**

- Ignition is reachable again and allows login or status-page access rather than showing gateway startup.
- The GetAgvStatuses request to `http://10.27.80.165:5000/GetAgvStatuses` returns HTTP 200.
- Returned AGV records are visible in the response, including status values such as `NORMAL`.
- If OptiSweep had to be restarted, a follow-up GetAgvStatuses request confirms response.
- The E-stop is released only after response confirmation.

**Failure Conditions:**

- Ignition does not come back up to a login-capable state.
- The GetAgvStatuses endpoint is unreachable or returns no response.
- The request returns no data.
- Response still cannot be confirmed after the documented OptiSweep restart and retry.
- Recovery would require undocumented actions beyond the source-shared sequence.


</details>

</details>

---

### 4 — Check AGV and system error state when service failure is not indicated (`diagnostic_decision`)

**Intent:** Use fleet and backend state evidence to identify an alternate AGV, system-error, or state-distribution condition when the service-failure pattern is not confirmed.

**Expects capability:** agv_active_errors, fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.5394, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (high, support, score=0.681, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Limited domain-term overlap between placeholder and runbook.
- `proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1` (low, support, score=0.6546, boosted=1.36) — Corroborate AGV Active Errors Using AGV Active Error Database Model + Error Code Dictionary + Sort GUID
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI (and corroborate via WCS/SSMS if available)): Alternate evidence indicates active AGV/system errors or RMS/backend disagreement.
- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): No relevant active errors; overall system state appears normal and the broad stoppage pattern is not confirmed.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI (attempt corroboration)): RMS or backend evidence is blank/unavailable or operational meaning cannot be established.

**Branches:**

- `unhealthy` → `node_8` when Active errors/abnormal state or conflict indicated
- `healthy` → `` when No relevant active errors; system normal

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

### 5 — Check for residual AGV synchronization issues after recovery (`diagnostic_decision`)

**Intent:** Determine whether AGVs remain out of sync or otherwise require authorized state correction after service or gateway recovery.

**Expects capability:** agv_active_errors, device_roster_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.4483, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.6483, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.3, boosted=0.9200000000000002) — Query Active AGV Errors From the WCS Database
  - gaps: Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.; Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI (plus corroborate via WCS/SSMS if available)): Residual out-of-sync/abnormal fleet state remains; discrepancy persists.
- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Fleet state consistent and no residual AGV error indicated.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Evidence is incomplete/blank or conflicting; cannot establish whether residual sync issues remain.

**Branches:**

- `unhealthy` → `node_6` when Residual out-of-sync/abnormal state remains
- `healthy` → `node_7` when Fleet state consistent; no residual error

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

### 6 — Apply authorized AGV state correction (`procedure_reference`)

**Intent:** Use the approved RMS or fleet-state procedure to correct identified out-of-sync AGV state when the responsible role confirms that correction is safe and supported.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- `proc_recover_from_agv_fault_during_exchange_recovery_v1` (medium, support, score=0.6669, boosted=0.8369) — Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1` (medium, support, score=0.5366, boosted=0.5366) — Restart Ignition and verify OptiSweep service response with GetAgvStatuses

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / fleet-state view): Authorized AGV state correction completed and assets available for validation.
- `unhealthy` (observer=remote; tool=RMS / fleet-state view): Correction cannot safely complete or affected AGV state remains unidentified/conflicting.
- `inconclusive` (observer=remote; tool=RMS / fleet-state view): Asset identification or outcome is ambiguous; cannot confirm correction effect.

**Branches:**

- `healthy` → `node_7` when Authorized state correction completed
- `unhealthy` → `node_8` when Correction cannot safely complete / remains conflicting

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (2)</summary>

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

<details><summary>Restart Ignition and verify OptiSweep service response with GetAgvStatuses (`proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1`)</summary>

##### Runbook: Restart Ignition and verify OptiSweep service response with GetAgvStatuses

- **Procedure ID:** `proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Conditional incident-derived recovery guidance for restarting Ignition and confirming OptiSweep service responsiveness before releasing the E-stop. The source instructs the operator to first E-stop the system, restart Ignition with `gwcmd -r`, wait until the gateway is back up and login is possible, then verify OptiSweep by sending a GetAgvStatuses request. If no response is returned, restart OptiSweep, send the request again, and only then release the E-stop.

**When To Use:**
Use when the incident-specific guidance indicates Ignition may need to be restarted and you need to confirm the OptiSweep service is responding again before releasing the E-stop.

**Safety Notes:**

- First E-stop the system before attempting the restart.
- Do not release the E-stop until OptiSweep response is confirmed.
- If Ignition does not come back up to a login-capable state, stop and do not perform undocumented changes beyond the source-shared restart sequence.
- If response still cannot be confirmed after the documented restart steps, stop and escalate rather than inventing additional recovery actions.

- **Source:** `incident_case` / `source_case_228086`

**Procedure Steps:**

###### Step 1 — E-stop the system before restart

**Responsible role:** L2_support

**Instruction:**
First E-stop the system before attempting the restart.

**Healthy condition:**
The system is in E-stop and restart activity has not yet begun.

**Expected result:**
The system is placed in E-stop before any Ignition restart action is taken.

**Step Images:**

![artifact_incident_228086_page_014_embedded_image_01](assets/0d41c4115fc03143.png)

*Emergency stop control area highlighted in the RMS/system control context.*

---

###### Step 2 — Restart Ignition from the Ignition directory

**Responsible role:** L2_support

**Instruction:**
Open a Windows command prompt on the Ignition host, navigate to the Ignition installation directory, and run `gwcmd -r` from `C:\Program Files\Inductive Automation\Ignition>`. Observe the console message `Waiting for Gateway restart...`.

**Healthy condition:**
The command prompt shows `gwcmd -r` executed from the Ignition directory and displays `Waiting for Gateway restart...`.

**Expected result:**
The Ignition gateway restart command is accepted and the console shows `Waiting for Gateway restart...`.

**Step Images:**

![artifact_incident_228086_page_015_embedded_image_01](assets/30dd5b0a07803c56.png)

*Command prompt in `C:\Program Files\Inductive Automation\Ignition>` showing `gwcmd -r` and `Waiting for Gateway restart...`.*

![artifact_incident_228086_page_012_nested_image_02](assets/9326afd07f2ffe67.png)

*Restart-instruction screenshot context showing the Ignition restart command sequence.*

---

###### Step 3 — Wait for Ignition to come back up

**Responsible role:** L2_support

**Instruction:**
Wait for Ignition to come back up, meaning it lets you log in and does not show the gateway starting up. Use the Ignition status/login page to confirm the gateway is reachable.

**Healthy condition:**
The Ignition Status > Systems > Overview page is reachable, with visible system widgets and no gateway-starting-up screen.

**Expected result:**
Ignition is reachable again and presents a login-capable or status page rather than a startup screen.

**Step Images:**

![artifact_incident_228086_page_016_embedded_image_01](assets/6e057be40744620d.png)

*Ignition Status > Systems > Overview page reachable in the browser, with Current Response Time and no startup screen.*

---

###### Step 4 — Send GetAgvStatuses request after Ignition restart

**Responsible role:** L2_support

**Instruction:**
Open the API client identified in the source as api dog and send a GetAgvStatuses request to `http://10.27.80.165:5000/GetAgvStatuses`.

**Healthy condition:**
The API client shows the GetAgvStatuses request executed successfully against the documented endpoint.

**Expected result:**
The request executes against the shown endpoint and returns a response from the OptiSweep service.

**Step Images:**

![artifact_incident_228086_page_017_embedded_image_01](assets/8625154eb02b186c.png)

*API client showing GET request to `http://10.27.80.165:5000/GetAgvStatuses`.*

---

###### Step 5 — Confirm HTTP 200 and returned AGV records

**Responsible role:** L2_support

**Instruction:**
Check that the GetAgvStatuses request returns HTTP 200 and returned AGV records. Visible records in the source include status values such as `NORMAL`. Do not treat the visible schema validation warning alone as a service outage if the request still returns HTTP 200 with data.

**Healthy condition:**
The response panel shows Success (200) / Status: 200 and returned JSON records with visible AGV status values such as `NORMAL`.

**Expected result:**
The API response shows Success/Status 200 and returned AGV records, including visible status values such as `NORMAL`.

**Step Images:**

![artifact_incident_228086_page_017_embedded_image_01](assets/8625154eb02b186c.png)

*Response panel showing Success/Status 200 and returned records with visible `NORMAL` values; note the validation warning but do not treat it alone as outage proof.*

---

###### Step 6 — If no response, restart OptiSweep and retry GetAgvStatuses

**Responsible role:** L2_support

**Instruction:**
If no response is given, restart OptiSweep, then send another GetAgvStatuses request to confirm response. The source supports this at a high level only; use the Windows Services console context shown for OptiSweep and do not invent additional click-by-click steps not present in the source.

**Healthy condition:**
The follow-up request returns a confirmed response after the OptiSweep restart.

**Expected result:**
OptiSweep is restarted and a follow-up GetAgvStatuses request is sent to confirm response.

**Step Images:**

![artifact_incident_228086_page_019_embedded_image_01](assets/3832c5ce44b05a86.png)

*Windows Services console with OptiSweep selected, showing Running state and restart control visible.*

![artifact_incident_228086_page_017_embedded_image_01](assets/8625154eb02b186c.png)

*Use the same GetAgvStatuses request view to retry and confirm response.*

---

###### Step 7 — Release the E-stop after response is confirmed

**Responsible role:** L2_support

**Instruction:**
Once the response is confirmed, release the E-stop.

**Healthy condition:**
A confirmed GetAgvStatuses response exists before the E-stop is released.

**Expected result:**
The E-stop is released only after OptiSweep response has been confirmed.

**Step Images:**

![artifact_incident_228086_page_014_embedded_image_01](assets/0d41c4115fc03143.png)

*System control context with emergency stop control area relevant to release after confirmation.*

---

**Success Criteria:**

- Ignition is reachable again and allows login or status-page access rather than showing gateway startup.
- The GetAgvStatuses request to `http://10.27.80.165:5000/GetAgvStatuses` returns HTTP 200.
- Returned AGV records are visible in the response, including status values such as `NORMAL`.
- If OptiSweep had to be restarted, a follow-up GetAgvStatuses request confirms response.
- The E-stop is released only after response confirmation.

**Failure Conditions:**

- Ignition does not come back up to a login-capable state.
- The GetAgvStatuses endpoint is unreachable or returns no response.
- The request returns no data.
- Response still cannot be confirmed after the documented OptiSweep restart and retry.
- Recovery would require undocumented actions beyond the source-shared sequence.


</details>

</details>

---

### 7 — Validate service, API, fleet state, and automated operation (`validation_gate`)

**Intent:** Confirm that the recovered service is responsive, AGV state is usable, and the site can resume stable automated operation.

**Expects capability:** wcs_api_responsiveness, fleet_system_status, agv_active_errors
**Expects surface:** wcs_api, rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.5211, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.5484, boosted=1.0733333333333333) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.6906, boosted=1.3139333333333334) — Query Active AGV Errors From the WCS Database
  - gaps: Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).
- Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=WCS/SSMS (active error query) + API validation (GetAgvStatuses) + RMS fleet view): Recovered service/API responsiveness and usable fleet state; site confirms stable automated operation resumed.
- `unhealthy` (observer=site_or_remote; tool=WCS/SSMS + API + RMS fleet view): Validation fails; continued stoppage or persistently faulted/unusable fleet state.
- `inconclusive` (observer=site_or_remote; tool=API + RMS fleet view): API reachability succeeds but operational recovery is not confirmed (e.g., schema warning / ambiguous validation).

**Branches:**

- `healthy` → `` when Recovered and stable
- `unhealthy` → `node_8` when Validation fails / contradictory / operation not resumed

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

### 8 — Stop and escalate unresolved or unsafe recovery (`escalation_gate`)

**Intent:** Hand off when the supported diagnostic and recovery path cannot safely establish a recovery state or validation fails.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=Windows Event Viewer / Windows Services + RMS + WCS/SSMS (read-only) + API evidence): Stop and escalate because recovery is unsafe, incomplete, or validation fails/contradictions remain.

**Branches:**

- `escalate` → `` when Escalate

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Broad stoppage confirmed | `node_2` |
| `node_1` | `healthy` | Localized/normal operation | `node_4` |
| `node_2` | `unhealthy` | Correlated service/application failure indicated | `node_4` |
| `node_2` | `healthy` | No correlated failure; OptiSweep running | `node_4` |
| `node_3` | `healthy` | Recovery completed (authorized) | `node_5` |
| `node_3` | `unhealthy` | Recovery incomplete/unsafe/no confirmed end state | `node_8` |
| `node_4` | `unhealthy` | Active errors/abnormal state or conflict indicated | `node_8` |
| `node_4` | `healthy` | No relevant active errors; system normal | `` |
| `node_5` | `unhealthy` | Residual out-of-sync/abnormal state remains | `node_6` |
| `node_5` | `healthy` | Fleet state consistent; no residual error | `node_7` |
| `node_6` | `healthy` | Authorized state correction completed | `node_7` |
| `node_6` | `unhealthy` | Correction cannot safely complete / remains conflicting | `node_8` |
| `node_7` | `healthy` | Recovered and stable | `` |
| `node_7` | `unhealthy` | Validation fails / contradictory / operation not resumed | `node_8` |
| `node_8` | `escalate` | Escalate | `` |

## Unresolved / Low-Confidence Links

- node_2: proc_verify_optsweep_wcs_windows_service_health_v1 (low)
- node_4: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_4: proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1 (low)
- node_5: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_5: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_5: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_7: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_7: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_7: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_8: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
