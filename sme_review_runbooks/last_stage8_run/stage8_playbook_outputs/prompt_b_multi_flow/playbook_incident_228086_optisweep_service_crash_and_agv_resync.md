# Recover robotic control after OptiSweep service failure and resynchronize out-of-sync AGVs

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228086_optisweep_service_crash_and_agv_resync` |
| Case ID | `228086` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- “Nothing is moving” / site-wide motion stoppage
- “Robotic system is not responding”
- Small sort not running
- RMS/HMI shows an abnormal/blank state (e.g., message like “.NET Control not created.”)
- AGVs reported out of sync

## Affected Systems

- OptiSweep service
- AGVs / robotic system
- RMS / HMI (ACB System RMS / map monitor)
- Ignition gateway (as a dependency path to OptiSweep/API)
- WCSWebApplication (as observed in Event Viewer context)
- Windows Event Viewer / Service Control Manager
- OptiSweep / WCS API endpoint used for GetAgvStatuses

## Nodes

### 1 — Confirm the stoppage pattern and whether the control stack appears unhealthy (`diagnostic_decision`)

**Intent:** Determine whether the reported site-wide stoppage aligns with an unhealthy robotic control stack state that warrants OptiSweep service/gateway recovery and AGV resynchronization.

**Expects capability:** fleet_system_status, zone_pairing_state, agv_active_errors
**Expects surface:** rms_ui, event_viewer
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.611, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_screen_for_system_faults_first_step_v1` (low, support, score=0.7176, boosted=1.0) — Check RMS screen for system faults as the first step during an OptiSweep support call
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_verify_optsweep_wcs_windows_service_health_v1` (low, support, score=0.4054, boosted=0.3412) — Verify OptiSweep/WCS Windows service health when RMS/logs appear silent
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Site confirmation of motion stoppage is not supported by abnormal control evidence; RMS shows normal/operational state and no corroborating service/application failure pattern is found.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): Incident-evidenced unhealthy control-stack pattern is corroborated and recovery is warranted.
- `inconclusive` (observer=site_or_remote; tool=Windows Event Viewer / Services): Evidence is mixed or insufficient (e.g., RMS abnormal but service/application corroboration cannot be confirmed).
- `escalate` (observer=remote; tool=RMS / AGV status UI): Insufficient evidence and/or conflicting signals prevent safe continuation of this OptiSweep crash/resync flow.

**Branches:**

- `unhealthy` → `node_2` when Unhealthy control-stack pattern corroborated
- `inconclusive` → `node_2` when Pattern not fully confirmed

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

<details><summary>Check RMS screen for system faults as the first step during an OptiSweep support call (`proc_check_rms_screen_for_system_faults_first_step_v1`)</summary>

##### Runbook: Check RMS screen for system faults as the first step during an OptiSweep support call

- **Procedure ID:** `proc_check_rms_screen_for_system_faults_first_step_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
During an OptiSweep support call, check the RMS / fleet status UI first to determine whether any system faults are present. This quickly establishes whether the issue is likely fleet-wide/system-level before deeper diagnostics.

**When To Use:**
Use at the start of a support call to answer: “Are there any system faults?” and to decide whether to proceed with deeper diagnostics based on whether system faults are visible on the RMS screen.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS / fleet status UI (RMS screen) using the provided dashboard URL

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (RMS screen) using the provided RMS dashboard URL.

**Healthy condition:**
RMS screen is accessible and shows the system-fault area/list/status indicator.

**Expected result:**
The RMS screen loads and is ready to view system-fault indications.

---

###### Step 2 — Check the RMS screen for system-fault indications

**Responsible role:** L1_support

**Instruction:**
On the RMS screen, look for the system-faults area/list/status indicator (system faults shown on the left).

**Healthy condition:**
No system-fault indication is shown in the system-faults area/list/status on the RMS screen.

**Expected result:**
You can observe whether system faults are present (system-fault indications visible) or absent (no system-fault indication shown).

---

###### Step 3 — If system faults are present, record what is shown on the RMS screen

**Responsible role:** L1_support

**Instruction:**
Record the system-fault indicators shown on the RMS screen, including any visible fault identifiers/status text.

