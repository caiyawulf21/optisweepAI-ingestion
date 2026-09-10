# Stage 5 Playbook Candidate Review - Case 223554

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 1 |
| Nodes | 5 |
| Nodes missing runbook placeholder | 0 |
| Validation errors | 0 |
| Warnings | 4 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
| Candidates with events | 0 |

## Confidence

| Confidence | Count |
| --- | --- |
| medium | 1 |

## Warnings

- playbook_candidate_incident_223554_hospital_induct_flow node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_223554_hospital_induct_flow node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_223554_hospital_induct_flow node node_3 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_223554_hospital_induct_flow node node_5 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_223554_hospital_induct_flow | medium | 5 |  | Use this path when a hospital station cannot add or induct totes, a robot appears shut down, or the site cannot start or sustain sort. Confirm the observable impact, check for A... |

## Candidate Details

### Hospital tote-induct or site-flow disruption with AGV state anomalies

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_223554_hospital_induct_flow |
| Goal | Restore safe hospital tote flow and broader site operation by distinguishing a localized hospital workflow problem from an AGV/tote-state or service-related disruption, applying only authorized high-level recovery actions, and validating stable operation. |
| Entry symptoms | Hospital station cannot add or induct totes.; Totes can be removed but cannot be added at the hospital area.; A robot or AGV is reported in a shut down state.; The site cannot start sort or goes down during sort.; Hospital backlog or abnormal tote flow to the hospital area is reported. |
| Tentative internal patterns | Possible hospital tote-association inconsistency after AGV removal without associated-tote removal.; Possible AGV roster, location, or rack-state inconsistency.; Possible AGV hospital-station server or OptiSweep service abnormality.; Possible downstream tote-flow disruption associated with tipper operation during recovery. |
| Affected systems/components | ACB hospital station; Hospital Lane; AGV hospital station; AGVs and robot locations; Totes and tote associations; OptiSweep services; Tippers; Sort operation |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | medium |
| Confidence reason | The packet contains a clear symptom-to-diagnostic-to-recovery shape, including hospital induct failure, AGV/tote anomalies, service-reset context, API/Aveva-based recovery references, and validation reports. Confidence is limited by fragmented chronology, second-hand statements, unreadable screenshots, and uncertainty about the actual cause and exact service actions. |

**Summary:** Use this path when a hospital station cannot add or induct totes, a robot appears shut down, or the site cannot start or sustain sort. Confirm the observable impact, check for AGV location or tote-association anomalies, consider the source-supported service and lane recovery path, and validate tote flow and site operation.

#### Support User Language Examples

- Hospital can't induct totes
- Hospital can't add totes
- They can remove totes but cannot add
- AGV is shut down
- AGVs are in the wrong location
- There are two AGVs under the rack
- Site is down
- Sort won't start
- Nothing is moving
- System is running now

#### Negative Or Absent Signals

- The source does not provide a confirmed root cause.
- The source does not provide readable live service-status values or named service states.
- The source does not establish that every reported AGV location anomaly caused the site-wide disruption.
- Several screenshots have unreadable labels or ambiguous color meanings.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm the observable hospital and site-flow impact | Determine whether the current report is an active hospital tote-induct problem, a broader sort disruption, or a localized condition that does not match this response path. | aud:operator, aud:L1_support | Procedure needed to confirm with the site whether totes can be added and removed at the affected hospital station, whether the reported robot or station is shut down, whether sort can start or remain running, and what the Hospital HMI or related HMI view visibly reports. | The case subject and closure summary describe inability to induct totes, while Teams messages describe inability to add totes and a later site-down or sort-start failure. |
| 2 | diagnostic_decision | Check for AGV location, roster, and tote-association anomalies | Determine whether the reported hospital-flow problem coincides with an AGV in an unexpected location, duplicate occupancy, disconnected tote, or residual tote association. | aud:operator, aud:L1_support, aud:L2_support | Procedure needed to compare the affected AGV or robot location and rack occupancy with the expected fleet or station state using the source-referenced HMI/layout view, the source-supported operational view or fleet status view, and API/Aveva state view when available; the procedure should also identify residual or disconnected tote associations without prescribing data mutations. | Teams messages and annotated HMI-style images describe an AGV in an unexpected location, two AGVs under a rack, and possible disconnected or residual tote associations. |
| 3 | diagnostic_decision | Determine whether the hospital-station service condition is contributing | Determine whether the reported AGV hospital-station server or OptiSweep service condition is present and sufficiently correlated with the hospital or site-flow symptoms. | aud:L1_support, aud:L2_support | Procedure needed to review the incident's AGV hospital-station and OptiSweep service evidence, inspect Windows Event Viewer and Windows Services for current service health when access is authorized, and correlate that state with Hospital Lane or HMI responsiveness without assuming that the historical reset note proves a current fault. | The source documents AGV hospital-station server issues, a need to reset services, and a closure statement that OptiSweep services were reset before Hospital Lane was restarted. |
| 4 | procedure_reference | Apply authorized high-level recovery for the identified condition | Use the approved recovery procedure appropriate to the confirmed condition: service or lane recovery, correction of supported AGV/tote state, or controlled physical AGV handling. | aud:L2_support, aud:L3_support, aud:operator | Procedure needed for the authorized recovery path selected from the diagnosis: reset or recover the named OptiSweep or AGV hospital-station services and restart Hospital Lane when approved; alternatively use the approved API dog or Aveva procedure for supported tote or AGV state correction; include site safety controls, role limits, and conditions for any physical AGV removal. Exact commands, click paths, and mutation steps belong in the linked runbook. | Historical evidence describes service reset and Hospital Lane restart, API dog removal of tote state, Aveva-based AGV/tote state correction, and removal of several AGVs during r... |
| 5 | validation_gate | Validate hospital flow, AGV state, and sustained sort recovery | Confirm that recovery restored the affected workflow without leaving residual AGV, tote, or station-state anomalies. | aud:operator, aud:L1_support, aud:L2_support | Procedure needed to validate Hospital Lane and hospital HMI tote-add and tote-remove behavior, confirm AGV roster and location state through the source-used fleet or Aveva/API view, confirm relevant service responsiveness when applicable, and monitor sort long enough to distinguish stable recovery from a temporary movement indication. | The source reports that totes could again be added and removed, robots were re-added and running, movement started, and the system was running by the later recovery updates. |

#### Extraction Notes

- The authoritative ingestion site is UPS Haslet TX (TXRTH), site_code ups_haslet_tx. Evidence also uses UPS Fort Worth, TX (Haslet), Fort Worth address text, and TXRTH - Haslet Hub; these appear compatible but the naming ambiguity is preserved.
- The candidate merges the original hospital-induct issue and the later same-day site-down or sort disruption because the packet presents them as one case with related AGV, tote, service, and recovery evidence.
- The source explicitly states that the cause was uncertain. AGV/tote association, AGV location, and service-health patterns are tentative internal context only.
- The source contains conflicting or incomplete evidence about the exact recovery sequence. Service reset, Hospital Lane restart, API dog/Aveva state correction, and AGV removal are retained as alternative source-reported recovery branches rather than a single canonical procedure.
- The page 5 and page 15 artifacts are notes or work-order evidence, not confirmed live Windows Services screens; service-health checks therefore remain diagnostic capabilities rather than source-observed completed checks.
- Several screenshots are low-resolution or unreadable, so their colors and labels are not used as confirmed operational indicators.
- No ontology backend mappings were supplied for the exact hospital tote-induction state, disconnected tote state, or API dog/Aveva mutations.
