# Check RMS page for remotely available Overall System AGV Status

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rms_page_overall_system_agv_status_remote_v1` |
| Title | Check RMS page for remotely available Overall System AGV Status |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that the “Overall System AGV Status” information is available remotely by navigating to the RMS page referenced in the training segment and confirming the page/view is present and described as showing the current system status.

## When To Use

Use when you need to confirm that the remotely accessible RMS page contains the “Overall System AGV Status” view that is described as showing the current system status.

## Access Or Tools Needed

* RMS (fleet / AGV status web) page access

## Related Operational Context

* ctx_training_video_rms_page_remote_availability_v1
* ctx_training_video_overall_system_agv_status_page_v1
* ctx_training_video_overall_system_agv_status_current_status_v1

## Procedure Steps

### Step 1 — Open the RMS page referenced for remote availability

**Responsible role:** L1_support

**Instruction:**
Navigate to the RMS page referenced by the training segment (the segment explicitly directs you to “go to RMS page”).

**Expected result:**
The RMS page is reachable remotely (i.e., it loads enough for you to look for the “Overall System AGV Status” view).

**Stop or Escalate If:**

* RMS page cannot be accessed remotely

---

### Step 2 — Locate the “Overall System AGV Status” view on the RMS page

**Responsible role:** L1_support

**Instruction:**
On the RMS page, find the view labeled “Overall System AGV Status”.

**Expected result:**
The “Overall System AGV Status” view is present on the RMS page.

**Stop or Escalate If:**

* “Overall System AGV Status” view is not available on the RMS page

---

### Step 3 — Confirm the view is intended to show current system status

**Responsible role:** L1_support

**Instruction:**
Confirm that the “Overall System AGV Status” view corresponds to the description that it shows the current status of the system.

**Expected result:**
The “Overall System AGV Status” view is the one described as showing the current system status.

**Stop or Escalate If:**

* The view does not show the current system status as expected

---

### Step 4 — Stop and escalate if RMS remote access or the view is unavailable

**Responsible role:** L1_support

**Instruction:**
If the RMS page cannot be accessed remotely or if the “Overall System AGV Status” view is not present, stop the check and escalate to FORTNA support for access/availability troubleshooting.

**Expected result:**
Escalation is initiated when either remote access fails or the view is missing.

**Stop or Escalate If:**

* RMS page cannot be accessed remotely
* “Overall System AGV Status” view is not available on the RMS page

---

## Success Criteria

* RMS page is accessible remotely.
* “Overall System AGV Status” view is present on the RMS page.
* The located view matches the description that it shows the current system status.

## Failure Conditions

* RMS page cannot be accessed remotely.
* “Overall System AGV Status” view is not present on the RMS page.

## Escalation Guidance

* Escalate to FORTNA support for access/availability troubleshooting if the RMS page cannot be accessed remotely or if the “Overall System AGV Status” view is not available.

## Missing Details / Known Gaps

* The packet does not provide the specific RMS URL/IP, login steps, or exact navigation controls to reach the “Overall System AGV Status” view within the RMS web application.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_check_rms_page_remote_availability
- Source ID: `training_video_day1`
- Source Type: `training_video`
