# Stage 5 Playbook Candidate Review - Case 218550

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 1 |
| Nodes | 6 |
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

- playbook_candidate_incident_218550_bagout_agv_sequence node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_218550_bagout_agv_sequence node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_218550_bagout_agv_sequence node node_3 (branching_condition) is missing expects_capability
- playbook_candidate_incident_218550_bagout_agv_sequence node node_5 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_218550_bagout_agv_sequence | medium | 6 |  | Use when bag-out stops or progresses only partially and the site reports that an AGV is not moving, robots are out of sequence, a pair is not exchanging, or a related HMI shows... |

## Candidate Details

### Troubleshoot bag-out stoppage with abnormal AGV or task sequencing

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_218550_bagout_agv_sequence |
| Goal | Determine whether an observable AGV, pairing, sequence, tote, or task condition is preventing bag-out from progressing; guide authorized recovery; and confirm that robots and bag-out operation return to a stable state. |
| Entry symptoms | Bag-out stops after sorting or does not progress to completion.; The site must manually bag out.; One or more AGVs or robots are not moving for an extended period.; The site reports a robot out of sequence or out of position.; Bag-out starts after an AGV-pair change but stops again.; A hospital-area HMI reports a fault or a stuck task is visible there. |
| Tentative internal patterns | Possible AGV sequence, pairing, roster, or position inconsistency; Possible robot task or command remaining stuck; Possible tote or hospital-workflow state mismatch; Possible AGV availability or low-battery interruption |
| Affected systems/components | Bag-out workflow; AGV / robot fleet; AGV pairs and sequence state; RMS; Hospital HMI; AVEVA screen visibility context; Tote and task workflow |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | medium |
| Confidence reason | The incident provides clear entry symptoms, named diagnostic surfaces, high-level recovery actions, and a successful validation outcome. Confidence is reduced because the exact failed component and decisive recovery action are not isolated, several OCR excerpts are ambiguous, and the HMI location wording conflicts with the authoritative ingestion site metadata. |

**Summary:** Use when bag-out stops or progresses only partially and the site reports that an AGV is not moving, robots are out of sequence, a pair is not exchanging, or a related HMI shows a fault.

#### Support User Language Examples

- Bag-out stopped
- Bag-out won't finish
- We are manually bagging out
- An AGV hasn't moved
- Robot is out of sequence
- Robots are out of position
- The pair is not exchanging
- Bag-out started then stopped
- Hospital HMI is showing a fault
- There may be a stuck task

#### Negative Or Absent Signals

- No confirmed single failed robot, task, tote, or root cause is established in the incident.
- No confirmed stack-light fault was reported during at least one bag-out observation.
- The exact decisive recovery action is not isolated in the source.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm bag-out stoppage and affected operational pattern | Confirm whether bag-out is stalled or only partially progressing and whether the observable pattern includes AGV inactivity, sequence or pairing concerns, or a related HMI fault. | aud:operator, aud:L1_support | Procedure needed to confirm with the site whether the affected bag-out flow is stopped or only partially progressing, whether manual bagging is being used, whether AGVs are actively routing to the affected workflow, and whether the issue began with a robot, pair, tote, or HMI observation. In RMS, check the fleet activity or status view for the affected operational area without relying on incident-specific robot identifiers. | The case subject and site messages describe a bag-out stoppage after sorting, manual bagging, and a robot believed to be out of sequence. The RMS artifact and related message re... |
| 2 | diagnostic_decision | Determine whether an AGV active error or abnormal fleet state is present | Determine whether an AGV, robot, or system active-error condition correlates with the bag-out stoppage. | aud:operator, aud:L1_support | Procedure needed to inspect the RMS fleet and activity views for active AGV faults, prolonged inactivity, unavailable robots, and abnormal status associated with the affected bag-out flow, and to review the source-named system active-error view when available. The procedure should define how to interpret an active error versus an unavailable or merely idle robot without prescribing commands. | Support reported checking activity and finding an AGV that had not moved for three hours, while the discussion also referred to checking system active error because the Aveva sc... |
| 3 | branching_condition | Check for sequence, pair, tote, or task-state evidence | Distinguish an AGV sequence or pairing concern from a tote or task condition visible through the hospital-area HMI. | aud:operator, aud:L1_support | Decision-rubric procedure needed to compare the site-reported sequence or pairing concern with the hospital HMI's visible fault or task state, the tote identity and physical location, and the RMS activity observation. The procedure should define when a reported HMI fault or tote mismatch is relevant to bag-out and when it should be treated as unconfirmed. | The source reports a tote read at the hospital while physically elsewhere, a hospital HMI fault, a stuck task visible only on that HMI, and a suspected robot out-of-sequence con... |
| 4 | procedure_reference | Apply authorized recovery for the identified AGV or sequence condition | Use the approved recovery path appropriate to the confirmed condition, such as restoring robot availability, correcting an AGV pair or sequence state, or handling a confirmed task or HMI condition. | aud:operator, aud:L2_support | Procedure needed for the authorized recovery path selected from the diagnostic evidence, including applicable AGV pair remove/add or replacement handling, robot availability and battery prerequisites, hospital HMI fault acknowledgement or retry when authorized, and any approved stuck-task recovery boundaries. The procedure must define role limits and must not assume that a specific robot or root cause has been confirmed. | The incident records robots being turned off because of low batteries, later turned back on, AGV pairs being removed and added, and advice to acknowledge and retry an HMI fault.... |
| 5 | validation_gate | Validate restored sequence and sustained bag-out operation | Confirm that robots are functional, the relevant sequence is stable, and bag-out completes or continues normally without immediate recurrence. | aud:operator, aud:L1_support | Procedure needed to validate the recovered workflow by observing bag-out progress, confirming robot movement and sequence through the RMS activity/status view when available, checking that any relevant HMI fault or task indication is cleared, and obtaining site confirmation that automated operation remains functional before declaring recovery. | The source states that with all robots in proper sequence the customer confirmed they were functional. It also records a temporary bag-out restart followed by another stop, so s... |
| 6 | escalation_gate | Stop and escalate when the supported path does not restore stable operation | Hand off when the abnormal state cannot be identified, authorized recovery is unavailable or unsuccessful, or validation fails after the supported troubleshooting path. | aud:L1_support, aud:L2_support | Procedure needed to prepare an escalation handoff with RMS activity and active-error evidence, HMI fault or stuck-task evidence, bag-out behavior, AGV sequence or pair changes attempted, robot power or availability observations, tote observations, validation results, and the limits or authorization constraints that prevented further action. | The source records that available troubleshooting options were exhausted at one point, that a prior pair adjustment only temporarily restored bag-out, and that the HMI/task issu... |

#### Extraction Notes

- Ingestion metadata is authoritative for site assignment: UPS Haslet TX (TXRTH), site code ups_haslet_tx.
- Evidence text alternates among UPS Haslet, UPS Fort Worth, TX (Haslet), and a hospital reference. The hospital wording is preserved as an operational area or interface reference, not substituted for the ingestion site.
- The suspected robot out-of-sequence condition is not confirmed diagnosis.
- The exact AGV identifier in the RMS artifact is not readable.
- The exact decisive recovery action is not isolated; pair changes, robot power-state changes, HMI acknowledgement/retry, and sequence restoration are all recorded but not causally separated.
- The HMI and technical screenshot artifacts are partly unreadable, so detailed status interpretation is not inferred.
