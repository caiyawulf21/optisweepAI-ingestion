# Use Memory Trend to Identify Service Crash/Restart vs Garbage Collection Pattern

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_memory_trend_identify_service_crash_restart_gc_v1` |
| Title | Use Memory Trend to Identify Service Crash/Restart vs Garbage Collection Pattern |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_service_health` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `service_crash_or_restart`, `shutdown_or_dwell_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the OptiSweep Memory Trend (memory over time) view to correlate a crash/service-stop window (silent period / service gone) with a garbage-collection memory-clearing pattern, then confirm memory build-up and resumed activity after the clearing.

## When To Use

When you need to interpret a Memory Trend chart to determine whether a service likely stopped/crashed and later restarted, and whether a garbage-collection memory-clearing pattern explains the memory drop followed by memory build-up.

## Do Not Use For

* Do not conclude a crash occurred if the Memory Trend pattern is ambiguous and you cannot match the described sequence (spike → long activity/draft → silent/nothing period → garbage-collection clearing → memory fills up again).

## Access Or Tools Needed

* Memory Trend display/view (shown as “Memory Trend 4GB”)
* Ability to view the memory trend over time

## Related Operational Context

* ctx_training_video_memory_trend_screen_v1
* ctx_training_video_garbage_collection_memory_pattern_v1
* ctx_training_video_service_stop_silent_logs_v1

## Visual References

![artifact_training_video_training_video_day2_0044_probably_understand_this_so_if_the_primary_03_07_17_500](assets/0f6cee71bf142dce.jpg)

*Memory Trend chart frame labeled “Memory Trend 4GB” used to identify the spike, long draft/activity, silent/nothing period, and garbage-collection clearing pattern.*

## Procedure Steps

### Step 1 — Open the Memory Trend view used for service behavior interpretation

**Responsible role:** L1_support

**Instruction:**
Open the Memory Trend display/view that shows the memory chart labeled “Memory Trend 4GB”.

**Expected result:**
You can see the Memory Trend 4GB chart with a time axis so you can identify the spike and subsequent segments.

---

### Step 2 — Locate the “good spike in the middle” and surrounding long activity/silent pattern

**Responsible role:** L1_support

**Instruction:**
On the Memory Trend 4GB chart, find the “good spike in the middle,” then identify the surrounding sequence: a big draft/long activity period, followed by a period of “nothing”/silent, and then activity again.

**Expected result:**
You can point to chart regions matching: (1) a “good spike in the middle,” (2) a big draft/long period, (3) a “nothing”/silent gap, and (4) activity resuming after the gap.

---

### Step 3 — Identify the garbage-collection portion where memory clears and then fills up again

**Responsible role:** L1_support

**Instruction:**
On the same Memory Trend 4GB chart, identify the “garbage collection” portion: memory clears out (a drop/clearing), followed by memory filling up again.

**Expected result:**
You can identify a memory-clearing segment consistent with “garbage collection” and then a subsequent memory build-up segment.

---

### Step 4 — Correlate the silent period with the expected ~10–12 minute service-stop/crash window

**Responsible role:** L1_support

**Instruction:**
Measure/estimate the duration of the “nothing”/silent gap on the Memory Trend chart and correlate it with the source’s expectation that the service can be silent for almost 10–12 minutes during the stop/crash window.

**Expected result:**
The silent/nothing gap duration on the chart is consistent with an approximately 10–12 minute window as described by the source.

---

### Step 5 — Explain whether the service likely stopped due to a crash and restarted after memory cleared

**Responsible role:** L1_support

**Instruction:**
Using the matched chart sequence (spike → big draft/long activity → silent/nothing period → garbage collection memory clearing → memory fills up again), determine whether it is consistent with the source’s crash/service-stop and later restart behavior.

**Expected result:**
Your interpretation can point to the chart segments that match the source’s described sequence and supports a crash/stop + restart explanation when the pattern is clear.

**Stop or Escalate If:**

* If the Memory Trend pattern cannot be matched to the described crash/silent/log-gap behavior, escalate for deeper log/service verification beyond the chart interpretation described in the source.
* Do not assume a crash occurred solely from the chart if the pattern is ambiguous.

---

## Success Criteria

* You can identify on the Memory Trend 4GB chart: a “good spike in the middle,” a big draft/long activity period, a “nothing”/silent gap, a garbage-collection memory-clearing segment, and subsequent memory build-up.
* The silent gap duration is consistent with the source’s expectation of almost 10–12 minutes where logs may be silent.
* Your conclusion distinguishes a likely crash/stop + restart pattern from garbage-collection clearing when the chart sequence matches clearly.

## Failure Conditions

* Memory Trend 4GB does not show a clear silent/nothing gap or does not show a garbage-collection clearing followed by memory build-up.
* The chart pattern is ambiguous such that you cannot confidently match the described crash/silent/log-gap sequence.

## Escalation Guidance

* If the Memory Trend pattern cannot be matched to the described crash/silent/log-gap behavior, escalate for deeper log/service verification beyond chart interpretation.
* If the pattern is ambiguous, do not assume a crash occurred solely from the chart.

## Missing Details / Known Gaps

* Exact navigation steps to open the Memory Trend view are not provided in the packet; only the chart label “Memory Trend 4GB” is referenced.
* The source does not provide explicit service names, specific Windows service identifiers, or exact log locations/queries; escalation is recommended when the chart pattern is ambiguous.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_memory_trend_service_crash_garbage_collection
- Source ID: `training_video_day2`
- Source Type: `training_video`
