# Hospital station cannot add or induct totes

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_restore` |
| Case ID | `223554` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital station unable to induct totes
- Site can remove totes but cannot add totes at the hospital
- Robot reported in a shut down state at the hospital station
- Hospital lane or hospital station reported as down or unable to start normal sort flow
- Original issue described as inability to add and remove totes correctly, later narrowed to add/induct failure

## Affected Systems

- ACB hospital station
- AGV hospital station
- Opti sweep services
- Hospital Lane
- robots/AGVs

## Nodes

### 1 — Confirm hospital tote-induction failure pattern (`diagnostic_decision`)

**Intent:** Determine whether the reported issue matches the reusable pattern of hospital station unable to add or induct totes, with possible broader hospital lane disruption.

**Expects capability:** hospital_diversion
**Expects surface:** hospital_hmi
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital tote-induction failure pattern confirmed (add/induct not working) while evidence on Hospital HMI indicates the station is in an abnormal/down/shut-down presentation consistent with the report.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital tote-induction pattern not confirmed; the issue appears unrelated to hospital-station add/induct behavior.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital pattern could not be confirmed due to limited information or inconsistent UI evidence.

**Branches:**

- `healthy` → `node_2` when Pattern confirmed (cannot add/induct; lane/station down/shut down language present)
- `unhealthy` → `node_7` when Pattern not confirmed

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Check for AGV hospital station server or service abnormality (`diagnostic_decision`)

**Intent:** Determine whether the incident matches the source-supported pattern of AGV hospital station server issues or service abnormality that may justify approved service recovery.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6174, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7364, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.709, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=WCS/SSMS (read-only) / AVEVA API view via WCS SQL-adjacent workflow): Supported abnormality indicated that justifies authorized service recovery (overall system state/services appear abnormal or not in expected running state).
- `unhealthy` (observer=remote; tool=WCS/SSMS (read-only) / AVEVA API view): No supported service abnormality found; do not assume service reset is the next step.
- `inconclusive` (observer=remote; tool=WCS/SSMS (read-only) / AVEVA API view): Evidence insufficient to confidently decide service recovery path.

**Branches:**

- `healthy` → `node_3` when Abnormal service/server pattern indicated
- `unhealthy` → `node_7` when No supported service abnormality found / inconclusive

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

### 3 — Perform approved service recovery for hospital-station services (`procedure_reference`)

**Intent:** Carry out the authorized recovery procedure for the affected Opti sweep or related hospital-station services when the abnormal service pattern is confirmed.

**Runbook Links:**

- `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (medium, support, score=0.6184, boosted=0.7884) — Recover an AGV That Lost a Tote Without Faulting
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=WCS/SSMS (read-only) / OptiSweep service response checks): Approved service recovery completed and evidence shows service response restored.
- `unhealthy` (observer=site_or_remote; tool=WCS/SSMS (read-only) / OptiSweep service response checks): Authorized recovery attempt does not restore expected service behavior.
- `inconclusive` (observer=site_or_remote; tool=WCS/SSMS (read-only) / OptiSweep service response checks): Recovery was initiated but evidence is unclear (partial restoration or intermittent checks).

**Branches:**

- `healthy` → `node_4` when Service recovery completed

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

### 4 — Have site perform approved Hospital Lane restart (`procedure_reference`)

**Intent:** Use the approved site-facing recovery procedure to restart Hospital Lane after service recovery when that step is authorized and required.

**Runbook Links:**

- `proc_recover_empty_agvs_that_lost_tasks_after_rms_restart_v1` (low, support, score=0.5538, boosted=0.7693) — Recover Empty AGVs That Lost Tasks After an RMS Restart
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=site; tool=Hospital HMI / lane UI): Hospital Lane restart completed and lane is ready for tote-induction validation.
- `unhealthy` (observer=site; tool=Hospital HMI / lane UI): Hospital Lane restart fails or does not return to operational readiness.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Restart attempted but lane readiness cannot be confirmed yet.

**Branches:**

- `inconclusive` → `node_5` when Hospital Lane restart completed

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

### 5 — Validate hospital tote add and remove behavior (`validation_gate`)

**Intent:** Confirm that the original hospital-station symptom is resolved after recovery.

**Expects capability:** hospital_diversion
**Expects surface:** hospital_hmi
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_identify_why_a_tote_was_sent_to_the_hospital_station_v1` (medium, operator, score=0.6357, boosted=0.8057) — Identify Why A Tote Was Sent To The Hospital Station
  - gaps: Limited domain-term overlap between placeholder and runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital tote add and remove behavior restored and station/lane no longer presents as down/shut down.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Validation fails: add/induct behavior remains broken after recovery.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Partial restoration or inconsistent results.

**Branches:**

- `healthy` → `node_7` when Tote add and remove restored
- `unhealthy` → `node_7` when Still failing after recovery

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

<details><summary>Identify Why A Tote Was Sent To The Hospital Station (`proc_identify_why_a_tote_was_sent_to_the_hospital_station_v1`)</summary>

##### Runbook: Identify Why A Tote Was Sent To The Hospital Station

- **Procedure ID:** `proc_identify_why_a_tote_was_sent_to_the_hospital_station_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the hospital station stacklight and green scanner to confirm a tote is present and determine the reason it was brought to the hospital station.

**When To Use:**
Use this procedure when a tote has been sent to the hospital station and the operator needs to confirm tote presence and determine why the tote was brought there for manual handling.

**Safety Notes:**

- The source states the tote is manually handled by an operator at the hospital station.
- Do not invent or apply unsupported follow-up handling steps, scanner interpretations, or controls not described in the source.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Go to the hospital station and check for tote presence indication

