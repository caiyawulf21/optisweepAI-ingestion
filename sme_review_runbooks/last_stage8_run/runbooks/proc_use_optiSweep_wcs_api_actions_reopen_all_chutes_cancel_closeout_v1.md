# Use OptiSweep/WCS API actions to reopen all chutes and cancel closeout exchanges

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_optiSweep_wcs_api_actions_reopen_all_chutes_cancel_closeout_v1` |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Capability Tags | `bag_out_or_closeout_state` |
| Access Surface | `apidog`, `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the OptiSweep / WCS API client (Apidog / WCS API) to (1) reopen any previously closed shoots/chutes and (2) cancel closeout exchanges that are not currently in progress. This is intended for recovery after a customer manual bag-out/closeout where the sort was not cycled.

## When To Use

When a customer did a manual bag out/closeout and the system needs to start up again without cycling the sort.

## Source Procedure References

- proc_use_optiSweep_wcs_api_actions_reopen_all_chutes_cancel_closeout_v1

## Procedure Steps

### Step 1 — Open the OptiSweep / WCS API client (Apidog / WCS API)

**Responsible role:** L1_support

**Instruction:**
Open the OptiSweep / WCS API client (Apidog / WCS API) and navigate to the System actions list.

**Expected result:**
The API client shows the available System actions, including the action named "Open All Chutes".

---

### Step 2 — Execute "Open All Chutes"

**Responsible role:** L1_support

**Instruction:**
Select the System action named "Open All Chutes" and execute it.

**Expected result:**
The "Open All Chutes" call completes successfully and returns a successful API response/status (no error).

---

### Step 3 — Verify "Open All Chutes" success via API response/status

**Responsible role:** L1_support

**Instruction:**
Check the API response/status returned by the "Open All Chutes" call and confirm it indicates success (no error).

**Expected result:**
"Open All Chutes" shows a successful API response/status.

---

### Step 4 — Execute "Cancel Close Out" (only if closeout exchanges are not in progress)

**Responsible role:** L1_support

**Instruction:**
If there are closeout exchanges that are not in progress, select the System action named "Cancel Close Out" and execute it.

**Expected result:**
The "Cancel Close Out" call completes successfully and returns a successful API response/status (no error).

---

### Step 5 — Verify "Cancel Close Out" success via API response/status

**Responsible role:** L1_support

**Instruction:**
Check the API response/status returned by the "Cancel Close Out" call and confirm it indicates success (no error).

**Expected result:**
"Cancel Close Out" shows a successful API response/status.

---

### Step 6 — Stop after both API calls succeed; do not perform additional system state changes

**Responsible role:** L1_support

**Instruction:**
Once both API calls have returned successful responses, stop the procedure and do not attempt additional system state changes in this procedure.

**Expected result:**
Procedure ends after successful completion of the executed actions.

---

## Success Criteria

- The "Open All Chutes" API call returns a successful response/status.
- If closeout exchanges were not in progress, the "Cancel Close Out" API call returns a successful response/status.

## Failure Conditions

- Either API call returns an error or does not complete successfully.
- After "Open All Chutes" succeeds, the system still appears to have closed chutes (requires deeper troubleshooting/escalation).

## Escalation Guidance

- Escalate if either API call returns an error or does not complete successfully (do not continue with other system actions in this procedure).
- If the system still appears to have closed chutes after "Open All Chutes" succeeds, escalate for deeper troubleshooting of system state/exchange status.

## Missing Details / Known Gaps

- The source does not provide the exact Apidog endpoint names/parameters or the exact success response fields; verification is therefore limited to confirming the call returns a successful response/status in the API client.
