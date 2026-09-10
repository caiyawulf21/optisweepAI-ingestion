# Manually Jog the Tipper End Effector Using Operator Station HMI (Visu_Dual_MCP)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_manually_jog_tipper_end_effector_visu_dual_mcp_v1` |
| Title | Manually Jog the Tipper End Effector Using Operator Station HMI (Visu_Dual_MCP) |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI jogging screen (Visu_Dual_MCP) to stop the automatic tipping cycle and manually move the tipper axes (Z1/A1 for left, Z2/A2 for right) using the +/− controls in Manual Mode.

## When To Use

When you need to move the tipper end effector into a desired maintenance position by manually jogging the left and/or right tipper axes from the operator station HMI (Visu_Dual_MCP).

## Safety And Operational Notes

* Stop jogging before the axis reaches a hard stop; pushing an axis to a hard stop registers a fault.

## Access Or Tools Needed

* Operator station HMI access
* Visu_Dual_MCP screen (F3)
* HMI controls: CYCLE STOP, JOG, axis +/− buttons (Z1, Z2, A1, A2)

## Related Operational Context

* ctx_manual_tipper_jogging_mode_v1
* ctx_manual_tipper_jogging_hmi_screen_v1
* ctx_manual_tipper_axis_hard_stop_fault_v1

## Visual References

![artifact_page_83_image_10](assets/acd8e7472a45f789.png)

*Visu_Dual_MCP jogging screen showing Manual Mode and the Z1/Z2/A1/A2 axis +/− controls.*

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Operator station main screen showing the CYCLE STOP button.*

## Procedure Steps

### Step 1 — Navigate to the Visu_Dual_MCP jogging screen (F3)

**Responsible role:** operator

**Instruction:**
On the operator station HMI, navigate to the "Visu_Dual_MCP" screen (F3).

**Expected result:**
The "Visu_Dual_MCP" screen is displayed and you can access the CYCLE STOP and JOG controls.

---

### Step 2 — Stop the automatic tipping cycle using CYCLE STOP

**Responsible role:** operator

**Instruction:**
Press "CYCLE STOP" to stop the automatic tipping cycle.

**Expected result:**
The automatic tipping cycle is stopped (CYCLE STOP action has been applied).

---

### Step 3 — Open the jogging screen using JOG

**Responsible role:** operator

**Instruction:**
Press "JOG" to open the jogging screen.

**Expected result:**
The jogging screen opens and shows Manual Mode.

---

### Step 4 — Confirm Manual Mode and identify axis controls (Z1, Z2, A1, A2)

**Responsible role:** operator

**Instruction:**
On the jogging screen, confirm you are in "Manual Mode" and identify the axis controls for Z1, Z2, A1, and A2.

**Expected result:**
Manual Mode is shown and the axis +/− controls for Z1, Z2, A1, and A2 are visible.

---

### Step 5 — Jog the left tipper axes (Z1/A1) or right tipper axes (Z2/A2) using +/−

**Responsible role:** operator

**Instruction:**
Select the axis you want to move and use the "−" and "+" buttons to move it: Z1 (vertical movement) and A1 (rotate gripper) move the left tipper; Z2 and A2 move the right tipper.

**Expected result:**
The selected axis responds to the jog command while Manual Mode is active.

---

### Step 6 — Use correct +/− motion behavior for Z and A axes

**Responsible role:** operator

**Instruction:**
Use the +/− behavior as documented: "+" moves the Z-axis up and rotates the A-axis toward the operator; "−" moves the Z-axis down and rotates the A-axis away from the operator.

**Expected result:**
Pressing "+" produces Z up + A toward operator motion; pressing "−" produces Z down + A away motion.

---

### Step 7 — Avoid hard stops; stop jogging before the axis reaches a hard stop

**Responsible role:** operator

**Instruction:**
Stop jogging before the axis reaches a hard stop. Do not push the axis into the hard stop.

**Expected result:**
No hard-stop fault is registered while jogging.

**Stop or Escalate If:**

* If an axis is driven into a hard stop and the axis registers a fault, stop further jogging and escalate to maintenance/support for the fault condition.

---

## Success Criteria

* Tipper end effector responds to selected axis jog commands while HMI is in Manual Mode.
* Operator avoids driving an axis into a hard stop (no hard-stop fault registered).

## Failure Conditions

* Axis registers a fault after being pushed to a hard stop.

## Escalation Guidance

* If an axis is driven into a hard stop and the axis registers a fault, stop further jogging and escalate to maintenance/support for the fault condition.

## Source Lineage

- Candidate IDs: candidate_manual_optisweep_jogging_tipper_visu_dual_mcp
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
