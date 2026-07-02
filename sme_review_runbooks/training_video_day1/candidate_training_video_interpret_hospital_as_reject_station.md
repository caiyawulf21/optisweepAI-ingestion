# Use the Hospital as the Reject Station for Unsorted Totes and Packages

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_hospital_as_reject_station_for_unsorted_totes_and_packages_v1` |
| Title | Use the Hospital as the Reject Station for Unsorted Totes and Packages |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

This source-backed reference explains that the hospital is used as a reject station for operator handling when a tote or package did not get sorted normally. The operator addresses those totes at the hospital so the packages can get back onto the system, but the training source does not provide detailed recovery or data-entry steps.

## When To Use

Use this reference when a tote or package is identified as having gone to the hospital instead of completing normal sort flow, and the operator needs to understand the documented purpose of the hospital handling point.

## Do Not Use For

* Do not use this runbook as a detailed recovery procedure for specific tipper faults or other equipment faults, because the source does not provide those steps.
* Do not use this runbook to invent detailed package reprocessing, system-entry, or HMI workflows not stated in the source.
* Do not use this runbook as a normal sort-destination procedure; the source describes the hospital as a reject station rather than a normal destination.

## Safety And Operational Notes

* This source is a training explanation and does not provide detailed physical handling or hazard controls.
* Do not perform unsupported recovery actions beyond the source-backed statement that the operator addresses those totes at the hospital.

## Access Or Tools Needed

* Access to the hospital or reject station area
* Physical access to the affected tote or package
* Source-backed understanding of hospital function from training

## Related Operational Context

* ctx_training_video_hospital_reject_station_v1

## Procedure Steps

### Step 1 — Identify that the tote or package has gone to the hospital

**Responsible role:** operator

**Instruction:**
Identify that the tote or package has gone to the hospital instead of being sorted normally.

**Expected result:**
The operator recognizes that the affected tote or package is in hospital handling flow.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Training frame and aligned transcript discussing hospital/reject handling for totes/packages that did not sort normally.*


**Stop or Escalate If:**

* Escalate if it is not clear whether the tote or package should be handled through the hospital.
* Stop if determining the item status would require unsupported assumptions beyond the source.

---

### Step 2 — Interpret the hospital as a reject station

**Responsible role:** operator

**Instruction:**
Recognize from the source that the hospital is a reject station for operator handling, not a normal sort destination.

**Expected result:**
The operator understands the intended function of the hospital location.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Transcript-aligned frame where the instructor explains that the hospital is a reject station for operator handling.*


**Stop or Escalate If:**

* Escalate if local handling expectations conflict with the source-backed definition and no source-supported clarification is available.

---

### Step 3 — Handle the tote at the hospital location

**Responsible role:** operator

**Instruction:**
Take the tote to the hospital handling point or address it at the hospital location as described in the source.

**Expected result:**
The tote is positioned or handled at the hospital location for operator attention.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Training frame associated with the hospital/reject-station explanation.*

![artifact_training_video_training_video_day1_0020_we_ve_got_your_entrance_queue_primary_00_43_45_000](assets/7b19755a4f0543af.jpg)

*Modularization slide showing hospital flow, including hospital entrance queue, drop-off, pickup, and exit queue concepts.*


**Stop or Escalate If:**

* Escalate if the tote or package cannot be addressed at the hospital using the documented operator handling concept.
* Stop if additional movement or recovery steps would require unsupported instructions not present in the source.

---

### Step 4 — Address the tote so packages can get back onto the system

**Responsible role:** operator

**Instruction:**
Address the tote there so that the packages can get back onto the system, using only the source-backed understanding that the operator handles those totes at the hospital.

**Expected result:**
The tote has been addressed at the hospital in line with the source-described purpose.

**Screens / Images:**

![artifact_training_video_training_video_day1_0021_yes_so_there_s_something_wrong_primary_00_47_36_500](assets/f18746c1af8c4b3c.jpg)

*Transcript-aligned frame stating that the operator addresses those totes so the packages get back.*


**Stop or Escalate If:**

* Escalate if the package cannot be returned to system flow through hospital handling.
* Do not invent detailed recovery actions beyond the source statement that the operator addresses those totes at the hospital.

---

### Step 5 — Record or communicate handling only if local practice requires it

**Responsible role:** operator

**Instruction:**
Record or communicate that the package was handled through the hospital if local practice requires it; the source does not provide detailed entry steps.

**Expected result:**
Any required local communication or recordkeeping is completed without adding unsupported process detail.

**Stop or Escalate If:**

* Escalate if required documentation or communication steps are needed but are not defined in the source.

---

## Success Criteria

* The operator correctly interprets the hospital as the reject station for unsorted totes or packages.
* The affected tote is handled at the hospital location.
* The tote is addressed there so the package can get back onto the system, consistent with the source.

## Failure Conditions

* The tote or package cannot be addressed at the hospital using the documented operator handling concept.
* The operator needs detailed recovery, HMI, or logging steps that are not provided by the source.
* The hospital is misinterpreted as a normal sort destination.

## Escalation Guidance

* Escalate if the tote or package cannot be addressed at the hospital using the documented operator handling concept.
* Escalate if additional recovery detail is required beyond the source statement that the operator addresses those totes at the hospital.
* Escalate if required documentation or communication steps are needed but are not defined in the source.

## Missing Details / Known Gaps

* The source does not provide detailed physical handling steps for how the operator addresses the tote at the hospital.
* The source does not provide HMI, RMS, or command-based actions for hospital handling in this context.
* The source does not define exact criteria for identifying every hospital case beyond the training explanation.
* The source does not provide detailed recordkeeping or communication steps.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_hospital_as_reject_station
- Source ID: `training_video_day1`
- Source Type: `training_video`
