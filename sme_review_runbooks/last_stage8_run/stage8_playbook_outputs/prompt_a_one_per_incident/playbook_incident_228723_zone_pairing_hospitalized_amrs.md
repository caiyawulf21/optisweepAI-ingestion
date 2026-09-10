# Zone unable to get a pair with AMRs diverting to hospital after recent robot handling

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228723_zone_pairing_hospitalized_amrs` |
| Case ID | `228723` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Affected zone reported as unable to get a pair
- ACB system reported down or production seriously impacted
- Replacement or multiple AMRs reported as going to the hospital lane
- Issue reported after low-battery AMR trouble, robot replacement, or remove/add activity

## Affected Systems

- RMS / fleet status
- AMRs / AGVs
- Hospital HMI / lane UI
- ACB system

## Nodes

### 1 — Confirm the pairing-failure and hospital-diversion symptom pattern (`diagnostic_decision`)

**Intent:** Determine whether the reported issue matches the pattern of an affected zone unable to get a pair with AMRs diverting to the hospital lane after recent robot handling activity.

**Expects capability:** hospital_diversion, zone_pairing_state
**Expects surface:** hospital_hmi
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Symptom pattern confirmed as resolved: affected zone pairs normally and AMRs are no longer diverting abnormally to the hospital lane.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Symptom pattern persists: affected zone still cannot get a pair and AMRs continue routing to the hospital lane after recent robot handling.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Insufficient corroboration: incomplete site report or Hospital HMI evidence unclear.
- `escalate` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital HMI cannot be checked or indicates broader outage preventing confirmation.

**Branches:**

- `unhealthy` → `node_2` when Affected zone still cannot get a pair and AMRs are diverting to hospital after recent robot replacement or remove/add activity
- `healthy` → `node_6` when Diagnostic check does not indicate the fault condition

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Check RMS for abnormal robot roster or mapping state (`diagnostic_decision`)

**Intent:** Determine whether RMS shows one or more robots in an abnormal roster, mapping, or related state that could explain the pairing failure and hospital diversion pattern.

**Expects capability:** device_roster_state, fleet_system_status, hospital_diversion
**Expects surface:** rms_ui, wcs_sql, hospital_hmi
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.7055, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_selected_robot_details_robot_id_location_node_code_tote_v1` (high, support, score=0.7953, boosted=1.0) — Check Selected Robot Details (Robot ID, Location, Node Code/Cell Code, Tote ID) in Robot Selection Overview
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7634, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI (and selected robot details screens)): RMS does not show abnormal roster/mapping state that would explain pairing failure and hospital diversion.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI + robot details / location state views): RMS indicates a specific abnormal robot mapping/roster state that matches the incident pattern.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): RMS evidence is unclear (e.g., unreadable screenshot/OCR) or cannot identify a specific target robot.
- `escalate` (observer=remote; tool=RMS / AGV status UI): RMS cannot be accessed or shows broader system faults preventing valid conclusions.

**Branches:**

- `unhealthy` → `node_3` when RMS indicates a specific robot is not mapped, improperly handled in remove/add flow, or otherwise abnormal
- `healthy` → `node_6` when RMS evidence is inconclusive or no supported abnormal robot target is identified

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

<details><summary>Check Selected Robot Details (Robot ID, Location, Node Code/Cell Code, Tote ID) in Robot Selection Overview (`proc_check_selected_robot_details_robot_id_location_node_code_tote_v1`)</summary>

##### Runbook: Check Selected Robot Details (Robot ID, Location, Node Code/Cell Code, Tote ID) in Robot Selection Overview

