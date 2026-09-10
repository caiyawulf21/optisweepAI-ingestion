# OptiSweep Brain MCP server

Agent-facing MCP surface for Brain ingestion, reconciliation, drafting, and
pipeline orchestration. Business logic lives in `brain_service.*`; this package
is thin validation + provider wiring + JSON shaping (`tools.py`) registered by
`server.py`.

## Run

```powershell
pip install -e mcp_server
python -m mcp_server.server
# or: optisweep-brain-mcp
```

Stdio MCP server name: `optisweep-brain`.

## Env / providers

Selection: `mcp_server/providers_config.py`. Full key inventory: repo-root
`.env.mock` (preferred for agents) or `.env.example`.

| Env | Default | Used by |
|-----|---------|---------|
| `OPTISWEEP_LLM_PROVIDER` | `azure_openai` | Most Brain tools |
| `OPTISWEEP_VISION_PROVIDER` | `azure_cv` | Pipeline ingest (CV OCR only) |
| `OPTISWEEP_EMBEDDING_PROVIDER` | `azure_openai` | `get_brain_context` when `query_text` set |
| `OPTISWEEP_STORAGE_BACKEND` | `local` | All storage reads/writes (`local` → `brain/data/local/`, `azure` → Cosmos) |
| `BRAIN_INGESTION_ENABLED` | forced `1` inside ingest tools | Pipeline Brain hooks |

Also need Azure OpenAI / Computer Vision / (optional) Cosmos vars from `.env.mock`
Blocks A–H depending on which tools you call.

## Tool catalog

Source of truth for **registered MCP names and exposed args**: `mcp_server/server.py`.
Implementations: `mcp_server/tools.py`.

### Create-path chain (one candidate at a time)

Typical order: `extract_evidence` → `classify_candidate` → `reconcile_candidate`
→ `validate_and_prepare_for_review`.

#### `extract_evidence`

| | |
|--|--|
| **Purpose** | Turn one bounded raw source packet into EvidenceUnit + raw claim candidates. |
| **Inputs** | `source_packet: dict` — bounded source payload (shape owned by `brain_service.extraction`). |
| **Outputs** | Extraction result model as JSON (`model_dump`). |
| **When** | First step on new source text/artifacts into Brain. |
| **Constraints** | Needs LLM. Does **not** judge truth, resolve entity ids, or decide duplicates. |

#### `classify_candidate`

| | |
|--|--|
| **Purpose** | Classify one raw claim candidate as Entity / Capability / Claim / Relationship. |
| **Inputs** | `candidate_text: str`, `evidence_id: str`, `likely_entity_ids: list[str] \| null` |
| **Outputs** | `ClassifiedCandidate` JSON. |
| **When** | After extraction, per candidate. |
| **Constraints** | Needs LLM + storage. Uses locked entity/claim boundary test. |

#### `reconcile_candidate`

| | |
|--|--|
| **Purpose** | Decide `REINFORCE` / `PATCH` / `CONFLICT` / `GAP` / `NEW_CANDIDATE` vs corpus. |
| **Inputs** | `classified: dict` — prior `ClassifiedCandidate` JSON. |
| **Outputs** | `ReconciliationDecision` JSON. |
| **When** | After classify, before review prep. |
| **Constraints** | Needs LLM + storage. Runs mandatory duplicate check for `NEW_CANDIDATE`. |

#### `validate_and_prepare_for_review`

| | |
|--|--|
| **Purpose** | Mechanically validate reconciled candidate; draft plain-language `BrainReview`. |
| **Inputs** | `reconciled: dict` — prior `ReconciliationDecision` JSON. |
| **Outputs** | `BrainReview` JSON. |
| **When** | Last Create-path step before human approval. |
| **Constraints** | Storage only (no LLM). **Never self-approves.** |

### Audit path

#### `find_audit_candidates`

