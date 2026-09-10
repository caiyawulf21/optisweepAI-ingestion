# Use the Aveva “API page” to interpret Overall System state and select the documented system functions (System Startup, System Bag Out, System Shutdown, System Purge)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_aveva_api_page_interpret_overall_system_state_and_functions_v1` |
| Title | Use the Aveva “API page” to interpret Overall System state and select the documented system functions (System Startup, System Bag Out, System Shutdown, System Purge) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Aveva “API page” (Overall System) to read the current “System State” and interpret what the documented left-side functions do: System Startup, System Bag Out (close out), System Shutdown, and System Purge—specifically including the documented differences between close out vs purge (tote coverage and label printing behavior).

## When To Use

When you need to confirm what the OptiSweep system is currently doing by reading the “System State” on the Aveva “API page,” and you need to explain the documented purpose/behavior of the left-side functions (System Startup, System Bag Out/close out, System Shutdown, System Purge) to guide support actions or troubleshooting discussions.

## Access Or Tools Needed

* Aveva HMI access to the “API page” (Overall System Aveva API page)
* Visual access to the left-side sections/labels: System State, System Startup, System Bag Out, System Shutdown, System Purge

## Related Operational Context

* ctx_training_video_api_page_overview_v1
* ctx_training_video_system_state_reference_v1
* ctx_training_video_system_startup_agv_staging_v1
* ctx_training_video_bag_out_close_out_reference_v1
* ctx_training_video_system_shutdown_agv_charging_v1
* ctx_training_video_system_purge_reference_v1

## Procedure Steps

### Step 1 — Open the Aveva “API page” and locate the left-side items (System State, System Startup, System Bag Out, System Shutdown, System Purge)

**Responsible role:** L1_support

**Instruction:**
On the Aveva HMI, open the Overall System “API page” (referred to as the “API page”). On the left side of the page, locate the labeled sections/items: “System State,” “System Startup,” “System Bag Out,” “System Shutdown,” and “System Purge.”

**Expected result:**
The left side of the Overall System Aveva “API page” shows the labeled items: System State, System Startup, System Bag Out, System Shutdown, and System Purge.

**Stop or Escalate If:**

* If the API page does not show the expected left-side items (System State, System Startup, System Bag Out, System Shutdown, System Purge), stop and escalate for guidance on the correct screen or access.

---

### Step 2 — Read the “System State” value to determine the current state the system is in

**Responsible role:** L1_support

**Instruction:**
On the Overall System Aveva “API page,” read the value displayed in the “System State” field.

**Expected result:**
You can point to the current “System State” value shown on the Aveva “API page.”

**Stop or Escalate If:**

* If the API page does not show the expected left-side items (including “System State”), stop and escalate for guidance on the correct screen or access.

---

### Step 3 — Interpret the documented behavior of “System Startup” (AGV staging for exchanges)

**Responsible role:** L1_support

**Instruction:**
If you need to explain what “System Startup” is intended to do, use the documented behavior shown in the source: AGVs are kept in a shut down state between sorts to allow them to charge, and System Startup triggers OptiSweep to stage the AGVs for exchanges.

**Expected result:**
You can accurately describe that System Startup is associated with staging AGVs for exchanges after AGVs have been kept in a shutdown state between sorts for charging.

**Stop or Escalate If:**

* Do not assume behavior beyond what the source states; escalate if the live system behavior contradicts the documented descriptions.

---

### Step 4 — Interpret the documented behavior of “System Bag Out” / close out (tote coverage and label printing)

**Responsible role:** L1_support

**Instruction:**
If you need to explain “System Bag Out” / close out behavior, use the documented behavior: at the end of a sort, close out is used to close all chutes and exchange all totes with items; close out only affects totes with items in it and prints labels.

**Expected result:**
You can accurately describe that close out (System Bag Out) closes all chutes and exchanges totes with items, and that it prints labels for those totes with items.

**Stop or Escalate If:**

* Do not assume behavior beyond what the source states (e.g., tote coverage and label printing). Escalate if the live system behavior contradicts the documented descriptions.

---

### Step 5 — Interpret the documented behavior of “System Shutdown” (AGV charger rotation state)

**Responsible role:** L1_support

**Instruction:**
If you need to explain “System Shutdown,” use the documented behavior: when the sort is done the system should be put in a shutdown state for AGVs to rotate on the charger.

**Expected result:**
You can accurately describe that System Shutdown is the post-sort shutdown state intended for AGVs to rotate on the charger.

**Stop or Escalate If:**

* Do not assume behavior beyond what the source states. Escalate if the live system behavior contradicts the documented descriptions.

---

### Step 6 — Interpret the documented behavior of “System Purge” (purge everything; no label printing at the tipper)

**Responsible role:** L1_support

**Instruction:**
If you need to explain “System Purge,” use the documented behavior: purge is like close out, but instead of only totes with items in it, it will purge everything; it exchanges every tote in the system and does not print a label at the tipper.

**Expected result:**
You can accurately describe that purge exchanges every tote in the system and does not print a label at the tipper (unlike close out which only affects totes with items and prints labels).

**Stop or Escalate If:**

* Do not assume behavior beyond what the source states (e.g., purge vs close out label printing and tote coverage). Escalate if the live system behavior contradicts the documented descriptions.

---

## Success Criteria

* You can identify the current “System State” value shown on the Overall System Aveva “API page.”
* You can accurately explain the documented purpose/behavior of System Startup, System Bag Out/close out, System Shutdown, and System Purge, including purge vs close out differences (tote coverage and label printing at the tipper).

## Failure Conditions

* The Overall System Aveva “API page” does not show one or more expected left-side items (System State, System Startup, System Bag Out, System Shutdown, System Purge).
* Live system behavior contradicts the documented descriptions for purge vs close out (tote coverage and label printing behavior).

## Escalation Guidance

* If the API page does not show the expected left-side items (System State, System Startup, System Bag Out, System Shutdown, System Purge), stop and escalate for guidance on the correct screen or access.
* If the live system behavior contradicts the documented descriptions (especially purge vs close out differences), escalate rather than assuming behavior.

## Missing Details / Known Gaps

* The source does not provide exact click-path/navigation steps to reach the Overall System Aveva “API page” beyond locating the left-side items on the page.
* The source does not list the specific possible values/enumerations for “System State,” only that it shows the current state.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_api_page_interpret_system_state_startup_bagout_shutdown_purge
- Source ID: `training_video_day1`
- Source Type: `training_video`
