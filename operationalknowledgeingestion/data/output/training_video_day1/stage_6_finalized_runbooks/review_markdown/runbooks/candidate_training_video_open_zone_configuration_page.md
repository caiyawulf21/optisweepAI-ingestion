# Open the Zone Configuration Page From the Overall System Aveva API Page

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_open_the_zone_configuration_page_from_the_overall_system_aveva_api_page_v1` |
| Title | Open the Zone Configuration Page From the Overall System Aveva API Page |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Access the Zone configuration page from the Overall System Aveva API page. The source confirms that the Overall System Aveva API page contains a Zone configuration option that pops up the zone configuration page, but also notes that nobody uses it. This runbook covers page access only and does not authorize configuration changes.

## When To Use

Use when support personnel need to access the Zone configuration page from the Overall System Aveva API page and only page access is required.

## Do Not Use For

* Do not use this runbook to make configuration changes, because the source only confirms how to open the page.
* Do not use this runbook as evidence that the Zone configuration page is commonly used; the speaker states that nobody uses it.

## Safety And Operational Notes

* This source segment only supports opening the Zone configuration page.
* Do not perform configuration changes based on this source segment because it does not describe safe edit actions.

## Access Or Tools Needed

* Access to the Overall System Aveva API page
* Zone configuration control

## Related Operational Context

* ctx_training_video_overall_system_aveva_api_page_v1
* ctx_training_video_zone_configuration_reference_v1

## Procedure Steps

### Step 1 — Open the Overall System Aveva API page

**Responsible role:** L2_support

**Instruction:**
Open the Overall System Aveva API page.

**Expected result:**
The Overall System Aveva API page is displayed.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*Overall System Aveva API page with the Zone configuration entry visible among the listed options.*


**Stop or Escalate If:**

* Stop or escalate if the Overall System Aveva API page cannot be opened.
* Stop or escalate if the page does not show the expected Zone configuration option.

---

### Step 2 — Locate the Zone configuration control

**Responsible role:** L2_support

**Instruction:**
Locate the Zone configuration control on the Overall System Aveva API page.

**Expected result:**
The Zone configuration control is identified on the page.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The Zone configuration entry listed with other Overall System Aveva API page options.*


**Stop or Escalate If:**

* Stop or escalate if the Zone configuration control is missing from the page.
* Stop or escalate if the page layout does not match the source-supported view.

---

### Step 3 — Select Zone configuration

**Responsible role:** L2_support

**Instruction:**
Select Zone configuration to open the zone configuration page.

**Expected result:**
The zone configuration page opens.

**Screens / Images:**

![artifact_training_video_training_video_day1_0067_we_also_have_reset_metrics_which_primary_02_19_13_500](assets/ce4a613aa5f38e03.jpg)

*The Zone configuration control on the Overall System Aveva API page that is used to pop up the zone configuration page.*


**Stop or Escalate If:**

* Escalate if the zone configuration page does not open.
* Stop if further action would require configuration changes not supported by this source.

---

## Success Criteria

* The Overall System Aveva API page is opened.
* The Zone configuration control is located.
* Selecting Zone configuration opens the zone configuration page.

## Failure Conditions

* The Overall System Aveva API page cannot be accessed.
* The Zone configuration control is not visible on the page.
* The zone configuration page does not open after selection.

## Escalation Guidance

* Escalate if the zone configuration page does not open.
* Escalate if the Overall System Aveva API page does not show the expected Zone configuration option.
* Do not proceed into configuration changes based on this source because edit actions are not documented.

## Missing Details / Known Gaps

* The source does not describe how to navigate to the Overall System Aveva API page from other screens.
* The source does not provide any safe or approved actions within the Zone configuration page after it opens.
* The source does not provide timing estimates.
* The source does not define production stop or LOTO requirements for this access action.

## Source Lineage

- Candidate IDs: candidate_training_video_open_zone_configuration_page
- Source ID: `training_video_day1`
- Source Type: `training_video`
