# Interpret AGB HV Charge Percentage During Extended Delay Or Troubleshooting

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_agb_hv_charge_percentage_during_extended_delay_or_troubleshooting_v1` |
| Title | Interpret AGB HV Charge Percentage During Extended Delay Or Troubleshooting |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the HV charge percentage shown in the selected AGB power section as an operational awareness reference during prolonged idle time or extended troubleshooting. The training source indicates 50% as an example displayed value and identifies roughly 30% to 32% as edging toward concern when the AGB has been sitting for hours or issue resolution is taking one to two hours.

## When To Use

Use when an AGB is selected in the interface and support needs to interpret the displayed HV charge percentage during extended delay, prolonged idle time, or troubleshooting that may take significant time.

## Do Not Use For

* Do not use this runbook as a formal shutdown threshold procedure.
* Do not use this runbook to determine a charging threshold or mandatory corrective action, because the source does not define one.
* Do not use this runbook as a recovery procedure for moving, restarting, or charging the AGB.

## Safety And Operational Notes

* This source provides operational awareness guidance only, not a formal battery control procedure.
* Do not invent a shutdown threshold, charging threshold, or corrective action because the source does not provide one.

## Access Or Tools Needed

* Access to the AGB selection interface
* Visibility of the power section and HV charge percentage
* Awareness of elapsed idle or troubleshooting time

## Related Operational Context

* ctx_training_video_agb_hv_power_display_v1
* ctx_training_video_agb_low_charge_operational_risk_v1

## Procedure Steps

### Step 1 — Select the AGB and view the power section

**Responsible role:** L1_support

**Instruction:**
Select the AGB in the interface and open or view the small section labeled power so the HV charge percentage is visible.

**Expected result:**
The selected AGB shows a power section with an HV charge percentage.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*The selected AGB detail area and the referenced power section where HV charge percentage is discussed.*


**Stop or Escalate If:**

* Stop if the HV charge percentage cannot be viewed from the selected AGB interface.

---

### Step 2 — Read the current HV charge percentage

**Responsible role:** L1_support

**Instruction:**
Read the current HV charge percentage displayed in the power section for the selected AGB.

**Expected result:**
A current HV charge percentage is identified for the selected AGB.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*The power section value referenced in training, including the example showing 50%.*


**Stop or Escalate If:**

* Stop if the displayed HV percentage is unavailable or unreadable.

---

### Step 3 — Compare the displayed value to the training examples

**Responsible role:** L1_support

**Instruction:**
Compare the observed HV charge percentage to the training examples: 50% is given as an example displayed reading, while 30% to 32% is described as edging toward concern when delays continue.

**Expected result:**
The current reading is categorized relative to the example values discussed in training.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*Training context tied to the HV percentage discussion and example values.*


**Stop or Escalate If:**

* Stop if interpretation depends on a formal threshold not stated in the source.

---

### Step 4 — Account for extended idle or troubleshooting time

**Responsible role:** L1_support

**Instruction:**
Consider whether the AGB has been sitting for hours or whether issue resolution is taking an hour or two, because the training source states those delays increase concern about the remaining HV charge.

**Expected result:**
The HV reading is interpreted in the context of elapsed idle or troubleshooting time.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*The training frame associated with the discussion of an AGB sitting for hours and low-30% HV during troubleshooting.*


**Stop or Escalate If:**

* Escalate if the issue remains unresolved while the HV percentage continues to trend toward the low values discussed in the source.

---

### Step 5 — Record approaching low-charge operational concern

**Responsible role:** L1_support

**Instruction:**
Record that the AGB is approaching a low-charge operational concern if the displayed percentage is in the low-30% range during extended delay conditions.

**Expected result:**
The AGB status is documented as approaching a low-charge operational concern when the source-supported conditions are met.

**Screens / Images:**

![artifact_training_video_training_video_day1_0048_like_it_sat_there_for_hours_primary_01_51_30_500](assets/111d7c343d0c86a3.jpg)

*The source segment supporting low-30% HV as edging toward concern during long delays.*


**Stop or Escalate If:**

* Escalate if the AGB cannot be moved.
* Escalate if the issue remains unresolved while the HV percentage continues to trend toward the low values discussed in the source.
* Do not proceed by inventing a shutdown threshold, charging threshold, or corrective action.

---

## Success Criteria

* The selected AGB HV charge percentage can be viewed in the power section.
* The current HV percentage is interpreted using only the source-provided examples and delay context.
* Low-30% readings during extended delay conditions are recognized as approaching operational concern without inventing unsupported thresholds or actions.

## Failure Conditions

* The AGB cannot be selected or the power section cannot be viewed.
* The HV charge percentage is not readable.
* The issue remains unresolved while the HV percentage continues to trend toward the low values discussed in the source.
* The user attempts to apply unsupported shutdown thresholds, charging thresholds, or corrective actions.

## Escalation Guidance

* Escalate if the AGB cannot be moved.
* Escalate if the issue remains unresolved while the HV percentage continues to trend toward the low values discussed in the source.
* Escalate rather than inventing a shutdown threshold, charging threshold, or corrective action not provided by the source.

## Missing Details / Known Gaps

* The source does not define a formal shutdown threshold for HV charge in this segment.
* The source does not define a mandatory charging threshold in this segment.
* The source does not provide a required corrective action when low-30% HV is observed during delay.
* The source does not specify how to record the concern in a system or log.
* The supplied artifact is only indirectly aligned to the HV discussion and does not clearly isolate the power section UI.

## Source Lineage

- Candidate IDs: candidate_training_video_interpret_agb_hv_charge_risk_during_extended_delay
- Source ID: `training_video_day1`
- Source Type: `training_video`
