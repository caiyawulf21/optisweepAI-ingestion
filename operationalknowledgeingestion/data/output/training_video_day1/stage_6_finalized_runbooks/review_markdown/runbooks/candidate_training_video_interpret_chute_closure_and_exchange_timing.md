# Interpret Chute Closure In Relation To Fullness And Exchange Timing

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_chute_closure_in_relation_to_fullness_and_exchange_timing_v1` |
| Title | Interpret Chute Closure In Relation To Fullness And Exchange Timing |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training source to interpret whether observed chute closure matches the documented behavior that chute closure occurs when the chute is full, and to compare that observation against the source discussion of exchange timing targets intended to complete exchanges before closure.

## When To Use

Use when reviewing or explaining an observed chute closure condition and determining whether it aligns with the source-described fullness-based closure behavior and exchange timing discussion.

## Do Not Use For

* Do not use as a corrective maintenance or control-adjustment procedure.
* Do not use to invent thresholds, control logic, or recovery actions beyond what the source explicitly states.
* Do not use when a root-cause diagnosis or corrective action is required but not supported by this source.

## Safety And Operational Notes

* This is an interpretation/reference procedure only.
* Do not invent control thresholds or corrective actions beyond the values explicitly stated in the source.

## Access Or Tools Needed

* Visibility into chute status
* Source-described exchange timing and chute closure reference

## Related Operational Context

* ctx_training_video_chute_closure_and_exchange_timing_v1

## Procedure Steps

### Step 1 — Observe chute closure and exchange pace

**Responsible role:** L1_support

**Instruction:**
Observe whether the chute is closed and note whether the operation appears to be keeping up with exchanges and tipping.

**Expected result:**
A clear observation is captured about chute status and whether exchanges and tipping appear to be keeping pace.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Look for the training discussion connecting chute closure with chute fullness and delayed exchanges.*


**Stop or Escalate If:**

* Escalate if the observed chute behavior cannot be clearly described well enough to compare with the source-described explanation.

---

### Step 2 — Interpret closure as fullness-based behavior

**Responsible role:** L1_support

**Instruction:**
Use the source description to interpret the closure: the chute gets closed when the chute is full, not only based on whether both AGVs are in the station.

**Expected result:**
The observed closure is interpreted using the source-described fullness-based explanation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Look for the statement that the chute gets closed when the chute is full.*

![artifact_training_video_training_video_day1_0014_oh_so_parcel_was_sort_down_primary_00_23_58_000](assets/fa4202ba8c63f0d4.jpg)

*Look for the tote fullness thresholds and the note that when a tote is full, the chute is unavailable.*


**Stop or Escalate If:**

* Escalate if the observed chute behavior cannot be reconciled with the source-described fullness-based closure explanation.

---

### Step 3 — Compare observation to exchange timing targets

**Responsible role:** L1_support

**Instruction:**
Compare the observed situation to the source timing discussion that exchanges are staged before 80% fullness, with a goal of median 8 second exchange time and a floor of 6.7 seconds.

**Expected result:**
The observation is compared against the source timing targets and staging discussion.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Look for the timing discussion stating exchange occurs before 80% fullness, with a median 8 second goal and 6.7 second floor.*

![artifact_training_video_training_video_day1_0015_so_the_exchange_so_like_i_primary_00_27_50_500](assets/af90ff3e77701e85.jpg)

*Look for the exchange staging and chute timing behavior described in the training frame.*


**Stop or Escalate If:**

* Escalate if the observed timing or closure behavior cannot be compared to the source-stated values and staging discussion without making unsupported assumptions.

---

### Step 4 — Record whether the condition matches the source-described case

**Responsible role:** L1_support

**Instruction:**
Record whether the observed closure appears consistent with the source-described case where delayed exchanges or slow tipping allow the chute to fill and close.

**Expected result:**
A documented interpretation states whether the observed closure is consistent with the source-described behavior.

**Screens / Images:**

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Use this training slide/frame as the image support for chute-full and exchange timing context.*


**Stop or Escalate If:**

* Escalate if the observed chute behavior cannot be reconciled with the source-described fullness-based closure explanation.
* Stop and escalate if documenting the condition would require inventing control thresholds or corrective actions beyond the values explicitly stated in the source.

---

## Success Criteria

* The user can interpret chute closure as a fullness-related condition.
* The user can relate the observed condition to the documented exchange timing targets discussed in the source.
* The final interpretation remains limited to source-supported statements.

## Failure Conditions

* The observed chute behavior cannot be reconciled with the source-described fullness-based closure explanation.
* The interpretation requires unsupported assumptions about control logic or AGV station presence.
* The user attempts to derive corrective actions or thresholds not explicitly stated in the source.

## Escalation Guidance

* Escalate if the observed chute behavior cannot be reconciled with the source-described fullness-based closure explanation.
* Escalate if a root-cause diagnosis or corrective action is needed, because this source provides interpretation guidance rather than a full troubleshooting or corrective procedure.
* Do not invent control thresholds or corrective actions beyond the values explicitly stated in the source.

## Missing Details / Known Gaps

* The source does not provide a corrective procedure for resolving chute closure conditions.
* The source does not define explicit operator actions beyond observing and interpreting the condition.
* The source does not provide a formal escalation path, named owner, or downstream troubleshooting workflow.
* The source does not provide commands, system navigation steps, or exact HMI page instructions for this interpretation task.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_chute_closure_and_exchange_timing
- Source ID: `training_video_day1`
- Source Type: `training_video`
