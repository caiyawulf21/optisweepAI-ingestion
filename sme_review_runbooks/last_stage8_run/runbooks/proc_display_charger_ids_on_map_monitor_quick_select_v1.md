# Display Charger IDs on the Map Using Map Monitor Quick Select

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_display_charger_ids_on_map_monitor_quick_select_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `agv_charging_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI Map Monitor Quick Select icon “View Charger Ids” to overlay unique charger IDs on the live map for charger-related identification/debugging.

## When To Use

When you need to identify which charger location corresponds to a specific charger ID during charger-related troubleshooting/identification.

## Source Procedure References

- proc_display_charger_ids_on_map_monitor_quick_select_v1

## Procedure Steps

### Step 1 — Open RMS Map Monitor Quick Select panel

**Responsible role:** L1_support

**Instruction:**
In the RMS / fleet status UI (rms_ui), open the Map Monitor view and locate the left-side “Map Monitor Quick Select” panel.

**Expected result:**
The left-side “Map Monitor Quick Select” panel is visible with Quick Select icons including “View Charger Ids”.

---

### Step 2 — Enable the “View Charger Ids” overlay

**Responsible role:** L1_support

**Instruction:**
In the Map Monitor Quick Select panel, click the “View Charger Ids” icon.

**Expected result:**
The map updates to display charger IDs at charger locations (unique IDs for all chargers in the system).

---

### Step 3 — Verify unique charger IDs display on the map

**Responsible role:** L1_support

**Instruction:**
On the map, verify that charger locations display unique charger IDs.

**Expected result:**
Charger locations on the map show unique charger IDs after selecting “View Charger Ids” (e.g., if there are 10 chargers, 10 unique IDs are shown).

---

## Success Criteria

- After clicking “View Charger Ids”, charger locations on the RMS map display unique charger IDs.

## Failure Conditions

- Charger IDs do not appear on the map after selecting “View Charger Ids”.

## Escalation Guidance

- If charger IDs do not display when the overlay is selected, stop and escalate for further RMS map/overlay troubleshooting.
