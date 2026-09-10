# Shut Down OptiSweep System Through the WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_shut_down_optisweep_system_through_wcs_api_v1` |
| Title | Shut Down OptiSweep System Through the WCS API |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API client to confirm that the system is in the running state, execute POST System Shutdown, and verify that GET System State reports shutdown.

## When To Use

Use the OptiSweep / WCS API when an authorized L2 or L3 support user needs to shut down the OptiSweep system from its live running state and verify the resulting system state.

## Do Not Use For

* Do not use POST System Shutdown unless GET System State confirms that the system is running.
* Do not use this procedure as a physical emergency stop or a substitute for site safety actions.
* Do not use this procedure when the API request cannot be executed or returns an unrecognized result; escalate instead.

## Safety And Operational Notes

* Confirm the current system state before issuing the shutdown request.
* POST System Shutdown is described as shutting down the system when it is in a running state.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client
* GET System State
* POST System Shutdown

## Related Operational Context

* ctx_training_video_system_api_operations_v1
* ctx_training_video_system_state_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*OptiSweep API overview showing the System API list and Apidog on the primary server.*

![artifact_training_video_training_video_day2_0028_so_we_have_open_all_shoots_primary_02_40_50_000](assets/8d1ae8b858eadecf.jpg)

*System API list showing GET System State, POST System Startup, and POST System Shutdown, with the shutdown state behavior described.*

## Procedure Steps

### Step 1 — Open the System Shutdown request in the WCS API client

**Responsible role:** L2_support

**Instruction:**
Open the OptiSweep / WCS API in Apidog or an equivalent approved API client and locate POST System Shutdown in the System API list.

**Expected result:**
The POST System Shutdown request is available in the OptiSweep / WCS API client.

**Stop or Escalate If:**

* Escalate if the API request cannot be executed or POST System Shutdown is not available.

---

### Step 2 — Verify the current state through the WCS API

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client, execute GET System State and inspect the returned current system state. Continue only when the returned state is running.

**Expected result:**
GET System State returns the current system state as running.

**Stop or Escalate If:**

* Stop if GET System State does not report running.
* Escalate if GET System State cannot be executed or returns an unrecognized result.

---

### Step 3 — Execute System Shutdown and query state again

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client, execute POST System Shutdown. After the request completes, execute GET System State again.

**Expected result:**
The shutdown request completes and a subsequent GET System State response is available for verification.

**Stop or Escalate If:**

* Escalate if the API request cannot be executed or returns an unrecognized result.

---

### Step 4 — Confirm the shutdown state

**Responsible role:** L2_support

**Instruction:**
Inspect the state returned by the post-request GET System State call and compare it with the documented shutdown state.

**Expected result:**
The post-request GET System State response reports shutdown.

**Stop or Escalate If:**

* Stop and escalate if the system state does not change to shutdown after the shutdown request.
* Escalate if the returned state is unrecognized.

---

## Success Criteria

* GET System State reports running before the shutdown request.
* POST System Shutdown executes successfully.
* A subsequent GET System State reports shutdown.

## Failure Conditions

* The system is not in the running state before POST System Shutdown.
* The API request cannot be executed.
* The API returns an unrecognized result.
* The system state does not change to shutdown after the request.

## Escalation Guidance

* Stop and escalate when the pre-shutdown state is not running.
* Escalate when the API request cannot be executed or returns an unrecognized result.
* Stop and escalate when the post-request system state does not change to shutdown.

## Missing Details / Known Gaps

* The source does not define the detailed response schema or HTTP status expected from POST System Shutdown.
* The source does not specify the exact API base URL, authentication method, request headers, or request body.
* The source does not provide a timeout or polling interval for the post-shutdown GET System State check.
* The source does not define the approved operational authorization or site notification process before shutdown.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_shutdown_system_wcs_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
