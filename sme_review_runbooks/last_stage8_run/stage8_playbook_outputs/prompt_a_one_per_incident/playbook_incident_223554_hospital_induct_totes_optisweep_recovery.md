# Hospital station unable to induct/add totes; site disrupted until OptiSweep/Hospital Lane recovery

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_223554_hospital_induct_totes_optisweep_recovery` |
| Case ID | `223554` |
| Extraction Mode | `one_playbook_candidate_per_incident` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- Hospital station cannot induct/add totes (totes can sometimes be removed but not added)
- Robot/AGV reported in a shut down state
- Site reported down or unable to start sort (may go down mid-sort)
- Backlog in the hospital area and disrupted tote flow to hospital

## Affected Systems

- ACB hospital station
- Hospital lane
- AGVs/robots
- Totes
- OptiSweep services
- Hospital station server/services (reported)
- Tippers (operator station context mentioned during recovery)

## Nodes

### 1 — Confirm hospital station tote add/induct failure and determine whether the disruption is system-wide or localized (`diagnostic_decision`)

**Intent:** Determine whether the observable hospital induct/add failure aligns with an abnormal system/fleet state that requires OptiSweep/Hospital Lane recovery, versus a localized hospital/tote handling state that still needs targeted validation.

**Expects capability:** fleet_system_status, agv_active_errors, hospital_diversion
**Expects surface:** rms_ui, wcs_sql, hospital_hmi
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1` (low, support, score=0.18, boosted=0.41) — Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Retrieval score 0.1800 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1` (low, support, score=0.1229, boosted=0.3529) — Add or Remove a Robot in the Geek Plus RMS Robot Selection Web View
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).; Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Retrieval score 0.1229 below medium threshold.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `fleet_system_status`: fleet/system-down status — check Overall System RMS / AGV status (optionally WCS system-state models for L2).
- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI & WCS/SSMS (read-only) views): Hospital HMI does not indicate hospital station unavailable/shut down/paused, and telemetry shows no abnormal active errors correlating to hospital lane disruption.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI & WCS/SSMS (read-only) views): Hospital HMI indicates hospital station unavailable/shut down/paused/unready state and WCS/RMS indicates abnormal system/fleet state or active errors during the same disruption window.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI & WCS/SSMS (read-only) views): Hospital HMI behavior is unclear or WCS/RMS telemetry cannot be accessed/read, so whether the disruption is system-wide vs localized cannot be confirmed.
- `escalate` (observer=site_or_remote; tool=RMS / WCS/SSMS (read-only) / Hospital HMI): Telemetry gap prevents confirmation and the system remains down/unable to start sort, indicating need for an outside diagnostic/escalation workflow beyond this single-candidate template.

**Branches:**

- `unhealthy` → `node_2` when Unhealthy: system-wide abnormal state correlating with hospital lane disruption
- `healthy` → `` when Healthy/Localized: hospital add failure without system abnormality

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (2)</summary>

<details><summary>Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests (`proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1`)</summary>

##### Runbook: Remove/Recover a specific AGV by robot ID using OptiSweep→Geek API requests

- **Procedure ID:** `proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1`
- **Procedure Type:** `operation`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Use the OptiSweep / WCS API client to send a Geek request to remove a specified AGV from the system (RemoveAgv) or re-add it (RecoverAGV). Both API actions require the target robot ID.

**When To Use:**
When you need to remove a specific AGV from the system roster (RemoveAgv) or re-add it (RecoverAGV) by sending the correct OptiSweep→Geek API request using the required robot ID.

- **Source:** `training_video` / `training_video_day2`

**Procedure Steps:**

###### Step 1 — Identify the target AGV robot ID for the API request

**Responsible role:** L2_support

**Instruction:**
Obtain the target AGV's robot ID that you will enter into the OptiSweep / WCS API request.

**Healthy condition:**
The robot ID you plan to use corresponds to the intended AGV you are trying to remove/recover.

**Expected result:**
You have a specific robot ID value ready to use for the RemoveAgv and RecoverAGV requests.

---

###### Step 2 — Select RemoveAgv in the OptiSweep / WCS API client and confirm it targets Geek removal by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RemoveAgv and confirm it is described as requiring the robot ID and sending a request to Geek to remove the specified AGV from the system.

**Healthy condition:**
RemoveAgv is the selected action and its description matches: requires robot ID; sends request to Geek to remove the specified AGV from the system.

**Expected result:**
The RemoveAgv action is selected in the API client and is associated with the robot ID input requirement.

---

###### Step 3 — Submit RemoveAgv request with the target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RemoveAgv request in the Apidog / WCS API client using the target robot ID you identified.

**Healthy condition:**
The API client response indicates the request was accepted/executed for RemoveAgv.

**Expected result:**
The RemoveAgv request is submitted and you receive an observable API client response indicating acceptance/execution (success or error).

---

###### Step 4 — Verify RemoveAgv request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RemoveAgv request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Healthy condition:**
Response indicates the request was accepted/executed for RemoveAgv.

**Expected result:**
The API client response for RemoveAgv shows an observable success/acceptance indicator (or an error indicator if it failed).

---

###### Step 5 — Select RecoverAGV in the OptiSweep / WCS API client and confirm it targets Geek add by robot ID

**Responsible role:** L2_support

**Instruction:**
In the Apidog / WCS API client, select the API action named RecoverAGV and confirm it is described as requiring the robot ID and sending a request to Geek to add the specified AGV to the system.

**Healthy condition:**
RecoverAGV is the selected action and its description matches: requires robot ID; sends request to Geek to add the specified AGV to the system.

**Expected result:**
The RecoverAGV action is selected in the API client and is associated with the robot ID input requirement.

---

###### Step 6 — Submit RecoverAGV request with the same target robot ID

**Responsible role:** L2_support

**Instruction:**
Submit the RecoverAGV request in the Apidog / WCS API client using the same robot ID used for RemoveAgv.

**Healthy condition:**
The API client response indicates the request was accepted/executed for RecoverAGV.

**Expected result:**
The RecoverAGV request is submitted and you receive an observable API client response indicating acceptance/success (or error).

---

###### Step 7 — Verify RecoverAGV request corresponds to intended action and response indicates acceptance/success

**Responsible role:** L2_support

**Instruction:**
Review the RecoverAGV request/response in the Apidog / WCS API client and verify the response indicates acceptance/execution (success vs error).

**Healthy condition:**
Response indicates the request was accepted/executed for RecoverAGV.

**Expected result:**
The API client response for RecoverAGV shows an observable success/acceptance indicator (or an error indicator if it failed).

---

**Success Criteria:**

- RemoveAgv request is accepted/executed for the specified robot ID (observable success/acceptance in the API client response).
- RecoverAGV request is accepted/executed for the same robot ID (observable success/acceptance in the API client response).

**Failure Conditions:**

- API client response indicates RemoveAgv failed/error.
- API client response indicates RecoverAGV failed/error.
- Robot ID is incorrect or missing (request cannot target intended AGV).


</details>

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

### 2 — Perform approved OptiSweep/Hospital Lane recovery when abnormal system state is indicated (`procedure_reference`)

**Intent:** Execute the approved recovery path for OptiSweep services and restart/bring Hospital Lane back to an operational state when the diagnostic indicates abnormal system disruption.

**Expects capability:** n/a
**Expects surface:** ignition_gateway, event_viewer, hospital_hmi
**Preferred audience:** L2_support

**Runbook Links:**

- `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1` (low, support, score=0.6207, boosted=0.7907) — Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_non_recoverable_operator_station_motor_fault_mcp_dual_f3_v1` (low, operator, score=0.6148, boosted=0.7848) — Recover Non-Recoverable Operator Station Motor Fault Using MCP_Dual (F3) Manual Jog, Reset, and Cycle Start
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1` (low, support, score=0.6065, boosted=0.7765) — Recover Empty AGVs That Lost Tasks After RMS Restart (Remove/Re-add AGVs Twice)
  - gaps: Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `hospital_diversion`: hospital-lane diversion — ask site about hospital stacklight/lane routing; check Hospital HMI and RMS fleet routing (optionally hospital DB models for L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI & overall system availability indicators): Approved recovery actions completed and hospital lane becomes operational; hospital induct/add is restored or system transitions out of shut down/unavailable state.
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI & WCS/SSMS (read-only) views): Recovery attempt does not transition hospital lane/hospital station out of unavailable state and induct/add remains blocked; telemetry remains abnormal.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI & WCS/SSMS (read-only) views): Recovery steps are performed but there is insufficient telemetry/HMI visibility to confirm lane operational transition.

**Branches:**

- `healthy` → `node_3` when Recovery completed (Hospital Lane operational again)
- `unhealthy` → `` when Recovery not completed / still unhealthy

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (1)</summary>

<details><summary>Recover Non-Recoverable Operator Station Motor Fault Using MCP_Dual (F3) Manual Jog, Reset, and Cycle Start (`proc_recover_non_recoverable_operator_station_motor_fault_mcp_dual_f3_v1`)</summary>

##### Runbook: Recover Non-Recoverable Operator Station Motor Fault Using MCP_Dual (F3) Manual Jog, Reset, and Cycle Start

- **Procedure ID:** `proc_recover_non_recoverable_operator_station_motor_fault_mcp_dual_f3_v1`
- **Procedure Type:** `recovery`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
When a non-recoverable operator station motor fault (e.g., motor overload) cannot be recovered in software, use the operator station HMI MCP_Dual screen (F3) to stop the cycle, enter manual jog mode, clear any axis faults with RESET, jog the correct axes to reposition the tote on/near the robot, then return to automatic mode and press CYCLE START to release the grippers and command the robot to the hospital station. After the robot leaves the tipper, press RESET.

**When To Use:**
Use this procedure when the operator station has a non-recoverable motor fault (example given: motor overload) and the station needs to be manually reset so the tote can be repositioned and the robot can be commanded to the hospital station.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Navigate to MCP_Dual (F3) on the operator station HMI

**Responsible role:** operator

**Instruction:**
On the operator station HMI, navigate to the "MCP_Dual" screen (F3).

**Healthy condition:**
MCP_Dual (F3) is visible and shows the Manual Mode Fault area and axis status indicators (Z1, Z2, A2, A1).

**Expected result:**
The MCP_Dual (F3) screen is displayed with the Manual Mode/Fault area and the visible controls used for recovery (including RESET and cycle controls).

---

###### Step 2 — Stop the tipping cycle with CYCLE STOP

**Responsible role:** operator

**Instruction:**
Press CYCLE STOP to stop the tipping cycle.

**Healthy condition:**
CYCLE STOP has been pressed and the cycle is in a stopped state.

**Expected result:**
The tipping cycle is stopped (cycle is halted) on the MCP_Dual (F3) screen.

---

###### Step 3 — Enter manual jog mode with JOG

**Responsible role:** operator

**Instruction:**
Press JOG to enter manual jog mode.

**Healthy condition:**
Manual Mode is indicated and the manual jog controls are available.

**Expected result:**
Manual jog mode is active (Manual Mode indicator/status is shown) on MCP_Dual (F3).

---

###### Step 4 — Clear any axis faults with RESET

**Responsible role:** operator

**Instruction:**
If any of the axes show a fault, press RESET to clear the fault.

**Healthy condition:**
No axis fault indicators remain visible on MCP_Dual (F3) after RESET.

**Expected result:**
Axis fault indicators clear after pressing RESET (no longer indicated on the affected axis/axes).

---

###### Step 5 — Jog axes to reposition the tote on/near the robot

**Responsible role:** operator

**Instruction:**
If the tote is lifted off the robot, jog either the Z-axis or A-axis, or both, to position the tote on or nearly on the robot. Use A1 and Z1 for the left axis; use A2 and Z2 for the right tipper.

**Healthy condition:**
Tote is positioned on/near the robot using the correct left/right axis controls (A1/Z1 for left; A2/Z2 for right).

**Expected result:**
The tote is positioned on or nearly on the robot by jogging the correct axis controls (left: A1/Z1, right: A2/Z2).

---

###### Step 6 — Return to automatic mode with AUTO

**Responsible role:** operator

**Instruction:**
Press AUTO to enter automatic mode.

**Healthy condition:**
AUTO mode is entered and the screen reflects automatic mode context.

**Expected result:**
Automatic mode is active (Manual Mode indicator clears/changes) on MCP_Dual (F3).

---

###### Step 7 — Start cycle with CYCLE START to release grippers and command hospital

**Responsible role:** operator

**Instruction:**
Press CYCLE START. The grippers will release and the robot will be commanded to go to the hospital station.

**Healthy condition:**
After pressing CYCLE START, grippers release and robot proceeds toward the hospital station.

**Expected result:**
Grippers release and the robot is commanded to go to the hospital station.

---

###### Step 8 — After robot leaves tipper, press RESET

**Responsible role:** operator

**Instruction:**
After the robot has left the tipper, press RESET.

**Healthy condition:**
Robot has left the tipper and RESET is pressed as the final action in the sequence.

**Expected result:**
RESET is pressed after robot departure from the tipper, completing the recovery sequence.

---

**Success Criteria:**

- Axis faults are cleared after pressing RESET in manual jog mode.
- Tote is positioned on or nearly on the robot using the correct axes (A1/Z1 for left; A2/Z2 for right).
- After pressing AUTO then CYCLE START, grippers release and the robot is commanded to go to the hospital station.
- After the robot has left the tipper, pressing RESET completes the recovery sequence.

**Failure Conditions:**

- Axis fault indicators remain after pressing RESET in manual jog mode.
- CYCLE START does not cause gripper release and does not command the robot to the hospital station.


</details>

</details>

<details><summary><strong>Support runbooks</strong> (2)</summary>

<details><summary>Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery) (`proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1`)</summary>

##### Runbook: Add an AGV to a Zone When There Is No Empty AGV Available (RMS Fault Recovery)

- **Procedure ID:** `proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Recover operation by stopping RMS, physically placing an AGV into the zone under the tote rack, adding the AGV in RMS using Tote API Controls, verifying the AGV turns blue and reaches AGV status/state "szonestaging" on the Hospital HMI/lane UI, then stopping again and resuming RMS.

