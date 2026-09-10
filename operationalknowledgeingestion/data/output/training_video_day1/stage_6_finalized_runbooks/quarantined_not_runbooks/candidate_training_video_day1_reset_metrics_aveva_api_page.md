# Reset system metrics from the Overall System Aveva API page (Reset Metrics / A tag)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_system_metrics_overall_system_aveva_api_page_v1` |
| Title | Reset system metrics from the Overall System Aveva API page (Reset Metrics / A tag) |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | None |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

When system metrics need to be cleared, you can manually reset them from the UPSHMI “Overall System Aveva API” page using the “Reset Metrics” control (speaker notes UPSHMI resets the metric when an “A tag” is hit). Metrics also reset automatically when a new sort plan is loaded.

## When To Use

Use when you need to manually reset system metrics from the UPSHMI “Overall System Aveva API” page. The source also states metrics reset automatically when a new sort plan is loaded, but this procedure provides the manual reset control on that page.

## Access Or Tools Needed

* UPSHMI access to the “Overall System Aveva API” page
* On-screen controls: “Reset Metrics” and the “A tag” mentioned by the speaker

## Related Operational Context

* ctx_training_video_overall_system_aveva_api_page_v1
* ctx_training_video_reset_metrics_reference_v1

## Procedure Steps

### Step 1 — Open the “Overall System Aveva API” page in the UPSHMI interface

**Responsible role:** L1_support

**Instruction:**
In UPSHMI, navigate to the screen labeled “Overall System Aveva API”.

**Expected result:**
The “Overall System Aveva API” page is displayed with the “Reset Metrics” control visible.

---

### Step 2 — Locate the “Reset Metrics” control on the page

**Responsible role:** L1_support

**Instruction:**
On the “Overall System Aveva API” page, find the “Reset Metrics” control.

**Expected result:**
You can point to the “Reset Metrics” control on the “Overall System Aveva API” page.

---

### Step 3 — Manually reset metrics using the documented manual reset action (A tag / Reset Metrics)

**Responsible role:** L1_support

**Instruction:**
Use the manual reset action for “Reset Metrics” on the “Overall System Aveva API” page. The speaker notes UPSHMI resets the metric when an “A tag” is hit.

**Expected result:**
The manual reset action is executed for system metrics.

**Stop or Escalate If:**

* If the metrics do not reset after using the documented manual reset action, stop and escalate to support for deeper investigation.

---

### Step 4 — Confirm the metrics have been reset

**Responsible role:** L1_support

**Instruction:**
After triggering “Reset Metrics”, confirm that the system metrics reflect the reset state (the source states metrics reset automatically when a new sort plan is loaded and can also be manually reset from this page).

**Expected result:**
System metrics show the reset result after the manual action.

**Stop or Escalate If:**

* If the metrics do not reset after using the documented manual reset action, stop and escalate to support for deeper investigation.
* Do not rely on this action to fix underlying errors if “Get errors” indicates active issues.

---

## Success Criteria

* After using the “Reset Metrics” manual action (A tag), the system metrics reflect a reset state on the UPSHMI “Overall System Aveva API” page.

## Failure Conditions

* Metrics do not reset after triggering the manual “Reset Metrics” action.
* “Get errors” indicates active issues and metrics reset is attempted as a substitute for addressing those errors.

## Escalation Guidance

* If metrics do not reset after using the documented manual reset action, stop and escalate to support for deeper investigation.

## Missing Details / Known Gaps

* The source does not explicitly name the exact on-screen label/location for the “A tag” beyond the speaker note; the runbook uses the “Reset Metrics” control as the manual reset action.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_reset_metrics_aveva_api_page
- Source ID: `training_video_day1`
- Source Type: `training_video`
