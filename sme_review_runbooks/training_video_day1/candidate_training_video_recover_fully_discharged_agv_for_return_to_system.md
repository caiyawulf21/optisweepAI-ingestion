# Recover A Fully Discharged AGV By Manual Charging And Returning It To The System

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_recover_fully_discharged_agv_by_manual_charging_and_returning_it_to_the_system_v1` |
| Title | Recover A Fully Discharged AGV By Manual Charging And Returning It To The System |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Recover an AGV that is fully discharged and cannot move by removing it from RMS, removing its tote, disabling a charger for exclusive use, manually charging the AGV until it boots, then adding it back into the system so it can charge itself or resume normal operation.

## When To Use

Use when an AGV is fully discharged or 'dead' and cannot move normally, and the source-described recovery method is to manually charge it until it boots and can be returned to the system.

## Do Not Use For

* Do not use when site-specific recovery controls are required but are not provided in the source.
* Do not use when the AGV cannot be safely moved.
* Do not use when the operator needs exact RMS remove or re-add UI steps that are not provided in the source.

## Safety And Operational Notes

* This procedure is not support-safe because it includes manual handling of a non-moving AGV.
* Stop if the AGV cannot be safely moved.
* The source does not provide detailed physical safety controls, floor access controls, or LOTO requirements.

## Access Or Tools Needed

* Access to RMS
* Access to charger disable and enable controls
* Physical access to the AGV
* Access to a charger or manual charger
* Ability to remove the tote from the AGV

## Related Operational Context

* ctx_training_video_manual_charging_use_case_v1
* ctx_training_video_disabled_charger_status_v1
* ctx_training_video_charging_control_architecture_v1

## Procedure Steps

### Step 1 — Identify the fully discharged AGV

**Responsible role:** L2_support

**Instruction:**
Identify the AGV that is fully discharged or 'dead' and will not move normally, matching the manual charging recovery case described in the source.

**Expected result:**
The affected AGV is identified as a manual charging recovery candidate.

**Stop or Escalate If:**

* The AGV condition does not clearly match the source-described fully discharged recovery case.
* Site-specific recovery controls are required but not provided in the source.

---

### Step 2 — Remove the AGV from RMS

**Responsible role:** L2_support

**Instruction:**
Remove the AGV from RMS as described in the source before proceeding with tote removal and manual charging recovery.

**Expected result:**
The AGV is removed from RMS.

**Stop or Escalate If:**

* Removing the AGV in RMS requires details not present in the source.

---

### Step 3 — Remove the tote from the AGV

**Responsible role:** L2_support

**Instruction:**
Remove the tote from the AGV.

**Expected result:**
The AGV is without a tote and ready for manual charging recovery.

**Stop or Escalate If:**

* The tote cannot be safely removed.
* Tote handling requires unsupported site-specific details.

---

### Step 4 — Disable a charger for manual charging use

**Responsible role:** L2_support

**Instruction:**
Disable the charger or chargers needed to support the manual charging activity so the location is not used for normal allocation.

**Expected result:**
The selected charger is logically unavailable for normal AGV allocation and can be used for the recovery.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection view, charger ID, charger enabled/disabled status, and the disable function used to reserve a charger for manual charging.*


**Stop or Escalate If:**

* The charger disable function is not available.
* The operator cannot confirm the charger is reserved from normal allocation.

---

### Step 5 — Manually position the AGV for charging

**Responsible role:** L2_support

**Instruction:**
Manually move the AGV onto a charger, or use the manual charger mentioned in the source if that is the site method.

**Expected result:**
The AGV is physically positioned for manual charging.

**Screens / Images:**

![artifact_training_video_training_video_day1_0047_so_hold_on_charger_selection_we_primary_01_48_23_000](assets/91afa453814aeed4.jpg)

*Charger Selection context showing the charger reserved for manual charging recovery.*


**Stop or Escalate If:**

* The AGV cannot be safely moved.
* Site-specific manual charging controls are required but not provided in the source.

---

### Step 6 — Wait for the AGV to boot

**Responsible role:** L2_support

**Instruction:**
Wait until the AGV has enough charge to boot up.

**Expected result:**
The AGV boots after receiving enough charge.

**Stop or Escalate If:**

* The AGV does not boot after manual charging.

---

### Step 7 — Add the AGV back into the system

**Responsible role:** L2_support

**Instruction:**
Add the AGV back into the system after it boots.

**Expected result:**
The AGV is returned to the system.

**Stop or Escalate If:**

* Re-adding the AGV in RMS requires details not present in the source.

---

### Step 8 — Return the AGV to normal charging or operation

**Responsible role:** L2_support

**Instruction:**
Allow the AGV to go charge itself or resume system-directed operation as described in the source.

**Expected result:**
The AGV resumes charging or normal system-controlled activity.

**Stop or Escalate If:**

* The AGV does not resume charging or normal system-controlled activity.

---

## Success Criteria

* The previously non-moving AGV gains enough charge to boot.
* The AGV is added back into the system.
* The AGV goes to charge itself or resumes normal system-controlled activity.

## Failure Conditions

* The AGV does not boot after manual charging.
* The AGV cannot be safely moved.
* Removing or re-adding the AGV in RMS requires details not present in the source.
* Site-specific recovery controls are required but not provided in the source.
* The AGV does not resume expected system-controlled behavior after re-add.

## Escalation Guidance

* Escalate if the AGV does not boot after manual charging.
* Escalate if the AGV cannot be safely moved.
* Escalate if site-specific recovery controls are required but not provided in the source.
* Escalate if removing or re-adding the AGV in RMS requires details not present in the source.

## Missing Details / Known Gaps

* The source does not provide exact RMS UI steps for removing the AGV.
* The source does not provide exact RMS UI steps for adding the AGV back into the system.
* The source does not provide a detailed physical movement method for the AGV.
* The source does not provide explicit charger re-enable as part of this candidate workflow, although related artifact text indicates chargers can be re-enabled after recovery.
* The source does not provide a time estimate for charging or recovery completion.
* The source does not provide explicit production stop or LOTO requirements.

## Source Lineage

- Candidate IDs: candidate_training_video_recover_fully_discharged_agv_for_return_to_system
- Source ID: `training_video_day1`
- Source Type: `training_video`
