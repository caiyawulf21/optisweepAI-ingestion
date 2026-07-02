# Remove a Robot From the Robot Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_remove_a_robot_from_the_robot_selection_screen_v1` |
| Title | Remove a Robot From the Robot Selection Screen |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection screen in the web application or Geek Plus RMS view to remove a robot by entering or selecting its robot ID, clicking Remove, and confirming the system reports successful removal.

## When To Use

Use this procedure when support personnel need to remove a robot from the Robot Selection screen in the web application or Geek Plus RMS view during troubleshooting or support-related robot management, using an OT-network-connected device or authorized remote access as described in the source.

## Do Not Use For

* Do not use this procedure to decide whether a robot should be removed; the source states debug scenarios and when to remove the robot are covered later and are not included in this segment.

## Safety And Operational Notes

* Use only authorized access to the web application or Geek Plus RMS view.
* The source does not provide approval criteria for when a robot should be removed; do not infer removal conditions from this segment alone.

## Access Or Tools Needed

* Access to the web application or Geek Plus RMS view
* Device connected to the OT network or authorized remote access through UPS VPN and Z Scaler
* Robot ID for the robot being removed

## Related Operational Context

* ctx_training_video_robot_selection_add_remove_v1
* ctx_training_video_robot_id_entry_reference_v1
* ctx_training_video_rms_access_otnet_v1
* ctx_training_video_remote_access_vpn_zscaler_v1
* ctx_training_video_hmi_station_availability_v1

## Procedure Steps

### Step 1 — Open the Robot Selection screen

**Responsible role:** L1_support

**Instruction:**
Open the web application or Geek Plus RMS view that shows the Robot Selection screen. Use a device on the OT network, or authorized remote access if available according to the source.

**Expected result:**
The Robot Selection screen is available for use.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Robot Selection screen in the web application / RMS view.*


**Stop or Escalate If:**

* Stop or escalate if access to the OT-network-hosted application is unavailable and no authorized remote access is available.

---

### Step 2 — Locate the Remove Robot area

**Responsible role:** L1_support

**Instruction:**
Locate the Remove Robot section on the Robot Selection screen.

**Expected result:**
The Remove Robot field and Remove button are visible.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Screen view showing the Robot Selection area with the Remove Robot field and Remove button.*


**Stop or Escalate If:**

* Stop or escalate if the Robot Selection screen does not show the Remove Robot controls.

---

### Step 3 — Enter or select the robot

**Responsible role:** L1_support

**Instruction:**
Enter the corresponding robot ID or select the robot in the Remove Robot area.

**Expected result:**
The intended robot is selected in the Remove Robot workflow.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Robot ID entry area and robot selection behavior in the Remove Robot section.*


**Stop or Escalate If:**

* Stop or escalate if the correct robot cannot be identified or selected.

---

### Step 4 — Click Remove

**Responsible role:** L1_support

**Instruction:**
Click "Remove."

**Expected result:**
The system processes the removal request.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Remove button in the Remove Robot section.*


**Stop or Escalate If:**

* Stop or escalate if the Remove action is unavailable or does not execute.

---

### Step 5 — Verify successful removal

**Responsible role:** L1_support

**Instruction:**
Verify that the system shows the removal was successful.

**Expected result:**
The system displays a successful removal confirmation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Success confirmation associated with the Remove Robot action.*


**Stop or Escalate If:**

* Escalate if the system does not show that removal was successful.

---

### Step 6 — Use robot ID field matching behavior if needed

**Responsible role:** L1_support

**Instruction:**
If needed, use the robot ID field behavior described in training to find an already introduced robot by typing identifying digits and selecting a matching result when shown.

**Expected result:**
A matching robot appears for selection when the field returns existing robot matches.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Robot field used for ID entry and matching robot selection behavior.*


**Stop or Escalate If:**

* Stop or escalate if matching results do not allow confident identification of the intended robot.

---

## Success Criteria

* The intended robot is entered or selected in the Remove Robot area.
* The Remove action is executed from the Robot Selection screen.
* The system shows that the removal was successful.

## Failure Conditions

* The web application or RMS view cannot be accessed.
* The Remove Robot section is not available.
* The correct robot cannot be identified or selected.
* The system does not show that removal was successful.

## Escalation Guidance

* Escalate if the system does not show that removal was successful.
* Escalate if access to the application or Robot Selection screen is unavailable.
* Escalate if the correct robot cannot be confidently identified for removal.
* Do not escalate based on inferred removal criteria from this segment; the source says when to remove the robot is covered later.

## Missing Details / Known Gaps

* The source segment does not define approval criteria or decision logic for when a robot should be removed.
* The source does not provide a time estimate for completing this procedure.
* The source does not specify whether production must be stopped before performing this action.
* The source does not specify LOTO requirements for this action.
* The source does not provide exact wording or location of the success message beyond stating that the system shows removal was successful.

## Source Lineage

- Candidate IDs: candidate_training_video_remove_robot_from_robot_selection
- Source ID: `training_video_day1`
- Source Type: `training_video`
