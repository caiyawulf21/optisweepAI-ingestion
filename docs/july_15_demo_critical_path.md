# July 15 Demo Critical Path

**Demo:** Wednesday July 15, 2026 — 9:30 AM  
**Status:** Internal planning (not for SME distribution)  
**Test plan:** [optisweep_ai_demo_test_plan.md](optisweep_ai_demo_test_plan.md)

---

## Priority order

```text
1. Per-source Stage 8 relationship linking (operational + incidence)     [done — Jul 8]
2. Shared Stages 6.5 → 7 → 8 (playbooks) → 8.5 (corpus links)           [6.5–8 done; 8.5 run next]
3. Stage 9 validation                                                    [implemented — run next]
4. Stage 10 embeddings                                                 [implemented — after Stage 9]
5. Stage 11 Cosmos + manifest                                          [implemented — after Stage 10]
6. App up (wired to Cosmos)
7. Demo dry-run
8. Demo (Jul 15)
9. Ingest new cases → 1–8 → 6.5–8.5 → Stage 9 → 10 → 11 → refresh app
```

**Blocker:** The app cannot retrieve until embeddings are published to Cosmos. Pipeline finish comes before any app work.

---

## Pipeline architecture (three subgraphs)

Stage numbers are **not** interchangeable across subgraphs. See [shared_pipeline_stages/README.md](../shared_pipeline_stages/README.md).

```text
OPERATIONAL SOURCE (per manual / training video)
  Stages 1–8 implemented
  Stage 8: artifact ↔ operational context ↔ source runbook links
  Handoff: stage_6_finalized_runbooks/ + stage_8_relationship_linking/

INCIDENCE SOURCE (per case)
  Stages 1–6 + 2.5 + Stage 8 implemented
  Stage 8: artifact ↔ incident record ↔ timeline ↔ source runbook links
  Handoff: stage_6_finalized_runbooks/ + stage_5 playbook candidates + stage_8_relationship_linking/

SHARED PUBLISH
  Stage 6.5  runbook pool + similarity           [implemented]
  Stage 7    cross-source runbook merge          [implemented]
  Stage 8    playbook finalization + node links  [implemented]
  Stage 8.5  corpus relationship graph           [implemented]
  Stage 9    corpus validation                   [implemented — publish gate]
  Stage 10   vector embedding generation         [implemented]
  Stage 11   Cosmos DB publish + manifest        [implemented]
```

**Naming clarity:** Operational/incidence **Stage 8** = per-source relationship linking. **Shared Stage 8** = playbook finalization. **Shared Stage 8.5** = aggregate per-source graphs + playbook→runbook edges into one corpus `relationship_links.json`.

---

## Corpus prep status (Jul 8 EOD)

| Stage | Scope | Status | Demo corpus notes |
|-------|-------|--------|-------------------|
| Op Stage 8 | Per operational source | **Done** | `manual_optisweep_om_v3`: **15,240 links** (127 artifacts, 276 context, 225 runbooks, 0 unresolved refs) |
| Inc Stage 8 | Per incident case | **Done** | `case_228086`: **122 links** (1 runbook); `case_228723`: **52 links** (artifact/incident/timeline only — 0 finalized runbooks yet) |
| Shared 6.5–7 | Cross-source runbooks | Done | ~399 canonical runbooks after merge |
| Shared 8 | Playbook→runbook (A + B) | Done | 228086 + 228723 playbooks |
| Shared 8.5 | Corpus link graph | Script ready | **Run next** — aggregates per-source graphs + playbook links; remaps source procedure IDs → canonical |
| Shared 9 | Corpus validation | Implemented | Publish gate — fails on unresolved playbook links or invalid 8.5 targets |
| Shared 10 | Embeddings | Implemented | Canonical runbooks (Stage 7) + playbook cards (Stage 8 A/B) |
| Shared 11 | Cosmos publish | Implemented | Local `publish_bundle/` + manifest; optional `--publish` when `COSMOS_*` env set |

**Before Phase 1 publish gate:** run Shared 8.5, then Stage 9 → 10 → 11 in order.

### What Stage 8 / 8.5 delivered (Jul 8)

**Per-source Stage 8** (operational + incidence) writes deterministic relationship edges without changing retrieval text:

