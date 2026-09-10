# Use the Zone Config Aveva API page to view lane zone assignments and (if needed) update zone configuration

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_use_zone_config_aveva_api_page_lane_zone_assignments_v1` |
| Title | Use the Zone Config Aveva API page to view lane zone assignments and (if needed) update zone configuration |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `zone_config_state` |
| Access Surface | `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Zone Config Aveva API page to view the current lane-to-zone assignments and processing sequence numbers via “Get Zone Configuration.” If the interface is being used for operational flexibility, use “Update Zone Configuration” to modify zone settings, noting that zone configuration changes are generally not used because zones are described as “equal zones.”

## When To Use

When you need visibility into how lanes are assigned to zones and what processing sequence numbers are configured, using the Zone Config Aveva API page’s “Get Zone Configuration” function. Optionally, when the interface is being used to modify zone settings for operational flexibility via “Update Zone Configuration.”

## Do Not Use For

* Do not rely on zone configuration updates for operational behavior unless the system is known to support/require them; the source states zone configuration changes are generally not used because zones are “equal zones.”

## Access Or Tools Needed

* Zone Config Aveva API page interface
* “Get Zone Configuration” function
* “Update Zone Configuration” function

## Related Operational Context

* ctx_training_video_zone_config_interface_overview_v1
* ctx_training_video_zone_config_get_configuration_v1
* ctx_training_video_zone_config_update_configuration_v1
* ctx_training_video_zone_config_legacy_equal_zones_v1

## Procedure Steps

### Step 1 — Open the Zone Config Aveva API page interface

**Responsible role:** L2_support

**Instruction:**
Open the Zone Config Aveva API page interface.

**Expected result:**
The Zone Config Aveva API page is displayed with the interface elements for viewing lane assignments/zones/processing sequence numbers and the “Get Zone Configuration” and “Update Zone Configuration” functions.

---

### Step 2 — Use “Get Zone Configuration” to fetch the current configuration of all lanes

**Responsible role:** L2_support

**Instruction:**
Use the “Get Zone Configuration” function to fetch the current configuration of all lanes.

**Expected result:**
The interface returns the current configuration of all lanes, providing visibility into how each lane is set up within the system.

**Stop or Escalate If:**

* If the interface does not return lane configuration data for “all lanes,” stop and escalate to support.

---

### Step 3 — Verify lane assignments, each lane’s zone, and processing sequence numbers in the results

**Responsible role:** L2_support

**Instruction:**
On the “Get Zone Configuration” results, verify that the interface shows lane assignments, each lane’s respective zone, and the processing sequence numbers.

**Expected result:**
You can observe lane assignments mapped to zones and see processing sequence numbers for those lanes in the results display.

---

### Step 4 — If needed, use “Update Zone Configuration” to modify zone settings

**Responsible role:** L2_support

**Instruction:**
If the interface is being used to change settings, use the “Update Zone Configuration” function to modify zone settings.

**Expected result:**
The “Update Zone Configuration” function is available and can be used to modify zone settings via the interface.

**Stop or Escalate If:**

* Because the source states zone configuration changes are generally not used due to “equal zones,” avoid relying on updates for operational behavior unless the system is known to support/require them.

---

### Step 5 — Confirm update intent aligns with “equal zones” guidance

**Responsible role:** L2_support

**Instruction:**
Confirm that the update aligns with the intended zone configuration behavior described in the source (zones are described as “equal zones” such that configuration changes are generally not used).

**Expected result:**
You determine that the planned update is consistent with the guidance that zone configuration changes are generally not used because zones are “equal zones.”

**Stop or Escalate If:**

* If you cannot justify the update against the “equal zones” guidance, stop and escalate to support.

---

## Success Criteria

* “Get Zone Configuration” returns the current configuration of all lanes.
* The results show lane assignments, each lane’s respective zone, and processing sequence numbers.
* If “Update Zone Configuration” is used, the update intent is consistent with the guidance that zone configuration changes are generally not used because zones are “equal zones.”

## Failure Conditions

* “Get Zone Configuration” does not return lane configuration data for “all lanes.”
* Results do not display lane assignments, zones, and processing sequence numbers as expected by the interface.

## Escalation Guidance

* If the interface does not return lane configuration data for “all lanes,” stop and escalate to support.

## Missing Details / Known Gaps

* The source does not provide explicit navigation/authentication steps to reach the Zone Config Aveva API page interface.
* The source does not provide field-level names/labels for the editable zone settings in “Update Zone Configuration,” nor the exact update workflow (inputs, validation, and confirmation outputs).

## Source Lineage

- Candidate IDs: candidate_training_video_zone_config_aveva_api_get_update
- Source ID: `training_video_day1`
- Source Type: `training_video`
