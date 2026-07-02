# Use RMS As A Support Entry Point To Gather Initial System Information

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_rms_as_a_support_entry_point_to_gather_initial_system_information_v1` |
| Title | Use RMS As A Support Entry Point To Gather Initial System Information |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Open the RMS web application, log in, and use the overview screen as an initial support view to understand current AGV or ATP-related issues before deeper troubleshooting.

## When To Use

Use when a support user receives a report that there is a problem and needs an initial system view in RMS to learn more information about AGV or ATP behavior.

## Do Not Use For

* Do not use this procedure as a root-cause or corrective-action procedure; this source only supports using RMS to gather initial information.
* Do not assume meanings for RMS fields, indicators, or controls that are not described in this source segment.
* Do not use this procedure to bypass OptiSweep control flows or make unsupported direct system changes through APIs.

## Safety And Operational Notes

* This source frames RMS here as a support-facing information-gathering interface.
* The source warns that bypassing OptiSweep and interacting outside supported flows can cause systems to get out of sync.
* Do not infer unsupported meanings or actions from interface elements not explained in this source.

## Access Or Tools Needed

* Access to the RMS web application
* Site-specific RMS address or unique IP address
* Username and password for RMS

## Related Operational Context

* ctx_training_video_rms_web_login_overview_screen_v1
* ctx_training_video_rms_system_overview_v1

## Procedure Steps

### Step 1 — Access the RMS web application

**Responsible role:** L1_support

**Instruction:**
Open the RMS web application using the site's RMS address or unique IP address.

**Expected result:**
The RMS web application is reached and ready for login.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*RMS described as a web application accessed through a unique IP address.*


**Stop or Escalate If:**

* Escalate if RMS cannot be accessed.

---

### Step 2 — Log in to RMS

**Responsible role:** L1_support

**Instruction:**
Log in with the assigned username and password.

**Expected result:**
The user is authenticated into RMS.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*Training context describing username and password entry for RMS access.*


**Stop or Escalate If:**

* Escalate if login cannot be completed.

---

### Step 3 — Open and observe the RMS overview screen

**Responsible role:** L1_support

**Instruction:**
Open the RMS overview screen and observe the information presented there.

**Expected result:**
The RMS overview screen is visible and available for initial review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*RMS overview-screen context from the training segment, including the overview area referenced in the candidate.*


**Stop or Escalate If:**

* Escalate if the overview screen is unavailable.

---

### Step 4 — Use the overview information to understand the issue

**Responsible role:** L1_support

**Instruction:**
Use the displayed RMS information to learn more about the AGV or ATP issue, consistent with the training segment's support purpose.

**Expected result:**
The user gains initial understanding of the reported issue from RMS.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*Support-oriented RMS overview context for learning more about ATP or AGV behavior.*


**Stop or Escalate If:**

* Stop if interpretation would require assuming meanings not described in this source.
* Escalate if RMS information is insufficient for further diagnosis.

---

### Step 5 — Record initial RMS observations

**Responsible role:** L1_support

**Instruction:**
Record what the RMS overview shows before moving to deeper troubleshooting, if additional investigation is needed.

**Expected result:**
Initial RMS observations are documented for follow-on troubleshooting.

**Stop or Escalate If:**

* Escalate if additional troubleshooting is needed but the initial RMS state cannot be captured or described from this source-supported view.

---

## Success Criteria

* The user successfully accesses RMS.
* The user logs in and reaches the overview screen.
* The user gathers initial information about the AGV or ATP issue from the RMS overview.
* Initial observations are recorded before deeper troubleshooting.

## Failure Conditions

* RMS cannot be accessed.
* Login cannot be completed.
* The overview screen is unavailable.
* The source does not provide enough detail to safely interpret specific fields or indicators.
* The source does not provide root-cause logic or corrective actions beyond initial information gathering.

## Escalation Guidance

* Escalate if RMS cannot be accessed or the overview screen is unavailable.
* Escalate if login cannot be completed with assigned credentials.
* Escalate if deeper troubleshooting is required because this source only supports initial information gathering.
* Do not proceed based on assumed meanings for fields or indicators not described in this source.

## Missing Details / Known Gaps

* The source does not provide specific RMS field definitions or indicator meanings.
* The source does not provide detailed navigation beyond accessing RMS, logging in, and viewing the overview screen.
* The source does not provide explicit corrective actions, root-cause decision logic, or escalation contacts.
* The source does not provide a time estimate for completing this procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_rms_as_support_entry_point
- Source ID: `training_video_day1`
- Source Type: `training_video`
