# Determine Tipper Or Station Status From Operator Station Stacklights

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_determine_tipper_or_station_status_from_operator_station_stacklights_v1` |
| Title | Determine Tipper Or Station Status From Operator Station Stacklights |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented operator station stacklight color, flashing pattern, and horn pattern to determine the current status of the corresponding tipper and station.

## When To Use

Use when an operator needs to identify the documented current status of the corresponding tipper or station by observing the operator station stacklights and any associated horn pattern.

## Do Not Use For

* Do not use to infer corrective actions when the source provides status meaning only.
* Do not use if the observed stacklight or horn pattern does not match any documented indication.

## Safety And Operational Notes

* This runbook is a status interpretation reference only.
* Do not infer corrective actions from the status mapping when the source provides status meaning only.

## Access Or Tools Needed

* Visual access to the operator station stacklights
* Ability to observe horn alarm presence and pattern
* Documented stacklight status mapping

## Related Operational Context

* ctx_manual_operator_station_stacklights_v1

## Procedure Steps

### Step 1 — Locate the operator station stacklights

**Responsible role:** operator

**Instruction:**
Locate the operator station stacklights at the top of either side of the frame.

**Expected result:**
The two operator station stacklights are identified for observation.

**Screens / Images:**

![artifact_fig_3_6_stacklight](assets/artifact_fig_3_6_stacklight.png)

*Physical appearance and location style of the stacklight assembly.*


**Stop or Escalate If:**

* The stacklights cannot be located.
* The stacklights are obstructed or not visible enough to interpret.

---

### Step 2 — Determine whether the indication is solid or flashing

**Responsible role:** operator

**Instruction:**
Observe whether the displayed indication is solid or flashing.

**Expected result:**
The indication is classified as either solid or flashing.

**Screens / Images:**

![artifact_fig_3_6_stacklight](assets/artifact_fig_3_6_stacklight.png)

*The illuminated stacklight section and whether it appears steady or flashing.*


**Stop or Escalate If:**

* The indication cannot be reliably determined as solid or flashing.
* The observed pattern appears inconsistent with the documented categories.

---

### Step 3 — Identify the color pattern and any horn alarm

**Responsible role:** operator

**Instruction:**
Identify the displayed color or color combination and note whether a horn alarm is present and whether it is long or intermittent.

**Expected result:**
The observed color or color combination and horn pattern are identified.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*VISU_ALARM view showing tipper alarms and timestamps if alarm context needs to be reviewed alongside the observed horn or stacklight indication.*


**Stop or Escalate If:**

* The observed color or color combination is unclear.
* A horn alarm is heard but its pattern cannot be determined.
* The observed indication does not appear to match a documented color or horn combination.

---

### Step 4 — Match the observed indication to the documented status mapping

**Responsible role:** operator

**Instruction:**
Compare the observed indication to the documented mappings: Solid Blue = tipper is paused; Solid Green = tipping in process; Solid Red = Estop is activated; Solid White = AGV is present (post-tipping); Solid Red, Yellow, Green = RMS error; Flashing Blue = tipper is disabled; Flashing Green = tipper is "starved"; Flashing Red = tipper is faulted; Flashing White = SurePost tote is being sent to the station; Flashing Yellow = AGV is present (pre-tipping); Flashing Green, Yellow, Green with long horn alarm = sort is starting; Flashing White with intermittent horn alarm = bagout is complete.

**Expected result:**
A documented status meaning is assigned to the observed indication.

**Screens / Images:**

![artifact_fig_3_6_stacklight](assets/artifact_fig_3_6_stacklight.png)

*Stacklight indicator reference while comparing observed color and flashing pattern.*

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*Alarm list and timestamps if additional alarm context is needed while interpreting fault-related or horn-related indications.*


**Stop or Escalate If:**

* The observed stacklight or horn pattern does not match any documented indication.
* The user is being asked to take corrective action not supported by this status-only mapping.

---

### Step 5 — Record or communicate the documented status

**Responsible role:** operator

**Instruction:**
Record or communicate the documented status meaning for the corresponding tipper or station.

**Expected result:**
The documented status meaning is recorded or communicated accurately.

**Screens / Images:**

![artifact_fig_4_28_operator_station_hmi_alarms_screen](assets/artifact_fig_4_28_operator_station_hmi_alarms_screen.jpeg)

*Alarm timestamps if needed to support communication of current alarm-related status context.*


**Stop or Escalate If:**

* The observed indication could not be matched to a documented status.
* There is uncertainty about the correct documented meaning to communicate.

---

## Success Criteria

* The user determines the documented current status of the corresponding tipper or station from the observed stacklight and horn pattern.
* The observed indication is matched to one documented mapping exactly.
* The documented status meaning is recorded or communicated accurately.

## Failure Conditions

* The stacklights cannot be located or observed clearly.
* The indication cannot be reliably distinguished as solid or flashing.
* The color pattern or horn pattern cannot be determined confidently.
* The observed stacklight or horn pattern does not match any documented indication.
* A user attempts to infer corrective action from a status-only mapping.

## Escalation Guidance

* Escalate if the observed stacklight or horn pattern does not match any documented indication.
* Escalate if the stacklight or horn pattern cannot be observed clearly enough to classify.
* Do not infer corrective actions from the status mapping when the source provides status meaning only.

## Missing Details / Known Gaps

* The packet does not provide a direct OCR text block for page 28 or page 58 in source_sections.
* The source does not provide corrective actions for any stacklight status in this packet.
* The source does not provide an estimated completion time.
* The source does not specify supporting roles beyond the operator.
* The source does not specify whether production stop or LOTO is required because this is a reference procedure.

## Source Lineage

- Candidate IDs: candidate_operator_interpret_operator_station_stacklight_status
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
