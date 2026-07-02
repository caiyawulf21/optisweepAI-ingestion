# Start the System From the HMI System API Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_start_the_system_from_the_hmi_system_api_screen_v1` |
| Title | Start the System From the HMI System API Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Initiate system startup from the system HMI by navigating to the system API screen and pressing the SYSTEM STARTUP control, as documented in the OptiSweep Operation and Maintenance Manual.

## When To Use

Use this procedure when the operator needs to initiate system startup from the system HMI using the documented system API screen control.

## Do Not Use For

* Do not use this runbook for startup verification, confirmation of successful startup completion, or recovery actions after startup, because those details are not provided in the source excerpt.
* Do not use this runbook for shutdown, close out, purge, or metrics reset actions, even though those controls are described on the system API screen in related source material.

## Safety And Operational Notes

* Use only the documented HMI actions from the source.
* Do not invent additional startup checks or recovery actions beyond the documented HMI steps.

## Access Or Tools Needed

* Access to the system HMI
* System API screen on the HMI

## Procedure Steps

### Step 1 — Navigate to the system API screen

**Responsible role:** operator

**Instruction:**
On the system HMI, navigate to the system API screen.

**Expected result:**
The system API screen is displayed on the HMI.

**Screens / Images:**

![artifact_page_81_image_2](assets/artifact_page_81_image_2.jpeg)

*System HMI screen associated with the startup procedure and the system API screen context.*

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*System API screen layout and controls used to identify the correct screen.*


**Stop or Escalate If:**

* The system API screen cannot be found or accessed on the HMI.

---

### Step 2 — Press SYSTEM STARTUP

**Responsible role:** operator

**Instruction:**
Press SYSTEM STARTUP on the system API screen.

**Expected result:**
The system startup command is initiated from the HMI using the SYSTEM STARTUP control.

**Screens / Images:**

![artifact_fig_4_9_system_api_controls](assets/artifact_fig_4_9_system_api_controls.jpeg)

*The System Startup control on the system API screen.*

![artifact_page_81_image_2](assets/artifact_page_81_image_2.jpeg)

*Startup procedure screen context associated with pressing SYSTEM STARTUP.*


**Stop or Escalate If:**

* The SYSTEM STARTUP control is not visible on the system API screen.
* Pressing SYSTEM STARTUP does not allow the operator to determine whether startup was initiated, because the source excerpt provides no verification or recovery guidance.

---

## Success Criteria

* The operator reaches the system API screen on the system HMI.
* The operator presses SYSTEM STARTUP on the system API screen.
* The startup command is initiated from the HMI as documented by the source.

## Failure Conditions

* The system API screen cannot be accessed.
* The SYSTEM STARTUP control cannot be found on the system API screen.
* The source excerpt does not provide verification indicators, failure indications, or post-action confirmation steps after pressing SYSTEM STARTUP.

## Escalation Guidance

* If the operator cannot access the system API screen, stop and seek site-specific guidance because the source does not provide alternate navigation or recovery steps.
* If the SYSTEM STARTUP control is unavailable or startup cannot be confirmed, escalate for SME review because the source excerpt does not provide troubleshooting or verification instructions.

## Missing Details / Known Gaps

* The source excerpt does not provide explicit confirmation indicators after pressing SYSTEM STARTUP.
* The source excerpt does not provide failure indications or troubleshooting steps for unsuccessful startup.
* The source excerpt does not provide escalation contacts or role boundaries beyond normal operator use.
* The source excerpt does not provide an estimated completion time.
* The source excerpt does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_start_system_from_hmi_api_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
