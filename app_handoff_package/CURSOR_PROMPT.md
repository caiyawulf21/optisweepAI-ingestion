# Cursor implementation brief — Cosmos-only playbook orchestration

**Audience:** AI agent in the OptiSweep AI **app repo** (backend + frontend).  
**Data source:** Azure Cosmos DB only — see `COSMOS_DATA_MAP.md`.  
**Goal:** Rip out legacy filesystem/YAML/CAT-1/root-cause orchestration. Wire playbook-first runtime to Cosmos. Low latency. No Azure AI Search.

---

## Rule zero

```
ALL corpus data is in Cosmos.
DELETE every code path that reads from local data/ files, YAML workflows,
root_cause_dataset, cat1_records, procedure dictionaries, or sample_data/.
```

If a loader does not query Cosmos with `publish_version_id`, remove it.

---

## Cosmos layout (read COSMOS_DATA_MAP.md)

| Container env | Contents |
|---------------|----------|
| `COSMOS_CONTAINER_RUNBOOKS` | Canonical runbooks + runbook embeddings |
| `COSMOS_CONTAINER_PLAYBOOKS_A` | Prompt A playbooks + playbook embeddings |
| `COSMOS_CONTAINER_PLAYBOOKS_B` | Prompt B playbooks + playbook embeddings |
| `COSMOS_CONTAINER_RELATIONSHIP_LINKS` | Sharded relationship graph |
| `COSMOS_CONTAINER_SOURCE_ARTIFACTS` | Artifact RAG (screenshots) |
| `COSMOS_CONTAINER_OPERATIONAL_CONTEXT` | Manual context RAG |

Partition key on every document: `publish_version_id`.  
Set `PUBLISH_VERSION_ID` from ingestion `publish_manifest.json`.

---

## DELETE LIST — remove from app repo

Execute this cleanup **before** adding new code. Delete files, routes, env flags, and tests that depend on them.

### Data files and loaders (delete entirely)

| Path / concept | Why |
|----------------|-----|
| `data/derived/root_cause_dataset.json` + loaders | Not published; playbooks replace case triage |
| `data/curated/cat1_records.json` + `LocalCat1RetrievalClient` | Not published; runbook embeddings in Cosmos |
| `data/workflows/*.yaml` + `data/workflows/canonical/*.yaml` | Not published; playbooks in Cosmos |
| `data/normalized/canonical_procedure_dictionary.json` | Not published |
| `data/normalized/discovered_canonical_procedures.json` | Not published |
| `data/normalized/canonical_images.json` | Use `artifact_runbook` links from Cosmos graph |
| `data/escalation/escalation_summaries.json` | Use runbook `escalation_guidance` field |
| `backend/app/routing/signal_alias_map.yaml` as routing spine | Optional keywords only; not orchestration |
| `LOCAL_CORPUS_PATH` / `sample_data/` / `RETRIEVAL_BACKEND=local_files` | Data is in Cosmos |
| Azure AI Search clients and index seed scripts | Not used; brute-force Cosmos vectors |

### Backend modules (delete or gut)

| Module | Action |
|--------|--------|
| `backend/app/graph/case_triage_graph.py` | **Delete** hot path; replace with `playbook_graph.py` |
| `backend/app/graph/graph.py` (`run_troubleshooting` legacy) | **Delete** |
| `root_cause_retrieval_node` | **Delete** |
| `case_summary` confirmation gate (blocking) | **Delete** — auto-pin on strong playbook match |
| `backend/app/routing/orchestration_logic.py` → `HybridWorkflowRouter` | **Delete** |
| `backend/app/routing/hybrid_workflow_router.py` | **Delete** |
| `DynamicProcedureSelector` + procedure dictionary scoring | **Delete** |
| `CanonicalWorkflowLoader` (YAML) | **Delete** |
| `WorkflowLoader` (legacy flat YAML) | **Delete** |
| `legacy_workflow` / `fallback_legacy` graph nodes | **Delete** |
| `dynamic_procedure_guidance` graph node | **Delete** |
| `retrieval_only` as primary path | **Delete** — keep thin runbook fallback only |
| `compute_deterministic_orchestration()` | **Delete** |
| `ENABLE_LLM_WORKFLOW_REASONING` overlay | **Delete** default; off permanently for demo |
| Session fields: `extracted_canonical_signals`, `case_triage_top_matches`, `suggested_workflow_id`, growing signal merge | **Delete** |

### Env flags (delete)

```env
USE_CANONICAL_ROUTING          # YAML router — gone
RETRIEVAL_BACKEND=local        # CAT-1 — gone
RETRIEVAL_BACKEND=azure_search # gone
RETRIEVAL_BACKEND=local_bm25_agent # gone
RETRIEVAL_BACKEND=local_files  # gone
ENABLE_DYNAMIC_PROCEDURE_GUIDANCE
ENABLE_LEGACY_WORKFLOW
LOCAL_CORPUS_PATH
```

### Keep (simplified)

| Keep | Change |
|------|--------|
| `POST /troubleshoot` | Wire to new `playbook_graph` |
| `escalation_node` | Simplify; read from runbook payload |
| Keyword symptom extract | Slim; no LLM by default |
| `SESSION_BACKEND` | Slim session schema |
| Azure OpenAI **embeddings** for query vector only | Same model as Stage 10 |

---

## Target runtime

```text
POST /troubleshoot
  session_load
    if session.active_playbook_id → playbook_execute (resume, zero retrieval)
    else:
      embed query (Azure, same model as Cosmos index)
      brute-force hybrid search playbook embeddings in Cosmos container A or B
      if score >= threshold → pin playbook_id, case_id from payload
      else brute-force search runbook embeddings in COSMOS_CONTAINER_RUNBOOKS
  playbook_execute
    load playbook.payload from Cosmos by record_id
    resolve runbook: node.resolved_runbook_ids[0] OR relationship_graph playbook_runbook edge
    load runbook.payload from Cosmos
    render one support-safe step + artifact_runbook images
    advance node / branch_clarification / escalation
  END
```

