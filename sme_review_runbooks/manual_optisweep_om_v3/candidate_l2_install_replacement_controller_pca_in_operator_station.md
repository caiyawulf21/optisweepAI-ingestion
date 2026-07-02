# Install Replacement Controller PCA In The Operator Station Control Box

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_replacement_controller_pca_in_the_operator_station_control_box_v1` |
| Title | Install Replacement Controller PCA In The Operator Station Control Box |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Install a replacement controller PCA into the operator station control box by transferring the plastic pieces and grounding wire, mounting the PCA, reconnecting the ribbon cable, Molex connectors, and FFC, remounting the control box, reinstalling panels as needed, and then restarting the operator station using the separately documented startup procedure.

## When To Use

Use this procedure when a replacement controller PCA is being installed in the operator station control box as part of restoring the operator station after controller PCA replacement.

## Do Not Use For

* Do not use this runbook as a complete controller PCA replacement procedure when removal steps are also required.
* Do not use this runbook to perform the operator station restart itself without the separate documented 'Starting The Operator Station' procedure on page 66.
* Do not use this runbook when the grounding wire, plastic pieces, retainer, ribbon cable, Molex connectors, or FFC cannot be installed as described.

## Safety And Operational Notes

* This procedure is not marked support-safe in the candidate and involves internal control box work and reconnection of multiple hardware components.
* Make sure excess cable is fed back into the stand and do not pinch any wires when hanging and securing the control box.
* Stop and escalate if any listed component cannot be installed or routed as described.

## Access Or Tools Needed

* Replacement controller PCA
* Two plastic pieces
* Grounding wire
* Fastener for grounding wire and plastic pieces
* Four M3 socket-head screws for PCA mounting
* Two M3 socket-head screws for retainer mounting
* Ribbon cable
* Retainer
* Three Molex connectors
* FFC
* Control box
* Stand with M8 button-head screws
* Top and/or bottom side panels, if removed
* Access to the operator station restart procedure on page 66

## Procedure Steps

### Step 1 — Transfer plastic pieces and grounding wire to the new PCA

**Responsible role:** L2_support

**Instruction:**
Transfer the two plastic pieces to the new PCA with the grounding wire in one corner, and use a fastener through all the parts to hold the grounding wire in place.

**Expected result:**
The two plastic pieces and grounding wire are installed on the new PCA and retained by the fastener.

**Stop or Escalate If:**

* The grounding wire cannot be installed in the required corner.
* The plastic pieces cannot be transferred or aligned.
* The fastener cannot pass through all parts to hold the grounding wire in place.

---

### Step 2 — Mount the new PCA in the control box

**Responsible role:** L2_support

**Instruction:**
Mount the new PCA in the box using the four M3 socket-head screws.

**Expected result:**
The replacement PCA is mounted in the control box using all four M3 socket-head screws.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller box location and mounting context for the controller assembly.*


**Stop or Escalate If:**

* The PCA cannot be mounted in the box.
* Any of the four M3 socket-head screws cannot be installed.

---

### Step 3 — Connect the ribbon cable and install the retainer

**Responsible role:** L2_support

**Instruction:**
Connect the ribbon cable and mount the retainer using the two M3 socket-head screws.

**Expected result:**
The ribbon cable is connected and the retainer is mounted with the two M3 socket-head screws.

**Stop or Escalate If:**

* The ribbon cable cannot be connected as described.
* The retainer cannot be mounted with the two M3 socket-head screws.

---

### Step 4 — Plug in the three Molex connectors

**Responsible role:** L2_support

**Instruction:**
Plug in the three Molex connectors.

**Expected result:**
All three Molex connectors are plugged in.

**Stop or Escalate If:**

* Any of the three Molex connectors cannot be plugged in as described.

---

### Step 5 — Plug in the FFC

**Responsible role:** L2_support

**Instruction:**
Plug in the FFC.

**Expected result:**
The FFC is plugged in.

**Screens / Images:**

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*Flat-flex cable appearance and related clamp hardware context.*


**Stop or Escalate If:**

* The FFC cannot be plugged in as described.

---

### Step 6 — Hang the control box on the stand and route cable safely

**Responsible role:** L2_support

**Instruction:**
Hang the control box on the M8 button-head screws on the stand, making sure to feed excess cable back into the stand and not pinch any wires.

**Expected result:**
The control box is hung on the stand and excess cable is routed back into the stand without pinched wires.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller box location and stand mounting context.*

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*General cable routing example to support avoiding pinched or poorly routed wires.*

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Cable routing and connector handling points relevant to feeding excess cable and avoiding wire damage.*


**Stop or Escalate If:**

* Cables cannot be routed back into the stand without pinching wires.
* The control box cannot be hung on the M8 button-head screws as described.

---

### Step 7 — Tighten the four M8 button-head screws

**Responsible role:** L2_support

**Instruction:**
Tighten the four M8 button-head screws securing the controller box to the stand.

**Expected result:**
The controller box is secured to the stand by the four M8 button-head screws.

**Screens / Images:**

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*Controller box mounting location for the stand attachment points.*


**Stop or Escalate If:**

* Any of the four M8 button-head screws cannot be tightened.
* The controller box is not secure after tightening.

---

### Step 8 — Reinstall side panels if necessary

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Any required top and/or bottom side panels are reinstalled.

**Stop or Escalate If:**

* Any required top and/or bottom side panel cannot be reinstalled.

---

### Step 9 — Restart the operator station using the documented startup procedure

**Responsible role:** L2_support

**Instruction:**
Restart the operator station using the documented 'Starting The Operator Station' procedure on page 66.

**Expected result:**
The operator station is ready to be restarted using the referenced startup procedure.

**Stop or Escalate If:**

* The separate 'Starting The Operator Station' procedure is not available.
* Installation issues remain unresolved before restart.

---

## Success Criteria

* The replacement controller PCA is installed in the control box.
* The two plastic pieces and grounding wire are transferred and secured.
* The ribbon cable, three Molex connectors, and FFC are reconnected.
* The control box is secured to the stand.
* Excess cable is fed back into the stand without pinched wires.
* Top and/or bottom side panels are reinstalled as needed.
* The operator station is ready to proceed with the documented restart procedure.

## Failure Conditions

* The grounding wire, plastic pieces, retainer, ribbon cable, Molex connectors, or FFC cannot be installed as described.
* Cables cannot be routed back into the stand without pinching wires.
* The controller box cannot be secured to the stand.
* The separate restart procedure is required but not included in this section.

## Escalation Guidance

* Escalate if the grounding wire, plastic pieces, retainer, ribbon cable, Molex connectors, or FFC cannot be installed as described.
* Escalate if cables cannot be routed back into the stand without pinching wires.
* Escalate if the controller box cannot be mounted or secured with the specified hardware.
* Escalate if restart cannot proceed because the separate 'Starting The Operator Station' procedure is needed and not available.

## Missing Details / Known Gaps

* The source packet does not provide OCR text for pages 179-181, so step wording is grounded primarily in the candidate and source references rather than direct section text quotes.
* No explicit torque values are provided in the packet for the M3 or M8 fasteners used in this installation section.
* No explicit PPE list is provided in the candidate for this installation section.
* The restart procedure content is not included in this packet; only the reference to page 66 is available.
* No directly matching artifact in the packet explicitly shows the plastic pieces, grounding wire corner location, PCA screw locations, or ribbon cable retainer placement for this exact section.

## Source Lineage

- Candidate IDs: candidate_l2_install_replacement_controller_pca_in_operator_station
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
