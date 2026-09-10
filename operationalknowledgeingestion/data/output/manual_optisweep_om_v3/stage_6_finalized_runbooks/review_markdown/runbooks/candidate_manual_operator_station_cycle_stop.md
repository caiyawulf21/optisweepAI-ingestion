# Stop the Operator Station using the CYCLE STOP button on the Operator Station Main Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_operator_station_cycle_stop_v1` |
| Title | Stop the Operator Station using the CYCLE STOP button on the Operator Station Main Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

An operator can stop the operator station by pressing the CYCLE STOP button on the operator station main screen.

## When To Use

Use when you need to stop the operator station cycle from the operator station main screen by pressing the CYCLE STOP control.

## Access Or Tools Needed

* tipper_hmi

## Related Operational Context

* ctx_manual_operator_station_stop_v1
* ctx_manual_operator_station_hmi_cycle_stop_v1

## Visual References

![artifact_page_82_image_2](assets/b2001df0f17c2fc8.jpeg)

*Operator station main screen showing the CYCLE STOP button (used for stopping the operator station).*

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

**Stop or Escalate If:**

* If pressing CYCLE STOP does not stop the operator station, stop further operation and escalate to support.

---

### Step 3 — Verify the operator station is stopped

**Responsible role:** operator

**Instruction:**
Observe the operator station after pressing CYCLE STOP to confirm it is stopped.

**Expected result:**
The operator station is stopped (the cycle is no longer running after pressing CYCLE STOP).

**Stop or Escalate If:**

* If the operator station does not stop, stop further operation and escalate to support.

---

## Success Criteria

* After pressing CYCLE STOP on the operator station main screen, the operator station stops and the cycle no longer runs.

## Failure Conditions

* CYCLE STOP does not stop the operator station cycle.

## Escalation Guidance

* If pressing CYCLE STOP does not stop the operator station, stop further operation and escalate to support.

## Source Lineage

- Candidate IDs: candidate_manual_operator_station_cycle_stop
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
