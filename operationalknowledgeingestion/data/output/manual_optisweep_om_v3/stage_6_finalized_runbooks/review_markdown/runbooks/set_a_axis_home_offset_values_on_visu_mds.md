# Set A-axis home offset values on the Visu_MDs screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_set_a_axis_home_offset_values_on_the_visu_mds_screen_v1` |
| Title | Set A-axis home offset values on the Visu_MDs screen |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

This commissioning procedure updates the A-axis Home Offset setting by navigating to the Visu_MDs screen, entering the previously recorded value into the New Value column for each A-axis, and pressing UPDATE to confirm the change.

## When To Use

Use during tipper commissioning when the previously recorded Home Offset value for each A-axis must be entered on the Visu_MDs screen.

## Do Not Use For

* Do not use this runbook to determine or calculate the Home Offset value; this procedure requires a value recorded in a previous procedure.
* Do not use this runbook for Z-axis home settings or other commissioning procedures.

## Safety And Operational Notes

* This procedure changes commissioning settings for A-axis home offsets.
* The source does not provide recovery or escalation steps if the value cannot be entered or confirmed.

## Access Or Tools Needed

* Access to the Visu_MDs screen
* F2 input/control
* Previously recorded Home Offset value from the previous procedure

## Procedure Steps

### Step 1 — Open the Visu_MDs screen

**Responsible role:** L2_support

**Instruction:**
Navigate to the "Visu_MDs" screen using F2.

**Expected result:**
The Visu_MDs screen is displayed and ready for parameter entry.

**Screens / Images:**

![artifact_page_203_image_2](assets/artifact_page_203_image_2.jpeg)

*Screen context near the A-axis home settings procedure and the Visu_MDs-related commissioning view.*

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*Operator station HMI reference showing that Visu_MDs is accessed using F2.*


**Stop or Escalate If:**

* The Visu_MDs screen cannot be accessed.

---

### Step 2 — Enter the recorded Home Offset value for an A-axis

**Responsible role:** L2_support

**Instruction:**
For an A-axis, locate the "Home Offset" setting and enter the value recorded in the previous procedure into the "New Value" column.

**Expected result:**
The recorded Home Offset value is entered in the New Value column for the selected A-axis.

**Screens / Images:**

![artifact_page_203_image_2](assets/artifact_page_203_image_2.jpeg)

*Area of the Visu_MDs-related screen context associated with A-axis Home Offset entry.*


**Stop or Escalate If:**

* The previously recorded Home Offset value is not available.
* The Home Offset field for the A-axis cannot be found.
* The value cannot be entered into the New Value column.

---

### Step 3 — Update the setting

**Responsible role:** L2_support

**Instruction:**
Press UPDATE to confirm the change.

**Expected result:**
The entered Home Offset value is confirmed on the Visu_MDs screen.

**Screens / Images:**

![artifact_page_203_image_2](assets/artifact_page_203_image_2.jpeg)

*Visu_MDs-related screen context associated with confirming the Home Offset change.*


**Stop or Escalate If:**

* The UPDATE action does not confirm the change.

---

### Step 4 — Repeat for the other A-axis if needed

**Responsible role:** L2_support

**Instruction:**
Repeat the entry and update for the other A-axis if needed.

**Expected result:**
Each applicable A-axis has its previously recorded Home Offset value entered and confirmed.

**Screens / Images:**

![artifact_page_203_image_2](assets/artifact_page_203_image_2.jpeg)

*A-axis home settings context for repeating the same update on the other A-axis.*


**Stop or Escalate If:**

* The second applicable A-axis cannot be updated using the same process.

---

## Success Criteria

* The previously recorded Home Offset value is entered and confirmed for each applicable A-axis on the Visu_MDs screen.

## Failure Conditions

* The Visu_MDs screen cannot be accessed.
* The previously recorded Home Offset value is unavailable.
* The Home Offset value cannot be entered in the New Value column.
* The change cannot be confirmed with UPDATE.

## Escalation Guidance

* The source does not provide recovery or escalation steps if the value cannot be entered or confirmed.
* Escalate for SME review if the required previously recorded Home Offset value is unavailable or the change cannot be confirmed.

## Missing Details / Known Gaps

* The source section text is not included in the packet; step wording is grounded from the candidate and artifact retrieval text.
* The source does not specify exact confirmation indicators after pressing UPDATE.
* The source does not provide troubleshooting, rollback, or recovery steps.
* The source does not specify whether production stop or LOTO is required.
* The source does not provide a time estimate for completing this procedure.

## Source Lineage

- Candidate IDs: set_a_axis_home_offset_values_on_visu_mds
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
