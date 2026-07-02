# Interpret Tote Fullness Thresholds And Pickup Priority From Volumetric Data

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_tote_fullness_thresholds_and_pickup_priority_from_volumetric_data_v1` |
| Title | Interpret Tote Fullness Thresholds And Pickup Priority From Volumetric Data |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the source-described tote fullness thresholds to interpret whether a tote is in a lower-priority pickup state, a higher-priority pickup state, or a full state that closes the chute. The source explains that software determines tote fullness from accumulated parcel dimension and weight data, with dimension scaling by package type such as boxes and bags.

## When To Use

Use when support or operations personnel need to interpret a tote's fullness status or relative pickup priority from the software-reported volumetric/fullness value using the threshold meanings described in the training source.

## Do Not Use For

* Do not use to set or change configured thresholds.
* Do not use to invent exact configured thresholds beyond the example values discussed in the source.
* Do not use as a tote dispatch, exchange, or AGV movement procedure.

## Safety And Operational Notes

* This is a reference procedure for interpretation of software-reported tote fullness states.
* When a tote is at the full threshold, the source states the chute is closed and the destination is marked unavailable so no more packages are diverted there during exchange.

## Access Or Tools Needed

* Access to the software view or data showing tote fullness or volumetric status
* Documented threshold meanings from the training source

## Related Operational Context

* ctx_training_video_tote_fullness_volumetric_thresholds_v1
* ctx_training_video_chute_close_on_full_v1

## Procedure Steps

### Step 1 — Identify the tote to interpret

**Responsible role:** L1_support

**Instruction:**
Identify the tote whose fullness needs to be interpreted in the available software or data view.

**Expected result:**
A specific tote is selected or identified for review.

**Stop or Escalate If:**

* Stop or escalate if the tote cannot be identified in the available software or data view.

---

### Step 2 — Review the software-calculated fullness value

**Responsible role:** L1_support

**Instruction:**
Check the tote fullness or volumetric value calculated by software from accumulated parcel dimension data. Note that the source says package type scaling differs for boxes and bags.

**Expected result:**
A current fullness or volumetric value is available for interpretation, with awareness that package type affects scaling.

**Screens / Images:**

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Look for the slide content stating that software updates tote cube or fullness using dimension and weight data, with scaling based on package type such as boxes and bags.*


**Stop or Escalate If:**

* Stop or escalate if no tote fullness or volumetric value is available.
* Stop or escalate if observed fullness behavior does not align with the source-described threshold meanings.

---

### Step 3 — Compare the value to the threshold bands

**Responsible role:** L1_support

**Instruction:**
Compare the observed fullness to the source-described threshold bands: over about 60% indicates pretty full and pickup should occur, over about 70% indicates higher pickup priority than lower percentages, and about 80% indicates full.

**Expected result:**
The tote is classified as pretty full, higher-priority for pickup, or full based on the source-described examples.

**Screens / Images:**

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Look for the slide and nearby transcript references to pretty full and full thresholds, and the retrieval text noting approximately 60%, 70%, and 80% fullness behavior.*


**Stop or Escalate If:**

* Stop or escalate if the observed fullness behavior does not align with the source-described threshold meanings.
* Stop or escalate if interpretation would require inventing exact configured thresholds beyond the example values discussed in the source.

---

### Step 4 — Verify chute-closed state when full

**Responsible role:** L1_support

**Instruction:**
If the tote is at the full threshold, verify whether the chute is already closed as described by the source.

**Expected result:**
A tote interpreted as full is also confirmed against the source-described chute-closed behavior.

**Screens / Images:**

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Look for the training slide or figure content showing pretty full versus full threshold behavior and the statement that when a tote is full the chute is unavailable or closed.*


**Stop or Escalate If:**

* Stop or escalate if the tote is at the full threshold but the chute is not closed or unavailable as described by the source.
* Stop or escalate if observed fullness behavior does not align with the source-described threshold meanings.

---

### Step 5 — Record the interpreted tote state

**Responsible role:** L1_support

**Instruction:**
Record the interpreted tote state and relative pickup priority using only the source-described threshold meanings.

**Expected result:**
The tote is documented as pretty full, higher-priority for pickup, or full with chute closed, based on the source.

**Stop or Escalate If:**

* Stop or escalate if the interpretation requires unsupported assumptions or invented exact thresholds.
* Stop or escalate if the observed fullness behavior does not align with the source-described threshold meanings.

---

## Success Criteria

* The tote can be classified using the source-described threshold meanings.
* The user can distinguish a pretty full state, a higher-priority pickup state, and a full state.
* If the tote is full, the interpretation includes the source-described chute-closed or unavailable condition.

## Failure Conditions

* The tote cannot be identified.
* No fullness or volumetric value is available for the tote.
* Observed fullness behavior does not align with the source-described threshold meanings.
* Interpretation would require inventing exact configured thresholds not supported by the source.
* A tote interpreted as full does not show the source-described chute-closed or unavailable behavior.

## Escalation Guidance

* Escalate if the observed fullness behavior does not align with the source-described threshold meanings.
* Escalate if a tote appears full but the chute is not closed or unavailable as described by the source.
* Escalate if interpretation depends on exact configured thresholds that are not provided in this source.

## Missing Details / Known Gaps

* The source does not identify a specific software screen name for viewing tote fullness.
* The source provides conversational example thresholds around 60%, 70%, and 80%, but does not establish site-specific configured values in this packet.
* The source does not define a formal recording location or documentation system for saving the interpreted tote state.
* The source does not provide exact operator role boundaries beyond the candidate's likely role.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_tote_fullness_thresholds_and_pickup_priority
- Source ID: `training_video_day1`
- Source Type: `training_video`
