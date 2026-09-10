# Bag-out stops after sorting with suspected AGV sequence or stuck-task indicators

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_218550_bagout_stoppage_agv_sequence_hmi_fault` |
| Case ID | `218550` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- System stopped at bag-out after sorting.
- Bag-out started, processed some items, then stopped again.
- Site is manually bagging out.
- A robot or AGV may be out of sequence or an exchange pair may have issues.
- An AGV appears not to have moved for an extended period.
- An HMI associated with the hospital area is showing a fault.
- A message fault may appear during bag-out even when no stack light fault is visible.

## Affected Systems

- bag-out stage
- AGV / robots
- RMS / fleet status
- Hospital HMI / lane UI
- Aveva screen visibility context

## Nodes

### 1 — Confirm the bag-out stoppage pattern matches this response path (`diagnostic_decision`)

**Intent:** Determine whether the reported issue is a bag-out-after-sorting stoppage with broad signs of AGV/robot disruption or related HMI fault context, rather than an unrelated localized issue.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (medium, support, score=0.7439, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (high, support, score=0.7102, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (high, support, score=0.7335, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `unhealthy` (observer=site; tool=RMS / AGV status UI | Hospital HMI / lane UI): Bag-out after sorting does not complete; manual bagging out is occurring/required; site reports AGV/robot sequencing/exchange-pair concerns and/or a hospital-area HMI fault context.
- `healthy` (observer=site; tool=Hospital HMI / lane UI | RMS / AGV status UI): Bag-out is completing normally or issue is clearly unrelated to AGV/HMI sequence behavior.
- `inconclusive` (observer=site_or_remote; tool=site interview): Symptom confirmation is incomplete (e.g., bag-out restart/stop cadence unclear; manual bagging out involvement unclear; HMI fault not confirmed).
- `escalate` (observer=remote; tool=RMS / AGV status UI | Hospital HMI / lane UI): Unable to determine whether the issue matches this playbook without excessive delay or safety/production impact warrants immediate deeper assistance.

**Branches:**

- `unhealthy` → `node_2` when Confirmed bag-out-after-sorting stoppage with AGV/robot/HMI abnormal context
- `healthy` → `` when Bag-out normal or not matching AGV/HMI-linked stoppage pattern
- `inconclusive` → `node_2` when Unclear symptom match

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

</details>

---

### 2 — Check RMS for AGV inactivity or abnormal fleet state tied to the stoppage (`diagnostic_decision`)

**Intent:** Determine whether RMS or related fleet-status evidence shows an AGV that is not moving, abnormal activity, or active error context that supports an AGV-side troubleshooting path.

**Expects capability:** device_roster_state, fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.7016, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_faults_and_active_agv_faults_overall_system_rms_v1` (high, support, score=0.8796, boosted=1.0) — Check Overall System Faults and Active AGV Faults on the Overall System RMS Page
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.8612, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `unhealthy` (observer=remote; tool=RMS / AGV status UI): RMS shows abnormal fleet state, AGV inactivity, exchange/backfill gap, or active error context consistent with sequence/pair disruption supporting recovery actions.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): RMS evidence is insufficient or ambiguous for AGV inactivity/exchange disruption (e.g., RMS partial visibility).
- `healthy` (observer=remote; tool=RMS / AGV status UI): No relevant AGV inactivity or fleet-state issue is visible; continue via other evidence paths only if indicated.
- `escalate` (observer=remote; tool=RMS / AGV status UI | wcs_sql): RMS cannot be accessed or evidence is not available and stoppage remains unresolved.

**Branches:**

- `unhealthy` → `node_3` when RMS shows AGV inactivity/abnormal fleet state consistent with sequence/pair disruption
- `healthy` → `` when RMS does not show relevant AGV inactivity/fleet-state issue

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

### 3 — Decide whether HMI-visible fault or stuck-task review is needed (`branching_condition`)

