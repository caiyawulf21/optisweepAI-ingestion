# Hospital tote induction failure with AGV or service-state disruption

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_and_agv_state_recovery` |
| Case ID | `223554` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital station cannot add or induct totes while tote removal may still work.
- A robot or AGV is reported in a shut down state, unexpected location, or abnormal rack/zone state.
- The site cannot start sort or goes down during sort.
- Hospital backlog or empty totes accumulate after tipping.
- Tipper operators report related station or alarm symptoms.

## Affected Systems

- ACB hospital station
- Hospital Lane
- AGV hospital station
- AGVs and robot roster/location state
- Tote associations and hospital tote flow
- OptiSweep services
- RMS or hospital HMI views
- Tippers and operator stations

## Nodes

### 1 — Confirm hospital induction or site-operation symptom (`diagnostic_decision`)

**Intent:** Confirm whether the reported problem is a hospital tote-add/induction failure, a broader inability to start or sustain sort, or a different symptom that should leave this path.

**Expects capability:** hospital_diversion, lane_or_chute_state
**Expects surface:** hospital_hmi, site_interview
**Preferred audience:** operator, L1_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital HMI indicates normal operation: totes can be added/inducted and removed/extracted with no relevant active hospital indication.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital induction/add is blocked and/or station evidence indicates a hospital workflow fault that matches the induction failure symptom class.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Cannot reliably confirm due to unreadable/unavailable HMI evidence or contradictory reports; symptom may be localized or mixed.

**Branches:**

- `unhealthy` → `node_2` when Confirmed hospital induction failure or broader sort operational disruption
- `healthy` → `` when Hospital add/remove and sort appear normal or symptom not for this path
- `escalate` → `node_8` when Evidence unavailable/contradictory

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Check hospital and fleet service health (`diagnostic_decision`)

**Intent:** Determine whether an abnormal OptiSweep, AGV hospital service, or related server/service state correlates with the hospital or site-wide symptom.

**Expects capability:** windows_service_or_event_log, wcs_service_health, wcs_api_responsiveness
**Expects surface:** event_viewer, wcs_api
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_verify_optsweep_wcs_windows_service_health_v1` (low, support, score=0.6433, boosted=1.0) — Verify OptiSweep/WCS Windows service health when RMS/logs appear silent
  - gaps: Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.
- `proc_confirm_rms_robotcontrol_load_during_services_unplanned_restart_v1` (low, support, score=0.4245, boosted=0.8245) — Confirm RMS robotControl screen loads during Services Unplanned restart (before UPS removes master estop)
  - gaps: Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.4796, boosted=1.0329333333333333) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `wcs_service_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `wcs_service_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Windows Services/Event Viewer + WCS API (read-only)): OptiSweep/WCS services appear healthy and API responsiveness is not indicating a server-side outage.
- `unhealthy` (observer=remote; tool=Windows Services/Event Viewer + WCS API (read-only)): Service/app issues correlate with the hospital/site symptom class (evidence of service trouble, stopped/crashed services, or unresponsive API).
- `inconclusive` (observer=remote; tool=Windows Services/Event Viewer + WCS API (read-only)): Live status evidence is unavailable/contradictory; cannot confirm service health from logs/host state.

**Branches:**

- `unhealthy` → `node_3` when Service/API health is abnormal
- `healthy` → `node_3` when Service/API appears responsive/healthy
- `escalate` → `node_8` when Live service evidence unavailable/contradictory

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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

<details><summary>Confirm RMS robotControl screen loads during Services Unplanned restart (before UPS removes master estop) (`proc_confirm_rms_robotcontrol_load_during_services_unplanned_restart_v1`)</summary>

##### Runbook: Confirm RMS robotControl screen loads during Services Unplanned restart (before UPS removes master estop)

