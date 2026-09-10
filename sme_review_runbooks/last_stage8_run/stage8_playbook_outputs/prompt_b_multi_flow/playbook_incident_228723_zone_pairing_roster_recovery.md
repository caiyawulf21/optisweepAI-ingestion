# Zone pairing failure with abnormal AMR routing

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_228723_zone_pairing_roster_recovery` |
| Case ID | `228723` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- A site reports that a zone cannot get an AGV or AMR pair.
- The ACB or related automated system is reported as down or unable to operate normally.
- Replacement or available AMRs route toward the hospital lane instead of serving the affected workflow.
- An AMR may be physically stranded, low on battery, under a rack, or otherwise unavailable.

## Affected Systems

- ACB or automated material-handling workflow
- AGVs / AMRs
- RMS fleet and roster views
- Zone pairing state
- Hospital lane or hospital workflow
- WCS robotics and mapping state

## Nodes

### 1 — Confirm the zone pairing failure and current routing symptom (`diagnostic_decision`)

**Intent:** Establish whether the reported issue is an active zone pairing failure and whether AMRs are being routed to an unexpected destination such as the hospital lane.

**Expects capability:** zone_pairing_state
**Expects surface:** rms_ui, site_interview
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1` (low, support, score=0.6642, boosted=0.8942) — Check RMS fleet status for AGVs in shutdown queues and zone cycling
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.6194, boosted=0.8494) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1` (low, support, score=0.6188, boosted=0.8488) — Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Site and RMS confirm normal pairing behavior and no ongoing unexpected hospital routing.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Active zone pairing failure and/or unexpected hospital routing is confirmed.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): RMS cannot be validated (blank/unreachable) or site cannot provide confirmable observations of pairing/routing.
- `escalate` (observer=remote; tool=RMS / AGV status UI): RMS is unavailable and cannot be resolved via the allowed operator/L1 checks.

**Branches:**

- `unhealthy` → `node_2` when Pairing failure or unexpected hospital routing confirmed
- `healthy` → `` when Pairing and routing appear normal or cannot be confirmed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

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

<details><summary>Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall) (`proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1`)</summary>

##### Runbook: Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)

- **Procedure ID:** `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Geek+ RMS / fleet status web UI to confirm the overall page is reachable and that it correctly separates fault categories: “system faults” on the left and “AGV system faults” on the right. If the RMS page is blank, treat it as a reachability/firewall symptom. Use the left/right placement to interpret whether the issue is communication loss vs an AGV that was commanded to move but is not in progress.

**When To Use:**
When you need to verify that the Geek+ RMS overall/fleet status page is reachable and that it is showing the expected fault panels (left system faults vs right AGV system faults), including the specific symptom where the page appears blank due to firewall not being open.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the Geek+ RMS / fleet status web UI (RMS overall page)

**Responsible role:** L1_support

**Instruction:**
Open the Geek+ RMS / fleet status web UI (RMS / fleet status UI).

**Healthy condition:**
The RMS overall page is visible and fault panels can be observed.

**Expected result:**
The RMS overall page loads (or you observe that it is blank).

---

###### Step 2 — Confirm the RMS page is not blank; if blank, treat as firewall/reachability symptom

**Responsible role:** L1_support

**Instruction:**
Check whether the RMS overall page shows content/fault panels. If it is blank, treat it as the firewall-not-open symptom described by the source.

**Healthy condition:**
Fault panels are visible (not blank).

**Expected result:**
Either (a) fault panels are visible, or (b) the page is blank consistent with firewall not being open.

---

###### Step 3 — Check left-side “system faults” panel

**Responsible role:** L1_support

**Instruction:**
On the RMS overall page, check the left side labeled area for “system faults”.

**Healthy condition:**
The left “system faults” panel is visible (fault rows/entries can be observed if present).

**Expected result:**
The left-side “system faults” area is visible and can be reviewed for any listed faults.

---

###### Step 4 — Check right-side “AGV system faults” panel

**Responsible role:** L1_support

**Instruction:**
On the RMS overall page, check the right side labeled area for “AGV system faults” (active AGV faults).

**Healthy condition:**
The right “AGV system faults” panel is visible (fault rows/entries can be observed if present).

**Expected result:**
The right-side “AGV system faults” area is visible and can be reviewed for any listed faults.

---

###### Step 5 — Interpret left/right fault placement for communication loss vs commanded-but-not-in-progress movement

**Responsible role:** L1_support

**Instruction:**
Use the source mapping: if you lose communication with a chat, expect it on the left “system faults”; if you told an AGV to move but it hasn’t moved, expect it on the right “AGV system faults”.

**Healthy condition:**
Observed faults align with the expected left/right meaning (left = communication loss; right = commanded move not in progress).

**Expected result:**
You can map the observed fault placement to either communication-loss (left) or commanded-but-not-in-progress movement (right).

---

**Success Criteria:**

- RMS overall page is reachable and not blank (fault panels visible).
- Left “system faults” and right “AGV system faults” areas are observable on the RMS overall page.
- Observed fault placement can be interpreted as communication loss (left) vs commanded-but-not-in-progress movement (right) using the source mapping.

**Failure Conditions:**

- RMS remains blank (no visible system/AGV fault panels).
- Left/right fault separation is not observable or does not align with the expected meaning (left = communication loss; right = commanded move not in progress).


</details>

<details><summary>Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger (`proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1`)</summary>

##### Runbook: Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger

- **Procedure ID:** `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI to determine whether AGVs are not progressing due to state-transition failure visibility patterns: (1) AGVs waiting to do an exchange during shutdown, and/or (2) startup delay while waiting for an AGV on the charger. The system is described as exposing this via system faults and visible waiting conditions.

**When To Use:**
Use when lifecycle progression appears delayed during shutdown/startup and you need to check whether RMS is showing AGVs in the documented waiting/fault visibility patterns (exchange-waiting during shutdown; charger-waiting startup delay).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI and navigate to AGV status/errors overview

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV status/errors overview area.

**Healthy condition:**
The RMS AGV status/errors overview area is populated and ready for inspection (not blank/unreachable).

**Expected result:**
You are viewing the RMS AGV status/errors overview area where AGV waiting conditions and system fault/alert visibility can be checked.

---

###### Step 2 — Check for AGVs waiting to do an exchange during shutdown

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, look for AGVs showing a waiting condition consistent with “waiting to do an exchange” during shutdown.

**Healthy condition:**
No widespread exchange-waiting indications are present when shutdown is expected to complete normally.

**Expected result:**
At least one AGV is indicated in RMS as waiting to do an exchange during shutdown (or you determine none are indicated).

---

###### Step 3 — Check for startup delay waiting for an AGV on the charger

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, look for startup delay evidence consistent with “waiting … for an AGV on the charger.”

**Healthy condition:**
No charger-waiting startup delay indications are present when startup proceeds normally.

**Expected result:**
At least one AGV is indicated in RMS as contributing to startup delay by waiting for an AGV on the charger (or you determine none are indicated).

---

###### Step 4 — Confirm system faults/alerts align with the waiting conditions

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, confirm whether system faults/alerts are visible and align with the exchange-waiting and/or charger-waiting conditions you observed.

**Healthy condition:**
Fault/alert visibility is consistent with normal operation (no fault entries that match the described waiting patterns).

**Expected result:**
RMS shows visible system fault/alert entries that align with the waiting conditions (or you determine there are no aligning fault/alert entries).

---

###### Step 5 — Stop and escalate on repeated or widespread waiting/fault indications

**Responsible role:** L1_support

**Instruction:**
If you see repeated or widespread waiting/fault indications that prevent lifecycle progression (e.g., multiple AGVs stuck in exchange-waiting or charger-waiting states), stop and escalate for deeper investigation.

**Healthy condition:**
No repeated/widespread waiting/fault indications are present; lifecycle progression is not blocked by the described patterns.

**Expected result:**
Escalation is initiated when the RMS evidence shows repeated/widespread waiting/fault indications consistent with the described patterns.

---

**Success Criteria:**

- RMS / fleet status UI shows either (a) AGVs indicated as waiting to do an exchange during shutdown and/or (b) startup delay evidence consistent with waiting for an AGV on the charger.
- RMS also shows visible system faults/alerts that align with the observed waiting conditions (when present).

**Failure Conditions:**

- RMS shows repeated/widespread AGVs waiting to do an exchange during shutdown.
- RMS shows repeated/widespread startup delay evidence consistent with waiting for an AGV on the charger.
- RMS shows system faults/alerts that align with the above waiting conditions.


</details>

</details>

---

### 2 — Check fleet roster and mapping consistency (`diagnostic_decision`)

**Intent:** Determine whether one or more AGVs have abnormal roster membership, mapping, location, or zone state that could explain the pairing failure.

**Expects capability:** device_roster_state
**Expects surface:** rms_ui, wcs_sql
**Preferred audience:** L1_support, L2_support

**Runbook Links:**

- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (medium, support, score=0.4893, boosted=1.0) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_rms_disconnected_agv_count_cause_v1` (low, support, score=0.646, boosted=0.8213) — Check RMS disconnected AGV count and identify likely disconnect cause (lost RMS comms vs turned off)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1` (low, support, score=0.3, boosted=0.3068) — Verify Robot Location model fields and location types/statuses used by RMS orange locations
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=remote; tool=RMS / AGV status UI): RMS roster/map evidence appears coherent for the relevant AGVs/zones; no abnormal/unmapped state found (or symptoms are inconclusive).
- `unhealthy` (observer=remote; tool=RMS / AGV status UI): Unmapped/missing/inconsistent roster or mapping state is indicated by RMS (and/or related read-only evidence).
- `inconclusive` (observer=remote; tool=RMS / AGV status UI): RMS tables are unreadable or evidence disagreements prevent a clear decision.
- `escalate` (observer=remote; tool=RMS / AGV status UI): RMS evidence cannot be obtained and disconnect/root-cause is suspected to be systemic rather than mapping/roster.

**Branches:**

- `unhealthy` → `node_3` when RMS/WCS indicates unmapped/missing/inconsistent roster state
- `inconclusive` → `node_4` when Roster/mapping appears coherent or inconclusive

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

<details><summary>Check RMS disconnected AGV count and identify likely disconnect cause (lost RMS comms vs turned off) (`proc_check_rms_disconnected_agv_count_cause_v1`)</summary>

##### Runbook: Check RMS disconnected AGV count and identify likely disconnect cause (lost RMS comms vs turned off)

- **Procedure ID:** `proc_check_rms_disconnected_agv_count_cause_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
On the RMS / fleet status UI map monitor summary, read the “count of AGVs disconnected” metric. Use the training’s definition to interpret “disconnected” as AGVs that have lost communication from RMS (RMS runs on the server; AGVs are on Wi‑Fi), then correlate the disconnected count with likely causes: Wi‑Fi/RMS communication loss vs AGVs being turned off.

