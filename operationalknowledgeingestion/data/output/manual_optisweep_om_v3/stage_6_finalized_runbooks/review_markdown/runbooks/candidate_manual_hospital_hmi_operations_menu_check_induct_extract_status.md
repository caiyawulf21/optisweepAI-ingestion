# Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_hospital_hmi_operations_menu_induct_extract_status_v1` |
| Title | Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages |
| Procedure Type | `diagnostic` |
| Primary Role | `operator` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `hospital_diversion` |
| Access Surface | `hospital_hmi` |
| Audience Roles | `operator` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Hospital HMI / lane UI Operations Menu screen to read the WCS-fed induct and extract position fields (AGV#, Tote ID, Bar Code, Status). Confirm the Status messages explain why the tote is there and what station operator menu/action to use.

## When To Use

When a tote arrives at the hospital station and you need to determine what tote/AGV is at the induct and extract positions and what the WCS status message requires the station operator to do next.

## Access Or Tools Needed

* Hospital HMI / lane UI (Hospital station Operations Menu screen)

## Related Operational Context

* ctx_manual_hospital_hmi_operations_screen_v1
* ctx_manual_hospital_induct_position_fields_v1
* ctx_manual_hospital_extract_position_fields_v1
* ctx_manual_hospital_wcs_status_messages_v1

## Visual References

![artifact_fig_4_30_hospital_hmi_operations_screen](assets/58e2c340dd4fc6cc.png)

*Hospital HMI Operations Menu screen showing read-only Induct Position and Extract Position panels (AGV#, Tote ID, Bar Code, Status).*

## Procedure Steps

### Step 1 — Open Hospital HMI Operations Menu and locate Induct Position / Extract Position sections

**Responsible role:** operator

**Instruction:**
On the Hospital HMI / lane UI, navigate to the Operations Menu screen that contains the "Induct Position" and "Extract Position" sections.

**Expected result:**
The screen shows both "Induct Position" and "Extract Position" sections.

---

### Step 2 — Read Induct Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Induct Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Expected result:**
The "Induct Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

**Stop or Escalate If:**

* Induct Position Status is missing/blank.
* Induct Position Status does not provide explanation/action guidance (why the tote is there and what menu/action to use).

---

### Step 3 — Read Extract Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Extract Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Expected result:**
The "Extract Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

**Stop or Escalate If:**

* Extract Position Status is missing/blank.
* Extract Position Status does not provide explanation/action guidance (why the tote is there and what menu/action to use).

---

### Step 4 — Confirm both Status messages are present and provide WCS explanation/action guidance

**Responsible role:** operator

**Instruction:**
Verify that the "Induct Position" Status and "Extract Position" Status messages are present and written as messages received from the WCS that explain why the tote is there and what menu/action the station operator needs to use.

**Expected result:**
Both Status fields contain non-blank WCS messages that provide explanation and action/menu guidance.

**Stop or Escalate If:**

* Induct Position Status is missing/blank or lacks explanation/action guidance.
* Extract Position Status is missing/blank or lacks explanation/action guidance.

---

## Success Criteria

* Induct Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
* Extract Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
* Both Status messages explain why the tote is there and what menu/action the station operator needs to use.

## Failure Conditions

* Induct Position Status is blank/missing.
* Extract Position Status is blank/missing.
* Either Status message does not provide explanation/action guidance (why the tote is there and what menu/action to use).

## Escalation Guidance

* If either position’s Status message is missing/blank or does not provide explanation/action guidance, stop and escalate for support.

## Missing Details / Known Gaps

* The candidate does not provide specific button-by-button navigation steps within the Hospital HMI to reach the Operations Menu screen; it only names the screen and required sections.

## Source Lineage

- Candidate IDs: candidate_manual_hospital_hmi_operations_menu_check_induct_extract_status
- Source ID: `manual_optisweep_om_v3`
- Source Type: `manual`
