# Display Station IDs on the Map Using Map Monitor Quick Select

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_display_station_ids_on_map_monitor_quick_select_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI Map Monitor Quick Select icon “View Station Ids” to overlay unique station identifiers on the live map. This helps identify/debug station-related issues by confirming station locations and their unique IDs are visible.

## When To Use

When you need to visually confirm station locations and their unique station IDs on the RMS Map Monitor map (stations are special locations distinct from cells) to support station-related identification/debugging.

## Source Procedure References

- proc_display_station_ids_on_map_monitor_quick_select_v1

## Procedure Steps

### Step 1 — Open RMS Map Monitor Quick Select panel

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (Map Monitor) and locate the left-side “Map Monitor Quick Select” panel.

**Expected result:**
The left-side “Map Monitor Quick Select” panel is visible with Quick Select icons including “View Station Ids”.

---

### Step 2 — Select “View Station Ids” overlay

**Responsible role:** L1_support

**Instruction:**
Click the “View Station Ids” icon in the Quick Select panel.

**Expected result:**
Station locations on the map display unique station IDs after selecting “View Station Ids”.

---

### Step 3 — Verify station unique IDs display on the map

**Responsible role:** L1_support

**Instruction:**
On the map, verify that station locations display unique station IDs.

**Expected result:**
Station locations show unique station IDs on the map.

---

## Success Criteria

- After selecting “View Station Ids”, station locations on the RMS Map Monitor map display unique station IDs.

## Failure Conditions

- Station IDs do not appear on the map after selecting “View Station Ids”.

## Escalation Guidance

- If station IDs do not display when the overlay is selected, stop and escalate for further RMS map/overlay troubleshooting.

## Missing Details / Known Gaps

- The packet requests image support for the post-click map view showing station IDs at station locations, but no separate artifact for the “station IDs displayed on the map” view is provided. Only the Quick Select icon panel artifact is available.
