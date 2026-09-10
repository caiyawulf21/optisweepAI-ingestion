# Stage 5 Runbook Candidate Review - Case 228086

## Summary

| Metric | Value |
| --- | --- |
| Candidates | 3 |
| Validation errors | 0 |
| Warnings | 0 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 3 |
| Candidates with events | 3 |

## Counts

### Procedure Types

| Type | Count |
| --- | --- |
| diagnostic | 2 |
| recovery | 1 |

### Roles

| Role | Count |
| --- | --- |
| L2_support | 3 |

## Candidate Index

| Candidate | Type | Role | Confidence | Artifacts | Events | Summary |
| --- | --- | --- | --- | --- | --- | --- |
| candidate_incident_228086_ignition_gateway_and_optisweep_validation | recovery | L2_support | medium | artifact_incident_228086_page_015_embedded_image_01, artifact_incident_228086_page_016_embedded_image_01, artifact_incident_228086_page_017_embedded_image_01, artifact_incident_228086_page_019_embedded_image_01 | incident_228086_event_018, incident_228086_event_019, incident_228086_event_022, incident_228086_event_023, incident_228086_event_024, incident_228086_event_025, incident_228086_event_026, incident_228086_event_027, incident_228086_event_028, incident_228086_event_029 | Use the Ignition gateway command prompt, Ignition gateway Systems Overview, Apidog / WCS API, and Windows Services to restart the gateway, verify the GetAgvStatuses response, an... |
| candidate_incident_228086_event_viewer_optisweep_failure_diagnostic | diagnostic | L2_support | high | artifact_incident_228086_page_027_embedded_image_01, artifact_incident_228086_page_028_embedded_image_01, artifact_incident_228086_page_029_embedded_image_01, artifact_incident_228086_page_019_embedded_image_01 | incident_228086_event_044, incident_228086_event_045, incident_228086_event_046, incident_228086_event_047, incident_228086_event_048, incident_228086_event_049, incident_228086_event_050, incident_228086_event_029 | Use Windows Event Viewer Application and System logs, then Windows Services, to correlate WCSWebApplication and OptiSweep failure evidence around 6:35-6:36 AM and check the curr... |
| candidate_incident_228086_ssms_agv_state_diagnostic | diagnostic | L2_support | low | artifact_incident_228086_page_024_embedded_image_01 | incident_228086_event_034 | Use WCS / Helix DB (SSMS) to inspect the robotics-related database query results and record the AGV State values returned during the incident-style diagnostic. |

## Candidate Details

### Ignition gateway restart and OptiSweep response validation

| Field | Value |
| --- | --- |
| Candidate ID | candidate_incident_228086_ignition_gateway_and_optisweep_validation |
| Goal | Restore and verify Ignition and OptiSweep responsiveness before returning the system to operation. |
| Type | recovery |
| Role | L2_support |
| Confidence | medium |
| Status | needs_review |

**Summary:** Use the Ignition gateway command prompt, Ignition gateway Systems Overview, Apidog / WCS API, and Windows Services to restart the gateway, verify the GetAgvStatuses response, and restart OptiSweep only when the API does not respond. A site operator performs the physical E-stop and release; support must not release it until API response is confirmed.

#### Rough Steps

- Have the site operator place the system in the physical E-stop state before the source-supported restart sequence; do not release the E-stop during recovery.
- Open a Windows Administrator Command Prompt, navigate to the Inductive Automation Ignition installation directory, run the source-shown `gwcmd -r` command, and wait for the console to indicate `Waiting for Gateway restart...`. [Image support needed: Windows Command Prompt showing the Ignition directory, `gwcmd -r`, and the gateway-restart waiting message.]
- Open the Ignition gateway at the Systems Overview page and check that the gateway responds, including the Current Response Time indicator and Recent Slow Response Events section. The incident evidence showed 11 ms and `No events to display`. [Image support needed: Ignition Status > Systems > Overview showing Current Response Time and Recent Slow Response Events.]
- Open Apidog / WCS API and send the `GetAgvStatuses` request. Check for HTTP Success/Status 200 and returned AGV records; the incident response showed records with visible `NORMAL` status values. [Image support needed: Apidog GetAgvStatuses request with HTTP 200 and returned AGV records.]
- If the status request does not respond, open Windows Services, select `OptiSweep`, use the visible `Restart the service` control, and then send `GetAgvStatuses` again. [Image support needed: Windows Services with OptiSweep selected and the Restart the service control visible.]
- After the API response is confirmed, have the site operator release the physical E-stop and confirm that the site can resume the auto bag-out operation.

**Expected result:** Ignition Systems Overview responds; GetAgvStatuses returns HTTP 200 with AGV records, with status values such as NORMAL visible in the response; OptiSweep is shown as Running in Windows Services if the service restart was required; and the site can resume auto bag-out after the operator releases the E-stop.

#### Failure Or Escalation Notes

- Stop before releasing the physical E-stop if GetAgvStatuses does not return a response after the documented OptiSweep restart and repeat check.
- Escalate if the Ignition gateway does not return to the Systems Overview page, the API remains nonresponsive, or OptiSweep does not show Running.
- The API evidence also showed a response-schema warning (`Response data differs from endpoint spec` and `$ should be object`); record that warning for review even when HTTP 200 and AGV records are returned.

#### Access Or Tools Needed

- Ignition gateway
- Windows Administrator Command Prompt
- Apidog / WCS API client
- OptiSweep / WCS API
- Windows Event Viewer / services
- GetAgvStatuses request
- Physical floor / grid for site-operator E-stop and release

#### Extraction Notes