**Intent:** Choose whether to continue down an HMI-focused branch based on reports of a hospital-area HMI fault, tote-specific fault context, or evidence that a stuck task may only be visible on that HMI.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, hospital_hmi, wcs_sql
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `unhealthy` (observer=site; tool=Hospital HMI / lane UI): HMI branch indicated: reported hospital HMI fault and/or evidence suggests stuck-task is only visible on that HMI interface.
- `healthy` (observer=site; tool=Hospital HMI / lane UI): HMI branch not indicated: no hospital HMI fault / no HMI-only stuck-task signal.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI | RMS / AGV status UI): HMI evidence is unclear; proceed to confirm hospital HMI fault state if feasible or default to AGV recovery if not.

**Branches:**

- `unhealthy` → `node_4` when Reported hospital HMI fault or stuck-task only visible on hospital HMI
- `healthy` → `node_5` when No HMI fault or HMI-only stuck-task signal
- `inconclusive` → `node_4` when HMI evidence inconclusive

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 4 — Inspect the hospital HMI fault or stuck-task presentation (`diagnostic_decision`)

**Intent:** Determine whether the hospital HMI shows a fault or stuck-task condition that aligns with the bag-out interruption and whether the approved local recovery path is applicable.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, hospital_hmi, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6069, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_overall_system_state_on_aveva_api_page_v1` (high, support, score=0.6616, boosted=1.0) — Check Overall System state on the AVEVA API page (System State / System Startup / Bag Out / Shutdown / Purge)
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_diagnose_agv_exchange_backfill_gap_v1` (high, support, score=0.7016, boosted=1.0) — Diagnose AGV exchange/backfill gap when an AGV moves out without a replacement
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital HMI shows a fault or stuck-task condition consistent with the bag-out interruption; local acknowledge-and-retry path likely applicable.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital HMI fault is present but cannot be confidently tied to the bag-out interruption, or the mapping to affected tote/task is unclear.
- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital HMI does not show a relevant fault or stuck-task condition for this issue.
- `escalate` (observer=remote; tool=Hospital HMI / lane UI): Hospital HMI fault persists and safe local recovery/acknowledge path cannot be performed.

**Branches:**

- `unhealthy` → `node_6` when HMI fault/stuck-task presentation matches and acknowledge-and-retry is applicable
- `healthy` → `node_5` when HMI evidence inconclusive or not relevant

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

### 5 — Perform approved AGV sequence or pair recovery (`procedure_reference`)

**Intent:** Apply the supported AGV recovery path when AGV inactivity, sequence disruption, or pair-related abnormal state is indicated.

**Runbook Links:**

- `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1` (low, support, score=0.7023, boosted=0.9723) — Recover an AGV That Lost a Tote Without an AGV Fault
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_remove_a_faulted_motionless_agv_from_the_floor_and_restore_operation_v1` (high, support, score=0.6969, boosted=0.7896) — Remove A Faulted Motionless AGV From The Floor And Restore Operation
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Recovery completed but bag-out may still be unstable; proceed to validation.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): Recovery could not be fully completed (authorization/availability/safety) or fleet restoration uncertain.
- `escalate` (observer=remote; tool=RMS / AGV status UI | Hospital HMI / lane UI): Supported recovery not authorized or not possible safely for the identified condition.

**Branches:**

- `healthy` → `node_7` when Approved AGV sequence or pair recovery completed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (2)</summary>

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

### 6 — Perform approved HMI acknowledge-and-retry recovery if the HMI branch is indicated (`procedure_reference`)

**Intent:** Use the supported HMI recovery action when the HMI fault presentation matches the issue and the approved local recovery path is available.

**Runbook Links:**

- `proc_use_execute_agv_command_for_system_recovery_v1` (low, support, score=0.6524, boosted=0.8224) — Use Execute AGV Command For System Recovery
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): HMI acknowledge-and-retry performed; bag-out still needs validation for stable resumption.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): HMI remains faulted after acknowledge-and-retry or outcome uncertain.
- `escalate` (observer=remote; tool=Hospital HMI / lane UI): Acknowledge-and-retry cannot be performed safely/authorized; proceed to escalation evidence packaging.

**Branches:**

- `healthy` → `node_7` when Approved HMI acknowledge-and-retry recovery completed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Use Execute AGV Command For System Recovery (`proc_use_execute_agv_command_for_system_recovery_v1`)</summary>

##### Runbook: Use Execute AGV Command For System Recovery

- **Procedure ID:** `proc_use_execute_agv_command_for_system_recovery_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Execute AGV Command control in the AGVs section of the System HMI API screen for system recovery when the system has gone down and messages were missed. The source documents the control and its purpose, but does not provide the command inputs, parameters, or confirmation behavior.

