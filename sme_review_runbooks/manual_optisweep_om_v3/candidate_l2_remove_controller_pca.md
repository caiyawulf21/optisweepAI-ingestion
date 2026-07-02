# Remove the Controller PCA

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_the_controller_pca_v1` |
| Title | Remove the Controller PCA |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely access the controller box and disconnect the Controller PCA for replacement removal. This source-specific runbook covers the documented removal portion only: lockout/tagout, required PPE and tools, optional station side panel removal for access, controller box release, ribbon cable retainer removal, and disconnecting the FFC, ribbon cable, and three Molex connectors from the Controller PCA.

## When To Use

Use when performing the documented removal portion of the Controller PCA replacement procedure in the OptiSweep Operation and Maintenance Manual, after the tipper has been locked out/tagged out and access to the controller box is required.

## Do Not Use For

* General operator execution.
* Reinstallation or verification steps, which are not present in this source packet.
* Use when the access hardware, fasteners, or connectors do not match the source description.

## Safety And Operational Notes

* LOTO the tipper before starting Controller PCA removal.
* Use safety glasses and gloves.
* Do not remove the four M8 button-head fasteners when releasing the controller box; loosen them and lift the box off the loosened fasteners.
* This procedure includes component removal and is not suitable for general operator execution.

## Access Or Tools Needed

* LOTO access for the tipper
* Safety glasses
* Gloves
* Replacement part: Controller PCA
* 1.5-mm hex wrench
* 6-mm hex wrench
* 3/8-in. wrench or socket
* Physical access to the station side panel and controller box

## Procedure Steps

### Step 1 — LOTO the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper as referenced by the manual before starting Controller PCA removal.

**Expected result:**
The tipper is in a locked out/tagged out state and safe for the documented removal work to begin.

**Stop or Escalate If:**

* LOTO cannot be completed or verified before proceeding.

---

### Step 2 — Gather PPE and tools

**Responsible role:** L2_support

**Instruction:**
Gather the documented PPE and tools: safety glasses, gloves, 1.5-mm hex wrench, 6-mm hex wrench, and 3/8-in. wrench or socket.

**Expected result:**
All documented PPE and tools are available at the work area before removal continues.

**Stop or Escalate If:**

* Required PPE or tools are not available.

---

### Step 3 — Remove the station side panel if needed

**Responsible role:** L2_support

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the station side panel, then remove the station side panel to access the motor.

**Expected result:**
The station side panel is removed when needed and access to the motor/internal area is available.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller/controller box location and surrounding access context after side panel removal.*

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Controller PCA procedure figure for the controller area associated with this removal task.*


**Stop or Escalate If:**

* The documented access hardware or fasteners do not match the source description.
* The side panel cannot be safely removed.

---

### Step 4 — Release the controller box

**Responsible role:** L2_support

**Instruction:**
Loosen the four M8 button-head screws to release the controller box; do not remove the fasteners, and lift the box off the loosened fasteners.

**Expected result:**
The controller box is released and lifted off the loosened fasteners without removing them.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller box location and mounting context associated with releasing the box.*

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Controller PCA figure for the controller box area used in this procedure.*


**Stop or Escalate If:**

* The controller box cannot be lifted off the loosened fasteners.
* The mounting hardware or securing points do not match the source description.

---

### Step 5 — Remove the ribbon cable retainer

**Responsible role:** L2_support

**Instruction:**
Remove the two M3 socket-head screws holding the ribbon cable retainer in place.

**Expected result:**
The ribbon cable retainer is removed and the ribbon cable connection is accessible.

**Screens / Images:**

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Controller PCA connection area where the ribbon cable retainer is located.*


**Stop or Escalate If:**

* The retainer hardware does not match the source description.
* The retainer cannot be safely removed.

---

### Step 6 — Disconnect the Controller PCA connections

**Responsible role:** L2_support

**Instruction:**
Unplug all documented connections from the PCA: the FFC, the ribbon cable, and the three Molex connectors.

**Expected result:**
The Controller PCA is disconnected from the FFC, ribbon cable, and three Molex connectors and is ready for the next replacement step.

**Screens / Images:**

![artifact_fig_7_19_controller_pca](assets/artifact_fig_7_19_controller_pca.png)

*Controller PCA connection area and the documented FFC, ribbon cable, and Molex connector locations.*

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*FFC-related connection hardware context for identifying the flat-flex cable style referenced in the procedure.*


**Stop or Escalate If:**

* Any PCA connection cannot be safely disconnected.
* The documented connectors do not match the source description.

---

## Success Criteria

* The tipper was locked out/tagged out before removal work began.
* The documented PPE and tools were used.
* The station side panel was removed if needed for access.
* The controller box was released by loosening the four M8 button-head screws without removing them.
* The ribbon cable retainer was removed by taking out the two M3 socket-head screws.
* The Controller PCA was disconnected from the FFC, ribbon cable, and three Molex connectors.
* The Controller PCA is ready for the next replacement step.

## Failure Conditions

* LOTO is not completed before work begins.
* Required PPE or tools are missing.
* Access hardware, fasteners, or connectors do not match the source description.
* The controller box cannot be lifted off the loosened fasteners.
* The ribbon cable retainer cannot be removed.
* Any PCA connection cannot be safely disconnected.

## Escalation Guidance

* Stop if the documented access hardware, fasteners, or connectors do not match the source description.
* Escalate if the controller box cannot be lifted off the loosened fasteners.
* Escalate if any PCA connection cannot be safely disconnected.
* Do not use this procedure for general operator execution.

## Missing Details / Known Gaps

* The source packet does not provide the full OCR text for section 7.3.18.1 Removal.
* No estimated time is supported in this packet for this specific procedure.
* The packet covers removal only and does not include reinstallation, post-removal verification, or return-to-service steps.
* No explicit role boundaries beyond L2_support are stated in the source packet.
* No commands are provided in the source packet.
* Production stop requirement is not explicitly stated in the source packet.

## Source Lineage

- Candidate IDs: candidate_l2_remove_controller_pca
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
