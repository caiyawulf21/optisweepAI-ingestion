from __future__ import annotations

import re
from typing import Any

from shared_pipeline_stages.stage_6_5.embedder import retrieval_text_hash
from shared_pipeline_stages.stage_8.schemas import (
    NodeRetrievalSummary,
    PlaybookRetrievalCard,
    PlaybookRetrievalIndexEntry,
)

MAX_RETRIEVAL_TEXT_CHARS = 12000

PROMPT_VARIANT_DIRS = {
    "prompt_a_one_per_incident": "one_playbook_candidate_per_incident",
    "prompt_b_multi_flow": "one_or_more_playbook_candidates_when_separable",
}


def extraction_mode_for_variant(variant_dir: str) -> str:
    return PROMPT_VARIANT_DIRS.get(variant_dir, variant_dir)


def playbook_id_from_candidate(candidate: dict[str, Any], case_id: str) -> str:
    candidate_id = str(candidate.get("playbook_candidate_id") or "").strip()
    if candidate_id:
        return candidate_id.replace("playbook_candidate_", "playbook_")
    return f"playbook_incident_{case_id}"


def build_node_retrieval_summary(node: dict[str, Any]) -> NodeRetrievalSummary:
    summary = NodeRetrievalSummary(
        node_id=str(node.get("node_id") or "").strip(),
        node_type=str(node.get("node_type") or "").strip(),
        title=str(node.get("title") or "").strip(),
        intent=str(node.get("intent") or node.get("goal") or "").strip(),
        runbook_placeholder=str(node.get("runbook_placeholder") or node.get("needed_runbook_capability") or "").strip(),
        expected_or_observed_result=str(node.get("expected_or_observed_result") or "").strip(),
        allowed_roles=[str(role) for role in node.get("allowed_roles") or [] if str(role).strip()],
    )
    summary.retrieval_text = build_node_retrieval_text(summary)
    return summary


def build_node_retrieval_text(summary: NodeRetrievalSummary) -> str:
    parts = [
        summary.node_type,
        summary.title,
        summary.intent,
        summary.runbook_placeholder,
        summary.expected_or_observed_result,
        " ".join(summary.allowed_roles),
    ]
    return _compact_text(parts)


def build_playbook_retrieval_card(
    candidate: dict[str, Any],
    *,
    case_id: str,
    extraction_mode: str,
) -> PlaybookRetrievalCard:
    playbook_id = playbook_id_from_candidate(candidate, case_id)
    node_summaries = [
        build_node_retrieval_summary(node)
        for node in candidate.get("nodes") or []
        if isinstance(node, dict)
    ]
    card = PlaybookRetrievalCard(
        playbook_id=playbook_id,
        playbook_candidate_id=str(candidate.get("playbook_candidate_id") or "").strip(),
        case_id=case_id,
        extraction_mode=extraction_mode,
        title=str(candidate.get("title") or "").strip(),
        user_facing_summary=str(candidate.get("user_facing_summary") or candidate.get("summary") or "").strip(),
        observed_entry_symptoms=[str(item) for item in candidate.get("observed_entry_symptoms") or [] if str(item).strip()],
        support_user_language_examples=[
            str(item) for item in candidate.get("support_user_language_examples") or [] if str(item).strip()
        ],
        affected_systems_or_components=[
            str(item) for item in candidate.get("affected_systems_or_components") or [] if str(item).strip()
        ],
        node_retrieval_summaries=node_summaries,
    )
    card.retrieval_text = build_playbook_retrieval_text(card)
    return card


def build_playbook_retrieval_text(card: PlaybookRetrievalCard) -> str:
    parts = [
        card.title,
        card.user_facing_summary,
        " ".join(card.observed_entry_symptoms),
        " ".join(card.support_user_language_examples),
        " ".join(card.affected_systems_or_components),
    ]
    return _compact_text(parts)


def build_playbook_retrieval_index(
    cards: list[PlaybookRetrievalCard],
    *,
    embedder,
) -> tuple[list[PlaybookRetrievalIndexEntry], str]:
    texts: list[str] = []
    specs: list[tuple[str, str, str, str]] = []
    for card in cards:
        texts.append(card.retrieval_text)
        specs.append(("playbook", card.playbook_id, card.playbook_id, ""))
        for node in card.node_retrieval_summaries:
            texts.append(node.retrieval_text)
            specs.append(("node", f"{card.playbook_id}::{node.node_id}", card.playbook_id, node.node_id))
    vectors = embedder.embed_texts(texts) if texts else []
    entries: list[PlaybookRetrievalIndexEntry] = []
    for (entry_kind, entry_id, playbook_id, node_id), text, vector in zip(specs, texts, vectors, strict=True):
        entries.append(
            PlaybookRetrievalIndexEntry(
                entry_id=entry_id,
                entry_kind=entry_kind,
                playbook_id=playbook_id,
                node_id=node_id,
                embedding_model=embedder.model_name,
                embedding_dimensions=len(vector),
                vector=vector,
                retrieval_text_hash=retrieval_text_hash(text),
            )
        )
    return entries, embedder.model_name


def _compact_text(parts: list[str]) -> str:
    text = " ".join(part.strip() for part in parts if part and part.strip())
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > MAX_RETRIEVAL_TEXT_CHARS:
        return text[:MAX_RETRIEVAL_TEXT_CHARS]
    return text
