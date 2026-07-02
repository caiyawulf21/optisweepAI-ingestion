# Interpret The High-Level Sort Lifecycle And AGV State Progression

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_the_high_level_sort_lifecycle_and_agv_state_progression_v1` |
| Title | Interpret The High-Level Sort Lifecycle And AGV State Progression |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-based reference to identify the current sort lifecycle phase and compare observed AGV and tote behavior against the training-described progression of startup, bulk sort, bag-out, and shutdown.

## When To Use

Use when reviewing or observing OptiSweep operation to determine whether the system appears to be in startup, bulk sort, bag-out, or shutdown, and to compare AGV behavior to the training-described lifecycle sequence.

## Do Not Use For

* Do not use this runbook as a detailed operating procedure for issuing controls or changing system state.
* Do not use this runbook to infer undocumented AGV state names, controls, corrective actions, thresholds, or transition logic.
* Do not use this runbook as the sole source for fault recovery or troubleshooting steps.

## Safety And Operational Notes

* This source provides a high-level lifecycle overview rather than a detailed operating procedure.
* Do not infer undocumented state names, controls, or corrective actions from this overview-only source.

## Access Or Tools Needed

* Access to observe system operation or AGV behavior
* Training source describing the sort lifecycle

## Related Operational Context

* ctx_training_video_sort_lifecycle_overview_v1
* ctx_training_video_agv_startup_and_shutdown_states_v1
* ctx_training_video_bulk_sort_and_bag_out_functions_v1

## Procedure Steps

### Step 1 — Identify the current sort phase

**Responsible role:** operator

**Instruction:**
Identify the current sort phase using the source-described lifecycle: startup, bulk of the sort, bag-out cycle, or shutdown.

**Expected result:**
The current observed condition is mapped to one of the documented lifecycle phases.

**Screens / Images:**

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Slide showing the lifecycle of a sort and the sequence of phases.*


**Stop or Escalate If:**

* Observed system behavior does not align with the documented lifecycle sequence.

---

### Step 2 — Verify startup state progression

**Responsible role:** operator

**Instruction:**
For startup, verify that AGVs are described as beginning in a shutdown state at specific charging locations and transitioning from a power cycling state to being staged for sort.

**Expected result:**
Startup is recognized as AGVs moving from shutdown at charging locations through power cycling to staged-for-sort.

**Screens / Images:**

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle slide text describing AGVs starting in shutdown at charging locations and moving to staged-for-sort during startup.*


**Stop or Escalate If:**

* Startup behavior does not align with the documented progression.
* The source overview is insufficient to determine a corrective action.

---

### Step 3 — Verify bulk sort behavior

**Responsible role:** operator

**Instruction:**
For the bulk of the sort, verify that items are being sorted and that AGVs take full totes to the tippers for bagging.

**Expected result:**
Bulk sort is recognized by active item sorting and AGVs moving full totes to tippers for bagging.

**Screens / Images:**

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle slide description of bulk sort where AGVs take full totes to tippers for bagging.*

![artifact_training_video_training_video_day1_0016_has_this_ever_happened_that_an_primary_00_30_23_500](assets/abc7a5228ea55d27.jpg)

*Tipper workflow showing a full tote assigned to a tipper, queued, tipped, and bag-label handling.*


**Stop or Escalate If:**

* Observed bulk sort behavior does not align with the documented lifecycle sequence.

---

### Step 4 — Verify bag-out behavior

**Responsible role:** operator

**Instruction:**
For bag-out, check whether locations that still have items in a tote are being cycled to finish out the sort.

**Expected result:**
Bag-out is recognized as cycling locations with remaining tote contents to complete the sort.

**Screens / Images:**

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle slide description of bag-out as cycling locations with remaining tote items to finish the sort.*

![artifact_training_video_training_video_day1_0057_i_don_t_remember_everything_that_primary_02_09_56_000](assets/e89b88ff5a9b5dcb.jpg)

*Bag-out control description stating system bag out closes destinations and exchanges totes with parcels in them.*


**Stop or Escalate If:**

* Bag-out behavior does not align with the documented lifecycle sequence.

---

### Step 5 — Verify shutdown return to chargers

**Responsible role:** operator

**Instruction:**
For shutdown, verify that AGVs cycle back to the charger to prepare for the next sort.

**Expected result:**
Shutdown is recognized by AGVs returning to chargers in preparation for the next sort.

**Screens / Images:**

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle slide description of shutdown with AGVs cycling back to chargers.*

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Charger flow showing charger entrance queue, tote drop-off while charging, tote pickup after charging, and exit queue.*


**Stop or Escalate If:**

* Shutdown behavior does not align with the documented lifecycle sequence.

---

### Step 6 — Compare observed behavior to the documented lifecycle

**Responsible role:** operator

**Instruction:**
Compare the observed system behavior to the source-described lifecycle sequence and record any phase that does not match the documented progression.

**Expected result:**
Any mismatch between observed behavior and the documented lifecycle is identified and recorded.

**Screens / Images:**

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle sequence used as the comparison baseline.*


**Stop or Escalate If:**

* Observed system behavior does not align with the documented lifecycle sequence.
* A mismatch requires corrective action not provided by this overview-only source.

---

## Success Criteria

* The current sort lifecycle phase can be identified as startup, bulk sort, bag-out, or shutdown.
* Observed AGV and tote behavior can be compared to the documented lifecycle sequence.
* Any mismatch between observed behavior and the documented progression is recorded for escalation.

## Failure Conditions

* Observed system behavior does not align with the documented lifecycle sequence.
* The current phase cannot be mapped to the source-described lifecycle.
* Observed startup, bulk sort, bag-out, or shutdown behavior differs from the training overview.

## Escalation Guidance

* Escalate if observed system behavior does not align with the documented lifecycle sequence.
* Escalate when a mismatch requires controls, state interpretation, or corrective actions not provided by this overview-only source.

## Missing Details / Known Gaps

* The source is a high-level training overview and does not provide detailed operator controls or exact system-state verification methods.
* The source does not provide explicit corrective actions for lifecycle mismatches.
* The source does not provide commands, thresholds, timing expectations, or formal escalation routing.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_sort_lifecycle_states
- Source ID: `training_video_day1`
- Source Type: `training_video`