**Turn 2+:** zero vector searches. Session carries `playbook_id`, `current_node_id`, `publish_version_id`.

---

## Staged implementation

### Stage 0 — Config and delete (do first)

1. Read `COSMOS_DATA_MAP.md` and `config/feature_flags.env.example`.
2. Set Cosmos env vars + `PUBLISH_VERSION_ID` from ingestion `publish_manifest.json`.
3. **Execute DELETE LIST above.** Remove dead imports and fix broken tests.
4. Confirm app starts with no filesystem corpus dependencies.

**Done when:** `grep -r "root_cause_dataset\|cat1_records\|workflows/canonical\|LOCAL_CORPUS" backend/` returns nothing.

---

### Stage 1 — Cosmos corpus client

Create `backend/app/corpus/cosmos_client.py`:

| Method | Cosmos query |
|--------|--------------|
| `load_embedding_index(version, record_types)` | All `doc_type=embedding` from playbooks A/B + runbooks + operational_context + source_artifacts containers |
| `get_playbook(playbook_id, variant)` | `doc_type=playbook` from A or B container |
| `get_runbook(procedure_id)` | `doc_type=runbook` from runbooks container |
| `load_relationship_graph(version)` | All `doc_type=relationship_graph` shards, merge `links[]` |
| `get_artifact(artifact_id)` | `doc_type=rag_record` from source_artifacts container |

- Cache embedding index + link graph in memory at startup (refresh on version change).
- Partition every query with `publish_version_id`.

**Done when:** Integration test loads real playbook `228086` and runbook from Cosmos.

---

### Stage 2 — Hybrid retrieval (no Azure AI Search)

Port scoring from `retrieval/local_hybrid_retriever.py` → `backend/app/retrieval/hybrid_retriever.py`.

```python
combined = 0.7 * cosine(query_vector, doc.vector) + 0.3 * jaccard(query_text, doc.embedded_text)
```

- Query embedding: Azure OpenAI, **same deployment as `embedding_model` in manifest**.
- Search playbook embeddings in active A/B container only (turn 1).
- Search runbook embeddings in runbooks container (fallback).
- Thresholds: rank/candidates from ~0.35; auto-pin only when hybrid ≥ 0.55 **and** entry-phrase coverage ≥ ~0.25 (or user picks). High-confidence pin ≥ 0.75.
- Also boost with `observed_entry_symptoms` / `support_user_language_examples` overlap from playbook payload.
- Do not lower the pin bar or inflate scores to fit sparse queries.

See `retrieval/ALGORITHMS.md` (playbook entry embed contract + pin vs rank).

**Done when:** "AGVs stopped" → 228086 playbook; "zone can't pair" → 228723 playbook against live Cosmos.

---

### Stage 3 — Slim session

```json
{
  "session_id": "...",
  "publish_version_id": "publish_...",
  "playbook_variant": "prompt_a",
  "active_playbook_id": null,
  "active_case_id": null,
  "current_node_id": null,
  "branch_state": {},
  "completed_node_ids": [],
  "operator_role": "L1_support"
}
```

Delete historical signal accumulation.

---

### Stage 4 — Playbook graph

Single graph `playbook_graph.py`:

| Node | Purpose |
|------|---------|
| `session_load` | Resume or retrieve |
| `playbook_retrieve` | Cosmos hybrid search |
| `playbook_execute` | Node + runbook + artifacts |
| `branch_clarification` | Unresolved `decision_outcomes` |
| `runbook_fallback` | Weak playbook match only |
| `escalation` | Role gate / user action |

No other graph files on the hot path.

---

### Stage 5 — Frontend

1. Remove blocking case-confirmation modal.
2. Playbook node stepper (title, intent, runbook step, branch buttons).
3. A/B toggle → `playbook_variant` → Cosmos container A vs B.
4. Images from `artifact_runbook` graph edges + source_artifacts container.
5. Delete UI that renders YAML workflow definitions.

---

### Stage 6 — Validation

| Prompt | Expected |
|--------|----------|
| 1 — AGVs stopped | 228086 Prompt A playbook from Cosmos |
| 2 — Zone can't pair | 228723 Prompt A playbook from Cosmos |
| 3–5 | Runbook fallback from Cosmos embeddings |

| Latency | Target |
|---------|--------|
| Turn 1 | < 500ms (embed + in-memory scan of Cosmos-loaded index) |
| Turn 2+ | < 100ms (ID lookups only) |

---

## Session schema mapping

| Playbook `payload` field | Session / runtime |
|--------------------------|-------------------|
| `playbook_id` | `active_playbook_id` |
| `case_id` | `active_case_id` |
| `nodes[].node_id` | `current_node_id` |
| `nodes[].resolved_runbook_ids` | runbook load key |
| `nodes[].decision_outcomes` / `branches` | clarification UI |
| `extraction_mode` | A/B variant |

Full field map: `schema/record_types.md`.

---

## Success criteria

- [ ] Zero filesystem corpus reads in backend
- [ ] All documents loaded from Cosmos by `publish_version_id`
- [ ] DELETE LIST items removed
- [ ] No Azure AI Search calls
- [ ] No `HybridWorkflowRouter` / `root_cause_retrieval` / YAML workflow loaders
- [ ] Turn 2+ performs zero vector searches
- [ ] Prompts 1–2 E2E against live Cosmos

**Start Stage 0 (delete) before writing new loaders.**
