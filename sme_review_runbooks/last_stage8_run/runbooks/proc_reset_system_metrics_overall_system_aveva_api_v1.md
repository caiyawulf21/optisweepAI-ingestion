# Reset system metrics from the Overall System Aveva API page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_system_metrics_overall_system_aveva_api_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `fleet_system_status` |
| Access Surface | `aveva_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the AVEVA HMI page labeled “Overall System Aveva API”, use “Reset Metrics” (and optionally “Reset Tipper Stats”) to clear metrics so the next metrics retrieval reflects the current sort plan state. Metrics also reset automatically when a new sort plan is loaded.

## When To Use

Use when the system metrics shown on the “Overall System Aveva API” page need to be cleared/restarted so the next metrics retrieval reflects the current sort plan state. Metrics also reset automatically when a new sort plan is loaded.

## Source Procedure References

- proc_reset_system_metrics_overall_system_aveva_api_v1

## Procedure Steps

### Step 1 — Open the AVEVA HMI “Overall System Aveva API” page

**Responsible role:** operator

**Instruction:**
Open the AVEVA HMI page labeled “Overall System Aveva API”.

**Expected result:**
The page displays the “Reset Metrics” control and the “Reset Tipper Stats” control.

---

### Step 2 — Reset system metrics

**Responsible role:** operator

**Instruction:**
Click the control labeled “Reset Metrics”.

**Expected result:**
The metrics are reset on the page (the page indicates metrics are reset).

---

### Step 3 — Optionally reset tipper stats

**Responsible role:** operator

**Instruction:**
If needed, click “Reset Tipper Stats” on the same “Overall System Aveva API” page.

**Expected result:**
Tipper stats are reset on the page (tipper metrics are cleared so they can be re-collected).

---

### Step 4 — Proceed to the next metrics retrieval after reset

**Responsible role:** operator

**Instruction:**
Stop once the reset action has been performed and the page is ready for the next metrics retrieval (for example, use “Get metrics” if you need to repopulate the metrics view).

**Expected result:**
The page is ready for the next metrics retrieval action (e.g., “Get metrics” is available to repopulate the metrics view).

---

## Success Criteria

- After clicking “Reset Metrics”, the page indicates metrics are reset.
- If “Reset Tipper Stats” is used, tipper metrics are reset/cleared so they can be re-collected.
- The page is ready for the next metrics retrieval (e.g., “Get metrics” can be used to repopulate the metrics view).

## Failure Conditions

- Reset controls do not appear to take effect (metrics do not clear/restart).
- Tipper stats do not clear/restart after using “Reset Tipper Stats” (if used).

## Escalation Guidance

- If the reset controls do not appear to take effect (metrics do not clear/restart), stop and escalate to support for further investigation of the AVEVA/metrics behavior.

## Missing Details / Known Gaps

- The packet does not specify the exact on-screen text/state that confirms metrics have reset (beyond the general statement that the page indicates metrics are reset).
