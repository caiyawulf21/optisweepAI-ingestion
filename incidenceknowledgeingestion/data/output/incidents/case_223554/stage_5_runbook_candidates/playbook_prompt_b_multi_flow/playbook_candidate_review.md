# Stage 5 Playbook Candidate Review - Case 223554

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 2 |
| Nodes | 10 |
| Nodes missing runbook placeholder | 0 |
| Validation errors | 0 |
| Warnings | 6 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
| Candidates with events | 0 |

## Confidence

| Confidence | Count |
| --- | --- |
| high | 1 |
| medium | 1 |

## Warnings

- playbook_candidate_incident_223554_hospital_tote_induction node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_223554_hospital_tote_induction node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_223554_hospital_tote_induction node node_4 (validation_gate) is missing expects_capability
- playbook_candidate_incident_223554_site_sort_unavailable node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_223554_site_sort_unavailable node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_223554_site_sort_unavailable node node_4 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_223554_hospital_tote_induction | high | 5 |  | Troubleshoot a hospital-station flow where totes cannot be added or inducted, especially when tote removal still works or an AGV appears in an unexpected location. |
| playbook_candidate_incident_223554_site_sort_unavailable | medium | 5 |  | Troubleshoot a broad operational outage where the site cannot start sort or stops during sort, with possible server or service abnormality and subsequent recovery validation. |

## Candidate Details

### Hospital station cannot add or induct totes

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_223554_hospital_tote_induction |
| Goal | Determine whether the hospital induction failure is associated with an abnormal AGV location, roster state, or tote association, then guide authorized recovery and validate that hospital tote add and remove operations work again. |
| Entry symptoms | The hospital station cannot add or induct totes.; Totes can be removed but cannot be added at the hospital.; A robot or AGV is reported in a shut down state.; An AGV appears not to belong in the displayed location, or two AGVs appear under the same rack or in the same zone.; Hospital backlog or tote flow disruption is reported. |
| Tentative internal patterns | Possible AGV-to-tote association left behind after AGV removal; Possible AGV roster, location, or rack-position mismatch; Possible hospital-station service or server abnormality |
| Affected systems/components | ACB hospital station; AGV hospital station; AGVs and robot roster/location state; Tote associations; Hospital lane; API dog / Aveva recovery interfaces |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | high |
| Confidence reason | The packet repeatedly documents hospital inability to add or induct totes, AGV location and tote-association anomalies, high-level corrective actions, and successful validation that totes could again be added and removed. |

**Summary:** Troubleshoot a hospital-station flow where totes cannot be added or inducted, especially when tote removal still works or an AGV appears in an unexpected location.

#### Support User Language Examples

- Hospital can't add totes
- Cannot induct at hospital
- Totes can come out but not go in
- Hospital tote add is not working
- AGV is in the wrong spot
- Two AGVs are under the rack
- Robot is shut down
- Hospital is backed up

#### Negative Or Absent Signals

- The packet does not establish that the entire site is down for every occurrence of this symptom.
- The packet does not confirm a single root cause; the removed-AGV and associated-tote explanation is explicitly presented as a possibility.
- The packet does not provide a confirmed live alarm code or exact service state for the hospital station.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm the hospital induction symptom and current AGV/tote context | Confirm whether the reported failure is specifically inability to add or induct totes at the hospital station and whether an affected AGV, rack position, or associated tote appears abnormal. | aud:operator, aud:L1_support | Procedure needed to interview the site about whether the affected hospital station can add and remove totes, inspect the Hospital HMI or other source-evidenced hospital layout view for the affected station, and compare the displayed AGV placement and tote association with the operator's physical observation. | The source reports that the site could remove totes but could not add them, and shows an annotated HMI-style layout in a discussion of an AGV being in the wrong location. |
| 2 | diagnostic_decision | Determine whether AGV and tote state is inconsistent | Determine whether an AGV removal, unexpected location, duplicate rack occupancy, or disconnected tote association is present and plausibly connected to the hospital induction symptom. | aud:L1_support, aud:L2_support | Procedure needed to inspect the hospital rack or AGV layout view and, where authorized, the API dog or Aveva-fed AGV and tote state for unexpected AGV placement, duplicate location occupancy, removed-AGV residue, or disconnected tote association; the procedure should define how to record evidence without changing state. | The packet repeatedly discusses an AGV in the wrong location, multiple AGVs under a rack, a disconnected tote, and use of API dog or Aveva to correct AGV and tote state. |
| 3 | procedure_reference | Apply authorized correction for supported AGV or tote-state mismatch | Use an authorized, source-supported recovery procedure to correct the affected AGV or tote state when the diagnostic evidence identifies a supported mismatch. | aud:operator, aud:L1_support | Procedure needed for authorized AGV and tote-state correction using the source-evidenced Aveva or API dog interface, including safety prerequisites, role limits, handling of an inducted or disconnected tote, and evidence capture; exact API actions and screen steps belong in the procedure. | The source reports high-level use of API dog and Aveva to remove totes, remove an AGV from a zone, and add a tote to a station; it does not provide the exact procedure. |
| 4 | validation_gate | Validate hospital tote flow and AGV recovery | Confirm that the hospital station accepts totes again and that the affected AGV and tote state no longer prevents normal flow. | aud:operator, aud:L1_support | Procedure needed to validate hospital-station tote add and remove behavior, confirm the affected AGV roster or location state through the source-evidenced hospital or AGV view, and monitor for continued backlog or recurrence before declaring the hospital flow recovered. | The source reports restoration of adding and removing totes and that all robots were re-added and running. |
| 5 | escalation_gate | Stop if hospital-state correction is unsupported or validation fails | Hand off when the hospital tote or AGV state cannot be safely identified or the approved correction does not restore hospital tote flow. | aud:L2_support, aud:L3_support | Procedure needed to prepare an escalation handoff containing hospital HMI or layout evidence, AGV and tote association observations, API dog or Aveva action results, validation results, and clear stop criteria; the handoff procedure must identify the role authorized to continue. | The packet documents uncertain cause, unreadable artifacts, and high-level state-correction actions without a complete supported procedure. |

