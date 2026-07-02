# Check Current System State On The Overall System API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_current_system_state_on_the_overall_system_api_page_v1` |
| Title | Check Current System State On The Overall System API Page |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

View the System State field on the Overall System Aveva API page to determine the current state the system is in.

## When To Use

Use this procedure when you need to check the current system state from the Overall System Aveva API page.

## Do Not Use For

* Do not use this procedure to infer a system state if the System State field is blank, unclear, or unavailable.
* Do not use this procedure to determine meanings of specific state values, because this source segment does not enumerate possible state values.

## Safety And Operational Notes

* This procedure is source-supported as a view/read/report action only.
* Do not infer a state if the System State field is blank, unclear, or unavailable.
* Escalate if the page cannot be accessed or the System State field is not visible.

## Access Or Tools Needed

* Access to the Overall System Aveva API page

## Related Operational Context

* ctx_training_video_api_page_overview_v1
* ctx_training_video_system_state_reference_v1

## Procedure Steps

### Step 1 — Open the Overall System Aveva API page

**Responsible role:** operator

**Instruction:**
Open or navigate to the Overall System Aveva API page referred to in training as the API page.

**Expected result:**
The Overall System Aveva API page is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*The Overall System Aveva API page with system-level items on the left side, including the System State field.*


**Stop or Escalate If:**

* The page cannot be accessed.
* The displayed page is not the Overall System Aveva API page.
* The System State field is not visible after opening the page.

---

### Step 2 — Locate the System State field

**Responsible role:** operator

**Instruction:**
Locate the System State field on the page.

**Expected result:**
The System State field is identified on the Overall System Aveva API page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*The System State field on the left side of the Overall System Aveva API page.*


**Stop or Escalate If:**

* The System State field is not visible.
* The field location is unclear on the page.

---

### Step 3 — Read the displayed system state

**Responsible role:** operator

**Instruction:**
Read the value shown in System State as the current state the system is in.

**Expected result:**
The current system state is identified from the displayed System State value.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*The value displayed in the System State field.*


**Stop or Escalate If:**

* The System State field is blank.
* The displayed value is unclear.
* The System State field is unavailable.
* You would need to infer the state rather than read it directly.

---

### Step 4 — Record or report the state exactly as shown

**Responsible role:** operator

**Instruction:**
Record or report the displayed state exactly as shown.

**Expected result:**
The observed system state is documented or communicated exactly as displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0066_so_kind_of_what_i_was_primary_02_18_32_000](assets/7f20b9d1dd84615e.jpg)

*The displayed System State value to copy exactly as shown.*


**Stop or Escalate If:**

* The displayed state cannot be read clearly enough to record exactly.
* The field is blank or unavailable.
* You are being asked to infer or reinterpret the state.

---

## Success Criteria

* The Overall System Aveva API page is accessed.
* The System State field is located.
* A readable System State value is observed.
* The displayed state is recorded or reported exactly as shown.

## Failure Conditions

* The Overall System Aveva API page cannot be accessed.
* The System State field is not visible.
* The System State field is blank, unclear, or unavailable.
* The user would need to infer the state instead of reading it directly.

## Escalation Guidance

* Escalate if the Overall System Aveva API page cannot be accessed.
* Escalate if the System State field is not visible.
* Do not infer a state if the field is blank, unclear, or unavailable; escalate instead.

## Missing Details / Known Gaps

* The source segment does not enumerate possible System State values.
* The source segment does not define follow-up actions for specific state values.
* The source segment does not provide an estimated completion time.
* The source segment does not specify supporting roles beyond the operator.
* The source segment does not provide navigation details for reaching the API page from other screens.

## Source Lineage

- Candidate IDs: candidate_training_video_check_system_state_on_api_page
- Source ID: `training_video_day1`
- Source Type: `training_video`
