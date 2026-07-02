# Remove a limit or home sensor

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_a_limit_or_home_sensor_v1` |
| Title | Remove a limit or home sensor |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Safely remove a limit or home sensor from the tipper by identifying the sensor and axis, applying lockout/tagout, disconnecting the sensor from the correct connection point, removing the retaining screw, and freeing the routed cable for replacement.

## When To Use

Use this procedure when a limit sensor or home sensor on the tipper must be removed as part of replacement service.

## Do Not Use For

* Installing a new limit or home sensor; the provided source packet only covers removal guidance.
* Determining exact sensor physical location; the candidate notes that location details are referenced on the previous page and are not included in this section.
* Recovering from cable routing problems or wire-tie constraints beyond the described removal actions.

## Safety And Operational Notes

* Use LOTO before performing the removal.
* Wear safety glasses and gloves.
* Access may be required near the A-axis motor or inside the control box depending on sensor axis.

## Access Or Tools Needed

* LOTO access for the tipper
* Replacement part: limit sensor or home sensor
* PPE: safety glasses
* PPE: gloves
* 1.5-mm hex wrench
* Tool to cut wire ties
* Wire ties
* Access to PCA near the A-axis motor for A-axis sensors
* Access to the CLINK controller inside the control box for Z-axis sensors

## Procedure Steps

### Step 1 — Gather required PPE, tools, and replacement part

**Responsible role:** L2_support

**Instruction:**
Gather the replacement limit sensor or home sensor, safety glasses, gloves, a 1.5-mm hex wrench, a tool to cut wire ties, and wire ties before starting the removal procedure.

**Expected result:**
All required PPE, tools, and materials are available at the work area.

**Stop or Escalate If:**

* Required PPE is unavailable.
* Required tools or replacement part are unavailable.

---

### Step 2 — Identify sensor type and axis

**Responsible role:** L2_support

**Instruction:**
Identify whether the sensor is a home sensor or limit sensor and whether it is on the A-axis or Z-axis. Use the source distinctions that home sensors are normally open (NO), limit sensors are normally closed (NC), Z-axis sensors have long cables greater than 6 ft, and A-axis sensors have shorter cables less than 2 ft.

**Expected result:**
The technician knows the sensor type and axis and can proceed to the correct connection point.

**Stop or Escalate If:**

* The sensor type cannot be determined.
* The axis cannot be determined.
* The technician cannot confirm the correct connection point from the available source.

---

### Step 3 — Lock out and tag out the tipper

**Responsible role:** L2_support

**Instruction:**
LOTO the tipper using the manual's Operator Station Lockout/Tagout procedure before disconnecting or removing the sensor.

**Expected result:**
The tipper is in a lockout/tagout state and safe for maintenance work.

**Stop or Escalate If:**

* LOTO cannot be applied.
* Any removal work would proceed without LOTO.

---

### Step 4 — Unplug the sensor from the correct connection point

**Responsible role:** L2_support

**Instruction:**
Unplug the sensor from its connection point. For an A-axis sensor, unplug it from the printed circuit assembly (PCA) near the A-axis motor. For a Z-axis sensor, unplug it from the CLINK controller inside the control box.

**Expected result:**
The sensor cable is electrically disconnected from the machine.

**Screens / Images:**

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Tip PCA area relevant to the A-axis sensor connection point.*

![artifact_fig_7_13_clink_controller](assets/artifact_fig_7_13_clink_controller.png)

*CLINK controller location inside the control box for the Z-axis sensor connection point.*


**Stop or Escalate If:**

* The correct connection point cannot be identified.
* The connection point cannot be accessed.
* Disconnecting the sensor would require steps not described in the source.

---

### Step 5 — Remove the retaining screw

**Responsible role:** L2_support

**Instruction:**
Remove the M3 button-head screw holding the sensor in place.

**Expected result:**
The sensor is no longer mechanically fastened at its mounting point.

**Screens / Images:**

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*Only limited related clamp and small-hardware context is available from this packet; use cautiously as supplemental visual context, not as direct sensor-specific evidence.*


**Stop or Escalate If:**

* The M3 button-head screw cannot be removed.
* The mounting arrangement does not match the source description.

---

### Step 6 — Feed the sensor through the routing hole during removal

**Responsible role:** L2_support

**Instruction:**
Feed the sensor through the hole used for the wire routing as it is removed.

**Expected result:**
The sensor body and cable are moving out through the routing hole.

**Screens / Images:**

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Cable routing path context that may help verify the withdrawal path.*

![artifact_fig_7_15_tip_cable](assets/artifact_fig_7_15_tip_cable.png)

*General tip or A-axis cable context that may help identify the routed cable path.*


**Stop or Escalate If:**

* The cable cannot be freed because of routing constraints beyond what is described.
* The cable binds and the source provides no additional recovery detail.

---

### Step 7 — Pull the sensor from the column for Z-axis removal

**Responsible role:** L2_support

**Instruction:**
For a Z-axis sensor, pull the sensor from the column.

**Expected result:**
The Z-axis sensor is removed from the column.

**Stop or Escalate If:**

* The Z-axis sensor does not withdraw from the column.
* Additional obstruction or routing detail is encountered that is not covered by the source.

---

### Step 8 — Free and remove the A-axis sensor cable

**Responsible role:** L2_support

**Instruction:**
For an A-axis sensor, pull the defective sensor away. Cut the wire tie if needed to free the cable.

**Expected result:**
The A-axis sensor and cable are freed from the machine routing path.

**Screens / Images:**

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*A-axis cable routing context that may help identify where the cable is tied or routed.*

![artifact_fig_7_18_tip_pca](assets/artifact_fig_7_18_tip_pca.png)

*Tip PCA area associated with the A-axis sensor cable connection.*


**Stop or Escalate If:**

* The cable cannot be freed after cutting the accessible wire tie described by the source.
* Routing or restraints beyond the described wire tie prevent removal.

---

### Step 9 — Optionally use the old sensor to guide the new cable path

**Responsible role:** L2_support

**Instruction:**
If helpful during replacement, connect the new sensor to the one being replaced before pulling through the cable routing so the new cable follows the same path.

**Expected result:**
If used, the old sensor helps guide the new sensor cable through the same routing path.

**Screens / Images:**

![artifact_fig_7_16_tip_cable_routing](assets/artifact_fig_7_16_tip_cable_routing.png)

*Routing context for following the same cable path during replacement.*


**Stop or Escalate If:**

* The routing path cannot be preserved using the described guidance.
* Replacement requires additional installation detail not present in the source.

---

## Success Criteria

* The limit or home sensor is disconnected from the correct connection point.
* The M3 button-head retaining screw is removed.
* The sensor and cable are removed from the mounting and routing path.
* For A-axis removal, any needed wire tie has been cut to free the cable.
* For Z-axis removal, the sensor has been pulled from the column.

## Failure Conditions

* LOTO is not applied before removal work.
* Sensor type or axis cannot be identified from the available source information.
* The correct connection point cannot be identified or accessed.
* The M3 button-head screw cannot be removed.
* The cable cannot be freed because of routing or wire ties beyond what is described in the source.

## Escalation Guidance

* Stop if LOTO cannot be applied and do not continue removal.
* Escalate for SME review if the sensor type, axis, or exact location cannot be confirmed from the available source.
* Escalate if cable routing or wire ties prevent removal beyond the limited recovery detail provided in the source.
* Escalate if the mounting arrangement or connection point does not match the source description.

## Missing Details / Known Gaps

* The source packet does not provide the actual OCR text for page 106 section 7.3.2.1; this runbook relies on the candidate extraction and attached packet artifacts.
* The source packet does not provide exact physical sensor location details; the candidate notes these are on the previous page and not included here.
* The source packet does not provide installation steps for the replacement sensor.
* The source packet does not provide estimated time for this specific sensor removal procedure.
* The source packet does not provide additional recovery steps if cable routing or wire ties prevent removal.

## Source Lineage

- Candidate IDs: replace_limit_or_home_sensor_removal
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