#### Extraction Notes

- Ingestion metadata is authoritative for site: UPS Haslet TX (TXRTH), site_code ups_haslet_tx.
- Evidence text also uses UPS Fort Worth, TX (Haslet) and a Fort Worth address; this appears compatible with the ingestion site but is preserved as an ambiguity.
- The removed-AGV and associated-tote explanation is a tentative internal pattern, not confirmed root cause.
- Several screenshots are low resolution or unreadable; branches require confirmation from current observable state.

### Site cannot start or sustain sort

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_223554_site_sort_unavailable |
| Goal | Determine whether the report represents a site-wide sort availability problem, assess the source-supported service or server recovery direction, and validate stable operation without treating the historical service hypothesis as confirmed cause. |
| Entry symptoms | The site is reported down.; The site cannot start sort.; The site goes down in the middle of sort.; Movement stops or the system is not running.; A work-order or repair note reports AGV hospital-station server issues and a need to reset services. |
| Tentative internal patterns | Possible OptiSweep or AGV-server service abnormality; Possible service reset and Hospital Lane restart recovery path; Possible broader operational effect from unresolved hospital AGV or tote state |
| Affected systems/components | Site-wide sort operation; OptiSweep services; AGV hospital station server; Hospital Lane; AGVs and tippers |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | medium |
| Confidence reason | The packet clearly documents site-down and sort-start failure reports, server/service-reset notes, a high-level OptiSweep service reset and Hospital Lane restart, and later reports that movement and the system resumed. Exact service diagnosis and validation evidence are incomplete. |

**Summary:** Troubleshoot a broad operational outage where the site cannot start sort or stops during sort, with possible server or service abnormality and subsequent recovery validation.

#### Support User Language Examples

- Site is down
- Can't start sort
- Sort went down
- We went down in the middle of sort
- Nothing is moving
- System is not running
- AGV server is having issues
- Services need to be reset

#### Negative Or Absent Signals

- The packet does not identify the application represented by the color-coded grid screenshot.
- The packet does not provide a confirmed service name, event ID, or live Windows service state.
- The packet does not establish that the server or service condition was the sole cause of the site-wide disruption.
- The hospital-specific tote and AGV anomalies may coexist with, precede, or contribute to the broader outage; their relationship is not confirmed.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm site-wide sort unavailability | Determine whether the report is a broad inability to start or sustain sort rather than only a localized hospital-station symptom. | aud:operator, aud:L1_support | Procedure needed to confirm with the site whether sort is unavailable across the operation, whether movement stopped or only the hospital flow is affected, and whether the available site status or dashboard view shows a readable down or running state; do not infer the meaning of unreadable color cells. | The source reports that the site was down and could not start sort or went down in the middle of sort; the associated dashboard screenshot is not readable enough to interpret in... |
| 2 | diagnostic_decision | Check for source-supported service or server abnormality | Determine whether the broad outage correlates with the documented AGV hospital-station server or service abnormality. | aud:L1_support, aud:L2_support | Procedure needed to inspect the AGV hospital-station server or OptiSweep service state using the named service evidence available in the case, including Windows Services or Event Viewer only if the current diagnostic artifact identifies those views, and to distinguish a live service fault from a historical notes entry. | The case artifacts and closure details mention AGV hospital-station server issues, services needing reset, and later reset of OptiSweep services, but do not show the live servic... |
| 3 | procedure_reference | Perform authorized service or lane recovery | Use the approved procedure for the documented service or Hospital Lane recovery path when the responsible role confirms that it is authorized and supported. | aud:L1_support, aud:operator | Procedure needed for authorized recovery of the source-named OptiSweep services and Hospital Lane, including operational safety preconditions, role limits, service-state evidence, and post-recovery checks; exact restart steps and commands belong in the runbook. | The closure summary says OptiSweep services were reset and the site restarted Hospital Lane; the packet does not provide exact steps. |
| 4 | validation_gate | Validate stable sort and movement recovery | Confirm that the site can start or sustain sort and that movement remains active after service or lane recovery. | aud:operator, aud:L1_support | Procedure needed to validate OptiSweep or service responsiveness, confirm Hospital Lane and site sort operation, observe sustained movement, and check for recurrence after recovery; the validation procedure should define the monitoring interval and evidence to retain without prescribing exact screen navigation. | The packet reports that movement started and the system was running, while the earlier symptom was inability to start or sustain sort. |
| 5 | escalation_gate | Stop if service recovery or sort validation fails | Hand off when the service or server condition cannot be confirmed, authorized recovery does not restore operation, or the site remains unable to start or sustain sort. | aud:L2_support, aud:L3_support | Procedure needed to prepare escalation evidence including service or server observations, Event Viewer or Windows Services evidence when available, sort availability reports, Hospital Lane state, recovery actions attempted, and validation results, with stop criteria and the receiving technical role. | The source contains incomplete service evidence, an unreadable dashboard artifact, and a site-wide outage that eventually recovered through multiple actions. |

#### Extraction Notes

- Ingestion metadata is authoritative for site: UPS Haslet TX (TXRTH), site_code ups_haslet_tx.
- Evidence text also uses UPS Fort Worth, TX (Haslet) and a Fort Worth address; this appears compatible with the ingestion site but is preserved as an ambiguity.
- The service/server condition is source-supported context, not confirmed root cause.
- The color-coded status screenshot is unreadable and must not drive a specific branch without current corroborating evidence.
