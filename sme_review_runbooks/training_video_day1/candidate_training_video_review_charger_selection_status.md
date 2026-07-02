# Review Charger Status And Associated Robot In Charger Selection

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_review_charger_status_and_associated_robot_in_charger_selection_v1` |
| Title | Review Charger Status And Associated Robot In Charger Selection |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Charger Selection view to identify a charger by charger ID, verify whether it is enabled or disabled, and see which robot is currently associated with that charger.

## When To Use

Use this procedure when support needs to inspect a charger in the Charger Selection view, confirm the charger's unique ID, verify whether the charger is enabled or disabled, and determine which robot is currently on or associated with that charger.

## Do Not Use For

* Do not use this runbook to disable or re-enable a charger; this source-specific procedure is limited to viewing and recording charger information.
* Do not use this runbook for manual robot charging or charger recovery actions beyond status review.

## Safety And Operational Notes

* This procedure is limited to viewing and recording information shown in the Charger Selection screen.
* The source notes that charger disablement affects whether RMS and WCS send AGVs to that charging location; do not change charger state as part of this procedure unless directed by a separate approved procedure.

## Access Or Tools Needed

* Access to the Charger Selection screen
* Visibility of charger IDs and charger status information

## Related Operational Context

* ctx_training_video_charger_selection_screen_v1

## Procedure Steps

### Step 1 — Open the Charger Selection view

**Responsible role:** L1_support

**Instruction:**
Open the Charger Selection view so charger IDs and charger details can be reviewed.

**Expected result:**
The Charger Selection view is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*The Charger Selection screen referenced in the training material.*


**Stop or Escalate If:**

* Escalate if the Charger Selection view does not show the charger information described in the source.

---

### Step 2 — Identify the charger by charger ID

**Responsible role:** L1_support

**Instruction:**
Identify the charging station by its unique charger ID in the Charger Selection view.

**Expected result:**
The target charger is located by its unique charger ID.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*The Charger Selection screen area showing charger ID selection.*


**Stop or Escalate If:**

* Escalate if the required charger ID cannot be identified in the Charger Selection view.

---

### Step 3 — Select the charger ID to view details

**Responsible role:** L1_support

**Instruction:**
Click the charger ID to view charger details.

**Expected result:**
Charger details for the selected charger are displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*The charger ID selection area used to open charger details.*


**Stop or Escalate If:**

* Escalate if selecting the charger ID does not show charger status or associated robot information.

---

### Step 4 — Review charger enabled or disabled status

**Responsible role:** L1_support

**Instruction:**
Check the displayed charger status and verify whether the charger is shown as enabled or disabled.

**Expected result:**
The charger status is confirmed as enabled or disabled.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*The Charger Selection screen area showing enabled or disabled charger status.*


**Stop or Escalate If:**

* Escalate if the Charger Selection view does not show charger status information described in the source.
* Escalate if the observed charger state does not match the expected operational understanding and further action is needed beyond viewing status.

---

### Step 5 — Review the robot associated with the charger

**Responsible role:** L1_support

**Instruction:**
Check which robot is shown as being on or associated with that charger.

**Expected result:**
The currently associated robot is identified from the charger details.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*The Charger Selection screen area showing the robot currently associated with the charger.*


**Stop or Escalate If:**

* Escalate if the Charger Selection view does not show the associated robot information described in the source.

---

### Step 6 — Record charger observations for follow-up

**Responsible role:** L1_support

**Instruction:**
Record the observed charger ID, charger status, and associated robot for support or operational follow-up.

**Expected result:**
The charger ID, charger status, and associated robot are documented.

**Stop or Escalate If:**

* Escalate if required charger details are not available to document.

---

## Success Criteria

* The correct charger is identified by unique charger ID.
* The selected charger's status is confirmed as enabled or disabled.
* The robot currently on or associated with the charger is identified.
* Observed charger details are recorded for support or operational follow-up.

## Failure Conditions

* The Charger Selection view is unavailable or does not open.
* The target charger cannot be identified by charger ID.
* Selecting the charger ID does not display charger details.
* Charger status or associated robot information is missing or unclear.
* The observed charger state requires action beyond status review.

## Escalation Guidance

* Escalate if the Charger Selection view does not show the charger status or associated robot information described in the source.
* Escalate if the observed charger state does not match the expected operational understanding and further action is needed beyond viewing status.

## Missing Details / Known Gaps

* The source packet does not provide exact navigation steps for reaching the Charger Selection view.
* The source packet does not provide a formal recording location or template for documenting observations.
* The source packet does not define expected charger state values beyond enabled or disabled.
* The source packet does not specify follow-up actions after an unexpected charger state is observed.

## Source Lineage

- Candidate IDs: candidate_training_video_review_charger_selection_status
- Source ID: `training_video_day1`
- Source Type: `training_video`
