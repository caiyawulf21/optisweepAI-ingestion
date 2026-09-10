# Follow the operator tip-start and bag-label handling steps during a tip cycle

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_follow_operator_tip_start_and_bag_label_handling_during_tip_cycle_v1` |
| Title | Follow the operator tip-start and bag-label handling steps during a tip cycle |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

During a tip cycle, the operator starts the tip using the operator station button. Software monitors the tip process and sends a chat prompt to UPS to print a bag label if the cycle started. After the tip, the operator applies the bag label to the bag, places the labeled bag on the takeaway, and hangs the next empty bag for the next tip.

## When To Use

Use this when an AGV tote is staged at the tipper and you are performing the operator portion of the tip cycle: start the tip, handle the UPS bag-label prompt, label the resulting bag, place it on the takeaway, and prepare the next empty bag.

## Safety And Operational Notes

* Do not continue the cycle blindly if the bag label prompt does not occur or the label cannot be applied; stop and escalate as described in the failure notes.

## Access Or Tools Needed

* Operator access to the tip-start button
* Ability to observe/receive the chat prompt for UPS bag label printing (as described by the source)
* Bag label handling materials (bag label and bag)

## Related Operational Context

* ctx_training_video_operator_role_in_tip_cycle_v1

## Procedure Steps

### Step 1 — Start the tip using the operator station button when the tipper is ready

**Responsible role:** operator

**Instruction:**
When the AGV arrives and the tipper is ready for the tip cycle, push the operator button to start the tip.

**Expected result:**
The tip cycle is started by the operator (tipper begins the tip process).

**Stop or Escalate If:**

* If the bag label prompt does not occur or the label cannot be applied, stop and escalate rather than continuing the cycle blindly.

---

### Step 2 — Watch for the software-driven chat prompt to UPS for bag label printing

**Responsible role:** operator

**Instruction:**
During the tip, watch for the software-driven prompt: the source states software monitors the tip process and sends a chat message to prompt UPS to print a bag label if the cycle started.

**Expected result:**
A chat message prompt is sent to prompt UPS to print a bag label for the started cycle.

**Stop or Escalate If:**

* If the bag label prompt does not occur, stop and escalate rather than continuing the cycle blindly.

---

### Step 3 — Apply the bag label to the bag after the tip

**Responsible role:** operator

**Instruction:**
After the tip completes, apply the bag label to the bag.

**Expected result:**
The bag has the bag label applied.

**Stop or Escalate If:**

* If the bag label prompt does not occur or the label cannot be applied, stop and escalate rather than continuing the cycle blindly.

---

### Step 4 — Place the labeled bag on the takeaway

**Responsible role:** operator

**Instruction:**
Place the labeled bag on the takeaway.

**Expected result:**
The labeled bag is placed on the takeaway.

---

### Step 5 — Hang the next empty bag for the next tip

**Responsible role:** operator

**Instruction:**
Hang the next empty bag for the next tip.

**Expected result:**
The next empty bag is hung and ready for the next tip cycle.

---

## Success Criteria

* Tip cycle is started by the operator.
* UPS bag label prompt occurs via the software-driven chat message (as described).
* Bag label is applied to the resulting bag.
* Labeled bag is placed on the takeaway.
* Next empty bag is hung for the next tip.

## Failure Conditions

* Bag label prompt does not occur.
* Bag label cannot be applied to the bag.
* Labeled bag is not placed on the takeaway.
* Next empty bag is not prepared/hung.

## Escalation Guidance

* If the bag label prompt does not occur or the label cannot be applied, stop and escalate rather than continuing the cycle blindly.

## Missing Details / Known Gaps

* The source does not name the specific HMI screen/control label for the operator tip-start button; steps are kept at the source-described level (push the operator button to start the tip).
* The source does not specify the exact UI location/label for the chat prompt; it only states that software sends a chat message to prompt UPS to print a bag label.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_operator_start_tip_and_bag_label_chat_prompt
- Source ID: `training_video_day1`
- Source Type: `training_video`
