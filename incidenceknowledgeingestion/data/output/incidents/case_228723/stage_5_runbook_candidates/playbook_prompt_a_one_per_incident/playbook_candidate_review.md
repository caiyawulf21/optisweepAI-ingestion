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

- playbook_candidate_incident_228723_zone5_pairing_amr_roster_recovery is missing candidate-level source_refs

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228723_zone5_pairing_amr_roster_recovery | medium | 6 |  | Use this troubleshooting pattern when a site reports a zone cannot get a pair and AMRs begin diverting to the hospital lane after a low-battery robot event, replacement attempt,... |

## Candidate Details

### Zone unable to get a pair with AMRs diverting to hospital after recent robot replacement or remove/add activity

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228723_zone5_pairing_amr_roster_recovery |
| Goal | Restore normal zone pairing and fleet behavior by identifying whether a recently replaced, added, or abnormal robot should be isolated from active operation, then confirming the system remains operational after the corrective action. |
| Entry symptoms | Site reports the ACB system is down; A specific zone, especially zone 5 in this incident, is unable to get a pair; After a low-battery AMR event or replacement attempt, AMRs begin going to the hospital lane; The issue appears after recent robot replacement, remove/add, or attempted addition of one or more AGVs |
| Tentative internal patterns | Recent robot remove/add or replacement activity may have left one or more robots in an abnormal RMS roster or mapping state; A robot shown as not mapped may correlate with zone pairing failure and broad AMR diversion behavior; Leaving an affected robot out of service for the rest of the sort was discussed as a possible workaround shape |
| Affected systems/components | ACB system; AMR/robot fleet; RMS; Zone 5 pairing behavior; Specific robots discussed in incident evidence including robot 158 and robot 153 |
| Roles | L1_support, L2_support, L3_support |
| Confidence | medium |
| Confidence reason | The incident contains a coherent troubleshooting shape and a reported recovery action tied to robot 158 removal, but the evidence is partly chat-based, some OCR is degraded, and the exact RMS state and authorized recovery boundaries are not fully documented in the packet. |

**Summary:** Use this troubleshooting pattern when a site reports a zone cannot get a pair and AMRs begin diverting to the hospital lane after a low-battery robot event, replacement attempt, or recent robot remove/add activity. The response pattern is to confirm the observable fleet behavior, inspect RMS for abnormal robot roster or mapping state, use the approved robot isolation or remove-from-service procedure if an affected robot is identified and authorized, then validate that pairing and site operation recover during monitoring.

#### Support User Language Examples

- Zone 5 is unable to get a pair
- Every AMR goes to the hospital
- They had a low battery AMR under the rack
- They tried replacing or adding AGVs and now the system is acting up
- Removing robot 158 may have fixed it

#### Negative Or Absent Signals

- The low-battery condition itself was discussed as not necessarily being the current issue
- Evidence does not confirm a software service crash or gateway outage
- Evidence does not provide a confirmed database-only fix path
- RMS screenshots are not legible enough to confirm exact table values directly from the packet

#### Nodes

| # | Type | Title | Intent | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm the observable symptom pattern and recent robot-handling context | Determine whether the incident matches the pattern of zone pairing failure plus abnormal AMR hospital diversion after a recent low-battery event, replacement attempt, or robot remove/add activity. | Procedure needed to confirm with the site which specific zone cannot get a pair, whether AMRs are actively going to the hospital lane, whether a low-battery robot was recently under the rack, and whether the site recently replaced, removed, or added one or more robots. In RMS, check the fleet or zone-related views available to support for signs that the reported zone and robot activity align with the site description. | The site reported zone 5 unable to get a pair; earlier low-battery AMR issues were discussed; after replacement attempts, AMRs were reportedly going to the hospital lane. |
| 2 | diagnostic_decision | Inspect RMS for abnormal robot roster, mapping, charging, or stuck-state indicators tied to the affected zone | Determine whether one or more specific robots appear to be in an abnormal state that could explain the pairing failure and broad AMR diversion behavior. | Procedure needed to inspect RMS robot roster and status views for the affected site, including whether recently replaced or added robots appear not mapped, improperly rostered, not charging, stuck on tasks, not moving, or otherwise abnormal. The procedure should also cover how to correlate specific robot IDs with the affected zone and recent remove/add activity. | Support chat discussed improper remove/add handling, possible roster issues in RMS, robot 158 removal, and robot 153 still reporting no charging or possibly stuck. |
| 3 | branching_condition | Decide whether an identified robot should be isolated from active operation using an approved procedure | Choose whether to proceed with supported robot isolation or remove-from-system handling for a specific abnormal robot, or continue investigation if no supported target is identified. | Decision rubric needed to determine whether a specific robot identified in RMS can be safely isolated, left out of service for the rest of the sort, or removed from the system under an approved support procedure. The rubric should reference RMS evidence, recent remove/add history, charging state, mapping state, and role authorization limits. | Support discussed an easier way than deeper correction, including leaving the unit out for the rest of the sort, and later the site removed robot 158 from the system. |
| 4 | procedure_reference | Perform the approved robot isolation or remove-from-system recovery action | Use the authorized operational procedure to remove the identified abnormal robot from active fleet participation or otherwise keep it out of service when that is the supported recovery path. | Procedure needed for authorized robot isolation, remove-from-system handling, or equivalent supported recovery in RMS for a named robot, including any required safety preconditions, coordination with the site, charging or parking expectations, and limits on who may perform or direct the action. | The reported recovery action was removal of robot 158 from the system, with the robot then on charger. |
| 5 | validation_gate | Validate that pairing and fleet behavior recover and remain stable during monitoring | Confirm that the affected zone can pair again, AMRs are no longer broadly diverting to the hospital lane, and the site remains operational after the recovery action. | Procedure needed to validate post-recovery state in RMS and with the site, including checking that the affected zone can obtain pairs again, confirming AMRs are no longer broadly routing to the hospital lane, reviewing the fleet roster for remaining abnormal robots, and monitoring for a defined observation period before declaring recovery. | Support remained on the call to monitor and reported the system remained operational after robot 158 was removed. |
| 6 | escalation_gate | Stop and escalate if no supported abnormal-robot recovery path is identified or validation fails | Hand off when RMS review does not reveal a supported robot isolation target, when authorized recovery cannot be performed, or when the zone and fleet behavior do not stabilize after the attempted action. | Procedure needed to prepare escalation evidence for higher-tier support, including the site symptom summary, recent robot replacement or remove/add history, RMS roster and status evidence for the affected robot IDs, any signs of not-mapped or not-charging state, actions already attempted, and post-action validation results showing whether pairing and hospital-lane behavior recovered. | The incident included escalation and discussion that if robots were not properly rostered in RMS, available responders might have limited corrective options; however, the final... |

#### Extraction Notes

- Exactly one playbook candidate was returned per instruction.
- The candidate is framed from observable symptoms rather than a fixed internal label such as not-mapped robot or RMS roster mismatch.
- The packet supports a broad troubleshooting pattern around abnormal robot state after replacement or remove/add activity, but does not provide enough detail to encode exact recovery steps.
- Robot 158 removal is captured as a source-supported recovery reference, not as a universally confirmed root cause.
- CBRE and case-management details were excluded from nodes because they are administrative rather than troubleshooting orchestration.
