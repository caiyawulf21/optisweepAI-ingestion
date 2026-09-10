# Resend Geek Command from Get AGV Status using the command GUID (for unplanned restart / missed request recovery)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resend_geek_command_from_get_agv_status_command_guid_v1` |
| Title | Resend Geek Command from Get AGV Status using the command GUID (for unplanned restart / missed request recovery) |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Get AGV Status / APIs surface to resend a Geek Plus request via the “ResendGeekCommand” function by supplying the required command GUID. This is intended to recover when Geek Plus may have missed the original request after an unplanned restart.

## When To Use

Use when an unplanned restart occurred and Geek Plus may have missed the request, and you need to resend the Geek command using the required command GUID.

## Access Or Tools Needed

* Access to the Get AGV Status / APIs interface that includes “ResendGeekCommand”
* Access to “GET command status” to view the “main GUID”
* Command GUID from the “command database model”

## Related Operational Context

* ctx_training_video_resend_geek_command_reference_v1
* ctx_training_video_command_guid_in_get_command_status_v1

## Visual References

![artifact_training_video_training_video_day2_0030_get_agv_status_shows_the_current_primary_02_43_04_500](assets/30f5c770747ce298.jpg)

*Get AGV Status / APIs panel showing “ResendGeekCommand” and the note that Geek command requires a command GUID; also indicates main GUID visibility in GET command status.*

## Procedure Steps

### Step 1 — Locate “ResendGeekCommand” on the Get AGV Status / APIs area and identify where the command GUID is sourced/entered

**Responsible role:** L2_support

**Instruction:**
On the Get AGV Status / APIs area, find the “ResendGeekCommand” capability. Use the same surface to identify the required “command GUID” input requirement.

**Expected result:**
You can see the “ResendGeekCommand” capability and understand that it requires a command GUID from the command database model.

**Stop or Escalate If:**

* If “ResendGeekCommand” cannot be found on the Get AGV Status / APIs area, stop and escalate (no further recovery steps are provided in the source).

---

### Step 2 — Obtain the correct command GUID for the affected command (main GUID from Get Command Status)

**Responsible role:** L2_support

**Instruction:**
Use the Get Command Status view to obtain the “main GUID” for the affected command. The source states the main GUID is visible in GET command status.

**Expected result:**
You have the correct command GUID (main GUID) for the affected command that will be used for the resend.

**Stop or Escalate If:**

* If the correct command GUID cannot be identified from Get Command Status (main GUID), stop and escalate.

---

### Step 3 — Enter/provide the command GUID to the “ResendGeekCommand” function

**Responsible role:** L2_support

**Instruction:**
In the “ResendGeekCommand” function on the Get AGV Status / APIs area, enter/provide the command GUID you obtained (main GUID from Get Command Status).

**Expected result:**
The “ResendGeekCommand” function has the command GUID populated/provided as required.

**Stop or Escalate If:**

* Do not attempt to resend without the command GUID requirement being satisfied.

---

### Step 4 — Execute the resend so the request is resent to Geek Plus

**Responsible role:** L2_support

**Instruction:**
Execute the “ResendGeekCommand” resend action on the Get AGV Status / APIs area.

**Expected result:**
The resend action is performed (the request is resent to Geek Plus).

**Stop or Escalate If:**

* If the resend does not result in any observable change in command status, stop and escalate.

---

### Step 5 — Confirm resend outcome by re-checking Get Command Status / Get AGV Status

**Responsible role:** L2_support

**Instruction:**
Re-check the Get Command Status / Get AGV Status display for updated command status information after executing “ResendGeekCommand.”

**Expected result:**
Get Command Status / Get AGV Status reflects updated command status information consistent with the resend.

**Stop or Escalate If:**

* If the resend does not result in any observable change in command status, stop and escalate.

---

## Success Criteria

* The “ResendGeekCommand” resend is executed using a command GUID (main GUID from Get Command Status).
* After execution, Get Command Status / Get AGV Status shows updated command status information (observable change).

## Failure Conditions

* Correct command GUID cannot be identified from Get Command Status (main GUID).
* Resend does not result in any observable change in command status.

## Escalation Guidance

* If the correct command GUID cannot be identified from Get Command Status (main GUID) or if the resend does not result in any observable change in command status, stop and escalate. The source does not provide additional recovery steps beyond this resend approach.

## Missing Details / Known Gaps

* The source does not provide the exact UI/API field name or button label for executing “ResendGeekCommand” (only that it requires a command GUID and resends to Geek Plus).
* The source does not specify what exact command status fields/values should change after resend (only that command status should be re-checked for updated information).

## Source Lineage

- Candidate IDs: candidate_training_video_d2_resend_geek_command_using_command_guid
- Source ID: `training_video_day2`
- Source Type: `training_video`
