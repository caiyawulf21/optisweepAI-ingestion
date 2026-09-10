# Interpret Container Selection screen: container/total ID and tote presence color coding

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_container_selection_screen_container_total_and_tote_color_v1` |
| Title | Interpret Container Selection screen: container/total ID and tote presence color coding |
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

Use the Container Selection screen to identify the selected container/total ID (e.g., the “113”) and determine whether a rack location has a tote by using the dark-blue vs light-blue color indicators. If you select a dark-blue (tote-present) cell, the screen shows a box icon and the tote number.

## When To Use

When you need to read the Container Selection screen to confirm which container/total ID is selected and whether a rack location is tote-present (dark blue) or empty (light blue), including verifying the tote number after selecting a tote-present cell.

## Access Or Tools Needed

* Container Selection HMI screen access
* Visual access to the screen’s container/total ID and dark-blue/light-blue indicators

## Related Operational Context

* ctx_training_video_container_selection_screen_overview_v1
* ctx_training_video_container_color_status_v1

## Procedure Steps

### Step 1 — Open the Container Selection screen (Container Selection 1 / Totes / Container / Location)

**Responsible role:** L1_support

**Instruction:**
Open the Container Selection screen that shows Container Selection 1 / Totes / Container / Location.

**Expected result:**
The Container Selection screen is visible with rack/location cells that use dark-blue vs light-blue to indicate tote presence vs empty rack, and with a green container/total ID field.

**Stop or Escalate If:**

* If the Container Selection screen cannot be opened or the expected container/total ID and color indicators are not visible, stop and escalate for clarification.

---

### Step 2 — Read the green container/total ID (e.g., “113”)

**Responsible role:** L1_support

**Instruction:**
Locate the green number labeled as the container/total ID and note its value (example given: “113”).

**Expected result:**
You can identify the green container/total ID value (example: “113”) and treat it as both the container and the total number/total ID as described.

**Stop or Escalate If:**

* If the screen does not show the expected green container/total ID, stop and escalate for clarification.

---

### Step 3 — Determine tote presence vs empty rack using dark-blue vs light-blue

**Responsible role:** L1_support

**Instruction:**
At the rack/location cell you care about, check the color indicator: dark blue means tote present; light blue means empty rack.

**Expected result:**
You can classify the rack/location as tote-present (dark blue) or empty (light blue) using the screen’s color coding.

**Stop or Escalate If:**

* If the color indicator meaning cannot be applied (colors/states differ from the source’s dark-blue vs light-blue meaning), stop and escalate for clarification.

---

### Step 4 — Select the dark-blue (tote-present) cell to reveal box icon and tote number

**Responsible role:** L1_support

**Instruction:**
If needed, select the dark-blue cell (tote-present rack/location) and observe whether a box icon appears and whether the tote number is shown.

**Expected result:**
After selecting a tote-present (dark-blue) cell, a box icon appears and the tote number is displayed.

**Stop or Escalate If:**

* If selecting the cell does not reveal the box icon and tote number as described, stop and escalate for clarification.

---

### Step 5 — Report what the screen indicates for that location (container/total ID and tote presence)

**Responsible role:** L1_support

**Instruction:**
Using the green container/total ID value and the dark-blue vs light-blue tote presence classification, report what the screen indicates for that location. If you selected the tote-present cell, include the tote number shown with the box icon.

**Expected result:**
You can state: (1) the green container/total ID value (example “113”), and (2) whether the rack/location is tote-present (dark blue) or empty (light blue), and (3) the tote number if the box icon/tote number was revealed after selection.

**Stop or Escalate If:**

* If the screen does not show the expected container/total ID or the color indicator meaning cannot be applied, stop and escalate for clarification.

---

## Success Criteria

* You correctly identify the green container/total ID value on the Container Selection screen (example “113”).
* You correctly classify the rack/location as tote-present (dark blue) vs empty rack (light blue).
* When selecting a tote-present (dark-blue) cell, the box icon appears and the tote number is displayed.

## Failure Conditions

* Green container/total ID is not visible or cannot be read.
* Dark-blue vs light-blue indicators do not match the described tote-present vs empty rack meaning.
* Selecting a tote-present cell does not show a box icon and tote number.

## Escalation Guidance

* If the screen does not show the expected container/total ID in green or the dark-blue vs light-blue meaning cannot be applied (e.g., colors/states differ from the described mapping), stop and escalate for clarification.

## Missing Details / Known Gaps

* The packet does not provide explicit navigation steps (click path) to open the Container Selection screen; it only states to open the screen described as showing Container Selection 1 / Totes / Container / Location.

## Source Lineage

- Candidate IDs: candidate_training_video_container_selection_interpret_container_total_and_color
- Source ID: `training_video_day1`
- Source Type: `training_video`
