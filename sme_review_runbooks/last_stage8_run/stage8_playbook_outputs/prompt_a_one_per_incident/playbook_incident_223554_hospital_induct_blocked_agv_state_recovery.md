# Hospital tote induction blocked with possible AGV state or hospital service disruption

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery` |
| Case ID | `223554` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital station unable to induct or add totes
- Site can remove totes but cannot add totes at the hospital area
- Robot reported in a shut down state
- Site cannot start sort or goes down during sort while hospital flow is disrupted
- Hospital backlog or excessive tote flow to hospital is reported
- AGVs appear in unexpected locations near the hospital pickup or rack area

## Affected Systems

- ACB hospital station
- AGV hospital station
- robots / AGVs
- Hospital Lane
- Opti sweep services
- RMS / fleet status
- Hospital HMI / lane UI
- AGV physical recovery / removal
- OptiSweep / WCS API

## Nodes

### 1 — Confirm the hospital-flow symptom pattern (`diagnostic_decision`)

**Intent:** Determine whether the reported issue matches the reusable pattern of hospital tote induction failure with broader operational impact rather than an unrelated localized complaint.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (medium, support, score=0.6903, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_screen_for_system_faults_first_step_v1` (high, support, score=0.6699, boosted=1.0) — Check RMS screen for system faults as the first step during an OptiSweep support call
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.6854, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Hospital workflow confirmation (site interview) + RMS / AGV status UI): Hospital-area symptom pattern confirmed: cannot add/induct totes at hospital station, robot(s) appear shut down/misplaced near hospital pickup/rack, and/or sort is blocked or stops.
- `healthy` (observer=site_or_remote; tool=Hospital workflow confirmation (site interview)): Non-matching pattern: normal hospital tote add/remove behavior or issue clearly outside hospital flow scope.
- `inconclusive` (observer=site_or_remote; tool=Hospital workflow confirmation (site interview)): Symptom evidence insufficient/ambiguous to confirm the reusable hospital-flow pattern.

**Branches:**

- `unhealthy` → `node_2` when hospital-flow pattern confirmed
- `inconclusive` → `node_6` when pattern not confirmed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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

### 2 — Check for AGV location or tote-association anomalies in the hospital area (`diagnostic_decision`)

**Intent:** Determine whether the hospital blockage is associated with AGVs in unexpected positions, duplicate occupancy near the rack, or a disconnected/associated tote condition that could block tote-add behavior.

**Expects capability:** fleet_system_status, agv_physical_recovery
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6061, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7629, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.7547, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI + hospital-area layout view (if available in RMS/HMI)): AGV/tote state anomaly indicated in hospital area.
- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI + hospital-area layout view (if available)): No hospital-area anomaly found (AGV positions/tote associations appear normal).
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Cannot determine whether anomaly exists due to insufficient or unreadable evidence.

**Branches:**

- `unhealthy` → `node_4` when agv/tote anomaly indicated
- `healthy` → `None` when no anomaly indicated
- `inconclusive` → `node_6` when uncertain evidence

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

### 3 — Check whether hospital-related services show an abnormal server or service condition (`diagnostic_decision`)

**Intent:** Determine whether the incident evidence supports a hospital-station server or service disruption that requires the approved service recovery path.

**Expects capability:** windows_service_or_event_log
**Expects surface:** event_viewer
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- `proc_verify_optsweep_wcs_windows_service_health_v1` (low, support, score=0.4462, boosted=0.4697) — Verify OptiSweep/WCS Windows service health when RMS/logs appear silent
  - gaps: Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Windows services / Event Viewer + OptiSweep/WCS service health (as available)): Hospital-related server/service abnormality is indicated.
- `inconclusive` (observer=site_or_remote; tool=Windows services / Event Viewer (as available)): No supported service abnormality found or findings remain inconclusive.

**Branches:**

- `unhealthy` → `node_4` when service abnormality indicated
- `inconclusive` → `node_6` when no supported service abnormality / inconclusive

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

