# Restore ACB pairing/zone operation by reconciling roster/map state and validating recovery

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228723_acb_zone_pairing_and_roster_recovery` |
| Case ID | `228723` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- ACB system reported down or not functioning normally
- A zone reports it is unable to get a pair (pairing failure symptom)
- AMRs/AGVs appear to route abnormally (e.g., to the hospital lane) during the pairing issue

## Affected Systems

- ACB system
- AMRs / AGVs
- RMS
- WCS / OptiSweep (implied by roster/map and pairing checks)

## Nodes

### 1 — Confirm zone pairing failure and whether fleet/roster/map state is inconsistent (`diagnostic_decision`)

**Intent:** Determine whether the reported “unable to get a pair / ACB down” symptom aligns with pairing failure and whether roster/map state appears abnormal for the affected zone.

**Expects capability:** zone_pairing_state, device_roster_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.591, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1` (low, support, score=0.7728, boosted=1.0) — Check RMS fleet status for AGVs in shutdown queues and zone cycling
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1` (low, support, score=0.3, boosted=0.2982) — Verify Robot Location model fields and location types/statuses used by RMS orange locations
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).
- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): RMS and (if available) SSMS corroboration show normal pairing/zone state and coherent roster/map consistency for the affected zone (no suspected unmapped/mismapped robots contributing).
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Pairing failure (“unable to get a pair”) is corroborated and roster/map inconsistency exists (e.g., suspected robot missing/mismapped/not mapped) consistent with the incident pattern.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): RMS/SSMS evidence is insufficient or conflicting (pairing state/roster/map state cannot be clearly corroborated).
- `escalate` (observer=remote; tool=WCS/SSMS (read-only)): Significant system-down/instability is confirmed without pairing/roster evidence clarity, requiring deeper L3/L4 investigation beyond this template.

**Branches:**

- `unhealthy` → `node_2` when RMS/SSMS show pairing failure and/or roster/map inconsistency
- `healthy` → `node_3` when RMS/SSMS do not show pairing failure or roster/map inconsistency
- `escalate` → `node_4` when Unable to corroborate or evidence insufficient

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View (`proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`)</summary>

##### Runbook: Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View

- **Procedure ID:** `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`
- **Procedure Type:** `operation`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Geek Plus RMS Robot Selection web view to add a robot by robot ID or remove an existing robot, and confirm success messages after each action.

**When To Use:**
When you need to manage the Geek Plus RMS robot roster using the Robot Selection Add/Remove workflow and verify the on-screen success confirmations.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open Geek Plus RMS web application from an authorized network path

**Responsible role:** L1_support

**Instruction:**
From an OT network device, open the Geek Plus RMS web application using the site/RMS address. If you are supporting remotely, ensure you are authorized to use the UPS VPN through Zscaler and can reach the site/RMS address.

**Healthy condition:**
You can access the Geek Plus RMS web application from your current network authorization path.

**Expected result:**
The Geek Plus RMS web application loads successfully and you can navigate to the Robot Selection screen.

---

###### Step 2 — Navigate to the Robot Selection screen with Add Robot and Remove Robot controls

**Responsible role:** L1_support

**Instruction:**
In the Geek Plus RMS web application, navigate to the Robot Selection screen that contains the Robot ID entry field and the Add Robot and Remove Robot controls.

**Healthy condition:**
You can see the Robot ID entry area and the Add/Remove controls on the Robot Selection screen.

**Expected result:**
The Robot Selection screen is visible with the Robot ID entry field and the Add and Remove controls.

---

###### Step 3 — Add a robot by robot ID

**Responsible role:** L1_support

**Instruction:**
In the Robot ID entry field, enter the corresponding robot ID. (If the robot is already introduced, partial numeric entry may surface matching robots.) Click the "Add" button.

**Healthy condition:**
The UI shows the success confirmation for the Add action after clicking "Add".

**Expected result:**
A confirmation message appears indicating the robot was added successfully ("adding was successful" / "robot was added successfully").

---

###### Step 4 — Remove a robot by robot ID or by selecting it from the list

**Responsible role:** L1_support

**Instruction:**
Enter the corresponding robot ID in the Robot ID entry field or select the robot from the list shown for that ID. Click the "Remove" button.

**Healthy condition:**
The UI shows the success confirmation for the Remove action after clicking "Remove".

**Expected result:**
A confirmation message appears indicating the robot was removed successfully ("removal was successful" / "remove what was successful").

---

**Success Criteria:**

- After clicking "Add", the Robot Selection screen displays an "adding was successful" confirmation message.
- After clicking "Remove", the Robot Selection screen displays a "removal was successful" confirmation message.

**Failure Conditions:**

- No success confirmation appears after clicking "Add".
- No success confirmation appears after clicking "Remove".


</details>

<details><summary>Check RMS fleet status for AGVs in shutdown queues and zone cycling (`proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1`)</summary>

##### Runbook: Check RMS fleet status for AGVs in shutdown queues and zone cycling

- **Procedure ID:** `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI to verify that AGVs are held in shutdown queues (shutdown state), then cycle into their assigned zones (4 zones) after startup, consistent with the system state model described in the segment.

