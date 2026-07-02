# Interpret Container Selection Colors And Locate A Tote Or Rack Entry

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_container_selection_colors_and_locate_a_tote_or_rack_entry_v1` |
| Title | Interpret Container Selection Colors And Locate A Tote Or Rack Entry |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Container Selection screen to determine whether a rack location contains an AG tote or is empty, and locate a tote by entering a location or tote/container number and selecting the returned rack or AGV location.

## When To Use

Use when viewing the Container Selection screen to interpret rack occupancy states or to look up where a tote is located by location or tote/container number.

## Do Not Use For

* Do not use this procedure to infer meanings for colors or icons beyond what the source states.
* Do not use this procedure as authorization to remove AGVs or remove items directly in this interface on an active system.
* Do not use this as a full end-to-end operating workflow; the source supports interpretation and lookup behavior only.

## Safety And Operational Notes

* The related training frame warns that on an active system one of the worst actions is removing an AGV.
* Not all users have credentials for all actions; the artifact notes operators should not have access while supervisors may.
* Direct customers to approved tools such as AVEVA or the portal/hospital workflow rather than removing items directly in this interface when that caution applies.

## Access Or Tools Needed

* Access to the Container Selection screen
* Visual access to rack color states and selection results
* Location number or tote/container number to search

## Related Operational Context

* ctx_training_video_operation_container_selection_tote_lookup_v1
* ctx_training_video_hmi_metric_container_selection_color_states_v1

## Procedure Steps

### Step 1 — Open or view the Container Selection screen

**Responsible role:** operator

**Instruction:**
Open or view the Container Selection screen for totes/containers.

**Expected result:**
The Container Selection screen is visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0045_i_i_would_say_like_the_primary_01_37_38_000](assets/f6cb873cf13e9adf.jpg)

*Container Selection / Totes view.*


**Stop or Escalate If:**

* The Container Selection screen cannot be accessed or does not match the documented screen context.

---

### Step 2 — Interpret rack color state

**Responsible role:** operator

**Instruction:**
Observe the rack color state on the screen and compare it to the documented color meanings: dark blue indicates the presence of an AG tote, and light blue indicates an empty rack.

**Expected result:**
The rack state is interpreted using the documented color meanings.

**Screens / Images:**

![artifact_training_video_training_video_day1_0045_i_i_would_say_like_the_primary_01_37_38_000](assets/f6cb873cf13e9adf.jpg)

*Screen area showing dark blue and light blue rack states.*


**Stop or Escalate If:**

* The screen display does not match the documented color meanings.
* Additional color meanings or icon meanings would need to be inferred beyond what the source states.

---

### Step 3 — Enter a location or tote number for lookup

**Responsible role:** operator

**Instruction:**
If you need to find a tote, type the location or number into the screen's lookup field using the source-described location or tote/container number entry.

**Expected result:**
The entered location or tote/container number is accepted for lookup.

**Screens / Images:**

![artifact_training_video_training_video_day1_0045_i_i_would_say_like_the_primary_01_37_38_000](assets/f6cb873cf13e9adf.jpg)

*Search or entry field on the Container Selection screen.*


**Stop or Escalate If:**

* The screen does not return a rack or AGV location for the entered value.

---

### Step 4 — Select the returned rack or AGV location

**Responsible role:** operator

**Instruction:**
Select the rack or AGV location returned by the screen for the entered location or number.

**Expected result:**
The selected rack or AGV location is displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0045_i_i_would_say_like_the_primary_01_37_38_000](assets/f6cb873cf13e9adf.jpg)

*Returned rack or AGV location associated with the entered value.*


**Stop or Escalate If:**

* No rack or AGV location is returned for the entered value.
* The returned result cannot be selected.

---

### Step 5 — Verify the selected result details

**Responsible role:** operator

**Instruction:**
Verify whether a box icon appears and whether the tote number is shown after selection, as described in the source.

**Expected result:**
The selected result shows the expected box icon and tote number when applicable.

**Screens / Images:**

![artifact_training_video_training_video_day1_0045_i_i_would_say_like_the_primary_01_37_38_000](assets/f6cb873cf13e9adf.jpg)

*Selected rack or AGV result showing a box icon and tote number.*


**Stop or Escalate If:**

* The selected result does not show the expected box icon or tote number.
* The screen behavior does not match the documented selection result.

---

## Success Criteria

* The user can identify whether a rack location is occupied or empty using the documented color meanings.
* The user can enter a location or tote/container number and identify the rack or AGV associated with that value.
* The selected result shows the expected tote-identifying details described by the source when applicable.

## Failure Conditions

* The screen display does not match the documented color meanings.
* The screen does not return a rack or AGV location for the entered value.
* The selected result does not show the expected box icon or tote number.
* The user would need to infer additional meanings for colors or icons beyond what the source states.

## Escalation Guidance

* Escalate if the screen display does not match the documented color meanings or does not return a rack or AGV location for the entered value.
* Stop and seek guidance if the interface behavior differs from the training source.
* Do not perform removal actions in this interface based on this reference; use approved tools/workflows noted in the source context when applicable.

## Missing Details / Known Gaps

* The source does not provide a precise navigation path to open the Container Selection screen.
* The source does not provide a time estimate for completing this reference task.
* The source does not define additional role boundaries beyond operator-level use and cautionary access notes.
* The source does not provide explicit field names for the lookup entry box.
* The source does not provide a full end-to-end operating workflow beyond interpretation and lookup behavior.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_container_selection_tote_presence_and_lookup
- Source ID: `training_video_day1`
- Source Type: `training_video`
