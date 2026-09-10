# Shared Pipeline Stages

Shared Stage 8 keeps canonical playbooks as diagnostic workflows. Each node
retains its Stage 5 reasoning, evidence and outcome fields, while
`evidence_collection_procedures` contains only compact references
(`procedure_id`, title, purpose, and required role). Full runbook steps are
resolved from the catalog by review/runtime surfaces and are not embedded in
the canonical playbook artifact.

Diagnostic nodes additionally receive an action plan authored by the LLM
(or by the explicit non-LLM fallback). It identifies
the executing role and preferred evidence surface, lists the evidence or
ontology fields to inspect, separates evidence-retrieval success from health
interpretation, and limits procedure resolution to one primary procedure plus
one distinct corroboration procedure. Missing ontology mappings become
conceptual guidance and SME/catalog gaps; executable generated SQL is
SELECT-only.

When Stage 8 uses the LLM, its diagnostic action-plan fields are preserved
verbatim and validation reports missing or malformed fields for SME review.
Deterministic action synthesis is available only through the explicit
`deterministic_action_fallback` test/non-LLM configuration.

Stage 8 also enforces output quality at finalization. The workflow graph must
have valid targets or terminal outcomes, reachable recovery and validation
paths, failure/inconclusive escalation paths, no orphaned nodes, and no
accidental cycles; violations stop generation with a structural validation
error. Runbook attachment is exact-fit across node type, trigger, evidence or
action, role, surface, safety, and expected outcome. Diagnostic plans use at
most three ontology entities and eight surface-validated fields, while
procedure, validation, and escalation nodes render their own support-facing
schemas. Canonical runbook execution results remain separate from the node's
healthy/unhealthy interpretation. For system/HMI checks, Stage 8 also emits
bounded, ontology-backed read-only WCS SQL database/model/field suggestions as
corroboration when the primary surface is not SQL; exact-fit, forbidden-family,
and safety gates remain unchanged.
Ontology resolution happens before optional runbook retrieval, so diagnostic
guidance remains actionable even when no reusable procedure is linked. Review
Markdown and HTML show the selected database, models, fields, relationships,
and freshness evidence, or a concise escalation boundary; catalog gaps remain
internal JSON metadata.

Ontology capability cards are the source of truth for Stage 5 and Stage 8
contracts. They define allowed diagnostic/control surfaces, forbidden
capabilities, prerequisites, WCS availability exceptions, and UI-to-WCS
read mappings. Remote diagnosis prefers read-only `wcs_sql`/SSMS whenever a
WCS-backed UI exists; VPN failure is the exception, and service-down cases
also use Ignition, host/service, API, and SQL evidence. Stage 8 records each
retrieval candidate's raw scores, contract metadata, exact-fit gaps, and
eligibility decision before semantic reranking. Service recovery cannot attach
without an explicit prior health diagnosis, and AGV/tote correction remains a
separate workflow.

`shared_pipeline_stages/` holds cross-pipeline stage code and shared local outputs. Both ingestion areas converge here after source-specific extraction.

## Pipeline Architecture

Two source-specific subgraphs feed one shared publish subgraph. Stage numbers are **not** interchangeable across subgraphs.

```text
INCIDENCE SOURCE (per case) — ends at Stage 8
  Stages 1–6 implemented (+ Stage 2.5)
  Stage 8 per-source relationship linking implemented
  Outputs: stage_6_finalized_runbooks/finalized_runbooks/*.json
           stage_8_relationship_linking/relationship_links.json
           stage_5 playbook candidates (Prompt A/B)

OPERATIONAL SOURCE (per manual / training video)
  Stages 1–8 implemented
  Outputs: stage_6_finalized_runbooks/finalized_runbooks/*.json
           stage_8_relationship_linking/relationship_links.json

        ↓  handoff at Stage 8 (runbooks + per-source relationship_links.json)

SHARED PUBLISH
  Stage 6.5  runbook pool + similarity        [implemented]
  Stage 7    cross-source runbook merge       [implemented]
  Stage 8    playbook finalization + linking  [implemented]
  Stage 8.5  corpus relationship linking     [implemented]
  Stage 9    corpus validation                [implemented — publish gate]
  Stage 10   vector embedding generation      [implemented]
  Stage 11   Cumulative Cosmos publish       [implemented — merge + gate + smoke + gate_phrase_table]
```

**Architecture note:** Stage 11 is cumulative (prior ∪ new). Thin `case:` publishes into a new partition are blocked. Operator-language enrichment runs in Stage 8 and again on the cumulative path. See `docs/architecture.md`.

