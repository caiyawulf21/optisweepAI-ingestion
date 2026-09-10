# Site-wide robotic motion stoppage with AGVs out of sync after control-service or gateway abnormality

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228086_site_wide_motion_stoppage_service_recovery` |
| Case ID | `228086` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `high` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Site reports that nothing is moving.
- Robotic system is reported as not responding.
- Small sort is not running.
- Totes cannot be removed from hospital.
- HMI or RMS appears abnormal, including question marks or a mostly blank page.
- AGVs are reported out of sync or behaving abnormally after the stoppage.

## Affected Systems

- OptiSweep service
- Windows Event Viewer / Service Control Manager
- Windows Services
- Ignition gateway
- WCSWebApplication
- RMS / HMI
- OptiSweep / WCS API
- AGVs / robotic system

## Nodes

### 1 — Confirm site-wide stoppage and abnormal control-system presentation (`diagnostic_decision`)

**Intent:** Determine whether the reported issue matches a broad robotic-system stoppage pattern rather than an isolated robot fault.

**Expects capability:** fleet_system_status
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (medium, support, score=0.6752, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_ui_confirm_rms_up_v1` (high, support, score=0.7725, boosted=1.0) — Check RMS fleet status UI to confirm RMS is up and running
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7624, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Evidence supports a site-wide robotic motion stoppage pattern (broad non-movement plus abnormal RMS/HMI presentation).
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Some stoppage symptoms are present, but the presentation abnormality is unclear or not consistently observed.
- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Impact appears localized and RMS/HMI appears normal; not consistent with a site-wide stoppage pattern.

**Branches:**

- `unhealthy` → `node_2` when Confirmed site-wide stoppage or abnormal RMS-HMI presentation
- `healthy` → `` when Localized impact only or normal RMS-HMI presentation

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

### 2 — Check for OptiSweep service failure evidence (`diagnostic_decision`)

**Intent:** Determine whether the OptiSweep service is in an abnormal state or recently terminated in a way that correlates with the stoppage.

**Expects capability:** windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_verify_optsweep_wcs_windows_service_health_v1` (low, support, score=0.893, boosted=1.0) — Verify OptiSweep/WCS Windows service health when RMS/logs appear silent
  - gaps: Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `unhealthy` (observer=remote; tool=Windows Event Viewer / Services): OptiSweep termination/service abnormality evidence is present.
- `healthy` (observer=remote; tool=Windows Event Viewer / Services): No OptiSweep failure evidence; service appears normal.
- `inconclusive` (observer=remote; tool=Windows Event Viewer / Services): Service evidence is incomplete/unclear.

**Branches:**

- `unhealthy` → `node_5` when OptiSweep termination evidence is present or current service state is abnormal
- `inconclusive` → `node_3` when Service failure is not clearly established or HMI/gateway symptoms remain unexplained

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

### 3 — Decide whether gateway or dependent application checks are needed (`branching_condition`)

**Intent:** Choose whether to continue with Ignition and application-layer diagnostics when service failure evidence is absent, incomplete, or insufficient to explain the stoppage.

**Expects capability:** gateway_health, windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer, ignition_gateway
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `unhealthy` (observer=remote; tool=Ignition Systems Overview + Windows Event Viewer (Application log)): Gateway or dependent application checks are needed before recovery.
- `healthy` (observer=remote; tool=Windows Event Viewer / Services): Skip gateway/application investigation because primary service failure is already established/authorized recovery path is available.
- `inconclusive` (observer=remote; tool=Ignition Systems Overview + Windows Event Viewer): Insufficient/ambiguous evidence to decide definitively.

**Branches:**

- `unhealthy` → `node_4` when Gateway or dependent application checks are needed
- `healthy` → `` when Skip to supported recovery

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 4 — Assess Ignition gateway and application-layer health (`diagnostic_decision`)

**Intent:** Determine whether the gateway is responsive and whether nearby application errors provide supporting evidence for the stoppage.

**Expects capability:** gateway_health, windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer, ignition_gateway
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- `proc_check_ignition_gateway_sys_perf_localhost_v1` (low, support, score=0.7949, boosted=1.0) — Check Ignition Gateway system performance status via localhost sys.perf page
  - gaps: Missing corroboration for `wcs_service_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_ignition_gateway_sys_perf_v1` (high, support, score=0.7334, boosted=0.9834) — Check Ignition Gateway system performance status via Ignition Gateway UI
  - gaps: Missing corroboration for `wcs_service_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `wcs_service_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `unhealthy` (observer=remote; tool=Ignition Systems Overview + Windows Event Viewer (Application log)): Gateway/app-layer appears unhealthy or contextual evidence supports dependency issues.
- `healthy` (observer=remote; tool=Ignition Systems Overview + Windows Event Viewer): Ignition gateway is responsive and app-layer evidence does not suggest a dependency failure.
- `inconclusive` (observer=remote; tool=Ignition Systems Overview + Windows Event Viewer): Partial evidence across gateway UI and event logs.

**Branches:**

- `unhealthy` → `node_5` when Gateway/app-layer unhealthy or dependency evidence present
- `healthy` → `node_5` when Gateway healthy; proceed with supported recovery path

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (2)</summary>

<details><summary>Check Ignition Gateway system performance status via localhost sys.perf page (`proc_check_ignition_gateway_sys_perf_localhost_v1`)</summary>

##### Runbook: Check Ignition Gateway system performance status via localhost sys.perf page

- **Procedure ID:** `proc_check_ignition_gateway_sys_perf_localhost_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Ignition Gateway web UI on the host to open the system performance status page at http://localhost:8088/web/status/sys.perf. Confirm the page loads and that system performance/health indicators are visible (not a connection/refused/unreachable error).

