# Use Aveva AGV Command Functions For Remove Recover Pause All And Resume All

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_aveva_agv_command_functions_for_remove_recover_pause_all_and_resume_all_v1` |
| Title | Use Aveva AGV Command Functions For Remove Recover Pause All And Resume All |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

This source-specific runbook captures the training-video-supported process for accessing the Aveva-exposed AGV command set and selecting one of the documented AGV control functions: remove AGV, recover AGV, pause all AGVs, or resume all AGVs. The source confirms these commands are available in Aveva as selected Geek+ RMS features, but does not provide detailed execution guardrails, confirmations, or command-specific input rules beyond what is visible on the referenced training material.

## When To Use

Use when L2 support needs to access the Aveva interface/API area that exposes selected Geek+ RMS AGV commands and invoke one of the documented actions shown in the source: remove AGV, recover AGV, pause all AGVs, or resume all AGVs.

## Do Not Use For

* Do not use when the intended command behavior, required inputs, or safe-use conditions are unclear.
* Do not use as a detailed per-command operating procedure; this source does not provide command-specific confirmations, prerequisites, or safety constraints.
* Do not enter AGV-specific identifiers or other inputs unless those identifiers or inputs are explicitly supported by the interface shown in the source.

## Safety And Operational Notes

* These commands can affect AGV fleet behavior.
* The source does not provide detailed per-command safety constraints or guardrails.
* Escalate if intended command behavior, required inputs, or safe-use conditions are unclear.

## Access Or Tools Needed

* Access to the Aveva interface or API page with AGV commands

## Related Operational Context

* ctx_training_video_aveva_api_geekplus_rms_commands_v1
* ctx_training_video_agv_command_set_reference_v1

## Procedure Steps

### Step 1 — Open the Aveva AGV command area

**Responsible role:** L2_support

**Instruction:**
Open the Aveva interface or API area that includes the AGV command functions shown in the training material.

**Expected result:**
The AGV-related Aveva API page or interface area is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0068_we_ve_implemented_some_of_the_primary_02_20_13_500](assets/12c1d5bc87b51b02.jpg)

*AGVs Aveva API page showing the command area and listed AGV command names.*


**Stop or Escalate If:**

* Stop and escalate if the Aveva AGV command area is not available or cannot be identified from the interface.
* Stop and escalate if it is unclear whether the displayed page is the documented AGV command set.

---

### Step 2 — Locate the documented AGV command options

**Responsible role:** L2_support

**Instruction:**
Locate the documented command options in the Aveva command list: remove AGV, recover AGV, pause all AGVs, and resume all AGVs.

**Expected result:**
The listed command options are visible in the interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0068_we_ve_implemented_some_of_the_primary_02_20_13_500](assets/12c1d5bc87b51b02.jpg)

*The command names shown on the AGVs Aveva API training slide, specifically remove AGV, recover AGV, pause all AGVs, and resume all AGVs.*


**Stop or Escalate If:**

* Stop and escalate if the command names shown in Aveva do not match the documented source list.
* Stop and escalate if the interface presents additional required choices or controls not explained by the source.

---

### Step 3 — Select the needed AGV control action

**Responsible role:** L2_support

**Instruction:**
Select the specific AGV control action needed from the documented command list.

**Expected result:**
The intended command is selected in the Aveva interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0068_we_ve_implemented_some_of_the_primary_02_20_13_500](assets/12c1d5bc87b51b02.jpg)

*The AGV command list in the Aveva API training slide to confirm the selected action is one of the documented commands.*


**Stop or Escalate If:**

* Stop and escalate if it is unclear which documented command should be used.
* Stop and escalate if the intended action is not one of the commands explicitly named in the source.

---

### Step 4 — Use only interface-supported target inputs

**Responsible role:** L2_support

**Instruction:**
If the selected action requires an AGV-specific target, use only the identifiers or inputs explicitly supported by the interface as shown in the source.

**Expected result:**
Any required target input is limited to what the interface explicitly supports.

**Screens / Images:**

![artifact_training_video_training_video_day1_0068_we_ve_implemented_some_of_the_primary_02_20_13_500](assets/12c1d5bc87b51b02.jpg)

*Any visible AGV command fields or labels on the AGVs Aveva API page; do not infer additional input requirements beyond what is shown.*


**Stop or Escalate If:**

* Stop and escalate if required AGV-specific identifiers or input rules are not clearly shown.
* Stop and escalate if the interface requires values or formatting not documented in the source.

---

### Step 5 — Execute only within the documented command set

**Responsible role:** L2_support

**Instruction:**
Execute the selected command only within the limits of the documented Aveva-exposed command set.

**Expected result:**
The selected documented command is invoked from the Aveva interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0068_we_ve_implemented_some_of_the_primary_02_20_13_500](assets/12c1d5bc87b51b02.jpg)

*The AGVs Aveva API command area showing the documented command set before execution.*


**Stop or Escalate If:**

* Stop and escalate if the command behavior, required confirmations, or expected outcome is unclear.
* Stop and escalate if the interface presents undocumented controls or side effects.
* Stop and escalate if safe-use conditions are unclear.

---

## Success Criteria

* The user can access the Aveva-exposed AGV command set.
* The documented command options can be identified: remove AGV, recover AGV, pause all AGVs, and resume all AGVs.
* One documented AGV control action is selected and invoked using only source-supported interface information.

## Failure Conditions

* The Aveva AGV command area cannot be located or accessed.
* The documented command names are not visible or do not match the source.
* Required command inputs, confirmations, or safe-use conditions are unclear.
* Execution appears to require undocumented parameters or behavior not supported by the source.

## Escalation Guidance

* Escalate if the intended command behavior is unclear.
* Escalate if required inputs or identifiers are unclear.
* Escalate if safe-use conditions are unclear.
* Escalate if the interface behavior does not match the documented training material.

## Missing Details / Known Gaps

* The source does not provide detailed per-command execution steps for remove AGV, recover AGV, pause all AGVs, or resume all AGVs.
* The source does not define command-specific prerequisites, confirmations, or rollback actions.
* The source does not specify exact AGV identifier formats or required input fields for AGV-targeted commands.
* The source does not provide explicit success/failure feedback indicators after command execution.
* The source does not define whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_use_aveva_agv_command_set_for_basic_agv_control
- Source ID: `training_video_day1`
- Source Type: `training_video`
