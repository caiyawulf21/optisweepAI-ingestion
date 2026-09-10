# Check RMS is up and running and verify SQL Server Agent is running (post-unplanned restart sanity check)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rms_up_and_sql_server_agent_running_post_unplanned_restart_sanity_check_v1` |
| Title | Check RMS is up and running and verify SQL Server Agent is running (post-unplanned restart sanity check) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `windows_service_or_event_log` |
| Access Surface | `rms_ui`, `wcs_sql`, `event_viewer` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `service_crash_or_restart`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Perform a post-unplanned restart sanity check by confirming RMS is up and running and verifying that the SQL Server Agent service is running in SQL Server Configuration Manager on the WCS backup server. This check is motivated by a prior issue where jobs were not cleaning up after an unplanned restart.

## When To Use

Use after an unplanned restart as a final sanity check to ensure RMS is up/running and SQL Server Agent is running (to reduce risk of follow-on issues such as jobs not cleaning up).

## Do Not Use For

* Do not proceed with further RMS/job health assumptions if RMS is not up/running or if SQL Server Agent is not running; stop and escalate per source guidance.

## Access Or Tools Needed

* RMS access (to view up/running status)
* RDP access to fortna-wcs-backup.txrth.otnet.ups.com
* SQL Server Configuration Manager
* SQL Server Agent service status visibility

## Related Operational Context

* ctx_training_video_rms_up_and_running_check_v1
* ctx_training_video_sql_server_agent_running_status_v1
* ctx_training_video_unplanned_restart_job_cleanup_issue_v1

## Visual References

![artifact_training_video_training_video_day2_0054_and_then_check_rms_to_make_primary_03_14_29_500](assets/fe38915b99de4ce2.jpg)

*Training video frame showing the post-unplanned restart check: check RMS up/running and verify SQL Server Configuration Manager shows SQL Server Agent running; includes the RDP target host name.*

## Procedure Steps

### Step 1 — Check RMS to make sure everything's up and running

**Responsible role:** L2_support

**Instruction:**
Using RMS access, check the RMS system status/dashboard to confirm RMS is up and running.

**Expected result:**
RMS indicates the system is up and running.

**Stop or Escalate If:**

* Stop and escalate if RMS does not appear up/running.

---

### Step 2 — RDP into the WCS backup server mentioned in the source

**Responsible role:** L2_support

**Instruction:**
Use RDP to connect to fortna-wcs-backup.txrth.otnet.ups.com.

**Expected result:**
You are connected to fortna-wcs-backup.txrth.otnet.ups.com and can open SQL Server Configuration Manager.

**Stop or Escalate If:**

* Stop and escalate if you cannot reach the server via RDP or cannot access SQL Server Configuration Manager.

---

### Step 3 — Open SQL Server Configuration Manager on the server

**Responsible role:** L2_support

**Instruction:**
On the connected server, open SQL Server Configuration Manager.

**Expected result:**
SQL Server Configuration Manager is open and ready to view service states.

**Stop or Escalate If:**

* Stop and escalate if SQL Server Configuration Manager cannot be opened.

---

### Step 4 — Verify that the SQL Server Agent service is running

**Responsible role:** L2_support

**Instruction:**
In SQL Server Configuration Manager, verify the SQL Server Agent service state is Running.

**Expected result:**
SQL Server Configuration Manager shows SQL Server Agent is running.

**Stop or Escalate If:**

* Stop and escalate if SQL Server Agent is not running.

---

### Step 5 — If SQL Server Agent is not running, stop and escalate

**Responsible role:** L2_support

**Instruction:**
If SQL Server Agent is not running, do not continue with further assumptions about RMS/job health; stop and escalate.

**Expected result:**
Escalation is initiated when SQL Server Agent is not running.

**Stop or Escalate If:**

* SQL Server Agent is not running.

---

## Success Criteria

* RMS indicates the system is up and running.
* SQL Server Configuration Manager shows SQL Server Agent is running.

## Failure Conditions

* RMS does not appear up/running.
* SQL Server Agent service is not running.

## Escalation Guidance

* Escalate if RMS does not appear up/running or if SQL Server Agent is not running, since the source notes an issue after unplanned restart where jobs were not cleaning up.

## Missing Details / Known Gaps

* The packet does not provide specific RMS UI field names/labels or exact indicators for 'up and running' beyond the instruction to check RMS.
* The packet does not provide the exact SQL Server Configuration Manager navigation path or the exact UI label for the SQL Server Agent state; only that it should be running.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_check_rms_and_sql_server_agent_running
- Source ID: `training_video_day2`
- Source Type: `training_video`
