# Check the RMS Screen for System Faults at the Start of a Support Call

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_the_rms_screen_for_system_faults_at_the_start_of_a_support_call_v1` |
| Title | Check the RMS Screen for System Faults at the Start of a Support Call |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RMS screen as the first diagnostic check during a support call to determine whether any system faults are currently shown and to establish an initial fact base before deeper analysis.

## When To Use

Use at the beginning of a support phone call when diagnosing a reported issue and you need to determine whether the system is currently showing faults in RMS.

## Do Not Use For

* Do not use this RMS check alone as a complete diagnosis or root-cause determination.
* Do not use when RMS access is unavailable without noting that the condition could not be confirmed from available screens.

## Safety And Operational Notes

* This source describes the RMS fault review as an initial diagnostic check only.
* Do not assume root cause from the RMS check alone.

## Access Or Tools Needed

* Access to the RMS screen
* Ability to view or receive reported system fault information during the support call

## Related Operational Context

* ctx_training_video_rms_system_faults_first_check_v1

## Procedure Steps

### Step 1 — Open the RMS screen first

**Responsible role:** L1_support

**Instruction:**
At the start of the support call, go to the RMS screen before deeper troubleshooting.

**Expected result:**
The RMS screen is opened or its current content is made available for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Support guidance stating the RMS screen should be the first step on a phone call.*

![artifact_training_video_training_video_day1_0063_do_you_have_any_system_faults_primary_02_15_57_000](assets/5c1dbf20176cd0a3.jpg)

*Overall System RMS page reference showing where system faults are viewed.*

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Overall System RMS page and note that the page may appear blank if firewall access is not open.*


**Stop or Escalate If:**

* RMS cannot be accessed or viewed from available support access.
* The page is blank and the current condition cannot be confirmed from available screens.

---

### Step 2 — Check for system faults on RMS

**Responsible role:** L1_support

**Instruction:**
Review the RMS screen and look for any system faults shown there.

**Expected result:**
You determine whether system faults are present on the RMS screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0063_do_you_have_any_system_faults_primary_02_15_57_000](assets/5c1dbf20176cd0a3.jpg)

*System faults area on the left side of the Overall System RMS page.*

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*System faults on the left and active AGV faults on the right.*


**Stop or Escalate If:**

* The RMS screen cannot be used to confirm whether faults are present.
* The displayed condition is unavailable because RMS visibility is blocked.

---

### Step 3 — Record the observed fault state

**Responsible role:** L1_support

**Instruction:**
Record whether faults are present and capture only the fault information that is visible on the RMS screen or directly reported from that screen.

**Expected result:**
The call notes include whether faults are present and what was observed from RMS.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Support guidance emphasizing use of the RMS fault state as the first fact base on the call.*


**Stop or Escalate If:**

* You cannot confirm the reported condition from available screens.
* The limitation in visibility prevents reliable documentation of the current fault state.

---

### Step 4 — Use RMS fault state as the initial diagnostic baseline

**Responsible role:** L1_support

**Instruction:**
Use the observed RMS fault state as the initial diagnostic baseline before attempting deeper analysis, and do not treat this check alone as a complete diagnosis.

**Expected result:**
Further troubleshooting starts from a confirmed initial RMS fault state.

**Screens / Images:**

![artifact_training_video_training_video_day1_0077_all_right_any_questions_on_the_primary_02_31_34_000](assets/1ff14c599affb0f9.jpg)

*Training guidance that this is the first step on a phone call, not the complete diagnosis.*


**Stop or Escalate If:**

* A root cause is being assumed from the RMS check alone.
* No confirmable RMS baseline can be established from available access.

---

## Success Criteria

* The RMS screen is checked at the start of the support call.
* It is established whether system faults are present on RMS.
* The observed RMS fault state is documented as the initial diagnostic baseline.

## Failure Conditions

* RMS cannot be accessed or is blank from available support access.
* The reported condition cannot be confirmed from available screens.
* The RMS check is used as a complete diagnosis instead of an initial diagnostic step.

## Escalation Guidance

* If the RMS screen cannot be accessed or the reported condition cannot be confirmed from available screens, capture that limitation in notes.
* If RMS visibility is blocked, note the access limitation rather than inferring system state.
* If deeper diagnosis is needed, continue beyond this initial RMS check rather than assuming root cause.

## Missing Details / Known Gaps

* The source does not provide exact RMS navigation steps.
* The source does not provide specific fault field names or required note-taking fields.
* The source does not define exact escalation targets after the initial RMS check.
* The source does not provide a time estimate for completing this check.

## Source Lineage

- Candidate IDs: candidate_training_video_check_rms_for_system_faults_on_support_call
- Source ID: `training_video_day1`
- Source Type: `training_video`
