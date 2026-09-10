# Stage 5 Playbook Candidate Review - Case 228086

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 1 |
| Nodes | 8 |
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

## Warnings

- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_3 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_5 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_7 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228086_sitewide_robotic_stoppage | high | 8 |  | Use this troubleshooting flow when a site reports that robotic operation has stopped, AGVs are not moving or are out of sync, small sort activity has stopped, or the RMS view is... |

## Candidate Details

### Robotic system not responding with AGVs stopped or out of sync

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228086_sitewide_robotic_stoppage |
| Goal | Determine whether the site-wide stoppage is associated with an abnormal OptiSweep, WCSWebApplication, or related gateway state; support authorized recovery; identify residual AGV synchronization or state issues; and confirm stable robotic operation before release. |
| Entry symptoms | Nothing is moving across the site or bots are stopped in multiple areas.; The robotic system is reported as not responding.; Small sort operation is not running.; AGVs are reported out of sync or several AGVs stop after a heartbeat issue.; Totes cannot be removed from the hospital workflow.; RMS or HMI is mostly blank or displays an apparent ".NET Control not created." message.; The site reports no obvious failed AGV even though automated movement has stopped. |
| Tentative internal patterns | Possible OptiSweep service termination or restart event associated with site-wide stoppage; Possible WCSWebApplication application or database-command fault near the service event; Possible residual AGV synchronization, roster, or state inconsistency after service recovery; Possible abnormal RMS rendering or control-state presentation; Possible webservice memory or log-growth condition requiring follow-up |
| Affected systems/components | OptiSweep service; AGVs and robotic system; RMS / HMI; WCSWebApplication; Ignition gateway; Windows Event Viewer / Service Control Manager; OptiSweep / WCS API; Hospital workflow; Small sort workflow |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | high |
| Confidence reason | The packet provides clear observable entry symptoms, named diagnostic surfaces, a source-supported service failure signal, a high-level recovery sequence, residual AGV correction, and multiple validation signals. Exact root cause and the significance of some memory and RMS messages remain uncertain. |

**Summary:** Use this troubleshooting flow when a site reports that robotic operation has stopped, AGVs are not moving or are out of sync, small sort activity has stopped, or the RMS view is blank or abnormal. Confirm the observable system state, inspect service and application evidence, recover the affected service or gateway through an authorized procedure, correct residual AGV state, and validate both service responsiveness and resumed operation.

#### Support User Language Examples

- Nothing is moving
- Bots stopped
- AGVs stopped
- AGVs are out of sync
- The robots aren't responding
- Small sort is down
- The RMS screen is blank
- We can't get totes out of hospital
- Several bots stopped after a heartbeat issue

#### Negative Or Absent Signals

