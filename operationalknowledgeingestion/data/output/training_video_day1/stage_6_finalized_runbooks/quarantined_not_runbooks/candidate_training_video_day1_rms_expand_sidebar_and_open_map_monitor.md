# Expand RMS sidebar menu and open Map Monitor

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_expand_rms_sidebar_and_open_map_monitor_v1` |
| Title | Expand RMS sidebar menu and open Map Monitor |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

From the RMS home screen, expand the (sometimes hidden) sidebar menu and select the second option, Map Monitor, to view the map and AGV movements.

## When To Use

Use when you need to access the RMS Map Monitor view to view the map and AGV movements.

## Access Or Tools Needed

* RMS application UI access
* Sidebar menu expand/collapse control
* Expanded sidebar menu options (Map Monitor as the second option)

## Related Operational Context

* ctx_training_video_rms_home_navigation_overview_v1
* ctx_training_video_rms_sidebar_menu_reference_v1
* ctx_training_video_map_monitor_screen_reference_v1

## Procedure Steps

### Step 1 — Locate the RMS sidebar menu area (may be hidden)

**Responsible role:** operator

**Instruction:**
On the RMS home screen, locate the sidebar menu area. The menu may be hidden.

**Expected result:**
You can see the sidebar menu area/control on the RMS home screen (even if currently collapsed/hidden).

---

### Step 2 — Expand the sidebar menu by clicking the referenced control (item number three)

**Responsible role:** operator

**Instruction:**
Expand the sidebar menu by clicking the referenced control (the source calls out “item number three”).

**Expected result:**
The sidebar menu expands and shows multiple options.

---

### Step 3 — Select the second option: Map Monitor

**Responsible role:** operator

**Instruction:**
In the expanded sidebar menu, select the second option: Map Monitor.

**Expected result:**
Map Monitor is selected from the sidebar menu.

**Stop or Escalate If:**

* If Map Monitor does not appear as the second option after expanding the sidebar, stop and escalate (no additional navigation troubleshooting is provided in the source).

---

### Step 4 — Confirm Map Monitor view opens and shows the map and AGV movements

**Responsible role:** operator

**Instruction:**
Confirm the Map Monitor view opens and shows the map and AGV movements.

**Expected result:**
The Map Monitor screen is displayed, showing the map and AGV movements.

---

## Success Criteria

* Map Monitor screen is displayed in RMS.
* The Map Monitor screen shows the map and AGV movements.

## Failure Conditions

* After expanding the sidebar, Map Monitor is not the second option.
* Map Monitor does not open or does not display the map and AGV movements.

## Escalation Guidance

* If Map Monitor does not appear as the second option after expanding the sidebar, stop and escalate (no additional navigation troubleshooting is provided in the source).

## Missing Details / Known Gaps

* The source does not provide the exact UI label/name of the sidebar expand control beyond “item number three.”
* The source does not provide additional troubleshooting steps if Map Monitor fails to open (only the stop-and-escalate condition is specified for when Map Monitor is not the second option).

## Source Lineage

- Candidate IDs: candidate_training_video_day1_rms_expand_sidebar_and_open_map_monitor
- Source ID: `training_video_day1`
- Source Type: `training_video`
