from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a", "an", "and", "for", "in", "of", "on", "the", "to", "use", "using", "with",
}


@dataclass(frozen=True)
class RetrievalConfig:
    vector_weight: float = 0.7
    lexical_weight: float = 0.3
    playbook_match_threshold: float = 0.55
    playbook_high_confidence_threshold: float = 0.75


@dataclass
class RetrievalHit:
    record_id: str
    record_type: str
    source_record_id: str
    title: str
    combined_score: float
    cosine_score: float
    jaccard_score: float
    filter_metadata: dict[str, Any]
    symptom_score: float = 0.0
    coverage: float = 0.0


def tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {token for token in tokens if token not in STOPWORDS and len(token) > 1}


def token_jaccard(first_text: str, second_text: str) -> float:
    first_tokens = tokenize(first_text)
    second_tokens = tokenize(second_text)
    if not first_tokens or not second_tokens:
        return 0.0
    return len(first_tokens & second_tokens) / len(first_tokens | second_tokens)


def cosine_similarity(first: list[float], second: list[float]) -> float:
    if not first or not second or len(first) != len(second):
        return 0.0
    dot = sum(a * b for a, b in zip(first, second))
    norm_a = math.sqrt(sum(a * a for a in first))
    norm_b = math.sqrt(sum(b * b for b in second))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def mock_embed(text: str, dimensions: int = 64) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [(digest[index % len(digest)] / 127.5) - 1.0 for index in range(dimensions)]
    norm = math.sqrt(sum(value * value for value in values)) or 1.0
    return [value / norm for value in values]


def entry_phrase_coverage(query_text: str, symptoms: list[str], examples: list[str] | None = None) -> float:
    query_tokens = tokenize(query_text)
    phrases = [str(p) for p in [*symptoms, *(examples or [])] if str(p).strip()]
    if not query_tokens or not phrases:
        return 0.0
    matched = 0
    for phrase in phrases:
        phrase_tokens = tokenize(phrase)
        if phrase_tokens and query_tokens & phrase_tokens:
            matched += 1
    return matched / len(phrases)


def symptom_overlap_score(query_text: str, symptoms: list[str], examples: list[str] | None = None) -> float:
    """Best phrase Jaccard dampened by entry-phrase coverage.

    A single exact phrase match must score high but not 1.0. Broader coverage of
    observed_entry_symptoms + support_user_language_examples raises the score.
    """
    query_tokens = tokenize(query_text)
    if not query_tokens:
        return 0.0
    phrases = [str(p) for p in [*symptoms, *(examples or [])] if str(p).strip()]
    if not phrases:
        return 0.0
    best = 0.0
    for phrase in phrases:
        phrase_tokens = tokenize(phrase)
        if not phrase_tokens:
            continue
        overlap = len(query_tokens & phrase_tokens) / len(query_tokens | phrase_tokens)
        best = max(best, overlap)
    coverage = entry_phrase_coverage(query_text, symptoms, examples)
    return 0.70 * best + 0.30 * coverage


class LocalHybridRetriever:
    def __init__(
        self,
        embedding_records: list[dict[str, Any]],
        config: RetrievalConfig | None = None,
        symptom_cards: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.records = embedding_records
        self.config = config or RetrievalConfig()
        self.symptom_cards = symptom_cards or {}

    @classmethod
    def from_corpus_dir(cls, corpus_dir: str | Path, config: RetrievalConfig | None = None) -> LocalHybridRetriever:
        root = Path(corpus_dir)
        path = root / "embeddings" / "local_embedding_records.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        symptom_cards: dict[str, dict[str, Any]] = {}
        for variant in ("prompt_a", "prompt_b"):
            cards_path = root / "playbooks" / variant / "playbook_retrieval_cards.json"
            if not cards_path.exists():
                continue
            cards_payload = json.loads(cards_path.read_text(encoding="utf-8"))
            for card in cards_payload.get("cards", []):
                playbook_id = str(card.get("playbook_id") or "")
                if playbook_id:
                    symptom_cards[playbook_id] = card
        return cls(payload.get("records", []), config=config, symptom_cards=symptom_cards)

    def _score_record(self, query_text: str, query_vector: list[float], record: dict[str, Any]) -> RetrievalHit:
        embedded_text = str(record.get("embedded_text") or "")
        vector = list(record.get("vector") or [])
        cosine = cosine_similarity(query_vector, vector) if query_vector else 0.0
        jaccard = token_jaccard(query_text, embedded_text)
        combined = self.config.vector_weight * cosine + self.config.lexical_weight * jaccard
        metadata = record.get("filter_metadata") or {}
        record_type = str(record.get("record_type") or "")
        source_record_id = str(record.get("source_record_id") or "")
        symptom_score = 0.0
        coverage = 0.0
        if record_type.startswith("playbook_"):
            card = self.symptom_cards.get(source_record_id, {})
            symptoms = list(card.get("observed_entry_symptoms") or [])
            examples = list(card.get("support_user_language_examples") or [])
            symptom_score = symptom_overlap_score(query_text, symptoms, examples)
            coverage = entry_phrase_coverage(query_text, symptoms, examples)
            combined = max(combined, symptom_score)
        return RetrievalHit(
            record_id=str(record.get("record_id") or ""),
            record_type=record_type,
            source_record_id=source_record_id,
            title=str(metadata.get("title") or ""),
            combined_score=round(combined, 4),
            cosine_score=round(cosine, 4),
            jaccard_score=round(jaccard, 4),
            filter_metadata=metadata,
            symptom_score=round(symptom_score, 4),
            coverage=round(coverage, 4),
        )

    def search(
        self,
        query_text: str,
        *,
        query_vector: list[float] | None = None,
        record_types: set[str] | None = None,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> list[RetrievalHit]:
        vector = query_vector if query_vector is not None else mock_embed(query_text)
        hits: list[RetrievalHit] = []
        for record in self.records:
            record_type = str(record.get("record_type") or "")
            if record_types and record_type not in record_types:
                continue
            hit = self._score_record(query_text, vector, record)
            if hit.combined_score >= min_score:
                hits.append(hit)
        hits.sort(key=lambda item: (-item.combined_score, item.source_record_id))
        return hits[:top_k]

    def search_playbooks(
        self,
        query_text: str,
        *,
        variant: str = "prompt_a",
        query_vector: list[float] | None = None,
        top_k: int = 3,
    ) -> list[RetrievalHit]:
        record_type = "playbook_prompt_a" if variant == "prompt_a" else "playbook_prompt_b"
        return self.search(
            query_text,
            query_vector=query_vector,
            record_types={record_type},
            top_k=top_k,
            min_score=0.0,
        )

    def search_runbooks(
        self,
        query_text: str,
        *,
        query_vector: list[float] | None = None,
        top_k: int = 5,
    ) -> list[RetrievalHit]:
        return self.search(
            query_text,
            query_vector=query_vector,
            record_types={"canonical_runbook", "incident_source_runbook"},
            top_k=top_k,
        )


def resolve_runbook_for_node(
    playbook_id: str,
    node_id: str,
    playbook_runbook_links: list[dict[str, Any]],
) -> str | None:
    matches = [
        link
        for link in playbook_runbook_links
        if link.get("playbook_id") == playbook_id and link.get("node_id") == node_id
    ]
    if not matches:
        return None
    matches.sort(key=lambda link: int(link.get("link_rank") or 999))
    return str(matches[0].get("procedure_id") or "") or None
