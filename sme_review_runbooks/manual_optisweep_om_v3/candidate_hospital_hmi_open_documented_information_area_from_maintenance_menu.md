# Select A Documented Information Area From The Hospital HMI Maintenance Menu

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_select_a_documented_information_area_from_the_hospital_hmi_maintenance_menu_v1` |
| Title | Select A Documented Information Area From The Hospital HMI Maintenance Menu |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Hospital HMI Maintenance Menu to select one of the four documented information-area buttons: 2.1 Manual Control, 2.2 IO Diagnostics, 2.3 Persistent Variables, or 2.4 Default.

## When To Use

Use this procedure when access is needed to one of the documented information areas available from the Hospital HMI Maintenance Menu.

## Do Not Use For

* Do not use this runbook to describe destination screen contents or resulting behavior after button selection unless supported by additional source material.

## Safety And Operational Notes

* This runbook is limited to HMI menu selection only.
* The source does not provide authorization for broader actions beyond selecting one of the documented Maintenance Menu buttons.

## Access Or Tools Needed

* Access to the Hospital HMI Maintenance Menu screen
* Ability to interact with the HMI
* Figure 4-38 or equivalent documented Maintenance Menu reference

## Related Operational Context

* ctx_manual_hospital_hmi_maintenance_menu_v1
* ctx_manual_hospital_hmi_manual_control_entry_v1
* ctx_manual_hospital_hmi_io_diagnostics_entry_v1
* ctx_manual_hospital_hmi_persistent_variables_entry_v1
* ctx_manual_hospital_hmi_default_entry_v1

## Procedure Steps

### Step 1 — Open or view the Maintenance Menu

**Responsible role:** L1_support

**Instruction:**
Open or view the Hospital HMI Maintenance Menu screen.

**Expected result:**
The Hospital HMI Maintenance Menu screen is visible.

**Screens / Images:**

![artifact_fig_4_38_hospital_hmi_maintenance_menu_screen](assets/artifact_fig_4_38_hospital_hmi_maintenance_menu_screen.png)

*Hospital HMI Maintenance Menu screen and its available maintenance access buttons.*

![artifact_fig_4_29_hospital_hmi_main_menu](assets/artifact_fig_4_29_hospital_hmi_main_menu.jpeg)

*Main Menu reference showing Maintenance Menu access if screen orientation is needed.*


**Stop or Escalate If:**

* Stop or escalate if the Hospital HMI Maintenance Menu screen cannot be opened or viewed.

---

### Step 2 — Identify the available documented buttons

**Responsible role:** L1_support

**Instruction:**
Identify the available buttons on the menu: "2.1 Manual Control," "2.2 IO Diagnostics," "2.3 Persistent Variables," and "2.4 Default."

**Expected result:**
The four documented Maintenance Menu buttons are identified on the screen.

**Screens / Images:**

![artifact_fig_4_38_hospital_hmi_maintenance_menu_screen](assets/artifact_fig_4_38_hospital_hmi_maintenance_menu_screen.png)

*Figure 4-38 showing the four selectable buttons on the Maintenance Menu.*


**Stop or Escalate If:**

* Escalate if the required button is not present on the Maintenance Menu.

---

### Step 3 — Select the required information area button

**Responsible role:** L1_support

**Instruction:**
Select the documented button for the information area you need to access.

**Expected result:**
One of the four documented information-area buttons is selected from the Maintenance Menu.

**Screens / Images:**

![artifact_fig_4_38_hospital_hmi_maintenance_menu_screen](assets/artifact_fig_4_38_hospital_hmi_maintenance_menu_screen.png)

*Maintenance Menu buttons used to select the desired information area.*


**Stop or Escalate If:**

* Escalate if the required button is not present on the Maintenance Menu.
* Stop if additional behavior beyond button selection would need to be described without source support.

---

### Step 4 — Verify and record the selected information area

**Responsible role:** L1_support

**Instruction:**
Verify that the selection was made from the Maintenance Menu screen and record which documented information area was chosen.

**Expected result:**
The selected documented information area is noted.

**Screens / Images:**

![artifact_fig_4_38_hospital_hmi_maintenance_menu_screen](assets/artifact_fig_4_38_hospital_hmi_maintenance_menu_screen.png)

*Maintenance Menu screen used as the source of the selected documented information area.*


**Stop or Escalate If:**

* Stop if confirmation would require describing destination screen contents or resulting behavior not supported by the source.

---

## Success Criteria

* A documented information area is selected from the Hospital HMI Maintenance Menu using one of the four available buttons.
* The chosen entry is one of the documented buttons: 2.1 Manual Control, 2.2 IO Diagnostics, 2.3 Persistent Variables, or 2.4 Default.

## Failure Conditions

* The Hospital HMI Maintenance Menu cannot be viewed.
* The required button is not present on the Maintenance Menu.
* The selected entry cannot be confirmed as one of the documented Maintenance Menu buttons.
* Additional destination-screen behavior would need to be described without source support.

## Escalation Guidance

* Escalate if the required button is not present on the Maintenance Menu.
* Do not describe the destination screen contents or resulting behavior beyond button selection unless supported by additional source material.

## Missing Details / Known Gaps

* The source does not describe the exact navigation path used to open the Maintenance Menu from prior screens within this procedure.
* The source does not describe confirmation behavior after selecting a Maintenance Menu button.
* The source does not provide destination screen contents for the 2.1 Manual Control or 2.3 Persistent Variables entries within this packet.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_hospital_hmi_open_documented_information_area_from_maintenance_menu
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
