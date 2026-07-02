# Quick replacement of the Z-axis cable carrier

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_quick_replacement_of_the_z_axis_cable_carrier_v1` |
| Title | Quick replacement of the Z-axis cable carrier |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Replace the Z-axis cable carrier by reusing the existing mounted end pieces when both ends of the carrier are in good condition. The source-backed procedure uses lockout/tagout, optional station side panel removal for access, removal of the old carrier from the mounted end pieces, preparation of the new carrier, positioning of internal dividers against the air line, closing the cross bars, and snapping the new carrier into the existing end pieces.

## When To Use

Use this quick replacement procedure to replace the Z-axis cable carrier when both ends of the existing carrier are in good condition and can remain mounted to the tipper.

## Do Not Use For

* Do not use this quick replacement procedure when both ends of the carrier are not in good condition.
* Do not use this procedure when replacement requires removal or replacement of the mounted end pieces.

## Safety And Operational Notes

* Lock out/tag out the tipper before performing the procedure.
* This quick replacement applies only when both ends of the carrier are in good condition.
* If side panel removal is needed, use a 3/8-in. wrench or socket and remove nine self-tapping fasteners securing the side panel.

## Access Or Tools Needed

* LOTO access for the tipper
* 3/8-in. wrench or socket
* Access to the station side panel
* Replacement cable carrier

## Procedure Steps

### Step 1 — Lock out/tag out the tipper

**Responsible role:** L2_support

**Instruction:**
Lock out/tag out the tipper as referenced by the source before starting the cable carrier replacement.

**Expected result:**
The tipper is locked out/tagged out and safe for maintenance access.

**Stop or Escalate If:**

* LOTO cannot be applied.
* Safe maintenance state cannot be confirmed.

---

### Step 2 — Remove the station side panel if needed

**Responsible role:** L2_support

**Instruction:**
If needed, use a 3/8-in. wrench or socket to remove the nine self-tapping fasteners securing the side panel, then remove the station side panel.

**Expected result:**
The station side panel is removed when needed and access is available.

**Screens / Images:**

![artifact_fig_7_10_pneumatic_cylinder](assets/artifact_fig_7_10_pneumatic_cylinder.png)

*Use the maintenance figure as contextual support for the station side panel access area referenced by the source note.*


**Stop or Escalate If:**

* Nine self-tapping fasteners cannot be removed with the specified tool.
* The side panel cannot be removed safely.
* Required access is still not available after panel removal.

---

### Step 3 — Disconnect the old cable carrier from the mounted end pieces

**Responsible role:** L2_support

**Instruction:**
Snap apart the cable carrier at both ends, leaving the end pieces attached to the tipper.

**Expected result:**
The cable carrier is disconnected from both mounted end pieces and the end pieces remain attached to the tipper.

**Stop or Escalate If:**

* Either end piece is not in good condition.
* An end piece does not remain attached to the tipper.
* The carrier cannot be snapped apart without damaging the mounted end pieces.

---

### Step 4 — Prepare the new cable carrier ends and open its cross bars

**Responsible role:** L2_support

**Instruction:**
Snap the ends off the new cable carrier and open all cross bars on the outside of the new cable carrier.

**Expected result:**
The new cable carrier ends are removed and all outside cross bars are open.

**Stop or Escalate If:**

* The new cable carrier cannot be prepared as described.
* Cross bars are damaged or do not open.

---

### Step 5 — Open the old cable carrier and remove it

**Responsible role:** L2_support

**Instruction:**
Open all cross bars on the outside of the old cable carrier and remove the old cable carrier from the system.

**Expected result:**
The old cable carrier is removed from the system.

**Stop or Escalate If:**

* The old cable carrier cannot be removed cleanly.
* Removal affects the mounted end pieces or surrounding components.

---

### Step 6 — Position the new cable carrier and set the internal dividers

**Responsible role:** L2_support

**Instruction:**
Place the new cable carrier roughly in position and move the internal dividers all the way to one side, against the air line.

**Expected result:**
The new cable carrier is positioned and the internal dividers are moved fully to one side against the air line.

**Stop or Escalate If:**

* Internal dividers cannot be moved all the way to one side.
* The dividers cannot be positioned against the air line.
* The new carrier cannot be placed in position.

---

### Step 7 — Close all cross bars on the new cable carrier

**Responsible role:** L2_support

**Instruction:**
Snap all cross bars closed.

**Expected result:**
All cross bars on the new cable carrier are closed.

**Stop or Escalate If:**

* Any cross bar cannot be snapped closed.
* Any cross bar does not remain closed.

---

### Step 8 — Snap the new cable carrier into the mounted end pieces

**Responsible role:** L2_support

**Instruction:**
Snap both ends of the new cable carrier into the end pieces that remain mounted.

**Expected result:**
Both ends of the new cable carrier are snapped into the existing mounted end pieces.

**Stop or Escalate If:**

* Either end of the new cable carrier does not snap into the mounted end piece.
* Mounted end pieces are damaged or do not retain the new carrier.
* Final installed condition does not match the expected result.

---

## Success Criteria

* The new cable carrier is installed in place of the old carrier.
* The internal dividers are positioned against the air line.
* All cross bars are closed.
* Both ends of the new cable carrier are snapped into the existing mounted end pieces.

## Failure Conditions

* Both ends of the existing carrier are not in good condition.
* LOTO cannot be applied or confirmed.
* The station side panel cannot be removed when needed.
* Mounted end pieces are damaged, removed, or cannot be reused.
* Internal dividers cannot be positioned against the air line.
* Cross bars cannot be opened or closed as required.
* The new cable carrier cannot be snapped into the existing mounted end pieces.

## Escalation Guidance

* Escalate if both ends of the existing carrier are not in good condition, because the source states the quick replacement applies only in that condition.
* Escalate if LOTO cannot be completed or safe maintenance state cannot be confirmed.
* Escalate if the mounted end pieces are damaged or cannot remain attached for reuse.
* Escalate if the new cable carrier cannot be installed with both ends snapped into the existing mounted end pieces.

## Missing Details / Known Gaps

* The source packet does not provide the OCR text for section 7.3.16.2, so step evidence is grounded primarily in the candidate and supplied source references.
* No source-supported restart, return-to-service, or post-install verification steps were provided in the packet.
* No source-supported estimated time was provided for this quick replacement procedure.
* No source-supported dedicated image of the Z-axis cable carrier end pieces was provided in the packet.

## Source Lineage

- Candidate IDs: z_axis_cable_carrier_quick_replacement
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
