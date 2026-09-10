# Windows Event Viewer / services check for OptiSweep and WCSWebApplication failures

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_windows_event_viewer_services_optisweep_wcs_failures_v1` |
| Title | Windows Event Viewer / services check for OptiSweep and WCSWebApplication failures |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `windows_service_or_event_log`, `wcs_service_health` |
| Access Surface | `event_viewer` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | `service_crash_or_restart`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Windows Event Viewer / services surface to inspect Application and System log entries around the reported 6:35-6:36 AM failure window, then verify the current OptiSweep service state. The check identifies WCSWebApplication database-command errors, OptiSweep termination events, and the live service status before further recovery action.

## When To Use

Use the Windows Event Viewer / services surface when OptiSweep or WCSWebApplication behavior is abnormal, the RMS is blank or unavailable, the system has stopped, or a service failure is suspected. Inspect the reported 6:35:24-6:36:07 AM window when validating this incident pattern before further recovery action.

## Do Not Use For

* Do not use Windows Event Viewer / services alone to infer root cause.
* Do not use this check as a substitute for RMS AGV status when the OptiSweep service is confirmed healthy.
* Do not make undocumented database, configuration, or infrastructure changes based only on Event Viewer entries.

## Safety And Operational Notes

* This is an inspection procedure. Do not infer root cause or perform undocumented database, configuration, or infrastructure changes from the Windows Event Viewer / services findings alone.
* The Event ID 7031 automatic restart message records configured corrective action; it does not by itself confirm that the restart succeeded.

## Access Or Tools Needed

* Windows Event Viewer / services
* Windows Logs > Application in Windows Event Viewer / services
* Windows Logs > System in Windows Event Viewer / services
* Windows Services MMC on the Windows Event Viewer / services surface
* OptiSweep service

## Visual References

![artifact_incident_228086_page_027_embedded_image_01](assets/abd43e133aa30f1d.jpeg)

*Windows Event Viewer / services Application log showing clustered WCSWebApplication and Application Error entries around 6:36:02 AM, with Windows Error Reporting Event 1001 at 6:36:07 AM.*

![artifact_incident_228086_page_028_embedded_image_01](assets/d4f3abbd8bd09df2.jpeg)

*Windows Event Viewer / services Application log showing WCSWebApplication Event ID 20102 and the message "Failed executing DbCommand (1,840ms)" at 6:35:24 AM.*

![artifact_incident_228086_page_029_embedded_image_01](assets/dabb6bbd62f07c7c.png)

*Windows Event Viewer / services System log showing Service Control Manager Event ID 7031 for unexpected OptiSweep termination and a configured restart after 60000 milliseconds.*

![artifact_incident_228086_page_019_embedded_image_01](assets/3832c5ce44b05a86.png)

*Windows Services MMC on the Windows Event Viewer / services surface with OptiSweep selected, showing Status Running and Startup Type Automatic.*

## Procedure Steps

### Step 1 — Inspect the Application log on Windows Event Viewer / services

**Responsible role:** L2_support

**Instruction:**
On the Windows Event Viewer / services surface, open Windows Logs > Application. Inspect entries around 6:35:24-6:36:07 AM, including WCSWebApplication Event ID 20102 with "Failed executing DbCommand (1,840ms)" and the nearby WCSWebApplication, Application Error, and Windows Error Reporting entries. Compare the source, event ID, timestamp, level, and message with the live entries.

**Expected result:**
The live Application log shows whether WCSWebApplication or Application Error entries are present in the selected time window, and the selected event exposes its source, event ID, timestamp, level, and message.

**Stop or Escalate If:**

* WCSWebApplication errors continue after the OptiSweep service is available.
* The live entries indicate an active or recurring application failure that cannot be explained by inspection alone.

---

### Step 2 — Inspect the System log on Windows Event Viewer / services

**Responsible role:** L2_support

**Instruction:**
On the Windows Event Viewer / services surface, select Windows Logs > System and inspect Service Control Manager Event ID 7031 for OptiSweep. Confirm whether the live event states that the service terminated unexpectedly and whether the recorded corrective action says Restart the service after 60000 milliseconds.

**Expected result:**
The live System log identifies whether Event ID 7031 exists for OptiSweep and displays the termination message and any recorded corrective action.

**Stop or Escalate If:**

* OptiSweep Event ID 7031 repeats.
* The event shows an unexpected termination and the current service state cannot be confirmed as Running.

---

### Step 3 — Verify OptiSweep in Windows Event Viewer / services

**Responsible role:** L2_support

**Instruction:**
On the Windows Event Viewer / services surface, open Windows Services, select OptiSweep, and inspect Status and Startup Type. Compare the current values with the Event Viewer / services findings. The incident capture showed Status Running and Startup Type Automatic; do not treat the available Restart the service link as proof that a restart was performed.

**Expected result:**
The live Windows Services MMC displays the current OptiSweep Status and Startup Type so they can be compared with the termination event.

**Stop or Escalate If:**

* OptiSweep is not Running.
* Event ID 7031 repeats or WCSWebApplication errors continue after the service is available.
* The service state cannot be reconciled with the Event Viewer / services findings.

---

## Success Criteria

* The Windows Event Viewer / services Application log has been inspected for the relevant time window and the live WCSWebApplication/Application Error state is identified.
* The Windows Event Viewer / services System log has been inspected for OptiSweep Event ID 7031 and any restart indication.
* The Windows Services MMC shows the current OptiSweep Status and Startup Type.
* No continuing WCSWebApplication errors, repeated OptiSweep Event ID 7031 events, or non-running OptiSweep state are present in the live check.

## Failure Conditions

* OptiSweep is not Running in Windows Services.
* OptiSweep Event ID 7031 repeats or continues to report unexpected termination.
* WCSWebApplication Event ID 20102 or other clustered WCSWebApplication/Application Error entries continue.
* The live evidence does not confirm that the configured automatic restart restored the service.

## Escalation Guidance

* Stop this diagnostic sequence and escalate to L2/L3 support if OptiSweep is not Running.
* Escalate if OptiSweep Event ID 7031 repeats.
* Escalate if WCSWebApplication errors continue after the service is available.
* Do not infer root cause or make undocumented database, configuration, or infrastructure changes from Event Viewer / services entries alone.

## Missing Details / Known Gaps

* The packet does not provide an ingestion site_location, site_code, or site label in source_package.site_location; the evidence-mentioned site was not substituted for authoritative ingestion metadata.
* The incident does not establish that this diagnostic sequence alone resolved the outage.
* No command-line recovery command, database remediation, configuration change, or infrastructure change is supported for this procedure.
* The Event ID 7031 automatic restart action is recorded, but successful restart completion is not directly evidenced by that event.
* No time estimate is supported by the source.

## Source Lineage

- Candidate IDs: candidate_incident_228086_event_viewer_optisweep_failure_check
- Source ID: `source_case_228086`
- Source Type: `incident_evidence_pdf`