**Healthy condition:**
N/A (this step applies only when system faults are present).

**Expected result:**
A clear note exists describing the visible system-fault indicators and any fault identifiers/status text shown on the RMS screen.

---

###### Step 4 — If no system faults are present, record absence and proceed with further evidence gathering

**Responsible role:** L1_support

**Instruction:**
Record that the RMS screen shows no system-fault indication, then proceed with further evidence gathering (the segment does not specify which next surfaces/steps to use).

**Healthy condition:**
No system-fault indication is shown on the RMS screen.

**Expected result:**
A note exists stating that no system-fault indication is visible on the RMS screen.

---

**Success Criteria:**

- RMS / fleet status UI is opened successfully (or escalation is triggered if it cannot be accessed).
- System-fault presence/absence is observed on the RMS screen and recorded (including visible fault identifiers/status text when present).

**Failure Conditions:**

- RMS screen cannot be accessed or does not load (e.g., blank).
- System-fault indications are visible on the RMS screen.


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

### 2 — Recover the control stack path (Ignition gateway and/or OptiSweep service) when unhealthy (`procedure_reference`)

**Intent:** Perform the approved recovery action(s) to restore OptiSweep responsiveness and the dependent control path so AGVs can be resynchronized.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_start_optisweep_agv_system_from_shutdown_reset_metrics_start_closeout_running_v1` (medium, operator, score=0.5624, boosted=0.7324) — Start OptiSweep AGV System From Shut-down Mode (Reset Metrics → Start → Close out/Bag Out → Running)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=WCS API / OptiSweep API and Windows Services): OptiSweep and/or dependency path is restored and responsive for downstream validation.
- `unhealthy` (observer=site_or_remote; tool=Windows Services / Ignition Systems Overview): Recovery actions fail or safe confirmation cannot be achieved.
- `escalate` (observer=remote; tool=Windows Services / Ignition Systems Overview): Unable to complete recovery safely or evidence remains inconclusive beyond operator scope.

**Branches:**

- `healthy` → `node_3` when Recovery responsiveness confirmed

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

---

### 3 — Validate OptiSweep responsiveness and AGV status reachability after recovery (`validation_gate`)

**Intent:** Confirm that the recovered control stack is responsive enough to query AGV statuses and that the system is not still in a faulted/unresponsive state.

**Expects capability:** wcs_api_responsiveness, fleet_system_status, agv_active_errors
**Expects surface:** ignition_gateway, wcs_api, event_viewer
**Preferred audience:** L2_support, operator

**Runbook Links:**

- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.6309, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (low, support, score=0.6416, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_pause_resume_all_agv_movement_pauseagvs_resumeagvs_v1` (low, support, score=0.7095, boosted=1.0733333333333333) — Pause and resume all AGV movement using PauseAGVs / ResumeAGVs API requests
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `wcs_api_responsiveness`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=WCS API / OptiSweep API (GetAgvStatuses) + Ignition Systems Overview): Control stack is responsive enough for AGV status reachability; system is ready for RMS resynchronization.
- `unhealthy` (observer=remote; tool=WCS API / OptiSweep API and Windows Services): Validation fails: API unreachable/errors or service/gateway responsiveness not restored.
- `inconclusive` (observer=site_or_remote; tool=Ignition gateway / API): Some diagnostics succeed but key reachability evidence is missing.

**Branches:**

- `healthy` → `node_4` when API reachability validated
- `unhealthy` → `node_2` when API/service/gateway not responsive

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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

<details><summary>Pause and resume all AGV movement using PauseAGVs / ResumeAGVs API requests (`proc_pause_resume_all_agv_movement_pauseagvs_resumeagvs_v1`)</summary>

##### Runbook: Pause and resume all AGV movement using PauseAGVs / ResumeAGVs API requests

- **Procedure ID:** `proc_pause_resume_all_agv_movement_pauseagvs_resumeagvs_v1`
- **Procedure Type:** `operation`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the OptiSweep / WCS API client (Apidog / WCS API) to send fleet-level PauseAGVs and ResumeAGVs requests to Geek. PauseAGVs pauses all AGV movement; ResumeAGVs resumes the paused AGVs. Confirm each request shows an observable success/acceptance result in the API client.

