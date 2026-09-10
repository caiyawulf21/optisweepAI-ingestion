# Verify Sorter Queue Flow: Entrance Queue → Queue Locations → Sorter Queue Locations → Exit Queue (and Shutdown Queues)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_sorter_queue_flow_entrance_to_exit_v1` |
| Title | Verify Sorter Queue Flow: Entrance Queue → Queue Locations → Sorter Queue Locations → Exit Queue (and Shutdown Queues) |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `sort_lifecycle_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `operator` |
| Failure Pattern Tags | `sort_lifecycle_stuck`, `site_stoppage` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented sorter queue layout to verify that AGVs/totes follow the expected queue sequence: entrance queue first, then queue locations for staging behind for an exchange, then sorter queue locations for tote pickup and leaving into the aisle, then exit queue after an exchange. Also verify shutdown queue destinations under the rack, including the tote-dependent split (AGVs without totes vs AGVs with totes) and the shutdown entry behavior (entrance during shutdown with a tote goes to “off the end” then shutdown).

## When To Use

When you need to understand or sanity-check where AGVs/totes should be staged and where they should go after an exchange, using the documented sorter queue layout and shutdown queue behavior.

## Do Not Use For

* Do not use this as a corrective procedure to change system routing or to perform AGV/tote removal/reassignment actions.

## Access Or Tools Needed

* Visual access to the sorter queue layout areas: entrance queue, queue locations, sorter queue locations, exit queue, shutdown queues (under the rack), and the “off the end” area.

## Related Operational Context

* ctx_training_video_sorter_queue_layout_v1
* ctx_training_video_shutdown_queue_locations_v1

## Procedure Steps

### Step 1 — Identify the sorter entrance queue area on the sorter layout

**Responsible role:** operator

**Instruction:**
On the sorter layout, locate the area labeled as the entrance queue.

**Expected result:**
You can point to the entrance queue area on the layout.

---

### Step 2 — Confirm the entrance queue rule (anything entering must go to entrance queue first)

**Responsible role:** operator

**Instruction:**
Using the documented rule, confirm that anything that wants to go into this sorter area must go to the entrance queue first.

**Expected result:**
You can state/confirm the rule: “anything that wants to go into this area must go to the entrance queue first.”

**Stop or Escalate If:**

* If observed movement does not align with the documented queue sequence (e.g., bypassing entrance queue), stop and escalate for support rather than guessing corrective actions.

---

### Step 3 — Locate the “queue locations” area used for AGVs staging behind for an exchange

**Responsible role:** operator

**Instruction:**
On the sorter layout, locate the area labeled “queue locations” and treat it as the staging area behind for an exchange.

**Expected result:**
You can identify the “queue locations” area and associate it with AGV staging behind for an exchange.

---

### Step 4 — Locate the “sorter queue locations” area where you pick up the tote and leave into the aisle

**Responsible role:** operator

**Instruction:**
On the sorter layout, locate the area labeled “sorter queue locations” and treat it as where you pick up the tote and leave into the aisle.

**Expected result:**
You can identify the “sorter queue locations” area and associate it with tote pickup and leaving into the aisle.

---

### Step 5 — After an exchange, confirm the next destination is the exit queue

**Responsible role:** operator

**Instruction:**
Using the documented rule, confirm that once you do an exchange, it must go to the exit queue (described as where it leaves before it could go to anywhere else it wants to go for shutdown).

**Expected result:**
You can confirm the rule: exchange → exit queue.

**Stop or Escalate If:**

* If observed movement does not align with the documented queue sequence (e.g., not going to exit queue after exchange), stop and escalate for support rather than guessing corrective actions.

---

### Step 6 — Locate the shutdown queues under the rack and identify the tote-dependent split (with totes vs without totes)

**Responsible role:** operator

**Instruction:**
On the sorter layout, locate the shutdown queues under the rack and identify the documented split: locations for AGVs without totes vs the location for AGVs with totes.

**Expected result:**
You can identify the under-rack shutdown locations and distinguish the tote/no-tote destinations.

---

### Step 7 — If entering during shutdown with a tote, follow the documented off-the-end then shutdown path

**Responsible role:** operator

**Instruction:**
If the system is in a shutdown state when entering the entrance and you have a tote, confirm the documented path: go to “off the end” and then go to the shutdown.

**Expected result:**
You can confirm the documented shutdown entry behavior for the tote-present case: entrance during shutdown + tote → off the end → shutdown.

**Stop or Escalate If:**

* If observed movement does not align with the documented queue sequence (including incorrect shutdown destination for tote vs no-tote), stop and escalate for support rather than guessing corrective actions.

---

## Success Criteria

* You can map observed/expected AGV/tote movement to the documented queue sequence: entrance queue first, then queue locations for staging behind for an exchange, then sorter queue locations for tote pickup and leaving into the aisle, then exit queue after an exchange.
* You can map shutdown behavior to the documented tote-dependent split under the rack (AGVs without totes vs AGVs with totes).
* For shutdown entry with a tote, you can confirm the documented off-the-end then shutdown path.

## Failure Conditions

* Observed movement bypasses the entrance queue rule.
* After an exchange, the AGV/tote does not go to the exit queue.
* During shutdown, AGVs with totes and without totes are sent to the wrong shutdown destinations under the rack.
* During shutdown entry with a tote, the AGV/tote does not follow the off-the-end then shutdown path.

## Escalation Guidance

* If observed movement does not align with the documented queue sequence (e.g., bypassing entrance queue, not going to exit queue after exchange, or incorrect shutdown destination for tote vs no-tote), stop and escalate for support rather than guessing corrective actions.

## Missing Details / Known Gaps

* The packet does not provide live UI labels/controls (e.g., exact RMS screen names or clickable elements) for locating these queue areas during an active system check; it only provides the documented layout frame and transcript.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_sorter_queue_entrance_to_exit
- Source ID: `training_video_day1`
- Source Type: `training_video`