**When To Use:**
When Ignition Gateway reachability or performance is suspected on the Ignition Gateway host, and you need a quick local check that the /web/status/sys.perf page is reachable and shows performance/health indicators.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open the Ignition Gateway sys.perf status page on localhost

**Responsible role:** L2_support

**Instruction:**
On the Ignition Gateway host, open a web browser and navigate to http://localhost:8088/web/status/sys.perf.

**Healthy condition:**
The sys.perf page loads with visible page content rather than an unreachable/error state.

**Expected result:**
The browser successfully loads the Ignition Gateway system performance status page at /web/status/sys.perf (page content visible; not a connection/refused/unreachable error).

---

###### Step 2 — Verify sys.perf performance/health indicators are visible

**Responsible role:** L2_support

**Instruction:**
On the loaded /web/status/sys.perf page, observe the system performance status indicators/readouts shown on the page.

**Healthy condition:**
Performance/health indicators/readouts are visible on the sys.perf page.

**Expected result:**
System performance/health information is displayed on the sys.perf page (not blank and not replaced by an error/unavailable state).

---

**Success Criteria:**

- http://localhost:8088/web/status/sys.perf loads successfully in a browser
- The sys.perf page displays system performance/health indicators (no connection/refused/unreachable error)

**Failure Conditions:**

- sys.perf page does not load due to unreachable/error state (e.g., connection refused/unreachable)
- sys.perf page loads but performance indicators show degraded/unacceptable status


</details>

<details><summary>Check Ignition Gateway system performance status via Ignition Gateway UI (`proc_check_ignition_gateway_sys_perf_v1`)</summary>

##### Runbook: Check Ignition Gateway system performance status via Ignition Gateway UI

