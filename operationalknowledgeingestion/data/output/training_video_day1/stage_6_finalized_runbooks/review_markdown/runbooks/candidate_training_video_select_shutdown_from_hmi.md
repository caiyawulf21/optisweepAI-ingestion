# Place the System into Shutdown from the HMI

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_place_the_system_into_shutdown_from_the_hmi_v1` |
| Title | Place the System into Shutdown from the HMI |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

The training states that after bag out the system returns to running, and that shutdown is a deliberate state the operator chooses from the Viva HMI when the next sort is not imminent.

## When To Use

Use when bag out has completed and the operator intends to place the system into shutdown rather than leave it in running state ready for another sort.

## Do Not Use For

* Do not use if you expect the system to enter shutdown automatically after bag out; the source states it returns to running unless shutdown is chosen.
* Do not use as a detailed HMI navigation procedure; the source does not provide the exact screen path, button label, or confirmation sequence.

## Safety And Operational Notes

* Use only the Viva HMI-based shutdown selection described by the source.
* The source does not provide any lockout, physical isolation, or production-stop prerequisites.

## Access Or Tools Needed

* Access to the Viva HMI
* Operator authority to select shutdown
* Visibility of current system state

## Related Operational Context

* ctx_training_video_post_bagout_running_state_v1
* ctx_training_video_hmi_shutdown_selection_v1
* ctx_training_video_shutdown_queue_reference_v1

## Procedure Steps

### Step 1 — Confirm the system is in running after bag out

**Responsible role:** operator

**Instruction:**
Check the current system state and confirm that after bag out completion the system is in running state rather than assuming it is already in shutdown.

**Expected result:**
The operator confirms the system remains in running after bag out unless shutdown has been deliberately selected.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Transcript-supported distinction between bag out completion, running state, and shutdown as a separate operator-selected state.*

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Overall system page area showing System State functions including shutdown.*


**Stop or Escalate If:**

* Escalate if the current system state cannot be determined from the HMI.
* Escalate if the system does not appear to return to running after bag out as described by the source.

---

### Step 2 — Select shutdown from the Viva HMI

**Responsible role:** operator

**Instruction:**
Use the Viva HMI to choose shutdown. The source supports that shutdown is something the operator chooses from the HMI, but it does not provide the exact screen path, button label, or confirmation sequence.

**Expected result:**
A deliberate shutdown request is made from the Viva HMI.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*Overall system page showing System Shutdown as one of the available system state actions.*

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Transcript evidence that shutdown is chosen from the HMI and references use of a Viva HMI.*


**Stop or Escalate If:**

* Escalate if shutdown cannot be selected from the HMI as described.
* Stop and escalate if the HMI path, button label, or confirmation sequence is required, because the source does not provide those details.

---

### Step 3 — Verify shutdown was intentionally entered

**Responsible role:** operator

**Instruction:**
Verify that shutdown was intentionally entered rather than assumed to happen automatically after bag out.

**Expected result:**
The operator confirms shutdown is the result of an intentional HMI action.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Evidence that running follows bag out unless shutdown is separately chosen.*


**Stop or Escalate If:**

* Escalate if the system state transition cannot be tied to an intentional HMI shutdown selection.
* Escalate if operators are relying on automatic post-bag-out shutdown behavior not supported by the source.

---

### Step 4 — Observe shutdown queue and charging behavior

**Responsible role:** operator

**Instruction:**
Expect AGVs to go into shutdown logic and charging behavior after shutdown is chosen, consistent with the training description.

**Expected result:**
AGVs are associated with shutdown queues and charger rotation behavior consistent with shutdown state.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Transcript-supported references to shutdown queues as where AGVs sit when shut down.*

![artifact_training_video_training_video_day1_0010_all_right_so_life_cycle_this_primary_00_15_09_500](assets/5959536fcd85fc0f.jpg)

*Lifecycle description showing AGVs returning to shutdown and cycling back to chargers.*

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*System Shutdown function and description that shutdown puts the system into a state for AGVs to rotate on chargers.*


**Stop or Escalate If:**

* Escalate if AGVs do not appear to enter shutdown queue behavior after shutdown is selected.
* Escalate if AGVs do not rotate on chargers as described by the source.

---

## Success Criteria

* The system is intentionally placed into shutdown from the Viva HMI.
* Shutdown is understood as a deliberate operator-selected state, not an automatic result of bag out.
* Observed AGV behavior is consistent with shutdown queues and charger rotation described by the source.

## Failure Conditions

* Shutdown cannot be selected from the HMI as described.
* Operators assume shutdown occurs automatically after bag out.
* The source-required HMI details needed to execute the action are unavailable because the source does not provide exact navigation or control names.
* AGV shutdown queue or charging behavior does not match the training description.

## Escalation Guidance

* Escalate if shutdown cannot be selected from the HMI as described by the source.
* Escalate if the current system state cannot be confirmed as running after bag out or shutdown after selection.
* Escalate if AGVs do not exhibit the shutdown queue or charger rotation behavior described in the training.
* Escalate for SME review because the source does not provide the exact HMI screen path, button label, or confirmation sequence.

## Missing Details / Known Gaps

* The source does not provide the exact Viva HMI screen path for selecting shutdown.
* The source does not provide the exact shutdown button label or control name.
* The source does not provide the confirmation sequence or expected on-screen confirmation text after selecting shutdown.
* The source does not provide a time estimate for shutdown completion.
* The source does not define explicit fault codes or thresholds for failed shutdown.

## Source Lineage

- Candidate IDs: candidate_training_video_select_shutdown_from_hmi
- Source ID: `training_video_day1`
- Source Type: `training_video`
