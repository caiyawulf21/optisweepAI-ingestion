# Check current secure connections via File > Connections window (test tunnel context)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_current_secure_connections_via_file_connections_window_test_tunnel_v1` |
| Title | Check current secure connections via File > Connections window (test tunnel context) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `gateway_health`, `wcs_api_responsiveness` |
| Access Surface | `wcs_api`, `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy`, `stunnel_or_chat_down` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep application UI to open File > Connections and view the current connections shown in the bottom area/pane. The source describes these as the current “secure connections,” which can be used while troubleshooting around test tunnel checks and related startup/delayed connectivity behavior.

## When To Use

When troubleshooting connectivity issues in the context of checking the test tunnel, and you need to view the current secure connections shown by the application’s File > Connections window.

## Do Not Use For

* Do not use this procedure as a complete connectivity remediation step; the source only instructs how to view the secure connections and does not provide additional corrective actions if the expected connections are not shown.

## Access Or Tools Needed

* OptiSweep application UI with a File menu
* Connections window accessible via File > Connections

## Related Operational Context

* ctx_training_video_network_connections_window_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0051_you_know_this_is_like_you_primary_03_13_45_500](assets/594db6d378d1227e.jpg)

*Frame showing the Connections window content (Network Connections / current connections list) referenced by the source while describing “secure connections.”*

## Procedure Steps

### Step 1 — Open the relevant application and navigate to File > Connections

**Responsible role:** L1_support

**Instruction:**
In the OptiSweep application, use the File menu and click Connections to open the Connections window.

**Expected result:**
The Connections window appears.

---

### Step 2 — Look at the bottom area where the source says it shows the current connections

**Responsible role:** L1_support

**Instruction:**
In the Connections window, check the bottom area/pane where the current connections are shown.

**Expected result:**
The bottom area/pane shows a list of current connections.

**Stop or Escalate If:**

* If the Connections window does not show current secure connections (i.e., no current connections list in the bottom area/pane), stop and escalate because the source provides no additional troubleshooting steps.

---

### Step 3 — Interpret the displayed connections as “secure connections” (per the source wording)

**Responsible role:** L1_support

**Instruction:**
Treat the connections shown in the bottom area/pane of the Connections window as the current “secure connections,” and use that observation as the connectivity state reference for the test tunnel troubleshooting context.

**Expected result:**
You can identify the current secure connections list displayed in the Connections window bottom area/pane.

**Stop or Escalate If:**

* If the secure connections list is not shown, stop and escalate (no further steps are provided in the source).

---

## Success Criteria

* File > Connections opens the Connections window.
* The bottom area/pane shows the current connections list.
* The current connections list is treated as the current “secure connections” per the source wording.

## Failure Conditions

* Connections window does not show current secure connections (no current connections list in the bottom area/pane).

## Escalation Guidance

* If the Connections window does not show current secure connections, stop and escalate because the source does not provide additional troubleshooting steps beyond viewing the secure connections.

## Missing Details / Known Gaps

* The source does not name the exact application window title for “Connections.”
* The source does not provide additional troubleshooting actions if the secure connections list is missing; escalation is required.

## Source Lineage

- Candidate IDs: candidate_training_video_day2_check_secure_connections_via_file_connections_window
- Source ID: `training_video_day2`
- Source Type: `training_video`
