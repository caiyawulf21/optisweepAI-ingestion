# Expand the RMS Sidebar and Open Map Monitor

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_expand_the_rms_sidebar_and_open_map_monitor_v1` |
| Title | Expand the RMS Sidebar and Open Map Monitor |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RMS sidebar menu to access the Map Monitor screen. The source describes the sidebar as sometimes hidden, explains that it can be expanded or collapsed, and identifies Map Monitor as the second menu option and a primary workspace for viewing the map and AGV movements.

## When To Use

Use this procedure when navigating within the RMS application to reach the Map Monitor screen from the RMS home or navigation screen, especially when the sidebar menu is hidden.

## Do Not Use For

* Do not use this procedure to guess alternate menu paths if the source-identified Map Monitor entry cannot be confirmed.
* Do not use this procedure if the sidebar cannot be expanded or the Map Monitor option is not visible; escalate for support instead.

## Safety And Operational Notes

* This source-backed procedure is limited to RMS screen navigation.
* Stop and escalate if the sidebar cannot be expanded or if the Map Monitor option is not visible.
* Do not guess other menu options if the source-identified Map Monitor entry cannot be confirmed.

## Access Or Tools Needed

* Access to the RMS application
* RMS home screen or navigation screen with sidebar menu

## Related Operational Context

* ctx_training_video_rms_home_navigation_overview_v1
* ctx_training_video_rms_sidebar_menu_reference_v1
* ctx_training_video_map_monitor_screen_reference_v1

## Procedure Steps

### Step 1 — Check whether the RMS sidebar menu is hidden

**Responsible role:** operator

**Instruction:**
Look at the RMS screen and determine whether the sidebar menu is currently hidden or already visible.

**Expected result:**
The current sidebar state is identified.

**Screens / Images:**

![artifact_training_video_training_video_day1_0023_ok_so_some_context_is_you_primary_00_55_32_000](assets/8ba388b364f56ff1.jpg)

*RMS home screen navigation area showing the sidebar menu concept and the expand/collapse behavior.*


**Stop or Escalate If:**

* The current screen does not allow the operator to determine whether the sidebar is hidden or expanded.

---

### Step 2 — Expand the sidebar menu if it is hidden

**Responsible role:** operator

**Instruction:**
If the menu is hidden, click the menu expand control referenced in the source to expand it.

**Expected result:**
The sidebar menu becomes visible in its expanded state.

**Screens / Images:**

![artifact_training_video_training_video_day1_0023_ok_so_some_context_is_you_primary_00_55_32_000](assets/8ba388b364f56ff1.jpg)

*The RMS screen area showing the sidebar expand control and the expanded versus collapsed menu state.*


**Stop or Escalate If:**

* The sidebar cannot be expanded.
* The expand control cannot be identified on the screen.

---

### Step 3 — Locate the Map Monitor option in the expanded sidebar

**Responsible role:** operator

**Instruction:**
In the expanded sidebar, locate the second option labeled Map Monitor.

**Expected result:**
The Map Monitor menu option is identified in the sidebar.

**Screens / Images:**

![artifact_training_video_training_video_day1_0023_ok_so_some_context_is_you_primary_00_55_32_000](assets/8ba388b364f56ff1.jpg)

*The expanded sidebar menu and the Map Monitor entry identified as the second option.*


**Stop or Escalate If:**

* The Map Monitor option is not visible.
* The operator cannot confirm the source-identified Map Monitor entry.
* Another menu option would need to be guessed.

---

### Step 4 — Select Map Monitor

**Responsible role:** operator

**Instruction:**
Select Map Monitor.

**Expected result:**
The system begins opening the Map Monitor view.

**Screens / Images:**

![artifact_training_video_training_video_day1_0023_ok_so_some_context_is_you_primary_00_55_32_000](assets/8ba388b364f56ff1.jpg)

*The Map Monitor option in the expanded sidebar before selection.*


**Stop or Escalate If:**

* Selecting Map Monitor does not open the expected screen.

---

### Step 5 — Verify the Map Monitor view is open

**Responsible role:** operator

**Instruction:**
Verify that the Map Monitor view opens and shows the map and AGV movements.

**Expected result:**
The Map Monitor screen is open and the user can view the map and AGV movements.

**Screens / Images:**

![artifact_training_video_training_video_day1_0023_ok_so_some_context_is_you_primary_00_55_32_000](assets/8ba388b364f56ff1.jpg)

*A source-backed example of the RMS navigation slide identifying Map Monitor as the place to view the map and AGV movements.*


**Stop or Escalate If:**

* The Map Monitor view does not open.
* The map is not visible.
* AGV movements are not visible.

---

## Success Criteria

* The sidebar is expanded if it was initially hidden.
* The Map Monitor option is located in the expanded sidebar.
* The Map Monitor view opens successfully.
* The user can view the map and AGV movements.

## Failure Conditions

* The sidebar cannot be expanded.
* The Map Monitor option is not visible.
* The operator cannot confirm the source-identified Map Monitor entry.
* The Map Monitor view does not open or does not show the map and AGV movements.

## Escalation Guidance

* If the sidebar cannot be expanded, stop and escalate for support.
* If the Map Monitor option is not visible, stop and escalate for support.
* Do not guess other menu options if the source-identified Map Monitor entry cannot be confirmed.

## Missing Details / Known Gaps

* The source does not provide the exact visual label or icon name for the sidebar expand control.
* The source does not provide a separate artifact showing the fully opened Map Monitor screen with map and AGV movement visibility in this packet.
* The source does not specify estimated completion time.
* The source does not specify supporting roles beyond the operator.
* The source does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_expand_rms_sidebar_and_open_map_monitor
- Source ID: `training_video_day1`
- Source Type: `training_video`
