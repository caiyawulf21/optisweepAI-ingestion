# Install Tip or A-Axis Cable

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_tip_or_a_axis_cable_v1` |
| Title | Install Tip or A-Axis Cable |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Install and route a new Tip or A-axis cable, connect the labeled M8 connectors to the documented components, secure the cable, reinstall covers and panels, and restart the operator station using the referenced startup procedure.

## When To Use

Use this procedure when installing a new Tip or A-axis cable as described in the OptiSweep Operation and Maintenance Manual section 7.3.15.2 Installation.

## Do Not Use For

* Do not use this runbook when connector labels or destinations do not match the documented connection points.
* Do not use this runbook if the cable cannot be routed and secured as documented.
* Do not continue with this runbook if the valve cover would pinch wires or the grommet cannot be inserted into the tote sensor wire notch.
* Do not use this runbook as a substitute for the operator station startup procedure; restart is only referenced to page 66.

## Safety And Operational Notes

* This is not marked support-safe in the candidate and involves internal hardware work.
* Stop if wires cannot be routed without dangling near the A-axis PCA or if the cable cannot be secured as documented.
* Stop if the dividers cannot be positioned between the cable and air line.
* Stop if any connector label or destination does not match the documented connection points.
* Stop if the valve cover would pinch wires or the grommet cannot be inserted into the tote sensor wire notch.

## Access Or Tools Needed

* Access to the A-axis PCA area
* New Tip or A-axis cable
* Cable carrier
* Wire ties
* Access to the grommet
* Access to the valve, tote detect sensor, longer gripper sensor, and shorter gripper sensor
* Valve cover
* Four M4x50 socket-head screws
* Access to top and/or bottom side panels
* Referenced procedure: Starting The Operator Station

## Procedure Steps

### Step 1 — Connect cable to A-axis PCA and route into cable carrier

**Responsible role:** L2_support

**Instruction:**
Plug the new cable into the A-axis PCA and route the cable around the gearbox and into and around the cable carrier.

**Expected result:**
The new cable is connected at the A-axis PCA and follows the documented path around the gearbox and through the cable carrier.

**Screens / Images:**

![artifact_fig_7_3_a_axis_pca_connections](assets/artifact_fig_7_3_a_axis_pca_connections.jpeg)

*A-axis PCA connection point for the cable.*

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Cable path around the gearbox and into the cable carrier.*

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Installation routing and connector handling points near the A-axis PCA and cable carrier.*


**Stop or Escalate If:**

* The cable cannot be connected to the A-axis PCA.
* The cable cannot be routed around the gearbox and into the cable carrier as documented.

---

### Step 2 — Close cable carrier cross bars and position dividers

**Responsible role:** L2_support

**Instruction:**
Close all cross bars and ensure the dividers are between the cable and air line.

**Expected result:**
All cross bars are closed and the dividers separate the cable from the air line.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Cable carrier area and divider placement between the cable and air line.*

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Cable routing through the carrier for comparison with the documented path.*


**Stop or Escalate If:**

* The dividers cannot be positioned between the cable and air line.
* The cable carrier cross bars cannot be closed with the cable in the documented position.

---

### Step 3 — Align cable markings and secure with wire ties

**Responsible role:** L2_support

**Instruction:**
Align the cable markings to the cable carrier and wire tie the cable in place as before, including both ends of the cable carrier and the tie point on the A-axis carriage.

**Expected result:**
Cable markings align to the cable carrier and the cable is secured at both ends of the cable carrier and at the A-axis carriage tie point.

**Screens / Images:**

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Cable routing and tie locations along the carrier path.*

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Cable marking alignment and wire tie locations at the cable carrier and A-axis carriage.*


**Stop or Escalate If:**

* The cable cannot be secured as documented.
* The cable markings cannot be aligned to the cable carrier.

---

### Step 4 — Contain cable near A-axis PCA

**Responsible role:** L2_support

**Instruction:**
Near the A-axis PCA, verify that no wires are dangling and use wire ties as needed to contain the cable.

**Expected result:**
No wires are dangling near the A-axis PCA and the cable is contained.

**Screens / Images:**

![artifact_fig_7_3_a_axis_pca_connections](assets/artifact_fig_7_3_a_axis_pca_connections.jpeg)

*A-axis PCA area where cable containment should be verified.*

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Cable handling near the A-axis PCA and surrounding routing area.*


**Stop or Escalate If:**

* Wires cannot be routed without dangling near the A-axis PCA.
* The cable cannot be contained as documented.

---

### Step 5 — Pass M8 connectors and cable jacket through grommet

**Responsible role:** L2_support

**Instruction:**
Route all four M8 connectors through the grommet one at a time, then push the end of the jacketed cable through the grommet.

**Expected result:**
All four M8 connectors and the jacketed cable end are passed through the grommet.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Grommet entry path and connector pass-through handling.*


**Stop or Escalate If:**

* All four M8 connectors cannot be routed through the grommet one at a time.
* The jacketed cable end cannot be pushed through the grommet.

---

### Step 6 — Connect Valve-labeled M8 connector

**Responsible role:** L2_support

**Instruction:**
Connect the 3-pin M8 connector labeled "Valve" to the valve.

**Expected result:**
The 3-pin M8 connector labeled "Valve" is connected to the valve.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Valve connection point for the 3-pin M8 connector labeled Valve.*


**Stop or Escalate If:**

* Any connector label or destination does not match the documented connection point.
* The 3-pin M8 connector labeled Valve cannot be connected to the valve.

---

### Step 7 — Connect 4-pin M8 connector to tote detect sensor

**Responsible role:** L2_support

**Instruction:**
Connect the 4-pin M8 connector to the tote detect sensor.

**Expected result:**
The 4-pin M8 connector is connected to the tote detect sensor.

**Stop or Escalate If:**

* Any connector label or destination does not match the documented connection point.
* The 4-pin M8 connector cannot be connected to the tote detect sensor.

---

### Step 8 — Connect LONG-labeled M8 connector

**Responsible role:** L2_support

**Instruction:**
Connect the 3-pin M8 connector labeled "LONG" to the longer gripper sensor.

**Expected result:**
The 3-pin M8 connector labeled "LONG" is connected to the longer gripper sensor.

**Stop or Escalate If:**

* Any connector label or destination does not match the documented connection point.
* The 3-pin M8 connector labeled LONG cannot be connected to the longer gripper sensor.

---

### Step 9 — Connect SHORT-labeled M8 connector

**Responsible role:** L2_support

**Instruction:**
Connect the 3-pin M8 connector labeled "SHORT" to the shorter gripper sensor.

**Expected result:**
The 3-pin M8 connector labeled "SHORT" is connected to the shorter gripper sensor.

**Stop or Escalate If:**

* Any connector label or destination does not match the documented connection point.
* The 3-pin M8 connector labeled SHORT cannot be connected to the shorter gripper sensor.

---

### Step 10 — Install valve cover and protect wiring

**Responsible role:** L2_support

**Instruction:**
Install the valve cover using the four M4x50 socket-head screws, make sure no wires are pinched along the cover edges, and insert the grommet into the notch for the tote sensor wire.

**Expected result:**
Valve cover is installed with four M4x50 socket-head screws, no wires are pinched, and the grommet is inserted into the tote sensor wire notch.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Valve cover area, screw locations, and grommet placement at the tote sensor wire notch.*


**Stop or Escalate If:**

* The valve cover would pinch wires.
* The grommet cannot be inserted into the tote sensor wire notch.
* The valve cover cannot be installed with the four M4x50 socket-head screws as documented.

---

### Step 11 — Reinstall side panels if needed

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Any removed top and/or bottom side panels are reinstalled.

**Stop or Escalate If:**

* Top and/or bottom side panels required for restoration cannot be reinstalled.

---

### Step 12 — Restart operator station using referenced procedure

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced startup procedure on page 66.

**Expected result:**
Operator station restart is initiated using the referenced startup procedure.

**Stop or Escalate If:**

* The referenced startup procedure on page 66 is unavailable.
* The operator station cannot be restarted using the referenced procedure.

---

## Success Criteria

* The new Tip or A-axis cable is installed and connected to the A-axis PCA.
* The cable is routed around the gearbox and through the cable carrier as documented.
* Cross bars are closed and dividers are between the cable and air line.
* Cable markings are aligned and the cable is secured with wire ties at the documented locations.
* No wires are dangling near the A-axis PCA.
* All four M8 connectors are routed through the grommet and connected to the documented components.
* The valve cover is installed with four M4x50 socket-head screws without pinched wires and with the grommet inserted into the tote sensor wire notch.
* Any necessary side panels are reinstalled.
* The operator station is restarted using the referenced startup procedure.

## Failure Conditions

* Wires cannot be routed without dangling near the A-axis PCA.
* The cable cannot be secured as documented.
* Dividers cannot be positioned between the cable and air line.
* Any connector label or destination does not match the documented connection points.
* The valve cover would pinch wires.
* The grommet cannot be inserted into the tote sensor wire notch.
* Required panels cannot be reinstalled.
* The operator station cannot be restarted using the referenced procedure.

## Escalation Guidance

* Escalate if cable routing near the A-axis PCA, gearbox, or cable carrier cannot be completed as documented.
* Escalate if divider placement between the cable and air line cannot be maintained.
* Escalate if any connector label or destination does not match the documented connection points.
* Escalate if the valve cover installation would pinch wires or the grommet cannot be seated in the tote sensor wire notch.
* Escalate if the referenced startup procedure on page 66 is needed but unavailable.

## Missing Details / Known Gaps

* The packet does not provide the full installation section text beyond the summarized candidate content.
* The source packet does not provide an explicit estimated time for the installation subsection.
* The source packet does not explicitly state whether production stop is required for this installation subsection.
* The source packet does not explicitly state whether LOTO is required for this installation subsection.
* The restart procedure is only referenced to page 66 and is not reproduced in this packet.
* No explicit torque values are provided in this packet for the four M4x50 socket-head screws.

## Source Lineage

- Candidate IDs: candidate_l2_install_tip_or_a_axis_cable
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
