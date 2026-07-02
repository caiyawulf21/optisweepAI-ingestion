# Identify Core OptiSweep Environment Components And Their Communication Path

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_core_optisweep_environment_components_and_their_communication_path_v1` |
| Title | Identify Core OptiSweep Environment Components And Their Communication Path |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training overview slide and transcript to identify the core components shown in the OptiSweep environment overview and confirm the communication roles described for UPS Chat and OptiSweep Software.

## When To Use

Use this reference procedure when reviewing the OptiSweep overview architecture from the training source to identify the labeled system components and restate the communication relationship described in the source between UPS Chat, OptiSweep Software, and connected building systems.

## Do Not Use For

* Do not use this runbook for configuration, commissioning, or troubleshooting of live communications.
* Do not use this runbook to infer additional interfaces, protocols, or data flows beyond what the source explicitly states.

## Safety And Operational Notes

* This is a reference procedure derived from a training overview segment rather than an operational control task.
* Do not infer additional interfaces, protocols, or data flows beyond what the source explicitly states.
* Escalate for clarification if a component or connection is not clearly labeled in the source material.

## Access Or Tools Needed

* Access to the training video segment or extracted slide
* Overview architecture diagram
* Transcript for the segment

## Related Operational Context

* ctx_training_video_ups_chat_standard_communication_v1
* ctx_training_video_optisweep_integration_role_v1
* ctx_training_video_core_elements_architecture_v1

## Procedure Steps

### Step 1 — Open the overview slide and locate the labeled components

**Responsible role:** operator

**Instruction:**
Open the training overview slide for the segment and locate the labeled components shown in the architecture diagram, including UPS Chat, tote tipper or tote tip stations, Geek+ AGVs, hospital controller, OptiSweep Software, sorter, printer, and Aveva HMI.

**Expected result:**
The labeled core elements on the overview slide are identified for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0005_so_we_talked_to_ups_chat_primary_00_05_38_000](assets/5b53abba3e1c6807.jpg)

*The overview architecture slide showing the labeled core elements and their connections.*


**Stop or Escalate If:**

* A component expected from the source cannot be clearly identified on the slide.
* The source material is unclear or not legible enough to confirm labels.

---

### Step 2 — Identify UPS Chat as the standard communication layer

**Responsible role:** operator

**Instruction:**
Identify UPS Chat on the diagram and note the transcript statement that UPS uses a standard communication method through all buildings and that sorters talk the same way through this chat.

**Expected result:**
UPS Chat is recognized as the standard communication layer described in the training source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0005_so_we_talked_to_ups_chat_primary_00_05_38_000](assets/5b53abba3e1c6807.jpg)

*The UPS Chat label and its placement in the overview architecture slide.*


**Stop or Escalate If:**

* The diagram label for UPS Chat is unclear.
* The communication role cannot be tied back to the supplied source evidence.

---

### Step 3 — Locate OptiSweep Software and note its integration role

**Responsible role:** operator

**Instruction:**
Locate OptiSweep Software on the diagram and note the source statement that OptiSweep software integrates everything so the connected systems talk and work as a team.

**Expected result:**
OptiSweep Software is identified as the integration layer described in the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0005_so_we_talked_to_ups_chat_primary_00_05_38_000](assets/5b53abba3e1c6807.jpg)

*The OptiSweep Software label and its relationship to the other components on the overview slide.*


**Stop or Escalate If:**

* The OptiSweep Software label is unclear on the source slide.
* The integration role cannot be confirmed from the supplied transcript evidence.

---

### Step 4 — Verify the stated communication path for scan tunnel, tipper, and sorter

**Responsible role:** operator

**Instruction:**
Use the transcript and diagram together to verify that communication with the scan tunnel, tipper, and sorter is described as requiring connection to UPS Chat.

**Expected result:**
The source-supported communication relationship is confirmed for the scan tunnel, tipper, and sorter.

**Screens / Images:**

![artifact_training_video_training_video_day1_0005_so_we_talked_to_ups_chat_primary_00_05_38_000](assets/5b53abba3e1c6807.jpg)

*The overview slide connections associated with UPS Chat and the connected equipment referenced by the transcript.*


**Stop or Escalate If:**

* The source does not clearly show or state the communication relationship for one of the listed systems.
* Any interpretation would require inferring protocols or flows not explicitly stated.

---

### Step 5 — Record the components and communication roles from the overview

**Responsible role:** operator

**Instruction:**
Record which components are presented as part of the OptiSweep environment overview and which communication role is assigned to UPS Chat versus OptiSweep Software.

**Expected result:**
A source-grounded summary is produced listing the overview components and distinguishing UPS Chat as the common communication layer from OptiSweep Software as the integration layer.

**Screens / Images:**

![artifact_training_video_training_video_day1_0005_so_we_talked_to_ups_chat_primary_00_05_38_000](assets/5b53abba3e1c6807.jpg)

*The full overview architecture slide used to summarize the component list and communication roles.*


**Stop or Escalate If:**

* You cannot distinguish whether a statement is directly supported by the source.
* A component or role assignment is ambiguous in the source material.

---

## Success Criteria

* The user can identify the core components shown in the overview architecture slide.
* The user can state, based on the source, that UPS Chat is the common communication layer.
* The user can state, based on the source, that OptiSweep Software is the integration layer that makes connected systems work as a team.
* The recorded summary does not add unsupported interfaces, protocols, or data flows.

## Failure Conditions

* The overview slide or transcript is unavailable or unclear.
* A listed component cannot be confidently identified from the source.
* The communication relationship for scan tunnel, tipper, or sorter cannot be confirmed from the supplied evidence.
* The reviewer must infer unsupported interfaces, protocols, or data flows to complete the summary.

## Escalation Guidance

* Escalate for clarification if a component or connection is not clearly labeled in the source material.
* Escalate if the source evidence is insufficient to distinguish the role of UPS Chat from the role of OptiSweep Software.
* Do not proceed with assumptions when the source does not explicitly support a communication path or component relationship.

## Missing Details / Known Gaps

* The source does not provide a formal time estimate for completing this reference review.
* The source does not define supporting roles beyond the primary operator review role.
* The source does not provide configuration steps, commands, or protocol-level details for communications.
* The source section text field is empty in the packet, so grounding relies on supplied source refs, artifact retrieval text, and context records.

## Source Lineage

- Candidate IDs: candidate_training_video_identify_optisweep_core_elements_and_communication_path
- Source ID: `training_video_day1`
- Source Type: `training_video`
