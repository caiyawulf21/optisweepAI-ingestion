# Resend an AGV Command to Geek+ Using the OptiSweep WCS API

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resend_an_agv_command_to_geek_using_the_optisweep_wcs_api_v1` |
| Title | Resend an AGV Command to Geek+ Using the OptiSweep WCS API |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `wcs_api`, `apidog`, `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `unplanned_restart` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep / WCS API through Apidog to resubmit a Geek+ AGV request when the command GUID is available, then review GET command status for the associated main GUID. This is useful after an unplanned restart when Geek+ may have missed the request.

## When To Use

Use when an AGV command request may have been missed by Geek+ after an unplanned restart and a command GUID is available from the command database model or command status data.

## Do Not Use For

* Do not use when the required command GUID is unavailable.
* Do not use as a physical AGV recovery or E-stop procedure.
* Do not treat execution of the resend request as confirmation that Geek+ completed the command; the packet does not provide completion confirmation.

## Safety And Operational Notes

* Confirm that a command GUID is present before submitting the resend request.
* Stop and escalate rather than attempting the resend when the command GUID is unavailable.

## Access Or Tools Needed

* OptiSweep / WCS API
* Apidog / WCS API client on the primary server
* WCS / Helix DB (SSMS) for command database model or command status data
* Resend Geek Command request
* GET command status

## Related Operational Context

* ctx_training_video_resend_geek_command_v1

## Visual References

![artifact_training_video_training_video_day2_0027_apis_up_db_suite_provides_apis_primary_02_39_55_500](assets/adfdc59640e17900.jpg)

*Apidog / WCS API overview showing AGV API requests, including GET Get Agv Statuses and POST Resend Geek Command.*

![artifact_training_video_training_video_day2_0030_get_agv_status_shows_the_current_primary_02_43_04_500](assets/30f5c770747ce298.jpg)

*AGV API view showing Get AGV Statuses fields and the Resend Geek Command request requiring a command GUID.*

## Procedure Steps

### Step 1 — Open the Resend Geek Command request in Apidog

**Responsible role:** L2_support

**Instruction:**
On the primary server, open Apidog / WCS API client and select the AGV request labeled "Resend Geek Command". Confirm that the related GET Get Agv Statuses request is available for status review.

**Expected result:**
The Apidog AGV request list displays POST Resend Geek Command and GET Get Agv Statuses.

**Stop or Escalate If:**

* Escalate if Apidog or the OptiSweep / WCS API cannot be accessed.
* Escalate if the Resend Geek Command request is not available.

---

### Step 2 — Obtain and verify the command GUID

**Responsible role:** L2_support

**Instruction:**
Review the command database model or AGV command status data in the WCS / Helix DB (SSMS) or the OptiSweep / WCS API. Locate the command GUID associated with the command. Confirm that the command GUID is present before continuing.

**Expected result:**
A command GUID is present for the AGV command selected for resend.

**Stop or Escalate If:**

* Stop and escalate if the required command GUID is unavailable.
* Escalate if the command data cannot identify the command GUID.

---

### Step 3 — Submit Resend Geek Command

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client, enter the verified command GUID into the "Resend Geek Command" request and execute the request. Do not submit the request if the command GUID is missing.

**Expected result:**
The Resend Geek Command request executes with the required command GUID and resends the request to Geek+.

**Stop or Escalate If:**

* Do not proceed if the command GUID is missing.
* Escalate if the resend request cannot be executed.

---

### Step 4 — Review GET command status and main GUID

**Responsible role:** L2_support

**Instruction:**
Open or review GET command status in the OptiSweep / WCS API client and inspect the returned command status information for the associated main GUID.

**Expected result:**
GET command status exposes the associated main GUID for the command.

**Stop or Escalate If:**

* Escalate if GET command status does not expose the expected main GUID.
* Escalate if command status cannot be retrieved after the resend request.

---

## Success Criteria

* A command GUID is available before the resend request is submitted.
* The Resend Geek Command request executes in the OptiSweep / WCS API client.
* The request is sent to Geek+.
* GET command status exposes the associated main GUID.

## Failure Conditions

* The command GUID is unavailable.
* Apidog or the OptiSweep / WCS API cannot be accessed.
* The Resend Geek Command request cannot be executed.
* GET command status does not expose the expected main GUID.

## Escalation Guidance

* Escalate when the required command GUID is unavailable.
* Escalate when the resend request cannot be executed.
* Escalate when GET command status does not expose the expected main GUID.
* The packet does not define an HTTP response interpretation, request body, or confirmation that Geek+ completed the command; obtain SME guidance for those conditions.

## Missing Details / Known Gaps

* The source does not provide the request body or exact parameter name and format used to submit the command GUID.
* The source does not provide an HTTP response code or response schema for a successful or failed resend.
* The source does not define how to confirm that Geek+ completed the resent command beyond the presence of the main GUID in GET command status.
* The source does not provide an exact SSMS query or database object path for locating the command GUID.
* The source does not specify whether production motion must be stopped before resending a command.

## Source Lineage

- Candidate IDs: candidate_training_video_resend_geek_command
- Source ID: `training_video_day2`
- Source Type: `training_video`
