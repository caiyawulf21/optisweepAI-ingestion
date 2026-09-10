# Plan: Catalog-grounded SQL runbooks for roster & hospital

Status: **deferred** (do not generate yet). Catalog grounding for `fleet_system_status` and gold-style `select_template`s landed first; Stage 5/backfill now prefer `agv_active_errors` for active-error language so `proc_query_active_agv_errors_from_the_wcs_database_v1` can link after rerun.

## Goal

Generate read-only WCS/SSMS diagnostic runbooks for capabilities that playbooks already advertise (`expects_surface` includes `wcs_sql`) but Stage 7 has **no** matching SQL procedure — especially `device_roster_state` and `hospital_diversion`. Follow the same step shape as the gold manual:

`operationalknowledgeingestion/data/output/active_agv_error_query_1/stage_6_finalized_runbooks/review_markdown/runbooks/candidate_manual_query_active_agv_errors.md`

Shared SSMS access steps (login → open DB → new query tab → paste → execute → review fields) + model-specific `SELECT` + field checklist.

## Why later

- Highest playbook SQL demand was `fleet_system_status` (catalog `sql_model_links` were empty) — filled first.
- Gold AGV-error SQL runbook exists but playbooks rarely emitted `agv_active_errors` — prompt/normalize/backfill fixed first so linking can be validated on rerun before inventing more SQL procs.
- Roster/hospital generation needs SME confirmation of catalog-derived column names / site DB FQNs (`Helix2x_*` wildcards on SorterSweeper).

## Priority targets (playbook demand snapshot)

| Capability | Playbook SQL-expecting nodes (prompt B) | Stage 7 SQL runbook | Catalog ready models |
| --- | --- | --- | --- |
| `device_roster_state` | 6 | none | `RobotLocationDatabaseModel`, `RobotDatabaseModel`, `SorterSideDatabaseModel`, `SortLocationsDatabaseModel` |
| `hospital_diversion` | 3 | none | `HospitalDatabaseModel`, `RobotDatabaseModel`, `LocationModel` (SorterSweeper) |

Skip `agv_physical_recovery` for SQL gen (physical floor / remove-AGV, not SSMS).

## Gold template contract

Reuse this skeleton; only the SELECT + field review change per model:

1. Log into the WCS primary server  
2. Open the WCS database  
3. Open a new query tab  
4. Paste the documented SQL  
5. Use the documented query text exactly (from `select_template.statement` when present)  
6. Execute the query  
7. Review the results area  
8. Check returned fields (from catalog `fields[].name` + meanings)

Tags on every generated runbook:

- `access_surface`: `["wcs_sql"]`  
- `capability_tags`: include the target capability (`device_roster_state` or `hospital_diversion`)  
- `audience_roles`: `L2_support` (SSMS)  
- `procedure_type`: `diagnostic`  
- Mark `validation_status`: `needs_sme_review` and `select_template.provenance`: `catalog_derived` until SME signs off  

## Suggested first procedures (when unblocking)

1. **Roster / locations** — `RobotLocationDatabaseModel` on `Helix2x_1Prod_Robotics` (8 detailed fields; RMS orange stations). Optional companion: `RobotDatabaseModel` live state.  
2. **Hospital routing** — `HospitalDatabaseModel` on robotics; optional SorterSweeper `LocationModel` where `Type`/zone/lane corroborate hospital diversion (confirm site FQN for `Helix2x_*_SorterSweeper`).

Add `select_template` on those models in `docs/ontology/catalogs/wcs_sql_catalog.json` before or during gen (mirror `SystemActiveErrorModel` / `SystemDatabaseModel`).

## Generation approach options

1. **Ontology-seeded Stage 5/6 operational pass** — packet with `allowed_access_surfaces` + ontology snippets including `select_template`; LLM finalizes steps under eligibility (no invented UIs; SQL only from template/catalog).  
2. **Deterministic scaffold script** — emit Stage 6 JSON from catalog `select_template` + shared SSMS step boilerplate, then SME review / Stage 6.5→7→8. Prefer this if we want zero SQL invention risk.  

Either path must land in the shared Stage 6.5 pool with tags so Stage 8 multi-link can pair RMS + SQL on the same capability.

## Preconditions before starting

- [ ] Rerun incident Stage 5→6 + shared 6.5→8 and confirm gold AGV SQL proc links when nodes expect `agv_active_errors` + `wcs_sql`  
- [ ] SME-confirm roster/hospital column spellings and SorterSweeper site DB name  
- [ ] Add `select_template` on chosen roster/hospital models  
- [ ] Decide scaffold script vs LLM Stage 6  

## Out of scope (for this plan)

- Filling empty `sql_model_links` for `zone_pairing_state` / `zone_config_state` / `wcs_service_health` (separate catalog work)  
- Stage 8 surface-preferring companion algorithm changes (optional linker improvement)  
- Mutating SQL / corrective actions  

## References

- Gold runbook MD (above)  
- `docs/ontology/catalogs/capability_catalog.json` — `device_roster_state`, `hospital_diversion` cards  
- `docs/ontology/catalogs/wcs_sql_catalog.json` — models + `select_template`  
- `docs/design_decisions/stage_8_capability_tags_and_linking_plan.md` — capability × surface multi-link  
