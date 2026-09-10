# Verify Sorter Queue Routing: Entrance Queue → Queue Locations → Sorter Queue Locations → Exit Queue → Shutdown Queues

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_sorter_queue_routing_entrance_to_shutdown_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `robot_dwell_or_shutdown_staging` |
| Access Surface | `rms_ui`, `site_interview` |
| Audience Roles | `L1_support`, `operator` |
| Failure Pattern Tags | `sort_lifecycle_stuck`, `zone_agv_mismatch` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the live sorter layout view (via RMS / fleet status UI when available, or site visual confirmation) to verify that AGVs/totes follow the documented sorter queue routing sequence: entrance queue first, then exchange staging (queue locations), then sorter queue locations for tote pickup/aisle entry, then exit queue after exchange, and finally shutdown queue positioning based on tote presence (including the 'off the end' path when entering shutdown from the entrance with a tote).

## When To Use

When you need to confirm that sorter queue routing is behaving correctly during normal sorter flow and during shutdown entry, specifically validating the expected queue-to-queue transitions and tote-dependent shutdown positioning.

## Source Procedure References

- proc_verify_sorter_queue_routing_entrance_to_shutdown_v1

## Procedure Steps

### Step 1 — Identify the sorter queue areas in the live layout view

**Responsible role:** L1_support

**Instruction:**
In the live sorter layout view available to support (RMS / fleet status UI when available), identify the following queue areas: entrance queue; queue locations (exchange staging); sorter queue locations (tote pickup / aisle entry); exit queue; shutdown queues (including under-rack shutdown locations for AGVs without totes and the shutdown location for AGVs with totes). If the live layout does not clearly label these areas, use site interview / visual confirmation to map the live labels to these documented queue-area names.

**Expected result:**
You can point to (or otherwise map) each of the named queue areas in the live view: entrance queue, queue locations for exchange staging, sorter queue locations for tote pickup/aisle entry, exit queue, and shutdown queues with tote-dependent positioning.

---

### Step 2 — Confirm AGV/tote enters via the entrance queue first

**Responsible role:** L1_support

**Instruction:**
Observe an AGV/tote that is entering the sorter area in the live view and confirm it first appears in the entrance queue.

**Expected result:**
The observed AGV/tote appears first in the entrance queue (no bypass to later queue areas).

---

### Step 3 — Confirm transition from entrance queue to exchange staging (queue locations)

**Responsible role:** L1_support

**Instruction:**
After the entrance queue, confirm the same AGV/tote transitions to the queue locations area where AGVs stage behind for an exchange.

**Expected result:**
The observed AGV/tote moves from the entrance queue into the queue locations (exchange staging) area.

---

### Step 4 — Confirm tote pickup at sorter queue locations (aisle entry)

**Responsible role:** L1_support

**Instruction:**
Confirm that after exchange staging, the tote is picked up at the sorter queue locations (the area described as where you pick up the tote and leave into the aisle).

**Expected result:**
The observed item reaches the sorter queue locations area where tote pickup/aisle entry occurs.

---

### Step 5 — Confirm post-exchange routing to exit queue

**Responsible role:** L1_support

**Instruction:**
After an exchange, confirm the AGV/tote goes to the exit queue (described as where it goes as it leaves before it could go to anywhere else for shutdown).

**Expected result:**
The observed item transitions to the exit queue after exchange.

---

### Step 6 — Confirm shutdown queue positioning based on tote presence

**Responsible role:** L1_support

**Instruction:**
When the system is in shutdown, confirm shutdown queue positioning based on tote presence: observe AGVs without totes moving to shutdown locations under the rack, and observe AGVs with totes moving to the shutdown location described as “for AGVs with Tots.”

**Expected result:**
In shutdown, the observed AGV/tote ends up in the correct shutdown location corresponding to whether a tote is present.

---

### Step 7 — Confirm 'off the end' behavior when entering shutdown from the entrance with a tote

**Responsible role:** L1_support

**Instruction:**
If entering shutdown from the entrance while a tote is present, confirm the documented 'off the end' path occurs before the shutdown location (entrance → off the end → shutdown).

**Expected result:**
For a tote-present item entering shutdown from the entrance, the item is observed at the 'off the end' location before it reaches the shutdown location.

---

## Success Criteria

- An observed AGV/tote entering the sorter area appears first in the entrance queue.
- The same AGV/tote transitions from entrance queue to queue locations for exchange staging.
- After exchange staging, the tote is picked up at sorter queue locations (aisle entry).
- After exchange, the AGV/tote goes to the exit queue.
- During shutdown, AGVs without totes are positioned at under-rack shutdown locations and AGVs with totes are positioned at the tote-specific shutdown location.
- When entering shutdown from the entrance with a tote, the item follows entrance → off the end → shutdown.

## Failure Conditions

- AGV/tote bypasses the entrance queue.
- AGV/tote does not stage in queue locations for exchange before sorter queue pickup.
- Tote pickup/aisle entry does not occur at sorter queue locations after exchange staging.
- AGV/tote does not go to exit queue after exchange.
- Shutdown placement does not match tote presence (tote-present in under-rack locations or tote-absent in tote-specific location).
- Entering shutdown from entrance with tote skips the 'off the end' step.

## Escalation Guidance

- Escalate if any observed routing transition deviates from the documented sequence (entrance queue bypass, missing exchange staging, missing exit queue after exchange, incorrect shutdown placement by tote presence, or missing 'off the end' step when entering shutdown from entrance with a tote).
- If the live layout view does not clearly label queue areas, stop and use site interview / visual confirmation to map live labels to the documented queue names before continuing verification.

## Missing Details / Known Gaps

- The packet does not explicitly name the exact live RMS screen/widget where the queue-area labels (entrance queue, queue locations, sorter queue locations, exit queue, shutdown queues, and 'off the end') appear. The procedure therefore relies on RMS / fleet status UI availability and site interview / visual confirmation to map live labels to the documented queue names.
