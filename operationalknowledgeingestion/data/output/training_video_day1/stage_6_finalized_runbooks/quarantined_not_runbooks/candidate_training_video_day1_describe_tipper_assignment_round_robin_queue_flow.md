# Describe the tipper assignment and entrance-queue flow for a full tote (round-robin to enabled tippers)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_describe_tipper_assignment_entrance_queue_round_robin_v1` |
| Title | Describe the tipper assignment and entrance-queue flow for a full tote (round-robin to enabled tippers) |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When a full tote on an AGV reaches the sorter, Execute assigns a specific tipper using round-robin among available enabled tippers serviced by the relevant queue. The AGV is then routed to the tipper entrance queue; when the AGV reaches the front of that entrance queue and the tipper becomes available, the AGV is sent to the tipper for the tip/clamp cycle.

## When To Use

Use this procedure to explain (and communicate) the tote-to-tipper assignment and entrance-queue gating behavior for a full tote on an AGV: round-robin selection among available enabled tippers serviced by the queue, followed by entrance-queue waiting until the tipper is available.

## Access Or Tools Needed

* Training video segment transcript (00:28:37.000 to 00:32:10.000) for tipper assignment and queueing rules

## Related Operational Context

* ctx_training_video_tipper_assignment_and_queueing_v1

## Procedure Steps

### Step 1 — Use the full-tote-to-sorter starting point

**Responsible role:** L1_support

**Instruction:**
Identify the scenario as: a full tote sits in the aisle on an AGV and reaches the sorter.

**Expected result:**
You can describe the flow starting from the moment the full tote reaches the sorter (not from a later stage such as tipper completion).

---

### Step 2 — Identify the tipper assignment step (Execute assigns a specific tipper)

**Responsible role:** L1_support

**Instruction:**
Explain that when the AGV reaches the sorter, Execute assigns a specific tipper.

**Expected result:**
Your explanation states that Execute assigns a specific tipper at the sorter arrival point.

---

### Step 3 — Apply the selection rule (round-robin among available enabled tippers serviced by this queue)

**Responsible role:** L1_support

**Instruction:**
Explain that the tipper selection uses round-robin to available enabled tippers serviced by this queue.

**Expected result:**
You can state: round-robin selection among available enabled tippers serviced by the queue.

---

### Step 4 — Apply the queueing rule (send AGV to the tipper entrance queue)

**Responsible role:** L1_support

**Instruction:**
Explain that after Execute assigns the tipper, the AGV is sent to the tipper entrance queue.

**Expected result:**
Your explanation states that the AGV is sent to the tipper entrance queue after tipper assignment.

---

### Step 5 — Apply entrance-queue gating (front of entrance queue + tipper availability -> send to tipper)

**Responsible role:** L1_support

**Instruction:**
Explain that when the AGV reaches the front of the tipper entrance queue and the tipper becomes available, the AGV is sent to the tipper.

**Expected result:**
You can state the gating condition: front-of-entrance-queue AND tipper availability triggers sending the AGV to the tipper.

---

## Success Criteria

* You can accurately explain the full-tote flow: Execute assigns a specific tipper using round-robin among available enabled tippers serviced by the queue, then routes the AGV to the tipper entrance queue.
* You can accurately explain the entrance-queue release condition: when the AGV reaches the front of the tipper entrance queue and the tipper becomes available, the AGV is sent to the tipper.

## Failure Conditions

* Explanation contradicts the round-robin/availability mechanism (e.g., claims a fixed tipper or ignores enabled/available constraints).
* Explanation omits the entrance-queue gating step or replaces it with a direct routing to the tipper.

## Escalation Guidance

* If observed tipper assignment behavior contradicts the round-robin/availability explanation, escalate for deeper system evidence beyond this training segment.

## Missing Details / Known Gaps

* No live operational verification steps are provided in the packet; this runbook is limited to explaining the described flow mechanism.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_describe_tipper_assignment_round_robin_queue_flow
- Source ID: `training_video_day1`
- Source Type: `training_video`