**When To Use:**
When you need to confirm that AGVs are in the shutdown state (shutdown queues) and then transition into their assigned zones (4 zones) after startup, using the live fleet status view in RMS.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI and view AGV roster/map

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV list/map view where you can see each AGV’s current state and/or location/zone assignment.

**Healthy condition:**
The RMS fleet status view is accessible and shows AGVs with state/location/zone information (enough to distinguish shutdown queues vs zone assignments).

**Expected result:**
You can see the AGV list/map view in RMS with each AGV’s current state and/or location/zone assignment visible.

---

###### Step 2 — Confirm AGVs are in shutdown queues (shutdown state)

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV list/map view, identify the relevant AGVs and confirm that their current state and/or location/zone assignment corresponds to shutdown queues (shutdown state), not idle/running zones.

**Healthy condition:**
AGVs expected to be in shutdown are consistently shown as being in shutdown queues/shutdown state.

**Expected result:**
AGVs that should be in shutdown are displayed in a shutdown queues/shutdown state condition in RMS (observable via their state and/or location/zone assignment).

---

###### Step 3 — Observe transition from shutdown queues into assigned zones (4 zones)

**Responsible role:** L1_support

**Instruction:**
Observe the AGVs in RMS over the expected startup transition window and confirm they move from shutdown queues into their assigned zones. The segment references 4 zones.

**Healthy condition:**
AGVs move out of shutdown queues into zone assignments rather than remaining in shutdown state.

**Expected result:**
AGVs transition from shutdown queues/shutdown state into their assigned zones (4 zones referenced in the segment).

---

###### Step 4 — If tipper/hospital scenario is active, confirm shutdown/startup cycle still holds

**Responsible role:** L1_support

**Instruction:**
If the segment’s scenario is active (tipper issue leading to hospital/reject handling), confirm in RMS that AGVs still follow the shutdown/startup cycle model: shutdown queues → assigned zones, rather than remaining stuck in shutdown queues.

**Healthy condition:**
No prolonged retention in shutdown queues beyond what the shutdown/startup logic implies; AGVs still enter their zone assignments.

**Expected result:**
Even during the tipper/hospital scenario, AGVs still transition from shutdown queues into their assigned zones in RMS.

---

**Success Criteria:**

- In RMS, AGVs expected to be in shutdown are shown in shutdown queues/shutdown state.
- After startup, those AGVs transition from shutdown queues into their assigned zones (4 zones referenced).
- During any tipper/hospital scenario, AGVs still follow shutdown queues → zones behavior rather than remaining stuck in shutdown.

**Failure Conditions:**

- AGVs remain in shutdown queues/shutdown state without transitioning into their assigned zones when startup is expected.
- RMS shows AGVs in non-shutdown zone assignments during a shutdown period.


</details>

<details><summary>Verify Robot Location model fields and location types/statuses used by RMS orange locations (`proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1`)</summary>