**Not shared / not on the demo critical path**

- Operational relationship linking (`operationalknowledgeingestion/stage8_relationship_linking.py`) and incident relationship linking (`incidenceknowledgeingestion/stage8_relationship_linking.py`) run per source before shared publish. **Shared Stage 8.5** aggregates those graphs plus playbook links. Playbook→runbook linking at the node level remains **Shared Stage 8**.
- Operational source-record validation (`stage9_validation_repair.py`) — helper utilities for artifacts/contexts/candidates during extraction only. The publish gate is **Shared Stage 9** on Stage 7+8 outputs.
- Stage 6.5 and Stage 8 use embeddings internally for similarity and retrieval during linking. **Shared Stage 10** is the full-corpus `EmbeddingRecord` export for Cosmos retrieval.

```text
shared_pipeline_stages/
  data/
    input/      optional shared inputs
    output/     shared stage outputs (Stage 6.5+)
    processed/  optional intermediate files
    review/     reviewer-facing samples and validation outputs
  stage_6_5/    runbook pool, similarity, merge prep
  stage_7/      cross-source merge and canonical catalog
  stage_8/      playbook finalization and runbook linking
  stage_8_5/    corpus relationship linking
  stage_9/      corpus validation (publish gate)
  stage_10/     full-corpus embedding generation
  stage_11/     Cosmos publish bundle + manifest
  stage_prompts.py
  scripts/
    stage6_5_build_runbook_pool.py
    stage7_merge_runbooks.py
    stage8_finalize_playbooks.py
    stage8_5_link_relationships.py
    stage9_validate_corpus.py
    stage10_generate_embeddings.py
    stage11_publish_cosmos.py
    stage6_5_tune_weights.py
    analyze_stage6_5_results.py
    analyze_stage6_5_nearmisses.py
    sync_sme_review_runbooks.py
    update_readme.py
  tests/
```

Source-specific outputs remain in each ingestion area:

```text
operationalknowledgeingestion/data/output/<source_id>/
incidenceknowledgeingestion/data/output/incidents/<case_id>/
```

Shared outputs are written under:

```text
shared_pipeline_stages/data/output/shared/
```

## Shared Stage 6.5: Runbook Pool Generation

Stage 6.5 reads Stage 6 finalized runbooks from one or more source output roots, embeds retrieval cards, scores cross-source similarity, and prepares merge clusters for Stage 7.

**When to rebuild:** after any source Stage 6 regen that should appear in the shared catalog (Day1/Day2 training, OM, AGV guide, incident Stage 6). Shared Stage 7 then merges; Shared Stage 8 re-links playbooks against the new catalog. **Always rebuilt:** orchestration shared publish forces Stage 6.5 whenever 7+ is requested; `stage8_finalize_playbooks.py` defaults to `--rebuild-pool` (6.5+7 before link). Day1/Day2 OpenAI-only regen scripts also refresh shared (`REGEN_REFRESH_SHARED=1`, default stages `6.5,7,8` via `scripts/shared_after_source_regen.py`).

Each retrieval card copies Stage 6 taxonomy tags (`capability_tags`, `access_surface`, `audience_roles`, `failure_pattern_tags`) into `retrieval_cards.json` and into `retrieval_text` used for embedding / similarity. Re-run Stage 6.5 after Stage 6 tag backfill so existing pool cards pick up tags.

Ontology catalogs (`docs/ontology/catalogs/`, taxonomy schema 0.4) hold
surface/SQL reference detail for operational and incident **runbook** Stage 5/6
mini-RAG. Incident playbook Stage 5 is source-grounded and does not receive
ontology surface suggestions; Stage 8 applies the catalog when selecting the
current diagnostic surface. Helper: `ontology_rag.py` (optional prompt
snippets; constrained IDs still from `runbook_tags.taxonomy_prompt_appendix()`).
`wcs_sql_catalog` models may carry `select_template` (gold or
catalog-derived SELECT text) for future SQL runbook scaffolding;
`fleet_system_status` now has `sql_model_links`. Deferred roster/hospital SQL
gen: `docs/plan_catalog_sql_runbooks_roster_hospital.md`.

**Inputs**

Each `--source-root` must contain:

```text
stage_6_finalized_runbooks/finalized_runbooks/*.json
```

**Run**

From the repo root:

