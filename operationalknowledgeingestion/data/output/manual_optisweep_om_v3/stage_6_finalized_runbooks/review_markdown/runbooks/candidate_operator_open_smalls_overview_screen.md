# Open the Smalls Overview HMI Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_smalls_overview_hmi_screen_v1` |
| Title | Open the Smalls Overview HMI Screen |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the Smalls overview screen from the HMI to view the smalls system layout and the color-coded status of each part of the system.

## When To Use

Use this procedure when an operator needs to open the "Smalls" overview screen from the system HMI to view the smalls system layout and overall color-coded status display.

## Do Not Use For

* Do not use this procedure for accessing the ACB System overview screen.
* Do not use this procedure for opening statistics, calculations, tipping station, or API control screens.

## Access Or Tools Needed

* Access to the system HMI
* SMALLS HMI navigation option

## Related Operational Context

* ctx_manual_smalls_overview_screen_v1
* ctx_manual_smalls_system_layout_reference_v1
* ctx_manual_acb_system_overview_navigation_v1

## Procedure Steps

### Step 1 — Go to the HMI with the SMALLS option

**Responsible role:** operator

**Instruction:**
Go to the system HMI where the SMALLS access option is available.

**Expected result:**
The operator is at an HMI screen where SMALLS can be selected.

**Screens / Images:**

![artifact_fig_4_4_smalls_system_overview_screen](assets/artifact_fig_4_4_smalls_system_overview_screen.jpeg)

*Reference the expected Smalls overview display that should be reachable after selecting SMALLS.*


**Stop or Escalate If:**

* Stop if the HMI cannot be accessed.
* Escalate if the SMALLS access option is not available.

---

### Step 2 — Press SMALLS

**Responsible role:** operator

**Instruction:**
Press SMALLS to access the "Smalls" overview screen.

**Expected result:**
The "Smalls" overview screen opens.

**Screens / Images:**

![artifact_fig_4_4_smalls_system_overview_screen](assets/artifact_fig_4_4_smalls_system_overview_screen.jpeg)

*Use this figure as the target screen that should appear after pressing SMALLS.*


**Stop or Escalate If:**

* Stop if the Smalls overview screen does not open after pressing SMALLS.

---

### Step 3 — Verify the Smalls overview screen opens

**Responsible role:** operator

**Instruction:**
Verify that the "Smalls" overview screen opens and displays the smalls system layout.

**Expected result:**
The displayed screen is the "Smalls" overview screen and it shows the smalls system layout.

**Screens / Images:**

![artifact_fig_4_4_smalls_system_overview_screen](assets/artifact_fig_4_4_smalls_system_overview_screen.jpeg)

*Compare the displayed HMI screen to the Smalls system overview layout shown in Figure 4-4.*


**Stop or Escalate If:**

* Escalate if the expected layout is not shown.

---

### Step 4 — Confirm color-coded status is shown

**Responsible role:** operator

**Instruction:**
Confirm that the screen shows a color-coded status for each part of the system.

**Expected result:**
The screen displays a color-coded status for each part of the system.

**Screens / Images:**

![artifact_fig_4_4_smalls_system_overview_screen](assets/artifact_fig_4_4_smalls_system_overview_screen.jpeg)

*Review the overview screen for the color-coded status indications associated with each part of the smalls system.*


**Stop or Escalate If:**

* Escalate if the expected color-coded status display is not shown.

---

## Success Criteria

* The "Smalls" overview screen opens after pressing SMALLS.
* The screen shows the smalls system layout.
* The screen shows a color-coded status for each part of the system.

## Failure Conditions

* The Smalls overview screen does not open after pressing SMALLS.
* The expected Smalls overview layout is not shown.
* The expected color-coded status display is not shown.

## Escalation Guidance

* Stop if the Smalls overview screen does not open after pressing SMALLS.
* Escalate if the expected layout is not shown.
* Escalate if the expected color-coded status display is not shown.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not specify required supporting roles.
* The source does not define specific status colors or their meanings for the Smalls overview screen.
* The source does not state whether production stop or LOTO is required.
* The source does not provide a screenshot of the exact SMALLS access control separate from the resulting overview screen.

## Source Lineage

- Candidate IDs: candidate_operator_open_smalls_overview_screen
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
