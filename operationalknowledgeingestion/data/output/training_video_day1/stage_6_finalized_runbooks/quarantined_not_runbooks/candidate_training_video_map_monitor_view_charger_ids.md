# Display charger unique IDs on Map Monitor using “View Charger Ids” icon

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_display_charger_unique_ids_map_monitor_v1` |
| Title | Display charger unique IDs on Map Monitor using “View Charger Ids” icon |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Map Monitor Quick Select panel to display unique charger IDs on the map so you can identify chargers by ID.

## When To Use

When you need to identify chargers by their unique IDs on the Map Monitor map display.

## Access Or Tools Needed

* Map Monitor screen
* Quick Select panel icon “View Charger Ids”

## Related Operational Context

* ctx_training_video_map_monitor_quick_select_overview_v1
* ctx_training_video_charger_ids_reference_v1

## Procedure Steps

### Step 1 — Open the Map Monitor screen that contains the Quick Select icons

**Responsible role:** L1_support

**Instruction:**
Open the Map Monitor screen that contains the Quick Select icons.

**Expected result:**
The Quick Select panel with icons is visible on the Map Monitor screen.

---

### Step 2 — Click the “View Charger Ids” icon in the Quick Select panel

**Responsible role:** L1_support

**Instruction:**
In the Quick Select panel, click the “View Charger Ids” icon.

**Expected result:**
Charger objects on the map display unique charger IDs after clicking “View Charger Ids.”

---

### Step 3 — Verify charger objects display unique charger IDs on the map

**Responsible role:** L1_support

**Instruction:**
On the map, verify that charger objects display unique charger IDs.

**Expected result:**
All chargers in the system show unique charger IDs on the map after clicking “View Charger Ids.”

**Stop or Escalate If:**

* If charger IDs are not visible, stop and escalate (no remediation steps are provided in the source).

---

## Success Criteria

* After clicking “View Charger Ids”, charger objects on the Map Monitor map display unique charger IDs.

## Failure Conditions

* Charger IDs do not appear on the map after clicking “View Charger Ids”.

## Escalation Guidance

* If charger IDs are not visible, stop and escalate because the source provides no troubleshooting/remediation steps.

## Missing Details / Known Gaps

* The source does not provide troubleshooting steps for cases where charger IDs do not appear; escalation is required.

## Source Lineage

- Candidate IDs: candidate_training_video_map_monitor_view_charger_ids
- Source ID: `training_video_day1`
- Source Type: `training_video`