**When To Use:**
Use this procedure during system recovery when the system went down and messages were missed, and the recovery action involves the Execute AGV Command control in the AGVs section of the API screen.

**Safety Notes:**

- This is a recovery-related control with potential system-wide impact.
- The source does not provide command inputs, parameters, or confirmation behavior; do not improvise unsupported recovery commands.
- Escalate if approved site documentation or support personnel cannot provide the required recovery command details.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open the AGVs section of the API screen

**Responsible role:** L2_support

**Instruction:**
Open the System HMI API screen and navigate to the AGVs section.

**Healthy condition:**
The AGV API Controls area is displayed and the AGV controls are available for review.

**Expected result:**
The AGVs section of the API screen is visible.

**Step Images:**

![artifact_fig_4_8_acb_api_screen](assets/b192077f772ce5cd.jpeg)

*The ACB API screen interface used to access AGV controls.*

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*The AGV API Controls area within the AGVs section of the API screen.*

---

###### Step 2 — Locate the Execute AGV Command control

**Responsible role:** L2_support

**Instruction:**
In the AGVs section, locate the Execute AGV Command control.

**Healthy condition:**
The Execute AGV Command control is visible in the AGV API Controls area.

**Expected result:**
The Execute AGV Command control is identified on the AGV API Controls screen.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*The Execute AGV Command control listed among the AGV API Controls.*

---

###### Step 3 — Use Execute AGV Command for documented recovery purpose

**Responsible role:** L2_support

**Instruction:**
Use Execute AGV Command as part of system recovery when the system went down and messages were missed. If the required command details are not available from approved site documentation or support personnel, stop and escalate.

**Healthy condition:**
The control is used only in the documented recovery scenario and the operator has approved recovery command details from site documentation or support personnel.

**Expected result:**
The Execute AGV Command control is used for the documented system recovery purpose related to missed messages.

**Step Images:**

![artifact_fig_4_12_agv_api_controls](assets/4f58f8bb3f0f6aea.jpeg)

*The Execute AGV Command control used for system recovery in the AGV API Controls screen.*

---

**Success Criteria:**

- The AGVs section of the API screen is accessed.
- The Execute AGV Command control is identified.
- The control is used only for the documented recovery case where the system went down and messages were missed.

**Failure Conditions:**

- The API screen or AGVs section cannot be accessed.
- The Execute AGV Command control cannot be located.
- The source does not provide enough detail to safely determine command inputs, parameters, or confirmation behavior.


</details>

</details>

---

### 7 — Validate that bag-out and robot sequence have recovered (`validation_gate`)

**Intent:** Confirm that the recovery restored normal operation and that the site is no longer blocked by the AGV/HMI condition.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, hospital_hmi, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6372, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_overall_system_agv_status_remote_availability_v1` (high, support, score=0.7346, boosted=1.0) — Check RMS for Overall System AGV Status to confirm remote availability
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.75, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | Hospital HMI / lane UI): Successful recovery: bag-out resumes or completes; robots/AGVs are back in proper sequence; any related hospital HMI fault is cleared; site reports normal function.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI | Hospital HMI / lane UI): Failed validation: bag-out stops again; robots remain out of sequence; or HMI/task fault persists.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | Hospital HMI / lane UI): Partial improvement/uncertain stability window (e.g., bag-out processed some items but did not complete; need another validation check).
- `escalate` (observer=remote; tool=RMS / AGV status UI | Hospital HMI / lane UI): Validation cannot be completed due to missing evidence or unsafe condition; proceed to escalation handoff.

**Branches:**

- `inconclusive` → `` when Bag-out resumes or completes and robots are back in proper sequence
- `unhealthy` → `node_8` when Bag-out remains unstable, stops again, or the fault condition persists
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

<details><summary>Check RMS for Overall System AGV Status to confirm remote availability (`proc_check_rms_overall_system_agv_status_remote_availability_v1`)</summary>

##### Runbook: Check RMS for Overall System AGV Status to confirm remote availability

- **Procedure ID:** `proc_check_rms_overall_system_agv_status_remote_availability_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status web UI to open the page titled “Overall System AGV Status” and confirm the page loads and displays the current overall system status content. This is used to verify remote availability of the RMS overview page.

