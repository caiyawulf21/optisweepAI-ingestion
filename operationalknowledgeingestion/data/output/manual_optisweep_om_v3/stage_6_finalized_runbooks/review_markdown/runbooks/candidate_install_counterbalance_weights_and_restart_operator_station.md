# Install Counter-Balance Weights and Restart the Operator Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_counterbalance_weights_and_restart_operator_station_v1` |
| Title | Install Counter-Balance Weights and Restart the Operator Station |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Install the counter-balance weights using four M10 socket head screws with lock washers, tighten to approximately 51 Nm (65 ft-lbs), account for acceptable carriage drift behavior if the gripper is not mounted, reinstall guarding if necessary, and then restart the operator station using the separately referenced startup procedure.

## When To Use

Use when reinstalling the OptiSweep counter-balance weights as documented in section 7.3.3.2 INSTALLATION, including restoring guarding if needed and returning the operator station to service by following the referenced startup procedure on page 66.

## Do Not Use For

* Do not use this runbook as a complete operator-station startup procedure; the restart steps are not provided in this source section and are only referenced to page 66.
* Do not use this runbook for general low-risk support handling; the source context includes a 20 kg (44 lb) weight assembly, guarding access, and possible carriage movement.

## Safety And Operational Notes

* This procedure is not support-safe for general support use.
* The counter-balance weights are about 20 kg (44 lb) total.
* Once the weights are in place, if the gripper is not yet mounted, the carriage may begin to move.
* The documented carriage movement is acceptable because the weights will drift to the lower hard stop.
* The procedure includes guarding reinstallation and moving mechanical components.

## Access Or Tools Needed

* Access to the counter-balance weight mounting area
* Four (4) M10 socket head screws
* Lock washers
* Tooling to install and tighten M10 socket head screws
* Torque tool capable of approximately 51 Nm (65 ft-lbs)
* Access to top and/or bottom side guarding
* Access to the operator station restart procedure on page 66

## Procedure Steps

### Step 1 — Install the counter-balance weights with specified hardware

**Responsible role:** L2_support

**Instruction:**
Hold the counter-balance weights in place and install four (4) M10 socket head screws with the lock washer. Account for the documented total weight of about 20 kg (44 lb) during handling.

**Expected result:**
The counter-balance weights are held in position and secured with four M10 socket head screws and lock washers.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counterbalance weight assembly and the hardware context associated with the counter-balance weights.*


**Stop or Escalate If:**

* The 20 kg (44 lb) weight assembly cannot be safely held or positioned.
* Required M10 socket head screws or lock washers are unavailable.
* The weights cannot be secured in place.

---

### Step 2 — Tighten the counter-balance mounting screws

**Responsible role:** L2_support

**Instruction:**
Tighten the installed screws to approximately 51 Nm (65 ft-lbs).

**Expected result:**
The installed counter-balance mounting screws are tightened to the documented torque value.

**Stop or Escalate If:**

* A torque tool capable of approximately 51 Nm (65 ft-lbs) is not available.
* The installed screws cannot be tightened to the documented torque.

---

### Step 3 — Verify acceptable carriage movement condition

**Responsible role:** L2_support

**Instruction:**
Note that once the weights are in place, if the gripper is not yet mounted, the carriage may begin to move. The documented movement is acceptable because the weights will drift to the lower hard stop.

**Expected result:**
The technician recognizes that drift to the lower hard stop is an acceptable documented condition when the gripper is not mounted.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counterbalance assembly context related to the documented drift behavior after installation.*


**Stop or Escalate If:**

* Carriage movement does not match the documented acceptable drift to the lower hard stop.
* Movement appears unsafe or uncontrolled.

---

### Step 4 — Reinstall guarding if necessary

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side guarding, if necessary.

**Expected result:**
Any required top and/or bottom side guarding is reinstalled.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counterbalance area context; use the available figure to orient to the assembly while restoring guarding.*


**Stop or Escalate If:**

* Required guarding cannot be reinstalled.
* Guarding access or fitment does not allow restoration to the documented condition.

---

### Step 5 — Restart the operator station using the referenced procedure

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced procedure "Starting The Operator Station" on page 66.

**Expected result:**
The operator station restart is initiated using the referenced startup procedure.

**Stop or Escalate If:**

* The referenced procedure "Starting The Operator Station" on page 66 is not available.
* The operator station does not restart when following the referenced procedure.

---

## Success Criteria

* The counter-balance weights are installed with four M10 socket head screws and lock washers.
* The installed screws are tightened to approximately 51 Nm (65 ft-lbs).
* Any required top and/or bottom side guarding is reinstalled.
* The operator station is restarted using the referenced page 66 procedure.

## Failure Conditions

* The 20 kg (44 lb) weight assembly cannot be safely handled or positioned.
* Required hardware is missing or cannot be installed.
* The screws cannot be tightened to approximately 51 Nm (65 ft-lbs).
* Carriage movement occurs in a way not described as acceptable by the source.
* Required guarding is not reinstalled.
* The referenced startup procedure on page 66 is unavailable or restart cannot be completed.

## Escalation Guidance

* Escalate if the weight assembly cannot be safely handled due to the documented 20 kg (44 lb) load.
* Escalate if carriage movement appears unsafe or differs from the documented acceptable drift to the lower hard stop.
* Escalate if guarding cannot be restored.
* Escalate if the separate operator station startup procedure on page 66 is required but unavailable.

## Missing Details / Known Gaps

* This source section does not provide the detailed restart steps for "Starting The Operator Station"; only the page 66 reference is available.
* The packet does not provide source section OCR text for page 112, so step wording is grounded primarily in the candidate and attached packet evidence.
* The packet does not explicitly state whether production stop is required.
* The packet does not explicitly state whether LOTO is required for this installation subsection.
* No second-person staffing requirement is explicitly provided for installation in the candidate, even though the related Figure 7-4 artifact retrieval text notes two people for the removal procedure.

## Source Lineage

- Candidate IDs: candidate_install_counterbalance_weights_and_restart_operator_station
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