- **Procedure ID:** `proc_check_ignition_gateway_sys_perf_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Ignition Gateway web UI to open the system performance status page for sys.perf and confirm the page loads and displays system performance status content.

**When To Use:**
When you need to verify that the Ignition Gateway system performance status page is reachable and that it shows sys.perf system performance status content.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open the Ignition Gateway sys.perf system performance status page

**Responsible role:** L1_support

**Instruction:**
Using a web browser, navigate to http://localhost:8088/web/status/sys.perf.

**Healthy condition:**
The sys.perf page opens successfully in the browser.

**Expected result:**
The browser loads the Ignition Gateway sys.perf status page (i.e., not a browser error page).

---

###### Step 2 — Confirm the loaded page corresponds to sys.perf and is not blank

**Responsible role:** L1_support

**Instruction:**
After the page loads, confirm the content corresponds to the sys.perf system performance status page and that the page shows system performance status information (not blank/failed content).

**Healthy condition:**
System performance/status content is visible on the sys.perf page.

**Expected result:**
The sys.perf page displays system performance status information (visible performance/status content).

---

**Success Criteria:**

- http://localhost:8088/web/status/sys.perf loads successfully in the browser
- The sys.perf page displays system performance status information (not blank/failed content)

**Failure Conditions:**

- sys.perf page is unreachable or fails to load (connection refused/timeout)
- sys.perf page loads but system performance/status content is missing/blank


</details>

</details>

---

### 5 — Perform approved recovery for the affected service or gateway (`procedure_reference`)

**Intent:** Carry out the authorized recovery action for the identified abnormal service or gateway path.

**Runbook Links:**

- `proc_recover_an_agv_from_a_bump_fault_code_v1` (medium, support, score=0.56, boosted=0.73) — Recover An AGV From A BUMP Fault Code
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=Windows Services + Ignition Systems Overview + WCS/OptiSweep API): Authorized recovery completed and affected service/gateway returns to responsive state for validation.
- `unhealthy` (observer=remote; tool=Windows Services / Ignition UI / API): Recovery could not be performed safely or successfully within authorization constraints.
- `inconclusive` (observer=remote; tool=Windows Services / Ignition UI / API): Recovery attempt completed but responsiveness evidence is partial.

**Branches:**

- `healthy` → `node_6` when Primary service or gateway recovery completed
- `escalate` → `node_9` when Recovery cannot be safely/successfully completed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Recover An AGV From A BUMP Fault Code (`proc_recover_an_agv_from_a_bump_fault_code_v1`)</summary>

##### Runbook: Recover An AGV From A BUMP Fault Code

- **Procedure ID:** `proc_recover_an_agv_from_a_bump_fault_code_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Recover a documented AGV BUMP fault when Geek+ cannot recover the AGV by gathering required fault details, confirming the BUMP fault information on the AGV Bump Fault Screen, stopping RMS, removing the obstruction, resetting the AGV, and resuming RMS.

**When To Use:**
Use this procedure for the documented AGV BUMP fault recovery case in the OptiSweep manual when Geek+ cannot recover the AGV.

**Safety Notes:**

- The source states to gather information before going inside the grid (the Dance Floor).
- This procedure includes going inside the grid and physically removing an obstruction.
- Safety controls beyond the documented E-stop actions are not specified in the supplied source excerpt.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Gather required fault information before entering the grid

**Responsible role:** L2_support

**Instruction:**
Before going inside the grid (the Dance Floor), gather the Robot ID, the fault description from RMS, whether RMS indicates the faulted AGV is holding a bin and the tote ID if present, and if the faulted AGV is under a rack, determine whether that AGV is the empty AGV for that zone.

**Healthy condition:**
Robot ID, RMS fault description, tote/bin status, tote ID if present, and under-rack empty-AGV status are known before entering the grid.

**Expected result:**
The responder has the AGV identity and required RMS fault context needed for the recovery.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*AGV identification and fault information relevant to the faulted robot.*

---

###### Step 2 — Confirm the documented BUMP fault case

**Responsible role:** L2_support

**Instruction:**
Identify that the AGV is in the documented BUMP fault case and check the exception information shown for code 21057 or 21060 if displayed on the AGV Bump Fault Screen.

**Healthy condition:**
The AGV Bump Fault Screen shows the documented BUMP fault context, with exception information matching code 21057 or 21060 when displayed.

**Expected result:**
The responder confirms the AGV fault matches the documented BUMP fault context and reviews the displayed exception information.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*Fault or exception display area, exception code area, and AGV identification on the AGV Bump Fault Screen.*

---

###### Step 3 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Healthy condition:**
RMS is in the stopped state required for the recovery sequence.

**Expected result:**
RMS is E-stopped.

---

###### Step 4 — Remove the obstruction

**Responsible role:** L2_support

**Instruction:**
Remove the obstruction.

**Healthy condition:**
The obstruction is no longer present and the AGV is clear of the bump condition.

**Expected result:**
The obstruction is removed from the AGV path or contact point.

---

###### Step 5 — Reset the AGV to clear the fault

