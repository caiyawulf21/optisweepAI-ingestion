# Display Charger IDs On the Map

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_display_charger_ids_on_the_map_v1` |
| Title | Display Charger IDs On the Map |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Map Monitor Quick Select control to display charger IDs on the map so chargers can be identified by their unique IDs.

## When To Use

Use when a support user needs to view charger identifiers on the Map Monitor and confirm which charger is which by its displayed unique ID.

## Do Not Use For

* Do not use this procedure to infer charger status or charger behavior from the ID display alone.

## Safety And Operational Notes

* This source supports displaying charger IDs only.
* Do not infer charger status or charger behavior from the ID display alone.

## Access Or Tools Needed

* Access to the Map Monitor screen
* Map Monitor Quick Select controls

## Related Operational Context

* ctx_training_video_map_monitor_quick_select_overview_v1
* ctx_training_video_charger_ids_reference_v1

## Procedure Steps

### Step 1 — Open Map Monitor and locate Quick Select

**Responsible role:** L1_support

**Instruction:**
Open the Map Monitor screen and locate the Quick Select area on the left-side panel.

**Expected result:**
The Map Monitor screen is visible and the Quick Select controls can be seen on the left-side panel.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The Map Monitor Quick Select panel on the left side, including the charger ID display icon.*


**Stop or Escalate If:**

* Escalate if the Map Monitor screen cannot be accessed.
* Escalate if the Quick Select controls are not visible.

---

### Step 2 — Select View Charger IDs

**Responsible role:** L1_support

**Instruction:**
Click the "View Charger Ids" icon.

**Expected result:**
The map updates to display charger IDs.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*The Quick Select icon used to display charger IDs.*


**Stop or Escalate If:**

* Escalate if charger IDs do not display after selecting the charger ID icon.

---

### Step 3 — Observe displayed charger IDs

**Responsible role:** L1_support

**Instruction:**
Observe the map and identify the displayed charger IDs.

**Expected result:**
Charger IDs are visible on the map and can be read by the user.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*Displayed charger ID labels associated with chargers on the map.*


**Stop or Escalate If:**

* Escalate if charger IDs do not display after selecting the charger ID icon.

---

### Step 4 — Verify charger IDs are unique

**Responsible role:** L1_support

**Instruction:**
Verify that each charger shown on the map has its own unique ID.

**Expected result:**
Each charger shown on the map is identifiable by a unique displayed ID.

**Screens / Images:**

![artifact_training_video_training_video_day1_0028_so_this_one_over_here_is_primary_01_12_24_500](assets/8de8739ca708d504.jpg)

*Charger labels on the map used to distinguish one charger from another.*


**Stop or Escalate If:**

* Escalate if charger IDs do not display after selecting the charger ID icon.
* Stop if attempting to use the ID display alone to determine charger status or behavior.

---

## Success Criteria

* The map displays charger IDs after the View Charger Ids icon is selected.
* Chargers shown on the map can be identified by their displayed unique IDs.

## Failure Conditions

* The Map Monitor screen cannot be accessed.
* The Quick Select area cannot be located.
* Charger IDs do not display after selecting the charger ID icon.
* The displayed ID view is used to infer charger status or charger behavior.

## Escalation Guidance

* Escalate if charger IDs do not display after selecting the charger ID icon.
* Do not use this procedure alone to determine charger status or charger behavior.

## Missing Details / Known Gaps

* The source does not provide a time estimate for this procedure.
* The source does not specify whether production stop is required.
* The source does not specify whether LOTO is required.
* The source does not provide additional troubleshooting steps if charger IDs fail to display.
* The source does not define role boundaries beyond support-oriented usage.

## Source Lineage

- Candidate IDs: candidate_training_video_display_charger_ids_on_map
- Source ID: `training_video_day1`
- Source Type: `training_video`
