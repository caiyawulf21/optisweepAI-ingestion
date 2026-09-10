# Stage 5 Playbook Candidate Review - Case 233681

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 2 |
| Nodes | 9 |
| Nodes missing runbook placeholder | 0 |
| Validation errors | 0 |
| Warnings | 5 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
| Candidates with events | 0 |

## Confidence

| Confidence | Count |
| --- | --- |
| high | 1 |
| low | 1 |

## Warnings

- playbook_candidate_incident_233681_site_communication_tote_exchange node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_233681_site_communication_tote_exchange node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_233681_site_communication_tote_exchange node node_4 (validation_gate) is missing expects_capability
- playbook_candidate_incident_233681_single_agv_interruption node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_233681_single_agv_interruption node node_3 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_233681_site_communication_tote_exchange | high | 5 |  | Use when totes are not exchanging or bag-out is unavailable across the operation, especially when the system appears to be running but communication with equipment or the sorter... |
| playbook_candidate_incident_233681_single_agv_interruption | low | 4 |  | Use when one AGV repeatedly stops and starts and appears to hold up part of the sorter while the broader system is otherwise operating. |

## Candidate Details

### Site-wide tote exchange failure with lost equipment communication

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_233681_site_communication_tote_exchange |
| Goal | Distinguish a site-wide tote-exchange workflow failure from an AGV hardware fault, investigate communication loss affecting XLEs, scanners, or the sorter, apply an authorized high-level recovery path, and validate resumed operation. |
| Entry symptoms | Totes are not exchanging after startup or during normal operation.; Bag-out is unavailable or no totes are being processed.; The sorter is not communicating with the system.; The system appears to be running, but AGV and tote workflows do not progress.; Communication-loss messages refer to XLEs.; Multiple TCP connectivity tests to XLE-related targets fail. |
| Tentative internal patterns | Possible XLE communication-path failure; Possible firewall or network-path blocking; Possible stunnel communication errors; Possible accumulated or abnormal task state |
| Affected systems/components | AGV system; Tote exchange and bag-out workflow; Sorter; XLE communication; Scanners; RMS monitoring; Stunnel communication component; Firewall or network path |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | high |
| Confidence reason | The packet provides repeated evidence of tote-exchange and bag-out failure, XLE communication loss, failed TCP connectivity tests, suspected firewall blocking, stunnel errors, interim purge recovery, and reported return of sorting. |

**Summary:** Use when totes are not exchanging or bag-out is unavailable across the operation, especially when the system appears to be running but communication with equipment or the sorter is impaired.

#### Support User Language Examples

- Totes aren't exchanging
- AGVs can't exchange totes
- We can't bag out
- The sorter isn't communicating
- The system looks like it's running but nothing is moving through
- XLE communication is lost
- TCP tests are failing
- The scanners can't talk to the system

#### Negative Or Absent Signals

- The site reported no AVEVA alarms.
- The site reported that required robots were present across the zones.
- The incident evidence reported that AGVs were not faulted or crashed.
- The evidence does not establish a specific endpoint, firewall rule, service failure, or confirmed root cause.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm a site-wide tote-exchange or bag-out workflow failure | Determine whether the reported problem is a broad tote-exchange or bag-out interruption rather than an isolated robot fault. | aud:operator, aud:L1_support | Procedure needed to confirm with the site whether totes are exchanging, whether bag-out is unavailable, whether the sorter is processing, and whether the issue affects multiple workflows. In RMS, inspect the fleet or map-monitoring view for overall robot status and current task activity without treating ambiguous counters as a confirmed fault. | The case reports inability to exchange totes and bag out, while RMS evidence and site statements indicate no AGVs were faulted or crashed. |
| 2 | diagnostic_decision | Determine whether equipment communication loss is present | Determine whether XLE, scanner, sorter, or related communication loss correlates with the tote-exchange failure. | aud:L1_support, aud:L2_support | Procedure needed to review the XLE communication-loss messages and stunnel error evidence, and to assess the incident-evidenced connectivity-test results for the affected communication path. The procedure should distinguish reachability, TCP connection failure, and application communication failure without assuming that a firewall is the confirmed cause. | The source reports repeated XLE communication-loss errors, failed TCP connectivity tests, stunnel errors, and a sorter that was not communicating. |
| 3 | procedure_reference | Apply an authorized communication-path recovery | Use the approved recovery path for the affected communication chain when communication loss is confirmed and the responsible role is authorized. | aud:L2_support, aud:L3_support | Procedure needed for authorized recovery of the XLE communication path, including coordination with the site network owner for any firewall or network-path correction, review of stunnel status, and controlled handling of any supported system-purge or restart-related recovery activity. The procedure must define role limits and safety prerequisites without embedding exact commands or configuration changes. | The source records a planned camera-tunnel/XLE reset, a system purge followed by movement and tote exchange, and a recorded firewall-related communication blockage. Exact recove... |
| 4 | validation_gate | Validate restored communication and sustained tote exchange | Confirm that recovery restored the affected workflow rather than only producing temporary movement. | aud:operator, aud:L1_support | Procedure needed to validate the affected communication path and workflow after recovery, including confirmation with the site that tote exchange, bag-out, scanner communication, and sorter processing remain normal, plus review of the incident-evidenced communication status for recurring XLE or stunnel errors. | The case records that sorting resumed, but also states that movement and tote exchange during the purge were interim and that closure did not independently prove sustained live-... |
| 5 | escalation_gate | Stop when communication recovery or validation cannot continue safely | Hand off when the communication path requires unsupported network or service changes, or when authorized recovery does not restore stable operation. | aud:L2_support, aud:L3_support | Procedure needed to prepare an escalation handoff containing XLE communication-loss evidence, connectivity-test results, stunnel error observations, sorter and tote-exchange impact, recovery actions attempted, and validation results, while identifying any required site network-owner or service-owner decision. | The source documents ongoing site network investigation, an apparent firewall issue, incomplete recovery validation, and later case closure without a complete live-system valida... |

