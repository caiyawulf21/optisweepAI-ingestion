# Open the ACB API Screen From the ACB System Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_acb_api_screen_from_the_acb_system_screen_v1` |
| Title | Open the ACB API Screen From the ACB System Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the ACB API screen from the ACB System screen using the documented API control on the System HMI.

## When To Use

Use this procedure when an operator needs to navigate from the ACB System screen to the ACB API screen on the System HMI.

## Do Not Use For

* Do not use this runbook for performing detailed control actions within the ACB API screen, because the source only documents how to access the screen.
* Do not use this runbook for recovery beyond basic navigation failure, because the source provides no further recovery steps.

## Safety And Operational Notes

* This source documents HMI navigation only.
* No lockout/tagout or production stop requirements are stated in the source.

## Access Or Tools Needed

* Access to the System HMI
* ACB System screen

## Related Operational Context

* ctx_manual_acb_api_screen_reference_v1

## Procedure Steps

### Step 1 — Go to the ACB System screen

**Responsible role:** operator

**Instruction:**
Go to the "ACB System" screen on the System HMI.

**Expected result:**
The ACB System screen is displayed and available for interaction.

**Screens / Images:**

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*Use this image as the ACB System screen reference before selecting API.*


**Stop or Escalate If:**

* The ACB System screen cannot be reached on the System HMI.

---

### Step 2 — Press API on the ACB System screen

**Responsible role:** operator

**Instruction:**
Press API on the "ACB System" screen to open the ACB API screen.

**Expected result:**
The system navigates from the ACB System screen to the ACB API screen.

**Screens / Images:**

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*Locate the ACB System screen where the API control is selected.*

![artifact_fig_4_8_acb_api_screen](assets/artifact_fig_4_8_acb_api_screen.jpeg)

*Reference the destination ACB API screen that should open after pressing API.*


**Stop or Escalate If:**

* The API control is not present on the "ACB System" screen.
* Pressing API does not open the ACB API screen.

---

### Step 3 — Verify the ACB API screen is displayed

**Responsible role:** operator

**Instruction:**
Verify that the ACB API screen is displayed.

**Expected result:**
The ACB API screen is open and available for use.

**Screens / Images:**

![artifact_fig_4_8_acb_api_screen](assets/artifact_fig_4_8_acb_api_screen.jpeg)

*Confirm the displayed screen matches the ACB API screen shown in Figure 4-8.*


**Stop or Escalate If:**

* The ACB API screen does not open.
* The displayed screen does not match the documented ACB API screen.

---

## Success Criteria

* The operator reaches the ACB System screen.
* Pressing API opens the ACB API screen.
* The ACB API screen is displayed and available for use.

## Failure Conditions

* The ACB System screen cannot be reached.
* The API control is not present on the "ACB System" screen.
* Pressing API does not open the ACB API screen.
* A different screen is displayed instead of the ACB API screen.

## Escalation Guidance

* Escalate if the API control is not present on the "ACB System" screen or the ACB API screen does not open, because the source provides no further recovery steps.

## Missing Details / Known Gaps

* The source does not provide a time estimate for this procedure.
* The source does not specify role boundaries beyond operator-level HMI use.
* The source does not provide recovery steps if navigation fails.
* The source does not document detailed actions to perform within the ACB API screen in this procedure.

## Source Lineage

- Candidate IDs: candidate_open_acb_api_screen_from_acb_system_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