| | |
|--|--|
| **Purpose** | Read-only scan for duplicates, mis-typed records, dangling refs. |
| **Inputs** | `record_ids: list[str] \| null` — optional subset; null = broader scan. |
| **Outputs** | `{ "findings": [ ... ] }` |
| **When** | Corpus hygiene / migration QA. |
| **Constraints** | Storage only. Deliberately over-reports; never resolves. |

#### `resolve_audit_candidate`

| | |
|--|--|
| **Purpose** | Propose `MERGE` / `RETYPE` / `RECLASSIFY` / `NOT_A_DUPLICATE` / `NEEDS_HUMAN`. |
| **Inputs** | `review: dict` — `BrainReview` JSON for one finding. |
| **Outputs** | Resolution proposal JSON. |
| **When** | After `find_audit_candidates` (or an existing audit review). |
| **Constraints** | Needs LLM + storage. **Proposes only** — does not write resolution to corpus. |

### Batch orchestration

#### `run_migration_batch`

| | |
|--|--|
| **Purpose** | Loop Create-path over a batch of item ids with preloaded packets. |
| **Inputs** | `items: list[str]`, `source_packets: dict[str, dict]` — map each item id → source packet. |
| **Outputs** | Migration report (`asdict`). |
| **When** | Bulk Brain migration without inventing a new per-source script. |
| **Constraints** | Needs LLM + storage. Packets must be supplied up front (MCP cannot pass callables). |

### Draft FROM Brain (not static ontology catalogs)

#### `draft_procedure`

| | |
|--|--|
| **Purpose** | Draft a Procedure for a Capability from Brain fields + retrieved context. |
| **Inputs** | `capability_id: str`, `distinguishing_token: str`, `scope: str`, `extra_source_evidence_ids: list[str] \| null`, `write: bool=false` |
| **Outputs** | `{ procedure, rationale, gaps, written }` |
| **When** | Capability exists; you want operator steps grounded in Brain, not `docs/ontology` snippets. |
| **Constraints** | Needs LLM + storage. Default `write=false` (inspect first). `write=true` persists Procedure + `NEW_CANDIDATE` review under `scope`. |

#### `draft_playbook`

| | |
|--|--|
| **Purpose** | Draft symptom-entry Playbook routing to **existing** Procedures via symptom graph. |
| **Inputs** | `entry_symptom_entity_ids: list[str]`, `distinguishing_token: str`, `scope: str`, `write: bool=false` |
| **Outputs** | `{ playbook, rationale, gaps, written }` |
| **When** | Procedures already drafted; build branching playbook from MAY_INDICATE/VERIFIES/CAUSES/CONTRIBUTES_TO. |
| **Constraints** | Needs LLM + storage. Never embeds Procedure steps — only `procedure_id` refs. Default dry-run (`write=false`). |

### Context / validation / SME review / run bookkeeping

#### `get_brain_context`

| | |
|--|--|
| **Purpose** | Build a `ContextPacket` (record IDs only) via id lookup, relationship hops, optional semantic search. |
| **Inputs** | `task: dict`, `entity_ids: list[str] \| null`, `relationship_types: list[str] \| null` (enum names), `hops: int=1`, `query_text: str \| null` |
| **Outputs** | `ContextPacket` JSON (IDs, never inlined bodies). |
| **When** | Agents need scoped Brain neighborhood for drafting/reasoning. |
| **Constraints** | Storage always; embeddings provider only if `query_text` set. Invalid relationship type strings fail. |

#### `validate_brain_records`

| | |
|--|--|
| **Purpose** | Schema + cross-ref validation for a batch of records. |
| **Inputs** | `records_by_type: dict` keys among: `evidence_units`, `entities`, `claims`, `relationships`, `capabilities`, `procedures`, `playbooks`, `reviews` |
| **Outputs** | `{ "valid": bool, "errors": [...] }` |
| **When** | Before write / after external transform. |
| **Constraints** | Unknown keys ignored. No LLM. |

#### `prepare_sme_review`