| Source | Link types | App/runtime value |
|--------|------------|-------------------|
| Operational | `artifact_context`, `artifact_runbook`, `context_runbook`, candidate links | Surface screenshots and context for a retrieved procedure |
| Incidence | `artifact_incident`, `artifact_timeline`, `incident_timeline`, `*_runbook` | Tie evidence and timeline events to incident playbooks and procedures |

**Shared Stage 8.5** merges per-source `relationship_links.json` plus Shared Stage 8 `playbook_runbook_links.json` into one corpus graph with:

- `link_scope: per_source` on source edges (with `source_root`, `source_id`, `source_type`)
- Canonical procedure ID remap via Stage 7 `candidate_to_procedure_mapping.json`
- `playbook_runbook` edges from Shared Stage 8 for post-retrieval orchestration

**228723 caveat:** Stage 8 ran but Stage 6 produced 0 finalized runbooks for that case. Prompt 2 playbook routing still works via Shared Stage 8 links to **canonical** runbooks; per-source artifact→runbook edges for 228723 will be sparse until Stage 6 is re-run.

---

## Phase 1 — Pipeline finish (Jul 8–11)

**Goal:** Publishable corpus the app can retrieve against.

| # | Task | Done when |
|---|------|-----------|
| 1.0 | **Per-source Stage 8** on all operational sources + ingested cases | **Done** — `manual_optisweep_om_v3`, `case_228086`, `case_228723` |
| 1.0b | **Shared 8.5** corpus relationship linking | `stage_8_5_relationship_linking/relationship_links.json` |
| 1.1 | **Stage 9 validation** on Stage 7 runbooks + Shared 8 playbooks + Stage 8.5 graph | `validation_report.json` passes (exit 0) |
| 1.2 | **Stage 10 embeddings** — canonical runbooks + playbook entry-symptom cards | `embedding_records.json` for every retrievable document |
| 1.3 | **Stage 11 Cosmos publish** — runbooks, playbooks, embeddings, relationship graph | `publish_bundle/` + optional Cosmos upload |
| 1.4 | **Stage 11 publish manifest** — version ID, record counts, embedding model, checksums, link counts | `publish_manifest.json` |
| 1.5 | **Stage 11 retrieval smoke test** — symptom-like text → relevant runbook/playbook | Top-k in `cosmos_publish_report.json` looks right for prompts 1–2 |

Stage 9 must pass before Stage 10–11 — no point vectorizing broken playbook links.

**Out of scope for now:** Azure AI Search, LangGraph orchestration, new case ingest.

### Dependency chain

```text
Per-source Stage 8 (all sources)
  → Shared 6.5 → 7 → 8 (playbooks)
    → Shared 8.5 (corpus relationship_links.json)
      → Stage 9 validate
        → Stage 10 embed
          → Stage 11 publish to Cosmos + manifest
            → app retrieval works
```

### Effects of Stage 8 / 8.5 on embed and Cosmos

| Layer | Changed by 8 / 8.5? | What happens |
|-------|---------------------|--------------|
| **Stage 10 vectors** | No | Embeddings still built from `retrieval_cards.json` (runbooks) and `playbook_retrieval_cards.json` (playbooks). Link fields do not alter embedded text. |
| **Stage 11 runbook docs** | Indirectly | Published runbooks are Shared Stage 7 canonical records. 8.5 remaps per-source procedure IDs → canonical IDs in the graph, not in runbook JSON. |
| **Stage 11 playbook docs** | No change | Shared Stage 8 playbooks unchanged; 8.5 adds `playbook_runbook` edges from `playbook_runbook_links.json`. |
| **Stage 11 companion graph** | **Yes — new** | Publish `stage_8_5_relationship_linking/relationship_links.json` for citation, image resolution, and post-retrieval navigation. |
| **Stage 9 validation** | **Yes — expanded** | Validate Shared 8 playbook→runbook links **and** 8.5 graph completeness (missing source roots, remap coverage, orphan playbook nodes). |
| **App Phase 2** | **Yes — enriched** | After vector retrieval: follow `playbook_runbook` edges to load procedures; follow `artifact_runbook` / `context_runbook` edges to surface screenshots. |

Operational context and source artifacts are embedded in Stage 10 and published in Stage 11 as `doc_type=embedding` (hybrid search) plus `doc_type=rag_record` (metadata lookup) in `COSMOS_CONTAINER_OPERATIONAL_CONTEXT` and `COSMOS_CONTAINER_SOURCE_ARTIFACTS`.