**When To Use:**
Use when there is no empty AGV available for a zone and you must recover by adding an AGV into the zone under the tote rack, ensuring it reaches the required "szonestaging" state before resuming RMS.

**Safety Notes:**

- E-stop RMS before making the AGV add/recovery changes in RMS.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — E-stop RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), press the E-stop for RMS.

**Healthy condition:**
E-stop control shows RMS is stopped (not running).

**Expected result:**
RMS is in an E-stopped state on the RMS / fleet status UI.

---

###### Step 2 — Move an AGV into the zone under the tote rack

**Responsible role:** L2_support

**Instruction:**
Move an AGV into the zone under the tote rack (physical_floor).

**Healthy condition:**
AGV is placed in the intended zone location under the tote rack (no mismatch between intended zone and physical placement).

**Expected result:**
An AGV is physically positioned in the zone under the tote rack.

---

###### Step 3 — Add the AGV in RMS using Tote API Controls

**Responsible role:** L2_support

**Instruction:**
On the RMS / fleet status UI (rms_ui), add the AGV using the "Tote API Controls" function.

**Healthy condition:**
After adding, the AGV begins the transition that results in the AGV turning blue.

**Expected result:**
The AGV is added in RMS via Tote API Controls (AGV appears in RMS roster/map context for the add operation).

