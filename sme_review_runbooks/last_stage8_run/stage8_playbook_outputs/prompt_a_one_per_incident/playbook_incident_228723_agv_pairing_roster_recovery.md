# AGV pairing failure with abnormal fleet roster or mapping state

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228723_agv_pairing_roster_recovery` |
| Case ID | `228723` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- A zone cannot get an AGV or AMR pair.
- The ACB system is reported as down or unable to operate normally.
- Replacement AMRs route to the hospital lane instead of serving the affected workflow.
- An AMR is reported with low battery, unable to leave an area, or otherwise not behaving normally.

## Affected Systems

- ACB system
- AMRs / AGVs
- RMS / fleet status
- Zone pairing state
- Hospital lane

## Nodes

### 1 — Confirm pairing failure and fleet behavior (`diagnostic_decision`)

**Intent:** Determine whether the reported issue is an active zone pairing failure accompanied by abnormal AGV or AMR behavior.

**Expects capability:** zone_pairing_state, fleet_system_status
**Expects surface:** rms_ui, site_interview
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.5123, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.5621, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.5693, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Zone pairing is normal and fleet routing behavior matches expected operation.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Active pairing failure and/or abnormal routing behavior is confirmed.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Symptoms are reported but key evidence (pairing/routing) cannot be confirmed reliably.
- `escalate` (observer=remote; tool=RMS / AGV status UI): Escalate if RMS access is unavailable or safety/authorization blockers prevent further confirmation.

**Branches:**

- `unhealthy` → `node_2` when Confirmed zone pairing failure or abnormal AGV routing is observed
- `healthy` → `node_5` when Pairing is normal and the reported abnormal routing/fleet symptom is not reproduced

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

### 2 — Check AGV roster and mapping consistency (`diagnostic_decision`)

**Intent:** Determine whether an AGV roster, mapping, location, or membership inconsistency is present after replacement or add/remove activity.

**Expects capability:** device_roster_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (medium, support, score=0.4822, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Limited domain-term overlap between placeholder and runbook.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (high, support, score=0.3875, boosted=1.0) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1` (low, support, score=0.3, boosted=0.2971) — Verify Robot Location model fields and location types/statuses used by RMS orange locations
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI): Rosters and mapping state are coherent (no unmapped/mismatched robot indicators).
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): Roster/mapping inconsistency is indicated (e.g., removed robot shown as not mapped / wrong zone).
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Evidence is insufficient (unreadable RMS fields or inaccessible SSMS).
- `escalate` (observer=remote; tool=RMS / AGV status UI): Escalate if inconsistencies cannot be interpreted or corroboration cannot be obtained.

**Branches:**

- `unhealthy` → `node_3` when Roster, mapping, location, or fleet membership inconsistency is indicated
- `healthy` → `node_5` when Roster and mapping state are coherent or suspected pattern is not indicated

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

### 3 — Use authorized AGV isolation or removal recovery when roster state is abnormal (`procedure_reference`)

**Intent:** Perform an approved site-side or system-side AGV isolation or removal action when an abnormal roster or mapping state is supported and the responsible role is authorized.

**Expects capability:** agv_physical_recovery, device_roster_state
**Expects surface:** physical_floor, rms_ui, wcs_api
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1` (low, operator, score=0.8081, boosted=1.0) — Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=physical_floor + RMS / AGV status UI): Authorized isolation/removal recovery completed; robot is in a safe intended state and no longer interferes with pairing.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Recovery fails or leaves the robot active in an abnormal state; fleet remains unable to pair.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Physical safety or system confirmation is missing.
- `escalate` (observer=site_or_remote; tool=physical_floor): Stop due to unsafe conditions or unauthorized/unapproved recovery execution.

**Branches:**

- `healthy` → `node_4` when Authorized AGV isolation or removal recovery is completed and the robot is in a safe, intended state
- `escalate` → `node_5` when Recovery cannot be performed safely, is unauthorized, fails, or leaves the robot in an abnormal state

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

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

</details>

---

### 4 — Validate pairing and stable automated operation (`validation_gate`)

**Intent:** Confirm that the affected workflow has recovered after the AGV isolation or removal action and remains stable during observation.

**Expects capability:** zone_pairing_state, fleet_system_status, device_roster_state
**Expects surface:** rms_ui, site_interview
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.4497, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Pairing and automated operation are restored and remain stable during monitoring.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Pairing failure/abnormal routing persists or recurs after recovery.
- `inconclusive` (observer=remote; tool=site_interview): Only narrative recovery or administrative case closure is available without direct operational/RMS confirmation.
- `escalate` (observer=remote; tool=RMS / AGV status UI): Escalate if the validation cannot be performed reliably or evidence conflicts.

**Branches:**

- `healthy` → `node_5` when Pairing and automated operation are restored and remain stable during monitoring
- `unhealthy` → `node_5` when Pairing failure, abnormal routing, or fleet inconsistency persists or recurs

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

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

</details>

---

### 5 — Stop when the supported recovery path is incomplete or validation fails (`escalation_gate`)

**Intent:** Hand off when safe authorization, reliable diagnostic evidence, or stable recovery is unavailable.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=WCS/SSMS (read-only) + RMS evidence): Escalate for unresolved pairing/roster recovery, unsafe/unauthorized physical action, or failed validation.
- `inconclusive` (observer=remote; tool=RMS / WCS/SSMS (read-only)): Some evidence is missing but can be collected; proceed to gather read-only evidence for handoff.
- `healthy` (observer=remote; tool=—): Not applicable: Stop gate indicates termination path rather than recovery success.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Confirmed zone pairing failure or abnormal AGV routing is observed | `node_2` |
| `node_1` | `healthy` | Pairing is normal and the reported abnormal routing/fleet symptom is not reproduced | `node_5` |
| `node_2` | `unhealthy` | Roster, mapping, location, or fleet membership inconsistency is indicated | `node_3` |
| `node_2` | `healthy` | Roster and mapping state are coherent or suspected pattern is not indicated | `node_5` |
| `node_3` | `healthy` | Authorized AGV isolation or removal recovery is completed and the robot is in a safe, intended state | `node_4` |
| `node_3` | `escalate` | Recovery cannot be performed safely, is unauthorized, fails, or leaves the robot in an abnormal state | `node_5` |
| `node_4` | `healthy` | Pairing and automated operation are restored and remain stable during monitoring | `node_5` |
| `node_4` | `unhealthy` | Pairing failure, abnormal routing, or fleet inconsistency persists or recurs | `node_5` |

## Unresolved / Low-Confidence Links

- node_1: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_1: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_1: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_2: proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1 (low)
- node_3: proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1 (low)
- node_4: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_5: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
