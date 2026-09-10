# Check Ignition Gateway system performance status via Ignition Gateway UI

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_ignition_gateway_sys_perf_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `gateway_health` |
| Access Surface | `ignition_gateway` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the Ignition Gateway web UI to open the system performance status page for sys.perf and confirm the page loads and displays system performance status content.

## When To Use

When you need to verify that the Ignition Gateway system performance status page is reachable and that it shows sys.perf system performance status content.

## Source Procedure References

- proc_check_ignition_gateway_sys_perf_v1

## Procedure Steps

### Step 1 — Open the Ignition Gateway sys.perf system performance status page

**Responsible role:** L1_support

**Instruction:**
Using a web browser, navigate to http://localhost:8088/web/status/sys.perf.

**Expected result:**
The browser loads the Ignition Gateway sys.perf status page (i.e., not a browser error page).

---

### Step 2 — Confirm the loaded page corresponds to sys.perf and is not blank

**Responsible role:** L1_support

**Instruction:**
After the page loads, confirm the content corresponds to the sys.perf system performance status page and that the page shows system performance status information (not blank/failed content).

**Expected result:**
The sys.perf page displays system performance status information (visible performance/status content).

---

## Success Criteria

- http://localhost:8088/web/status/sys.perf loads successfully in the browser
- The sys.perf page displays system performance status information (not blank/failed content)

## Failure Conditions

- sys.perf page is unreachable or fails to load (connection refused/timeout)
- sys.perf page loads but system performance/status content is missing/blank

## Escalation Guidance

- If the sys.perf page is unreachable or fails to load, stop and escalate for Ignition gateway health investigation.
- If the sys.perf page loads but shows no system performance/status content, stop and escalate.

## Missing Details / Known Gaps

- The source does not provide specific field names/values or exact visual indicators on the sys.perf page beyond that it is a system performance status/performance page; success is therefore limited to page load and presence of visible performance/status content.
