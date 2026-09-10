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
- playbook_candidate_incident_218550_bagout_agv_sequence node node_3 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_218550_bagout_agv_sequence node node_5 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_218550_bagout_agv_sequence | medium | 6 |  | Use this path when automated bag-out stops or progresses only partially and site personnel report that an AGV is not moving, a robot may be out of sequence, or a related HMI sho... |

## Candidate Details

### Bag-out stoppage with unresponsive or out-of-sequence AGVs

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_218550_bagout_agv_sequence |
| Goal | Determine whether the bag-out stoppage is associated with an abnormal AGV, pairing or sequence state, or an HMI-visible task or tote condition; apply only source-supported authorized recovery direction; and confirm that AGVs and bag-out remain functional. |
| Entry symptoms | Automated bag-out stops after sorting or starts and then stops before completion.; Manual bagging out is required because the automated process does not progress.; One or more AGVs or robots appear not to be moving.; The site reports that a robot may be out of sequence or out of position.; An HMI associated with the hospital area shows a fault or a task-related condition. |
| Tentative internal patterns | Possible AGV sequence, pairing, roster, or position inconsistency.; Possible stuck task or tote association condition visible on an HMI.; Possible AGV inactivity or active-error condition.; Possible prior robot removal or replacement without a corresponding replacement in the operating sequence. |
| Affected systems/components | Bag-out stage; AGV / robot fleet; AGV pairing or sequence state; RMS; Hospital-area HMI; Tote or task handling workflow; AVEVA screen visibility context |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | medium |
| Confidence reason | The packet contains a clear observable symptom, repeated AGV-related troubleshooting observations, source-supported pairing and sequence recovery direction, HMI fault evidence, and a customer-confirmed recovery state. However, the exact fault, decisive action, and complete diagnostic evidence are incomplete or ambiguous. |

**Summary:** Use this path when automated bag-out stops or progresses only partially and site personnel report that an AGV is not moving, a robot may be out of sequence, or a related HMI shows a fault.

#### Support User Language Examples

- Bag-out stopped
- Bag out started then stopped
- We are manually bagging out
- AGV stopped
- The robot hasn't moved
- Robots are out of sequence
- One pair won't start bag-out
- The hospital HMI has a fault
- There is a stuck task

#### Negative Or Absent Signals

- No stack-light fault was reported during one bag-out observation.
- The exact AGV identifier, active error, task state, and decisive recovery action were not consistently readable or isolated.
- The source does not confirm that the HMI update or stuck-task recovery process was completed.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm automated bag-out stoppage and affected operating scope | Confirm that automated bag-out is stopped or only partially progressing and determine whether the condition is site-wide, localized to a zone or pair, or limited to a tote or task. | aud:operator, aud:L1_support | Procedure needed to interview the site about whether automated bag-out is stopped, whether it started and stopped again, whether manual bagging is being used, and which affected zone, pair, tote, or task is involved; use the incident-supported RMS activity or status view when available to compare the affected operating scope. | The case and chat evidence describe a bag-out stoppage after sorting, manual bagging, and a need to identify the affected robot or exchange pair. |
| 2 | diagnostic_decision | Check for AGV inactivity or active fault evidence | Determine whether one or more AGVs show abnormal inactivity, active error, or a related sequence or pairing indication that correlates with the bag-out stoppage. | aud:operator, aud:L1_support | Procedure needed to inspect RMS fleet activity and status for AGV movement, active fault indications, and sequence or pairing abnormalities, and to compare the affected AGV or pair with the bag-out stoppage; if the relevant screen is unavailable, use the source-mentioned system active-error view without assuming a specific backend field. | The source explicitly records an RMS-style observation that an AGV did not move for three hours and preserves a discussion about checking system active error. |
| 3 | diagnostic_decision | Check HMI-visible task, tote, or lane fault | Determine whether an HMI-visible fault, stuck task, tote association, or hospital-area workflow condition is preventing bag-out from progressing. | aud:operator, aud:L1_support | Procedure needed to inspect the source-named hospital-area HMI for the displayed fault, task state, tote identity or location indication, and whether the workflow request progresses; include the approved HMI acknowledgement or retry decision rubric without prescribing exact screen navigation or physical disconnection. | The source reports a hospital HMI fault, a tote read at an unexpected location, a stuck task visible only on that HMI, and guidance to acknowledge and try again. |
| 4 | procedure_reference | Restore the affected AGV sequence or pairing state through an authorized recovery path | Use an approved, role-authorized recovery procedure to restore the affected AGV or pair to a valid operating sequence when the diagnostic evidence supports that direction. | aud:L2_support, aud:L3_support | Procedure needed for authorized AGV sequence, pairing, removal, replacement, or controlled return-to-operation recovery, including the requirement that an AGV removed from the grid be appropriately replaced and that safety and role limits be respected; do not infer a specific robot or exact recovery action. | Support asked the site to remove and add AGV pairs; the source also states that a removed AGV without a tote must be replaced and later reports robots in proper sequence. |
| 5 | validation_gate | Validate stable AGV operation and automated bag-out | Confirm that the recovery restored the affected workflow and that AGVs remain functional rather than merely showing a temporary improvement. | aud:operator, aud:L1_support | Procedure needed to validate sustained AGV availability and sequence state through the source-supported RMS activity view, confirm bag-out progress with the site, and check the relevant hospital-area HMI for recurrence of the fault or stuck-task indication before declaring recovery. | The source records customer confirmation that robots were functional in proper sequence and a later all-good response after HMI-related troubleshooting. |
| 6 | escalation_gate | Stop and escalate when the supported path cannot establish stable recovery | Hand off when the available evidence does not identify a supported recovery path, authorized recovery cannot be completed safely, or validation fails after recovery. | aud:L2_support, aud:L3_support | Procedure needed to prepare an escalation handoff with RMS activity evidence, HMI or hospital-area fault evidence, affected scope, sequence or pairing state, recovery attempts, role and safety constraints, and validation outcomes; include stop criteria for repeated bag-out stoppage or unresolved AGV inactivity. | The source states that available troubleshooting options were exhausted, additional technical assistance was requested, and the exact decisive recovery was not isolated. |

#### Extraction Notes

- Ingestion metadata is authoritative for site assignment: UPS Haslet TX (TXRTH), site_code ups_haslet_tx.
- Evidence uses several location phrases, including UPS Haslet, UPS Fort Worth, and hospital. The hospital wording may refer to an internal operating area; it is preserved as an ambiguity and does not replace the ingestion site.
- The suspected out-of-sequence robot, stuck task, tote mismatch, and AGV inactivity are source-supported tentative patterns, not confirmed root causes.
- The decisive recovery action is not isolated. The packet supports a broad recovery direction involving AGV sequence or pairing restoration and HMI/task investigation, but not a canonical procedure.
- The source includes unreadable or garbled artifacts and does not provide validated backend mappings for bag-out, task, tote, or pairing state.
- No production automation, canonical runbook ID, final issue classification, or support-coordination node was created.