- **Procedure ID:** `proc_check_selected_robot_details_robot_id_location_node_code_tote_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the live RMS / fleet status UI Robot Selection Overview to select a robot and read its robot ID, location, node code (cell code), and tote presence/ID indicators—including the “?” tote mismatch case and the “layer_1” case when no tote is carried.

**When To Use:**
When you need to identify which robot is involved in an issue by checking the selected robot’s identifiers and tote status in the Robot Selection Overview detail panel.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open Robot Selection Overview and ensure Robot x Robot mode

**Responsible role:** L1_support

**Instruction:**
In the RMS / fleet status UI (rms_ui), open the Robot Selection Overview screen and ensure the view is in “Robot x Robot” mode (Robot option selected).

**Healthy condition:**
Selecting robots in the panel will show a selected robot box/outline and populate robot details in the expandable detail panel.

**Expected result:**
The Robot Selection Overview shows the Robot x Robot / Robot option selected and a robot list/grid that can be clicked to select a robot.

---

###### Step 2 — Select the robot in the panel

**Responsible role:** L1_support

**Instruction:**
Click a specific robot on the Robot Selection Overview panel so it becomes the selected robot (it should show a box/outline around the selected robot).

**Healthy condition:**
The selected robot box/outline is visible and the detail panel is ready to show robot-specific fields.

**Expected result:**
A box/outline appears around the selected robot, indicating it is the active selection.

---

###### Step 3 — Expand the robot detail section if hidden

**Responsible role:** L1_support

**Instruction:**
If the robot detail section is hidden, click the small arrow control to expand it so the full robot detail information is visible.

**Healthy condition:**
The detail panel expands successfully and shows all relevant fields/indicators.

**Expected result:**
The expanded detail panel displays the robot ID, location, node code (cell code), and tote indicator fields.

---

###### Step 4 — Record/verify robot ID and location

**Responsible role:** L1_support

**Instruction:**
In the expanded details, record/verify the robot ID and location fields for the selected robot.

**Healthy condition:**
Robot ID and location fields populate and correspond to the selected robot.

**Expected result:**
The detail panel shows robot ID and location values for the selected robot.

---

###### Step 5 — Verify node code (cell code) for the robot

**Responsible role:** L1_support

**Instruction:**
Verify the node code field and confirm it corresponds to the cell code for the robot (use the displayed node code value as the cell code reference).

**Healthy condition:**
Node code is present and can be used as the cell code reference for the robot’s location.

**Expected result:**
The detail panel shows a node code value, and you treat that node code as the cell code for the robot.

---

###### Step 6 — Check tote ID/presence under the robot ID

**Responsible role:** L1_support

**Instruction:**
Under the robot ID in the tote section, check the tote entry: if a tote ID is shown (e.g., “tote #96”), note the tote ID.

**Healthy condition:**
Tote ID is present under the robot ID when the robot is carrying a tote.

**Expected result:**
A tote ID value is shown under the robot ID when the robot has a tote.

---

###### Step 7 — Interpret leading “?” tote mismatch indicator

**Responsible role:** L1_support

**Instruction:**
If the tote entry shows a “?” before the tote value, interpret it as: the robot was removed but the tote was not (tote mismatch).

**Healthy condition:**
The UI clearly shows “?” before the tote value in the tote section under the robot ID.

**Expected result:**
A leading “?” appears before the tote value, indicating robot removed but tote not removed.

---

###### Step 8 — Confirm no-tote state shows “layer_1” and no brown-box tote indicator

**Responsible role:** L1_support

**Instruction:**
If no tote is present, confirm the UI shows “layer_1” and that the brown-box tote indicator is not shown.

**Healthy condition:**
No tote state is represented by “layer_1” with no brown-box tote indicator.

**Expected result:**
The tote section indicates “layer_1” and there is no brown-box tote indicator.

---

**Success Criteria:**

- You can identify the selected robot’s robot ID and location from the expanded Robot Selection Overview detail panel.
- You can read the node code value and use it as the cell code reference for the robot.
- You can determine tote state from the tote section: tote ID present, leading “?” tote mismatch, or “layer_1” no-tote state.

**Failure Conditions:**

- Detail section cannot be expanded (small arrow does not reveal details).
- Robot ID/location/tote fields do not populate after selecting a robot.
- Node code field is missing or does not populate after selection/expansion.


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

### 3 — Decide whether supported robot isolation or removal is indicated (`branching_condition`)

**Intent:** Choose whether to continue with approved AGV isolation or removal handling for a specific abnormal robot versus stopping because no supported target robot or condition is identified.

**Expects capability:** device_roster_state, agv_physical_recovery
**Expects surface:** rms_ui, physical_floor, wcs_sql
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI): A specific abnormal robot is identified and the current role is authorized to proceed with supported isolation/removal.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): An abnormal robot is suggested but evidence is insufficient to justify supported isolation/removal criteria.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Robot target may exist but evidence quality is degraded (e.g., unreadable RMS screenshot), preventing confident selection.
- `escalate` (observer=site_or_remote; tool=N/A (role gate)): Role authorization does not permit continuing to physical/supported recovery action.

**Branches:**

- `healthy` → `node_4` when A specific abnormal robot is identified and the role is authorized for supported isolation/removal
- `unhealthy` → `node_6` when No supported abnormal robot path identified or evidence/role is insufficient

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 4 — Perform approved isolation or removal of the abnormal robot (`procedure_reference`)

**Intent:** Carry out the authorized AGV isolation or removal action for the identified abnormal robot so it is no longer disrupting normal pairing or routing.

**Runbook Links:**

- `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (low, support, score=0.6873, boosted=0.9573) — Remove An AGV From The System Using The API Screen
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI (post-action verification start)): Robot/AGV is isolated/removed from active operation using approved handling.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Removal/isolation attempt does not prevent disruption (robot remains active or symptom persists immediately).
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Action executed but verification evidence is missing/unclear.
- `escalate` (observer=site; tool=N/A (safety/authorization gate)): Safety/authorization constraint violated or action cannot be completed safely.