- **Procedure ID:** `proc_confirm_rms_robotcontrol_load_during_services_unplanned_restart_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI to confirm the robotControl/monitor screen fully loads before proceeding with the Services Unplanned restart sequence timing that is tied to UPS removing the master estop.

**When To Use:**
When performing (or preparing to perform) the Services Unplanned restart sequence and you must verify the RMS robotControl/monitor screen is reachable and fully loads before the UPS-related step involving master estop removal.

**Safety Notes:**

- Do not proceed to the UPS/master estop timing step if the RMS robotControl/monitor screen fails to load or remains in a loading/error state.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI to the robotControl monitor path

**Responsible role:** L1_support

**Instruction:**
In a browser, open the RMS / fleet status UI using the RMS URL path fragment shown in the reference that ends with "monitor/robotControl".

**Healthy condition:**
The RMS robotControl/monitor view route is reached (no immediate navigation error).

**Expected result:**
The browser navigates to the RMS robotControl/monitor view (URL path includes "monitor/robotControl").

---

###### Step 2 — Log into RMS

**Responsible role:** L1_support

**Instruction:**
Log into RMS using the site/FORTNA credentials workflow you normally use for RMS access.

**Healthy condition:**
No authentication error is shown; the robotControl/monitor page proceeds to load.

**Expected result:**
You are authenticated in RMS and the robotControl/monitor view can begin loading.

---

###### Step 3 — Wait for robotControl/monitor screen to fully load

**Responsible role:** L1_support

**Instruction:**
Wait for the robotControl/monitor screen to fully load until the page finishes loading and the robotControl view elements are visible (not blank, not stuck loading, not showing an error state).

**Healthy condition:**
RobotControl view elements are visible and the page is not in a persistent loading state or error state.

**Expected result:**
The RMS robotControl/monitor view loads successfully and is visibly present in the RMS UI (not blank, not stuck loading, not showing an error).

---

**Success Criteria:**

- robotControl/monitor view is visibly present in RMS UI (not blank, not stuck loading, not showing an error).

**Failure Conditions:**

- robotControl/monitor page is blank, remains in loading, or shows an error state.


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

### 3 — Check AGV roster, location, and tote association state (`diagnostic_decision`)

**Intent:** Determine whether AGV location, roster, task, or tote-association anomalies are present and may be blocking hospital induction or broader flow.

**Expects capability:** device_roster_state, agv_active_errors, robot_command_or_task_state
**Expects surface:** rms_ui, wcs_sql, wcs_api
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.6124, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.5012, boosted=1.0733333333333333) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_query_active_agv_errors_from_the_wcs_database_v1` (low, support, score=0.3, boosted=0.8833333333333333) — Query Active AGV Errors From the WCS Database
  - gaps: Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.; Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Wrong catalog family: active AGV error SQL (SystemActiveErrorModel) does not corroborate this node's expected capabilities — pick the WCS/SSMS model that matches roster, lifecycle, hospital, pairing, or service-health intent.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS fleet status + WCS/SSMS read-only error evidence): AGV roster/location/task state appears coherent and no evidence of stranded/disconnected tote association that would block hospital induction.
- `unhealthy` (observer=remote; tool=RMS fleet status + WCS/SSMS read-only error evidence): Detected anomalies in AGV roster/location/task or tote associations (e.g., shutdown state or unexpected location/duplicate occupancy), suggesting a state inconsistency contribution to hospital induction/flow.
- `inconclusive` (observer=remote; tool=RMS + WCS/SSMS read-only evidence): Evidence of roster/tote association anomalies cannot be confirmed (unreadable screenshots, remote evidence unavailable, RMS/backend disagreement).

**Branches:**

- `unhealthy` → `node_4` when AGV roster/location/task/association anomaly present
- `healthy` → `node_4` when Roster/location/task state coherent
- `escalate` → `node_8` when Fleet/association evidence unavailable or contradictory

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

### 4 — Check tipper station contribution when hospital flow follows tipping (`diagnostic_decision`)

**Intent:** Determine whether a tipper alarm, station state, or operator-station condition is contributing to totes being directed incorrectly or the hospital workflow not progressing.

