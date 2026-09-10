# Check Current OptiSweep System State in the WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_current_optisweep_system_state_in_the_wcs_api_v1` |
| Title | Check Current OptiSweep System State in the WCS API |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog or an equivalent approved API client to retrieve and interpret the current system state before assessing lifecycle status.

## When To Use

Use this diagnostic when live OptiSweep lifecycle status is needed before interpreting system behavior or deciding whether the system is running or shut down. Perform the check on the OptiSweep / WCS API through Apidog or another approved API client.

## Do Not Use For

* Do not use this procedure to start up or shut down the system; those are separate API operations.
* Do not use this procedure to infer the meaning of a state that is not explicitly returned by the API.
* Do not use this procedure as a training-material orientation or architecture walkthrough.

## Safety And Operational Notes

* This procedure uses the GET System State diagnostic request and does not direct the user to execute state-changing API operations.
* Do not infer an unlisted state meaning from the returned response.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client
* GET System State

## Related Operational Context

* ctx_training_video_system_api_operations_v1
* ctx_training_video_system_state_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Apidog / WCS API System API list showing GET System State.*

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*System API list and live-state interpretation showing GET System State, including running and shutdown relationships.*

## Procedure Steps

### Step 1 — Locate GET System State in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
Open the OptiSweep / WCS API in Apidog or another approved API client and locate the GET System State request in the System API list.

**Expected result:**
The GET System State request is visible and available to execute in the OptiSweep / WCS API client.

**Stop or Escalate If:**

* Escalate to L3 support or the API/system owner if GET System State cannot be located or selected.

---

### Step 2 — Execute GET System State in the OptiSweep / WCS API

**Responsible role:** L2_support

**Instruction:**
Execute the GET System State request in Apidog or the approved OptiSweep / WCS API client and inspect the returned current system state.

**Expected result:**
The request returns the current live OptiSweep system state.

**Stop or Escalate If:**

* Escalate to L3 support or the API/system owner if the GET System State request cannot be executed.
* Escalate to L3 support or the API/system owner if the request does not return a current state.

---

### Step 3 — Interpret the returned system state

**Responsible role:** L2_support

**Instruction:**
Use the state explicitly returned by GET System State to determine whether the system is in a running state, a shutdown state, or another state explicitly returned by the OptiSweep / WCS API.

**Expected result:**
The returned response is classified as running, shutdown, or another explicitly returned state without inferring an unlisted meaning.

**Stop or Escalate If:**

* Escalate to L3 support or the API/system owner if the returned state is unavailable or its meaning is not explicitly defined by the response or supported reference.

---

## Success Criteria

* GET System State is available in the OptiSweep / WCS API client.
* The request returns the current live OptiSweep system state.
* The returned state is identified as running, shutdown, or another state explicitly returned by the API without unsupported inference.

## Failure Conditions

* GET System State cannot be located or executed.
* The API request does not return a current system state.
* The returned state is not explicitly interpretable from the available response or source-supported state meanings.

## Escalation Guidance

* Escalate to L3 support or the API/system owner if the System State request cannot be executed.
* Escalate to L3 support or the API/system owner if no current state is returned.
* Do not infer an unlisted state meaning.

## Missing Details / Known Gaps

* The source does not provide response-field names for GET System State.
* The source does not provide HTTP success criteria, response codes, or request URL details.
* The source names running and shutdown states but does not define the meanings of other possible returned states.
* The source does not provide a specific API endpoint address or authentication procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_check_system_state_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
