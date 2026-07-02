# Stage 5 Playbook Candidate Review - Case 228086

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 1 |
| Nodes | 7 |
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

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228086_sitewide_motion_stop_optisweep_recovery | high | 7 |  | Use this response pattern when a site reports that nothing is moving, the robotic system is not responding, small sort is not running, or multiple AGVs are not moving, and suppo... |

## Candidate Details

### Site-wide robotic movement stoppage with abnormal RMS/HMI state and possible service failure

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228086_sitewide_motion_stop_optisweep_recovery |
| Goal | Restore robotic system responsiveness and site movement after a site-wide stoppage by confirming the affected service and interface state, performing approved recovery for the supported service/gateway path, correcting AGVs left out of sync in RMS, and validating recovery through service state, API response, RMS state, and site operation. |
| Entry symptoms | Nothing is moving at the site.; Robotic system reported as not responding.; Small sort is not running.; Multiple bots or AGVs are not moving in various areas.; Totes cannot be removed from hospital.; RMS or HMI shows question marks or an abnormal blank state.; RMS/HMI screen shows '.NET Control not created.' |
| Tentative internal patterns | OptiSweep service termination around 06:36 correlated with AGVs going out of sync and site stoppage.; Abnormal RMS/HMI blank state with '.NET Control not created.' may be a useful indicator during this response path.; Concurrent WCSWebApplication application-log and database-command errors were present near the same time as the service failure.; Ignition gateway restart and status review were used as part of the troubleshooting path, but the incident evidence does not prove Ignition was the confirmed root cause. |
| Affected systems/components | OptiSweep service; AGV/robotic system; RMS / Geek+ RMS; Ignition gateway; Windows Event Viewer; Windows Services; WCSWebApplication; GetAgvStatuses API endpoint |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | high |
| Confidence reason | The incident contains a clear technical response path supported by multiple evidence types: site symptom reports, Event Viewer service-failure evidence, Windows Services state, Ignition status/restart evidence, API validation evidence, and case comments stating that resetting OptiSweep and fixing out-of-sync AGVs in RMS restored operation. |

**Summary:** Use this response pattern when a site reports that nothing is moving, the robotic system is not responding, small sort is not running, or multiple AGVs are not moving, and support needs to determine whether a named service or gateway issue is involved, recover the supported service path, correct any AGVs left out of sync in RMS, and validate that motion has resumed.

#### Support User Language Examples

- UPS haslet nothing is moving
- robotic system not responding
- small sort not running
- 4-6 bots currently not moving in various areas
- they can't remove totes from hospital either
- question marks on HMI
- there was no fault or any failed AGVs

#### Negative Or Absent Signals

- Site reported no obvious fault or failed AGV visible during initial report.
- Memory review shared in the incident did not indicate memory alone caused the crash.

#### Nodes

