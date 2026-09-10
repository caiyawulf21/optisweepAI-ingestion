# Verify how OptiSweep APIs connect to API Dog and Ignition (from the documented API overview)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_optisweep_apis_connection_to_apidog_and_ignition_v1` |
| Title | Verify how OptiSweep APIs connect to API Dog and Ignition (from the documented API overview) |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | `L2_support` |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `apidog`, `ignition_gateway`, `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the source-backed mapping to explain which component uses the OptiSweep APIs: OptiSweep provides APIs for “get data” and “make requests,” API Dog is installed on the primary servers, and the same APIs feed Ignition.

## When To Use

Use this when you need a source-backed explanation of the data/request path between OptiSweep APIs, API Dog (on the primary servers), and Ignition, or when you are troubleshooting and need to determine whether observed behavior aligns with the documented mapping.

## Do Not Use For

* Do not use this as a step-by-step diagnostic procedure to validate live API endpoints, request parameters, or response payloads; the source segment provides only the architectural mapping statement and does not include concrete live checks.

## Access Or Tools Needed

* API Dog (primary servers) access (for explanation/verification, if available)
* Ignition access (for explanation/verification, if available)

## Related Operational Context

* ctx_training_video_optisweep_api_overview_v1
* ctx_training_video_apidog_primary_servers_v1
* ctx_training_video_ignition_api_feed_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Training video frame showing the mapping statement: OptiSweep APIs provide “get data” and “make requests,” API Dog is installed on the primary servers, and the same APIs feed Ignition.*

## Procedure Steps

### Step 1 — Identify the documented purpose of the OptiSweep APIs (get data / make requests)

**Responsible role:** L1_support

**Instruction:**
Use the source mapping statement to identify that the OptiSweep “up DB suite” provides APIs used to “get data” and to “make requests.”

**Expected result:**
You can state that the OptiSweep APIs are used for both retrieving data (“get data”) and sending requests (“make requests”).

---

### Step 2 — Confirm the documented tooling location: API Dog installed on the primary servers

**Responsible role:** L1_support

**Instruction:**
Use the source mapping statement to confirm that API Dog is installed on the primary servers.

**Expected result:**
You can state that API Dog is installed on the primary servers.

---

### Step 3 — Confirm the documented integration: the same APIs feed Ignition

**Responsible role:** L1_support

**Instruction:**
Use the source mapping statement to confirm that the same OptiSweep APIs feed Ignition.

**Expected result:**
You can state that the same APIs feed Ignition.

---

### Step 4 — Use the mapping to attribute observed behavior to API Dog (primary servers) and/or Ignition

**Responsible role:** L1_support

**Instruction:**
When live behavior does not match what you expect from the documented mapping, use the mapping (OptiSweep APIs → API Dog on primary servers; same APIs feed Ignition) to frame whether the observed behavior is associated with API Dog (primary servers) and/or Ignition as the consumer.

**Expected result:**
You can accurately describe whether the observed behavior is consistent with the documented path (API Dog on primary servers and Ignition consuming the same APIs).

**Stop or Escalate If:**

* If the live system behavior does not align with this documented mapping, escalate to deeper support procedures (the source segment does not provide further diagnostic steps).

---

## Success Criteria

* You can accurately describe the relationship between OptiSweep APIs, API Dog installed on the primary servers, and Ignition consuming the same APIs.

## Failure Conditions

* You cannot explain the documented mapping between OptiSweep APIs, API Dog (primary servers), and Ignition.
* Your explanation contradicts the documented mapping statement.

## Escalation Guidance

* If live system behavior does not align with the documented mapping, escalate to deeper support procedures; this source segment does not provide further diagnostic steps.

## Missing Details / Known Gaps

* The source segment provides an architectural mapping statement but does not include concrete live UI fields, request/response examples, or step-by-step checks to validate API Dog vs Ignition behavior on a running system.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_interpret_apidog_and_ignition_api_path
- Source ID: `training_video_day2`
- Source Type: `training_video`
