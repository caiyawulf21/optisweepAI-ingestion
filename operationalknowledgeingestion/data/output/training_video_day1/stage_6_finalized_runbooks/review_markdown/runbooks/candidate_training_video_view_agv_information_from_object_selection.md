# View AGV Information By Selecting The AGV Object

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_view_agv_information_by_selecting_the_agv_object_v1` |
| Title | View AGV Information By Selecting The AGV Object |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the interface object selection behavior under AGV to display AGV-specific information for a selected AGV. The source supports that selecting the AGV object causes AGV information to be shown, but does not define the exact fields displayed.

## When To Use

Use when you need to view AGV-specific information in the interface by selecting an AGV object.

## Do Not Use For

* Do not use this runbook to interpret undocumented AGV information fields or values.
* Do not use this runbook for AGV control, movement, recovery, or Go-to actions; the source only supports viewing AGV information after selection.

## Safety And Operational Notes

* This source describes a view/selection interaction only.
* Do not infer meanings for AGV information fields that are not identified in the source.

## Access Or Tools Needed

* Access to the object selection interface
* Ability to select an AGV object

## Related Operational Context

* ctx_training_video_agv_object_selection_v1

## Procedure Steps

### Step 1 — Open the object selection area

**Responsible role:** operator

**Instruction:**
Go to the object selection area in the interface.

**Expected result:**
The object selection area is visible and ready for selection.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*The training frame associated with the AGV object selection discussion.*


**Stop or Escalate If:**

* Escalate if the object selection area cannot be accessed.

---

### Step 2 — Select the AGV object

**Responsible role:** operator

**Instruction:**
Under AGV, select the AGV object you are interested in.

**Expected result:**
The AGV object is selected in the interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*Any AGV object selection area or AGV-related selection context shown in the training frame.*


**Stop or Escalate If:**

* Escalate if selecting the AGV object does not display AGV information.

---

### Step 3 — Observe the displayed AGV information

**Responsible role:** operator

**Instruction:**
Observe the AGV information displayed after the AGV is selected.

**Expected result:**
AGV information is displayed for the selected AGV.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*The AGV-related information area that should populate after AGV selection.*


**Stop or Escalate If:**

* Escalate if no AGV information is displayed after selection.

---

### Step 4 — Use the displayed AGV information

**Responsible role:** operator

**Instruction:**
Use the displayed AGV information for the item you are interested in, as referenced by the transcript.

**Expected result:**
The operator has the AGV information needed for the selected item.

**Screens / Images:**

![artifact_training_video_training_video_day1_0041_yeah_understood_yeah_so_you_have_primary_01_35_15_000](assets/7f8052d822849714.jpg)

*The AGV information shown after selection; use only what is visibly presented.*


**Stop or Escalate If:**

* Escalate if the information needed is not displayed.
* Stop if interpretation would require undocumented field meanings or values.

---

## Success Criteria

* The AGV object can be selected under AGV in the interface.
* The interface displays AGV information for the selected AGV object.

## Failure Conditions

* The object selection area cannot be accessed.
* Selecting the AGV object does not display AGV information.
* The source does not provide enough detail to interpret specific AGV information fields.

## Escalation Guidance

* Escalate if selecting the AGV object does not display AGV information.
* Escalate if the required AGV information is not visible after selection.
* Do not infer undocumented values, labels, or meanings for AGV information fields.

## Missing Details / Known Gaps

* The source does not identify the exact AGV information fields, labels, or values shown after selection.
* The source does not specify the exact screen name or navigation path to the object selection area.
* The source does not define any timing expectation for the AGV information to appear.
* The source does not specify role boundaries beyond general operator use.

## Source Lineage

- Candidate IDs: candidate_training_video_view_agv_information_from_object_selection
- Source ID: `training_video_day1`
- Source Type: `training_video`
