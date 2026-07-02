# Stage 5 Playbook Candidate Review - Case 228086

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 2 |
| Nodes | 13 |
| Nodes missing runbook placeholder | 0 |
| Validation errors | 0 |
| Warnings | 0 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
| Candidates with events | 0 |

## Confidence

| Confidence | Count |
| --- | --- |
| high | 1 |
| low | 1 |

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228086_site_motion_stoppage_optisweep_recovery | high | 7 |  | Use this candidate when the site reports that nothing is moving, the robotic system is not responding, or RMS/HMI shows an abnormal blank state. The troubleshooting shape in thi... |
| playbook_candidate_incident_228086_wcswebapp_ignition_error_investigation | low | 6 |  | Use this lower-confidence candidate when responders enter from observable log or monitoring evidence rather than from the site's motion-stoppage report—for example, clustered WC... |

## Candidate Details

### Site-wide robotic movement stopped with AGVs out of sync after control-service disruption

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228086_site_motion_stoppage_optisweep_recovery |
| Goal | Restore robotic/AGV operation after a site-wide stoppage associated with abnormal OptiSweep service state and post-recovery AGV desynchronization. |
| Entry symptoms | Site reports that nothing is moving.; Robotic system is reported as not responding.; Small sort is not running.; Multiple bots or AGVs are not moving in various areas.; RMS/HMI shows an abnormal blank state with '.NET Control not created.'; Question marks are visible on the HMI.; Totes cannot be removed from hospital. |
| Tentative internal patterns | OptiSweep service termination around 06:36 correlated with site-wide stoppage and AGV desynchronization.; Post-service-recovery work in RMS was needed to locate and fix out-of-sync AGVs one by one.; Ignition gateway restart and API status checks were used as supporting recovery/validation evidence in the incident. |
| Affected systems/components | OptiSweep service; AGV/robotic system; RMS / Geek+ RMS; HMI; Windows Event Viewer; Windows Services; Ignition gateway; GetAgvStatuses API endpoint |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | high |
| Confidence reason | The incident contains a clear troubleshooting sequence with observable entry symptoms, named tools, a supported recovery direction, and explicit validation evidence: Event Viewer and service-state checks, OptiSweep reset, RMS correction of out-of-sync AGVs, Windows Services running state, API 200/NORMAL responses, and site resumption of auto bag out. |

**Summary:** Use this candidate when the site reports that nothing is moving, the robotic system is not responding, or RMS/HMI shows an abnormal blank state. The troubleshooting shape in this incident was to confirm abnormal service and UI state, recover the OptiSweep service if authorized, inspect RMS for out-of-sync AGVs, correct affected AGVs, and validate recovery through service state, API response, and resumed site operation.

#### Support User Language Examples

- UPS Haslet nothing is moving
- robotic system not responding
- small sort not running
- 4-6 bots currently not moving in various areas
- AGVs out of sync
- question marks on HMI
- .NET Control not created

#### Negative Or Absent Signals

- Site reported no obvious fault or failed AGV visible at initial report.
- Memory review later did not indicate that memory caused an Ignition crash.

#### Nodes

