# Remove the controller PCA assembly access components and release the controller box

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_controller_pca_assembly_access_components_and_release_controller_box_v1` |
| Title | Remove the controller PCA assembly access components and release the controller box |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely prepare for controller PCA replacement by gathering the specified tools and PPE, locking out/tagging out the tipper, removing the station side panel if needed for access, loosening the controller box mounting screws without removing them, and lifting the controller box off the loosened fasteners.

## When To Use

Use this procedure when performing the removal/access portion of Controller PCA replacement and access to the controller box is required.

## Do Not Use For

* Do not use this runbook as a complete Controller PCA replacement procedure; the supplied source section is removal-only and does not include the actual PCA swap or reinstallation steps.
* Do not use this procedure if lockout/tagout cannot be completed safely.

## Safety And Operational Notes

* Wear safety glasses and gloves.
* LOTO the tipper before performing removal steps.
* Do not remove the four M8 button-head screws when releasing the controller box; only loosen them.

## Access Or Tools Needed

* Replacement part: Controller PCA
* PPE: Safety glasses
* PPE: Gloves
* 1.5-mm hex wrench
* 6-mm hex wrench
* 3/8-in. wrench or socket
* LOTO access for the tipper
* Access to the station side panel and controller box

## Procedure Steps

### Step 1 — Gather required replacement part, PPE, and tools

**Responsible role:** L2_support

**Instruction:**
Gather the replacement Controller PCA, safety glasses, gloves, a 1.5-mm hex wrench, a 6-mm hex wrench, and a 3/8-in. wrench or socket.

**Expected result:**
All listed PPE, tools, and the replacement Controller PCA are available at the work area.

**Screens / Images:**

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Use the figure to confirm the component being serviced is the Controller PCA/controller box assembly.*


**Stop or Escalate If:**

* Required PPE is not available.
* Required tools are not available.
* The replacement Controller PCA is not available or cannot be confirmed.

---

### Step 2 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper as referenced by "Operator Station Lockout/Tagout" on page 2.

**Expected result:**
The tipper is locked out/tagged out and safe for maintenance access.

**Stop or Escalate If:**

* Lockout/tagout cannot be completed safely.
* The referenced lockout/tagout procedure is unavailable.
* The tipper cannot be verified in a safe maintenance state.

---

### Step 3 — Remove the station side panel if access is needed

**Responsible role:** L2_support

**Instruction:**
If necessary to gain access, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the station side panel, then remove the station side panel to access the motor.

**Expected result:**
The station side panel is removed when needed, providing access to the internal service area.

**Screens / Images:**

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Look for the controller PCA/controller box service area associated with this procedure.*


**Stop or Escalate If:**

* The station side panel cannot be accessed.
* The documented nine self-tapping fasteners cannot be removed with the specified tool.
* Removing the side panel does not provide the expected access.

---

### Step 4 — Loosen the controller box mounting screws

**Responsible role:** L2_support

**Instruction:**
Loosen the four M8 button-head screws to release the controller box; do not remove the fasteners.

**Expected result:**
The controller box is released from the mounting points while the fasteners remain in place.

**Screens / Images:**

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Identify the Controller PCA/controller box and the mounting area associated with the four M8 button-head screws.*

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Use the related controller box figure as supplemental visual guidance for controller box location and release fastener context.*


**Stop or Escalate If:**

* The four M8 button-head screws cannot be identified.
* The screws cannot be loosened using the documented approach.
* The controller box does not release after loosening the documented fasteners.
* A fastener would need to be removed contrary to the source instruction.

---

### Step 5 — Lift the controller box off the loosened fasteners

**Responsible role:** L2_support

**Instruction:**
Lift the controller box off the loosened fasteners.

**Expected result:**
The controller box is free of the loosened fasteners and accessible for the next stage of controller PCA replacement work.

**Screens / Images:**

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Confirm controller box location and mounting relationship before lifting it off the loosened fasteners.*

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Use as supplemental visual reference for controller box position and release orientation.*


**Stop or Escalate If:**

* The controller box cannot be lifted off the loosened fasteners.
* Additional undocumented fasteners or obstructions are encountered.
* The controller box cannot be accessed or released using the documented fasteners and tools.

---

## Success Criteria

* The required PPE, tools, and replacement Controller PCA are gathered.
* The tipper is locked out/tagged out.
* The station side panel is removed if needed for access.
* The four M8 button-head screws are loosened without being removed.
* The controller box is released and can be lifted off the loosened fasteners.

## Failure Conditions

* Lockout/tagout cannot be completed safely.
* The station side panel cannot be accessed or removed using the documented fasteners and tools.
* The controller box cannot be accessed or released using the documented fasteners and tools.
* The source section is incomplete for the full Controller PCA replacement beyond removal/access.

## Escalation Guidance

* Stop and escalate if lockout/tagout cannot be completed safely.
* Stop and escalate if the station side panel or controller box cannot be accessed or released using the documented fasteners and tools.
* Escalate for additional source material or SME guidance for the actual PCA swap and reinstallation because the supplied source is removal-only.

## Missing Details / Known Gaps

* The supplied source packet does not include the actual OCR/body text for section 7.3.18 or 7.3.18.1.
* The supplied source is removal-only and does not include the actual Controller PCA swap steps.
* No installation or reassembly steps are provided in this packet.
* No estimated task duration is supported by the supplied candidate/source packet for this specific procedure.
* No explicit production stop requirement is stated in the supplied packet.

## Source Lineage

- Candidate IDs: controller_pca_removal
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
