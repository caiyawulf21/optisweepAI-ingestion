# Shared Pipeline Stages

`shared_pipeline_stages/` holds cross-pipeline stage code and shared local outputs. Both ingestion areas converge here after source-specific extraction.

```text
shared_pipeline_stages/
  data/
    input/      optional shared inputs
    output/     shared stage outputs (Stage 6.5+)
    processed/  optional intermediate files
    review/     reviewer-facing samples and validation outputs
  stage_6_5/    runbook pool, similarity, merge prep
  stage_prompts.py
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

**Inputs**

Each `--source-root` must contain:

```text
stage_6_finalized_runbooks/finalized_runbooks/*.json
```

**Run**

From the repo root:

```powershell
python scripts/stage6_5_build_runbook_pool.py `
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

## Related Docs

- Root overview: `README.md`
- Operational source stages and review: `operationalknowledgeingestion/README.md`
- Incident source stages and review: `incidenceknowledgeingestion/README.md`
- Shared Stage 6 prompts: `stage_prompts/stage_6/README.md`
