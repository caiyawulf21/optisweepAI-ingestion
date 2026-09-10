# Clear flashing ESTOP fault at the operator station using HMI RESET

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_clear_flashing_estop_fault_operator_station_hmi_reset_v1` |
| Title | Clear flashing ESTOP fault at the operator station using HMI RESET |
| Procedure Type | `recovery` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `e_stop_or_safety_stop` |
| Access Surface | `physical_floor`, `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

If the operator station ESTOP is flashing, pull out the ESTOP and press RESET on the operator station HMI to clear faults so startup actions (homing/cycle start) can proceed.

## When To Use

Use when the operator station control panel shows the ESTOP is flashing and you need to clear the fault condition so you can proceed with operator station startup actions (homing/cycle start).

## Safety And Operational Notes

* Only the operator should perform physical E-stop actions.

## Access Or Tools Needed

* Operator station control panel
* Operator station HMI screen with RESET

## Related Operational Context

* ctx_manual_operator_station_estop_reset_v1

## Visual References

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Operator station main screen image showing the operator station startup context and the instruction: if ESTOP is flashing, pull out the ESTOP and press RESET on the HMI screen to clear faults.*

![artifact_page_84_image_10](assets/4732f0f687f2382f.png)

*HMI screen capture showing operator station fault display context (MCP_Dual / manual mode fault display) used with RESET for fault clearing.*

![artifact_page_84_image_13](assets/37a39c61d1bfe406.png)

*Operator station HMI screen showing manual mode fault status and RESET control for non-recoverable operator station motor faults (RESET used to clear faults).*

## Procedure Steps

### Step 1 — Check whether the operator station ESTOP is flashing

**Responsible role:** operator

**Instruction:**
At the operator station control panel, check whether the ESTOP is flashing.

**Expected result:**
The ESTOP status is observed as flashing (fault condition present).

---

### Step 2 — Pull out the ESTOP if it is flashing

**Responsible role:** operator

**Instruction:**
If the ESTOP is flashing, pull out the ESTOP.

**Expected result:**
The ESTOP has been pulled out (physical ESTOP action completed).

---

### Step 3 — Press HMI RESET to clear faults

**Responsible role:** operator

**Instruction:**
On the operator station HMI screen, press RESET to clear any faults.

**Expected result:**
After pressing RESET, the flashing ESTOP fault condition is cleared (the ESTOP is no longer flashing).

**Stop or Escalate If:**

* If the ESTOP remains flashing after pulling out ESTOP and pressing HMI RESET, stop and escalate rather than continuing with homing/cycle start.

---

### Step 4 — Confirm the flashing ESTOP condition is cleared before proceeding

**Responsible role:** operator

**Instruction:**
Confirm the fault condition is cleared by checking that the ESTOP is no longer flashing; proceed only if the flashing condition is no longer present.

**Expected result:**
The ESTOP is no longer flashing (fault condition cleared).

**Stop or Escalate If:**

* If the ESTOP remains flashing after pulling out ESTOP and pressing HMI RESET, stop and escalate rather than continuing with homing/cycle start.

---

## Success Criteria

* ESTOP is no longer flashing after pulling out the ESTOP and pressing RESET on the operator station HMI.

## Failure Conditions

* ESTOP remains flashing after pulling out the ESTOP and pressing HMI RESET.

## Escalation Guidance

* If the ESTOP remains flashing after pulling out ESTOP and pressing HMI RESET, stop and escalate rather than continuing with homing/cycle start.

## Source Lineage

- Candidate IDs: candidate_manual_operator_station_estop_reset_flashing
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
