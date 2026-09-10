# Day 2 / Ontology Deep Dive: Why Backend (SQL/SSMS) Evidence Loses to RMS/UI

**Date:** 2026-08-07
**Trigger:** Case 218550 and 223554 playbooks (`data/output/debug/stage8_four_case_review/.../prompt_a_one_per_incident/`)
skew RMS/UI-heavy on diagnostic nodes that are conceptually about backend state
(AGV state, hospital tote flow, exchange sequence/backfill), even though a rich
SQL/SSMS ontology catalog already exists. This doc is the requested deep dive
before touching playbook-generation prompts again — it separates "the ontology
content is too shallow" from "the ontology content exists but never reaches
Stage 8's scoring," and records the concrete changes applied plus what remains
open.

**Bottom line:** the ontology *content* (`docs/ontology/catalogs/wcs_sql_catalog.json`)
was already deep — 51 documented models with fields, enums, and evidence. The
actual defects were (1) a **wiring gap**: `capability_catalog.json`'s
`support_contract` was empty for 18 of 26 capabilities (including
`agv_active_errors` / `wcs_system_faults`, used by both target playbooks),
which silently zeroed Stage 8's surface-match scoring bonus for SQL
candidates on those nodes; and (2) a **linking-code gap**: Stage 8's
`filter_intent_compatible_matches` only allowed SQL/SSMS candidates through
its filter for roster/mapping-flavored nodes — hospital-flow and
sequence/backfill nodes had no equivalent allowance. One genuine **content**
gap remains: `zone_pairing_state` has no dedicated SQL model anywhere in the
operational corpus (confirmed, not assumed — see §5).

---

## 1. Day 2 procedure → backend mapping (108 files)

All 108 Day 2 training-video runbook candidates were read in full — 80
quarantined-as-not-a-runbook candidates plus 28 kept/finalized runbooks under
`operationalknowledgeingestion/data/output/training_video_day2/stage_6_finalized_runbooks/`.
Each was checked against `wcs_sql_catalog.json`'s existing model list.

### Already well documented (confirmed, no gap)

The large majority of Day 2 procedures map cleanly onto models the catalog
already documents in full: `AgvActiveErrorDatabaseModel` / `AgvErrorModel` /
`SystemActiveErrorModel` / `SystemErrorActivityModel` (error lookup +
active-error rows), `RobotCommandDatabaseModel` / `RobotTaskDatabaseModel`
(+ their `RobotCommandActivity` / `RobotTaskActivity` archives),
`SystemDatabaseModel` (system status + sort GUID, full enum), `HospitalTagsModel`
(`TagTypeParent` in/out), `TipperDepartureActivityModel`, `ShutDownStaging`,
`ChargingDatabaseModel` / `ChargingLocationDatabaseModel` /
`ChargingThresholdsDatabaseModel`, and the top-level WCS database taxonomy
(Audit / GeekAgv / OPCComms / Robotics / SorterSweeper / EntityLogs). These
needed no changes.

Roughly 25–30 of the 108 files are pure UI/RMS/Ignition/Windows-Service
surface documentation with no backend model behind them at all (Map Monitor
E-stop checks, Ignition gateway sys-perf, Windows Services status, stunnel
connection checks, memory-trend HMI reads, process/meta references like
admin-password handover). These are correctly surface-only and are **not**
ontology gaps — they should stay RMS/Ignition/Windows-Services-tagged.

### Genuine gaps found and fixed in this pass

