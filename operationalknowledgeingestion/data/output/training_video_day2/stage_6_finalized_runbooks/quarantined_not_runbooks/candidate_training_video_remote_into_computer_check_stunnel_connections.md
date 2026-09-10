# Check Open stunnel Connections After Remote Access to the Computer

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_open_stunnel_connections_after_remote_access_v1` |
| Title | Check Open stunnel Connections After Remote Access to the Computer |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `stunnel`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `stunnel_or_chat_down` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After remotely accessing the OptiSweep computer, verify that the Open stunnel connections view shows exactly 3 connections with labels AI01, AI02, and SortationChat (via File -> connections).

## When To Use

Use when you have remotely accessed the OptiSweep computer and need to confirm the expected Open stunnel secure connections are present and correctly labeled.

## Access Or Tools Needed

* Remote access to the computer (per training segment evidence).
* Open stunnel application/view.
* Menu access within the stunnel view: File -> connections.

## Related Operational Context

* ctx_training_video_remote_access_to_computer_v1
* ctx_training_video_stunnel_connection_view_v1
* ctx_training_video_stunnel_connection_names_v1

## Visual References

![artifact_training_video_training_video_day2_0053_i_can_remote_into_the_computer_primary_03_14_10_500](assets/25797fc2584e113f.jpg)

*Training frame showing the Open stunnel view and OCR text indicating File -> connections and expected 3 connections labeled AI01, AI02, SortationChat.*

## Procedure Steps

### Step 1 — Remotely access the computer

**Responsible role:** L1_support

**Instruction:**
Using your remote access method to the computer (as referenced in the source segment), connect to the OptiSweep computer.

**Expected result:**
You are successfully connected to the computer and can open the Open stunnel view.

**Stop or Escalate If:**

* If you cannot remotely access the computer, stop and escalate for remote access troubleshooting.

---

### Step 2 — Open the stunnel-related application/view

**Responsible role:** L1_support

**Instruction:**
Open the Open stunnel view/application referenced in the source frame.

**Expected result:**
The Open stunnel view is open and ready for navigation to the connections list.

**Stop or Escalate If:**

* If Open stunnel cannot be opened, stop and escalate for application access/troubleshooting.

---

### Step 3 — Navigate to File -> connections in the stunnel view

**Responsible role:** L1_support

**Instruction:**
In the Open stunnel view, use the menu path indicated by the source OCR: Under file -> click connections.

**Expected result:**
The connections list/window is displayed.

**Stop or Escalate If:**

* If the connections list does not open, stop and escalate for UI navigation/application troubleshooting.

---

### Step 4 — Confirm the connections list shows 3 connections

**Responsible role:** L1_support

**Instruction:**
In the connections list, confirm it shows exactly 3 connections.

**Expected result:**
The connections list shows 3 connections.

**Stop or Escalate If:**

* If the connections view does not show 3 connections, stop and escalate for further troubleshooting.

---

### Step 5 — Verify connection labels are AI01, AI02, and SortationChat

**Responsible role:** L1_support

**Instruction:**
In the connections list, verify the connection labels include AI01, AI02, and SortationChat.

**Expected result:**
The connections list includes labels AI01, AI02, and SortationChat.

**Stop or Escalate If:**

* If the labels do not include AI01, AI02, and SortationChat, stop and escalate for further troubleshooting.

---

## Success Criteria

* Open stunnel connections view shows exactly 3 connections.
* The three connections are labeled AI01, AI02, and SortationChat.

## Failure Conditions

* Connections list count is not 3.
* Connection labels do not include AI01, AI02, and SortationChat.

## Escalation Guidance

* If the connections view does not show 3 connections or the labels do not include AI01, AI02, and SortationChat, stop and escalate for further troubleshooting (source provides only the stop/escalate trigger, not the next diagnostic actions).

## Missing Details / Known Gaps

* The source does not provide explicit step-by-step escalation troubleshooting actions beyond stopping when the expected connections count/labels are not present.
* The source OCR quality is medium and may contain minor label recognition errors; the procedure relies on the stated expected labels AI01, AI02, and SortationChat.

## Source Lineage

- Candidate IDs: candidate_training_video_remote_into_computer_check_stunnel_connections
- Source ID: `training_video_day2`
- Source Type: `training_video`
