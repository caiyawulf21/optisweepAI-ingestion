# Perform a Bag Out by Sorter Leg

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_a_bag_out_by_sorter_leg_v1` |
| Title | Perform a Bag Out by Sorter Leg |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the bag out control to apply bag out to a selected sorter leg instead of the full system. The source confirms that bag out can be chosen by leg of the sorter, but does not provide exact interface labels or detailed completion validation steps.

## When To Use

Use when bag out needs to be applied to a selected sorter leg and the bag out control supports leg-based selection.

## Do Not Use For

* Do not use as a documented procedure for full-system bag out; this source distinguishes bag out by sorter leg from overall system bag out.
* Do not use when exact interface labels, confirmation states, or completion criteria are required; the source does not provide those details.

## Safety And Operational Notes

* The source does not provide specific safety hazards, lockout/tagout requirements, or production stop requirements for this action.
* Do not assume additional controls, confirmations, or cancellation behavior beyond what is stated in the source.

## Access Or Tools Needed

* Access to the bag out control system
* Ability to identify sorter legs in the control interface

## Related Operational Context

* ctx_training_video_bag_out_by_sorter_leg_v1

## Procedure Steps

### Step 1 — Access the bag out control system

**Responsible role:** operator

**Instruction:**
Access the bag out control system and navigate to the bag out control options.

**Expected result:**
The bag out control options are visible to the user.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*Bag out control slide/frame showing bag out control behavior and related options.*


**Stop or Escalate If:**

* Escalate if the bag out control system cannot be accessed.

---

### Step 2 — Identify the bag out by leg option

**Responsible role:** operator

**Instruction:**
Identify the option indicating that bag out can be performed by leg of the sorter.

**Expected result:**
A leg-based bag out option is present in the control.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*Text or control area indicating that a user can choose to bag out by leg of the sorter.*


**Stop or Escalate If:**

* Escalate if the control does not allow leg selection when this option is expected from the source.

---

### Step 3 — Select the desired sorter leg

**Responsible role:** operator

**Instruction:**
Select the desired sorter leg for the bag out action.

**Expected result:**
The intended sorter leg is selected for bag out.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*Bag out control context associated with leg-based bag out selection.*


**Stop or Escalate If:**

* Escalate if the desired sorter leg cannot be selected.

---

### Step 4 — Start bag out for the selected leg

**Responsible role:** operator

**Instruction:**
Start the bag out for the selected sorter leg using the bag out control.

**Expected result:**
Bag out begins for the selected sorter leg.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*Bag out control context where the selected leg bag out would be initiated.*


**Stop or Escalate If:**

* Escalate if the selected leg bag out does not start.

---

### Step 5 — Observe bag out behavior for the selected leg

**Responsible role:** operator

**Instruction:**
Observe the bag out behavior for the selected leg using the system's displayed exchange activity or status if available.

**Expected result:**
The system shows bag out activity associated with the selected sorter leg rather than only a full-system action.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*Any displayed bag out or exchange-related status associated with bag out control behavior.*


**Stop or Escalate If:**

* Escalate if the control does not show leg-specific behavior when leg-based bag out was selected.
* Escalate if confirmation of completion is required; the source does not provide detailed validation steps for confirming completion by leg.

---

## Success Criteria

* The bag out control supports selection by sorter leg.
* The intended sorter leg is selected.
* Bag out is initiated for the selected leg rather than only as a full-system action.

## Failure Conditions

* The bag out control cannot be accessed.
* The control does not allow leg selection when this option is expected from the source.
* The desired sorter leg cannot be selected.
* The bag out action does not start for the selected leg.
* The source does not provide detailed validation steps for confirming completion by leg.

## Escalation Guidance

* Escalate if the control does not allow leg selection when this option is expected from the source.
* Escalate if the selected leg cannot be chosen or the bag out action does not start.
* Escalate when confirmation of completion by leg is required, because the source does not provide detailed validation steps.

## Missing Details / Known Gaps

* Exact interface labels for selecting bag out by sorter leg are not provided in the source.
* The source does not provide a detailed click path to open the bag out control.
* The source does not provide explicit confirmation indicators for successful completion of bag out by leg.
* The source does not provide timing expectations for the action.
* The source does not specify whether production must be stopped before performing this action.
* The source does not specify lockout/tagout requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_bag_out_by_sorter_leg
- Source ID: `training_video_day1`
- Source Type: `training_video`
