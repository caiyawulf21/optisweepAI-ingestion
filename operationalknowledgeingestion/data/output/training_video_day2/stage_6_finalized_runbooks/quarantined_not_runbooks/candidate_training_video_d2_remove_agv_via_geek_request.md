# Remove a specified AGV via Geek request (RemoveAgv) using robot ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_a_specified_agv_via_geek_request_removeagv_robot_id_v1` |
| Title | Remove a specified AGV via Geek request (RemoveAgv) using robot ID |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Send the OptiSweep-to-Geek AGV API request function RemoveAgv with the required robot ID to remove the specified AGV from the system.

## When To Use

Use when you need to remove a specific AGV from the system by issuing the OptiSweep AGVs RemoveAgv request to Geek, and you have the required robot ID for that AGV.

## Do Not Use For

* Do not proceed without a robot ID (the source states RemoveAgv requires the robot ID).

## Access Or Tools Needed

* OptiSweep APIs (AGVs) RemoveAgv function
* Geek (Geek Plus) request capability
* Robot ID for the specified AGV
* API Dog (API client) on the primary servers (as described in the source)

## Related Operational Context

* ctx_training_video_agv_api_remove_recover_v1

## Visual References

![artifact_training_video_training_video_day2_0029_remove_agv_this_requires_the_robot_primary_02_42_03_000](assets/eb66b08e3471dd95.jpg)

*Frame showing: 'Remove AGV. This requires the robot ID and we'll send a request to Geek to remove the specified AGV from the system.'*

## Procedure Steps

### Step 1 — Identify the target AGV's robot ID

**Responsible role:** L2_support

**Instruction:**
Obtain the robot ID for the AGV you intend to remove. Ensure you have the correct robot ID before sending any RemoveAgv request.

**Expected result:**
You have a robot ID value for the specific AGV you want removed.

**Stop or Escalate If:**

* If you cannot provide a robot ID, do not proceed.

---

### Step 2 — Send the RemoveAgv request to Geek using the robot ID

**Responsible role:** L2_support

**Instruction:**
Using the OptiSweep APIs (AGVs) RemoveAgv function, send a request to Geek to remove the specified AGV, and include the required robot ID in the request.

**Expected result:**
A RemoveAgv request is issued to Geek for the specified robot ID.

---

### Step 3 — Confirm the RemoveAgv request was issued for the specified robot ID

**Responsible role:** L2_support

**Instruction:**
Verify that the RemoveAgv request you issued is associated with the same robot ID as the target AGV.

**Expected result:**
Evidence shows the RemoveAgv request tied to the specified robot ID was issued.

**Stop or Escalate If:**

* If the AGV does not appear to be removed after the request, escalate for deeper troubleshooting of the Geek request/response path.

---

## Success Criteria

* Geek receives the RemoveAgv request for the specified robot ID, resulting in the specified AGV being removed from the system.

## Failure Conditions

* Robot ID is missing (do not proceed).
* After the request, the AGV does not appear to be removed from the system.

## Escalation Guidance

* If the AGV does not appear to be removed after the request, escalate for deeper troubleshooting of the Geek request/response path.

## Missing Details / Known Gaps

* The source does not show the exact OptiSweep API invocation surface (e.g., specific endpoint name, request payload fields, or how to view the request/response) beyond stating the RemoveAgv function requires robot ID and sends a request to Geek.
* The source does not provide an explicit live verification method (which UI/API response field or status indicates the AGV was removed).

## Source Lineage

- Candidate IDs: candidate_training_video_d2_remove_agv_via_geek_request
- Source ID: `training_video_day2`
- Source Type: `training_video`