**When To Use:**
When you need to pause all AGV movement fleet-wide (PauseAGVs) or resume the paused fleet (ResumeAGVs) by sending the correct API request to Geek, and you can observe the request/response outcome in the OptiSweep / WCS API client.

**Safety Notes:**

- This procedure is a fleet-level movement pause/resume action via API requests to Geek.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Select the PauseAGVs API action and confirm it pauses all AGV movement

**Responsible role:** L2_support

**Instruction:**
On the OptiSweep / WCS API client surface (Apidog / WCS API), select the API action named PauseAGVs and confirm it is described as making a request to Geek to pause all AGV movement.

**Healthy condition:**
PauseAGVs is selected and its description matches: request to Geek to pause all AGV movement.

**Expected result:**
The API client is set to the PauseAGVs action, and the action description indicates it will make a request to Geek to pause all AGV movement.

---

###### Step 2 — Submit the PauseAGVs request

**Responsible role:** L2_support

**Instruction:**
Submit the PauseAGVs request from the OptiSweep / WCS API client (Apidog / WCS API).

**Healthy condition:**
The API client shows a successful/accepted outcome for the PauseAGVs request (observable in the client’s request/response result).

**Expected result:**
The PauseAGVs request is sent from the API client and a request/response result is displayed.

---

###### Step 3 — Verify PauseAGVs request success/acceptance in the API client

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client (Apidog / WCS API), verify the PauseAGVs request shows an observable success/acceptance result for the request.

**Healthy condition:**
Success/acceptance is shown for PauseAGVs in the API client request/response outcome.

**Expected result:**
The API client displays an observable success/acceptance result for the PauseAGVs request.

---

###### Step 4 — Select the ResumeAGVs API action and confirm it resumes all paused AGV movement

**Responsible role:** L2_support

**Instruction:**
On the OptiSweep / WCS API client surface (Apidog / WCS API), select the API action named ResumeAGVs and confirm it is described as making a request to Geek to resume all AGV movement.

**Healthy condition:**
ResumeAGVs is selected and its description matches: request to Geek to resume all AGV movement.

**Expected result:**
The API client is set to the ResumeAGVs action, and the action description indicates it will make a request to Geek to resume all AGV movement.

---

###### Step 5 — Submit the ResumeAGVs request

**Responsible role:** L2_support

**Instruction:**
Submit the ResumeAGVs request from the OptiSweep / WCS API client (Apidog / WCS API).

**Healthy condition:**
The API client shows a successful/accepted outcome for the ResumeAGVs request (observable in the client’s request/response result).

**Expected result:**
The ResumeAGVs request is sent from the API client and a request/response result is displayed.

---

###### Step 6 — Verify ResumeAGVs request success/acceptance in the API client

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client (Apidog / WCS API), verify the ResumeAGVs request shows an observable success/acceptance result for the request.

**Healthy condition:**
Success/acceptance is shown for ResumeAGVs in the API client request/response outcome.

**Expected result:**
The API client displays an observable success/acceptance result for the ResumeAGVs request.

---

**Success Criteria:**

- PauseAGVs request is executed and the API client shows an observable success/acceptance result for the request.
- ResumeAGVs request is executed and the API client shows an observable success/acceptance result for the request.

**Failure Conditions:**

- API client shows an error/failed outcome for PauseAGVs.
- API client shows an error/failed outcome for ResumeAGVs.


</details>

</details>

---

### 4 — Resynchronize/correct out-of-sync AGVs in RMS (`procedure_reference`)

**Intent:** Use RMS to locate AGVs that are out of sync and correct them so the site can resume automated bag-out/small sort operations.

**Expects capability:** agv_active_errors, device_roster_state, robot_command_or_task_state
**Expects surface:** rms_ui
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_check_overall_system_agv_status_popup_agv_destination_errors_v1` (low, support, score=0.7665, boosted=1.0) — Check Overall System AGV Status popup for AGVs with destination errors
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_use_rms_map_monitor_message_panel_agv_faults_v1` (low, support, score=0.7653, boosted=1.0) — Use RMS Map Monitor Message Panel to view AGV fault list, fault details, and locate a faulted AGV
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1` (low, support, score=0.7957, boosted=1.0) — Check RMS fleet status for AGVs in shutdown queues and zone cycling
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `robot_command_or_task_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Previously out-of-sync AGVs are corrected in RMS and expected operational states resume.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): RMS remains unusable or corrections do not clear abnormal states.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Partial correction succeeded but evidence is insufficient to declare stability.

