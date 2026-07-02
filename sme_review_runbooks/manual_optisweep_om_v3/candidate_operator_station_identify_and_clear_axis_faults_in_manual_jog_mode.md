# Identify Axis Faults and Clear Them in Manual Jog Mode on the Operator Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_axis_faults_and_clear_them_in_manual_jog_mode_on_the_operator_station_v1` |
| Title | Identify Axis Faults and Clear Them in Manual Jog Mode on the Operator Station |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station MCP_Dual screen in manual jog mode to identify whether Z1, Z2, A1, or A2 shows a fault and clear the displayed fault with RESET.

## When To Use

Use when the operator needs to check the operator station manual jog display for axis fault presence on Z1, Z2, A1, or A2 and perform the documented RESET action to clear a displayed fault.

## Do Not Use For

* Do not use this procedure to interpret the meaning of a fault beyond the displayed Fault indication.
* Do not use this procedure as a complete recovery procedure when additional recovery steps are required after fault clearing.
* Do not use this procedure for diagnostics not shown on the operator station HMI axis display.

## Safety And Operational Notes

* This runbook is source-supported as part of a documented recovery sequence and is limited to identifying displayed axis faults and using RESET to clear them.
* The source does not provide additional diagnostic interpretation if the fault indication remains after RESET.
* Do not infer fault meanings beyond the displayed Fault indication described in the source.

## Access Or Tools Needed

* Access to the operator station HMI
* MCP_Dual screen (F3)
* JOG control
* RESET control
* Visibility of Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis indicators
* Manual Mode indication
* Fault indication on the HMI

## Related Operational Context

* ctx_manual_operator_station_hmi_reference_v1
* ctx_manual_estop_reset_reference_v1

## Procedure Steps

### Step 1 — Open the MCP_Dual operator station screen

**Responsible role:** operator

**Instruction:**
Navigate to the operator station MCP_Dual screen using F3.

**Expected result:**
The MCP_Dual operator station screen is displayed.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*F3 mapping to the operator station MCP_Dual/Visu_MCP_Dual screen.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Operator station HMI layout associated with the non-recoverable fault recovery context.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Axis display area and RESET-related HMI elements on the operator station screen.*


**Stop or Escalate If:**

* The MCP_Dual screen cannot be reached using F3.
* The operator station HMI is unavailable or does not show the expected control screen.

---

### Step 2 — Enter manual jog mode

**Responsible role:** operator

**Instruction:**
Press JOG to enter manual jog mode and verify the Manual Mode indication is shown.

**Expected result:**
The HMI enters manual jog mode and shows Manual Mode.

**Screens / Images:**

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Manual Mode indication and axis control area.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Manual Mode text and axis display region.*

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*Manual jog mode interface example.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Manual jog mode reference used during fault recovery.*


**Stop or Escalate If:**

* JOG does not open manual jog mode.
* Manual Mode indication is not shown after pressing JOG.

---

### Step 3 — Inspect the axis indicators

**Responsible role:** operator

**Instruction:**
Inspect the displayed axis indicators for Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis.

**Expected result:**
The operator can see the four axis indicators on the display.

**Screens / Images:**

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Axis labels and control area for Z1, Z2, A1, and A2.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Axis labels and fault-related display elements.*

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*Manual jog mode interface showing the axis indicators.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Axis display area referenced in the fault recovery procedure.*


**Stop or Escalate If:**

* The required axis indicators are not visible on the HMI.
* The operator cannot determine which displayed indicators correspond to Z1, Z2, A1, and A2.

---

### Step 4 — Check for a Fault indication on any axis

**Responsible role:** operator

**Instruction:**
Check whether any axis shows a Fault indication.

**Expected result:**
The operator determines whether a Fault indication is present on any of the four axes.

**Screens / Images:**

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Fault indication in the axis area.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Manual mode axis controls and any visible Fault status.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Manual jog mode reference for checking whether Z1, Z2, A1, or A2 shows a fault.*


**Stop or Escalate If:**

* The HMI display is unclear and fault status cannot be determined.
* A fault is shown and does not match the limited source-supported handling in this runbook.

---

### Step 5 — Press RESET to clear a displayed axis fault

**Responsible role:** operator

**Instruction:**
If an axis shows a fault, press RESET to clear the fault.

**Expected result:**
The RESET action is issued for the displayed axis fault condition.

**Screens / Images:**

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*RESET control on the operator station HMI.*

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*RESET instruction and nearby axis/fault display elements.*

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*Manual jog mode interface used when clearing operator station motor faults.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*RESET context in the manual jog mode fault recovery reference.*


**Stop or Escalate If:**

* RESET does not clear the displayed fault.
* The RESET control is unavailable.
* The source-supported procedure does not provide further interpretation or corrective action after RESET fails.

---

### Step 6 — Confirm the fault indication is cleared

**Responsible role:** operator

**Instruction:**
Confirm whether the fault indication is no longer shown on the affected axis.

**Expected result:**
The operator determines whether the affected axis no longer shows Fault.

**Screens / Images:**

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Axis area where Fault should no longer be shown after RESET.*

![artifact_page_85_image_10](assets/artifact_page_85_image_10.png)

*Manual jog mode axis display after the reset attempt.*

![artifact_page_85_image_21](assets/artifact_page_85_image_21.png)

*Affected axis area used for post-RESET confirmation.*


**Stop or Escalate If:**

* The fault indication remains after RESET.
* The source does not provide additional diagnostic interpretation or next-step correction if the fault remains.

---

## Success Criteria

* The operator reaches the MCP_Dual screen and enters manual jog mode.
* The operator can inspect Z1 Axis, Z2 Axis, A1 Axis, and A2 Axis for a Fault indication.
* If a fault is displayed, RESET is pressed.
* The affected axis no longer shows the Fault indication after RESET.

## Failure Conditions

* The MCP_Dual screen cannot be accessed.
* Manual Mode does not appear after pressing JOG.
* The axis indicators cannot be viewed clearly enough to determine fault status.
* A displayed fault remains after pressing RESET.
* The source does not provide further diagnostic interpretation for a persistent fault.

## Escalation Guidance

* Escalate if the MCP_Dual screen cannot be accessed or the expected HMI view is unavailable.
* Escalate if JOG does not place the station into manual jog mode.
* Escalate if the axis fault indication remains after RESET.
* Escalate if additional diagnosis is needed, because the source does not provide further interpretation of persistent axis faults.

## Missing Details / Known Gaps

* The source packet does not provide an explicit estimated time.
* The source packet does not state whether production stop is required for this isolated diagnostic procedure.
* The source packet does not state whether lockout/tagout is required for this isolated diagnostic procedure.
* The source does not provide additional diagnostic interpretation if the fault indication remains after RESET.
* The source does not provide a detailed decision path when no fault is shown but the operator still suspects an axis problem.

## Source Lineage

- Candidate IDs: candidate_operator_station_identify_and_clear_axis_faults_in_manual_jog_mode
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
