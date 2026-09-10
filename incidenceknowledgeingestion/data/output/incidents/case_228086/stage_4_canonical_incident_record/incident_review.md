# Stage 4 Incident Review - Case 228086

## Canonical Summary

| Field | Value |
| --- | --- |
| Incident | UPS Haslet robotic system not responding; AGVs out of sync and small sort stopped |
| Status | resolved |
| Validation status | needs_sme_review |
| Site | UPS Fort Worth, TX (Haslet) |
| Reported at | 2026-02-20T07:19:00 |
| Resolved at | 2026-02-20T14:58:00 |
| Resolution time | 7h 39m |
| Downtime minutes | 459 |
| KPI confidence | medium |
| Timeline events | 50 |
| Canonical validation errors | 0 |
| Timeline validation errors | 0 |

## KPI Tracking

| Field | Value |
| --- | --- |
| Start | 2026-02-20T07:19:00 |
| End | 2026-02-20T14:58:00 |
| Elapsed minutes | 459 |
| Basis | Use CBRE/work-order entry time as the source-supported tracking start and the Salesforce close comment stating the site is running as the tracking end. |
| Confidence | medium |

### KPI Notes

- The close timestamp is user-provided review evidence from a Salesforce comment screenshot.
- The tracking start is the current best extracted source-supported start time, not necessarily the first physical failure moment.
- KPI tracking start (2026-02-20T07:19:00) is later than 8 earlier timeline signal(s).

## Early Failure Signals (Before KPI Start)

| Timestamp | Type | Summary | Linked event |
| --- | --- | --- | --- |
| 2026-02-20T06:21:00 | status_update | Reported site said nothing was moving and there were no faults or failed AGVs. | incident_228086_event_003 |
| 2026-02-20T06:54:00 | system_event | RMS screenshot showed mostly blank ACB System 1 page with ".NET Control not created." | incident_228086_event_006 |
| 2026-02-20T06:36:07 | system_event | Windows Error Reporting Event 1001 was logged in the Application log. | incident_228086_event_044 |
| 2026-02-20T06:36:02 | system_event | Multiple WCSWebApplication and Application Error entries were visible around 6:36:02 AM. | incident_228086_event_045 |
| 2026-02-20T06:35:24 | system_event | WCSWebApplication Event ID 20102 logged a database command execution failure. | incident_228086_event_046 |
| 2026-02-20T06:35:24 | system_event | Application log showed WCSWebApplication error Event ID 20102 with failed DbCommand execution. | incident_228086_event_047 |
| 2026-02-20T06:35:24 | system_event | Multiple WCSWebApplication errors were visible in Event Viewer at 6:35:24 AM. | incident_228086_event_048 |
| 2026-02-20T06:36:02 | system_event | Service Control Manager logged that the OptiSweep service terminated unexpectedly. | incident_228086_event_049 |

## Linked Timeline Events

- incident_228086_event_013
- incident_228086_event_029
- incident_228086_event_032
- incident_228086_event_037
- incident_228086_event_039
- incident_228086_event_044
- incident_228086_event_045
- incident_228086_event_046
- incident_228086_event_049
- incident_228086_event_050
- incident_228086_event_003
- incident_228086_event_006

## Incident Narrative

**Description:** High-priority production incident at the UPS Fort Worth/Haslet site where the robotic system stopped responding and site operations reported that nothing was moving. Evidence shows OptiSweep service termination at about 6:36 AM, concurrent WCSWebApplication/application errors, AGVs going out of sync, and abnormal RMS/HMI behavior. Troubleshooting included Event Viewer review, Ignition gateway restart activity, service-state checks, API validation checks, and RMS review of AGV state. Case comments indicate the OptiSweep service was reset, out-of-sync AGVs were corrected in RMS, and the site resumed auto bag-out before later being reported as running.

**Operational impact:** Production was seriously impacted. The small sort was not running, bots were not moving in various areas, totes could not be removed from hospital, and the site shifted to manual bag-out during part of the incident.

**Resolution:** Source-supported recovery actions indicate the OptiSweep service was reset, RMS was used to locate and correct out-of-sync AGVs, and the site resumed auto bag-out. Later review evidence states the site was running at case close. Memory/log-size follow-up for the faulted web application was noted but not confirmed as the definitive incident fix.