**Branches:**

- `healthy` → `node_5` when RMS state corrected

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

<details><summary>Use RMS Map Monitor Message Panel to view AGV fault list, fault details, and locate a faulted AGV (`proc_use_rms_map_monitor_message_panel_agv_faults_v1`)</summary>

##### Runbook: Use RMS Map Monitor Message Panel to view AGV fault list, fault details, and locate a faulted AGV

- **Procedure ID:** `proc_use_rms_map_monitor_message_panel_agv_faults_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI Map Monitor message panel to identify faulted/disconnected AGVs, view the selected fault’s details, and use the “Locate Faulted AGV” control to bring up the corresponding location cue.

**When To Use:**
When you need to determine which AGVs are faulted and/or disconnected and then inspect the fault details and locate the affected AGV using the RMS Map Monitor message panel.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS / fleet status UI and navigate to the Map Monitor message panel

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the Map Monitor message panel on the right side of the interface.

**Healthy condition:**
All labeled panel sections are present and readable in the Map Monitor message panel.

**Expected result:**
The Map Monitor message panel is visible on the right side and shows the labeled items: “Count of active Robots”, “Count of Robots charging”, “Drop down to show AGV faults”, “Count of AGVs disconnected”, “Inspection to view details of fault”, and “Locate Faulted AGV”.

---

###### Step 2 — Verify the active robot and charging count metrics

**Responsible role:** L1_support

**Instruction:**
On the Map Monitor message panel, locate and verify the fields labeled “Count of active Robots” and “Count of Robots charging”.

**Healthy condition:**
The panel shows numeric values for “Count of active Robots” and “Count of Robots charging”.

**Expected result:**
Both count fields are displayed on the panel.

---

###### Step 3 — Open the AGV faults dropdown to display the fault list

**Responsible role:** L1_support

**Instruction:**
Use the dropdown labeled “Drop down to show AGV faults” to display the AGV fault list.

**Healthy condition:**
Fault entries are visible in the dropdown list.

**Expected result:**
The AGV faults dropdown expands and shows fault entries.

---

###### Step 4 — Check the count of AGVs disconnected

**Responsible role:** L1_support

**Instruction:**
On the same Map Monitor message panel, locate and check the field labeled “Count of AGVs disconnected”.

**Healthy condition:**
The “Count of AGVs disconnected” field displays a current numeric count.

**Expected result:**
A numeric value is shown for “Count of AGVs disconnected”.

---

###### Step 5 — Select a fault entry and confirm fault details update

**Responsible role:** L1_support

**Instruction:**
In the AGV faults list, select a fault entry and use the “Inspection to view details of fault” area to confirm the fault details update for the selected entry.

**Healthy condition:**
Fault details change when you select different fault entries.

**Expected result:**
The “Inspection to view details of fault” area updates to show details for the selected fault entry.

---

###### Step 6 — Locate the faulted AGV using the “Locate Faulted AGV” control

**Responsible role:** L1_support

**Instruction:**
Use “Locate Faulted AGV” to bring up the faulted AGV location cue (e.g., map highlight/selection) and confirm the located AGV corresponds to the selected fault.

**Healthy condition:**
The map/location cue highlights/selects the AGV associated with the selected fault.

**Expected result:**
A location cue appears for the faulted AGV after using “Locate Faulted AGV”, and it corresponds to the selected fault entry.

---

**Success Criteria:**

- The Map Monitor message panel shows “Count of active Robots” and “Count of Robots charging”.
- The “Drop down to show AGV faults” displays fault entries.
- Selecting a fault entry updates the “Inspection to view details of fault” area.
- Using “Locate Faulted AGV” produces a location cue that corresponds to the selected faulted AGV.

**Failure Conditions:**

- AGV faults dropdown shows no fault entries while AGV issues are reported.
- Fault details do not update after selecting a fault entry.
- Locate Faulted AGV location cue does not correspond to the selected fault.


</details>

<details><summary>Check RMS fleet status for AGVs in shutdown queues and zone cycling (`proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1`)</summary>

##### Runbook: Check RMS fleet status for AGVs in shutdown queues and zone cycling

- **Procedure ID:** `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI to verify that AGVs are held in shutdown queues (shutdown state), then cycle into their assigned zones (4 zones) after startup, consistent with the system state model described in the segment.