```powershell
python shared_pipeline_stages/scripts/stage6_5_build_runbook_pool.py `
  --source-root operationalknowledgeingestion/data/output/manual_optisweep_om_v3 `
  --source-root operationalknowledgeingestion/data/output/training_video_day1 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228086 `
  --output-dir shared_pipeline_stages/data/output/shared
```

Use `--skip-embed` or `--use-mock-embedder` for structural tests without Azure OpenAI embeddings.

**Outputs**

```text
shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool/
  runbook_pool.json
  retrieval_cards.json
  runbook_retrieval_index.json
  merge_clusters.json
  pass_through_runbooks.json
  runbook_similarity.json
  runbook_pool_report.json
```

## How To Review Shared Stage 6.5 Outputs

Review in this order:

1. **`runbook_pool_report.json`**
   - Confirm `input_runbook_count` matches the number of finalized runbooks you expect from all source roots.
   - Check `merge_cluster_count` and `pass_through_count` are reasonable.
   - Inspect `top_cross_source_pairs` for obvious false positives or missing expected matches.
   - Review score distributions (`cosine_distribution`, `combined_distribution`) before changing thresholds.

2. **`merge_clusters.json`**
   - Open each cluster and confirm the grouped runbooks describe the same procedure across sources.
   - Check `source_types` for expected cross-source coverage (for example manual + training video + incident).
   - Read `evidence_notes`, `pairwise_matches`, and `metadata_warnings`.
   - Treat `merge_hint: needs_review` and `requires_stage_7_llm: true` as SME review gates, not auto-merge approval.
   - Flag clusters with `opposing_actions_detected: true` immediately.

3. **`pass_through_runbooks.json`**
   - Confirm runbooks marked `pass_through_reason: no_match` are genuinely unique procedures.
   - Spot-check a sample against `runbook_pool.json` to ensure nothing was incorrectly excluded from clustering.

4. **`runbook_pool.json` and `retrieval_cards.json`**
   - Verify titles, summaries, procedure types, and source lineage on indexed runbooks.
   - Confirm retrieval text is usable for search and Stage 7 merge prep.

5. **`runbook_similarity.json`**
   - Use this for deeper inspection when a cluster looks suspicious.
   - Compare high-scoring pairs manually before changing `--min-merge-score` or `--high-confidence-score`.

6. **Source finalized runbooks**
   - When a cluster looks wrong, open the underlying files in each source root:
     `stage_6_finalized_runbooks/finalized_runbooks/<procedure_id>.json`
   - Compare steps, source refs, and validation status before approving a merge.

## Review Rules

- Default validation status remains `needs_sme_review` until a reviewer approves.
- Do not treat similarity scores as proof that two runbooks should merge.
- Do not publish to Cosmos DB or vector search from Stage 6.5 outputs directly.
- Stage 6.5 prepares merge candidates; Shared Stage 7 performs selective LLM merge on approved clusters.

## Shared Stage 7: Cross-Source Runbook Merge

Stage 7 reads Stage 6.5 merge clusters and pass-through lists, promotes pass-through finalized runbooks without LLM cost, and runs LLM merge calls only on merge sub-clusters (auto-split to max 3 runbooks per call).

**Inputs**

```text
shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool/
  merge_clusters.json
  pass_through_runbooks.json
  runbook_pool.json
```

**Run (dry-run, pass-through only)**

```powershell
python shared_pipeline_stages/scripts/stage7_merge_runbooks.py `
  --pool-dir shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool `
  --output-dir shared_pipeline_stages/data/output/shared
```

**Run (with LLM merge calls)**

```powershell
python shared_pipeline_stages/scripts/stage7_merge_runbooks.py `
  --pool-dir shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool `
  --output-dir shared_pipeline_stages/data/output/shared `
  --llm
```

**Outputs**

```text
shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/
  canonical_runbooks.json
  candidate_to_procedure_mapping.json
  runbook_merge_report.json
  merge_packets.json
  review_markdown/merge_comparison_review.md
  review_markdown/runbooks/*.md
  review_markdown/assets/*
```

## Shared Stage 8: Playbook Finalization

Stage 8 links incident Stage 5 playbook candidates to canonical runbooks from Stage 7, emits dual Prompt A/B finalized packets, and writes Markdown + HTML review outputs. **`--llm` is required**; deterministic (no-LLM) finalization is not supported.

