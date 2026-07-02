# Perform Full Replacement Of The Z-Axis Cable Carrier

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_perform_full_replacement_of_the_z_axis_cable_carrier_v1` |
| Title | Perform Full Replacement Of The Z-Axis Cable Carrier |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | `operator` |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Replace the Z-axis cable carrier while retaining the existing air line and FFC, then verify the carrier is correctly reinstalled and restart the operator station.

## When To Use

Use when performing the documented full replacement of the Z-axis cable carrier on the tipper, while preserving and reinstalling the existing air line and flat-flex cable (FFC), followed by inspection and operator station restart.

## Do Not Use For

* Do not use for general operator execution.
* Do not use if lockout/tagout cannot be completed using the referenced Operator Station Lockout/Tagout procedure.
* Do not continue if the FFC clamps cannot remain identifiable or cannot be realigned to the earlier marks.
* Do not use as a procedure for replacing the air line or FFC themselves; this source-specific procedure preserves and reinstalls the existing air line and FFC.

## Safety And Operational Notes

* This procedure includes lockout/tagout and component replacement.
* The procedure is not support-safe for general operator execution.
* Stop if lockout/tagout cannot be completed using the referenced procedure.
* Stop if dividers press on the FFC, cross bars do not close, joints are not fully seated, or the carrier does not appear uniform end to end.

## Access Or Tools Needed

* Access to the tipper
* Operator Station Lockout/Tagout procedure
* 3/8-in. wrench or socket
* Marker or tape
* Tooling to remove and install M3 socket-head screws
* Tooling to remove and install M3 flat-head fasteners
* Wire ties
* Replacement cable carrier
* Access to the station side panel and cable carrier ends
* Starting The Operator Station procedure

## Procedure Steps

### Step 1 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the referenced Operator Station Lockout/Tagout procedure.

**Expected result:**
The tipper is locked out and tagged out per the referenced procedure.

**Stop or Escalate If:**

* Lockout/tagout cannot be completed using the referenced procedure.

---

### Step 2 — Remove the station side panel if needed

**Responsible role:** L2_support

**Instruction:**
If necessary, use a 3/8-in. wrench or socket to remove the nine self-tapping screws securing the side panel, then remove the station side panel to access the motor.

**Expected result:**
The side panel is removed when needed and access to the service area is available.

**Screens / Images:**

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Maintenance diagram context for side-panel access and routing area during tipper service.*

![artifact_fig_7_15_tip_cable](assets/artifact_fig_7_15_tip_cable.png)

*Related maintenance figure showing side-panel removal context during cable service.*


**Stop or Escalate If:**

* The side panel cannot be removed as needed to access the service area.

---

### Step 3 — Mark the air line and FFC positions

**Responsible role:** L2_support

**Instruction:**
Mark the air line and FFC at both ends where they enter and exit the cable carrier using a marker or tape.

**Expected result:**
Reference marks are present at both ends for the air line and FFC.

**Screens / Images:**

![artifact_page_166_image_2](assets/artifact_page_166_image_2.jpeg)

*Related cable carrier service context for marking where the cable enters the carrier on both ends.*


**Stop or Escalate If:**

* The air line and FFC positions cannot be clearly marked or preserved for reinstallation.

---

### Step 4 — Document and release the air line ties

**Responsible role:** L2_support

**Instruction:**
Note how the air line is tied to the cable carrier and cut the wire ties.

**Expected result:**
The air line tie arrangement has been noted and the wire ties have been removed.

**Screens / Images:**

![artifact_page_166_image_2](assets/artifact_page_166_image_2.jpeg)

*Related cable carrier service context showing documentation and cutting of cable ties at both ends.*


**Stop or Escalate If:**

* The original tie arrangement cannot be determined well enough to restore the air line position.

---

### Step 5 — Remove the FFC clamp screws

**Responsible role:** L2_support

**Instruction:**
At both ends of the cable carrier, remove the M3 socket-head screws holding the FFC clamps in place. Keep the clamps on the FFC if possible.

**Expected result:**
The FFC clamps are released from both ends of the cable carrier.

**Screens / Images:**

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*FFC clamp hardware and M3 socket-head screw context.*


**Stop or Escalate If:**

* The FFC clamps do not remain identifiable or cannot be realigned to the earlier marks.

---

### Step 6 — Detach the old cable carrier from both ends

**Responsible role:** L2_support

**Instruction:**
Detach the cable carrier by removing the four M3 screws at both ends of the cable carrier.

**Expected result:**
The cable carrier is detached from both ends.

**Stop or Escalate If:**

* The cable carrier cannot be detached from both ends.

---

### Step 7 — Remove the old cable carrier from the air line and FFC

**Responsible role:** L2_support

**Instruction:**
Open all cross bars on the outside of the cable carrier and remove the carrier from the FFC and air line; one end of the cable carrier may need to be snapped off to fully remove it.

**Expected result:**
The old cable carrier is removed from the retained air line and FFC.

**Screens / Images:**

![artifact_page_166_image_2](assets/artifact_page_166_image_2.jpeg)

*Related cable carrier context for opening snap-open cross bars during removal.*


**Stop or Escalate If:**

* The old carrier cannot be removed without losing control of the retained air line or FFC routing.

---

### Step 8 — Prepare the new cable carrier

**Responsible role:** L2_support

**Instruction:**
Open all cross bars on the new cable carrier and probably one end.

**Expected result:**
The new cable carrier is open and ready for installation around the retained components.

**Stop or Escalate If:**

* The new cable carrier cannot be opened or prepared for installation.

---

### Step 9 — Position the new carrier and dividers

**Responsible role:** L2_support

**Instruction:**
Put the new cable carrier roughly in place while positioning the internal dividers all the way to one side, against the air line.

**Expected result:**
The new carrier is roughly positioned and the dividers are set against the air line side.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Related installation context showing cable carrier routing and divider placement between cable and air line.*


**Stop or Escalate If:**

* The dividers cannot be positioned to keep separation between the air line and FFC.

---

### Step 10 — Close the carrier and verify divider clearance

**Responsible role:** L2_support

**Instruction:**
Snap all cross bars closed, ensuring none of the dividers are pressing on the FFC, and snap the end back on if necessary.

**Expected result:**
The carrier is closed and the FFC is not being pressed by the dividers.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Related installation context for closing cross bars and maintaining divider separation between cable and air line.*


**Stop or Escalate If:**

* Dividers press on the FFC.
* Cross bars do not close.
* The carrier end cannot be restored as needed.

---

### Step 11 — Mount both ends of the new cable carrier

**Responsible role:** L2_support

**Instruction:**
Mount both ends using four M3 flat-head fasteners.

**Expected result:**
Both ends of the new cable carrier are mounted.

**Stop or Escalate If:**

* The carrier cannot be secured at both ends.

---

### Step 12 — Reattach the FFC clamps to the new carrier

**Responsible role:** L2_support

**Instruction:**
Attach the FFC clamps using the M3 socket-head screws at both cable carrier ends, ensuring the FFC clamps align with the marks made earlier.

**Expected result:**
The FFC clamps are reattached and aligned to the earlier marks.

**Screens / Images:**

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*FFC clamp hardware and M3 socket-head screw context for clamp reattachment.*


**Stop or Escalate If:**

* The FFC clamps do not remain identifiable or cannot be realigned to the earlier marks.

---

### Step 13 — Reposition and tie the air line

**Responsible role:** L2_support

**Instruction:**
Position the air line in the cable carrier using the earlier marks and wire tie it in place.

**Expected result:**
The air line is positioned according to the earlier marks and secured with wire ties.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Related installation context for securing retained components with wire ties at cable carrier ends.*


**Stop or Escalate If:**

* The air line cannot be restored to the earlier marked position.
* The air line cannot be secured in place.

---

### Step 14 — Inspect the installed cable carrier

**Responsible role:** L2_support

**Instruction:**
Inspect the cable carrier to ensure all cross bars are closed, the dividers are not pressing on the FFC, and all cable carrier joints are fully seated; the cable carrier should look uniform end to end.

**Expected result:**
The installed cable carrier passes visual inspection.

**Screens / Images:**

![artifact_page_167_image_2](assets/artifact_page_167_image_2.jpeg)

*Related installation context for cross-bar closure and internal separation of cable and air line.*


**Stop or Escalate If:**

* Dividers press on the FFC.
* Cross bars do not close.
* Joints are not fully seated.
* The carrier does not appear uniform end to end.

---

### Step 15 — Reinstall side panels if needed

**Responsible role:** L2_support

**Instruction:**
Reinstall the top and/or bottom side panels, if necessary.

**Expected result:**
Any removed side panels are reinstalled.

**Stop or Escalate If:**

* Required panels cannot be reinstalled.

---

### Step 16 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Restart the operator station using the referenced Starting The Operator Station procedure.

**Expected result:**
The operator station is restarted per the referenced procedure.

**Stop or Escalate If:**

* The operator station cannot be restarted using the referenced procedure.

---

## Success Criteria

* The new Z-axis cable carrier is installed.
* The existing air line and FFC are correctly positioned using the earlier marks.
* FFC clamps are reattached and aligned to the earlier marks.
* All cross bars are closed.
* Dividers are not pressing on the FFC.
* All cable carrier joints are fully seated.
* The cable carrier looks uniform end to end.
* Panels are reinstalled as needed.
* The operator station is restarted using the referenced procedure.

## Failure Conditions

* LOTO cannot be completed using the referenced procedure.
* The FFC clamps do not remain identifiable or cannot be realigned to the earlier marks.
* Dividers press on the FFC.
* Cross bars do not close.
* Cable carrier joints are not fully seated.
* The cable carrier does not appear uniform end to end.
* Required panels cannot be reinstalled.
* The operator station cannot be restarted using the referenced procedure.

## Escalation Guidance

* Stop and escalate if lockout/tagout cannot be completed using the referenced Operator Station Lockout/Tagout procedure.
* Stop and escalate if the FFC clamps cannot remain identifiable or cannot be realigned to the earlier marks.
* Stop and escalate if dividers press on the FFC, cross bars do not close, joints are not fully seated, or the carrier does not appear uniform end to end.
* Escalate to appropriate maintenance/engineering support if the new cable carrier cannot be mounted or restored to a uniform installed condition.

## Missing Details / Known Gaps

* The packet does not provide the full verbatim source text for section 7.3.16.3, so step wording is finalized from the candidate and packet evidence only.
* No estimated time is provided in the packet for this specific procedure.
* No explicit PPE list is provided in the packet for this specific procedure.
* No explicit torque values or fastener torque requirements are provided in the packet.
* No explicit post-restart functional test is provided in the packet beyond restarting the operator station.
* The packet does not identify a source-specific figure dedicated to the Z-axis cable carrier full replacement; attached artifacts are related contextual visuals from the same source bundle.

## Source Lineage

- Candidate IDs: candidate_l2_full_replace_z_axis_cable_carrier
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
