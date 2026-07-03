from __future__ import annotations

from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.schemas import MergeCluster, RetrievalCard


def write_merge_cluster_review_markdown(
    output_path: str | Path,
    *,
    experiment_name: str,
    config: dict[str, Any],
    merge_clusters: list[MergeCluster],
    cards_by_id: dict[str, RetrievalCard],
    embedding_model: str,
    runbook_count: int,
    pass_through_count: int,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Stage 6.5 Merge Cluster Review — {experiment_name}",
        "",
        "## Run configuration",
        "",
        f"- Embedding model: `{embedding_model}`",
        f"- Runbooks indexed: {runbook_count}",
        f"- Merge clusters: {len(merge_clusters)}",
        f"- Pass-through runbooks: {pass_through_count}",
        "",
        "| Parameter | Value |",
        "| --- | --- |",
    ]
    for key, value in config.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## How pairs were scored",
            "",
            "```text",
            "combined = vector_weight * cosine + lexical_weight * jaccard",
            "if opposing_actions: combined *= opposing_action_penalty",
            "```",
            "",
            "Lexical (Jaccard) compares **stopword-filtered word tokens** from retrieval text — "
            "order-independent, not exact phrases. Stopwords (`the`, `and`, `for`, …) and "
            "single-character tokens are excluded; action synonyms are normalized "
            "(`verify`/`review`/`inspect` → `check`). See "
            "[Lexical similarity explained](../../stage_6_5_markdown/lexical_similarity_explained.md).",
            "",
        ]
    )
    if not merge_clusters:
        lines.append("No merge clusters were produced at this threshold and weight configuration.")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    for index, cluster in enumerate(merge_clusters, start=1):
        lines.extend(_cluster_section(index, cluster, cards_by_id, config))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _cluster_section(
    index: int,
    cluster: MergeCluster,
    cards_by_id: dict[str, RetrievalCard],
    config: dict[str, Any],
) -> list[str]:
    lines = [
        f"## Cluster {index}: `{cluster.merge_cluster_id}`",
        "",
        f"- **Merge hint:** `{cluster.merge_hint}`",
        f"- **Top combined score:** {cluster.similarity_score}",
        f"- **Source types:** {', '.join(cluster.source_types)}",
        f"- **Requires Stage 7 LLM:** {cluster.requires_stage_7_llm}",
        "",
        "### Why these runbooks were linked",
        "",
    ]
    for note in cluster.evidence_notes:
        lines.append(f"- {note}")
    lines.append("")
    lines.append(
        "Clustering uses **single-linkage**: if A matches B and B matches C above "
        f"`min_merge_score` ({config.get('min_merge_score', '?')}), all three can "
        "appear in one cluster even when A↔C is weaker."
    )
    lines.extend(["", "### Runbooks in this cluster", ""])
    for runbook_id in cluster.finalized_runbook_ids:
        card = cards_by_id.get(runbook_id)
        if card is None:
            lines.append(f"- `{runbook_id}` (card missing)")
            continue
        lines.extend(_runbook_block(card))
    lines.extend(["", "### Pairwise links inside this cluster", ""])
    if not cluster.pairwise_matches:
        lines.append("_No pairwise matches recorded._")
    else:
        lines.append("| Combined | Cosine | Jaccard | Runbook A | Runbook B | Notes |")
        lines.append("| ---: | ---: | ---: | --- | --- | --- |")
        for match in cluster.pairwise_matches:
            title_a = _short_title(cards_by_id.get(match.source_id))
            title_b = _short_title(cards_by_id.get(match.target_id))
            notes = []
            if match.opposing_actions_detected:
                notes.append("opposing actions")
            notes.extend(match.metadata_warnings or [])
            note_text = "; ".join(notes) if notes else ""
            lines.append(
                f"| {match.combined_score} | {match.cosine_score} | {match.jaccard_score} "
                f"| {title_a} | {title_b} | {note_text} |"
            )
            lines.append("")
            lines.append(
                f"Linked because combined **{match.combined_score}** = "
                f"{config.get('vector_weight', '?')}×{match.cosine_score} + "
                f"{config.get('lexical_weight', '?')}×{match.jaccard_score}"
                + (f", then ×{config.get('opposing_action_penalty')} opposing-action penalty" if match.opposing_actions_detected else "")
                + f" ≥ min_merge_score **{config.get('min_merge_score', '?')}**."
            )
            lines.append("")
    lines.append("---")
    lines.append("")
    return lines


def _runbook_block(card: RetrievalCard) -> list[str]:
    when_to_use = card.when_to_use.strip() or "_Not specified._"
    summary = card.summary.strip() or "_Not specified._"
    return [
        f"#### [{card.source_type}] {card.title}",
        "",
        f"- **Procedure ID:** `{card.finalized_runbook_id}`",
        f"- **Candidate ID:** `{card.candidate_id}`",
        f"- **Procedure type:** `{card.procedure_type or 'unknown'}`",
        f"- **Role:** `{card.role_required or 'unknown'}`",
        "",
        "**Summary:**",
        "",
        summary,
        "",
        "**When to use:**",
        "",
        when_to_use,
        "",
    ]


def _short_title(card: RetrievalCard | None) -> str:
    if card is None:
        return "?"
    title = card.title.replace("|", "/")
    return title[:48] + ("…" if len(title) > 48 else "")
