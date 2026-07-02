# Remove the ClearLink (CLINK) Controller

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_the_clearlink_clink_controller_v1` |
| Title | Remove the ClearLink (CLINK) Controller |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Remove the ClearLink (CLINK) controller from its controller box for replacement or service by applying lockout/tagout, using required PPE and tools, accessing the controller area if needed, releasing the controller box, disconnecting the controller cables, and removing the controller from the box.

## When To Use

Use this procedure when the ClearLink (CLINK) controller must be removed from the controller box for replacement or service.

## Do Not Use For

* Do not use this procedure when the required Operator Station Lockout/Tagout procedure is not available.
* Do not use this procedure for normal operator tasks.
* Do not use this procedure as a reinstallation or replacement instruction beyond controller removal.

## Safety And Operational Notes

* Use the referenced Operator Station Lockout/Tagout procedure before accessing or removing the controller.
* Wear safety glasses and gloves.
* Do not remove the four M8 button-head screws when releasing the controller box; loosen them and lift the box off the loosened fasteners.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure
* Safety glasses
* Gloves
* Replacement CLINK controller
* 2-mm hex wrench
* Tool to cut wire ties
* Wire ties
* 3/8-in. wrench or socket if side panel removal is necessary

## Procedure Steps

### Step 1 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure before beginning controller removal.

**Expected result:**
The tipper is locked out and tagged out and safe to access for service.

**Stop or Escalate If:**

* The referenced lockout/tagout procedure is not available.
* LOTO cannot be completed as required.

---

### Step 2 — Put on required PPE

**Responsible role:** L2_support

**Instruction:**
Put on safety glasses and gloves before performing the removal procedure.

**Expected result:**
Required PPE is in place before work continues.

**Stop or Escalate If:**

* Required PPE is not available.

---

### Step 3 — Gather required tools and parts

**Responsible role:** L2_support

**Instruction:**
Gather the replacement CLINK controller, 2-mm hex wrench, tool to cut wire ties, wire ties, and if necessary a 3/8-in. wrench or socket.

**Expected result:**
All listed tools and parts are available for the removal task.

**Stop or Escalate If:**

* Required tools or parts are not available.

---

### Step 4 — Remove the station side panel if access is needed

**Responsible role:** L2_support

**Instruction:**
If necessary, remove the nine self-tapping fasteners from the station side panel with a 3/8-in. wrench or socket, then remove the station side panel to access the area.

**Expected result:**
The controller area is accessible.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Use the CLINK controller figure to identify the controller box area and access location after removing the station side panel.*


**Stop or Escalate If:**

* The side panel cannot be removed safely.
* Access to the controller area remains blocked after panel removal.

---

### Step 5 — Release the controller box

**Responsible role:** L2_support

**Instruction:**
Loosen the four M8 button-head screws to release the controller box. Do not remove these fasteners. Lift the box off the loosened fasteners.

**Expected result:**
The controller box is released from its mounting fasteners and can be lifted free.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller box mounting location and the four M8 button-head screw attachment points.*


**Stop or Escalate If:**

* The controller box cannot be released after loosening the four M8 button-head screws.
* The box does not lift free from the loosened fasteners.

---

### Step 6 — Disconnect the CLINK controller cables

**Responsible role:** L2_support

**Instruction:**
Disconnect the cables connected to the CLINK controller.

**Expected result:**
All cables connected to the CLINK controller are disconnected.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Identify the CLINK controller and the connected cables to be disconnected.*


**Stop or Escalate If:**

* Cable connections cannot be safely disconnected.
* The connected cables cannot be clearly identified from the available source material.

---

### Step 7 — Remove the controller from the box

**Responsible role:** L2_support

**Instruction:**
Remove the two M5 socket-head fasteners holding the controller in the box and lift the controller out.

**Expected result:**
The CLINK controller is removed from the controller box and lifted out.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller seated in the box and the fastener locations used to secure it.*


**Stop or Escalate If:**

* The controller cannot be removed after the two M5 socket-head fasteners are removed.
* The controller remains mechanically bound in the box.

---

## Success Criteria

* The CLINK controller is removed from the controller box.
* The controller has been lifted out for replacement or further service.

## Failure Conditions

* The referenced lockout/tagout procedure is not available.
* The controller box cannot be released after loosening the four M8 button-head screws.
* Cable connections cannot be safely disconnected.
* The controller cannot be removed from the box.

## Escalation Guidance

* Escalate if the source-referenced lockout/tagout procedure is not available.
* Escalate if the controller box cannot be released after loosening the four M8 button-head screws.
* Escalate if cable connections cannot be safely disconnected.
* Because this procedure involves LOTO, panel removal, hardware removal, and controller disconnection in the tipper area, it should be handled by L2 support rather than an operator.

## Missing Details / Known Gaps

* The source packet does not provide the body text of section 7.3.13.1 Removal; step wording is grounded from the candidate and artifact retrieval text.
* No connector names, cable labels, or disconnect sequence are provided in the source packet.
* No torque values are provided for removed fasteners.
* No reinstallation or replacement steps are included in this removal-only procedure.
* No explicit production stop requirement is stated in the packet.

## Source Lineage

- Candidate IDs: candidate_l2_remove_clink_controller_from_controller_box
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
