# Confirm RMS-to-OptiSweep communication uses REST API (and avoid bypassing OptiSweep software)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_rms_to_optisweep_rest_api_boundary_v1` |
| Title | Confirm RMS-to-OptiSweep communication uses REST API (and avoid bypassing OptiSweep software) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `rms_ui`, `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `system_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When investigating an issue between the RMS and OptiSweep, treat the communication path as API-based—specifically REST API—and avoid sending requests in a way that bypasses the OptiSweep software flow. Bypassing OptiSweep software can leave OptiSweep unaware of the transaction (no knowledge of the database of that transaction), which can lead to out-of-sync behavior.

## When To Use

Use this when a support call involves an issue “between RMS and OptiSweep” and you need to frame the communication boundary correctly (REST API integration) and ensure you do not bypass OptiSweep software in a way that can desynchronize transaction visibility.

## Do Not Use For

* Do not use this as a step-by-step guide to perform direct/bypassing API transactions outside the documented OptiSweep software flow (the source explicitly warns against bypassing).
* Do not use this to obtain concrete request/response field mappings for REST calls; the source only points to where the API spec lives (Confluence) and does not provide field-level troubleshooting steps.

## Safety And Operational Notes

* Avoid bypassing OptiSweep software flow when sending API requests; the source warns this can cause OptiSweep to be unaware of the transaction and lead to out-of-sync behavior.

## Access Or Tools Needed

* RMS web application access (RMS web location; unique IP address; username/password mentioned in the segment)
* Confluence access to the API spec for both RMS and Geek Plus
* Awareness of REST API / Geek Plus API usage (as referenced by the segment)

## Related Operational Context

* ctx_training_video_rms_optisweep_api_integration_v1
* ctx_training_video_optisweep_sync_boundary_with_rms_v1

## Procedure Steps

### Step 1 — Treat RMS↔OptiSweep communication as REST API-based when investigating an issue

**Responsible role:** L2_support

**Instruction:**
When the issue is described as being “between RMS and OptiSweep,” frame the communication path as API-based and specifically REST API (as stated in the segment).

**Expected result:**
You can explain that RMS communicates with OptiSweep via REST API, and you align your investigation approach to that boundary.

---

### Step 2 — Do not bypass OptiSweep software flow when considering direct REST/API requests

**Responsible role:** L2_support

**Instruction:**
If you are considering sending requests directly (e.g., via Geek Plus API / REST API), verify that you are not bypassing the OptiSweep software flow. The segment warns that bypassing OptiSweep software can leave OptiSweep unaware of what happened and without knowledge of the database of that transaction.

**Expected result:**
You stop or avoid bypass actions and instead keep the OptiSweep software flow as the authoritative path for transactions.

**Stop or Escalate If:**

* If the investigation requires direct API actions beyond the documented support boundary (i.e., bypassing OptiSweep software flow), stop and escalate to the appropriate deep-dive/support session described by the training segment.

---

### Step 3 — Use the documented API specification location on Confluence for REST/API details

**Responsible role:** L2_support

**Instruction:**
If you need API specifications, use the documented location: the API spec is on Confluence for both RMS and Geek Plus.

**Expected result:**
You retrieve the correct API spec from Confluence for both RMS and Geek Plus to support your investigation within the supported boundary.

---

## Success Criteria

* Support can correctly state that RMS communicates with OptiSweep via REST API.
* Support avoids bypassing OptiSweep software flow and can explain the out-of-sync risk if bypass occurs (OptiSweep doesn’t know what happened; no knowledge of the database of that transaction).
* If API specifications are needed, support uses the Confluence API spec location for both RMS and Geek Plus.

## Failure Conditions

* Bypass actions are attempted such that OptiSweep software does not know what happened and lacks knowledge of the database of the transaction.
* API troubleshooting proceeds without using the referenced Confluence API spec location.

## Escalation Guidance

* If the investigation requires direct API actions beyond the documented support boundary (i.e., bypassing OptiSweep software flow), stop and escalate to the appropriate support/deep-dive session described by the training segment.

## Missing Details / Known Gaps

* The segment does not provide concrete REST API request/response fields, endpoints, or example payloads for RMS↔OptiSweep troubleshooting.
* The segment does not provide specific RMS UI navigation steps or specific system fault fields to check for this REST boundary topic (it only states that RMS web application exists and that the API spec is on Confluence).
* The segment references a deep-dive session for further details, but does not name the exact session title/agenda or provide a concrete escalation path beyond “later tomorrow/deep dive session.”

## Source Lineage

- Candidate IDs: candidate_training_video_day1_rms_optisweep_rest_api_boundary_check
- Source ID: `training_video_day1`
- Source Type: `training_video`
