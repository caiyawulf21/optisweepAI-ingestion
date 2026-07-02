# Access The RMS Web Application And Reach The Overview Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_access_the_rms_web_application_and_reach_the_overview_screen_v1` |
| Title | Access The RMS Web Application And Reach The Overview Screen |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Open the site RMS web application using the site-specific address associated with the site's Argus server, log in with username and password, and confirm the RMS overview screen is displayed. The training segment presents this as a support-facing starting point for learning more about a system issue.

## When To Use

Use when support personnel need to access a site's RMS web application and verify they have reached the RMS overview screen as the starting point for investigating or learning more about a system issue.

## Do Not Use For

* Do not use for deeper RMS navigation or troubleshooting actions not shown in this source segment.
* Do not use when the site-specific RMS web location or unique IP address is not known.
* Do not use when valid RMS username and password are not available.

## Safety And Operational Notes

* The source frames this as a support-facing access and viewing procedure only.
* The source does not provide authorization to bypass OptiSweep or perform direct control changes in RMS.
* The source notes risk of systems getting out of sync if OptiSweep is bypassed; this runbook is limited to access and overview confirmation.

## Access Or Tools Needed

* Access to the site's RMS web location or unique IP address
* Username and password for RMS
* Web browser access to the RMS web application

## Related Operational Context

* ctx_training_video_rms_site_access_model_v1
* ctx_training_video_rms_web_login_overview_screen_v1

## Procedure Steps

### Step 1 — Obtain the site RMS web address

**Responsible role:** L1_support

**Instruction:**
Obtain the site-specific RMS web location or unique IP address associated with the site's Argus server.

**Expected result:**
A valid RMS web location or unique IP address for the site is available.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*Reference that each site has an Argus server and RMS is accessed through a web location or unique IP address.*


**Stop or Escalate If:**

* Stop and escalate if the site-specific RMS address or unique IP address is not known.

---

### Step 2 — Open the RMS web application

**Responsible role:** L1_support

**Instruction:**
Open the RMS web application at the site-specific address or unique IP address.

**Expected result:**
The RMS web application is opened and ready for login.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*The training frame and transcript context describing access to the RMS web application through the site-specific address.*


**Stop or Escalate If:**

* Stop and escalate if the RMS web application cannot be reached from the provided site-specific address.

---

### Step 3 — Log in with username and password

**Responsible role:** L1_support

**Instruction:**
Enter the provided username and password to log in.

**Expected result:**
The user is authenticated into RMS.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*The segment context stating that after accessing the address, the user enters username and password.*


**Stop or Escalate If:**

* Stop and escalate if valid username and password are not available.
* Stop and escalate if the provided credentials are not accepted.

---

### Step 4 — Confirm the overview screen is displayed

**Responsible role:** L1_support

**Instruction:**
Confirm that the RMS overview screen appears after login.

**Expected result:**
The RMS overview screen is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*The RMS web application overview screen shown in the training video frame, including the overview area mentioned in the transcript.*


**Stop or Escalate If:**

* Escalate if the expected overview screen does not appear after login.

---

### Step 5 — Use the overview screen as the starting point

**Responsible role:** L1_support

**Instruction:**
Use the overview screen as the starting point for learning more information about the system issue, as described in the training segment.

**Expected result:**
The user is positioned at the RMS overview screen and can begin reviewing system information from that starting point.

**Screens / Images:**

![artifact_training_video_training_video_day1_0022_rms_is_the_robot_management_system_primary_00_52_41_500](assets/c5866ddbebd54b66.jpg)

*The overview screen context presented as the support starting point for learning more about system behavior or issues.*


**Stop or Escalate If:**

* Escalate if the overview screen cannot be reached or confirmed.

---

## Success Criteria

* The site-specific RMS web location or unique IP address is obtained.
* The RMS web application opens from that address.
* The user logs in with username and password.
* The RMS overview screen is displayed after login.

## Failure Conditions

* The site-specific RMS address or unique IP address is not known.
* Valid username and password are not available.
* The RMS web application cannot be reached.
* The expected overview screen does not appear after login.

## Escalation Guidance

* Escalate if the site-specific RMS address or unique IP address is not known.
* Escalate if valid username and password are not available.
* Escalate if the expected overview screen does not appear after login.

## Missing Details / Known Gaps

* The source does not provide the actual RMS URL, hostname, or IP address format.
* The source does not provide example usernames or password handling guidance.
* The source does not define what specific overview screen fields must be checked beyond confirming the overview screen is displayed.
* The source does not provide detailed next-step navigation from the overview screen.

## Source Lineage

- Candidate IDs: candidate_training_video_access_rms_web_overview
- Source ID: `training_video_day1`
- Source Type: `training_video`
