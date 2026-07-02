# Identify Main Components At The Operator Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_main_components_at_the_operator_station_v1` |
| Title | Identify Main Components At The Operator Station |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station overview, Figure 3-1, and Table 3-1 from the manual to locate and identify the documented operator station components in the area where an operator receives parcels from the tippers.

## When To Use

Use this reference procedure when a user needs to visually identify the documented operator station components and compare the physical station to the manual's listed features.

## Do Not Use For

* Do not use this procedure to operate the HMI.
* Do not use this procedure to operate the push-buttons.
* Do not infer component names or locations beyond what is stated in the section text, Figure 3-1 metadata, and Table 3-1.

## Safety And Operational Notes

* This runbook is a visual identification reference only.
* Do not infer component names or locations beyond what is stated in the source.
* Escalate if the physical station does not match the documented feature list or figure.

## Access Or Tools Needed

* Physical access or visual access to the operator station
* Figure 3-1 Operator Station (Panels Removed for Clarity)
* Table 3-1 Operator Station Features

## Related Operational Context

* ctx_manual_operator_station_overview_v1
* ctx_manual_operator_station_component_reference_v1
* ctx_manual_operator_station_hmi_reference_v1
* ctx_manual_hospital_station_stacklight_reference_v1

## Procedure Steps

### Step 1 — Go to the operator station area

**Responsible role:** operator

**Instruction:**
Go to the operator station, defined by the manual as the area where an operator receives parcels from the tippers.

**Expected result:**
You are positioned at the documented operator station area.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Overall operator station layout and the area where the main components are shown together.*


**Stop or Escalate If:**

* The physical area does not match the documented operator station description.

---

### Step 2 — Identify the two tippers

**Responsible role:** operator

**Instruction:**
Identify the two tippers at the operator station using the documented feature list and Figure 3-1.

**Expected result:**
Two tippers are identified at the operator station.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The tipper locations in the overall operator station view.*

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Tipper assembly appearance and labeled tipper components for supplemental identification.*


**Stop or Escalate If:**

* Two tippers are not present.
* The physical station does not match the documented feature list or figure.

---

### Step 3 — Locate the chute

**Responsible role:** operator

**Instruction:**
Locate the chute at the operator station using Figure 3-1 and the Table 3-1 feature list.

**Expected result:**
The chute is identified at the operator station.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The chute area in the operator station reference photo.*


**Stop or Escalate If:**

* The chute cannot be identified.
* The physical station does not match the documented feature list or figure.

---

### Step 4 — Locate the two stacklights

**Responsible role:** operator

**Instruction:**
Locate the two stacklights mounted on the top of the frame on either side of the chute.

**Expected result:**
Two stacklights are identified in the documented mounting positions.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The top of the frame on either side of the chute where the two stacklights are documented.*


**Stop or Escalate If:**

* Two stacklights are not visible in the documented positions.
* The physical station does not match the documented feature list or figure.

---

### Step 5 — Identify the plastic curtains

**Responsible role:** operator

**Instruction:**
Identify the plastic curtains at the operator station using Figure 3-1 and Table 3-1.

**Expected result:**
The plastic curtains are identified.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The plastic curtain position in the operator station reference photo.*


**Stop or Escalate If:**

* The plastic curtains cannot be identified.
* The physical station does not match the documented feature list or figure.

---

### Step 6 — Locate the operator station HMI

**Responsible role:** operator

**Instruction:**
Locate the operator station HMI using Figure 3-1 and Table 3-1. This step is for identification only, not operation.

**Expected result:**
The operator station HMI is identified.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The operator station HMI location in the overall station view.*

![artifact_fig_4_20_operator_station_hmi_data_screen](assets/artifact_fig_4_20_operator_station_hmi_data_screen.png)

*Supplemental example of an operator station HMI screen layout.*

![artifact_fig_4_26_operator_station_hmi_machine_data_screen](assets/artifact_fig_4_26_operator_station_hmi_machine_data_screen.png)

*Supplemental example of an operator station HMI screen layout.*


**Stop or Escalate If:**

* The operator station HMI cannot be identified.
* The physical station does not match the documented feature list or figure.

---

### Step 7 — Locate the push-buttons

**Responsible role:** operator

**Instruction:**
Locate the push-buttons at the operator station and verify that the section states there are four push-buttons.

**Expected result:**
The push-buttons are identified and the documented quantity is recognized as four.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The push-button area in the operator station reference photo.*


**Stop or Escalate If:**

* The push-buttons cannot be identified.
* The physical station does not match the documented feature list or figure.

---

### Step 8 — Identify the rotary station

**Responsible role:** operator

**Instruction:**
Identify the rotary station at the operator station using Figure 3-1 and, if needed, the supplemental rotary station figure.

**Expected result:**
The rotary station is identified.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*The rotary station location in the overall operator station view.*

![artifact_fig_3_2_rotary_station](assets/artifact_fig_3_2_rotary_station.png)

*Supplemental rotary station photo for component recognition.*


**Stop or Escalate If:**

* The rotary station cannot be identified.
* The physical station does not match the documented feature list or figure.

---

### Step 9 — Compare observed components to Table 3-1

**Responsible role:** operator

**Instruction:**
Compare the observed components to Table 3-1 to verify that the station features match the documented list: tipper, chute, stacklight, plastic curtain, operator station HMI, push-buttons, and rotary station.

**Expected result:**
The observed operator station components match the documented feature list.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Overall station layout for comparison against the documented feature list.*


**Stop or Escalate If:**

* The physical station does not match the documented feature list or figure.

---

## Success Criteria

* The user can identify the documented operator station components: tipper, chute, stacklight, plastic curtain, operator station HMI, push-buttons, and rotary station.
* The observed station features match the documented list in Table 3-1 and the layout shown in Figure 3-1.

## Failure Conditions

* The physical station does not match the documented feature list or figure.
* A listed component cannot be identified from the physical station and supplied source evidence.
* The user must infer component names or locations beyond what is stated in the source.

## Escalation Guidance

* Escalate if the physical station does not match the documented feature list or figure.
* Escalate if any listed component cannot be confidently identified using the supplied source evidence.
* Do not infer undocumented component names, locations, or functions.

## Missing Details / Known Gaps

* The source packet does not provide an estimated completion time.
* The source packet does not state whether production stop is required.
* The source packet does not state whether LOTO is required.
* The source packet does not provide detailed role boundaries beyond operator use.
* The source packet does not provide the full OCR text of section 3.2 on page 24 in source_sections.text.

## Source Lineage

- Candidate IDs: candidate_operator_station_identify_main_components
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
