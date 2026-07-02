# Perform a System Bag Out

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_a_system_bag_out_v1` |
| Title | Perform a System Bag Out |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the overall system bag out control to initiate a system-wide bag out that closes all destinations and exchanges totes or chutes that contain parcels. The source also states that any exchange already in process must finish.

## When To Use

Use when a system-wide bag out is needed and the intended behavior is to close all destinations and exchange totes or chutes that still contain parcels.

## Do Not Use For

* Do not use if the intended action is to stop an exchange that is already in process; the source states in-process exchanges must finish.
* Do not use when a leg-specific bag out is desired; the source notes bag out can also be chosen by leg of the sorter, which is a different option.
* Do not use as a cancel-bag-out action; the source distinguishes manual cancel bag out from system bag out.

## Safety And Operational Notes

* The source describes this as a user-selectable control action but does not provide additional safety controls or warnings.
* Do not assume an exchange already in process will stop; the source states it must finish.

## Access Or Tools Needed

* Access to the bag out control system
* Visibility to bag out status or exchange activity

## Related Operational Context

* ctx_training_video_system_bag_out_overview_v1
* ctx_training_video_cancel_bag_out_reference_v1

## Procedure Steps

### Step 1 — Access the overall system bag out control

**Responsible role:** operator

**Instruction:**
Open or navigate to the overall system control area and locate the bag out control for the system.

**Expected result:**
The overall system bag out control is visible and available for selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0054_all_right_so_i_ll_go_primary_02_08_20_500](assets/03b58ff4e823b6af.jpg)

*The overall system main overview screen with bag out listed among the right-hand side controls.*

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*The overall system bag out control slide describing the available bag out behavior.*


**Stop or Escalate If:**

* Escalate if the overall system bag out control is not visible or accessible.

---

### Step 2 — Select system bag out

**Responsible role:** operator

**Instruction:**
Select the system bag out option for the sorter from the overall system bag out control.

**Expected result:**
The system bag out action is initiated.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*The overall system bag out control content describing system bag out as a selectable option.*


**Stop or Escalate If:**

* Escalate if the system bag out option is unavailable.
* Escalate if the interface behavior does not match the documented system bag out description.

---

### Step 3 — Confirm all destinations close

**Responsible role:** operator

**Instruction:**
Confirm that the bag out action closes all destinations.

**Expected result:**
All destinations are closed as part of the system bag out.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*The slide text stating that system bag out will close all destinations.*


**Stop or Escalate If:**

* Escalate if all destinations do not close.
* Escalate if observed behavior does not match the documented system bag out description.

---

### Step 4 — Verify occupied totes or chutes are exchanged

**Responsible role:** operator

**Instruction:**
Verify that totes or chutes with parcels in them are exchanged as part of the bag out process.

**Expected result:**
Occupied totes or chutes containing parcels are exchanged.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*The slide text stating that system bag out exchanges chutes or totes with parcels in them.*


**Stop or Escalate If:**

* Escalate if occupied totes or chutes are not exchanged.
* Escalate if observed bag out behavior does not match the documented system bag out description.

---

### Step 5 — Observe in-process exchanges continue to completion

**Responsible role:** operator

**Instruction:**
Observe that any exchange already in process must finish and is not canceled by this action.

**Expected result:**
Any exchange already in process continues to completion.

**Screens / Images:**

![artifact_training_video_training_video_day1_0055_you_have_your_bag_out_control_primary_02_09_02_500](assets/de935058b7aa3faa.jpg)

*The bag out control slide text describing cancel bag out behavior and noting that an item already in exchange must finish.*


**Stop or Escalate If:**

* Escalate if an exchange already in process does not continue to completion.
* Do not expect an exchange already in process to stop; escalate if observed behavior differs.

---

## Success Criteria

* System bag out is initiated from the overall system bag out control.
* All destinations are closed.
* Totes or chutes containing parcels are exchanged.
* Any exchange already in process continues to completion.

## Failure Conditions

* The overall system bag out control cannot be accessed.
* The system bag out option cannot be selected.
* All destinations do not close.
* Occupied totes or chutes with parcels are not exchanged.
* Observed behavior does not match the documented system bag out description.
* An exchange already in process does not continue to completion.

## Escalation Guidance

* Escalate if observed bag out behavior does not match the documented system bag out description.
* Escalate if the overall system bag out control is unavailable or inaccessible.
* Escalate if destinations do not close or occupied totes/chutes are not exchanged.
* Escalate if an exchange already in process does not finish as described by the source.

## Missing Details / Known Gaps

* The source does not provide exact button names for the system bag out control.
* The source does not provide exact confirmation prompts or UI messages.
* The source does not provide a time estimate for completing the procedure.
* The source does not specify whether production must be stopped before initiating system bag out.
* The source does not specify any LOTO requirement.
* The source describes behavior but does not provide a detailed verification screen or status indicator list.

## Source Lineage

- Candidate IDs: candidate_training_video_initiate_system_bag_out
- Source ID: `training_video_day1`
- Source Type: `training_video`
