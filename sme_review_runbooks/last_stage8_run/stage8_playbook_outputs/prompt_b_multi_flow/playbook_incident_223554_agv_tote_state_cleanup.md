# Hospital flow blocked by AGV or tote state inconsistency

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_agv_tote_state_cleanup` |
| Case ID | `223554` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- AGV does not belong in the shown location
- Two AGVs under the rack in the same zone
- Disconnected tote remains in the system
- Hospital is backed up while AGVs are picking tasks from abnormal positions
- Robots need to be taken out and later re-added to restore operation

## Affected Systems

- robots/AGVs
- RMS / fleet status
- ACB hospital station
- AGV hospital station

## Nodes

### 1 — Confirm AGV or tote inconsistency pattern (`diagnostic_decision`)

**Intent:** Determine whether the reported issue matches the reusable pattern of abnormal AGV placement, disconnected tote state, or hospital backup caused by AGV/tote inconsistency.

**Expects capability:** device_roster_state, fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.626, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_click_dark_blue_rack_in_rms_view_associated_tote_v1` (high, support, score=0.7789, boosted=1.0) — Click a dark blue rack in RMS to view which tote is associated to that rack
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.797, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): An inconsistency pattern is observed that matches abnormal AGV placement and/or a tote record inconsistency (e.g., AGV in wrong location, multiple AGVs in same under-rack area, tote indicates disconnected/remaining state).
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): RMS evidence is incomplete or unclear for whether the reported symptom is actually the reusable AGV/tote inconsistency pattern.
- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): No repeatable AGV/tote inconsistency pattern is confirmed.

**Branches:**

- `unhealthy` → `node_2` when Confirmed abnormal AGV placement/tote disconnection/hospital backup tied to AGV/tote inconsistency
- `inconclusive` → `node_7` when Pattern not confirmed

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

<details><summary>Click a dark blue rack in RMS to view which tote is associated to that rack (`proc_click_dark_blue_rack_in_rms_view_associated_tote_v1`)</summary>

##### Runbook: Click a dark blue rack in RMS to view which tote is associated to that rack

- **Procedure ID:** `proc_click_dark_blue_rack_in_rms_view_associated_tote_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI map to verify which tote number is currently associated with a specific rack location. Dark blue/violet rack locations indicate a tote is present; clicking the rack reveals the tote number so you can compare it to the expected tote for that rack position and detect mismatches.

**When To Use:**
When you need to confirm the tote number RMS shows for a particular rack position (e.g., to validate whether the correct tote is on the expected sorter destination rack).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI and locate the rack position to verify

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (map view) and find the rack location you want to verify.

**Healthy condition:**
The target rack location is visible and has a color state you can distinguish (dark blue/violet vs lighter blue).

**Expected result:**
You can visually identify the target rack location on the RMS map.

---

###### Step 2 — Confirm the rack is dark blue/violet (tote present)

**Responsible role:** L1_support

**Instruction:**
Confirm the rack location color is dark blue (almost like a violet).

**Healthy condition:**
Dark blue/violet rack tone is present (tote present).

**Expected result:**
The rack location you plan to click is dark blue/violet, indicating a tote is on that rack.

---

###### Step 3 — Click the dark blue rack location on the RMS map

**Responsible role:** L1_support

**Instruction:**
Click the dark blue rack location on the RMS map.

**Healthy condition:**
After clicking, a tote number/identifier is displayed for that rack.

**Expected result:**
RMS updates to show the tote identifier/number associated with the clicked rack.

---

###### Step 4 — Read the tote number shown for the clicked rack

**Responsible role:** L1_support

**Instruction:**
Observe the tote identifier/number displayed for that rack after clicking.

**Healthy condition:**
The tote number/identifier is readable and corresponds to the clicked rack location.

**Expected result:**
A tote number/identifier is visible in RMS for the clicked rack.

---

###### Step 5 — Compare displayed tote number to expected tote number for that rack position

**Responsible role:** L1_support

**Instruction:**
Compare the tote number displayed in RMS to the expected tote number for that rack position (for example, if someone reports tote HV 110 but RMS shows 113).

**Healthy condition:**
Displayed tote number matches the expected tote number for that rack position.

**Expected result:**
You determine whether the displayed tote number matches or mismatches the expected tote number for the rack position.

---

**Success Criteria:**

- RMS shows a tote number after clicking the dark blue/violet rack location.
- The displayed tote number matches the expected tote number for the rack position (or you escalate when it does not).

**Failure Conditions:**

- Rack is not dark blue/violet (appears light blue indicating empty) when you expect a tote.
- After clicking, RMS does not display a tote number/identifier for the rack.
- Displayed tote number does not match the expected tote number for the rack position.


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

### 2 — Determine whether the issue is a disconnected tote record or abnormal AGV placement (`branching_condition`)

**Intent:** Choose the supported cleanup direction based on whether the dominant abnormality is tote-association inconsistency, AGV placement inconsistency, or both.

**Expects capability:** device_roster_state, fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Disconnected/inducted tote record problem is indicated as the dominant issue.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Abnormal AGV placement/roster inconsistency is indicated as the dominant issue.
- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Neither supported cleanup path can be justified by evidence.

**Branches:**

- `unhealthy` → `node_3` when Disconnected tote / inducted-tote record indicated
- `unhealthy` → `node_4` when Abnormal AGV placement / roster inconsistency indicated
- `escalate` → `node_7` when Neither supported cleanup path is supported by evidence

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 3 — Perform approved tote-state cleanup (`procedure_reference`)

**Intent:** Use the authorized tote cleanup procedure when a disconnected or inducted tote record is blocking recovery.

**Runbook Links:**

- `proc_recover_empty_agvs_that_lost_tasks_after_rms_restart_v1` (medium, support, score=0.6412, boosted=0.8567) — Recover Empty AGVs That Lost Tasks After an RMS Restart
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Tote-state cleanup completed and the inconsistency is cleared enough for movement to resume.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Tote-state cleanup did not clear the blocking condition.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Cleanup executed but evidence of correction cannot be confirmed within RMS views available.

**Branches:**

- `healthy` → `node_5` when Tote-state cleanup completed
- `unhealthy` → `node_7` when Tote-state cleanup not effective

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Recover Empty AGVs That Lost Tasks After an RMS Restart (`proc_recover_empty_agvs_that_lost_tasks_after_rms_restart_v1`)</summary>

##### Runbook: Recover Empty AGVs That Lost Tasks After an RMS Restart

- **Procedure ID:** `proc_recover_empty_agvs_that_lost_tasks_after_rms_restart_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Restore empty AGVs after task loss caused by an RMS restart by stopping RMS, removing and re-adding AGVs without totes twice using Tote API Controls, verifying the documented HMI state when restart is involved, and then resuming RMS using the documented start procedure.

