# Verify OPC COM tag subscription/update behavior between Ignition, OPC server, and Sorter Sweeper (hospital/tippers tags)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_opc_com_tag_subscription_update_behavior_between_ignition_opc_server_and_sorter_sweeper_v1` |
| Title | Verify OPC COM tag subscription/update behavior between Ignition, OPC server, and Sorter Sweeper (hospital/tippers tags) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Validate the tag-based communication loop described in the source segment: Ignition’s built-in tag provider connects to hospital and tippers tags; the OPC communication module connects to the OPC server and subscribes to tags; when a tag updates, the update is forwarded to Sorter Sweeper for processing; Sorter Sweeper sends data back to the OPC communication module, which writes to the OPC server; and the tag provider reflects the updated data back to the system.

## When To Use

Use when you need to confirm that the OPC COM tag subscription/update loop is functioning end-to-end between Ignition’s tag provider, the OPC server, the OPC communication module (OPC COM), and Sorter Sweeper, specifically for hospital and tippers tag behavior.

## Access Or Tools Needed

* Access to the OPC COM module runtime/logging or an equivalent way to observe tag update propagation (the source does not specify the exact tool).
* Access to Ignition tag provider behavior for hospital/tippers tags (the source does not specify the exact Ignition screen).
* OPC server connectivity/visibility (the source does not specify the exact method).

## Related Operational Context

* ctx_training_video_opc_com_tag_flow_v1

## Visual References

![artifact_training_video_training_video_day2_0004_so_sorter_sweeper_module_orchestrates_the_primary_00_05_52_500](assets/ad817609844d3adb.jpg)

*Segment frame describing the OPC COM / Ignition tag provider / OPC server subscription and the forwarding of tag updates to Sorter Sweeper, plus write-back to the OPC server.*

## Procedure Steps

### Step 1 — Confirm the described components and tag flow boundaries (Ignition tag provider ↔ hospital/tippers ↔ OPC COM ↔ OPC server ↔ Sorter Sweeper)

**Responsible role:** L2_support

**Instruction:**
Using the source-described architecture, confirm you are validating: (1) Ignition’s built-in tag provider connecting to the hospital and tippers relaying relevant tags, (2) the OPC communication module connecting to the OPC server and subscribing to tags, (3) tag updates being forwarded to Sorter Sweeper for processing, and (4) Sorter Sweeper sending messages back to the OPC communication module, which writes data to the OPC server via the tag provider.

**Expected result:**
You can identify the loop endpoints as: Ignition tag provider (hospital/tippers tags) → OPC communication module (OPC server subscriptions) → Sorter Sweeper (processing on tag update) → OPC communication module (writes back to OPC server) → tag provider reflects updated data back to the system.

---

### Step 2 — Verify OPC communication module subscribes to OPC server tags

**Responsible role:** L2_support

**Instruction:**
Check that the OPC communication module is connected to the OPC server and has active tag subscriptions for the relevant tags (hospital/tippers tags as described). Use the available OPC COM runtime/logging or equivalent observation method in your environment (the source does not specify the exact tool).

**Expected result:**
OPC COM is connected to the OPC server and is subscribed to tags such that tag updates can be received and forwarded.

**Stop or Escalate If:**

* If you cannot confirm OPC COM connectivity/subscription evidence, stop and escalate for deeper OPC COM/OPC server troubleshooting (the source provides no remediation steps).

---

### Step 3 — Verify tag updates propagate from OPC COM subscriptions to Sorter Sweeper processing

**Responsible role:** L2_support

**Instruction:**
Trigger or observe a tag update on the OPC server side (for the relevant hospital/tippers tags) and confirm that the update is sent to the Sorter Sweeper module for processing. Use your available observation method for Sorter Sweeper processing behavior (the source does not specify the exact UI/log/DB to check).

**Expected result:**
When a tag is updated, Sorter Sweeper receives the update for processing.

**Stop or Escalate If:**

* If tag updates are not reaching Sorter Sweeper, stop and escalate for deeper OPC COM/OPC server/Tag provider troubleshooting (the segment does not provide specific remediation steps).

---

### Step 4 — Verify Sorter Sweeper writes back through OPC COM to the OPC server

**Responsible role:** L2_support

**Instruction:**
After confirming Sorter Sweeper processes the tag update, verify that Sorter Sweeper sends messages to the OPC communication module and that OPC communication module writes the data to the OPC server.

**Expected result:**
Sorter Sweeper outputs result in OPC COM writing data back to the OPC server.

**Stop or Escalate If:**

* If Sorter Sweeper outputs are not being written back to the OPC server, stop and escalate for deeper OPC COM/OPC server/Tag provider troubleshooting (the segment does not provide specific remediation steps).

---

### Step 5 — Confirm tag provider reflects updated data back through the loop (Ignition tag provider gets back updated data)

**Responsible role:** L2_support

**Instruction:**
Using the described loop, confirm that after OPC COM writes data to the OPC server, the tag provider gets back the updated data (described as “using tag provider gets back to Todd. Sorter.”). Observe the updated data availability using your available Ignition/tag provider observation method (the source does not specify the exact screen).

**Expected result:**
Updated data is observable via the tag provider path back into the system (Todd/Sorter side as described).

**Stop or Escalate If:**

* If the updated data does not return via the tag provider path, stop and escalate for deeper OPC COM/OPC server/Tag provider troubleshooting (the segment does not provide specific remediation steps).

---

## Success Criteria

* You confirm OPC COM subscribes to OPC server tags.
* You confirm a tag update results in an update being sent to Sorter Sweeper for processing.
* You confirm Sorter Sweeper sends messages to OPC COM and OPC COM writes data back to the OPC server.
* You confirm the tag provider reflects updated data back into the system.

## Failure Conditions

* OPC COM is not connected to the OPC server or subscriptions are not active.
* Tag updates do not reach Sorter Sweeper.
* Sorter Sweeper outputs are not written back to the OPC server.
* Updated data does not return via the tag provider path.

## Escalation Guidance

* If tag updates are not reaching Sorter Sweeper or Sorter Sweeper outputs are not being written back to the OPC server, stop and escalate for deeper OPC COM/OPC server/Tag provider troubleshooting. The source segment does not provide specific remediation steps.

## Missing Details / Known Gaps

* The source does not specify the exact live observation surface (Ignition screen, OPC COM log view, or OPC server tag browser) to confirm subscription status and tag update propagation.
* The source does not provide specific tag names/paths for the hospital/tippers tags to use as concrete verification targets.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_verify_opc_com_tag_subscription_updates_to_sorter_sweeper
- Source ID: `training_video_day2`
- Source Type: `training_video`