##### Runbook: Verify Robot Location model fields and location types/statuses used by RMS orange locations

- **Procedure ID:** `proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Using the WCS / Helix DB (SSMS) read-only access surface, verify the Robot Location database model table includes the expected location attributes (station number, occupied, zone, closeout zone, location type, max AGVs, dwell-time tracking) and that the enumerated location types/statuses match the RMS orange location categories (sorter/tipper/hospital/shut down/GLD pre queue).

**When To Use:**
When you need to confirm that RMS orange location categories are backed by the expected Robot Location model/table definition in the WCS/Robotics database (fields present and location type/status enumerations match the expected categories).

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open WCS / Helix DB (SSMS) read-only access surface

**Responsible role:** L2_support

**Instruction:**
Use the WCS / Helix DB (SSMS) access surface to connect to the OptiSweep/WCS database that contains the Robotics database model table definitions for the Robot Location model.

**Healthy condition:**
You can browse the database objects needed to locate the Robot Location database model table definition.

**Expected result:**
SSMS is connected to the OptiSweep/WCS database that contains the Robotics database model table definitions for the Robot Location model.

---

###### Step 2 — Locate Robot Location database model table and verify required location attributes

**Responsible role:** L2_support

**Instruction:**
In SSMS, locate the Robot Location database model table definition and verify it includes fields/attributes for: station number, occupied (occupied or not), zone, closeout zone, location type, Max number of AGVs allowed at that location, and whether the location should be tracked for dwell time there.

**Healthy condition:**
All required attributes are present in the Robot Location model/table definition with names/meaning consistent with the expected set (station number, occupied, zone, closeout zone, location type, max AGVs, dwell tracking).

**Expected result:**
The Robot Location database model table definition shows the expected location attributes: station number, occupied, zone, closeout zone, location type, Max number of AGVs allowed, and dwell-time tracking (tracked vs not tracked).

---

###### Step 3 — Verify Robot Location model includes expected location types/statuses for RMS orange categories

**Responsible role:** L2_support

**Instruction:**
In the same Robot Location model/table definition, verify the listed location types/statuses include the categories: sorter entrance queue, sorter queue, sorter exit queue; tipper, tipper queue, tipper exit queue; hospital drop off, hospital entrance queue, hospital pickup, hospital exit queue; queue shut down, off the end shut down queue; GLD pre queue entrance, GLD pre queue exit.

**Healthy condition:**
All listed categories appear in the Robot Location model/table definition (as location types/statuses) with names consistent with the expected set.

**Expected result:**
The Robot Location model/table definition includes the named location types/statuses for sorter/tipper/hospital/shut down/GLD pre queue categories.

---

###### Step 4 — Cross-check RMS orange location categories map to the same Robot Location types/statuses

**Responsible role:** L2_support

**Instruction:**
Using the Robot Location model/table definition you verified, confirm that the segment’s RMS orange location categories correspond to the same named location types/statuses you see in the Robot Location model/table definition.

**Healthy condition:**
The set of location types/statuses in the Robot Location model/table definition matches the expected RMS orange categories (sorter/tipper/hospital/shut down/GLD pre queue).

**Expected result:**
The RMS orange location categories map consistently to the location types/statuses present in the Robot Location model/table definition.

---

**Success Criteria:**

- Robot Location model/table definition includes required location attributes: station number, occupied, zone, closeout zone, location type, max AGVs, dwell-time tracking.
- Robot Location model/table definition includes expected location types/statuses: sorter entrance/queue/exit; tipper/tipper queue/tipper exit; hospital drop off/entrance queue/pickup/exit queue; queue shut down/off-the-end shut down; GLD pre queue entrance/exit.
- RMS orange location categories map consistently to the same named location types/statuses in the Robot Location model/table definition.

**Failure Conditions:**

- One or more required Robot Location attributes are missing or named differently such that the expected set cannot be confirmed.
- One or more expected location types/statuses are missing from the Robot Location model/table definition.
- RMS orange location categories cannot be mapped consistently to the Robot Location model/table definition.


</details>

</details>

---

### 2 — Isolate the inconsistent robot from the system (site-side removal) and ensure it is placed on charger (`procedure_reference`)

**Intent:** If roster/map inconsistency is confirmed or strongly suspected, perform the supported isolation/removal path for the inconsistent robot and prepare for system recovery monitoring.

**Expects capability:** agv_physical_recovery, device_roster_state
**Expects surface:** rms_ui, wcs_sql, physical_floor
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.6987, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_physical_recovery`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=site; tool=RMS / AGV status UI): Isolated robot is successfully removed from the problematic mapping context and the system/zone symptom begins to improve.
- `unhealthy` (observer=site; tool=RMS / AGV status UI): Robot isolation/removal does not change pairing symptom trajectory; the inconsistent mapping condition persists.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Isolation action completed but evidence is unclear whether symptom should be changing yet (insufficient monitoring window or RMS state not accessible).

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View (`proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`)</summary>

