# Hospital-area HMI fault with tote or stuck-task visibility concern

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_218550_hospital_hmi_fault` |
| Case ID | `218550` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital-area HMI is showing a fault.
- Site asks whether the HMI should be unplugged.
- A tote or task issue appears to be visible only on that HMI.
- Acknowledge and retry behavior is discussed as the immediate recovery action.
- A stuck task is reported as visible only on that HMI.

## Affected Systems

- Hospital HMI / lane UI
- HMI
- tote/task visibility context

## Nodes

### 1 — Confirm the reported HMI fault matches the hospital-area tote or task pattern (`diagnostic_decision`)

**Intent:** Determine whether the issue is specifically a hospital-area HMI fault with tote or task visibility concerns, rather than a general bag-out or fleet-state issue.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6098, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.6852, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.7123, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=hospital Hmi / lane UI): HMI-localized pattern confirmed: hospital-area HMI shows a fault and the tote/task visibility concern is tied to that HMI (not general bag-out/fleet outage).
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): Mismatch: the reported symptom is not localized to the hospital-area HMI (e.g., broader bag-out/fleet/system issue).
- `inconclusive` (observer=site_or_remote; tool=hospital Hmi / lane UI): Cannot confirm the HMI fault presentation due to unreadable fault text or insufficient evidence.
- `escalate` (observer=remote; tool=hospital Hmi / lane UI): Unclear/unsafe scenario: cannot verify fault state or localization and site requests unsafe action (e.g., unplug decision) without sufficient info.

**Branches:**

- `healthy` → `node_2` when Confirmed hospital-area HMI fault or tote/task visible on that HMI
- `unhealthy` → `` when HMI fault pattern not matched

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

### 2 — Use the approved HMI fault recovery path instead of unplugging the HMI (`procedure_reference`)

**Intent:** Apply the supported HMI recovery action for this fault presentation and avoid unsupported power-disconnect behavior.

**Runbook Links:**

- `proc_automatically_reference_all_tipper_axes_from_the_hmi_v1` (low, support, score=0.6018, boosted=0.814) — Automatically reference all tipper axes from the HMI
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=hospital Hmi / lane UI): Approved HMI recovery completed: HMI remains connected (no unplug action) and retry/acknowledge has been performed.
- `unhealthy` (observer=site_or_remote; tool=hospital Hmi / lane UI): Recovery not completed: acknowledge-and-retry cannot be performed or the fault persists immediately after retry.
- `inconclusive` (observer=site_or_remote; tool=hospital Hmi / lane UI): Acknowledged but uncertain outcome (e.g., fault state unclear or site cannot yet confirm retry effect).

**Branches:**

- `healthy` → `node_3` when Approved HMI recovery action completed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Automatically reference all tipper axes from the HMI (`proc_automatically_reference_all_tipper_axes_from_the_hmi_v1`)</summary>

##### Runbook: Automatically reference all tipper axes from the HMI

- **Procedure ID:** `proc_automatically_reference_all_tipper_axes_from_the_hmi_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the operator station HMI controls to automatically reference all tipper axes, confirm completion by verifying the reference status indicators show green "R" icons, then return the system to AUTO and restart operation.

**When To Use:**
Use this procedure when tipper axes need to be automatically referenced from the HMI and the system must be returned to operation after referencing completes.

**Safety Notes:**

- Do not continue to AUTO and CYCLE START until referencing is completed and the "R" icons have turned green.
- The surrounding maintenance note states that a tipper needs to be re-commissioned after any part is replaced.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Press RESET

**Responsible role:** L2_support

**Instruction:**
Press RESET on the HMI or operator controls.

**Healthy condition:**
RESET is pressed and the procedure can continue to AUTO REF.

**Expected result:**
The system accepts the reset input so the automatic referencing sequence can proceed.

**Step Images:**

![artifact_page_103_image_2](assets/8caf84ff57cdad0a.jpeg)

*Operator station HMI/operator controls associated with the referencing procedure context.*

---

###### Step 2 — Start automatic axis referencing

**Responsible role:** L2_support

**Instruction:**
Press AUTO REF to reference all of the axes of the tippers.

**Healthy condition:**
Automatic referencing starts for all tipper axes.

**Expected result:**
The system begins automatically referencing all tipper axes.

**Step Images:**

![artifact_page_103_image_2](assets/8caf84ff57cdad0a.jpeg)

*HMI/operator station screen area used for axis referencing controls, including AUTO REF.*

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Nearby startup context mentioning homing axes using AUTO REF.*

---

###### Step 3 — Verify referencing completion

**Responsible role:** L2_support

**Instruction:**
Verify that the "R" icons turn green to confirm referencing is completed.

**Healthy condition:**
All required "R" icons are green.

**Expected result:**
The reference status indicators show green "R" icons, confirming referencing is complete.

**Step Images:**

![artifact_page_103_image_2](assets/8caf84ff57cdad0a.jpeg)

*Axis reference status indicators on the operator station HMI; confirm the 'R' icons are green.*

![artifact_page_103_image_3](assets/8ec7e8899bc0ced7.png)

