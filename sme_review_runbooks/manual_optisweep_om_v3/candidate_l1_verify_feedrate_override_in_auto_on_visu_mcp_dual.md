# Verify Feedrate Override Setting During Auto Operation on the Visu_MCP_Dual Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_feedrate_override_setting_during_auto_operation_on_the_visu_mcp_dual_screen_v1` |
| Title | Verify Feedrate Override Setting During Auto Operation on the Visu_MCP_Dual Screen |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | `operator` |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify on the Visu_MCP_Dual tipper machine control panel that the Feedrate Override display is at the documented 100% setting when the tipper is operating in Auto mode. This runbook is limited to observation and verification only; the source notes that adjustment is for maintenance personnel during troubleshooting or maintenance.

## When To Use

Use when you need to confirm whether the Feedrate Override shown on the Visu_MCP_Dual screen matches the documented expected setting during Auto operation of the tipper.

## Do Not Use For

* Do not use this runbook to adjust the Feedrate Override setting.
* Do not use this runbook as authorization to change controller settings or maintenance parameters.
* Do not use this runbook to verify non-Auto operating modes, because the documented 100% expectation is specifically stated for Auto mode.

## Safety And Operational Notes

* This runbook is verification-only and does not include changing settings.
* The source states maintenance personnel can adjust Feedrate Override for troubleshooting or maintenance purposes; if adjustment is needed, escalate rather than change the setting within this procedure.

## Access Or Tools Needed

* Access to the operator station HMI
* Visu_MCP_Dual screen
* Feedrate Override display

## Related Operational Context

* ctx_manual_tipper_feedrate_override_reference_v1
* ctx_manual_tipper_parameter_access_roles_v1
* ctx_manual_tipper_control_modes_and_cycle_controls_v1

## Procedure Steps

### Step 1 — Open the Visu_MCP_Dual screen and locate Feedrate Override

**Responsible role:** L1_support

**Instruction:**
At the operator station HMI, navigate to the Tipper Machine Control Panel screen identified as "Visu_MCP_Dual" and locate the Feedrate Override display on that screen.

**Expected result:**
The Visu_MCP_Dual screen is open and the Feedrate Override display is visible for review.

**Screens / Images:**

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Use the operator station display controls reference showing F3 mapped to "Visu_MCP_Dual" and screen navigation options.*

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the primary tipper machine control panel screen view to confirm you are on the Visu_MCP_Dual screen.*


**Stop or Escalate If:**

* The operator station HMI is not accessible.
* The Visu_MCP_Dual screen cannot be reached.
* The Feedrate Override display cannot be identified on the screen.

---

### Step 2 — Confirm the tipper is in Auto mode

**Responsible role:** L1_support

**Instruction:**
On the same Visu_MCP_Dual screen, confirm that the tipper is operating in Auto mode using the documented AUTO control state and related cycle controls shown on the screen.

**Expected result:**
You can determine whether the tipper is in Auto mode from the Visu_MCP_Dual screen.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Look at the AUTO button and the CYCLE START/CYCLE STOP controls on the Visu_MCP_Dual operator station control panel.*


**Stop or Escalate If:**

* Auto mode cannot be confirmed from the HMI.
* The tipper is not operating in Auto mode, so the documented 100% expectation does not apply for this verification.

---

### Step 3 — Read the Feedrate Override value

**Responsible role:** L1_support

**Instruction:**
Read the Feedrate Override value shown on the Visu_MCP_Dual display while the tipper is in Auto mode.

**Expected result:**
The currently displayed Feedrate Override value is identified.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the Visu_MCP_Dual screen reference while locating and reading the Feedrate Override area.*


**Stop or Escalate If:**

* The Feedrate Override value is not visible.
* The displayed value cannot be read reliably.

---

### Step 4 — Compare the displayed value to the documented Auto-mode setting

**Responsible role:** L1_support

**Instruction:**
Compare the displayed Feedrate Override value to the documented expected setting of 100% for Auto mode.

**Expected result:**
You determine whether the displayed value matches the documented Auto-mode setting.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the Visu_MCP_Dual screen reference for the Auto-mode control context while comparing the displayed Feedrate Override value.*


**Stop or Escalate If:**

* The displayed Feedrate Override is not 100% while the tipper is operating in Auto mode.

---

### Step 5 — Record and escalate a mismatch

**Responsible role:** L1_support

**Instruction:**
If the displayed Feedrate Override is not 100% while the tipper is operating in Auto mode, record the mismatch and escalate for maintenance review rather than attempting adjustment within this procedure.

**Expected result:**
A nonconforming Auto-mode Feedrate Override condition is documented and routed for follow-up.

**Screens / Images:**

![artifact_fig_4_19_operator_station_control_panel](assets/artifact_fig_4_19_operator_station_control_panel.png)

*Use the Visu_MCP_Dual screen reference to identify the operating context associated with the mismatch.*


**Stop or Escalate If:**

* The displayed Feedrate Override is not 100% during Auto operation.
* Adjustment appears necessary, because the source reserves adjustment for maintenance personnel.
* You cannot determine whether the displayed value reflects a valid operating condition.

---

## Success Criteria

* The Visu_MCP_Dual screen is accessed successfully.
* Auto mode status is confirmed on the tipper control panel.
* The Feedrate Override value is read from the display.
* The displayed value is verified against the documented 100% expectation for Auto mode.
* Any mismatch is recorded and escalated for maintenance review.

## Failure Conditions

* The Visu_MCP_Dual screen cannot be accessed.
* Auto mode cannot be confirmed.
* The Feedrate Override value cannot be read.
* The Feedrate Override is not 100% while the tipper is operating in Auto mode.
* An adjustment is required but the current procedure only supports verification.

## Escalation Guidance

* Escalate to maintenance if the Feedrate Override is not 100% while the tipper is operating in Auto mode.
* Escalate to maintenance if correction or adjustment is needed, because the source states maintenance personnel can adjust this for troubleshooting or maintenance purposes.
* Escalate if the HMI does not provide enough information to confirm Auto mode or read the Feedrate Override value.

## Missing Details / Known Gaps

* The packet does not provide the exact on-screen visual location of the Feedrate Override field within Figure 4-19.
* The packet does not provide a documented recording system, log format, or ticketing destination for mismatch documentation.
* The packet does not provide a documented escalation contact, team name, or response path beyond maintenance personnel.
* The packet does not provide a time estimate for completing this verification.
* The packet does not state whether production must be stopped or whether LOTO is required for this verification.

## Source Lineage

- Candidate IDs: candidate_l1_verify_feedrate_override_in_auto_on_visu_mcp_dual
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
