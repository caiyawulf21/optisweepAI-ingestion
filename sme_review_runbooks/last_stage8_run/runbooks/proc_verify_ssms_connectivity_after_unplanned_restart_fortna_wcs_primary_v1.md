# Verify SQL Server Management Studio connectivity after an unplanned restart on the FORTNA WCS primary host

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_ssms_connectivity_after_unplanned_restart_fortna_wcs_primary_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Capability Tags | `wcs_service_health` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

After an unplanned restart on the FORTNA WCS primary host, use RDP to open SQL Server Management Studio (SSMS) and confirm that you can successfully connect to the SQL Server on the host named fortna-wcs-primary.txrth.otnet.ups.com.

## When To Use

Use this as a basic validation step after an unplanned restart on the FORTNA WCS primary host to confirm SSMS connectivity before deeper service/DB connectivity troubleshooting.

## Source Procedure References

- proc_verify_ssms_connectivity_after_unplanned_restart_fortna_wcs_primary_v1

## Procedure Steps

### Step 1 — RDP to the FORTNA WCS primary host named in the check

**Responsible role:** L2_support

**Instruction:**
Use RDP to connect to the host named fortna-wcs-primary.txrth.otnet.ups.com.

**Expected result:**
You are connected to the host fortna-wcs-primary.txrth.otnet.ups.com and can launch applications on it.

---

### Step 2 — Open SQL Server Management Studio (SSMS) on the connected host

**Responsible role:** L2_support

**Instruction:**
On the connected host, open SQL Server Management Studio (SSMS).

**Expected result:**
SSMS launches successfully and is ready for a connection attempt.

---

### Step 3 — Attempt the SSMS connectivity check and confirm success

**Responsible role:** L2_support

**Instruction:**
In SSMS, perform the connectivity check by verifying that you can connect (the connection attempt succeeds rather than failing).

**Expected result:**
The SSMS connection attempt succeeds (i.e., you are able to establish a connection rather than receiving a connection failure).

---

### Step 4 — Stop and escalate if SSMS connectivity fails

**Responsible role:** L2_support

**Instruction:**
If SSMS cannot connect, stop and escalate for further service/DB connectivity troubleshooting; do not proceed with dependent checks.

**Expected result:**
A failure outcome is recognized and escalation is initiated rather than continuing with downstream validation steps.

---

## Success Criteria

- SSMS connectivity check succeeds: the SSMS connection attempt to the SQL Server on fortna-wcs-primary.txrth.otnet.ups.com succeeds.

## Failure Conditions

- SSMS connection attempt fails (cannot establish a connection).

## Escalation Guidance

- If SSMS cannot connect, stop and escalate for further service/DB connectivity troubleshooting (do not proceed with dependent checks).

## Missing Details / Known Gaps

- The packet does not specify the SSMS server/instance name, authentication method, or exact UI fields to use for the connection attempt; the procedure only requires confirming that the connection attempt succeeds vs fails.
