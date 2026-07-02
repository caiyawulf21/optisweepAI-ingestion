# Prepare and access the Tip (A-Axis) PCA for replacement

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_prepare_and_access_the_tip_a_axis_pca_for_replacement_v1` |
| Title | Prepare and access the Tip (A-Axis) PCA for replacement |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely prepare for Tip (A-Axis) PCA replacement by gathering the specified replacement part, PPE, and tools, locking out/tagging out the tipper, removing the station side panel if needed, and using Figure 7-18 to identify the Tip PCA area to be serviced.

## When To Use

Use this procedure when preparing to access the Tip (A-Axis) controller PCA area for replacement work as described in section 7.3.17 of the OptiSweep Operation and Maintenance Manual.

## Do Not Use For

* Do not use this procedure to perform the full PCA replacement beyond the initial access/removal steps, because the supplied source content is truncated.
* Do not use this procedure without first performing lockout/tagout of the tipper.

## Safety And Operational Notes

* Wear safety glasses and gloves.
* Perform lockout/tagout of the tipper before proceeding.
* Do not proceed without performing LOTO.

## Access Or Tools Needed

* LOTO access for the tipper
* Replacement part: Controller PCA
* PPE: safety glasses
* PPE: gloves
* 1.5-mm hex wrench
* 3/8-in. wrench or socket
* Wire ties

## Procedure Steps

### Step 1 — Gather required replacement part, PPE, and tools

**Responsible role:** L2_support

**Instruction:**
Gather the replacement Controller PCA, safety glasses, gloves, 1.5-mm hex wrench, 3/8-in. wrench or socket, and wire ties before starting the procedure.

**Expected result:**
All listed parts, PPE, and tools are available at the work area.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Use the figure context for the Tip PCA procedure while preparing the correct replacement part and service setup.*


**Stop or Escalate If:**

* Required PPE is not available.
* The replacement Controller PCA is not available.
* Required tools are not available.

---

### Step 2 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
Perform lockout/tagout of the tipper using the referenced Operator Station Lockout/Tagout procedure on page 2 before continuing.

**Expected result:**
The tipper is locked out/tagged out and safe for access work.

**Stop or Escalate If:**

* LOTO cannot be completed.
* The equipment cannot be verified as locked out/tagged out.
* Any condition prevents safe isolation of the tipper.

---

### Step 3 — Remove side panel fasteners if needed

**Responsible role:** L2_support

**Instruction:**
If needed to gain access, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel.

**Expected result:**
The side panel fasteners are removed and the panel is ready to be taken off.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Use the Tip PCA maintenance diagram as the visual support referenced for the access/removal procedure.*


**Stop or Escalate If:**

* The side panel cannot be removed as described.
* The fasteners cannot be removed with the specified tool.
* Any unexpected obstruction prevents safe panel access.

---

### Step 4 — Remove the station side panel

**Responsible role:** L2_support

**Instruction:**
Remove the station side panel to access the motor area after the panel fasteners have been removed if required.

**Expected result:**
The station side panel is removed and the motor area is accessible.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Look at the figure for the Tip PCA location and the accessed area after side panel removal.*


**Stop or Escalate If:**

* The side panel cannot be removed as described.
* The motor area is not accessible after panel removal.
* Any unexpected condition is found after opening the panel.

---

### Step 5 — Identify the Tip PCA using Figure 7-18

**Responsible role:** L2_support

**Instruction:**
Use Figure 7-18 to identify the Tip PCA or controller PCA in the accessed area.

**Expected result:**
The Tip PCA/controller PCA is visually identified in the opened service area.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Identify the Tip PCA / controller PCA location shown in Figure 7-18.*


**Stop or Escalate If:**

* The Tip PCA cannot be identified with confidence.
* The accessed area does not match the referenced figure.
* Further replacement steps are needed but not present in the supplied source.

---

## Success Criteria

* Required replacement part, PPE, and tools are gathered.
* The tipper has been locked out/tagged out.
* The station side panel has been removed if needed.
* The motor and Tip (A-Axis) PCA area are accessible.
* The Tip PCA/controller PCA has been identified using Figure 7-18.

## Failure Conditions

* LOTO is not performed before proceeding.
* Required tools, PPE, or replacement part are missing.
* The side panel cannot be removed as described.
* The Tip PCA/controller PCA cannot be identified from the accessed area.
* The source content does not provide the remaining replacement steps.

## Escalation Guidance

* Stop and escalate to qualified site support if the side panel cannot be removed as described.
* Do not proceed if LOTO cannot be completed or verified.
* Escalate for SME review if additional replacement steps are needed beyond this access/removal portion because the supplied source is truncated.

## Missing Details / Known Gaps

* The supplied source text is truncated and only covers the initial removal/access portion of the Tip (A-Axis) PCA replacement procedure.
* The full replacement, reconnection, reassembly, and post-maintenance verification steps are not present in the packet.
* The source sections included in the packet contain no OCR text, so step wording is grounded from the candidate and artifact retrieval text only.
* No explicit role boundaries beyond the inferred L2_support executor are provided in the source packet.
* No explicit production stop requirement is stated in the supplied source packet.

## Source Lineage

- Candidate IDs: tip_a_axis_pca_replacement_removal_access
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
