# Add An AGV Back Into The System Using Recover AGV

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_add_an_agv_back_into_the_system_using_recover_agv_v1` |
| Title | Add An AGV Back Into The System Using Recover AGV |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Recover AGV control in the AGVs section of the System HMI API screen to add a specified AGV back into the system by entering its AGV ID.

## When To Use

Use when an AGV needs to be added back into the system and the AGV ID is known, using the Recover AGV control in the AGVs section of the API screen.

## Do Not Use For

* Do not use for AGV removal from the system; the source identifies Remove AGV as a separate control.
* Do not use when validation messages, prerequisites, or alternate recovery conditions are required; the source does not provide them.

## Safety And Operational Notes

* This is a system HMI recovery action.
* The source does not provide additional safety warnings, interlocks, or lockout requirements for this action.

## Access Or Tools Needed

* Access to the System HMI API screen
* AGVs section of the API screen
* AGV ID

## Related Operational Context

* ctx_manual_tote_api_controls_overview_v1
* ctx_manual_tote_api_controls_agv_recovery_reference_v1

## Procedure Steps

### Step 1 — Open the AGVs section of the API screen

**Responsible role:** L1_support

**Instruction:**
Open the System HMI API screen and navigate to the AGVs section.

**Expected result:**
The AGVs section of the API screen is visible.

**Screens / Images:**

![artifact_fig_4_8_acb_api_screen](assets/artifact_fig_4_8_acb_api_screen.jpeg)

*The API screen entry point used to access system, AGV, and tote controls.*

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The AGV API Controls area showing the AGVs section and Recover AGV control.*


**Stop or Escalate If:**

* Stop or escalate if the AGVs section of the API screen cannot be opened.
* Stop or escalate if the Recover AGV control is not available on the AGV API Controls screen.

---

### Step 2 — Locate the Recover AGV control and AGV ID field

**Responsible role:** L1_support

**Instruction:**
On the AGV API Controls screen, locate the Recover AGV control and the AGV ID entry field used for the recovery action.

**Expected result:**
The Recover AGV control and AGV ID input field are identified.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Recover AGV control and the AGV ID entry area within the AGV API Controls screen.*


**Stop or Escalate If:**

* Stop or escalate if the AGV ID entry field cannot be found.
* Stop or escalate if the Recover AGV control cannot be identified.

---

### Step 3 — Enter the AGV ID

**Responsible role:** L1_support

**Instruction:**
Enter the AGV ID for the AGV to be added back into the system.

**Expected result:**
The intended AGV ID is entered in the AGV ID field.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The AGV ID entry field used with Recover AGV.*


**Stop or Escalate If:**

* Stop or escalate if the correct AGV ID is not known.
* Stop or escalate if the AGV ID cannot be entered into the field.

---

### Step 4 — Use Recover AGV to add the AGV back into the system

**Responsible role:** L1_support

**Instruction:**
Use the Recover AGV control after entering the AGV ID to add the AGV back into the system.

**Expected result:**
The specified AGV is added back into the system.

**Screens / Images:**

![artifact_fig_4_12_agv_api_controls](assets/artifact_fig_4_12_agv_api_controls.jpeg)

*The Recover AGV control used to submit the AGV ID and add the AGV back into the system.*


**Stop or Escalate If:**

* Escalate if the AGV cannot be added back to the system after entering the AGV ID.

---

## Success Criteria

* The specified AGV is added back into the system.
* The Recover AGV action is completed using the AGV ID entry on the AGV API Controls screen.

## Failure Conditions

* The API screen or AGVs section cannot be accessed.
* The Recover AGV control or AGV ID field cannot be located.
* The AGV ID cannot be entered or is not known.
* The AGV cannot be added back into the system after using Recover AGV.

## Escalation Guidance

* Escalate if the AGV cannot be added back into the system after entering the AGV ID.
* Escalate if required validation messages, prerequisites, or confirmation indicators are needed but not available in the source.

## Missing Details / Known Gaps

* The source does not provide explicit confirmation messages or validation indicators for successful AGV recovery.
* The source does not provide detailed prerequisites beyond entering an AGV ID.
* The source does not provide a detailed navigation sequence beyond using the API screen and AGVs section.
* The source does not provide timing estimates for this procedure.
* The source does not specify production stop or LOTO requirements for this action.

## Source Lineage

- Candidate IDs: candidate_l1_recover_agv_into_system_by_agv_id
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
