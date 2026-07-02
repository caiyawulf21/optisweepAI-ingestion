# Place a Return Tote on the Hospital Station Induct Side

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_place_return_tote_on_hospital_station_induct_side_v1` |
| Title | Place a Return Tote on the Hospital Station Induct Side |
| Procedure Type | `operation` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Return a tote to the system from the hospital station by placing the tote on the left-side induct area of the station and ensuring it is flush against the end stops.

## When To Use

Use this procedure when a tote at the hospital station is going back into the system and must be physically placed on the station induct side.

## Do Not Use For

* Do not use this procedure for totes that are not going back into the system.
* Do not use this procedure as a complete hospital station workflow; the source only supports the physical tote placement portion.

## Safety And Operational Notes

* Use only the documented physical placement steps supported by the source.
* The source does not provide additional handling instructions if the tote cannot be positioned flush against the end stops.

## Access Or Tools Needed

* Physical access to the hospital station induct side
* Tote to be returned to the system
* Visibility of the end stops

## Related Operational Context

* ctx_manual_hospital_station_overview_v1
* ctx_manual_hospital_station_main_menu_access_v1

## Procedure Steps

### Step 1 — Identify the hospital station induct side

**Responsible role:** operator

**Instruction:**
Identify the induct side of the hospital station. The source identifies the induct side as the left side of the station.

**Expected result:**
The operator has identified the left-side induct area of the hospital station.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station view showing the tote handling area and the left-side induct location.*


**Stop or Escalate If:**

* Stop if the induct side cannot be confidently identified from the source-supported station context.

---

### Step 2 — Place the tote on the induct side

**Responsible role:** operator

**Instruction:**
If the tote is going back into the system, place the tote on the induct side of the hospital station.

**Expected result:**
The tote is placed on the left-side induct area of the station.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*Hospital station tote handling area associated with placing a tote back into the system.*

![artifact_fig_4_31_hospital_hmi_add_tote_screen](assets/artifact_fig_4_31_hospital_hmi_add_tote_screen.png)

*Add Tote screen context indicating the tote is sent back into the system after it is positioned properly on the induct side.*


**Stop or Escalate If:**

* Stop if the tote is not intended to go back into the system.
* Escalate if the tote cannot be placed on the induct side and the source provides no alternate handling steps.

---

### Step 3 — Align the tote against the end stops

**Responsible role:** operator

**Instruction:**
Position the tote so it is flush against the end stops.

**Expected result:**
The tote is flush against the end stops on the induct side.

**Screens / Images:**

![artifact_page_92_image_2](assets/artifact_page_92_image_2.png)

*End-stop area and tote placement position used to verify the tote is flush against the stops.*


**Stop or Escalate If:**

* Escalate if the tote cannot be positioned flush against the end stops.
* Stop if the final tote alignment cannot be verified.

---

## Success Criteria

* The tote is placed on the hospital station induct side.
* The induct side used is the left side of the station.
* The tote is flush against the end stops.

## Failure Conditions

* The tote is placed on the wrong side of the station.
* The tote is not flush against the end stops.
* The source does not provide additional recovery steps if correct flush positioning cannot be achieved.

## Escalation Guidance

* Escalate if the tote cannot be positioned flush against the end stops.
* Escalate if the operator cannot determine the correct induct-side placement from the available source-supported station context.
* Use SME review because the source does not provide additional handling or recovery instructions for misalignment.

## Missing Details / Known Gaps

* The source does not provide a time estimate for this procedure.
* The source does not provide additional recovery or alternate handling steps if the tote cannot be positioned flush against the end stops.
* The source does not specify whether production stop or LOTO is required.
* The source does not provide a direct confirmation indicator that the tote has been accepted back into the system within this narrow physical-placement procedure.

## Source Lineage

- Candidate IDs: candidate_operator_place_return_tote_on_hospital_station_induct_side
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
