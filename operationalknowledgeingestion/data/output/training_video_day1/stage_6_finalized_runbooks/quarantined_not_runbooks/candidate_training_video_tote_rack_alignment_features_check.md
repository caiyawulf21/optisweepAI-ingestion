# Identify tote rack centering features (little feet and side fins) and their purpose

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_tote_rack_centering_features_v1` |
| Title | Identify tote rack centering features (little feet and side fins) and their purpose |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_exchange_sequence` |
| Access Surface | `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Visually identify the tote rack centering mechanisms in the OptiSweep tote-on-cylinder area: the tote sits on the cylinder, the rack’s “little feet” align the tote to the center when it drops, and the side “fins” help move packages toward the center after off-center impacts.

## When To Use

Use when you need to confirm (by visual inspection) that the tote rack hardware includes the centering features described for tote drops: tote-on-cylinder positioning, little feet for center alignment, and side fins for centering after off-center hits.

## Do Not Use For

* Do not use this procedure as a substitute for troubleshooting RMS/WCS/SSMS/API faults; this runbook is limited to visual identification of tote rack hardware features.

## Access Or Tools Needed

* Visual access to the tote rack/tote-on-cylinder hardware

## Related Operational Context

* ctx_training_video_tote_racking_overview_v1
* ctx_training_video_tote_rack_alignment_features_v1
* ctx_training_video_tote_rack_package_centering_fins_v1
* ctx_training_video_tote_rack_design_intent_v1

## Procedure Steps

### Step 1 — Locate the tote rack area described in the tote-on-cylinder hardware

**Responsible role:** operator

**Instruction:**
Visually locate the tote rack area where the tote sits on the cylinder (the tote-on-cylinder position).

**Expected result:**
You can point to the tote-on-cylinder area of the tote rack (the location where the tote sits on the cylinder).

**Stop or Escalate If:**

* If you cannot locate the tote-on-cylinder area, stop and escalate to training/support for clarification.

---

### Step 2 — Confirm the tote sits on the cylinder at the tote rack

**Responsible role:** operator

**Instruction:**
Confirm that the tote is positioned on the cylinder at the tote rack (tote-on-cylinder positioning).

**Expected result:**
The tote is visibly seated on the cylinder at the tote rack location.

**Stop or Escalate If:**

* If the tote rack area does not show the expected tote-on-cylinder seating condition, stop and escalate to training/support for clarification.

---

### Step 3 — Identify the tote rack “little feet” and their centering purpose

**Responsible role:** operator

**Instruction:**
Look for the “little feet” on the tote rack and confirm they are present on the rack hardware around the tote drop position.

**Expected result:**
You can point to the rack’s “little feet” feature.

**Stop or Escalate If:**

* If the tote rack does not appear to have the described little feet, stop and escalate to training/support for clarification.

---

### Step 4 — Identify the tote rack side “fins” and their off-center centering purpose

**Responsible role:** operator

**Instruction:**
Look for the side “fins” on the tote rack and confirm they are present on the rack hardware along the sides of the tote drop area.

**Expected result:**
You can point to the rack’s side fins feature.

**Stop or Escalate If:**

* If the tote rack does not appear to have the described side fins, stop and escalate to training/support for clarification.

---

### Step 5 — Note building-specific impact severity guidance (building vs Hazlett)

**Responsible role:** operator

**Instruction:**
If comparing sites/buildings, note the source guidance that in this building it “doesn’t matter as much” because the actual drop is more severe at Hazlett, where something needs to hit against to ensure centering and reduce items on the floor.

**Expected result:**
You can state the source’s site/building guidance: this building is less sensitive; Hazlett drop severity requires centering impact behavior to reduce items on the floor.

---

## Success Criteria

* You can identify and describe the tote rack centering mechanisms: tote sits on the cylinder; little feet align the tote to the center when it drops; side fins help move packages toward the center after off-center hits.

## Failure Conditions

* Tote rack does not appear to have the described little feet.
* Tote rack does not appear to have the described side fins.
* Tote-on-cylinder seating area cannot be confirmed.

## Escalation Guidance

* If the tote rack does not appear to have the described little feet or side fins, stop and escalate to training/support for clarification.

## Missing Details / Known Gaps

* The packet does not provide exact physical dimensions, locations, or naming conventions for the little feet and side fins beyond the visual feature descriptions.

## Source Lineage

- Candidate IDs: candidate_training_video_tote_rack_alignment_features_check
- Source ID: `training_video_day1`
- Source Type: `training_video`