| Model | Gap | Day 2 source | Fix applied |
| --- | --- | --- | --- |
| `SortLocationsDatabaseModel` | All 4 fields flagged `needs_sme`; zone→sequence→station lookup mechanism undocumented | `candidate_training_video_d2_sorter_zone_exit_queue_sequence_mapping_lookup` | Documented the (zone, shutdown-queue-sequence) → station/location lookup mechanism, the sequence-1–4-from-sorter-entrance-queue rule, and compression-preserves-order behavior, with example outputs (station 300; zone 3→301; zone 3→2302) |
| `HospitalTagsModel."Value / variable type columns"` | Flagged `needs_sme`; zero/one value-column selection mechanism undocumented | `candidate_training_video_d2_hospital_tag_variable_type_value_column_lookup` | Documented the variable-type → lookup-table → single active zero/one value-column mechanism |
| `RobotLocationDatabaseModel` | Coordinate field semantics absent | `candidate_training_video_d2_robot_location_model_interpret_location_fields` | Added `Coordinates (XY)` field: lat/long-style, unit = centimeters |
| `ChargingThresholdsDatabaseModel` | Emergency-charging cross-sorter-side fallback rule absent | `candidate_training_video_day2_charging_db_model_tables_interpret` | Documented fallback (use another sorter side's free charger) + lowest-charge cycling behavior |
| `RobotCommandDatabaseModel` | "Sent time" / "in-progress time" lifecycle fields and queue-capacity implication absent | `candidate_training_video_diagnostic_robot_command_database_model_table_status` | Added both fields; documented that in-progress frees destination queue/location capacity, and that sent-without-in-progress indicates a stuck command |
| `SorterSideDatabaseModel.Disabled` | Field existed but the phase-based CSV-load business rule was undocumented | `candidate_training_video_diagnostic_sorter_side_disabled_phase_configuration_csv_enable_phase` | Documented that a sorter side reading `Disabled` during phased cutover may be expected config (not in phase-one CSV load yet), flipped later by a phase-based DB update script |

`LocationActiveDwellModel`'s archive cross-reference (`LocationDwellActivity`)
was checked and found **already present** in the catalog (line ~1968) — the
research pass that flagged it as missing was wrong on this one point; no
change was needed.

### Confirmed remaining gap — since resolved (see §1a)

`RobotDatabaseModel`'s core fields (`State`, `ToteName`, `AssignedSorterSide`,
`CurrentLocationId`, `DestinationLocationId`) were flagged `needs_sme` in this
pass because no Day 2 file in the 108-file corpus narrates this model's
fields directly. That gap was closed in a follow-up pass once the source
"OptiSweep Training Slides [INTERNAL ONLY].pdf" deck was supplied directly —
see §1a below for what changed.

---

## 1a. Follow-up pass: full training-slides PDF supplied directly (2026-08-07, later same day)

The user subsequently supplied the full "OptiSweep Training Slides [INTERNAL
ONLY].pdf" deck — the same underlying training material Day 2's OCR/transcript
pipeline had only partially captured. This deck's live-query screenshots
(SSMS results with real column names and example values) let several
previously-`needs_sme` gaps get closed with actual schema detail instead of
paraphrased mechanism descriptions.

**Resolved in `wcs_sql_catalog.json`:**

