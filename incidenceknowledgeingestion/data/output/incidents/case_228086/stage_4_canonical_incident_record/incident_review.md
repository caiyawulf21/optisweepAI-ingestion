# Stage 4 Incident Review - Case 228086

## Canonical Summary

| Field | Value |
| --- | --- |
| Incident | UPS Haslet robotic system not responding; AGVs out of sync after OptiSweep service crash |
| Status | resolved |
| Validation status | needs_sme_review |
| Site | UPS Fort Worth, TX (Haslet) |
| Reported at | 2026-02-20T07:19:00 |
| Resolved at | 2026-02-20T14:58:00 |
| Resolution time | 7h 39m |
| Downtime minutes | 459 |
| KPI confidence | medium |
| Timeline events | 38 |
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

## Incident Narrative

**Description:** High-priority production incident at the UPS Haslet/Fort Worth site where the robotic system stopped responding and site movement halted. Source evidence shows OptiSweep service termination at about 06:36, AGVs going out of sync, abnormal RMS/HMI state, and concurrent WCS web application/database-related errors. Investigation included Event Viewer review, Ignition status checks, service-state checks, API validation, and RMS review of affected AGVs.

**Operational impact:** Production was seriously impacted. Evidence states nothing was moving, the robotic system was not responding, the small sort was not running, bots could not move in various areas, and the site had to manually bag out before resuming automated bag-out activity.

**Resolution:** Source-supported recovery evidence says the OptiSweep service was reset after the crash, then RMS was used to locate and fix AGVs that were out of sync, after which the site resumed the auto bag-out procedure. Additional investigation noted a faulted webservice/web application associated with memory usage and log-size tracking.

## Symptoms

- Nothing was moving at the site.
- Robotic system was reported as not responding.
- Small sort was not running.
- Multiple bots/AGVs were not moving and AGVs were reported out of sync.
- RMS/HMI evidence showed an abnormal blank state with '.NET Control not created.'
- Application and service errors were recorded around 2026-02-20 06:35-06:36, including WCSWebApplication errors and an OptiSweep service termination.

## Systems Involved

- OptiSweep service
- AGV/robotic system
- RMS / Geek+ RMS
- Ignition gateway
- WCSWebApplication
- Windows Event Viewer / Service Control Manager
- CBRE ServiceInsight work order system

## Follow Up Required

- SME review of location ambiguity between Haslet/Fort Worth and Alliance, TX references.
- SME review of whether WCS web application memory/log growth was a related contributing issue or a separate concurrent fault.
- Confirm whether KPI should measure full customer downtime or case-handling duration.
- Review service/application logs and Event Viewer evidence around 06:35-06:36 for final incident classification.

## Warnings

- Resolved timestamp relies on Stage 4 review evidence rather than extracted OCR/artifact inputs.
- Location is ambiguous across Haslet/Fort Worth/TXRTH and an apparent Alliance, TX reference.
- Concurrent OptiSweep and WCS web application faults are documented, but root cause and causal ordering remain uncertain.
- stage4_page_chunk_001: Pages 3-5 contain garbled OCR; events from those pages rely on enriched artifact evidence and are lower confidence.
- stage4_page_chunk_001: Several Teams message timestamps in pages 2 and 6-7 appear inconsistent or partially garbled in OCR; partial or missing timestamp status was used where needed.
- stage4_page_chunk_001: Excluded generic meeting-link and add-to-call logistics unless they materially affected incident communication state.
- stage4_page_chunk_002: Several pages in this chunk have low, garbled, or missing OCR; artifact evidence was used where available.
- stage4_page_chunk_002: Some case status changes and comments in page 21 do not show visible timestamps in the provided OCR.
- stage4_page_chunk_002: Page 26 contains attributed statements about memory usage causing a webservice fault; recorded as source-reported diagnostic notes, not resolved root cause.
- stage4_page_chunk_003: Page OCR contains some garbled event IDs and host text; confidence was reduced where exact values were uncertain.
- stage4_page_chunk_003: Only events supported by pages 27-29 and linked artifact evidence were included.

