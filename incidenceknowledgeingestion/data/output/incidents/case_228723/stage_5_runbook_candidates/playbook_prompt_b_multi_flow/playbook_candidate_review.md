# Stage 5 Playbook Candidate Review - Case 228723

## Summary

| Metric | Value |
| --- | --- |
| Playbook candidates | 1 |
| Nodes | 6 |
| Nodes missing runbook placeholder | 0 |
| Validation errors | 0 |
| Warnings | 4 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 0 |
| Candidates with events | 0 |

## Confidence

| Confidence | Count |
| --- | --- |
| medium | 1 |

## Warnings

- playbook_candidate_incident_228723_zone_pairing_roster_anomaly node node_1 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228723_zone_pairing_roster_anomaly node node_2 (diagnostic_decision) is missing expects_capability
- playbook_candidate_incident_228723_zone_pairing_roster_anomaly node node_3 (branching_condition) is missing expects_capability
- playbook_candidate_incident_228723_zone_pairing_roster_anomaly node node_5 (validation_gate) is missing expects_capability

## Candidate Index

| Candidate | Confidence | Nodes | Events | Summary |
| --- | --- | --- | --- | --- |
| playbook_candidate_incident_228723_zone_pairing_roster_anomaly | medium | 6 |  | Use when a site reports that a zone cannot obtain a pair, AMRs are not behaving as expected, or replacement AMRs are routing to the hospital instead of supporting the affected w... |

## Candidate Details

### Zone pairing failure with abnormal AMR routing or roster state

| Field | Value |
| --- | --- |
| Candidate ID | playbook_candidate_incident_228723_zone_pairing_roster_anomaly |
| Goal | Confirm the observable pairing and fleet symptoms, determine whether the affected AMR roster or mapping state is abnormal, guide an authorized site-side isolation or removal decision when supported, and validate that normal operation returns. |
| Entry symptoms | A zone is unable to get a pair.; The ACB workflow is reported as down or unable to operate.; Replacement AMRs route to the hospital lane instead of supporting the affected zone.; An AMR is reported with low battery or is physically under a rack.; The site reports that AMR behavior remains abnormal after an attempted replacement. |
| Tentative internal patterns | Possible abnormal robot roster or mapping state after remove/add activity; Possible unassigned or unmapped AMR affecting pairing or task assignment; Possible residual physical or location state involving an AMR unable to reach charging; Possible routing or workflow diversion toward the hospital lane |
| Affected systems/components | ACB system; AMRs / AGVs; RMS; Hospital lane |
| Roles | L1_support, L2_support, L3_support, operator |
| Confidence | medium |
| Confidence reason | The packet contains a clear observable symptom pattern, a named RMS surface, repeated discussion of remove/add and mapping state, a source-supported site-side recovery action, and reported post-action stability. Confidence is limited because the RMS details are partly unreadable, the recovery was narrative rather than independently verified, and the source uses inconsistent ACB/ECB naming. |

**Summary:** Use when a site reports that a zone cannot obtain a pair, AMRs are not behaving as expected, or replacement AMRs are routing to the hospital instead of supporting the affected workflow.

#### Support User Language Examples

- Zone can't get a pair
- Nothing is pairing in the zone
- ACB is down
- AMRs are going to the hospital
- The replacement robots keep going to hospital
- We have a low-battery robot under the rack
- The robots were removed and added but it still isn't working
- The fleet is not taking tasks

#### Negative Or Absent Signals

- The source does not provide a confirmed service crash, API failure, or database error.
- The source does not independently confirm that low battery was the current cause; one support message described it as a possible initiating condition rather than the current cause.
- The RMS screenshot details are not sufficiently legible to establish exact status fields or error codes.
- Recovery was reported by site communication and short monitoring, not independently confirmed by readable live telemetry.

#### Nodes

