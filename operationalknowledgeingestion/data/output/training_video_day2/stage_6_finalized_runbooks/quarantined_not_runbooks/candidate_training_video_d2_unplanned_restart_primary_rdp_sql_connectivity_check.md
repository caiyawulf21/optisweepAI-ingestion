# Verify SQL connectivity after unplanned restart by RDP to fortna-wcs-primary and connecting via SSMS

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_sql_connectivity_after_unplanned_restart_primary_rdp_ssms_v1` |
| Title | Verify SQL connectivity after unplanned restart by RDP to fortna-wcs-primary and connecting via SSMS |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

After an unplanned restart, RDP into the primary server (fortna-wcs-primary.txrth.otnet.ups.com) and use SQL Server Management Studio (SSMS) to confirm you can connect to the SQL instance. A successful SSMS connection is the observable evidence that the restarted SQL services are up and running.

## When To Use

Use when an unplanned restart has occurred and you need to verify that the primary server is reachable and that SQL connectivity works from the current support/session.

## Access Or Tools Needed

* RDP access to fortna-wcs-primary.txrth.otnet.ups.com
* SQL Server Management Studio (SSMS)

## Related Operational Context

* ctx_training_video_unplanned_restart_primary_rdp_v1
* ctx_training_video_sql_server_management_studio_reference_v1
* ctx_training_video_sql_services_running_status_v1

## Visual References

![artifact_training_video_training_video_day2_0048_you_unplanned_restart_again_from_your_primary_03_12_51_000](assets/fa52ee0845d1af6a.jpg)

*Frame showing the instruction to RDP into fortna-wcs-primary.txrth.otnet.ups.com and open SSMS to check that you can connect.*

![artifact_training_video_training_video_day2_0050_just_make_sure_it_s_good_primary_03_13_25_500](assets/26787b28eb66297d.jpg)

*Frame reinforcing the SSMS connectivity check (“Just make sure it’s good.”).*

## Procedure Steps

### Step 1 — RDP into the primary server fortna-wcs-primary.txrth.otnet.ups.com

**Responsible role:** L2_support

**Instruction:**
From your support session, RDP into the primary server named in the source: fortna-wcs-primary.txrth.otnet.ups.com.

**Expected result:**
You have an active RDP session to fortna-wcs-primary.txrth.otnet.ups.com.

**Stop or Escalate If:**

* If you cannot reach the primary via RDP, stop and escalate for deeper troubleshooting (the source only specifies the connectivity check after RDP).

---

### Step 2 — Open SQL Server Management Studio (SSMS) and attempt to connect

**Responsible role:** L2_support

**Instruction:**
In the RDP session, open SQL Server Management Studio (SSMS) and attempt to connect to the SQL instance on the primary server. The source’s check is to confirm that you can connect.

**Expected result:**
SSMS connection attempt succeeds (you can connect).

**Stop or Escalate If:**

* If SSMS cannot connect to the primary SQL endpoint, stop and escalate for deeper troubleshooting (the source only specifies the connectivity check).

---

### Step 3 — Confirm restarted SQL services are up and running (via successful SSMS connectivity)

**Responsible role:** L2_support

**Instruction:**
After the SSMS connectivity check, confirm the source-stated expectation by using the successful SSMS connection as the observable evidence that the SQL services/sequels are up and running.

**Expected result:**
SSMS connectivity is successful, consistent with the source instruction to ensure the sequels are up and running.

**Stop or Escalate If:**

* If SSMS connectivity does not succeed, stop and escalate for deeper troubleshooting (the source only specifies the connectivity check).

---

## Success Criteria

* SSMS can connect to the SQL instance on the primary server after the unplanned restart.

## Failure Conditions

* SSMS cannot connect to the primary SQL endpoint after the unplanned restart.

## Escalation Guidance

* If SSMS cannot connect to the primary SQL endpoint, stop and escalate for deeper troubleshooting (the source only specifies the connectivity check).

## Missing Details / Known Gaps

* The source does not specify the SSMS instance name, database name, or exact connection fields to enter; the runbook therefore keeps the check at the level of “attempt to connect and confirm success.”

## Source Lineage

- Candidate IDs: candidate_training_video_d2_unplanned_restart_primary_rdp_sql_connectivity_check
- Source ID: `training_video_day2`
- Source Type: `training_video`
