# Apidog / WCS API recovery of hospital tote and AGV state

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_apidog_wcs_api_recovery_hospital_tote_agv_state_v1` |
| Title | Apidog / WCS API recovery of hospital tote and AGV state |
| Procedure Type | `recovery` |
| Primary Role | `L2_support` |
| Supporting Roles | `L1_support`, `operator` |
| Support Safe | Yes |
| Capability Tags | `agv_physical_recovery`, `tote_lifecycle_state`, `wcs_api_responsiveness` |
| Access Surface | `apidog`, `wcs_api`, `tipper_hmi`, `hospital_hmi`, `rms_ui` |
| Audience Roles | `L1_support`, `L2_support`, `operator` |
| Failure Pattern Tags | `tote_error_noread_or_mismatch`, `robot_task_or_command_stuck` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Source-specific recovery procedure for UPS Haslet TX (TXRTH) using the Apidog / WCS API client, Tipper HMI / WebVisu / VISU, Hospital HMI / lane UI, and live AGV status. The incident records removal of an inducted tote, removal of disconnected tote 51 associated with AGV 1555012, removal of affected AGVs, and subsequent restoration of movement and hospital tote handling. Exact API requests and AGV controls are not documented and require SME review before operational publication.

## When To Use

Use for the UPS Haslet TX (TXRTH) hospital tote-flow condition when an inducted tote is preventing movement or a disconnected tote remains associated with an AGV, and recovery must be coordinated through the Apidog / WCS API client with live confirmation on the Tipper HMI / WebVisu / VISU, Hospital HMI / lane UI, or RMS / fleet status UI.

## Do Not Use For

* Do not use when the tote identity, AGV identity, required API action, or live API result cannot be confirmed.
* Do not use as a published procedure for AGV removal or recovery until the required Apidog / WCS API controls are documented and reviewed.

## Safety And Operational Notes

* When operators are not present at the tippers, the Tipper HMI / WebVisu / VISU station should be placed on pause during recovery so totes do not continue routing to the hospital.
* Do not guess an endpoint, request, tote identity, or AGV control when it cannot be confirmed on the live Apidog / WCS API client.

## Access Or Tools Needed

* Apidog / WCS API client
* OptiSweep / WCS API
* Tipper HMI / WebVisu / VISU
* Hospital HMI / lane UI
* RMS / fleet status UI
* Live AGV and tote status

## Procedure Steps

### Step 1 — Pause the Tipper HMI / WebVisu / VISU station

**Responsible role:** operator

**Instruction:**
Coordinate with the site and place the station on pause on the Tipper HMI / WebVisu / VISU when operators are not present at the tippers.

**Expected result:**
The Tipper HMI / WebVisu / VISU shows the station in a paused state, or the site confirms that the station has been paused.

**Stop or Escalate If:**

* Stop recovery if the station cannot be placed on pause or its paused state cannot be confirmed.

---

### Step 2 — Remove the inducted tote through the Apidog / WCS API client

**Responsible role:** L1_support

**Instruction:**
In the Apidog / WCS API client, locate and execute only the incident-supported action for removal of the confirmed inducted tote. Confirm the live API response before proceeding.

**Expected result:**
The Apidog / WCS API client returns a live result showing that the confirmed inducted tote was removed.

**Stop or Escalate If:**

* Stop if the inducted tote identity or the live removal result cannot be confirmed.
* Do not guess an endpoint or request body.

---

### Step 3 — Remove disconnected tote 51 through the Apidog / WCS API client

**Responsible role:** L1_support

**Instruction:**
In the Apidog / WCS API client, confirm tote 51 and its association with AGV 1555012, then perform only the documented incident-supported removal action and inspect the live result.

**Expected result:**
The Apidog / WCS API client returns a live result showing that tote 51 was removed.

**Stop or Escalate If:**

* Stop if tote 51 or AGV 1555012 cannot be confirmed on the live Apidog / WCS API client.
* Do not remove an unconfirmed tote.

---

### Step 4 — Remove affected AGVs from the flow through the Apidog / WCS API client

**Responsible role:** L2_support

**Instruction:**
Using only the documented site/support control on the Apidog / WCS API client, review and remove the confirmed affected AGVs from the flow. The incident identifies AGVs 1542188 and 1555028 and states that additional AGVs were also taken out. Corroborate the resulting AGV state on the RMS / fleet status UI.

**Expected result:**
The Apidog / WCS API client and RMS / fleet status UI show the confirmed affected AGVs removed from the flow or no longer blocking the hospital process.

**Stop or Escalate If:**

* Stop if the required AGV control or affected AGV identity cannot be confirmed.
* Escalate for L2/L3 review if an AGV remains in a blocking state or the documented control is unavailable.

---

### Step 5 — Verify recovery on the Apidog / WCS API client and live site surfaces

**Responsible role:** L1_support

**Instruction:**
Check the live movement and tote state on the Apidog / WCS API client or related live status surface. Coordinate with the site to verify on the Hospital HMI / lane UI that totes can be added and removed, and confirm that the robots have been re-added and are running.

**Expected result:**
Live status shows movement has resumed, the site confirms that the hospital can add and remove totes, and the site confirms that the robots are re-added and running.

**Stop or Escalate If:**

* Escalate if the system does not resume movement.
* Escalate if the hospital still cannot add and remove totes.
* Escalate if the robots cannot be re-added or are not running.

---

## Success Criteria

* The inducted tote removal is confirmed by a live Apidog / WCS API result.
* Tote 51 associated with AGV 1555012 is removed and no longer present as a disconnected tote.
* Confirmed affected AGVs are no longer blocking the hospital flow.
* System movement resumes.
* The site can add and remove totes at the hospital.
* The robots are re-added and back up and running.

## Failure Conditions

* The required API request, endpoint, tote identity, AGV identity, or live result cannot be confirmed.
* The inducted tote or tote 51 remains in the blocking or disconnected state.
* Affected AGVs remain in a blocking state or cannot be removed using the documented control.
* System movement does not resume.
* The hospital cannot add or remove totes.
* Robots cannot be re-added or remain not running.

## Escalation Guidance

* Stop and escalate for support review when the required API action, tote identity, AGV identity, or live result is not confirmed.
* Escalate to L2/L3 support for undocumented or unavailable AGV removal controls.
* Escalate if system movement, hospital tote add/remove capability, or robot operation is not restored after the documented incident-supported actions.

## Missing Details / Known Gaps

* Exact Apidog / WCS API endpoint names are not provided.
* Exact API request methods, parameters, request bodies, and response examples are not provided.
* The exact live Apidog / WCS API control for removing AGVs is not provided.
* The complete list of additional AGVs removed during the incident is not provided.
* No incident artifact IDs or usable screenshots are available for the requested API and AGV-state visual references.
* The incident does not establish a single confirmed root cause; suspected AGV/tote association issues remain incident context.

## Source Lineage

- Candidate IDs: candidate_incident_223554_api_tote_agv_recovery
- Source ID: `source_case_223554`
- Source Type: `incident_case`
