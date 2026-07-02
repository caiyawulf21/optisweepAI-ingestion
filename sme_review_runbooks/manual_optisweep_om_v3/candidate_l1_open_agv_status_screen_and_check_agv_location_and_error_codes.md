# Open the AGV Status Screen and Check AGV Locations and Current Error Codes

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_agv_status_screen_and_check_agv_locations_and_current_error_codes_v1` |
| Title | Open the AGV Status Screen and Check AGV Locations and Current Error Codes |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the AGV Status screen from the system HMI and review the displayed AGV locations and any current AGV error codes.

## When To Use

Use this procedure when AGV location information or currently displayed AGV error codes need to be checked from the system HMI.

## Do Not Use For

* Do not use this procedure to interpret AGV error code meanings when the source does not define them.
* Do not use this procedure for corrective action or AGV recovery steps, because the source only supports access to the AGV Status screen and observation of displayed information.

## Safety And Operational Notes

* This is an HMI-based observation procedure supported as safe by the source candidate.
* Do not infer corrective actions from displayed AGV error codes unless supported by another approved source.

## Access Or Tools Needed

* Access to the system HMI display
* AGV STATUS control in the upper-left corner of the display
* AGV Status screen

## Related Operational Context

* ctx_manual_agv_status_screen_v1
* ctx_manual_agv_location_and_error_visibility_v1

## Procedure Steps

### Step 1 — Open the AGV Status screen

**Responsible role:** L1_support

**Instruction:**
On the system HMI display, press AGV STATUS in the upper-left corner of the display to access the "AGV Status" screen.

**Expected result:**
The AGV Status screen opens on the HMI.

**Screens / Images:**

![artifact_fig_4_1_acb_system_overview_screen](assets/artifact_fig_4_1_acb_system_overview_screen.jpeg)

*Use the system HMI display context while locating the AGV STATUS access point in the upper-left corner of the display.*

![artifact_fig_4_17_agv_status_screen](assets/artifact_fig_4_17_agv_status_screen.jpeg)

*Reference the target AGV Status screen that should appear after pressing AGV STATUS.*


**Stop or Escalate If:**

* Escalate if the AGV Status screen cannot be accessed from the AGV STATUS control described in the source.

---

### Step 2 — Confirm the AGV Status screen is displayed

**Responsible role:** L1_support

**Instruction:**
Confirm that the "AGV Status" screen is displayed.

**Expected result:**
The displayed screen matches the AGV Status screen.

**Screens / Images:**

![artifact_fig_4_17_agv_status_screen](assets/artifact_fig_4_17_agv_status_screen.jpeg)

*Compare the displayed HMI screen to the AGV Status screen reference.*


**Stop or Escalate If:**

* Escalate if the displayed screen cannot be confirmed as the AGV Status screen.

---

### Step 3 — Review AGV locations

**Responsible role:** L1_support

**Instruction:**
Review the location shown for the AGVs on the screen.

**Expected result:**
AGV location information is visible on the AGV Status screen.

**Screens / Images:**

![artifact_fig_4_17_agv_status_screen](assets/artifact_fig_4_17_agv_status_screen.jpeg)

*Look for the AGV location information shown on the AGV Status screen.*


**Stop or Escalate If:**

* Escalate if AGV location information is not visible on the AGV Status screen.

---

### Step 4 — Review current AGV error codes

**Responsible role:** L1_support

**Instruction:**
Review any error codes shown for an AGV that is currently experiencing an error.

**Expected result:**
Any current AGV error codes shown on the screen are identified.

**Screens / Images:**

![artifact_fig_4_17_agv_status_screen](assets/artifact_fig_4_17_agv_status_screen.jpeg)

*Look for any current AGV error codes displayed for AGVs experiencing an error.*


**Stop or Escalate If:**

* Escalate if the displayed AGV condition cannot be interpreted from the available source because the source only states that current error codes are shown and does not define their meanings.

---

### Step 5 — Record displayed AGV status information

**Responsible role:** L1_support

**Instruction:**
Record the displayed AGV location information and any current error codes exactly as shown on the screen.

**Expected result:**
The displayed AGV location information and any current error codes are documented exactly as shown.

**Screens / Images:**

![artifact_fig_4_17_agv_status_screen](assets/artifact_fig_4_17_agv_status_screen.jpeg)

*Use the AGV Status screen as the reference for the location and current error code information to be recorded.*


**Stop or Escalate If:**

* Escalate if the displayed information cannot be clearly read or recorded exactly as shown.

---

## Success Criteria

* The AGV Status screen is accessed from the system HMI.
* Displayed AGV locations are reviewed.
* Any current AGV error codes shown on the screen are reviewed.
* Displayed AGV location information and any current error codes are recorded exactly as shown.

## Failure Conditions

* The AGV Status screen cannot be accessed from the AGV STATUS control described in the source.
* The displayed screen cannot be confirmed as the AGV Status screen.
* AGV location information is not visible on the screen.
* The displayed AGV condition cannot be interpreted from the available source because error code meanings are not defined.
* Displayed AGV information cannot be recorded exactly as shown.

## Escalation Guidance

* Escalate if the AGV Status screen cannot be accessed from the AGV STATUS control described in the source.
* Escalate if the displayed AGV condition cannot be interpreted from the available source because the source only states that current error codes are shown and does not define their meanings.

## Missing Details / Known Gaps

* The source does not define the meanings of AGV error codes shown on the AGV Status screen.
* The source does not provide corrective actions based on displayed AGV error codes.
* The source does not provide an estimated completion time.
* The source does not specify whether production stop or LOTO is required; this procedure is limited to HMI observation.

## Source Lineage

- Candidate IDs: candidate_l1_open_agv_status_screen_and_check_agv_location_and_error_codes
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
