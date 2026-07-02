# Remove Tip Or A-Axis PCA Connections And Access Panel

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_tip_or_a_axis_pca_connections_and_access_panel_v1` |
| Title | Remove Tip Or A-Axis PCA Connections And Access Panel |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Disconnect the documented Tip or A-Axis PCA connections and remove the station side panel if needed as part of the source-backed PCA removal procedure. The source-backed actions in this excerpt cover lockout/tagout, side panel removal for access, and disconnecting the FFC, three green terminal blocks, and two Molex connectors.

## When To Use

Use when performing the documented removal portion of the Tip (or A-Axis) PCA replacement procedure and access is needed to the PCA and its electrical connections.

## Do Not Use For

* Do not use for steps beyond the documented removal actions in this source excerpt.
* Do not use when the required lockout/tagout procedure cannot be confirmed.
* Do not use when connector identification or original connection locations cannot be confirmed from the source and equipment state.

## Safety And Operational Notes

* LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure on page 2 before beginning removal work.
* Use safety glasses and gloves.
* This procedure includes component disconnection work and is not marked support-safe.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure on page 2
* Safety glasses
* Gloves
* 3/8-in. wrench or socket
* Visual and physical access to the station side panel and PCA
* Replacement controller PCA
* 1.5-mm hex wrench
* Wire ties

## Procedure Steps

### Step 1 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure on page 2 before performing any removal or disconnection work.

**Expected result:**
The tipper is in the documented lockout/tagout state required for PCA removal work.

**Stop or Escalate If:**

* The required Operator Station Lockout/Tagout procedure cannot be confirmed.
* The tipper cannot be placed in the required lockout/tagout state.

---

### Step 2 — Remove the station side panel if needed

**Responsible role:** L2_support

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel to access the PCA area.

**Expected result:**
The station side panel is removed when needed and the PCA area is accessible.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Tip PCA area and general PCA location after side panel removal.*

![artifact_fig_7_15_tip_cable](assets/artifact_fig_7_15_tip_cable.png)

*Nearby side panel access context showing removal of nine self-tapping screws to access internal tipper components.*


**Stop or Escalate If:**

* The side panel fasteners or access method cannot be confirmed from the source and equipment state.
* Removing the side panel does not provide clear access to the PCA area.

---

### Step 3 — Unplug the FFC from the PCA

**Responsible role:** L2_support

**Instruction:**
Unplug the FFC from the PCA.

**Expected result:**
The FFC is disconnected from the PCA.

**Screens / Images:**

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*FFC identification and A-axis PCA connection context.*

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*General Tip PCA location to orient the FFC connection area.*


**Stop or Escalate If:**

* The FFC connection on the PCA cannot be identified with confidence from the source and equipment state.
* The cable or connector does not match the documented FFC connection.

---

### Step 4 — Unplug the three green terminal blocks and record their locations

**Responsible role:** L2_support

**Instruction:**
Unplug the three green terminal blocks, and note where each one was plugged in.

**Expected result:**
All three green terminal blocks are disconnected and their original locations are recorded or otherwise preserved.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Tip PCA layout for identifying the green terminal block connection area.*


**Stop or Escalate If:**

* The three green terminal blocks cannot be positively identified.
* The original connection locations cannot be preserved or confirmed before disconnection.

---

### Step 5 — Unplug the two Molex connectors

**Responsible role:** L2_support

**Instruction:**
Unplug the two Molex connectors.

**Expected result:**
Both Molex connectors are disconnected from the PCA assembly.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Tip PCA layout for general Molex connector location and orientation.*


**Stop or Escalate If:**

* The two Molex connectors cannot be positively identified from the source and equipment state.
* Additional undocumented connectors appear to require removal.

---

## Success Criteria

* The tipper has been locked out/tagged out using the referenced procedure.
* The station side panel has been removed if needed for access.
* The FFC has been unplugged from the PCA.
* The three green terminal blocks have been unplugged and their original locations noted.
* The two Molex connectors have been unplugged.
* The PCA electrical connections covered by this excerpt are disconnected in preparation for further PCA replacement work.

## Failure Conditions

* LOTO cannot be confirmed.
* The side panel or its fasteners cannot be removed as documented.
* The FFC, green terminal blocks, or Molex connectors cannot be positively identified.
* Original connector locations cannot be confirmed or preserved.
* The task would require proceeding beyond the documented removal actions in this source excerpt.

## Escalation Guidance

* Escalate if the required lockout/tagout procedure cannot be confirmed.
* Escalate if connector identification cannot be confirmed from the source and equipment state.
* Escalate if original connection locations cannot be determined before disconnecting the terminal blocks.
* Do not proceed beyond the documented removal actions in this source excerpt.

## Missing Details / Known Gaps

* The source packet does not provide the full OCR text of section 7.3.17.1 Removal.
* The source excerpt does not provide explicit connector pinouts, labels, or exact physical locations for the three green terminal blocks and two Molex connectors.
* The source excerpt does not include the continuation of the replacement procedure beyond these removal actions.
* The source does not explicitly state whether production stop is required.
* The source does not provide a source-specific do-not-use list beyond the documented excerpt boundaries.

## Source Lineage

- Candidate IDs: candidate_l2_remove_tip_a_axis_pca_connections_and_access_panel
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