**Branches:**

- `unhealthy` → `node_5` when Robot has been isolated or removed using approved handling

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Remove An AGV From The System Using The API Screen (`proc_remove_an_agv_from_the_system_using_the_api_screen_v1`)</summary>

##### Runbook: Remove An AGV From The System Using The API Screen

- **Procedure ID:** `proc_remove_an_agv_from_the_system_using_the_api_screen_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Remove a specified AGV from the system from the AGVs section of the API screen by entering the AGV ID and using the Remove AGV control. The source also states that if the AGV has an issue it must be physically removed from the system, and if it has a tote it must be taken to the hospital where the tote is removed and later recovered when put back in the system.

**When To Use:**
Use when a specified AGV must be removed from the system using its AGV ID from the AGVs section of the API screen, including recovery situations where the AGV has an issue and must be removed from service.

**Safety Notes:**

- The source states that if an AGV has an issue, it must be physically removed from the system.
- If the AGV has a tote, it must be taken to the hospital where the tote is removed.
- This source section does not provide detailed physical handling or hospital safety steps; follow site-specific safety and handling procedures.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the AGVs section of the API screen

**Responsible role:** L2_support

**Instruction:**
Open the API screen and navigate to the AGVs section.

**Healthy condition:**
The AGV API Controls area is open and the Remove AGV control is available.

**Expected result:**
The AGVs section of the API screen is visible.

**Step Images:**

![artifact_fig_4_8_acb_api_screen](assets/b192077f772ce5cd.jpeg)

*API screen entry point and overall ACB API interface.*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*AGVs section of the API screen and the Remove AGV control.*

---

###### Step 2 — Locate the Remove AGV control and AGV ID field

**Responsible role:** L2_support

**Instruction:**
In the AGVs section, locate the Remove AGV control and the AGV ID entry field.

**Healthy condition:**
The operator can clearly identify where to enter the AGV ID and where to trigger removal.

**Expected result:**
The Remove AGV control and AGV ID field are identified and ready for use.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*Remove AGV control and AGV ID entry area in the AGV API Controls screen.*

---

###### Step 3 — Enter the AGV ID

**Responsible role:** L2_support

**Instruction:**
Enter the AGV ID for the AGV to be removed.

**Healthy condition:**
The intended AGV ID is present in the entry field.

**Expected result:**
The target AGV ID is entered in the AGV ID field.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*AGV ID entry field used with Remove AGV.*

---

###### Step 4 — Use Remove AGV to remove the AGV from the system

**Responsible role:** L2_support

**Instruction:**
Use the Remove AGV control to remove that AGV from the system.

**Healthy condition:**
The AGV is no longer in service in the system after the removal action.

**Expected result:**
The specified AGV is removed from the system.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*Remove AGV control in the AGV API Controls screen.*

---

###### Step 5 — Physically remove the AGV if it has an issue

**Responsible role:** L2_support

**Instruction:**
If the AGV has an issue, physically remove the AGV from the system.

**Healthy condition:**
The AGV is no longer physically present in the active system where it can affect operation.

**Expected result:**
The issue-affected AGV is physically removed from the system.

**Step Images:**

![artifact_fig_4_37_hospital_hmi_add_remove_agv_screen](assets/2c21ae93aa1bc610.png)

*Hospital HMI Add/Remove AGV screen associated with removing an AGV from service.*

---

###### Step 6 — Take a tote-carrying AGV to the hospital and remove the tote

**Responsible role:** L2_support

**Instruction:**
If the AGV has a tote, take the AGV to the hospital and remove the tote there.

**Healthy condition:**
The AGV reaches the hospital process point and the tote is removed there.

**Expected result:**
The tote is removed from the AGV at the hospital.

**Step Images:**

![artifact_fig_4_37_hospital_hmi_add_remove_agv_screen](assets/2c21ae93aa1bc610.png)

*Hospital HMI Add/Remove AGV screen for AGV handling at the hospital station.*

---

###### Step 7 — Return the tote to the system for recovery

**Responsible role:** L2_support

**Instruction:**
Return the tote to the system so it can be recovered when it is put back in the system.

**Healthy condition:**
The tote is put back into the system and is available for recovery.

**Expected result:**
The tote is returned for recovery back into the system.

**Step Images:**

![artifact_page_93_image_2](assets/d1045eabc9fd3587.png)

*Add Tote or confirmation-related screen associated with returning a tote into the system.*

![artifact_fig_4_14_tote_api_controls](assets/a518b5a9f87fa387.jpeg)

*Tote API Controls area relevant to tote-related system actions.*

---

**Success Criteria:**

- The specified AGV is removed from the system using the AGV ID.
- If the AGV had an issue, it is physically removed from the system.
- If the AGV had a tote, the tote is removed at the hospital and returned to the system for recovery.

**Failure Conditions:**

- The API screen or AGVs section cannot be accessed.
- The Remove AGV control or AGV ID field cannot be used.
- The AGV is not removed from the system after the removal action.
- A problem AGV cannot be physically removed from the system.
- A tote on the AGV cannot be removed at the hospital or cannot be returned for recovery.


</details>

</details>

---

### 5 — Validate that pairing and AMR flow have recovered (`validation_gate`)

**Intent:** Confirm that the affected zone can pair again, AMRs are no longer diverting abnormally to hospital, and the system remains stable during a short monitoring period.

**Expects capability:** fleet_system_status, hospital_diversion, zone_pairing_state
**Expects surface:** rms_ui, hospital_hmi, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6505, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.7245, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7055, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI + Hospital HMI / lane UI): Recovery holds: affected zone can pair again, and AMRs stop abnormal hospital diversion during short monitoring.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI + Hospital HMI / lane UI): Validation fails: pairing/hospital diversion persists or worsens after removal action.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI + Hospital HMI / lane UI): Recovery evidence incomplete during monitoring period.
- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI): System remains unstable during monitoring window (recurrence).

**Branches:**

- `unhealthy` → `node_6` when Recovery validation criteria are not met
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

### 6 — Stop and escalate if no supported abnormal robot path is identified or validation fails (`escalation_gate`)

**Intent:** Hand off when approved checks do not identify a supported robot-isolation target, when the role is not authorized to continue, or when pairing and routing do not normalize after the supported recovery attempt.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / Hospital HMI / incident case notes): Escalation prepared appropriately with evidence and no unsupported/unauthorized recovery actions executed.
- `unhealthy` (observer=site_or_remote; tool=RMS / Hospital HMI): Validation fails and evidence is not sufficient to proceed with additional supported steps in this playbook.
- `inconclusive` (observer=site_or_remote; tool=N/A (process gate)): Role/scope ambiguity: unclear if current role is authorized to continue or whether supported targets can be identified.
- `escalate` (observer=remote; tool=Case management / escalation channel): Proceed to escalation with evidence package.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Affected zone still cannot get a pair and AMRs are diverting to hospital after recent robot replacement or remove/add activity | `node_2` |
| `node_1` | `healthy` | Diagnostic check does not indicate the fault condition | `node_6` |
| `node_2` | `unhealthy` | RMS indicates a specific robot is not mapped, improperly handled in remove/add flow, or otherwise abnormal | `node_3` |
| `node_2` | `healthy` | RMS evidence is inconclusive or no supported abnormal robot target is identified | `node_6` |
| `node_3` | `healthy` | A specific abnormal robot is identified and the role is authorized for supported isolation/removal | `node_4` |
| `node_3` | `unhealthy` | No supported abnormal robot path identified or evidence/role is insufficient | `node_6` |
| `node_4` | `unhealthy` | Robot has been isolated or removed using approved handling | `node_5` |
| `node_5` | `unhealthy` | Recovery validation criteria are not met | `node_6` |
| `node_5` | `healthy` | Recovery validation criteria are met | `` |

## Unresolved / Low-Confidence Links

- node_1: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_2: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_3: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_4: proc_remove_an_agv_from_the_system_using_the_api_screen_v1 (low)
- node_5: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_6: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
