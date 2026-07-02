# Interpret Overall System Bag Out Control Options

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_overall_system_bag_out_control_options_v1` |
| Title | Interpret Overall System Bag Out Control Options |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the source slide content to interpret the documented meaning of the Overall System Bag Out Control options, including system bag out, bag out by sorter leg, cancel bag out for manual bag out, and pre bag out.

## When To Use

Use this reference when reviewing the Overall System Bag Out Control slide or equivalent documented source content and you need to understand what each listed bag out option means according to the training material.

## Do Not Use For

* Do not use this runbook as an execution procedure for performing bag out actions.
* Do not use this runbook to infer button paths, popup behavior, navigation steps, or system responses beyond the source-provided descriptions.
* Do not use this runbook if the available screen, popup, or control labels do not match the source terminology.

## Safety And Operational Notes

* Use only the source-provided descriptions when interpreting bag out options.
* Do not infer execution steps, button paths, or system responses beyond the source-provided descriptions.
* Escalate if the available screen, popup, or control labels do not match the source terminology.

## Access Or Tools Needed

* Access to the training slide or equivalent documented bag out control reference
* Ability to view the bag out control terminology used in the source

## Related Operational Context

* ctx_training_video_overall_system_bag_out_control_v1
* ctx_training_video_manual_bag_out_cancel_option_v1
* ctx_training_video_pre_bag_out_exchange_scope_v1

## Procedure Steps

### Step 1 — Locate Overall System Bag Out Control information

**Responsible role:** operator

**Instruction:**
Locate the "Overall System Bag Out Control" information in the source and review the slide or frame that contains the option descriptions.

**Expected result:**
The correct source slide or frame is visible for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0057_i_don_t_remember_everything_that_primary_02_09_56_000](assets/e89b88ff5a9b5dcb.jpg)

*Slide title 'Overall System Bag Out Control' and the bullet list describing the bag out options.*


**Stop or Escalate If:**

* The available screen, popup, or control labels do not match the source terminology.
* The referenced Overall System Bag Out Control content cannot be confirmed from the source.

---

### Step 2 — Interpret system bag out behavior

**Responsible role:** operator

**Instruction:**
Identify the documented "system bag out" behavior and note that it will close all destinations and exchange all totes with parcels in them.

**Expected result:**
The meaning of system bag out is recorded exactly as described in the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0057_i_don_t_remember_everything_that_primary_02_09_56_000](assets/e89b88ff5a9b5dcb.jpg)

*Bullet text describing that system bag out closes all destinations and exchanges all totes with parcels in them.*


**Stop or Escalate If:**

* The displayed description does not match the source wording for system bag out.
* Additional behavior must be assumed because the source description is insufficient for the intended use.

---

### Step 3 — Interpret bag out by sorter leg

**Responsible role:** operator

**Instruction:**
Identify the documented option to bag out by leg of the sorter and note that the source presents this as a user-selectable scope.

**Expected result:**
The meaning of bag out by sorter leg is recorded as a selectable scope described by the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0057_i_don_t_remember_everything_that_primary_02_09_56_000](assets/e89b88ff5a9b5dcb.jpg)

*Bullet text stating that a user could choose to bag out by leg of the sorter.*


**Stop or Escalate If:**

* The available control labels do not match the source terminology for bag out by leg of the sorter.
* Selection behavior or scope must be inferred beyond the source statement.

---

### Step 4 — Interpret cancel bag out for manual bag out

**Responsible role:** operator

**Instruction:**
Identify the documented "cancel bag out" behavior for manual bag out and note that it will cancel any exchange task that is not in process.

**Expected result:**
The meaning of cancel bag out is recorded exactly as described in the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0057_i_don_t_remember_everything_that_primary_02_09_56_000](assets/e89b88ff5a9b5dcb.jpg)

*Bullet text describing cancel bag out for manual bag out and its effect on exchange tasks not in process.*


**Stop or Escalate If:**

* The available terminology for manual bag out or cancel bag out does not match the source.
* The user needs behavior details beyond the source statement about exchange tasks not in process.

---

### Step 5 — Interpret pre bag out behavior

**Responsible role:** operator

**Instruction:**
Identify the documented "pre bag out" behavior and note that it exchanges the lowest 25% of destinations per leg of the sorter.

**Expected result:**
The meaning of pre bag out is recorded exactly as described in the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0057_i_don_t_remember_everything_that_primary_02_09_56_000](assets/e89b88ff5a9b5dcb.jpg)

*Bullet text stating that pre bag out exchanges the lowest 25% of destinations per leg of the sorter.*


**Stop or Escalate If:**

* The displayed pre bag out description does not match the source wording.
* Additional operational detail is required beyond the source statement.

---

### Step 6 — Record the option meaning using source wording

**Responsible role:** operator

**Instruction:**
Record the meaning of the bag out option being discussed using only the source-provided descriptions.

**Expected result:**
A source-grounded interpretation of the selected bag out option is documented.

**Screens / Images:**

![artifact_training_video_training_video_day1_0057_i_don_t_remember_everything_that_primary_02_09_56_000](assets/e89b88ff5a9b5dcb.jpg)

*All listed bag out option descriptions to ensure the recorded meaning stays aligned with the source.*


**Stop or Escalate If:**

* You must infer execution steps, button paths, or system responses beyond the source-provided descriptions.
* The available screen, popup, or control labels do not match the source terminology.

---

## Success Criteria

* The user can distinguish the documented effect of system bag out, bag out by sorter leg, cancel bag out, and pre bag out.
* All recorded meanings remain limited to the source-provided descriptions.

## Failure Conditions

* The available screen, popup, or control labels do not match the source terminology.
* The user attempts to infer execution steps, button paths, or system responses beyond the source-provided descriptions.
* The source content needed to interpret an option cannot be confirmed.

## Escalation Guidance

* Escalate if the available screen, popup, or control labels do not match the source terminology.
* Escalate if an operational decision requires execution steps, button paths, or system responses not provided by this source.
* Escalate for SME review if the source wording is insufficient for the intended operational use.

## Missing Details / Known Gaps

* The source provides descriptive behavior only and does not provide explicit execution steps.
* The source does not provide button names, navigation paths, or popup interaction steps for these bag out options.
* The source does not provide role boundaries beyond general operator-oriented training context.
* The source does not provide time estimates, production stop requirements, or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_overall_system_bag_out_control_options
- Source ID: `training_video_day1`
- Source Type: `training_video`
