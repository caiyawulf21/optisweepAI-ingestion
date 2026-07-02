# Distinguish Whether An AGV Is In The System Versus In The Map

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_distinguish_whether_an_agv_is_in_the_system_versus_in_the_map_v1` |
| Title | Distinguish Whether An AGV Is In The System Versus In The Map |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the map monitor summary area and AGV map display to determine whether an AGV is currently in the viewed map, disconnected but still present in the map, or still part of the RMS system after being removed from the map.

## When To Use

Use when you need to interpret AGV presence and status in RMS/map views and determine whether an AGV is still shown in the active map, disconnected within the map, or present in the system but not associated with the viewed map.

## Do Not Use For

* Do not use this runbook to remove, repair, or recover an AGV.
* Do not use this runbook to infer corrective actions beyond status interpretation.
* Do not use this runbook to decide that an AGV has been intentionally removed unless the displayed counts and map state support that interpretation.

## Safety And Operational Notes

* This source describes status interpretation only, not AGV control or recovery actions.
* Do not infer removal or repair actions because the source only explains status meaning and count behavior.

## Access Or Tools Needed

* Access to the map monitor summary area
* Access to the AGV map display

## Related Operational Context

* ctx_training_video_in_system_vs_in_map_agv_status_v1

## Procedure Steps

### Step 1 — Locate AGV summary counts

**Responsible role:** L1_support

**Instruction:**
Open the map monitor view and locate the summary area that shows AGV-related counts, including the indicators used to understand AGVs in the map and disconnected AGVs.

**Expected result:**
The AGV summary area is visible and ready for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*Map monitor summary area with AGV-related indicators, including disconnected AGV count and other summary fields.*


**Stop or Escalate If:**

* Escalate if the displayed counts needed for interpretation are not available in the visible interface.

---

### Step 2 — Compare map and system presence counts

**Responsible role:** L1_support

**Instruction:**
Compare the count of AGVs shown in the map with the count of AGVs that are still in the system but not in the map.

**Expected result:**
You can tell whether there are AGVs present in the system that are not currently associated with the viewed map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*Summary indicators used to compare AGV presence in the map versus AGV-related system counts.*


**Stop or Escalate If:**

* Escalate if the displayed counts and map state do not align with the source-described behavior.

---

### Step 3 — Check whether the specific AGV still appears on the map

**Responsible role:** L1_support

**Instruction:**
If checking a specific AGV, inspect the map and verify whether that AGV still appears on the map even if it is disconnected.

**Expected result:**
You can confirm whether the AGV is still displayed on the map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0024_once_you_click_on_it_it_primary_00_56_52_000](assets/cceab8d98381b6c6.jpg)

*Overall map view where AGV presence or absence can be checked.*

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*Robot selection/map-related view showing robot color meanings, including purple for disconnected.*


**Stop or Escalate If:**

* Escalate if the AGV cannot be located and the counts do not clarify whether it is still in the map.

---

### Step 4 — Interpret purple AGV as disconnected but still in the map

**Responsible role:** L1_support

**Instruction:**
If the AGV appears purple on the map or robot view, interpret that as disconnected while still remaining in the map.

**Expected result:**
A purple AGV is classified as disconnected but still in the map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0029_all_right_so_the_robot_selection_primary_01_15_18_000](assets/5ffd5d9071f8b918.jpg)

*Robot color legend/description indicating purple means robot disconnected.*


**Stop or Escalate If:**

* Escalate if the AGV appears in a state that conflicts with the source-described purple disconnected meaning.

---

### Step 5 — Interpret removed AGV as system-only and not in the viewed map

**Responsible role:** L1_support

**Instruction:**
If the AGV has been removed and is no longer associated with the map you are viewing, interpret it as still part of the overall system but not in that map.

**Expected result:**
The AGV is classified as system-only relative to the viewed map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*Summary/map context used to distinguish AGVs still in the system from AGVs associated with the viewed map.*


**Stop or Escalate If:**

* Escalate if the displayed counts and map state do not align with the source-described behavior.

---

### Step 6 — Record the AGV status interpretation

**Responsible role:** L1_support

**Instruction:**
Record whether the AGV is in the map, disconnected in the map, or in the system but not in the map.

**Expected result:**
A clear status interpretation is documented.

**Stop or Escalate If:**

* Escalate if the status cannot be determined from the displayed counts and map state.
* Do not infer removal or repair actions because the source only explains status meaning and count behavior.

---

## Success Criteria

* The user can distinguish between an AGV that is in the map, disconnected but still shown in the map, and in the system but not in the map.
* The interpretation is based on displayed counts and map state consistent with the source description.

## Failure Conditions

* Displayed counts and map state do not align with the source-described behavior.
* The AGV cannot be confidently classified as in-map, disconnected in-map, or system-only.
* The interface does not provide enough visible information to support the interpretation.

## Escalation Guidance

* Escalate if the displayed counts and map state do not align with the source-described behavior.
* Escalate if the status cannot be determined from the available summary and map views.
* Do not infer removal or repair actions because the source only explains status meaning and count behavior.

## Missing Details / Known Gaps

* The source packet does not provide exact field labels for the map-versus-system counts.
* The source packet does not provide a dedicated image showing the specific in-system-but-not-in-map count.
* The source packet does not provide a formal recording location or template for documenting the interpreted status.
* The source does not define follow-up actions after classification beyond escalation for inconsistency.

## Source Lineage

- Candidate IDs: candidate_training_video_distinguish_agv_in_system_vs_in_map_status
- Source ID: `training_video_day1`
- Source Type: `training_video`