**When To Use:**
When you need a first-pass diagnostic using RMS’s disconnected AGV count to understand whether AGVs are likely disconnected due to lost RMS/Wi‑Fi communication versus being turned off.

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI map monitor summary area

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the map monitor summary/message panel area that includes the “count of AGVs disconnected” metric.

**Healthy condition:**
The map monitor summary/message panel is visible and the disconnected AGV count metric is readable.

**Expected result:**
The RMS UI shows the map monitor summary/message panel with a visible “count of AGVs disconnected” value.

---

###### Step 2 — Read the “count of AGVs disconnected” value

**Responsible role:** L1_support

**Instruction:**
In the RMS map monitor summary/message panel, locate and read the “count of AGVs disconnected” value.

**Healthy condition:**
A single disconnected count value is displayed in the metric list.

**Expected result:**
You have the numeric value for “count of AGVs disconnected” as shown in the RMS UI.

---

###### Step 3 — Interpret “disconnected” as lost RMS communication (RMS server + AGVs on Wi‑Fi)

**Responsible role:** L1_support

**Instruction:**
Use the definition: treat “disconnected” as AGVs that have lost communication from RMS (RMS is the application running on the server; AGVs are on the Wi‑Fi).

**Healthy condition:**
You can state that “disconnected” means lost communication from RMS to AGVs (RMS server application; AGVs on Wi‑Fi).

**Expected result:**
Your interpretation of the disconnected count is explicitly tied to lost communication from RMS to AGVs over Wi‑Fi.

---

###### Step 4 — Correlate disconnected count with likely causes: Wi‑Fi/RMS comms loss vs AGV turned off

**Responsible role:** L1_support

**Instruction:**
Correlate the disconnected count with likely causes: (1) AGVs lost communication with the Wi‑Fi on site, or (2) the AGV was turned off.

**Healthy condition:**
Your hypothesis aligns with the observed situation (e.g., if AGVs were turned off, you expect to see disconnect; if not, you consider Wi‑Fi/RMS communication loss).

**Expected result:**
You produce a likely cause hypothesis that matches one of the two causes explicitly described: Wi‑Fi/RMS communication loss or AGV turned off.

---

**Success Criteria:**

- You can read the RMS “count of AGVs disconnected” metric from the RMS / fleet status UI.
- You interpret “disconnected” as lost communication from RMS to AGVs over Wi‑Fi.
- You correlate the disconnected count to one of the two explicitly described likely causes: Wi‑Fi/RMS communication loss or AGV turned off.

**Failure Conditions:**

- Disconnected count is high and you cannot determine whether the cause is communication loss vs AGVs being turned off using only this metric.


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

### 3 — Perform authorized AGV isolation or roster recovery (`procedure_reference`)

**Intent:** Use the approved recovery path for an AGV that is confirmed to be unmapped, incorrectly rostered, or otherwise preventing normal fleet operation.

**Expects capability:** agv_physical_recovery, device_roster_state
**Expects surface:** physical_floor, rms_ui, wcs_api
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1` (low, operator, score=0.8138, boosted=1.0) — Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_agv_bump_fault_rms_estop_agv_reset_v1` (low, support, score=0.8051, boosted=1.0) — Recover an AGV from a "Bump" fault (Exception Codes 21057/21060) using RMS E-stop and AGV RESET
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1` (low, support, score=0.8347, boosted=1.0) — Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice)
  - gaps: Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `device_roster_state`: roster/mapping abnormality — check RMS map monitor / robot roster (optionally WCS robot-location models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=physical_floor): Authorized isolation/recovery action completes and RMS state becomes coherent; pairing can proceed.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Recovery action fails or leaves roster state abnormal/persistent unsafe condition.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Recovery performed but system-side state cannot be verified.
- `escalate` (observer=remote; tool=physical_floor): Cannot proceed safely/authorizedly with isolation/recovery.

**Branches:**

- `healthy` → `node_5` when Authorized recovery completed; system-side state observable
- `escalate` → `node_6` when Recovery cannot be performed safely/authorizedly or state persists

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

<details><summary>Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET (`proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1`)</summary>

##### Runbook: Clear AGV Motionless on Floor Fault Using RMS (If Needed), E-Stop Zone Map, and Blue RESET

- **Procedure ID:** `proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1`
- **Procedure Type:** `recovery`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
For an AGV motionless on the floor (fault), locate the faulted AGV (optionally using RMS to identify the AGV error), stop the appropriate E-stop zone using the E-stop zone map, remove the faulted AGV, pull the E-STOP, and press the blue RESET button to resume operation.

**When To Use:**
Use when an AGV is motionless on the floor and the issue is identified as a fault, requiring physical removal of the faulted AGV and an E-stop zone reset to resume system operation.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Locate the faulted AGV (use RMS if needed)

**Responsible role:** operator

**Instruction:**
If the faulted AGV is not immediately obvious, use the RMS / fleet status UI to identify the AGV error/faulted unit.

**Healthy condition:**
RMS indicates the faulted AGV/error state for the unit you are targeting for removal.

**Expected result:**
You have identified the faulted AGV that is motionless on the floor.

---

###### Step 2 — Stop the appropriate E-stop zone using the E-stop zone map

**Responsible role:** operator

**Instruction:**
Reference the E-stop zone map and press the E-STOP for the appropriate E-stop zone.

**Healthy condition:**
The E-stop you pressed corresponds to the zone for the faulted AGV identified in Step 1.

**Expected result:**
The appropriate E-stop zone is stopped.

---

###### Step 3 — Remove the faulted AGV

**Responsible role:** operator

**Instruction:**
Remove the faulted AGV from the floor/system area.

**Healthy condition:**
The faulted AGV is no longer present in the faulted location/zone.

**Expected result:**
The faulted AGV has been removed.

---

###### Step 4 — Pull the E-STOP

**Responsible role:** operator

**Instruction:**
Pull the E-STOP.

**Healthy condition:**
E-STOP is in the pulled state as part of the reset procedure.

**Expected result:**
The E-STOP has been pulled (reset sequence is ready for blue RESET).

---

###### Step 5 — Press the blue RESET button

**Responsible role:** operator

**Instruction:**
Press the blue RESET button.

**Healthy condition:**
System operation resumes (no longer remains in the faulted/stopped state).

**Expected result:**
The system resumes operation after the reset.

---

###### Step 6 — Confirm the system resumes operation

**Responsible role:** operator

**Instruction:**
Confirm that the system resumes operation following the blue RESET.

**Healthy condition:**
System is running/operational after reset.

**Expected result:**
Operation resumes.

---

**Success Criteria:**

- After pulling the E-STOP and pressing the blue RESET button, the system resumes operation.

**Failure Conditions:**

- System does not resume operation after pressing the blue RESET button.
- RMS does not clearly identify the faulted AGV.


</details>

</details>

<details><summary><strong>Support runbooks</strong> (2)</summary>

<details><summary>Recover an AGV from a "Bump" fault (Exception Codes 21057/21060) using RMS E-stop and AGV RESET (`proc_recover_agv_bump_fault_rms_estop_agv_reset_v1`)</summary>

##### Runbook: Recover an AGV from a "Bump" fault (Exception Codes 21057/21060) using RMS E-stop and AGV RESET

- **Procedure ID:** `proc_recover_agv_bump_fault_rms_estop_agv_reset_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
When an AGV cannot be recovered by Geek+ and the RMS shows an AGV "Bump" fault (Exception Codes 21057 or 21060), stop RMS, remove the obstruction, hold the AGV RESET button for two seconds to clear the fault, press E-stop again, and resume RMS.

