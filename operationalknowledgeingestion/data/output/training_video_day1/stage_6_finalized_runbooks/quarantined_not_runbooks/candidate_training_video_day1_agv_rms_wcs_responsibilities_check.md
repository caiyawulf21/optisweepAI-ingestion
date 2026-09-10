# Identify Responsibility Split Between AGV Onboard Sensors, Geek+ RMS, and WCS for Routing and Alarm Codes

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_responsibility_split_agv_rms_wcs_alarm_routing_v1` |
| Title | Identify Responsibility Split Between AGV Onboard Sensors, Geek+ RMS, and WCS for Routing and Alarm Codes |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this checklist to map the responsibility for obstacle sensing, alarm code generation/visibility, task queuing/execution, and routing decision across Geek+ AGV onboard hardware, Geek+ RMS, and WCS/office software—using only the responsibility split described in the provided training segment.

## When To Use

When you need to explain or confirm, for a given observed behavior, which component owns that responsibility in the Geek+ AGV / Geek+ RMS / WCS architecture described in the segment (obstacle sensing, alarm code visibility, task queuing/execution, and routing decision).

## Do Not Use For

* Do not use this procedure to perform live troubleshooting of specific faults (e.g., specific AGV fault codes, tipper faults, or queue states) because it does not provide system-specific diagnostic steps beyond mapping responsibilities.

## Access Or Tools Needed

* RMS screen visibility (as referenced in the segment)

## Related Operational Context

* ctx_training_video_agv_rms_system_overview_v1
* ctx_training_video_agv_vs_rms_responsibilities_v1
* ctx_training_video_rms_alarm_visibility_v1
* ctx_training_video_wcs_to_rms_task_queue_v1

## Procedure Steps

### Step 1 — Confirm the control architecture described in the segment (AGVs over QR codes; controlled by Geek+ RMS)

**Responsible role:** L1_support

**Instruction:**
State the segment’s architecture: the AGVs operate over QR codes and are controlled by the Geek+ RMS (Geek+ RMS is the robot management software that dictates what the robot needs to do).

**Expected result:**
You can clearly state that, in this architecture, Geek+ RMS is the robot management layer controlling AGV movement over QR-code operation.

**Stop or Escalate If:**

* If you cannot clearly state the segment’s control architecture ownership (AGV QR-code operation + Geek+ RMS control), stop and escalate for system-specific clarification beyond what this segment provides.

---

### Step 2 — For obstacle detection: identify that AGV onboard physical/collision sensors detect an obstacle and report the condition back to RMS

**Responsible role:** L1_support

**Instruction:**
State that obstacle detection is performed by the AGV onboard physical/collision sensors, which trigger when an obstacle is present and report the information back to RMS.

**Expected result:**
You can map “obstacle detected” behavior to AGV onboard sensors reporting back to RMS.

**Stop or Escalate If:**

* If you cannot map obstacle detection to AGV onboard sensors reporting to RMS, stop and escalate for system-specific clarification beyond what this segment provides.

---

### Step 3 — For alarm visibility: verify that RMS generates an alarm code visible on the RMS screen

**Responsible role:** L1_support

**Instruction:**
State that when the AGV reports an obstacle condition to RMS, RMS generates an alarm code that is visible to users on the RMS screen (including “UPS whoever’s looking at the RMS screen”).

**Expected result:**
You can map “alarm code shown on RMS screen” behavior to RMS generating the alarm code after receiving obstacle information from the AGV.

**Stop or Escalate If:**

* If you cannot map alarm visibility to RMS generating an alarm code visible on the RMS screen, stop and escalate for system-specific clarification beyond what this segment provides.

---

### Step 4 — For task assignment and queuing: identify that WCS assigns tasks and they queue in RMS

**Responsible role:** L1_support

**Instruction:**
State that WCS/office software assigns robot movement tasks (move from location to location, then to the next), and those tasks go into a queue that lives in RMS.

**Expected result:**
You can map “movement task assigned” to WCS assignment and “task queue exists” to RMS queue ownership.

**Stop or Escalate If:**

* If you cannot map task assignment to WCS and task queuing to RMS, stop and escalate for system-specific clarification beyond what this segment provides.

---

### Step 5 — For execution: confirm that RMS executes tasks 1 by 1 by sending commands to the AGV; AGV has no knowledge of the task queue

**Responsible role:** L1_support

**Instruction:**
State that RMS executes queued tasks 1 by 1 by sending commands to the AGV, and that the AGV does not have knowledge of the task queue.

**Expected result:**
You can map “sequential task execution” to RMS sending commands to the AGV, with AGV lacking queue knowledge.

**Stop or Escalate If:**

* If you cannot map task execution to RMS sending commands to the AGV (and AGV lacking queue knowledge), stop and escalate for system-specific clarification beyond what this segment provides.

---

### Step 6 — For routing: confirm that routing is decided by RMS (Geek+ determines the best route from point A to point B)

**Responsible role:** L1_support

**Instruction:**
State that routing is decided by RMS, and that Geek+ determines the best route to navigate from point A to point B.

**Expected result:**
You can map “route choice” behavior to RMS routing decision (Geek+ determines best route).

**Stop or Escalate If:**

* If you cannot map routing decision to RMS/Geek+ as described in the segment, stop and escalate for system-specific clarification beyond what this segment provides.

---

### Step 7 — Stop when you can clearly state the component owner for each responsibility (AGV sensors, RMS alarm codes/execution, WCS task assignment, RMS routing)

**Responsible role:** L1_support

**Instruction:**
Using only the segment’s described language, confirm you can map each observed behavior to its responsibility owner: obstacle sensing (AGV), alarm code generation/visibility (RMS), task queuing/execution (RMS), and routing decision (RMS), with task assignment originating from WCS.

**Expected result:**
You can produce a complete mapping statement that assigns each responsibility to exactly one owner as described in the segment.

**Stop or Escalate If:**

* If you cannot map a behavior to one of the described responsibility owners (AGV vs RMS vs WCS), stop and escalate for system-specific clarification beyond what this segment provides.

---

## Success Criteria

* You can map obstacle detection to AGV onboard sensors reporting to RMS.
* You can map alarm code visibility on the RMS screen to RMS generating the alarm code.
* You can map task assignment origin to WCS and task queuing/execution to RMS (queue lives in RMS; RMS executes tasks 1 by 1 by sending commands to the AGV).
* You can map routing decision to RMS/Geek+ (best route from point A to point B).

## Failure Conditions

* You cannot assign any of the responsibilities (obstacle sensing, alarm code generation/visibility, task queuing/execution, routing decision) to the correct component owner as described in the segment.

## Escalation Guidance

* If you cannot map a behavior to one of the described responsibility owners (AGV vs RMS vs WCS), stop and escalate for system-specific clarification beyond what this segment provides.

## Missing Details / Known Gaps

* This procedure is a responsibility-mapping reference and does not include live RMS/WCS/AGV UI steps, specific alarm-code formats, or how to verify queue/routing state in a live system beyond the segment’s described ownership.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_agv_rms_wcs_responsibilities_check
- Source ID: `training_video_day1`
- Source Type: `training_video`
