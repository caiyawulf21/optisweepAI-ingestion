# Recognize Exception box / abnormal use fields on the Container Selection screen as not used in this implementation

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recognize_exception_box_abnormal_use_not_used_v1` |
| Title | Recognize Exception box / abnormal use fields on the Container Selection screen as not used in this implementation |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this guide to interpret the right-hand-side “Exception box” area on the Geek Plus Container Selection screen correctly. In this implementation, the abnormal use / abnormal code location / exception-related fields are present but have not been used operationally, so they should not be treated as the site’s troubleshooting source.

## When To Use

When a support user is viewing the Geek Plus Container Selection screen and sees the right-hand-side “exception box” area with abnormal-related fields, and needs to avoid misinterpreting those fields as active operational signals for this site.

## Do Not Use For

* Do not use these exception/abnormal fields as the primary basis for diagnosing an operational issue on this site.

## Access Or Tools Needed

* Container Selection HMI screen access
* Visibility of the exception box area and abnormal-related fields

## Related Operational Context

* ctx_training_video_exception_box_feature_scope_v1

## Procedure Steps

### Step 1 — Open the Container Selection screen and locate the right-hand-side “exception box” area

**Responsible role:** L1_support

**Instruction:**
Open the Geek Plus Container Selection screen and find the right-hand-side “exception box” area.

**Expected result:**
You can visually identify the right-hand-side “exception box” area on the Container Selection screen.

---

### Step 2 — Identify the abnormal-related fields in the exception box area

**Responsible role:** L1_support

**Instruction:**
In the exception box area, identify the abnormal-related items mentioned in the segment: abnormal use and abnormal code location / exception-related fields.

**Expected result:**
You can point to the abnormal use / abnormal code location / exception-related fields within the exception box area.

---

### Step 3 — Treat exception/abnormal fields as not used operationally in this implementation

**Responsible role:** L1_support

**Instruction:**
When you see the exception box abnormal-related fields, interpret them as present but not used operationally at this site. Use the segment’s guidance: “I haven’t seen this… we haven’t had to use this” and “we do not… we are not using” these Geek Plus exception-box features here.

**Expected result:**
You correctly conclude that the abnormal use / abnormal code location / exception-related fields are not the site’s active operational signals, so you do not base troubleshooting decisions on them.

**Stop or Escalate If:**

* If the site begins using exception-box features operationally (contrary to this guidance), stop and escalate for updated guidance.

---

### Step 4 — If asked, explain the operational scope: Geek Plus used for robots/movement with custom APIs for control

**Responsible role:** L1_support

**Instruction:**
If someone asks what the exception box abnormal-related fields mean operationally, explain that this site uses Geek Plus mainly for robots and movement, while custom APIs provide more control; exception-box features are associated with end-to-end control scenarios.

**Expected result:**
You can explain that the exception-box abnormal-related fields are not part of this site’s operational control path, because the site relies on custom APIs for end-to-end control rather than Geek Plus exception-box features.

---

## Success Criteria

* Support user can correctly interpret the exception box abnormal-related fields as present but not used operationally in this implementation.
* Troubleshooting avoids treating those fields as active operational signals for this site.

## Failure Conditions

* Misinterpretation: abnormal use / abnormal code location / exception-related fields are treated as active operational indicators for this site.
* Continued use of exception-box fields after evidence that the site has started using them operationally.

## Escalation Guidance

* If the site begins using exception-box features operationally (contrary to the guidance in this segment), stop using this interpretation and escalate for updated guidance.

## Missing Details / Known Gaps

* The packet does not provide exact field labels as they appear in the live UI (only the concepts: abnormal use, abnormal code location, exception-related items).
* The packet does not provide step-by-step navigation clicks within the Container Selection screen beyond “open the Container Selection screen.”

## Source Lineage

- Candidate IDs: candidate_training_video_container_selection_exception_box_abnormal_use_not_used
- Source ID: `training_video_day1`
- Source Type: `training_video`