| # | Type | Title | Intent | Expects | Runbook placeholder | Source-supported description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diagnostic_decision | Confirm zone pairing failure and abnormal AMR behavior | Determine whether the reported issue is an active zone pairing failure accompanied by abnormal AMR routing or inability to support the affected workflow. | aud:operator, aud:L1_support | Procedure needed to confirm with the site whether the affected zone is currently unable to get a pair, whether AMRs are routing to the hospital lane instead of the expected workflow, whether a low-battery or physically obstructed AMR is involved, and whether RMS shows the same abnormal fleet or pairing presentation; use generic affected-zone and reported-robot references rather than incident-specific identifiers. | The site reported inability to get a pair, AMRs going to the hospital, and an earlier low-battery AMR condition. RMS artifacts show status tables with abnormal-looking red entri... |
| 2 | diagnostic_decision | Determine whether AMR roster or mapping state is abnormal | Determine whether recent AMR replacement or remove/add activity left an AMR missing, unmapped, incorrectly rostered, or otherwise unable to receive the expected task. | aud:operator, aud:L1_support | Procedure needed to inspect the RMS fleet or robot status view for the affected AMR's roster membership, mapped or unmapped indication, location, and assignment-related abnormal state, and to compare the displayed state with the site's reported remove/add history without relying on incident-specific robot identifiers. | Support discussion proposed improper remove/add or RMS rostering as a possible explanation. Resolution text states that a robot was shown as not mapped, but the source does not... |
| 3 | branching_condition | Choose supported fleet-state recovery path | Choose whether the affected AMR should remain isolated from the active fleet under an authorized site procedure, or whether the evidence does not support that path. | aud:operator, aud:L2_support | Procedure needed to apply the decision rubric for an AMR shown as unmapped or incorrectly rostered, including comparison of RMS state with site physical confirmation and the safety and authorization criteria for any site-side isolation or remove-from-system action; do not encode exact remove/add steps here. | The source records site-side removal of a robot from the system and placement on charger after discussion of roster and mapping concerns. It does not provide a complete or repea... |
| 4 | procedure_reference | Perform authorized AMR isolation or removal action | Carry out the source-supported high-level recovery action when the affected AMR is linked to the abnormal roster or mapping state and the authorized site procedure permits it. | aud:operator, aud:L2_support | Procedure needed for authorized site-side AMR isolation or removal from active system participation, including physical safety prerequisites, charging or holding-state requirements, RMS state confirmation, and role limits; the procedure must define the approved remove/add handling without embedding exact operational steps here. | The source-supported recovery was site removal of an AMR from the system followed by placement on charger. The source does not document exact steps and does not establish that t... |
| 5 | validation_gate | Validate restored pairing and stable AMR operation | Confirm that the affected workflow has recovered after the authorized fleet-state action and remains operational during observation. | aud:operator, aud:L1_support | Procedure needed to validate the affected zone's pairing behavior through site observation, confirm expected AMR routing and fleet state in RMS, and define a short stability-monitoring period before declaring recovery; include criteria for failed validation and evidence capture without prescribing exact screen navigation. | The source reports that operation resumed after robot removal and remained operational during approximately 10 minutes of monitoring, while acknowledging that the recovery was r... |
| 6 | escalation_gate | Stop if the supported fleet-state path does not restore operation | Stop and hand off when the roster or mapping evidence is inconclusive, the authorized recovery action cannot be performed safely, or validation fails after the supported path. | aud:L2_support, aud:L3_support | Procedure needed to prepare a technical escalation handoff with the site symptom description, RMS roster or mapping evidence, physical AMR state, remove/add or isolation actions attempted, pairing and hospital-routing observations, monitoring results, and explicit stop or safety conditions. | The incident contains ambiguous RMS evidence, unresolved symptoms after an earlier remove/add attempt, and reported recovery that required monitoring. These support a stop condi... |

#### Extraction Notes

- source_package.site_location is empty, so no authoritative ingestion site, site code, or site location metadata was available to populate.
- The canonical incident record identifies the site as UPS Fort Worth, TX (Haslet), but this is treated as source incident context rather than authoritative source_package.site_location metadata.
- The source alternates between ACB and ECB system naming in different sections; the candidate uses the source's more frequent ACB wording and records the inconsistency rather than resolving it.
- The RMS artifact is visibly relevant but has garbled OCR and unreadable detailed status values.
- The reported recovery is based on site and support messages plus short monitoring, not independent live telemetry.
- The source supports a tentative roster or mapping pattern, not a confirmed root cause.