**When To Use:**
When you need to confirm that the RMS fleet status UI is reachable remotely and that the “Overall System AGV Status” overview page is displaying the current overall system status.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS / fleet status UI (RMS web UI)

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status web UI (rms_ui).

**Healthy condition:**
The RMS UI is reachable and responsive enough to navigate to the “Overall System AGV Status” page.

**Expected result:**
RMS / fleet status UI opens successfully (i.e., you can proceed to navigate within RMS).

---

###### Step 2 — Navigate to the “Overall System AGV Status” page

**Responsible role:** L1_support

**Instruction:**
Within RMS, navigate to the page titled “Overall System AGV Status”.

**Healthy condition:**
The page header/title “Overall System AGV Status” is present.

**Expected result:**
The “Overall System AGV Status” page is displayed (page title/header visible).

---

###### Step 3 — Verify the page displays the current overall system status content

**Responsible role:** L1_support

**Instruction:**
On the “Overall System AGV Status” page, observe the page content that indicates the current overall system status (the page is described as showing the current status).

**Healthy condition:**
The page shows current status content (i.e., the page is populated with status information rather than blank/unreachable).

**Expected result:**
The “Overall System AGV Status” page loads and displays current overall system status information (not blank/unavailable).

---

**Success Criteria:**

- RMS / fleet status UI is reachable remotely.
- The “Overall System AGV Status” page loads successfully.
- The “Overall System AGV Status” page displays current overall system status content (not blank/unavailable).

**Failure Conditions:**

- RMS / fleet status UI cannot be reached remotely.
- “Overall System AGV Status” page does not load.
- “Overall System AGV Status” page content is missing/blank.


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

### 8 — Escalate if supported recovery does not restore stable bag-out (`escalation_gate`)

**Intent:** Stop and escalate when the available AGV/HMI troubleshooting path is exhausted, unsupported, or fails validation.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=RMS / AGV status UI | Hospital HMI / lane UI): Escalate: supported AGV/HMI recovery cannot restore stable bag-out; authorization/safety prevents further recovery; or validation fails.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Confirmed bag-out-after-sorting stoppage with AGV/robot/HMI abnormal context | `node_2` |
| `node_1` | `healthy` | Bag-out normal or not matching AGV/HMI-linked stoppage pattern | `` |
| `node_1` | `inconclusive` | Unclear symptom match | `node_2` |
| `node_2` | `unhealthy` | RMS shows AGV inactivity/abnormal fleet state consistent with sequence/pair disruption | `node_3` |
| `node_2` | `healthy` | RMS does not show relevant AGV inactivity/fleet-state issue | `` |
| `node_3` | `unhealthy` | Reported hospital HMI fault or stuck-task only visible on hospital HMI | `node_4` |
| `node_3` | `healthy` | No HMI fault or HMI-only stuck-task signal | `node_5` |
| `node_3` | `inconclusive` | HMI evidence inconclusive | `node_4` |
| `node_4` | `unhealthy` | HMI fault/stuck-task presentation matches and acknowledge-and-retry is applicable | `node_6` |
| `node_4` | `healthy` | HMI evidence inconclusive or not relevant | `node_5` |
| `node_5` | `healthy` | Approved AGV sequence or pair recovery completed | `node_7` |
| `node_6` | `healthy` | Approved HMI acknowledge-and-retry recovery completed | `node_7` |
| `node_7` | `inconclusive` | Bag-out resumes or completes and robots are back in proper sequence | `` |
| `node_7` | `unhealthy` | Bag-out remains unstable, stops again, or the fault condition persists | `node_8` |
| `node_7` | `healthy` | Recovery validation criteria are met | `` |

## Unresolved / Low-Confidence Links

- node_2: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_3: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_5: proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1 (low)
- node_6: proc_use_execute_agv_command_for_system_recovery_v1 (low)
- node_8: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