Linking guards: recovery-prep runbooks are hard-rejected for check-only nodes (unless the node mentions grid entry); if no compatible candidate survives, the node stays **unresolved** (no nearest-neighbor fallback). Pairing / hospital / roster mismatch gaps **cap link confidence to low**. Decision outcomes include `observer` + `tool_or_view` for attainable evidence (RMS and/or WCS/SSMS when the node expects it).

**Capability / role multi-link (A3):** Stage 8 boosts candidates when `node.expects_capability ∩ runbook.capability_tags` is non-empty, prefers compatible `access_surface` / `audience_roles`, and allows multi-link for the same capability across different surfaces (e.g. RMS UI + WCS/SSMS) or roles (**RMS ≈ operator/L1; WCS/SSMS ≈ L2/L3**). Intent scoring does **not** prefer RMS fleet-status peers over SSMS/`wcs_sql` when the node job is system state or active errors. Query text and retrieval rescoring include `expects_*` tags. Prompt policy: `stage_prompts/stage_8/stage8_playbook_linking_prompt.md`. If expected surfaces remain uncovered after primary + fleet companions (common when three RMS peers fill the node), Stage 8 injects or swaps in a capability-matching catalog peer for the missing surface (priority includes `wcs_sql`). **WCS SQL peers are capability-specific:** active-error SQL (gold: `proc_query_active_agv_errors_from_the_wcs_database_v1` from Active AGV error Query 1) is linked when the node expects `agv_active_errors` and title/intent (or `wcs_sql` placeholder) asks for AGV/system error state — not only the literal phrase “active AGV errors”. When `agv_active_errors` is expected, Stage 8 will **not** fill uncovered `wcs_sql` with related-only peers (e.g. SortGuid/`sort_lifecycle_state`); leave a catalog gap instead of attaching the wrong family. Pool-only or untagged Stage 6 runbooks (e.g. case 228086 Ignition restart) are hydrated via `infer_runbook_tags` before linking so Ignition/WCS support surfaces can attach. Prefer WCS + Ignition for remote support; do not force RMS/Aveva substitutes.

**Gap messaging (B3) / branch cleanup (B4) / SME pack (B5):** `match_gaps` and node `catalog_gaps` name actionable missing evidence paths (capability-tagged). `sanitize_playbook_branch_graph` drops empty/`from_node`-less and duplicate playbook-level branch rows; review MD/HTML marks procedure/escalation nodes with “no branch outcomes — proceed / escalate.” Full LLM re-run for pilot cases exports to `sme_review_runbooks/stage_8_playbooks_capability_tags/`. See `docs/design_decisions/stage_5_8_c2_b2_b1_changelog.md`.

On finalize, Stage 8 enriches `support_user_language_examples` for **every** playbook (case seed phrases + learned operator language) so sparse speech like `"AGVs aren't moving"` / `"no RMS alarms"` lands on retrieval cards and embeddings. Empty examples fail the Stage 11 cumulative gate. See `stage_8/support_language.py` and `docs/architecture.md`.

**Run (Azure embeddings + LLM link refinement)**

```powershell
python shared_pipeline_stages/scripts/stage8_finalize_playbooks.py `
  --pool-dir shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --incidents-root incidenceknowledgeingestion/data/output/incidents `
  --output-dir shared_pipeline_stages/data/output/shared `
  --llm
```

Use `--mock-embedder` only for local structural tests; `--llm` is still required.

For previously generated Stage 8 artifacts, migrate embedded runbook payloads
to compact references with:

```powershell
python shared_pipeline_stages/scripts/migrate_stage8_playbook_artifacts.py `
  shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/canonical_runbooks.json
```
**Outputs**

```text
shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/
  prompt_a_one_per_incident/
    canonical_playbooks.json
    playbook_runbook_links.json
    playbook_retrieval_cards.json
    playbook_retrieval_index.json
    playbook_finalization_report.json
    review_markdown/playbooks/*.md
    review_markdown/playbooks/*.html
  prompt_b_multi_flow/
    (same structure)
  stage_8_comparison_report.json
```

## Shared Stage 8.5: Corpus Relationship Linking

Stage 8.5 aggregates per-source `relationship_links.json` files from operational and incident outputs, optionally remaps source runbook IDs to canonical procedure IDs from Stage 7, and merges Shared Stage 8 playbook→runbook links into one corpus-wide graph.

**Inputs**

Each `--source-root` must contain:

```text
<source-root>/stage_8_relationship_linking/relationship_links.json
```

Optional shared inputs:

```text
shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/candidate_to_procedure_mapping.json
shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/*/playbook_runbook_links.json
```

**Run**