---

###### Step 4 — Wait for the AGV to turn blue on the RMS UI

**Responsible role:** L2_support

**Instruction:**
Wait for the AGV to turn blue on the RMS / fleet status UI (rms_ui).

**Healthy condition:**
AGV indicator on RMS transitions to blue after the add action.

**Expected result:**
The added AGV changes to blue on the RMS UI.

---

###### Step 5 — Verify AGV status/state is exactly "szonestaging" on the Hospital HMI

**Responsible role:** L2_support

**Instruction:**
On the Hospital HMI / lane UI (hospital_hmi), verify the AGV status/state is exactly "szonestaging".

**Healthy condition:**
AGV state/status equals exactly "szonestaging".

**Expected result:**
Hospital HMI shows the AGV state/status value "szonestaging".

---

###### Step 6 — If AGV is moving to the Hospital, remove and add it again

**Responsible role:** L2_support

**Instruction:**
If the AGV is moving to the Hospital (Hospital HMI shows Hospital destination/state), remove the AGV and add it again (repeat the add step).

**Healthy condition:**
After remove/re-add, the AGV can reach "szonestaging" on the Hospital HMI.

**Expected result:**
AGV is removed from the system and then re-added so it can transition back toward "szonestaging".

---

###### Step 7 — Press E-stop again on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
Press the E-stop again on the RMS / fleet status UI (rms_ui).

