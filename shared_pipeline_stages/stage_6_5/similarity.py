from __future__ import annotations

import re
from dataclasses import dataclass

from shared_pipeline_stages.stage_6_5.schemas import PairwiseMatch, RetrievalCard, ScoreDistribution

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "use",
    "using",
    "with",
}

ACTION_EQUIVALENTS = {
    "check": "check",
    "verify": "check",
    "review": "check",
    "inspect": "check",
    "start": "start",
    "starting": "start",
    "stop": "stop",
    "stopping": "stop",
    "shutdown": "stop",
    "add": "add",
    "remove": "remove",
}

OPPOSING_ACTIONS = {
    frozenset({"start", "stop"}),
    frozenset({"add", "remove"}),
}


@dataclass(frozen=True)
class SimilarityConfig:
    vector_weight: float = 0.7
    lexical_weight: float = 0.3
    opposing_action_penalty: float = 0.5
    min_merge_score: float = 0.62
    high_confidence_score: float = 0.78


def cosine_similarity(first: list[float], second: list[float]) -> float:
    if not first or not second or len(first) != len(second):
        return 0.0
    dot = sum(a * b for a, b in zip(first, second))
    norm_a = sum(a * a for a in first) ** 0.5
    norm_b = sum(b * b for b in second) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def token_jaccard(first_text: str, second_text: str) -> float:
    first_tokens = _meaningful_tokens(first_text)
    second_tokens = _meaningful_tokens(second_text)
    if not first_tokens or not second_tokens:
        return 0.0
    return len(first_tokens & second_tokens) / len(first_tokens | second_tokens)


def detect_opposing_actions(first: RetrievalCard, second: RetrievalCard) -> bool:
    first_actions = _primary_actions(first)
    second_actions = _primary_actions(second)
    if not first_actions or not second_actions:
        return False
    for left in first_actions:
        for right in second_actions:
            if frozenset({left, right}) in OPPOSING_ACTIONS:
                return True
    return False


def metadata_warnings(first: RetrievalCard, second: RetrievalCard) -> list[str]:
    warnings: list[str] = []
    if first.procedure_type and second.procedure_type and first.procedure_type != second.procedure_type:
        warnings.append(
            f"procedure_type mismatch: {first.procedure_type} vs {second.procedure_type}"
        )
    if first.role_required and second.role_required and first.role_required != second.role_required:
        warnings.append(f"role_required mismatch: {first.role_required} vs {second.role_required}")
    if first.source_type == second.source_type:
        warnings.append(f"same source_type: {first.source_type}")
    return warnings


def score_pair(
    first: RetrievalCard,
    second: RetrievalCard,
    first_vector: list[float],
    second_vector: list[float],
    config: SimilarityConfig,
) -> PairwiseMatch:
    cosine = cosine_similarity(first_vector, second_vector)
    jaccard = token_jaccard(first.retrieval_text, second.retrieval_text)
    combined = config.vector_weight * cosine + config.lexical_weight * jaccard
    opposing = detect_opposing_actions(first, second)
    if opposing:
        combined *= config.opposing_action_penalty
    return PairwiseMatch(
        source_id=first.finalized_runbook_id,
        target_id=second.finalized_runbook_id,
        cosine_score=round(cosine, 4),
        jaccard_score=round(jaccard, 4),
        combined_score=round(combined, 4),
        opposing_actions_detected=opposing,
        metadata_warnings=metadata_warnings(first, second),
    )


def merge_hint_for_score(score: float, config: SimilarityConfig) -> str | None:
    if score >= config.high_confidence_score:
        return "likely_same_procedure"
    if score >= config.min_merge_score:
        return "needs_review"
    return None


def score_distribution(values: list[float]) -> ScoreDistribution:
    if not values:
        return ScoreDistribution()
    ordered = sorted(values)
    count = len(ordered)
    midpoint = ordered[count // 2]
    p95_index = min(count - 1, int(count * 0.95))
    return ScoreDistribution(
        count=count,
        min=round(ordered[0], 4),
        max=round(ordered[-1], 4),
        mean=round(sum(ordered) / count, 4),
        p50=round(midpoint, 4),
        p95=round(ordered[p95_index], 4),
    )


def _primary_actions(card: RetrievalCard) -> set[str]:
    actions: set[str] = set()
    for verb in card.action_verbs:
        normalized = ACTION_EQUIVALENTS.get(verb.lower(), verb.lower())
        actions.add(normalized)
    for token in _tokens(card.title):
        normalized = ACTION_EQUIVALENTS.get(token)
        if normalized:
            actions.add(normalized)
    return actions


def _meaningful_tokens(value: str) -> set[str]:
    return {
        ACTION_EQUIVALENTS.get(token, token)
        for token in _tokens(value)
        if token not in STOPWORDS and len(token) > 1
    }


def _tokens(value: str) -> list[str]:
    value = value.lower().replace("_", " ")
    return re.findall(r"[a-z0-9]+", value)
