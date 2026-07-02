# Process a Full Destination in a Belted ACB Solution

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_process_a_full_destination_in_a_belted_acb_solution_v1` |
| Title | Process a Full Destination in a Belted ACB Solution |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Process a full destination in the belted ACB flow by dropping the full destination bin onto the takeaway conveyor, allowing packages to move as a slug down the chute into the bag station, then labeling, zipping, and placing the completed bag on the takeaway belt.

## When To Use

Use when a destination is full in the belted ACB solution and the documented flow is to move the full destination bin onto the takeaway conveyor so packages can be conveyed as a slug into the bag station for bag handling.

## Do Not Use For

* Do not use for AGV/tipper OptiSweep bagging flows.
* Do not use for traditional small sort bagging flows where the operator closes the destination, prints and applies a label, zips the bag, places it on a takeaway belt, and reopens the chute at the sorter location.
* Do not use for fault recovery, jam recovery, or conveyor/bin-drop failures because the source does not provide those recovery steps.

## Safety And Operational Notes

* The source provides a high-level operating sequence only and does not provide detailed safety controls or recovery instructions.
* If the conveyor-to-bag-station flow cannot be completed, stop and escalate because no fault handling is provided in the source.

## Access Or Tools Needed

* Belted ACB destination bin
* Takeaway conveyor
* Chute
* Bag station
* Label
* Takeaway belt

## Related Operational Context

* ctx_training_video_belted_acb_solution_reference_v1

## Procedure Steps

### Step 1 — Identify the full destination in the belted ACB solution

**Responsible role:** operator

**Instruction:**
Identify that the destination is full in the belted ACB solution before starting the bag flow.

**Expected result:**
A full destination requiring the belted ACB bag flow has been identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*The belted ACB portion of the comparison slide showing that when a destination is full, the bin is dropped onto a takeaway conveyor and conveyed to a bag station.*


**Stop or Escalate If:**

* The condition does not match a full destination in the belted ACB solution.
* The operator cannot confirm the documented belted ACB flow from the available source evidence.

---

### Step 2 — Drop the full destination bin onto the takeaway conveyor

**Responsible role:** operator

**Instruction:**
Drop the full destination bin onto the takeaway conveyor as described by the source.

**Expected result:**
The full destination bin is transferred onto the takeaway conveyor.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*The belted ACB flow description indicating the full destination bin is dropped onto a takeaway conveyor.*


**Stop or Escalate If:**

* The bin does not drop onto the takeaway conveyor.
* The documented flow cannot continue and no recovery steps are provided by the source.

---

### Step 3 — Allow packages to convey as a slug into the bag station

**Responsible role:** operator

**Instruction:**
Allow the takeaway conveyor to convey the packages as a slug down the chute into the bag station.

**Expected result:**
Packages move as a slug down the chute and arrive at the bag station.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*The belted ACB description showing packages conveyed as a slug down a chute into a bag station.*


**Stop or Escalate If:**

* Packages do not convey correctly to the bag station.
* The conveyor-to-bag-station flow cannot be completed and the source provides no fault handling.

---

### Step 4 — Apply the label to the bag at the bag station

**Responsible role:** operator

**Instruction:**
At the bag station, apply the label to the bag.

**Expected result:**
The bag has the label applied.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*OCR text on the comparison slide describing bag handling actions including printing and applying a label.*


**Stop or Escalate If:**

* The bag cannot be labeled and the source provides no alternate handling.

---

### Step 5 — Zip the bag

**Responsible role:** operator

**Instruction:**
Zip up the bag.

**Expected result:**
The bag is zipped closed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*OCR text on the slide listing the bagging action to zip the bag.*


**Stop or Escalate If:**

* The bag cannot be zipped and the source provides no recovery guidance.

---

### Step 6 — Place the bag on the takeaway belt

**Responsible role:** operator

**Instruction:**
Place the bag on the takeaway belt.

**Expected result:**
The completed bag is placed on the takeaway belt.

**Screens / Images:**

![artifact_training_video_training_video_day1_0004_so_right_so_i_don_t_primary_00_04_19_500](assets/8b89cfd9f3ba9edc.jpg)

*OCR text on the slide listing placement of the bag on a takeaway belt.*


**Stop or Escalate If:**

* The bag cannot be placed on the takeaway belt.
* The documented flow cannot be completed and the source provides no fault handling.

---

## Success Criteria

* The full destination bin is dropped onto the takeaway conveyor.
* Packages are conveyed as a slug down the chute into the bag station.
* The bag is labeled.
* The bag is zipped.
* The bag is placed on the takeaway belt.

## Failure Conditions

* The bin does not drop onto the takeaway conveyor.
* Packages do not convey correctly to the bag station.
* The bag cannot be labeled, zipped, or placed on the takeaway belt.
* Any part of the conveyor-to-bag-station flow cannot be completed and the source provides no recovery steps.

## Escalation Guidance

* Escalate if the bin does not drop or packages do not convey correctly because the source does not provide recovery steps.
* Escalate if the documented conveyor-to-bag-station flow cannot be completed because no fault handling is provided in the source.

## Missing Details / Known Gaps

* The source does not provide detailed operator controls for how the bin is dropped onto the takeaway conveyor.
* The source does not provide explicit fault handling, jam recovery, or exception steps for conveyor or bag station issues.
* The source does not provide timing estimates.
* The source does not explicitly define supporting roles or escalation contacts.
* The source packet contains no commands, HMI navigation steps, or control panel instructions for this procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_process_full_destination_in_belted_acb
- Source ID: `training_video_day1`
- Source Type: `training_video`
