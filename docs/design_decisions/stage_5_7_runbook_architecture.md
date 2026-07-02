# Stage 5–8 Runbook Architecture

This note defines the runbook extraction and finalization architecture used by
both `operationalknowledgeingestion` and `incidenceknowledgeingestion`.

Canonical runbook structure reference:
[`incidenceknowledgeingestion/datastructureprompts/Runbook Example.md`](../../incidenceknowledgeingestion/datastructureprompts/Runbook%20Example.md)

Stage 6 LLM runtime reference (trimmed, appended to system prompt):
[`stage_prompts/stage_6/stage6_runbook_finalization_structure_reference.md`](../../stage_prompts/stage_6/stage6_runbook_finalization_structure_reference.md)

Related notes:

- [Runbook Candidate Pool, Merge Review, And Azure Publishing Design Notes](runbook_candidate_pool_and_azure_review_design.md)
- [Stage 5/6 Playbook Extraction Mode Decision Notes](stage_5_6_playbook_extraction_modes.md)

## Overall Principle

- **Stages 1–6 are source-specific** (manual, training slides, transcripts, incidents, SOPs, SME documents).
- **Stages 6.5–8 are shared** across all sources.
- **Stage 5 drafts** runbook candidates from a single source.
- **Stage 6 finalizes** source-specific runbooks with full artifact/context attachment.
- **Stage 7 merges only when needed** — it does not run on every runbook.

Each stage must be labeled **Deterministic** or **LLM Assisted**.

## Source-Specific Stages (1–6)

| Stage | Name | Mode |
| --- | --- | --- |
| 1 | Source bundle / source package loading | Deterministic |
| 2 | Source artifact and image extraction | Deterministic |
| 3 | Source artifact enrichment | LLM Assisted |
| 4 | Operational context extraction (or canonical incident record for incidents) | LLM Assisted |
| 5 | Runbook candidate discovery | LLM Assisted |
| 6 | Source runbook finalization | LLM Assisted |

Incident Stage 5 also runs playbook candidate discovery (Prompt A/B) as separate
LLM calls. Playbook outputs stay source-specific until Shared Stage 8.

## Stage 5 — Runbook Candidate Discovery (LLM Assisted)

**Purpose:** Discover and **draft** reusable runbook candidates from a single source.

The candidate is already drafted at this stage: title, goal, rough steps,
procedure type, role, and source refs. It is not yet a finalized runbook.

**Output:** `runbook_candidates.json`

**Rules:**

- Produce source-derived runbook candidate drafts only.
- Preserve source lineage.
- Do not merge or normalize across sources.
- Do not attach full artifact payloads or operational context records yet.
- Do not create workflow logic or relationships.

## Stage 6 — Source Runbook Finalization (LLM Assisted)

This stage runs independently inside each source ingestion pipeline.

**Purpose:** Turn each Stage 5 candidate draft into a **finalized source-specific
runbook** with all supporting evidence attached.

**Responsibilities:**

- Expand Stage 5 candidate drafts into full runbook structure per Runbook Example.md.
- Attach relevant source artifacts and image refs.
- Attach operational context records.
- Attach relevant source sections and OCR text.
- Attach nearby figures/tables.
- Attach source lineage and source metadata.
- Attach existing runbook reference if explicitly provided in the source.
- Produce Markdown + JSON review outputs per candidate.
- Preserve one finalized runbook per candidate.

**Do NOT:**

- Search other sources.
- Merge candidates across sources.
- Deduplicate across sources.
- Make cross-source merge decisions.

**Output:**

```text
finalized_runbooks/*.json
review_markdown/runbooks/*.md
runbook_finalization_report.json
```

Stage 6 creates complete, reviewable runbooks for one source. Cross-source
canonical merging happens later and only when Shared Stage 6.5 identifies a merge
cluster.

## Stage 6.5 — Shared Runbook Pool & Merge Preparation (Deterministic)

This is the **first shared stage**.

**Inputs:**

- Finalized runbooks from every source-specific Stage 6 output.

**Purpose:** Index all finalized runbooks and identify which ones need Shared
Stage 7 merge work.

**Responsibilities:**

- Build the shared runbook pool from all finalized source runbooks.
- Create retrieval cards for every finalized runbook.
- Generate normalized searchable metadata.
- Generate embeddings (or placeholder hooks).
- Build a runbook retrieval index.
- Compute cross-source similarity scores.
- Generate merge clusters and merge hints.
- Mark singleton runbooks for deterministic pass-through (no Stage 7 LLM).
- Preserve complete source lineage.

**Important:** Stage 6.5 does **not** merge runbooks. It only prepares merge
candidates and pass-through decisions.

**Outputs:**