**When To Use:**
Use this procedure when the RMS / fleet status UI shows an AGV "Bump" fault and the exception code is 21057 or 21060, and the AGV needs on-site recovery by removing the obstruction and resetting the AGV.

**Safety Notes:**

- Stop RMS (E-stop) before removing the obstruction and performing the AGV RESET sequence.
- Do not proceed with reset/resume if you cannot safely remove the obstruction.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Identify the AGV "Bump" fault and confirm the Exception Code (21057 or 21060)

**Responsible role:** L2_support

**Instruction:**
In the RMS / fleet status UI, locate the AGV "Bump" fault screen and confirm the Exception Code shown is 21057 or 21060.

**Healthy condition:**
The active fault shown on the RMS "Bump" fault screen matches 21057 or 21060 for the intended AGV.

**Expected result:**
The RMS "Bump" fault screen for the affected AGV shows Exception Code 21057 (Robot front collision bar triggers) or 21060 (robot triggers the obstacle avoidance).

---

###### Step 2 — E-stop the RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, activate the E-stop function.

**Healthy condition:**
E-stop is active and the recovery sequence is not attempted while RMS is running.

**Expected result:**
RMS is in an E-stopped state (E-stop activated) while the "Bump" fault recovery sequence proceeds.

---

###### Step 3 — Remove the obstruction that caused the bump

**Responsible role:** L2_support

**Instruction:**
Remove the physical obstruction causing the bump (for example, at the AGV/robot front collision bar area).

**Healthy condition:**
The obstruction is cleared and the area is safe for the AGV to be reset and RMS to be resumed.

**Expected result:**
The physical obstruction is removed so the AGV/robot front collision bar area is clear.

---

###### Step 4 — Click and hold AGV RESET for two seconds to clear the fault

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, click the AGV RESET button and hold it for two (2) seconds.

**Healthy condition:**
The fault-clearing action completes (as indicated by the recovery sequence proceeding to the next step).

**Expected result:**
The AGV RESET action is held for two seconds to clear the fault.

---

###### Step 5 — Press E-stop again

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, press E-stop again.

**Healthy condition:**
The sequence proceeds exactly as specified: E-stop again after AGV RESET.

**Expected result:**
RMS E-stop is pressed again as part of the recovery sequence.

---

###### Step 6 — Resume RMS

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI, resume RMS to normal operation.

**Healthy condition:**
The RMS no longer displays the active "Bump" fault for the affected AGV and RMS is back in normal operation.

**Expected result:**
RMS is resumed to normal operation and the affected AGV is no longer showing the active "Bump" fault.

---

**Success Criteria:**

- Exception Code 21057/21060 "Bump" fault is cleared for the affected AGV after holding AGV RESET for two seconds.
- RMS is resumed to normal operation and the RMS no longer shows the active "Bump" fault for the affected AGV.

**Failure Conditions:**

- The "Bump" fault does not clear after holding AGV RESET for two seconds.
- The obstruction cannot be safely removed.


</details>

<details><summary>Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice) (`proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1`)</summary>

##### Runbook: Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice)

