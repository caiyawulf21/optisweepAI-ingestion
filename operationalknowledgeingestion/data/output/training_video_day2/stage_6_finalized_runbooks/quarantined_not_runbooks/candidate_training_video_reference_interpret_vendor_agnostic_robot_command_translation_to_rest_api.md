# Interpret How Generic Robot Commands Are Translated to Vendor REST API via Geek Plus COM Module

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_interpret_generic_robot_command_translation_to_vendor_rest_api_v1` |
| Title | Interpret How Generic Robot Commands Are Translated to Vendor REST API via Geek Plus COM Module |
| Procedure Type | `reference` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `robot_command_or_task_state`, `wcs_api_responsiveness` |
| Access Surface | `wcs_sql`, `wcs_api` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | `api_unresponsive` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the Robot Command Database model command names to understand how OptiSweep’s Robotics module issues generic internal robot commands to the Geek Plus COM module, and how that COM module translates those vendor-agnostic commands into the vendor-specific REST API POST requests (then converts responses back to what OptiSweep expects). This supports vendor-agnostic command modeling and helps interpret why command names remain generic.

## When To Use

When you need to interpret the vendor-agnostic internal robot command model (generic command names) and understand the translation layer that produces vendor REST API POST requests via the Geek Plus COM module.

## Do Not Use For

* Do not use this runbook to verify a specific vendor REST endpoint URL, request payload fields, or response schema—those details are not provided in the source packet.

## Access Or Tools Needed

* Robot Command Database model table view (RobotCommandDatabaseModel) showing generic command names

## Related Operational Context

* ctx_training_video_vendor_agnostic_robot_command_model_v1

## Visual References

![artifact_training_video_training_video_day2_0014_the_robot_command_database_model_table_primary_01_18_59_000](assets/bc80d134a7f69ff3.jpg)

*RobotCommandDatabaseModel command names list (e.g., EmptyGoTo, PickupTote, MoveTote, DropOffTote, RemoveAgv, ReleaseAgv, GoCharge) and description that these are generic internal commands translated by Geek Plus COM module into REST API POST requests.*

![artifact_training_video_training_video_day2_0008_we_use_for_this_database_when_primary_00_11_14_000](assets/f7783ed9b4087772.jpg)

*WCS creates several databases; OptiSweep only utilizes entity logs for logging; includes context about debugging/logging and related database models (Audit Geek, OPC Comms, Robotics, Sworder Sweeper).*

## Procedure Steps

### Step 1 — Review generic command names in RobotCommandDatabaseModel

**Responsible role:** L2_support

**Instruction:**
Open the Robot Command Database model table view (RobotCommandDatabaseModel) and review the listed generic command names shown in the artifact (e.g., EmptyGoTo, PickupTote, MoveTote, DropOffTote, RemoveAgv, ReleaseAgv, GoCharge).

**Expected result:**
You can point to the generic command names in RobotCommandDatabaseModel that represent internal actions (tote pickup/move/drop-off, AGV remove/release, and charging-related commands).

---

### Step 2 — Confirm the commands are internal/generic (not vendor-specific)

**Responsible role:** L2_support

**Instruction:**
Using the source description, confirm that the RobotCommandDatabaseModel commands are described as generic internal commands between the Robotics module and the Geek Plus COM module (and that a different vendor would use a different translation module while keeping the internal command model generic).

**Expected result:**
You can state (based on the source) that these commands are “very generic” and “not vendor specific,” and that the Geek Plus COM module translates them into the vendor REST API POST requests.

**Stop or Escalate If:**

* If you need endpoint/payload verification (URL, request body fields, response fields), stop—this packet does not provide those details.

---

### Step 3 — Interpret the translation path to vendor REST API POST requests

**Responsible role:** L2_support

**Instruction:**
Using the source description, interpret the translation path as: Robotics module issues generic internal commands -> Geek Plus COM module translates them into the actual vendor REST API POST request -> Geek Plus COM module converts it back to the way OptiSweep expects.

**Expected result:**
You can correctly describe the translation layer: Geek Plus COM module is the component that translates internal generic commands into the vendor REST API POST request (and then converts responses back to OptiSweep’s expected format).

**Stop or Escalate If:**

* If you require REST endpoint/payload details, escalate—this packet only states “POST request” and “REST API” without endpoint/payload fields.

---

### Step 4 — If troubleshooting vendor differences, note translation module swap while internal model stays generic

**Responsible role:** L2_support

**Instruction:**
When troubleshooting requires understanding vendor differences, use the source statement that a different vendor would have a different translation module, while the internal command model remains generic.

**Expected result:**
You can explain that vendor-specific behavior is handled by the translation module (Geek Plus COM module for Geek Plus), while the internal command names remain generic in RobotCommandDatabaseModel.

**Stop or Escalate If:**

* If you need API request/response fields (endpoint, payload, response schema), escalate because the packet does not include them.

---

## Success Criteria

* You can identify generic command names in RobotCommandDatabaseModel (e.g., EmptyGoTo, PickupTote, MoveTote, DropOffTote, RemoveAgv, ReleaseAgv, GoCharge).
* You can explain the translation path: Robotics module -> Geek Plus COM module -> vendor REST API POST request, with conversion back to OptiSweep expectations.
* You do not claim endpoint/payload specifics that are not present in the packet.

## Failure Conditions

* You interpret the command names as vendor-specific REST endpoints/payloads (not supported by the packet).
* You attempt to verify REST endpoint/payload/response fields without source evidence.

## Escalation Guidance

* If deeper API-level verification is required (REST endpoint URL, request payload structure, response fields), escalate because the packet only states that the Geek Plus COM module translates commands into a REST API POST request without providing endpoint/payload details.

## Missing Details / Known Gaps

* No REST endpoint URL, request payload fields, or response schema details are provided in the packet (only “POST request” and “REST API”).
* No explicit database column names/fields (e.g., command GUID field name) are provided in the packet for RobotCommandDatabaseModel; only the table is referenced as tracking command status.

## Source Lineage

- Candidate IDs: candidate_training_video_reference_interpret_vendor_agnostic_robot_command_translation_to_rest_api
- Source ID: `training_video_day2`
- Source Type: `training_video`