**Responsible role:** L2_support

**Instruction:**
Click the AGV RESET button for two seconds to clear the fault.

**Healthy condition:**
The BUMP fault clears after the AGV RESET button is held for two seconds.

**Expected result:**
The AGV fault is cleared.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*AGV RESET button location on the AGV Bump Fault Screen.*

---

###### Step 6 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
Press E-stop again.

**Healthy condition:**
The second E-stop action is completed as specified by the manual.

**Expected result:**
The documented second E-stop action is completed.

---

###### Step 7 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
Resume RMS.

**Healthy condition:**
RMS resumes and the AGV BUMP fault remains cleared.

**Expected result:**
RMS is resumed and the documented recovery sequence is complete.

---

**Success Criteria:**

- The obstruction is removed.
- The AGV fault is cleared using the AGV RESET button.
- RMS is resumed.
- The documented BUMP recovery sequence completes without the fault persisting.

**Failure Conditions:**

- Required pre-entry fault information cannot be gathered.
- The fault does not match the documented BUMP fault case.
- RMS cannot be E-stopped or resumed as documented.
- The obstruction cannot be removed.
- The AGV fault does not clear after the documented reset sequence.


</details>

</details>

---

### 6 — Check for residual AGV desynchronization after service recovery (`diagnostic_decision`)

**Intent:** Determine whether AGVs remain out of sync and require RMS-based correction before normal operation can resume.

**Expects capability:** device_roster_state, fleet_system_status, gateway_health
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6219, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_selected_robot_details_robot_id_location_node_code_tote_v1` (high, support, score=0.6225, boosted=1.0) — Check Selected Robot Details (Robot ID, Location, Node Code/Cell Code, Tote ID) in Robot Selection Overview
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7188, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).
- Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `unhealthy` (observer=remote; tool=RMS / AGV status UI): Residual AGV desynchronization remains and needs RMS-based correction.
- `healthy` (observer=remote; tool=RMS / AGV status UI): No residual AGV sync issue is present; fleet appears synchronized.
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): AGV state is unclear; evidence is incomplete.

**Branches:**

- `unhealthy` → `node_7` when Out-of-sync or abnormal AGVs are present in RMS
- `healthy` → `node_8` when No residual AGV sync issue is found

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

### 7 — Perform supported AGV resynchronization or correction in RMS (`procedure_reference`)

**Intent:** Apply the approved RMS-based correction path for AGVs left out of sync after the primary service or gateway issue is addressed.

**Runbook Links:**

- `proc_recover_an_agv_from_a_bump_fault_code_v1` (low, support, score=0.6606, boosted=0.8306) — Recover An AGV From A BUMP Fault Code
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI): AGV correction in RMS completed and residual out-of-sync blockers removed.
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): AGV state could not be corrected with approved supported RMS actions.

**Branches:**

- `healthy` → `node_8` when AGV correction completed
- `escalate` → `node_9` when AGV correction failed / unsupported state suggests escalation

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Recover An AGV From A BUMP Fault Code (`proc_recover_an_agv_from_a_bump_fault_code_v1`)</summary>

##### Runbook: Recover An AGV From A BUMP Fault Code

- **Procedure ID:** `proc_recover_an_agv_from_a_bump_fault_code_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Recover a documented AGV BUMP fault when Geek+ cannot recover the AGV by gathering required fault details, confirming the BUMP fault information on the AGV Bump Fault Screen, stopping RMS, removing the obstruction, resetting the AGV, and resuming RMS.

**When To Use:**
Use this procedure for the documented AGV BUMP fault recovery case in the OptiSweep manual when Geek+ cannot recover the AGV.

**Safety Notes:**

- The source states to gather information before going inside the grid (the Dance Floor).
- This procedure includes going inside the grid and physically removing an obstruction.
- Safety controls beyond the documented E-stop actions are not specified in the supplied source excerpt.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Gather required fault information before entering the grid

**Responsible role:** L2_support

**Instruction:**
Before going inside the grid (the Dance Floor), gather the Robot ID, the fault description from RMS, whether RMS indicates the faulted AGV is holding a bin and the tote ID if present, and if the faulted AGV is under a rack, determine whether that AGV is the empty AGV for that zone.

