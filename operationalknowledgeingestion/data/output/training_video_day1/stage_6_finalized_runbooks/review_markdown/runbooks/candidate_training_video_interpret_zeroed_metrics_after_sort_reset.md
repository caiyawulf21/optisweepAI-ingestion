# Interpret Zeroed Or No-Data Metrics After a Sort Reset

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_zeroed_or_no_data_metrics_after_a_sort_reset_v1` |
| Title | Interpret Zeroed Or No-Data Metrics After a Sort Reset |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use this source-backed interpretation when current metrics or statistics appear blank, no-data, or zeroed after a sort cycle. The source explains that a sort cycle sends a reset metrics bit, resets tipper metrics, and generates a new sort GUID. Because statistics are tied to the sort GUID, the current display may legitimately show no data or zeroed values for the new sort context.

## When To Use

Use when reviewing a current metrics or statistics display after a sort cycle and the values appear blank, no-data, or all zeroed out, and you need to determine whether that state is expected based on sort GUID reset behavior described in this source.

## Do Not Use For

* Do not use this runbook to claim that historical totals should still appear on the current sort display.
* Do not use this runbook to conclude that totals are missing from the database.
* Do not use this runbook to retrieve historical data or run database queries, because this source does not provide those steps.

## Safety And Operational Notes

* This is an interpretive reference procedure only; no physical action, control action, or reset action is provided by this source.
* Do not assume missing current display values mean historical data was lost; the source states historical data is retained in the database.

## Access Or Tools Needed

* Access to the current metrics display
* Source-backed understanding of sort GUID metric reset behavior

## Related Operational Context

* ctx_training_video_sort_guid_metrics_reset_v1
* ctx_training_video_historical_sort_data_reference_v1

## Procedure Steps

### Step 1 — Review the current metrics display

**Responsible role:** L1_support

**Instruction:**
Review the displayed metrics or statistics for the current sort context.

**Expected result:**
The current metrics or statistics display is visible and ready to be assessed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Use the referenced training frame as nearby visual context for the page being discussed while interpreting current metrics behavior.*


**Stop or Escalate If:**

* Escalate if the current metrics display cannot be reviewed well enough to determine what state it is showing.

---

### Step 2 — Identify whether the display is blank or zeroed

**Responsible role:** L1_support

**Instruction:**
Check whether the values appear as no data or all zeroed out.

**Expected result:**
You can state whether the current display appears blank, no-data, or zeroed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0061_this_page_should_show_rms_but_primary_02_13_06_000](assets/1edf4bf1b0b38c00.jpg)

*Look at the page context being discussed while assessing whether the current statistics view is showing no data or zeroed values.*


**Stop or Escalate If:**

* Escalate if the observed metric behavior is neither normal populated data nor the source-described no-data/zeroed state.

---

### Step 3 — Compare the observation to sort reset behavior

**Responsible role:** L1_support

**Instruction:**
Compare that observation to the source explanation that a sort cycle sends a reset metrics bit, resets tipper metrics, and generates a new sort GUID.

**Expected result:**
The observed display state is evaluated against the source-described reset sequence.

**Stop or Escalate If:**

* Escalate if the observed metric behavior does not match the source-described reset behavior.

---

### Step 4 — Interpret the display using sort GUID scoping

**Responsible role:** L1_support

**Instruction:**
Use the source rule that statistics are tied to the sort GUID to interpret why the tables may show no data after the reset.

**Expected result:**
You can explain that the current display is scoped to the new sort GUID and therefore may show no data or zeros immediately after reset.

**Stop or Escalate If:**

* Stop and avoid concluding that historical totals should still be visible on the current sort display.
* Escalate if the display behavior cannot be explained by sort GUID scoping.

---

### Step 5 — Document the interpretation and avoid incorrect conclusions

**Responsible role:** L1_support

**Instruction:**
Record that the displayed zeroed or no-data state is consistent with a new sort GUID rather than assuming historical totals should still be visible on the current sort display.

**Expected result:**
The observed state is documented as consistent with a new sort GUID and not treated as proof of missing historical data.

**Stop or Escalate If:**

* Stop and avoid claiming totals are missing from the database; the source says historical data is retained there.
* Escalate if the observed metric behavior still does not fit the source-described reset behavior.

---

## Success Criteria

* The user can explain that current metrics may appear zeroed or empty because the sort reset created a new sort GUID.
* The user understands that the current display is scoped to the new sort rather than historical totals.
* The user does not incorrectly conclude that historical data is missing from the database.

## Failure Conditions

* Observed metric behavior does not match the source-described reset behavior.
* The display state is interpreted as database data loss without source support.
* The current display cannot be confidently tied to the active sort context.

## Escalation Guidance

* Escalate if the observed metric behavior does not match the source-described reset behavior.
* Escalate if the display cannot be interpreted using the source rule that statistics are tied to the sort GUID.
* Escalate if additional historical retrieval or validation steps are needed, because this source does not provide those procedures.

## Missing Details / Known Gaps

* The source does not provide a specific screen navigation path for opening the metrics display.
* The source does not provide a command, query, or workflow for retrieving historical sort data.
* The source does not define a time window for how long no-data or zeroed values remain visible after reset.
* The source does not specify exact escalation targets or routing.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_zeroed_metrics_after_sort_reset
- Source ID: `training_video_day1`
- Source Type: `training_video`
