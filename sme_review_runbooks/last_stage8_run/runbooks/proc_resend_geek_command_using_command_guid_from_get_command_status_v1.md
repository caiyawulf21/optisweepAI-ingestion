# Resend Geek command using the command GUID from Get Command Status (Geek Plus missed request recovery)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_resend_geek_command_using_command_guid_from_get_command_status_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Capability Tags | `agv_active_errors` |
| Access Surface | `rms_ui`, `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the command GUID shown in the live “Get Command Status” view to call the ResendGeekCommand function, which resends the request to Geek Plus. This is intended for recovery when Geek Plus may have missed the request after an unplanned restart.

## When To Use

When Geek Plus may have missed a command request after an unplanned restart, and you need to resend that Geek command using the command GUID visible in the live Get Command Status area.

## Source Procedure References

- proc_resend_geek_command_using_command_guid_from_get_command_status_v1

## Procedure Steps

### Step 1 — Open the live Get Command Status area and locate the command GUID

**Responsible role:** L2_support

**Instruction:**
In the live RMS / fleet status UI, open the area that includes “Get Command Status” (within the Get AGV status/command status view) and locate the main GUID / command GUID shown there.

**Expected result:**
A command GUID (main GUID/command GUID) is visible in the Get Command Status view.

---

### Step 2 — Invoke ResendGeekCommand using the command GUID

**Responsible role:** L2_support

**Instruction:**
Using the OptiSweep / WCS API client workflow, call ResendGeekCommand and provide the command GUID you identified from Get Command Status.

**Expected result:**
ResendGeekCommand is executed for the selected command GUID.

---

### Step 3 — Verify command status reflects the resend attempt

**Responsible role:** L2_support

**Instruction:**
Return to the live Get Command Status / command status view and observe for evidence that the resend was issued for the same command GUID (e.g., updated GET command status fields associated with that GUID).

**Expected result:**
The Get Command Status / command status view reflects the resend attempt for the same command GUID.

---

## Success Criteria

- ResendGeekCommand is executed using the command GUID from Get Command Status
- Get Command Status / command status view shows an observable update for the same command GUID after the resend attempt

## Failure Conditions

- Command GUID is not available in Get Command Status
- ResendGeekCommand cannot be executed due to missing/invalid GUID
- No observable change in command status for the same GUID after resend attempt

## Escalation Guidance

- Escalate if the command GUID is not available in Get Command Status or if the resend does not result in any observable change in command status for the same GUID.

## Missing Details / Known Gaps

- The packet does not provide the exact live UI/API client workflow for invoking ResendGeekCommand (e.g., which specific button/menu in RMS or which exact API client request fields beyond “command GUID”).
