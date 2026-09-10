# Display All AGV Active Paths on the Map Using Map Monitor Quick Select

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_display_all_agv_active_paths_map_monitor_quick_select_v1` |
| Title | Display All AGV Active Paths on the Map Using Map Monitor Quick Select |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RMS / fleet status UI Map Monitor Quick Select icon “View all AGV active paths” to overlay active AGV routes on the live map as small blue lines from each AGV to its intended destination.

## When To Use

When you need a visual confirmation of where each AGV is headed (active routes) on the live RMS map.

## Access Or Tools Needed

* RMS / fleet status UI (rms_ui) with Map Monitor Quick Select panel

## Related Operational Context

* ctx_training_video_agv_active_paths_display_v1
* ctx_training_video_map_monitor_quick_select_overview_v1

## Visual References

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*Map Monitor Quick Select panel showing the icon “View all AGV active paths” and related Quick Select icons (station IDs, charger IDs, and selection modes).*

## Procedure Steps

### Step 1 — Open Map Monitor Quick Select panel in RMS / fleet status UI

**Responsible role:** L1_support

**Instruction:**
In the RMS / fleet status UI (rms_ui), locate the left-side “Map Monitor Quick Select” panel.

**Expected result:**
The left-side Map Monitor Quick Select panel is visible and includes the icon labeled “View all AGV active paths”.

---

### Step 2 — Select “View all AGV active paths” icon

**Responsible role:** L1_support

**Instruction:**
Click the “View all AGV active paths” icon in the Map Monitor Quick Select panel.

**Expected result:**
Active AGV paths are displayed on the map as small blue lines, each starting from an AGV and ending at where that AGV wants to go.

**Stop or Escalate If:**

* If the map shows no active-path blue lines while AGVs are expected to be moving, stop and escalate for further fleet status checks.

---

### Step 3 — Verify blue active-path overlays on the map

**Responsible role:** L1_support

**Instruction:**
On the map, verify that active paths are displayed as small blue lines that start from each AGV and end at where that AGV wants to go.

**Expected result:**
The map displays small blue lines for all active AGV routes, each line starting at an AGV and ending at that AGV’s intended destination.

**Stop or Escalate If:**

* If the map shows no blue lines while AGVs are expected to be moving, stop and escalate to deeper RMS/WCS checks.

---

## Success Criteria

* On the RMS map, small blue lines appear for active AGV routes, each line starting at an AGV and ending at that AGV’s intended destination.

## Failure Conditions

* No active-path blue lines appear when AGVs are expected to be moving.

## Escalation Guidance

* If no active-path blue lines appear while AGVs are expected to be moving, stop and escalate for further fleet status checks (deeper RMS/WCS checks).

## Missing Details / Known Gaps

* The packet does not specify the exact deeper RMS/WCS checks to run after escalation (only that escalation should go to deeper RMS/WCS checks).

## Source Lineage

- Candidate IDs: candidate_training_video_day1_map_monitor_view_all_agv_active_paths
- Source ID: `training_video_day1`
- Source Type: `training_video`
