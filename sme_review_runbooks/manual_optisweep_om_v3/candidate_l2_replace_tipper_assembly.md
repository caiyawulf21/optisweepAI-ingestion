# Replace The Tipper Assembly

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_replace_the_tipper_assembly_v1` |
| Title | Replace The Tipper Assembly |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Remove an existing tipper and install a replacement tipper on the existing sub-plate using the documented service disconnection and reconnection steps. The source-supported flow includes lockout/tagout, PPE, optional side-panel removal for access, disconnecting power, Ethernet, air, and conduit services, supporting the tipper while removing the mounting screws, installing the replacement tipper, reconnecting services, reinstalling removed components as needed, and restarting the operator station.

## When To Use

Use this procedure when the tipper assembly must be removed and replaced on the existing sub-plate using the documented maintenance process in the OptiSweep Operation and Maintenance Manual.

## Do Not Use For

* Do not use this runbook for gripper replacement only.
* Do not use this runbook for counter-balance weight removal only.
* Do not use this runbook for startup-only actions without tipper replacement.

## Safety And Operational Notes

* Apply lockout/tagout to the tipper before service using the referenced Operator Station Lockout/Tagout procedure.
* Required PPE includes safety glasses and gloves.
* Support the tipper during removal from the sub-plate.
* Cover the air line and quick disconnect with tape to prevent debris from entering either side of the air line.

## Access Or Tools Needed

* Replacement tipper
* Safety glasses
* Gloves
* 3/8-in. wrench or socket if side-panel removal is necessary
* Access to the station side panel, control box, ClearLink controller, air-line quick disconnect, conduit, and sub-plate mounting screws
* Referenced Operator Station Lockout/Tagout procedure
* Referenced Starting The Operator Station procedure
* Referenced Gripper Replacement procedure if gripper removal is performed
* Referenced Counter-balance weights procedure if weight removal is performed

## Related Operational Context

* ctx_manual_stacklight_component_reference_v1
* ctx_manual_tipper_replacement_safety_v1
* ctx_manual_tipper_related_components_v1

## Procedure Steps

### Step 1 — Apply lockout/tagout

**Responsible role:** L2_support

**Instruction:**
Apply lockout/tagout to the tipper using the referenced Operator Station Lockout/Tagout procedure before performing any replacement work.

**Expected result:**
The tipper is locked out and tagged out for maintenance.

**Stop or Escalate If:**

* Stop if lockout/tagout cannot be applied using the referenced procedure.

---

### Step 2 — Put on required PPE

**Responsible role:** L2_support

**Instruction:**
Put on safety glasses and gloves before continuing with the tipper replacement procedure.

**Expected result:**
Required PPE is in place.

**Stop or Escalate If:**

* Stop if required PPE is not available.

---

### Step 3 — Remove station side panel if access is needed

**Responsible role:** L2_support

**Instruction:**
If necessary for access, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel.

**Expected result:**
The side panel is removed when needed and access to the motor/service area is available.

**Screens / Images:**

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*Use as image support for the side-panel and ClearLink controller access area referenced in the candidate note.*

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller box location behind the access area after side-panel removal.*


**Stop or Escalate If:**

* Escalate if the side panel cannot be removed as documented.

---

### Step 4 — Disconnect power cable at the control box

**Responsible role:** L2_support

**Instruction:**
Remove the control box and disconnect the power cable at the 6-pin Molex connector, then push the cable into the column.

**Expected result:**
The power cable is disconnected and moved into the column.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Control box and ClearLink controller location used for service disconnection context.*


**Stop or Escalate If:**

* Escalate if the control box or power connection cannot be disconnected as documented.

---

### Step 5 — Disconnect Ethernet from the ClearLink controller

**Responsible role:** L2_support

**Instruction:**
Unplug the Ethernet cable from the ClearLink controller and push it into the column.

**Expected result:**
The Ethernet cable is disconnected and moved into the column.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*ClearLink controller location for Ethernet disconnection.*


**Stop or Escalate If:**

* Escalate if the Ethernet connection cannot be disconnected as documented.

---

### Step 6 — Disconnect the air line at the quick disconnect

**Responsible role:** L2_support

**Instruction:**
Disconnect the air line at the quick disconnect at the bottom of the column, leaving the quick disconnect with the tipper side of the air line.

**Expected result:**
The air line is disconnected at the bottom of the column.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Pneumatic service area context for locating the air-line service path.*


**Stop or Escalate If:**

* Escalate if the air line or quick disconnect cannot be disconnected as documented.

---

### Step 7 — Tape over the air line and quick disconnect

**Responsible role:** L2_support

**Instruction:**
Add tape over the air line and quick disconnect to prevent debris from entering either side of the air line.

**Expected result:**
The disconnected air line and quick disconnect are protected from contamination.

**Stop or Escalate If:**

* Stop if contamination protection cannot be applied to the disconnected air line.

---

### Step 8 — Disconnect conduit and free service cables

**Responsible role:** L2_support

**Instruction:**
Fully disconnect the conduit bringing power, air, and Ethernet to the column, and pull these cables free from the tipper.

**Expected result:**
The conduit and service bundle are disconnected and free from the tipper.

**Stop or Escalate If:**

* Escalate if service connections or conduit cannot be disconnected as documented.

---

### Step 9 — Optionally remove gripper and counter-balance weights

**Responsible role:** L2_support

**Instruction:**
If needed for safer or easier replacement, remove the gripper and the counter-balance weights using the referenced procedures.

**Expected result:**
Optional related components are removed only when needed for access or safer handling.

**Screens / Images:**

![artifact_fig_7_4_counterbalance_weight](assets/artifact_fig_7_4_counterbalance_weight.png)

*Counter-balance weight assembly referenced for the optional removal procedure.*


**Stop or Escalate If:**

* Escalate if optional related components cannot be removed using the referenced procedures.

---

### Step 10 — Support the tipper and remove mounting screws

**Responsible role:** L2_support

**Instruction:**
Support the tipper and remove the four hex head screws holding the tipper to the sub-plate.

**Expected result:**
The existing tipper is detached from the sub-plate while supported.

**Stop or Escalate If:**

* Stop if the tipper cannot be safely supported during removal.
* Escalate if mounting hardware cannot be disconnected as documented.

---

### Step 11 — Install the replacement tipper

**Responsible role:** L2_support

**Instruction:**
Install the new tipper onto the existing sub-plate.

**Expected result:**
The replacement tipper is mounted on the existing sub-plate.

**Stop or Escalate If:**

* Escalate if the replacement tipper cannot be installed as documented.

---

### Step 12 — Reconnect conduit and services

**Responsible role:** L2_support

**Instruction:**
Reconnect the conduit, power, air, and Ethernet to the column and control box.

**Expected result:**
All documented services are reconnected to the replacement tipper.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Control box and ClearLink controller area for reconnecting Ethernet and power service context.*


**Stop or Escalate If:**

* Escalate if service connections, conduit, or mounting hardware cannot be reconnected as documented.

---

### Step 13 — Reinstall the gripper if it was removed

**Responsible role:** L2_support

**Instruction:**
Mount the gripper again if it was removed.

**Expected result:**
The gripper is reinstalled when applicable.

**Stop or Escalate If:**

* Escalate if the gripper cannot be remounted as required.

---

### Step 14 — Reinstall removed side panels

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels if they were removed.

**Expected result:**
Removed side panels are reinstalled.

**Stop or Escalate If:**

* Escalate if removed panels cannot be reinstalled.

---

### Step 15 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Restart the operator station using the referenced startup procedure.

**Expected result:**
The operator station is restarted after installation.

**Stop or Escalate If:**

* Escalate if the operator station cannot be restarted after installation.

---

## Success Criteria

* The replacement tipper is mounted to the existing sub-plate.
* Required power, Ethernet, air, and conduit connections are restored.
* Removed panels or related components are reinstalled as needed.
* The operator station is restarted.

## Failure Conditions

* Lockout/tagout cannot be applied using the referenced procedure.
* The tipper cannot be safely supported during removal.
* Service connections, conduit, or mounting hardware cannot be disconnected or reconnected as documented.
* The operator station cannot be restarted after installation.

## Escalation Guidance

* Stop the procedure if lockout/tagout cannot be applied using the referenced procedure.
* Stop the procedure if the tipper cannot be safely supported during removal.
* Escalate if service connections, conduit, or mounting hardware cannot be disconnected or reconnected as documented.
* Escalate if the operator station cannot be restarted after installation.

## Missing Details / Known Gaps

* The source packet does not provide the full verbatim page text for section 7.3.22.
* The source does not provide torque values for reinstallation fasteners.
* The source does not provide a documented estimated completion time for tipper replacement.
* The source does not provide explicit post-restart verification checks or status indicators.
* The source does not provide detailed instructions for control box removal beyond the candidate summary and related artifact context.
* The source does not provide explicit criteria for when gripper or counter-balance weight removal is required versus optional.

## Source Lineage

- Candidate IDs: candidate_l2_replace_tipper_assembly
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
