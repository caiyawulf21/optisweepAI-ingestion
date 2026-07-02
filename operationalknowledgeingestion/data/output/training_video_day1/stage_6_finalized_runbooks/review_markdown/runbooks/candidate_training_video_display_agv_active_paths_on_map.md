# Display All AGV Active Paths On the Map

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_display_all_agv_active_paths_on_the_map_v1` |
| Title | Display All AGV Active Paths On the Map |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Map Monitor Quick Select control to display all AGV active paths on the map as small blue lines from each AGV to its destination.

## When To Use

Use when you need to visualize AGV active routes in Map Monitor and confirm that active paths are shown from each AGV to where it wants to go.

## Do Not Use For

* Do not use this procedure to infer path meaning beyond the source description of blue lines from AGVs to destinations.

## Safety And Operational Notes

* This source describes a display/visualization action in Map Monitor and does not describe any physical intervention.
* Do not infer path meaning beyond the source description of blue lines from AGVs to destinations.

## Access Or Tools Needed

* Access to the Map Monitor screen
* Map Monitor Quick Select controls

## Related Operational Context

* ctx_training_video_map_monitor_quick_select_overview_v1
* ctx_training_video_agv_active_paths_display_v1

## Procedure Steps

### Step 1 — Open Map Monitor and locate Quick Select

**Responsible role:** L1_support

**Instruction:**
Open the Map Monitor screen and locate the Quick Select area on the left-side panel.

**Expected result:**
The Map Monitor screen is open and the Quick Select area is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The Map Monitor Quick Select panel on the left side, including the icon set used for path display.*


**Stop or Escalate If:**

* Stop or escalate if Map Monitor cannot be accessed.
* Stop or escalate if the Quick Select area is not visible or cannot be identified.

---

### Step 2 — Select View all AGV active paths

**Responsible role:** L1_support

**Instruction:**
Click the "View all AGV active paths" icon.

**Expected result:**
The active path display is enabled on the map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The Quick Select icon identified as View all AGV active paths.*


**Stop or Escalate If:**

* Escalate if the expected active path display does not appear after clicking the icon.

---

### Step 3 — Observe the displayed active path indicators

**Responsible role:** L1_support

**Instruction:**
Observe the map for active path indicators shown as small blue lines.

**Expected result:**
Small blue lines are visible on the map as active path indicators.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The map display behavior associated with the active paths icon and the expected blue-line path overlay.*


**Stop or Escalate If:**

* Escalate if the expected active path display does not appear after clicking the icon.

---

### Step 4 — Verify each blue line runs from AGV to destination

**Responsible role:** L1_support

**Instruction:**
Verify that each displayed blue line starts from an AGV and ends where the AGV wants to go.

**Expected result:**
Each displayed blue line runs from an AGV to its intended destination.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The active path visualization concept described for AGVs and their destinations.*


**Stop or Escalate If:**

* Escalate if the expected active path display does not appear after clicking the icon.
* Stop if interpretation would require inferring path meaning beyond the source description.

---

## Success Criteria

* The Map Monitor Quick Select area is located.
* The "View all AGV active paths" icon is selected.
* The map displays all active AGV paths as small blue lines.
* The displayed blue lines run from each AGV to where it wants to go.

## Failure Conditions

* Map Monitor cannot be opened.
* The Quick Select area cannot be located.
* The expected active path display does not appear after clicking the icon.
* The displayed map state does not match the source description of blue lines from AGVs to destinations.

## Escalation Guidance

* Escalate if the expected active path display does not appear after clicking the icon.
* Escalate if Map Monitor or the Quick Select area is unavailable.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not specify whether production stop is required.
* The source does not specify LOTO requirements.
* The source does not provide additional troubleshooting steps if the icon click does not produce the expected display.

## Source Lineage

- Candidate IDs: candidate_training_video_display_agv_active_paths_on_map
- Source ID: `training_video_day1`
- Source Type: `training_video`
