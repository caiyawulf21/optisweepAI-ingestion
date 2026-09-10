"""Cross-case semantic duplicate detection for finalized playbooks.

Cosmos upsert + deterministic playbook_id (derived from case_id) already
prevent exact-ID duplicates on republish. This module catches the remaining
gap: two different case_ids whose playbooks describe the same underlying
failure mode, which would otherwise publish as two unrelated documents.

This is advisory only. Different case_id values are different source
incidents by definition, so a high similarity score is a "flag for SME
review" signal, not proof of a duplicate to auto-merge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app_handoff_package.retrieval.local_hybrid_retriever import (
    cosine_similarity,
    token_jaccard,
)

DUPLICATE_SCORE_THRESHOLD = 0.75
VECTOR_WEIGHT = 0.7
LEXICAL_WEIGHT = 0.3


@dataclass
class DuplicateCandidatePair:
    playbook_id_a: str
    case_id_a: str
    title_a: str
    playbook_id_b: str
    case_id_b: str
    title_b: str
    cosine: float
    jaccard: float
    combined: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "playbook_id_a": self.playbook_id_a,
            "case_id_a": self.case_id_a,
            "title_a": self.title_a,
            "playbook_id_b": self.playbook_id_b,
            "case_id_b": self.case_id_b,
            "title_b": self.title_b,
            "cosine": round(self.cosine, 4),
            "jaccard": round(self.jaccard, 4),
            "combined": round(self.combined, 4),
        }


@dataclass
class DuplicateCheckResult:
    checked_count: int
    flagged_pairs: list[DuplicateCandidatePair] = field(default_factory=list)

    @property
    def has_flags(self) -> bool:
        return bool(self.flagged_pairs)

    def to_dict(self) -> dict[str, Any]:
        return {
            "checked_count": self.checked_count,
            "flagged_pair_count": len(self.flagged_pairs),
            "threshold": DUPLICATE_SCORE_THRESHOLD,
            "flagged_pairs": [pair.to_dict() for pair in self.flagged_pairs],
        }

    def warnings(self) -> list[str]:
        return [
            (
                f"Possible duplicate playbooks: {pair.playbook_id_a} (case {pair.case_id_a}) "
                f"and {pair.playbook_id_b} (case {pair.case_id_b}) score {pair.combined:.2f} "
                f"on title/entry-symptom similarity (threshold {DUPLICATE_SCORE_THRESHOLD}). "
                "Different case_id values are distinct source incidents — review before "
                "publish; if confirmed, mark the superseded one with superseded_by_playbook_id "
                "rather than deleting it."
            )
            for pair in self.flagged_pairs
        ]


def _entry_text(payload: dict[str, Any]) -> str:
    """Same field contract as the playbook embedding text (retrieval/ALGORITHMS.md):
    title + observed_entry_symptoms + support_user_language_examples only."""
    parts = [str(payload.get("title") or "")]
    parts.extend(str(item) for item in payload.get("observed_entry_symptoms") or [] if str(item).strip())
    parts.extend(
        str(item) for item in payload.get("support_user_language_examples") or [] if str(item).strip()
    )
    return "\n".join(part for part in parts if part.strip())


def check_playbook_duplicates(
    playbooks: list[dict[str, Any]],
    *,
    embeddings_by_playbook_id: dict[str, list[float]] | None = None,
    threshold: float = DUPLICATE_SCORE_THRESHOLD,
) -> DuplicateCheckResult:
    """Flag playbook pairs from different case_ids with high title/entry-symptom similarity.

    playbooks: list of playbook payload dicts (payload.playbook_id, payload.case_id,
        payload.title, payload.observed_entry_symptoms, payload.support_user_language_examples).
    embeddings_by_playbook_id: optional playbook_id -> vector map (same vectors already
        computed for the playbook embedding docs) to include cosine similarity. When
        omitted, comparison falls back to lexical (jaccard) similarity only.
    """
    entries: list[dict[str, Any]] = []
    for payload in playbooks:
        playbook_id = str(payload.get("playbook_id") or "").strip()
        case_id = str(payload.get("case_id") or "").strip()
        if not playbook_id:
            continue
        entries.append(
            {
                "playbook_id": playbook_id,
                "case_id": case_id,
                "title": str(payload.get("title") or ""),
                "text": _entry_text(payload),
                "vector": (embeddings_by_playbook_id or {}).get(playbook_id) or [],
            }
        )

    flagged: list[DuplicateCandidatePair] = []
    checked = 0
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            a, b = entries[i], entries[j]
            if not a["case_id"] or not b["case_id"] or a["case_id"] == b["case_id"]:
                # Same case_id (or missing) is a rerun of the same incident, not a
                # cross-incident duplicate — Cosmos upsert already collapses that.
                continue
            checked += 1
            jaccard = token_jaccard(a["text"], b["text"])
            cosine = cosine_similarity(a["vector"], b["vector"]) if a["vector"] and b["vector"] else 0.0
            combined = (
                VECTOR_WEIGHT * cosine + LEXICAL_WEIGHT * jaccard
                if a["vector"] and b["vector"]
                else jaccard
            )
            if combined >= threshold:
                flagged.append(
                    DuplicateCandidatePair(
                        playbook_id_a=a["playbook_id"],
                        case_id_a=a["case_id"],
                        title_a=a["title"],
                        playbook_id_b=b["playbook_id"],
                        case_id_b=b["case_id"],
                        title_b=b["title"],
                        cosine=cosine,
                        jaccard=jaccard,
                        combined=combined,
                    )
                )

    flagged.sort(key=lambda pair: -pair.combined)
    return DuplicateCheckResult(checked_count=checked, flagged_pairs=flagged)
