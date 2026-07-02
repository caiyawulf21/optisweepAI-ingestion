# Install Replacement Tipper Onto Existing Sub-Plate

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_replacement_tipper_onto_existing_sub_plate_v1` |
| Title | Install Replacement Tipper Onto Existing Sub-Plate |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Install a new tipper onto the existing sub-plate, reconnect the documented conduit, power, air, and Ethernet connections to the column and control box, reinstall related components and panels as needed, and restart the operator station.

## When To Use

Use this procedure when replacing a tipper and the documented installation portion is required to restore the station after the old tipper has been removed and the existing sub-plate remains in place.

## Do Not Use For

* Do not use this runbook as a complete tipper replacement procedure; the source packet only supports the installation portion.
* Do not use this runbook when detailed torque values, alignment checks, or verification criteria are required; those details are not provided in the source.
* Do not use this runbook as a substitute for the referenced gripper replacement or operator-station starting procedures.

## Safety And Operational Notes

* PPE identified in the candidate: safety glasses and gloves.
* This procedure is not marked support-safe in the candidate because it involves equipment replacement and reconnection of power, air, Ethernet, and mechanical components.
* If installation cannot be completed using the documented connections and referenced procedures, escalate.

## Access Or Tools Needed

* Replacement part: Tipper
* PPE: Safety glasses, gloves
* Access to the tipper, existing sub-plate, column, control box, and side panels
* Referenced procedure: Gripper Replacement
* Referenced procedure: Starting The Operator Station

## Procedure Steps

### Step 1 — Install the new tipper onto the existing sub-plate

**Responsible role:** L2_support

**Instruction:**
Install the new tipper onto the existing sub-plate.

**Expected result:**
The replacement tipper is mounted onto the existing sub-plate.

**Screens / Images:**

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*General A-axis/tipper mechanical assembly area for orientation during installation.*

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*General counterbalance assembly location on the tipper for mechanical orientation.*


**Stop or Escalate If:**

* The replacement tipper cannot be installed onto the existing sub-plate.
* The installation cannot be completed with the documented connections and referenced procedures.

---

### Step 2 — Reconnect conduit, power, air, and Ethernet

**Responsible role:** L2_support

**Instruction:**
Connect the conduit, power, air, and Ethernet to the column and control box.

**Expected result:**
The documented conduit, power, air, and Ethernet connections are restored to the column and control box.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller/controller box location that may help identify cable connection area.*

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Controller box area for orientation during reconnection.*

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*Cable routing and connection area on the tipper assembly.*


**Stop or Escalate If:**

* Any required conduit, power, air, or Ethernet connection cannot be completed.
* The documented connections and referenced procedures are insufficient to complete installation.

---

### Step 3 — Mount the gripper if necessary

**Responsible role:** L2_support

**Instruction:**
Mount the gripper, if necessary, using the referenced gripper replacement procedure.

**Expected result:**
The gripper is mounted when required.

**Screens / Images:**

![artifact_fig_7_6_gearbox](assets/artifact_fig_7_6_gearbox.png)

*General tipper assembly area where gripper-related mechanical restoration may be associated.*


**Stop or Escalate If:**

* The gripper is required but the referenced gripper replacement procedure is unavailable.
* The gripper cannot be mounted using the referenced procedure.

---

### Step 4 — Reinstall top and or bottom side panels if necessary

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Any required top and/or bottom side panels are reinstalled.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Station/controller box area that may be behind a side panel.*

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Controller box access area associated with side panel removal/reinstallation.*


**Stop or Escalate If:**

* Required side panels cannot be reinstalled.
* Panel restoration cannot be completed with the available documentation.

---

### Step 5 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced starting procedure.

**Expected result:**
The operator station is restarted using the referenced procedure.

**Stop or Escalate If:**

* The referenced starting procedure is unavailable.
* The operator station cannot be restarted using the referenced starting procedure.

---

## Success Criteria

* The replacement tipper is installed on the existing sub-plate.
* The documented conduit, power, air, and Ethernet connections are restored.
* The gripper is mounted if required.
* The top and/or bottom side panels are reinstalled if required.
* The operator station is restarted.

## Failure Conditions

* The replacement tipper cannot be installed on the existing sub-plate.
* Required conduit, power, air, or Ethernet connections cannot be completed.
* The gripper cannot be mounted when required.
* Required side panels cannot be reinstalled.
* The operator station cannot be restarted using the referenced procedure.
* The source does not provide detailed torque values, alignment checks, or verification details.

## Escalation Guidance

* Escalate if the installation cannot be completed with the documented connections and referenced procedures.
* Escalate when required referenced procedures are unavailable.
* Escalate if any required mechanical, electrical, pneumatic, or Ethernet reconnection cannot be completed.

## Missing Details / Known Gaps

* Source section text is empty in the packet; step wording is grounded primarily in the candidate and source reference metadata.
* No detailed installation substeps, fastener specifications, torque values, alignment instructions, or acceptance checks are provided in the packet.
* No explicit commands are provided in the packet.
* No explicit production-stop or LOTO requirement is stated in the supplied installation section packet.
* No explicit role boundaries beyond L2_support are provided.
* No explicit success verification beyond installation completion and restart is provided.

## Source Lineage

- Candidate IDs: candidate_l2_install_replacement_tipper_on_existing_subplate
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
