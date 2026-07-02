# Identify Aveva As The HMI Platform Used In UPS Buildings

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_aveva_as_the_hmi_platform_used_in_ups_buildings_v1` |
| Title | Identify Aveva As The HMI Platform Used In UPS Buildings |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the referenced training slide and transcript segment to verify that the source identifies Aveva as the HMI platform used in UPS buildings. This runbook is limited to source-backed platform identification and does not provide HMI operating instructions.

## When To Use

Use when you need to confirm, from this training source only, which HMI platform is named for the described UPS building environment.

## Do Not Use For

* Do not use this runbook to operate Aveva.
* Do not use this runbook to infer specific HMI screens, controls, buttons, workflows, or navigation paths.
* Do not use this runbook when a task requires actual HMI operating steps.

## Safety And Operational Notes

* This source segment supports platform identification only.
* Do not invent HMI screen names, buttons, or workflows because they are not provided in this segment.

## Access Or Tools Needed

* Access to the training video segment or extracted slide
* Transcript for the segment

## Related Operational Context

* ctx_training_video_aveva_hmi_usage_v1
* ctx_training_video_core_elements_architecture_v1

## Procedure Steps

### Step 1 — Open the overview slide and locate the Aveva HMI label

**Responsible role:** operator

**Instruction:**
Open the overview training slide for the cited segment and locate the label for Aveva HMI in the architecture diagram.

**Expected result:**
The overview slide visibly includes an Aveva HMI label among the core system elements.

**Screens / Images:**

![artifact_training_video_training_video_day1_0005_so_we_talked_to_ups_chat_primary_00_05_38_000](assets/5b53abba3e1c6807.jpg)

*The core elements architecture slide showing UPS Chat, tote handling equipment, AGVs, hospital controller, OptiSweep software, sorter, printer, and the Aveva HMI label.*


**Stop or Escalate If:**

* Stop if the referenced slide or artifact is unavailable.
* Escalate if the image is too unclear to confirm the Aveva HMI label from the source artifact.

---

### Step 2 — Confirm the transcript statement about Aveva usage

**Responsible role:** operator

**Instruction:**
Review the transcript or evidence summary for the cited segment and confirm that it states UPS in all their buildings uses Aveva for HMIs.

**Expected result:**
The transcript evidence explicitly states that UPS in all their buildings uses Aveva for HMIs.

**Stop or Escalate If:**

* Stop if the transcript for the cited segment is not available.
* Escalate if the source wording cannot be verified from the provided evidence.

---

### Step 3 — Record Aveva as the named HMI platform

**Responsible role:** operator

**Instruction:**
Record Aveva as the HMI platform named in this source segment.

**Expected result:**
Aveva is documented as the HMI platform identified by this training source segment.

**Screens / Images:**

![artifact_training_video_training_video_day1_0005_so_we_talked_to_ups_chat_primary_00_05_38_000](assets/5b53abba3e1c6807.jpg)

*Use the overview slide as the visual reference supporting the recorded identification of Aveva HMI.*


**Stop or Escalate If:**

* Escalate if another task requires more than platform identification from this segment.

---

### Step 4 — Limit use of the result to platform identification only

**Responsible role:** operator

**Instruction:**
Use this identification only as a source-backed platform reference and do not infer specific HMI screens, controls, or navigation paths from this segment.

**Expected result:**
The result is used only to identify the platform and not as an operating procedure.

**Stop or Escalate If:**

* Escalate if a task requires actual HMI operating steps.
* Stop if someone requests screen names, buttons, workflows, or navigation paths not provided in this segment.

---

## Success Criteria

* The reviewer verifies from the overview slide that Aveva HMI is labeled in the architecture diagram.
* The reviewer verifies from the transcript evidence that UPS in all their buildings uses Aveva for HMIs.
* Aveva is recorded as the HMI platform named in this source segment.
* No unsupported HMI operating details are inferred from this segment.

## Failure Conditions

* The overview slide or transcript evidence cannot be accessed or verified.
* The Aveva HMI label cannot be confirmed from the provided artifact.
* The user attempts to derive operating steps, controls, or navigation from this source segment.

## Escalation Guidance

* Escalate if a task requires actual HMI operating steps, since this source only provides platform identification.
* Escalate if image quality or transcript availability prevents confirmation from the cited source.
* Escalate if additional HMI details are needed beyond the statement that Aveva is the platform used.

## Missing Details / Known Gaps

* This source segment does not provide HMI operating steps.
* This source segment does not provide specific HMI screen names, controls, buttons, or navigation paths.
* The packet does not provide a fuller transcript body in source_sections text for this segment.

## Source Lineage

- Candidate IDs: candidate_training_video_identify_aveva_as_hmi_platform_in_ups_buildings
- Source ID: `training_video_day1`
- Source Type: `training_video`
