from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.embedder import (
    AzureOpenAIEmbedder,
    MockRunbookEmbedder,
    RunbookEmbedder,
    retrieval_text_hash,
)
from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_6_5.loader import load_finalized_runbooks
from shared_pipeline_stages.stage_6_5.merge_prep import build_merge_clusters_and_pass_through
from shared_pipeline_stages.stage_6_5.retrieval_card import build_retrieval_card
from shared_pipeline_stages.stage_6_5.retriever import InMemoryRunbookRetriever
from shared_pipeline_stages.stage_6_5.schemas import (
    MergeCluster,
    PassThroughRunbook,
    RetrievalCard,
    RetrievalIndexEntry,
    RunbookPoolEntry,
    RunbookPoolReport,
    RunbookPoolResult,
    RunbookSimilarityEntry,
)
from shared_pipeline_stages.stage_6_5.similarity import SimilarityConfig, score_distribution


STAGE6_5_DIR_NAME = "stage_6_5_runbook_pool"


@dataclass(frozen=True)
class PoolBuildConfig:
    min_merge_score: float = 0.62
    high_confidence_score: float = 0.78
    vector_weight: float = 0.7
    lexical_weight: float = 0.3
    opposing_action_penalty: float = 0.5
    top_k: int = 10
    skip_embed: bool = False
    use_mock_embedder: bool = False


def build_runbook_pool(
    source_roots: list[str | Path],
    output_dir: str | Path,
    *,
    config: PoolBuildConfig | None = None,
    embedder: RunbookEmbedder | None = None,
    generated_at: str | None = None,
) -> RunbookPoolResult:
    build_config = config or PoolBuildConfig()
    similarity_config = SimilarityConfig(
        vector_weight=build_config.vector_weight,
        lexical_weight=build_config.lexical_weight,
        opposing_action_penalty=build_config.opposing_action_penalty,
        min_merge_score=build_config.min_merge_score,
        high_confidence_score=build_config.high_confidence_score,
    )
    timestamp = generated_at or datetime.now(UTC).isoformat().replace("+00:00", "Z")
    output_path = Path(output_dir)
    if output_path.name != STAGE6_5_DIR_NAME:
        output_path = output_path / STAGE6_5_DIR_NAME
    output_path.mkdir(parents=True, exist_ok=True)

    runbooks, load_warnings = load_finalized_runbooks(source_roots)
    cards = [build_retrieval_card(runbook) for runbook in runbooks]
    index_path = output_path / "runbook_retrieval_index.json"
    existing_index = _load_existing_index(index_path)
    active_embedder = _resolve_embedder(build_config, embedder)
    vectors, embeddings_generated, embeddings_cached = _build_vectors(
        cards,
        active_embedder,
        existing_index,
        skip_embed=build_config.skip_embed,
    )

    retriever = InMemoryRunbookRetriever(cards, vectors, similarity_config)
    merge_clusters, pass_through, all_pairs, similarity_by_runbook = build_merge_clusters_and_pass_through(
        cards,
        retriever,
        similarity_config,
        top_k=build_config.top_k,
    )

    pool_entries = [_pool_entry(runbook) for runbook in runbooks]
    index_entries = _index_entries(cards, vectors, active_embedder.model_name)
    similarity_entries = [
        RunbookSimilarityEntry(
            finalized_runbook_id=runbook_id,
            top_cross_source_matches=matches,
        )
        for runbook_id, matches in sorted(similarity_by_runbook.items())
    ]
    report = _build_report(
        generated_at=timestamp,
        cards=cards,
        merge_clusters=merge_clusters,
        pass_through=pass_through,
        all_pairs=all_pairs,
        build_config=build_config,
        embedding_model=active_embedder.model_name,
        embeddings_generated=embeddings_generated,
        embeddings_cached=embeddings_cached,
        warnings=load_warnings,
    )
    result = RunbookPoolResult(
        generated_at=timestamp,
        runbook_count=len(cards),
        merge_cluster_count=len(merge_clusters),
        pass_through_count=len(pass_through),
    )

    write_json(output_path / "runbook_pool.json", {"entries": pool_entries, **result.model_dump()})
    write_json(output_path / "retrieval_cards.json", cards)
    write_json(output_path / "runbook_retrieval_index.json", index_entries)
    write_json(output_path / "runbook_similarity.json", similarity_entries)
    write_json(output_path / "merge_clusters.json", merge_clusters)
    write_json(output_path / "pass_through_runbooks.json", pass_through)
    write_json(output_path / "runbook_pool_report.json", report)
    return result


def _resolve_embedder(
    build_config: PoolBuildConfig,
    embedder: RunbookEmbedder | None,
) -> RunbookEmbedder:
    if embedder is not None:
        return embedder
    if build_config.use_mock_embedder or build_config.skip_embed:
        return MockRunbookEmbedder()
    return AzureOpenAIEmbedder()