- The site initially reported no specific fault or failed AGV.
- The available evidence does not confirm that the Ignition memory trend caused the stoppage.
- A successful HTTP response and returned AGV records do not by themselves confirm that all AGVs are synchronized or that production has recovered.
- The Windows Services screenshot shows OptiSweep running, but does not establish whether it was running before or after a restart.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm the stoppage pattern and abnormal control-system presentation | Determine whether the report represents a broad robotic-operation stoppage with an abnormal RMS or HMI presentation rather than an isolated AGV issue. | aud:operator, aud:L1_support | Procedure needed to confirm with the site whether the affected zone or workflow has broad loss of movement, whether small sort or hospital handling is also stopped, and whether RMS/HMI shows a populated normal status view or a blank/control-not-created presentation. Use generic affected-zone and reported-robot questioning rather than incident-specific identifiers. | The source reports a site-wide or multi-area motion stoppage, no obvious failed AGV, stopped small sort, hospital tote-removal difficulty, and abnormal RMS/HMI presentation. |
| 2 | diagnostic_decision | Determine whether a named service or application failure correlates with the stoppage | Use the available Windows log evidence to determine whether OptiSweep or WCSWebApplication entered an abnormal state near the onset of the operational stoppage. | aud:L1_support, aud:L2_support | Procedure needed to inspect Windows Event Viewer System and Application logs for OptiSweep Service Control Manager termination events and clustered WCSWebApplication or Application Error entries, and to correlate their timing with the reported stoppage without inferring root cause from the event alone. | The source contains Event Viewer evidence of OptiSweep termination, clustered WCSWebApplication errors, a failed database command, and a later OptiSweep Running state. |
| 3 | diagnostic_decision | Check whether Ignition gateway health is abnormal or merely a related observation | Determine whether the Ignition gateway shows a current responsiveness problem or whether the memory observation is only follow-up context. | aud:L1_support, aud:L2_support | Procedure needed to inspect the Ignition gateway Systems Overview for gateway responsiveness, current response behavior, recent slow-response events, and available CPU or memory trend evidence, while treating unlabeled trend changes as inconclusive unless correlated with a confirmed failure. | The source includes requests to determine whether Ignition crashed, memory trend charts, an Ignition Systems Overview showing 11 ms response and no recent slow-response events,... |
| 4 | procedure_reference | Perform authorized recovery of the affected gateway or OptiSweep service | Use the approved role-specific recovery procedure for the service or gateway identified by the diagnostic evidence. | aud:L2_support, aud:L3_support | Procedure needed for authorized recovery of the named Ignition gateway or OptiSweep service, including safety preconditions, role limits, expected downtime, and the distinction between gateway recovery and OptiSweep service recovery. The source shows Ignition gateway restart activity and OptiSweep reset activity but does not establish a canonical procedure. | The source shows an Ignition gateway restart in progress, reports that OptiSweep was reset, and later shows OptiSweep Running. Exact commands and procedures are intentionally no... |
| 5 | diagnostic_decision | Determine whether residual AGV state requires correction after service recovery | Identify whether AGVs remain out of sync, unmapped, or otherwise abnormal after the service or gateway recovery. | aud:operator, aud:L2_support | Procedure needed to inspect the RMS fleet or map view for residual out-of-sync, unavailable, unmapped, or abnormal-state AGVs after service recovery, using generic asset identification and state-correction criteria. The procedure should distinguish diagnosis from any authorized AGV correction action. | After the OptiSweep reset, the source says RMS was used to locate and fix out-of-sync AGVs one by one. The packet also includes RMS map and SSMS state evidence. |
| 6 | procedure_reference | Apply authorized correction for residual AGV synchronization or state issues | Perform the approved correction for AGVs identified as out of sync or otherwise abnormal, without treating the historical correction as a universal procedure. | aud:L2_support, aud:L3_support | Procedure needed for authorized RMS-based correction of an identified out-of-sync or abnormal AGV state, including safety prerequisites, asset-selection controls, role limits, and criteria for stopping before any physical AGV recovery. Exact historical correction steps are intentionally left to the procedure layer. | The source reports that RMS was used to locate and fix out-of-sync AGVs after the OptiSweep reset, but it does not provide a complete reusable procedure. |
| 7 | validation_gate | Validate service responsiveness, AGV status, and resumed operation | Confirm that the recovered service and fleet state support stable automated operation before declaring the troubleshooting path complete. | aud:operator, aud:L1_support, aud:L2_support | Procedure needed to validate OptiSweep responsiveness in Windows Services and through the source-evidenced GetAgvStatuses API client, inspect returned AGV status records, confirm RMS shows the expected fleet state, and obtain site confirmation that automated movement or auto bag-out has resumed. Treat an HTTP 200 response with a schema warning as partial evidence rather than complete recovery. | The source provides Windows Services, GetAgvStatuses API, RMS follow-up, and site resumption evidence, while explicitly leaving the API schema warning and complete restoration s... |
| 8 | escalation_gate | Stop and escalate when recovery or validation remains unsupported or fails | Hand off only when the supported diagnostic, recovery, and validation path cannot safely continue or does not restore stable operation. | aud:L1_support, aud:L2_support | Procedure needed to prepare an escalation handoff with Event Viewer System and Application evidence, Windows Services state, Ignition gateway status, GetAgvStatuses response evidence, RMS fleet-state evidence, recovery actions attempted, validation results, safety constraints, and explicit stop criteria. | The incident evidence supports stopping when service recovery, AGV correction, or validation does not establish stable operation. Historical coordination and case-management act... |

#### Extraction Notes

- source_package.site_location is empty, so no authoritative ingestion site, site code, or site location metadata was available to populate.
- The incident evidence identifies the site as UPS Fort Worth, TX (Haslet), but that evidence-derived location is not substituted for missing ingestion metadata.
- Some RMS messages, host names, timestamps, and OCR-derived event IDs are uncertain; reusable nodes avoid those incident-specific identifiers.
- The apparent RMS message ".NET Control not created." is retained as an observed symptom, not a confirmed diagnosis.
- The WCSWebApplication database-command error and memory observations are treated as tentative internal context and supporting diagnostic branches, not confirmed root cause.
- The API schema warning is treated as an ambiguity requiring interpretation, not as proof that the API or service failed.
- The source records an E-stop-related wait, but no E-stop node is created because the playbook does not need to orchestrate physical safety control beyond procedure prerequisites.