##### Runbook: Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View

- **Procedure ID:** `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`
- **Procedure Type:** `operation`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Geek Plus RMS Robot Selection web view to add a robot by robot ID or remove an existing robot, and confirm success messages after each action.

**When To Use:**
When you need to manage the Geek Plus RMS robot roster using the Robot Selection Add/Remove workflow and verify the on-screen success confirmations.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open Geek Plus RMS web application from an authorized network path

**Responsible role:** L1_support

**Instruction:**
From an OT network device, open the Geek Plus RMS web application using the site/RMS address. If you are supporting remotely, ensure you are authorized to use the UPS VPN through Zscaler and can reach the site/RMS address.

**Healthy condition:**
You can access the Geek Plus RMS web application from your current network authorization path.

**Expected result:**
The Geek Plus RMS web application loads successfully and you can navigate to the Robot Selection screen.

---

###### Step 2 — Navigate to the Robot Selection screen with Add Robot and Remove Robot controls

**Responsible role:** L1_support

**Instruction:**
In the Geek Plus RMS web application, navigate to the Robot Selection screen that contains the Robot ID entry field and the Add Robot and Remove Robot controls.

**Healthy condition:**
You can see the Robot ID entry area and the Add/Remove controls on the Robot Selection screen.

**Expected result:**
The Robot Selection screen is visible with the Robot ID entry field and the Add and Remove controls.

---

###### Step 3 — Add a robot by robot ID

**Responsible role:** L1_support

**Instruction:**
In the Robot ID entry field, enter the corresponding robot ID. (If the robot is already introduced, partial numeric entry may surface matching robots.) Click the "Add" button.

**Healthy condition:**
The UI shows the success confirmation for the Add action after clicking "Add".

**Expected result:**
A confirmation message appears indicating the robot was added successfully ("adding was successful" / "robot was added successfully").

---

###### Step 4 — Remove a robot by robot ID or by selecting it from the list

**Responsible role:** L1_support

**Instruction:**
Enter the corresponding robot ID in the Robot ID entry field or select the robot from the list shown for that ID. Click the "Remove" button.

**Healthy condition:**
The UI shows the success confirmation for the Remove action after clicking "Remove".

**Expected result:**
A confirmation message appears indicating the robot was removed successfully ("removal was successful" / "remove what was successful").

---

**Success Criteria:**

- After clicking "Add", the Robot Selection screen displays an "adding was successful" confirmation message.
- After clicking "Remove", the Robot Selection screen displays a "removal was successful" confirmation message.

**Failure Conditions:**

- No success confirmation appears after clicking "Add".
- No success confirmation appears after clicking "Remove".


</details>

</details>

---

### 3 — Validate that pairing/zone operation is stable after isolation (`validation_gate`)

**Intent:** Confirm the affected zone pairing symptoms and overall system behavior return to normal and remain stable for a short monitoring window.

**Expects capability:** fleet_system_status, zone_pairing_state, device_roster_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.5022, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Pairing/zone operation is stable for the short monitoring window after isolation.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Validation fails: pairing failure persists or fleet remains unstable after isolation and monitoring.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Monitoring window not sufficient or evidence is ambiguous.

