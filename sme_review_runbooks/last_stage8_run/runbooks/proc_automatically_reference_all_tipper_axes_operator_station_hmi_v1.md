# Automatically Reference All Tipper Axes Using Operator Station HMI (RESET → AUTO REF → AUTO → CYCLE START)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_automatically_reference_all_tipper_axes_operator_station_hmi_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the operator station HMI to run automatic axis referencing for all tipper axes. Confirm referencing completion by watching the 'R' icons turn green, then press AUTO and CYCLE START to resume operation.

## When To Use

Use when tipper axes need re-commissioning/initialization and you need to automatically reference all tipper axes from the operator station HMI, then restart operation.

## Source Procedure References

- proc_automatically_reference_all_tipper_axes_operator_station_hmi_v1

## Procedure Steps

### Step 1 — Press RESET on the operator station HMI

**Responsible role:** operator

**Instruction:**
On the operator station HMI, press RESET.

**Expected result:**
The automatic referencing sequence is initiated (next step AUTO REF becomes the action to reference all tipper axes).

---

### Step 2 — Press AUTO REF to reference all tipper axes

**Responsible role:** operator

**Instruction:**
Press AUTO REF to reference all of the axes of the tippers.

**Expected result:**
Referencing begins and the 'R' icons will indicate progress.

---

### Step 3 — Verify referencing completion by watching 'R' icons turn green

**Responsible role:** operator

**Instruction:**
Watch the 'R' icons until they turn green, indicating referencing is completed.

**Expected result:**
All relevant 'R' icons turn green (referencing completed).

---

### Step 4 — Press AUTO after referencing is completed

**Responsible role:** operator

**Instruction:**
When referencing is completed, press AUTO.

**Expected result:**
AUTO is pressed after the 'R' icons are green.

---

### Step 5 — Press CYCLE START to restart operation

**Responsible role:** operator

**Instruction:**
Press CYCLE START to restart operation.

**Expected result:**
The operation cycle restarts after AUTO is set.

---

## Success Criteria

- After pressing AUTO REF, the 'R' icons turn green (referencing completed).
- After pressing AUTO and CYCLE START, operation restarts.

## Failure Conditions

- The 'R' icons do not turn green after AUTO REF.

## Escalation Guidance

- If the 'R' icons do not turn green, stop and escalate for support rather than proceeding to AUTO/CYCLE START.
