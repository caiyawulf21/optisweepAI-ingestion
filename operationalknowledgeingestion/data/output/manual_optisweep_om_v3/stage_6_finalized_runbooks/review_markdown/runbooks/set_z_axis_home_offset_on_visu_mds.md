# Set Z-axis home position using the Home Offset field

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_set_z_axis_home_position_using_the_home_offset_field_v1` |
| Title | Set Z-axis home position using the Home Offset field |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Visu_MDs screen (F2) to enter the previously recorded Z-axis position value into the Home Offset setting for each Z-axis, then confirm each change with UPDATE.

## When To Use

Use during tipper commissioning when the previously recorded Z-axis position values are available and need to be entered as the Home Offset for each Z-axis on the Visu_MDs screen.

## Do Not Use For

* Do not use when the previously recorded Z-axis position values are not available.
* Do not use if the Visu_MDs screen, Home Offset setting, New Value column, or UPDATE control is not available as described.

## Safety And Operational Notes

* This procedure depends on previously recorded Z-axis position values from the prior procedure.
* Stop and escalate if the HMI elements needed for this procedure are not available as described.

## Access Or Tools Needed

* Access to the HMI
* Visu_MDs screen (F2)
* Previously recorded Z-axis position values for each tipper

## Procedure Steps

### Step 1 — Open the Visu_MDs screen

**Responsible role:** L2_support

**Instruction:**
Navigate to the "Visu_MDs" screen using F2.

**Expected result:**
The Visu_MDs screen is displayed and the Home Offset setting area is available for review.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Overall Visu_MDs machine data screen layout for axis parameter editing.*

![artifact_page_194_image_2](assets/artifact_page_194_image_2.jpeg)

*Operator station HMI reference for accessing the Visu_MDs screen using F2.*

![artifact_page_205_image_2](assets/artifact_page_205_image_2.jpeg)

*Screen or nearby artifact support for the Visu_MDs page with Home Offset and UPDATE workflow.*

![artifact_page_205_image_3](assets/artifact_page_205_image_3.png)

*Screen or nearby artifact support for the Visu_MDs page with Home Offset and UPDATE workflow.*


**Stop or Escalate If:**

* The Visu_MDs screen is not available.
* The Home Offset setting or New Value column is not available as described.

---

### Step 2 — Enter the recorded Home Offset value for one Z-axis

**Responsible role:** L2_support

**Instruction:**
For one Z-axis, locate the "Home Offset" setting and enter the value recorded in the previous procedure into the "New Value" column.

**Expected result:**
The recorded value is entered into the New Value column for the selected Z-axis Home Offset setting.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Axis parameter rows and editable machine data fields on the Visu_MDs screen.*

![artifact_page_205_image_2](assets/artifact_page_205_image_2.jpeg)

*Nearby artifact support for the Home Offset entry workflow on the Visu_MDs screen.*

![artifact_page_205_image_3](assets/artifact_page_205_image_3.png)

*Nearby artifact support for the Home Offset entry workflow on the Visu_MDs screen.*


**Stop or Escalate If:**

* The previously recorded Z-axis position value is not available.
* The Home Offset setting or New Value column is not available as described.

---

### Step 3 — Confirm the change with UPDATE

**Responsible role:** L2_support

**Instruction:**
Press UPDATE to confirm the change.

**Expected result:**
The entered Home Offset value is confirmed on the HMI.

**Screens / Images:**

![artifact_page_205_image_2](assets/artifact_page_205_image_2.jpeg)

*Nearby artifact support for the UPDATE control used to confirm the Home Offset change.*

![artifact_page_205_image_3](assets/artifact_page_205_image_3.png)

*Nearby artifact support for the UPDATE control used to confirm the Home Offset change.*


**Stop or Escalate If:**

* The UPDATE control is not available as described.
* The change cannot be confirmed on the HMI.

---

### Step 4 — Repeat for the other Z-axis

**Responsible role:** L2_support

**Instruction:**
Repeat the Home Offset entry and UPDATE action for the other Z-axis.

**Expected result:**
Both Z-axes have their recorded Home Offset values entered and confirmed.

**Screens / Images:**

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Multiple axis parameter areas on the Visu_MDs screen for applying the same workflow to the other Z-axis.*

![artifact_page_205_image_2](assets/artifact_page_205_image_2.jpeg)

*Nearby artifact support for repeating the Home Offset and UPDATE workflow for each Z-axis.*

![artifact_page_205_image_3](assets/artifact_page_205_image_3.png)

*Nearby artifact support for repeating the Home Offset and UPDATE workflow for each Z-axis.*


**Stop or Escalate If:**

* The recorded value for the other Z-axis is not available.
* The Home Offset setting, New Value column, or UPDATE control is not available for the other Z-axis.

---

## Success Criteria

* The recorded Z-axis position value is entered as the Home Offset for each Z-axis.
* Each Home Offset change is confirmed with UPDATE.

## Failure Conditions

* Previously recorded Z-axis position values are not available.
* The Visu_MDs screen is not available.
* The Home Offset setting is not available as described.
* The New Value column is not available as described.
* The UPDATE control is not available as described.

## Escalation Guidance

* Stop and escalate for support if the previously recorded Z-axis position values are not available.
* Stop and escalate for support if the Visu_MDs screen, Home Offset setting, New Value column, or UPDATE control is not available as described.

## Missing Details / Known Gaps

* The source packet does not provide the exact recorded Z-axis position values to enter.
* The source section text for page 205 is empty in the packet, so step wording is grounded from the candidate and nearby artifact retrieval text.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: set_z_axis_home_offset_on_visu_mds
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
