# Recover a specified AGV via Geek request (RecoverAgv) using robot ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_specified_agv_via_geek_request_recoveragv_robotid_v1` |
| Title | Recover a specified AGV via Geek request (RecoverAgv) using robot ID |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Send the OptiSweep AGV API function RecoverAgv to Geek using the required robot ID so Geek adds the specified AGV back to the system (described as the same as Add AGV in Geek Plus).

## When To Use

Use when an AGV needs to be recovered by re-adding it in Geek, and you have the required robot ID to target the specific AGV.

## Do Not Use For

* Do not proceed if you cannot provide the robot ID (the source states RecoverAgv requires the robot ID).

## Access Or Tools Needed

* OptiSweep APIs (AGVs) RecoverAgv function
* Geek (Geek Plus) request capability
* Robot ID for the specified AGV

## Related Operational Context

* ctx_training_video_agv_api_remove_recover_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*Training frame listing AGV API functions and explicitly stating RecoverAGV requires the robot ID and sends a request to Geek to add the specified AGV to the system.*

## Procedure Steps

### Step 1 — Identify the target AGV's robot ID

**Responsible role:** L2_support

**Instruction:**
Obtain the robot ID for the specific AGV you intend to recover. Do not proceed without the robot ID.

**Expected result:**
You have a robot ID value for the specified AGV to use as the required input to RecoverAgv.

**Stop or Escalate If:**

* If you cannot provide a robot ID, do not proceed.

---

### Step 2 — Send the RecoverAgv request to Geek using the robot ID

**Responsible role:** L2_support

**Instruction:**
Use the OptiSweep AGV API function RecoverAgv and send the request to Geek with the required robot ID. The source describes Recover AGV as the same thing as Add AGV in Geek Plus.

**Expected result:**
A RecoverAgv request is issued to Geek for the specified robot ID (request is tied to that robot ID).

---

### Step 3 — Confirm the RecoverAgv request was issued for the specified robot ID

**Responsible role:** L2_support

**Instruction:**
Verify that the RecoverAgv request you issued is tied to the same robot ID as the target AGV.

**Expected result:**
The RecoverAgv request is confirmed as being for the specified robot ID.

**Stop or Escalate If:**

* If the AGV does not appear to be recovered after the request, escalate for deeper troubleshooting of the Geek request/response path.

---

## Success Criteria

* Geek receives the RecoverAgv request for the specified robot ID, resulting in the specified AGV being added back to the system.

## Failure Conditions

* No robot ID available (procedure must not be executed).
* RecoverAgv request is not tied to the intended robot ID.
* AGV does not appear to be recovered after the request.

## Escalation Guidance

* If the AGV does not appear to be recovered after the request, escalate for deeper troubleshooting of the Geek request/response path.

## Missing Details / Known Gaps

* The source does not show the exact OptiSweep API invocation surface (e.g., which UI/API client screen or exact request/response fields) for RecoverAgv.
* The source does not provide an explicit live verification method/field to confirm Geek processed the RecoverAgv request beyond the request being issued.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_recover_agv_via_geek_request
- Source ID: `training_video_day2`
- Source Type: `training_video`
