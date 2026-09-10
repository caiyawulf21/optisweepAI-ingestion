# Clustered WCS web-application errors during robotic outage

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228086_wcswebapplication_fault_investigation` |
| Case ID | `228086` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Windows Event Viewer shows clustered WCSWebApplication errors
- Application log shows Windows Error Reporting or Application Error entries around the outage time
- Event Viewer shows failed database-command execution for WCSWebApplication
- Support observes a faulted web application or webservice during or after robotic recovery

## Affected Systems

- WCSWebApplication
- Windows Event Viewer / Application log
- Windows Error Reporting
- database
- webservice application

## Nodes

### 1 — Confirm clustered application-fault pattern in Event Viewer (`diagnostic_decision`)

**Intent:** Determine whether the incident includes a meaningful WCS web-application fault pattern rather than isolated noise.

**Expects capability:** windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer
**Preferred audience:** L1_support, L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: Catalog gap for `wcs_service_health`: no compatible runbook survived filters; keep unresolved rather than linking a wrong-domain neighbor.
  - catalog gap: Catalog gap for `windows_service_or_event_log`: no compatible runbook survived filters; keep unresolved rather than linking a wrong-domain neighbor.
  - catalog gap: Preferred surfaces for a future SME gap runbook: `event_viewer`.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Event Viewer): Clustered WCSWebApplication/application-side errors are present around the outage time (not isolated noise).
- `inconclusive` (observer=site_or_remote; tool=Event Viewer): Some application errors are present but clustering or causality is unclear.
- `healthy` (observer=site_or_remote; tool=Event Viewer): No meaningful clustered application-fault pattern is present.

**Branches:**

- `unhealthy` → `node_2` when Clustered WCSWebApplication or related application errors are present
- `healthy` → `node_5` when Diagnostic check does not indicate the fault condition

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Check for database-command failure details (`diagnostic_decision`)

**Intent:** Determine whether the application fault pattern includes database-command execution failures that may justify deeper application or database escalation.

**Expects capability:** windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: Catalog gap for `wcs_service_health`: no compatible runbook survived filters; keep unresolved rather than linking a wrong-domain neighbor.
  - catalog gap: Catalog gap for `windows_service_or_event_log`: no compatible runbook survived filters; keep unresolved rather than linking a wrong-domain neighbor.
  - catalog gap: Preferred surfaces for a future SME gap runbook: `event_viewer`.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Event Viewer): Database-command failure details are confirmed and match the application-fault pattern.
- `inconclusive` (observer=site_or_remote; tool=Event Viewer): Application errors persist but database-command failure details are missing/unclear.
- `healthy` (observer=site_or_remote; tool=Event Viewer): No database-command failure evidence is present for the WCSWebApplication fault window.

**Branches:**

- `healthy` → `node_5` when Diagnostic check does not indicate the fault condition

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 3 — Decide whether the application fault remains operationally relevant after primary recovery (`branching_condition`)

**Intent:** Choose whether to continue application-fault investigation based on whether the web-application issue appears ongoing or still blocks recovery after service and fleet stabilization.

**Expects capability:** windows_service_or_event_log, wcs_service_health
**Expects surface:** event_viewer
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Event Viewer): Continue investigation: application fault appears ongoing or still blocks recovery.
- `healthy` (observer=site_or_remote; tool=Event Viewer): Deprioritize/exit flow: site operations resumed and no continuing application-side symptom is evident.
- `inconclusive` (observer=site_or_remote; tool=Event Viewer): Unclear whether the fault persists; evidence is insufficient.

**Branches:**

- `unhealthy` → `node_4` when Clustered WCSWebApplication or related application errors are present
- `healthy` → `node_5` when Site operations have resumed and no continuing application-side symptom is evident
- `inconclusive` → `node_4` when Application remains faulted / current evidence points to unresolved application-side failure

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 4 — Assess memory or log-growth suspicion as tentative context (`diagnostic_decision`)

**Intent:** Capture whether current evidence suggests a memory or log-growth pattern worth including in escalation context without treating it as confirmed root cause.

**Expects capability:** gateway_health
**Expects surface:** ignition_gateway
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- `proc_check_ignition_gateway_sys_perf_localhost_v1` (medium, support, score=0.6102, boosted=0.8702) — Check Ignition Gateway system performance status via localhost sys.perf page
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Decision Outcomes:**

- `unhealthy` (observer=site_or_remote; tool=Ignition gateway / sys performance view): Tentative memory/log-growth concern is supported enough to include in escalation context.
- `inconclusive` (observer=site_or_remote; tool=Ignition gateway / sys performance view): Some suspicion exists but evidence is not strong enough to document meaningfully.
- `healthy` (observer=site_or_remote; tool=Ignition gateway / sys performance view): No supported memory/log-growth pattern is found; do not emphasize in escalation.

**Branches:**

- `healthy` → `node_5` when Diagnostic check does not indicate the fault condition

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

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

</details>

---

### 5 — Escalate unresolved application fault with evidence package (`escalation_gate`)

**Intent:** Stop and escalate when the application-fault pattern is confirmed but no supported recovery path is established within the current role or the fault remains unresolved after primary recovery.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=site_or_remote; tool=Event Viewer + application fault evidence summary): Escalate with a complete evidence package because the application-fault pattern persists/unresolved and no supported standalone remediation is established.
- `healthy` (observer=site_or_remote; tool=Event Viewer): Close/deprioritize if evidence no longer indicates an active application fault.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Clustered WCSWebApplication or related application errors are present | `node_2` |
| `node_1` | `healthy` | Diagnostic check does not indicate the fault condition | `node_5` |
| `node_2` | `healthy` | Diagnostic check does not indicate the fault condition | `node_5` |
| `node_3` | `unhealthy` | Clustered WCSWebApplication or related application errors are present | `node_4` |
| `node_3` | `healthy` | Site operations have resumed and no continuing application-side symptom is evident | `node_5` |
| `node_3` | `inconclusive` | Application remains faulted / current evidence points to unresolved application-side failure | `node_4` |
| `node_4` | `healthy` | Diagnostic check does not indicate the fault condition | `node_5` |

## Unresolved / Low-Confidence Links

- node_1: unresolved — Catalog gap for `wcs_service_health`: no compatible runbook survived filters; keep unresolved rather than linking a wrong-domain neighbor.
- node_2: unresolved — Catalog gap for `wcs_service_health`: no compatible runbook survived filters; keep unresolved rather than linking a wrong-domain neighbor.
- node_3: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_5: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
