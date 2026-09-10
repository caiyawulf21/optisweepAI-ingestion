# Use API Dog to observe Ignition HMI API request/response behavior (fault stats, pause, recover, startup)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_api_dog_to_observe_ignition_hmi_request_response_behavior_v1` |
| Title | Use API Dog to observe Ignition HMI API request/response behavior (fault stats, pause, recover, startup) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness`, `gateway_health` |
| Access Surface | `apidog`, `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use API Dog on a primary server to verify that AVEVA/HMI actions are implemented as request/response calls through Ignition (used as an OPC server). Confirm that API Dog returns responses reflecting system state (e.g., startup returns a response indicating whether the system is in the running/shutdown state) and that data-oriented calls return payloads rather than downstream module-to-module tracing.

## When To Use

When you need to confirm that AVEVA/HMI interactions are correctly represented at the Ignition-hosted API layer as request/response behavior (GET-style data fetches and push-button/action-style requests like startup), and to interpret the returned response as system state (running/shutdown) rather than expecting internal module-to-module flow tracing.

## Do Not Use For

* Do not use this procedure to perform deep downstream module-to-module tracing for failures (the source states this level of stacking/flow tracing is not exposed at the HMI API request/response layer).

## Access Or Tools Needed

* API Dog
* Primary server access (APIs are locally hosted and installed on every primary server)
* API guide / API documentation referenced by the source

## Related Operational Context

* ctx_training_video_api_hosting_on_primary_servers_v1
* ctx_training_video_ignition_as_opc_bridge_for_aveva_v1
* ctx_training_video_hmi_api_request_response_model_v1

## Visual References

![artifact_training_video_training_video_day2_0033_a_purge_or_close_so_manual_primary_02_50_45_500](assets/a47b2c64a103b938.jpg)

*Frame showing Ignition has the APIs outlined in the API guide and that AVEVA sends a request which Ignition processes and returns responses (fault stats, pause, recover).*

## Procedure Steps

### Step 1 — Connect to a primary server where the Ignition-hosted APIs are locally hosted

**Responsible role:** L2_support

**Instruction:**
Jump onto a primary server. The source states the APIs are locally hosted and installed on every primary server, and that anyone can jump on the primary to get to all the APIs.

**Expected result:**
You are operating from a primary server environment where the locally hosted APIs are available for API Dog calls.

---

### Step 2 — Open API Dog and locate the shared API collection/documentation used for Ignition HMI APIs

**Responsible role:** L2_support

**Instruction:**
Open API Dog and locate the shared API collection/documentation referenced by the source. The source states they use API Dog rather than Postman and that there is API documentation in an API guide (Word document mentioned).

**Expected result:**
API Dog is open and you have access to the API guide/collection entries needed to call the Ignition-hosted APIs.

---

### Step 3 — Run an API Dog call for an HMI action (e.g., startup) to observe request/response behavior

**Responsible role:** L2_support

**Instruction:**
In API Dog, run an API call corresponding to an HMI action such as “startup”. The source states AVEVA hits a request tag; Ignition processes and returns responses.

**Expected result:**
API Dog returns a response message for the startup action.

**Stop or Escalate If:**

* If API Dog calls do not return responses or return unexpected errors, escalate to support (source indicates deeper module-to-module tracing is not available at this layer).

---

### Step 4 — Interpret the startup response as system state (running vs shutdown) rather than expecting internal flow tracing

**Responsible role:** L2_support

**Instruction:**
Read the API Dog response message from the startup call and determine whether it indicates the system is in the running state or not (and similarly for shutdown state). The source states there is no stacking/flow tracing at this level—only request/response.

**Expected result:**
You can map the response message to system state constraints (e.g., response indicates system is not in the running state when startup is clicked in the wrong state).

**Stop or Escalate If:**

* If the response does not reflect system state gating or is missing/unexpected, escalate to support (source: deeper module-to-module tracing is not exposed at this layer).

---

### Step 5 — For data-oriented calls, confirm you receive a response payload (not downstream module-to-module flow)

**Responsible role:** L2_support

**Instruction:**
Run a data-oriented API Dog call (the source describes these as mainly fetching data). Confirm that the call returns a response payload rather than a trace of downstream module-to-module flow.

**Expected result:**
API Dog returns a response payload for data-oriented calls.

**Stop or Escalate If:**

* If API Dog calls do not return responses or return unexpected errors, escalate to support (source: deeper module-to-module tracing is not available at this layer).

---

### Step 6 — If you suspect downstream failures (e.g., 55XX), note that this layer does not expose module-to-module stacking/flow tracing

**Responsible role:** L2_support

**Instruction:**
When interpreting API Dog results, remember the source claim: there is no stacking/flow tracing at this level. Even if a downstream module call fails with a 55XX error, the HMI API request/response layer only provides the response indicating state (or failure) rather than a trace of where it stopped.

**Expected result:**
You do not attempt to infer internal module call chains from the API Dog request/response layer; you treat the response as the observable signal.

**Stop or Escalate If:**

* If you need deeper downstream failure origin beyond request/response, escalate to support (source: deeper stacking/flow tracing is not exposed at the HMI API request/response layer).

---

## Success Criteria

* API Dog calls return request/response outputs for Ignition-hosted HMI APIs used by AVEVA.
* Startup action responses reflect system state gating (running vs shutdown) as described by the source.
* Data-oriented calls return response payloads (mainly fetching data) rather than downstream module-to-module flow traces.

## Failure Conditions

* API Dog calls do not return responses or return unexpected errors.
* Startup response does not indicate system state gating (running/shutdown) or is missing/unexpected.
* Attempting to diagnose downstream module call origin using only HMI API request/response outputs.

## Escalation Guidance

* If API Dog calls do not return responses or return unexpected errors, escalate to support. The source indicates deeper module-to-module stacking/flow tracing is not exposed at this HMI API request/response layer.

## Missing Details / Known Gaps

* The packet does not provide exact API endpoints, request parameter names, or the specific API Dog collection name.
* The packet does not provide the exact API Dog UI labels/fields to click for the startup call; steps are kept at the source-described request/response behavior level.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_api_dog_request_response_model_vhmiapi
- Source ID: `training_video_day2`
- Source Type: `training_video`
