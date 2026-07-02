# Add a Robot From the Robot Selection Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_add_a_robot_from_the_robot_selection_screen_v1` |
| Title | Add a Robot From the Robot Selection Screen |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Selection screen in the web application or Geek Plus RMS view to add a robot by entering its robot ID, clicking Add, and confirming the system reports the add was successful. The training frames this as a support-oriented action used during troubleshooting.

## When To Use

Use when support personnel need to add a robot from the Robot Selection screen in the web application or Geek Plus RMS view, including troubleshooting situations described in the training.

## Do Not Use For

* Do not use this runbook to decide the correct circumstances for putting a robot back into the system; the source states that the correct way to put it back is covered later.
* Do not assume this procedure provides criteria for when a robot should be added; the source segment primarily shows how to perform the add action.

## Safety And Operational Notes

* Use only authorized access to the web application or Geek Plus RMS view.
* Remote access to the RMS view depends on authorization for UPS VPN through Zscaler.
* The source frames add/remove robot actions as support mechanics used during troubleshooting.

## Access Or Tools Needed

* Access to the web application or Geek Plus RMS view
* Device connected to the OT network or authorized remote access through UPS VPN and Z Scaler
* Robot ID for the robot being added

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
Open the web application or Geek Plus RMS view that shows the Robot Selection screen. Use a device on the OT network, or authorized remote access if available.

**Expected result:**
The Robot Selection screen is visible in the web application or RMS view.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Robot Selection screen in the web application / Geek Plus RMS view.*


**Stop or Escalate If:**

* Stop or escalate if OT network access is unavailable and remote access is not authorized.
* Stop or escalate if the Robot Selection screen cannot be reached.

---

### Step 2 — Locate the Add Robot section

**Responsible role:** L1_support

**Instruction:**
Locate the Add Robot section on the Robot Selection screen, including the robot ID input field and the Add button.

**Expected result:**
The Add Robot input field and Add button are identified on the screen.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Add Robot input field and Add button in the Robot Selection area.*


**Stop or Escalate If:**

* Stop or escalate if the Add Robot controls are not present on the Robot Selection screen.

---

### Step 3 — Enter the robot ID

**Responsible role:** L1_support

**Instruction:**
Enter the corresponding robot ID in the Add Robot field.

**Expected result:**
The target robot ID is entered in the Add Robot field.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Robot ID entry field under the Add Robot section.*


**Stop or Escalate If:**

* Stop or escalate if the correct robot ID is not known.
* Stop or escalate if the field does not accept the robot ID.

---

### Step 4 — Click Add

**Responsible role:** L1_support

**Instruction:**
Click "Add."

**Expected result:**
The system processes the add request for the entered robot ID.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Add button in the Robot Selection Add Robot section.*


**Stop or Escalate If:**

* Stop or escalate if the Add button is unavailable or does not respond.

---

### Step 5 — Verify successful add confirmation

**Responsible role:** L1_support

**Instruction:**
Verify that the system shows the adding was successful.

**Expected result:**
The system displays a successful add confirmation.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Success confirmation associated with the Add Robot action.*


**Stop or Escalate If:**

* Escalate if the system does not show that adding was successful.

---

### Step 6 — Use matching robot lookup if partial entry returns results

**Responsible role:** L1_support

**Instruction:**
If the robot has already been introduced in the system, type identifying ending digits in the robot field and select a matching robot if the system shows matching results.

**Expected result:**
A matching robot can be identified from the field results when partial ending digits are entered.

**Screens / Images:**

![artifact_training_video_training_video_day1_0033_yeah_because_it_has_front_sensors_primary_01_19_57_000](assets/088261e049fd7bf7.jpg)

*Robot field used for ID entry; use it to observe whether matching robot results appear.*


**Stop or Escalate If:**

* Stop or escalate if multiple matches appear and the correct robot cannot be identified.
* Stop or escalate if expected matching results do not appear.

---

## Success Criteria

* The specified robot is added in the web application.
* The system displays a successful add confirmation.

## Failure Conditions

* Robot Selection screen cannot be accessed.
* Add Robot controls are not available.
* The correct robot ID cannot be entered or identified.
* The system does not show that adding was successful.

## Escalation Guidance

* Escalate if the system does not show that adding was successful.
* Escalate if authorized access to the Robot Selection screen is not available.
* Escalate if the correct robot cannot be confidently identified from the robot ID field or matching results.
* Do not infer the correct circumstances for adding a robot back; the source says the correct way to put it back is covered later.

## Missing Details / Known Gaps

* The source does not provide a specific success message text.
* The source does not provide a time estimate for completing the procedure.
* The source does not define whether production must be stopped before performing this action.
* The source does not define LOTO requirements for this action.
* The source does not provide exact navigation steps to reach the Robot Selection screen beyond accessing the web application or RMS view.
* The source does not provide decision criteria for when a robot should be added back; it states that topic is covered later.

## Source Lineage

- Candidate IDs: candidate_training_video_add_robot_from_robot_selection
- Source ID: `training_video_day1`
- Source Type: `training_video`
