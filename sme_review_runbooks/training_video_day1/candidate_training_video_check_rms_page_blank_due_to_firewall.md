# Check Whether the Overall System RMS Page Is Blank Because RMS Access Is Blocked

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_whether_the_overall_system_rms_page_is_blank_because_rms_access_is_blocked_v1` |
| Title | Check Whether the Overall System RMS Page Is Blank Because RMS Access Is Blocked |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-specific diagnostic check to determine whether a blank Overall System RMS page matches the training-source explanation that the page should display the Geek+ RMS web page but may appear blank when firewall access is not open. This procedure is limited to observation and documentation only.

## When To Use

Use when reviewing the Overall System RMS page and the RMS display area is blank, and you need to determine whether that blank condition is consistent with the source-described access limitation rather than assuming an on-screen data issue.

## Do Not Use For

* Do not use this procedure to confirm a specific network root cause beyond the source statement that the firewall is not open.
* Do not use this procedure to open the firewall or perform network remediation.
* Do not use this procedure as a replacement for deeper RMS access troubleshooting when RMS visibility is required.

## Safety And Operational Notes

* This procedure is observational and documentation-focused only.
* Do not assume the blank page confirms any specific network root cause beyond the source statement that the firewall is not open.
* If RMS visibility is required and the page remains blank, escalate.

## Access Or Tools Needed

* Access to the Overall System RMS page
* Source-backed description of expected RMS page contents

## Related Operational Context

* ctx_training_video_rms_visibility_on_thin_clients_v1

## Procedure Steps

### Step 1 — Open or view the Overall System RMS page

**Responsible role:** L1_support

**Instruction:**
Open or view the Overall System RMS page and locate the area where RMS content is expected to appear.

**Expected result:**
The Overall System RMS page is visible for inspection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*The Overall System RMS page area that should display RMS content.*


**Stop or Escalate If:**

* The Overall System RMS page cannot be accessed for review.

---

### Step 2 — Observe whether the RMS display area is blank

**Responsible role:** L1_support

**Instruction:**
Inspect the RMS web page area and note whether it is blank instead of showing the expected RMS content.

**Expected result:**
You can state whether the RMS display area is blank.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*The RMS web page area that should contain the Geek+ RMS display.*


**Stop or Escalate If:**

* RMS visibility is required and the page remains blank.

---

### Step 3 — Compare the blank display to the source-described firewall limitation

**Responsible role:** L1_support

**Instruction:**
Compare the observed blank display to the source statement that the page should show RMS but can appear blank when the firewall is not open.

**Expected result:**
You can determine whether the blank page is consistent with the source-described access limitation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*The slide text and associated explanation that the page should show RMS but may be blank when firewall access is not open.*


**Stop or Escalate If:**

* You need confirmation of a specific network root cause beyond the source statement.
* RMS visibility is required and the page remains blank.

---

### Step 4 — Confirm the expected RMS page contents

**Responsible role:** L1_support

**Instruction:**
Confirm that the expected page content would normally include the Geek+ RMS web page, with system faults on the left and active AGV faults on the right.

**Expected result:**
You can describe the expected RMS content that is missing from the blank page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*The description of expected RMS content, including system faults on the left and active AGV faults on the right.*


**Stop or Escalate If:**

* Expected RMS visibility is needed for active troubleshooting and the page remains blank.

---

### Step 5 — Document the blank page and the source-backed access limitation

**Responsible role:** L1_support

**Instruction:**
Record that the page is blank and note the source-backed possibility that firewall access is preventing RMS from being displayed.

**Expected result:**
The observation is documented with the source-backed explanation and any need for escalation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*The source statement supporting documentation that the page may be blank when firewall access is not open.*


**Stop or Escalate If:**

* RMS visibility is required and the page remains blank.
* Additional troubleshooting requires confirmation beyond the source-described limitation.

---

## Success Criteria

* The Overall System RMS page has been reviewed.
* The observer has determined whether the RMS display area is blank.
* The blank condition, if present, has been documented as consistent with the source-described firewall access limitation.
* Any need for escalation due to required RMS visibility has been noted.

## Failure Conditions

* The Overall System RMS page cannot be accessed.
* The RMS display area remains blank when visibility is required.
* The blank page is treated as confirmed root cause without source support.
* Expected RMS content cannot be confirmed from the supplied source evidence.

## Escalation Guidance

* Escalate if RMS visibility is required and the page remains blank.
* Escalate if further diagnosis requires confirmation beyond the source statement that the firewall is not open.
* Escalate if the page cannot be accessed or reviewed.

## Missing Details / Known Gaps

* The source does not provide firewall-opening or network-remediation steps.
* The source does not provide a command, path, or system control to restore RMS visibility.
* The source does not provide a time estimate for completing this check.
* The source does not define a more specific escalation target or routing path.
* The source section text is empty in the packet; evidence is derived from candidate refs, artifact retrieval text, and context records.

## Source Lineage

- Candidate IDs: candidate_training_video_check_rms_page_blank_due_to_firewall
- Source ID: `training_video_day1`
- Source Type: `training_video`
