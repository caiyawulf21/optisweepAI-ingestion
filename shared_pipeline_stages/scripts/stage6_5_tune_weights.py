"""Run Stage 6.5 weight-tuning experiments with separate outputs per configuration."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.stage_6_5.pool_builder import PoolBuildConfig, build_runbook_pool

SOURCE_ROOTS = [
    REPO_ROOT / "operationalknowledgeingestion/data/output/manual_optisweep_om_v3",
    REPO_ROOT / "operationalknowledgeingestion/data/output/training_video_day1",
    REPO_ROOT / "incidenceknowledgeingestion/data/output/incidents/case_228086",
]

TUNING_OUTPUT_DIR = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_tuning"
EMBEDDINGS_SOURCE = REPO_ROOT / "shared_pipeline_stages/data/output/shared/stage_6_5_runbook_pool"
SUMMARY_PATH = REPO_ROOT / "shared_pipeline_stages/stage_6_5_markdown/tuning_results_summary.md"

EXPERIMENTS: list[tuple[str, PoolBuildConfig]] = [
    (
        "baseline_v0.7_l0.3",
        PoolBuildConfig(
            experiment_name="baseline_v0.7_l0.3",
            vector_weight=0.7,
            lexical_weight=0.3,
            min_merge_score=0.62,
            high_confidence_score=0.78,
        ),
    ),
    (
        "low_lexical_v0.85_l0.15",
        PoolBuildConfig(
            experiment_name="low_lexical_v0.85_l0.15",
            vector_weight=0.85,
            lexical_weight=0.15,
            min_merge_score=0.62,
            high_confidence_score=0.78,
        ),
    ),
    (
        "low_lexical_v0.9_l0.1",
        PoolBuildConfig(
            experiment_name="low_lexical_v0.9_l0.1",
            vector_weight=0.9,
            lexical_weight=0.1,
            min_merge_score=0.62,
            high_confidence_score=0.78,
        ),
    ),
    (
        "lower_threshold_min0.58",
        PoolBuildConfig(
            experiment_name="lower_threshold_min0.58",
            vector_weight=0.7,
            lexical_weight=0.3,
            min_merge_score=0.58,
            high_confidence_score=0.78,
        ),
    ),
]


def main() -> None:
    TUNING_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    baseline_dir: Path | None = None
    results: list[dict] = []

    for index, (name, config) in enumerate(EXPERIMENTS):
        reuse_from = EMBEDDINGS_SOURCE if index == 0 else baseline_dir
        run_config = replace(config, reuse_embeddings_from=reuse_from)
        print(f"\n=== Running {name} ===")
        if reuse_from:
            print(f"Reusing embeddings from: {reuse_from}")
        result = build_runbook_pool(
            source_roots=SOURCE_ROOTS,
            output_dir=TUNING_OUTPUT_DIR,
            config=run_config,
        )
        experiment_dir = TUNING_OUTPUT_DIR / name
        if index == 0:
            baseline_dir = experiment_dir
        report = json.loads((experiment_dir / "runbook_pool_report.json").read_text(encoding="utf-8"))
        clusters = json.loads((experiment_dir / "merge_clusters.json").read_text(encoding="utf-8"))
        cluster_titles = [_cluster_title(cluster, experiment_dir) for cluster in clusters]
        results.append(
            {
                "name": name,
                "dir": str(experiment_dir.relative_to(REPO_ROOT)).replace("\\", "/"),
                "runbook_count": result.runbook_count,
                "merge_cluster_count": result.merge_cluster_count,
                "pass_through_count": result.pass_through_count,
                "embeddings_generated": report.get("embeddings_generated", 0),
                "embeddings_cached": report.get("embeddings_cached", 0),
                "combined_max": _distribution_get(report, "combined_distribution", "max"),
                "cluster_titles": cluster_titles,
            }
        )
        print(f"  Runbooks: {result.runbook_count}")
        print(f"  Merge clusters: {result.merge_cluster_count}")
        print(f"  Embeddings cached: {report.get('embeddings_cached', 0)}")

    _write_summary(results)
    print(f"\nSummary written: {SUMMARY_PATH}")


def _cluster_title(cluster: dict, experiment_dir: Path) -> str:
    pool = json.loads((experiment_dir / "runbook_pool.json").read_text(encoding="utf-8"))
    titles = {entry["finalized_runbook_id"]: entry["title"] for entry in pool.get("entries", [])}
    member_titles = [titles.get(rid, rid) for rid in cluster.get("finalized_runbook_ids", [])]
    hint = cluster.get("merge_hint", "")
    score = cluster.get("similarity_score", 0)
    return f"{cluster.get('merge_cluster_id')} (score={score}, {hint}): " + "; ".join(member_titles[:3]) + (
        f" (+{len(member_titles) - 3} more)" if len(member_titles) > 3 else ""
    )


def _distribution_get(report: dict, key: str, field: str) -> str:
    value = report.get(key, {}).get(field)
    return str(value) if value is not None else "n/a"


def _write_summary(results: list[dict]) -> None:
    timestamp = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    lines = [
        "# Stage 6.5 Tuning Results Summary",
        "",
        f"Generated: {timestamp}",
        "",
        "See [weight_tuning_experiments.md](weight_tuning_experiments.md) for methodology.",
        "",
        "## Comparison",
        "",
        "| Experiment | Clusters | Pass-through | Combined max | Embeddings cached |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in results:
        lines.append(
            f"| `{row['name']}` | {row['merge_cluster_count']} | {row['pass_through_count']} "
            f"| {row['combined_max']} | {row['embeddings_cached']} |"
        )
    lines.extend(["", "## Cluster titles by experiment", ""])
    for row in results:
        lines.append(f"### `{row['name']}`")
        lines.append("")
        lines.append(f"Output: `{row['dir']}/`")
        lines.append("")
        if not row["cluster_titles"]:
            lines.append("_No merge clusters._")
        else:
            for title in row["cluster_titles"]:
                lines.append(f"- {title}")
        lines.append("")
    lines.extend(
        [
            "## Notes",
            "",
            "- Lexical Jaccard uses stopword-filtered tokens (not exact phrases).",
            "- Each experiment directory contains `merge_cluster_review.md` with full runbook descriptions and link explanations.",
            "- Lower lexical weight increases reliance on Azure embedding cosine similarity.",
            "",
        ]
    )
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
