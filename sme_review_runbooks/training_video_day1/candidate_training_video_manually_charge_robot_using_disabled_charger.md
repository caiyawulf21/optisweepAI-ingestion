# Reserve A Charger And Manually Push A Robot Into It For Charging

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reserve_a_charger_and_manually_push_a_robot_into_it_for_charging_v1` |
| Title | Reserve A Charger And Manually Push A Robot Into It For Charging |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Charger Selection function to reserve a charger for a specific robot by disabling that charger so no other robot is sent there, manually push the desired AGV into the charging station, allow it to charge, and then return the charger to normal enabled use.

## When To Use

Use when a charger is needed to manually charge a specific robot and you must prevent other robots from being sent to that charging station while the robot is being manually placed there.

## Do Not Use For

* Do not use this procedure if you cannot restore the charger to enabled or on state after manual charging.
* Do not use this procedure as a way to leave a charger disabled or off during normal operation, especially at sites with limited charger count.

## Safety And Operational Notes

* Use physical access to the charging station and robot only as supported by site practice; the source confirms manual pushing of the AGV but does not provide detailed physical handling precautions.
* Do not leave the charger disabled or off after manual charging.
* At sites with limited charger count, leaving one charger off or not re-enabled reduces available charging capacity and can significantly lengthen charging time.

## Access Or Tools Needed

* Access to the Charger Selection screen
* Permission to disable and re-enable a charger
* Physical access to the charging station and robot

## Related Operational Context

* ctx_training_video_manual_charging_with_disabled_charger_v1
* ctx_training_video_charger_selection_screen_reference_v1
* ctx_training_video_charger_availability_site_capacity_v1

## Procedure Steps

### Step 1 — Open Charger Selection and select the charger

**Responsible role:** L1_support

**Instruction:**
Open the Charger Selection interface and select the charger you intend to use for manual charging so you can view its charger information.

**Expected result:**
The selected charger is displayed in Charger Selection with charger information available for review.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Charger Selection slide text indicating charger selection and viewing charger information.*


**Stop or Escalate If:**

* Escalate if the Charger Selection interface is not available.
* Escalate if the intended charger cannot be selected or charger information cannot be viewed.

---

### Step 2 — Disable the selected charger

**Responsible role:** L1_support

**Instruction:**
Disable the selected charger so no other robot is sent to that charging station.

**Expected result:**
The charger is reserved for manual charging use and other robots are not sent to that station.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Slide text stating that the charger can be disabled so no other robot is sent to that charging station.*


**Stop or Escalate If:**

* Escalate if the charger cannot be disabled.
* Stop if the system still appears able to send other robots to the selected charger.

---

### Step 3 — Manually push the desired AGV into the disabled charging station

**Responsible role:** L1_support

**Instruction:**
Manually push the desired AGV into the disabled charging station.

**Expected result:**
The intended AGV is positioned in the reserved charging station.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Slide text stating that the desired AGV can then be pushed into the disabled charging station.*


**Stop or Escalate If:**

* Escalate if the desired AGV cannot be manually pushed into the charging station.
* Escalate if the charger cannot be used for the manual charging setup described in the source.

---

### Step 4 — Allow the robot to charge manually

**Responsible role:** L1_support

**Instruction:**
Allow the robot to charge manually at that station.

**Expected result:**
The robot receives charge while positioned in the reserved charger.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Discussion describing manual charging and the need to return the charger to normal use afterward.*


**Stop or Escalate If:**

* Escalate if the robot cannot be charged manually as described.
* Escalate if the robot does not appear to recover charge.

---

### Step 5 — Re-enable or turn the charger back on after removing the robot

**Responsible role:** L1_support

**Instruction:**
After removing the robot, turn the charger back on or re-enable it so the charger returns to normal system use.

**Expected result:**
The charger is restored to normal availability for system-assigned charging.

**Screens / Images:**

![artifact_training_video_training_video_day1_0050_and_i_think_under_20_it_primary_01_53_04_000](assets/fe40e8a3c226304c.jpg)

*Discussion noting that operators should turn the charger back on or re-enable it after use so charger capacity is not reduced.*


**Stop or Escalate If:**

* Escalate if the charger cannot be turned back on or re-enabled.
* Stop and escalate if the charger remains unavailable after the robot is removed.

---

## Success Criteria

* The selected charger is reserved so no other robot is sent there during setup.
* The desired AGV is manually placed into the charging station.
* The robot is manually charged at the station.
* The charger is restored to enabled or on state after the robot is removed.

## Failure Conditions

* The charger cannot be selected or charger information cannot be viewed.
* The charger cannot be disabled as described.
* Other robots may still be sent to the charger after it is disabled.
* The desired AGV cannot be manually placed into the charging station.
* The robot does not charge manually as expected.
* The charger cannot be re-enabled or turned back on after use.
* The charger is left disabled or off, reducing available charging capacity.

## Escalation Guidance

* Escalate if the charger cannot be disabled, re-enabled, or used as described in the source.
* Escalate if the desired AGV cannot be manually pushed into the disabled charging station.
* Escalate if the robot does not recover charge as expected.
* Escalate immediately if the charger cannot be returned to normal use after manual charging.

## Missing Details / Known Gaps

* The source does not provide exact button labels or click paths for disabling or re-enabling the charger.
* The source does not provide a precise confirmation indicator showing successful charger disablement or re-enablement.
* The source does not provide detailed physical handling instructions for pushing the AGV.
* The source does not provide a defined charging duration or target battery threshold for ending manual charging in this procedure.
* The source notes uncertainty about whether the robot must be on to charge manually.

## Source Lineage

- Candidate IDs: candidate_training_video_manually_charge_robot_using_disabled_charger
- Source ID: `training_video_day1`
- Source Type: `training_video`
