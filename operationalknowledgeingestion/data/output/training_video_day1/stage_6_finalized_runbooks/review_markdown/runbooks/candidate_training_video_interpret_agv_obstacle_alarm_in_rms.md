# Interpret AGV Obstacle Alarm Visibility In RMS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_agv_obstacle_alarm_visibility_in_rms_v1` |
| Title | Interpret AGV Obstacle Alarm Visibility In RMS |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RMS screen and source-described AGV-to-RMS reporting behavior to understand that an AGV obstacle condition has been detected and surfaced as an alarm code in RMS.

## When To Use

Use this reference when reviewing an RMS screen to understand whether a visible AGV alarm code may represent an obstacle condition reported by the AGV's onboard hardware to RMS.

## Do Not Use For

* Do not use this runbook to determine corrective actions for the alarm.
* Do not use this runbook to infer alarm meanings beyond the source statement that RMS generates a visible alarm code when the AGV hardware detects an obstacle.
* Do not use this runbook as a troubleshooting procedure when an obstacle is suspected but no RMS alarm code is visible.

## Safety And Operational Notes

* This source describes alarm interpretation only and does not provide physical intervention steps.
* Do not infer route logic, corrective actions, or hardware repair actions beyond what is stated in the source.

## Access Or Tools Needed

* Access to the RMS screen
* Visibility into AGV alarm code display in RMS

## Related Operational Context

* ctx_training_video_rms_alarm_visibility_v1
* ctx_training_video_agv_vs_rms_responsibilities_v1

## Procedure Steps

### Step 1 — View the RMS screen

**Responsible role:** L1_support

**Instruction:**
Open or view the RMS screen where AGV information and alarm codes are visible.

**Expected result:**
The RMS screen is available for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*RMS referenced as the management system receiving AGV-reported conditions and surfacing alarm visibility.*


**Stop or Escalate If:**

* Escalate if the RMS screen cannot be viewed, because the source does not provide access troubleshooting steps.

---

### Step 2 — Identify the AGV entry under review

**Responsible role:** L1_support

**Instruction:**
Identify the AGV or robot entry being reviewed on the RMS screen.

**Expected result:**
A specific AGV or robot entry is selected or identified for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*Training slide context showing RMS as the place where AGV alarms are visible and where AGV-versus-RMS responsibilities are discussed.*


**Stop or Escalate If:**

* Escalate if the AGV or robot entry cannot be identified, because the source does not provide navigation or lookup instructions.

---

### Step 3 — Check for a visible alarm code

**Responsible role:** L1_support

**Instruction:**
Check whether an alarm code is displayed for the AGV in RMS.

**Expected result:**
The user confirms whether an alarm code is visible for the AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*The source-supported concept that RMS generates an alarm code visible on the RMS screen when the AGV reports an obstacle condition.*


**Stop or Escalate If:**

* Escalate if the RMS screen does not show an alarm code but the AGV is believed to have detected an obstacle, because the source does not provide further troubleshooting steps.

---

### Step 4 — Interpret the alarm as AGV-reported obstacle detection

**Responsible role:** L1_support

**Instruction:**
Interpret the displayed alarm in the context of the source statement that when the AGV physical hardware detects an obstacle in front of it, that condition is reported back to RMS and RMS generates an alarm code.

**Expected result:**
The visible RMS alarm is understood as reflecting an obstacle condition detected by AGV hardware and reported to RMS.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*AGV forward collision sensors and the AGV-versus-RMS responsibility explanation showing obstacle detection on the AGV and alarm generation in RMS.*


**Stop or Escalate If:**

* Stop interpretation if additional alarm meaning or corrective action is needed, because the source does not provide that detail.

---

### Step 5 — Record the interpretation boundary

**Responsible role:** L1_support

**Instruction:**
Record that the visible RMS alarm reflects a condition reported by the AGV's onboard sensing hardware rather than route logic performed on the AGV itself.

**Expected result:**
The interpretation is documented in a source-consistent way.

**Screens / Images:**

![artifact_training_video_training_video_day1_0006_one_question_we_were_in_the_primary_00_07_43_500](assets/dfa70c7e7d05da5a.jpg)

*The division of responsibilities between AGV onboard sensing and RMS supervisory control.*


**Stop or Escalate If:**

* Escalate if a corrective action or deeper troubleshooting path is required, because the source does not provide one.

---

## Success Criteria

* The user can recognize that an obstacle detected by AGV hardware is surfaced as an alarm code on the RMS screen.
* The user can distinguish AGV onboard sensing responsibility from RMS alarm presentation responsibility.

## Failure Conditions

* The RMS screen cannot be viewed.
* The AGV entry cannot be identified on the RMS screen.
* No alarm code is visible when an obstacle condition is believed to exist.
* The user infers unsupported alarm meanings or corrective actions beyond the source.

## Escalation Guidance

* Escalate if the RMS screen does not show an alarm code but the AGV is believed to have detected an obstacle, because the source does not provide further troubleshooting steps.
* Escalate if access to RMS or the relevant AGV view is unavailable.
* Escalate if corrective action, alarm code decoding, or remediation is required, because the source only supports interpretation of alarm visibility and reporting path.

## Missing Details / Known Gaps

* The source does not provide specific alarm code values or a code list.
* The source does not provide corrective actions for obstacle alarms.
* The source does not provide troubleshooting steps for cases where an obstacle is suspected but no alarm is visible in RMS.
* The source does not provide a time estimate for this review.
* The source does not specify whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_agv_obstacle_alarm_in_rms
- Source ID: `training_video_day1`
- Source Type: `training_video`
