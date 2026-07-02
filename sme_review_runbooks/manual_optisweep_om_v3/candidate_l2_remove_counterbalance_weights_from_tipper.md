# Remove Counterbalance Weights From the Tipper

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_counterbalance_weights_from_tipper_v1` |
| Title | Remove Counterbalance Weights From the Tipper |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | `L2_support` |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely remove the tipper counterbalance weights and associated fasteners using the documented removal procedure. The source states that two people are required, the tipper must be locked out/tagged out, guarding may need to be removed for access, four M10 socket head screws with lock washers secure the weights, and the carriage may drift so that the gripper moves to the lower hard stop after the weights are removed.

## When To Use

Use this procedure when service work requires removal of the tipper counterbalance weights as documented in section 7.3.3.1 Removal of the OptiSweep Operation and Maintenance Manual.

## Do Not Use For

* Do not use for general operator tasks.
* Do not use when the required two-person handling support is not available.
* Do not use as a substitute for the separate Operator Station Lockout/Tagout procedure referenced by the source.

## Safety And Operational Notes

* This procedure is not support-safe for general operator use.
* Two people are required by the source.
* Perform the referenced Operator Station Lockout/Tagout procedure before accessing or removing the counterbalance weights.
* Guarding may need to be removed to gain access.
* The counterbalance weights total about 20 kg (44 lb).
* As the fourth fastener is removed, hold the weights so they do not fall.
* After removal, the carriage may begin to move; the documented acceptable result is that the gripper drifts to the lower hard stop.

## Access Or Tools Needed

* Tipper access
* Operator Station Lockout/Tagout procedure
* Safety glasses
* Gloves
* 16-mm hex wrench
* 3/8-in. wrench/socket
* Two people

## Procedure Steps

### Step 1 — Prepare personnel, PPE, and tools

**Responsible role:** L2_support

**Instruction:**
Use two people for the procedure and gather the documented PPE and tools: safety glasses, gloves, 16-mm hex wrench, and 3/8-in. wrench/socket.

**Expected result:**
Two qualified people are present and the required PPE and tools are available at the tipper.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Review the counterbalance weight assembly location to understand the work area before starting.*


**Stop or Escalate If:**

* Two people are not available.
* Required PPE or tools are not available.

---

### Step 2 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure on page 2.

**Expected result:**
The tipper is locked out/tagged out in accordance with the referenced procedure.

**Stop or Escalate If:**

* The tipper cannot be placed in the required LOTO state.
* The referenced Operator Station Lockout/Tagout procedure is unavailable.

---

### Step 3 — Remove guarding if needed for access

**Responsible role:** L2_support

**Instruction:**
Remove the top and/or bottom side guarding if necessary to access the counterbalance weights.

**Expected result:**
The counterbalance weight area is accessible for fastener removal.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Use Figure 7-4 to identify the counterbalance weight area and the guarding/access area around the assembly.*


**Stop or Escalate If:**

* Required access to the counterbalance weights cannot be obtained.
* Guarding removal exposes conditions not covered by the source procedure.

---

### Step 4 — Remove the four counterbalance fasteners

**Responsible role:** L2_support

**Instruction:**
Remove the four M10 socket head screws holding the counterbalance weights in place, including the lock washers.

**Expected result:**
All four M10 socket head screws and their lock washers are removed from the counterbalance weight assembly.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Identify the counterbalance weights, the four M10 socket head screws, lock washers, and mounting points shown in Figure 7-4.*


**Stop or Escalate If:**

* A fastener cannot be removed.
* The weights cannot be controlled during fastener removal.

---

### Step 5 — Support the weights during final fastener removal

**Responsible role:** L2_support

**Instruction:**
As the fourth fastener is removed, hold the weights so they do not fall; the source states the weights are about 20 kg (44 lb) total.

**Expected result:**
The weights remain controlled and do not fall as the final fastener is removed.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Use Figure 7-4 to confirm the weight assembly orientation and where support is needed during final fastener removal.*


**Stop or Escalate If:**

* The weights cannot be controlled during removal.
* The weights begin to fall or shift unexpectedly.

---

### Step 6 — Remove the weights and verify acceptable carriage drift

**Responsible role:** L2_support

**Instruction:**
Remove the counterbalance weights and observe that the carriage may begin to move; the documented acceptable result is that the gripper drifts to the lower hard stop.

**Expected result:**
The counterbalance weights are removed from the tipper, and any resulting carriage movement is limited to the documented acceptable drift of the gripper to the lower hard stop.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Use Figure 7-4 as the reference for the counterbalance weight assembly being removed.*


**Stop or Escalate If:**

* Observed movement does not match the documented acceptable drift to the lower hard stop.

---

## Success Criteria

* The tipper counterbalance weights are removed.
* All four M10 socket head screws and lock washers have been removed from the weight assembly.
* The weights are controlled during removal and do not fall.
* Any resulting carriage movement matches the documented acceptable condition: the gripper drifts to the lower hard stop.

## Failure Conditions

* The procedure is attempted without two people.
* The tipper is not locked out/tagged out.
* The counterbalance weights cannot be safely controlled during removal.
* The weights fall or are at risk of falling during final fastener removal.
* Observed carriage movement does not match the documented acceptable drift to the lower hard stop.

## Escalation Guidance

* Stop the procedure if the weights cannot be controlled during removal.
* Stop and escalate if the observed movement does not match the documented acceptable drift to the lower hard stop.
* Escalate if the referenced Operator Station Lockout/Tagout procedure cannot be completed or is unavailable.

## Missing Details / Known Gaps

* The packet does not include the full source text for section 7.3.3.1 Removal, so exact manual wording beyond the candidate and artifact retrieval text is limited.
* The referenced Operator Station Lockout/Tagout procedure is external to this section and its detailed steps are not included in this packet.
* No estimated time is provided in the supplied source evidence.
* No explicit role split beyond the source-stated two-person requirement is provided.

## Source Lineage

- Candidate IDs: candidate_l2_remove_counterbalance_weights_from_tipper
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
