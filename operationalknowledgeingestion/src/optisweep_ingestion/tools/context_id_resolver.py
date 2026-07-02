"""Resolve operational context IDs across naming drift and extraction variants."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

CONTEXT_ID_RE = re.compile(r"^ctx_[a-z0-9_]+_v1$", re.IGNORECASE)


def normalize_context_slug(context_id: str) -> str:
    slug = str(context_id or "").strip().lower()
    slug = slug.removeprefix("ctx_").removesuffix("_v1")
    if slug.startswith("manual_"):
        slug = slug[7:]
    return re.sub(r"[^a-z0-9]+", "_", slug).strip("_")


def build_context_resolution_index(contexts: list[dict[str, Any]]) -> dict[str, Any]:
    by_id: dict[str, str] = {}
    by_slug: dict[str, str] = {}
    slug_entries: list[tuple[str, str]] = []
    for context in contexts:
        context_id = str(context.get("context_id") or "").strip()
        if not context_id:
            continue
        by_id[context_id] = context_id
        slug = normalize_context_slug(context_id)
        if slug and slug not in by_slug:
            by_slug[slug] = context_id
        slug_entries.append((slug, context_id))
    return {
        "by_id": by_id,
        "by_slug": by_slug,
        "slug_entries": slug_entries,
    }


def _slug_score(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    sequence_score = SequenceMatcher(None, left, right).ratio()
    left_tokens = set(left.split("_"))
    right_tokens = set(right.split("_"))
    token_score = 0.0
    if left_tokens and right_tokens:
        token_score = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
    if left in right or right in left:
        return max(sequence_score, token_score, 0.85)
    return max(sequence_score, token_score)


def resolve_context_id(
    context_id: str,
    index: dict[str, Any],
    *,
    min_score: float = 0.55,
) -> str | None:
    ref = str(context_id or "").strip()
    if not ref:
        return None
    by_id: dict[str, str] = index["by_id"]
    if ref in by_id:
        return ref

    slug = normalize_context_slug(ref)
    by_slug: dict[str, str] = index["by_slug"]
    if slug in by_slug:
        return by_slug[slug]

    manual_slug = f"manual_{slug}" if slug else ""
    if manual_slug in by_slug:
        return by_slug[manual_slug]

    best_id = ""
    best_score = 0.0
    for candidate_slug, candidate_id in index["slug_entries"]:
        score = _slug_score(slug, candidate_slug)
        if score > best_score:
            best_score = score
            best_id = candidate_id
    if best_score >= min_score:
        return best_id
    return None


def resolve_context_ids(
    context_ids: list[str],
    contexts: list[dict[str, Any]] | dict[str, dict[str, Any]],
    *,
    min_score: float = 0.55,
) -> tuple[list[str], list[str]]:
    if isinstance(contexts, dict):
        context_list = list(contexts.values())
    else:
        context_list = contexts
    index = build_context_resolution_index(context_list)
    resolved: list[str] = []
    notes: list[str] = []
    seen: set[str] = set()
    for context_id in context_ids:
        ref = str(context_id or "").strip()
        if not ref:
            continue
        target = resolve_context_id(ref, index, min_score=min_score)
        if not target:
            notes.append(f"Unresolved context id '{ref}'")
            continue
        if target != ref:
            notes.append(f"Resolved context id '{ref}' -> '{target}'")
        if target not in seen:
            seen.add(target)
            resolved.append(target)
    return resolved, notes


def resolve_candidate_context_ids(
    candidate: dict[str, Any],
    contexts: list[dict[str, Any]] | dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    updated = dict(candidate)
    resolved_ids, notes = resolve_context_ids(updated.get("related_context_ids") or [], contexts)
    updated["related_context_ids"] = resolved_ids
    return updated, notes