| # | Type | Title | Intent | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm site-wide robotic stoppage and abnormal RMS/HMI presentation | Determine whether the incident matches the observable symptom pattern of site-wide motion stoppage with abnormal RMS/HMI behavior rather than a single isolated AGV issue. | Procedure needed to confirm with the site whether nothing is moving, whether the small sort is not running, whether bots are stopped in multiple areas, whether totes cannot be removed from hospital, and whether question marks are visible on the HMI. In RMS / ACB System 1 - RMS, inspect for abnormal blank-state behavior and messages such as '.NET Control not created.' and review visible system or AGV error areas if present. | Initial reports described nothing moving, robotic system not responding, small sort not running, bots not moving in various areas, question marks on HMI, and RMS/HMI blank state... |
| 2 | diagnostic_decision | Check whether OptiSweep service failure evidence is present | Determine whether the stoppage correlates with abnormal OptiSweep service state using named Windows service and log sources. | Procedure needed to inspect Windows Event Viewer System log for Service Control Manager events affecting the OptiSweep service, especially unexpected termination events such as Event 7031, and to inspect Windows Services for the current OptiSweep service state, startup type, and whether the service is running or requires supported recovery. | The incident explicitly checked Event Viewer for service failures and captured Event 7031 showing OptiSweep terminated unexpectedly at 06:36:02; later Windows Services showed Op... |
| 3 | procedure_reference | Perform approved OptiSweep service recovery if abnormal and authorized | Use the approved recovery procedure for the OptiSweep service when service failure evidence is present and the responder is authorized to act. | Procedure needed for authorized recovery of the OptiSweep service, including required safety preconditions, role limits, and any dependency checks before and after service reset or restart. | Case comments state that after resetting the OptiSweep service, the team used RMS to locate out-of-sync AGVs and fix them. |
| 4 | diagnostic_decision | Determine whether AGVs remain out of sync after service recovery | Check whether service recovery alone restored fleet consistency or whether specific AGVs still require correction in RMS. | Procedure needed to inspect the AGV fleet, roster, map, system errors, and AGV error views in RMS / Geek+ RMS after OptiSweep recovery, identify which AGV IDs are out of sync or missing from expected state, and determine whether targeted AGV correction is required. | The incident states that after OptiSweep reset, RMS was used to locate AGVs that were out of sync and fix them one by one; another note mentioned a possibly removed or missing AGV. |
| 5 | procedure_reference | Apply approved RMS correction for affected out-of-sync AGVs | Carry out the supported AGV correction workflow in RMS for the specific assets identified as out of sync. | Procedure needed for authorized correction of out-of-sync or missing AGV state in RMS / Geek+ RMS, including how to apply the approved asset-state correction for identified AGV IDs and any safety or operational preconditions before returning the fleet to service. | The incident explicitly says out-of-sync AGVs were fixed one by one in RMS after the OptiSweep service reset. |
| 6 | validation_gate | Validate service responsiveness and fleet recovery | Confirm that the service is running, AGV status responses are healthy enough to proceed, and the site has resumed operation. | Procedure needed to validate recovery by checking OptiSweep in Windows Services, sending the GetAgvStatuses request to the incident-evidenced API endpoint and reviewing HTTP status plus returned AGV status values, and confirming in RMS and with the site that automated movement or auto bag out has resumed. | Validation evidence included Windows Services showing OptiSweep running, API GetAgvStatuses returning HTTP 200 with NORMAL statuses, and case comments saying the site resumed au... |
| 7 | escalation_gate | Escalate if supported recovery does not restore stable fleet operation | Stop and escalate when service recovery and RMS correction do not produce a stable, validated recovery path. | Procedure needed to prepare escalation evidence including Windows Event Viewer System and Application log captures, Windows Services state for OptiSweep, RMS fleet or error views showing remaining abnormal AGVs, GetAgvStatuses API response evidence, and a summary of all recovery actions and validation outcomes attempted. | The incident provides evidence sources that would be needed for escalation if recovery had failed, including Event Viewer, Windows Services, RMS, and API validation artifacts. |

#### Extraction Notes

- The incident supports one dominant recovery flow with a post-recovery RMS correction phase; this was kept as one candidate rather than split because AGV correction occurs after service recovery and is part of the same operational goal.
- Ignition restart evidence was treated as a branchable supporting recovery capability rather than a separate main candidate for this operational stoppage flow.

### Application-log and gateway-health investigation during robotic system outage

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228086_wcswebapp_ignition_error_investigation |
| Goal | Assess whether application-log errors or gateway-health signals indicate a separate platform issue that needs supported recovery or escalation during a robotic-system outage. |
| Entry symptoms | Responders see clustered WCSWebApplication errors in Windows Event Viewer Application log.; Responders are asked whether Ignition crashed.; Ignition memory trend is reviewed because a crash is suspected.; Ignition status page or uptime/response indicators are checked after suspected instability.; A web application or webservice is described as faulted in incident notes. |
| Tentative internal patterns | WCSWebApplication database-command errors clustered around 06:35:24 and additional application errors around 06:36:02.; Source comments tentatively associated a faulted webservice/web application with memory usage and log-size concerns.; Ignition gateway restart and status-page checks were used as part of investigation and possible recovery support. |
| Affected systems/components | WCSWebApplication; Windows Event Viewer Application log; Windows Error Reporting; Ignition gateway; Ignition Systems Overview page; Ignition memory trend; database-related application layer |
| Roles | L1_support, L2_support, L3_support |
| Confidence | low |
| Confidence reason | The incident strongly supports diagnostic checks and evidence collection for this flow, but it does not provide a complete, clearly authorized, reusable recovery path for WCSWebApplication or the attributed memory/log issue. It is still useful as a low-confidence candidate because the investigation shape is source-supported and distinct. |

**Summary:** Use this lower-confidence candidate when responders enter from observable log or monitoring evidence rather than from the site's motion-stoppage report—for example, clustered WCSWebApplication errors in Event Viewer, questions about whether Ignition crashed, or a need to assess gateway health after a suspected application fault. The incident supports a lightweight investigation path, but not a complete standalone recovery workflow.

