# Distinguish station labels from tote/container cells on the Container Selection screen (associated IDs)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_distinguish_station_labels_from_tote_cells_v1` |
| Title | Distinguish station labels from tote/container cells on the Container Selection screen (associated IDs) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `device_roster_state` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen’s visual indicators to determine whether a selected element represents a tote/container cell (blue/dark-blue occupancy indicators) or a station label (no blue/dark-blue tote indicators) that has associated IDs.

## When To Use

When a support user needs to interpret what the Container Selection screen is showing for a given location—specifically, whether the element is a tote/container cell (with blue/dark-blue indicators) or a station label (no blue/dark-blue indicators) with associated IDs.

## Access Or Tools Needed

* Container Selection HMI screen access
* Visual access to the presence/absence of blue/dark-blue indicators and the station label area

## Related Operational Context

* ctx_training_video_station_labels_and_ids_v1
* ctx_training_video_container_color_status_v1

## Procedure Steps

### Step 1 — Open the Container Selection screen and observe the container area elements

**Responsible role:** L1_support

**Instruction:**
Open the Container Selection screen and look at the elements/cells/labels under the container area.

**Expected result:**
You can visually distinguish the element you are about to interpret (the one with either blue/dark-blue tote indicators or without them).

**Stop or Escalate If:**

* If the indicator state is unclear or contradicts the expected behavior described in the source, stop and escalate for clarification.

---

### Step 2 — Determine whether the element has blue/dark-blue tote indicators

**Responsible role:** L1_support

**Instruction:**
Check the selected element for the blue/dark-blue tote indicators.

**Expected result:**
You classify the element correctly: blue/dark-blue indicators indicate a tote/container cell; absence of those indicators indicates a station label.

**Stop or Escalate If:**

* If the indicator state is unclear or contradicts the expected behavior described in the source, stop and escalate for clarification.

---

### Step 3 — If no blue/dark-blue indicators are present, treat the element as a station label and identify its associated IDs

**Responsible role:** L1_support

**Instruction:**
If the element does not have the blue/dark-blue indicators, treat it as a station label (special label) and note that it has associated IDs.

**Expected result:**
You can report that the element is a station label and that it has associated IDs (as opposed to a tote/container cell).

**Stop or Escalate If:**

* If the indicator state is unclear or contradicts the expected behavior described in the source, stop and escalate for clarification.

---

### Step 4 — Use the distinction when reporting what the screen is showing for a given location

**Responsible role:** L1_support

**Instruction:**
When reporting what the Container Selection screen shows for a given location, include whether the element is a station label (no blue/dark-blue tote indicators; associated IDs) or a tote/container cell (blue/dark-blue tote indicators).

**Expected result:**
Your report matches the element’s indicator state: station vs tote/container cell is stated consistently with the source’s color/indicator rules.

**Stop or Escalate If:**

* If the indicator state is unclear or contradicts the expected behavior described in the source, stop and escalate for clarification.

---

## Success Criteria

* For the element you interpret on the Container Selection screen, you correctly classify it as either a station label (no blue/dark-blue tote indicators; associated IDs) or a tote/container cell (blue/dark-blue tote indicators).

## Failure Conditions

* Indicator state is misread, causing station labels to be treated as tote/container cells (or the reverse).
* Indicator state is unclear; classification cannot be made confidently.

## Escalation Guidance

* If the screen element’s indicator state is unclear or contradicts the source’s described behavior, stop and escalate for clarification.

## Missing Details / Known Gaps

* The packet does not provide explicit UI control names for where station associated IDs are displayed on the Container Selection screen; it only states that stations have associated IDs.

## Source Lineage

- Candidate IDs: candidate_training_video_container_selection_station_labels_distinct_from_tote_cells
- Source ID: `training_video_day1`
- Source Type: `training_video`