- **Procedure ID:** `proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
If empty AGVs lose their tasks after an RMS restart, stop RMS, remove and re-add the affected empty AGVs without totes twice, verify each AGV is in the "szonestaging" state on the HMI, press E-stop again when ready, then resume RMS.

**When To Use:**
Use when empty AGVs have lost their tasks because the RMS was restarted, and the recovery guidance calls for removing and re-adding the AGVs twice and confirming "szonestaging" before resuming RMS.

**Safety Notes:**

- Do not resume RMS until the affected AGVs are confirmed in the "szonestaging" state on the HMI.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), press the E-stop for RMS.

**Healthy condition:**
The RMS E-stop control is engaged/active on the RMS / fleet status UI.

**Expected result:**
RMS is in an E-stopped state on the RMS / fleet status UI.

---

###### Step 2 — Remove and re-add empty AGVs without totes twice using Tote API Controls

**Responsible role:** L2_support

**Instruction:**
Using the Tote API Controls flow within the RMS / fleet status UI (rms_ui), remove and re-add the affected empty AGVs without totes twice.

**Healthy condition:**
The AGVs proceed through the expected post-add state progression (next step will verify "szonestaging").

**Expected result:**
Each affected empty AGV has been removed and re-added twice via the RMS Tote API Controls flow.

---

###### Step 3 — Verify AGVs are in "szonestaging" on the HMI

**Responsible role:** L2_support

**Instruction:**
If the system needs to be restarted, verify on the HMI (hospital_hmi) that the affected AGVs are in the "szonestaging" state by referencing the AGV state/value on the HMI.

**Healthy condition:**
AGV status is "szonestaging" for the affected empty AGVs.

**Expected result:**
The affected empty AGVs show AGV status/state value "szonestaging" on the HMI.

---

###### Step 4 — Press E-stop again when ready to resume

**Responsible role:** L2_support

**Instruction:**
When the affected empty AGVs are confirmed in "szonestaging" on the HMI, press the E-stop again on the RMS / fleet status UI (rms_ui) when ready to resume.

**Healthy condition:**
E-stop again action is accepted and the system is ready for RMS resumption.

**Expected result:**
The RMS E-stop control is pressed again (as indicated by the RMS / fleet status UI).

---

###### Step 5 — Resume RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), resume RMS.

**Healthy condition:**
RMS is resumed and the affected empty AGVs are no longer in the lost-task condition.

**Expected result:**
RMS resumes/starts successfully on the RMS / fleet status UI.

---

**Success Criteria:**

- RMS is resumed on the RMS / fleet status UI.
- Affected empty AGVs are no longer in the lost-task condition after the remove/re-add cycle and "szonestaging" verification.

**Failure Conditions:**

- Any affected empty AGV cannot be brought to "szonestaging".
- Lost-task condition persists after the twice remove/re-add process and RMS resumption.


</details>

</details>

---

### 4 — Investigate hospital-lane diversion when roster state appears healthy (`diagnostic_decision`)

**Intent:** Determine whether unexpected hospital routing remains the active observable symptom after no clear roster or mapping mismatch is found.

**Expects capability:** hospital_diversion
**Expects surface:** hospital_hmi, rms_ui
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1` (low, support, score=0.6632, boosted=0.8465) — Check RMS fleet status for AGVs in shutdown queues and zone cycling
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.
- `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1` (low, support, score=0.609, boosted=0.739) — Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.
- `proc_check_hospital_hmi_operations_menu_induct_extract_status_v1` (low, operator, score=0.3, boosted=1.13) — Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages
  - gaps: Wrong catalog family: hospital HMI/stacklight does not corroborate RMS roster/mapping (use RMS map/roster views; hospital UI is secondary diversion corroboration only).; Retrieval score 0.3000 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).
- Wrong catalog family: hospital HMI/stacklight does not corroborate RMS roster/mapping (use RMS map/roster views; hospital UI is secondary diversion corroboration only).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital diversion is absent and pairing/operation appears normal.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI / lane UI): Unexpected hospital diversion persists.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI / lane UI): Hospital lane UI not observable or signals cannot be clearly interpreted.
- `escalate` (observer=remote; tool=Hospital HMI / lane UI): Divergence persists with insufficient evidence for safe further recovery.

**Branches:**

- `healthy` → `node_6` when Hospital diversion absent; pairing/operation normal
- `unhealthy` → `node_6` when Unexpected hospital diversion persists

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

<details><summary>Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages (`proc_check_hospital_hmi_operations_menu_induct_extract_status_v1`)</summary>

##### Runbook: Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages

- **Procedure ID:** `proc_check_hospital_hmi_operations_menu_induct_extract_status_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the Hospital HMI / lane UI Operations Menu screen to read the WCS-fed induct and extract position fields (AGV#, Tote ID, Bar Code, Status). Confirm the Status messages explain why the tote is there and what station operator menu/action to use.

**When To Use:**
When a tote arrives at the hospital station and you need to determine what tote/AGV is at the induct and extract positions and what the WCS status message requires the station operator to do next.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open Hospital HMI Operations Menu and locate Induct Position / Extract Position sections

**Responsible role:** operator

**Instruction:**
On the Hospital HMI / lane UI, navigate to the Operations Menu screen that contains the "Induct Position" and "Extract Position" sections.

**Healthy condition:**
"Induct Position" and "Extract Position" sections are visible on the Operations Menu screen.

**Expected result:**
The screen shows both "Induct Position" and "Extract Position" sections.

---

###### Step 2 — Read Induct Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Induct Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Healthy condition:**
AGV#, Tote ID, Bar Code, and Status are present in the "Induct Position" section as read-only WCS data.

**Expected result:**
The "Induct Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

---

###### Step 3 — Read Extract Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Extract Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Healthy condition:**
AGV#, Tote ID, Bar Code, and Status are present in the "Extract Position" section as read-only WCS data.

**Expected result:**
The "Extract Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

---

###### Step 4 — Confirm both Status messages are present and provide WCS explanation/action guidance

**Responsible role:** operator

**Instruction:**
Verify that the "Induct Position" Status and "Extract Position" Status messages are present and written as messages received from the WCS that explain why the tote is there and what menu/action the station operator needs to use.

**Healthy condition:**
Induct Position Status and Extract Position Status each provide a clear WCS message describing why the tote is there and what menu/action to perform.

**Expected result:**
Both Status fields contain non-blank WCS messages that provide explanation and action/menu guidance.

---

**Success Criteria:**

- Induct Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
- Extract Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
- Both Status messages explain why the tote is there and what menu/action the station operator needs to use.

**Failure Conditions:**

- Induct Position Status is blank/missing.
- Extract Position Status is blank/missing.
- Either Status message does not provide explanation/action guidance (why the tote is there and what menu/action to use).


</details>

</details>

<details><summary><strong>Support runbooks</strong> (2)</summary>

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

<details><summary>Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger (`proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1`)</summary>

##### Runbook: Check RMS / fleet status UI for AGVs waiting to exchange during shutdown or startup delay waiting on charger

- **Procedure ID:** `proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI to determine whether AGVs are not progressing due to state-transition failure visibility patterns: (1) AGVs waiting to do an exchange during shutdown, and/or (2) startup delay while waiting for an AGV on the charger. The system is described as exposing this via system faults and visible waiting conditions.

**When To Use:**
Use when lifecycle progression appears delayed during shutdown/startup and you need to check whether RMS is showing AGVs in the documented waiting/fault visibility patterns (exchange-waiting during shutdown; charger-waiting startup delay).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open RMS / fleet status UI and navigate to AGV status/errors overview

**Responsible role:** L1_support

**Instruction:**
Open the RMS / fleet status UI (rms_ui) and navigate to the AGV status/errors overview area.

**Healthy condition:**
The RMS AGV status/errors overview area is populated and ready for inspection (not blank/unreachable).

**Expected result:**
You are viewing the RMS AGV status/errors overview area where AGV waiting conditions and system fault/alert visibility can be checked.

---

###### Step 2 — Check for AGVs waiting to do an exchange during shutdown

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, look for AGVs showing a waiting condition consistent with “waiting to do an exchange” during shutdown.

**Healthy condition:**
No widespread exchange-waiting indications are present when shutdown is expected to complete normally.

**Expected result:**
At least one AGV is indicated in RMS as waiting to do an exchange during shutdown (or you determine none are indicated).

---

###### Step 3 — Check for startup delay waiting for an AGV on the charger

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, look for startup delay evidence consistent with “waiting … for an AGV on the charger.”

**Healthy condition:**
No charger-waiting startup delay indications are present when startup proceeds normally.

**Expected result:**
At least one AGV is indicated in RMS as contributing to startup delay by waiting for an AGV on the charger (or you determine none are indicated).

---

###### Step 4 — Confirm system faults/alerts align with the waiting conditions

**Responsible role:** L1_support

**Instruction:**
In the RMS AGV status/errors overview, confirm whether system faults/alerts are visible and align with the exchange-waiting and/or charger-waiting conditions you observed.

**Healthy condition:**
Fault/alert visibility is consistent with normal operation (no fault entries that match the described waiting patterns).

**Expected result:**
RMS shows visible system fault/alert entries that align with the waiting conditions (or you determine there are no aligning fault/alert entries).

---

###### Step 5 — Stop and escalate on repeated or widespread waiting/fault indications

**Responsible role:** L1_support

**Instruction:**
If you see repeated or widespread waiting/fault indications that prevent lifecycle progression (e.g., multiple AGVs stuck in exchange-waiting or charger-waiting states), stop and escalate for deeper investigation.

**Healthy condition:**
No repeated/widespread waiting/fault indications are present; lifecycle progression is not blocked by the described patterns.

**Expected result:**
Escalation is initiated when the RMS evidence shows repeated/widespread waiting/fault indications consistent with the described patterns.

---

**Success Criteria:**

- RMS / fleet status UI shows either (a) AGVs indicated as waiting to do an exchange during shutdown and/or (b) startup delay evidence consistent with waiting for an AGV on the charger.
- RMS also shows visible system faults/alerts that align with the observed waiting conditions (when present).

**Failure Conditions:**

- RMS shows repeated/widespread AGVs waiting to do an exchange during shutdown.
- RMS shows repeated/widespread startup delay evidence consistent with waiting for an AGV on the charger.
- RMS shows system faults/alerts that align with the above waiting conditions.


</details>

</details>

---

### 5 — Validate normal pairing and stable fleet operation (`validation_gate`)

**Intent:** Confirm that the affected workflow has recovered and remains operational after the diagnostic or recovery path.

