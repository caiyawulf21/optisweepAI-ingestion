# Use Go To To Drop Off An AGV At The Hospital During A Quick Recovery Scenario

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_go_to_to_drop_off_an_agv_at_the_hospital_during_a_quick_recovery_scenario_v1` |
| Title | Use Go To To Drop Off An AGV At The Hospital During A Quick Recovery Scenario |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection Go-to function as a quick recovery aid in the example scenario where a tipper goes down and an AGV will not leave. The source states the operator can remove and add the AGV, then use Go to to send it to a selected square at the hospital, and that the AGV will pick up a new task once its tote has been removed.

## When To Use

Use in the source-described quick recovery example when equipment is down, specifically when a tipper goes down and an AGV will not leave, and the AGV is being repositioned to the hospital using the Go-to function.

## Do Not Use For

* Do not use as a fully operationalized remove/add AGV procedure; the source states to remove and add the AGV but does not define how to perform that subprocedure.
* Do not use when a different recovery path is required; this source only supports the specific example recovery scenario described.
* Do not assume this source authorizes AGV removal on an active system without role or site approval; related packet evidence notes access may be restricted and warns against removing an AGV on an active system.

## Safety And Operational Notes

* The source frames this as a quick recovery example, not a complete controlled maintenance procedure.
* The source does not define the remove and add AGV subprocedure; obtain SME review before operationalizing that portion.
* Packet evidence indicates removing an AGV on an active system may be a restricted or high-risk action.

## Access Or Tools Needed

* Access to the OptiSweep map screen
* Ability to select the AGV
* Go to function
* Confirm control
* Ability to remove the tote from the AGV

## Related Operational Context

* ctx_training_video_go_to_recovery_use_case_v1
* ctx_training_video_agv_task_resumption_after_tote_removal_v1
* ctx_training_video_robot_selection_go_to_function_v1

## Procedure Steps

### Step 1 — Identify the affected AGV on the map

**Responsible role:** operator

**Instruction:**
On the map, identify the AGV involved in the recovery scenario where a tipper goes down and the AGV will not leave.

**Expected result:**
The affected AGV is visually identified on the map and ready for selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0040_so_i_actually_covered_it_over_primary_01_34_56_000](assets/903dfff9c643e46a.jpg)

*Robot Selection Go-to slide and map-selection context showing that the AGV is selected from the map.*


**Stop or Escalate If:**

* Stop and escalate if the affected AGV cannot be confidently identified on the map.
* Stop and escalate if the map view does not allow AGV selection.

---

### Step 2 — Remove and add the AGV

**Responsible role:** operator

**Instruction:**
Remove and add the AGV as stated in the source for this recovery example. Because the source does not define how to perform this subprocedure, use only approved site-specific controls and permissions.

**Expected result:**
The AGV has been removed and added back as part of the example recovery setup.

**Stop or Escalate If:**

* Stop and escalate if the operator does not have credentials to remove and add the AGV.
* Stop and escalate if site policy does not permit AGV removal on an active system.
* Stop and escalate because the source does not provide the remove/add subprocedure details.

---

### Step 3 — Select the AGV

**Responsible role:** operator

**Instruction:**
Select the AGV on the map.

**Expected result:**
The AGV is selected as the active object in the interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0040_so_i_actually_covered_it_over_primary_01_34_56_000](assets/903dfff9c643e46a.jpg)

*The visible step list showing 'Select an AGV' and the map-selection context.*


**Stop or Escalate If:**

* Stop and escalate if the AGV cannot be selected from the map.

---

### Step 4 — Select Go to

**Responsible role:** operator

**Instruction:**
Select Go to.

**Expected result:**
The Go-to function is activated for the selected AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0040_so_i_actually_covered_it_over_primary_01_34_56_000](assets/903dfff9c643e46a.jpg)

*The visible step list showing 'Select Go to' in the Robot Selection Go-to function.*


**Stop or Escalate If:**

* Stop and escalate if the Go-to function is not available for the selected AGV.

---

### Step 5 — Select the hospital destination square

**Responsible role:** operator

**Instruction:**
Select the destination square used to drop the AGV off at the hospital.

**Expected result:**
A destination square is selected for the AGV's Go-to movement toward the hospital.

**Screens / Images:**

![artifact_training_video_training_video_day1_0040_so_i_actually_covered_it_over_primary_01_34_56_000](assets/903dfff9c643e46a.jpg)

*The visible step list showing square selection and the recovery text describing drop-off at the hospital.*


**Stop or Escalate If:**

* Stop and escalate if the correct hospital destination square cannot be determined from the source and local map context.
* Stop and escalate if the selected square does not represent the intended hospital drop-off area.

---

### Step 6 — Confirm the Go-to command

**Responsible role:** operator

**Instruction:**
Select Confirm.

**Expected result:**
The Go-to command is confirmed for the selected AGV and destination square.

**Screens / Images:**

![artifact_training_video_training_video_day1_0040_so_i_actually_covered_it_over_primary_01_34_56_000](assets/903dfff9c643e46a.jpg)

*The visible step list showing 'Select Confirm' as the final Go-to action.*


**Stop or Escalate If:**

* Stop and escalate if the system does not accept the confirmation.
* Stop and escalate if the AGV does not proceed as expected after confirmation.

---

### Step 7 — Remove the tote from the AGV

**Responsible role:** operator

**Instruction:**
Remove the tote from the AGV.

**Expected result:**
The tote is removed from the AGV and the AGV becomes able to pick up a new task as described by the source.

**Stop or Escalate If:**

* Escalate if the AGV does not resume by picking up a new task after tote removal.
* Stop and escalate if tote removal cannot be completed safely or with approved site handling.

---

## Success Criteria

* The AGV is dropped off at the hospital using the Go-to function.
* The tote is removed from the AGV.
* The AGV picks up a new task after tote removal.

## Failure Conditions

* The AGV cannot be identified or selected on the map.
* The remove/add AGV action cannot be performed or is not permitted.
* The correct hospital destination square cannot be determined.
* The Go-to command cannot be confirmed.
* The AGV does not pick up a new task after tote removal.

## Escalation Guidance

* Escalate for SME or supervisor review before operational use because the source does not define the remove/add AGV subprocedure.
* Escalate if permissions are insufficient to remove and add the AGV.
* Escalate if the AGV does not resume by picking up a new task after tote removal, because no further recovery steps are provided in this source.

## Missing Details / Known Gaps

* The source does not define how to perform the remove and add AGV subprocedure.
* The source does not specify the exact hospital destination square or map coordinates.
* The source does not provide explicit validation checks showing how to confirm the AGV has reached the hospital.
* The source does not provide timing expectations for task resumption after tote removal.
* The source does not define role-based authorization boundaries beyond indirect evidence that some users may lack remove/add permissions.

## Source Lineage

- Candidate IDs: candidate_training_video_reposition_agv_to_hospital_for_quick_recovery
- Source ID: `training_video_day1`
- Source Type: `training_video`
