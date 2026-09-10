# Check RMS fleet status for AGVs in shutdown queues and zone cycling

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI to verify that AGVs are held in shutdown queues (shutdown state), then cycle into their assigned zones (4 zones) after startup, consistent with the system state model described in the segment.

## When To Use

When you need to confirm that AGVs are in the shutdown state (shutdown queues) and then transition into their assigned zones (4 zones) after startup, using the live fleet status view in RMS.

## Source Procedure References

- proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1

## Procedure Steps

### Step 1 — Open RMS / fleet status UI and view AGV roster/map

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV list/map view where you can see each AGV’s current state and/or location/zone assignment.

**Expected result:**
You can see the AGV list/map view in RMS with each AGV’s current state and/or location/zone assignment visible.

---

### Step 2 — Confirm AGVs are in shutdown queues (shutdown state)

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV list/map view, identify the relevant AGVs and confirm that their current state and/or location/zone assignment corresponds to shutdown queues (shutdown state), not idle/running zones.

**Expected result:**
AGVs that should be in shutdown are displayed in a shutdown queues/shutdown state condition in RMS (observable via their state and/or location/zone assignment).

---

### Step 3 — Observe transition from shutdown queues into assigned zones (4 zones)

**Responsible role:** L1_support

**Instruction:**
Observe the AGVs in RMS over the expected startup transition window and confirm they move from shutdown queues into their assigned zones. The segment references 4 zones.

**Expected result:**
AGVs transition from shutdown queues/shutdown state into their assigned zones (4 zones referenced in the segment).

---

### Step 4 — If tipper/hospital scenario is active, confirm shutdown/startup cycle still holds

**Responsible role:** L1_support

**Instruction:**
If the segment’s scenario is active (tipper issue leading to hospital/reject handling), confirm in RMS that AGVs still follow the shutdown/startup cycle model: shutdown queues → assigned zones, rather than remaining stuck in shutdown queues.

**Expected result:**
Even during the tipper/hospital scenario, AGVs still transition from shutdown queues into their assigned zones in RMS.

---

## Success Criteria

- In RMS, AGVs expected to be in shutdown are shown in shutdown queues/shutdown state.
- After startup, those AGVs transition from shutdown queues into their assigned zones (4 zones referenced).
- During any tipper/hospital scenario, AGVs still follow shutdown queues → zones behavior rather than remaining stuck in shutdown.

## Failure Conditions

- AGVs remain in shutdown queues/shutdown state without transitioning into their assigned zones when startup is expected.
- RMS shows AGVs in non-shutdown zone assignments during a shutdown period.

## Escalation Guidance

- Escalate if AGVs remain in shutdown queues/shutdown state without transitioning into their zones when the system is expected to be starting up.
- Escalate if RMS shows inconsistent state/location (e.g., AGVs not in shutdown queues during a shutdown period, or not entering zones after startup).

## Missing Details / Known Gaps

- The packet does not provide the exact RMS UI field/label mapping for “shutdown queues” (e.g., which specific state name or zone/location label in RMS corresponds to shutdown queues). This must be confirmed on the live RMS UI during execution.