**Expects capability:** tipper_station_fault, opc_connection_or_tipper_heartbeat
**Expects surface:** tipper_hmi, ignition_gateway, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_check_smalls_system_health_smalls_overview_hmi_v1` (low, operator, score=0.7168, boosted=0.7468) — Check SMALLS System Health Using the Smalls Overview HMI Screen (Color-Coded Layout)
  - gaps: Missing corroboration for `opc_connection_or_tipper_heartbeat`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `tipper_station_fault`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1` (low, operator, score=0.5857, boosted=0.6157) — Start OptiSweep AGV System From Shut-down Mode (Reset Metrics → Start → Close out/Bag Out → Running)
  - gaps: Missing corroboration for `opc_connection_or_tipper_heartbeat`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `tipper_station_fault`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_start_optsweep_agv_system_reset_metrics_start_closeout_bagout_verify_running_shutdown_v1` (low, operator, score=0.5821, boosted=0.6121) — Start OptiSweep AGV System (Reset Metrics → Start System → Close Out/Bag Out → Verify Running → Shut Down)
  - gaps: Missing corroboration for `opc_connection_or_tipper_heartbeat`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `tipper_station_fault`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `opc_connection_or_tipper_heartbeat`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `tipper_station_fault`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Tipper HMI / Operator station stacklights): Tipper station contribution not indicated: no relevant VISU/tipper station state alarm evidence and heartbeat/operational indicators are normal (as observable via station stacklights).
- `unhealthy` (observer=site_or_remote; tool=Tipper HMI / Operator station stacklights): Tipper station contribution indicated: active tipper alarm/station fault evidence observed and should be incorporated into recovery direction selection.
- `inconclusive` (observer=site_or_remote; tool=Tipper HMI / Operator station stacklights): Tipper evidence unavailable/ambiguous (second-hand only or unreadable screen evidence).

**Branches:**

- `unhealthy` → `node_5` when Tipper alarm/station fault/heartbeat abnormal observed
- `healthy` → `node_5` when Tipper evidence normal
- `inconclusive` → `node_5` when Tipper evidence unavailable/ambiguous

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (3)</summary>

<details><summary>Check SMALLS System Health Using the Smalls Overview HMI Screen (Color-Coded Layout) (`proc_check_smalls_system_health_smalls_overview_hmi_v1`)</summary>

##### Runbook: Check SMALLS System Health Using the Smalls Overview HMI Screen (Color-Coded Layout)

- **Procedure ID:** `proc_check_smalls_system_health_smalls_overview_hmi_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the SMALLS overview screen on the System HMI to quickly identify which parts of the SMALLS system are in a normal vs abnormal (color-coded) status based on the system layout.

**When To Use:**
When you need a fast, at-a-glance health check of the SMALLS system parts using the color-coded SMALLS system layout.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the "Smalls" overview screen from the System HMI

**Responsible role:** operator

**Instruction:**
On the System HMI, press the SMALLS button to open the "Smalls" overview screen.

**Healthy condition:**
The "Smalls" overview screen loads successfully and shows the SMALLS system layout.

**Expected result:**
The "Smalls" overview screen is displayed.

---

###### Step 2 — Review the SMALLS system layout on the "Smalls" overview screen

**Responsible role:** operator

**Instruction:**
On the "Smalls" overview screen, review the SMALLS system layout.

**Healthy condition:**
The layout is fully visible and each part is present on the screen for color inspection.

**Expected result:**
You can see the SMALLS system layout with parts displayed for status checking.

---

###### Step 3 — Check each SMALLS part’s color-coded status indicator

**Responsible role:** operator

**Instruction:**
For each part shown on the layout, observe the color-coded status indicator.

**Healthy condition:**
All parts show the normal/expected color-coded status indicators for their respective parts.

**Expected result:**
You have identified which parts (if any) show abnormal color-coded status (i.e., not the normal/expected color for that part).

---

###### Step 4 — Identify abnormal parts and decide whether to stop/escalate

**Responsible role:** operator

**Instruction:**
Identify any parts whose color-coded status indicates an abnormal condition (i.e., not the normal/expected color for that part). If the layout indicates an offline/blocked section requiring support action, treat it as abnormal.

