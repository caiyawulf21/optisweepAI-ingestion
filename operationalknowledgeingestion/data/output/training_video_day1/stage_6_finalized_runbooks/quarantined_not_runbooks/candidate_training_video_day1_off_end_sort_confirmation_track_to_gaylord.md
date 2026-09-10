# Track parcels that go off the end via sort confirmations (Gaylord destinations)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_track_parcels_off_end_sort_confirmations_gaylord_v1` |
| Title | Track parcels that go off the end via sort confirmations (Gaylord destinations) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state` |
| Access Surface | None |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When a parcel goes off the end of the sorter into a Gaylord at Hazleton, the system still generates sort confirmation messages that indicate two off-end destinations. Use those sort confirmations to track the parcel while it remains on the sorter, and rely on the system’s cleanup behavior once the parcel is sorted or rejected (removed from tables).

## When To Use

Use this when you need to track a parcel that has gone off the end of the sorter into a Gaylord at Hazleton, and you want to use the system’s off-end sort confirmations to follow it until it is sorted or rejected.

## Access Or Tools Needed

* Access to the live view/log where sort confirmations for off-end destinations are shown

## Related Operational Context

* ctx_training_video_off_end_sort_confirmation_v1

## Procedure Steps

### Step 1 — Identify the off-end condition (Gaylord at Hazleton)

**Responsible role:** L1_support

**Instruction:**
Using the live view/log you have for sort confirmations, confirm the parcel is in the off-end scenario described: it went off the end into a Gaylord at Hazleton.

**Expected result:**
You can associate the parcel with the off-end Gaylord-at-Hazleton scenario.

---

### Step 2 — Check for sort confirmation messages indicating two off-end destinations

**Responsible role:** L1_support

**Instruction:**
In the live view/log where sort confirmations are shown, locate the parcel’s sort confirmation entries for the off-end Gaylord-at-Hazleton scenario and confirm they indicate two off-end destinations.

**Expected result:**
Sort confirmation messages are present and show the parcel went off the end with two destinations (one of two off-end destinations).

**Stop or Escalate If:**

* Escalate if off-end sort confirmations are not present (source indicates tracking relies on those confirmations).

---

### Step 3 — Use the confirmations to track the parcel while it remains on the sorter

**Responsible role:** L1_support

**Instruction:**
Using the off-end sort confirmation entries you found, track the parcel’s off-end destination status while it remains on the sorter (the source describes this as “kind of somewhat track it”).

**Expected result:**
You can follow the parcel’s off-end destination information from the sort confirmations until it is sorted or rejected.

---

### Step 4 — Verify cleanup after the parcel is sorted or rejected (removed from tables)

**Responsible role:** L1_support

**Instruction:**
After the parcel is sorted or rejected, verify that the system removes the parcel from its tables (the source describes cleanup to keep the system clean).

**Expected result:**
The parcel is no longer present in the system tables used for tracking after it is sorted or rejected.

---

## Success Criteria

* Off-end sort confirmations exist for the parcel and indicate two off-end destinations for the Gaylord at Hazleton scenario.
* Using those confirmations, you can track the parcel while it remains on the sorter.
* After the parcel is sorted or rejected, the parcel is removed from the system tables used for tracking.

## Failure Conditions

* Off-end sort confirmations are missing for the parcel (tracking cannot be performed as described).
* Parcel remains in tables after it has been sorted or rejected (cleanup did not occur).

## Escalation Guidance

* Escalate if off-end sort confirmations are not present, since the source indicates tracking relies on those confirmations.

## Missing Details / Known Gaps

* The packet does not provide a concrete screenshot/frame or named live UI/log location specifically showing the off-end sort confirmation entries; Stage 6 cannot map the step to an exact RMS/SSMS/API Dog screen label beyond the generic “live view/log where sort confirmations are shown.”

## Source Lineage

- Candidate IDs: candidate_training_video_day1_off_end_sort_confirmation_track_to_gaylord
- Source ID: `training_video_day1`
- Source Type: `training_video`
