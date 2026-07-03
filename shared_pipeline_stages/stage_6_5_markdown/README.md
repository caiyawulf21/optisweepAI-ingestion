# Stage 6.5 Markdown Documentation

This folder documents how Shared Stage 6.5 scores runbook similarity, how merge clusters
are formed, and how we tune weights before Stage 7.

## Contents

| Document | Purpose |
| --- | --- |
| [Lexical similarity explained](lexical_similarity_explained.md) | How Jaccard keyword scoring works (stopwords, order, synonyms) |
| [Weight tuning experiments](weight_tuning_experiments.md) | Test plan and methodology for tuning runs |
| [Tuning results summary](tuning_results_summary.md) | Generated comparison after experiments complete |

## Related outputs

Each tuning experiment writes its own directory under:

```text
shared_pipeline_stages/data/output/shared/stage_6_5_tuning/{experiment_name}/
  runbook_pool.json
  merge_clusters.json
  merge_cluster_review.md   ← human-readable cluster explanations
  runbook_pool_report.json
```

The production-style Azure embedding run lives at:

```text
shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool/
```

## Quick reference: combined score

```text
combined = vector_weight × cosine + lexical_weight × jaccard
if opposing_actions: combined × opposing_action_penalty
```

Pairs with `combined ≥ min_merge_score` can form merge cluster edges (cross-source only).
