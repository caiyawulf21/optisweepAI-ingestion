# Remove a tote from the system (Remove tote requires tote ID; AGV must be removed first)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_tote_requires_toteid_agv_removed_dependency_v1` |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Capability Tags | `bag_out_or_closeout_state`, `wcs_api_responsiveness` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Remove a tote from the system using the OptiSweep / WCS API, but only after confirming the required dependency: the AGV must be removed before the tote can be removed. The tote removal request requires a ToteID.

## When To Use

When you need to remove a tote from the system and the system enforces the dependency that the AGV must be removed first; the tote removal request requires a ToteID.

## Source Procedure References

- proc_remove_tote_requires_toteid_agv_removed_dependency_v1

## Procedure Steps

### Step 1 — Confirm the AGV is removed before attempting tote removal

**Responsible role:** L2_support

**Instruction:**
Before you attempt the tote removal request in the OptiSweep / WCS API client (Apidog / WCS API), confirm the AGV-removed dependency is satisfied (AGV must be removed before the tote can be removed).

**Expected result:**
You have confirmed that the AGV removal dependency is satisfied prior to sending the tote removal request.

---

### Step 2 — Send tote removal request using required ToteID via Apidog / WCS API

**Responsible role:** L2_support

**Instruction:**
In the OptiSweep / WCS API client (Apidog / WCS API), perform the tote removal action using the required ToteID.

**Expected result:**
A tote removal request is sent that includes the required ToteID.

---

### Step 3 — Verify API response confirms tote removal

**Responsible role:** L2_support

**Instruction:**
Observe the API response/result from the tote removal request to confirm the tote is removed from the system.

**Expected result:**
The API response/result indicates success/removal confirmation for the tote removal request.

---

## Success Criteria

- Tote removal succeeds only after the AGV is removed.
- The tote is removed from the system when the tote removal request includes the required ToteID.

## Failure Conditions

- Tote removal fails due to AGV not removed dependency.
- API rejects tote removal even after AGV removal.

## Escalation Guidance

- If tote removal continues to be rejected after confirming the AGV-removed dependency is satisfied, escalate because the API continues to reject removal even after AGV removal.

## Missing Details / Known Gaps

- The source does not provide the specific tote-removal API endpoint name, request field names (beyond the requirement for ToteID), or the exact success/failure response payload/status fields to check in Apidog.
- The source does not provide a live UI/API evidence frame showing the tote removal request form fields (ToteID input) or the removal response payload/status.
