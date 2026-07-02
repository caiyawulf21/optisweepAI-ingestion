# Determine Operator Station And Tipper Status From Stacklight Indications

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_determine_operator_station_and_tipper_status_from_stacklight_indications_v1` |
| Title | Determine Operator Station And Tipper Status From Stacklight Indications |
| Procedure Type | `reference` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented operator station stacklight colors, flashing patterns, and horn patterns to determine the current status of the corresponding tipper and station.

## When To Use

Use this reference when you need to identify the current documented status of an operator station or corresponding tipper by observing the station stacklights and any associated horn pattern.

## Do Not Use For

* Do not use this runbook to infer corrective actions beyond the documented status meanings.
* Do not use this runbook when the observed stacklight or horn pattern does not match any documented indication in the source.

## Safety And Operational Notes

* This runbook is limited to observing, matching, and recording status indications from the source.
* Do not infer corrective actions beyond the documented status meanings.

## Access Or Tools Needed

* Visual access to the operator station stacklights
* Ability to hear horn alarms at the station
* Documented stacklight status mapping

## Related Operational Context

* ctx_manual_operator_station_stacklights_overview_v1
* ctx_manual_operator_station_stacklight_statuses_v1

## Procedure Steps

### Step 1 — Locate the operator station stacklights

**Responsible role:** operator

**Instruction:**
Go to the operator station and locate the two stacklights at the top of either side of the frame.

**Expected result:**
The two operator station stacklights are identified.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Look for the operator station layout and the stacklights mounted on the top of the frame on either side of the chute.*


**Stop or Escalate If:**

* Escalate if the stacklights cannot be located or observed.

---

### Step 2 — Determine whether the indication is solid or flashing

**Responsible role:** operator

**Instruction:**
Observe whether the active indication is solid or flashing.

**Expected result:**
The indication is classified as either solid or flashing.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the operator station reference image to confirm the physical location of the stacklights while observing their behavior.*


**Stop or Escalate If:**

* Escalate if the observed light behavior cannot be determined.

---

### Step 3 — Identify the displayed color or color sequence

**Responsible role:** operator

**Instruction:**
Identify the displayed color or color sequence, including Blue, Green, Red, White, Yellow, or the documented multi-color combinations.

**Expected result:**
The observed color or color sequence is identified.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the station photo to orient yourself to the stacklight location while identifying the active color or sequence.*


**Stop or Escalate If:**

* Escalate if the observed color or sequence does not match a documented indication.

---

### Step 4 — Listen for any horn pattern

**Responsible role:** operator

**Instruction:**
Listen for any horn pattern and note whether there is a long horn alarm or an intermittent horn alarm when present.

**Expected result:**
Any associated horn pattern is identified and noted.

**Screens / Images:**

![artifact_fig_3_1_operator_station_panels_removed_for_clarity](assets/artifact_fig_3_1_operator_station_panels_removed_for_clarity.jpeg)

*Use the operator station reference image to confirm you are at the correct station while listening for any horn associated with the stacklight indication.*


**Stop or Escalate If:**

* Escalate if a horn pattern is needed to interpret the indication but cannot be heard or distinguished.

---

### Step 5 — Match the observed indication to the documented status mapping

**Responsible role:** operator

**Instruction:**
Compare the observed indication to the documented mapping: Solid Blue = tipper is paused; Solid Green = tipping in process; Solid Red = Estop is activated; Solid White = AGV is present (post-tipping); Solid Red, Yellow, Green = RMS error; Flashing Blue = tipper is disabled; Flashing Green = tipper is "starved"; Flashing Red = tipper is faulted; Flashing White = SurePost tote is being sent to the station; Flashing Yellow = AGV is present (pre-tipping); Flashing Green, Yellow, Green with long horn alarm = sort is starting; Flashing White with intermittent horn alarm = bagout is complete.

**Expected result:**
A documented status meaning is matched to the observed indication.

**Stop or Escalate If:**

* Escalate if the observed stacklight or horn pattern does not match any documented indication in the source.
* Stop if interpretation would require inferring corrective actions beyond the documented status meanings.

---

### Step 6 — Record or communicate the matched status

**Responsible role:** operator

**Instruction:**
Record or communicate the documented status meaning that matches the observed indication.

**Expected result:**
The matched documented status is recorded or communicated.

**Stop or Escalate If:**

* Escalate if no documented status meaning can be matched.
* Stop if communication would require unsupported corrective guidance.

---

## Success Criteria

* The user identifies the documented current status of the corresponding tipper or station from the observed stacklight and horn indication.
* The matched status meaning is recorded or communicated without adding unsupported corrective action.

## Failure Conditions

* The stacklights cannot be located or observed.
* The light behavior cannot be determined as solid or flashing.
* The color or sequence cannot be identified.
* A required horn pattern cannot be heard or distinguished.
* The observed stacklight or horn pattern does not match any documented indication in the source.

## Escalation Guidance

* Escalate if the observed stacklight or horn pattern does not match any documented indication in the source.
* Do not infer corrective actions beyond the documented status meanings.

## Missing Details / Known Gaps

* The source provides status meanings only and does not provide corrective actions for any stacklight condition.
* The source does not provide a time estimate for using this reference.
* The source does not specify production stop or LOTO requirements for this reference activity.
* No source-specific artifact in the packet directly shows the operator station stacklight indications themselves; the attached image is a station layout reference.

## Source Lineage

- Candidate IDs: candidate_operator_station_interpret_stacklight_status
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
