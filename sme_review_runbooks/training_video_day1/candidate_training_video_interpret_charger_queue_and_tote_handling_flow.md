# Interpret AGV Flow Through the Charger Module

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_agv_flow_through_the_charger_module_v1` |
| Title | Interpret AGV Flow Through the Charger Module |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training material for the charger module to interpret the expected AGV sequence through charger entrance queue, tote drop-off, charging without a tote, tote pickup when applicable, and exit queue.

## When To Use

Use this reference when reviewing the charger module training diagram or observing AGV movement to compare actual charger-area behavior against the documented sequence described in the training source.

## Do Not Use For

* Do not use this as a charging control procedure.
* Do not use this source alone to infer charger fault causes.
* Do not use this source alone to define recovery actions.

## Safety And Operational Notes

* This candidate is an interpretation aid derived from training narration and slide content, not an operational charging control procedure.
* Do not infer charger fault causes or recovery actions from this training segment alone.

## Access Or Tools Needed

* Access to the training slide or diagram for the charger module
* Ability to observe AGV position relative to charger entrance queue, tote locations, pickup, and exit queue

## Related Operational Context

* ctx_training_video_charger_queue_and_tote_handling_v1

## Procedure Steps

### Step 1 — Identify charger flow locations on the training diagram

**Responsible role:** operator

**Instruction:**
Locate the charger portion of the modularization diagram or training material and identify the entrance queue, tote drop-off locations, tote pickup location, and exit queue.

**Expected result:**
The charger flow locations are identifiable on the source material.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Charger area labels and flow elements showing entrance queue, tote drop-off locations, tote pickup, and exit queue.*


**Stop or Escalate If:**

* Escalate if the charger movement reference points cannot be identified from the source material.

---

### Step 2 — Confirm charger entry through the entrance queue

**Responsible role:** operator

**Instruction:**
Confirm that the AGV enters the charger through the entrance queue.

**Expected result:**
The AGV path into the charger is interpreted as entering through the entrance queue.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*The charger entrance queue and the AGV approach path into the charger module.*


**Stop or Escalate If:**

* Escalate if observed charger movement does not match the documented entrance queue sequence.

---

### Step 3 — Verify tote drop-off before charging

**Responsible role:** operator

**Instruction:**
Verify that the AGV drops off its tote at the tote location before charging.

**Expected result:**
The AGV is interpreted as dropping off its tote before charging.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Tote drop-off locations in the charger module and their position before the charging step.*


**Stop or Escalate If:**

* Escalate if observed charger movement does not match the documented tote drop-off before charging.

---

### Step 4 — Confirm charging occurs without a tote

**Responsible role:** operator

**Instruction:**
Check that the AGV charges without a tote on it, consistent with the source statement that it does not like to charge with totes on it.

**Expected result:**
The charging state is interpreted as occurring without a tote on the AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*The charger flow sequence showing tote drop-off before charging and pickup after charging.*


**Stop or Escalate If:**

* Escalate if observed charger movement does not match the documented no-tote charging sequence.

---

### Step 5 — Verify tote pickup after charging

**Responsible role:** operator

**Instruction:**
After charging, verify that the AGV goes to pick up its tote.

**Expected result:**
The AGV is interpreted as returning to tote pickup after charging.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*The tote pickup location and its position after the charging step.*


**Stop or Escalate If:**

* Escalate if observed charger movement does not match the documented tote pickup after charging.

---

### Step 6 — Apply the shutdown-state tote exception

**Responsible role:** operator

**Instruction:**
In a shutdown state, note the source exception that some AGVs may not have totes and therefore do not need the tote pickup step.

**Expected result:**
Shutdown-state observations are interpreted with the tote exception in mind.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*The charger flow context while applying the shutdown-state exception for AGVs without totes.*


**Stop or Escalate If:**

* Escalate if shutdown-state charger movement cannot be reconciled with the source-noted tote exception.

---

### Step 7 — Confirm exit through the charger exit queue

**Responsible role:** operator

**Instruction:**
Confirm that after charging and any tote pickup, the AGV proceeds to the exit queue.

**Expected result:**
The AGV is interpreted as leaving the charger through the exit queue.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*The charger exit queue and the final AGV path after charging and any tote pickup.*


**Stop or Escalate If:**

* Escalate if observed charger movement does not match the documented exit queue sequence.

---

## Success Criteria

* The user can trace the documented charger-module sequence from entrance queue to exit queue.
* Observed AGV movement can be compared against the source-described sequence of tote drop-off, charging without a tote, tote pickup when applicable, and exit.

## Failure Conditions

* Observed charger movement does not match the documented entrance, tote drop-off, charging, tote pickup when applicable, and exit sequence.
* The source material is insufficient to confidently identify charger flow locations.
* The user attempts to infer charger fault causes or recovery actions from this training segment alone.

## Escalation Guidance

* Escalate if observed charger movement does not match the documented entrance, tote drop-off, charging, tote pickup when applicable, and exit sequence.
* Escalate for SME review if charger behavior appears inconsistent with the training reference and additional operational guidance is needed.
* Do not infer charger fault causes or recovery actions from this training segment alone.

## Missing Details / Known Gaps

* The source does not provide a formal charging control procedure.
* The source does not define fault causes, recovery actions, or troubleshooting commands for charger issues.
* The source does not specify timing expectations for each charger flow step.
* The source does not define role boundaries beyond operator-level interpretation use.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_charger_queue_and_tote_handling_flow
- Source ID: `training_video_day1`
- Source Type: `training_video`
