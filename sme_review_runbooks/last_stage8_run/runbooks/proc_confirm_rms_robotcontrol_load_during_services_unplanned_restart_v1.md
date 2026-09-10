# Confirm RMS robotControl screen loads during Services Unplanned restart (before UPS removes master estop)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_confirm_rms_robotcontrol_load_during_services_unplanned_restart_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | `gateway_health`, `wcs_service_health` |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | `gateway_unhealthy`, `api_unresponsive`, `web_app_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the RMS / fleet status UI to confirm the robotControl/monitor screen fully loads before proceeding with the Services Unplanned restart sequence timing that is tied to UPS removing the master estop.

## When To Use

When performing (or preparing to perform) the Services Unplanned restart sequence and you must verify the RMS robotControl/monitor screen is reachable and fully loads before the UPS-related step involving master estop removal.

## Source Procedure References

- proc_confirm_rms_robotcontrol_load_during_services_unplanned_restart_v1

## Safety And Operational Notes

- Do not proceed to the UPS/master estop timing step if the RMS robotControl/monitor screen fails to load or remains in a loading/error state.

## Procedure Steps

### Step 1 — Open RMS / fleet status UI to the robotControl monitor path

**Responsible role:** L1_support

**Instruction:**
In a browser, open the RMS / fleet status UI using the RMS URL path fragment shown in the reference that ends with "monitor/robotControl".

**Expected result:**
The browser navigates to the RMS robotControl/monitor view (URL path includes "monitor/robotControl").

---

### Step 2 — Log into RMS

**Responsible role:** L1_support

**Instruction:**
Log into RMS using the site/FORTNA credentials workflow you normally use for RMS access.

**Expected result:**
You are authenticated in RMS and the robotControl/monitor view can begin loading.

---

### Step 3 — Wait for robotControl/monitor screen to fully load

**Responsible role:** L1_support

**Instruction:**
Wait for the robotControl/monitor screen to fully load until the page finishes loading and the robotControl view elements are visible (not blank, not stuck loading, not showing an error state).

**Expected result:**
The RMS robotControl/monitor view loads successfully and is visibly present in the RMS UI (not blank, not stuck loading, not showing an error).

---

## Success Criteria

- robotControl/monitor view is visibly present in RMS UI (not blank, not stuck loading, not showing an error).

## Failure Conditions

- robotControl/monitor page is blank, remains in loading, or shows an error state.

## Escalation Guidance

- If the robotControl screen fails to load or remains in a loading/error state, stop and escalate for RMS connectivity/service troubleshooting rather than proceeding with the UPS/master estop timing step.

## Missing Details / Known Gaps

- The packet does not provide explicit UI field names or a detailed visual checklist for what specific robotControl elements must be visible beyond the general requirement that the page is not blank/loading/error.