*Operator station HMI view associated with nearby axis referencing context; look for the reference status indicators and green 'R' icons.*

---

###### Step 4 — Return the system to AUTO

**Responsible role:** L2_support

**Instruction:**
When referencing is completed, press AUTO.

**Healthy condition:**
AUTO is selected only after referencing completion has been confirmed.

**Expected result:**
The system is returned to AUTO mode.

**Step Images:**

![artifact_page_86_image_13](assets/52c4e0c6458d0b6f.png)

*Operator station controls associated with AUTO mode selection.*

![artifact_page_103_image_2](assets/8caf84ff57cdad0a.jpeg)

*Operator station HMI/operator controls used to continue from referencing completion to AUTO.*

---

###### Step 5 — Restart operation

**Responsible role:** L2_support

**Instruction:**
Press CYCLE START to restart operation.

**Healthy condition:**
The system restarts operation after AUTO has been selected and referencing has completed.

**Expected result:**
Operation restarts after CYCLE START is pressed.

**Step Images:**

![artifact_page_86_image_13](assets/52c4e0c6458d0b6f.png)

*Operator station controls associated with CYCLE START.*

![artifact_page_103_image_2](assets/8caf84ff57cdad0a.jpeg)

*Operator station HMI/operator controls used to restart operation after referencing.*

---

**Success Criteria:**

- All tipper axes are referenced.
- The "R" icons are green.
- The system is returned to AUTO.
- Operation restarts after CYCLE START is pressed.

**Failure Conditions:**

- The system does not accept RESET or AUTO REF.
- The "R" icons do not turn green.
- Referencing completion cannot be confirmed.
- AUTO or CYCLE START cannot be performed successfully.
- Operation does not restart after CYCLE START is pressed.


</details>

</details>

---

### 3 — Validate that the HMI fault and tote or task condition cleared (`validation_gate`)

**Intent:** Confirm that the HMI fault is no longer blocking operation and that the tote or task condition associated with the screen has cleared.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, hospital_hmi, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6124, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_state_on_aveva_api_page_v1` (high, support, score=0.6419, boosted=1.0) — Check Overall System state on the AVEVA API page (System State / System Startup / Bag Out / Shutdown / Purge)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_diagnose_agv_exchange_backfill_gap_v1` (high, support, score=0.6279, boosted=1.0) — Diagnose AGV exchange/backfill gap when an AGV moves out without a replacement
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=hospital Hmi / lane UI): Recovered: hospital HMI fault is cleared and tote/task condition is validated as normal.
- `unhealthy` (observer=site_or_remote; tool=hospital Hmi / lane UI): Validation failed: HMI fault persists and/or the tote/task issue remains visible on that HMI.
- `inconclusive` (observer=site_or_remote; tool=hospital Hmi / lane UI): Cannot confirm clearance due to unclear screen state or inability to correlate the tote/task condition with the hospital HMI display.

**Branches:**

- `healthy` → `` when HMI fault cleared and tote/task condition validated as normal
- `unhealthy` → `node_4` when HMI fault persists or tote/task issue remains after recovery

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

<details><summary>Diagnose AGV exchange/backfill gap when an AGV moves out without a replacement (`proc_diagnose_agv_exchange_backfill_gap_v1`)</summary>

##### Runbook: Diagnose AGV exchange/backfill gap when an AGV moves out without a replacement