## Timeline

| # | Timestamp | Type | Summary | Systems | Confidence | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | partial | symptom_reported | Site reported multiple bots not moving after a heartbeat issue. | OptiSweep, AGV/robotic system | medium | case_228086:page_2 / stage4_page_chunk_001 |
| 2 | partial | symptom_reported | Additional site impact reported: totes could not be removed from hospital and question marks were visible on the HMI. | HMI, Ignition | medium | case_228086:page_2 / stage4_page_chunk_001 |
| 3 | partial | symptom_reported | Site contact reported that nothing was moving during normal operation and there was no fault or failed AGV visible. | AGV/robotic system | medium | case_228086:page_2 / stage4_page_chunk_001 |
| 4 | missing | diagnostic_evidence_shared | RMS screen evidence showed an abnormal blank state with a message indicating '.NET Control not created.' | RMS, ACB System 1 | low | case_228086:page_3 / artifact_incident_228086_page_003_embedded_image_01 / stage4_page_chunk_001 |
| 5 | missing | diagnostic_evidence_shared | RMS screenshot showed '.NET Control not created.' on a mostly blank status page. | RMS, ACB System 1 | medium | case_228086:page_5 / artifact_incident_228086_page_005_embedded_image_01 / stage4_page_chunk_001 |
| 6 | partial | action_taken | A responder confirmed being on RDP. | RDP | medium | case_228086:page_6 / stage4_page_chunk_001 |
| 7 | 2026-02-20T09:03 | diagnostic_request | A 24-hour Ignition Server memory snapshot was requested to check for a crash. | Ignition Server | high | case_228086:page_6 / stage4_page_chunk_001 |
| 8 | partial | follow_up | Possible Sunday onsite startup support was raised if the Ignition root cause remained unknown. | Ignition | medium | case_228086:page_6 / stage4_page_chunk_001 |
| 9 | 2026-02-20T09:17 | diagnostic_evidence_shared | Memory trend was shared for review. | Ignition Server | high | case_228086:page_7 / stage4_page_chunk_001; case_228086:page_8 / artifact_incident_228086_page_008_embedded_image_01 / stage4_page_chunk_001 |
| 10 | 2026-02-20T09:24 | status_update | Site was finishing bagout and troubleshooting would resume after the e-stop was removed. | system | high | case_228086:page_7 / stage4_page_chunk_001 |
| 11 | 2026-02-20T05:24 | validation_result | Memory review found no indication that memory caused a crash. | Ignition Server | medium | case_228086:page_7 / stage4_page_chunk_001; case_228086:page_8 / artifact_incident_228086_page_008_embedded_image_01 / stage4_page_chunk_001 |
| 12 | 2026-02-20T09:24 | status_update | UPS was no longer on the line and was manually bagging out. |  | high | case_228086:page_7 / stage4_page_chunk_001 |
| 13 | 2026-02-20T09:45 | action_taken | A direction was given to start the tippers. | tippers | high | case_228086:page_9 / stage4_page_chunk_001 |
| 14 | 2026-02-20T09:50 | status_update | Support reported that the site was done with bagging out. |  | medium | case_228086:page_10 / stage4_page_chunk_001 |
| 15 | 2026-02-20T09:52 | diagnostic_note | A support participant stated that from the system state it never started bag out. | system | medium | case_228086:page_10 / stage4_page_chunk_001 |
| 16 | 2026-02-20T11:43 | diagnostic_note | A zone was reported missing an AGV in system errors. | RMS | medium | case_228086:page_11 / stage4_page_chunk_002 |
| 17 | missing | diagnostic_note | Memory trend was reported as looking better. | Ignition | medium | case_228086:page_12 / stage4_page_chunk_002 |
| 18 | missing | follow_up | Restart guidance was shared for use if Ignition needed to be restarted. | Ignition, OptiSweep | medium | case_228086:page_12 / stage4_page_chunk_002 |
| 19 | missing | action_taken | An Ignition gateway restart command was executed. | Ignition | high | case_228086:page_15 / stage4_page_chunk_002 |
| 20 | missing | diagnostic_evidence_shared | Ignition Systems Overview page was captured showing the gateway responding. | Ignition | medium | case_228086:page_16 / stage4_page_chunk_002 |
| 21 | missing | validation_result | GetAgvStatuses API check returned data successfully. | OptiSweep, AGV/robotic system | medium | case_228086:page_17 / stage4_page_chunk_002 |
| 22 | missing | validation_result | OptiSweep service was shown running in Windows Services. | OptiSweep | medium | case_228086:page_19 / stage4_page_chunk_002 |
| 23 | missing | symptom_reported | Case 00228086 was created for a site-wide motion stoppage. | AGV/robotic system | high | case_228086:page_21 / stage4_page_chunk_002 |
| 24 | missing | case_status_change | Case status was updated from New to In Progress. |  | high | case_228086:page_21 / stage4_page_chunk_002 |
| 25 | missing | diagnostic_note | Investigation focused on a possibly removed AGV. | AGV/robotic system | high | case_228086:page_21 / stage4_page_chunk_002 |
| 26 | missing | case_status_change | Case workflow later showed transitions to Resolved and then RCA Pending. |  | medium | case_228086:page_21 / stage4_page_chunk_002 |
| 27 | missing | diagnostic_evidence_shared | A SQL query was used during a Teams call to inspect AGV state values. | AGV/robotic system, RMS | low | case_228086:page_24 / artifact_incident_228086_page_024_embedded_image_01 / stage4_page_chunk_002 |
| 28 | missing | symptom_reported | A CBRE emergency work order recorded that the robotic system was not responding and the small sort was not running. | AGV/robotic system, small sort | high | case_228086:page_25 / artifact_incident_228086_page_025_embedded_image_01 / stage4_page_chunk_002 |
| 29 | 2026-02-20T06:36 | system_event | OptiSweep service crash at 6:36 AM was reported as causing AGVs to go out of sync and the system to stop. | OptiSweep, AGV/robotic system | high | case_228086:page_26 / stage4_page_chunk_002 |
| 30 | missing | diagnostic_note | Event Viewer was checked for service failures or errors. | Windows Event Viewer, OptiSweep | high | case_228086:page_26 / stage4_page_chunk_002 |
| 31 | missing | action_taken | OptiSweep service was reset and out-of-sync AGVs were corrected in RMS. | OptiSweep, RMS, AGV/robotic system | high | case_228086:page_26 / stage4_page_chunk_002 |
| 32 | missing | status_update | Site resumed the auto bag out procedure after AGV resynchronization work. | AGV/robotic system, RMS | high | case_228086:page_26 / stage4_page_chunk_002 |
| 33 | missing | escalation | Database team assistance was requested to investigate a faulted web application. | WCSWebApplication, database | medium | case_228086:page_26 / stage4_page_chunk_002 |
| 34 | missing | diagnostic_note | A webservice application fault was attributed in the source to memory usage and log growth concerns. | webservice application, infrastructure | medium | case_228086:page_26 / stage4_page_chunk_002 |
| 35 | 2026-02-20T06:35:24 | system_event | Application log shows WCSWebApplication error event 20102 with failed database command execution. | WCSWebApplication, Windows Event Viewer, Application log, fortna-wcs-primary.txrth.otnet.ups.com | high | case_228086:page_28 / artifact_incident_228086_page_028_embedded_image_01 / stage4_page_chunk_003; case_228086:page_28 / artifact_incident_228086_page_028_embedded_image_01 / stage4_artifact_chunk_003 |
| 36 | 2026-02-20T06:36:02 | system_event | Application log shows clustered WCSWebApplication and Application Error entries. | WCSWebApplication, Windows Event Viewer, Application log | medium | case_228086:page_27 / artifact_incident_228086_page_027_embedded_image_01 / stage4_page_chunk_003; case_228086:page_27 / artifact_incident_228086_page_027_embedded_image_01 / stage4_artifact_chunk_003 |
| 37 | 2026-02-20T06:36:02 | system_event | System log records OptiSweep service terminating unexpectedly with automatic restart scheduled. | OptiSweep service, Service Control Manager, Windows Event Viewer, System log | high | case_228086:page_29 / artifact_incident_228086_page_029_embedded_image_01 / stage4_page_chunk_003; case_228086:page_29 / artifact_incident_228086_page_029_embedded_image_01 / stage4_artifact_chunk_003 |
| 38 | 2026-02-20T06:36:07 | system_event | Windows Error Reporting event 1001 is logged in the Application log. | Windows Error Reporting, Windows Event Viewer, Application log | high | case_228086:page_27 / artifact_incident_228086_page_027_embedded_image_01 / stage4_page_chunk_003; case_228086:page_27 / artifact_incident_228086_page_027_embedded_image_01 / stage4_artifact_chunk_003 |

