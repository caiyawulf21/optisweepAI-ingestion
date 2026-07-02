# Review AGV Fault And Disconnect Items In The Map Monitor Message Panel

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_agv_fault_and_disconnect_items_in_the_map_monitor_message_panel_v1` |
| Title | Review AGV Fault And Disconnect Items In The Map Monitor Message Panel |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Map Monitor message panel on the right side of the interface to review the AGV fault-related items shown in the training source: the AGV faults drop-down, the count of AGVs disconnected, the fault detail inspection area, and the Locate Faulted AGV item. This runbook is limited to identifying and recording what is visibly shown in the interface as documented by the source.

## When To Use

Use when reviewing the Map Monitor message panel to identify AGV fault-related controls and disconnect information exactly as shown in the training source.

## Do Not Use For

* Do not use for fault recovery or corrective action steps not stated in the source.
* Do not use to interpret fault meanings beyond the visible labels shown in the interface.
* Do not use to infer navigation behavior or system behavior not explicitly documented in this source.

## Safety And Operational Notes

* This runbook is diagnostic and limited to visual review of interface items shown in the source.
* Do not invent fault meanings, recovery actions, or navigation behavior not stated in the source.

## Access Or Tools Needed

* Access to the Map Monitor interface
* Visual access to the message panel
* Training slide or screenshot with AGV fault-related labels

## Related Operational Context

* ctx_training_video_map_monitor_message_panel_v1
* ctx_training_video_agv_fault_panel_items_v1

## Procedure Steps

### Step 1 — View the Map Monitor message panel

**Responsible role:** L1_support

**Instruction:**
Open or view the Map Monitor message panel on the right side of the interface.

**Expected result:**
The right-side message panel is visible for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The right-side Map Monitor message panel and its listed AGV fault-related items.*


**Stop or Escalate If:**

* Escalate if AGV fault-related items expected from the source are missing from the panel.

---

### Step 2 — Identify the AGV faults drop-down

**Responsible role:** L1_support

**Instruction:**
Identify the drop-down described as showing AGV faults.

**Expected result:**
The AGV faults drop-down is located in the message panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The item labeled as the drop down to show AGV faults.*


**Stop or Escalate If:**

* Escalate if AGV fault-related items expected from the source are missing from the panel.

---

### Step 3 — Check the disconnected AGV count

**Responsible role:** L1_support

**Instruction:**
Check the displayed 'Count of AGVs disconnected' item.

**Expected result:**
The disconnected AGV count item is visible in the message panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The item labeled count of AGVs disconnected.*


**Stop or Escalate If:**

* Escalate if AGV fault-related items expected from the source are missing from the panel.

---

### Step 4 — Inspect the fault detail area

**Responsible role:** L1_support

**Instruction:**
Inspect the panel for the area or control described as inspection to view details of fault.

**Expected result:**
The fault detail inspection area or control is identified in the panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The area described as inspection to view details of fault.*


**Stop or Escalate If:**

* Escalate if AGV fault-related items expected from the source are missing from the panel.

---

### Step 5 — Identify the Locate Faulted AGV item

**Responsible role:** L1_support

**Instruction:**
Identify the item labeled 'Locate Faulted AGV.'

**Expected result:**
The Locate Faulted AGV item is visible in the panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The item labeled Locate Faulted AGV.*


**Stop or Escalate If:**

* Escalate if AGV fault-related items expected from the source are missing from the panel.

---

### Step 6 — Record the visible AGV fault-related items

**Responsible role:** L1_support

**Instruction:**
Record the visible AGV fault-related items exactly as shown by the interface without adding undocumented interpretations.

**Expected result:**
A source-aligned record of the visible AGV fault-related items is created.

**Screens / Images:**

![artifact_training_video_training_video_day1_0025_ok_so_on_the_right_side_primary_00_57_51_000](assets/c0e2b74f80320155.jpg)

*The AGV fault-related labels to be recorded exactly as shown.*


**Stop or Escalate If:**

* Stop if the review requires interpreting fault meanings or recovery actions not stated in the source.
* Escalate if AGV fault-related items expected from the source are missing from the panel.

---

## Success Criteria

* The Map Monitor message panel on the right side of the interface is identified.
* The AGV faults drop-down is located.
* The count of AGVs disconnected item is located.
* The fault detail inspection area is located.
* The Locate Faulted AGV item is located.
* The visible AGV fault-related items are recorded exactly as shown without unsupported interpretation.

## Failure Conditions

* The expected AGV fault-related items are missing from the panel.
* The panel cannot be matched to the source-backed training view.
* The review requires unsupported interpretation of fault meanings or recovery behavior.

## Escalation Guidance

* Escalate if AGV fault-related items expected from the source are missing from the panel.
* Escalate for SME review if interpretation beyond visible labels is required.
* Do not invent fault meanings, recovery actions, or navigation behavior not stated in the source.

## Missing Details / Known Gaps

* The source does not provide fault resolution steps.
* The source does not define the exact interaction behavior of the AGV faults drop-down.
* The source does not define the exact behavior of the fault detail inspection area.
* The source does not define the exact behavior of the Locate Faulted AGV item.
* The source does not provide timing estimates, production stop requirements, or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_review_agv_fault_items_in_map_monitor_message_panel
- Source ID: `training_video_day1`
- Source Type: `training_video`