- **Procedure ID:** `proc_diagnose_agv_exchange_backfill_gap_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Diagnose why a front AGV moved out without a replacement/backfill by checking (1) whether the trailing AGV had a fault (including the case where it was reported ready for a new task and faulted at the same time) and (2) whether chute closure/fullness and exchange timing targets indicate exchanges were not completed before chute closure.

**When To Use:**
Use when you observe or are told that an AGV moved out without another AGV backfilling/replacing it during an exchange, and you need live evidence to confirm whether the trailing AGV fault/ready+fault timing and/or chute fullness/closure and exchange timing targets contributed.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI and identify the AGV pair for the exchange event

**Responsible role:** L2_support

**Instruction:**
Using the RMS / fleet status UI (rms_ui), locate the AGV pair involved in the exchange event: the AGV that moved out (front) and the AGV that should have backfilled (trailing).

**Healthy condition:**
The RMS view clearly shows the relevant AGVs and their status/error context for the exchange event you are investigating.

**Expected result:**
You have identified the specific trailing AGV associated with the exchange event time window (so you can check whether it faulted when the front AGV moved out).

---

###### Step 2 — Check trailing AGV status for fault at the time the front AGV moved out

**Responsible role:** L2_support

**Instruction:**
In RMS / fleet status UI (rms_ui), check the trailing (behind) AGV’s status/error indicators around the time the front AGV moved out. Confirm whether the trailing AGV is faulted, or shows a fault coincident with being reported ready for a new task.

**Healthy condition:**
Trailing AGV shows no fault at the relevant time (or fault timing does not coincide with the front AGV move-out), suggesting the gap may be explained by other factors (e.g., chute fullness/exchange timing).

**Expected result:**
You find live evidence that the trailing AGV had an active fault at (or coincident with) the time the front AGV moved out, consistent with the described pairing/backfill failure mechanism.

---

###### Step 3 — If RMS is inconclusive, query WCS / Helix DB (SSMS) for trailing AGV fault/backfill failure evidence

**Responsible role:** L2_support

**Instruction:**
Using WCS / Helix DB (SSMS) (wcs_sql), query the OptiSweep DB for the same time window to find evidence of a fault/backfill failure for the trailing AGV (e.g., AGV state/error records).

**Healthy condition:**
Database records show no fault/backfill failure for the trailing AGV in the relevant time window, shifting focus to chute fullness/closure and exchange timing.

**Expected result:**
You identify live database evidence that the trailing AGV faulted (or otherwise failed to support backfill) during the exchange window corresponding to the front AGV move-out.

---

###### Step 4 — Check chute fullness/closure and exchange timing targets around the event

**Responsible role:** L2_support

**Instruction:**
Using WCS / Helix DB (SSMS) (wcs_sql), review live system data available for chute fullness and exchange timing metrics around the event time window. Look for conditions consistent with chute closure when the chute is full and exchange not completing before the 80% threshold (with exchange timing deviating from the median ~8 seconds and floor ~6.7 seconds).

**Healthy condition:**
Chute fullness/closure did not occur before exchanges completed, and exchange timing aligns with the described targets (median ~8s, floor ~6.7s).

**Expected result:**
You find live evidence that chute fullness/closure occurred (or was imminent) such that exchanges were not completed before the 80% threshold, and/or exchange timing deviated from the described targets (median ~8s, floor ~6.7s).

---

###### Step 5 — Stop and escalate based on confirmed evidence (or lack of evidence)

**Responsible role:** L2_support

**Instruction:**
Based on your findings from RMS and WCS/Helix DB, decide whether to escalate. Escalate when you confirm the trailing AGV fault/ready+fault timing mechanism or confirm chute fullness/insufficient exchange timing mechanism, or when you cannot confirm either mechanism with live evidence.

**Healthy condition:**
Evidence supports one or both mechanisms described (trailing AGV fault timing and/or fullness-driven chute closure with exchange timing deviation).

**Expected result:**
A clear diagnostic conclusion is produced: (1) trailing AGV fault/ready+fault timing explains the missing backfill, and/or (2) chute fullness/closure and exchange timing targets indicate exchanges were not completed before 80%. If neither is supported by live evidence, escalation occurs due to unconfirmed cause.

---

**Success Criteria:**

- You confirm (with live RMS and/or WCS/Helix DB evidence) that the trailing AGV fault/ready+fault timing explains why the front AGV moved out without replacement/backfill.
- OR you confirm (with live WCS/Helix DB evidence) that chute fullness/closure occurred such that exchanges were not completed before the 80% threshold, with exchange timing deviating from the described targets (median ~8s, floor ~6.7s).
- If neither mechanism is supported by live evidence, you escalate rather than assuming the cause.

**Failure Conditions:**

- Trailing AGV fault/ready+fault timing is present at the time the front AGV moved out, consistent with missing backfill.
- Chute fullness/closure occurs (or is imminent) such that exchanges were not completed before reaching 80%, with exchange timing deviating from median ~8s and floor ~6.7s.
- RMS and WCS/Helix DB show no trailing AGV fault/backfill failure evidence and no chute fullness/exchange timing evidence consistent with the described mechanisms.


</details>

</details>

---

### 4 — Escalate if the HMI fault persists or a stuck-task path is needed beyond supported recovery (`escalation_gate`)

**Intent:** Stop and escalate when acknowledge-and-retry does not clear the HMI fault or when the issue appears to require deeper stuck-task identification or unsupported HMI changes.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=hospital Hmi / lane UI): Non-escalation: the issue clears and validation succeeds.
- `unhealthy` (observer=remote; tool=hospital Hmi / lane UI): Escalate: HMI fault persists or stuck-task recovery beyond supported path is needed.
- `inconclusive` (observer=site_or_remote; tool=hospital Hmi / lane UI): Escalation pending clarification: evidence is incomplete (cannot capture readable fault text; tote/task localization uncertain).

**Branches:**

- `unhealthy` → `` when Escalation condition met (fault persists / deeper stuck-task path needed)

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `healthy` | Confirmed hospital-area HMI fault or tote/task visible on that HMI | `node_2` |
| `node_1` | `unhealthy` | HMI fault pattern not matched | `` |
| `node_2` | `healthy` | Approved HMI recovery action completed | `node_3` |
| `node_3` | `healthy` | HMI fault cleared and tote/task condition validated as normal | `` |
| `node_3` | `unhealthy` | HMI fault persists or tote/task issue remains after recovery | `node_4` |
| `node_4` | `unhealthy` | Escalation condition met (fault persists / deeper stuck-task path needed) | `` |

## Unresolved / Low-Confidence Links

- node_2: proc_automatically_reference_all_tipper_axes_from_the_hmi_v1 (low)
- node_4: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
