# Stop the OptiSweep System Using the System HMI API Screen (SYSTEM SHUTDOWN)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `fleet_system_status` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the system HMI API screen to initiate SYSTEM SHUTDOWN and confirm the AGVs transition to a shutdown queue between sorts.

## When To Use

When you need to stop the OptiSweep system between sorts so AGVs move to a shutdown queue.

## Source Procedure References

- proc_stop_optsweepsystem_via_system_hmi_api_screen_system_shutdown_v1

## Safety And Operational Notes

- The system should be shutdown between sorts to allow AGVs to charge.

## Procedure Steps

### Step 1 — Navigate to the system API screen on the system HMI

**Responsible role:** operator

**Instruction:**
On the system HMI, navigate to the system API screen.

**Expected result:**
The system API screen is open and ready for the SYSTEM SHUTDOWN action.

---

### Step 2 — Press SYSTEM SHUTDOWN

**Responsible role:** operator

**Instruction:**
Press SYSTEM SHUTDOWN on the system API screen.

**Expected result:**
SYSTEM SHUTDOWN is initiated.

---

### Step 3 — Confirm AGVs transition to the shutdown queue

**Responsible role:** operator

**Instruction:**
Observe that the AGVs go to a shutdown queue after SYSTEM SHUTDOWN.

**Expected result:**
AGVs are in a shutdown queue state.

---

## Success Criteria

- After pressing SYSTEM SHUTDOWN, AGVs are in a shutdown queue state.

## Failure Conditions

- AGVs do not transition to the shutdown queue after SYSTEM SHUTDOWN.

## Escalation Guidance

- Escalate if AGVs do not transition to the shutdown queue after SYSTEM SHUTDOWN.

## Missing Details / Known Gaps

- The packet does not specify the exact live UI element/label used to confirm that AGVs are in the shutdown queue (e.g., which screen/field shows the queue state).
