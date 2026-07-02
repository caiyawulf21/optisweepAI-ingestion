# Start The Tip Cycle And Complete Post-Tip Bag Handling

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_start_the_tip_cycle_and_complete_post_tip_bag_handling_v1` |
| Title | Start The Tip Cycle And Complete Post-Tip Bag Handling |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Operator procedure for starting a tip cycle after an AGV has staged at the tipper, then completing the source-described post-tip bag handling: respond to the bag label prompt, label the bag, place it on the takeaway, and hang the next empty bag.

## When To Use

Use when an AGV has reached the tip location and the system has indicated the AGV is staged for a tip at the tipper, and the operator needs to start the tip and complete the associated bag handling sequence.

## Do Not Use For

* Do not use if the AGV has not staged for a tip at the tipper.
* Do not use to perform unsupported recovery, fault handling, or additional operator actions not described by the source.
* Do not use as a detailed HMI or control-name reference; the source does not provide exact control or screen names.

## Safety And Operational Notes

* Use only the operator actions explicitly described by the source.
* Do not add unsupported actions, timing logic, or recovery steps beyond button press, observation, label handling, takeaway placement, and next-bag setup.

## Access Or Tools Needed

* Operator access to the tipper station
* Start-tip button or operator control
* Bag label
* Bag takeaway access
* Replacement empty bag

## Related Operational Context

* ctx_training_video_tip_staging_and_opc_notification_v1
* ctx_training_video_operator_role_in_tip_cycle_v1

## Procedure Steps

### Step 1 — Confirm AGV is staged for tip

**Responsible role:** operator

**Instruction:**
Wait for the AGV to reach the tip location and for the system to indicate that the AGV has staged for a tip at the tipper.

**Expected result:**
The AGV is at the tip location and staged for tip.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Slide/frame content describing a full tote on an AGV being moved to the tipper, staged for tip, and reported to the tipper controller via OPC.*


**Stop or Escalate If:**

* AGV has not staged for a tip.

---

### Step 2 — Start the tip

**Responsible role:** operator

**Instruction:**
Use the operator control to push the button to start the tip.

**Expected result:**
The tip cycle starts after the operator button press.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Frame/slide text stating that the operator pushes a button to start the tip.*

![artifact_training_video_training_video_day1_0008_todd_s_the_tipper_expert_we_primary_00_10_34_000](assets/f05d964a25e93a10.jpg)

*Tipper station/operator station slide showing operator controls and ready-to-tip button context.*


**Stop or Escalate If:**

* The tipper does not perform the expected behavior after the start action.

---

### Step 3 — Observe clamp and tip sequence

**Responsible role:** operator

**Instruction:**
Observe that the tipper clamps the tote and performs the tip as described by the source.

**Expected result:**
The tipper clamps the tote and completes the tip motion.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Slide/frame text describing that the tipper clamps the tote and software monitors tip progress.*

![artifact_training_video_training_video_day1_0008_todd_s_the_tipper_expert_we_primary_00_10_34_000](assets/f05d964a25e93a10.jpg)

*Tipper station slide showing clamp and tipping arm operation.*


**Stop or Escalate If:**

* Tipper does not clamp the tote.
* Tipper does not perform the expected tip behavior after the start action.

---

### Step 4 — Watch for bag label prompt

**Responsible role:** operator

**Instruction:**
Watch for the source-described chat message prompt to print a bag label if the tip cycle has started.

**Expected result:**
A chat message prompt to print a bag label is observed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Slide/frame text stating that software monitors tip progress and sends a chat message to prompt bag label printing.*


**Stop or Escalate If:**

* The source-described bag label prompt is not observed when expected.

---

### Step 5 — Apply the bag label

**Responsible role:** operator

**Instruction:**
After the empty tote is returned to the AGV, apply the bag label to the bag.

**Expected result:**
The bag is labeled.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Slide/frame text describing empty tote return to the AGV and operator bag labeling.*


**Stop or Escalate If:**

* The empty tote is not returned to the AGV as described.
* Bag label cannot be applied.

---

### Step 6 — Place the labeled bag on the takeaway

**Responsible role:** operator

**Instruction:**
Place the labeled bag on the takeaway.

**Expected result:**
The labeled bag is placed on the takeaway.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Slide/frame text stating that the operator places the bag on a takeaway.*


**Stop or Escalate If:**

* The labeled bag cannot be placed on the takeaway.

---

### Step 7 — Hang the next empty bag

**Responsible role:** operator

**Instruction:**
Hang the next empty bag for the next tip.

**Expected result:**
A replacement empty bag is hung and ready for the following tip.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Slide/frame text stating that the operator hangs the next empty bag.*


**Stop or Escalate If:**

* The next empty bag cannot be hung or prepared.

---

## Success Criteria

* The tip cycle is started after the AGV is staged at the tipper.
* The tipper clamps the tote and performs the tip as described by the source.
* The bag label prompt is observed.
* The bag is labeled after the empty tote is returned to the AGV.
* The labeled bag is placed on the takeaway.
* The next empty bag is hung for the following tip.

## Failure Conditions

* AGV does not stage for tip.
* Tip does not start after button press.
* Tipper does not clamp or tip as expected.
* Bag label prompt is not observed.
* Bag is not labeled.
* Labeled bag is not placed on the takeaway.
* Next empty bag is not hung.

## Escalation Guidance

* Stop and escalate if the AGV has not staged for a tip.
* Stop and escalate if the tipper does not perform the expected clamp and tip behavior after the start action.
* Do not add unsupported recovery or alternate operator actions beyond those described by the source.

## Missing Details / Known Gaps

* Exact button/control name is not provided by the source.
* Exact screen or chat interface name for the bag label prompt is not provided by the source.
* The source does not provide detailed fault recovery steps for missing label prompts or failed tip behavior within this procedure.
* The source does not provide a time estimate for completing the procedure.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_start_tip_and_complete_operator_bag_handling
- Source ID: `training_video_day1`
- Source Type: `training_video`