**Healthy condition:**
Robot ID, RMS fault description, tote/bin status, tote ID if present, and under-rack empty-AGV status are known before entering the grid.

**Expected result:**
The responder has the AGV identity and required RMS fault context needed for the recovery.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*AGV identification and fault information relevant to the faulted robot.*

---

###### Step 2 — Confirm the documented BUMP fault case

**Responsible role:** L2_support

**Instruction:**
Identify that the AGV is in the documented BUMP fault case and check the exception information shown for code 21057 or 21060 if displayed on the AGV Bump Fault Screen.

**Healthy condition:**
The AGV Bump Fault Screen shows the documented BUMP fault context, with exception information matching code 21057 or 21060 when displayed.

**Expected result:**
The responder confirms the AGV fault matches the documented BUMP fault context and reviews the displayed exception information.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*Fault or exception display area, exception code area, and AGV identification on the AGV Bump Fault Screen.*

---

###### Step 3 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
E-stop the RMS.

**Healthy condition:**
RMS is in the stopped state required for the recovery sequence.

**Expected result:**
RMS is E-stopped.

---

###### Step 4 — Remove the obstruction

**Responsible role:** L2_support

**Instruction:**
Remove the obstruction.

**Healthy condition:**
The obstruction is no longer present and the AGV is clear of the bump condition.

**Expected result:**
The obstruction is removed from the AGV path or contact point.

---

###### Step 5 — Reset the AGV to clear the fault

**Responsible role:** L2_support

**Instruction:**
Click the AGV RESET button for two seconds to clear the fault.

**Healthy condition:**
The BUMP fault clears after the AGV RESET button is held for two seconds.

**Expected result:**
The AGV fault is cleared.

**Step Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/87f1d32e67350071.jpeg)

*AGV RESET button location on the AGV Bump Fault Screen.*

---

###### Step 6 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
Press E-stop again.

**Healthy condition:**
The second E-stop action is completed as specified by the manual.

**Expected result:**
The documented second E-stop action is completed.

---

###### Step 7 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
Resume RMS.

**Healthy condition:**
RMS resumes and the AGV BUMP fault remains cleared.

**Expected result:**
RMS is resumed and the documented recovery sequence is complete.

---

**Success Criteria:**

- The obstruction is removed.
- The AGV fault is cleared using the AGV RESET button.
- RMS is resumed.
- The documented BUMP recovery sequence completes without the fault persisting.

**Failure Conditions:**

- Required pre-entry fault information cannot be gathered.
- The fault does not match the documented BUMP fault case.
- RMS cannot be E-stopped or resumed as documented.
- The obstruction cannot be removed.
- The AGV fault does not clear after the documented reset sequence.


</details>

</details>

---

### 8 — Validate service responsiveness and operational recovery (`validation_gate`)

**Intent:** Confirm that the recovered service path is responsive, AGV status is available, and the site has resumed automated operation.

**Expects capability:** fleet_system_status, gateway_health, windows_service_or_event_log
**Expects surface:** rms_ui, wcs_api, ignition_gateway, wcs_sql
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.6468, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_ignition_gateway_sys_perf_localhost_v1` (high, support, score=0.7226, boosted=1.0) — Check Ignition Gateway system performance status via localhost sys.perf page
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (high, support, score=0.7105, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `gateway_health`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `windows_service_or_event_log`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=WCS/SSMS (read-only) | RMS / AGV status UI | Ignition Systems Overview): Service responsiveness + AGV status data available + site automation resumed.
- `unhealthy` (observer=remote; tool=WCS/SSMS (read-only) | RMS / AGV status UI | Ignition Systems Overview): Validation fails; service path not fully recovered or AGV sync blockers persist.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI | WCS/SSMS (read-only) | Ignition Systems Overview): Some validation evidence is incomplete.

**Branches:**

- `healthy` → `` when Validation confirms recovery
- `unhealthy` → `node_9` when Validation fails

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

<details><summary>Check Ignition Gateway system performance status via localhost sys.perf page (`proc_check_ignition_gateway_sys_perf_localhost_v1`)</summary>

##### Runbook: Check Ignition Gateway system performance status via localhost sys.perf page

- **Procedure ID:** `proc_check_ignition_gateway_sys_perf_localhost_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Ignition Gateway web UI on the host to open the system performance status page at http://localhost:8088/web/status/sys.perf. Confirm the page loads and that system performance/health indicators are visible (not a connection/refused/unreachable error).