#### Support User Language Examples

- Anyone able to quickly determine if Ignition crashed or not?
- take a 24-hr snapshot of Ignition Server memory usage to see if it crashed
- WCSWebApplication errors
- web application is faulted
- memory trend is looking better

#### Negative Or Absent Signals

- Memory review did not indicate that memory caused a crash.
- The incident does not show a confirmed standalone recovery for WCSWebApplication.
- The incident does not prove that the webservice memory/log issue was the root cause of the site stoppage.

#### Nodes

| # | Type | Title | Intent | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm whether the entry pattern is application-log or gateway-health instability | Determine whether responders are entering from clustered application errors, suspected Ignition crash, or gateway-health concerns rather than from direct fleet-state symptoms. | Procedure needed to confirm whether the current entry pattern is driven by Windows Event Viewer Application log errors for WCSWebApplication or Application Error, by a site/support question about whether Ignition crashed, or by abnormal Ignition monitoring evidence such as memory trend changes or gateway status concerns. The procedure should specify which Event Viewer log to inspect and which Ignition monitoring views to review first. | The incident included direct questions about whether Ignition crashed, requests for memory snapshots, and Event Viewer evidence of clustered WCSWebApplication and Application Er... |
| 2 | diagnostic_decision | Inspect Windows Event Viewer for clustered application faults | Determine whether the application layer shows a concentrated error pattern that should influence recovery or escalation. | Procedure needed to inspect Windows Event Viewer Application log on the affected host for WCSWebApplication errors, Application Error events, and Windows Error Reporting entries around the incident time; capture event IDs, timestamps, and whether the visible pattern includes failed database-command execution or clustered repeated errors. | The incident captured WCSWebApplication Event ID 20102 with failed DbCommand execution at 06:35:24, repeated WCSWebApplication errors and Application Error entries at 06:36:02,... |
| 3 | diagnostic_decision | Assess Ignition gateway health using memory trend and status page | Determine whether available Ignition monitoring evidence supports a current gateway-health problem or weakens the crash hypothesis. | Procedure needed to review the Ignition Server memory trend over the recent incident window, inspect the Ignition Systems Overview page for uptime or current response indicators, and note whether the gateway is reachable, responsive, and showing recent slow-response or other abnormal indicators. | The incident requested a 24-hour memory snapshot, shared memory trend evidence, noted that memory did not indicate a crash, and captured the Ignition Systems Overview page showi... |
| 4 | branching_condition | Choose supported next step based on gateway responsiveness and service dependency checks | Decide whether the path should continue with supported gateway/service recovery checks or move to escalation because the evidence does not support a safe local continuation. | Procedure needed to apply the decision rubric for whether to continue with approved Ignition gateway recovery and dependent-service verification, including checking whether the gateway is reachable, whether it has returned to a usable login or status state, and whether the OptiSweep service still responds after any gateway recovery action. | Incident guidance said that if Ignition needed restart, responders should wait for it to come back up and then verify OptiSweep still responded to GetAgvStatuses; if no response... |
| 5 | validation_gate | Validate gateway and dependent service responsiveness after supported recovery | Confirm that the gateway is back up and that dependent service/API checks are responsive enough to hand control back to the main operational recovery flow. | Procedure needed to validate Ignition gateway recovery by checking the Ignition Systems Overview or equivalent gateway status page for responsiveness, then validating dependent OptiSweep responsiveness through the GetAgvStatuses API endpoint used in this incident and recording whether a response is returned. | The incident showed an Ignition status page capture and API validation through GetAgvStatuses after restart-related activity. |
| 6 | escalation_gate | Escalate unresolved application-layer or memory/log-growth concerns | Stop and escalate when application faults remain unexplained or when the incident evidence only supports specialist investigation rather than further supported frontline action. | Procedure needed to prepare escalation handoff evidence for application-layer or infrastructure review, including Windows Event Viewer Application log screenshots for WCSWebApplication and Application Error events, Ignition memory trend and Systems Overview captures, any gateway restart evidence, API response evidence, and the incident notes describing the faulted web application or webservice and associated memory or log-size concern. | The incident explicitly involved inviting database-team help for a faulted web application and included only tentative source-attributed statements about memory usage and log-si... |

#### Extraction Notes

- This candidate is intentionally low confidence because the incident supports investigation and escalation shape more strongly than a complete standalone recovery path.
- The source-attributed memory/log-size explanation was preserved only as tentative internal pattern context and not used as a confirmed diagnosis.