## Symptoms

- Nothing was moving at the site.
- Robotic system was reported as not responding.
- Small sort was not running.
- AGVs were reported out of sync.
- RMS/HMI showed a mostly blank screen with message '.NET Control not created.'
- WCSWebApplication and application errors were visible around 6:35-6:36 AM.
- OptiSweep service termination event was recorded at 6:36 AM.

## Systems Involved

- OptiSweep service
- AGVs / robotic system
- RMS / HMI
- Ignition gateway
- WCSWebApplication
- Windows Event Viewer / Service Control Manager
- CBRE ServiceInsight work order system

## Follow Up Required

- SME review of whether memory usage and log growth were contributing factors for the faulted web application.
- Confirm exact operational recovery time from original Salesforce close comment evidence.
- Review location ambiguity between Haslet/Fort Worth and Alliance, TX references.
- Review whether removed or out-of-sync AGV conditions require separate corrective tracking.

## Warnings

- Resolved time is based on Stage 4 review evidence rather than extracted OCR/artifact content in the original package.
- Location evidence is ambiguous between Haslet/Fort Worth TXRTH site references and an RMS screenshot showing Alliance, TX.
- Several pages/artifacts have garbled or missing OCR, so some details remain uncertain.
- Memory/log-size issue is recorded as a source-reported contributing concern, not a confirmed root cause.
- stage4_page_chunk_001: Pages 3-5 rely primarily on artifact evidence because page OCR is garbled.
- stage4_page_chunk_001: Page 4 appears to be a duplicate of page 3; retained only one additional event because it adds distinct visible detail (Primary tab and OPC Server: Primary).
- stage4_page_chunk_001: Several page 2 and page 6 timestamps/messages contain OCR noise or merged chat lines.
- stage4_page_chunk_002: Page 14 OCR was garbled; artifact evidence was used as the primary source for that page.
- stage4_page_chunk_002: Several timestamps in Teams content are only partially visible, so timestamps were left null and preserved in details/source quotes.
- stage4_page_chunk_002: Pages 9-11 were mostly meeting logistics and were largely excluded except where they reflected incident state or customer-impacting coordination.
- stage4_page_chunk_003: Pages 20, 22, and 23 did not provide usable OCR for timeline extraction in this chunk.
- stage4_page_chunk_003: Page 24 relied on artifact evidence because page OCR was low quality.
- stage4_page_chunk_003: Some screenshots provide state snapshots without visible timestamps, so several events use timestamp_status 'missing'.
- stage4_page_chunk_003: Case workflow status changes on page 21 are recorded as case events and not treated as direct proof of operational recovery.
- stage4_page_chunk_004: Page 25 OCR was garbled; artifact evidence was used as the primary source for that page.
- stage4_page_chunk_004: Several page 26 comment timestamps are only partially visible, so timestamps were left null with partial status.
- stage4_page_chunk_004: Some Event Viewer OCR on pages 27-28 contains noisy event IDs or hostnames; uncertainties were preserved.
- stage4_artifact_chunk_001: This extraction used artifact evidence cards as the primary source for pages 3-13 in the current chunk.
- stage4_artifact_chunk_001: Several artifacts in this chunk have garbled or low-quality OCR; confidence was reduced and uncertainties were preserved.
- stage4_artifact_chunk_001: Page 4 duplicate RMS monitor photo was not emitted as a separate event because it was a near-duplicate of page 3 without materially new incident state.
- stage4_artifact_chunk_002: No reliable visible timestamps were available in this evidence chunk for most events, so timestamps were left null.
- stage4_artifact_chunk_002: Page 21 case workflow status changes were included as case-status evidence, but they do not independently prove operational recovery.
- stage4_artifact_chunk_002: Page 14 and page 24 artifacts were included with lower confidence because their operational significance is not fully clear from the screenshots alone.
- stage4_artifact_chunk_003: Page 26 chat timestamps are only partially visible, so those events use timestamp null with timestamp_status partial.
- stage4_artifact_chunk_003: Pages 26 embedded thumbnails were excluded as separate events because their contents are unreadable and do not add distinct supported incident state beyond the chat narrative.
- Timeline event incident_228086_evt_005 timestamp 2026-02-20T06:21:00 appears before earlier event incident_228086_evt_004 (2026-02-20T08:14:00); verify OCR or source order.
- Timeline event incident_228086_evt_008 timestamp 2026-02-20T06:36:07 appears before earlier event incident_228086_evt_003_005 (2026-02-23T09:18:00); verify OCR or source order.
- Timeline event incident_228086_evt_009 timestamp 2026-02-20T06:36:02 appears before earlier event incident_228086_evt_008 (2026-02-20T06:36:07); verify OCR or source order.
- Timeline event incident_228086_evt_010 timestamp 2026-02-20T06:35:24 appears before earlier event incident_228086_evt_009 (2026-02-20T06:36:02); verify OCR or source order.

