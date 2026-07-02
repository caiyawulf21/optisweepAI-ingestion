# View Tote Associated To A Rack In The RMS Map

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_tote_associated_to_a_rack_in_the_rms_map_v1` |
| Title | View Tote Associated To A Rack In The RMS Map |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RMS map container selection view to click a rack location and see which tote the system associates with that rack. The source specifically states that clicking a dark blue rack shows the tote on that rack, and that rack position labels should match what is shown in the map.

## When To Use

Use this procedure when you need to inspect a rack location in the RMS/map view and confirm which tote the system says is associated with that rack, including comparison to the physical tote label when visible.

## Do Not Use For

* Do not use this procedure as a recovery procedure for a tote mismatch; this source segment does not provide corrective actions.
* Do not use this procedure to recover an empty rack condition; this source segment does not provide a recovery action when the rack is shown as empty.
* Do not use this procedure to remove AGVs or perform other control actions not described in this source.

## Safety And Operational Notes

* This source supports viewing and inspecting rack/container information in the RMS map.
* The broader training warns against taking unsupported control actions in the interface; this runbook is limited to inspection and comparison only.

## Access Or Tools Needed

* Access to the RMS/map view
* Container selection control
* Visibility of physical tote and rack labels if comparing system state to the floor

## Related Operational Context

* ctx_training_video_rack_location_map_reference_v1
* ctx_training_video_rack_click_tote_identity_v1

## Procedure Steps

### Step 1 — Open the RMS map and container selection view

**Responsible role:** operator

**Instruction:**
Open the RMS map and go to the container selection area so rack locations can be selected for inspection.

**Expected result:**
The container selection control and rack map are visible and ready for selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Screen area showing the container selection control and rack map.*

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Container Selection view and rack color indicators.*


**Stop or Escalate If:**

* Stop if you do not have access to the RMS/map view.
* Escalate if the container selection area needed for rack inspection is not available.

---

### Step 2 — Select the rack location to inspect

**Responsible role:** operator

**Instruction:**
Select the rack location on the map that you want to inspect.

**Expected result:**
The intended rack location is selected in the map view.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Rack locations in the map that can be clicked for more information.*


**Stop or Escalate If:**

* Stop if you cannot identify the intended rack position on the map.
* Escalate if the map does not allow the rack location to be selected.

---

### Step 3 — Click the dark blue rack to view associated information

**Responsible role:** operator

**Instruction:**
If the rack is dark blue, click the rack to view its associated information.

**Expected result:**
The system displays information for the selected rack, including the tote on that rack.

**Screens / Images:**

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Dark blue rack indicator meaning a tote is present.*

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Example of clicking a dark blue rack to inspect tote information.*

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Container selection screen showing dark blue tote-present and light blue empty rack states.*


**Stop or Escalate If:**

* Stop if the rack is shown as empty; this source does not provide a recovery action.
* Escalate if clicking a dark blue rack does not show the associated tote information.

---

### Step 4 — Read the tote identifier shown for the rack

**Responsible role:** operator

**Instruction:**
Read the tote identifier shown for that rack.

**Expected result:**
The tote identifier associated with the selected rack is visible to the operator.

**Screens / Images:**

![artifact_training_video_training_video_day1_0039_everything_else_oh_on_this_slide_primary_01_33_22_500](assets/da0cea32ab366bcb.jpg)

*Displayed tote number/identifier after selecting a location.*

![artifact_training_video_training_video_day1_0036_container_selection_so_you_may_have_primary_01_27_03_500](assets/ca29decebed3b78d.jpg)

*Selected location showing a box icon and tote number.*


**Stop or Escalate If:**

* Escalate if the selected dark blue rack does not display a tote identifier.

---

### Step 5 — Compare the displayed tote identifier to the physical tote label if needed

**Responsible role:** operator

**Instruction:**
If needed, compare the displayed tote identifier to the physical tote label seen at the rack location.

**Expected result:**
The operator determines whether the physical tote label matches the tote identifier shown in the map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Rack/tote lookup concept used to compare map state to physical labels.*


**Stop or Escalate If:**

* Escalate if the physical tote label does not match the tote shown in the map.

---

### Step 6 — Confirm the rack position label and map location naming

**Responsible role:** operator

**Instruction:**
Use the rack position label and map location naming to confirm you are checking the intended rack position.

**Expected result:**
The operator confirms the selected map location matches the intended physical rack position.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Rack location naming and selected rack position in the map.*


**Stop or Escalate If:**

* Stop if the rack position label does not match the map location you selected.
* Escalate if you cannot confidently confirm the intended rack position.

---

## Success Criteria

* The operator can select the intended rack in the RMS/container selection map view.
* For a dark blue rack, the system displays the tote associated with that rack.
* The operator can read and confirm the tote identifier shown for the selected rack.

## Failure Conditions

* The RMS/container selection view is not accessible.
* The intended rack location cannot be selected.
* The rack is shown as empty when a tote lookup is expected.
* Clicking a dark blue rack does not show tote information.
* The physical tote label does not match the tote shown in the map.
* The rack position label does not match the selected map location.

## Escalation Guidance

* If the physical tote label does not match the tote shown in the map, record the mismatch and escalate or continue with a source-backed recovery procedure from another source.
* If the rack is shown as empty, stop this procedure; this source does not provide a recovery action.
* If the interface does not show tote information for a dark blue rack, escalate for support review.

## Missing Details / Known Gaps

* The source does not provide a time estimate for this procedure.
* The source does not define a corrective action for a tote mismatch.
* The source does not define a recovery action when the rack is shown as empty.
* The source does not specify production stop or LOTO requirements for this inspection activity.
* The source does not define role boundaries beyond operator-level use of the view.

## Source Lineage

- Candidate IDs: candidate_training_video_view_tote_associated_to_rack
- Source ID: `training_video_day1`
- Source Type: `training_video`