```powershell
python shared_pipeline_stages/scripts/stage8_5_link_relationships.py `
  --source-root operationalknowledgeingestion/data/output/manual_optisweep_om_v3 `
  --source-root incidenceknowledgeingestion/data/output/incidents/case_228086 `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --stage8-dir shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  --output-dir shared_pipeline_stages/data/output/shared
```

**Outputs**

```text
shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking/
  relationship_links.json
  relationship_linking_report.json
```

## Shared Stage 9: Corpus Validation

Stage 9 validates shared Stage 7 canonical runbooks, Shared Stage 8 finalized playbooks, and the Shared Stage 8.5 corpus relationship graph before embedding or publishing.

**Purpose**

Confirm link integrity, branch coverage, schema correctness, zero unresolved playbook→runbook links, and acceptable 8.5 remap coverage (source procedure IDs → canonical IDs).

**Inputs**

```text
shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/canonical_runbooks.json
shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/
shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking/relationship_links.json
```

**Run**

```powershell
python shared_pipeline_stages/scripts/stage9_validate_corpus.py `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --stage8-dir shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  --stage85-dir shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking `
  --output-dir shared_pipeline_stages/data/output/shared
```

**Outputs**

```text
shared_pipeline_stages/data/output/shared/stage_9_validation/validation_report.json
shared_pipeline_stages/data/output/shared/stage_9_validation/extraction_report.json
```

Stage 9 must pass (exit 0) before Stage 10–11.

## Shared Stage 10: Vector Embedding Generation

Stage 10 creates `EmbeddingRecord` exports for every retrievable document in the published corpus. **One shared stage, one embedding model, one publish batch** — operational and incidence sources contribute different record types into the same export.

| Record type | Source | Embedded from | Runtime role |
|-------------|--------|---------------|--------------|
| `canonical_runbook` | Shared Stage 7 | Rebuilt retrieval card from each canonical runbook | Procedure retrieval (prompts 3–5, playbook node fallback) |
| `playbook_prompt_a` | Shared Stage 8 Prompt A | `playbook_retrieval_cards.json` entry-symptom text | Symptom routing — Prompt A container |
| `playbook_prompt_b` | Shared Stage 8 Prompt B | `playbook_retrieval_cards.json` entry-symptom text | Symptom routing — Prompt B container |
| `operational_context` | Per-source Stage 4 | `retrieval_text` or title/summary only | Generic RAG — operational context container |
| `source_artifact` | Per-source Stage 2/3 | `retrieval_text` or title/summary only | Generic RAG — source artifact container |

Operational and incidence datasets do **not** get separate embedding pipelines or models. They differ by `record_type`, `source_type`, and filter metadata (`case_id`, `extraction_mode`, `procedure_id`, etc.) on each `EmbeddingRecord`.

**Inputs**

```text
shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks/canonical_runbooks.json
shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/prompt_a_one_per_incident/playbook_retrieval_cards.json
shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks/prompt_b_multi_flow/playbook_retrieval_cards.json
```

**Run**

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

Outputs include grouped files: `embedding_records_canonical_runbooks.json`, `embedding_records_playbooks_prompt_a.json`, `embedding_records_playbooks_prompt_b.json`, `embedding_records_operational_context.json`, `embedding_records_source_artifacts.json`.

**Outputs**

```text
shared_pipeline_stages/data/output/shared/stage_10_embeddings/embedding_records.json
shared_pipeline_stages/data/output/shared/stage_10_embeddings/embedding_generation_report.json
```

Each `EmbeddingRecord` includes: stable record ID, `record_type`, source record ID, embedded text, vector, embedding model name/version, source refs, and filter metadata for Cosmos queries and the app A/B toggle.

## Shared Stage 11: Cumulative Cosmos Publish And Manifest

Stage 11 must never ship a **narrower** newest partition than prior successful publishes. The app uses `AUTO_PUBLISH_VERSION=true`; a thin newest publish breaks Guided Troubleshoot.

**Flow (LangGraph + `cumulative_publish.py`)**

```text
assemble candidate bundle
  → merge prior Cosmos / local baseline (corpus_merge)
  → enrich support_user_language_examples on all playbooks
  → rebuild entry-scoped playbook embed text + embeddings as needed
  → build gate_phrase_table (prior ∪ seed ∪ new examples)
  → pre-publish gate (fail on dropped cases / empty examples / material count drops)
  → retrieval + gate-phrase smoke
  → write data/output/cosmos_publish (+ optional Cosmos upload, scope=all)
