# Ontology surface catalogs & Stage 6 mini-RAG

**Status:** accepted (pilot)  
**Date:** 2026-07-31  
**Schema:** taxonomy / catalogs `0.4`

## Problem

Stage 6 currently receives only constrained tag ID lists via `taxonomy_prompt_appendix()`. Flat IDs (`capability_tags`, `access_surface`, …) without **surface → activity → observable outcome → failure/capability** links produce runbook/playbook discrepancies:

- Same job tagged inconsistently across RMS vs SSMS vs API.
- Field/model names appear in training but are not machine-retrievable for enrichment.
- Day 2 DB depth cannot land in Stage 6 prompts as giant catalogs (token blow-up) and must not become Stage 5 `expects_*` IDs.

## Target model

1. **Constrained vocab** (stable IDs): capabilities, access_surfaces, audience_roles, failure_patterns, procedure_intents — still the only IDs for Stage 5 `expects_*` and Stage 6 tags.
2. **Rich capability cards** (`catalogs/capability_catalog.json`): each job links to primary/secondary **access surfaces**, **SQL databases/models**, **API checks**, **activities by role**, **observables** (healthy/degraded/escalate), **failure_patterns**, and **role_paths**. Taxonomy capability entries stay thin IDs; cards are the enrichment source.
3. **Per-access_surface reference catalogs** under `docs/ontology/catalogs/`: purpose, when_to_use / not_for, activities, observables, and (for `wcs_sql`) databases → models → **fields with meanings**.
4. **Cross-link tables**: `capability_failure_edges`, `surface_activities` (surface ↔ activity ↔ observables ↔ capability/failure hints).
5. **Stage 5 + Stage 6 enrichment** via **mini-RAG** (option B): Stage 5 gets 1–2 **surface/capability** snippets (~800 chars) when speech does not already name a live surface; Stage 6 gets 1–3 deeper **model → capability → activity → surface** snippets (~1200 chars) keyed by candidate tags + free text.

## Storage layout (machine-retrievable)

```text
docs/ontology/
  taxonomy/runbook_capability_taxonomy.json   # schema 0.4 — constrained IDs + edge tables + catalog_refs
    catalogs/
      catalog_index.json                        # layout + retrieval contract
      capability_catalog.json                   # rich capability cards (surfaces/DBs/APIs/activities)
      cross_links.json                          # capability↔failure, surface activities
      wcs_sql_catalog.json                      # deep SQL (primary)
    wcs_api_catalog.json
    rms_ui_catalog.json
    ignition_gateway_catalog.json
    stunnel_catalog.json
    event_viewer_catalog.json
    apidog_catalog.json
    aveva_hmi_catalog.json
    tipper_hmi_catalog.json
    hospital_hmi_catalog.json
  sources/                                    # reserved for Day1 / Day2 packs / OM manual excerpts
    day1/  day2/  om_manual/                  # provenance packs (future)
  support_roles_components_and_adjacency.md
```

**Provenance contract** on catalog rows:

| Field | Purpose |
| --- | --- |
| `evidence[]` | `{source, kind, snippet}` from OCR / transcript / SQL guide / slides |
| `source_refs` | Pack identifiers (`training_video_day2`, `active_agv_error_query_1`, …) |
| `needs_sme` | Meaning unknown — **do not invent** |
| `gaps` | Explicit holes for later Day1 / OM / Confluence |

Same store must later hold Day 1 training + OptiSweep OM manual as additional source packs without changing constrained IDs.

## SQL catalog depth (`wcs_sql`)

For each database: purpose, when_to_use, not_for, OptiSweep use flag, evidence.  
For each model/table: purpose, fields[{name, meaning, evidence, needs_sme}], enums, archive table, capability_hints, gaps.  
Primary evidence: Day 2 `stage_1` slide-segment **transcript** + `stage_2` **ocr_text** / nearby_text; slides PascalCase inventory; Active AGV SQL guide for `SystemActiveErrorModel` columns.

## Other surfaces

RMS, Ignition, Stunnel, Event Viewer, Apidog, AVEVA, tipper/hospital HMIs: **seed** activities + observables from adjacency §4–5 and Day1/Day2 OCR where present; mark gaps. Physical E-stop remains **operator**; RMS soft stop / PauseAGVs is L2/L3; AVEVA is site/operator primary.

## Stage 5 / Stage 6 retrieval (wired)

| Item | Choice |
| --- | --- |
| Helper | `shared_pipeline_stages/ontology_rag.py` — `ontology_snippets_for_stage5` / `ontology_snippets_for_stage6` |
| Keys | Inferred via `infer_ontology_query` from section/candidate text + artifact OCR/nearby; plus explicit Stage 6 tags |
| Packet field | `ontology_snippets` on Stage 5 discovery packets and Stage 6 finalization packets |
| Stage 5 budget | max 2 snippets × ~800 chars; prefer `surface:` / `capability:`; skip when section already surface-grounded (manuals); training always retrieves |
| Stage 6 budget | max 3 snippets × ~1200 chars; prefer `model:` then capability/activity/surface |
| Guardrails | Snippets propose surfaces/fields/observables only; source/OCR wins; `needs_sme` stays a gap; do not invent steps or UIs from snippets alone |
| Constrained IDs | Stage 6 taxonomy appendix remains mandatory |

**Why split budgets:** Training often names actions without naming the live surface in surrounding text — Stage 5 needs a thin surface/capability hint; Stage 6 needs deep model/observable grounding for finalize.

## Migration 0.3 → 0.4

| Stays constrained | Moves / grows as reference-only |
| --- | --- |
| capability / surface / role / failure / intent IDs | Full `wcs_sql` / `wcs_api` bodies → `docs/ontology/catalogs/` |
| Tag normalization via `taxonomy_id_sets()` | Field meanings, activities, evidence |
| | New: `capability_failure_edges`, `surface_activities`, `catalog_refs` |

Inline `wcs_sql_catalog` / `wcs_api_catalog` on the taxonomy file become **thin indexes** (`relocated_to`) for older consumers; do not expand constrained IDs casually.

## Related

- [`docs/ontology/taxonomy/README.md`](../ontology/taxonomy/README.md)
- [`docs/ontology/catalogs/catalog_index.json`](../ontology/catalogs/catalog_index.json)
- [`support_roles_components_and_adjacency.md`](../ontology/support_roles_components_and_adjacency.md)
- [`stage_8_capability_tags_and_linking_plan.md`](stage_8_capability_tags_and_linking_plan.md)