**When To Use:**
When you need to confirm that AGVs are in the shutdown state (shutdown queues) and then transition into their assigned zones (4 zones) after startup, using the live fleet status view in RMS.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI and view AGV roster/map

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV list/map view where you can see each AGV’s current state and/or location/zone assignment.

**Healthy condition:**
The RMS fleet status view is accessible and shows AGVs with state/location/zone information (enough to distinguish shutdown queues vs zone assignments).

**Expected result:**
You can see the AGV list/map view in RMS with each AGV’s current state and/or location/zone assignment visible.

---

###### Step 2 — Confirm AGVs are in shutdown queues (shutdown state)

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV list/map view, identify the relevant AGVs and confirm that their current state and/or location/zone assignment corresponds to shutdown queues (shutdown state), not idle/running zones.

**Healthy condition:**
AGVs expected to be in shutdown are consistently shown as being in shutdown queues/shutdown state.

**Expected result:**
AGVs that should be in shutdown are displayed in a shutdown queues/shutdown state condition in RMS (observable via their state and/or location/zone assignment).

---

###### Step 3 — Observe transition from shutdown queues into assigned zones (4 zones)

**Responsible role:** L1_support

**Instruction:**
Observe the AGVs in RMS over the expected startup transition window and confirm they move from shutdown queues into their assigned zones. The segment references 4 zones.

**Healthy condition:**
AGVs move out of shutdown queues into zone assignments rather than remaining in shutdown state.

**Expected result:**
AGVs transition from shutdown queues/shutdown state into their assigned zones (4 zones referenced in the segment).

---

###### Step 4 — If tipper/hospital scenario is active, confirm shutdown/startup cycle still holds

**Responsible role:** L1_support

**Instruction:**
If the segment’s scenario is active (tipper issue leading to hospital/reject handling), confirm in RMS that AGVs still follow the shutdown/startup cycle model: shutdown queues → assigned zones, rather than remaining stuck in shutdown queues.

**Healthy condition:**
No prolonged retention in shutdown queues beyond what the shutdown/startup logic implies; AGVs still enter their zone assignments.

**Expected result:**
Even during the tipper/hospital scenario, AGVs still transition from shutdown queues into their assigned zones in RMS.

---

**Success Criteria:**

- In RMS, AGVs expected to be in shutdown are shown in shutdown queues/shutdown state.
- After startup, those AGVs transition from shutdown queues into their assigned zones (4 zones referenced).
- During any tipper/hospital scenario, AGVs still follow shutdown queues → zones behavior rather than remaining stuck in shutdown.

**Failure Conditions:**

- AGVs remain in shutdown queues/shutdown state without transitioning into their assigned zones when startup is expected.
- RMS shows AGVs in non-shutdown zone assignments during a shutdown period.


</details>

</details>

---

### 5 — Confirm operational recovery and stability (AGVs moving / small sort running) (`validation_gate`)

**Intent:** Validate that the site has returned to stable operation after service recovery and AGV resynchronization.