```

**Why:** Pilot publishes that only contained bag-out / hospital cases dropped `228086`; stoppage queries then ranked wrong. Cumulative merge + gate + smoke close that hole. Operator phrases and keyword tables publish with the same `publish_version_id` so app YAML is fallback-only.

**Key modules**

| Module | Role |
| --- | --- |
| `stage_11/corpus_merge.py` | Merge prior bundle + candidate |
| `stage_11/publish_gate.py` | Fail upload if corpus shrinks or examples empty |
| `stage_11/gate_phrase_table.py` | Versioned phrase doc for app keyword gating |
| `stage_11/cumulative_publish.py` | End-to-end cumulative path |
| `stage_8/support_language.py` | Operator-language enrichment (also at Stage 8 finalize) |

**Containers (env vars)**

```text
COSMOS_ENDPOINT
COSMOS_KEY
COSMOS_DATABASE
COSMOS_CONTAINER_RUNBOOKS
COSMOS_CONTAINER_PLAYBOOKS_A
COSMOS_CONTAINER_PLAYBOOKS_B
COSMOS_CONTAINER_OPERATIONAL_CONTEXT
COSMOS_CONTAINER_SOURCE_ARTIFACTS
COSMOS_CONTAINER_RELATIONSHIP_LINKS
COSMOS_CONTAINER_CANONICAL_IMAGES
COSMOS_CONTAINER_GATE_PHRASE_TABLES   # default: gate_phrase_tables
```

Blob image upload (Stage 11):

```text
AZURE_STORAGE_CONNECTION_STRING
AZURE_CANONICAL_IMAGES_CONTAINER
AZURE_STORAGE_ACCOUNT_URL
```

**Publish bundle layout**

```text
publish_bundle/
  runbooks/documents.json
  runbooks/embeddings.json
  playbooks_prompt_a/documents.json
  playbooks_prompt_a/embeddings.json
  playbooks_prompt_b/documents.json
  playbooks_prompt_b/embeddings.json
  operational_context/rag_records.json
  operational_context/embeddings.json
  source_artifacts/rag_records.json
  source_artifacts/embeddings.json
  canonical_images/documents.json
  relationship_links/shard_000.json
  gate_phrase_tables/documents.json
```

Relationship links are sharded to stay under the Cosmos 2 MB document limit. Gate phrase contract: `app_handoff_package/GATE_PHRASE_TABLE_CONTRACT.md`.

**Run (prefer orchestration cumulative path)**

```powershell
python orchestration/scripts/run_ingestion_agent.py `
  --source "data/inbox/incidents/Case 228086 Data.pdf" `
  --with-publish `
  --publish-to-cosmos `
  --publish-scope all
```

Standalone Stage 11 assemble (legacy path; still prefer cumulative via orchestration):

```powershell
python shared_pipeline_stages/scripts/stage11_publish_cosmos.py `
  --stage7-dir shared_pipeline_stages/data/output/shared/stage_7_merged_runbooks `
  --stage8-dir shared_pipeline_stages/data/output/shared/stage_8_finalized_playbooks `
  --stage10-dir shared_pipeline_stages/data/output/shared/stage_10_embeddings `
  --stage85-dir shared_pipeline_stages/data/output/shared/stage_8_5_relationship_linking `
  --output-dir shared_pipeline_stages/data/output/shared
```

**Outputs**

```text
data/output/cosmos_publish/publish_manifest.json
data/output/cosmos_publish/publish_manifest_diff.json
data/output/cosmos_publish/case_inventory.json
data/output/cosmos_publish/retrieval_smoke_report.json
data/output/cosmos_publish/publish_bundle/
shared_pipeline_stages/data/output/shared/stage_11_cosmos_publish/   # candidate assemble
```

`publish_manifest.json` includes publish version ID, record counts, embedding model, checksums, container refs, Stage 8.5 link counts, and gate phrase table presence.

## Related Docs

- Architecture + why: `docs/architecture.md`
- README update hook: `docs/README_UPDATE.md`
- Root overview: `README.md`
- Orchestration / LangGraph publish: `orchestration/README.md`
- Operational source stages: `operationalknowledgeingestion/README.md`
- Incident source stages: `incidenceknowledgeingestion/README.md`
- App gate phrases: `app_handoff_package/GATE_PHRASE_TABLE_CONTRACT.md`
- Shared Stage 6 prompts: `stage_prompts/stage_6/README.md`