### Stage 8.5 → 9 → 10 → 11 runbook (Jul 9–10)

Run from repo root after Shared 6.5–8 outputs exist.

**Shared 8.5 — corpus relationship graph**

```powershell
python shared_pipeline_stages/scripts/stage8_5_link_relationships.py `
  --source-root operationalknowledgeingestion/data/output/manual_optisweep_om_v3 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228086 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228723 `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --stage8-dir shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  --output-dir shared_pipeline_stages/data/output/shared
```

**Stage 9 — publish gate (must exit 0 before embed/publish)**

Validates: Stage 7 canonical runbook schema; Shared Stage 8 playbook graph integrity; zero unresolved node links; `playbook_runbook_links.json` targets exist in canonical catalog; Stage 8.5 link targets and expected source roots.

```powershell
python shared_pipeline_stages/scripts/stage9_validate_corpus.py `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --stage8-dir shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  --stage85-dir shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking `
  --source-root operationalknowledgeingestion/data/output/manual_optisweep_om_v3 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228086 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228723 `
  --output-dir shared_pipeline_stages/data/output/shared
```

Outputs: `stage_9_validation/validation_report.json`, `extraction_report.json`

**Stage 10 — full-corpus embeddings**

| Record type | Source | Embedded from |
|-------------|--------|---------------|
| `canonical_runbook` | Shared Stage 7 | Rebuilt retrieval card text per canonical runbook |
| `playbook` | Shared Stage 8 (A + B) | `playbook_retrieval_cards.json` entry-symptom text |
| `operational_context` | Per-source Stage 4 | `retrieval_text` / title+summary |
| `source_artifact` | Per-source Stage 2/3 | `retrieval_text` / title+summary |

```powershell
python shared_pipeline_stages/scripts/stage10_generate_embeddings.py `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --stage8-dir shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  --source-root operationalknowledgeingestion/data/output/manual_optisweep_om_v3 `
  --source-root operationalknowledgeingestion/data/output/training_video_day1 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228086 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228723 `
  --output-dir shared_pipeline_stages/data/output/shared
```

Use `--use-mock-embedder` for structural tests only. Production demo uses Azure OpenAI embeddings (`AZURE_OPENAI_*`, `AZURE_EMBEDDINGS_DEPLOYMENT`).

Outputs: `stage_10_embeddings/embedding_records.json`, `embedding_generation_report.json`

**Stage 11 — publish bundle + manifest (+ optional Cosmos upload)**

Writes versioned `publish_bundle/` (runbooks, playbooks, embeddings, relationship graph) and `publish_manifest.json` with checksums and link counts. Retrieval smoke test runs against playbook embeddings.

```powershell
python shared_pipeline_stages/scripts/stage11_publish_cosmos.py `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --stage8-dir shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  --stage10-dir shared_pipeline_stages/data/output/shared/stage_10_embeddings `
  --stage85-dir shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking `
  --output-dir shared_pipeline_stages/data/output/shared
