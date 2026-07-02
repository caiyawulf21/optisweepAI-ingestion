# Identify Sorter Queue, Exit, and Shutdown Locations on the Sorter Layout

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_sorter_queue_exit_and_shutdown_locations_on_the_sorter_layout_v1` |
| Title | Identify Sorter Queue, Exit, and Shutdown Locations on the Sorter Layout |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented sorter layout training material to identify the entrance queue, exchange staging queue locations, sorter queue locations, exit queue, and shutdown queue locations. This reference also captures the source-described distinction between shutdown positions for AGVs without totes and AGVs with totes, including the noted off-the-end path for an AGV entering during shutdown with a tote.

## When To Use

Use when reviewing the sorter layout training material or equivalent layout view to understand where AGVs and totes are expected to enter, stage for exchange, pick up totes into the aisle, exit after exchange, and position during shutdown.

## Do Not Use For

* Not for issuing AGV movement commands or changing system state.
* Not for inferring exact physical positions beyond what is stated in the source and visible in the referenced layout artifact.
* Not for site-specific validation when observed floor labeling or layout differs from the documented training material.

## Safety And Operational Notes

* This is a reference procedure derived from training material and does not provide control actions or system commands.
* Escalate if the observed layout or site labeling does not match the documented queue and shutdown area descriptions.

## Access Or Tools Needed

* Access to the sorter layout training material or equivalent layout view
* Visual access to the referenced layout artifact if available

## Related Operational Context

* ctx_training_video_sorter_queue_layout_v1
* ctx_training_video_shutdown_queue_locations_v1

## Procedure Steps

### Step 1 — Open the sorter layout view

**Responsible role:** operator

**Instruction:**
Locate the sorter layout view or training slide that shows the queue areas for the sorter layout.

**Expected result:**
The sorter layout image is available for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Layout image showing entrance queue, queue locations, sorter queue locations, exit queue, and shutdown queue areas.*


**Stop or Escalate If:**

* The referenced layout artifact is not available.
* The visible layout does not support identification of the documented areas.

---

### Step 2 — Identify the entrance queue

**Responsible role:** operator

**Instruction:**
Identify the entrance queue on the layout and verify that it is the first queue area described for anything entering the sorter area.

**Expected result:**
The entrance queue is identified as the first queue area for entry into the sorter area.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*The entrance queue location on the sorter layout.*


**Stop or Escalate If:**

* The observed layout or labeling does not match the documented entrance queue description.

---

### Step 3 — Identify exchange staging queue locations

**Responsible role:** operator

**Instruction:**
Identify the queue locations where AGVs stage behind for an exchange.

**Expected result:**
The exchange staging queue locations are identified on the layout.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Queue locations described as AGVs staging behind for an exchange.*


**Stop or Escalate If:**

* The layout does not clearly show the queue locations used for exchange staging.

---

### Step 4 — Identify sorter queue locations for tote pickup

**Responsible role:** operator

**Instruction:**
Identify the sorter queue locations where the tote is picked up and moved into the aisle.

**Expected result:**
The sorter queue locations for tote pickup are identified on the layout.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Sorter queue locations described as the points where the tote is picked up and moved into the aisle.*


**Stop or Escalate If:**

* The layout does not clearly distinguish sorter queue locations from other queue areas.

---

### Step 5 — Identify the exit queue

**Responsible role:** operator

**Instruction:**
Identify the exit queue and verify that after an exchange the AGV goes to the exit queue before going anywhere else.

**Expected result:**
The exit queue is identified as the next destination after an exchange.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*The exit queue location on the sorter layout.*


**Stop or Escalate If:**

* The observed layout or labeling does not match the documented exit queue description.

---

### Step 6 — Identify shutdown queue locations by tote state

**Responsible role:** operator

**Instruction:**
Identify the shutdown queue locations and compare which positions are described for AGVs without totes versus the location described for AGVs with totes.

**Expected result:**
Shutdown queue locations are identified, including the distinction between AGVs without totes and AGVs with totes.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Shutdown queue locations and any visible distinction between AGVs without totes and AGVs with totes.*


**Stop or Escalate If:**

* The shutdown locations shown on the layout do not match the documented tote-dependent shutdown description.

---

### Step 7 — Check whether shutdown locations are under the rack

**Responsible role:** operator

**Instruction:**
Check whether the shutdown locations are described as under the rack and note that distinction if visible on the layout.

**Expected result:**
The reviewer notes whether the shutdown locations are shown or described as under the rack.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Layout or diagram showing shutdown locations under the rack if visible.*


**Stop or Escalate If:**

* The source description says shutdown locations are under the rack but the available layout view is too unclear to confirm.

---

### Step 8 — Note shutdown entry behavior for AGVs with totes

**Responsible role:** operator

**Instruction:**
If reviewing shutdown entry behavior, note that an AGV entering during shutdown with a tote is described as going off the end and then to shutdown.

**Expected result:**
The shutdown entry behavior for an AGV with a tote is documented as part of the layout interpretation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0019_for_our_sorter_we_have_our_primary_00_39_18_000](assets/d4c5dd8d9edcbcd4.jpg)

*Any visible path or labeled area supporting the off-the-end routing note during shutdown entry with a tote.*


**Stop or Escalate If:**

* The observed layout or site behavior appears inconsistent with the documented off-the-end shutdown entry description.

---

## Success Criteria

* The entrance queue is identified as the first queue area for entry into the sorter area.
* The exchange staging queue locations are identified.
* The sorter queue locations for tote pickup into the aisle are identified.
* The exit queue is identified as the destination after exchange.
* Shutdown queue locations are identified, including the distinction between AGVs without totes and AGVs with totes.
* The under-rack shutdown note and off-the-end shutdown entry behavior are captured when visible or described.

## Failure Conditions

* The referenced layout artifact is unavailable or unclear.
* The observed layout or site labeling does not match the documented queue and shutdown descriptions.
* Exact physical positions would need to be inferred beyond what is stated in the source.

## Escalation Guidance

* Escalate if the observed layout or site labeling does not match the documented queue and shutdown area descriptions.
* Escalate if the available artifact does not clearly support identification of the required queue or shutdown locations.
* Do not infer exact physical positions beyond what is stated in the source and visible in the referenced layout artifact.

## Missing Details / Known Gaps

* The source provides a layout explanation rather than a full operating procedure.
* The source does not provide commands, control actions, or HMI navigation steps for this reference task.
* The source does not provide a time estimate.
* The source does not define exact physical coordinates or labels for each queue position beyond the layout explanation.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_sorter_queue_and_shutdown_locations
- Source ID: `training_video_day1`
- Source Type: `training_video`
