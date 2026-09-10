# Check Operational State Transitions: Running ↔ Bag Out/Close Out, Then Shutdown (State Model)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_operational_state_transitions_running_bagout_closeout_then_shutdown_state_model_v1` |
| Title | Check Operational State Transitions: Running ↔ Bag Out/Close Out, Then Shutdown (State Model) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that the live system follows the operational state model: after bag out/close out completes, the system automatically returns to the running state; chutes are closed during the close/bag-out phase; and shutdown is the last state chosen from the Viva HMI (not an automatic end-of-bag-out behavior).

## When To Use

Use when you need to confirm that the system’s operational state transitions match the expected cycle after bag out/close out, and that shutdown is only entered when selected from the HMI.

## Do Not Use For

* Do not use this procedure as a remediation guide for specific state-transition failures; the source does not provide corrective actions beyond escalation.

## Access Or Tools Needed

* Viva HMI (used to put the system into shutdown)
* Any live system view used to observe current state (exact UI elements not named in the source)

## Related Operational Context

* ctx_training_video_system_state_model_v1
* ctx_training_video_post_bagout_running_state_v1
* ctx_training_video_hmi_shutdown_selection_v1

## Procedure Steps

### Step 1 — Identify the current system state (running vs bagging out vs close out)

**Responsible role:** L1_support

**Instruction:**
On the live system view (Viva HMI or other live state indicator available to you), determine whether the system is currently in one of the main states described: “running,” “bagging out,” or “close out.”

**Expected result:**
You can classify the current system state as running, bagging out, or close out based on the live state indicator you are viewing.

---

### Step 2 — Verify the close out / bag out transition back to running

**Responsible role:** L1_support

**Instruction:**
If the system is in bagging out or close out, observe the transition after completion and confirm that it returns to the running state automatically.

**Expected result:**
After bag out/close out completes, the system returns to the running state automatically.

**Stop or Escalate If:**

* Stop and escalate if the system does not return to running after bag out/close out as described.

---

### Step 3 — Confirm chute condition concept during close/bag-out and running-to-close/bag-out behavior

**Responsible role:** L1_support

**Instruction:**
During the close out/bag out phase, confirm the chute condition concept described: “the chutes are closed.” Also confirm that the system can go from running to close or bag out and then returns to running afterward.

**Expected result:**
Chutes are closed during close/bag-out, and the system transitions running → close/bag out → running afterward.

**Stop or Escalate If:**

* Stop and escalate if the observed behavior does not match the described running ↔ close/bag-out ↔ running behavior.

---

### Step 4 — Confirm shutdown is selected from the HMI and is the last state

**Responsible role:** L1_support

**Instruction:**
If shutdown is observed, verify it aligns with the rule that shutdown is something you choose from the HMI (Viva HMI) and is the last state shutdown.

**Expected result:**
Shutdown is entered only after an HMI selection (Viva HMI), and it appears as the last state in the cycle.

**Stop or Escalate If:**

* Stop and escalate if shutdown appears without the described HMI selection.

---

## Success Criteria

* Observed state transitions match the model: running → bag out/close out → running automatically after bag out/close out completes.
* Chutes are closed during the close/bag-out phase conceptually as described.
* Shutdown is only entered as a chosen last state from the Viva HMI (not automatically at end of bag out).

## Failure Conditions

* System does not return to running after bag out/close out.
* Running → close/bag-out → running sequence does not occur as described.
* Shutdown appears without the described HMI selection behavior.

## Escalation Guidance

* Escalate if state transitions do not follow the described running/bag out/close out/shutdown behavior. The source does not provide remediation steps.

## Missing Details / Known Gaps

* The source does not name specific Viva HMI screen/control labels or exact state indicator field names for “running,” “bagging out,” “close out,” and “shutdown.”
* The source does not provide specific corrective actions if transitions fail; it only provides expected behavior and escalation guidance.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_operational_state_model_running_bag_out_close_out_shutdown
- Source ID: `training_video_day1`
- Source Type: `training_video`
