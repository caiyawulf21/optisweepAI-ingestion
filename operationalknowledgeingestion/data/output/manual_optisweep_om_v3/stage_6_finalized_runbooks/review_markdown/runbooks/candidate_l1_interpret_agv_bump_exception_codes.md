# Interpret AGV BUMP Exception Codes On The Bump Fault Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_agv_bump_exception_codes_on_the_bump_fault_screen_v1` |
| Title | Interpret AGV BUMP Exception Codes On The Bump Fault Screen |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented BUMP exception codes in the source manual to identify whether an AGV BUMP fault corresponds to a front collision bar trigger or an obstacle avoidance trigger, and record the interpretation with the AGV fault details.

## When To Use

Use when reviewing an AGV BUMP fault in RMS or on the AGV Bump Fault Screen and you need to interpret the documented meaning of exception code 21057 or 21060 from the source manual.

## Do Not Use For

* Do not use for exception codes other than 21057 or 21060.
* Do not use to infer corrective actions or fault meanings beyond the source-provided exception descriptions.

## Safety And Operational Notes

* This runbook is a reference/interpretation aid only and does not authorize physical intervention or unsupported recovery actions.
* The source states that before going inside the grid (the Dance Floor), specific AGV fault information should be gathered first: Robot ID, fault description from RMS, whether the AGV is holding a bin and tote ID, and whether an AGV under a rack is the empty AGV for that zone.

## Access Or Tools Needed

* Access to RMS or the AGV Bump Fault Screen
* Documented BUMP exception code mapping

## Related Operational Context

* ctx_manual_bump_fault_overview_v1
* ctx_manual_bump_exception_codes_v1
* ctx_manual_agv_bump_fault_screen_v1
* ctx_manual_fault_recovery_prereq_info_v1

## Procedure Steps

### Step 1 — Open or view the AGV Bump Fault Screen or related fault information

**Responsible role:** L1_support

**Instruction:**
Open or view the AGV Bump Fault Screen or related RMS fault information for the affected AGV.

**Expected result:**
The AGV BUMP fault details are visible for review.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*The AGV "Bump" Fault Screen shown in Figure 5-2, used as the reference screen for BUMP fault information.*


**Stop or Escalate If:**

* The affected AGV's BUMP fault information cannot be located in RMS or on the AGV Bump Fault Screen.

---

### Step 2 — Locate the displayed BUMP exception code

**Responsible role:** L1_support

**Instruction:**
Locate the displayed exception code associated with the BUMP fault.

**Expected result:**
A specific BUMP exception code is identified from the displayed fault information.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*The BUMP fault display area where the exception code information appears.*


**Stop or Escalate If:**

* The exception code is not shown or cannot be read from the available fault information.

---

### Step 3 — Compare the displayed code to the documented values

**Responsible role:** L1_support

**Instruction:**
Compare the displayed exception code to the documented values in the source manual.

**Expected result:**
The displayed code is matched to a documented exception meaning or identified as not covered by the source.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*The BUMP fault screen context while comparing the displayed exception code to the documented code meanings.*


**Stop or Escalate If:**

* The displayed exception code does not match 21057 or 21060.

---

### Step 4 — Interpret code 21057 as front collision bar triggered

**Responsible role:** L1_support

**Instruction:**
If the code is 21057, record that the robot front collision bar triggered.

**Expected result:**
Code 21057 is interpreted using the source-provided meaning.

**Stop or Escalate If:**

* The displayed code is 21057 but the source meaning cannot be confirmed from the provided documentation.

---

### Step 5 — Interpret code 21060 as obstacle avoidance triggered

**Responsible role:** L1_support

**Instruction:**
If the code is 21060, record that the robot triggered obstacle avoidance.

**Expected result:**
Code 21060 is interpreted using the source-provided meaning.

**Stop or Escalate If:**

* The displayed code is 21060 but the source meaning cannot be confirmed from the provided documentation.

---

### Step 6 — Record the Robot ID, RMS fault description, and interpreted meaning

**Responsible role:** L1_support

**Instruction:**
Record the Robot ID and the fault description from RMS together with the interpreted exception meaning.

**Expected result:**
The AGV fault record includes the Robot ID, RMS fault description, and the documented meaning of the exception code.

**Screens / Images:**

![artifact_fig_5_2_agv_bump_fault_screen](assets/artifact_fig_5_2_agv_bump_fault_screen.jpeg)

*The AGV Bump Fault Screen context while capturing the Robot ID and fault information for documentation.*


**Stop or Escalate If:**

* The displayed exception code does not match the documented values 21057 or 21060.
* Required AGV fault details such as Robot ID or RMS fault description are unavailable.
* Additional fault meaning or corrective action would need to be inferred beyond the source.

---

## Success Criteria

* The displayed AGV BUMP exception code is identified and matched to a documented source value.
* Code 21057 is recorded as "Robot front collision bar triggers" when present.
* Code 21060 is recorded as "The robot triggers the obstacle avoidance" when present.
* The Robot ID and RMS fault description are recorded together with the interpreted exception meaning.

## Failure Conditions

* The BUMP fault information cannot be accessed or read.
* The displayed exception code is not 21057 or 21060.
* The user attempts to infer additional meanings or corrective actions not supported by the source.
* Required AGV fault details such as Robot ID or RMS fault description are missing.

## Escalation Guidance

* Escalate if the displayed exception code does not match the documented values 21057 or 21060.
* Escalate if the BUMP fault information cannot be viewed or the exception code cannot be read.
* Do not infer additional fault meanings or corrective actions beyond the source-provided exception descriptions.

## Missing Details / Known Gaps

* The source packet does not provide an estimated completion time.
* The source packet does not specify whether production stop or LOTO is required for this reference activity.
* The source packet does not provide a detailed field-by-field layout of where the exception code appears on the screen beyond Figure 5-2.
* The source packet does not define actions for exception codes other than 21057 and 21060.

## Source Lineage

- Candidate IDs: candidate_l1_interpret_agv_bump_exception_codes
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
