# Site cannot start or sustain sort

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_site_sort_unavailable` |
| Case ID | `223554` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- The site is reported down.
- The site cannot start sort.
- The site goes down in the middle of sort.
- Movement stops or the system is not running.
- A work-order or repair note reports AGV hospital-station server issues and a need to reset services.

## Affected Systems

- Site-wide sort operation
- OptiSweep services
- AGV hospital station server
- Hospital Lane
- AGVs and tippers

## Nodes

### 1 — Confirm site-wide sort unavailability (`diagnostic_decision`)

**Objective:** Determine whether the report is a broad inability to start or sustain sort rather than only a localized hospital-station symptom.

**Why this check is next:** The source reports that the site was down and could not start sort or went down in the middle of sort; the associated dashboard screenshot is not readable enough to interpret independently.

**Action:**

Confirm with the site whether sort is unavailable site-wide (and whether broad movement is absent), and treat any unreadable dashboard colors as un-interpretable until readable operational state is provided.

**Suggested database check:**

- **Database:** robotics
  - **Model:** HospitalDatabaseModel
  - **Inspect:** Hospital entrance and exit queue locations.
  - **Inspect:** Hospital tote drop-off location.
- **Database:** sorter_sweeper
  - **Model:** HospitalTagsModel
  - **Inspect:** Whether tag is in or out; drives action.
  - **Inspect:** List of hospital controller tags.
  - **Inspect:** Modular typed value columns (string/bool) selected by variable type.
- **Database:** robotics
  - **Model:** RobotDatabaseModel
  - **Inspect:** Robot state enum (Tipper/Hospital/Charger/Sorter/GLD/ShutDown family).
  - **Inspect:** Tote currently associated with robot.
  - **Inspect:** Assigned sorter side.

**Healthy:** Sort starts and continues with normal movement across the operation (not just a single hospital station).

**Unhealthy:** The site is down, sort cannot start, or sort stops broadly with movement broadly absent.

**Inconclusive:** The dashboard/screenshot is unreadable (no interpretable legend/labels), or the report is limited to one station/one AGV and cannot establish site-wide impact.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** operator, L1_support

**Runbook Links:**

- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.

**Source Evidence:**

- Site was reported down and could not start sort or went down during sort.

**Branches:**

- `unhealthy` → `node_2` when Broad unavailability confirmed
- `healthy` → `` when Hospital-only symptom
- `inconclusive` → `node_5` when Unclear / unreadable evidence

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Check for source-supported service or server abnormality (`diagnostic_decision`)

**Objective:** Determine whether the broad outage correlates with the documented AGV hospital-station server or service abnormality.

**Why this check is next:** The case artifacts and closure details mention AGV hospital-station server issues, services needing reset, and later reset of OptiSweep services, but do not show the live service state or exact service names.

**Action:**

Inspect the documented OptiSweep/AGV hospital-station server or related service evidence to determine whether the abnormality is live (responsive issues) versus only a historical work-order note.

**Suggested database check:**

- **Database:** robotics
  - **Model:** HospitalDatabaseModel
  - **Inspect:** Hospital entrance and exit queue locations.
  - **Inspect:** Hospital tote drop-off location.
- **Database:** sorter_sweeper
  - **Model:** HospitalTagsModel
  - **Inspect:** Whether tag is in or out; drives action.
  - **Inspect:** List of hospital controller tags.
  - **Inspect:** Modular typed value columns (string/bool) selected by variable type.
- **Database:** robotics
  - **Model:** RobotDatabaseModel
  - **Inspect:** Robot state enum (Tipper/Hospital/Charger/Sorter/GLD/ShutDown family).
  - **Inspect:** Tote currently associated with robot.
  - **Inspect:** Assigned sorter side.

**Healthy:** Relevant services/host state are responsive and no current abnormal condition is observed in the evidence you can inspect.

**Unhealthy:** The evidence indicates a live service/server abnormality consistent with the outage symptom (e.g., stopped services or crash/restart abnormality).

**Inconclusive:** Only a historical notes/work-order entry is available; exact service names or live state cannot be confirmed from the available artifact(s).

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1` (low, support, score=0.5828, boosted=0.7828) — Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.

**Evidence Collection Procedures:**

