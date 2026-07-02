# Interpret Map Monitor Message Panel Robot And AGV Status Items

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_map_monitor_message_panel_robot_and_agv_status_items_v1` |
| Title | Interpret Map Monitor Message Panel Robot And AGV Status Items |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Map Monitor message panel on the right side of the interface to identify the robot count and AGV fault-related items shown in the training slide.

## When To Use

Use when reviewing the Map Monitor interface to identify the message panel items documented in the training source, including robot counts, AGV fault-related items, disconnected AGV count, fault detail inspection area, locate faulted AGV item, and the E-stop-related item.

## Do Not Use For

* Do not use for corrective action, fault recovery, or control actuation because the source only supports identifying displayed items.
* Do not use to infer meanings, actions, or corrective steps beyond the items explicitly shown in the source.

## Safety And Operational Notes

* The source references an 'E stop the system' item, but this runbook only covers identifying its presence.
* No safe actuation procedure for the E-stop-related item is provided in this packet.

## Access Or Tools Needed

* Access to the Map Monitor interface
* Visual access to the message panel on the right side
* Training slide or screenshot showing the documented panel items

## Related Operational Context

* ctx_training_video_map_monitor_message_panel_v1
* ctx_training_video_robot_count_metrics_v1
* ctx_training_video_agv_fault_panel_items_v1
* ctx_training_video_estop_system_control_reference_v1

## Procedure Steps

### Step 1 — Locate the Map Monitor message panel

**Responsible role:** operator

**Instruction:**
Locate the Map Monitor message panel on the right side of the interface.

**Expected result:**
The right-side message panel is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The Map Monitor message panel on the right side of the interface.*


**Stop or Escalate If:**

* Escalate if the Map Monitor message panel is not visible.
* Escalate if the displayed panel cannot be matched to the documented interface.

---

### Step 2 — Identify robot count items

**Responsible role:** operator

**Instruction:**
Identify the displayed robot count items labeled 'Count of active Robots' and 'Count of Robots charging.'

**Expected result:**
Both robot count labels are identified in the panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The robot count items labeled 'Count of active Robots' and 'Count of Robots charging.'*


**Stop or Escalate If:**

* Escalate if the documented robot count items cannot be matched to the interface.

---

### Step 3 — Check for AGV faults drop-down

**Responsible role:** operator

**Instruction:**
Check whether the panel includes a drop-down to show AGV faults.

**Expected result:**
The AGV faults drop-down item is identified if present.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The item described as a drop-down to show AGV faults.*


**Stop or Escalate If:**

* Escalate if the documented AGV faults item cannot be matched to the interface.

---

### Step 4 — Identify disconnected AGV count

**Responsible role:** operator

**Instruction:**
Identify the displayed 'Count of AGVs disconnected' item.

**Expected result:**
The disconnected AGV count item is identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The item labeled 'Count of AGVs disconnected.'*


**Stop or Escalate If:**

* Escalate if the disconnected AGV count item cannot be matched to the interface.

---

### Step 5 — Inspect fault detail reference area

**Responsible role:** operator

**Instruction:**
Inspect the panel for the area or control described as inspection to view details of fault.

**Expected result:**
The fault detail inspection area or control is identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The area or control described as inspection to view details of fault.*


**Stop or Escalate If:**

* Escalate if the fault detail inspection area cannot be matched to the interface.

---

### Step 6 — Identify locate faulted AGV item

**Responsible role:** operator

**Instruction:**
Identify the control or item labeled 'Locate Faulted AGV.'

**Expected result:**
The locate faulted AGV item is identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The control or item labeled 'Locate Faulted AGV.'*


**Stop or Escalate If:**

* Escalate if the locate faulted AGV item cannot be matched to the interface.

---

### Step 7 — Note E-stop system item if visible

**Responsible role:** operator

**Instruction:**
Note that the panel also references 'E stop the system,' and record that this item is present if visible.

**Expected result:**
The E-stop-related item is noted as present if visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The item referenced as 'E stop the system.'*


**Stop or Escalate If:**

* Do not actuate the E-stop-related item based on this runbook.
* Escalate if clarification is needed on the function or safe use of the E-stop-related item.

---

## Success Criteria

* The user can identify the Map Monitor message panel on the right side of the interface.
* The user can identify the documented robot count items.
* The user can identify the documented AGV fault-related items, disconnected AGV count, fault detail inspection reference, locate faulted AGV item, and E-stop-related item if visible.

## Failure Conditions

* The Map Monitor message panel is not visible.
* The documented items cannot be matched to the interface.
* The user attempts to infer meanings, actions, or corrective steps beyond the source.

## Escalation Guidance

* Escalate if the Map Monitor message panel is not visible or the documented items cannot be matched to the interface.
* Escalate if clarification is needed because the source does not provide corrective actions or operating procedures for these items.

## Missing Details / Known Gaps

* The source does not provide corrective actions for any identified panel item.
* The source does not provide commands, thresholds, or operating limits for the displayed counts.
* The source does not provide a safe actuation procedure for the E-stop-related item.
* The source does not define role boundaries beyond operator-level identification of the displayed items.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_map_monitor_message_panel_status_items
- Source ID: `training_video_day1`
- Source Type: `training_video`
