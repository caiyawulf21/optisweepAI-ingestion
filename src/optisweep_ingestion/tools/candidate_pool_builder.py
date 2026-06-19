"""Stage 6 deterministic candidate pool builder."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from optisweep_ingestion.schemas.candidate_pool import CandidateCluster, CandidatePacket, CandidatePool
from optisweep_ingestion.utils.json_utils import read_json, write_json

MIN_GROUP_SIMILARITY = 0.62
HIGH_CONFIDENCE_SIMILARITY = 0.78

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
    "diagnose": "check",
    "diagnostic": "check",
    "start": "start",
    "starting": "start",
    "stop": "stop",
    "stopping": "stop",
    "shutdown": "stop",
    "shut": "stop",
    "recover": "recover",
    "recovery": "recover",
    "reset": "recover",
    "initialize": "initialize",
    "initialise": "initialize",
    "add": "add",
    "remove": "remove",
}

OPPOSING_ACTIONS = {
    ("start", "stop"),
    ("add", "remove"),
}


def build_candidate_pool(
    candidate_paths: list[str | Path],
    output_dir: str | Path,
    generated_at: str | None = None,
) -> CandidatePool:
    """Build and write candidate_pool.json from one or more candidate JSON files."""
    candidates = load_candidates(candidate_paths)
    clusters = cluster_candidates(candidates)
    pool = CandidatePool(
        generated_at=generated_at or datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        candidate_cluster_count=len(clusters),
        candidate_clusters=clusters,
    )
    write_json(Path(output_dir) / "candidate_pool.json", pool)
    return pool


def load_candidates(candidate_paths: list[str | Path]) -> list[dict[str, Any]]:
    """Load candidate records from arrays or wrapper objects containing candidates."""
    candidates: list[dict[str, Any]] = []
    for path in candidate_paths:
        payload = read_json(path)
        records = _candidate_records_from_payload(payload)
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f"Candidate file contains a non-object record: {path}")
            candidates.append(record)
    return candidates


def cluster_candidates(candidates: list[dict[str, Any]]) -> list[CandidateCluster]:
    """Group source-specific candidates into conservative candidate clusters."""
    sorted_candidates = sorted(
        candidates,
        key=lambda item: (
            _normalized_title(str(item.get("title") or "")),
            str(item.get("candidate_id") or ""),
        ),
    )
    working_clusters: list[list[dict[str, Any]]] = []
    for candidate in sorted_candidates:
        best_index = _best_cluster_index(candidate, working_clusters)
        if best_index is None:
            working_clusters.append([candidate])
        else:
            working_clusters[best_index].append(candidate)
    return [_build_cluster(records) for records in working_clusters]


def _candidate_records_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("candidates", "runbook_candidates", "candidate_packets"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("Candidate input must be a list or an object with candidates/runbook_candidates.")


def _best_cluster_index(candidate: dict[str, Any], clusters: list[list[dict[str, Any]]]) -> int | None:
    best_index: int | None = None
    best_score = 0.0
    for index, cluster in enumerate(clusters):
        score = max(_candidate_similarity(candidate, other) for other in cluster)
        if score > best_score:
            best_score = score
            best_index = index
    if best_index is None:
        return None
    if best_score >= HIGH_CONFIDENCE_SIMILARITY:
        return best_index
    if _has_strong_shared_intent(candidate, clusters[best_index][0]):
        return best_index
    if best_score >= MIN_GROUP_SIMILARITY and _has_compatible_intent(candidate, clusters[best_index][0]):
        return best_index
    return None


def _candidate_similarity(first: dict[str, Any], second: dict[str, Any]) -> float:
    first_tokens = _meaningful_tokens(_candidate_match_text(first))
    second_tokens = _meaningful_tokens(_candidate_match_text(second))
    if not first_tokens or not second_tokens:
        return 0.0
    return len(first_tokens & second_tokens) / len(first_tokens | second_tokens)


def _has_compatible_intent(first: dict[str, Any], second: dict[str, Any]) -> bool:
    first_action = _primary_action(first)
    second_action = _primary_action(second)
    if first_action and second_action and tuple(sorted([first_action, second_action])) in OPPOSING_ACTIONS:
        return False
    if first_action and second_action and first_action != second_action:
        shared = _meaningful_tokens(_candidate_match_text(first)) & _meaningful_tokens(_candidate_match_text(second))
        return len(shared) >= 3
    return True


def _has_strong_shared_intent(first: dict[str, Any], second: dict[str, Any]) -> bool:
    first_action = _primary_action(first)
    second_action = _primary_action(second)
    if first_action and second_action and first_action != second_action:
        return False
    shared = _meaningful_tokens(_candidate_match_text(first)) & _meaningful_tokens(_candidate_match_text(second))
    return len(shared) >= 4


def _build_cluster(candidates: list[dict[str, Any]]) -> CandidateCluster:
    packets = [_candidate_packet(candidate) for candidate in candidates]
    normalized_title = _choose_normalized_title(candidates)
    aggregate_artifact_ids = _ordered_unique(
        artifact_id
        for candidate in candidates
        for artifact_id in _artifact_ids(candidate)
    )
    aggregate_context_ids = _ordered_unique(
        context_id
        for candidate in candidates
        for context_id in candidate.get("related_context_ids", [])
    )
    aggregate_source_refs = _merge_unique_dicts(
        ref
        for candidate in candidates
        for ref in [*(candidate.get("source_refs") or []), *(candidate.get("evidence_source_refs") or [])]
        if isinstance(ref, dict)
    )
    source_types = _ordered_unique(str(candidate.get("source_type") or "") for candidate in candidates)
    candidate_ids = [str(candidate.get("candidate_id") or "") for candidate in candidates]
    return CandidateCluster(
        candidate_cluster_id=f"cluster_{_slug(normalized_title)}",
        normalized_title=normalized_title,
        candidate_count=len(candidates),
        source_types=source_types,
        candidate_ids=candidate_ids,
        candidate_packets=packets,
        aggregate_artifact_ids=aggregate_artifact_ids,
        aggregate_context_ids=aggregate_context_ids,
        aggregate_source_refs=aggregate_source_refs,
        stage7_notes=_stage7_notes(candidates, source_types),
    )


def _candidate_packet(candidate: dict[str, Any]) -> CandidatePacket:
    return CandidatePacket(
        candidate_id=str(candidate.get("candidate_id") or ""),
        source_id=str(candidate.get("source_id") or ""),
        source_type=str(candidate.get("source_type") or ""),
        title=str(candidate.get("title") or ""),
        candidate_goal=str(candidate.get("candidate_goal") or ""),
        likely_procedure_type=str(candidate.get("likely_procedure_type") or ""),
        likely_role_required=str(candidate.get("likely_role_required") or ""),
        ingestion_batch_id=str(candidate.get("ingestion_batch_id") or ""),
        artifact_ids=_artifact_ids(candidate),
        related_context_ids=[str(value) for value in candidate.get("related_context_ids", [])],
        rough_steps=[str(value) for value in candidate.get("rough_steps", [])],
        source_grounded_values=candidate.get("source_grounded_values", []),
        source_refs=candidate.get("source_refs", []),
        evidence_source_refs=candidate.get("evidence_source_refs", []),
    )


def _stage7_notes(candidates: list[dict[str, Any]], source_types: list[str]) -> list[str]:
    notes = [f"{len(candidates)} source candidate(s) describe this procedure area."]
    if len(source_types) > 1:
        notes.append("Multiple source types are represented: " + ", ".join(source_types) + ".")
    if any(candidate.get("related_artifact_ids") or candidate.get("artifact_ids") for candidate in candidates):
        notes.append("Supporting artifacts are available for Stage 7 review.")
    if any(candidate.get("failure_or_escalation_notes") for candidate in candidates):
        notes.append("At least one source includes failure or escalation notes.")
    return notes


def _choose_normalized_title(candidates: list[dict[str, Any]]) -> str:
    with_scores = sorted(
        candidates,
        key=lambda candidate: (
            _source_title_rank(str(candidate.get("source_type") or "")),
            -len(str(candidate.get("title") or "")),
            str(candidate.get("title") or ""),
        ),
    )
    return _clean_title(str(with_scores[0].get("title") or "Untitled Candidate"))


def _source_title_rank(source_type: str) -> int:
    ranks = {"manual": 0, "sop": 1, "sme": 2, "training_slide": 3, "training_transcript": 4, "incident": 5}
    return ranks.get(source_type, 10)


def _candidate_match_text(candidate: dict[str, Any]) -> str:
    return " ".join(
        [
            str(candidate.get("title") or ""),
            str(candidate.get("candidate_goal") or ""),
            str(candidate.get("summary") or ""),
        ]
    )


def _primary_action(candidate: dict[str, Any]) -> str:
    for token in _tokens(str(candidate.get("title") or "")):
        action = ACTION_EQUIVALENTS.get(token)
        if action:
            return action
    return ""


def _meaningful_tokens(value: str) -> set[str]:
    return {
        ACTION_EQUIVALENTS.get(token, token)
        for token in _tokens(value)
        if token not in STOPWORDS and len(token) > 1
    }


def _tokens(value: str) -> list[str]:
    value = value.lower().replace("_", " ")
    return re.findall(r"[a-z0-9]+", value)


def _artifact_ids(candidate: dict[str, Any]) -> list[str]:
    return [str(value) for value in candidate.get("artifact_ids") or candidate.get("related_artifact_ids") or []]


def _normalized_title(value: str) -> str:
    return " ".join(_tokens(_clean_title(value)))


def _clean_title(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return re.sub(r"_+", "_", slug) or "untitled"


def _ordered_unique(values: Any) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value or "")
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def _merge_unique_dicts(values: Any) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for value in values:
        marker = json.dumps(value, sort_keys=True)
        if marker not in seen:
            seen.add(marker)
            result.append(value)
    return result
