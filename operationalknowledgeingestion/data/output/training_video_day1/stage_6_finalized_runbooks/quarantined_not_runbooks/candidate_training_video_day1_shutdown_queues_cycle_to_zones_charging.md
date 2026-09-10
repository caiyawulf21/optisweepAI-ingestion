# Explain/Verify Shutdown Queues Behavior: AGVs in Shutdown State Cycle to Charge, Then Move to Zones

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_explain_verify_shutdown_queues_behavior_agvs_cycle_to_charge_then_zones_v1` |
| Title | Explain/Verify Shutdown Queues Behavior: AGVs in Shutdown State Cycle to Charge, Then Move to Zones |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `gateway_health` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `shutdown_or_dwell_abnormal`, `charging_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Geek+ RMS walkthrough to confirm that when the system is in the AGV shutdown state, AGVs remain in shutdown logic, cycle through charging, and then—on startup—move into their assigned zones (4 zones referenced).

## When To Use

When you need to interpret/verify the expected AGV behavior during the system shutdown state: AGVs sit in shutdown queues, cycle through charging, and then move into their assigned zones when the system starts up.

## Access Or Tools Needed

* Geek+ RMS walkthrough view (RMS web page used in the segment)
* Any live view used in the RMS walkthrough to observe AGV state/zone assignment (exact UI elements not named in the source)

## Related Operational Context

* ctx_training_video_shutdown_queue_reference_v1

## Procedure Steps

### Step 1 — Identify the system state being discussed as “shutdown state” (not actively sorting parcels)

**Responsible role:** L1_support

**Instruction:**
On the Geek+ RMS walkthrough view, confirm you are validating behavior for the shutdown state (described as when the system is not actively sorting parcels and is in a transition between two sorts).

**Expected result:**
You are observing/validating AGV behavior that corresponds to the shutdown state (not the running/bagging-out/close-out sorting phases).

---

### Step 2 — Verify the meaning of “shutdown queues” as the holding location for AGVs in shutdown state

**Responsible role:** L1_support

**Instruction:**
Using the Geek+ RMS walkthrough view, verify that “shutdown queues” correspond to the holding location for AGVs while they are in shutdown state.

**Expected result:**
Shutdown queues are confirmed as the location where AGVs sit when they are shut down.

---

### Step 3 — Observe/confirm shutdown logic: AGVs stay in shutdown logic and cycle through each AGV to charge

**Responsible role:** L1_support

**Instruction:**
On the Geek+ RMS walkthrough view, observe that AGVs remain in shutdown logic and cycle through each AGV to charge them while in shutdown queues/shutdown state.

**Expected result:**
AGVs remain in shutdown logic and you observe them cycling for charging (described as cycling through each of the AGVs to charge them).

**Stop or Escalate If:**

* AGVs do not appear to remain in shutdown queues/shutdown logic during shutdown state
* AGVs do not cycle through charging while in shutdown state

---

### Step 4 — Check startup behavior: AGVs move from shutdown queues into their own zones (4 zones referenced)

**Responsible role:** L1_support

**Instruction:**
On the Geek+ RMS walkthrough view, after startup, confirm that AGVs move from shutdown queues into their assigned zones. Note that the segment references 4 zones.

**Expected result:**
AGVs move from shutdown queues into their own zones after startup; 4 zones are referenced in the segment.

**Stop or Escalate If:**

* After startup, AGVs do not move into their assigned zones

---

## Success Criteria

* Shutdown queues are confirmed as the holding location for AGVs in shutdown state
* While in shutdown state, AGVs remain in shutdown logic and cycle through charging
* On startup, AGVs move from shutdown queues into their assigned zones (4 zones referenced)

## Failure Conditions

* AGVs do not remain in shutdown queues/shutdown logic during shutdown state
* AGVs do not cycle through charging while in shutdown state
* After startup, AGVs do not move into their assigned zones

## Escalation Guidance

* Escalate if observed behavior does not match the described shutdown-queue charging cycle and zone movement; the source provides definitions but no specific corrective actions.

## Missing Details / Known Gaps

* The source does not name specific Geek+ RMS screen/field labels to directly confirm “shutdown queues,” “charging cycle,” or “zone assignment.” Steps therefore rely on observable behavior described in the segment.
* The source does not provide corrective actions if behavior does not match; escalation guidance is limited to raising the mismatch.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_shutdown_queues_cycle_to_zones_charging
- Source ID: `training_video_day1`
- Source Type: `training_video`
