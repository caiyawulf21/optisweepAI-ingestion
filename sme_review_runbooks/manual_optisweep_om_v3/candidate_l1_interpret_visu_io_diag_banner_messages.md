# Check And Record VISU_IO_DIAG Banner Messages

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_and_record_visu_io_diag_banner_messages_v1` |
| Title | Check And Record VISU_IO_DIAG Banner Messages |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the VISU_IO_DIAG informational banner on the Operator Station HMI to review alarms or informational messages and record the messages shown. The source describes this screen as read-only and intended for troubleshooting.

## When To Use

Use when troubleshooting from the Operator Station HMI and you need to review the alarms or informational messages currently displayed in the VISU_IO_DIAG banner.

## Do Not Use For

* Do not use this procedure to perform corrective action, because the source only documents message display and navigation.
* Do not infer message meaning beyond what is explicitly displayed.

## Safety And Operational Notes

* The VISU_IO_DIAG screen is read-only and can be used for troubleshooting.

## Access Or Tools Needed

* Access to the Operator Station HMI
* VISU_IO_DIAG screen

## Related Operational Context

* ctx_manual_visu_io_diag_screen_overview_v1
* ctx_manual_visu_io_diag_banner_messages_v1

## Procedure Steps

### Step 1 — Open the VISU_IO_DIAG screen

**Responsible role:** L1_support

**Instruction:**
Open the VISU_IO_DIAG screen on the Operator Station HMI.

**Expected result:**
The VISU_IO_DIAG screen is displayed on the Operator Station HMI.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*Overall VISU_IO_DIAG screen layout and the informational banner area.*

![artifact_fig_4_18_operator_station_display_controls](assets/artifact_fig_4_18_operator_station_display_controls.png)

*Display controls and screen access reference showing VISU_IO_DIAG availability.*


**Stop or Escalate If:**

* Escalate if the VISU_IO_DIAG screen cannot be accessed from the Operator Station HMI.

---

### Step 2 — Locate the informational banner

**Responsible role:** L1_support

**Instruction:**
Locate the informational banner on the VISU_IO_DIAG screen that displays alarms or informational messages.

**Expected result:**
The informational banner is identified on the screen.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*The informational banner area on the VISU_IO_DIAG screen.*


**Stop or Escalate If:**

* Escalate if the informational banner described in the source is not visible on the VISU_IO_DIAG screen.

---

### Step 3 — Observe the current banner message

**Responsible role:** L1_support

**Instruction:**
Observe the currently displayed banner message.

**Expected result:**
The current alarm or informational message shown in the banner is visible to the user.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*The text currently shown in the informational banner.*


**Stop or Escalate If:**

* Escalate if the banner message area is present but no message can be read.

---

### Step 4 — Navigate through banner messages

**Responsible role:** L1_support

**Instruction:**
Use the arrows on the right side of the banner to move through the available messages one at a time.

**Expected result:**
The banner advances through available messages one at a time using the right-side arrows.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*The arrows on the right side of the informational banner used for message navigation.*


**Stop or Escalate If:**

* Escalate if banner messages cannot be navigated using the arrows described in the source.

---

### Step 5 — Record each displayed message

**Responsible role:** L1_support

**Instruction:**
Record each displayed alarm or informational message shown in the banner as you review the available messages.

**Expected result:**
Each displayed alarm or informational message has been documented.

**Screens / Images:**

![artifact_fig_4_27_operator_station_io_diagnostics_screen](assets/artifact_fig_4_27_operator_station_io_diagnostics_screen.jpeg)

*The read-only diagnostics screen and banner messages being reviewed for documentation.*


**Stop or Escalate If:**

* Escalate if messages cannot be fully reviewed because the banner cannot be navigated.
* Do not infer message meaning beyond what is explicitly displayed.

---

## Success Criteria

* The VISU_IO_DIAG screen is opened successfully.
* The informational banner is located.
* Available banner messages are reviewed using the right-side arrows.
* Each displayed alarm or informational message is recorded.

## Failure Conditions

* The VISU_IO_DIAG screen cannot be accessed.
* The informational banner cannot be identified.
* Banner messages cannot be navigated using the arrows described in the source.
* Displayed messages cannot be read or fully documented.

## Escalation Guidance

* Escalate if banner messages cannot be navigated using the arrows described in the source.
* Escalate if the VISU_IO_DIAG screen or informational banner is not accessible as described.
* Do not infer message meaning beyond what is explicitly displayed.

## Missing Details / Known Gaps

* The source does not provide a detailed method for how to record messages.
* The source does not define the exact access sequence beyond identifying VISU_IO_DIAG as an Operator Station HMI screen and related display controls.
* The source does not provide interpretation guidance for specific banner messages.
* The source does not provide an estimated completion time.
* The source does not state whether production stop or LOTO is required.

## Source Lineage

- Candidate IDs: candidate_l1_interpret_visu_io_diag_banner_messages
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
