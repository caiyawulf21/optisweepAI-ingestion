# Explain the Basic Tipper Tote Handling Sequence

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_explain_basic_tipper_tote_handling_sequence_v1` |
| Title | Explain the Basic Tipper Tote Handling Sequence |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Source-specific explanatory runbook describing the normal tipper tote handling sequence documented in the manual: the tipper receives a tote from an AGV, the gripper senses the tote, the gripper pulls the tote up the tipper, and the tote is emptied into a chute.

## When To Use

Use when an operator or reviewer needs to describe or visually verify the documented normal tipper operating concept from AGV tote receipt through parcel discharge into the chute.

## Do Not Use For

* Troubleshooting abnormal tipper behavior
* Recovery from sequence failures or jams
* Detailed startup, shutdown, jogging, or maintenance actions
* Any procedure requiring controls, commands, timing, or acceptance thresholds not provided in this source section

## Safety And Operational Notes

* This candidate is based on a high-level operating description only.
* Do not add recovery or troubleshooting actions because the source section provides operating description only.

## Access Or Tools Needed

* Visual access to a tipper in operation or to the documented operating description
* Source description of tipper operation
* Figure 3-4 for gripper identification

## Related Operational Context

* ctx_manual_tipper_system_overview_v1
* ctx_manual_tipper_component_inventory_v1

## Procedure Steps

### Step 1 — Confirm tote receipt from an AGV

**Responsible role:** operator

**Instruction:**
Confirm from observation or from the source description that the tipper receives a tote from an AGV.

**Expected result:**
The tote is identified as arriving to the tipper from an AGV, matching the documented starting point of the sequence.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Overall operator station context showing the tipper and chute area.*


**Stop or Escalate If:**

* The observed sequence does not match the documented order of receive, sense, pull up, and empty into the chute.

---

### Step 2 — Identify the gripper as the sensing component

**Responsible role:** operator

**Instruction:**
Observe that the gripper is the component on the tipper that senses the tote. Use Figure 3-4 to identify the gripper if needed.

**Expected result:**
The gripper is identified as the tote-sensing component on the tipper.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Locate the gripper identified in Figure 3-4 as component 14 on the tipper assembly.*


**Stop or Escalate If:**

* The gripper cannot be identified from the provided figure or observation.
* The observed sensing component does not match the documented gripper reference.

---

### Step 3 — Verify the gripper pulls the tote up the tipper

**Responsible role:** operator

**Instruction:**
Verify that after sensing the tote, the gripper pulls the tote up the tipper.

**Expected result:**
The tote is pulled upward on the tipper after the gripper senses it.

**Screens / Images:**

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use the tipper component diagram as a reference for the gripper and tipper assembly during the pull-up portion of the sequence.*


**Stop or Escalate If:**

* The tote is not pulled up the tipper after sensing.
* The observed order differs from the documented sequence.

---

### Step 4 — Verify parcels empty into the chute

**Responsible role:** operator

**Instruction:**
Verify that the tote is tipped so the parcels empty into the chute.

**Expected result:**
Parcels are discharged from the tote into the chute.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Reference the chute location in the operator station layout.*

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Reference the tipper assembly involved in lifting and tipping the tote.*


**Stop or Escalate If:**

* Parcels do not empty into the chute.
* The observed discharge step does not follow the documented receive, sense, pull-up, and empty order.

---

### Step 5 — Record that the observed sequence matches the documented operating concept

**Responsible role:** operator

**Instruction:**
Record that the observed sequence matches the documented tipper operating concept if tote receipt, gripper sensing, pull-up, and parcel discharge into the chute all occur in order.

**Expected result:**
A documented confirmation exists that the observed sequence matches the manual’s operating description.

**Stop or Escalate If:**

* The observed sequence does not match the documented order of receive, sense, pull up, and empty into the chute.

---

## Success Criteria

* The user can describe and verify the documented normal tipper handling sequence from tote receipt through parcel discharge.
* The sequence is confirmed in the documented order: receive tote from AGV, gripper senses tote, gripper pulls tote up the tipper, and parcels empty into the chute.

## Failure Conditions

* The observed sequence does not match the documented order of receive, sense, pull up, and empty into the chute.
* The gripper cannot be identified as the sensing component from the provided source evidence.
* The source-supported sequence cannot be confirmed from observation or documentation.

## Escalation Guidance

* Escalate if the observed sequence does not match the documented order of receive, sense, pull up, and empty into the chute.
* Do not add recovery or troubleshooting actions because the source section provides operating description only.

## Missing Details / Known Gaps

* The source provides a high-level operating description only and does not provide detailed operator controls or execution steps.
* The source does not provide commands, HMI actions, timing, acceptance thresholds, or quantitative validation criteria.
* The source does not specify role boundaries beyond general operator use.
* The source does not provide explicit production stop or LOTO requirements for this explanatory sequence.

## Source Lineage

- Candidate IDs: candidate_explain_basic_tipper_tote_handling_sequence
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
