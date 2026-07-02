# Interpret Shutdown-State AGV Replacement Behavior Through the Hospital

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_shutdown_state_agv_replacement_behavior_through_the_hospital_v1` |
| Title | Interpret Shutdown-State AGV Replacement Behavior Through the Hospital |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Reference runbook based on a training example describing expected AGV behavior during shutdown-state replacement handling. In the example, an AGV is removed without a tote and another AGV is added; the added AGV goes through the hospital first and then determines where an AGV is missing.

## When To Use

Use this runbook when reviewing or interpreting a shutdown-state scenario in which one AGV was removed without a tote and another AGV was added, and you need to compare observed behavior to the training example for expected routing through the hospital.

## Do Not Use For

* Do not use this as a complete procedure for removing or adding AGVs.
* Do not use this to infer broader AGV routing logic beyond the specific shutdown-state example described in the source.
* Do not use this for non-shutdown-state AGV behavior interpretation unless separately supported by source evidence.

## Safety And Operational Notes

* This is an interpretation/reference runbook, not a control procedure.
* The source warns by omission that it does not provide the actual add/remove AGV procedure; only the resulting behavior is described.
* Do not generalize the example into unsupported routing or control logic.

## Access Or Tools Needed

* Awareness that the system is in shutdown state
* Ability to observe AGV removal and added AGV movement
* Access to the training explanation of shutdown-state replacement behavior

## Related Operational Context

* ctx_training_video_shutdown_agv_rebalance_v1
* ctx_training_video_hospital_reject_and_home_base_v1

## Procedure Steps

### Step 1 — Confirm the scenario matches the training example

**Responsible role:** L1_support

**Instruction:**
Confirm that the observed scenario is a shutdown-state example in which an AGV was removed without a tote and another AGV was added.

**Expected result:**
The observed case matches the source example closely enough to use this reference.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Hospital area and modular flow context referenced by the training explanation for shutdown-state AGV handling.*


**Stop or Escalate If:**

* Stop if the system is not in shutdown state.
* Stop if the removed AGV was not removed without a tote.
* Stop if there was no added AGV to compare against the example.

---

### Step 2 — Verify the added AGV goes through the hospital first

**Responsible role:** L1_support

**Instruction:**
Observe the added AGV and verify that it goes through the hospital first rather than directly to another location.

**Expected result:**
The added AGV routes through the hospital first.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Hospital flow and entrance queue concepts supporting the expectation that the added AGV goes through the hospital first.*


**Stop or Escalate If:**

* Escalate if the shutdown-state replacement scenario is present but the added AGV does not go through the hospital first as described.

---

### Step 3 — Observe how the AGV determines where it is needed

**Responsible role:** L1_support

**Instruction:**
Observe whether the AGV then determines where an AGV is missing, described in the source as going to the shorter side.

**Expected result:**
After going through the hospital, the AGV determines where it is needed based on a missing AGV condition.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Overall modular flow context after hospital movement; use this only as visual support for the narrated example.*


**Stop or Escalate If:**

* Escalate if the AGV behavior after hospital routing conflicts with the documented example.

---

### Step 4 — Record the behavior as the documented training example

**Responsible role:** L1_support

**Instruction:**
Record that this hospital-first movement is the documented behavior for the shutdown-state replacement example.

**Expected result:**
The observation is documented as matching the training example.

**Stop or Escalate If:**

* Stop if documentation would require broader claims than the source supports.

---

### Step 5 — Escalate if observed behavior does not match the example

**Responsible role:** L1_support

**Instruction:**
If the added AGV does not follow the hospital-first path described in the source example, stop and escalate.

**Expected result:**
A mismatch is escalated rather than interpreted as normal behavior.

**Stop or Escalate If:**

* Escalate if the shutdown-state replacement scenario is present but the added AGV does not go through the hospital first as described.
* Escalate if the scenario appears similar but key conditions cannot be confirmed from observation.

---

## Success Criteria

* The observed shutdown-state replacement scenario matches the source example conditions.
* The added AGV is observed going through the hospital first.
* The added AGV is then observed determining where an AGV is missing, consistent with the source example.
* The behavior is documented as a source-specific training example without overgeneralization.

## Failure Conditions

* Observed scenario does not match the source example.
* Added AGV does not go through the hospital first.
* Observed behavior is generalized beyond what the source explicitly states.
* The source is treated as a full operational add/remove procedure when it is only a narrated example.

## Escalation Guidance

* Escalate when the shutdown-state replacement scenario is present but the added AGV does not go through the hospital first as described.
* Escalate when key scenario conditions cannot be confirmed from observation.
* Escalate to SME review if broader routing interpretation is needed beyond the narrated example.

## Missing Details / Known Gaps

* The source does not provide the actual operational steps for removing an AGV or adding an AGV.
* The source does not define the exact system indicators or UI screens used to confirm shutdown state in this example.
* The source does not specify formal escalation targets or routing.
* The source provides a narrated example rather than a complete diagnostic or recovery workflow.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_shutdown_agv_replacement_through_hospital
- Source ID: `training_video_day1`
- Source Type: `training_video`
