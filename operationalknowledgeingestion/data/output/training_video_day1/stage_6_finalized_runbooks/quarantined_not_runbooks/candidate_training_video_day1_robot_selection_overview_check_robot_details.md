# Use the Robot Selection Overview panel to identify the selected robot, its location, and tote status

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_robot_selection_overview_panel_to_identify_robot_details_v1` |
| Title | Use the Robot Selection Overview panel to identify the selected robot, its location, and tote status |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection Overview HMI panel to identify the selected robot’s robot ID and location, and determine whether the robot is carrying a tote, has a tote mismatch (tote “?”), or has no tote (shows “layer_1”).

## When To Use

When you need to quickly identify which robot is causing an issue and confirm its robot ID, location, and tote status from the Robot Selection Overview panel after selecting a robot.

## Access Or Tools Needed

* Tote/robot selection HMI screen: Robot Selection Overview (Robot x Robot panel)
* Mouse/pointing device to click a robot and the small arrow to expand the detail section

## Related Operational Context

* ctx_training_video_robot_selection_panel_overview_v1
* ctx_training_video_robot_detail_fields_v1
* ctx_training_video_tote_presence_indicators_v1

## Procedure Steps

### Step 1 — Open the Robot Selection Overview view (Robot x Robot panel)

**Responsible role:** L1_support

**Instruction:**
Open the Robot Selection Overview view where the “Robot x Robot” panel and the robot-selection behavior are shown.

**Expected result:**
The Robot Selection Overview panel is visible and you can click a robot in the robot list/grid.

---

### Step 2 — Select a robot and confirm it is highlighted with a box

**Responsible role:** L1_support

**Instruction:**
Click the robot you want to investigate on the Robot Selection Overview panel and confirm the selected robot has a box around it.

**Expected result:**
The selected robot is highlighted with a box around it, indicating the panel has switched to that robot’s details.

**Stop or Escalate If:**

* If the selected robot highlight/box does not appear or does not match the intended robot, stop and escalate to support.

---

### Step 3 — Expand the robot detail section if it is hidden

**Responsible role:** L1_support

**Instruction:**
If the robot detail section is hidden, click the small arrow control to expand it so all robot detail information is visible.

**Expected result:**
The robot detail section expands and shows the available robot detail information.

**Stop or Escalate If:**

* If the detail section cannot be expanded (small arrow not available/does nothing), stop and escalate to support.

---

### Step 4 — Record the robot ID and location from the expanded details

**Responsible role:** L1_support

**Instruction:**
In the expanded details, record the robot ID and location fields shown for the selected robot.

**Expected result:**
You have captured the selected robot’s robot ID and location from the detail panel.

**Stop or Escalate If:**

* If robot ID/location indicators are not visible, stop and escalate to support.

---

### Step 5 — Check tote area under the robot ID and note tote ID (or tote mismatch indicator)

**Responsible role:** L1_support

**Instruction:**
Under the robot ID, check the tote indicator. If a tote ID is shown (example shown: tote #96), note the tote ID.

**Expected result:**
The tote indicator under the robot ID is identified and you have noted the tote ID when present.

**Stop or Escalate If:**

* If the robot ID/location/tote indicators are not visible or do not match the expected panel behavior described in the source, stop and escalate to support.

---

### Step 6 — Interpret tote indicator with a “?” before it as robot removed but tote not removed

**Responsible role:** L1_support

**Instruction:**
If the tote text shows a “?” before it, interpret it as: the robot was removed but the tote has not.

**Expected result:**
You correctly classify the tote state as a mismatch using the “?” indicator.

**Stop or Escalate If:**

* If the tote indicator does not match the expected “?” behavior, stop and escalate to support.

---

### Step 7 — Confirm no-tote state shows “layer_1” and no brown-box tote visual

**Responsible role:** L1_support

**Instruction:**
If the robot does not have a tote, confirm the display shows “layer_1” and that the brown-box tote visual is not shown.

**Expected result:**
You confirm the robot is in the no-tote state by observing “layer_1” and absence of the brown-box tote visual.

**Stop or Escalate If:**

* If the tote/no-tote indicators do not match the expected panel behavior, stop and escalate to support.

---

## Success Criteria

* Robot ID and location are recorded for the selected robot from the Robot Selection Overview detail panel.
* Tote status is classified as one of: tote ID shown (tote present), tote “?” prefix (robot removed but tote not removed), or “layer_1” with no brown-box tote visual (no tote).

## Failure Conditions

* Detail section cannot be expanded (small arrow not available/does nothing).
* Robot ID/location/tote indicators are not visible or do not match the expected panel behavior.
* Tote indicator state cannot be determined (e.g., unclear “?” prefix or unclear “layer_1”/brown-box visual).

## Escalation Guidance

* If the detail section cannot be expanded or if robot ID/location/tote indicators are not visible or do not match expected behavior, stop and escalate to support.

## Missing Details / Known Gaps

* The packet does not provide the exact HMI navigation path/menu name to reach the Robot Selection Overview view; it only references opening the view and selecting robots within it.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_robot_selection_overview_check_robot_details
- Source ID: `training_video_day1`
- Source Type: `training_video`