**When To Use:**
When Ignition Gateway reachability or performance is suspected on the Ignition Gateway host, and you need a quick local check that the /web/status/sys.perf page is reachable and shows performance/health indicators.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open the Ignition Gateway sys.perf status page on localhost

**Responsible role:** L2_support

**Instruction:**
On the Ignition Gateway host, open a web browser and navigate to http://localhost:8088/web/status/sys.perf.

**Healthy condition:**
The sys.perf page loads with visible page content rather than an unreachable/error state.

**Expected result:**
The browser successfully loads the Ignition Gateway system performance status page at /web/status/sys.perf (page content visible; not a connection/refused/unreachable error).

---

###### Step 2 — Verify sys.perf performance/health indicators are visible

**Responsible role:** L2_support

**Instruction:**
On the loaded /web/status/sys.perf page, observe the system performance status indicators/readouts shown on the page.

**Healthy condition:**
Performance/health indicators/readouts are visible on the sys.perf page.

**Expected result:**
System performance/health information is displayed on the sys.perf page (not blank and not replaced by an error/unavailable state).

---

**Success Criteria:**

- http://localhost:8088/web/status/sys.perf loads successfully in a browser
- The sys.perf page displays system performance/health indicators (no connection/refused/unreachable error)

**Failure Conditions:**

- sys.perf page does not load due to unreachable/error state (e.g., connection refused/unreachable)
- sys.perf page loads but performance indicators show degraded/unacceptable status


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

### 9 — Escalate if supported recovery path does not restore stable operation (`escalation_gate`)

**Intent:** Stop and escalate when the available supported checks and recovery actions do not identify a safe or successful path to restore stable operation.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=Windows Event Viewer + Windows Services + Ignition Systems Overview + WCS/OptiSweep API + RMS / AGV status UI): Supported recovery is exhausted/unsafe/unsuccessful; escalation is required.

**Branches:**

- `escalate` → `` when Escalate if supported recovery path does not restore stable operation

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Confirmed site-wide stoppage or abnormal RMS-HMI presentation | `node_2` |
| `node_1` | `healthy` | Localized impact only or normal RMS-HMI presentation | `` |
| `node_2` | `unhealthy` | OptiSweep termination evidence is present or current service state is abnormal | `node_5` |
| `node_2` | `inconclusive` | Service failure is not clearly established or HMI/gateway symptoms remain unexplained | `node_3` |
| `node_3` | `unhealthy` | Gateway or dependent application checks are needed | `node_4` |
| `node_3` | `healthy` | Skip to supported recovery | `` |
| `node_4` | `unhealthy` | Gateway/app-layer unhealthy or dependency evidence present | `node_5` |
| `node_4` | `healthy` | Gateway healthy; proceed with supported recovery path | `node_5` |
| `node_5` | `healthy` | Primary service or gateway recovery completed | `node_6` |
| `node_5` | `escalate` | Recovery cannot be safely/successfully completed | `node_9` |
| `node_6` | `unhealthy` | Out-of-sync or abnormal AGVs are present in RMS | `node_7` |
| `node_6` | `healthy` | No residual AGV sync issue is found | `node_8` |
| `node_7` | `healthy` | AGV correction completed | `node_8` |
| `node_7` | `escalate` | AGV correction failed / unsupported state suggests escalation | `node_9` |
| `node_8` | `healthy` | Validation confirms recovery | `` |
| `node_8` | `unhealthy` | Validation fails | `node_9` |
| `node_9` | `escalate` | Escalate if supported recovery path does not restore stable operation | `` |

## Unresolved / Low-Confidence Links

- node_2: proc_verify_optsweep_wcs_windows_service_health_v1 (low)
- node_3: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_4: proc_check_ignition_gateway_sys_perf_localhost_v1 (low)
- node_6: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_7: proc_recover_an_agv_from_a_bump_fault_code_v1 (low)
- node_8: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_9: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
