# Stage 8 Link Scoring And Confidence

Date: 2026-07-06

This note documents retrieval and confidence tuning applied in Stage 8 playbook
finalization after the pilot run showed too many medium-confidence links and
procedure-type mismatches (for example recovery runbooks linked to diagnostic
nodes).

## Goals

1. Improve semantic alignment between playbook node placeholders and canonical runbooks.
2. Prefer procedure types that match node intent.
3. Retrieve at node granularity, not whole-playbook text.
4. Tighten multi-runbook selection so compound placeholders do not over-link.
5. Raise confidence on strong rank-1 matches when anchors and types align.

## Query normalization before embedding

Playbook placeholders often start with boilerplate such as "Procedure needed to…".
That wording adds little retrieval signal and dilutes embeddings.

`link_scoring.build_retrieval_query_text()` builds the embed/search query from:

- `node_type`
- `title`
- `intent` / `goal`
- normalized placeholder (boilerplate stripped via `normalize_placeholder_text()`)
- incident `affected_systems_or_components`

Stage 8 embeds this normalized node query, not the raw placeholder alone or the
full playbook card.

## Procedure-type boost and filtering

`runbook_search.search()` applies two complementary rules:

1. **Hard filter**: candidates whose `procedure_type` is blocked for the node type
   are excluded (for example `recovery` on `diagnostic_decision`).
2. **Soft boost**: compatible types receive +0.08 when they are the preferred
   type for the node, or +0.05 when they are in the allowed set
   (`link_scoring.procedure_type_boost()`).

Rankings use boosted combined score after lexical/vector similarity.

## Node-level retrieval

Retrieval is performed per finalized playbook node:

- Each node gets its own normalized query text and embedding.
- `RunbookCatalogSearch.search_for_node()` wraps query construction and search.
- The LLM linking packet receives `node_runbook_candidates` keyed by `node_id`.

Playbook-level retrieval cards remain for indexing and review metadata, but
linking decisions use node-scoped candidate lists.

## Multi-runbook selection (tightened)

Multiple runbooks per node remain allowed (max 3) but only when:

1. The placeholder is genuinely compound (`COMPOUND_PLACEHOLDER_PATTERN`), or
   for `validation_gate` when explicit conjunction language is present.
2. For non-validation nodes, at least two distinct domain anchor groups appear
   in the normalized placeholder.
3. Secondary runbooks must pass:
   - `boosted_score >= 0.42`
   - anchor overlap `>= 0.15`
   - procedure-type compatibility
   - confidence not `unresolved`

Similar titles/procedure IDs are deduplicated before adding a secondary link.

## Confidence tiers

Thresholds (tuned for playbook placeholder ↔ runbook card geometry):

| Tier | Boosted score floor |
|------|---------------------|
| high | ≥ 0.48 |
| medium | ≥ 0.38 |
| low | ≥ 0.28 |
| unresolved | below 0.28 |

`evaluate_link_confidence()` combines:

- boosted retrieval score
- anchor overlap between node query and runbook text
- procedure-type compatibility
- link rank (rank 1 can be elevated to high with strong overlap)
- optional LLM-provided confidence (honored for rank-1 high when type-compatible)

Incident-derived runbooks are no longer globally preferred. Incident reordering
uses a small margin (0.02) and linking policy tells the LLM to prefer incident
sources only for `procedure_reference` nodes.

## Intent phase alignment

Some runbooks are tagged `diagnostic` but are recovery-prep procedures (for example
gather fault information before entering the grid). Check-only playbook nodes should
not link those when a status-check runbook is available.

`link_scoring.py` classifies:

- **Check-phase nodes** — titles/intents with determine/check/whether/verify language
- **Recovery-prep runbooks** — when_to_use/title patterns such as "before entering the grid"
- **Status-check runbooks** — patterns such as "check overall system RMS"

Scoring applies +0.12 for status-check alignment and -0.18 for recovery-prep on
check nodes. `reconcile_llm_runbook_links()` overrides an LLM/recovery-prep rank-1
pick when a better status-check candidate exists within the override margin.

## Canonical source preference

Stage 7 keeps many overlapping topics as separate canonical runbooks (218 manual,
174 training_video). Training-video cards often score higher on incident playbooks
because their retrieval text mirrors support-call language ("first question on a
support call", "Overall System RMS").

Stage 8 applies source adjustments during ranking:

- `manual` / `sop` / `sme`: +0.06 to +0.08
- `training_video` / training slide sources: -0.06

Incident-derived runbooks are preferred only on `procedure_reference` nodes.


| Module | Responsibility |
|--------|----------------|
| `stage_8/link_scoring.py` | Query normalization, anchors, boosts |
| `stage_8/runbook_search.py` | Catalog search, type filter/boost, node search |
| `stage_8/normalize.py` | Match selection, confidence, multi-runbook rules |
| `stage_8/playbook_builder.py` | Node-level embed + search orchestration |

## Related

- [Stage 8 Playbook Finalization & Runbook Linking](stage_8_playbook_finalization.md)

## Review image embedding

Stage 8 HTML/MD review files copy runbook images into `review_markdown/playbooks/assets/`
using `stage_7/artifact_images.py`. The artifact index must include every source package
that contributed runbooks:

- `stage_3_artifact_enrichment/source_artifacts_enriched.json` (incidents, manuals)
- `stage_2_source_artifacts/source_artifacts_enriched.json` (training videos)

`resolve_artifact_image_path()` resolves storage paths relative to each ingestion package
root (`operationalknowledgeingestion/`, `incidenceknowledgeingestion/`).

To regenerate review files for an existing Stage 8 output without relinking:

```powershell
python shared_pipeline_stages/scripts/stage8_finalize_playbooks.py --refresh-reviews
```