**Expects capability:** zone_pairing_state, fleet_system_status
**Expects surface:** rms_ui, wcs_sql, site_interview
**Preferred audience:** operator, L1_support, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.5194, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1` (low, support, score=0.5622, boosted=1.0) — Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.5692, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=RMS / AGV status UI): Pairing succeeds, expected routing resumes, and stability remains during monitoring.
- `unhealthy` (observer=site_or_remote; tool=RMS / AGV status UI): Pairing fails again, hospital diversion continues, or new abnormal roster state appears.
- `inconclusive` (observer=site_or_remote; tool=RMS / AGV status UI): Recovery was reported but live evidence cannot be obtained for stable operation.

**Branches:**

- `healthy` → `` when Successful pairing + stable routing during monitoring
- `unhealthy` → `node_6` when Validation failure (pairing fails again / diversion continues / roster becomes abnormal)

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (3)</summary>

<details><summary>Access RMS web application via site Argus server IP and verify the RMS overview screen loads (`proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1`)</summary>

##### Runbook: Access RMS web application via site Argus server IP and verify the RMS overview screen loads

- **Procedure ID:** `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Verify that the RMS / fleet status web UI is reachable from a supported workstation using the site-provided unique IP, that login succeeds with the provided username/password, and that the RMS overview screen loads. Use this as the first connectivity/login check when troubleshooting RMS web availability.

**When To Use:**
Use when you need a first-pass check that the RMS web application is reachable and that authentication leads to the RMS overview screen (the initial landing/overview page).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS web location using the site-provided unique IP

**Responsible role:** L1_support

**Instruction:**
From a supported workstation, open a web browser and navigate to the site-provided RMS web location using the unique IP address for the RMS service.

**Healthy condition:**
The RMS web application page is reachable and displays the RMS login flow.

**Expected result:**
The RMS web application landing page loads (i.e., the browser reaches the RMS web location).

---

###### Step 2 — Authenticate on the RMS login page

**Responsible role:** L1_support

**Instruction:**
On the RMS login page, enter the username and password provided for RMS access, then submit/login.

**Healthy condition:**
After submitting credentials, the RMS overview screen is reached.

**Expected result:**
Login succeeds and the session proceeds to the RMS overview screen.

---

###### Step 3 — Verify the RMS overview screen is displayed

**Responsible role:** L1_support

**Instruction:**
After login, verify you are on the RMS overview screen (the screen described as “this is what you will see… the overview screen”).

**Healthy condition:**
The overview screen loads successfully after login.

**Expected result:**
The RMS overview screen is displayed.

---

**Success Criteria:**

- RMS web application is reachable using the site’s unique IP.
- Login succeeds using the provided username/password.
- The RMS overview screen is displayed after login.

**Failure Conditions:**

- RMS web application is unreachable (page won’t load).
- Login does not lead to the RMS overview screen.


</details>

<details><summary>Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed) (`proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`)</summary>

##### Runbook: Check AGV state, command vitals, and active AGV/system errors on Get AGV Status (HMI/API-backed)