def _build_vectors(
    cards: list[RetrievalCard],
    embedder: RunbookEmbedder,
    existing_index: dict[str, RetrievalIndexEntry],
    *,
    skip_embed: bool,
) -> tuple[dict[str, list[float]], int, int]:
    vectors: dict[str, list[float]] = {}
    to_embed: list[RetrievalCard] = []
    generated = 0
    cached = 0
    for card in cards:
        text_hash = retrieval_text_hash(card.retrieval_text)
        existing = existing_index.get(card.finalized_runbook_id)
        if (
            existing
            and existing.retrieval_text_hash == text_hash
            and existing.vector
            and existing.embedding_model == embedder.model_name
        ):
            vectors[card.finalized_runbook_id] = existing.vector
            cached += 1
        else:
            to_embed.append(card)
    if to_embed and not skip_embed:
        embedded = embedder.embed_texts([card.retrieval_text for card in to_embed])
        for card, vector in zip(to_embed, embedded):
            vectors[card.finalized_runbook_id] = vector
            generated += 1
    elif to_embed and skip_embed:
        mock = MockRunbookEmbedder()
        embedded = mock.embed_texts([card.retrieval_text for card in to_embed])
        for card, vector in zip(to_embed, embedded):
            vectors[card.finalized_runbook_id] = vector
            generated += 1
    return vectors, generated, cached


def _load_existing_index(path: Path) -> dict[str, RetrievalIndexEntry]:
    if not path.exists():
        return {}
    payload = read_json(path)
    entries: list[Any]
    if isinstance(payload, list):
        entries = payload
    elif isinstance(payload, dict):
        entries = payload.get("entries") or payload.get("index_entries") or []
    else:
        return {}
    result: dict[str, RetrievalIndexEntry] = {}
    for item in entries:
        if not isinstance(item, dict):
            continue
        entry = RetrievalIndexEntry.model_validate(item)
        result[entry.finalized_runbook_id] = entry
    return result


def _index_entries(
    cards: list[RetrievalCard],
    vectors: dict[str, list[float]],
    model_name: str,
) -> list[RetrievalIndexEntry]:
    entries: list[RetrievalIndexEntry] = []
    for card in cards:
        vector = vectors.get(card.finalized_runbook_id, [])
        entries.append(
            RetrievalIndexEntry(
                finalized_runbook_id=card.finalized_runbook_id,
                embedding_model=model_name,
                embedding_dimensions=len(vector),
                vector=vector,
                retrieval_text_hash=retrieval_text_hash(card.retrieval_text),
            )
        )
    return entries


def _pool_entry(runbook: dict[str, Any]) -> RunbookPoolEntry:
    metadata = runbook.get("metadata") or {}
    return RunbookPoolEntry(
        finalized_runbook_id=str(runbook.get("procedure_id") or ""),
        candidate_id=str(runbook.get("candidate_id") or ""),
        title=str(runbook.get("title") or ""),
        source_id=str(metadata.get("source_id") or ""),
        source_type=str(metadata.get("source_type") or ""),
        procedure_type=str(runbook.get("procedure_type") or ""),
        role_required=str(runbook.get("role_required") or runbook.get("responsible_role") or ""),
        validation_status=str(runbook.get("validation_status") or ""),
        source_path=str(runbook.get("_source_path") or ""),
        source_lineage=runbook.get("source_lineage") or [],
    )


def _build_report(
    *,
    generated_at: str,
    cards: list[RetrievalCard],
    merge_clusters: list[MergeCluster],
    pass_through: list[PassThroughRunbook],
    all_pairs: list[Any],
    build_config: PoolBuildConfig,
    embedding_model: str,
    embeddings_generated: int,
    embeddings_cached: int,
    warnings: list[str] | None = None,
) -> RunbookPoolReport:
    cosine_values = [match.cosine_score for match in all_pairs]
    jaccard_values = [match.jaccard_score for match in all_pairs]
    combined_values = [match.combined_score for match in all_pairs]
    return RunbookPoolReport(
        generated_at=generated_at,
        input_runbook_count=len(cards),
        merge_cluster_count=len(merge_clusters),
        pass_through_count=len(pass_through),
        embedding_model=embedding_model,
        embeddings_generated=embeddings_generated,
        embeddings_cached=embeddings_cached,
        config=asdict(build_config),
        cosine_distribution=score_distribution(cosine_values),
        jaccard_distribution=score_distribution(jaccard_values),
        combined_distribution=score_distribution(combined_values),
        top_cross_source_pairs=all_pairs[:20],
        warnings=warnings or [],
    )
