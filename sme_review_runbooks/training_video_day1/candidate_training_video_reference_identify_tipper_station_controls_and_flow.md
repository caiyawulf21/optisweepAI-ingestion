# Identify Tipper Station Controls And Verify The Documented Tote Handling Flow

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_identify_tipper_station_controls_and_verify_the_documented_tote_handling_flow_v1` |
| Title | Identify Tipper Station Controls And Verify The Documented Tote Handling Flow |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the training material to identify the operator-facing controls at a tipper station and verify whether the observed station layout and tote handling flow match the documented clamp-tip-return sequence.

## When To Use

Use when an operator or reviewer needs to recognize the documented tipper station setup from the training source and compare the observed station arrangement or tote handling flow against the training description.

## Do Not Use For

* Detailed troubleshooting or fault recovery beyond identifying the documented HMI purpose and operator controls.
* Inferring undocumented control meanings, corrective actions, or operating limits from this training segment alone.
* Executing a production change, restart, or recovery procedure not explicitly described in this source.

## Safety And Operational Notes

* The training source identifies an operator E-stop as part of the tipper station setup.
* Do not infer undocumented control meanings or corrective actions from this segment alone.

## Access Or Tools Needed

* Visual access to the operator station
* Training slide or source excerpt describing the tipper station
* Visibility of the HMI, E-stop, ready-to-tip button, AGV tote position, and chute

## Related Operational Context

* ctx_training_video_tipper_station_overview_v1
* ctx_training_video_tipper_component_flow_v1
* ctx_training_video_tipper_hmi_reference_v1
* ctx_training_video_tipper_operator_controls_v1
* ctx_training_video_tipper_safety_estop_v1

## Procedure Steps

### Step 1 — Locate the operator station and identify the tipper setup

**Responsible role:** operator

**Instruction:**
Locate the operator station and identify the tipper setup. Confirm from the training source that each station is described as having two tippers.

**Expected result:**
The operator station is identified and the documented two-tipper station arrangement is recognized.

**Screens / Images:**

![artifact_training_video_training_video_day1_0008_todd_s_the_tipper_expert_we_primary_00_10_34_000](assets/f05d964a25e93a10.jpg)

*The training slide statement that each operator station has two tippers and the overall tipper station depiction.*


**Stop or Escalate If:**

* The observed station setup does not match the documented training description.
* The station cannot be visually confirmed against the source material.

---

### Step 2 — Identify the operator-facing controls

**Responsible role:** operator

**Instruction:**
Identify the operator-facing controls called out in the source: the self-contained HMI, the E-stop, and the ready-to-tip button.

**Expected result:**
The documented HMI and operator controls are recognized at the station or in the source reference.

**Screens / Images:**

![artifact_training_video_training_video_day1_0008_todd_s_the_tipper_expert_we_primary_00_10_34_000](assets/f05d964a25e93a10.jpg)

*The slide text describing the self-contained HMI for operation and fault recovery and the operator E-stop and ready-to-tip button.*


**Stop or Escalate If:**

* The station controls do not match the documented training description.
* A control is present but its meaning would require inference beyond what the source states.

---

### Step 3 — Observe tote position for tipper handling

**Responsible role:** operator

**Instruction:**
Observe whether a tote from the AGV is positioned for tipper handling.

**Expected result:**
The tote position relative to the AGV and tipper can be observed and compared to the documented handling flow.

**Screens / Images:**

![artifact_training_video_training_video_day1_0008_todd_s_the_tipper_expert_we_primary_00_10_34_000](assets/f05d964a25e93a10.jpg)

*The slide description that the tipper clamps a tote from the AGV and returns the tote back onto the AGV.*


**Stop or Escalate If:**

* The tote or AGV relationship at the station does not match the documented training description.
* The tote position cannot be verified visually.

---

### Step 4 — Verify the documented clamp-tip-return sequence

**Responsible role:** operator

**Instruction:**
Verify the documented motion sequence against what is present at the station: the tipper clamps the tote from the AGV, the tipping arm dumps contents onto the chute, and the tote is placed back onto the AGV.

**Expected result:**
The observed station behavior or arrangement is confirmed as matching or not matching the documented clamp-tip-return flow.

**Screens / Images:**

![artifact_training_video_training_video_day1_0008_todd_s_the_tipper_expert_we_primary_00_10_34_000](assets/f05d964a25e93a10.jpg)

*The slide text describing tote clamping from the AGV, tipping contents onto the chute, and placing the tote back onto the AGV.*


**Stop or Escalate If:**

* The handling sequence does not match the documented training description.
* Observed motion suggests a different sequence than clamp, tip to chute, and return to AGV.

---

### Step 5 — Record mismatches to the documented description

**Responsible role:** operator

**Instruction:**
Record any mismatch between the observed station setup or motion and the documented training description, without inventing corrective actions.

**Expected result:**
Any mismatch is documented for follow-up or escalation.

**Stop or Escalate If:**

* The station controls or handling sequence do not match the documented training description.
* Additional interpretation or corrective action would require information not present in this source.

---

## Success Criteria

* The operator-facing controls identified at the station match the documented source references for the self-contained HMI, E-stop, and ready-to-tip button.
* The observed station layout matches the documented description that each operator station has two tippers.
* The observed tote handling flow matches the documented sequence: clamp tote from AGV, tip contents onto chute, and place tote back onto AGV.
* Any mismatch is recorded without adding unsupported corrective actions.

## Failure Conditions

* The station layout does not match the documented two-tipper operator station description.
* The documented controls cannot be identified or do not match what is present.
* The observed tote handling sequence does not match the documented clamp-tip-return flow.
* The reviewer would need to infer undocumented meanings or corrective actions to continue.

## Escalation Guidance

* Escalate if the station controls or handling sequence do not match the documented training description.
* Escalate when the observed station cannot be confidently compared to the source using only the provided training evidence.
* Do not propose corrective actions from this source alone; request additional procedure or SME guidance if needed.

## Missing Details / Known Gaps

* The source is a training overview and does not provide a detailed operating sequence for pressing controls or initiating a tip.
* The source does not provide timing expectations, acceptance tolerances, or corrective actions.
* The source does not define escalation contacts or downstream documentation requirements for recorded mismatches.
* The source does not specify whether production stop or LOTO is required for any mismatch condition.

## Source Lineage

- Candidate IDs: candidate_training_video_reference_identify_tipper_station_controls_and_flow
- Source ID: `training_video_day1`
- Source Type: `training_video`
