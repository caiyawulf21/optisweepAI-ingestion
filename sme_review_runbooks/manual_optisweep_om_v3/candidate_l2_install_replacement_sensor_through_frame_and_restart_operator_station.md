# Install Replacement Sensor Through Frame And Restart Operator Station

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_install_replacement_sensor_through_frame_and_restart_operator_station_v1` |
| Title | Install Replacement Sensor Through Frame And Restart Operator Station |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Reconnect and secure a replacement sensor after it has already been routed through the frame, reinstall retained hardware and grommets, and then restart the operator station using the separately referenced startup procedure.

## When To Use

Use this procedure for the installation portion of a replacement sensor task after the replacement sensor has already been routed through the frame and the remaining documented actions are to reconnect, secure, restore removed grommets, and restart the operator station.

## Do Not Use For

* Do not use this runbook for the earlier sensor removal or routing steps; this excerpt begins after routing has already occurred.
* Do not use this runbook as the full operator station startup procedure; the source directs the user to the separate procedure "Starting The Operator Station" on page 66.
* Do not use this runbook as a complete safety/setup procedure because the excerpt does not contain the full safety context for component replacement work.

## Safety And Operational Notes

* This is component replacement work and the full safety/setup context is not contained in this excerpt.
* Use the separate referenced procedure for restarting the operator station; this section does not provide those steps.

## Access Or Tools Needed

* Access to the routed replacement sensor
* Access to the M8 connection
* Access to the M3 button-head screw
* Access to any removed grommets
* Operator station restart procedure on page 66

## Procedure Steps

### Step 1 — Verify sensor routing is complete

**Responsible role:** L2_support

**Instruction:**
Verify the replacement sensor has already been routed through the frame before continuing with installation.

**Expected result:**
The replacement sensor is confirmed to be routed through the frame and ready for reconnection and securing.

**Stop or Escalate If:**

* Stop if the replacement sensor has not already been routed through the frame.
* Escalate if prior removal or routing steps are needed, because they are not provided in this excerpt.

---

### Step 2 — Connect the M8 connection

**Responsible role:** L2_support

**Instruction:**
Connect the M8 connection for the replacement sensor.

**Expected result:**
The M8 connection is connected.

**Screens / Images:**

![artifact_fig_7_3_a_axis_pca_connections](assets/artifact_fig_7_3_a_axis_pca_connections.jpeg)

*A-axis sensor PCA connection locations relevant to sensor installation and reconnection.*

![artifact_fig_7_2_z_axis_clink_connections](assets/artifact_fig_7_2_z_axis_clink_connections.jpeg)

*Z-axis sensor wiring connection diagram if the replacement sensor is a Z-axis sensor installation.*


**Stop or Escalate If:**

* Stop if the M8 connection cannot be positively identified from the current source context.
* Escalate if the connection does not match the expected installation point or cannot be secured.

---

### Step 3 — Reinstall the M3 button-head screw

**Responsible role:** L2_support

**Instruction:**
Re-install the M3 button-head screw.

**Expected result:**
The replacement sensor is secured with the M3 button-head screw.

**Screens / Images:**

![artifact_fig_7_3_a_axis_pca_connections](assets/artifact_fig_7_3_a_axis_pca_connections.jpeg)

*Maintenance diagram for the A-axis sensor PCA connections used during sensor installation, referenced as image support for reinstalling and securing the sensor.*


**Stop or Escalate If:**

* Stop if the M3 button-head screw is unavailable or cannot be reinstalled.
* Escalate if the sensor cannot be secured after reinstalling the screw.

---

### Step 4 — Reinstall removed grommets

**Responsible role:** L2_support

**Instruction:**
Re-install any removed grommets.

**Expected result:**
Any grommets removed during the preceding work are reinstalled.

**Screens / Images:**

![artifact_fig_7_2_z_axis_clink_connections](assets/artifact_fig_7_2_z_axis_clink_connections.jpeg)

*Lower grommet routing context for Z-axis sensor installation, if applicable to the replaced sensor.*


**Stop or Escalate If:**

* Stop if removed grommets cannot be identified or reinstalled.
* Escalate if the installation cannot be restored to its prior routed/grommet condition.

---

### Step 5 — Restart the operator station

**Responsible role:** L2_support

**Instruction:**
Re-start the operator station using the referenced procedure "Starting The Operator Station" on page 66.

**Expected result:**
The operator station is restarted by following the separate startup procedure.

**Screens / Images:**

![artifact_page_82_image_2](assets/artifact_page_82_image_2.jpeg)

*System/operator station screen context associated with stopping and startup procedures for the operator station.*


**Stop or Escalate If:**

* Stop if the separate procedure "Starting The Operator Station" is not available.
* Escalate if operator station restart requires steps not contained in this excerpt and the referenced procedure cannot be followed.

---

## Success Criteria

* The replacement sensor is connected.
* The M3 button-head screw is reinstalled and the sensor is secured.
* Any removed grommets are reinstalled.
* The operator station is restarted using the referenced startup procedure.

## Failure Conditions

* The replacement sensor has not been routed through the frame before beginning this excerpted installation.
* The M8 connection cannot be connected.
* The M3 button-head screw cannot be reinstalled or the sensor remains unsecured.
* Removed grommets are not reinstalled.
* The operator station restart procedure is unavailable or not followed.

## Escalation Guidance

* Escalate when prior removal or routing steps are required, because this excerpt begins mid-procedure.
* Escalate when the separate operator station startup procedure is needed but not available in the current work context.
* Escalate if the sensor cannot be connected or secured with the documented hardware.
* Escalate if full safety/setup context is required for the component replacement task, because it is not contained in this excerpt.

## Missing Details / Known Gaps

* The source excerpt text for page 109 is not present in the packet; step wording is derived from the candidate and attached evidence only.
* The excerpt does not provide the detailed restart steps for "Starting The Operator Station"; it only references that separate procedure.
* The excerpt does not provide complete safety controls, production stop requirements, or LOTO requirements for this installation segment.
* The source does not specify whether this installation segment applies to a specific sensor axis in every case; attached figures provide A-axis and Z-axis context only.
* No commands are provided in the source packet for this procedure.

## Source Lineage

- Candidate IDs: candidate_l2_install_replacement_sensor_through_frame_and_restart_operator_station
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
