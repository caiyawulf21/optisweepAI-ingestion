# Check AGV State, Command Vitals, and Errors in the OptiSweep WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_agv_state_command_vitals_and_errors_in_the_optisweep_wcs_api_v1` |
| Title | Check AGV State, Command Vitals, and Errors in the OptiSweep WCS API |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | `L2_support` |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors`, `robot_command_or_task_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support`, `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog to inspect an AGV's live state, current command fields, vitals, network identity, AGV errors, system errors, and errorAlert indicator.

## When To Use

Use this Apidog / OptiSweep WCS API diagnostic when support needs to verify an AGV's live state, current command information, vitals, network identity, or AGV and system error indications.

## Do Not Use For

* Do not use this procedure to remove, recover, pause, resume, or execute an AGV command.
* Do not use this procedure to infer a healthy battery or voltage range; the source provides example values but no complete operating thresholds.
* Do not use this procedure as a physical AGV recovery or E-stop procedure.

## Safety And Operational Notes

* This procedure is diagnostic and does not direct a production stop, physical intervention, or AGV control request.
* Do not substitute a control request such as PauseAgvs, RemoveAgv, RecoverAgv, or Resend Geek Command for this read-only status inspection.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client on the primary server
* The AGV request labeled "Get Agv Statuses"

## Related Operational Context

* ctx_training_video_agv_status_screen_v1
* ctx_training_video_agv_status_fields_v1
* ctx_training_video_agv_error_alert_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Apidog / WCS API overview showing the AGVS area and the Get Agv Statuses request.*

![artifact_training_video_training_video_day2_0030_get_agv_status_shows_the_current_primary_02_43_04_500](assets/30f5c770747ce298.jpg)

*Get Agv Statuses response showing AGV name, state, command fields, battery, voltage, status, IP, error fields, and errorAlert.*

## Procedure Steps

### Step 1 — Open Get Agv Statuses in the Apidog WCS API client

**Responsible role:** L1_support

**Instruction:**
In the Apidog / WCS API client, open the AGVS area and select the request labeled "Get Agv Statuses".

**Expected result:**
The Get Agv Statuses request is open and can return an AGV status response.

**Stop or Escalate If:**

* Stop the diagnostic and escalate to L2_support if the Get Agv Statuses response cannot be obtained.

---

### Step 2 — Identify the AGV and inspect its state in the Apidog WCS API response

**Responsible role:** L1_support

**Instruction:**
In the Apidog / WCS API response, locate the affected AGV by its "name" and review its "state". Record the returned value exactly, including values such as "AtSorterEntranceQueue" or "SWaitingInzone".

**Expected result:**
The response identifies the AGV and provides its current state value.

**Stop or Escalate If:**

* Escalate to L2_support if the response does not identify the AGV or provide its state.

---

### Step 3 — Inspect current command fields in the Apidog WCS API response

**Responsible role:** L1_support

**Instruction:**
In the Apidog / WCS API response for the identified AGV, review "commandGuid", "commandName", and "commandStatus". Record empty command fields as empty.

**Expected result:**
The response shows the available command GUID, command name, and command status values for the AGV.

**Stop or Escalate If:**

* Escalate to L2_support if the command fields are unavailable or cannot be associated with the affected AGV.

---

### Step 4 — Inspect AGV vitals and network identity in the Apidog WCS API

**Responsible role:** L1_support

**Instruction:**
In the Apidog / WCS API response, review "battery", "voltage", "status", and "ip" for the identified AGV. Record the displayed values without applying an unsupported battery or voltage threshold.

**Expected result:**
The response provides the AGV's displayed battery value, voltage value, status, and IP address.

**Stop or Escalate If:**

* Escalate to L2_support if the response does not provide the AGV vitals or network identity needed for the diagnostic.

---

### Step 5 — Inspect AGV and system errors in the Apidog WCS API response

**Responsible role:** L1_support

**Instruction:**
In the Apidog / WCS API response, review "errorCode", "errorDescription", "errorCause", "systemErrorDescription", "systemErrorResolution", and "errorAlert". Treat populated error fields or "errorAlert": true as reported error indications. For active system errors, the related error information can include the error name, area, error code, last-seen time, system error description, and system error resolution.

**Expected result:**
The response shows the AGV and system error fields and indicates whether errorAlert is true or false.

**Stop or Escalate If:**

* Escalate to L2_support when "errorAlert" is true.
* Escalate when AGV or system error fields contain a reported error requiring further investigation.

---

## Success Criteria

* The Apidog / WCS API Get Agv Statuses request returns a response.
* The affected AGV is identified by name and its state is recorded.
* Command fields, vitals, status, IP, AGV error fields, system error fields, and errorAlert are reviewed.
* Any reported error or true errorAlert is escalated to L2_support.

## Failure Conditions

* The Get Agv Statuses response cannot be obtained.
* The response does not identify the AGV or does not provide state and error fields.
* AGV or system error fields are populated.
* errorAlert is true.

## Escalation Guidance

* Escalate to L2_support if the Apidog / OptiSweep WCS API response cannot be obtained or does not contain the required AGV state and error fields.
* Escalate to L2_support when errorAlert is true or AGV or system error fields contain a reported error.
* Include the AGV name, state, command fields, vitals, IP, error fields, system error fields, and errorAlert value in the escalation record.

## Missing Details / Known Gaps

* The source does not define complete healthy or failure thresholds for battery, voltage, or AGV state values.
* The source does not provide the exact API endpoint, authentication method, or request execution control beyond the Get Agv Statuses request label.
* The source does not define an escalation destination or detailed remediation procedure for each reported AGV or system error.
* The source does not establish whether production stopping is required for any condition in this read-only diagnostic.

## Source Lineage

- Candidate IDs: candidate_training_video_get_agv_statuses_diagnostic
- Source ID: `training_video_day2`
- Source Type: `training_video`