- `proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1` — Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures (L2_support): Use Windows Event Viewer / services to inspect the live Windows Application and System logs, then verify the current OptiSweep service state. Correlate WCSWebApplication database-command errors around 6:35-6:36 AM with OptiSweep Service Control Manager Event 7031 and the current Windows Services status before further recovery.

**Source Evidence:**

- AGV hospital station is described as having server issues and needing services reset.
- Resolution details state that Opti sweep services were reset.

**Branches:**

- `unhealthy` → `node_5` when Current service abnormality indicated
- `inconclusive` → `node_5` when No current abnormality / only historical notes

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures (`proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1`)</summary>

##### Runbook: Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures

- **Procedure ID:** `proc_windows_event_viewer_services_optisweep_wcswebapplication_diagnostic_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use Windows Event Viewer / services to inspect the live Windows Application and System logs, then verify the current OptiSweep service state. Correlate WCSWebApplication database-command errors around 6:35-6:36 AM with OptiSweep Service Control Manager Event 7031 and the current Windows Services status before further recovery.

**When To Use:**
Use Windows Event Viewer / services when the live OptiSweep or WCS-backed system is unresponsive, when clustered WCSWebApplication errors are suspected, or when a service crash or restart must be correlated with the incident. Inspect the live Windows Application and System logs and current Windows Services state before performing further recovery.

**Safety Notes:**

- This is an inspection and diagnostic procedure; do not infer root cause from clustered errors.
- Automatic restart configuration records an intended Windows action, not confirmed service recovery.
- Do not perform further recovery based only on the historical service-state screenshot.

- **Source:** `incident_case` / `source_case_228086`

**Procedure Steps:**

###### Step 1 — Inspect the Windows Event Viewer Application log

**Responsible role:** L2_support

**Instruction:**
In Windows Event Viewer / services, open Windows Logs > Application and inspect entries around 2/20/2026 6:35:24-6:36:07 AM. Open the WCSWebApplication error details, including Event ID 20102, and check nearby Application Error or Windows Error Reporting entries.

**Healthy condition:**
No new or repeated WCSWebApplication or related application errors appear in the current inspection window.

**Expected result:**
The Application log shows whether WCSWebApplication Event ID 20102 with 'Failed executing DbCommand (1,840ms)' and nearby clustered application errors are present in the inspected time window.

**Step Images:**

![artifact_incident_228086_page_027_embedded_image_01](assets/abd43e133aa30f1d.jpeg)

*Windows Event Viewer Application log showing Windows Error Reporting Event 1001 and clustered WCSWebApplication and Application Error entries around 6:36 AM.*

![artifact_incident_228086_page_028_embedded_image_01](assets/d4f3abbd8bd09df2.jpeg)

*Windows Event Viewer Application log showing WCSWebApplication Event ID 20102 and the 'Failed executing DbCommand (1,840ms)' message.*

---

###### Step 2 — Inspect the OptiSweep termination event

**Responsible role:** L2_support

**Instruction:**
In Windows Event Viewer / services, select Windows Logs > System and open the Service Control Manager event for OptiSweep. Check for Event ID 7031, Level Error, and inspect whether the message states that OptiSweep terminated unexpectedly and Windows planned to restart it after 60000 milliseconds.

**Healthy condition:**
No new or repeated OptiSweep Event ID 7031 termination is present in the current System log inspection.

**Expected result:**
The System log identifies whether an OptiSweep Event ID 7031 termination is present and whether the event contains the 60000-millisecond restart message.

**Step Images:**

![artifact_incident_228086_page_029_embedded_image_01](assets/dabb6bbd62f07c7c.png)

*Windows Event Viewer System log showing OptiSweep Service Control Manager Event 7031, unexpected termination, and the planned 60000-millisecond restart.*

---

###### Step 3 — Verify the current OptiSweep service state

**Responsible role:** L2_support

**Instruction:**
In Windows Event Viewer / services, open Windows Services, select OptiSweep, and inspect the current Status and Startup Type.

**Healthy condition:**
OptiSweep is currently shown as Running and its Startup Type is shown as Automatic.

**Expected result:**
Windows Services displays the current OptiSweep Status and Startup Type, allowing the live service state to be compared with the Event Viewer evidence.

**Step Images:**

![artifact_incident_228086_page_019_embedded_image_01](assets/3832c5ce44b05a86.png)

*Windows Services showing OptiSweep selected with Status Running and Startup Type Automatic.*

---

###### Step 4 — Correlate Windows Event Viewer / services evidence with the live incident state

**Responsible role:** L2_support

**Instruction:**
Compare the timestamps and live entries in Windows Event Viewer / services with the current incident state and the current OptiSweep status in Windows Services. Do not treat the configured automatic restart as proof that recovery completed.

**Healthy condition:**
The current Windows Services state is Running and the current Event Viewer inspection shows no new or repeated relevant errors.

**Expected result:**
The diagnostic conclusion separately identifies the observed WCSWebApplication errors, any OptiSweep Event 7031 termination, and the current OptiSweep service state.

---

**Success Criteria:**

- Windows Event Viewer / services inspection identifies whether current Application log evidence includes WCSWebApplication Event ID 20102 or clustered related errors.
- Windows Event Viewer / services inspection identifies whether an OptiSweep Event ID 7031 termination is present and whether a 60000-millisecond restart was configured.
- Windows Services shows the current OptiSweep Status and Startup Type.
- The diagnostic conclusion does not claim recovery or root cause without live supporting evidence.

**Failure Conditions:**

- WCSWebApplication Event ID 20102 or clustered application errors are present or repeating in the current inspection.
- OptiSweep Event ID 7031 is present or repeating in the current System log inspection.
- OptiSweep is not shown as Running in Windows Services.
- The available evidence only shows a configured restart and does not establish that recovery completed.
- The evidence is insufficient to establish a definitive root cause.


</details>

</details>

---

### 3 — Perform authorized service or lane recovery (`procedure_reference`)

**Objective:** Use the approved procedure for the documented service or Hospital Lane recovery path when the responsible role confirms that it is authorized and supported.

**Why this check is next:** The closure summary says OptiSweep services were reset and the site restarted Hospital Lane; the packet does not provide exact steps.

**Action:**

Perform an authorized OptiSweep service recovery and Hospital Lane restart only when the responsible role confirms it is authorized and supported, then prepare evidence that the recovery completed successfully and did not uncover unsafe anomalies.

**Healthy:** Authorized recovery/restart is completed and service/lane responsiveness returns (movement begins again).

**Unhealthy:** Recovery is rejected, service/lane remains abnormal, or the action would affect an unsafe/unknown operational state.

**Inconclusive:** Recovery completion is asserted but no direct service/lane/movement evidence is observable; or no authorized role is available.

**Procedure Reference:**

- **Trigger condition:** L1/L2 support or the authorized site role observes that the approved service recovery or Hospital Lane restart has completed. Progress signal: service responsiveness or lane availability returns. Unhealthy signal: the recovery is rejected, the service remains abnormal, or the action would affect an unsafe or unknown operational state. Inconclusive: completion is asserted but no observable service, lane, or movement change is available.
- **Selected procedure:** unresolved
- **Selection rationale:** n/a
- **Success confirmation:** n/a
- **Failure boundary:** Stop at the documented failure condition and escalate; do not invent a recovery path.

**Prerequisites:**

- None
- None

**Safety checks:**

- None

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L1_support, operator

**Runbook Links:**

- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.

**Source Evidence:**

- Reset Opti sweep services and had site restart Hospital Lane.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / operational status view): Authorized recovery completes; service/lane responsiveness returns and movement begins again.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / service evidence view): Recovery fails or is rejected; service/lane remains abnormal.
- `inconclusive` (observer=remote; tool=Hospital HMI / site interview): Recovery completion cannot be directly observed with service/lane/movement evidence.

**Branches:**

- `healthy` → `node_4` when Recovery completed and observable
- `unhealthy` → `node_5` when Recovery cannot be performed or remains abnormal

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 4 — Validate stable sort and movement recovery (`validation_gate`)

**Objective:** Confirm that the site can start or sustain sort and that movement remains active after service or lane recovery.

**Why this check is next:** The packet reports that movement started and the system was running, while the earlier symptom was inability to start or sustain sort.

**Validate:**

Validate stable sort and movement recovery after service/lane recovery by confirming sort startup, continued movement, and absence of immediate recurrence.

**Success:** Sort starts and remains active; movement is active and the site remains running/stable after recovery.

**Failure:** Sort cannot start, stops again after recovery, or movement does not resume / quickly stops.

**Inconclusive:** Only generic 'system is running' message is available; insufficient evidence of sustained sort or movement.

**Validation Gate:**

**Validation checklist:**

- Confirm the owning service remains running and stable.
- Confirm the supported API or control endpoint responds.
- Confirm the source-observed HMI state and ask the site to repeat the affected workflow.
- Observe the affected workflow for recurrence during the stated observation window.

**Required evidence sources:** a site interview

**Stable-operation observation:** Observe the affected workflow for recurrence during the defined observation window; a reachable screen or successful request alone is not recovery.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** operator, L1_support

**Runbook Links:**

- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.

**Source Evidence:**

- Chat reports that movement started and the system was running.

**Branches:**

- `healthy` → `` when Stable recovery confirmed
- `unhealthy` → `node_5` when Validation failure

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 5 — Stop if service recovery or sort validation fails (`escalation_gate`)

**Objective:** Hand off when the service or server condition cannot be confirmed, authorized recovery does not restore operation, or the site remains unable to start or sustain sort.

**Why this check is next:** The source contains incomplete service evidence, an unreadable dashboard artifact, and a site-wide outage that eventually recovered through multiple actions.

**Action:**

Stop and prepare a controlled handoff to L2/L3 when service recovery or sustained sort validation cannot be confirmed; compile evidence and ensure receiving role has what is needed to proceed safely.

**Healthy:** A complete evidence package is produced and the handoff is controlled (no further unsupported troubleshooting).

**Unhealthy:** Sort remains unavailable after supported recovery attempts or evidence is insufficient and continued changes would be unsafe/unauthorized.

**Inconclusive:** Only unreadable dashboard or historical notes are available and current service name/state cannot be identified; evidence package must be completed as best as possible.

**Escalation Gate:**

- **Reason:** Hand off when the service or server condition cannot be confirmed, authorized recovery does not restore operation, or the site remains unable to start or sustain sort.
- **Required next team:** The owning L2/L3 service or controls team
**Evidence package:**

- Sort availability/sort-start and sustained movement results (site reports)
- Service/server observations attempted and their outcomes (Event Viewer / Windows Services if available)
- Hospital Lane state evidence (where available) and recovery actions attempted
- Any recurrence signals and why further recovery would be unsafe/unsupported
- {'page_ref': 'case_223554:page_6', 'chunk_id': 'stage4_page_chunk_001', 'site_code': 'ups_haslet_tx', 'site_label': 'UPS Haslet TX (TXRTH)', 'quote_or_summary': 'The site was reported down and could not start sort or went down during sort.'}
**Actions attempted:**

- None
**Unresolved questions:**

- None

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- No linked procedure; escalate if the required state cannot be confirmed using the available approved evidence sources.

**Source Evidence:**

- The site was reported down and could not start sort or went down during sort.

**Decision Outcomes:**

- `healthy` (observer=remote; tool=compiled evidence (Event Viewer + site reports)): Evidence package complete; controlled handoff to L2/L3 ready.
- `unhealthy` (observer=remote; tool=site interview + Event Viewer evidence (if available)): Service recovery/validation failed and further changes would be unsafe or unsupported.
- `inconclusive` (observer=remote; tool=site interview + partial artifacts): Evidence insufficient due to unreadable dashboard or missing service state; escalate with what is available.
- `escalate` (observer=remote; tool=handoff package): Escalation required to L2/L3 for next corrective actions.

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Broad unavailability confirmed | `node_2` |
| `node_1` | `healthy` | Hospital-only symptom | `` |
| `node_1` | `inconclusive` | Unclear / unreadable evidence | `node_5` |
| `node_2` | `unhealthy` | Current service abnormality indicated | `node_5` |
| `node_2` | `inconclusive` | No current abnormality / only historical notes | `node_5` |
| `node_3` | `healthy` | Recovery completed and observable | `node_4` |
| `node_3` | `unhealthy` | Recovery cannot be performed or remains abnormal | `node_5` |
| `node_4` | `healthy` | Stable recovery confirmed | `` |
| `node_4` | `unhealthy` | Validation failure | `node_5` |
