# Use the Zone Config Aveva API page to update lane zone settings

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_zone_config_aveva_api_page_update_zone_configuration_v1` |
| Title | Use the Zone Config Aveva API page to update lane zone settings |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `zone_config_state` |
| Access Surface | None |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

A support user can use the Zone Config Aveva API page’s “Update Zone Configuration” function to modify zone settings for lanes, so operations can adapt based on system needs or changing requirements.

## When To Use

Use when you need to modify lane zone settings using the Zone Config Aveva API page’s “Update Zone Configuration” function so the system’s lane configuration can adapt to system needs or changing requirements.

## Access Or Tools Needed

* Zone Config Aveva API page interface
* “Update Zone Configuration” control/button
* Editable lane zone settings fields/controls on that page

## Related Operational Context

* ctx_training_video_zone_config_aveva_api_page_v1
* ctx_training_video_update_zone_configuration_v1

## Procedure Steps

### Step 1 — Open the Zone Config Aveva API page interface

**Responsible role:** L2_support

**Instruction:**
Open the Zone Config Aveva API page interface.

**Expected result:**
The Zone Config Aveva API page is displayed with lane assignments, their respective zones, and processing sequence numbers visible.

---

### Step 2 — Locate the “Update Zone Configuration” control/button

**Responsible role:** L2_support

**Instruction:**
Locate the control/button labeled “Update Zone Configuration” on the Zone Config Aveva API page.

**Expected result:**
The “Update Zone Configuration” control/button is visible on the page.

---

### Step 3 — Modify lane zone settings in the editable fields/controls

**Responsible role:** L2_support

**Instruction:**
Use the page’s lane zone settings fields/controls to modify the zone settings for the relevant lanes.

**Expected result:**
The lane zone settings fields/controls reflect the new values you entered for the relevant lanes.

---

### Step 4 — Click “Update Zone Configuration” to apply changes

**Responsible role:** L2_support

**Instruction:**
Click “Update Zone Configuration” to apply the changes.

**Expected result:**
The update action is submitted via the “Update Zone Configuration” control.

**Stop or Escalate If:**

* If the update does not reflect on the page after clicking “Update Zone Configuration,” stop and escalate for deeper troubleshooting of the Aveva API update path.

---

### Step 5 — Confirm updated zone settings are reflected on the page

**Responsible role:** L2_support

**Instruction:**
Confirm the updated zone settings are reflected on the page (lane assignments/zones/processing sequence numbers as displayed).

**Expected result:**
The page reflects the modified lane zone configuration (lane assignments/zones/processing sequence numbers show the updated values).

**Stop or Escalate If:**

* If the update does not reflect on the page after clicking “Update Zone Configuration,” stop and escalate for deeper troubleshooting of the Aveva API update path.
* Do not proceed with repeated updates without confirming what changed on-screen.

---

## Success Criteria

* After clicking “Update Zone Configuration,” the Zone Config Aveva API page displays the updated lane zone settings (lane assignments/zones/processing sequence numbers as shown on the page).

## Failure Conditions

* “Update Zone Configuration” does not apply changes (updated values do not appear on the page).
* No confirmation/status is shown after clicking “Update Zone Configuration” (if the UI provides one).

## Escalation Guidance

* If the update does not reflect on the page after clicking “Update Zone Configuration,” stop and escalate for deeper troubleshooting of the Aveva API update path.

## Missing Details / Known Gaps

* The source packet does not provide concrete UI field names for the lane zone settings inputs/controls, nor the exact on-screen confirmation/status message text after clicking “Update Zone Configuration.”
* The source packet does not specify the exact refresh/verification mechanism (e.g., whether “Get Zone Configuration” must be used after update) or the exact UI labels for lane assignment/zone/processing sequence number fields.

## Source Lineage

- Candidate IDs: candidate_training_video_zone_config_aveva_api_update_zone_configuration
- Source ID: `training_video_day1`
- Source Type: `training_video`
