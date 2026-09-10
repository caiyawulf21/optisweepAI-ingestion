# Display station unique IDs on Map Monitor using “View Station Ids” icon

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_display_station_unique_ids_map_monitor_v1` |
| Title | Display station unique IDs on Map Monitor using “View Station Ids” icon |
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

Use the Map Monitor Quick Select panel to display station unique IDs on the map. Stations are special locations with unique IDs (distinct from cells), which helps identify and debug station-related issues.

## When To Use

When you need to visually identify station locations on the Map Monitor map and confirm station unique IDs are being shown (for station-related debugging/identification).

## Access Or Tools Needed

* Map Monitor screen
* Quick Select panel icon “View Station Ids”

## Related Operational Context

* ctx_training_video_map_monitor_quick_select_overview_v1
* ctx_training_video_station_ids_reference_v1

## Procedure Steps

### Step 1 — Open the Map Monitor screen that contains the Quick Select icons

**Responsible role:** L1_support

**Instruction:**
Open the Map Monitor screen that includes the Quick Select panel with the icons (including “View Station Ids”).

**Expected result:**
The Quick Select panel with the “View Station Ids” icon is visible on the Map Monitor screen.

---

### Step 2 — Click the “View Station Ids” icon in the Quick Select panel

**Responsible role:** L1_support

**Instruction:**
In the Quick Select panel, click the “View Station Ids” icon.

**Expected result:**
Station unique IDs are enabled for display on the map (station objects will show unique IDs).

---

### Step 3 — Verify station locations show unique station IDs on the map

**Responsible role:** L1_support

**Instruction:**
On the map, look for station objects showing unique station IDs.

**Expected result:**
Station objects display unique station IDs on the map.

**Stop or Escalate If:**

* If station IDs are not visible, stop and escalate (no remediation steps are provided in the source).

---

### Step 4 — Interpret station vs cell distinction when reading the map

**Responsible role:** L1_support

**Instruction:**
When interpreting the map, use the source-provided distinction: stations are special locations with unique IDs, while cells are a different object type (described as light blue/gray in the source).

**Expected result:**
You can correctly distinguish station objects (unique station IDs) from cells (different object type/color).

---

## Success Criteria

* Station objects display unique station IDs on the Map Monitor map after selecting “View Station Ids”.
* Station vs cell distinction is correctly applied when reading the map (stations are special locations with unique IDs; cells are a different object type).

## Failure Conditions

* Station IDs are not visible after clicking “View Station Ids”.
* Station vs cell distinction cannot be applied (cells mistaken for stations).

## Escalation Guidance

* If station IDs are not visible, stop and escalate because the source provides no remediation steps.

## Missing Details / Known Gaps

* The source does not provide troubleshooting/remediation steps for cases where station IDs do not appear; it only instructs to stop and escalate.

## Source Lineage

- Candidate IDs: candidate_training_video_map_monitor_view_station_ids
- Source ID: `training_video_day1`
- Source Type: `training_video`