## Timeline

| # | Timestamp | Type | Summary | Systems | Confidence | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | partial | symptom_reported | Reported bots not moving after a heartbeat issue. | OptiSweep service, AGVs / robotic system | medium | case_228086:page_2 / stage4_page_chunk_001 |
| 2 | 2026-02-20T08:14:00 | symptom_reported | Reported totes could not be removed from hospital and HMI showed question marks; asked if Ignition crashed. | HMI, Ignition gateway | medium | case_228086:page_2 / stage4_page_chunk_001 |
| 3 | 2026-02-20T06:21:00 | status_update | Reported site said nothing was moving and there were no faults or failed AGVs. | AGVs / robotic system | medium | case_228086:page_2 / stage4_page_chunk_001 |
| 4 | missing | diagnostic_evidence_shared | RMS screen showed ACB System 1 with apparent message "NET Control not created." | RMS / HMI, AGVs / robotic system, ACB System 1 | medium | case_228086:page_3 / artifact_incident_228086_page_003_embedded_image_01 / stage4_page_chunk_001; case_228086:page_3 / artifact_incident_228086_page_003_embedded_image_01 / stage4_artifact_chunk_001 |
| 5 | missing | diagnostic_evidence_shared | Duplicate RMS view showed Primary tab and OPC Server: Primary with blank main panel. | RMS / HMI, OPC Server | medium | case_228086:page_4 / artifact_incident_228086_page_004_embedded_image_01 / stage4_page_chunk_001 |
| 6 | 2026-02-20T06:54:00 | system_event | RMS screenshot showed mostly blank ACB System 1 page with ".NET Control not created." | RMS / HMI | medium | case_228086:page_5 / artifact_incident_228086_page_005_embedded_image_01 / stage4_page_chunk_001 |
| 7 | missing | symptom_reported | RMS screenshot showed a mostly blank page with the visible message ".NET Control not created." | RMS / HMI, ACB System 1 | medium | case_228086:page_5 / artifact_incident_228086_page_005_embedded_image_01 / stage4_artifact_chunk_001 |
| 8 | 2026-02-20T09:03:00 | diagnostic_request | Requested a 24-hour snapshot of Ignition server memory usage to check for a crash. | Ignition gateway, server memory, memory monitoring | high | case_228086:page_6 / stage4_page_chunk_001; case_228086:page_6 / artifact_incident_228086_page_006_full_page_01 / stage4_artifact_chunk_001 |
| 9 | missing | diagnostic_request | A Teams message asked whether someone knew how to verify an Ignition crash and walk UPS through restarting the server if needed. | Ignition gateway | high | case_228086:page_6 / artifact_incident_228086_page_006_full_page_01 / stage4_artifact_chunk_001 |
| 10 | partial | follow_up | Reported request for Sunday onsite startup support if Ignition root cause remained unknown. | Ignition gateway | medium | case_228086:page_6 / stage4_page_chunk_001 |
| 11 | partial | diagnostic_evidence_shared | Memory trend was shared for review. | Ignition gateway, memory monitoring | medium | case_228086:page_7 / stage4_page_chunk_002; case_228086:page_8 / artifact_incident_228086_page_008_embedded_image_01 / stage4_page_chunk_002 |
| 12 | partial | diagnostic_request | Support asked how to determine whether Ignition had crashed and how to restart it if needed. | Ignition gateway | high | case_228086:page_7 / stage4_page_chunk_002 |
| 13 | partial | status_update | Site was finishing bagout and troubleshooting had to wait until the e-stop was removed. | site operations, bagout process | high | case_228086:page_7 / stage4_page_chunk_002 |
| 14 | partial | diagnostic_note | Memory review did not indicate that memory caused a crash. | Ignition gateway, memory monitoring, CPU monitoring | high | case_228086:page_7 / stage4_page_chunk_002; case_228086:page_8 / artifact_incident_228086_page_008_embedded_image_01 / stage4_page_chunk_002 |
| 15 | partial | status_update | UPS was no longer on the hotline and was manually bagging out. | site operations, bagout process | high | case_228086:page_7 / stage4_page_chunk_002 |
| 16 | missing | diagnostic_evidence_shared | Memory trend chart showed high memory followed by a sharp drop and lower sustained usage. | Ignition gateway, memory monitoring | medium | case_228086:page_8 / artifact_incident_228086_page_008_embedded_image_01 / stage4_page_chunk_002; case_228086:page_8 / stage4_page_chunk_002; case_228086:page_8 / artifact_incident_228086_page_008_embedded_image_01 / stage4_artifact_chunk_001 |
| 17 | partial | diagnostic_note | Memory trend was reported as looking better. | Ignition gateway, memory monitoring | high | case_228086:page_12 / stage4_page_chunk_002; case_228086:page_12 / artifact_incident_228086_page_012_nested_image_01 / stage4_page_chunk_002; case_228086:page_13 / artifact_incident_228086_page_013_embedded_image_01 / stage4_page_chunk_002 |
| 18 | missing | action_taken | An Ignition gateway restart command was shown as being run. | Ignition gateway, Windows command prompt | medium | case_228086:page_12 / artifact_incident_228086_page_012_nested_image_02 / stage4_page_chunk_002; case_228086:page_12 / stage4_page_chunk_002; case_228086:page_12 / artifact_incident_228086_page_012_nested_image_02 / stage4_artifact_chunk_001 |
| 19 | missing | validation_check | A Get Agv Statuses request was identified as the post-restart validation check for OptiSweep responsiveness. | OptiSweep service, AGVs / robotic system, API Dog | high | case_228086:page_12 / stage4_page_chunk_002 |
| 20 | missing | validation_result | A later memory trend chart showed usage remaining below a higher red line with no visible threshold crossing. | memory monitoring, Ignition gateway | medium | case_228086:page_13 / artifact_incident_228086_page_013_embedded_image_01 / stage4_artifact_chunk_001 |
| 21 | missing | diagnostic_evidence_shared | RMS map screenshot showed a selected robot in GO_CHARGING state and an emergency stop control area highlighted. | RMS / HMI, AGVs / robotic system | medium | case_228086:page_14 / artifact_incident_228086_page_014_embedded_image_01 / stage4_page_chunk_002; case_228086:page_14 / artifact_incident_228086_page_014_embedded_image_01 / stage4_artifact_chunk_002 |
| 22 | missing | action_taken | Ignition gateway restart command was executed from the Ignition installation directory. | Ignition gateway, Windows command prompt | high | case_228086:page_15 / artifact_incident_228086_page_015_embedded_image_01 / stage4_page_chunk_003; case_228086:page_15 / artifact_incident_228086_page_015_embedded_image_01 / stage4_artifact_chunk_002 |
| 23 | missing | diagnostic_evidence_shared | Ignition Systems Overview page showed the gateway responding with no recent slow response events. | Ignition gateway | medium | case_228086:page_16 / artifact_incident_228086_page_016_embedded_image_01 / stage4_page_chunk_003; case_228086:page_16 / artifact_incident_228086_page_016_embedded_image_01 / stage4_artifact_chunk_002 |
| 24 | missing | validation_result | Ignition Systems Overview showed the gateway responding with 11 ms current response time and no recent slow response events. | Ignition gateway | medium | case_228086:page_16 / artifact_incident_228086_page_016_embedded_image_01 / stage4_artifact_chunk_002 |
| 25 | missing | validation_result | GetAgvStatuses API request returned HTTP 200 with AGV records. | OptiSweep service, AGVs / robotic system, API client | medium | case_228086:page_17 / artifact_incident_228086_page_017_embedded_image_01 / stage4_page_chunk_003; case_228086:page_17 / artifact_incident_228086_page_017_embedded_image_01 / stage4_artifact_chunk_002 |
| 26 | missing | validation_check | A GetAgvStatuses API check returned HTTP 200 with data, but the response failed schema validation. | AGVs / robotic system | medium | case_228086:page_17 / artifact_incident_228086_page_017_embedded_image_01 / stage4_artifact_chunk_002 |
| 27 | missing | validation_result | API validation reported a schema mismatch despite the successful response. | API client, AGVs / robotic system | medium | case_228086:page_17 / artifact_incident_228086_page_017_embedded_image_01 / stage4_artifact_chunk_002 |
| 28 | 2026-02-23T09:18:00 | validation_check | Instructions recorded to verify OptiSweep responsiveness after Ignition restart using a Get Statuses request. | OptiSweep service, Ignition gateway, API client | high | case_228086:page_18 / stage4_page_chunk_003 |
| 29 | missing | validation_result | OptiSweep service was shown as running in Windows Services. | OptiSweep service, Windows Services | high | case_228086:page_19 / artifact_incident_228086_page_019_embedded_image_01 / stage4_page_chunk_003; case_228086:page_19 / artifact_incident_228086_page_019_embedded_image_01 / stage4_artifact_chunk_002; case_228086:page_19 / artifact_incident_228086_page_019_embedded_image_01 / stage4_artifact_chunk_002 |
| 30 | missing | symptom_reported | Case was created for a site-wide motion stoppage at UPS Haslet. | Salesforce case system, AGVs / robotic system | high | case_228086:page_21 / stage4_page_chunk_003; case_228086:page_21 / artifact_incident_228086_page_021_full_page_01 / stage4_artifact_chunk_002 |
| 31 | missing | symptom_reported | The Salesforce case recorded the incident subject as 'UPS haslet nothing is moving' with high production impact. | AGVs / robotic system | high | case_228086:page_21 / artifact_incident_228086_page_021_full_page_01 / stage4_artifact_chunk_002 |
| 32 | missing | case_status_change | Case status changed from New to In Progress. | Salesforce case system | high | case_228086:page_21 / stage4_page_chunk_003; case_228086:page_21 / artifact_incident_228086_page_021_full_page_01 / stage4_artifact_chunk_002; case_228086:page_21 / stage4_page_chunk_003 |
| 33 | missing | diagnostic_note | Investigation focused on a possibly removed AGV that was not known to be removed. | AGVs / robotic system | medium | case_228086:page_21 / stage4_page_chunk_003; case_228086:page_21 / artifact_incident_228086_page_021_full_page_01 / stage4_artifact_chunk_002 |
| 34 | missing | diagnostic_evidence_shared | A Teams troubleshooting call reviewed SQL query results showing multiple AGV state values. | AGVs / robotic system, SQL Server Management Studio, Teams, RMS / HMI | medium | case_228086:page_24 / artifact_incident_228086_page_024_embedded_image_01 / stage4_page_chunk_003; case_228086:page_24 / artifact_incident_228086_page_024_embedded_image_01 / stage4_artifact_chunk_002; case_228086:page_24 / artifact_incident_228086_page_024_embedded_image_01 / stage4_artifact_chunk_002 |
| 35 | missing | symptom_reported | CBRE work order records an emergency site issue with the robotic system not responding and small sort not running. | CBRE ServiceInsight work order system, AGVs / robotic system, small sort | high | case_228086:page_25 / artifact_incident_228086_page_025_embedded_image_01 / stage4_page_chunk_004; case_228086:page_25 / artifact_incident_228086_page_025_embedded_image_01 / stage4_artifact_chunk_003 |
| 36 | partial | diagnostic_note | Investigation focused on whether any service failed or whether Event Viewer showed an error. | Windows Event Viewer, services | medium | case_228086:page_26 / stage4_page_chunk_004; case_228086:page_26 / artifact_incident_228086_page_026_full_page_01 / stage4_artifact_chunk_003 |
| 37 | partial | system_event | OptiSweep service crash at 6:36 AM was reported as causing AGVs to go out of sync and the system to stop. | OptiSweep service, AGVs / robotic system | high | case_228086:page_26 / stage4_page_chunk_004 |
| 38 | partial | status_update | Chat update reported the OptiSweep service crashed at 6:36 AM, AGVs went out of sync, and the system stopped. | OptiSweep service, AGVs / robotic system | medium | case_228086:page_26 / artifact_incident_228086_page_026_full_page_01 / stage4_artifact_chunk_003 |
| 39 | partial | action_taken | After resetting the OptiSweep service, the team used RMS to find and fix AGVs that were out of sync. | OptiSweep service, RMS / HMI, AGVs / robotic system | high | case_228086:page_26 / stage4_page_chunk_004 |
| 40 | partial | action_taken | Chat update said the OptiSweep service was reset and out-of-sync AGVs were corrected in RMS. | OptiSweep service, RMS / HMI, AGVs / robotic system | medium | case_228086:page_26 / artifact_incident_228086_page_026_full_page_01 / stage4_artifact_chunk_003 |
| 41 | partial | status_update | Site resumed the auto bag out procedure after out-of-sync AGVs were corrected. | RMS / HMI, AGVs / robotic system, auto bag out procedure | medium | case_228086:page_26 / stage4_page_chunk_004; case_228086:page_26 / artifact_incident_228086_page_026_full_page_01 / stage4_artifact_chunk_003 |
| 42 | partial | diagnostic_note | Investigation shifted to a faulted web application, with database-team assistance requested. | web application, database, backup server | medium | case_228086:page_26 / stage4_page_chunk_004 |
| 43 | partial | diagnostic_evidence_shared | A webservice application was reported faulted because of memory usage, with log size identified for continued tracking. | webservice application, infrastructure, logs | medium | case_228086:page_26 / stage4_page_chunk_004 |
| 44 | 2026-02-20T06:36:07 | system_event | Windows Error Reporting Event 1001 was logged in the Application log. | Windows Event Viewer, Windows Error Reporting, Application log, WCSWebApplication | high | case_228086:page_27 / artifact_incident_228086_page_027_embedded_image_01 / stage4_page_chunk_004; case_228086:page_27 / artifact_incident_228086_page_027_embedded_image_01 / stage4_artifact_chunk_003 |
| 45 | 2026-02-20T06:36:02 | system_event | Multiple WCSWebApplication and Application Error entries were visible around 6:36:02 AM. | WCSWebApplication, Windows Event Viewer, Application log | high | case_228086:page_27 / artifact_incident_228086_page_027_embedded_image_01 / stage4_page_chunk_004 |
| 46 | 2026-02-20T06:35:24 | system_event | WCSWebApplication Event ID 20102 logged a database command execution failure. | WCSWebApplication, Windows Event Viewer, Application log, database | high | case_228086:page_28 / artifact_incident_228086_page_028_embedded_image_01 / stage4_page_chunk_004 |
| 47 | 2026-02-20T06:35:24 | system_event | Application log showed WCSWebApplication error Event ID 20102 with failed DbCommand execution. | WCSWebApplication, Windows Event Viewer, Application log, fortna-wcs-primary.txrth.otnet.ups.com | medium | case_228086:page_28 / artifact_incident_228086_page_028_embedded_image_01 / stage4_artifact_chunk_003 |
| 48 | 2026-02-20T06:35:24 | system_event | Multiple WCSWebApplication errors were visible in Event Viewer at 6:35:24 AM. | WCSWebApplication, Windows Event Viewer, Application log | medium | case_228086:page_28 / artifact_incident_228086_page_028_embedded_image_01 / stage4_page_chunk_004 |
| 49 | 2026-02-20T06:36:02 | system_event | Service Control Manager logged that the OptiSweep service terminated unexpectedly. | OptiSweep service, Service Control Manager, Windows Event Viewer, System log | high | case_228086:page_29 / artifact_incident_228086_page_029_embedded_image_01 / stage4_page_chunk_004; case_228086:page_29 / artifact_incident_228086_page_029_embedded_image_01 / stage4_artifact_chunk_003 |
| 50 | 2026-02-20T06:36:02 | action_taken | Automatic corrective action was configured to restart the OptiSweep service after 60000 milliseconds. | OptiSweep service, Service Control Manager, Windows Event Viewer, System log | high | case_228086:page_29 / artifact_incident_228086_page_029_embedded_image_01 / stage4_page_chunk_004 |

