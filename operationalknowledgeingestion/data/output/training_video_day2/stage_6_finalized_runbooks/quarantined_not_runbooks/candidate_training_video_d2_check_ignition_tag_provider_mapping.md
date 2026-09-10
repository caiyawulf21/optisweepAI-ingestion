# Verify Ignition tag provider mapping for OptiSweep communication (SYS1 → tags → AvevaTest)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_verify_ignition_tag_provider_mapping_optsweep_sys1_to_avevatest_v1` |
| Title | Verify Ignition tag provider mapping for OptiSweep communication (SYS1 → tags → AvevaTest) |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `wcs_api_responsiveness` |
| Access Surface | `wcs_sql`, `rms_ui` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `mapping_abnormal` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Verify that the Ignition tag provider mapping contains the expected station/hospital tag namespaces (GLDStation* and Hospital1, plus TipperStation* entries with the documented suffix naming) and that SYS1’s metric-to-tag conversion is reflected by the presence of the tags AvevaTest is expected to read.

## When To Use

Use when you need to confirm that OptiSweep communication is using the documented Ignition tag provider mapping and that SYS1 metrics are converted into tags that AvevaTest reads.

## Do Not Use For

* Do not use this procedure as a substitute for deeper tag provider/mapping configuration troubleshooting if the expected mapped tag namespaces are missing; escalate to the appropriate tag provider/mapping configuration support procedure.

## Access Or Tools Needed

* Ignition tag browser/tree access
* Ability to view tag names/namespaces such as GLDStation1a/1b, GLDStation2a/2b, Hospital1, and TipperStation*

## Related Operational Context

* ctx_training_video_tag_provider_mapping_v1
* ctx_training_video_sys1_metric_conversion_v1
* ctx_training_video_ignition_tag_tree_reference_v1
* ctx_training_video_station_tag_naming_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0040_but_i_hate_it_this_is_primary_03_02_40_500](assets/bc5e79eb1b97586c.jpg)

*Ignition tag tree/tag provider mapping slide showing expected namespaces (GLDStation*, Hospital1, TipperStation* with suffix naming) and the SYS1 → tags → AvevaTest concept.*

## Procedure Steps

### Step 1 — Open the Ignition tag browser/tree and locate the expected station/hospital tag namespaces

**Responsible role:** L2_support

**Instruction:**
In the Ignition tag browser/tree, locate the tag namespace entries shown in the source for station/hospital mapping, including GLDStation* entries (e.g., GLDStation1a/GLDStation1b and GLDStation2a/GLDStation2b), Hospital1, and TipperStation* entries with the documented suffix naming (e.g., 1a/1b, 2a/2b, etc.).

**Expected result:**
The Ignition tag tree contains the mapped station/hospital tag namespaces shown in the source (GLDStation* and Hospital1, plus TipperStation* entries with the documented suffix naming).

**Stop or Escalate If:**

* Expected mapped tag namespaces from the source (e.g., GLDStation1b / GLDStation2a / GLDStation2b / Hospital1 / TipperStation* nodes) are not present in the Ignition tag tree where they should be mapped.

---

### Step 2 — Confirm SYS1 metric-to-tag conversion is reflected by the presence of AvevaTest-readable tags

**Responsible role:** L2_support

**Instruction:**
Using the Ignition tag browser/tree, verify that the tags implied by the SYS1 → tags → AvevaTest concept are present under the mapped station/hospital namespaces (GLDStation* / Hospital1 / TipperStation*). Treat the presence of these tags as evidence that SYS1’s metrics are being converted into tags AvevaTest can read.

**Expected result:**
The SYS1→tags→AvevaTest mapping concept is reflected by the presence of the tags AvevaTest is expected to read under the Ignition mapping.

**Stop or Escalate If:**

* Expected mapped tag namespaces from the source (e.g., GLDStation1b / GLDStation2a / GLDStation2b / Hospital1 / TipperStation* nodes) are not present in the Ignition tag tree where they should be mapped.
* Do not proceed with configuration changes based only on this training segment; use deeper support procedures for tag provider/mapping configuration if needed.

---

## Success Criteria

* Ignition tag tree shows the mapped station/hospital namespaces from the source: GLDStation* (including GLDStation1b, GLDStation2a, GLDStation2b), Hospital1, and TipperStation* entries with the documented suffix naming.
* The SYS1 → tags → AvevaTest mapping concept is reflected by the presence of the expected tags AvevaTest is expected to read under the Ignition mapping.

## Failure Conditions

* One or more expected mapped namespaces (GLDStation1b / GLDStation2a / GLDStation2b / Hospital1 / TipperStation* nodes) are missing from the Ignition tag tree where they should be mapped.
* SYS1 → tags → AvevaTest mapping concept cannot be supported because the expected tags are not present under the Ignition mapping.

## Escalation Guidance

* If expected mapped tag namespaces are missing or not present where the source indicates they should be mapped, stop and escalate to deeper tag provider/mapping configuration support procedures. Do not proceed with configuration changes based only on this segment.

## Missing Details / Known Gaps

* The source does not provide explicit Ignition navigation/click-path steps (menus/Designer vs web view). This runbook therefore focuses on locating the expected tag namespaces in the Ignition tag browser/tree rather than prescribing UI navigation.

## Source Lineage

- Candidate IDs: candidate_training_video_d2_check_ignition_tag_provider_mapping
- Source ID: `training_video_day2`
- Source Type: `training_video`
