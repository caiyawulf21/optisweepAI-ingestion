# Resend Geek Command Using A Command GUID After Geek+ Communication Retry Stops

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resend_geek_command_using_a_command_guid_after_geek_communication_retry_stops_v1` |
| Title | Resend Geek Command Using A Command GUID After Geek+ Communication Retry Stops |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Aveva-exposed Resend Geek Command function to resend a command to Geek Plus after retries have stopped or after a Geek Plus restart or error, by specifying the command GUID.

## When To Use

Use when a command previously sent to Geek Plus needs to be resent after retries have stopped, or after a Geek Plus server restart or error, and the command GUID is known.

## Do Not Use For

* Do not use when the correct command GUID is not available.
* Do not use as a substitute for Execute AGV command; this procedure is specifically for resending a prior command by command GUID.
* Do not assume retry counts, confirmation indicators, or follow-up validation steps that are not provided by the source.

## Safety And Operational Notes

* This is described as a recovery-oriented system action and should be performed with awareness that it replays a prior command to Geek Plus.
* Do not invent or rely on unsupported success indicators, retry thresholds, or additional control steps not stated in the source.

## Access Or Tools Needed

* Access to the Aveva interface or API page with AGV commands
* The command GUID for the command to resend
* Awareness that the prior command encountered an error or retry exhaustion

## Related Operational Context

* ctx_training_video_resend_geek_command_reference_v1

## Procedure Steps

### Step 1 — Open the AGV command area in Aveva

**Responsible role:** L2_support

**Instruction:**
Open the Aveva interface or API area where AGV-related commands are available.

**Expected result:**
The AGV-related Aveva API page or equivalent command area is open.

**Screens / Images:**

![artifact_training_video_training_video_day1_0068_we_ve_implemented_some_of_the_primary_02_20_13_500](assets/12c1d5bc87b51b02.jpg)

*AGVs Aveva API page and the listed recovery functions that expose selected Geek+ RMS commands.*


**Stop or Escalate If:**

* Stop or escalate if the Aveva AGV command area is not accessible.
* Stop or escalate if the expected AGV recovery functions are not present.

---

### Step 2 — Locate Resend Geek Command

**Responsible role:** L2_support

**Instruction:**
Locate the recovery function named Resend Geek Command.

**Expected result:**
The Resend Geek Command function is identified and ready for input.

**Screens / Images:**

![artifact_training_video_training_video_day1_0068_we_ve_implemented_some_of_the_primary_02_20_13_500](assets/12c1d5bc87b51b02.jpg)

*The AGV recovery/API function list where Resend Geek Command is discussed alongside other recovery-oriented functions.*


**Stop or Escalate If:**

* Stop or escalate if Resend Geek Command is not available in the interface.

---

### Step 3 — Identify the command GUID to resend

**Responsible role:** L2_support

**Instruction:**
Identify the command GUID for the command that was previously sent to Geek Plus and needs to be resent.

**Expected result:**
A command GUID is available for entry into the resend function.

**Stop or Escalate If:**

* Stop or escalate if the correct command GUID is not available.

---

### Step 4 — Enter the command GUID

**Responsible role:** L2_support

**Instruction:**
Enter or specify the command GUID in the Resend Geek Command input.

**Expected result:**
The command GUID is populated in the Resend Geek Command input.

**Stop or Escalate If:**

* Stop or escalate if the command GUID cannot be entered or cannot be verified as the intended command.

---

### Step 5 — Execute the resend

**Responsible role:** L2_support

**Instruction:**
Execute the resend action so the command is sent again to Geek Plus.

**Expected result:**
The specified command is resent to Geek Plus using the provided command GUID.

**Stop or Escalate If:**

* Stop or escalate if resend does not succeed after Geek Plus is up.

---

## Success Criteria

* The Resend Geek Command function is accessed.
* The intended command GUID is specified.
* The command is resent to Geek Plus.

## Failure Conditions

* The AGV-related Aveva API page or recovery function is not accessible.
* Resend Geek Command cannot be located.
* The correct command GUID is not available.
* The resend does not succeed after Geek Plus is up.

## Escalation Guidance

* Escalate if the correct command GUID is not available.
* Escalate if resend does not succeed after Geek Plus is up.
* Escalate if the required recovery function is unavailable in the Aveva interface.

## Missing Details / Known Gaps

* The source does not provide exact UI navigation steps to reach the Resend Geek Command function.
* The source does not provide the exact field name or button label used to submit the resend.
* The source does not provide explicit confirmation messages or post-action validation steps.
* The source does not provide retry counts, timeout values, or additional troubleshooting logic if resend fails.

## Source Lineage

- Candidate IDs: candidate_training_video_resend_geek_command_after_retry_stops
- Source ID: `training_video_day1`
- Source Type: `training_video`
