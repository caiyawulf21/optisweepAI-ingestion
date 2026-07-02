# Stop the Tipping Cycle From MCP_Dual During Non-Recoverable Operator Station Motor Fault Recovery

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_stop_tipping_cycle_from_mcp_dual_during_non_recoverable_operator_station_motor_fault_recovery_v1` |
| Title | Stop the Tipping Cycle From MCP_Dual During Non-Recoverable Operator Station Motor Fault Recovery |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the operator station HMI to open the MCP_Dual screen and press CYCLE STOP to stop the tipping cycle as part of the documented recovery process for a non-recoverable operator station motor fault that cannot be recovered in software and requires manual reset.

## When To Use

Use this procedure during recovery of a non-recoverable operator station motor fault when the documented manual process instructs the user to stop the tipping cycle from the operator station HMI.

## Do Not Use For

* Do not use this as a complete recovery procedure for the non-recoverable fault; the provided source excerpt includes only the initial HMI actions.
* Do not use this for faults that can be recovered via software.
* Do not continue beyond stopping the tipping cycle if the remaining manual reset steps are not available from the source.

## Safety And Operational Notes

* The source states that some faults in this category cannot be recovered via software and require manual reset.
* This runbook covers only the initial stopping actions from the provided source excerpt.
* Because the documented recovery is incomplete in the supplied excerpt, stop and escalate before attempting unsupported follow-on recovery actions.

## Access Or Tools Needed

* Access to the operator station HMI
* MCP_Dual screen (F3)
* CYCLE STOP control

## Related Operational Context

* ctx_manual_nonrecoverable_faults_overview_v1
* ctx_manual_operator_station_motors_nonrecoverable_fault_v1
* ctx_manual_motor_overload_tipper_gripper_fault_example_v1
* ctx_manual_mcp_dual_hmi_screen_reference_v1
* ctx_manual_cycle_stop_control_reference_v1

## Procedure Steps

### Step 1 — Navigate to the MCP_Dual screen

**Responsible role:** L2_support

**Instruction:**
At the operator station HMI, navigate to the "MCP_Dual" screen using F3.

**Expected result:**
The MCP_Dual screen is displayed on the operator station HMI.

**Screens / Images:**

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Operator station HMI screen snippet associated with non-recoverable fault recovery; use it to identify the MCP_Dual/operator station control context and visible axis controls.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Operator station HMI view showing manual mode axis controls and RESET control in the same recovery context.*


**Stop or Escalate If:**

* The operator station HMI is not accessible.
* F3 does not navigate to the MCP_Dual screen.
* The displayed screen does not match the recovery context supported by the source.
* Additional recovery steps are needed but are not available in the provided source excerpt.

---

### Step 2 — Press CYCLE STOP

**Responsible role:** L2_support

**Instruction:**
On the MCP_Dual screen, press CYCLE STOP to stop the tipping cycle.

**Expected result:**
The tipping cycle is stopped from the operator station HMI.

**Screens / Images:**

![artifact_page_84_image_13](assets/artifact_page_84_image_13.png)

*Operator station HMI recovery-context screen snippet to orient to the control area associated with stopping the tipping cycle.*

![artifact_page_84_image_10](assets/artifact_page_84_image_10.png)

*Operator station HMI view in the same non-recoverable fault recovery context; use as supporting visual context for the operator station controls.*


**Stop or Escalate If:**

* Pressing CYCLE STOP does not stop the tipping cycle.
* The CYCLE STOP control cannot be located on the operator station HMI.
* The fault requires additional manual reset actions that are not present in the provided source excerpt.
* The condition appears non-recoverable in software and the next documented manual steps are unavailable.

---

## Success Criteria

* The operator station HMI is navigated to the MCP_Dual screen using F3.
* CYCLE STOP is pressed on MCP_Dual.
* The tipping cycle is stopped as part of the documented non-recoverable fault recovery process.

## Failure Conditions

* The fault cannot be recovered in software and requires manual reset.
* The MCP_Dual screen cannot be accessed from the operator station HMI.
* The tipping cycle does not stop after pressing CYCLE STOP.
* The provided source excerpt does not include the remaining manual reset steps needed to continue recovery.

## Escalation Guidance

* Escalate or defer further recovery if additional manual reset steps are required but not available in the provided source.
* Escalate if the MCP_Dual screen cannot be reached or the operator station HMI is unavailable.
* Escalate if pressing CYCLE STOP does not stop the tipping cycle.
* Do not invent or perform unsupported follow-on recovery actions beyond the source-backed steps.

## Missing Details / Known Gaps

* The provided source excerpt does not include the remaining manual reset steps after stopping the tipping cycle.
* The source does not specify estimated completion time.
* The source does not explicitly state whether production stop or LOTO is required for these initial HMI actions.
* The source does not provide explicit role boundaries beyond the recovery context.
* The supplied source_sections text is empty; grounding relies on candidate source refs, artifacts, and context records in the packet.

## Source Lineage

- Candidate IDs: candidate_l2_stop_tipping_cycle_from_mcp_dual_during_nonrecoverable_operator_station_motor_fault
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
