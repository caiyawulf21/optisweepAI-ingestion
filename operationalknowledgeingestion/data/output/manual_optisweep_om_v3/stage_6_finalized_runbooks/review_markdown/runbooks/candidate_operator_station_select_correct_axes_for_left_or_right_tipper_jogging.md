# Select the Correct Axis Controls for Left or Right Tipper Jogging

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_select_correct_axis_controls_for_left_or_right_tipper_jogging_v1` |
| Title | Select the Correct Axis Controls for Left or Right Tipper Jogging |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented operator station axis mapping to choose the correct A and Z axis pair before jogging a tote position. The source states that A1 and Z1 are used for the left axis, and A2 and Z2 are used for the right tipper.

## When To Use

Use this reference when working at the operator station HMI to select the correct axis controls before jogging for tote repositioning or manual jog mode tasks where the screen shows Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis.

## Do Not Use For

* Do not use undocumented axis mappings.
* Do not use this runbook as a complete jogging or fault-recovery procedure; the source here provides axis assignment only.

## Safety And Operational Notes

* Use only the documented axis assignment from the source.
* If the screen labeling is unclear, stop and escalate rather than using an undocumented mapping.

## Access Or Tools Needed

* Access to the operator station HMI
* MCP_Dual screen
* Visibility of Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis labels
* Documented left/right axis mapping

## Related Operational Context

* ctx_manual_operator_station_hmi_reference_v1

## Procedure Steps

### Step 1 — Open the operator station screen and locate the axis labels

**Responsible role:** operator

**Instruction:**
Open the operator station MCP_Dual screen and locate the axis labels Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis.

**Expected result:**
The operator station screen displays the four axis labels needed for selection.

**Screens / Images:**

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Manual mode axis controls on the operator station HMI, including Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Screen snippet showing the axis labels and control layout.*

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*HMI view showing the four axis labels in the operator station screen.*


**Stop or Escalate If:**

* The screen does not show Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis.
* The screen labeling is unclear.

---

### Step 2 — Identify whether the jog action is for the left axis or right tipper

**Responsible role:** operator

**Instruction:**
Identify whether the jog action is being performed for the left axis or the right tipper.

**Expected result:**
The operator has determined whether the intended jog target is the left axis or the right tipper.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*Left and right tipper axis control groupings on the manual jogging screen.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Manual jog mode interface context where the axis selection is applied.*


**Stop or Escalate If:**

* It is not clear whether the jog action is for the left axis or the right tipper.

---

### Step 3 — Select A1 and Z1 for the left axis

**Responsible role:** operator

**Instruction:**
For the left axis, select A1 and Z1 as the documented controls.

**Expected result:**
The left-axis jog selection uses A1 and Z1.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*A1 AXIS and Z1 AXIS controls associated with the left tipper.*

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*Manual jog mode interface showing A1 and Z1 among the available axis labels.*


**Stop or Escalate If:**

* A1 and Z1 are not available for selection when the left axis is intended.
* The screen labeling does not support confirming the left-axis assignment.

---

### Step 4 — Select A2 and Z2 for the right tipper

**Responsible role:** operator

**Instruction:**
For the right tipper, select A2 and Z2 as the documented controls.

**Expected result:**
The right-tipper jog selection uses A2 and Z2.

**Screens / Images:**

![artifact_page_83_image_10](assets/artifact_page_83_image_10.png)

*A2 AXIS and Z2 AXIS controls associated with the right tipper.*

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*Manual jog mode interface showing A2 and Z2 among the available axis labels.*


**Stop or Escalate If:**

* A2 and Z2 are not available for selection when the right tipper is intended.
* The screen labeling does not support confirming the right-tipper assignment.

---

### Step 5 — Verify the selected axis labels match the documented assignment before jogging

**Responsible role:** operator

**Instruction:**
Before jogging, verify that the selected axis labels on the screen match the documented left or right assignment.

**Expected result:**
The selected axis pair matches the documented mapping for the intended side before any jog movement is performed.

**Screens / Images:**

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*Manual jog mode interface example used when clearing operator station motor faults and repositioning a tote.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Manual jog mode reference showing the axis labels and jog context.*


**Stop or Escalate If:**

* The selected axis labels do not match the documented assignment.
* The screen labeling is unclear.
* Only an undocumented mapping appears possible.

---

## Success Criteria

* The operator selects the documented A and Z axis pair that matches the intended left axis or right tipper.
* The on-screen labels are verified before jogging.
* No undocumented axis mapping is used.

## Failure Conditions

* The required axis labels are not visible on the screen.
* The operator cannot determine whether the jog action is for the left axis or the right tipper.
* The selected axis pair does not match the documented mapping.
* The screen labeling is unclear.
* An undocumented axis mapping would be required.

## Escalation Guidance

* Stop and escalate if the screen labeling is unclear.
* Stop and escalate if the required axis labels are not visible.
* Stop and escalate if the intended left/right assignment cannot be determined from the available source-backed information.
* Do not proceed using undocumented axis mappings.

## Missing Details / Known Gaps

* The source does not define how to determine left versus right beyond the stated mapping.
* The source does not provide additional correction steps if the screen labeling is unclear.
* The source does not provide a time estimate for this reference procedure.
* The source does not state whether production stop or LOTO is required for this reference activity.

## Source Lineage

- Candidate IDs: candidate_operator_station_select_correct_axes_for_left_or_right_tipper_jogging
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
