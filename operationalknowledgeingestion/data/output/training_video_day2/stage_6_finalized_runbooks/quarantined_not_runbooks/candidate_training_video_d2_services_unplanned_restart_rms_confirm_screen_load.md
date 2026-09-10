# Confirm RMS screen loads during Services Unplanned restart (before UPS-related master estop removal)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_rms_screen_loads_during_services_unplanned_restart_v1` |
| Title | Confirm RMS screen loads during Services Unplanned restart (before UPS-related master estop removal) |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `web_app_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that the Fortna RMS web interface finishes loading the "monitor/robotControl" screen for the "Services Unplanned restart" context before proceeding with the UPS-related master estop removal step.

## When To Use

Use when performing a "Services Unplanned restart" support activity and you must confirm the Fortna RMS "monitor/robotControl" screen is fully loaded and ready before the UPS-related master estop removal step is performed.

## Do Not Use For

* Do not proceed to any UPS/master estop-related action if the RMS screen does not load or remains in a loading/failed state.

## Safety And Operational Notes

* Stop and escalate if the RMS screen does not load or remains in a loading/failed state; do not proceed with the UPS/master estop-related action.

## Access Or Tools Needed

* RMS web access
* Browser access to the RMS URL path fragment shown in the source (includes "monitor/robotControl")

## Related Operational Context

* ctx_training_video_services_unplanned_restart_rms_screen_v1
* ctx_training_video_rms_robotcontrol_monitor_reference_v1
* ctx_training_video_master_estop_ups_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0052_no_it_s_it_s_just_primary_03_14_05_500](assets/b57e4dd0b50bf822.jpg)

*Training frame showing the "Services Unplanned restart" instruction to log into RMS and confirm the screen loads before UPS removes the master estop, including an RMS URL path fragment ending with "monitor/robotControl".*

## Procedure Steps

### Step 1 — Open the RMS web interface using the URL path fragment that includes "monitor/robotControl"

**Responsible role:** L1_support

**Instruction:**
In a browser, open the Fortna RMS URL path fragment shown in the source that ends with "monitor/robotControl" (the source frame is under the "Services Unplanned restart" heading).

**Expected result:**
The RMS page navigation reaches the "monitor/robotControl" screen context (URL path fragment includes "monitor/robotControl").

**Stop or Escalate If:**

* If you cannot reach the "monitor/robotControl" screen context, stop and escalate for deeper troubleshooting rather than proceeding with the UPS/master estop-related action.

---

### Step 2 — Log into RMS for the "Services Unplanned restart" context

**Responsible role:** L1_support

**Instruction:**
Log into Fortna RMS as part of the "Services Unplanned restart" activity.

**Expected result:**
You are logged into RMS and can load the referenced "monitor/robotControl" screen.

**Stop or Escalate If:**

* If login prevents reaching the "monitor/robotControl" screen, stop and escalate for deeper troubleshooting rather than proceeding with the UPS/master estop-related action.

---

### Step 3 — Navigate to/ensure the "monitor/robotControl" screen is the one that loads

**Responsible role:** L1_support

**Instruction:**
Ensure the RMS page that loads corresponds to the "monitor/robotControl" screen (the source frame references an RMS URL path fragment ending with "monitor/robotControl").

**Expected result:**
The loaded page corresponds to the "monitor/robotControl" screen context.

**Stop or Escalate If:**

* If the wrong screen loads (not the "monitor/robotControl" context), stop and escalate for deeper troubleshooting rather than proceeding with the UPS/master estop-related action.

---

### Step 4 — Confirm the "monitor/robotControl" screen has fully loaded (ready, not still loading/failed)

**Responsible role:** L1_support

**Instruction:**
Confirm the "monitor/robotControl" page is fully loaded and ready to view (not still loading and not in a failed state).

**Expected result:**
The RMS "monitor/robotControl" screen is fully loaded and ready to view.

**Stop or Escalate If:**

* If the RMS screen does not load or remains in a loading/failed state, stop and escalate for deeper troubleshooting rather than proceeding with the UPS/master estop-related action.

---

### Step 5 — Proceed only after the RMS "monitor/robotControl" screen is confirmed loaded

**Responsible role:** L1_support

**Instruction:**
Only proceed with the UPS-related step described by the "Services Unplanned restart" activity after you have confirmed the RMS "monitor/robotControl" screen is fully loaded and ready.

**Expected result:**
You have completed the RMS readiness check and are cleared to proceed to the next UPS/master estop-related action per the support sequence.

**Stop or Escalate If:**

* If the RMS screen is not fully loaded/ready, do not proceed; stop and escalate for deeper troubleshooting.

---

## Success Criteria

* Fortna RMS "monitor/robotControl" screen is fully loaded and ready to view before any UPS-related master estop removal step is performed.

## Failure Conditions

* RMS "monitor/robotControl" screen does not load or remains in a loading/failed state.

## Escalation Guidance

* If the RMS screen does not load or remains in a loading/failed state, stop and escalate for deeper troubleshooting rather than proceeding with the UPS/master estop-related action.

## Missing Details / Known Gaps

* The packet does not provide explicit, observable UI labels/fields beyond the referenced "monitor/robotControl" path fragment and the general requirement that the screen "loads" (no specific loading indicator text or success UI element is named).
* The packet does not provide the exact RMS login method/credentials steps or the exact UPS/master estop removal procedure steps (only the ordering constraint is referenced).

## Source Lineage

- Candidate IDs: candidate_training_video_d2_services_unplanned_restart_rms_confirm_screen_load
- Source ID: `training_video_day2`
- Source Type: `training_video`
