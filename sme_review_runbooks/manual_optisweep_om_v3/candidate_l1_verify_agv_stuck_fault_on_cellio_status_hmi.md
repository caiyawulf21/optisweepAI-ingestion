# Verify AGV Stuck Fault on the CellIO Status HMI Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_agv_stuck_fault_on_cellio_status_hmi_v1` |
| Title | Verify AGV Stuck Fault on the CellIO Status HMI Screen |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI to verify the documented AGV Stuck condition by navigating to the Visu_ManControl screen, opening CellIO Status, selecting the affected tipper, and confirming that OUT Fault Status is 82.

## When To Use

Use this procedure when an AGV remains at the tipper after tote-tipping is complete and the source procedure calls for HMI verification of the AGV Stuck non-recoverable fault condition.

## Do Not Use For

* Do not use this runbook to perform recovery actions such as forcing OUT W1 values; this runbook covers verification only.
* Do not use this runbook to interpret undocumented fault values beyond confirming whether OUT Fault Status equals 82.

## Safety And Operational Notes

* This source-specific runbook is limited to HMI verification and does not include physical intervention.
* The source describes this as a non-recoverable fault condition associated with an AGV remaining at the tipper after tote-tipping is complete, likely due to a communication issue.

## Access Or Tools Needed

* Operator station HMI
* Access to the "Visu_ManControl" screen
* "CellIO Status" button/view

## Related Operational Context

* ctx_manual_agv_stuck_fault_overview_v1
* ctx_manual_visu_mancontrol_cellio_status_screen_v1
* ctx_manual_out_fault_status_82_v1

## Procedure Steps

### Step 1 — Navigate to the Visu_ManControl screen

**Responsible role:** L1_support

**Instruction:**
Go to the operator station HMI and navigate to the "Visu_ManControl" screen.

**Expected result:**
The Visu_ManControl screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*Use the manual control screen reference to identify the Visu_ManControl layout and the area where CellIO Status access is available.*

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*Look for the operator station screen context associated with the AGV Stuck verification procedure.*


**Stop or Escalate If:**

* Stop if the operator station HMI is not accessible.
* Escalate if the Visu_ManControl screen cannot be identified or opened.

---

### Step 2 — Open CellIO Status

**Responsible role:** L1_support

**Instruction:**
Press the "CellIO Status" button.

**Expected result:**
The CellIO Status view opens from the Visu_ManControl screen.

**Screens / Images:**

![artifact_fig_4_23_operator_station_hmi_manual_control_screen](assets/artifact_fig_4_23_operator_station_hmi_manual_control_screen.jpeg)

*Locate the CellIO Status access on the Visu_ManControl screen.*

![artifact_page_87_image_3](assets/artifact_page_87_image_3.jpeg)

*Use the page 87 AGV Stuck procedure screen artifact for the CellIO Status verification context.*


**Stop or Escalate If:**

* Stop if the CellIO Status button cannot be found.
* Escalate if the CellIO Status view does not open after pressing the button.

---

### Step 3 — Select the affected tipper

**Responsible role:** L1_support

**Instruction:**
Select the tipper where the AGV is stuck.

**Expected result:**
The affected tipper is selected in the CellIO Status view.

**Screens / Images:**

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*Use the AGV Stuck procedure screen artifact to identify the tipper selection context.*

![artifact_page_87_image_3](assets/artifact_page_87_image_3.jpeg)

*Look for the HMI area associated with selecting the affected tipper.*


**Stop or Escalate If:**

* Stop if the correct tipper cannot be identified or selected.

---

### Step 4 — Verify OUT Fault Status equals 82

**Responsible role:** L1_support

**Instruction:**
Check the "OUT Fault Status" field for the selected tipper and verify that the value is 82.

**Expected result:**
The user confirms whether the selected tipper shows OUT Fault Status value 82.

**Screens / Images:**

![artifact_page_87_image_2](assets/artifact_page_87_image_2.jpeg)

*Look for the OUT Fault Status field location associated with the selected tipper.*

![artifact_page_87_image_3](assets/artifact_page_87_image_3.jpeg)

*Use the page 87 AGV Stuck screen artifact to identify where the OUT Fault Status value is displayed.*


**Stop or Escalate If:**

* Escalate if the observed OUT Fault Status does not match the documented value of 82.
* Escalate if the OUT Fault Status field cannot be read or verified.

---

## Success Criteria

* The operator station HMI is used to navigate to Visu_ManControl and open CellIO Status.
* The affected tipper is selected.
* OUT Fault Status is successfully checked for the selected tipper.
* The verification result is determined based on whether the displayed value is 82.

## Failure Conditions

* The operator station HMI or required screen cannot be accessed.
* The CellIO Status button or view cannot be opened.
* The correct tipper cannot be identified or selected.
* OUT Fault Status does not equal 82.
* The displayed fault status cannot be read or verified.

## Escalation Guidance

* Escalate if the correct tipper cannot be identified or selected.
* Escalate if the observed OUT Fault Status does not match the documented value of 82.
* Escalate if the HMI does not provide access to the required Visu_ManControl or CellIO Status views.
* Do not apply undocumented fault interpretation within this runbook.

## Missing Details / Known Gaps

* The source packet does not provide an estimated completion time.
* The source packet does not specify whether production stop is required for this verification-only procedure.
* The source packet does not specify whether LOTO is required.
* The source packet does not provide explicit role boundaries beyond the candidate's L1_support designation.
* The source packet does not include explicit screen coordinates or control locations for tipper selection or the OUT Fault Status field.

## Source Lineage

- Candidate IDs: candidate_l1_verify_agv_stuck_fault_on_cellio_status_hmi
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
