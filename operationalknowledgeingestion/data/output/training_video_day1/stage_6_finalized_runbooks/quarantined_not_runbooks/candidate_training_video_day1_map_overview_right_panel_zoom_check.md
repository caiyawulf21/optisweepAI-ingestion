# Use Map Overview right-side panel to view additional information (zoom into right panel)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_map_overview_right_panel_info_zoom_v1` |
| Title | Use Map Overview right-side panel to view additional information (zoom into right panel) |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

On the Map Overview HMI, the right-side panel provides additional information. This procedure helps you locate that right-side panel on the live Map Overview screen and use the UI zoom/focus behavior to view the additional information shown there.

## When To Use

When you are on the OptiSweep HMI screen labeled "Map Overview" and need to view the additional information that is shown in the right-side panel (including using the UI zoom/focus into that panel).

## Access Or Tools Needed

* Access to the "Map Overview" HMI screen
* Ability to zoom/focus the Map Overview UI (if available)

## Related Operational Context

* ctx_training_video_map_overview_right_panel_v1
* ctx_training_video_map_overview_screen_presence_v1
* ctx_training_video_right_panel_information_area_v1

## Procedure Steps

### Step 1 — Open the "Map Overview" screen and locate the right-side panel area

**Responsible role:** operator

**Instruction:**
Open the HMI screen labeled "Map Overview" and locate the right-side panel area on that screen.

**Expected result:**
You can visually identify the right-side panel area on the live "Map Overview" screen.

**Stop or Escalate If:**

* If the right-side panel cannot be found, stop and request assistance from support.

---

### Step 2 — Confirm the right-side panel is the information area and zoom/focus into it

**Responsible role:** operator

**Instruction:**
Using the Map Overview UI, confirm you are looking at the right-side panel information area, then zoom or focus into that right panel if the UI supports it (the training segment indicates the next view zooms into the right panel).

**Expected result:**
After zooming/focusing, the additional information shown in the right-side panel is visible to you.

**Stop or Escalate If:**

* If the right-side panel cannot be zoomed/focused, stop and request assistance from support.
* Do not guess panel meanings beyond what is visible on the live Map Overview screen.

---

### Step 3 — Use the additional information shown in the zoomed right panel as context for the Map Overview screen

**Responsible role:** operator

**Instruction:**
Observe the additional information presented in the zoomed right panel and use it as the context for what is shown on the Map Overview screen.

**Expected result:**
You can reference the additional information displayed in the zoomed right panel while interpreting the Map Overview screen.

**Stop or Escalate If:**

* If you cannot see the additional information in the zoomed right panel, stop and request assistance from support.
* Do not guess panel meanings beyond what is visible on the live Map Overview screen.

---

## Success Criteria

* Right-side panel on the live "Map Overview" screen is identifiable.
* Zoom/focus into the right panel (when supported by the UI) results in the additional information being visible.
* You can use the additional information shown in the zoomed right panel as context for interpreting the Map Overview screen.

## Failure Conditions

* Right-side panel cannot be found on the "Map Overview" screen.
* Right-side panel cannot be zoomed/focused to reveal additional information.
* Additional information in the right panel is not visible/readable.

## Escalation Guidance

* If the right-side panel cannot be found or cannot be zoomed/focused, stop and request assistance from support.

## Missing Details / Known Gaps

* The source segment does not specify the exact UI control/gesture used to zoom/focus into the right panel (e.g., button name, icon, or mouse action).
* The source segment does not name what specific fields/labels are shown in the right-side panel beyond the statement that it provides "some more information".

## Source Lineage

- Candidate IDs: candidate_training_video_day1_map_overview_right_panel_zoom_check
- Source ID: `training_video_day1`
- Source Type: `training_video`