## Timeline Review Notes

### Event 1: Site reported multiple bots not moving after a heartbeat issue.
- Visible time on the page is inconsistent/partial due to OCR noise.
- The exact wording around the building report is partially garbled.

### Event 2: Additional site impact reported: totes could not be removed from hospital and question marks were visible on the HMI.
- The message combines observed symptoms with a diagnostic question.
- Exact timestamp is partial due to OCR.

### Event 3: Site contact reported that nothing was moving during normal operation and there was no fault or failed AGV visible.
- Part of the sentence is truncated by OCR.
- Garrett's full identity/role is not fully established in this chunk.

### Event 4: RMS screen evidence showed an abnormal blank state with a message indicating '.NET Control not created.'
- Artifact OCR is garbled.
- Operational significance of the message is uncertain.

### Event 5: RMS screenshot showed '.NET Control not created.' on a mostly blank status page.
- No reliable event timestamp is extracted from the page OCR.
- The screenshot timestamp/location string in artifact enrichment may be imperfect due to garbled OCR.

### Event 6: A responder confirmed being on RDP.
- Timestamp is partially garbled by OCR.

### Event 8: Possible Sunday onsite startup support was raised if the Ignition root cause remained unknown.
- The final word is truncated by OCR.
- This is a follow-up planning item, not a confirmed action.

