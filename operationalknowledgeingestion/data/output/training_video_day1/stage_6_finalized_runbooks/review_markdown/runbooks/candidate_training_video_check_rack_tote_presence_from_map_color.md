# Check Rack Tote Presence From RMS Map Color

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_rack_tote_presence_from_rms_map_color_v1` |
| Title | Check Rack Tote Presence From RMS Map Color |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the RMS/container selection map view to determine whether a rack location currently has a tote or is empty by interpreting the rack color. The training source states that a dark blue or violet rack indicates a tote is present, while a light blue rack indicates the rack is empty.

## When To Use

Use this reference procedure when you need to determine tote presence at a rack location from the RMS/map container selection view, or when comparing displayed rack state to expected physical tote presence.

## Do Not Use For

* Do not use this runbook as a corrective procedure for tote addition problems or other recovery actions; the source indicates those later steps are covered elsewhere.
* Do not infer corrective actions from rack color alone.

## Safety And Operational Notes

* This runbook is limited to visual interpretation of rack state in the RMS/container selection view.
* If displayed rack color does not match expected physical tote presence, stop using this reference as the sole basis for action and escalate or continue investigation.

## Access Or Tools Needed

* Access to the RMS/map view
* Container selection view showing rack locations

## Related Operational Context

* ctx_training_video_rack_location_map_reference_v1
* ctx_training_video_rack_color_tote_presence_v1

## Procedure Steps

### Step 1 — Open the RMS map and container selection view

**Responsible role:** operator

**Instruction:**
Open the RMS map view and use the container selection area to view rack locations.

**Expected result:**
The rack locations are visible in the RMS/container selection view.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Screen area showing rack locations and the container selection control.*


**Stop or Escalate If:**

* The RMS/container selection view cannot be accessed.
* Rack locations are not visible in the map view.

---

### Step 2 — Locate the rack position on the map

**Responsible role:** operator

**Instruction:**
Locate the rack position you want to check on the map.

**Expected result:**
The target rack location is identified on the RMS map.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Rack locations in the map view that can be clicked or inspected.*


**Stop or Escalate If:**

* The intended rack location cannot be identified on the map.

---

### Step 3 — Observe the rack color

**Responsible role:** operator

**Instruction:**
Observe the rack color and distinguish between the darker blue or violet tone and the lighter blue tone.

**Expected result:**
The rack color is identified as either dark blue/violet or light blue.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Example of the two rack colors in the map view.*


**Stop or Escalate If:**

* The rack color cannot be reliably distinguished.

---

### Step 4 — Interpret dark blue or violet as tote present

**Responsible role:** operator

**Instruction:**
Interpret a dark blue or violet rack as a rack with a tote present.

**Expected result:**
A dark blue or violet rack is understood to indicate tote presence.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Dark blue or violet rack example indicating tote present.*


**Stop or Escalate If:**

* The dark blue or violet rack state does not match expected physical tote presence.

---

### Step 5 — Interpret light blue as empty rack

**Responsible role:** operator

**Instruction:**
Interpret a light blue rack as an empty rack with no tote present.

**Expected result:**
A light blue rack is understood to indicate no tote is present.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Light blue rack example indicating empty rack.*


**Stop or Escalate If:**

* The light blue rack state does not match expected physical tote presence.

---

### Step 6 — Compare displayed state to physical expectation if needed

**Responsible role:** operator

**Instruction:**
If needed, compare the displayed rack state to what is physically expected at that location, such as whether a tote should be present.

**Expected result:**
The operator confirms whether the displayed rack state matches expected physical tote presence.

**Screens / Images:**

![artifact_training_video_training_video_day1_0037_what_are_these_these_are_rack_primary_01_29_18_500](assets/a335d2897ab8abf1.jpg)

*Rack state display used to compare map indication against expected tote presence.*


**Stop or Escalate If:**

* The displayed rack color does not match the expected physical tote presence.
* Further corrective action is needed, because this reference does not define recovery steps.

---

## Success Criteria

* The user can determine from the map whether a rack location is shown as occupied by a tote or empty.
* The user correctly interprets dark blue or violet as tote present.
* The user correctly interprets light blue as empty.

## Failure Conditions

* The RMS/container selection map view cannot be accessed.
* The target rack location cannot be identified.
* The rack color cannot be clearly distinguished.
* Displayed rack color does not match expected physical tote presence.
* A corrective or recovery action is needed beyond simple state interpretation.

## Escalation Guidance

* Escalate or continue investigation if the displayed rack color does not match the expected physical tote presence.
* Do not infer corrective actions from this runbook alone; the source says later steps for tote addition problems are covered elsewhere.

## Missing Details / Known Gaps

* The source does not provide a time estimate for this procedure.
* The source does not specify production stop requirements.
* The source does not specify LOTO requirements.
* The source does not define corrective actions when displayed rack state does not match physical expectation.
* The packet includes additional related artifacts showing similar container selection content, but this candidate directly references only one artifact.

## Source Lineage

- Candidate IDs: candidate_training_video_check_rack_tote_presence_from_map_color
- Source ID: `training_video_day1`
- Source Type: `training_video`
