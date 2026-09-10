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
- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_4 (validation_gate) is missing expects_capability
- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_5 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228086_sitewide_robotic_stoppage node node_7 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228086_sitewide_robotic_stoppage | high | 8 |  | Use this response pattern when operators report that robots or AGVs are stopped, nothing is moving, the small sort is not running, or the robotic system is not responding. Confi... |

## Candidate Details

### Site-wide robotic stoppage with AGV synchronization loss

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228086_sitewide_robotic_stoppage |
| Goal | Restore stable robotic and sort operation by distinguishing a site-wide control-system or service interruption from a localized AGV condition, then validating service responsiveness, AGV state, and resumed automated operation. |
| Entry symptoms | Operators reported that nothing was moving.; The robotic system was reported as not responding.; The small sort was not running.; Multiple bots were reported as not moving in different areas.; Totes could not be removed from the hospital workflow.; The RMS/HMI appeared mostly blank and displayed a message reported as '.NET Control not created.'; AGVs were reported as out of sync. |
| Tentative internal patterns | Possible OptiSweep service termination or restart condition; Possible WCSWebApplication or related application fault; Possible AGV synchronization or roster-state inconsistency after service recovery; Possible Ignition gateway availability or performance concern |
| Affected systems/components | OptiSweep service; AGVs and robotic system; RMS / HMI; Ignition gateway; WCSWebApplication; Windows Event Viewer / Service Control Manager; OptiSweep / WCS API; Small sort and hospital workflow |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | high |
| Confidence reason | The packet contains direct source artifacts and case comments covering the symptom pattern, Event Viewer evidence, service recovery, RMS AGV correction, API validation, and operational recovery. Exact recovery commands and the definitive causal chain are intentionally not inferred. |

**Summary:** Use this response pattern when operators report that robots or AGVs are stopped, nothing is moving, the small sort is not running, or the robotic system is not responding. Confirm the scope and observable system state, investigate service and application health, restore the named robotic service or gateway through an approved procedure, correct residual AGV synchronization issues, and validate API and operational recovery.

#### Support User Language Examples

- AGVs stopped
- AGVs are stopped
- robots stopped
- nothing is moving
- the robots aren't moving
- small sort stopped
- robotic system not responding
- AGVs are out of sync
- can't get the totes out
- RMS is blank

#### Negative Or Absent Signals

