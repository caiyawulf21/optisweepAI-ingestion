# Check Tipper Process Status and Send/Pause Controls on the VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_tipper_process_status_send_pause_visu_data_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `hospital_diversion` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the Operator Station HMI (VISU_DATA screen), verify the tipper Process Status indicators (green states) and use the VISU_DATA controls to send a tote to the hospital (SEND LEFT TO HOSPITAL / SEND RIGHT TO HOSPITAL) or pause both tippers (PAUSE TIPPER).

## When To Use

Use when you need to (1) confirm the current tipper process state indicators on the VISU_DATA screen and (2) send the tote at the left or right tipper to the hospital, or pause both tippers.

## Source Procedure References

- proc_check_tipper_process_status_send_pause_visu_data_v1

## Procedure Steps

### Step 1 — Open the Operator Station HMI and navigate to the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
On the Operator Station HMI, open the VISU_DATA screen (Operator Station HMI Data Screen).

**Expected result:**
The VISU_DATA screen is displayed, including the Process Status section and the buttons SEND LEFT TO HOSPITAL, SEND RIGHT TO HOSPITAL, and PAUSE TIPPER.

---

### Step 2 — Verify green Process Status indicators in the Process Status section

**Responsible role:** operator

**Instruction:**
In the Process Status section, observe the green status indicators for: In Cycle (Auto mode), Tipper Ready, AGV Present, Tip in Process, Tipper Clear, and Tipper Faulted.

**Expected result:**
The Process Status indicators show green states corresponding to the current tipper process state (as defined by the VISU_DATA Process Status indicators).

---

### Step 3 — Send the tote at the left tipper to the hospital

**Responsible role:** operator

**Instruction:**
If a tote is currently at the left tipper and needs to be sent to the hospital, press SEND LEFT TO HOSPITAL.

**Expected result:**
Pressing SEND LEFT TO HOSPITAL initiates sending the tote at the left tipper to the hospital.

---

### Step 4 — Send the tote at the right tipper to the hospital

**Responsible role:** operator

**Instruction:**
If a tote is currently at the right tipper and needs to be sent to the hospital, press SEND RIGHT TO HOSPITAL.

**Expected result:**
Pressing SEND RIGHT TO HOSPITAL initiates sending the tote at the right tipper to the hospital.

---

### Step 5 — Pause both tippers

**Responsible role:** operator

**Instruction:**
If you need to pause both tippers, press PAUSE TIPPER.

**Expected result:**
Pressing PAUSE TIPPER pauses both tippers.

---

## Success Criteria

- Process Status indicators on VISU_DATA show the expected green meanings for the intended action.
- SEND LEFT TO HOSPITAL or SEND RIGHT TO HOSPITAL is used only when the intended tipper state is consistent with the Process Status indicators.
- PAUSE TIPPER is used to pause both tippers when needed.

## Failure Conditions

- Process Status indicators do not match the expected green states for the intended action (e.g., tipper not ready / not in the expected state).
- Tipper Faulted indicator is green when you are attempting an action that requires a non-faulted state (mismatch between intended action and observed indicator state).

## Escalation Guidance

- If the Process Status indicators do not show the expected green states for the action you are attempting (e.g., tipper not ready / faulted state not reflected), stop using the send/pause controls and escalate per site procedure.

## Missing Details / Known Gaps

- The source defines the Process Status indicator meanings and the purpose of the SEND LEFT/RIGHT TO HOSPITAL and PAUSE TIPPER buttons, but does not provide additional post-press verification fields on VISU_DATA beyond the indicator mismatch stop rule. If the site requires a specific confirmation after pressing (e.g., which indicator should change next), that is not specified in the provided packet.