#### Extraction Notes

- Ingestion metadata is authoritative for site assignment: UPS Haslet TX (TXRTH), site_code ups_haslet_tx.
- The source uses both Haslet and UPS Fort Worth, TX (Haslet); these are consistent with the authoritative ingestion site and do not require replacement.
- Firewall involvement is source-supported as a recorded or suspected explanation, not a confirmed diagnosis.
- The exact endpoint addresses, ports, firewall rule, stunnel change, and purge procedure are not reliable or complete enough for reusable procedural steps.
- The RMS screenshot contains ambiguous identifiers and values; those details were not used as confirmed decision criteria.

### Single AGV intermittently stopping and obstructing sorter flow

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_233681_single_agv_interruption |
| Goal | Distinguish an isolated intermittently stopping AGV from the site-wide communication flow, assess whether the asset presents an active fault or physical obstruction, and determine whether authorized physical recovery or removal is required. |
| Entry symptoms | One AGV stops and starts intermittently.; The intermittent AGV holds up one side of the sorter.; The broader sorter may otherwise be operating after communication recovery. |
| Tentative internal patterns | Possible isolated AGV operational interruption; Possible AGV task, path, or physical-state issue; Possible localized sorter obstruction |
| Affected systems/components | Individual AGV; Sorter; RMS monitoring; Physical floor or AGV handling |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | low |
| Confidence reason | The packet contains one report of an AGV stopping and starting, a conditional suggestion to remove it, and no confirmed diagnosis, removal, or validation sequence. |

**Summary:** Use when one AGV repeatedly stops and starts and appears to hold up part of the sorter while the broader system is otherwise operating.

#### Support User Language Examples

- One AGV keeps stopping and starting
- A robot is holding up one side of the sorter
- One AGV is blocking the sorter
- The system is mostly back but one robot keeps stopping
- Should we remove the robot?

#### Negative Or Absent Signals

- The source does not confirm that the AGV was faulted.
- The source does not confirm that the AGV was physically removed.
- The source does not establish whether the issue was caused by hardware, pathing, task state, or communication.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm an isolated intermittently stopping AGV | Determine whether one identifiable AGV is repeatedly stopping and starting while obstructing sorter flow, rather than the site-wide communication symptom recurring. | aud:operator, aud:L1_support | Procedure needed to confirm the affected robot's current behavior and identity through site observation and the RMS fleet or map-monitoring view, including whether the interruption is isolated and whether RMS shows an active AGV error or abnormal state. | The source reports that an AGV identified in the chat as 052 was stopping and starting and holding up one side of the sorter. |
| 2 | procedure_reference | Use the authorized isolated-AGV recovery path | Apply the approved recovery direction for an isolated intermittently stopping AGV, including physical isolation or removal only when authorized and safe. | aud:operator, aud:L2_support | Procedure needed for authorized isolated-AGV assessment and physical recovery or removal, including safety prerequisites, role limits, fleet-impact checks, and criteria for deciding whether the affected asset may be taken out of service. Do not infer or prescribe a specific removal action from the incident alone. | The source records a conditional plan to take the affected AGV out if the stop/start behavior continued, but does not document completion. |
| 3 | validation_gate | Validate clearance of the localized sorter interruption | Confirm that the isolated AGV condition no longer blocks sorter operation and that the broader fleet remains stable. | aud:operator, aud:L1_support | Procedure needed to monitor the affected sorter section and confirm stable AGV or fleet status in RMS after isolated-AGV recovery, including confirmation that the obstruction does not recur during normal operation. | The incident provides a localized symptom but no documented confirmation that the sorter remained clear after the conditional removal discussion. |
| 4 | escalation_gate | Stop if isolated AGV recovery is unsafe or unsuccessful | Hand off when the asset cannot be safely handled, the symptom persists, or the evidence is insufficient to choose a supported recovery. | aud:L2_support, aud:L3_support | Procedure needed to prepare an isolated-AGV escalation handoff containing asset identity, RMS status evidence, site observation of stop/start behavior, sorter impact, physical safety constraints, recovery attempted, and validation outcome. | The incident records a conditional removal discussion but no confirmed completion or diagnosis. |

#### Extraction Notes

- This candidate is intentionally low confidence because the packet contains only one sparse report of the isolated AGV symptom.
- The source identifier '052' is preserved only in source references and is not used in reusable node fields.
- No confirmed AGV fault, physical obstruction, removal, or successful validation is documented.
- The ingestion site remains UPS Haslet TX (TXRTH), site_code ups_haslet_tx.
