# Verify Divider Placement In The Z-Axis Cable Carrier

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_divider_placement_in_the_z_axis_cable_carrier_v1` |
| Title | Verify Divider Placement In The Z-Axis Cable Carrier |
| Procedure Type | `diagnostic` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Inspect the Z-Axis cable carrier to verify that dividers are present where applicable and positioned correctly between the cable and the air line so the air line does not contact the FFC. The source states dividers are included in every second link, several missing dividers are acceptable, and installed dividers should be fully to one side against the air line.

## When To Use

Use this procedure when inspecting the Z-Axis cable carrier condition or verifying whether divider placement matches the documented configuration in section 7.3.16.

## Do Not Use For

* Do not use this procedure to determine an exact required count of missing dividers beyond the source statement that several missing dividers are acceptable.
* Do not use this procedure as a replacement or repair procedure for the Z-Axis cable carrier.

## Safety And Operational Notes

* Use only the visual inspection criteria supported by the source.
* Do not infer a stricter divider quantity requirement than the source provides.
* Escalate if divider position cannot be verified or if the air line appears able to contact the FFC.

## Access Or Tools Needed

* Visual access to the Z-Axis cable carrier
* Figure 7-17 Cable Carrier

## Procedure Steps

### Step 1 — Locate the Z-Axis cable carrier

**Responsible role:** L1_support

**Instruction:**
Locate the Z-Axis cable carrier and visually inspect the cable carrier links.

**Expected result:**
The Z-Axis cable carrier is identified and its links are visible for inspection.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Use Figure 7-17 to identify the cable carrier assembly and the links where dividers are installed.*

![artifact_fig_3_4_tipper_components_left_tipper_shown](assets/artifact_fig_3_4_tipper_components_left_tipper_shown.png)

*Use Figure 3-4 to identify the Z-axis cable carrier location within the tipper components.*


**Stop or Escalate If:**

* Escalate if the divider position cannot be verified because the cable carrier cannot be clearly inspected.

---

### Step 2 — Identify divider locations in the links

**Responsible role:** L1_support

**Instruction:**
Identify the dividers between the cable and the air line in every second link.

**Expected result:**
Divider locations can be recognized in the links where they are intended to be installed.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Look for the divider location between the cable and air line in the cable carrier links.*


**Stop or Escalate If:**

* Escalate if divider position cannot be verified.

---

### Step 3 — Assess missing dividers against source allowance

**Responsible role:** L1_support

**Instruction:**
Check whether some dividers are missing and note that the source states it is acceptable for several of these dividers to be missing.

**Expected result:**
The observed condition is compared to the source statement that several missing dividers are acceptable.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Use the cable carrier figure as a visual reference while checking whether divider positions are populated or missing.*


**Stop or Escalate If:**

* Escalate if the condition cannot be verified without assuming an exact allowed number of missing dividers.

---

### Step 4 — Verify divider position against the air line

**Responsible role:** L1_support

**Instruction:**
Verify the installed dividers are all the way to one side against the air line.

**Expected result:**
Installed dividers are positioned fully to one side against the air line.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Inspect divider placement relative to the air line and confirm the divider is fully to one side against the air line.*


**Stop or Escalate If:**

* Escalate if divider position cannot be verified.
* Escalate if any installed divider is not all the way to one side against the air line.

---

### Step 5 — Confirm separation between air line and FFC

**Responsible role:** L1_support

**Instruction:**
Confirm the divider position prevents the air line from contacting the FFC.

**Expected result:**
The air line is kept from contacting the FFC by the divider placement.

**Screens / Images:**

![artifact_fig_7_17_cable_carrier](assets/artifact_fig_7_17_cable_carrier.png)

*Inspect the cable carrier routing to confirm divider placement keeps the air line separated from the FFC.*

![artifact_fig_7_14_flat_flex_cable](assets/artifact_fig_7_14_flat_flex_cable.png)

*Use the FFC figure as a reference for the flat-flex cable mentioned in the inspection criterion.*


**Stop or Escalate If:**

* Escalate if the air line appears able to contact the FFC.
* Escalate if divider position cannot be verified.

---

## Success Criteria

* The Z-Axis cable carrier can be visually inspected.
* Divider locations between the cable and air line in every second link are identifiable.
* Observed missing dividers are evaluated using only the source statement that several missing dividers are acceptable.
* Installed dividers are all the way to one side against the air line.
* The air line is prevented from contacting the FFC.

## Failure Conditions

* The cable carrier or divider positions cannot be clearly inspected.
* Divider position cannot be verified.
* An installed divider is not all the way to one side against the air line.
* The air line appears able to contact the FFC.
* The inspection would require inventing an exact allowed number of missing dividers not provided by the source.

## Escalation Guidance

* Escalate if divider position cannot be verified.
* Escalate if the air line appears able to contact the FFC.
* Do not declare failure solely from several missing dividers because the source states that several missing dividers are acceptable.
* Escalate for further review if the observed condition cannot be assessed without assuming details not stated in the source.

## Missing Details / Known Gaps

* The source packet does not provide an estimated inspection time.
* The source packet does not explicitly state whether production stop is required for this inspection.
* The source packet does not explicitly state whether LOTO is required for this inspection-only verification.
* The source packet does not provide a more specific acceptance threshold for how many dividers may be missing beyond stating that several missing dividers are acceptable.

## Source Lineage

- Candidate IDs: candidate_l1_verify_z_axis_cable_carrier_divider_position
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