| | |
|--|--|
| **Purpose** | Persist a `BrainReview` for human approval (caller supplies explanation text). |
| **Inputs** | `candidate_record_ids: list[str]`, `kind: str`, `proposed_change: str` |
| **Outputs** | Saved `BrainReview` JSON. |
| **When** | Packaging a change set for SME without LLM-authored copy. |
| **Constraints** | Storage write to scope `reviews/prepared`. `kind` must be a `ReviewKind` value: `reinforce`, `patch`, `conflict`, `gap`, `new_candidate`, `audit_finding`. No LLM. |

#### `get_ingestion_run`

| | |
|--|--|
| **Purpose** | Load saved ingestion job bookkeeping by `run_id`. |
| **Inputs** | `run_id: str` |
| **Outputs** | Run record dict, or `null` if missing. |
| **When** | Follow-up after `ingest_*` tools. |
| **Constraints** | Storage only. |

### Pipeline orchestration (subprocess CLIs)

Both tools set `BRAIN_INGESTION_ENABLED=1`, force `--ocr-backend azure_cv`, and call
`orchestration/scripts/run_ingestion_agent.py`. They do **not** reimplement stages.

> **MCP vs tools.py:** `tools.py` also accepts `run_shared_publish`, `publish_to_cosmos`,
> `publish_scope`, but `server.py` does **not** expose those MCP parameters today —
> shared publish / Cosmos publish stay at their tool defaults (`False`). To publish,
> run the orchestration CLI directly or extend the `@server.tool` signatures.

#### `ingest_incident_pdf`

| | |
|--|--|
| **Purpose** | Run incidence Stages (default `1,2,2.5,3,4,5,6,8`) with in-tandem Brain hooks. |
| **Inputs (MCP)** | `source_pdf_path: str`, `case_id: str`, `site_code: str="ups_haslet_tx"`, `output_dir: str \| null`, `stages: str="1,2,2.5,3,4,5,6,8"` |
| **Outputs** | `{ run_id, succeeded, output_dir, review_status, stdout_tail, stderr_tail }` |
| **When** | Ingest one incident PDF end-to-end via the same orchestrator a human uses. |
| **Constraints** | Filename must encode `case_id` (e.g. `Case 233681 Data.pdf`) — mismatch returns `succeeded=false` without running. Requires Azure CV (+ LLM for later stages). Default output: `incidenceknowledgeingestion/data/output/incidents/case_<case_id>/`. Saves ingestion run to storage. `site_code` is accepted on the MCP surface but not currently passed into the CLI command. |

#### `ingest_operational_source`

| | |
|--|--|
| **Purpose** | Run operational Stages (default `1,2,3,4,5,6,8`) with Brain hooks; Brain scope `operational_sources/<source_id>`. |
| **Inputs (MCP)** | `source_pdf_path: str`, `source_id: str`, `source_type: str="manual"`, `output_dir: str \| null`, `stages: str="1,2,3,4,5,6,8"` |
| **Outputs** | Same shape as `ingest_incident_pdf`. |
| **When** | Ingest a manual/ops PDF (or path the orchestrator accepts) into operational pipeline + Brain. |
| **Constraints** | Azure CV + LLM as for incidence. Default output: `operationalknowledgeingestion/data/output/<source_id>/`. `source_type` is accepted on MCP but not currently passed into the CLI command. |

## Out of scope

This server does **not** serve end-user runtime chat context or app feedback loops
(those belong in the separate appcode repo). See `brain/AGENT_DESIGN_NOTES.md` and
`AGENT_AZURE_HANDOFF.md` for contracts and Azure setup.

## Related paths

| Path | Role |
|------|------|
| `mcp_server/server.py` | MCP registration |
| `mcp_server/tools.py` | Tool implementations |
| `mcp_server/providers_config.py` | Provider factories |
| `brain_service/` | Domain logic |
| `.env.mock` | Agent-readable env inventory |
