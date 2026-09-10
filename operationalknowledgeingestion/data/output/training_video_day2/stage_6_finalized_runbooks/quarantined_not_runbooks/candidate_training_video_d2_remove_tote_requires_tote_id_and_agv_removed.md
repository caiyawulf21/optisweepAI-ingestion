# Remove tote from the system: ensure AGV is removed first and provide tote ID

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_tote_ensure_agv_removed_and_provide_tote_id_v1` |
| Title | Remove tote from the system: ensure AGV is removed first and provide tote ID |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `tote_lifecycle_state` |
| Access Surface | `wcs_api` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Removing a tote requires a tote ID, and the AGV must be removed before the tote can be removed.

## When To Use

Use when you need to remove a tote from the system and the system enforces the dependency that the AGV must be removed first, and you must supply a tote ID to perform the removal.

## Access Or Tools Needed

* OptiSweep/WCS API access (tote-related APIs are referenced in the source).

## Related Operational Context

* ctx_training_video_tote_removal_dependency_v1

## Visual References

![artifact_training_video_training_video_day2_0030_get_agv_status_shows_the_current_primary_02_43_04_500](assets/30f5c770747ce298.jpg)

*Frame showing GetAGVStatuses behavior (AGV state/command/vitals/errors) to support confirming AGV removal status before tote removal.*

![artifact_training_video_training_video_day2_0031_for_totes_we_have_exchange_sorter_primary_02_44_11_000](assets/54d41adfcf4b3f8f.jpg)

*Frame showing tote API notes including: 'Remove to requires a tote ID' and 'AGV must be removed before the tote can be removed.'*

## Procedure Steps

### Step 1 — Confirm you have the tote ID required to remove the tote

**Responsible role:** L1_support

**Instruction:**
Obtain the tote ID for the tote you intend to remove so you can supply it to the tote removal action.

**Expected result:**
You have a tote ID available to use for the tote removal request.

---

### Step 2 — Ensure the AGV is removed before attempting tote removal

**Responsible role:** L1_support

**Instruction:**
Before issuing the tote removal action, confirm the AGV is removed (the dependency is: AGV removal must happen first). Use the AGV status view/API behavior described in the source to verify AGV state/command/errors as needed.

**Expected result:**
The AGV is confirmed removed (so the dependency is satisfied) before you proceed with tote removal.

**Stop or Escalate If:**

* If the AGV cannot be confirmed as removed, do not proceed with tote removal; re-check AGV removal status first.

---

### Step 3 — Execute tote removal using the tote ID

**Responsible role:** L1_support

**Instruction:**
Execute the documented tote removal action using the tote ID you confirmed in Step 1 (after AGV removal is confirmed in Step 2).

**Expected result:**
The tote is removed from the system after the AGV has been removed.

**Stop or Escalate If:**

* If the tote cannot be removed, re-check that the AGV has been removed and that the tote ID is correct; then escalate if still blocked.

---

## Success Criteria

* Tote removal completes such that the tote is removed from the system.
* AGV removal is confirmed prior to tote removal (dependency satisfied).

## Failure Conditions

* Tote removal fails and the tote remains in the system.
* AGV was not removed prior to tote removal attempt.
* Tote ID provided is incorrect.

## Escalation Guidance

* If the tote cannot be removed after re-checking AGV removal status and tote ID correctness, escalate.

## Missing Details / Known Gaps

* The source does not provide the exact API/method name or request/response fields for the 'Remove tote' action in the provided text; only the dependency (tote ID required, AGV removed first) is stated.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_remove_tote_requires_tote_id_and_agv_removed
- Source ID: `training_video_day2`
- Source Type: `training_video`