### 4 — Perform the approved recovery for the indicated fault path (`procedure_reference`)

**Intent:** Carry out the supported recovery path for the fault pattern identified by prior diagnostics, whether that is hospital-related service recovery, AGV/tote state correction, or authorized AGV removal/re-add activity needed to restore flow.

**Runbook Links:**

- `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (medium, support, score=0.6911, boosted=0.9611) — Recover an AGV That Lost a Tote Without Faulting
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_a_faulted_motionless_agv_from_the_floor_and_restore_operation_v1` (high, support, score=0.6551, boosted=0.7051) — Remove A Faulted Motionless AGV From The Floor And Restore Operation
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI + hospital station/HMI + OptiSweep/WCS state): Approved recovery completed; system ready for post-recovery validation.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI + hospital station/HMI): Recovery incomplete or unsafe to complete, or approved actions did not restore normal hospital flow indicators.

**Branches:**

- `healthy` → `node_5` when Approved recovery completed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (2)</summary>

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

<details><summary>Remove A Faulted Motionless AGV From The Floor And Restore Operation (`proc_remove_a_faulted_motionless_agv_from_the_floor_and_restore_operation_v1`)</summary>

##### Runbook: Remove A Faulted Motionless AGV From The Floor And Restore Operation

- **Procedure ID:** `proc_remove_a_faulted_motionless_agv_from_the_floor_and_restore_operation_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Recover from an AGV motionless-on-floor fault by locating the faulted AGV, identifying and stopping the correct E-stop zone, removing the AGV from the floor, then restoring operation with the documented E-stop release and blue RESET sequence.

**When To Use:**
Use when an AGV is faulted and motionless on the floor and the documented troubleshooting sequence calls for locating the AGV, stopping the appropriate E-stop zone, removing the AGV, and resetting the system.

**Safety Notes:**

- This procedure is not marked support-safe because the source does not describe the safe handling method for physically removing the AGV.
- Use site safety controls and local procedures for physical AGV removal; this source does not provide those details.
- Stop and escalate if the AGV cannot be safely removed.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Locate the faulted AGV

**Responsible role:** L2_support

**Instruction:**
Locate the faulted AGV on the floor. If needed, reference RMS for AGV error information to help identify the AGV.

**Healthy condition:**
The specific AGV requiring recovery is clearly identified from floor observation and/or RMS error information.

**Expected result:**
The faulted motionless AGV is identified.

**Step Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/d87070d22301b81d.jpeg)

*Use as a visual example of a faulted AGV screen context during recovery.*

---

###### Step 2 — Identify the appropriate E-stop zone

**Responsible role:** L2_support

**Instruction:**
Reference the E-stop zone map to identify the appropriate E-stop zone for the faulted AGV.

**Healthy condition:**
The E-stop zone corresponding to the faulted AGV location is known before the zone is stopped.

**Expected result:**
The correct E-stop zone is identified.

---

###### Step 3 — Stop the appropriate E-stop zone

**Responsible role:** L2_support

**Instruction:**
Press E-STOP to stop the appropriate E-stop zone.

**Healthy condition:**
The intended E-stop zone is stopped and the area is isolated for AGV removal.

**Expected result:**
The appropriate E-stop zone is stopped.

---

###### Step 4 — Remove the faulted AGV from the floor

**Responsible role:** L2_support

**Instruction:**
Remove the faulted AGV from the floor.

**Healthy condition:**
The faulted AGV is no longer on the floor in the affected area.

**Expected result:**
The faulted AGV is removed from the floor.

---

###### Step 5 — Release the E-stop

**Responsible role:** L2_support

**Instruction:**
Pull E-STOP.

**Healthy condition:**
The E-stop is pulled out/released and the system is ready for reset.

**Expected result:**
The E-stop is released.

**Step Images:**

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Reference ESTOP clearing and RESET context associated with pulling out ESTOP and clearing faults.*

---

###### Step 6 — Press the blue RESET button

**Responsible role:** L2_support

**Instruction:**
Press the blue RESET button.

**Healthy condition:**
The reset completes without additional fault indication.

**Expected result:**
The reset is accepted and the system clears the fault condition.

**Step Images:**

![artifact_fig_5_4_faulted_agv_with_tote_screen](assets/d87070d22301b81d.jpeg)

*Candidate-provided image support for a faulted AGV screen during the fault recovery procedure.*

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Reference RESET-related HMI context associated with clearing faults after ESTOP is pulled out.*

---

###### Step 7 — Verify the system resumes operation

**Responsible role:** L2_support

**Instruction:**
Verify that the system resumes operation.

**Healthy condition:**
Normal operation resumes after the reset sequence.

**Expected result:**
The system resumes operation.

---

**Success Criteria:**

- The faulted AGV is identified.
- The appropriate E-stop zone is stopped.
- The faulted AGV is removed from the floor.
- The E-stop is released and the blue RESET button is pressed.
- The system resumes operation.

**Failure Conditions:**

- The faulted AGV cannot be identified from floor observation and RMS reference.
- The correct E-stop zone cannot be determined.
- The AGV cannot be safely removed.
- The reset sequence does not clear the fault.
- The system does not resume operation after the documented reset sequence.


</details>

</details>

---

### 5 — Validate hospital tote handling and robot recovery (`validation_gate`)

**Intent:** Confirm that hospital tote operations and related robot flow have recovered after the approved recovery action.

**Expects capability:** device_roster_state, fleet_system_status, hospital_diversion
**Expects surface:** rms_ui, wcs_api, hospital_hmi, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.597, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (high, support, score=0.5577, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.6941, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital station/HMI + RMS / AGV status UI + (if applicable) WCS/OptiSweep checks): Hospital tote handling and robot flow recovered.
- `unhealthy` (observer=site_or_remote; tool=Hospital station/HMI + RMS / AGV status UI): Validation fails or recovery is not stable.
- `inconclusive` (observer=site_or_remote; tool=Hospital station/HMI + RMS / AGV status UI): Cannot fully validate recovery due to incomplete evidence or ambiguous observations.

**Branches:**

- `healthy` → `` when Hospital tote handling and robot flow validated as recovered
- `unhealthy` → `node_6` when Validation fails or recovery is not stable

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

### 6 — Stop and escalate if supported diagnostics or recovery do not restore stable operation (`escalation_gate`)

**Intent:** Hand off when the available evidence does not clearly support a safe next recovery step, when authorized recovery cannot be performed, or when validation fails after supported recovery.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI, Windows service evidence (if available), hospital HMI/symptom notes): Escalation required: supported AGV/tote-state or service-abnormality path cannot be identified safely, or validation fails after supported recovery.

**Branches:**

- `escalate` → `` when supported path exhausted/unresolved

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | hospital-flow pattern confirmed | `node_2` |
| `node_1` | `inconclusive` | pattern not confirmed | `node_6` |
| `node_2` | `unhealthy` | agv/tote anomaly indicated | `node_4` |
| `node_2` | `healthy` | no anomaly indicated | `` |
| `node_2` | `inconclusive` | uncertain evidence | `node_6` |
| `node_3` | `unhealthy` | service abnormality indicated | `node_4` |
| `node_3` | `inconclusive` | no supported service abnormality / inconclusive | `node_6` |
| `node_4` | `healthy` | Approved recovery completed | `node_5` |
| `node_5` | `healthy` | Hospital tote handling and robot flow validated as recovered | `` |
| `node_5` | `unhealthy` | Validation fails or recovery is not stable | `node_6` |
| `node_6` | `escalate` | supported path exhausted/unresolved | `` |

## Unresolved / Low-Confidence Links

- node_2: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_3: proc_verify_optsweep_wcs_windows_service_health_v1 (low)
- node_5: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_6: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
