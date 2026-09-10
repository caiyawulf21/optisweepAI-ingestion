# Open Ignition Gateway locally in a browser and view the system performance status page (sys.perf)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_ignition_gateway_sys_perf_local_v1` |
| Title | Open Ignition Gateway locally in a browser and view the system performance status page (sys.perf) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `gateway_health` |
| Access Surface | `ignition_gateway`, `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `api_unresponsive`, `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the locally hosted Ignition Gateway web UI to open the system performance status page at http://localhost:8088/web/status/sys.perf for a quick, observable check during troubleshooting/inspection.

## When To Use

When you need to verify that the locally hosted Ignition Gateway performance status page is reachable and displays the system performance (sys.perf) view for support troubleshooting.

## Do Not Use For

* Do not use this procedure as a basis for configuration changes if the localhost URL or the sys.perf status page does not load.

## Access Or Tools Needed

* Web browser
* Local network access to the Ignition Gateway host (localhost:8088 as shown in the source)
* Ignition Gateway web UI

## Related Operational Context

* ctx_training_video_local_gateway_access_example_v1
* ctx_training_video_sys_perf_status_path_v1

## Visual References

![artifact_training_video_training_video_day2_0045_that_we_could_have_running_locally_primary_03_09_39_500](assets/120f5e2da0503667.jpg)

*Frame showing the Ignition Gateway UI accessed via browser and the sys.perf status path on localhost:8088 (/web/status/sys.perf).*

## Procedure Steps

### Step 1 — Open a web browser on the machine with local Ignition Gateway access

**Responsible role:** L1_support

**Instruction:**
On a machine that has access to the local Ignition Gateway, open a web browser.

**Expected result:**
A browser session is ready to navigate to the local Ignition Gateway URL.

---

### Step 2 — Navigate to the Ignition Gateway system performance status page (sys.perf)

**Responsible role:** L1_support

**Instruction:**
In the browser address bar, navigate to: http://localhost:8088/web/status/sys.perf

**Expected result:**
The browser displays the Ignition Gateway system performance status page at the /web/status/sys.perf path using localhost:8088.

**Stop or Escalate If:**

* If the localhost URL does not load or the sys.perf status page is unavailable, stop and escalate (no recovery steps are provided in the source).

---

### Step 3 — Confirm the page is the Ignition Gateway system performance status view (sys.perf)

**Responsible role:** L1_support

**Instruction:**
Verify that the loaded page corresponds to the Ignition Gateway system performance status page (sys.perf) for the local gateway.

**Expected result:**
The browser shows the Ignition Gateway system performance status page for sys.perf.

**Stop or Escalate If:**

* If the page does not load or sys.perf status is unavailable, stop and escalate rather than making configuration changes based only on this snippet.

---

## Success Criteria

* Browser successfully loads http://localhost:8088/web/status/sys.perf and displays the Ignition Gateway system performance status page (sys.perf).

## Failure Conditions

* localhost URL does not load
* sys.perf status page is unavailable

## Escalation Guidance

* If the localhost URL does not load or the sys.perf status page is unavailable, stop and escalate to support. The source provides no further recovery steps.

## Missing Details / Known Gaps

* The source packet does not specify what exact fields/metrics on the sys.perf page should be interpreted for troubleshooting beyond confirming the page loads.
* The source packet does not provide any recovery actions if the sys.perf page fails to load (only stop and escalate).

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_ignition_gateway_local_sys_perf
- Source ID: `training_video_day2`
- Source Type: `training_video`