**Responsible role:** operator

**Instruction:**
Go to the hospital station and observe the station indication that shows a tote is present.

**Healthy condition:**
A tote-present indication is observed at the hospital station.

**Expected result:**
The operator identifies whether the station indicates a tote is present.

**Step Images:**

![artifact_fig_3_5_hospital_station](assets/e6eaf45fdaa4c26f.png)

*Use the hospital station photo to identify the station and its stacklight context.*

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Use the hospital station operation artifact as supporting visual context for hospital station tote handling.*

---

###### Step 2 — Confirm the tote is on the operator-right side of the hospital station

**Responsible role:** operator

**Instruction:**
Confirm the AGV has brought the tote to the right side of the hospital station from the operator's perspective.

**Healthy condition:**
The tote is present on the right side of the hospital station from the operator's perspective.

**Expected result:**
The operator confirms the tote is positioned on the right side of the hospital station.

**Step Images:**

![artifact_page_92_image_2](assets/ef35eabc75ef8254.png)

*Use the hospital station operation artifact for visual context on AGV tote delivery and station sides.*

---

###### Step 3 — Use the green scanner to determine the reason for hospital station routing

**Responsible role:** operator

**Instruction:**
Use the green scanner at the hospital station to determine the reason the tote was brought to the station.

**Healthy condition:**
A reason for the tote being sent to the hospital station is obtained using the green scanner.

**Expected result:**
The scanner provides the reason the tote was brought to the hospital station.

**Step Images:**

![artifact_fig_4_33_hospital_hmi_no_read_bar_code_screen](assets/ade215aeb0f38448.png)

*Use as an example of a hospital station exception screen related to a no-read barcode condition.*

![artifact_fig_4_34_hospital_hmi_bar_code_mismatch_screen](assets/cc4e50eeac8e7240.png)

*Use as an example of a hospital station exception screen related to barcode mismatch.*

![artifact_fig_4_35_hospital_hmi_tote_failed_to_empty_screen](assets/6cfcf13257c66c75.png)

*Use as an example of a hospital station exception screen related to tote failed to empty.*

![artifact_fig_4_36_hospital_hmi_sent_from_bagging_station_screen](assets/1612450530188bc6.png)

*Use as an example of a hospital station screen associated with a sent-from-bagging-station condition.*

---

###### Step 4 — Record or communicate the reported reason

**Responsible role:** operator

**Instruction:**
Record or communicate the reason reported by the scanner for manual handling of the tote.

**Healthy condition:**
The scanner-reported reason is clearly recorded or communicated.

**Expected result:**
The reason is captured or communicated for the next action outside this runbook.

---

**Success Criteria:**

- The operator confirms a tote is present at the hospital station.
- The operator confirms the tote is on the right side of the hospital station from the operator's perspective.
- The operator determines the reason the tote was brought to the hospital station using the green scanner.
- The reason is recorded or communicated for manual handling.

**Failure Conditions:**

- The hospital station does not indicate a tote is present when expected.
- The tote is not on the expected side of the hospital station.
- The green scanner does not provide a reason.
- The source does not provide enough detail to continue with interpretation or follow-up handling.


</details>

</details>

---

### 6 — Check for residual AGV or tote inconsistencies after hospital recovery (`branching_condition`)

**Intent:** Determine whether the original hospital issue is resolved but residual AGV/tote state problems still need separate cleanup.

**Expects capability:** device_roster_state, fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.5907, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7397, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.7131, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI and related RMS views): No residual AGV/tote inconsistencies indicated; hospital recovery flow can end.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI and related RMS views): Residual AGV or tote inconsistencies indicated; separate cleanup may be required after hospital recovery.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Cannot confidently determine residual consistency due to incomplete evidence or ambiguous RMS data.

**Branches:**

- `unhealthy` → `` when Residual inconsistency indicated
- `healthy` → `` when No residual inconsistency indicated

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

### 7 — Escalate if supported hospital recovery path is not identified or validation fails (`escalation_gate`)

**Intent:** Stop and escalate when the symptom pattern is matched but the available evidence does not support a safe authorized recovery path, or when recovery does not restore hospital tote induction.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=Hospital HMI / lane UI + RMS / WCS views as needed for evidence): Escalation required: supported recovery path not identified or validation fails to restore tote induction.
- `inconclusive` (observer=remote; tool=Hospital HMI / lane UI + RMS / WCS views): Evidence gathered but still insufficient; continue collecting artifacts/observations prior to escalation.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `healthy` | Pattern confirmed (cannot add/induct; lane/station down/shut down language present) | `node_2` |
| `node_1` | `unhealthy` | Pattern not confirmed | `node_7` |
| `node_2` | `healthy` | Abnormal service/server pattern indicated | `node_3` |
| `node_2` | `unhealthy` | No supported service abnormality found / inconclusive | `node_7` |
| `node_3` | `healthy` | Service recovery completed | `node_4` |
| `node_4` | `inconclusive` | Hospital Lane restart completed | `node_5` |
| `node_5` | `healthy` | Tote add and remove restored | `node_7` |
| `node_5` | `unhealthy` | Still failing after recovery | `node_7` |
| `node_6` | `unhealthy` | Residual inconsistency indicated | `` |
| `node_6` | `healthy` | No residual inconsistency indicated | `` |

## Unresolved / Low-Confidence Links

- node_1: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_4: proc_recover_empty_agvs_that_lost_tasks_after_rms_restart_v1 (low)
- node_6: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_7: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
