# Stage 5 Runbook Candidate Review - Case 223554

## Summary

| Metric | Value |
| --- | --- |
| Candidates | 1 |
| Validation errors | 0 |
| Warnings | 0 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
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
| candidate_incident_223554_hospital_tote_agv_recovery | recovery | L2_support | medium |  | incident_223554_event_020, incident_223554_event_023, incident_223554_event_031, incident_223554_event_032, incident_223554_event_039, incident_223554_event_040 | Source evidence describes an incident recovery sequence using Apidog / WCS API to remove an inducted tote and a disconnected tote, with the tipper station paused during recovery... |

## Candidate Details

### Recover hospital tote flow using Apidog / WCS API and validate AGV operation

| Field | Value |
| --- | --- |
| Candidate ID | candidate_incident_223554_hospital_tote_agv_recovery |
| Goal | Restore hospital-station tote induction and AGV flow after an inducted-tote or disconnected-tote condition, then verify that totes can be added and removed and that the system is running. |
| Type | recovery |
| Role | L2_support |
| Confidence | medium |
| Status | needs_review |

**Summary:** Source evidence describes an incident recovery sequence using Apidog / WCS API to remove an inducted tote and a disconnected tote, with the tipper station paused during recovery. The incident later reported that tote add/remove operation, robot re-addition, and overall system operation were restored. This candidate does not specify undocumented API request names or AGV controls.

#### Rough Steps

- On the Tipper HMI / WebVisu / VISU, place the station on pause before recovery when operators are not present at the tippers, so totes do not continue going to the hospital during the recovery process.
- Open Apidog / WCS API client and use the source-supported tote-removal action to remove the inducted tote that is preventing hospital flow. [Image support needed: the Apidog / WCS API request or response showing the inducted tote removal action and its result.]
- In Apidog / WCS API client, address the disconnected tote association identified for the affected AGV; for the documented tote 51 condition, use the source-supported API action when the tote cannot be removed from the hospital normally. [Image support needed: the API client view showing the affected tote association and the resulting removal status.]
- Use the source-supported AGV recovery action to take affected AGVs out of the obstructed state or location, including the AGVs identified in the incident, and re-add the robots as required by the live system state. Do not perform an undocumented AGV or tote mutation.
- On the Hospital HMI / lane UI, verify that the hospital station can add and remove totes again, and confirm that the affected robots are re-added and back up and running.
- Confirm the system is running after recovery; stop the recovery if tote operations remain unavailable, robots cannot be re-added, or the required API action or AGV state is not identifiable.

**Expected result:** The hospital station accepts tote additions and removals, affected robots are re-added and operating, and the system is running. The incident reported these conditions after recovery and stated that the issue was resolved by approximately 9:00 PM ET.

#### Failure Or Escalation Notes

- Stop before making any API or AGV state change that is not explicitly identifiable from the live system or the source-supported recovery action.
- Escalate for L2/L3 review if the tote cannot be removed through the documented Apidog / WCS API action, if the AGV association remains disconnected, or if the Hospital HMI still cannot add or remove totes.
- The incident records multiple possible contributing conditions and does not confirm one normalized root cause; do not treat the AGV/tote association explanation as definitive.

#### Access Or Tools Needed

- Apidog / WCS API client
- OptiSweep / WCS API
- Tipper HMI / WebVisu / VISU
- Hospital HMI / lane UI
- Affected AGV and tote identifiers from the live incident state

#### Extraction Notes

- The source calls the API client 'API dog' and separately states that Aveva uses the same endpoints; the live taxonomy names the verified surface as Apidog / WCS API client and OptiSweep / WCS API.
- The source gives concrete recovery actions and successful validation results but does not provide API request names, parameters, response codes, or exact AGV control names.
- The source reports AGV/tote association as a possible explanation and explicitly says the cause was not certain.
- The service-reset statements were not included as steps because the packet does not identify service names, controls, commands, or reset validation.
