# Recover site-wide motion stoppage by restoring OptiSweep/WCS responsiveness and resynchronizing AGVs

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228086_optisweep_crash_agv_out_of_sync_recovery` |
| Case ID | `228086` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- “Nothing is moving” across the site
- “Robotic system is not responding”
- “Small sort is not running”
- “AGVs are out of sync”
- RMS/HMI shows an abnormal/blank state with a message like “.NET Control not created.”
- WCS web application/application errors appear around the same time as the incident

## Affected Systems

- OptiSweep service
- WCSWebApplication / WCS web application
- Windows Event Viewer / Service Control Manager
- Ignition gateway (Systems Overview / status)
- RMS / HMI (ACB System RMS / Map Monitor)
- OptiSweep / WCS API endpoint used for AGV status validation (GetAgvStatuses)
- AGVs / robotic system (out-of-sync behavior)

## Nodes

### 1 — Confirm the stoppage pattern and whether OptiSweep/WCS responsiveness is faulted (`diagnostic_decision`)

**Intent:** Determine whether the reported site-wide “nothing is moving” aligns with an OptiSweep/WCS responsiveness fault pattern that warrants service restoration and AGV resynchronization.

**Expects capability:** fleet_system_status, agv_active_errors, windows_service_or_event_log
**Expects surface:** rms_ui, event_viewer, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI + WCS/SSMS (read-only)): Site symptom (“nothing is moving” / small sort stopped) is corroborated by evidence of OptiSweep/WCS faulting: RMS abnormal/blank presentation and clustered system fault/error evidence consistent with service/web responsiveness failure.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI + WCS/SSMS (read-only)): Conflicting or missing corroboration: RMS appears normal or no corroborating OptiSweep/WCS fault evidence is found for the outage window.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI + WCS/SSMS (read-only)): Evidence cannot be matched strongly: partial UI issues (blank RMS) without clear SQL corroboration, or only partial faulting is observable remotely.

**Branches:**

- `healthy` → `node_2` when Incident-supported stoppage pattern confirmed
- `unhealthy` → `` when No corroboration / conflicting evidence

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Restore OptiSweep/WCS responsiveness and prepare AGV resynchronization (`procedure_reference`)

**Intent:** Perform the approved recovery actions to restore service responsiveness (OptiSweep and any required gateway/web dependencies) so AGV state can be corrected.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_recover_from_agv_fault_during_exchange_recovery_v1` (medium, support, score=0.6256, boosted=0.7956) — Recover From AGV Fault During Exchange (RMS E-stop, remove faulted AGV, backfill, introduce new tote + empty AGV)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=WCS/SSMS (read-only) / GetAgvStatuses (API-backed)): Service restoration completed and OptiSweep/WCS responsiveness is sufficient to proceed to RMS correction.
- `unhealthy` (observer=site_or_remote; tool=WCS/SSMS (read-only) / GetAgvStatuses (API-backed)): Service restoration did not restore responsiveness sufficiently to proceed.
- `inconclusive` (observer=site_or_remote; tool=WCS/SSMS (read-only) / GetAgvStatuses (API-backed)): Responsiveness appears partially restored but verification results are unclear (e.g., transient success or schema warnings without clear operational meaning).

**Branches:**

- `healthy` → `node_3` when Restoration validated enough to correct AGVs
- `unhealthy` → `node_1` when Restoration insufficient

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

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

### 3 — Correct out-of-sync AGVs in RMS after service restoration (`procedure_reference`)

**Intent:** Use RMS to locate and correct AGVs that are out of sync so motion and small sort can resume.

**Expects capability:** device_roster_state, agv_active_errors, robot_command_or_task_state
**Expects surface:** rms_ui
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (low, support, score=0.7424, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_ui_confirm_rms_up_v1` (low, support, score=0.3245, boosted=0.2745) — Check RMS fleet status UI to confirm RMS is up and running
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Retrieval score 0.3245 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): RMS out-of-sync corrections applied and AGVs resume stable operation without the out-of-sync symptom.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): RMS corrections do not clear the out-of-sync condition or RMS remains abnormal/unresponsive.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI + WCS/SSMS (read-only) optional): RMS corrections are applied but evidence of outcome is ambiguous (some AGVs corrected, others unclear).

**Branches:**

- `healthy` → `node_4` when Out-of-sync corrections successful
- `unhealthy` → `node_2` when Corrections ineffective / RMS abnormal

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (2)</summary>

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

### 4 — Validate responsiveness and that AGVs are no longer in active error/out-of-sync state (`validation_gate`)

**Intent:** Confirm that the system is stable after restoration and RMS corrections by validating OptiSweep responsiveness and checking AGV active errors/state.

**Expects capability:** agv_active_errors, fleet_system_status, wcs_api_responsiveness, gateway_health
**Expects surface:** rms_ui, wcs_sql, ignition_gateway, wcs_api
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6225, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.6996, boosted=1.065) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1` (low, support, score=0.7748, boosted=1.335) — Corroborate AGV Active Errors Using AGV Active Error Database Model + Error Code Dictionary + Sort GUID
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=GetAgvStatuses (API-backed) + WCS/SSMS (read-only) + RMS / AGV status UI): Recovery is stable: OptiSweep API responsiveness is good and AGVs are no longer in active error/out-of-sync state.
- `unhealthy` (observer=site_or_remote; tool=GetAgvStatuses (API-backed) + WCS/SSMS (read-only) + RMS / AGV status UI): Recovery incomplete: API/service responsiveness fails or active error evidence persists and/or RMS remains blank/error-like.
- `inconclusive` (observer=site_or_remote; tool=GetAgvStatuses (API-backed) + WCS/SSMS (read-only) + RMS / AGV status UI): Validation signals are mixed (e.g., API reachable but semantics unclear; RMS shows partial clearing).

**Branches:**

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

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `healthy` | Incident-supported stoppage pattern confirmed | `node_2` |
| `node_1` | `unhealthy` | No corroboration / conflicting evidence | `` |
| `node_2` | `healthy` | Restoration validated enough to correct AGVs | `node_3` |
| `node_2` | `unhealthy` | Restoration insufficient | `node_1` |
| `node_3` | `healthy` | Out-of-sync corrections successful | `node_4` |
| `node_3` | `unhealthy` | Corrections ineffective / RMS abnormal | `node_2` |
| `node_4` | `healthy` | Recovery validation criteria are met | `` |

## Unresolved / Low-Confidence Links

- node_1: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_3: proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1 (low)
- node_3: proc_check_rms_fleet_status_ui_confirm_rms_up_v1 (low)
- node_4: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_4: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_4: proc_corroborate_agv_active_errors_using_agv_active_error_db_model_error_code_dictionary_sort_guid_v1 (low)
