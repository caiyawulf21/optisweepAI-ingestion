# View system metrics via “Get metrics” pop-up on the Overall System Aveva API page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_system_metrics_get_metrics_popup_overall_system_aveva_api_v1` |
| Title | View system metrics via “Get metrics” pop-up on the Overall System Aveva API page |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `wcs_api_responsiveness` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `web_app_fault` |
| Validation Status | `needs_smeme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the “Get metrics” control on the Overall System Aveva API page in UPSHMI to open the metrics pop-up/page that displays all system metrics.

## When To Use

When you need to retrieve and view all system metrics from the UPSHMI Overall System Aveva API page using the “Get metrics” pop-up.

## Access Or Tools Needed

* UPSHMI access to the “Overall System Aveva API” page
* On-screen control: “Get metrics”
* Metrics pop-up/page display

## Related Operational Context

* ctx_training_video_overall_system_aveva_api_page_v1
* ctx_training_video_metrics_and_errors_popups_v1

## Procedure Steps

### Step 1 — Open the “Overall System Aveva API” page in UPSHMI

**Responsible role:** L1_support

**Instruction:**
In UPSHMI, open the “Overall System Aveva API” page.

**Expected result:**
The “Overall System Aveva API” page is displayed with controls including “Get metrics”.

**Stop or Escalate If:**

* If you cannot reach the page or cannot find the “Get metrics” control, stop and escalate to support.

---

### Step 2 — Locate the “Get metrics” control on the Overall System Aveva API page

**Responsible role:** L1_support

**Instruction:**
On the “Overall System Aveva API” page, locate the control labeled “Get metrics”.

**Expected result:**
The “Get metrics” control is located and ready to be selected.

**Stop or Escalate If:**

* If “Get metrics” is not visible on the page, stop and escalate to support.

---

### Step 3 — Select “Get metrics” to open the metrics pop-up/page

**Responsible role:** L1_support

**Instruction:**
Select “Get metrics” on the Overall System Aveva API page.

**Expected result:**
A metrics pop-up/page appears showing the system metrics.

**Stop or Escalate If:**

* If the metrics pop-up does not appear, stop and escalate to support.
* If the metrics pop-up appears but does not reflect expected system state, consider checking “Get errors” as described by the source.

---

### Step 4 — Review the displayed system metrics on the pop-up/page

**Responsible role:** L1_support

**Instruction:**
On the metrics pop-up/page, review the displayed system metrics values/fields.

**Expected result:**
The metrics pop-up/page shows all system metrics (as indicated by the “Get metrics” behavior).

**Stop or Escalate If:**

* If metrics appear but do not reflect expected system state, consider checking “Get errors” as described by the source.

---

## Success Criteria

* Selecting “Get metrics” opens the metrics pop-up/page.
* The metrics pop-up/page displays system metrics (i.e., “Get metrics gets all the system metrics”).

## Failure Conditions

* Metrics pop-up/page does not appear after selecting “Get metrics”.
* Metrics pop-up/page appears but does not reflect expected system state.

## Escalation Guidance

* If the metrics pop-up does not appear, stop and escalate to support.
* If metrics appear but do not reflect expected system state, check “Get errors” (also a pop-up on the Overall System Aveva API page) as the next diagnostic step.

## Missing Details / Known Gaps

* The packet does not provide the specific names/labels of the individual system metric fields shown on the metrics pop-up/page.

## Source Lineage

- Candidate IDs: candidate_training_video_day1_get_metrics_popup_aveva_api_page
- Source ID: `training_video_day1`
- Source Type: `training_video`