| # | Type | Title | Intent | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm site-wide stoppage pattern and abnormal interface state | Determine whether the reported issue matches the broad stoppage pattern that warrants checking the OptiSweep, RMS, and Ignition recovery path. | Procedure needed to confirm with the site whether movement is stopped across the site or affected areas, whether small sort is not running, whether totes cannot be removed from hospital, and whether HMI or RMS shows question marks or a blank '.NET Control not created.' state. In RMS or the relevant HMI view, inspect the affected ACB System 1 / RMS screen and any visible AGV or system error sections for abnormal blank-state indicators. | Initial reports described nothing moving, robotic system not responding, small sort not running, bots not moving, hospital tote removal blocked, question marks on HMI, and RMS/H... |
| 2 | diagnostic_decision | Check for OptiSweep service failure and related application evidence | Determine whether the stoppage correlates with an OptiSweep service termination and nearby application-log errors that support the service-recovery path. | Procedure needed to inspect Windows Event Viewer on the affected host, including the System log for Service Control Manager Event 7031 involving the OptiSweep service and the Application log for clustered WCSWebApplication, Application Error, or Windows Error Reporting events around the reported outage time. The procedure should also cover how to capture the relevant timestamps and correlate them to the site stoppage. | The incident includes explicit Event Viewer evidence of OptiSweep terminating unexpectedly at 06:36:02 and nearby WCSWebApplication database-command and application errors. |
| 3 | procedure_reference | Perform approved recovery for the affected service or gateway path | Carry out the supported recovery action for the named service or gateway when the diagnostic evidence supports that path and the role is authorized. | Procedure needed for authorized recovery of the OptiSweep service and, if required by the approved support path, the Ignition gateway. The procedure must include required safety preconditions such as any site stop or E-stop prerequisites referenced in the incident, role limits for who may perform the recovery, and how to determine when the gateway is back up enough to continue validation. | Case comments state the OptiSweep service was reset after the crash. Separate incident evidence also shows an Ignition gateway restart being initiated and guidance that Ignition... |
| 4 | diagnostic_decision | Determine whether AGVs remain out of sync after service recovery | Check whether the service or gateway recovery left AGVs in an abnormal synchronization or mapping state that still blocks site operation. | Procedure needed to inspect Geek+ RMS or the relevant fleet/roster/map view for AGVs that are out of sync, missing from expected zones, removed unexpectedly, or otherwise abnormal after OptiSweep recovery. The procedure should cover how to identify the specific AGV IDs or zones requiring correction using RMS system errors, AGV errors, roster, or map-monitor evidence. | The incident states that after the OptiSweep reset, RMS was used to locate AGVs that were out of sync and fix them one by one. Separate comments mention a possibly removed AGV a... |
| 5 | procedure_reference | Correct identified out-of-sync AGVs in RMS | Apply the approved RMS-based correction process to the specific AGVs or zones identified as abnormal after service recovery. | Procedure needed for authorized RMS correction of AGVs that remain out of sync after OptiSweep recovery, including how to work through identified AGV IDs or zones one by one in Geek+ RMS and any safety or role restrictions that apply before returning the site to automated operation. | The case comment explicitly states that out-of-sync AGVs were fixed one by one in RMS after the OptiSweep service reset. |
| 6 | validation_gate | Validate service responsiveness, AGV status, and site recovery | Confirm that the service and gateway path are responsive, AGV status data is returning, RMS no longer shows blocking abnormal state, and the site can resume automated work. | Procedure needed to validate recovery by checking OptiSweep in Windows Services, reviewing the Ignition Systems Overview page if that component was part of the recovery path, sending the GetAgvStatuses request to the incident-evidenced API endpoint and interpreting HTTP status plus returned AGV records, and confirming in Geek+ RMS and with the site that automated movement or auto bag-out has resumed. | Validation evidence includes OptiSweep shown running in Windows Services, GetAgvStatuses returning HTTP 200 with NORMAL statuses, Ignition status page responsiveness, and case c... |
| 7 | escalation_gate | Stop and escalate if supported recovery path does not restore stable operation | Hand off when the supported checks and authorized recovery path do not identify a safe next step, AGVs cannot be resynchronized, or validation fails after recovery. | Procedure needed to prepare escalation handoff evidence including Windows Event Viewer System log evidence for OptiSweep Event 7031, Application log evidence for WCSWebApplication or Application Error events, Windows Services state for OptiSweep, Ignition status or restart evidence if used, GetAgvStatuses response evidence, RMS screenshots showing remaining out-of-sync or missing AGVs, and a summary of all recovery and validation actions attempted. | The incident shows multiple subsystems involved and mentions database-team review of a faulted web application. Escalation is appropriate if the supported recovery path fails or... |

#### Extraction Notes

- Exactly one playbook candidate was returned per the variant A cardinality rule.
- The candidate merges the strongest source-supported troubleshooting path: confirm broad stoppage symptoms, verify service failure evidence, perform authorized service/gateway recovery, correct out-of-sync AGVs in RMS, then validate recovery.
- Ignition restart evidence is included as part of the troubleshooting path because it appears in the incident, but it is not treated as the confirmed root cause.
- WCSWebApplication, memory-usage, and log-size observations are retained as tentative internal context and escalation evidence, not as required runtime entry criteria or confirmed diagnosis.
- Exact restart commands and detailed operational steps were intentionally kept out of nodes and represented only as runbook placeholders.
