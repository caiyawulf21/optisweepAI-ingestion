# Use Ignition log in the web UI to investigate Ignition-related issues before/around OptiSweep restart

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_ignition_log_web_ui_investigate_ignition_issues_before_around_optsweep_restart_v1` |
| Title | Use Ignition log in the web UI to investigate Ignition-related issues before/around OptiSweep restart |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `gateway_health`, `wcs_api_responsiveness` |
| Access Surface | `tipper_hmi`, `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

When Ignition-related issues occur (for example, Ignition taking too long and OPC retry behaving oddly), use the Ignition log available in the Ignition web UI to review log evidence for the relevant time window. If logs/memory details are implicated, route the memory details question to controls as suggested by the source.

## When To Use

Use when Ignition issues are suspected as the cause of OptiSweep restart needs—specifically when Ignition “took too long” and the “retry”/OPC behavior is described as weird/odd, and you need evidence from the Ignition web UI log.

## Access Or Tools Needed

* Ignition web UI access
* Ability to view Ignition logs in the web UI (as referenced by the source)

## Related Operational Context

* ctx_training_video_ignition_web_ui_logs_v1
* ctx_training_video_ignition_optisweep_restart_context_v1

## Visual References

![artifact_training_video_training_video_day2_0041_this_is_just_the_gateway_and_primary_03_03_43_000](assets/ec2354c26e54703e.jpg)

*Ignition Gateway UI web browser view; source describes memory usage chart and that this is the Ignition performance page accessible via web browser.*

## Procedure Steps

### Step 1 — Open the Ignition web UI and locate the Ignition log referenced by the source

**Responsible role:** L2_support

**Instruction:**
Open the Ignition Gateway web UI in a web browser and navigate to the Ignition log area referenced by the source (the source explicitly states the Ignition log is “right in that web UI”).

**Expected result:**
You can view the Ignition log within the Ignition web UI.

**Stop or Escalate If:**

* If the Ignition log is not accessible or does not provide useful information, escalate to controls/support as suggested by the source.

---

### Step 2 — Review Ignition log entries for the time window when Ignition took too long / OPC retry behaved oddly

**Responsible role:** L2_support

**Instruction:**
In the Ignition web UI log view, review the log entries corresponding to the time window when Ignition “took too long” and when the “retry”/OPC behavior was described as weird/odd.

**Expected result:**
You identify relevant Ignition log entries that correspond to the symptom time window.

**Stop or Escalate If:**

* If the Ignition log is not accessible or does not provide useful information, escalate to controls/support as suggested by the source.

---

### Step 3 — If memory details are implicated, ask controls about logs and memory details

**Responsible role:** L2_support

**Instruction:**
If the investigation indicates memory details may be implicated, treat “logs and memory details” as items to ask controls about (per the source).

**Expected result:**
Controls are engaged for interpretation/confirmation of the implicated “logs and memory details.”

**Stop or Escalate If:**

* If controls cannot be engaged or memory details cannot be obtained, escalate to controls/support as suggested by the source.

---

## Success Criteria

* Ignition log is accessible in the Ignition web UI.
* Ignition log entries relevant to the symptom time window (Ignition taking too long / OPC retry behaving oddly) are identified.
* If memory details are implicated, controls are asked to review logs and memory details.

## Failure Conditions

* Ignition log is not accessible in the web UI.
* Ignition log does not provide useful information for the symptom window.

## Escalation Guidance

* If the Ignition log is not accessible or does not provide useful information, escalate to controls/support as suggested by the source.
* If memory details are implicated, ask controls about “logs and memory details” (source guidance).

## Missing Details / Known Gaps

* The packet does not include concrete navigation steps or specific UI labels/fields for the Ignition log view inside the web UI (candidate confidence is low until a segment with the actual UI elements is available).
* The packet does not specify the exact time-window selection mechanism (e.g., filters, timestamps, or controls) within the Ignition log UI.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_ignition_log_web_ui_check_for_ignition_issues
- Source ID: `training_video_day2`
- Source Type: `training_video`
