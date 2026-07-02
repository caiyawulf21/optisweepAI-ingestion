# Send An AGV To The Hospital To Drop The Tote And Reinitialize

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_send_an_agv_to_the_hospital_to_drop_the_tote_and_reinitialize_v1` |
| Title | Send An AGV To The Hospital To Drop The Tote And Reinitialize |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the AGV Go-to function as a recovery method to send an AGV to the hospital so the tote can be removed there, allowing the AGV to drop, reinitialize, and return to picking up a new tote instead of being physically moved.

## When To Use

Use when an AGV recovery situation requires sending the AGV to the hospital so its tote can be removed and the AGV can reinitialize and receive a new task. The source specifically describes this as a quick recovery approach using Go-to instead of physically moving the AGV out, after the AGV has been removed and added back in the described recovery example.

## Do Not Use For

* Do not use when the source conditions for Go-to are not met, such as when the AGV is still in a task.
* Do not use as justification to invent additional recovery branches beyond the source-backed hospital drop-off and tote removal sequence.
* Do not treat this source as approval for broad AGV removal actions on an active system beyond the specific recovery example described.

## Safety And Operational Notes

* The source presents this as a way to avoid physically moving or pushing the AGV out by using the Go-to function instead.
* The source indicates WCS will not reinitialize the AGV until the tote is removed and added again if the AGV remains in an improper bound state.
* A nearby source segment warns that removing an AGV on an active system is a high-risk action and may be restricted by credentials; this runbook does not expand AGV removal steps beyond the source example.

## Access Or Tools Needed

* Access to the AGV control interface with robot selection
* Go to function
* Map or destination selection including hospital
* Physical access or process access to remove the tote at the hospital

## Related Operational Context

* ctx_training_video_agv_go_to_function_v1
* ctx_training_video_hospital_dropoff_recovery_context_v1
* ctx_training_video_wcs_reinitialize_binding_context_v1

## Procedure Steps

### Step 1 — Remove and add the AGV back as part of the recovery example

**Responsible role:** operator

**Instruction:**
Perform the AGV remove-and-add action as referenced in the source recovery example before proceeding with the hospital Go-to workflow.

**Expected result:**
The AGV has been removed and added back as described in the source example and is ready for the next recovery action.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Recovery explanation tying remove-and-add of the AGV to later hospital drop-off and reinitialization.*


**Stop or Escalate If:**

* Stop or escalate if the AGV remains in an improper bound state and does not proceed toward reinitialization.
* Stop or escalate if local permissions or approved process do not allow the remove-and-add action.

---

### Step 2 — Use Go-to instead of physically moving the AGV

**Responsible role:** operator

**Instruction:**
Use the Go-to function for this recovery instead of physically moving the AGV out.

**Expected result:**
The recovery proceeds through the AGV interface and map-based destination selection rather than manual physical movement.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Go-to function description stating it saves the operator from pushing the AGV and supports recovery repositioning.*


**Stop or Escalate If:**

* Stop or escalate if the AGV is still in a task and therefore does not meet the source condition for Go-to use.
* Stop or escalate if the interface does not allow Go-to selection for the AGV.

---

### Step 3 — Select the AGV and choose the hospital destination

**Responsible role:** operator

**Instruction:**
Select the AGV, select Go to, and choose the hospital destination on the map or destination selection used for recovery.

**Expected result:**
The hospital destination is selected for the AGV in the Go-to workflow.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Robot Selection Go-to workflow and the recovery use of hospital as the destination.*


**Stop or Escalate If:**

* Stop or escalate if the AGV is not idle or not eligible for Go-to.
* Stop or escalate if the hospital destination cannot be identified in the available map or destination selector.

---

### Step 4 — Confirm the hospital destination

**Responsible role:** operator

**Instruction:**
Confirm the selected destination so the AGV navigates to the hospital.

**Expected result:**
The AGV is sent toward the hospital destination.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Final confirm step in the Go-to workflow.*


**Stop or Escalate If:**

* Stop or escalate if the AGV does not accept the destination or does not navigate toward the hospital.

---

### Step 5 — Remove the tote at the hospital

**Responsible role:** operator

**Instruction:**
At the hospital, remove the tote from the AGV so the AGV can drop and reinitialize.

**Expected result:**
The tote is removed at the hospital and the AGV is able to drop and reinitialize.

**Screens / Images:**

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Hospital area flow showing hospital entrance queue and drop-off context.*

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Recovery explanation stating the tote is removed at the hospital so the AGV can reinitialize.*


**Stop or Escalate If:**

* Stop or escalate if the tote cannot be removed at the hospital.
* Stop or escalate if WCS does not reinitialize the AGV after tote removal because the tote remains improperly bound.

---

### Step 6 — Verify the AGV reinitializes and picks up a new tote

**Responsible role:** operator

**Instruction:**
Verify that the AGV comes back and picks up a new tote after the hospital tote removal and reinitialization sequence.

**Expected result:**
The AGV reinitializes and receives a new task or tote as described by the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0035_it_d_be_a_question_mark_primary_01_25_36_500](assets/e520d09776d18225.jpg)

*Recovery outcome stating the AGV reinitializes and picks up a new tote.*


**Stop or Escalate If:**

* Stop or escalate if the AGV does not pick up a new tote after hospital drop-off and tote removal.
* Stop or escalate if WCS still does not reinitialize the AGV.

---

## Success Criteria

* The AGV is sent to the hospital using Go-to.
* The tote is removed at the hospital.
* The AGV drops and reinitializes.
* The AGV comes back and picks up a new tote or receives a new task as described by the source.

## Failure Conditions

* The AGV is still in a task and cannot be sent using Go-to.
* The AGV cannot be selected or the Go-to function is unavailable.
* The hospital destination cannot be selected or confirmed.
* The tote is not removed at the hospital.
* WCS does not reinitialize the AGV because the tote remains improperly bound.
* The AGV does not come back or does not pick up a new tote.

## Escalation Guidance

* Escalate if the AGV remains in an improper bound state after remove-and-add and hospital tote removal.
* Escalate if the tote cannot be removed at the hospital.
* Escalate if WCS does not reinitialize the AGV after the tote is removed.
* Escalate if permissions or approved process do not allow the required AGV recovery actions.

## Missing Details / Known Gaps

* The source does not provide the exact remove-and-add AGV interface steps within this packet.
* The source does not provide a precise hospital map coordinate, square code, or destination code.
* The source does not provide detailed tote removal handling instructions beyond removing the tote at the hospital.
* The source does not provide a time estimate for completing this recovery.
* The source does not explicitly define escalation ownership beyond indicating when reinitialization does not occur.

## Source Lineage

- Candidate IDs: candidate_training_video_send_agv_to_hospital_for_tote_drop_and_reinitialize
- Source ID: `training_video_day1`
- Source Type: `training_video`
