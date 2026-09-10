# Reset Tipper Stats Data to Zero on the VISU_DATA Screen

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_reset_tipper_stats_data_to_zero_on_visu_data_screen_v1` |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Capability Tags | `agv_active_errors` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

The Operator Station HMI VISU_DATA screen includes a Tipper Stats section with a DATA RESET button. Pressing DATA RESET clears the displayed tipper statistics data to zero.

## When To Use

Use when you need to clear the displayed Tipper Stats counters on the Operator Station HMI VISU_DATA screen (e.g., to start a fresh measurement window for Totes Processed, Faults, Avg Cycle Time, Avg Totes/Hour, and Time Starved).

## Source Procedure References

- proc_reset_tipper_stats_data_to_zero_on_visu_data_screen_v1

## Procedure Steps

### Step 1 — Open the Operator Station HMI and navigate to the VISU_DATA screen

**Responsible role:** operator

**Instruction:**
On the Operator Station HMI, navigate to the VISU_DATA screen (Operator Station HMI Data Screen).

**Expected result:**
The VISU_DATA screen is displayed with the Tipper Stats section visible.

---

### Step 2 — Locate the DATA RESET button for the Tipper Stats section

**Responsible role:** operator

**Instruction:**
On the VISU_DATA screen, locate the DATA RESET button within the Tipper Stats section.

**Expected result:**
You can identify the DATA RESET button associated with the Tipper Stats section.

---

### Step 3 — Press DATA RESET to reset Tipper Stats to zero

**Responsible role:** operator

**Instruction:**
Press the DATA RESET button for the Tipper Stats section.

**Expected result:**
The displayed Tipper Stats values reset to zero after the button press.

---

### Step 4 — Verify Tipper Stats values reset to zero

**Responsible role:** operator

**Instruction:**
Verify the Tipper Stats values shown on the VISU_DATA screen have reset to zero values as displayed (e.g., Totes Processed, Faults, Avg Cycle Time, Avg Totes/Hour, Time Starved).

**Expected result:**
All displayed Tipper Stats counters show zero values.

---

## Success Criteria

- After pressing DATA RESET, the displayed Tipper Stats values on VISU_DATA show zero values.

## Failure Conditions

- Tipper Stats values on VISU_DATA do not reset to zero after pressing DATA RESET.

## Escalation Guidance

- If the displayed Tipper Stats values do not reset to zero, stop and escalate for support rather than repeatedly pressing the reset.

## Missing Details / Known Gaps

- The source states DATA RESET resets the data to zero but does not specify which exact fields are zeroed beyond the displayed Tipper Stats values; this runbook verifies the displayed Tipper Stats values as shown on VISU_DATA.
