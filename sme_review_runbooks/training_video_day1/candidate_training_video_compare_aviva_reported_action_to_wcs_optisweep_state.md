# Compare an Operator-Reported Aviva Action Against WCS or OptiSweep System State

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_compare_an_operator_reported_aviva_action_against_wcs_or_optisweep_system_state_v1` |
| Title | Compare an Operator-Reported Aviva Action Against WCS or OptiSweep System State |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | `operator` |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use operator-reported information from Aviva and compare it against the state visible in WCS or OptiSweep to determine whether an Aviva-issued action, such as startup, is reflected in backend system state and to identify a likely communication mismatch.

## When To Use

Use this diagnostic when an operator reports that an action was performed in Aviva, or that Aviva shows a particular status, and support needs to verify whether WCS or OptiSweep reflects the same state. This is especially applicable when support users do not have direct Aviva access.

## Do Not Use For

* Do not use this procedure as a direct method to fix Aviva-side issues.
* Do not use this procedure to claim confirmed root cause when only a state mismatch has been observed.
* Do not use this procedure when direct Aviva interaction is required but support does not have Aviva access.

## Safety And Operational Notes

* This source describes a diagnostic comparison activity only; it does not authorize changing Aviva, WCS, or OptiSweep state.
* If support does not have Aviva access, rely on the operator to report what is visible in Aviva and note that limitation.
* If a mismatch is observed, document it as an observed communication issue for follow-up rather than assuming support can directly correct Aviva.

## Access Or Tools Needed

* Access to WCS or OptiSweep system state
* Operator assistance to report what is visible in Aviva
* Knowledge of the reported action sent from Aviva

## Related Operational Context

* ctx_training_video_aviva_access_limits_for_support_v1
* ctx_training_video_wcs_optisweep_state_comparison_v1
* ctx_training_video_aviva_hmi_not_manager_v1

## Procedure Steps

### Step 1 — Collect the operator-reported Aviva action and status

**Responsible role:** L1_support

**Instruction:**
Ask the operator what action was performed in Aviva, such as pressing a startup-related control, and ask what status they currently see in Aviva. If you do not have Aviva access, rely on the operator to report what is visible and note that limitation.

**Expected result:**
You have a clear operator-reported Aviva action and current Aviva status to use as the comparison baseline.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Transcript-supported guidance that non-UPS support users may not have Aviva access and should direct the operator on where to look in Aviva.*


**Stop or Escalate If:**

* Support cannot access Aviva and the operator cannot provide reliable Aviva status details.
* The reported Aviva action is too vague to compare against WCS or OptiSweep state.

---

### Step 2 — Check WCS or OptiSweep for current system state

**Responsible role:** L1_support

**Instruction:**
Use WCS or OptiSweep to check the current state of the system after the reported Aviva action.

**Expected result:**
You can identify the current state shown in WCS or OptiSweep for the condition the operator reported from Aviva.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Training segment stating that after an Aviva-triggered API or write error, support should check WCS or OptiSweep to see the state of the system.*


**Stop or Escalate If:**

* WCS or OptiSweep state is not accessible to support.
* The backend state cannot be determined from the available WCS or OptiSweep view.

---

### Step 3 — Compare the reported Aviva state to backend state

**Responsible role:** L1_support

**Instruction:**
Compare the operator-reported Aviva action and status to the state visible in WCS or OptiSweep.

**Expected result:**
You can state whether the backend system reflects the same condition the operator reported from Aviva.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Segment describing comparison of Aviva-issued actions, such as startup, against WCS or OptiSweep state.*


**Stop or Escalate If:**

* The operator-reported Aviva state cannot be matched to any observable WCS or OptiSweep state.
* The comparison indicates a mismatch that requires follow-up documentation.

---

### Step 4 — Verify whether the expected state change is present

**Responsible role:** L1_support

**Instruction:**
Verify whether the expected state change is present, such as whether startup is reflected in WCS or OptiSweep.

**Expected result:**
You confirm either that the expected state change is present or that it is absent in backend state.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Example in the training that if Aviva put the system in startup, support should verify whether startup is visible in WCS or OptiSweep.*


**Stop or Escalate If:**

* The expected state change is absent in WCS or OptiSweep after the operator reports it was issued in Aviva.

---

### Step 5 — Document any mismatch as an observed communication issue

**Responsible role:** L1_support

**Instruction:**
If the reported Aviva action is not reflected in WCS or OptiSweep, document the mismatch as an observed communication issue rather than assuming support can directly fix Aviva.

**Expected result:**
The mismatch is documented clearly as an observed communication issue for follow-up.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Training guidance that a startup mismatch between Aviva and WCS or OptiSweep indicates a communication issue and that support may not be able to directly fix Aviva.*


**Stop or Escalate If:**

* A mismatch is observed between Aviva-reported action and WCS or OptiSweep state.
* The issue appears to be on the Aviva side and support cannot directly remediate it.

---

## Success Criteria

* The operator-reported Aviva action and status are captured.
* The current state in WCS or OptiSweep is reviewed.
* Support determines whether the backend state matches the reported Aviva action.
* Any mismatch is documented as an observed communication issue for follow-up.

## Failure Conditions

* Support lacks Aviva access and the operator cannot provide usable Aviva details.
* WCS or OptiSweep state cannot be determined.
* The reported Aviva action is not reflected in WCS or OptiSweep.
* Support overstates the finding as a confirmed root cause or direct Aviva fix.

## Escalation Guidance

* If support does not have Aviva access, rely on the operator to report what is visible in Aviva and note that limitation.
* If the observed state in WCS or OptiSweep does not match the operator-reported Aviva action, capture the mismatch for follow-up rather than claiming a confirmed root cause.
* If the issue appears to be Aviva-side, note that the source states there may be nothing support can do to directly fix Aviva.

## Missing Details / Known Gaps

* The source does not specify the exact WCS or OptiSweep screen name to use for viewing system state.
* The source does not provide exact field names, buttons, or navigation steps inside WCS or OptiSweep for this comparison.
* The source does not provide a formal documentation template for recording the mismatch.
* The source gives startup as an example but does not provide a broader validated list of Aviva actions to compare.
* The source does not provide an estimated completion time.

## Source Lineage

- Candidate IDs: candidate_training_video_compare_aviva_reported_action_to_wcs_optisweep_state
- Source ID: `training_video_day1`
- Source Type: `training_video`
