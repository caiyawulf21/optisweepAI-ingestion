# Use Summary Counts To Check Active And Charging Robots

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_summary_counts_to_check_active_and_charging_robots_v1` |
| Title | Use Summary Counts To Check Active And Charging Robots |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the map monitor summary area to identify the displayed count of robots actively running in the system and the displayed count of robots actively charging.

## When To Use

Use this reference when you need to read the map monitor summary metrics for active robot count and charging robot count.

## Do Not Use For

* Do not use these counts alone to infer performance conditions.
* Do not use these counts alone to infer fault conditions.
* Do not use this procedure as a corrective action; the source supports reading the counts, not acting on them.

## Safety And Operational Notes

* This source supports viewing summary metrics only.
* Escalate if the displayed counts appear inconsistent with the visible system state and the source provides no further explanation.

## Access Or Tools Needed

* Access to the map monitor summary area

## Related Operational Context

* ctx_training_video_robot_count_summary_metrics_v1

## Procedure Steps

### Step 1 — Locate the active robot count

**Responsible role:** operator

**Instruction:**
Open or view the map monitor summary area and locate the active robot count indicator.

**Expected result:**
The active robot count field is visible in the summary area.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*The map monitor summary area where the active robot count is shown.*


**Stop or Escalate If:**

* The active robot count is not visible.
* The displayed summary area does not match the referenced map monitor view.

---

### Step 2 — Read the active robot count

**Responsible role:** operator

**Instruction:**
Read the displayed active robot count and interpret it as the number of robots actively running in the system.

**Expected result:**
You know the current number of robots actively running.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*The active robot count value in the map monitor summary area.*


**Stop or Escalate If:**

* The displayed count appears inconsistent with the visible system state and no explanation is available in the source.

---

### Step 3 — Locate the charging robot count

**Responsible role:** operator

**Instruction:**
In the same map monitor summary area, locate the charging robot count indicator.

**Expected result:**
The charging robot count field is visible in the summary area.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*The map monitor summary area where the charging robot count is shown.*


**Stop or Escalate If:**

* The charging robot count is not visible.
* The displayed summary area does not match the referenced map monitor view.

---

### Step 4 — Read the charging robot count

**Responsible role:** operator

**Instruction:**
Read the displayed charging robot count and interpret it as the number of robots actively charging at that moment.

**Expected result:**
You know the current number of robots actively charging.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*The charging robot count value in the map monitor summary area.*


**Stop or Escalate If:**

* The displayed count appears inconsistent with the visible system state and no explanation is available in the source.

---

### Step 5 — Record the displayed counts

**Responsible role:** operator

**Instruction:**
Record the displayed active robot count and charging robot count.

**Expected result:**
The current active and charging robot counts are documented.

**Screens / Images:**

![artifact_training_video_training_video_day1_0027_so_let_s_see_number_the_primary_01_04_37_000](assets/f39715fd83a18208.jpg)

*The active and charging robot count values to be recorded.*


**Stop or Escalate If:**

* One or both displayed counts appear inconsistent with the visible system state and the source provides no further explanation.

---

## Success Criteria

* The active robot count is identified from the map monitor summary area.
* The charging robot count is identified from the map monitor summary area.
* The displayed active and charging counts are recorded.

## Failure Conditions

* The active robot count cannot be located or read.
* The charging robot count cannot be located or read.
* The displayed counts appear inconsistent with the visible system state and the source provides no explanation.

## Escalation Guidance

* Escalate if the displayed counts appear inconsistent with the visible system state and the source provides no further explanation.
* Do not infer performance or fault conditions from the counts alone unless supported elsewhere.

## Missing Details / Known Gaps

* The source does not provide a precise UI navigation path to the map monitor summary area.
* The source does not define a required recording destination or format for the counts.
* The source does not provide thresholds or interpretation rules beyond identifying active and charging counts.

## Source Lineage

- Candidate IDs: candidate_training_video_use_robot_summary_counts_to_check_active_and_charging_robots
- Source ID: `training_video_day1`
- Source Type: `training_video`
