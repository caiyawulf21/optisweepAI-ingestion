# Reset tipper stats from the Overall System Aveva API page (Reset Tipper Stats)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_tipper_stats_overall_system_aveva_api_page_v1` |
| Title | Reset tipper stats from the Overall System Aveva API page (Reset Tipper Stats) |
| Procedure Type | `recovery` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors` |
| Access Surface | None |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the “Reset Tipper Stats” control on the UPSHMI “Overall System Aveva API” page to manually reset tipper metrics/stats. The source also states tipper metrics reset automatically when a new sort plan is loaded, but the same metrics can be manually reset from this page.

## When To Use

When tipper metrics/stats need to be cleared and re-initialized manually from the UPSHMI “Overall System Aveva API” page using the “Reset Tipper Stats” control.

## Access Or Tools Needed

* UPSHMI access to the “Overall System Aveva API” page
* On-screen control: “Reset Tipper Stats”

## Related Operational Context

* ctx_training_video_overall_system_aveva_api_page_v1
* ctx_training_video_reset_tipper_stats_reference_v1

## Procedure Steps

### Step 1 — Open the “Overall System Aveva API” page in UPSHMI

**Responsible role:** L1_support

**Instruction:**
In UPSHMI, open the “Overall System Aveva API” page.

**Expected result:**
The “Overall System Aveva API” page is displayed and includes the “Reset Tipper Stats” control.

**Stop or Escalate If:**

* If the page does not display the “Reset Tipper Stats” control, stop and escalate for deeper troubleshooting.

---

### Step 2 — Locate the “Reset Tipper Stats” control on the page

**Responsible role:** L1_support

**Instruction:**
On the “Overall System Aveva API” page, find the “Reset Tipper Stats” control.

**Expected result:**
The “Reset Tipper Stats” control is located and ready to be used.

**Stop or Escalate If:**

* If “Reset Tipper Stats” is not visible, stop and escalate for deeper troubleshooting.

---

### Step 3 — Perform the manual reset action for “Reset Tipper Stats”

**Responsible role:** L1_support

**Instruction:**
Use the “Reset Tipper Stats” control on the “Overall System Aveva API” page to perform the manual reset action.

**Expected result:**
The manual reset action is executed (tipper metrics/stats are reset as described by the source).

**Stop or Escalate If:**

* If tipper stats do not change after the manual reset action, stop and escalate for deeper troubleshooting.
* If “Get errors” shows current errors, do not assume reset alone resolves the underlying issue.

---

### Step 4 — Verify that tipper stats/metrics have been reset

**Responsible role:** L1_support

**Instruction:**
Check the tipper metrics/stats area on the UPSHMI “Overall System Aveva API” page (or the metrics view opened from this page) to confirm the values reflect the reset.

**Expected result:**
Tipper stats/metrics show the reset effect consistent with the source statement that metrics reset on new sort plan load and can also be manually reset.

**Stop or Escalate If:**

* If tipper stats do not change after the manual reset action, stop and escalate for deeper troubleshooting.
* If “Get errors” shows current errors, do not assume reset alone resolves the underlying issue.

---

## Success Criteria

* After using “Reset Tipper Stats,” the displayed tipper metrics/stats reflect a reset (cleared/zeroed) state consistent with the source’s reset behavior.

## Failure Conditions

* Tipper stats/metrics do not change after the manual reset action.
* Current errors are present when checking via “Get errors,” indicating reset alone may not resolve the underlying issue.

## Escalation Guidance

* If tipper stats do not change after the manual reset action, stop and escalate for deeper troubleshooting.
* If “Get errors” shows current errors, do not assume reset alone resolves the underlying issue; escalate for deeper troubleshooting.

## Missing Details / Known Gaps

* The source does not specify the exact on-screen field(s) or numeric values that should change immediately after pressing “Reset Tipper Stats.”
* The source does not describe the exact interaction mechanics (e.g., confirmation dialog vs direct reset) beyond the general manual reset concept.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_reset_tipper_stats_aveva_api_page
- Source ID: `training_video_day1`
- Source Type: `training_video`
