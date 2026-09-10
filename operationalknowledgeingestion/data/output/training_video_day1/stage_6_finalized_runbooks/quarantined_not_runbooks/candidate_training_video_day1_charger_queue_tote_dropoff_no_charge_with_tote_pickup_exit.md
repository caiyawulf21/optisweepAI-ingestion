# Follow Charger entrance queue → tote drop-off → charge (no totes on AGV) → tote pickup → exit queue

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_follow_charger_entrance_queue_tote_dropoff_charge_tote_pickup_exit_v1` |
| Title | Follow Charger entrance queue → tote drop-off → charge (no totes on AGV) → tote pickup → exit queue |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery` |
| Access Surface | `physical_floor` |
| Audience Roles | `operator` |
| Failure Pattern Tags | `charging_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify the charger-area flow described in the source: an AGV enters via the charger entrance queue, drops off its tote at the charger tote locations before charging (the AGV “doesn't like to charge with totes on it”), then after charging completes it picks up its tote in a shutdown state and proceeds to its exit queue. For AGVs without totes, confirm they skip the tote pickup/drop-off behavior.

## When To Use

Use when you need to confirm that AGVs are following the expected charger-area tote-handling and charging sequence (drop tote before charging; do not charge with tote on the AGV; pick up tote after charging; then go to exit queue).

## Do Not Use For

* Do not use this procedure as a recovery playbook for charger faults; the source provides no recovery steps if the behavior is incorrect.

## Access Or Tools Needed

* Live visibility of AGV behavior at the charger area (entrance queue, tote drop-off locations, charging, tote pickup, exit queue)
* Source diagram/frame for charger module naming (charger, entrance queue, tote locations, exit queue)

## Related Operational Context

* ctx_training_video_charger_queue_and_tote_handling_v1

## Procedure Steps

### Step 1 — Identify the AGV’s charger entrance queue entry

**Responsible role:** operator

**Instruction:**
At the charger area, locate the AGV as it enters the charger entrance queue and confirm it is moving into the charger area as described in the source.

**Expected result:**
The AGV is observed entering the charger area via the charger entrance queue.

---

### Step 2 — Observe tote drop-off at charger tote locations before charging

**Responsible role:** operator

**Instruction:**
Watch the AGV at the charger tote locations and confirm it drops off its tote there before the charging period begins.

**Expected result:**
The AGV drops off its tote at the charger tote locations before charging.

**Stop or Escalate If:**

* If the AGV appears to begin charging while a tote is still on it, stop and escalate (the source states the AGV “doesn't like to charge with totes on it” and provides no recovery steps).

---

### Step 3 — Confirm charging occurs with no tote on the AGV

**Responsible role:** operator

**Instruction:**
During the charging period, confirm the tote is not on the AGV (the source states the AGV does not like to charge with totes on it).

**Expected result:**
The AGV charges while no tote is on the AGV.

**Stop or Escalate If:**

* If the AGV appears to charge with a tote still on it, stop and escalate; the source does not provide recovery steps.

---

### Step 4 — After charging completes, observe tote pickup in shutdown state

**Responsible role:** operator

**Instruction:**
After charging completes, observe the AGV as it goes to pick up its tote, noting that the source describes this as occurring in a shutdown state.

**Expected result:**
Once charging is done, the AGV goes to pick up its tote in a shutdown state.

---

### Step 5 — Observe AGV proceeds to its exit queue after picking up the tote

**Responsible role:** operator

**Instruction:**
After the AGV picks up its tote, observe it moving to the exit queue as described in the source.

**Expected result:**
The AGV goes to its exit queue after picking up the tote.

---

### Step 6 — For AGVs without totes, confirm they skip tote pickup/drop-off behavior

**Responsible role:** operator

**Instruction:**
Identify AGVs without totes and confirm they do not need to perform the tote pickup/drop-off behavior described for charging.

**Expected result:**
AGVs without totes skip the tote pickup/drop-off portion of the charger flow.

---

## Success Criteria

* An AGV follows the charger flow: entrance queue → tote drop-off at charger tote locations → charging with no tote on the AGV → tote pickup → exit queue.
* For AGVs without totes, the tote pickup/drop-off portion is skipped.

## Failure Conditions

* AGV appears to charge with a tote still on it.
* AGV does not drop off its tote at charger tote locations before charging (when it has a tote).
* AGV does not pick up its tote after charging completes (when a tote is expected).
* AGV does not proceed to the exit queue after tote pickup.

## Escalation Guidance

* If an AGV appears to charge with a tote still on it (contrary to the source statement), stop and escalate. The source provides no recovery steps.

## Missing Details / Known Gaps

* The source does not provide explicit live UI indicators or specific observable status fields for “charging” vs “shutdown state”; this runbook relies on physical/visual observation only.
* The source provides no recovery steps if the AGV charges with a tote on it or if the flow deviates.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_charger_queue_tote_dropoff_no_charge_with_tote_pickup_exit
- Source ID: `training_video_day1`
- Source Type: `training_video`
