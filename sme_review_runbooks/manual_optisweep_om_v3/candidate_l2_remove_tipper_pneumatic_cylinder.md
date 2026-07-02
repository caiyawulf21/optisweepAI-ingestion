# Remove the Tipper Pneumatic Cylinder

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_the_tipper_pneumatic_cylinder_v1` |
| Title | Remove the Tipper Pneumatic Cylinder |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely remove the pneumatic cylinder from the tipper by locking out the equipment, gaining access to the cylinder, disconnecting the air lines, and releasing the cylinder from its rod-end and lower-bracket mounting points.

## When To Use

Use when the pneumatic cylinder must be removed from the tipper assembly as described in the OptiSweep Operation and Maintenance Manual section for pneumatic cylinder removal.

## Do Not Use For

* Do not use this as an operator procedure; the source-backed candidate indicates this task should be handled by L2 support because it includes LOTO, guarded/internal access, pneumatic disconnection, and mechanical component removal.
* Do not use when source-supported access, tools, or lockout/tagout controls are unavailable.

## Safety And Operational Notes

* Perform lockout/tagout before beginning work using the referenced Operator Station Lockout/Tagout procedure.
* Use safety glasses and gloves.
* Use caution when releasing the rod-end connection because the lift plate will drop a short distance.
* Stop and escalate if the cylinder, retaining ring, pin, air lines, bracket, or fasteners cannot be removed as described by the source.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure
* Replacement pneumatic cylinder
* Safety glasses
* Gloves
* 3/8-in. wrench or socket
* 24-mm open-ended wrench
* 4-mm hex wrench
* 5-mm hex wrench
* Loctite

## Procedure Steps

### Step 1 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced "Operator Station Lockout/Tagout" procedure on page 2 before performing any removal work.

**Expected result:**
The tipper is isolated and safe for maintenance access.

**Stop or Escalate If:**

* Lockout/tagout cannot be completed using the referenced procedure.
* The equipment cannot be confirmed in a safe isolated state.

---

### Step 2 — Remove the station side panel if access is needed

**Responsible role:** L2_support

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel to access the area.

**Expected result:**
The side panel is removed when needed and the cylinder access area is exposed.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Pneumatic cylinder location and surrounding access area associated with Figure 7-10.*


**Stop or Escalate If:**

* The side panel cannot be removed as described.
* Fasteners cannot be removed with the specified tool.
* Access to the cylinder area is still not available after panel removal.

---

### Step 3 — Remove the gripper cover

**Responsible role:** L2_support

**Instruction:**
Remove the gripper cover by removing the eight M8 button-head screws.

**Expected result:**
The gripper cover is removed and the cylinder area is further exposed.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Pneumatic cylinder removal context and nearby cover/access area associated with Figure 7-10.*


**Stop or Escalate If:**

* The gripper cover cannot be removed as described.
* The M8 button-head screws cannot be removed.

---

### Step 4 — Disconnect the air lines from the cylinder

**Responsible role:** L2_support

**Instruction:**
Remove the two air lines from the pneumatic cylinder.

**Expected result:**
Both air lines are disconnected from the cylinder.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Pneumatic cylinder identification and air-line connection area associated with Figure 7-10.*


**Stop or Escalate If:**

* The air lines cannot be disconnected as described.
* The cylinder remains connected by air lines after attempted removal.

---

### Step 5 — Release the rod-end connection

**Responsible role:** L2_support

**Instruction:**
At the rod end of the cylinder, remove one retaining ring and pull the pin to release the lift plate. Use caution because the lift plate will drop a short distance.

**Expected result:**
The rod end is disconnected from the lift plate.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Rod-end area of the pneumatic cylinder and associated mounting/release context from Figure 7-10.*


**Stop or Escalate If:**

* The retaining ring cannot be removed.
* The pin cannot be pulled.
* The rod-end connection cannot be released as described.
* The lift plate behavior is not as expected when released.

---

### Step 6 — Release the lower bracket and free the cylinder

**Responsible role:** L2_support

**Instruction:**
At the bottom of the cylinder, remove the two M6 socket head screws to release half of the lower bracket and free the air cylinder.

**Expected result:**
The lower bracket is released and the air cylinder is free for removal.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Bottom of the pneumatic cylinder and lower bracket area associated with Figure 7-10.*


**Stop or Escalate If:**

* The two M6 socket head screws cannot be removed.
* The lower bracket cannot be released as described.
* The air cylinder is not free after the bracket is released.

---

## Success Criteria

* The pneumatic cylinder is freed from its air connections and mounting points and removed from the tipper assembly.
* The tipper was locked out/tagged out before removal work.
* The side panel and gripper cover were removed as needed to gain access.
* The two air lines were disconnected from the cylinder.
* The rod-end retaining ring and pin were removed and the lift plate released.
* The lower bracket was released by removing the two M6 socket head screws.

## Failure Conditions

* Lockout/tagout cannot be completed or confirmed.
* The side panel, gripper cover, air lines, retaining ring, pin, lower bracket, or fasteners cannot be removed as described.
* The lift plate behavior during rod-end release is not as expected.
* The cylinder remains captured after the documented removal steps are completed.

## Escalation Guidance

* Escalate to appropriate support if lockout/tagout cannot be completed using the referenced procedure.
* Escalate if the cylinder, retaining ring, pin, air lines, bracket, or fasteners cannot be removed as described by the source.
* Because this procedure includes LOTO and component removal, it should be handled by L2 support rather than an operator.

## Missing Details / Known Gaps

* The packet does not provide the OCR/body text of section 7.3.10.1, so step wording is grounded primarily in the candidate and artifact retrieval text.
* No source-supported estimated time is provided in the packet for this removal procedure.
* The packet does not provide explicit role boundaries beyond the candidate’s L2_support designation.
* The packet does not provide explicit source text for production stop requirements.
* The packet includes tools for pneumatic cylinder replacement at the section level, but not every tool is explicitly tied to a specific removal step in the supplied evidence.
* No explicit command-line, HMI, or software commands are provided in the source packet.

## Source Lineage

- Candidate IDs: candidate_l2_remove_tipper_pneumatic_cylinder
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