```

Add `--publish` when `COSMOS_ENDPOINT`, `COSMOS_KEY`, `COSMOS_DATABASE`, `COSMOS_CONTAINER` are configured. Without `--publish`, the local bundle is the app handoff artifact.

Outputs: `stage_11_cosmos_publish/publish_manifest.json`, `cosmos_publish_report.json`, `publish_bundle/*.json`

---

## Phase 2 — App up (Jul 11–13)

**Goal:** App retrieves from Cosmos embeddings, not raw filesystem.

| # | Task | Done when |
|---|------|-----------|
| 2.1 | **Agent brief** — app repo + Cosmos connection + publish manifest schema | Spec written |
| 2.2 | Wire app retrieval to **Cosmos vector search** (playbooks first, then runbooks) | Symptom query returns candidates |
| 2.3 | Load playbook orchestration from published playbook records | 228086 + 228723 routable |
| 2.4 | Surface linked runbook steps from published runbook records | Procedure steps render |
| 2.5 | A/B toggle — filter by `prompt_a` vs `prompt_b` playbook set | Toggle works |
| 2.6 | Image assets — resolve from published asset paths, 8.5 `artifact_runbook` links, or `sme_review_runbooks/**/assets/` | Screenshots show |
| 2.7 | **End-to-end smoke** — prompts 1–2 through full retrieve → route → procedure flow | App usable in browser |

### Agent handoff minimum

- Cosmos endpoint, container(s), and query pattern for vector retrieval
- `publish_manifest.json` — version, record IDs, schema, link counts
- Published `relationship_links.json` (Stage 8.5) — playbook→runbook, artifact→runbook, context→runbook edges with canonical procedure IDs
- `sme_review_runbooks/` — reference for MD/HTML structure and image paths if not stored in Cosmos
- A/B toggle = metadata filter on playbook records (`extraction_mode`), not a directory swap

App code lives in a separate directory; reconfiguration is handled by an AI agent against `sme_review_runbooks/` and the published Cosmos corpus.

---

## Phase 3 — Demo prep (Jul 13–14)

| # | Task | By |
|---|------|-----|
| 3.1 | Scoring sheet from test plan rubric | Fri Jul 11 |
| 3.2 | Dry-run **prompts 1–2** (A and B) | Tue Jul 14 |
| 3.3 | Dry-run **prompts 3–5** — runbook retrieval only; capture gap notes | Tue Jul 14 |
| 3.4 | Email team: app link + [test plan](optisweep_ai_demo_test_plan.md) | Mon Jul 14 |
| 3.5 | Run-of-show + driver/scorer roles | Tue Jul 14 |
| 3.6 | Morning check Jul 15, 9:00 AM | Wed Jul 15 |

### Jul 15 expectations

| Prompt | Expectation |
|--------|-------------|
| 1 — AGVs stopped | Full playbook path (228086 + related cases after ingest) |
| 2 — Zone can't pair | Full playbook path (228723) |
| 3 — Bag-out stuck | Best-effort runbook retrieval; incident playbooks after ingest |
| 4 — Tote in RMS | Best-effort runbook retrieval; incident playbooks after ingest |
| 5 — Tipper heartbeat | Best-effort runbook retrieval; incident playbooks after ingest |

Set honest expectations in the demo intro: prompts 1–2 are the primary test; prompts 3–5 improve after case ingest (Round 2, week of Jul 20).

### Demo day checklist

- [ ] App up; Cosmos retrieval working
- [ ] A/B toggle works
- [ ] Prompts 1–2 dry-run successful in last 24h
- [ ] Scoring sheet ready
- [ ] Test plan link shared
- [ ] Driver + scorer assigned
- [ ] Fallback: HTML playbooks in `sme_review_runbooks/stage_8_playbooks/` if app fails

---

## Phase 4 — Case ingest (after app is stable)

**Goal:** Full coverage for all 5 prompts. Run after Phase 1–3, or immediately post-demo.

PDFs are ready. No SME review gate on source documents — ingest straight through the pipeline.

| # | Task | Done when |
|---|------|-----------|
| 4.1 | Stage all PDFs in `incidenceknowledgeingestion/data/input/incidents/` | Inventory complete |
| 4.2 | Batch **Stages 1–6** per case | Output per `case_<id>/` |
| 4.3 | **Stage 5** playbook discovery (A + B) per case | Playbook candidates per case |
| 4.4 | **Stage 8** per-source relationship linking per case | `relationship_links.json` per case |
| 4.5 | **Re-run shared 6.5 → 7 → 8 → 8.5** with expanded incident pool | New playbooks + updated corpus graph |
| 4.6 | **Stage 9** on expanded corpus | Clean validation |
| 4.7 | **Re-run Stage 10–11** (new embeddings + Cosmos version in manifest) | Cosmos updated |
| 4.8 | **Export to `sme_review_runbooks/`** | Review tree current |
| 4.9 | **Refresh app** — point at new publish version | Prompts 3–5 routable |
| 4.10 | Dry-run all 5 prompts | Round 2 ready (Jul 20) |

### Case inventory

| Prompt | Cases | Status (Jul 8) |
|--------|-------|----------------|
| 1 — AGVs stopped | 228086, 229488, (+ others) | 228086 ingested + Stage 8 done; PDFs ready for rest |
| 2 — Zone can't pair | 228723, (+ others) | 228723 ingested + Stage 8 done (52 links; re-run Stage 6 for runbook edges) |
| 3 — Bag-out stuck | 229589, 218550, 219684 | PDFs ready |
| 4 — Tote in RMS | 220884, 230250 | PDFs ready |
| 5 — Tipper heartbeat | 229374, 229716, 229777 | PDFs ready |

Cases can be ingested in parallel where Azure OpenAI quota allows.

### Post-ingest dependency chain

```text
Ingest Stages 1–6 + Stage 8 (all cases)
  → Stage 5 playbooks
    → shared 6.5 → 7 → 8 → 8.5
      → Stage 9 validate
        → Stage 10 re-embed
          → Stage 11 re-publish Cosmos (new version)
            → refresh app
              → Round 2 dry-run
