# Home tipper axes (Z1/A1 and Z2/A2) using AUTO REF and verify home proximity switch stop

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_home_tipper_axes_auto_ref_verify_home_proximity_switch_stop_v1` |
| Title | Home tipper axes (Z1/A1 and Z2/A2) using AUTO REF and verify home proximity switch stop |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Home all tipper axes so the system can proceed to cycle start. Use AUTO REF to home the left tipper axes (Z1/A1) and right tipper axes (Z2/A2), and verify the axis button state changes green→yellow while moving and that the tipper motor stops after sensing the “home” proximity switch.

## When To Use

Use when the system/operator station needs to home every tipper axis (Z1/A1 left tipper and Z2/A2 right tipper) before pressing CYCLE START.

## Access Or Tools Needed

* Operator station control panel
* Operator station HMI screen showing AUTO REF and axis button indicators

## Related Operational Context

* ctx_manual_tipper_axis_homing_v1

## Visual References

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Operator station main screen image showing the CYCLE STOP button and the homing step text (AUTO REF; axis button green→yellow; home proximity switch stop).*

## Procedure Steps

### Step 1 — Identify left and right tipper axis controls (Z1/A1 and Z2/A2) on the operator station

**Responsible role:** operator

**Instruction:**
At the operator station, identify the axis controls for Z1 and A1 (left tipper) and Z2 and A2 (right tipper) on the operator station HMI.

**Expected result:**
You can clearly locate the axis controls/indicators corresponding to Z1/A1 (left) and Z2/A2 (right) on the operator station HMI.

---

### Step 2 — Press AUTO REF to home all tipper axes

**Responsible role:** operator

**Instruction:**
Press AUTO REF to reference/home every axis (Z1/A1 and Z2/A2).

**Expected result:**
The homing sequence starts for the axes.

**Stop or Escalate If:**

* If axis buttons do not change green→yellow when AUTO REF is pressed, stop and escalate.

---

### Step 3 — Verify axis button state changes green→yellow while moving

**Responsible role:** operator

**Instruction:**
Observe each axis button for Z1/A1 and Z2/A2 and confirm the axis button changes from green to yellow to indicate it is moving.

**Expected result:**
Each axis button changes from green to yellow during AUTO REF homing.

**Stop or Escalate If:**

* If axis buttons do not change green→yellow when AUTO REF is pressed, stop and escalate.

---

### Step 4 — Verify tipper motor stops after sensing the “home” proximity switch

**Responsible role:** operator

**Instruction:**
Watch the tipper motor movement for each side until it senses the “home” proximity switch, then confirm the motor stops.

**Expected result:**
For each axis/side, the tipper motor moves until it senses the “home” proximity switch, then stops.

**Stop or Escalate If:**

* If the motor does not stop at the 'home' proximity switch, stop and escalate.

---

### Step 5 — Confirm homing is complete for both left (Z1/A1) and right (Z2/A2) axes before proceeding

**Responsible role:** operator

**Instruction:**
Confirm homing is complete for both left (Z1/A1) and right (Z2/A2) axes before proceeding to cycle start.

**Expected result:**
Both left and right tipper axes have completed homing (no longer moving as part of AUTO REF).

**Stop or Escalate If:**

* If homing is not complete for both left and right axes, stop and escalate.

---

## Success Criteria

* Axis buttons for Z1/A1 and Z2/A2 change from green to yellow while moving during AUTO REF.
* Tipper motor movement stops after sensing the “home” proximity switch.
* Homing is complete for both left (Z1/A1) and right (Z2/A2) axes before proceeding.

## Failure Conditions

* Axis buttons do not change green→yellow when AUTO REF is pressed.
* Tipper motor does not stop at the “home” proximity switch.
* Homing is not complete for both left (Z1/A1) and right (Z2/A2) axes.

## Escalation Guidance

* Stop and escalate if axis buttons do not change green→yellow when AUTO REF is pressed, or if the motor does not stop at the 'home' proximity switch.

## Missing Details / Known Gaps

* The candidate requests specific screenshots for green→yellow axis button state and home proximity switch behavior, but only one relevant operator-station image artifact (page 82) is attached at runbook level in this packet. If additional artifacts are required for those specific visuals, they are not provided as step-level evidence here.

## Source Lineage

- Candidate IDs: candidate_manual_operator_station_home_axes_auto_ref
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
