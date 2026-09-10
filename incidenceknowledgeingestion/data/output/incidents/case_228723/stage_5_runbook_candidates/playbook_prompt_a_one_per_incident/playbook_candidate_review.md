# Stage 5 Playbook Candidate Review - Case 228723

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 1 |
| Nodes | 5 |
| Nodes missing runbook placeholder | 0 |
| Validation errors | 0 |
| Warnings | 3 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
| Candidates with events | 0 |

## Confidence

| Confidence | Count |
| --- | --- |
| medium | 1 |

## Warnings

- playbook_candidate_incident_228723_agv_pairing_roster_recovery node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228723_agv_pairing_roster_recovery node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228723_agv_pairing_roster_recovery node node_4 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228723_agv_pairing_roster_recovery | medium | 5 |  | Use this path when a site reports that an ACB or zone cannot obtain an AMR pair, multiple AMRs route unexpectedly, or the system appears down after an AMR replacement or add/rem... |

## Candidate Details

### AMR pairing failure with abnormal fleet roster or mapping state

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228723_agv_pairing_roster_recovery |
| Goal | Determine whether the pairing failure is associated with an abnormal AMR roster or mapping state, use an authorized site-side isolation or removal procedure when supported, and confirm that normal pairing and operation return. |
| Entry symptoms | A site reports that an ACB or affected zone cannot get a pair.; The ACB system is described as down or production is seriously impacted.; Replacement AMRs reportedly route to the hospital lane instead of supporting the affected workflow.; An AMR was previously reported with low battery or in an abnormal physical location.; The issue follows an AMR replacement, add, or remove activity. |
| Tentative internal patterns | Possible abnormal AMR roster or mapping state after add/remove activity; Possible robot-location or pairing inconsistency affecting task assignment; Possible residual abnormal state after an earlier low-battery or physically inaccessible AMR event |
| Affected systems/components | ACB system; AMRs / AGVs; RMS; Hospital lane; Affected zone pairing workflow |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | medium |
| Confidence reason | The packet contains a clear observable symptom, a named RMS surface, discussion of possible roster/add-remove behavior, a source-supported site removal action, and reported recovery. Confidence is limited because the RMS details are partly unreadable, recovery was reported rather than independently measured, and the source contains inconsistent ACB/ECB naming. |

**Summary:** Use this path when a site reports that an ACB or zone cannot obtain an AMR pair, multiple AMRs route unexpectedly, or the system appears down after an AMR replacement or add/remove event.

#### Support User Language Examples

- Zone can't get a pair
- ACB system is down
- AMRs are going to the hospital
- The robot was replaced and nothing is pairing
- AGV was added but it is not getting a task
- Robot is not mapped
- Robots are not working after an add/remove

#### Negative Or Absent Signals

- The source does not independently establish that low battery was the current cause.
- The source does not provide readable RMS status values or a confirmed error code.
- The source does not independently validate recovery through live telemetry.
- No authoritative site location metadata was supplied in source_package.site_location.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm the observable pairing and routing pattern | Determine whether the site is experiencing an active pairing failure with abnormal AMR routing or behavior after a replacement or add/remove event. | aud:operator, aud:L1_support | Procedure needed to interview the site about the affected zone's pairing availability, intended AMR routing, recent replacement or add/remove activity, and current physical robot behavior; this is an evidence-collection and interpretation aid, not a case-intake procedure. | The source records site-reported inability to get a pair, replacement AMRs going to the hospital lane, and earlier low-battery and robot-location circumstances. |
| 2 | diagnostic_decision | Check fleet roster and mapping state | Determine whether RMS shows an abnormal robot membership, mapping, or status condition that could explain the pairing failure. | aud:operator, aud:L1_support | Procedure needed to inspect the RMS fleet or robot status view for roster membership, mapping, location, and exception indicators associated with the affected workflow, and to interpret whether the displayed state is consistent with normal pairing. | The source identifies RMS as the system used to view robot status and states that a removed robot was shown as not mapped; the artifact shows red-highlighted RMS table entries. |
| 3 | procedure_reference | Use an authorized site-side robot isolation or removal path | If an abnormal roster or mapping condition is supported, use the approved site procedure to isolate or remove the affected robot from the operating system and place it in a safe non-operational state. | aud:operator | Procedure needed for authorized site-side AGV physical isolation and system removal, including safety prerequisites, handling of a robot in an abnormal location, charger placement, and confirmation of the corresponding RMS state; exact removal or handling steps belong in the runbook. | The incident reports site-side removal of a robot from the system and placement on a charger, followed by reported system recovery. |
| 4 | validation_gate | Confirm pairing and operational stability | Determine whether the affected workflow has recovered after the authorized robot isolation or removal action. | aud:operator, aud:L1_support | Procedure needed to validate pairing availability through site observation and to review the RMS fleet or robot status view for persistent abnormal membership, mapping, or exception indicators during a defined monitoring period. | The source reports that the system began functioning after robot removal and remained operational during approximately ten minutes of monitoring, while acknowledging that the re... |
| 5 | escalation_gate | Stop when the supported roster-recovery path is unsafe or unsuccessful | Hand off when the abnormal state cannot be safely isolated, the available evidence is inconclusive, or pairing and stable operation do not return after the supported path. | aud:L2_support, aud:L3_support | Procedure needed to prepare an escalation handoff containing the site-observed pairing and routing symptoms, RMS screenshots or status evidence, physical robot state, actions attempted, authorization constraints, and validation results; it must define stop criteria without prescribing case-management or communication workflow. | The incident record shows incomplete and partly conflicting evidence, including unreadable RMS details, a delayed recovery report, and unresolved ambiguity about the cause. |

#### Extraction Notes

- Exactly one candidate was produced for the incident packet.
- source_package.site_location is empty; no ingestion site, site_code, or site_label was populated from that metadata.
- The canonical record identifies UPS Fort Worth, TX (Haslet), but this candidate does not place that incident-specific site name in reusable node fields.
- The source alternates between ACB and ECB naming; this ambiguity is preserved rather than resolved.
- RMS screenshots contain unreadable or garbled details. Red entries are treated only as possible exception indicators.
- The source supports a tentative roster or mapping pattern and a reported recovery after robot removal, not a confirmed root cause.
- No ontology-backed WCS SQL, API, service, or database evidence was used because those surfaces were not established by the incident evidence as the historical troubleshooting surface.
- The later CBRE work-order artifact and case-management history were excluded from the technical path.
