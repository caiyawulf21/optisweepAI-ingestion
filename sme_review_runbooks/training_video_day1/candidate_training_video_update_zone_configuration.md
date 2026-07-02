# Modify Zone Settings on the Zone Config Aveva API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_modify_zone_settings_on_the_zone_config_aveva_api_page_v1` |
| Title | Modify Zone Settings on the Zone Config Aveva API Page |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | No |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Update Zone Configuration function on the Zone Config Aveva API page to review current lane-to-zone configuration information and modify supported zone settings when operational needs require a configuration change.

## When To Use

Use when zone settings need to be modified through the Zone Config Aveva API page to adapt operations based on system needs or changing requirements, and when the current lane assignments, respective zones, and processing sequence numbers need to be reviewed as part of that change.

## Do Not Use For

* Do not use when the required zone setting change is unclear from the source.
* Do not use if the page does not allow the intended modification.
* Do not use if the updated configuration cannot be verified from the displayed information.

## Safety And Operational Notes

* This procedure is not marked support-safe because it changes configuration that may affect operations.
* The source does not define safeguards, approval requirements, or rollback steps for zone configuration changes.
* Stop and escalate if the intended change is unclear or cannot be verified from the page.

## Access Or Tools Needed

* Access to the Zone Config Aveva API page
* Update Zone Configuration function

## Related Operational Context

* ctx_training_video_zone_config_aveva_api_page_v1
* ctx_training_video_update_zone_configuration_v1

## Procedure Steps

### Step 1 — Open the Zone Config Aveva API page

**Responsible role:** L2_support

**Instruction:**
Open or navigate to the Zone Config Aveva API page.

**Expected result:**
The Zone Config Aveva API page is displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0071_how_did_you_get_to_the_primary_02_24_46_500](assets/8f63c893394861e4.jpg)

*Zone Config Aveva API page title and the available configuration functions shown on the slide.*


**Stop or Escalate If:**

* The Zone Config Aveva API page is not available.
* The displayed page does not match the Zone Config Aveva API page.

---

### Step 2 — Review current lane and zone configuration

**Responsible role:** L2_support

**Instruction:**
Review the current lane assignments, respective zones, and processing sequence numbers shown on the page before making changes.

**Expected result:**
The current lane assignments, zones, and processing sequence numbers are visible and understood before modification.

**Screens / Images:**

![artifact_training_video_training_video_day1_0071_how_did_you_get_to_the_primary_02_24_46_500](assets/8f63c893394861e4.jpg)

*Overview content showing lane assignments, respective zones, and processing sequence numbers.*


**Stop or Escalate If:**

* The current lane assignments, zones, or processing sequence numbers cannot be reviewed from the page.
* The required zone setting change is unclear from the source.

---

### Step 3 — Locate the Update Zone Configuration function

**Responsible role:** L2_support

**Instruction:**
Locate the Update Zone Configuration function on the page.

**Expected result:**
The Update Zone Configuration function is identified on the Zone Config Aveva API page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0071_how_did_you_get_to_the_primary_02_24_46_500](assets/8f63c893394861e4.jpg)

*The Update Zone Configuration function on the Zone Config Aveva API page.*


**Stop or Escalate If:**

* The Update Zone Configuration function is not available on the page.
* The page does not allow the intended modification.

---

### Step 4 — Modify the zone settings

**Responsible role:** L2_support

**Instruction:**
Use the Update Zone Configuration function to modify the zone settings supported by the page.

**Expected result:**
The intended zone settings are modified through the Update Zone Configuration function.

**Screens / Images:**

![artifact_training_video_training_video_day1_0071_how_did_you_get_to_the_primary_02_24_46_500](assets/8f63c893394861e4.jpg)

*The Update Zone Configuration function referenced on the Zone Config Aveva API page slide.*


**Stop or Escalate If:**

* The required zone setting change is unclear from the source.
* The page does not allow the intended modification.

---

### Step 5 — Verify the updated configuration

**Responsible role:** L2_support

**Instruction:**
Verify that the updated configuration reflects the intended zone settings for the affected lanes.

**Expected result:**
The displayed configuration reflects the intended zone settings for the affected lanes.

**Screens / Images:**

![artifact_training_video_training_video_day1_0071_how_did_you_get_to_the_primary_02_24_46_500](assets/8f63c893394861e4.jpg)

*Displayed lane assignments, zones, and processing sequence numbers after the change.*


**Stop or Escalate If:**

* The updated configuration cannot be verified from the displayed information.
* The displayed settings do not reflect the intended change.

---

## Success Criteria

* The Zone Config Aveva API page is accessed successfully.
* Current lane assignments, respective zones, and processing sequence numbers are reviewed before the change.
* The Update Zone Configuration function is located and used.
* The intended zone settings for the affected lanes are reflected in the displayed configuration.

## Failure Conditions

* The Zone Config Aveva API page cannot be accessed or does not display as expected.
* Current configuration details cannot be reviewed from the page.
* The required zone setting change is unclear from the source.
* The page does not allow the intended modification.
* The updated configuration cannot be verified from the displayed information.

## Escalation Guidance

* Stop and escalate if the required zone setting change is unclear from the source.
* Escalate if the page does not allow the intended modification.
* Escalate if the updated configuration cannot be verified from the displayed information.

## Missing Details / Known Gaps

* The source does not provide exact navigation steps to reach the Zone Config Aveva API page.
* The source does not identify the exact editable fields or controls within Update Zone Configuration.
* The source does not describe save, submit, confirm, or rollback actions.
* The source does not define permissions, approvals, or role boundaries beyond inferred support ownership.
* The source does not provide validation criteria beyond reviewing displayed configuration information.
* The source does not state whether production must be stopped before making this change.
* The source does not provide timing estimates for completing the procedure.

## Source Lineage

- Candidate IDs: candidate_training_video_update_zone_configuration
- Source ID: `training_video_day1`
- Source Type: `training_video`
