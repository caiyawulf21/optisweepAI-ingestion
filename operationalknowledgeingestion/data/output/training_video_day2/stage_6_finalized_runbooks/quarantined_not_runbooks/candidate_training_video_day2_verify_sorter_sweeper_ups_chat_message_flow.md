# Verify Sorter Sweeper UPS chat message flow for tote induction, sorting, closeout, and label printing

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_sorter_sweeper_ups_chat_message_flow_v1` |
| Title | Verify Sorter Sweeper UPS chat message flow for tote induction, sorting, closeout, and label printing |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness`, `gateway_health`, `sorter_item_or_scan_state` |
| Access Surface | `stunnel`, `wcs_api`, `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy`, `system_fault` |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

Remote diagnostic to confirm the UPS-facing chat message sequence used by the Sorter Sweeper orchestration (tote inducted → destination enabled → scan data collection → sort → sort confirmation/final destination → hot bin closeout exchange when applicable → destination close before exchange → print label message). Use the missing/absent message stage as the evidence point for escalation to the responsible module (Sorter Sweeper vs XLE COM vs UPS chat integration).

## When To Use

Use when you need to verify that the documented UPS chat message flow for tote processing at the sorter is occurring in the expected order and that the Sorter Sweeper orchestration is acting on each stage (including closeout and label printing).

## Do Not Use For

* Do not use this procedure as a corrective runbook to change message mappings or implement new integrations; it is diagnostic and relies on observing the presence/absence of the documented message stages.

## Access Or Tools Needed

* Access to the UPS chat message integration surface used by Sorter Sweeper / XLE COM (exact UI/logging surface not specified in the source).
* Ability to observe message presence for: tote inducted, destination enabled, scan data (scan tunnel), sort (XLE/UPS version of WCS), sort confirmation, hot bin closeout (hot bin message), sure post notification, destination close, and print label message.

## Related Operational Context

* ctx_training_video_sorter_sweeper_system_overview_v1
* ctx_training_video_ups_chat_message_flow_v1

## Visual References

![artifact_training_video_training_video_day2_0004_so_sorter_sweeper_module_orchestrates_the_primary_00_05_52_500](assets/ad817609844d3adb.jpg)

*Diagram/frame describing the Sorter Sweeper orchestration and the UPS chat message flow stages (tote inducted, destination enabled, scan data, sort, sort confirmation, hot bin closeout, sure post, destination close, print label).*

## Procedure Steps

### Step 1 — Confirm Sorter Sweeper orchestration and its communication path to UPS chat

**Responsible role:** L2_support

**Instruction:**
On the live system, use the known architecture to anchor where the UPS chat messages originate/are handled: Sorter Sweeper (tote state machine) orchestrates tote movement; XLE COM manages communication between Sorter Sweeper and the UPS chat server; OPC COM manages communication between the robotics module and Geek Plus RMS server.

**Expected result:**
You can map each observed message stage to the described path: Sorter Sweeper sends/receives via XLE COM to the UPS chat server, and Sorter Sweeper updates tote state based on received UPS chat messages (including scan data and sort confirmation).

**Stop or Escalate If:**

* If you cannot observe any UPS chat message exchange at all, stop and escalate for deeper system-side investigation of the Sorter Sweeper ↔ XLE COM ↔ UPS chat integration.

---

### Step 2 — Validate tote arrival triggers “tote inducted” and “destination enabled” messages to chat

**Responsible role:** L2_support

**Instruction:**
Trigger/observe a tote arrival at the sorter and verify that Sorter Sweeper sends a “tote inducted” message and a “destination enabled” message to the UPS chat server.

**Expected result:**
For the observed tote arrival, both “tote inducted” and “destination enabled” messages appear in the UPS chat message exchange as described.

**Stop or Escalate If:**

* If “tote inducted” and/or “destination enabled” are missing for the tote arrival, stop and escalate for deeper system-side investigation of the responsible module (Sorter Sweeper vs XLE COM vs UPS chat integration).

---

### Step 3 — Verify scan data collection from scan tunnel and parcel dimensions/load category

**Responsible role:** L2_support

**Instruction:**
During the same tote processing window, verify that scan data from the scan tunnel is received/listened to on the chat and that parcel dimensions and load category are collected.

**Expected result:**
Scan data is present and parcel dimensions and load category are collected for the parcel/tote being processed.

**Stop or Escalate If:**

* If scan data (or the derived dimensions/load category collection) is missing, stop and escalate for deeper system-side investigation of the scan data → chat integration and/or Sorter Sweeper handling.

---

### Step 4 — Verify “sort” is sent from XLE (UPS version of WCS) and destinations are collected

**Responsible role:** L2_support

**Instruction:**
Observe the sort stage for the parcel/tote and verify that “sort” is sent from XLE (described as the UPS version of WCS) onto the chat, and that possible destinations are collected for each parcel.