- The Ignition restart was shown as initiated, but the command screenshot did not show completion; the later Ignition status and API evidence provide partial validation.
- The source records an E-stop precondition and release-after-confirmation instruction, but the physical E-stop must be performed by the site operator, not L2 support.
- The source-package site_location object is empty. Evidence identifies the site as UPS Fort Worth, TX (Haslet), but ingestion site metadata was not available to populate site_code or site_location.

### Windows Event Viewer and Services diagnostic for OptiSweep and WCSWebApplication failures

| Field | Value |
| --- | --- |
| Candidate ID | candidate_incident_228086_event_viewer_optisweep_failure_diagnostic |
| Goal | Confirm whether the incident includes the source-observed OptiSweep service termination and clustered WCSWebApplication errors before performing further recovery. |
| Type | diagnostic |
| Role | L2_support |
| Confidence | high |
| Status | needs_review |

**Summary:** Use Windows Event Viewer Application and System logs, then Windows Services, to correlate WCSWebApplication and OptiSweep failure evidence around 6:35-6:36 AM and check the current OptiSweep service state.

#### Rough Steps

- Open Windows Event Viewer and select Windows Logs > Application. Check the entries around 2/20/2026 6:35:24-6:36:07 AM for WCSWebApplication errors, including Event ID 20102 with `Failed executing DbCommand (1,840ms)`, and nearby Application Error or Windows Error Reporting entries. [Image support needed: Event Viewer Application log showing the clustered WCSWebApplication errors and Event ID 20102 details.]
- Select Windows Logs > System and open the Service Control Manager event for OptiSweep. Check for Event ID 7031, Level Error, stating that the OptiSweep service terminated unexpectedly and that Windows planned a restart in 60000 milliseconds. [Image support needed: Event Viewer System log Event 7031 showing the OptiSweep termination and 60000-millisecond restart message.]
- Open Windows Services, select `OptiSweep`, and record whether Status is `Running` and Startup Type is `Automatic`. [Image support needed: Windows Services with OptiSweep selected and its Running status and Automatic startup type visible.]
- Compare the Event Viewer timestamps and service state with the live incident state; do not treat the configured automatic restart as proof that recovery completed.

**Expected result:** The diagnostic record identifies whether the live logs contain the source-observed WCSWebApplication database-command error and OptiSweep Event 7031 termination, and Windows Services shows whether OptiSweep is currently Running with Automatic startup.

#### Failure Or Escalation Notes

- Stop and escalate if Event Viewer shows new or repeated WCSWebApplication errors, Event 7031 repeats, or OptiSweep is not Running.
- Do not infer root cause from the clustered errors; the incident evidence supports correlation but not a definitive cause.
- A configured automatic restart after 60000 milliseconds does not confirm that the service successfully restarted.

#### Access Or Tools Needed

- Windows Event Viewer / services
- Windows Logs > Application
- Windows Logs > System
- Windows Services
- WCSWebApplication Event ID 20102
- OptiSweep Service Control Manager Event ID 7031

#### Extraction Notes

- The event evidence clearly documents failures and a configured restart action, but does not establish root cause.
- The service-state screenshot has no timestamp and does not prove whether the Running state was before or after a restart.
- The source-package site_location object is empty. Evidence identifies the site as UPS Fort Worth, TX (Haslet), but ingestion site metadata was not available to populate site_code or site_location.

### WCS / Helix DB (SSMS) AGV state inspection

| Field | Value |
| --- | --- |
| Candidate ID | candidate_incident_228086_ssms_agv_state_diagnostic |
| Goal | Inspect live AGV state records in SSMS when RMS reports AGVs out of sync or the robotic system is stopped. |
| Type | diagnostic |
| Role | L2_support |
| Confidence | low |
| Status | needs_review |

**Summary:** Use WCS / Helix DB (SSMS) to inspect the robotics-related database query results and record the AGV State values returned during the incident-style diagnostic.

#### Rough Steps

- Open WCS / Helix DB (SSMS) and connect to the robotics-related database context shown in the incident evidence.
- Run the source-provided robotics AGV state check without adding undocumented query text, and wait for the SSMS status bar to show that the query executed successfully. [Image support needed: SSMS robotics-related database window with the query results grid and successful execution status.]
- Inspect the returned State column and record the visible values, including examples shown in the incident such as LeavingCharger, MovingToChargerExitQueue, MovingToSorterExitQueue, MovingToTipperQueue, SQExchanging, SQStagingExchange, SWaitingForExchange, and SWaitingInzone.
- Compare the returned AGV state records with the live RMS / fleet status UI; do not change database values from this read-only diagnostic.

**Expected result:** SSMS executes the source-provided check successfully and returns a populated AGV results grid with State values. The result is a diagnostic record for comparison with RMS / fleet status UI, not proof that any listed state is faulty by itself.

#### Failure Or Escalation Notes

- Stop and escalate if SSMS cannot connect, the query does not execute successfully, or the expected AGV state results are unavailable.
- Do not infer that a listed state is abnormal without the corresponding live RMS context or SME interpretation.
- Do not modify database records; the incident evidence supports read-only state inspection only.

#### Access Or Tools Needed

- WCS / Helix DB (SSMS)
- Robotics-related database context
- AGV State column
- RMS / fleet status UI

#### Extraction Notes

- The packet does not provide a reliable database name, table name, model name, or complete SQL statement; Stage 6 should supply any query detail only from validated source material.
- The operational meaning of the listed AGV states is not established by the incident evidence alone.
- The source-package site_location object is empty. Evidence identifies the site as UPS Fort Worth, TX (Haslet), but ingestion site metadata was not available to populate site_code or site_location.
