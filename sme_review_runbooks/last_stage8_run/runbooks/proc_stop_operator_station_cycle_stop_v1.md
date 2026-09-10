# Stop the Operator Station using the CYCLE STOP button on the Operator Station Main Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_operator_station_cycle_stop_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

An operator can stop the operator station by pressing the CYCLE STOP button on the operator station main screen.

## When To Use

Use when you need to stop the operator station cycle from the operator station main screen by pressing the CYCLE STOP control.

## Source Procedure References

- proc_stop_operator_station_cycle_stop_v1

## Procedure Steps

### Step 1 — Open the Operator Station Main Screen

**Responsible role:** operator

**Instruction:**
On the operator station HMI, navigate to the operator station main screen.

**Expected result:**
The operator station main screen is displayed and the CYCLE STOP control is available for use.

---

### Step 2 — Press CYCLE STOP to stop the operator station

**Responsible role:** operator

**Instruction:**
Press the CYCLE STOP button on the operator station main screen.

**Expected result:**
The operator station stops after pressing CYCLE STOP.

---

### Step 3 — Verify the operator station is stopped

**Responsible role:** operator

**Instruction:**
Observe the operator station after pressing CYCLE STOP to confirm it is stopped.

**Expected result:**
The operator station is stopped (the cycle is no longer running after pressing CYCLE STOP).

---

## Success Criteria

- After pressing CYCLE STOP on the operator station main screen, the operator station stops and the cycle no longer runs.

## Failure Conditions

- CYCLE STOP does not stop the operator station cycle.

## Escalation Guidance

- If pressing CYCLE STOP does not stop the operator station, stop further operation and escalate to support.
