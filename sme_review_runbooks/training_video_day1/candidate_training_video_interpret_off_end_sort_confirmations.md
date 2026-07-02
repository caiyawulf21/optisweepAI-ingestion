# Interpret Off-End Sort Confirmations To Track Parcel Destination

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_off_end_sort_confirmations_to_track_parcel_destination_v1` |
| Title | Interpret Off-End Sort Confirmations To Track Parcel Destination |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use parcel sort confirmation information to determine which reported off-end destination an off-end parcel went to. The source states that parcels going off the end of the sorter can still be tracked through sort confirmations indicating one of two off-end destinations, until the parcel is sorted or rejected and removed from tables.

## When To Use

Use when a parcel did not sort to a chute and tote and instead went off the end of the sorter, and you need to determine the reported off-end destination from available sort confirmation information.

## Do Not Use For

* Do not use to invent or assume the exact two off-end destination names when they are not provided in the source.
* Do not use to define downstream handling beyond what the source states.
* Do not use when no sort confirmation is available for the parcel.

## Safety And Operational Notes

* This is a reference interpretation task based on system information; no physical intervention is supported by the source.
* Do not infer unsupported parcel handling actions or destination labels from incomplete source evidence.

## Access Or Tools Needed

* Access to sort confirmation information for the parcel

## Related Operational Context

* ctx_training_video_off_end_sort_confirmation_v1

## Procedure Steps

### Step 1 — Identify the off-end parcel

**Responsible role:** L1_support

**Instruction:**
Identify the parcel that did not sort to a chute and tote and instead went off the end of the sorter.

**Expected result:**
The parcel under review is confirmed as an off-end parcel.

**Stop or Escalate If:**

* The parcel cannot be confidently identified.
* There is no basis to conclude the parcel went off the end of the sorter.

---

### Step 2 — Check sort confirmation for off-end reporting

**Responsible role:** L1_support

**Instruction:**
Check the sort confirmation for that parcel to see whether an off-end destination is reported.

**Expected result:**
A sort confirmation is found and indicates whether an off-end destination is reported.

**Stop or Escalate If:**

* No sort confirmation is available for the off-end parcel.
* The sort confirmation does not show usable off-end destination information.

---

### Step 3 — Distinguish between the two reported off-end destinations

**Responsible role:** L1_support

**Instruction:**
Use the source-described sort confirmation information to distinguish between the two off-end destinations.

**Expected result:**
The reported off-end destination is distinguished using the sort confirmation information.

**Stop or Escalate If:**

* The sort confirmation does not clearly distinguish between the two off-end destinations.
* You would need to invent the exact destination names to proceed.

---

### Step 4 — Record the reported off-end destination

**Responsible role:** L1_support

**Instruction:**
Record the reported off-end destination and note that tracking continues through sort confirmations until the parcel is sorted or rejected and removed from tables.

**Expected result:**
The reported off-end destination is documented with the source-supported tracking limitation.

**Stop or Escalate If:**

* The reported destination is ambiguous.
* The parcel record is no longer available because it has been sorted or rejected and removed from tables.

---

## Success Criteria

* The user determines the reported off-end destination for the parcel from sort confirmation information.
* The user documents that tracking visibility is limited and continues only until the parcel is sorted or rejected and removed from tables.

## Failure Conditions

* No sort confirmation is available for the off-end parcel.
* The sort confirmation does not provide enough information to distinguish the off-end destination.
* The user would need to invent exact destination names or downstream handling not supported by the source.
* The parcel record is no longer available because it has been sorted or rejected and removed from tables.

## Escalation Guidance

* Escalate if no sort confirmation is available for the off-end parcel.
* Escalate if the sort confirmation does not clearly distinguish the off-end destination.
* Do not invent the exact destination names or downstream handling beyond what the source states.

## Missing Details / Known Gaps

* The source does not provide the exact names of the two off-end destinations.
* The source does not identify the exact interface or screen used to view the sort confirmations.
* The source does not provide a visual artifact specifically showing the off-end sort confirmation view.
* The source evidence is marked low confidence because the transcript is truncated.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_off_end_sort_confirmations
- Source ID: `training_video_day1`
- Source Type: `training_video`