**Branches:**

- `healthy` → `` when Validation confirms normal pairing/zone operation and stable system behavior
- `unhealthy` → `node_4` when Validation fails: pairing failure persists or system remains unstable

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View (`proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`)</summary>

##### Runbook: Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View

- **Procedure ID:** `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1`
- **Procedure Type:** `operation`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Geek Plus RMS Robot Selection web view to add a robot by robot ID or remove an existing robot, and confirm success messages after each action.

**When To Use:**
When you need to manage the Geek Plus RMS robot roster using the Robot Selection Add/Remove workflow and verify the on-screen success confirmations.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open Geek Plus RMS web application from an authorized network path

**Responsible role:** L1_support

**Instruction:**
From an OT network device, open the Geek Plus RMS web application using the site/RMS address. If you are supporting remotely, ensure you are authorized to use the UPS VPN through Zscaler and can reach the site/RMS address.

**Healthy condition:**
You can access the Geek Plus RMS web application from your current network authorization path.

**Expected result:**
The Geek Plus RMS web application loads successfully and you can navigate to the Robot Selection screen.

---

###### Step 2 — Navigate to the Robot Selection screen with Add Robot and Remove Robot controls

**Responsible role:** L1_support

**Instruction:**
In the Geek Plus RMS web application, navigate to the Robot Selection screen that contains the Robot ID entry field and the Add Robot and Remove Robot controls.

**Healthy condition:**
You can see the Robot ID entry area and the Add/Remove controls on the Robot Selection screen.

**Expected result:**
The Robot Selection screen is visible with the Robot ID entry field and the Add and Remove controls.

---

###### Step 3 — Add a robot by robot ID

**Responsible role:** L1_support

**Instruction:**
In the Robot ID entry field, enter the corresponding robot ID. (If the robot is already introduced, partial numeric entry may surface matching robots.) Click the "Add" button.

**Healthy condition:**
The UI shows the success confirmation for the Add action after clicking "Add".

**Expected result:**
A confirmation message appears indicating the robot was added successfully ("adding was successful" / "robot was added successfully").

---

###### Step 4 — Remove a robot by robot ID or by selecting it from the list

**Responsible role:** L1_support

**Instruction:**
Enter the corresponding robot ID in the Robot ID entry field or select the robot from the list shown for that ID. Click the "Remove" button.

**Healthy condition:**
The UI shows the success confirmation for the Remove action after clicking "Remove".

**Expected result:**
A confirmation message appears indicating the robot was removed successfully ("removal was successful" / "remove what was successful").

---

**Success Criteria:**

- After clicking "Add", the Robot Selection screen displays an "adding was successful" confirmation message.
- After clicking "Remove", the Robot Selection screen displays a "removal was successful" confirmation message.

**Failure Conditions:**

- No success confirmation appears after clicking "Add".
- No success confirmation appears after clicking "Remove".


</details>

</details>

---

### 4 — Escalate if pairing failure persists after roster/map reconciliation and isolation validation (`escalation_gate`)

**Intent:** Stop the current orchestration path when the supported checks and validation do not show recovery, and hand off with evidence for deeper L3/L4 investigation.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=RMS / AGV status UI): Escalation handoff is initiated after validation failure (no stable recovery).

**Branches:** no branch outcomes — proceed / escalate (procedure or escalation node).


**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | RMS/SSMS show pairing failure and/or roster/map inconsistency | `node_2` |
| `node_1` | `healthy` | RMS/SSMS do not show pairing failure or roster/map inconsistency | `node_3` |
| `node_1` | `escalate` | Unable to corroborate or evidence insufficient | `node_4` |
| `node_3` | `healthy` | Validation confirms normal pairing/zone operation and stable system behavior | `` |
| `node_3` | `unhealthy` | Validation fails: pairing failure persists or system remains unstable | `node_4` |

## Unresolved / Low-Confidence Links

- node_1: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_1: proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1 (low)
- node_1: proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1 (low)
- node_2: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_3: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_4: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
