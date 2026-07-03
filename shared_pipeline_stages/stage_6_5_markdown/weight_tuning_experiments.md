# Stage 6.5 Weight Tuning Experiments

## Goal

Find similarity weight and threshold settings that produce **useful merge clusters**
(manual ↔ training pairs for the same procedure) without over-chaining unrelated
runbooks, before running selective Stage 7 LLM merges.

## Methodology

### Inputs

Stage 6 finalized runbooks from:

- `operationalknowledgeingestion/data/output/manual_optisweep_om_v3`
- `operationalknowledgeingestion/data/output/training_video_day1`
- `incidenceknowledgeingestion/data/output/incidents/case_228086`

### Embeddings

- Model: Azure `text-embedding-3-small` (1536 dimensions)
- First baseline run loads or generates embeddings once
- Subsequent experiments **reuse** `runbook_retrieval_index.json` from baseline (clustering-only, no re-embed)

### Scoring formula

```text
combined = vector_weight × cosine + lexical_weight × jaccard
if opposing_actions (start/stop, add/remove in title/verbs): combined × opposing_action_penalty
```

### Lexical (Jaccard) token rules

Lexical similarity is **order-independent** and uses **stopword-filtered tokens only**:

| Rule | Detail |
| --- | --- |
| Stopwords excluded | `a`, `an`, `and`, `for`, `in`, `of`, `on`, `the`, `to`, `use`, `using`, `with` |
| Length filter | tokens with length ≤ 1 dropped |
| Synonym normalization | `verify`, `review`, `inspect` → `check`; `shutdown` → `stop`; etc. |
| Not used | exact phrase matching, word order, metadata fields |

See [lexical_similarity_explained.md](lexical_similarity_explained.md).

### Clustering

- Cross-source pairs only (`manual` ↔ `training_video`, etc.)
- Per runbook: top-K matches with `combined ≥ min_merge_score`
- Single-linkage connected components → merge clusters (≥2 source types)

### Outputs per experiment

```text
shared_pipeline_stages/data/output/shared/stage_6_5_tuning/{experiment_name}/
  merge_clusters.json
  merge_cluster_review.md    ← titles, summaries, pairwise link explanations
  runbook_pool_report.json
```

## Experiments

| Experiment | vector_weight | lexical_weight | min_merge_score | high_confidence_score | Hypothesis |
| --- | ---: | ---: | ---: | ---: | --- |
| `baseline_v0.7_l0.3` | 0.70 | 0.30 | 0.62 | 0.78 | Current default; reference run |
| `low_lexical_v0.85_l0.15` | 0.85 | 0.15 | 0.62 | 0.78 | Less lexical pull; rely more on embeddings |
| `low_lexical_v0.9_l0.1` | 0.90 | 0.10 | 0.62 | 0.78 | Minimal lexical influence |
| `lower_threshold_min0.58` | 0.70 | 0.30 | 0.58 | 0.78 | Same weights; admit more borderline pairs |

Shared defaults unless noted:

- `opposing_action_penalty`: 0.5
- `top_k`: 10

## Evaluation criteria

For each experiment review `merge_cluster_review.md` and record:

1. **Cluster count** — fewer false chains preferred
2. **Cluster quality** — do 2-runbook manual↔training pairs look like same procedure?
3. **Over-chaining** — flag clusters with >3 runbooks or weak transitive links
4. **Near-miss pairs** — pairs scoring 0.55–0.62 that might deserve merge at lower threshold
5. **Incident isolation** — case 228086 runbook should stay pass-through unless clearly related

## Running experiments

```bash
python shared_pipeline_stages/scripts/stage6_5_tune_weights.py
```

Results summary written to [tuning_results_summary.md](tuning_results_summary.md).

## Next steps after tuning

1. Pick weights/threshold for production Stage 6.5 defaults
2. Run Stage 7 on high-confidence 2-runbook clusters first
3. Manually review AGV multi-runbook clusters before merging