**Expected result:**
A “sort” exchange occurs on the chat and possible destinations for the parcel are collected.

**Stop or Escalate If:**

* If “sort” is missing or possible destinations are not collected, stop and escalate for deeper system-side investigation of the XLE COM / UPS chat sort integration.

---

### Step 5 — Verify “sort confirmation” is received/sent and final destination is determined

**Responsible role:** L2_support

**Instruction:**
Observe the chat exchange for the parcel/tote and verify that a “sort confirmation” is received/sent from the sorter onto the chat and that the final destination is determined.

**Expected result:**
A “sort confirmation” stage is present in the chat exchange and the final destination for the parcel is determined.

**Stop or Escalate If:**

* If “sort confirmation” is missing or final destination is not determined, stop and escalate for deeper system-side investigation of Sorter Sweeper’s confirmation handling and/or XLE COM chat integration.

---

### Step 6 — If closeout is involved, verify hot bin closeout via “hot bin message” and immediate exchange

**Responsible role:** L2_support

**Instruction:**
For totes that are expected to be “hot bin,” verify that UPS can trigger a hot bin closeout by sending a “hot bin message,” and that an exchange is performed immediately as described.

**Expected result:**
When a tote is “hot bin,” a “hot bin message” is observed and the exchange occurs immediately.

**Stop or Escalate If:**

* If hot bin closeout is missing for hot bin totes (no “hot bin message” and/or no immediate exchange), stop and escalate for deeper system-side investigation of the closeout trigger handling.

---

### Step 7 — Verify “sure post” notification and tipper bag switching notification before the tip

**Responsible role:** L2_support

**Instruction:**
Observe the chat exchange for the destination load status and verify that UPS notifies when the load for a destination is a “sure post,” and that the system notifies the tipper before the tip so they can switch out the bag to a Poly bag.

**Expected result:**
A “sure post” notification is observed for the destination load, and the tipper is notified before the tip (enabling the poly bag switch).

**Stop or Escalate If:**

* If “sure post” notification is missing or tipper pre-tip notification is missing, stop and escalate for deeper system-side investigation of the sure post handling and tipper notification path.

---

### Step 8 — Verify “destination close” message is sent before exchange when tote is ready to leave

**Responsible role:** L2_support

**Instruction:**
When the tote is ready to leave for the exchange, verify that a “destination close” message is sent onto the chat before the exchange.

**Expected result:**
For the tote ready to leave, “destination close” appears on the chat before the exchange occurs.

**Stop or Escalate If:**

* If “destination close” is missing or not ordered before exchange, stop and escalate for deeper system-side investigation of the destination close stage handling.

---

### Step 9 — Verify “print label message” is sent to the printer at the tipper

**Responsible role:** L2_support

**Instruction:**
At the tipper stage for the processed tote, verify that a “print label message” is sent to the printer so it can print a label provided by XLE.

**Expected result:**
A “print label message” is observed being sent to the printer for the tote at the tipper stage.

**Stop or Escalate If:**

* If “print label message” is missing, stop and escalate for deeper system-side investigation of the label printing trigger path (Sorter Sweeper ↔ XLE COM ↔ printer integration).

---

## Success Criteria

* For a tote processing cycle, the documented UPS chat message stages are observed in order: tote inducted + destination enabled → scan data collection (dimensions/load category) → sort (XLE/UPS version of WCS) → sort confirmation/final destination → (if applicable) hot bin closeout via hot bin message with immediate exchange → destination close before exchange → print label message to printer.

## Failure Conditions

* Missing “tote inducted” and/or “destination enabled” after tote arrival.
* Missing scan data collection (dimensions/load category not collected).
* Missing “sort” stage and/or missing possible destinations collection.
* Missing “sort confirmation” and/or final destination determination.
* Missing hot bin closeout trigger (“hot bin message”) and/or exchange not performed immediately for hot bin totes.
* Missing “sure post” notification and/or tipper not notified before the tip.
* Missing “destination close” before exchange.
* Missing “print label message” to the printer at the tipper stage.

## Escalation Guidance

* If one or more documented message types are missing (e.g., no destination enabled after tote inducted, no sort confirmation, no destination close before exchange, or no print label message), stop and escalate for deeper system-side investigation of the responsible module (Sorter Sweeper vs XLE COM vs UPS chat integration).
* Use the first missing/inaction message stage as the evidence point for escalation; do not assume corrective actions not described in the segment.

## Missing Details / Known Gaps

* The source does not specify the exact live UI/logging surface where UPS chat messages (tote inducted, destination enabled, sort, sort confirmation, hot bin message, destination close, print label message) can be observed. This runbook therefore describes what to verify but cannot name a specific SSMS table, Helix DB view, or chat log screen.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_verify_sorter_sweeper_ups_chat_message_flow
- Source ID: `training_video_day2`
- Source Type: `training_video`
