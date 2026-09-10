"""Shared Stage 10 full-corpus embedding generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from shared_pipeline_stages.stage_6_5.embedder import MockRunbookEmbedder, RunbookEmbedder, retrieval_text_hash
from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_6_5.retrieval_card import build_retrieval_card
from shared_pipeline_stages.stage_10.rag_retrieval_text import (
    build_operational_context_retrieval_text,
    build_source_artifact_retrieval_text,
)
from shared_pipeline_stages.stage_10.schemas import EmbeddingRecord
from shared_pipeline_stages.stage_10.source_loader import load_source_roots_contexts_and_artifacts

STAGE10_DIR_NAME = "stage_10_embeddings"
STAGE8_VARIANTS = (
    ("prompt_a_one_per_incident", "playbook_prompt_a"),
    ("prompt_b_multi_flow", "playbook_prompt_b"),
)


@dataclass
class EmbeddingBuildResult:
    record_count: int
    runbook_record_count: int
    playbook_prompt_a_count: int
    playbook_prompt_b_count: int
    operational_context_count: int
    source_artifact_count: int
    embedding_model: str
    embedding_dimensions: int
    warnings: list[str] = field(default_factory=list)

    @property
    def playbook_record_count(self) -> int:
        return self.playbook_prompt_a_count + self.playbook_prompt_b_count


def generate_corpus_embeddings(
    *,
    stage7_dir: str | Path,
    stage8_dir: str | Path,
    output_dir: str | Path,
    source_roots: list[str | Path] | None = None,
    embedder: RunbookEmbedder | None = None,
    use_mock_embedder: bool = False,
) -> EmbeddingBuildResult:
    stage7_path = Path(stage7_dir)
    stage8_path = _resolve_stage8_dir(Path(stage8_dir))
    output_path = _resolve_output_path(Path(output_dir))
    output_path.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(UTC).isoformat()
    active_embedder = embedder or (MockRunbookEmbedder() if use_mock_embedder else _default_embedder())

    warnings: list[str] = []
    records: list[EmbeddingRecord] = []

    canonical_path = stage7_path / "canonical_runbooks.json"
    if not canonical_path.exists():
        raise FileNotFoundError(f"Stage 10 requires {canonical_path}")
    payload = read_json(canonical_path)
    runbooks = payload.get("runbooks") if isinstance(payload, dict) else payload
    if not isinstance(runbooks, list):
        raise ValueError(f"{canonical_path} must contain a runbooks list.")

    for runbook in runbooks:
        if not isinstance(runbook, dict):
            continue
        procedure_id = str(runbook.get("procedure_id") or "").strip()
        if not procedure_id:
            warnings.append("Skipping runbook without procedure_id.")
            continue
        card = build_retrieval_card(runbook)
        text = card.retrieval_text.strip()
        if not text:
            warnings.append(f"Skipping empty retrieval text for {procedure_id}.")
            continue
        vector = active_embedder.embed_texts([text])[0]
        metadata = runbook.get("metadata") or {}
        records.append(
            EmbeddingRecord(
                record_id=f"emb_runbook_{procedure_id}",
                record_type="canonical_runbook",
                source_record_id=procedure_id,
                source_type=str(metadata.get("source_type") or ""),
                embedded_text=text,
                vector=vector,
                embedding_model=active_embedder.model_name,
                embedding_dimensions=len(vector),
                retrieval_text_hash=retrieval_text_hash(text),
                filter_metadata={
                    "procedure_id": procedure_id,
                    "procedure_type": str(runbook.get("procedure_type") or ""),
                    "source_id": str(metadata.get("source_id") or ""),
                    "validation_status": str(runbook.get("validation_status") or ""),
                },
                source_refs=runbook.get("source_refs") or [],
            )
        )

    playbook_prompt_a_count = 0
    playbook_prompt_b_count = 0
    for variant, record_type in STAGE8_VARIANTS:
        cards_path = stage8_path / variant / "playbook_retrieval_cards.json"
        if not cards_path.exists():
            warnings.append(f"Missing playbook retrieval cards: {cards_path}")
            continue
        cards_payload = read_json(cards_path)
        cards = cards_payload.get("cards") if isinstance(cards_payload, dict) else cards_payload
        if not isinstance(cards, list):
            warnings.append(f"{cards_path} must contain a cards list.")
            continue
        for card in cards:
            if not isinstance(card, dict):
                continue
            playbook_id = str(card.get("playbook_id") or "").strip()
            text = str(card.get("retrieval_text") or "").strip()
            if not playbook_id or not text:
                warnings.append("Skipping playbook card missing playbook_id or retrieval_text.")
                continue
            vector = active_embedder.embed_texts([text])[0]
            records.append(
                EmbeddingRecord(
                    record_id=f"emb_{record_type}_{playbook_id}",
                    record_type=record_type,
                    source_record_id=playbook_id,
                    source_type="incident",
                    embedded_text=text,
                    vector=vector,
                    embedding_model=active_embedder.model_name,
                    embedding_dimensions=len(vector),
                    retrieval_text_hash=retrieval_text_hash(text),
                    filter_metadata={
                        "playbook_id": playbook_id,
                        "case_id": str(card.get("case_id") or ""),
                        "extraction_mode": str(card.get("extraction_mode") or variant),
                        "validation_status": str(card.get("validation_status") or ""),
                    },
                    source_refs=[{"playbook_candidate_id": card.get("playbook_candidate_id")}],
                )
            )
            if record_type == "playbook_prompt_a":
                playbook_prompt_a_count += 1
            else:
                playbook_prompt_b_count += 1

    operational_context_count = 0
    source_artifact_count = 0
    if not source_roots:
        warnings.append(
            "No --source-root provided; operational_context and source_artifact embeddings will be skipped."
        )
    else:
        contexts, artifacts, load_warnings = load_source_roots_contexts_and_artifacts(source_roots)
        warnings.extend(load_warnings)
        if not contexts:
            warnings.append(
                "Source roots provided but no operational_context records were loaded "
                "(expected stage_4_operational_context/operational_context.json)."
            )
        if not artifacts:
            warnings.append(
                "Source roots provided but no source_artifact records were loaded "
                "(expected stage_2/stage_3 source_artifacts*.json)."
            )
        for context in contexts:
            context_id = str(context.get("context_id") or "").strip()
            text = build_operational_context_retrieval_text(context)
            summary = str(context.get("summary") or "").strip()
            if not context_id or not text:
                continue
            vector = active_embedder.embed_texts([text])[0]
            records.append(
                EmbeddingRecord(
                    record_id=f"emb_ctx_{context_id}",
                    record_type="operational_context",
                    source_record_id=context_id,
                    source_type=str(context.get("source_type") or ""),
                    embedded_text=text,
                    vector=vector,
                    embedding_model=active_embedder.model_name,
                    embedding_dimensions=len(vector),
                    retrieval_text_hash=retrieval_text_hash(text),
                    filter_metadata={
                        "context_id": context_id,
                        "context_type": str(context.get("context_type") or ""),
                        "source_id": str(context.get("source_id") or ""),
                        "summary": summary,
                        "validation_status": str(context.get("validation_status") or ""),
                    },
                    source_refs=context.get("source_refs") or [],
                )
            )
            operational_context_count += 1

        for artifact in artifacts:
            artifact_id = str(artifact.get("artifact_id") or "").strip()
            text = build_source_artifact_retrieval_text(artifact)
            summary = str(artifact.get("summary") or "").strip()
            if not artifact_id or not text:
                continue
            vector = active_embedder.embed_texts([text])[0]
            records.append(
                EmbeddingRecord(
                    record_id=f"emb_artifact_{artifact_id}",
                    record_type="source_artifact",
                    source_record_id=artifact_id,
                    source_type=str(artifact.get("source_type") or ""),
                    embedded_text=text,
                    vector=vector,
                    embedding_model=active_embedder.model_name,
                    embedding_dimensions=len(vector),
                    retrieval_text_hash=retrieval_text_hash(text),
                    filter_metadata={
                        "artifact_id": artifact_id,
                        "artifact_type": str(artifact.get("artifact_type") or ""),
                        "source_id": str(artifact.get("source_id") or ""),
                        "summary": summary,
                        "storage_path": str(artifact.get("storage_path") or ""),
                    },
                    source_refs=artifact.get("source_refs") or [],
                )
            )
            source_artifact_count += 1

    grouped = _group_records(records)
    write_json(output_path / "embedding_records.json", [record.model_dump(mode="json") for record in records])
    for name, rows in grouped.items():
        write_json(output_path / f"embedding_records_{name}.json", rows)

    dimensions = records[0].embedding_dimensions if records else 0
    report = {
        "stage": "10",
        "stage_name": "embedding_generation",
        "generated_at": generated_at,
        "embedding_model": active_embedder.model_name,
        "embedding_dimensions": dimensions,
        "record_counts": {
            "total": len(records),
            "canonical_runbook": sum(1 for record in records if record.record_type == "canonical_runbook"),
            "playbook_prompt_a": playbook_prompt_a_count,
            "playbook_prompt_b": playbook_prompt_b_count,
            "operational_context": operational_context_count,
            "source_artifact": source_artifact_count,
        },
        "inputs": {
            "stage7_dir": str(stage7_path),
            "stage8_dir": str(stage8_path),
            "source_roots": [str(Path(root)) for root in source_roots or []],
        },
        "warnings": warnings,
        "outputs": {
            "embedding_records": str(output_path / "embedding_records.json"),
        },
    }
    write_json(output_path / "embedding_generation_report.json", report)
    return EmbeddingBuildResult(
        record_count=len(records),
        runbook_record_count=sum(1 for record in records if record.record_type == "canonical_runbook"),
        playbook_prompt_a_count=playbook_prompt_a_count,
        playbook_prompt_b_count=playbook_prompt_b_count,
        operational_context_count=operational_context_count,
        source_artifact_count=source_artifact_count,
        embedding_model=active_embedder.model_name,
        embedding_dimensions=dimensions,
        warnings=warnings,
    )


def _group_records(records: list[EmbeddingRecord]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {
        "canonical_runbooks": [],
        "playbooks_prompt_a": [],
        "playbooks_prompt_b": [],
        "operational_context": [],
        "source_artifacts": [],
    }
    mapping = {
        "canonical_runbook": "canonical_runbooks",
        "playbook_prompt_a": "playbooks_prompt_a",
        "playbook_prompt_b": "playbooks_prompt_b",
        "operational_context": "operational_context",
        "source_artifact": "source_artifacts",
    }
    for record in records:
        key = mapping.get(record.record_type)
        if key:
            grouped[key].append(record.model_dump(mode="json"))
    return grouped


def _default_embedder() -> RunbookEmbedder:
    from shared_pipeline_stages.stage_6_5.embedder import AzureOpenAIEmbedder

    return AzureOpenAIEmbedder()


def _resolve_stage8_dir(stage8_dir: Path) -> Path:
    if stage8_dir.name == "stage_8_finalized_playbooks":
        return stage8_dir
    nested = stage8_dir / "stage_8_finalized_playbooks"
    return nested if nested.exists() else stage8_dir


def _resolve_output_path(output_dir: Path) -> Path:
    if output_dir.name == STAGE10_DIR_NAME:
        return output_dir
    return output_dir / STAGE10_DIR_NAME
