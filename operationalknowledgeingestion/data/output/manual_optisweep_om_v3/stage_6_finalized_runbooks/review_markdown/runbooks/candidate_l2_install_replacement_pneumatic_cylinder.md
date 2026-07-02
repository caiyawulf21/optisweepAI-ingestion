# Install a Replacement Pneumatic Cylinder

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_replacement_pneumatic_cylinder_v1` |
| Title | Install a Replacement Pneumatic Cylinder |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Install a new pneumatic cylinder by transferring the required fittings and spherical rod end from the old cylinder, mounting the new cylinder in the bracket, reconnecting the rod end and air lines, restoring the cover plate and side panels as needed, and restarting the operator station using the referenced startup procedure.

## When To Use

Use this procedure when replacing a pneumatic cylinder and the installation portion of the replacement task is required after removal of the old cylinder.

## Do Not Use For

* Do not use for pneumatic cylinder removal.
* Do not use as a standalone operator station startup procedure; this runbook only references the startup procedure on page 66.
* Do not use when required installation details or referenced restart instructions are unavailable.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate.
* The source packet for this installation excerpt does not provide additional installation-specific safety controls, so no further controls are asserted here.
* Use the referenced startup procedure on page 66 rather than inventing restart actions.

## Access Or Tools Needed

* Replacement pneumatic cylinder
* Old cylinder for transfer of air fittings and spherical rod end
* Air fittings
* Spherical rod end
* Bracket halves
* Two (2) M6 socket head screws
* Pin
* Retaining ring
* Air lines
* Cover plate
* Eight (8) M8 button-head screws
* Access to top and/or bottom side panels
* Access to the referenced operator station startup procedure on page 66

## Procedure Steps

### Step 1 — Transfer fittings and spherical rod end

**Responsible role:** L2_support

**Instruction:**
Transfer the air fittings and spherical rod end from the old cylinder to the new cylinder.

**Expected result:**
The replacement cylinder has the required air fittings and spherical rod end installed.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Pneumatic cylinder identification and the general cylinder assembly referenced by the replacement procedure.*


**Stop or Escalate If:**

* The air fittings cannot be transferred or installed as shown in the source.
* The spherical rod end cannot be transferred or installed as shown in the source.

---

### Step 2 — Mount cylinder in bracket

**Responsible role:** L2_support

**Instruction:**
Place the bottom of the cylinder in the bracket and install the other half of the bracket with the two (2) M6 socket head screws.

**Expected result:**
The cylinder is seated in the bracket and secured with the bracket half and two M6 socket head screws.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Pneumatic cylinder location and general mounting context for bracket installation.*


**Stop or Escalate If:**

* The cylinder cannot be placed in the bracket as shown in the source.
* The bracket half or the two (2) M6 socket head screws cannot be installed as shown in the source.

---

### Step 3 — Connect rod end to lift plate

**Responsible role:** L2_support

**Instruction:**
Slip the rod end between the brackets on the lift plate and insert the pin and retaining ring.

**Expected result:**
The rod end is positioned between the lift plate brackets and retained with the pin and retaining ring.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*General pneumatic cylinder assembly context related to rod-end connection.*


**Stop or Escalate If:**

* The rod end cannot be installed between the lift plate brackets as shown in the source.
* The pin or retaining ring cannot be installed as shown in the source.

---

### Step 4 — Reconnect air lines

**Responsible role:** L2_support

**Instruction:**
Reconnect the air lines.

**Expected result:**
The air lines are reconnected to the replacement cylinder.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*General pneumatic cylinder identification and air-line connection context.*


**Stop or Escalate If:**

* The air lines cannot be reconnected as shown in the source.

---

### Step 5 — Replace cover plate

**Responsible role:** L2_support

**Instruction:**
Replace the cover plate using the eight (8) M8 button-head screws.

**Expected result:**
The cover plate is reinstalled with eight M8 button-head screws.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*General pneumatic cylinder service area associated with cover plate reassembly.*


**Stop or Escalate If:**

* The cover plate cannot be replaced as shown in the source.
* The eight (8) M8 button-head screws cannot be installed as shown in the source.

---

### Step 6 — Reinstall side panels if necessary

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Any removed top and/or bottom side panels are reinstalled.

**Stop or Escalate If:**

* A required top and/or bottom side panel cannot be reinstalled.

---

### Step 7 — Restart operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced startup procedure on page 66.

**Expected result:**
The operator station is restarted using the referenced startup procedure.

**Stop or Escalate If:**

* The referenced operator station restart procedure is not available to the user.

---

## Success Criteria

* The replacement pneumatic cylinder is installed.
* Required fittings and the spherical rod end have been transferred to the new cylinder.
* The cylinder is mounted in the bracket and connected to the lift plate.
* Air lines are reconnected.
* The cover plate and any necessary side panels are reinstalled.
* The operator station is restarted using the referenced startup procedure.

## Failure Conditions

* Cylinder, bracket, rod end, pin, retaining ring, fittings, or air lines cannot be installed as shown in the source.
* Cover plate or side panels cannot be reinstalled.
* Referenced operator station startup procedure is not available.

## Escalation Guidance

* Escalate if the cylinder, bracket, rod end, pin, retaining ring, fittings, or air lines cannot be installed as shown in the source.
* Escalate if the referenced operator station restart procedure is not available to the user.

## Missing Details / Known Gaps

* The source packet does not provide the installation section text content, only the candidate-derived steps and source reference.
* No torque values are provided for the M6 socket head screws or M8 button-head screws.
* No explicit verification checks, leak checks, or post-install functional checks are provided in the source packet.
* No estimated completion time is provided for this installation excerpt.
* No installation-specific safety controls, production-stop requirement, or LOTO requirement are stated in the supplied installation excerpt.
* No dedicated installation figure for each step is supplied in the packet; only the general pneumatic cylinder figure is available.

## Source Lineage

- Candidate IDs: candidate_l2_install_replacement_pneumatic_cylinder
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