| Model | What changed |
| --- | --- |
| `RobotDatabaseModel` | Full field list added from a live query screenshot (p.77): `Name, State, ToteId, SorterSideId, CurrentLocationId, DestinationLocationId, CommandId, ChargesSinceLastCharged, ChargeKick, Status, ErrorCode, Coordinate, CellCode, Angle, Battery, Current, Voltage, Temperature, Ip, IsToteEmpty, LastCommandGuid`. Full `State` enum families (Tipper/Hospital/Charger/Sorter [In/Out, Queue, Locations, GLD]/ShutDown) added from pp.78-80. This closes the confirmed-remaining-gap noted above — the "Day2 has no field-level detail for this model" limitation no longer applies once the full slide deck is available. Two prior field names were corrected: `ToteName` → `ToteId`, `AssignedSorterSide` → `SorterSideId`. |
| `RobotLocationDatabaseModel` | `LocationStatus` enum confirmed (`Enabled/Stopped/Disabled`, was `needs_sme`); added `Sequence`, `CellCode`, `LastSent` fields from a live query screenshot (p.70). |
| `SortLocationsDatabaseModel` | Real column names confirmed: `SorterId, StagingId, QueueId, Sequence, SorterSideDatabaseModelId` (was `needs_sme` on all 4 fields). Clarified `QueueId` is specifically where an empty-tote AGV stages to backfill the `SorterId` location during an exchange. |
| `ChargingDatabaseModel` / `ChargingLocationDatabaseModel` / `ChargingThresholdsDatabaseModel` | Real column names and live example values added: `ChargingDatabaseModel.Name` (e.g. ChargerArea1-3); `ChargingLocationDatabaseModel.{SorterId,Charger,ToteStandId,Sequence,ChargingDatabaseModelId}`; `ChargingThresholdsDatabaseModel.{Charged=80,CanBeKicked=50,GoCharge=40,EmergencyCharge=30}` (was `needs_sme` on all three). |
| `HospitalDatabaseModel` / `HosptialSorterSideDatabaseModel` / `CellCodeDatabaseModel` | Real column names added: `HospitalDatabaseModel.{Name,EntranceId,DropOffId,InductionId,ExitId,Disabled}`; `HosptialSorterSideDatabaseModel.{SorterId,HospitalDatabaseModelId}` (was fully `needs_sme`); `CellCodeDatabaseModel.{CellCode,X,Y,HospitalDatabaseModelId}` (was fully `needs_sme`). |
| `EntityLogs.DeveloperLogs` | Full field list added: `EntityInserted, Id, Message, Level, Exception, TraceId, HostName, InstanceName, AssemblyName, ClassName, MethodName, LineNumber` — resolves the "EntityLogs field detail is thin" gap noted in the original Day 2 mapping. |
| `Audit.TaskIdToRequestId` | Real column names confirmed: `AgvId, GeekPlusTaskId, AgvCommandRequestId` (prior doc used placeholder names `GeekTaskId`/`CommandGuid`). |
| `GeekAgvActionLoggingModel` / `LatticeCodeModel` / `OpcConfiguration` / `OpcTags` | Full field lists added, resolving the "column-level names not listed in Day2 narration" gaps noted for all four models. |
| `HospitalTagsModel` | Full field list added: `TagTypeParent, TagTypeChild, TagPath, VariableType, StringValue, IntValue, UintValue, BoolValue, Date_Time, HospitalStationId` — resolves the `needs_sme` gap on the "Value / variable type columns" mechanism flagged in the original pass (§1, table row 2). `VariableType` is the actual selector column (values `BoolVal/StringVal/IntVal/UintVal`), confirming the zero/one active-column mechanism Day 2 only described narratively. |

`capability_catalog.json`'s `device_roster_state.field_highlights` entries for
`RobotDatabaseModel` were updated to match the corrected field names and
`needs_sme: false`.

All changes cite `optisweep_training_slides` as the source with page numbers;
none invent schema not directly visible in a slide screenshot or explicitly
stated in slide prose. 103/103 Stage 8 tests still pass after these edits.

---

## 2. Root-cause trace: why 218550 and 223554 skew RMS/UI

Two independent, code-verified mechanisms were found — not a single bug, and
not (only) a source-evidence problem.

### 2a. Stage 5 was source-grounded correctly — this is not the cause

