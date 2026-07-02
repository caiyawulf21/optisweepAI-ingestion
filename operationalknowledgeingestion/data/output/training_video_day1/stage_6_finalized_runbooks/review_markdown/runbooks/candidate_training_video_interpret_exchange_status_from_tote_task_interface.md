# Interpret Exchange Status Information From the Tote Task Interface

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_exchange_status_information_from_the_tote_task_interface_v1` |
| Title | Interpret Exchange Status Information From the Tote Task Interface |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Tote Task interface to identify exchange-related status information shown for a tote task, including exchange type, priority indication, original destination, readiness for exchange, and any displayed indication that an AGV is behind it ready to go.

## When To Use

Use this runbook when reviewing the Tote Task interface to understand the exchange-related values displayed for a tote's current task.

## Do Not Use For

* Do not use this runbook to infer exchange logic or make operational decisions beyond the values explicitly shown on the interface.
* Do not use this runbook if the exchange-related fields are not visible and cannot be confirmed from the Tote Task interface.

## Safety And Operational Notes

* This source describes screen interpretation only.
* Do not infer exchange logic or operational decisions beyond the values explicitly shown in the source.

## Access Or Tools Needed

* Access to the Tote Task interface
* Visibility of exchange-related fields on the Tote Task screen

## Related Operational Context

* ctx_training_video_tote_task_interface_overview_v1
* ctx_training_video_exchange_type_status_reference_v1

## Procedure Steps

### Step 1 — Open or view the Tote Task interface

**Responsible role:** L1_support

**Instruction:**
Open or view the Tote Task interface for the tote being reviewed.

**Expected result:**
The Tote Task interface is visible for the tote under review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Tote Tasks Aveva API page showing current task details and exchange-related information.*


**Stop or Escalate If:**

* Escalate if the exchange-related fields are not visible.
* Escalate if the Tote Task interface for the tote being reviewed cannot be confirmed.

---

### Step 2 — Locate exchange-related information

**Responsible role:** L1_support

**Instruction:**
Locate the exchange-related information shown for the current task, including what kind of exchange type it is doing.

**Expected result:**
The exchange-related fields for the current task are identified on screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Current task details area where exchange type is described.*


**Stop or Escalate If:**

* Escalate if the exchange-related fields are not visible.
* Escalate if the meaning of the displayed exchange information is unclear from the interface.

---

### Step 3 — Check whether the exchange is priority

**Responsible role:** L1_support

**Instruction:**
Check whether the exchange is indicated as a priority.

**Expected result:**
The priority indication for the exchange is identified exactly as displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Exchange-related details showing whether the exchange is a priority.*


**Stop or Escalate If:**

* Escalate if the priority field is not visible.
* Escalate if the meaning of the priority indication is unclear from the interface.

---

### Step 4 — Review the Original Destination value

**Responsible role:** L1_support

**Instruction:**
Review the Original Destination value associated with the tote.

**Expected result:**
The Original Destination value is identified from the interface.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Original Destination field in the Tote Task details.*


**Stop or Escalate If:**

* Escalate if the Original Destination field is not visible.
* Escalate if the displayed value cannot be read clearly.

---

### Step 5 — Check whether the tote is ready for exchange

**Responsible role:** L1_support

**Instruction:**
Check whether the tote is shown as ready for exchange.

**Expected result:**
The tote's readiness-for-exchange status is identified exactly as displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Exchange-related details showing whether the tote is ready for exchange.*


**Stop or Escalate If:**

* Escalate if the ready-for-exchange field is not visible.
* Escalate if the meaning of the readiness indication is unclear from the interface.

---

### Step 6 — Observe any AGV-behind-ready indication

**Responsible role:** L1_support

**Instruction:**
Observe whether the interface indicates an AGV behind it ready to go, if that information is displayed.

**Expected result:**
Any displayed indication that an AGV is behind it ready to go is noted exactly as shown.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Any transcript-supported indication that an AGV behind the tote is ready to go.*


**Stop or Escalate If:**

* Escalate if this information is expected but not visible.
* Escalate if the meaning of the AGV-behind-ready indication is unclear from the interface.

---

### Step 7 — Record the displayed exchange values exactly as shown

**Responsible role:** L1_support

**Instruction:**
Record the displayed exchange type and readiness-related values exactly as shown.

**Expected result:**
The displayed exchange type, priority indication, original destination, readiness-for-exchange status, and any AGV-behind-ready indication are documented exactly as displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0075_current_task_and_you_know_you_primary_02_26_49_500](assets/e9be849441aecf97.jpg)

*Exchange-related values to capture exactly as displayed on the Tote Task interface.*


**Stop or Escalate If:**

* Escalate if the exchange-related fields are not visible.
* Escalate if their meaning is unclear from the interface.
* Stop and do not infer exchange logic or operational decisions beyond the values explicitly shown in the source.

---

## Success Criteria

* The user identifies the displayed exchange type from the Tote Task interface.
* The user identifies whether the exchange is shown as priority.
* The user identifies the Original Destination value.
* The user identifies whether the tote is shown as ready for exchange.
* If displayed, the user notes whether the interface indicates an AGV behind it ready to go.
* All values are recorded exactly as shown without inference.

## Failure Conditions

* Exchange-related fields are not visible.
* The meaning of displayed fields is unclear from the interface.
* Original Destination or readiness-related values cannot be read.
* The AGV-behind-ready indication is ambiguous or unlabeled.
* The reviewer infers logic or decisions beyond what is explicitly shown.

## Escalation Guidance

* Escalate if the exchange-related fields are not visible or their meaning is unclear from the interface.
* Escalate if expected exchange status information cannot be confirmed directly from the Tote Task screen.
* Do not infer exchange logic or operational decisions beyond the values explicitly shown in the source.

## Missing Details / Known Gaps

* The source does not provide exact field labels for all exchange-related values.
* The source does not provide a documented navigation path to open the Tote Task interface.
* The source does not provide a time estimate for completing this reference check.
* The exact field label for the AGV-behind-ready indication is not provided in the OCR text.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_exchange_status_from_tote_task_interface
- Source ID: `training_video_day1`
- Source Type: `training_video`