**Healthy condition:**
No parts indicate abnormal color-coded status; no offline/blocked section is indicated.

**Expected result:**
You have a clear list of abnormal parts (if any) and a decision to escalate when abnormality is widespread or unclear.

---

**Success Criteria:**

- Operator can open the "Smalls" overview screen and visually identify abnormal color-coded status indicators for any SMALLS parts.
- Operator escalates when multiple parts show abnormal color-coded status or when abnormality is unclear.

**Failure Conditions:**

- One or more SMALLS parts show abnormal color-coded status indicators.
- Multiple SMALLS parts show abnormal color-coded status indicators.
- The operator cannot determine which parts are abnormal from the screen.
- The layout indicates an offline/blocked section requiring support action.


</details>

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

<details><summary>Start OptiSweep AGV System (Reset Metrics → Start System → Close Out/Bag Out → Verify Running → Shut Down) (`proc_start_optsweep_agv_system_reset_metrics_start_closeout_bagout_verify_running_shutdown_v1`)</summary>

##### Runbook: Start OptiSweep AGV System (Reset Metrics → Start System → Close Out/Bag Out → Verify Running → Shut Down)

- **Procedure ID:** `proc_start_optsweep_agv_system_reset_metrics_start_closeout_bagout_verify_running_shutdown_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Perform the required AGV start-up prerequisites (nine empty AGVs: five under the north rack and four under the south rack), start the OptiSweep system 15 minutes before the sort, run the documented start sequence (Reset Metrics → Start System → Close Out/Bag Out), verify the system returns to the "Running" state after Bag Out, and then shut down.

**When To Use:**
Use to start the OptiSweep AGV system for an upcoming sort, ensuring the system is properly prepared (nine empty AGVs) and that the system transitions back to the "Running" state after close out (Bag Out).

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Verify nine empty AGVs are present (5 north / 4 south)

**Responsible role:** operator

**Instruction:**
Verify there are nine (9) AGVs without totes in the system: five (5) under the north rack and four (4) under the south rack.

**Healthy condition:**
North rack has 5 AGVs without totes and south rack has 4 AGVs without totes.

**Expected result:**
You confirm five (5) empty AGVs under the north rack and four (4) empty AGVs under the south rack.

---

###### Step 2 — Move an empty AGV into the missing zone and add it to RMS (if needed)

**Responsible role:** operator

**Instruction:**
If fewer than nine empty AGVs are present, move an AGV without a tote into the zone that is missing an empty AGV, then add that AGV to the RMS after moving it.

**Healthy condition:**
After adding the moved AGV in RMS, the AGV is successfully registered (per the RMS add screen procedure, the AGV turns blue and its status is verified as "szonestaging").

**Expected result:**
The missing zone now has an empty AGV, and the moved AGV has been added to RMS.

---

###### Step 3 — Confirm start timing (15 minutes before sort starts)

**Responsible role:** operator

**Instruction:**
Confirm the system start will occur 15 minutes before the sort starts.

**Healthy condition:**
System start is initiated at the required lead time (15 minutes before sort starts).

**Expected result:**
You confirm the start time is set to occur 15 minutes before the sort begins.

---

###### Step 4 — Reset metrics

**Responsible role:** operator

**Instruction:**
On the system control surface (System API Controls), perform the Reset Metrics step.

**Healthy condition:**
Reset Metrics is executed as the first step in the sequence before starting the system.

**Expected result:**
Metrics have been reset (Reset Metrics action completed on the System API Controls screen).

---

###### Step 5 — Start the system

**Responsible role:** operator

**Instruction:**
On the system control surface (System API Controls), start the system using the System Startup control.

**Healthy condition:**
System Startup is executed after Reset Metrics and before Close Out (Bag Out).

**Expected result:**
The system is placed into the running state via the System Startup control.

---

###### Step 6 — Perform close out (Bag Out)

**Responsible role:** operator

**Instruction:**
On the system control surface (System API Controls), perform Close Out (Bag Out) as the next step in the sequence.

**Healthy condition:**
Close Out (Bag Out) completes as the third step in the sequence.

**Expected result:**
Close out (Bag Out) is completed.

---

###### Step 7 — Verify system returns to "Running" after Bag Out

**Responsible role:** operator

**Instruction:**
After close out (Bag Out) is completed, verify the system state returns to "Running".

**Healthy condition:**
System state shows "Running".

**Expected result:**
System state is "Running" after Bag Out completes.

---

###### Step 8 — Shut down the system

**Responsible role:** operator

**Instruction:**
On the system control surface (System API Controls), shut down the system using the System Shutdown control.

**Healthy condition:**
Shutdown is performed as the final step after Bag Out and verification of "Running".

**Expected result:**
System shutdown is initiated/completed via the System Shutdown control.

---

**Success Criteria:**

- Nine empty AGVs prerequisite is satisfied (5 under north rack, 4 under south rack), with any moved empty AGV added to RMS.
- System is started 15 minutes before the sort starts.
- After close out (Bag Out) is completed, the system state returns to "Running".
- System shutdown is completed as the final step.

**Failure Conditions:**

- System does not return to "Running" after close out (Bag Out).
- Nine empty AGV prerequisite cannot be met (not 5 north / 4 south) without moving an empty AGV and adding it to RMS.


</details>

</details>

---

### 5 — Select supported recovery direction (`branching_condition`)

**Intent:** Select service recovery, AGV/tote-state correction, tipper-state handling, or a combined authorized path based on observed evidence rather than the tentative hypothesis alone.

**Expects capability:** wcs_service_health, device_roster_state, tipper_station_fault
**Expects surface:** event_viewer, wcs_api, rms_ui, wcs_sql, tipper_hmi
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Event Viewer/Services + RMS + Hospital HMI + tipper HMI + read-only WCS/SSMS): A supported and authorized recovery direction is identified based on confirmed evidence (service/API vs AGV/tote vs tipper), not on tentative patterns alone.
- `unhealthy` (observer=remote; tool=Event Viewer/Services + RMS + Hospital HMI + tipper HMI + read-only WCS/SSMS): Recovery direction cannot be supported by evidence or contradicts observed state; do not proceed with recovery mutations.
- `inconclusive` (observer=remote; tool=Event Viewer/Services + RMS + Hospital HMI + tipper HMI + read-only WCS/SSMS): Insufficient or partial evidence prevents confident selection of a safe, authorized path.
- `escalate` (observer=remote; tool=Evidence packet compilation): Need escalation due to missing evidence or inability to identify a supported recovery direction.

**Branches:**

- `healthy` → `node_6` when Supported recovery direction identified
- `escalate` → `node_8` when No supported recovery direction or insufficient evidence

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 6 — Perform authorized recovery for service and operational state (`procedure_reference`)

**Intent:** Apply the approved recovery path for the observed service, AGV/tote state, or tipper condition within role and safety limits.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, operator

**Runbook Links:**

- `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1` (low, support, score=0.6967, boosted=0.8667) — Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI + RMS + WCS/SSMS read-only/API response): Authorized recovery completed with observable improvement and stable evidence from the relevant systems.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI + RMS + WCS/SSMS read-only/API response): Recovery does not complete successfully or creates/keeps an unresolved state inconsistency.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI + RMS + WCS/SSMS read-only/API response): Recovery actions taken but no reliable post-action evidence can be obtained.

**Branches:**

- `healthy` → `node_7` when Authorized recovery completed
- `escalate` → `node_8` when Recovery cannot be completed safely or remains unsupported

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

### 7 — Validate hospital induction and stable site operation (`validation_gate`)

**Intent:** Confirm that the hospital workflow and broader sort operation have recovered and remain stable before declaring the troubleshooting path successful.

**Expects capability:** hospital_diversion, device_roster_state, wcs_api_responsiveness, fleet_system_status
**Expects surface:** hospital_hmi, rms_ui, wcs_sql, wcs_api, event_viewer
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.5897, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.3, boosted=0.9299999999999999) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1` (low, support, score=0.3, boosted=0.7350000000000001) — Check OPC COM tag subscription updates flowing to Sorter Sweeper (Ignition tag provider → OPC server → Sorter Sweeper processing)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI + RMS fleet status + WCS/SSMS read-only/API): Hospital induction recovered and stable: totes can be added/removed and hospital backlog progresses; fleet motion/roster state appears coherent and sort starts/continues.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI + RMS fleet status + WCS/SSMS read-only/API): Validation failure: hospital induction remains blocked or fleet/tote state remains abnormal and sort is down/unstable.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI + RMS fleet status + WCS/SSMS read-only/API): Partial validation: operations appear to be running but workflow-specific evidence is not confirmed or is contradictory.