**Expects capability:** fleet_system_status, agv_active_errors, sort_lifecycle_state
**Expects surface:** rms_ui, wcs_api
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6449, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `sort_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (low, support, score=0.7897, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Missing corroboration for `sort_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_resend_geek_command_using_command_guid_from_get_command_status_v1` (low, support, score=0.3, boosted=0.6033333333333334) — Resend Geek command using the command GUID from Get Command Status (Geek Plus missed request recovery)
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `sort_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.; Procedure type 'recovery' is not ideal for node type 'validation_gate'.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `sort_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI + WCS API (optional corroboration)): Operational recovery confirmed: automation resumes and abnormal conditions are gone.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Degraded recovery: only partial/manual bag-out possible or AGVs remain in abnormal states.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Recovery may be present but evidence is not yet sufficient to declare stability.
- `escalate` (observer=remote; tool=Windows Services / Ignition Systems Overview): Control stack is still unresponsive or RMS cannot be used safely for resynchronization corrections.

**Branches:**

- `healthy` → `` when Operational recovery confirmed

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

<details><summary>Resend Geek command using the command GUID from Get Command Status (Geek Plus missed request recovery) (`proc_resend_geek_command_using_command_guid_from_get_command_status_v1`)</summary>

##### Runbook: Resend Geek command using the command GUID from Get Command Status (Geek Plus missed request recovery)

- **Procedure ID:** `proc_resend_geek_command_using_command_guid_from_get_command_status_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the command GUID shown in the live “Get Command Status” view to call the ResendGeekCommand function, which resends the request to Geek Plus. This is intended for recovery when Geek Plus may have missed the request after an unplanned restart.

**When To Use:**
When Geek Plus may have missed a command request after an unplanned restart, and you need to resend that Geek command using the command GUID visible in the live Get Command Status area.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open the live Get Command Status area and locate the command GUID

**Responsible role:** L2_support

**Instruction:**
In the live RMS / fleet status UI, open the area that includes “Get Command Status” (within the Get AGV status/command status view) and locate the main GUID / command GUID shown there.

**Healthy condition:**
The Get Command Status view shows a valid main GUID/command GUID value that can be used for the resend.

**Expected result:**
A command GUID (main GUID/command GUID) is visible in the Get Command Status view.

---

###### Step 2 — Invoke ResendGeekCommand using the command GUID

**Responsible role:** L2_support

**Instruction:**
Using the OptiSweep / WCS API client workflow, call ResendGeekCommand and provide the command GUID you identified from Get Command Status.

**Healthy condition:**
The resend call is issued with the same command GUID that is shown in Get Command Status.

**Expected result:**
ResendGeekCommand is executed for the selected command GUID.

---

###### Step 3 — Verify command status reflects the resend attempt

**Responsible role:** L2_support

**Instruction:**
Return to the live Get Command Status / command status view and observe for evidence that the resend was issued for the same command GUID (e.g., updated GET command status fields associated with that GUID).

**Healthy condition:**
Command status/response fields for the same GUID show an observable update consistent with the resend attempt.

**Expected result:**
The Get Command Status / command status view reflects the resend attempt for the same command GUID.

---

**Success Criteria:**

- ResendGeekCommand is executed using the command GUID from Get Command Status
- Get Command Status / command status view shows an observable update for the same command GUID after the resend attempt

**Failure Conditions:**

- Command GUID is not available in Get Command Status
- ResendGeekCommand cannot be executed due to missing/invalid GUID
- No observable change in command status for the same GUID after resend attempt


</details>

</details>

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Unhealthy control-stack pattern corroborated | `node_2` |
| `node_1` | `inconclusive` | Pattern not fully confirmed | `node_2` |
| `node_2` | `healthy` | Recovery responsiveness confirmed | `node_3` |
| `node_3` | `healthy` | API reachability validated | `node_4` |
| `node_3` | `unhealthy` | API/service/gateway not responsive | `node_2` |
| `node_4` | `healthy` | RMS state corrected | `node_5` |
| `node_5` | `healthy` | Operational recovery confirmed | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_1: proc_check_rms_screen_for_system_faults_first_step_v1 (low)
- node_1: proc_verify_optsweep_wcs_windows_service_health_v1 (low)
- node_3: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
- node_3: proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1 (low)
- node_3: proc_pause_resume_all_agv_movement_pauseagvs_resumeagvs_v1 (low)
- node_4: proc_check_overall_system_agv_status_popup_agv_destination_errors_v1 (low)
- node_4: proc_use_rms_map_monitor_message_panel_agv_faults_v1 (low)
- node_4: proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1 (low)
- node_5: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_5: proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1 (low)
- node_5: proc_resend_geek_command_using_command_guid_from_get_command_status_v1 (low)