- The site initially reported no known failed AGV or visible AGV fault.
- The source does not confirm that the apparent RMS message represented a specific root cause.
- The source does not confirm that memory usage caused the service or application failure.
- A successful HTTP response did not eliminate the API client's schema validation warning.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm the observable scope of the stoppage | Determine whether the report represents a site-wide or broad robotic stoppage with abnormal control-system presentation rather than an isolated robot issue. | aud:operator, aud:L1_support | Procedure needed to ask the site which affected areas or workflows are stopped, whether multiple robots are stationary, and whether automated sorting or hospital tote removal is affected; also inspect the RMS/HMI overview for a normally populated versus mostly blank operational display and any readable system or AGV error indicators. | The incident began with reports that nothing was moving, the small sort was not running, and the robotic system was not responding; RMS screenshots showed an abnormal mostly bla... |
| 2 | diagnostic_decision | Check for a named service or application failure | Determine whether Windows evidence indicates an OptiSweep service termination or clustered WCSWebApplication/application errors that correlate with the broad stoppage. | aud:L1_support, aud:L2_support | Procedure needed to inspect Windows Event Viewer System and Application logs for the named OptiSweep service and WCSWebApplication, including Service Control Manager termination events, the visible Event 7031 category, clustered application errors, and the WCSWebApplication Event 20102 failed-command evidence, while preserving timestamps and uncertainty. | The source shows OptiSweep Event 7031 termination evidence and clustered WCSWebApplication/Application Error entries around 6:35-6:36 AM. |
| 3 | procedure_reference | Restore the affected OptiSweep or gateway service through an approved procedure | Perform the source-supported recovery direction for the affected control service or gateway when the authorized support role confirms an abnormal service or gateway state. | aud:L2_support, aud:L3_support | Procedure needed for authorized recovery of the named OptiSweep service or Ignition gateway, including safety prerequisites, role limits, recovery completion criteria, and the distinction between a service reset, gateway restart, and unsupported configuration or database changes. | The source records OptiSweep reset activity, an Ignition gateway restart attempt, automatic service restart behavior, and later evidence of the OptiSweep service in a Running st... |
| 4 | validation_gate | Validate service and API responsiveness | Confirm that the recovered control path responds before attempting residual AGV correction or releasing the site to automated operation. | aud:L1_support, aud:L2_support | Procedure needed to validate OptiSweep responsiveness through the incident-evidenced GetAgvStatuses API endpoint, inspect returned AGV records without treating the client schema warning as a confirmed service failure, and corroborate with Ignition Systems Overview and Windows Services when those surfaces are available. | The source defines GetAgvStatuses as a post-restart responsiveness check and shows HTTP 200 with returned AGV records, while also documenting Ignition and Windows Services checks. |
| 5 | diagnostic_decision | Determine whether residual AGV synchronization issues remain | Identify whether individual AGVs remain out of sync after service responsiveness has returned. | aud:operator, aud:L2_support | Procedure needed to inspect the RMS fleet or map view for out-of-sync AGVs and to corroborate relevant robot state through the read-only robotics database view in SQL Server Management Studio or the GetAgvStatuses response; the procedure must define how to distinguish residual synchronization problems from normal charging, queueing, or exchange states. | After the OptiSweep reset, RMS was used to locate and correct AGVs that remained out of sync; a separate artifact shows read-only SSMS inspection of AGV states. |
| 6 | procedure_reference | Correct residual AGV synchronization state | Use the authorized RMS recovery procedure to correct individually identified out-of-sync AGVs after the control service is responsive. | aud:L2_support, aud:L3_support | Procedure needed for authorized RMS handling of an individually identified out-of-sync AGV, including safety preconditions, role limits, identification of the affected asset, correction completion criteria, and boundaries for physical AGV recovery or unsupported state changes. | The historical response used RMS to locate and fix out-of-sync AGVs one by one after resetting OptiSweep. |
| 7 | validation_gate | Validate stable automated operation | Confirm that service responsiveness, AGV state, and the affected automated workflows have recovered sufficiently to declare the technical response successful. | aud:operator, aud:L1_support, aud:L2_support | Procedure needed to validate OptiSweep service state, repeat the GetAgvStatuses responsiveness check, review RMS fleet state for residual synchronization issues, and obtain site confirmation that automated movement and the affected sort or bag-out workflow remain operational before declaring recovery. | The historical response reported resumed auto bag-out after service reset and RMS correction, with API and service-state evidence used as validation. |
| 8 | escalation_gate | Stop when the supported recovery path cannot be validated | Hand off when the authorized diagnostic, recovery, or validation path is unavailable, unsafe, unauthorized, or does not restore stable operation. | aud:L2_support, aud:L3_support | Procedure needed to prepare a technical escalation handoff with Windows Event Viewer System and Application evidence, OptiSweep Windows Services state, Ignition gateway status, GetAgvStatuses response evidence, RMS AGV-state evidence, recovery attempts, validation results, and explicit stop criteria. | The incident evidence includes unresolved ambiguity around the web application, service recovery outcome, memory/log follow-up, and the API schema warning, supporting a technica... |

#### Extraction Notes

- source_package.site_location is empty, so authoritative ingestion site metadata was not available to populate a site context or site code.
- The canonical record names the site as UPS Fort Worth, TX (Haslet), but this is evidence-derived context rather than source_package.site_location ingestion metadata.
- The apparent '.NET Control not created.' RMS message and the meaning of several AGV states require SME review.
- The packet supports a reusable troubleshooting response shape but does not prove one definitive root cause.
- The memory trend and reported web-application memory/log issue are retained only as tentative context and are not used as confirmed entry criteria.
- The API response was successful but displayed a schema validation warning; this is treated as an ambiguity, not as proof of API failure.
- No canonical runbook IDs, production automation bindings, final classification, or finalized playbook are created at this stage.
