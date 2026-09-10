# Troubleshoot zone unable to get a pair with AMRs routing to hospital lane

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228723_zone_pair_fail_hospital_routing` |
| Case ID | `228723` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- “Zone 5 can’t get a pair.”
- “The ACB system is down.”
- “AMRs keep going to the hospital lane.”
- “Nothing is pairing in that zone.”
- “We replaced an AMR but the pairing issue didn’t clear right away.”

## Affected Systems

- ACB system (zone pairing behavior)
- AMRs / AGVs
- RMS (fleet/zone pairing UI)
- WCS / OptiSweep backend state (via SSMS read-only)

## Nodes

### 1 — Confirm the pairing-failure + hospital-lane routing symptom pattern (`diagnostic_decision`)

**Intent:** Determine whether the reported issue matches a zone pairing failure (unable to get a pair) with abnormal hospital-lane routing behavior, and identify the affected zone(s) for targeted checks.

**Expects capability:** zone_pairing_state, hospital_diversion, fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6308, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.6515, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.7397, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Symptom pattern confirmed as zone pairing failure + abnormal hospital-lane routing via site report and corroborating RMS/WCS signals; affected zone identified for targeted follow-up.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | hospital HMI): Symptom pattern appears matched and needs immediate corroboration escalation if backend indicators strongly show degraded conditions.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Could not confirm the pairing-failure + hospital routing pattern with accessible RMS/SSMS indicators.
- `escalate` (observer=site_or_remote; tool=RMS / AGV status UI): Pattern not matched; re-triage to a different flow.

**Branches:**

- `healthy` → `node_2` when Pair-fail + hospital diversion pattern confirmed
- `escalate` → `` when Pattern not matched

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

### 2 — Check fleet/system state for corroborating degraded conditions (`diagnostic_decision`)

**Intent:** Determine whether the overall system/fleet state is degraded or down (consistent with the ACB system down report) and whether there are active backend/system faults that could explain pairing failure and hospital-lane routing.

**Expects capability:** fleet_system_status, gateway_health, windows_service_or_event_log, wcs_system_faults
**Expects surface:** rms_ui, wcs_sql, event_viewer, ignition_gateway
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6437, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.7247, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.
- `proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1` (low, support, score=0.3, boosted=0.7350000000000001) — Check OPC COM tag subscription updates flowing to Sorter Sweeper (Ignition tag provider → OPC server → Sorter Sweeper processing)
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `wcs_system_faults`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Overall system/fleet state is healthy/running or inconclusive; proceed to coordinate add-remove/isolation action and re-validate zone pairing/routing.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Overall system/fleet state is degraded or down, corroborating the ACB-system-down report; coordinate add-remove/isolation with system-side state awareness.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | (optional) Ignition/Event Viewer): Some checks are unavailable (e.g., RMS blank due to access/firewall, SSMS telemetry incomplete).

**Branches:**

- `unhealthy` → `node_3` when Degraded/Down corroborated in RMS/SSMS
- `healthy` → `node_3` when Healthy/Running or inconclusive

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

### 3 — Apply the site’s roster/add-remove or isolation action (as already attempted) with system-side corroboration (`procedure_reference`)

**Intent:** If the symptom pattern is confirmed, coordinate the next safe troubleshooting direction around the site’s add/remove or isolation actions, ensuring the system-side state is consistent with the action and that the affected robot(s) are not still causing the pairing failure.

**Expects capability:** device_roster_state, zone_pairing_state, hospital_diversion
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.6784, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): After approved add/remove or isolation action, zone pairing indicators no longer show the same pair-fail pattern and abnormal hospital routing reduces/stops.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): System-side state does not change as expected after the action; pairing failure and/or abnormal hospital routing persists.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Action performed but validation signals are incomplete/inconclusive due to missing or blank UI/telemetry.

**Branches:**

- `healthy` → `node_4` when Proceed to stability validation after corroborated roster/state alignment

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

### 4 — Validate stable recovery of pairing and routing behavior (`validation_gate`)

**Intent:** Confirm that the zone pairing failure is resolved and that AMRs no longer exhibit abnormal hospital-lane routing, and that the system remains stable for a short monitoring window.

**Expects capability:** zone_pairing_state, hospital_diversion, fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6176, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1` (low, support, score=0.6946, boosted=1.0) — Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.6496, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | hospital HMI): Recovery validated and stable: pairing returns to normal and hospital-lane routing stops; remains stable for monitoring window (~10 minutes).
- `unhealthy` (observer=remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Recovery not validated: pairing failure persists or hospital-lane routing continues after the monitoring window.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Unable to confirm stability due to missing/blank telemetry or UI access limitations.
- `escalate` (observer=remote; tool=RMS / AGV status UI | WCS/SSMS (read-only)): Escalate to deeper technical flow if recovery not validated.

**Branches:**

- `healthy` → `` when Recovery validated (pairing normal + hospital diversion stops; stable during monitoring window)
- `escalate` → `` when Recovery not validated (pair-fail persists or hospital diversion continues)

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

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `healthy` | Pair-fail + hospital diversion pattern confirmed | `node_2` |
| `node_1` | `escalate` | Pattern not matched | `` |
| `node_2` | `unhealthy` | Degraded/Down corroborated in RMS/SSMS | `node_3` |
| `node_2` | `healthy` | Healthy/Running or inconclusive | `node_3` |
| `node_3` | `healthy` | Proceed to stability validation after corroborated roster/state alignment | `node_4` |
| `node_4` | `healthy` | Recovery validated (pairing normal + hospital diversion stops; stable during monitoring window) | `` |
| `node_4` | `escalate` | Recovery not validated (pair-fail persists or hospital diversion continues) | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_1: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_1: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
- node_2: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_2: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_2: proc_check_opc_com_tag_subscription_updates_to_sorter_sweeper_v1 (low)
- node_3: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_4: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_4: proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1 (low)
- node_4: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