**When To Use:**
Use when empty AGVs have lost their tasks because the RMS was restarted.

**Safety Notes:**

- This procedure includes E-stop use and system recovery actions.
- If the system needs to be restarted, make sure the AGVs are in the "szonestaging" state.
- The manual notes that the best practice is to shut down and restart to ensure everything is in sync.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop RMS

**Responsible role:** L2_support

**Instruction:**
E-stop RMS.

**Healthy condition:**
RMS is in the E-stopped/stopped condition required by the recovery procedure.

**Expected result:**
RMS is stopped so AGV recovery actions can be performed.

---

###### Step 2 — Remove and re-add empty AGVs twice

**Responsible role:** L2_support

**Instruction:**
Remove and re-add AGVs without totes twice using the Tote API Controls referenced by the manual.

**Healthy condition:**
AGVs without totes have completed the documented remove/re-add cycle twice.

**Expected result:**
The affected empty AGVs have been removed and re-added twice through the documented controls.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*AGV API Controls for Remove AGV and Recover AGV functions used to remove and add AGVs back into the system.*

---

###### Step 3 — Verify AGVs are in "szonestaging" before restart-related actions

**Responsible role:** L2_support

**Instruction:**
If the system is to be restarted, verify on the HMI that the AGVs are in the "szonestaging" state.

**Healthy condition:**
Affected AGVs display the "szonestaging" state on the HMI.

**Expected result:**
The AGV state shown on the HMI is confirmed as "szonestaging" when restart-related actions are needed.

**Step Images:**

![artifact_fig_5_3_add_agv_to_zone_with_no_empty_agv_screen](assets/ec83d895fff08cd8.jpeg)

*The recovery screen context associated with verifying AGV status is "szonestaging" on the HMI.*

---

###### Step 4 — Press the E-stop again when ready to resume

**Responsible role:** L2_support

**Instruction:**
Press the E-stop again when ready to resume.

**Healthy condition:**
The procedure is positioned to proceed to RMS resume per the manual sequence.

**Expected result:**
The documented pre-resume E-stop action has been completed.

---

###### Step 5 — Resume RMS using the documented start procedure

**Responsible role:** L2_support

**Instruction:**
Resume RMS using the documented system start procedure.

**Healthy condition:**
RMS resumes successfully after AGV recovery.

**Expected result:**
RMS is resumed using the referenced starting procedure.

**Step Images:**

![artifact_fig_5_1_system_in_shut_down_mode](assets/597651fff1a13999.jpeg)

*System shut-down/startup context associated with restarting and resuming the system.*

---

**Success Criteria:**