- **Procedure ID:** `proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the Get AGV Status view (RMS / fleet status UI) to confirm the current AGV state, current command vitals (described as “teal vitals”), and whether the HMI error alert flag is set to true and bubbles to the top when an AGV error or system error is active.

**When To Use:**
Use when you need to verify whether any AGV errors or system errors are currently active and are being surfaced by the Get AGV Status HMI error alert behavior (alert becomes true and bubbles to the top).

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Open Get AGV Status view and locate AGV state, teal command vitals, and error sections

**Responsible role:** L1_support

**Instruction:**
Open the live Get AGV Status view/screen in the RMS / fleet status UI that shows: (1) AGV state, (2) current command vitals (described as “teal vitals”), and (3) sections for AGV errors and system errors.

**Healthy condition:**
For the AGV(s) shown, the screen is populated with AGV state and teal vitals, and the AGV errors/system errors sections are present for evaluation.

**Expected result:**
The Get AGV Status screen displays AGV state, current command vitals (“teal vitals”), and areas where AGV errors and system errors are shown.

---

###### Step 2 — Verify displayed AGV state and current command vitals (teal vitals) for a selected AGV entry

**Responsible role:** L1_support

**Instruction:**
Select an AGV row/entry on the Get AGV Status screen and verify the displayed AGV state and the current command vitals (described as “teal vitals”).

**Healthy condition:**
AGV state and teal vitals are present for the selected AGV entry.

**Expected result:**
For the selected AGV entry, the AGV state and teal vitals are populated and visible on the Get AGV Status screen.

---

###### Step 3 — Check error alert flag behavior (must be true and bubble to the top when an error exists)

**Responsible role:** L1_support

**Instruction:**
On the Get AGV Status screen, check whether an error alert is present and whether it is set to true when there is an error (system error or “geek error”). Confirm that the alert bubbles to the top in the HMI when errors exist.

**Healthy condition:**
With an active error condition, the error alert changes to true and appears at the top (bubbles up).

**Expected result:**
When an AGV error or system error exists, the error alert flag is set to true and bubbles to the top in the HMI.

---

###### Step 4 — Confirm AGV errors and/or system errors sections are populated when the alert indicates an error

**Responsible role:** L1_support

**Instruction:**
If the error alert indicates an error, confirm the Get AGV Status screen is showing AGV errors and/or system errors (described as being populated from the system faults table / active faults).

**Healthy condition:**
AGV errors and/or system errors lists/fields contain entries consistent with the active error condition.

**Expected result:**
When the error alert indicates an error, the AGV errors and/or system errors sections on the Get AGV Status screen are populated.

---

**Success Criteria:**

- When an AGV error or system error exists, the Get AGV Status HMI error alert flag is set to true and bubbles to the top.
- For the selected AGV entry, AGV state and current command vitals (“teal vitals”) are populated.
- When the error alert indicates an error, the AGV errors and/or system errors sections are populated.

**Failure Conditions:**

- Error alert is not set to true while an active AGV/system error condition is observed.
- Error alert does not bubble to the top in the HMI despite an observed AGV/system error.
- Error alert indicates an error but AGV errors/system errors sections are not populated as expected.


</details>

<details><summary>Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up (`proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1`)</summary>

##### Runbook: Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up

- **Procedure ID:** `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `L1_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the RMS / fleet status UI pop-up titled “Overall System AGV Status” to confirm the current overall AGV/AUV system status is populated and capture the displayed overall status wording/values for troubleshooting context.

**When To Use:**
When you need a first confirmation of whether the overall AGV/AUV system status page is populated and what overall status it reports (e.g., to establish whether the system appears reachable vs overall-down/unreachable).

- **Source:** `training_video` / `training_video_day1`

**Procedure Steps:**

###### Step 1 — Open the RMS / fleet status UI and navigate to the “Overall System AGV Status” pop-up

**Responsible role:** L1_support

**Instruction:**
In the RMS / fleet status UI (rms_ui), open the pop-up/page titled “Overall System AGV Status”.

**Healthy condition:**
The pop-up/page titled “Overall System AGV Status” is reachable and displayed.

**Expected result:**
The “Overall System AGV Status” pop-up/page is opened and visible.

---

###### Step 2 — Verify the “Overall System AGV Status” page is populated (not blank/unavailable)

**Responsible role:** L1_support

**Instruction:**
On the “Overall System AGV Status” page, confirm the page shows current status details (i.e., the status content is present rather than blank/unreachable).

**Healthy condition:**
Status content is present on the “Overall System AGV Status” page (the page is not blank/unreachable).

**Expected result:**
The “Overall System AGV Status” page shows current overall AGV/AUV status details (not blank/unavailable).

---

###### Step 3 — Record the displayed overall status value(s) from the pop-up

**Responsible role:** L1_support

**Instruction:**
Record the displayed overall status value(s) shown on the “Overall System AGV Status” page using the exact on-screen wording/fields present.

**Healthy condition:**
The recorded values match the on-screen overall status details currently shown on the page.

**Expected result:**
You have captured the displayed overall status value(s)/wording from the “Overall System AGV Status” pop-up.

---

**Success Criteria:**

- The “Overall System AGV Status” pop-up/page is reachable and populated with current status details.
- The displayed overall status value(s)/wording are recorded from the pop-up.

**Failure Conditions:**

- “Overall System AGV Status” pop-up/page is blank or unavailable (overall system-down/unreachable symptom).


</details>

</details>

---

### 6 — Stop when the supported recovery path does not restore operation (`escalation_gate`)

**Intent:** Hand off when the pairing failure, roster inconsistency, unsafe physical condition, or abnormal hospital routing persists after the available supported checks and authorized recovery path.

**Expects capability:** n/a
**Expects surface:** n/a
**Preferred audience:** L2_support, L3_support

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=remote; tool=WCS/SSMS (read-only) and RMS / AGV status UI): Escalation required due to persistent pairing failure/abnormal routing or unresolved roster inconsistency after supported path, or inability to perform safe/authorized physical handling.

**Branches:**

- `escalate` → `` when Stop and hand off with evidence package

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Pairing failure or unexpected hospital routing confirmed | `node_2` |
| `node_1` | `healthy` | Pairing and routing appear normal or cannot be confirmed | `` |
| `node_2` | `unhealthy` | RMS/WCS indicates unmapped/missing/inconsistent roster state | `node_3` |
| `node_2` | `inconclusive` | Roster/mapping appears coherent or inconclusive | `node_4` |
| `node_3` | `healthy` | Authorized recovery completed; system-side state observable | `node_5` |
| `node_3` | `escalate` | Recovery cannot be performed safely/authorizedly or state persists | `node_6` |
| `node_4` | `healthy` | Hospital diversion absent; pairing/operation normal | `node_6` |
| `node_4` | `unhealthy` | Unexpected hospital diversion persists | `node_6` |
| `node_5` | `healthy` | Successful pairing + stable routing during monitoring | `` |
| `node_5` | `unhealthy` | Validation failure (pairing fails again / diversion continues / roster becomes abnormal) | `node_6` |
| `node_6` | `escalate` | Stop and hand off with evidence package | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1 (low)
- node_1: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
- node_1: proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1 (low)
- node_2: proc_check_rms_disconnected_agv_count_cause_v1 (low)
- node_2: proc_verify_robot_location_model_fields_and_rms_orange_location_types_v1 (low)
- node_3: proc_clear_agv_motionless_fault_using_rms_estop_zone_reset_v1 (low)
- node_3: proc_recover_agv_bump_fault_rms_estop_agv_reset_v1 (low)
- node_3: proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1 (low)
- node_4: proc_check_rms_fleet_status_shutdown_queues_zone_cycling_v1 (low)
- node_4: proc_check_rms_fleet_status_agvs_exchange_waiting_startup_delay_v1 (low)
- node_4: proc_check_hospital_hmi_operations_menu_induct_extract_status_v1 (low)
- node_5: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_5: proc_check_agv_state_command_vitals_active_errors_get_agv_status_v1 (low)
- node_5: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_6: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