`stage4_evidence_chunks.json` for both cases was searched for `SQL`, `SSMS`,
`Helix`, `WCS`, `database` — **zero hits in both cases**. The humans in these
incidents only ever referenced RMS, Hospital HMI, and AVEVA. Per
`docs/ontology/stage5_surface_evidence_guidance.md` ("do not add RMS, HMI,
AVEVA, SQL/SSMS... unless the original source explicitly names the surface"),
Stage 5 correctly stayed source-grounded and correctly deferred the
surface decision to Stage 8 via `stage8_candidate_surfaces: ["rms_ui",
"wcs_sql", ...]` on the relevant nodes. **Stage 5's behavior is not the
problem.**

Contrast: case 228086's own evidence chunk **does** show a real SSMS
screenshot (`artifact_incident_228086_page_024_embedded_image_01`: "SQL
Server Management Studio open to a robotics-related database... AGV or robot
state values including LeavingCharger, MovingToChargerExitQueue"), which is
why that case could legitimately elevate `wcs_sql` with `explicit_source`/
`source_artifact_visible` provenance. 218550/223554 have no equivalent
artifact, so they cannot get this same explicit elevation — that's a fact
about their evidence, not a defect.

### 2b. Stage 8 retrieval scored SQL candidates as eligible — then lost the ranking (wiring gap)

Per-node retrieval telemetry (`retrieval_decision_telemetry.json`,
`canonical_playbooks.json`'s `retrieval_eligibility_trace`) shows, for
218550 node_2 ("Check for AGV inactivity or active fault evidence"), **both**
SQL runbooks scored as `eligible: true` with zero exact-fit gaps:

```
proc_wcs_helix_db_ssms_agv_state_inspection_v1        combined=0.5744  eligible=true, gaps=[]
proc_query_active_agv_errors_from_the_wcs_database_v1 combined=0.5745  eligible=true
```

but ranked below the RMS candidate that was actually linked:

```
proc_check_rms_fleet_status_agvs_exchange_waiting...  combined=0.6048  <- selected
```

Traced to source: `capability_catalog.json`'s `agv_active_errors` entry (used
by this exact node) had rich `sql_model_links` / `field_highlights` /
`primary_access_surfaces: [rms_ui, wcs_sql, wcs_api]` sitting right next to an
**empty** `"support_contract": {}`. Stage 8's scoring code reads only the
populated field:

```python
# shared_pipeline_stages/stage_8/link_scoring.py — node_expects_surfaces()
for item in node.get("ontology_capabilities") or []:
    contract = item.get("support_contract")
    if not isinstance(contract, dict):
        continue
    surfaces.update(contract.get("diagnostic_surfaces") or [])
```

Since `agv_active_errors.support_contract` was `{}`, `node_expects_surfaces()`
returned an empty set for this node, so the `+0.10`/`+0.08` surface-match
bonus in `link_scoring.py` never fired for **either** candidate — the only
remaining tiebreaker was the audience-role bonus, which favors the RMS
runbook (`audience_roles: [operator, L1_support]`, matching the node's
`preferred_audience`) over the SQL runbook (`audience_roles: [L2_support]`
only). A count across the catalog: **18 of 26 capabilities had `support_contract:
{}`**, including `agv_active_errors` and `wcs_system_faults` — exactly the two
capabilities the AGV-state/system-fault nodes in both target playbooks rely
on. Only 8 capabilities (`device_roster_state`, `hospital_diversion`,
`gateway_health`, `wcs_service_health`, `wcs_api_responsiveness`,
`windows_service_or_event_log`, `robot_command_or_task_state`,
`tote_lifecycle_state`) had a populated contract — which is also why
228086's roster/gateway/service-health nodes worked better: they happened to
land on already-wired capabilities.

**Fix applied:** populated `support_contract` (with `backend_mappings`
pointing at the already-documented `wcs_sql_catalog.json` models/fields) for
`agv_active_errors`, `wcs_system_faults`, `tote_exchange_sequence`, and
`zone_pairing_state` in `docs/ontology/catalogs/capability_catalog.json`. No
new SQL facts were invented — every field name and model reference was
copied from the `sql_model_links`/`field_highlights` blocks that were already
sitting unused in the same capability record.

### 2c. Stage 8's linking-code filter had no SQL-allowance for hospital/pairing or sequence/backfill nodes (code gap)

Separately, and more decisively for 223554: `filter_intent_compatible_matches`
in `shared_pipeline_stages/stage_8/normalize.py` filters candidates per node
category. For roster/mapping nodes (`node_needs_roster_mapping_check`,
`shared_pipeline_stages/stage_8/link_scoring.py:888`), the allowed-candidate
branch explicitly includes `runbook_is_wcs_sql_diagnostic_state(runbook,
match)` — a recognizer function
(`shared_pipeline_stages/stage_8/link_scoring.py:631`) written specifically to
"recognize read-only Helix/SSMS state evidence even without RMS wording."

But the parallel branch for pairing/hospital nodes
(`node_needs_pairing_validation`, driven by `PAIRING_VALIDATION_NODE_PATTERN`
= `pair|pairing|hospital lane|hospital diversion|hospital workflow|fleet
behavior`) **did not** include `runbook_is_wcs_sql_diagnostic_state` in its
allowed set — only `runbook_is_fleet_rms_status_check` or a generic
RMS/fleet/pair/hospital status-check regex. There was also no predicate at
all for AGV-exchange-sequence/backfill nodes (218550's core diagnostic
topic — "front AGV moved out without the trailing AGV backfilling").

This directly contradicts the already-written policy in
`docs/ontology/playbook_expects_guidance.md`: *"Treat `rms_ui` and `wcs_sql`
as equal-weight corroboration paths... Do not treat RMS as the primary and
SSMS as optional."* The code implemented that policy for one node category
and not the others.

**Fix applied** (`shared_pipeline_stages/stage_8/normalize.py`,
`shared_pipeline_stages/stage_8/link_scoring.py`):

1. Added `runbook_is_wcs_sql_diagnostic_state(runbook, match)` to the allowed
   set for `node_needs_pairing_validation` nodes (was missing).
2. Added two new node predicates, mirroring `node_needs_roster_mapping_check`
   exactly:
   - `node_needs_hospital_flow_check` — hospital lane/diversion/workflow/
     induct/extract/queue/station/tote-flow nodes.
   - `node_needs_sequence_backfill_check` — backfill/out-of-sequence/
     trailing-AGV/exchange-sequence/shutdown-queue-sequence/tote-association
     nodes.
3. Wired both into `filter_intent_compatible_matches` with the same
   allowed-candidate shape as the roster/mapping branch: fleet RMS status
   check, hospital UI reference (hospital-flow only), `wcs_sql` diagnostic
   state, or a topic-matching generic status check. Neither branch forces a
   SQL link — they only stop the filter from *excluding* an eligible SQL
   candidate, exactly like the existing roster/mapping branch.

All 103 existing Stage 8 tests
(`test_stage_8_5_relationship_linking.py`, `test_stage_8_playbook_finalization.py`,
`test_stage_8_retrieval_eligibility.py`) still pass after these changes.

### 2d. The "home-case" retrieval boost structurally favors incident-native runbooks

`shared_pipeline_stages/stage_8/runbook_search.py`'s
`preferred_incident_source` logic gives `boosted_score: 1.0` when a
candidate runbook's source case matches the case being linked. Case 228086's
SQL runbook (`proc_wcs_helix_db_ssms_agv_state_inspection_v1`) was itself
*derived from* case 228086's own SSMS screenshot, so it gets this boost on
228086's own playbook. 218550/223554 have no incident-native SQL runbook of
their own, so they structurally cannot receive this same boost regardless of
how well the ontology is documented. This is a scoring-mechanism fact worth
knowing, not a defect to fix — it is working as designed (prefer a
case-native procedure when one exists) and is noted here only so it isn't
mistaken for another instance of the wiring gap in §2b.

---

## 3. Genuine content gap: `zone_pairing_state` has no SQL model anywhere in the corpus

Before treating this as unfixable, the full operational corpus was searched
for hidden pairing-specific SQL evidence — Day 2, the OM manual
(`manual_optisweep_om_v3`), all four review incident cases (including 228723,
the dedicated zone-pairing/roster case), and the existing design doc
`docs/plan_catalog_sql_runbooks_roster_hospital.md`. Result:

- 228723's own Stage 5 evidence states outright: *"does not provide readable
  RMS field names or a validated mapping from the red table entries to a
  specific pairing state"* — its source is RMS-only.
- `docs/plan_catalog_sql_runbooks_roster_hospital.md` already lists filling
  `zone_pairing_state`'s empty `sql_model_links` as explicitly **out of
  scope** for that plan (separate catalog work, not yet done).
- No Day 2 or OM-manual procedure names a pairing-specific table or model.

There is no real SQL model to document here — inventing one would violate
this project's own source-grounding rule (`stage5_surface_evidence_guidance.md`:
do not add a surface/model the source doesn't support). Instead,
`zone_pairing_state`'s new `support_contract` (see §2b fix) cross-links it to
the already-evidenced `RobotDatabaseModel`/`RobotLocationDatabaseModel` fields
used by `device_roster_state`, with an explicit note that this is a
cross-link to the closest available backend evidence (an "unable to get a
pair" symptom is operationally a roster/location mismatch), not a
source-confirmed pairing-specific SQL model. This keeps Stage 8 able to
surface *some* backend corroboration for pairing nodes without fabricating
schema detail.

---

## 4. Changes applied in this pass

| File | Change |
| --- | --- |
| `docs/ontology/catalogs/wcs_sql_catalog.json` | Filled 6 confirmed field/model gaps from Day 2 evidence (§1) |
| `docs/ontology/catalogs/capability_catalog.json` | Populated `support_contract` for `agv_active_errors`, `wcs_system_faults`, `tote_exchange_sequence`, `zone_pairing_state` (cross-linked, not fabricated) |
| `shared_pipeline_stages/stage_8/link_scoring.py` | Added `HOSPITAL_FLOW_NODE_PATTERN`, `SEQUENCE_BACKFILL_NODE_PATTERN`, `node_needs_hospital_flow_check()`, `node_needs_sequence_backfill_check()` |
| `shared_pipeline_stages/stage_8/normalize.py` | Added `runbook_is_wcs_sql_diagnostic_state` to the pairing-validation allowed set; added filter branches for the two new node categories |
| `docs/design_decisions/stage_8_playbook_finalization.md` | (Prior session) documented the backend-vs-UI evidence rule this fix implements |

No changes were made to Stage 5/6/7 prompts or extraction logic — this pass
is entirely ontology-content and Stage 8 linking/scoring, per the "don't
change playbook generation again yet" instruction that opened this task.

---

## 5. Retrieval implications for Stage 8 (how to use the richer ontology going forward)

- Stage 8 should continue to derive backend SQL/SSMS evidence from the
  node's `ontology_capabilities[].support_contract.diagnostic_surfaces`, not
  from re-scanning node text for surface keywords — that field is now
  populated for the four capabilities that were blocking 218550/223554, so no
  code change was needed there beyond the data fill.
- Prefer backend diagnosis for system-state nodes (AGV state, hospital flow,
  tote/task state, sequence/backfill, tipper state) — this is now
  structurally possible for all four of those categories, not just
  roster/mapping.
- Keep operator-required UI procedures as their own exception path — the
  hospital-flow branch still allows `runbook_is_hospital_ui_reference` through
  the filter; it does not force a SQL-only outcome.
- Preserve service-health/restart/gateway nodes as their own surface family —
  untouched by this change; `INFRA_DOMAIN_PATTERNS` and the Windows-Service/
  Ignition/OptiSweep predicates are unaffected.
- At most one RMS/UI check plus one SQL/SSMS check per in-scope diagnostic
  node, per the backend-vs-UI evidence rule already documented in
  `docs/design_decisions/stage_8_playbook_finalization.md#backend-vs-ui-evidence-rule-2026-08-07`
  — that rule's exceptions (operator-required UI, service-health,
  service-restart, gateway-health, Event Viewer/Windows Services/API nodes)
  are the same exception list left untouched by this change.

---

## 6. Remaining open gaps (not fixed this pass)

- **The training-slides PDF was never actually ingested by the pipeline** —
  it sits untracked in git at
  `operationalknowledgeingestion/data/input/videos/OptiSweep Training Slides [INTERNAL ONLY].pdf`
  (added one day before the Day 2 video run, but never referenced by any
  manifest or pipeline output). Day 2 ran through the video path instead
  (`training_video_day2/stage_1_source_bundle/training_video_ingestion_report.json`
  shows `input_video_path`/`input_vtt_path` + `"ocr_status": {"backend":
  "tesseract"}`), which OCRs lossy screen-recorded video frames rather than
  extracting the PDF's native text/tables. This repo already has a working
  PDF-native ingestion entrypoint
  (`operationalknowledgeingestion/scripts/stage1_extract_source_bundle.py`,
  used for `manual_optisweep_om_v3` and `active_agv_error_query_1`) that was
  simply never pointed at this file. The `wcs_sql_catalog.json` fills made in
  §1a are a one-time manual backfill from a chat-supplied PDF, not a durable
  fix — if Day 2 (or any future re-ingestion) reruns without this PDF
  properly ingested through the manual/PDF pipeline, this detail does not
  regenerate automatically and the catalog will silently drift stale again.
  **Recommended follow-up:** move/copy the PDF into `data/input/manuals/`
  (or a new `data/input/slides/`) and run
  `stage1_extract_source_bundle.py --source-pdf ".../OptiSweep Training Slides [INTERNAL ONLY].pdf" --source-type manual ...`
  through the same stage chain used for the OM manual, so future Stage 5/6
  runs can derive runbook candidates from the real column/enum text instead
  of OCR paraphrase.
- `RobotDatabaseModel`'s fields were resolved in the §1a follow-up pass once
  the full training-slides PDF was supplied — no longer an open gap.
- `zone_pairing_state` still has no dedicated SQL model (§5) — only a
  cross-link to roster/location fields. If a future incident or training
  source shows a real pairing-state table, replace the cross-link note with
  a proper `sql_model_links` entry.
- `OpcConfiguration` / `OpcTags` (OPCComms database) were also resolved in the
  §1a follow-up pass (full field lists now documented from the training-slides
  PDF, p.68).
- Several SorterSweeper-database models (`LocationModel`, `ToteModel`,
  `ItemModels`, `IgnitionLaneActivityModel`) have further live-query detail
  available in the training-slides PDF (pp.90-104) that was not transcribed
  into the catalog in this pass — the highest-value/most-referenced gaps
  (`RobotDatabaseModel`, `HospitalTagsModel`, Charging/Hospital/CellCode
  models, `EntityLogs`, `Audit`, `GeekAgv`) were prioritized instead. Revisit
  if a future node category needs deeper SorterSweeper field detail.
- This pass did not re-run the Stage 8 pipeline end-to-end against
  218550/223554 to confirm the linking outcome actually flips (that requires
  an LLM-driven Stage 8 run, which is a pipeline execution, not a docs/code
  change). The regression check below verifies the code path is reachable
  and non-breaking; it does not re-generate the playbooks.

---

## 7. Regression checks

1. **Existing suite, unchanged:** `pytest shared_pipeline_stages/tests/test_stage_8_5_relationship_linking.py
   shared_pipeline_stages/tests/test_stage_8_playbook_finalization.py
   shared_pipeline_stages/tests/test_stage_8_retrieval_eligibility.py` — 103
   passed, 0 failed, after all edits in this doc.
2. **JSON validity:** both `wcs_sql_catalog.json` and `capability_catalog.json`
   parse cleanly after edits (`python -c "import json; json.load(...)"`).
3. **Python syntax:** both edited modules
   (`shared_pipeline_stages/stage_8/link_scoring.py`,
   `shared_pipeline_stages/stage_8/normalize.py`) parse cleanly
   (`python -c "import ast; ast.parse(...)"`).
4. **New predicate behavior (manual trace, not yet a unit test):**
   `node_needs_hospital_flow_check` matches node text containing "hospital
   lane", "hospital induct", "tote induct", etc.; `node_needs_sequence_backfill_check`
   matches "backfill", "trailing agv", "shutdown queue sequence", etc. Suggest
   adding explicit unit tests for these two predicates plus a
   `filter_intent_compatible_matches` case asserting a `wcs_sql`-surfaced
   candidate survives filtering for a hospital-flow node — this was verified
   by function-level pattern testing during this pass but not committed as a
   new automated test, since the task scope was the ontology/linking deep
   dive rather than new test authorship. Recommend as the next small
   follow-up before the next Stage 8 four-case regeneration.
