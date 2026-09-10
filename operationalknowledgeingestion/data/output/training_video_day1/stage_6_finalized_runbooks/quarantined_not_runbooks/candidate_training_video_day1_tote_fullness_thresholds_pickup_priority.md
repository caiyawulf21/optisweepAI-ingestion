# Determine tote pickup priority from volumetric thresholds (pretty full vs full)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_determine_tote_pickup_priority_from_volumetric_thresholds_v1` |
| Title | Determine tote pickup priority from volumetric thresholds (pretty full vs full) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_lifecycle_state` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `mapping_abnormal`, `sort_lifecycle_stuck` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use OptiSweep’s tote fullness logic (accumulated parcel dimensions scaled by package type) to determine tote pickup priority. The source describes two fullness thresholds: “pretty full” at ~60% and “full” at ~80%. Priority increases as fullness rises through the ~60/70/80 ranges, and at ~80% the chute is closed (highest priority).

## When To Use

When you need to explain or validate why a tote is being selected for pickup next based on fullness priority derived from volumetric thresholds (~60% pretty full, ~80% full) and the intermediate ~70% priority range.

## Do Not Use For

* Do not use this procedure as a corrective playbook for missing/incorrect dimension data; the source does not provide corrective steps for that condition.

## Access Or Tools Needed

* Access to the live display/log/metric that shows tote fullness/volumetrics (or the scaled dimension data used by software).

## Related Operational Context

* ctx_training_video_tote_fullness_volumetric_thresholds_v1

## Procedure Steps

### Step 1 — Locate the tote fullness basis used by software (scaled dimensions by package type)

**Responsible role:** L1_support

**Instruction:**
On the live system, identify the tote fullness metric/inputs that reflect accumulated parcel dimensions scaled by package type (the source describes that software updates tote fullness as parcel dimension data is scaled up/down based on configuration/package type).

**Expected result:**
You can state that tote fullness is determined by software using dimension data scaled by package type, and that tote fullness is updated as parcel dimension data is received and scaled.

**Stop or Escalate If:**

* If you cannot confirm the fullness metric basis is scaled dimension data by package type, stop and escalate for deeper investigation (the source does not provide corrective steps).

---

### Step 2 — Confirm package-type scaling examples (boxes vs bags) used in fullness computation

**Responsible role:** L1_support

**Instruction:**
When interpreting the fullness percentage, account for the source-described scaling examples: boxes are scaled higher (example ~120%) while bags are scaled lower (example ~70% or 60%).

**Expected result:**
You can explain that the fullness percentage is influenced by package-type scaling (e.g., boxes ~120% and bags ~70%/60% in the source examples).

**Stop or Escalate If:**

* If you cannot determine which package-type scaling applies to the tote’s contents, stop and escalate for deeper investigation (the source does not provide corrective steps).

---

### Step 3 — Check tote fullness against the two thresholds: pretty full (~60%) and full (~80%)

**Responsible role:** L1_support

**Instruction:**
Read the live tote fullness percentage/volumetrics and compare it to the source thresholds: pretty full at ~60% and full at ~80%.

**Expected result:**
You can categorize the tote fullness as: pretty full (~60%), intermediate (~70%), or full (~80%).

**Stop or Escalate If:**

* If the fullness metric is missing/undefined or you cannot compare it to ~60% and ~80%, stop and escalate for deeper investigation (the source does not provide corrective steps).

---

### Step 4 — Determine tote pickup priority from the fullness range (60/70/80) and chute closure at 80%

**Responsible role:** L1_support

**Instruction:**
Use the source priority guidance: (1) over 60% but under 70% = lowest priority; (2) over 70% but under 80% = next priority; (3) at 80% = highest priority because the chute is closed.

**Expected result:**
You can state the expected pickup priority for the tote based on where its fullness falls relative to ~60%, ~70%, and ~80%, including that ~80% corresponds to chute closure.

**Stop or Escalate If:**

* If the observed fullness does not align with the expected threshold behavior described by the source, stop and escalate for deeper investigation (the source does not provide corrective steps).

---

### Step 5 — If fullness is over the pretty-full threshold (~60%), expect an internal pick-up tote request

**Responsible role:** L1_support

**Instruction:**
For a tote whose fullness is over ~60% (pretty full), verify that the system behavior corresponds to the source-described internal pick-up tote request being sent.

**Expected result:**
You can describe that when volume metrics goes over 60%, the system marks it for pick up and sends a pick up tote request internally.

**Stop or Escalate If:**

* If observed behavior does not match the source-described threshold behavior, stop and escalate for deeper investigation (the source does not provide corrective steps).

---

## Success Criteria

* You can explain tote pickup priority using the source thresholds: pretty full ~60%, intermediate ~70%, full ~80%.
* You can state that at ~80% the chute is closed (highest priority) and that the chute closure behavior is part of the full-state logic.
* For a tote over ~60%, you can describe the expected internal pick-up tote request behavior described by the source.

## Failure Conditions

* Observed fullness/priority behavior does not align with the source-described threshold behavior.
* You cannot map the observed fullness metric to the source-described ~60% and ~80% thresholds.

## Escalation Guidance

* If observed fullness does not align with the expected threshold behavior described by the source, stop and escalate for deeper investigation. The source does not provide corrective steps.

## Missing Details / Known Gaps

* The source does not name the exact live UI fields/labels where tote fullness/volumetrics are displayed, so this runbook cannot specify where to read the fullness percentage on the live surface.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_tote_fullness_thresholds_pickup_priority
- Source ID: `training_video_day1`
- Source Type: `training_video`
