# Stage 5 Runbook Candidate Review - Case 228086

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
| recovery | 1 |

### Roles

| Role | Count |
| --- | --- |
| L2_support | 1 |

## Candidate Index

| Candidate | Type | Role | Confidence | Artifacts | Events | Summary |
| --- | --- | --- | --- | --- | --- | --- |
| candidate_incident_228086_restart_ignition_and_verify_optisweep_response | recovery | L2_support | medium | artifact_incident_228086_page_014_embedded_image_01, artifact_incident_228086_page_015_embedded_image_01, artifact_incident_228086_page_016_embedded_image_01, artifact_incident_228086_page_017_embedded_image_01, artifact_incident_228086_page_019_embedded_image_01, artifact_incident_228086_page_012_nested_image_02 | incident_228086_event_018, incident_228086_event_019, incident_228086_event_020, incident_228086_event_021, incident_228086_event_022 | The incident packet includes a conditional restart sequence for Ignition: first E-stop the system, restart Ignition, wait until the gateway is back up and login is possible, the... |

## Candidate Details

### Restart Ignition and verify OptiSweep service response with GetAgvStatuses

| Field | Value |
| --- | --- |
| Candidate ID | candidate_incident_228086_restart_ignition_and_verify_optisweep_response |
| Goal | Perform the source-shared Ignition restart sequence safely and confirm the OptiSweep service is responding again before releasing the E-stop. |
| Type | recovery |
| Role | L2_support |
| Confidence | medium |
| Status | needs_review |

**Summary:** The incident packet includes a conditional restart sequence for Ignition: first E-stop the system, restart Ignition, wait until the gateway is back up and login is possible, then verify OptiSweep is responding by sending a GetAgvStatuses request. If no response is returned, restart OptiSweep, send the request again, and once confirmed release the E-stop.

#### Rough Steps

- First E-stop the system before attempting the restart. [Image support needed: RMS or system control context showing an emergency stop control area referenced in the source.]
- Restart Ignition using the shown command sequence from a Windows command prompt in the Ignition installation directory; the source shows `gwcmd -r` and a console message `Waiting for Gateway restart...`. [Image support needed: command prompt in `C:\Program Files\Inductive Automation\Ignition>` showing `gwcmd -r` and `Waiting for Gateway restart...`.]
- Wait for Ignition to come back up, meaning it lets you log in and does not show the gateway starting up. [Image support needed: Ignition Status > Systems > Overview page reachable in the browser rather than a startup screen.]
- Verify the OptiSweep service is still responding after Ignition is restarted by opening the API client and sending a GetAgvStatuses request to the shown endpoint. [Image support needed: API client showing GET `http://10.27.80.165:5000/GetAgvStatuses`.]
- Check that the API request returns HTTP 200 and returned AGV records, with visible statuses such as `NORMAL`. [Image support needed: API response panel showing Success/Status 200 and returned records with `NORMAL` values.]
- If no response is given, restart OptiSweep, then send another GetAgvStatuses request to confirm response. [Image support needed: Windows Services console with OptiSweep selected and restart control visible.]
- Once the response is confirmed, release the E-stop.

**Expected result:** Ignition is reachable again, the OptiSweep service responds to GetAgvStatuses, and the E-stop can be released after confirmation. The endpoint returns HTTP 200 with AGV status records, and visible records include expected status values such as NORMAL.

#### Failure Or Escalation Notes

- If Ignition does not come back up to a login-capable state, stop and do not perform undocumented changes beyond the source-shared restart sequence.
- If GetAgvStatuses gives no response after the Ignition restart, the source says to restart OptiSweep and repeat the request.
- If response still cannot be confirmed after the documented restart steps, stop and escalate rather than inventing additional recovery actions.
- If the request does not return a response, the source-linked restart guidance says OptiSweep may need to be restarted before retrying.
- Do not treat the schema validation warning alone as a service outage; the incident shows it alongside a successful HTTP 200 response.
- If the endpoint is unreachable or returns no data, stop and use only source-supported recovery actions.

#### Access Or Tools Needed

- Access to the system E-stop control
- Windows command prompt on the Ignition host
- Ignition installation directory access
- Ignition web status/login page access
- API client identified in the source as api dog
- Access to the GetAgvStatuses endpoint
- Windows Services access for OptiSweep restart if needed
- Network access to `http://10.27.80.165:5000/GetAgvStatuses`
- Permission to query the OptiSweep API

#### Extraction Notes

- The restart sequence is explicitly presented as conditional guidance in the incident, not as a confirmed full execution path at that moment.
- The packet supports the command `gwcmd -r`, the wait condition, the API validation step, the no-response contingency, and E-stop release.
- The packet does not provide a documented Windows Services click-by-click restart sequence for OptiSweep, so that substep is kept high level.
- This candidate is limited to the API validation check evidenced in the packet.
- The packet supports the endpoint, HTTP 200 check, returned records, and visible NORMAL values.
- The schema mismatch warning is included as an observed check result, not as a failure conclusion.
- Merged validation follow-up candidate into this recovery runbook: candidate_incident_228086_validate_optisweep_agv_status_api_response
