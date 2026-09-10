# Use the HMI Memory Trend view to recognize a crash example (Memory Trend 4GB/3GB/2GB/0MB over time)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_hmi_memory_trend_view_to_recognize_crash_example_v1` |
| Title | Use the HMI Memory Trend view to recognize a crash example (Memory Trend 4GB/3GB/2GB/0MB over time) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `gateway_health` |
| Access Surface | `hospital_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

During a suspected crash, use the HMI Memory Trend view to confirm the displayed memory scale labels (4GB/3GB/2GB/0MB) and the time axis labels across the shown window, then describe the observed memory trend behavior relative to those labeled levels.

## When To Use

When you are diagnosing a suspected crash and need to visually confirm what the HMI Memory Trend chart is showing (GB/MB scale labels and the time axis) so you can describe the memory trend behavior over the displayed time window.

## Access Or Tools Needed

* HMI screen access to the "Memory Trend" view

## Related Operational Context

* ctx_training_video_crash_example_memory_trend_v1
* ctx_training_video_memory_trend_metric_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0042_this_is_an_example_of_a_primary_03_04_50_500](assets/cfaa60975c33aef8.jpg)

*HMI frame showing the "Memory Trend" chart with the 4GB/3GB/2GB/0MB scale and time labels 12:30–13:20 (crash example).*

## Procedure Steps

### Step 1 — Open/locate the HMI screen area that shows the "Memory Trend" display

**Responsible role:** L1_support

**Instruction:**
On the live HMI, navigate to the screen area that contains the chart labeled "Memory Trend".

**Expected result:**
You can point to the HMI "Memory Trend" chart area.

**Stop or Escalate If:**

* Memory Trend view cannot be found on the HMI

---

### Step 2 — Verify the Memory Trend scale/labels visible on the chart include "4GB", "3GB", "2GB", and "0MB"

**Responsible role:** L1_support

**Instruction:**
On the HMI Memory Trend chart, verify the visible scale labels include 4GB, 3GB, 2GB, and 0MB.

**Expected result:**
The chart shows the labeled levels "4GB", "3GB", "2GB", and "0MB".

**Stop or Escalate If:**

* Chart does not show the expected labeled scale elements (4GB/3GB/2GB/0MB)

---

### Step 3 — Check the time axis labels shown on the chart

**Responsible role:** L1_support

**Instruction:**
On the HMI Memory Trend chart, check the visible time axis labels (example shows labels such as 12:30 through 13:20).

**Expected result:**
The chart shows time axis labels across the displayed window (e.g., 12:30, 12:40, 12:50, 13:00, 13:10, 13:20 in the example).

**Stop or Escalate If:**

* Expected time axis labels are not visible/readable on the Memory Trend chart

---

### Step 4 — Observe the plotted memory behavior across the displayed time window and note which labeled levels (4GB/3GB/2GB/0MB) the trend approaches or reaches

**Responsible role:** L1_support

**Instruction:**
On the HMI Memory Trend chart, observe how the plotted memory values move across the time window and note whether the trend approaches or reaches the labeled levels (4GB/3GB/2GB/0MB).

**Expected result:**
You can describe the observed trend behavior relative to the labeled levels (e.g., whether it approaches/reaches 4GB, 3GB, 2GB, or 0MB during the shown window).

---

### Step 5 — Stop and escalate if the Memory Trend view is not present or expected labels/time axis are not visible

**Responsible role:** L1_support

**Instruction:**
If you cannot find the Memory Trend view, or if the chart does not show the expected labeled scale/time axis elements, stop this check and escalate for the correct crash diagnostic surface.

**Expected result:**
You stop the Memory Trend check and escalate due to missing/incorrect chart elements.

**Stop or Escalate If:**

* Memory Trend view cannot be found on the HMI
* Chart does not show expected labeled scale/time axis elements from the crash example

---

## Success Criteria

* On the live HMI, the "Memory Trend" chart is located and visible.
* The chart shows the labeled levels 4GB, 3GB, 2GB, and 0MB.
* The chart shows readable time axis labels across the displayed window (example: 12:30–13:20).
* You can describe the observed memory trend behavior relative to the labeled levels across the shown time window.

## Failure Conditions

* Memory Trend view cannot be found on the HMI.
* Expected scale labels (4GB/3GB/2GB/0MB) are missing or not visible.
* Expected time axis labels are missing or not visible/readable.
* Memory trend plot is not visible/legible such that you cannot compare it to labeled levels.

## Escalation Guidance

* If the Memory Trend view is not present or the expected labeled scale/time axis elements are not visible, stop and escalate for the correct crash diagnostic surface.

## Missing Details / Known Gaps

* The packet does not specify the exact HMI navigation path/menu name(s) to reach the Memory Trend view; it only provides the chart label and example frame evidence.
* The packet does not provide explicit thresholds or numeric interpretation rules for what memory behavior indicates a crash beyond observing the trend relative to the labeled levels.

## Source Lineage

- Candidate IDs: candidate_training_video_diagnostic_memory_trend_crash_example
- Source ID: `training_video_day2`
- Source Type: `training_video`
