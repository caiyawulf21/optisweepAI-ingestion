# Stage 5 Runbook Candidate Review - Case 218550

## Summary

| Metric | Value |
| --- | --- |
| Candidates | 1 |
| Validation errors | 0 |
| Warnings | 0 |
| Dropped candidates | 0 |
| Deduped candidates | 0 |
| Candidates with artifacts | 1 |
| Candidates with events | 1 |

## Counts

### Procedure Types

| Type | Count |
| --- | --- |
| recovery | 1 |

### Roles

| Role | Count |
| --- | --- |
| operator | 1 |

## Candidate Index

| Candidate | Type | Role | Confidence | Artifacts | Events | Summary |
| --- | --- | --- | --- | --- | --- | --- |
| candidate_incident_218550_hospital_hmi_acknowledge_retry | recovery | operator | medium | artifact_incident_218550_page_012_nested_image_01 | incident_218550_event_024, incident_218550_event_025, incident_218550_event_026 | Use the Hospital HMI / lane UI to acknowledge the displayed fault, retry the operation, confirm that the affected tote is tote 28, and verify that the site reports the condition... |

## Candidate Details

### Hospital HMI / lane UI fault acknowledge-and-retry check

| Field | Value |
| --- | --- |
| Candidate ID | candidate_incident_218550_hospital_hmi_acknowledge_retry |
| Goal | Clear and validate a reported HMI fault associated with tote 28 without unplugging the HMI. |
| Type | recovery |
| Role | operator |
| Confidence | medium |
| Status | needs_review |

**Summary:** Use the Hospital HMI / lane UI to acknowledge the displayed fault, retry the operation, confirm that the affected tote is tote 28, and verify that the site reports the condition is clear.

#### Rough Steps

- Open the Hospital HMI / lane UI and confirm that the fault is displayed; do not unplug the HMI. [Image support needed: HMI screen showing the fault condition with the red header and green list elements described in the incident artifact.]
- Select the HMI acknowledge control, then retry the operation. [Image support needed: Hospital HMI / lane UI showing the acknowledge control and the post-acknowledge retry state.]
- Confirm that the tote at the hospital station is tote 28 and verify that the site reports the condition as all good. [Image support needed: HMI or lane UI showing tote ID 28 and the cleared or normal state.]

**Expected result:** The HMI fault is acknowledged and the retry succeeds; the affected tote is confirmed as 28 and the site reports that everything is good.

#### Failure Or Escalation Notes

- Do not unplug the HMI as a troubleshooting action.
- Stop and escalate for further support if the fault remains after acknowledge-and-retry, tote 28 cannot be confirmed, or the site cannot report an all-good state.
- The packet also identifies a stuck-task visibility limitation on this HMI, but it does not provide a reusable stuck-task recovery sequence.

#### Access Or Tools Needed

- Hospital HMI / lane UI

#### Extraction Notes

- The acknowledge-and-retry instruction and successful tote 28 validation are source-supported.
- The packet uses 'hospital' in the incident messages while ingestion metadata identifies UPS Haslet TX (TXRTH); ingestion site metadata is authoritative and the location wording remains ambiguous.
- The embedded HMI text is largely unreadable, so image-supported details are limited to the described HMI layout and surrounding chat evidence.