```text
runbook_pool.json
retrieval_cards.json
runbook_similarity.json
runbook_retrieval_index.json
merge_clusters.json
pass_through_runbooks.json
```

## Stage 7 — Cross-Source Runbook Merge (LLM Assisted, Selective)

**Purpose:** Merge finalized runbooks from different sources when they represent
the same reusable procedure.

**Cost rule:** Stage 7 must **not** run on every runbook. Most finalized
runbooks should pass through Shared Stage 6.5 without an LLM merge call.

**When Stage 7 runs:**

- Shared Stage 6.5 marks a merge cluster with `likely_same_procedure` or
  `needs_review` above threshold.
- Two or more finalized runbooks from different sources appear to describe the
  same procedure.

**When Stage 7 does NOT run:**

- Singleton finalized runbooks with no merge cluster.
- Runbooks marked `unrelated` or below merge threshold.
- Pass-through runbooks promoted deterministically from `pass_through_runbooks.json`.

**Input (per merge cluster only):**

- Finalized runbooks in the cluster.
- Similarity evidence and merge hints from Stage 6.5.
- Existing canonical runbook (if applicable).

**Responsibilities:**

- Decide whether cluster members represent the same reusable procedure.
- Merge cross-source evidence when appropriate.
- Produce one merged canonical runbook (Markdown + JSON).
- Preserve source lineage from every contributing source.
- Record merge history, conflicts, and gaps.

**Output:**

```text
canonical_runbooks.json
review_markdown/runbooks/*.md
runbook_merge_report.json
candidate_to_procedure_mapping.json
```

Stage 7 owns **cross-source merge decisions only**. It does not re-draft
runbooks that Stage 6 already finalized unless a merge is required.

## Stage 8 — Playbook Finalization & Runbook Linking (LLM Assisted, Shared)

**Purpose:** Link finalized/canonical runbooks to playbooks and finalize
playbooks for runtime use.

**Inputs:**

- Canonical runbooks and pass-through finalized runbooks from Stage 6.5/7.
- Playbook candidates from incident Stage 5 (Prompt A/B).
- Operational context and source artifacts as needed.

**Responsibilities:**

- Resolve playbook `runbook_placeholder` nodes to canonical or finalized runbook IDs.
- Finalize playbook structure for review and runtime orchestration.
- Preserve source lineage and uncertainty.
- Do not treat single-incident playbooks as canonical without review.

**Output:**

```text
canonical_playbooks.json
review_markdown/playbooks/*.md
playbook_runbook_links.json
playbook_finalization_report.json
```

## Shared Stages After Stage 8

| Stage | Name | Mode |
| --- | --- | --- |
| 9 | Relationship linking | Deterministic (LLM fallback) |
| 10 | Validation and repair | Deterministic (LLM repair fallback) |
| 11 | Final reviewed output writing | Deterministic |
| 12+ | Embedding generation, publishing, knowledge graph | Deterministic / service |

## LangGraph Orchestration Shape

```text
Source-specific subgraph (per manual, video, incident, SOP, SME doc)
  Stage 1  [Deterministic]
  Stage 2  [Deterministic]
  Stage 3  [LLM Assisted]
  Stage 4  [LLM Assisted]
  Stage 5  [LLM Assisted]   draft runbook candidates
  Stage 6  [LLM Assisted]   finalize source runbooks
        |
        v
Shared finalization subgraph
  Stage 6.5  [Deterministic]  pool + similarity + merge clusters + pass-through
  Stage 7    [LLM Assisted]   merge clusters only (not every runbook)
  Stage 8    [LLM Assisted]   link runbooks to playbooks + finalize playbooks
  Stage 9+   [mixed]          links, validation, publish
```

## Cost And Responsibility Summary

| Stage | LLM on every item? | Primary output |
| --- | --- | --- |
| 5 | Yes (per candidate) | Draft candidates |
| 6 | Yes (per candidate) | Finalized source runbooks |
| 6.5 | No | Pool, similarity, merge clusters |
| 7 | **No — merge clusters only** | Merged canonical runbooks |
| 8 | Per playbook batch | Linked/finalized playbooks |

## Implementation Status

| Component | Operational | Incident | Shared |
| --- | --- | --- | --- |
| Stage 5 runbook candidates | Implemented | Implemented | — |
| Stage 6 runbook finalization | Implemented | Implemented | — |
| Stage 6.5 runbook pool | Legacy pool builder exists; needs refactor | — | Planned |
| Stage 7 merge-only | Prompt exists; needs merge-only refactor | — | Planned |
| Stage 8 playbook linking | — | Playbook candidates exist | Planned |

The existing operational `candidate_pool_builder.py` predates this architecture.
Refactor it into Stage 6.5 merge preparation over **finalized runbooks**, not
Stage 5 candidates or packet enrichment.