**Healthy condition:**
E-stop control indicates RMS is stopped (not running).

**Expected result:**
RMS reflects the E-stopped state again on the RMS / fleet status UI.

---

###### Step 8 — Resume RMS on the RMS / fleet status UI

**Responsible role:** L2_support

**Instruction:**
Resume RMS on the RMS / fleet status UI (rms_ui) (Starting the System procedure reference).

**Healthy condition:**
RMS shows resumed/started state after the second E-stop press.

**Expected result:**
RMS is resumed/started on the RMS / fleet status UI.

---

**Success Criteria:**

- The selected AGV appears as blue on the RMS UI.
- The Hospital HMI shows the AGV status/state exactly "szonestaging".
- RMS is resumed after the second E-stop press.

**Failure Conditions:**

- AGV does not reach "szonestaging" after being added.
- AGV repeatedly moves to the Hospital instead of staging.
- RMS cannot be resumed after the second E-stop press.


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

### 3 — Validate hospital induct/add and overall sort flow stability after recovery (`validation_gate`)

**Intent:** Confirm that the hospital station can add/induct totes again and that the system remains stable (no immediate recurrence of site-down / unable-to-start-sort behavior).

**Expects capability:** fleet_system_status, agv_active_errors, zone_pairing_state
**Expects surface:** hospital_hmi, rms_ui, wcs_sql
**Preferred audience:** operator, L2_support