## Timeline Review Notes

### Event 1: Reported bots not moving after a heartbeat issue.
- Part of the message is truncated/garbled around the OptiSweep reference.

### Event 2: Reported totes could not be removed from hospital and HMI showed question marks; asked if Ignition crashed.
- OCR punctuation and spacing are noisy.

### Event 3: Reported site said nothing was moving and there were no faults or failed AGVs.
- Part of the sentence is truncated by OCR, but the main incident state is readable.

### Event 4: RMS screen showed ACB System 1 with apparent message "NET Control not created."
- Artifact and page OCR are garbled.
- Exact wording and operational significance of the message require SME review.
- Exact message wording is not fully reliable.
- Operational significance of the displayed message is unclear.

### Event 5: Duplicate RMS view showed Primary tab and OPC Server: Primary with blank main panel.
- This page is marked as a duplicate of page 3 evidence.
- OCR is garbled and small text is uncertain.

### Event 6: RMS screenshot showed mostly blank ACB System 1 page with ".NET Control not created."
- Timestamp and location are taken from artifact interpretation, not clean OCR.
- Operational impact beyond the visible UI state is not directly shown.

### Event 7: RMS screenshot showed a mostly blank page with the visible message ".NET Control not created."
- Bottom error details are unreadable.
- Artifact OCR is garbled.
- The visible timestamp/location noted in artifact enrichment is not fully reliable.

