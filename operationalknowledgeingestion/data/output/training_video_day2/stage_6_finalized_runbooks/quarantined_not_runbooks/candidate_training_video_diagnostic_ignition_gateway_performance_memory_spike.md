# Use Ignition Gateway Performance Page to Check for Memory Spike/Drop During a Crash

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_ignition_gateway_performance_page_to_check_memory_spike_drop_v1` |
| Title | Use Ignition Gateway Performance Page to Check for Memory Spike/Drop During a Crash |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `gateway_health` |
| Access Surface | `event_viewer`, `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `gateway_unhealthy` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Ignition Gateway performance page web UI to check whether the Gateway memory usage chart shows a spike followed by a drop to 0, which the source describes as a crash indicator.

## When To Use

When users report symptoms such as the hospital not working / not communicating information, and you want to check whether the Ignition Gateway shows a crash pattern using the Gateway performance page memory usage chart.

## Do Not Use For

* Do not use this check as the only proof that there was no Gateway issue; the source notes symptoms/calls may not always map directly to the first observed call/symptom.

## Access Or Tools Needed

* Web browser access to the Ignition Gateway status/performance page
* Ignition Gateway performance page UI (memory usage chart)

## Related Operational Context

* ctx_training_video_ignition_gateway_performance_page_v1
* ctx_training_video_gateway_memory_usage_metric_v1
* ctx_training_video_gateway_support_diagnostics_v1

## Visual References

![artifact_training_video_training_video_day2_0041_this_is_just_the_gateway_and_primary_03_03_43_000](assets/ec2354c26e54703e.jpg)

*Ignition Gateway performance page screenshot showing the memory usage chart and the described crash indicator (memory spiked then dropped to 0).*

## Procedure Steps

### Step 1 — Open the Ignition Gateway performance page in a web browser

**Responsible role:** L1_support

**Instruction:**
In a web browser, open the Ignition Gateway status/performance page using the URL shown in the source: http://localhost:8088/web/status/sys.performance? (as displayed in the source frames).

**Expected result:**
The Ignition Gateway performance page loads in the browser (the source describes it as the “performance page of Ignition itself”).

---

### Step 2 — Locate the memory usage chart on the performance page

**Responsible role:** L1_support

**Instruction:**
On the Ignition Gateway performance page, find the memory usage chart (described in the source as the “light chart… is the memory usage”).

**Expected result:**
The memory usage chart is visible on the performance page.

---

### Step 3 — Observe the memory usage trend for a crash pattern (spike then drop to 0)

**Responsible role:** L1_support

**Instruction:**
Watch the memory usage chart and check whether memory “spiked and then dropped to 0.”

**Expected result:**
The memory usage chart shows a spike followed by a drop to 0 (matching the source-described crash evidence).

---

### Step 4 — Decide whether to follow up based on the chart result

**Responsible role:** L1_support

**Instruction:**
If the memory chart shows the spike-then-drop-to-0 pattern, treat it as matching the source-described crash evidence for support follow-up. If it does not show that pattern but the issue is still reported, escalate to deeper Ignition service diagnostics.

**Expected result:**
Either (a) the chart matches the crash indicator pattern, or (b) the chart does not match and you escalate because the source warns symptoms may not map directly.

**Stop or Escalate If:**

* Issue is still reported, but the memory chart does not show the described spike-then-drop-to-0 pattern

---

## Success Criteria

* Memory usage chart shows a spike followed by a drop to 0 on the Ignition Gateway performance page.

## Failure Conditions

* Memory usage chart does not show the spike-then-drop-to-0 pattern while the issue is still being reported.

## Escalation Guidance

* If the memory chart does not show the described spike-then-drop-to-0 pattern but the issue is still reported, escalate to deeper Ignition service diagnostics.

## Missing Details / Known Gaps

* The source does not provide exact UI field/label names for the memory chart beyond “light chart” / “memory usage chart.”
* The source does not specify the exact time window or how to correlate the chart timeframe to the crash event.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_ignition_gateway_performance_memory_spike
- Source ID: `training_video_day2`
- Source Type: `training_video`