- Empty AGVs that lost tasks have been removed and re-added twice using Tote API Controls.
- When restart-related actions are involved, AGVs are verified on the HMI to be in the "szonestaging" state.
- RMS is resumed using the documented system start procedure.

**Failure Conditions:**

- RMS cannot be E-stopped or resumed as required.
- Affected AGVs cannot be removed and re-added twice.
- AGVs are not in the documented "szonestaging" state before restart-related actions.
- The required HMI state cannot be verified.
- System synchronization concerns remain after recovery actions.


</details>

</details>

---

### 4 — Perform approved AGV recovery or temporary removal (`procedure_reference`)

**Intent:** Use the authorized AGV recovery procedure when abnormal AGV placement or roster inconsistency is blocking recovery.

**Runbook Links:**

- `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (low, support, score=0.6957, boosted=0.9657) — Recover an AGV That Lost a Tote Without Faulting
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): AGV recovery/temporary removal completed and fleet can progress.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): AGV recovery/temporary removal did not clear the blocking placement/roster issue.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Removal action completed but RMS evidence cannot confirm which AGVs/placements remain problematic.

**Branches:**

- `healthy` → `node_5` when AGV recovery / temporary removal completed
- `unhealthy` → `node_7` when AGV recovery did not clear blocking condition

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

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

</details>

---

### 5 — Validate that movement and system operation resumed (`validation_gate`)

**Intent:** Confirm that the AGV/tote cleanup restored movement and that the system is back up.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6594, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1` (high, support, score=0.8004, boosted=1.0) — Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7936, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Recovery succeeded: movement resumes and system is running normally (hospital flow backup relieved enough to proceed).
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Validation fails: movement does not resume or system remains not running normally.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Movement appears to resume but full restoration of all robots may still be incomplete.

**Branches:**

- `healthy` → `node_7` when Movement resumed and system running
- `unhealthy` → `node_7` when Movement did not resume / system not running normally

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

### 6 — Perform approved AGV re-add or fleet restoration (`procedure_reference`)

**Intent:** Return corrected AGVs to normal running state after cleanup when the approved recovery path requires re-add.

**Runbook Links:**

- `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (low, support, score=0.6898, boosted=0.9598) — Recover an AGV That Lost a Tote Without Faulting
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1` (high, support, score=0.6822, boosted=0.9522) — Recover an AGV That Lost a Tote Without an AGV Fault
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (high, support, score=0.6309, boosted=0.9464) — Remove An AGV From The System Using The API Screen
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Fleet restoration completed: affected robots/AGVs are back up and in normal running state.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Re-add/restoration does not complete; robots remain unavailable or in inconsistent states.

**Branches:**

- `healthy` → `` when AGV re-add / fleet restoration completed
- `unhealthy` → `node_7` when Robots not fully restored

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

### 7 — Escalate if AGV or tote cleanup does not restore stable movement (`escalation_gate`)

**Intent:** Stop and escalate when the AGV/tote inconsistency pattern is confirmed but supported cleanup and restoration do not return the system to stable running state.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Supported cleanup and validation did not restore stable movement; escalate with RMS evidence of abnormal AGV placement/tote-state inconsistency and actions taken.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Movement status is ambiguous or evidence cannot be fully captured; request additional support/clarification while preparing what evidence is available.

**Branches:**

- `escalate` → `` when Cleanup/restore failed or unsupported by evidence/role

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Confirmed abnormal AGV placement/tote disconnection/hospital backup tied to AGV/tote inconsistency | `node_2` |
| `node_1` | `inconclusive` | Pattern not confirmed | `node_7` |
| `node_2` | `unhealthy` | Disconnected tote / inducted-tote record indicated | `node_3` |
| `node_2` | `unhealthy` | Abnormal AGV placement / roster inconsistency indicated | `node_4` |
| `node_2` | `escalate` | Neither supported cleanup path is supported by evidence | `node_7` |
| `node_3` | `healthy` | Tote-state cleanup completed | `node_5` |
| `node_3` | `unhealthy` | Tote-state cleanup not effective | `node_7` |
| `node_4` | `healthy` | AGV recovery / temporary removal completed | `node_5` |
| `node_4` | `unhealthy` | AGV recovery did not clear blocking condition | `node_7` |
| `node_5` | `healthy` | Movement resumed and system running | `node_7` |
| `node_5` | `unhealthy` | Movement did not resume / system not running normally | `node_7` |
| `node_6` | `healthy` | AGV re-add / fleet restoration completed | `` |
| `node_6` | `unhealthy` | Robots not fully restored | `node_7` |
| `node_7` | `escalate` | Cleanup/restore failed or unsupported by evidence/role | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_2: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_4: proc_recover_an_agv_that_lost_a_tote_without_faulting_v1 (low)
- node_6: proc_recover_an_agv_that_lost_a_tote_without_faulting_v1 (low)
- node_7: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