```

---

## Calendar

| Day | Focus |
|-----|--------|
| **Wed Jul 8** | Per-source Stage 8 complete on demo sources; Shared 9–11 implemented; run Shared 8.5 |
| **Thu Jul 9** | Run 8.5 → Stage 9 validate → Stage 10 embeddings (Azure) |
| **Fri Jul 10** | Stage 11 publish bundle + manifest; retrieval smoke test; optional Cosmos upload |
| **Sat Jul 11** | App agent brief; wire app to Cosmos |
| **Sun Jul 12** | App: router, A/B toggle, runbooks, images, 8.5 link navigation — prompts 1–2 E2E |
| **Mon Jul 13** | App polish; email team; scoring sheet |
| **Tue Jul 14** | Dry-run all 5 prompts |
| **Wed Jul 15 9:30** | **Demo** |
| **Post-demo** | Batch case ingest → 1–8 → 6.5–8.5 → Stage 9–11 → app refresh |
| **Week of Jul 20** | Round 2 with full prompt coverage |

---

## Milestones: before vs after demo

| Milestone | Before Jul 15 | After ingest |
|-----------|---------------|--------------|
| Per-source Stage 8 | Manual + 228086 + 228723 done | All cases linked |
| Shared 8.5 | Run Jul 9 on demo sources | Expanded graph |
| Stage 9 | Implemented; run after 8.5 | Re-validated with new cases |
| Stage 10 | Implemented; run after Stage 9 pass | Regenerated |
| Stage 11 | Implemented; local bundle + optional Cosmos | Expanded version |
| App | Retrieving from Cosmos + link graph | Refreshed to new publish version |
| Playbooks | 2 cases (228086, 228723) | All cases per prompt |
| Prompts 1–2 | Production-ready | Stronger with more cases |
| Prompts 3–5 | Runbook retrieval only | Full incident playbooks |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Missing per-source Stage 8 before 8.5 | 8.5 skips source roots without links (warning only); run Stage 8 on every source before 8.5 |
| 8.5 canonical remap gaps | Stage 9 flags unmapped source procedure IDs; review `candidate_to_procedure_mapping.json` |
| Stage 9 finds playbook link gaps | Fix in Shared 8 re-run before Stage 10–11; do not skip validation |
| Stage 11 not ready by Jul 11 | App work blocked — prioritize Phase 1 |
| App ignores 8.5 graph | Prompts 1–2 still work on vectors alone; images/citations weaker without link traversal |
| App agent slips | Minimum viable: prompts 1–2 E2E before demo |
| Ingest last = weak 3–5 on Jul 15 | Set expectations; Round 2 is the real 3–5 test |
| Re-ingest breaks published corpus | Version Cosmos records; keep demo version until smoke-tested |

---

## Post-demo pipeline (not on critical path)

| Task | Target |
|------|--------|
| LangGraph orchestration (operational + incidence → shared → publish) | Late July |
| Harden shared Stages 9–11 automation | Jul 20 Round 2 (stages implemented Jul 8) |
| Embed operational context / artifacts as separate record types (Stage 10 v2) | Post-demo |
| Update `development_status.md` | After ingest batch |
| Handoff to Ravi Mareddy & team | Late July |

---

## Related resources

- [Demo test plan](optisweep_ai_demo_test_plan.md)
- [Shared pipeline stages](../shared_pipeline_stages/README.md)
- [Stage 8 link scoring design](design_decisions/stage_8_link_scoring_and_confidence.md)
- [SME review runbooks](../sme_review_runbooks/)
- [Stage 8 playbooks — Prompt A](../sme_review_runbooks/stage_8_playbooks/prompt_a_one_per_incident/)
- [Stage 8 playbooks — Prompt B](../sme_review_runbooks/stage_8_playbooks/prompt_b_multi_flow/)
- [Azure review design](design_decisions/runbook_candidate_pool_and_azure_review_design.md)

