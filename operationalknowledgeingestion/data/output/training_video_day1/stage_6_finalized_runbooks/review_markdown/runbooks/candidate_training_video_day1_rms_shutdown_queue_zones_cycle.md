# Check RMS fleet status for AGVs in shutdown queues and zone cycling

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1` |
| Title | Check RMS fleet status for AGVs in shutdown queues and zone cycling |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | `L2_support` |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RMS / fleet status UI to verify that AGVs are held in shutdown queues (shutdown state), then cycle into their assigned zones (4 zones) after startup, consistent with the system state model described in the segment.

## When To Use

When you need to confirm that AGVs are in the shutdown state (shutdown queues) and then transition into their assigned zones (4 zones) after startup, using the live fleet status view in RMS.

## Access Or Tools Needed

* RMS / fleet status UI (rms_ui)

## Related Operational Context

* ctx_training_video_shutdown_queue_reference_v1
* ctx_training_video_system_state_model_v1

## Visual References

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Training video frame segment (timestamp ~00:47:36.500) containing the shutdown queues → cycle → 4 zones explanation and the mention of AGVs cycling through charging while in shutdown logic.*

## Procedure Steps

### Step 1 — Open RMS / fleet status UI and view AGV roster/map

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV list/map view where you can see each AGV’s current state and/or location/zone assignment.

**Expected result:**
You can see the AGV list/map view in RMS with each AGV’s current state and/or location/zone assignment visible.

**Stop or Escalate If:**

* RMS fleet status UI is not accessible or does not show AGV state/location/zone fields needed for the check.

---

### Step 2 — Confirm AGVs are in shutdown queues (shutdown state)

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV list/map view, identify the relevant AGVs and confirm that their current state and/or location/zone assignment corresponds to shutdown queues (shutdown state), not idle/running zones.

**Expected result:**
AGVs that should be in shutdown are displayed in a shutdown queues/shutdown state condition in RMS (observable via their state and/or location/zone assignment).

**Stop or Escalate If:**

* AGVs are not shown in shutdown queues/shutdown state when shutdown is expected.

---

### Step 3 — Observe transition from shutdown queues into assigned zones (4 zones)

**Responsible role:** L1_support

**Instruction:**
Observe the AGVs in RMS over the expected startup transition window and confirm they move from shutdown queues into their assigned zones. The segment references 4 zones.

**Expected result:**
AGVs transition from shutdown queues/shutdown state into their assigned zones (4 zones referenced in the segment).

**Stop or Escalate If:**

* AGVs remain in shutdown queues/shutdown state without transitioning into their zones when the system is expected to be starting up.

---

### Step 4 — If tipper/hospital scenario is active, confirm shutdown/startup cycle still holds

**Responsible role:** L1_support

**Instruction:**
If the segment’s scenario is active (tipper issue leading to hospital/reject handling), confirm in RMS that AGVs still follow the shutdown/startup cycle model: shutdown queues → assigned zones, rather than remaining stuck in shutdown queues.

**Expected result:**
Even during the tipper/hospital scenario, AGVs still transition from shutdown queues into their assigned zones in RMS.

**Stop or Escalate If:**

* AGVs remain in shutdown queues/shutdown state without transitioning into their zones during the scenario.

---

## Success Criteria

* In RMS, AGVs expected to be in shutdown are shown in shutdown queues/shutdown state.
* After startup, those AGVs transition from shutdown queues into their assigned zones (4 zones referenced).
* During any tipper/hospital scenario, AGVs still follow shutdown queues → zones behavior rather than remaining stuck in shutdown.

## Failure Conditions

* AGVs remain in shutdown queues/shutdown state without transitioning into their assigned zones when startup is expected.
* RMS shows AGVs in non-shutdown zone assignments during a shutdown period.

## Escalation Guidance

* Escalate if AGVs remain in shutdown queues/shutdown state without transitioning into their zones when the system is expected to be starting up.
* Escalate if RMS shows inconsistent state/location (e.g., AGVs not in shutdown queues during a shutdown period, or not entering zones after startup).

## Missing Details / Known Gaps

* The packet does not provide the exact RMS UI field/label mapping for “shutdown queues” (e.g., which specific state name or zone/location label in RMS corresponds to shutdown queues). This must be confirmed on the live RMS UI during execution.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_rms_shutdown_queue_zones_cycle
- Source ID: `training_video_day1`
- Source Type: `training_video`
