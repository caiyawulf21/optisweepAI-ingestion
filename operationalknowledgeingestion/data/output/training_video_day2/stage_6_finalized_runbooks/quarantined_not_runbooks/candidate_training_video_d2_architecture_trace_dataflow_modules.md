# Trace OptiSweep architecture data/command flow across modules (Scanner/PLC → XLE chat/OBC com → Ignition tags → Sorter sweeper → Robotics maps → Geek Plus COM → Geek Plus API)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_trace_optsweep_architecture_data_command_flow_modules_v1` |
| Title | Trace OptiSweep architecture data/command flow across modules (Scanner/PLC → XLE chat/OBC com → Ignition tags → Sorter sweeper → Robotics maps → Geek Plus COM → Geek Plus API) |
| Procedure Type | `reference` |
| Primary Role | `L1_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `fleet_system_status`, `wcs_api_responsiveness` |
| Access Surface | `wcs_api`, `wcs_sql` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the documented OptiSweep architecture path to explain which OptiSweep module owns each part of the UPS-side data/command path: UPS-side scanner/ASX/XLE printers/sorter PLCs communicate via XLE chat over S tunnel to the XLE chat module; the XLE chat OBC com module subscribes to tags and Ignition for read/write with tippers; sorter sweeper acts as a tote state machine; sorter sweeper requests robotics actions (pick up/move out/drop off); robotics routes those actions through named maps; Geek Plus COM translates robotics commands into Geek Plus API requests; Ignition is the HMI base used to collect data and send to Aviva for UPS, running on the OPC server (Windows).

## When To Use

When you need to map a symptom to the most likely owning OptiSweep module by following the documented architecture path (UPS-side equipment → XLE chat/S tunnel → XLE chat OBC com + Ignition tags → sorter sweeper tote state machine → robotics maps → Geek Plus COM → Geek Plus API).

## Access Or Tools Needed

* Ability to reference the architecture terms and module responsibilities as described in the source segment (XLE chat, S tunnel, XLE chat OBC com module, Ignition tags, sorter sweeper tote state machine, robotics module maps, Geek Plus COM, Geek Plus API requests, Aviva for UPS).

## Related Operational Context

* ctx_training_video_optisweep_architecture_overview_v1
* ctx_training_video_xle_chat_and_obc_com_reference_v1
* ctx_training_video_sorter_sweeper_module_reference_v1
* ctx_training_video_robotics_module_and_maps_reference_v1
* ctx_training_video_geekplus_com_translation_reference_v1
* ctx_training_video_ignition_platform_reference_v1

## Visual References

![artifact_training_video_training_video_day2_0003_so_we_kind_of_started_this_primary_00_02_12_500](assets/994a86f756480c79.jpg)

*Architecture overview showing UPS-side equipment (scanner/ASX/XLE printers/sorter PLCs) and OptiSweep modules (XLE chat, XLE chat OBC com, sorter sweeper, robotics module, Geek Plus COM, Ignition/Windows service, OPC server).*

## Procedure Steps

### Step 1 — Identify the UPS-side equipment that interfaces into OptiSweep

**Responsible role:** L1_support

**Instruction:**
Using the architecture overview, name the UPS-side equipment that interfaces into OptiSweep: scanner, ASX, XLE printers, and sorter PLCs.

**Expected result:**
You can correctly state the UPS-side starting equipment list (scanner, ASX, XLE printers, sorter PLCs) as the source of the path that flows into OptiSweep.

---

### Step 2 — Locate the secure UPS-to-OptiSweep communication path via XLE chat and S tunnel

**Responsible role:** L1_support

**Instruction:**
From the architecture overview, describe that UPS-side systems communicate through XLE chat, and that OptiSweep uses S tunnel to securely communicate through XLE chat.

**Expected result:**
You can state that XLE chat is the communication path and that S tunnel is used for secure communication.

---

### Step 3 — Follow the handoff from XLE chat module to XLE chat OBC com module (Ignition tags subscription/read-write)

**Responsible role:** L1_support

**Instruction:**
Using the architecture overview, explain that the XLE chat module talks to the XLE chat OBC com module, and that the OBC com module subscribes to tags and Ignition to enable reading and writing from tippers.

**Expected result:**
You can describe the module handoff: XLE chat module → XLE chat OBC com module, and that OBC com subscribes to tags and Ignition for read/write from tippers.

---

### Step 4 — Trace the next responsibility to the sorter sweeper module (tote state machine)

**Responsible role:** L1_support

**Instruction:**
Using the architecture overview and sorter sweeper module frame, explain that sorter sweeper is basically a tote state machine that tracks packages as they come in, updates information, and tracks it at the tipper.

**Expected result:**
You can state that sorter sweeper is the tote state machine responsible for tracking packages/totes and tracking at the tipper.

---

### Step 5 — Trace sorter sweeper requests to the robotics module (pick up/move out/drop off tote)

**Responsible role:** L1_support

**Instruction:**
Using the architecture overview, describe that sorter sweeper makes requests to the robotics module such as pick up tote, move out tote, and drop off tote.

**Expected result:**
You can list the movement-related requests from sorter sweeper to robotics module: pick up tote, move out tote, drop off tote.

---

### Step 6 — Trace robotics module routing through named maps (entrance/queue/execute for sorter and tipper)

**Responsible role:** L1_support

**Instruction:**
Using the architecture overview, describe that robotics module runs the requests through the maps: shorter entrance sorter queue, sorter sorter execute tipper entrance queue, and tipper tipper execute sorter entrance queue.

**Expected result:**
You can name the map/queue routing responsibilities exactly as listed in the source architecture overview.

---

### Step 7 — Trace vendor translation to Geek Plus COM (robotics commands → Geek Plus API requests)

**Responsible role:** L1_support

**Instruction:**
Using the architecture overview, explain that Geek Plus COM translates commands from the robotics module into what Geek Plus requires and sends them as API requests to Geek Plus.

**Expected result:**
You can describe Geek Plus COM as the translation layer that sends Geek Plus API requests based on robotics module commands.

---

### Step 8 — Use Ignition as the HMI base and note Ignition/OPC server placement (Windows)

**Responsible role:** L1_support

**Instruction:**
Using the architecture overview, describe that Ignition is the HMI base used to collect data and send to Aviva for UPS, and that Ignition/OPC runs on the OPC server (Windows-based).

**Expected result:**
You can state that Ignition is the HMI base for data collection and sending to Aviva for UPS, and that Ignition/OPC runs on the OPC server in a Windows environment.

---

## Success Criteria

* You can describe the documented module-by-module ownership of the data/command path using the source-backed architecture terms: XLE chat/S tunnel → XLE chat OBC com + Ignition tags → sorter sweeper tote state machine → robotics module maps → Geek Plus COM translation → Geek Plus API requests.
* You can correctly name the example movement requests from sorter sweeper to robotics module (pick up tote, move out tote, drop off tote) and the named robotics maps/queues listed in the source.

## Failure Conditions

* You cannot map a symptom to a specific module using the source-described path.
* You cannot name the required module sequence or the named map/queue routing responsibilities from the source.

## Escalation Guidance

* If you cannot map a symptom to a specific module using the source-described path, escalate to deeper troubleshooting documentation for the specific module (XLE chat OBC com module, sorter sweeper module, robotics module/maps, or Geek Plus COM module).

## Missing Details / Known Gaps

* The packet does not provide concrete live troubleshooting inspection steps (e.g., specific SSMS queries, WCS/Helix DB tables, API endpoints, or UI locations) to validate module ownership against live system state.
* The packet does not provide explicit failure signals/fields per module (e.g., which exact tag names, status codes, or request/response identifiers to check).

## Source Lineage

- Candidate IDs: candidate_training_video_d2_architecture_trace_dataflow_modules
- Source ID: `training_video_day2`
- Source Type: `training_video`
