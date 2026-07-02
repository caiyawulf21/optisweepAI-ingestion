# View Cell QR Code And Identify Station Details From Cell Selection

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_cell_qr_code_and_identify_station_details_from_cell_selection_v1` |
| Title | View Cell QR Code And Identify Station Details From Cell Selection |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the cell selection view in the OptiSweep map interface to select a map cell, read the displayed 8-digit cell code (also described as the QR code or node code), and determine whether the selected cell is a station by checking whether it is an orange cell and whether workstation ID information is shown.

## When To Use

Use this reference procedure when support personnel need to identify a selected map cell's unique 8-digit cell code and determine whether the selected cell is a station with workstation ID information shown in the cell details view.

## Do Not Use For

* Do not use this procedure to interpret design-oriented map detail fields as primary troubleshooting indicators when the source says support should focus mainly on node code and workstation ID.
* Do not assume a cell has multiple cell code values; the source describes the cell code as unique.

## Safety And Operational Notes

* This source segment is instructional/reference-oriented and does not describe a control action on equipment.
* Support should focus primarily on the node code/cell code and workstation ID fields called out in the source.

## Access Or Tools Needed

* Access to the cell selection view in the map interface
* Visual access to the selected cell information panel

## Related Operational Context

* ctx_training_video_cell_selection_qr_code_v1
* ctx_training_video_station_cell_workstation_id_v1
* ctx_training_video_cell_code_unique_identifier_v1
* ctx_training_video_support_relevance_of_cell_fields_v1

## Procedure Steps

### Step 1 — Open or use cell selection view

**Responsible role:** L1_support

**Instruction:**
Open the map interface and use the cell selection view so that cell information can be displayed when a map cell is selected.

**Expected result:**
Cell selection is active and the interface is ready for a cell click.

**Screens / Images:**

![artifact_training_video_training_video_day1_0046_all_right_the_next_object_is_primary_01_42_16_500](assets/e896cf332f19ee2a.jpg)

*Cell selection screen/frame and the selected cell information panel.*


**Stop or Escalate If:**

* The map interface does not allow cell selection.
* The selected cell information panel is not visible after entering cell selection.

---

### Step 2 — Select a map cell

**Responsible role:** L1_support

**Instruction:**
Click on a cell in the map to display its cell information.

**Expected result:**
The selected cell's information appears in the cell details area.

**Screens / Images:**

![artifact_training_video_training_video_day1_0046_all_right_the_next_object_is_primary_01_42_16_500](assets/e896cf332f19ee2a.jpg)

*The selected cell and the details panel that appears after clicking it.*


**Stop or Escalate If:**

* Cell information does not appear after selecting a cell.
* The selected cell cannot be matched to a displayed details panel.

---

### Step 3 — Read the 8-digit cell code

**Responsible role:** L1_support

**Instruction:**
Read the displayed 8-digit number and treat it as the cell code for that location. The source also refers to this value as the QR code or node code.

**Expected result:**
A single 8-digit cell code is identified for the selected location.

**Screens / Images:**

![artifact_training_video_training_video_day1_0046_all_right_the_next_object_is_primary_01_42_16_500](assets/e896cf332f19ee2a.jpg)

*The QR code/node code field showing the 8-digit cell code.*


**Stop or Escalate If:**

* No 8-digit code is shown for the selected cell.
* There is ambiguity about the code value for the selected location.

---

### Step 4 — Determine whether the cell is a station

**Responsible role:** L1_support

**Instruction:**
Check whether the selected cell is an orange cell, because the source states orange cells are stations.

**Expected result:**
The user determines whether the selected cell is a station.

**Screens / Images:**

![artifact_training_video_training_video_day1_0046_all_right_the_next_object_is_primary_01_42_16_500](assets/e896cf332f19ee2a.jpg)

*Orange station cells on the map.*


**Stop or Escalate If:**

* The cell color is not visible or cannot be interpreted.
* The interface does not clearly indicate whether the selected cell is orange.

---

### Step 5 — Check for workstation ID on station cells

**Responsible role:** L1_support

**Instruction:**
If the selected cell is a station cell, look for the additional workstation ID information shown in the cell details panel.

**Expected result:**
For a station cell, workstation ID information is identified in the details panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0046_all_right_the_next_object_is_primary_01_42_16_500](assets/e896cf332f19ee2a.jpg)

*The station cell details panel showing additional information including workstation ID.*


**Stop or Escalate If:**

* An orange station cell does not show workstation ID information.
* The details panel appears inconsistent with the selected station cell.

---

### Step 6 — Use the cell code when communicating the destination

**Responsible role:** L1_support

**Instruction:**
Use the displayed cell code when communicating a destination cell to an operator, as described in the training example.

**Expected result:**
The destination location is communicated using the displayed unique cell code.

**Screens / Images:**

![artifact_training_video_training_video_day1_0046_all_right_the_next_object_is_primary_01_42_16_500](assets/e896cf332f19ee2a.jpg)

*The displayed node code/QR code used as the location identifier.*


**Stop or Escalate If:**

* The displayed cell code cannot be read clearly enough to communicate.
* There is uncertainty about whether the displayed code matches the intended destination cell.

---

## Success Criteria

* The selected map cell's 8-digit cell code is identified from the cell details view.
* The user can determine whether the selected cell is a station based on the orange cell indication.
* If the selected cell is a station, the workstation ID information is identified.

## Failure Conditions

* Cell selection does not display cell information.
* The 8-digit cell code is not visible or is ambiguous.
* Station status cannot be determined from the selected cell.
* A selected orange station cell does not show the expected workstation ID information.
* Support personnel focus on non-primary design-oriented fields instead of the node code and workstation ID emphasized by the source.

## Escalation Guidance

* Escalate for SME review if the selected cell does not show the expected QR code/node code information.
* Escalate for SME review if an orange station cell does not show workstation ID information.
* Escalate if map details appear inconsistent and the issue depends on design-oriented fields the source says are not normally the support focus.

## Missing Details / Known Gaps

* The source does not provide a precise navigation path for opening the cell selection view.
* The source does not provide a formal escalation owner or team.
* The source does not provide a time estimate for completing this reference task.
* The source does not enumerate all fields shown in the cell details panel beyond emphasizing node code and workstation ID as the main support-relevant items.

## Source Lineage

- Candidate IDs: candidate_training_video_view_cell_qr_code_and_station_details
- Source ID: `training_video_day1`
- Source Type: `training_video`
