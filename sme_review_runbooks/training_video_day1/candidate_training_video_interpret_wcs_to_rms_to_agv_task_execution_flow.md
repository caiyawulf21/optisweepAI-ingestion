# Interpret Robot Task Execution Flow From WCS Through RMS To AGV

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_robot_task_execution_flow_from_wcs_through_rms_to_agv_v1` |
| Title | Interpret Robot Task Execution Flow From WCS Through RMS To AGV |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training-video-described control flow to explain how a robot movement task originates in WCS, is queued in RMS, and is executed by RMS through commands sent to the AGV.

## When To Use

Use when explaining or interpreting the high-level task execution path described in the training source for robot movement requests, including where tasks originate, where they queue, and how AGVs receive execution commands.

## Do Not Use For

* Do not use for UI navigation, queue-name lookup, or command-format details, because the source does not provide them.
* Do not use to infer system interfaces, queue internals, or lower-level execution behavior not explicitly stated in the source.
* Do not use as a recovery or control procedure for changing live system behavior.

## Safety And Operational Notes

* This is an interpretation/reference procedure, not an operational control workflow.
* Do not infer queue details, command formats, or system interfaces not stated in the source.

## Access Or Tools Needed

* Description of the robot task or movement request
* Source-backed WCS, RMS, and AGV task flow explanation

## Related Operational Context

* ctx_training_video_wcs_to_rms_task_queue_v1
* ctx_training_video_agv_rms_system_overview_v1

## Procedure Steps

### Step 1 — Identify the movement task being discussed

**Responsible role:** L1_support

**Instruction:**
Identify the robot movement request or task being discussed, such as moving from one location to another.

**Expected result:**
A specific movement task or request is defined for explanation.

**Stop or Escalate If:**

* The reported behavior or question cannot be tied to a specific movement request described at a high level.

---

### Step 2 — Associate task origin with WCS

**Responsible role:** L1_support

**Instruction:**
Associate the task origin with the office software described in the source as WCS.

**Expected result:**
The task is understood to originate from WCS according to the source.

**Stop or Escalate If:**

* The behavior being analyzed cannot be explained by WCS assigning the task at a high level.

---

### Step 3 — Note that tasks queue in RMS

**Responsible role:** L1_support

**Instruction:**
Note that the source states the assigned tasks go into a queue that lives in RMS.

**Expected result:**
The task is understood to enter an RMS queue after assignment.

**Stop or Escalate If:**

* Additional queue details are needed beyond the source's high-level statement.
* Someone requests queue names, queue logic, or queue internals not provided by the source.

---

### Step 4 — Interpret RMS as the executor of queued tasks

**Responsible role:** L1_support

**Instruction:**
Interpret RMS as the component that executes queued tasks one by one by sending commands to the AGV.

**Expected result:**
RMS is understood as the system that executes queued tasks sequentially through AGV commands.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Look for statements that Geek+ RMS directly controls AGVs, handles movement, and determines routing from point A to point B.*


**Stop or Escalate If:**

* The reported behavior cannot be explained by RMS executing queued tasks sequentially.
* A deeper interface or command-level explanation is required but not present in the source.

---

### Step 5 — Explain that the AGV receives commands rather than holding the higher-level task sequence

**Responsible role:** L1_support

**Instruction:**
Use this flow to explain that the AGV does not hold the higher-level task sequence knowledge described in the source; it receives commands from RMS.

**Expected result:**
The user can explain that higher-level task sequencing resides with RMS, while the AGV receives execution commands.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Look for the slide and transcript content showing RMS as the robot management system that receives tasks, maintains the queue, determines routing, and sends commands to AGVs, while AGV hardware handles onboard sensing.*


**Stop or Escalate If:**

* A reported behavior cannot be explained by the source-described WCS-to-RMS-to-AGV flow because the segment provides only a high-level overview.
* Someone asks for onboard AGV logic, command formats, or interfaces not stated in the source.

---

## Success Criteria

* The user can explain that WCS assigns the task.
* The user can explain that the task is queued in RMS.
* The user can explain that RMS executes queued tasks one by one by sending commands to the AGV.
* The user can explain that the AGV receives commands rather than holding the higher-level task sequence described in the source.

## Failure Conditions

* The task origin, queue location, or execution role is attributed to the wrong component.
* The AGV is described as owning higher-level task sequencing without source support.
* Unsupported details are inferred about queue internals, command formats, or interfaces.
* The reported behavior requires more than the high-level overview provided by the source.

## Escalation Guidance

* Escalate if a reported behavior cannot be explained by the source-described WCS-to-RMS-to-AGV flow, because the segment provides only a high-level overview.
* Escalate when lower-level queue behavior, command formats, or system interface details are required.
* Escalate for SME review if the interpretation would affect troubleshooting or operational decisions beyond this source's scope.

## Missing Details / Known Gaps

* The source does not provide UI navigation steps.
* The source does not provide queue names or queue configuration details.
* The source does not provide command syntax, API details, or interface payloads for this flow.
* The source provides a high-level overview only, not a troubleshooting decision tree.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_wcs_to_rms_to_agv_task_execution_flow
- Source ID: `training_video_day1`
- Source Type: `training_video`
