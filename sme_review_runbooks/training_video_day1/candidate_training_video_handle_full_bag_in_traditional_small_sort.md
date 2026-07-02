# Handle a Full Bag in a Traditional Small Sort System

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_handle_a_full_bag_in_a_traditional_small_sort_system_v1` |
| Title | Handle a Full Bag in a Traditional Small Sort System |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Operator flow for a traditional small sort system when a destination bag becomes full: close the destination, print and apply a label, zip the bag, place it on the takeaway belt, and reopen the chute or destination for continued parcel flow.

## When To Use

Use when operating a traditional small sort system and a destination or chute bag becomes full and must be processed using the manual bagging sequence described in the source.

## Do Not Use For

* Do not use for OptiSweep AGV/tipper bag-out workflows.
* Do not use as a troubleshooting procedure for label printer failures, chute reopening failures, or other exceptions not covered by the source.
* Do not use for belted ACB or Fortna automated consolidated bagging flows shown only for comparison in the source.

## Safety And Operational Notes

* The source characterizes the traditional process as operator-intensive, slow, physically strenuous, and inefficient.
* No source-supported lockout, guarding, ergonomic control, or production-stop instructions are provided in this packet.

## Access Or Tools Needed

* Assigned destination or chute in a traditional small sort system
* Bag at the destination
* Label printer
* Takeaway belt

## Related Operational Context

* ctx_training_video_traditional_small_sort_bagging_reference_v1

## Procedure Steps

### Step 1 — Monitor the assigned destination or chute

**Responsible role:** operator

**Instruction:**
Monitor the assigned destination or chute in the traditional small sort system until the bag becomes full.

**Expected result:**
The operator identifies a full bag at the assigned destination or chute.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*Traditional small sort comparison slide showing operators assigned about 20-25 destinations and the manual full-bag handling sequence.*


**Stop or Escalate If:**

* Bag fullness cannot be determined from the available operating cues.
* The documented sequence cannot be started because the operating condition does not match the source-described traditional flow.

---

### Step 2 — Close the destination

**Responsible role:** operator

**Instruction:**
Close the destination when the bag is full.

**Expected result:**
The destination is closed before the full bag is handled further.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*Text on the traditional small sort slide stating that when a bag is full the operator closes the destination.*


**Stop or Escalate If:**

* The destination cannot be closed.
* The documented sequence cannot be completed as described in the source.

---

### Step 3 — Print the bag label

**Responsible role:** operator

**Instruction:**
Print the bag label as described in the source.

**Expected result:**
A bag label is printed for the full bag.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*Traditional flow text indicating the operator prints and applies a label after closing the destination.*


**Stop or Escalate If:**

* The label does not print.
* The label printing step cannot be completed using the documented operating flow.

---

### Step 4 — Apply the printed label to the bag

**Responsible role:** operator

**Instruction:**
Apply the printed label to the bag.

**Expected result:**
The printed label is attached to the full bag.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*Traditional flow text indicating the operator prints and applies a label.*


**Stop or Escalate If:**

* The printed label is missing or unusable.
* The bag cannot be labeled as described in the source.

---

### Step 5 — Zip up the bag

**Responsible role:** operator

**Instruction:**
Zip up the bag.

**Expected result:**
The full bag is zipped.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*Traditional flow text indicating the operator zips the bag after labeling.*


**Stop or Escalate If:**

* The bag cannot be zipped.
* The sequence cannot continue safely or as documented.

---

### Step 6 — Place the bag on the takeaway belt

**Responsible role:** operator

**Instruction:**
Place the bag on the takeaway belt.

**Expected result:**
The full, labeled, zipped bag is placed on the takeaway belt.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*Traditional flow text indicating the operator places the bag on a takeaway belt.*


**Stop or Escalate If:**

* The takeaway belt is unavailable or the bag cannot be placed on it.
* The documented sequence cannot be completed.

---

### Step 7 — Reopen the chute or destination

**Responsible role:** operator

**Instruction:**
Reopen the chute or destination so additional parcels can continue to fall into a new bag.

**Expected result:**
The chute or destination is reopened for continued parcel flow.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*Traditional flow text indicating the operator reopens the chute after placing the bag on the takeaway belt.*


**Stop or Escalate If:**

* The chute or destination cannot be reopened.
* The operating sequence cannot be restored to continued parcel flow.

---

## Success Criteria

* The full bag is closed, labeled, zipped, and placed on the takeaway belt.
* The chute or destination is reopened for continued parcel flow.
* The documented manual sequence is completed in the order described by the source.

## Failure Conditions

* The label does not print.
* The destination cannot be closed.
* The bag cannot be labeled or zipped.
* The bag cannot be placed on the takeaway belt.
* The chute or destination cannot be reopened.
* Any condition requiring troubleshooting beyond the linear operating flow described in the source.

## Escalation Guidance

* Escalate if the documented sequence cannot be completed because the source only describes the operating flow.
* Escalate if the label does not print because the source does not provide troubleshooting steps.
* Escalate if the destination or chute cannot be reopened because the source does not provide troubleshooting or recovery guidance.

## Missing Details / Known Gaps

* The source does not define the exact method or control used to close the destination.
* The source does not define the exact method used to print the bag label.
* The source does not define label placement requirements on the bag.
* The source does not define how a new bag is installed after the full bag is removed.
* The source does not provide troubleshooting, recovery, or exception-handling steps for print failures or reopening failures.
* The source does not provide time estimates, staffing variations, or explicit safety controls beyond describing the process as physically strenuous.

## Source Lineage

- Candidate IDs: candidate_training_video_handle_full_bag_in_traditional_small_sort
- Source ID: `training_video_day1`
- Source Type: `training_video`
