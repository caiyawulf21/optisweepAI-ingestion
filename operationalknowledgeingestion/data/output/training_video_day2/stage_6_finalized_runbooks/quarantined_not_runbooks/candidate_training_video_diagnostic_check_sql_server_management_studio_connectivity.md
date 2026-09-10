# Verify SQL Server Management Studio connectivity after RDP to fortna-wcs-primary

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_ssms_connectivity_after_rdp_to_fortna_wcs_primary_v1` |
| Title | Verify SQL Server Management Studio connectivity after RDP to fortna-wcs-primary |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `service_crash_or_restart` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After remote access to the FORTNA WCS primary host, verify that SQL Server Management Studio (SSMS) can connect successfully as part of services unplanned restart validation.

## When To Use

Use when validating a services-related unplanned restart and you need to confirm that SSMS connectivity works after RDP to the FORTNA WCS primary host.

## Access Or Tools Needed

* RDP access to fortna-wcs-primary.txrth.otnet.ups.com
* SQL Server Management Studio (SSMS)

## Related Operational Context

* ctx_training_video_services_unplanned_restart_reference_v1
* ctx_training_video_fortna_wcs_primary_host_reference_v1
* ctx_training_video_sql_server_management_studio_connectivity_check_v1

## Visual References

![artifact_training_video_training_video_day2_0050_just_make_sure_it_s_good_primary_03_13_25_500](assets/26787b28eb66297d.jpg)

*Frame showing: RDP into fortna-wcs-primary.txrth.otnet.ups.com, opening SQL Server Management Studio, and the instruction to check that you can connect.*

## Procedure Steps

### Step 1 — RDP into fortna-wcs-primary.txrth.otnet.ups.com

**Responsible role:** L2_support

**Instruction:**
RDP into the host named in the source: fortna-wcs-primary.txrth.otnet.ups.com.

**Expected result:**
You have an active RDP session to fortna-wcs-primary.txrth.otnet.ups.com.

**Stop or Escalate If:**

* If you cannot reach the host via RDP, stop and escalate for deeper connectivity troubleshooting.

---

### Step 2 — Open SQL Server Management Studio (SSMS)

**Responsible role:** L2_support

**Instruction:**
Open SQL Server Management Studio (SSMS) on the RDP session host.

**Expected result:**
SSMS is open and ready for a connectivity attempt.

**Stop or Escalate If:**

* If SSMS cannot be opened, stop and escalate for deeper connectivity/troubleshooting.

---

### Step 3 — Check that you can connect in SSMS

**Responsible role:** L2_support

**Instruction:**
In SSMS, perform the connectivity check and verify that you can connect.

**Expected result:**
SSMS connectivity check succeeds (you can connect).

**Stop or Escalate If:**

* If SSMS cannot connect, stop and escalate for deeper connectivity troubleshooting.

---

## Success Criteria

* After RDP to fortna-wcs-primary.txrth.otnet.ups.com, SSMS connectivity check succeeds (you can connect).

## Failure Conditions

* SSMS connectivity check fails (cannot connect).

## Escalation Guidance

* If SSMS cannot connect after RDP to fortna-wcs-primary.txrth.otnet.ups.com, stop and escalate for deeper connectivity troubleshooting.

## Missing Details / Known Gaps

* The source does not specify SSMS connection target details (server/database name) or the exact SSMS UI fields/buttons to use for the connectivity attempt.
* The source does not provide the observable SSMS success/failure UI labels (e.g., exact dialog text) beyond the general instruction to 'check that you can connect'.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_check_sql_server_management_studio_connectivity
- Source ID: `training_video_day2`
- Source Type: `training_video`
