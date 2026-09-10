# Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Capability Tags | None |
| Access Surface | `rms_ui` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Use the Get AGV Status view (RMS / fleet status UI) to confirm the current AGV state, current command vitals (described as “teal vitals”), and whether the HMI error alert flag is set to true and bubbles to the top when an AGV error or system error is active.

## When To Use

Use when you need to verify whether any AGV errors or system errors are currently active and are being surfaced by the Get AGV Status HMI error alert behavior (alert becomes true and bubbles to the top).

## Source Procedure References

- proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1

## Procedure Steps

### Step 1 — Open Get AGV Status view and locate AGV state, teal command vitals, and error sections

**Responsible role:** L1_support

**Instruction:**
Open the live Get AGV Status view/screen in the RMS / fleet status UI that shows: (1) AGV state, (2) current command vitals (described as “teal vitals”), and (3) sections for AGV errors and system errors.

**Expected result:**
The Get AGV Status screen displays AGV state, current command vitals (“teal vitals”), and areas where AGV errors and system errors are shown.

---

### Step 2 — Verify displayed AGV state and current command vitals (teal vitals) for a selected AGV entry

**Responsible role:** L1_support

**Instruction:**
Select an AGV row/entry on the Get AGV Status screen and verify the displayed AGV state and the current command vitals (described as “teal vitals”).

**Expected result:**
For the selected AGV entry, the AGV state and teal vitals are populated and visible on the Get AGV Status screen.

---

### Step 3 — Check error alert flag behavior (must be true and bubble to the top when an error exists)

**Responsible role:** L1_support

**Instruction:**
On the Get AGV Status screen, check whether an error alert is present and whether it is set to true when there is an error (system error or “geek error”). Confirm that the alert bubbles to the top in the HMI when errors exist.

**Expected result:**
When an AGV error or system error exists, the error alert flag is set to true and bubbles to the top in the HMI.

---

### Step 4 — Confirm AGV errors and/or system errors sections are populated when the alert indicates an error

**Responsible role:** L1_support

**Instruction:**
If the error alert indicates an error, confirm the Get AGV Status screen is showing AGV errors and/or system errors (described as being populated from the system faults table / active faults).

**Expected result:**
When the error alert indicates an error, the AGV errors and/or system errors sections on the Get AGV Status screen are populated.

---

## Success Criteria

- When an AGV error or system error exists, the Get AGV Status HMI error alert flag is set to true and bubbles to the top.
- For the selected AGV entry, AGV state and current command vitals (“teal vitals”) are populated.
- When the error alert indicates an error, the AGV errors and/or system errors sections are populated.

## Failure Conditions

- Error alert is not set to true while an active AGV/system error condition is observed.
- Error alert does not bubble to the top in the HMI despite an observed AGV/system error.
- Error alert indicates an error but AGV errors/system errors sections are not populated as expected.

## Escalation Guidance

- Escalate if the error alert does not change to true when an error exists, or if it does not bubble to the top in the HMI despite an observed AGV/system error condition.

## Missing Details / Known Gaps

- The packet does not provide the exact RMS navigation path/menu clicks to reach the Get AGV Status view; it only references opening the Get AGV Status screen.