### Event 8: Requested a 24-hour snapshot of Ignition server memory usage to check for a crash.
- Actor name for this specific request is not clearly supported.

### Event 9: A Teams message asked whether someone knew how to verify an Ignition crash and walk UPS through restarting the server if needed.
- This is a request/discussion, not a confirmed action.

### Event 10: Reported request for Sunday onsite startup support if Ignition root cause remained unknown.
- Timestamp is not clearly readable.
- The final word is truncated by OCR.

### Event 11: Memory trend was shared for review.
- The page OCR does not fully preserve the surrounding sentence context for how the chart was shared.

### Event 14: Memory review did not indicate that memory caused a crash.
- The chart shows a notable memory change, but the message explicitly says it did not indicate a crash.

### Event 16: Memory trend chart showed high memory followed by a sharp drop and lower sustained usage.
- The chart does not itself label the cause or significance of the drop.
- No explicit alarm or crash label is visible.
- Meaning of the red horizontal line is not labeled.

### Event 17: Memory trend was reported as looking better.
- The exact threshold meaning on the chart is not labeled.
- The chart crop does not label the threshold/reference line.
- The exact metric name is not fully readable inside the crop.

### Event 18: An Ignition gateway restart command was shown as being run.
- The exact command text is partially garbled.
- The screenshot does not show the final restart outcome.
- Exact command syntax is unclear due to low-quality OCR.
- The screenshot does not show whether the gateway restart succeeded.
- The failed ls -1 command is incidental and not evidence of incident outcome.

### Event 20: A later memory trend chart showed usage remaining below a higher red line with no visible threshold crossing.
- The red line is not explicitly labeled.
- A normal-looking memory trend does not by itself rule out incident relevance.

### Event 21: RMS map screenshot showed a selected robot in GO_CHARGING state and an emergency stop control area highlighted.
- It is unclear whether the emergency stop was active or simply highlighted for attention.
- Page OCR for this page was garbled, so interpretation relies on artifact enrichment.
- It is unclear whether the emergency stop was active or only highlighted.
- OCR is garbled and surrounding page context is unreliable.

### Event 22: Ignition gateway restart command was executed from the Ignition installation directory.
- No visible timestamp is provided for the command execution.
- The screenshot does not show whether the restart completed successfully.

### Event 23: Ignition Systems Overview page showed the gateway responding with no recent slow response events.
- No visible timestamp is shown for this status snapshot.
- The incident relevance of the 'License Incomplete' banner is unclear.

### Event 24: Ignition Systems Overview showed the gateway responding with 11 ms current response time and no recent slow response events.
- The License Incomplete banner may be incidental rather than incident-relevant.
- No timestamp is visible for when this status snapshot was captured.

_Additional events with uncertainties omitted from Markdown: 25._
