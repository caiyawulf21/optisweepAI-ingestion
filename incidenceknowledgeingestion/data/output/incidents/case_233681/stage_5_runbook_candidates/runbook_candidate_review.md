# Stage 5 Runbook Candidate Review - Case 233681

## Summary

| Metric | Value |
| --- | --- |
| Candidates | 1 |
| Validation errors | 0 |
| Warnings | 0 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 1 |
| Candidates with events | 1 |

## Counts

### Procedure Types

| Type | Count |
| --- | --- |
| diagnostic | 1 |

### Roles

| Role | Count |
| --- | --- |
| L2_support | 1 |

## Candidate Index

| Candidate | Type | Role | Confidence | Artifacts | Events | Summary |
| --- | --- | --- | --- | --- | --- | --- |
| candidate_incident_233681_xle_communication_diagnostic | diagnostic | L2_support | medium | artifact_incident_233681_page_004_nested_image_01, artifact_incident_233681_page_005_nested_image_01, artifact_incident_233681_page_006_detected_region_01, artifact_incident_233681_page_012_nested_image_01 | incident_233681_event_005, incident_233681_event_006, incident_233681_event_008, incident_233681_event_009, incident_233681_event_017 | Use the RMS / fleet status UI, Ignition gateway, and S-Tunnel / Chat path to compare AGV and task state with XLE communication indicators. The incident showed no reported AGV fa... |

## Candidate Details

### Diagnose XLE communication loss using RMS, Ignition gateway, and S-Tunnel / Chat path

| Field | Value |
| --- | --- |
| Candidate ID | candidate_incident_233681_xle_communication_diagnostic |
| Goal | Determine whether tote-exchange and sorter stoppage is associated with active XLE communication loss, abnormal RMS task state, or S-Tunnel communication errors. |
| Type | diagnostic |
| Role | L2_support |
| Confidence | medium |
| Status | needs_review |

**Summary:** Use the RMS / fleet status UI, Ignition gateway, and S-Tunnel / Chat path to compare AGV and task state with XLE communication indicators. The incident showed no reported AGV faults or crashes, 80 canceled and 88 received tasks, repeated lost-communication messages, failed TCP connectivity checks on port 42400, and stunnel errors. Do not modify firewall or service configuration from this diagnostic procedure.

#### Rough Steps

- Open the RMS / fleet status UI and check the current robot status, current task data, and tote-exchange or bag-out operating state. Record whether AGVs are reported as faulted or crashed and record the displayed canceled and received task counts. [Image support needed: RMS screen showing current robot status, task data, and any active fault or communication indicators.]
- Open the Ignition gateway Systems Overview or status view and check for a current or recent message stating lost communication to XLEs. Compare the live result with the incident evidence, which showed repeated communication-lost entries and failed TCP connectivity checks on port 42400. [Image support needed: Ignition status or diagnostic view showing the XLE communication status or the source-documented connectivity result.]
- Open the S-Tunnel / Chat path and check the connection list and current error state for stunnel communication. Record whether stunnel errors are present and whether scanners or the sorter are reported as unable to communicate with the system. [Image support needed: S-Tunnel / Chat path view showing the connection list or stunnel error state.]
- Compare the three live observations: RMS task and AGV state, XLE communication status, and S-Tunnel errors. A communication-related abnormal state is supported when XLE loss or stunnel errors coincide with tote exchange or sorter communication failure, even when no AGV fault or crash is reported.

**Expected result:** For a recovered live job, the XLE communication-loss indication and stunnel errors should be absent, connectivity should no longer show the source-documented failed TCP result on port 42400, and the site should be able to exchange totes and sort again. The incident reported sorting resumed, but did not provide independent sustained live-system validation.

#### Failure Or Escalation Notes

- Stop the diagnostic and escalate to L2/L3 or the site network owner if XLE communication remains lost, stunnel continues to report errors, TCP connectivity remains failed, or the sorter remains non-communicating.
- Do not change firewall rules, restart undocumented services, or perform a system purge from this diagnostic candidate; the incident does not document the required controls or exact corrective change.
- If RMS shows no AGV faults or crashes but task counts or tote exchange remain abnormal, retain the communication evidence and escalate rather than treating the condition as an AGV hardware fault.

#### Access Or Tools Needed

- RMS / fleet status UI
- Ignition gateway
- S-Tunnel / Chat path
- Source-documented Test-NetConnection diagnostic against the documented XLE targets on port 42400

#### Extraction Notes

- The incident provides a repeatable diagnostic pattern but not a complete confirmed recovery procedure.
- Several IP addresses and some command fields in the connectivity screenshot are OCR-uncertain; this candidate deliberately does not reproduce those endpoint values.
- The recorded firewall explanation and sorting recovery are incident evidence, not a documented firewall change or independently validated sustained live result.
- The artifact classified as a Windows Services screenshot contains chat evidence and does not directly show a service restart control.