### Event 9: Memory trend was shared for review.
- The chart does not itself confirm cause of crash.

### Event 11: Memory review found no indication that memory caused a crash.
- The visible timestamp on Michael Langley's message may be OCR-distorted.
- This is an attributed diagnostic conclusion, not definitive root cause.

### Event 13: A direction was given to start the tippers.
- The message records guidance/action direction, not confirmation that the tippers were started.

### Event 14: Support reported that the site was done with bagging out.
- The sentence is slightly ungrammatical in OCR but the status update is clear.

### Event 15: A support participant stated that from the system state it never started bag out.
- The message may combine a diagnostic observation with coordination guidance.

### Event 16: A zone was reported missing an AGV in system errors.
- The visible timestamp appears to be 2/15/2026, which may be historical context rather than the main incident day.

### Event 17: Memory trend was reported as looking better.
- No visible timestamp is provided for this statement.
- The chart threshold meaning is not explicitly labeled.

### Event 18: Restart guidance was shared for use if Ignition needed to be restarted.
- This is guidance shared in the source, not proof that all steps were executed at this point.

### Event 19: An Ignition gateway restart command was executed.
- The screenshot does not show the final restart outcome.

### Event 20: Ignition Systems Overview page was captured showing the gateway responding.
- No visible timestamp is shown for when this status page was captured.
- The incident relevance of the `License Incomplete` banner is unclear.

### Event 21: GetAgvStatuses API check returned data successfully.
- The screenshot supports successful API response, but the schema mismatch warning may or may not be incident-relevant.

### Event 22: OptiSweep service was shown running in Windows Services.
- No visible timestamp is shown for this service-state capture.
- The screenshot does not prove whether a restart had just occurred.

### Event 23: Case 00228086 was created for a site-wide motion stoppage.
- The exact case creation timestamp is not visible in the provided page OCR.

_Additional events with uncertainties omitted from Markdown: 11._