**Branches:**

- `healthy` → `` when Validated hospital induction + stable operation
- `unhealthy` → `node_8` when Hospital induction blocked or sort remains unstable/down

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

</details>

---

### 8 — Stop and escalate when supported recovery or validation fails (`escalation_gate`)

**Intent:** Stop the playbook when evidence is insufficient, recovery is unauthorized or unsafe, or the hospital or site-wide operation remains unstable after the supported path.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=Event Viewer + Windows Services + RMS + WCS/SSMS read-only + Hospital HMI/tipper HMI): Stop: insufficient evidence, unsupported recovery attempt, unauthorized/unsafe actions, or stability not restored after authorized recovery.
- `inconclusive` (observer=remote; tool=Evidence package compilation): Stop/hold pending evidence completion because logs/screens/evidence are missing or unreadable.

**Branches:**

- `escalate` → `` when Escalation evidence package is complete and handoff is accepted

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Confirmed hospital induction failure or broader sort operational disruption | `node_2` |
| `node_1` | `healthy` | Hospital add/remove and sort appear normal or symptom not for this path | `` |
| `node_1` | `escalate` | Evidence unavailable/contradictory | `node_8` |
| `node_2` | `unhealthy` | Service/API health is abnormal | `node_3` |
| `node_2` | `healthy` | Service/API appears responsive/healthy | `node_3` |
| `node_2` | `escalate` | Live service evidence unavailable/contradictory | `node_8` |
| `node_3` | `unhealthy` | AGV roster/location/task/association anomaly present | `node_4` |
| `node_3` | `healthy` | Roster/location/task state coherent | `node_4` |
| `node_3` | `escalate` | Fleet/association evidence unavailable or contradictory | `node_8` |
| `node_4` | `unhealthy` | Tipper alarm/station fault/heartbeat abnormal observed | `node_5` |
| `node_4` | `healthy` | Tipper evidence normal | `node_5` |
| `node_4` | `inconclusive` | Tipper evidence unavailable/ambiguous | `node_5` |
| `node_5` | `healthy` | Supported recovery direction identified | `node_6` |
| `node_5` | `escalate` | No supported recovery direction or insufficient evidence | `node_8` |
| `node_6` | `healthy` | Authorized recovery completed | `node_7` |
| `node_6` | `escalate` | Recovery cannot be completed safely or remains unsupported | `node_8` |
| `node_7` | `healthy` | Validated hospital induction + stable operation | `` |
| `node_7` | `unhealthy` | Hospital induction blocked or sort remains unstable/down | `node_8` |
| `node_8` | `escalate` | Escalation evidence package is complete and handoff is accepted | `` |

## Unresolved / Low-Confidence Links

- node_1: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_2: proc_verify_optsweep_wcs_windows_service_health_v1 (low)
- node_2: proc_confirm_rms_robotcontrol_load_during_services_unplanned_restart_v1 (low)
- node_2: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_3: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_3: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_3: proc_query_active_agv_errors_from_the_wcs_database_v1 (low)
- node_4: proc_check_smalls_system_health_smalls_overview_hmi_v1 (low)
- node_4: proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1 (low)
- node_4: proc_start_optsweep_agv_system_reset_metrics_start_closeout_bagout_verify_running_shutdown_v1 (low)
- node_5: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_6: proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1 (low)
- node_7: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_7: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_7: proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1 (low)
- node_8: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
