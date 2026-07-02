# Navigate From the Hospital HMI Main Menu to Available Menus

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_navigate_from_the_hospital_hmi_main_menu_to_available_menus_v1` |
| Title | Navigate From the Hospital HMI Main Menu to Available Menus |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Hospital HMI Main Menu and its documented right-side function keys to open available menus for Hospital Station tote handling. The source identifies access to Operator Menu, Maintenance Menu, and Alarms from the Main Menu, and documents quick-access mappings for F1 through F6.

## When To Use

Use when an operator needs to navigate on the Hospital HMI from the Main Menu to one of the documented menus using the on-screen menu options or the right-side quick-access function keys.

## Do Not Use For

* Do not use this runbook for performing actions inside the Maintenance Menu; the source only documents navigation to that menu, not maintenance procedures.
* Do not use this runbook to infer undocumented menu behavior, permissions, or actions beyond the Main Menu access and function-key mappings shown in the source.

## Safety And Operational Notes

* This runbook is limited to HMI navigation only.
* Review role appropriateness before using maintenance functions, because the source does not describe what actions are permitted inside the Maintenance Menu.

## Access Or Tools Needed

* Access to the Hospital HMI
* Hospital Station Main Menu screen
* Documented F-key control mapping from Table 4-12

## Related Operational Context

* ctx_manual_hospital_hmi_screens_overview_v1
* ctx_manual_hospital_hmi_main_menu_function_keys_v1

## Procedure Steps

### Step 1 — Open or view the Hospital HMI Main Menu

**Responsible role:** operator

**Instruction:**
Open or view the Hospital Station Main Menu on the HMI.

**Expected result:**
The Hospital HMI Main Menu is displayed.

**Screens / Images:**

![artifact_fig_4_29_hospital_hmi_main_menu](assets/artifact_fig_4_29_hospital_hmi_main_menu.jpeg)

*Hospital HMI Main Menu screen layout and right-side quick-access buttons.*


**Stop or Escalate If:**

* The displayed screen does not show the documented Main Menu options or F-key mappings.

---

### Step 2 — Identify the available destination menus

**Responsible role:** operator

**Instruction:**
Identify the available destination menus listed from the Main Menu: Operator Menu, Maintenance Menu, and Alarms.

**Expected result:**
The operator recognizes the documented destination menus available from the Main Menu.

**Screens / Images:**

![artifact_fig_4_29_hospital_hmi_main_menu](assets/artifact_fig_4_29_hospital_hmi_main_menu.jpeg)

*Menu access points for Operator Menu, Maintenance Menu, and Alarms.*


**Stop or Escalate If:**

* The displayed screen does not show the documented Main Menu options or F-key mappings.

---

### Step 3 — Use quick-access buttons to open the desired menu

**Responsible role:** operator

**Instruction:**
Use the right-hand quick-access buttons as documented to navigate: press F1 for Operator menu, F2 for Maintenance menu, or F6 for Alarms.

**Expected result:**
The selected menu opens from the Main Menu.

**Screens / Images:**

![artifact_fig_4_29_hospital_hmi_main_menu](assets/artifact_fig_4_29_hospital_hmi_main_menu.jpeg)

*Right-side quick-access buttons and their menu assignments.*


**Stop or Escalate If:**

* The displayed screen does not show the documented Main Menu options or F-key mappings.
* The selected function key does not open the expected menu.
* Maintenance functions are needed beyond navigation and role appropriateness is unclear.

---

### Step 4 — Use Main menu or Previous screen navigation if needed

**Responsible role:** operator

**Instruction:**
If needed for navigation, use F5 for Main menu or F3 for Previous screen as documented.

**Expected result:**
The HMI returns to the Main Menu or the previous screen as selected.

**Screens / Images:**

![artifact_fig_4_29_hospital_hmi_main_menu](assets/artifact_fig_4_29_hospital_hmi_main_menu.jpeg)

*Main Menu screen and right-side quick-access controls including F5 and F3.*


**Stop or Escalate If:**

* The displayed screen does not show the documented Main Menu options or F-key mappings.
* F5 or F3 does not navigate to the expected screen.

---

### Step 5 — Use Setup menu quick access if needed

**Responsible role:** operator

**Instruction:**
If Setup menu access is needed from the quick-access controls, use F4 as listed in Table 4-12.

**Expected result:**
The Setup menu is opened using the documented quick-access key.

**Screens / Images:**

![artifact_fig_4_29_hospital_hmi_main_menu](assets/artifact_fig_4_29_hospital_hmi_main_menu.jpeg)

*Right-side quick-access controls including the F4 Setup menu mapping.*


**Stop or Escalate If:**

* The displayed screen does not show the documented Main Menu options or F-key mappings.
* F4 does not open the Setup menu as listed in Table 4-12.

---

## Success Criteria

* The Hospital HMI Main Menu is displayed and matches the documented layout.
* The operator can identify the documented available menus from the Main Menu.
* The selected menu opens using the documented quick-access function key mapping.

## Failure Conditions

* The displayed screen does not show the documented Main Menu options or F-key mappings.
* A documented function key does not open the expected menu.
* The operator needs maintenance actions beyond navigation, but the source does not define those actions or role boundaries.

## Escalation Guidance

* Escalate if the displayed screen does not show the documented Main Menu options or F-key mappings.
* Escalate if a documented function key does not open the expected menu.
* Review role appropriateness before using maintenance functions, because the source does not describe what actions are permitted inside the Maintenance Menu.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not define role boundaries for access to Maintenance Menu or Setup menu.
* The source does not describe actions to perform inside the Maintenance Menu, Setup menu, or Alarms after navigation.
* The source section text is not provided in the packet beyond referenced summaries and artifact retrieval text.

## Source Lineage

- Candidate IDs: candidate_operator_navigate_hospital_hmi_main_menu_to_available_menus
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
