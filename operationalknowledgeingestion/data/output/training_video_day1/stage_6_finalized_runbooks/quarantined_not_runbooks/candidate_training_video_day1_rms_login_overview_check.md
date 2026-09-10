# Access RMS web application (via Argus server) and verify the overview screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_access_rms_web_app_via_argus_and_verify_overview_v1` |
| Title | Access RMS web application (via Argus server) and verify the overview screen |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the site Argus server information and the site-specific unique IP to open the RMS web application, log in with the RMS username/password, and confirm the RMS overview screen loads.

## When To Use

When you need to access the RMS web application for a site and confirm that, after login, the user lands on the RMS overview screen.

## Access Or Tools Needed

* Browser access to the RMS web location using the site unique IP address
* RMS username and password
* Site Argus server information (as referenced by the training segment)

## Related Operational Context

* ctx_training_video_rms_system_overview_v1
* ctx_training_video_rms_site_access_model_v1
* ctx_training_video_rms_web_login_overview_screen_v1

## Procedure Steps

### Step 1 — Identify the site Argus server and the RMS web location (RMS service) address, including the unique IP address for the site

**Responsible role:** L1_support

**Instruction:**
From the site access information you have, identify the Argus server for the site and the RMS web location address that uses the site unique IP to access the RMS service.

**Expected result:**
You have the site unique IP address (RMS web location) available to enter into a browser.

---

### Step 2 — Open the RMS web application using the unique IP address in a browser

**Responsible role:** L1_support

**Instruction:**
In a browser, open the RMS web application by entering the site unique IP address for the RMS service.

**Expected result:**
The RMS web application page loads in the browser (ready for username/password entry).

**Stop or Escalate If:**

* If the RMS web page does not load (e.g., blank page due to firewall not open), stop and escalate for support.

---

### Step 3 — Enter the username and password for RMS

**Responsible role:** L1_support

**Instruction:**
On the RMS web application login page, enter the RMS username and password and submit to log in.

**Expected result:**
Login succeeds and the RMS overview screen is displayed.

---

### Step 4 — Verify the RMS overview screen loads

**Responsible role:** L1_support

**Instruction:**
After login, verify that the RMS overview screen is displayed. Confirm the overview screen appearance as shown in the provided reference frame (including the top-left indicator mentioned in the segment).

**Expected result:**
The RMS overview screen is displayed after login.

**Stop or Escalate If:**

* If the RMS overview screen does not load after login, stop and escalate for support (the segment frames this as the first place to pinpoint the problem via the RMS web page).

---

## Success Criteria

* RMS web application opens successfully using the site unique IP address.
* After entering username and password, the RMS overview screen is displayed.

## Failure Conditions

* RMS web page shows blank due to firewall not open.
* RMS overview screen does not load after login.

## Escalation Guidance

* If the RMS overview screen does not load after login, stop and escalate for support to pinpoint the problem via the RMS web page.

## Missing Details / Known Gaps

* The source does not provide concrete UI control names/labels for the RMS login fields (it only states “username and password”).
* The source does not provide the exact browser URL format or the exact UI label text for the overview screen beyond the concept of an overview screen and a small top-left indicator.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_rms_login_overview_check
- Source ID: `training_video_day1`
- Source Type: `training_video`
