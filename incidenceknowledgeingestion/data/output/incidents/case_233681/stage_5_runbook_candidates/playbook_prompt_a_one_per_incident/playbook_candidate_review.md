# Stage 5 Playbook Candidate Review - Case 233681

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

- playbook_candidate_incident_233681_tote_exchange_communication_loss node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_233681_tote_exchange_communication_loss node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_233681_tote_exchange_communication_loss node node_3 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_233681_tote_exchange_communication_loss node node_5 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_233681_tote_exchange_communication_loss | medium | 6 |  | Use this troubleshooting pattern when AGVs are not exchanging totes or the site cannot bag out, especially when the sorter is not communicating or the site reports communication... |

## Candidate Details

### AGV tote exchange unavailable with sorter or XLE communication loss

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_233681_tote_exchange_communication_loss |
| Goal | Determine whether the tote-exchange stoppage is associated with a site-wide operational communication problem, collect evidence about XLE and network connectivity, perform only an authorized high-level recovery action when supported, and validate resumed tote exchange and sorting. |
| Entry symptoms | AGVs are unable to exchange totes.; The site cannot bag out or process totes normally.; The sorter is not communicating with the system.; The system appears to be running or AGVs are not individually faulted, but tote exchange and task processing are not progressing.; Tasks accumulate or are canceled while normal tote movement is unavailable. |
| Tentative internal patterns | XLE communication interruption; Network or firewall path blocking communication; Stunnel communication errors; Abnormal task or tote-exchange state without an individual AGV fault |
| Affected systems/components | AGV system; Tote exchange; Bag-out function; Sorter; XLE communication; RMS monitoring; Stunnel communication component; Firewall or network path |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | medium |
| Confidence reason | The packet contains a coherent symptom, diagnostic, high-level recovery, and operational validation pattern. Confidence is limited because the exact network endpoints, firewall change, purge procedure, and sustained post-recovery validation are not documented. |

**Summary:** Use this troubleshooting pattern when AGVs are not exchanging totes or the site cannot bag out, especially when the sorter is not communicating or the site reports communication errors.

#### Support User Language Examples

- AGVs stopped exchanging totes
- AGVs can't exchange totes
- Unable to exchange totes
- We can't bag out
- The sorter is not communicating
- Nothing is moving through the sorter
- The system looks up but totes are not moving
- No AGVs are faulted but the system cannot run
- XLE communication is lost
- Stunnel is throwing errors

#### Negative Or Absent Signals

- The site reported no AVEVA alarms.
- The site reported that required robots were checked across the zones without an identified issue.
- The site reported that AGVs were not faulted or crashed.
- The RMS screenshot did not establish a specific AGV fault or crash state.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm a broad tote-exchange or bag-out stoppage | Determine whether the reported problem affects normal tote exchange or bag-out operation broadly enough to follow the communication-loss investigation path. | aud:operator, aud:L1_support | Procedure needed to confirm with the site whether the affected zone or workflow is unable to exchange totes, whether bag-out is unavailable, whether sorter movement is absent, and whether any AGVs are visibly faulted. In RMS, inspect the fleet or map-monitoring view for the affected workflow's current robot and task state; use the site-reported AVEVA alarm state only as supporting context. | The case began with totes not exchanging after startup and later described inability to bag out while AGVs were not reported as faulted or crashed. |
| 2 | diagnostic_decision | Check for XLE or stunnel communication-loss evidence | Determine whether the operational stoppage correlates with an explicit XLE communication-loss message or stunnel error condition. | aud:L1_support, aud:L2_support | Procedure needed to inspect the incident-relevant RMS or system-message view for current XLE communication-loss entries and to review the named stunnel communication component for active errors or connection-state indicators, without assuming that historical messages prove a current failure. | The source contains repeated XLE communication-loss messages and a later report that stunnel was generating errors. |
| 3 | diagnostic_decision | Assess connectivity between the system and XLE-related endpoints | Determine whether the communication problem is accompanied by failed network connectivity to the XLE-related targets identified in the incident evidence. | aud:L1_support, aud:L2_support | Procedure needed to review or repeat the source-supported network connectivity check for the relevant XLE-related endpoints and communication port, record whether reachability and TCP connectivity succeed or fail, and distinguish endpoint, network-path, and service-level ambiguity without embedding commands or exact endpoint values. | The incident diagnostic screenshot reported lost communication to XLEs and failed TCP connectivity on the displayed communication port for multiple targets. |
| 4 | procedure_reference | Use an authorized communication recovery path | Apply the approved high-level recovery path for the confirmed communication or abnormal tote-exchange condition, subject to site safety and role authorization. | aud:operator, aud:L2_support | Procedure needed for the authorized recovery path applicable to the confirmed communication condition, including the role boundary for any system purge, camera-tunnel or XLE reset, stunnel or network remediation, required operating-state preconditions, and prohibition on unsupported firewall or database changes. | The incident records a system purge, planned camera-tunnel and XLE reset, and later firewall-related remediation associated with resumed movement and tote exchange. |
| 5 | validation_gate | Validate sustained tote exchange and sorting | Confirm that operational recovery is complete and not limited to temporary movement during an active purge or partial communication recovery. | aud:operator, aud:L1_support | Procedure needed to validate sustained tote exchange, bag-out, and sorter operation with the site, review current RMS robot and task activity, and confirm that XLE or stunnel communication errors are not recurring before declaring recovery. | Sorting was reported to have resumed, but the packet explicitly notes that sustained normal operation was not independently validated and that purge completion was initially pen... |
| 6 | escalation_gate | Stop and escalate when communication recovery or validation fails | Hand off when the authorized diagnostic and recovery path cannot safely identify or correct the communication condition, or when operational validation fails. | aud:L2_support, aud:L3_support | Procedure needed to prepare an escalation handoff containing the XLE communication messages, stunnel error evidence, connectivity-test outcomes, RMS or site operational observations, recovery actions attempted, role and authorization constraints, and validation results; the handoff must identify whether the unresolved boundary is network or firewall ownership, communication service health, or operational recovery. | The incident involved ongoing network-side investigation, a suspected firewall blocker, incomplete endpoint detail, and limited sustained validation evidence. |

#### Extraction Notes

- The authoritative ingestion site is UPS Haslet TX (TXRTH), site_code ups_haslet_tx; all source references preserve that site metadata.
- Evidence location text such as UPS Fort Worth, TX (Haslet) is consistent with the authoritative ingestion site, so no site conflict was identified.
- The firewall explanation is source-supported but remains a tentative internal pattern in this candidate; the packet does not provide the exact firewall rule, endpoint, or corrective change.
- The packet contains both a broad tote-exchange communication incident and a later localized report of one AGV intermittently stopping. The localized report is treated as a residual validation concern rather than a separate candidate because cardinality requires one broad response pattern.
- Connectivity endpoint and port values are inconsistent or partly garbled in OCR and are intentionally not embedded in reusable node decision fields.
- The source records resumed sorting and movement during or after recovery, but sustained live-system validation is incomplete.
- No canonical runbook IDs, production automation bindings, final classification, or confirmed root cause were created.