**Runbook Links:**

- `proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1` (low, support, score=0.582, boosted=1.0) — Access RMS web application via site Argus server IP and verify the RMS overview screen loads
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1` (low, support, score=0.6797, boosted=1.0) — Check AUV/AGV overall fleet status using the “Overall System AGV Status” pop-up
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.
- `proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1` (low, support, score=0.7179, boosted=1.0) — Check Geek+ RMS overall page for system faults vs AGV system faults (and handle blank RMS due to firewall)
  - gaps: Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).; Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `agv_active_errors`: AGV active errors — check RMS active AGV faults and/or WCS/SSMS SystemActiveErrorModel (L2).
- Missing corroboration for `zone_pairing_state`: zone pairing failure — ask site whether the zone can obtain a pair; check RMS zone/AGV status and/or remote WCS pairing-related views (L2).

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=Hospital HMI indicators + RMS / WCS (read-only)): Hospital add/induct restored and sort flow is stable (no immediate recurrence of site-down / unable-to-start-sort).
- `unhealthy` (observer=site_or_remote; tool=Hospital HMI indicators + RMS / WCS (read-only)): Validation fails: hospital induct/add remains unavailable or sort cannot start / goes down again.
- `inconclusive` (observer=site_or_remote; tool=Hospital HMI indicators + RMS / WCS (read-only)): Partial improvement observed but telemetry and/or error visibility is unavailable/unreadable, preventing confirmation of stability.
- `escalate` (observer=site_or_remote; tool=Hospital HMI indicators + RMS / WCS (read-only)): Hospital induct/add still fails and system remains abnormal after recovery validation; escalate outside this candidate template.

**Branches:**

- `healthy` → `` when Validation success: stable hospital induct/add and sort flow
- `escalate` → `` when Validation failure: still unable to induct/add or system goes down again

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

</details>

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Unhealthy: system-wide abnormal state correlating with hospital lane disruption | `node_2` |
| `node_1` | `healthy` | Healthy/Localized: hospital add failure without system abnormality | `` |
| `node_2` | `healthy` | Recovery completed (Hospital Lane operational again) | `node_3` |
| `node_2` | `unhealthy` | Recovery not completed / still unhealthy | `` |
| `node_3` | `healthy` | Validation success: stable hospital induct/add and sort flow | `` |
| `node_3` | `escalate` | Validation failure: still unable to induct/add or system goes down again | `` |

## Unresolved / Low-Confidence Links

- node_1: proc_remove_recover_agv_by_robot_id_optisweep_geek_api_v1 (low)
- node_1: proc_add_or_remove_robot_in_geek_plus_rms_robot_selection_web_view_v1 (low)
- node_2: proc_add_agv_to_zone_no_empty_agv_rms_fault_recovery_v1 (low)
- node_2: proc_recover_non_recoverable_operator_station_motor_fault_mcp_dual_f3_v1 (low)
- node_2: proc_recover_empty_agvs_lost_tasks_after_rms_restart_remove_readd_twice_v1 (low)
- node_3: proc_access_rms_web_ui_via_site_argus_ip_and_verify_overview_v1 (low)
- node_3: proc_check_auv_agv_overall_fleet_status_overall_system_agv_status_popup_v1 (low)
- node_3: proc_check_geek_rms_overall_system_faults_vs_agv_faults_v1 (low)
