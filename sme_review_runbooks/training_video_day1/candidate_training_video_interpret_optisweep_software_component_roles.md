# Identify The Role Of Core OptiSweep Software Components

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_the_role_of_core_optisweep_software_components_v1` |
| Title | Identify The Role Of Core OptiSweep Software Components |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training source software overview slide and aligned transcript to identify the documented role of OptiSweep software, AVEVA, Ignition, Chat XLE, and S-Tunnel in the OptiSweep environment.

## When To Use

Use when a support user needs to identify or restate the documented role of the core software components shown in the training overview: OptiSweep software, AVEVA, Ignition, Chat XLE, and S-Tunnel.

## Do Not Use For

* Do not use for troubleshooting, configuration, or corrective action steps not stated in the source.
* Do not use to infer additional software behavior beyond the overview material.
* Do not use when a component role is needed beyond what is explicitly stated in the training source.

## Safety And Operational Notes

* This is a reference procedure derived from training material and does not provide operational control actions.
* Do not infer unsupported functions, configuration details, or troubleshooting actions from this overview-only material.

## Access Or Tools Needed

* Access to the training video segment or extracted slide
* Software overview slide for this segment

## Related Operational Context

* ctx_training_video_optisweep_software_overview_v1
* ctx_training_video_ignition_opc_server_reference_v1
* ctx_training_video_aveva_hmi_reference_v1
* ctx_training_video_chatxle_stunnel_network_boundary_v1

## Procedure Steps

### Step 1 — Open the software overview source and locate the listed components

**Responsible role:** L1_support

**Instruction:**
Open the training software overview source for this segment and locate the listed components: OptiSweep software, AVEVA, Ignition, Chat XLE, and S-Tunnel.

**Expected result:**
The user is viewing the source slide and can see the named components and their labels.

**Screens / Images:**

![artifact_training_video_training_video_day1_0009_software_we_have_of_course_our_primary_00_12_23_000](assets/05680eadbeac5e35.jpg)

*The training slide showing the software component list and labels for OptiSweep software, AVEVA - HMI, Ignition - OPC Server, Chat XLE - UPS communications, and S-Tunnel.*


**Stop or Escalate If:**

* Stop if the training slide cannot be accessed or read.
* Escalate if the component list cannot be confirmed from the supplied source evidence.

---

### Step 2 — Identify OptiSweep software as the integrating layer

**Responsible role:** L1_support

**Instruction:**
Identify OptiSweep software as the integrating layer based on the transcript statement that it integrates everything.

**Expected result:**
OptiSweep software is recorded as the integrating layer in the environment described by the source.

**Screens / Images:**

![artifact_training_video_training_video_day1_0009_software_we_have_of_course_our_primary_00_12_23_000](assets/05680eadbeac5e35.jpg)

*The OptiSweep software item on the software overview slide and the aligned retrieval text stating that OptiSweep integrates everything.*


**Stop or Escalate If:**

* Escalate if a more detailed OptiSweep function is requested than the source provides.
* Stop if the integrating role cannot be tied back to the supplied training evidence.

---

### Step 3 — Identify AVEVA as the HMI

**Responsible role:** L1_support

**Instruction:**
Identify AVEVA as the HMI using the slide label 'AVEVA - HMI.'

**Expected result:**
AVEVA is recorded as the HMI.

**Screens / Images:**

![artifact_training_video_training_video_day1_0009_software_we_have_of_course_our_primary_00_12_23_000](assets/05680eadbeac5e35.jpg)

*The AVEVA label on the software overview slide showing 'AVEVA - HMI.'*


**Stop or Escalate If:**

* Escalate if a role beyond HMI is needed from this source.
* Stop if the AVEVA label cannot be verified from the supplied evidence.

---

### Step 4 — Identify Ignition as the OPC server

**Responsible role:** L1_support

**Instruction:**
Identify Ignition as the OPC server using the slide label 'Ignition - OPC Server' and the transcript statement that it communicates through the tippers through OPC.

**Expected result:**
Ignition is recorded as the OPC server in the OptiSweep environment.

**Screens / Images:**

![artifact_training_video_training_video_day1_0009_software_we_have_of_course_our_primary_00_12_23_000](assets/05680eadbeac5e35.jpg)

*The Ignition label on the software overview slide showing 'Ignition - OPC Server' and the aligned transcript evidence about communication through tippers via OPC.*


**Stop or Escalate If:**

* Escalate if protocol or interface details beyond the source are required.
* Stop if the OPC server role cannot be confirmed from the supplied evidence.

---

### Step 5 — Identify Chat XLE as the UPS communications component

**Responsible role:** L1_support

**Instruction:**
Identify Chat XLE as the UPS communications component using the slide label 'Chat xLE — UPS communications.'

**Expected result:**
Chat XLE is recorded as the UPS communications component.

**Screens / Images:**

![artifact_training_video_training_video_day1_0009_software_we_have_of_course_our_primary_00_12_23_000](assets/05680eadbeac5e35.jpg)

*The Chat XLE label on the software overview slide showing UPS communications.*


**Stop or Escalate If:**

* Escalate if more detailed Chat XLE behavior is needed than the source provides.
* Stop if the UPS communications role cannot be verified from the supplied evidence.

---

### Step 6 — Identify S-Tunnel as the secure connection path across the network boundary

**Responsible role:** L1_support

**Instruction:**
Identify S-Tunnel as the secure or encrypted connection path from the OT network to the UPS network using the slide text and transcript explanation.

**Expected result:**
S-Tunnel is recorded as the secure or encrypted path between OTNet and the UPS network.

**Screens / Images:**

![artifact_training_video_training_video_day1_0009_software_we_have_of_course_our_primary_00_12_23_000](assets/05680eadbeac5e35.jpg)

*The S-Tunnel label on the software overview slide and the aligned explanation that communication crosses from OTNet to the UPS network through S-Tunnel as a secure channel.*


**Stop or Escalate If:**

* Escalate if detailed network design or tunnel configuration is requested.
* Stop if the secure-channel role across the OTNet and UPS network boundary cannot be confirmed from the supplied evidence.

---

### Step 7 — Record the component role mapping exactly as documented

**Responsible role:** L1_support

**Instruction:**
Record the component role mapping exactly as documented without adding unsupported functions or troubleshooting actions.

**Expected result:**
A source-grounded mapping is produced for all listed components without unsupported additions.

**Screens / Images:**

![artifact_training_video_training_video_day1_0009_software_we_have_of_course_our_primary_00_12_23_000](assets/05680eadbeac5e35.jpg)

*Use the full software overview slide as the final check that each component role matches the documented labels and transcript statements.*


**Stop or Escalate If:**

* Escalate if a consumer requests component roles beyond what is explicitly stated in the source.
* Stop if any role statement cannot be traced back to the supplied training evidence.

---

## Success Criteria

* The user can map OptiSweep software, AVEVA, Ignition, Chat XLE, and S-Tunnel to their documented roles using the training source.
* Each role statement is traceable to the supplied slide or transcript evidence.
* No unsupported functions, troubleshooting actions, or configuration details are added.

## Failure Conditions

* A component role cannot be confirmed from the supplied source evidence.
* The source slide or transcript is unavailable or unreadable.
* The resulting mapping includes inferred behavior or unsupported details not present in the source.

## Escalation Guidance

* Escalate if a component role is needed beyond what is explicitly stated in the source.
* Escalate if detailed configuration, troubleshooting, or architecture interpretation is requested from this overview-only material.
* Escalate if any component mapping cannot be grounded to the supplied training evidence.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not define supporting roles beyond the primary L1 support interpretation.
* The source does not provide commands, configuration steps, or troubleshooting procedures for these components.
* The source does not provide explicit do-not-use cases beyond the overview-only limitation and no-inference guidance.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_optisweep_software_component_roles
- Source ID: `training_video_day1`
- Source Type: `training_video`
