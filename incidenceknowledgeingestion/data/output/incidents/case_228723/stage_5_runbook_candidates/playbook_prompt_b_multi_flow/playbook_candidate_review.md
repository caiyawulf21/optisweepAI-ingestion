# Stage 5 Playbook Candidate Review - Case 228723

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 1 |
| Nodes | 6 |
| Nodes missing runbook placeholder | 0 |
| Validation errors | 0 |
| Warnings | 1 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
| Candidates with events | 0 |

## Confidence

| Confidence | Count |
| --- | --- |
| medium | 1 |

## Warnings

- playbook_candidate_incident_228723_zone5_pairing_hospital_diversion_after_robot_change is missing candidate-level source_refs

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228723_zone5_pairing_hospital_diversion_after_robot_change | medium | 6 |  | Use this candidate when a site reports a zone cannot get a pair and AMRs begin going to the hospital after a recent AMR replacement, add, or remove/add attempt. The incident sug... |

## Candidate Details

### Zone cannot get a pair and AMRs divert to hospital after recent robot replacement or remove/add activity

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228723_zone5_pairing_hospital_diversion_after_robot_change |
| Goal | Restore normal pairing and fleet movement when a zone-level pairing complaint is accompanied by hospital diversion behavior after recent robot handling changes, without assuming the exact root cause in advance. |
| Entry symptoms | Site reports the ACB system is down; A specific zone, especially zone 5 in this incident, is unable to get a pair; After an AMR with low battery or an AMR replacement attempt, AMRs begin going to the hospital lane; The issue appears after the site attempted to add, remove, or replace one or more AGVs or AMRs |
| Tentative internal patterns | Recent AMR remove/add or replacement activity may correlate with abnormal fleet roster or mapping state in RMS; A single robot in an abnormal state may block or disrupt broader zone behavior until isolated from the active system; Improper remove/add handling through the hospital flow was discussed as a possible contributing pattern; Unmapped or improperly added robots were discussed as a recurring prior-call pattern |
| Affected systems/components | ACB system; AMR/robot fleet; RMS; Zone 5 pairing behavior; Hospital lane / hospital workflow |
| Roles | L1_support, L2_support, L3_support |
| Confidence | medium |
| Confidence reason | The incident provides a coherent troubleshooting shape and a reported recovery action tied to robot 158 being removed after being shown as not mapped. Confidence is reduced because several details are speculative, screenshots are partially unreadable, and the evidence does not provide a fully explicit reusable decision rubric. |

**Summary:** Use this candidate when a site reports a zone cannot get a pair and AMRs begin going to the hospital after a recent AMR replacement, add, or remove/add attempt. The incident suggests checking whether recent fleet changes left one or more robots in an abnormal RMS roster or mapping state, then using an approved robot-isolation or removal procedure and validating that pairing and fleet behavior return to normal.

#### Support User Language Examples

- Zone 5 is unable to get a pair
- Every AMR goes to the hospital
- They had a low battery AMR under the rack and replaced it
- They may not have removed and added it properly
- Robot 158 was shown as not mapped

#### Negative Or Absent Signals

- The low-battery condition was discussed as the event that started the problem, but source discussion explicitly suggested it was not the current issue
- No direct source evidence confirms a service crash, gateway outage, or API failure
- RMS screenshots are not legible enough to confirm exact table values or alarms from the images alone

#### Nodes

| # | Type | Title | Intent | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm the pairing-failure and hospital-diversion symptom pattern | Determine whether the current incident matches the observable pattern of a zone unable to get a pair after recent robot handling changes, with AMRs diverting to the hospital. | Procedure needed to confirm with the site which specific zone cannot get a pair, whether AMRs are actively going to the hospital lane, whether a low-battery robot was recently found under the rack, and whether the site recently replaced, added, or removed any AMRs. In RMS, inspect the fleet or zone-related views that can corroborate abnormal hospital-diversion behavior and recent robot roster changes. | The site reported zone 5 was unable to get a pair; earlier issues involved a low-battery AMR under the rack; after replacement attempts, AMRs were going to the hospital. |
| 2 | branching_condition | Check whether recent remove/add or replacement activity is part of the incident context | Choose the next troubleshooting direction based on whether the symptom pattern follows recent robot replacement, add, or remove/add handling. | Procedure needed to review recent site-reported robot handling history and any RMS evidence of recent add, remove, replacement, or hospital-flow activity for specific robot IDs, including how to distinguish a fresh fleet-change issue from an unrelated zone fault. | Support discussion suggested the issue sounded related to attempted replacement AMRs and that the site had tried adding two AGVs. |
| 3 | diagnostic_decision | Inspect RMS for abnormal robot roster or mapping state tied to the incident | Determine whether one or more robots involved in the recent change appear abnormal in RMS, such as not mapped, improperly rostered, or otherwise inconsistent with normal tasking behavior. | Procedure needed to inspect RMS fleet, roster, and mapping-related views for the specific robots involved in the recent change, including how to identify signs such as not mapped, abnormal roster state, inability to receive tasks, or other exception indicators for named robot IDs. | Support discussion suggested robots may not have been removed and added properly and later resolution notes stated robot 158 was shown as not mapped. |
| 4 | procedure_reference | Perform approved isolation or removal of the suspect robot from the active system | If RMS and incident context support a suspect robot as the likely blocker, perform the authorized robot-isolation or removal action rather than continuing to operate it in the active fleet. | Procedure needed for authorized isolation or removal of a specific robot from the active RMS-managed fleet, including any required hospital-flow handling, charging-state considerations, safety preconditions, and role limits for leaving the unit out of service for the remainder of operations if appropriate. | Support discussion suggested there might be an easier workaround and to leave the unit out for the rest of the sort; the reported recovery action was removal of robot 158 from t... |
| 5 | validation_gate | Validate that pairing and fleet behavior have returned to normal | Confirm that the zone can pair again and that AMRs are no longer broadly diverting to the hospital after the suspect robot is isolated. | Procedure needed to validate recovery in RMS and with the site by checking that the affected zone can obtain pairs again, that AMRs are no longer broadly routing to the hospital lane, that the suspect robot remains isolated as intended, and that operations remain stable during a defined monitoring period. | The site believed removing robot 158 may have fixed the issue; later update said the system began functioning again and remained operational during monitoring. |
| 6 | escalation_gate | Stop and escalate if supported fleet-state checks do not identify a safe recovery path or validation fails | Hand off when the observable symptom pattern persists but the available RMS checks do not clearly identify a supported robot-isolation path, or when the issue remains after the approved action. | Procedure needed to prepare escalation evidence for higher-tier fleet or engineering review, including the site symptom summary, affected zone, robot IDs recently added or removed, RMS fleet and mapping screenshots or exports for the suspect robots, notes on hospital-diversion behavior, and results of any approved isolation or validation steps already attempted. | Support discussion suggested limited options if robots were not properly rostered in RMS, and the case status was escalated during the incident before recovery was confirmed. |

#### Extraction Notes

- The candidate is entered from observable symptoms rather than the internal label of 'not mapped' or 'improper remove/add'.
- Robot 158 removal is represented as a procedure reference, not as a guaranteed fix.
- The incident suggests but does not prove that improper remove/add handling caused the outage.
- RMS is named because the incident explicitly references RMS and shows RMS screenshots, even though screenshot detail is partially unreadable.
