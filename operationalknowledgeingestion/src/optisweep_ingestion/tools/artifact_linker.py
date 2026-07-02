"""Deterministic artifact and image-reference linking for Stages 4–6."""

from __future__ import annotations

import re
from typing import Any

from operationalknowledgeingestion.src.optisweep_ingestion.tools.context_id_resolver import resolve_candidate_context_ids

IMAGE_NOTE_MARKER = "[Image support needed:"
IMAGE_NOTE_RE = re.compile(re.escape(IMAGE_NOTE_MARKER), re.IGNORECASE)
QUOTED_TEXT_RE = re.compile(r'"([^"]{2,120})"')
FIGURE_NUMBER_RE = re.compile(r"figure\s*(\d+)\s*[-.]?\s*(\d+)", re.IGNORECASE)
SCREEN_NAME_RE = re.compile(r"\b(visu_[a-z0-9_]+)\b", re.IGNORECASE)
VISUAL_STEP_RE = re.compile(
    r"\b(hmi|screen|visu_|figure|stacklight|photo|diagram|schematic|interface|panel|button|alarm)\b",
    re.IGNORECASE,
)
SCREEN_IMAGE_TYPES = {
    "hmi_screenshot",
    "operator_station_screen",
    "hospital_hmi_screen",
    "manual_control_screen",
    "training_video_frame",
}
HMI_CONTEXT_TYPES = {
    "hmi_screen_reference",
    "hmi_metric_reference",
    "hmi_alarm_reference",
    "hmi_control_reference",
}


def index_artifacts(artifacts: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["artifact_id"]): item for item in artifacts if item.get("artifact_id")}


def pages_from_source_refs(refs: list[Any]) -> set[int]:
    pages: set[int] = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        page = ref.get("page")
        if page is None:
            continue
        try:
            pages.add(int(page))
        except (TypeError, ValueError):
            continue
        page_end = ref.get("page_end")
        if page_end is not None:
            try:
                pages.add(int(page_end))
            except (TypeError, ValueError):
                pass
    return pages


def expand_pages(pages: set[int], margin: int = 3) -> set[int]:
    expanded: set[int] = set()
    for page in pages:
        for offset in range(-margin, margin + 1):
            candidate = page + offset
            if candidate > 0:
                expanded.add(candidate)
    return expanded


def figure_ids_from_source_refs(refs: list[Any]) -> set[str]:
    figure_ids: set[str] = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        figure_id = str(ref.get("figure_id") or "").strip().lower()
        if figure_id:
            figure_ids.add(figure_id)
        figure_number = str(ref.get("figure_number") or "")
        match = FIGURE_NUMBER_RE.search(figure_number)
        if match:
            figure_ids.add(f"fig_{match.group(1)}_{match.group(2)}")
    return figure_ids


def _normalize_term(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").lower()).strip("_")


def _artifact_text_blob(artifact: dict[str, Any]) -> str:
    parts = [
        str(artifact.get("artifact_id") or ""),
        str(artifact.get("title") or ""),
        str(artifact.get("short_description") or ""),
        str(artifact.get("summary") or ""),
        str(artifact.get("retrieval_text") or ""),
        str(artifact.get("detailed_description") or ""),
        str(artifact.get("figure_id") or ""),
        str(artifact.get("figure_number") or ""),
        " ".join(str(item) for item in artifact.get("tags") or []),
        " ".join(str(item) for item in artifact.get("what_to_look_at") or []),
        " ".join(str(item) for item in artifact.get("key_terms") or []),
    ]
    return " ".join(parts).lower()


def collect_record_text(record: dict[str, Any]) -> str:
    parts = [
        str(record.get("title") or ""),
        str(record.get("summary") or ""),
        str(record.get("details") or ""),
        str(record.get("candidate_goal") or ""),
        str(record.get("retrieval_text") or ""),
        " ".join(str(item) for item in record.get("rough_steps") or []),
        " ".join(str(item) for item in record.get("access_or_tools_needed") or []),
        " ".join(str(item) for item in record.get("key_terms") or []),
        " ".join(str(item) for item in record.get("applies_to") or []),
    ]
    for ref in record.get("source_refs") or []:
        if isinstance(ref, dict):
            parts.append(str(ref.get("quote_or_summary") or ""))
            parts.append(str(ref.get("figure_number") or ""))
    return " ".join(parts)


def extract_search_terms(record: dict[str, Any]) -> list[str]:
    text = collect_record_text(record)
    terms: list[str] = []
    seen: set[str] = set()

    def add_term(raw: Any) -> None:
        normalized = _normalize_term(raw)
        if len(normalized) < 3 or normalized in seen:
            return
        seen.add(normalized)
        terms.append(normalized)

    for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_/-]{2,}", text):
        add_term(token)
    for match in QUOTED_TEXT_RE.finditer(text):
        add_term(match.group(1))
    for match in SCREEN_NAME_RE.finditer(text):
        add_term(match.group(1))
    for term in record.get("key_terms") or []:
        add_term(term)
    for ref in record.get("source_refs") or []:
        if not isinstance(ref, dict):
            continue
        if ref.get("figure_id"):
            add_term(ref["figure_id"])
        figure_number = str(ref.get("figure_number") or "")
        figure_match = FIGURE_NUMBER_RE.search(figure_number)
        if figure_match:
            add_term(f"fig_{figure_match.group(1)}_{figure_match.group(2)}")
    return terms


def _score_artifact(
    artifact: dict[str, Any],
    *,
    terms: list[str],
    pages: set[int],
    figure_ids: set[str],
    prefer_screen_types: bool,
) -> int:
    score = 0
    artifact_figure = str(artifact.get("figure_id") or "").strip().lower()
    if artifact_figure and artifact_figure in figure_ids:
        score += 120
    try:
        artifact_page = int(artifact.get("page_number") or 0)
    except (TypeError, ValueError):
        artifact_page = 0
    if artifact_page and artifact_page in pages:
        score += 35

    blob = _artifact_text_blob(artifact)
    blob_normalized = blob.replace("-", "_").replace(" ", "_")
    for term in terms:
        if not term:
            continue
        if term in blob or term in blob_normalized:
            score += 18

    if prefer_screen_types and str(artifact.get("image_type") or "") in SCREEN_IMAGE_TYPES:
        score += 12
    return score


def find_matching_artifact_ids(
    record: dict[str, Any],
    artifacts: list[dict[str, Any]],
    *,
    existing_ids: set[str] | None = None,
    max_results: int = 8,
    page_margin: int = 3,
    min_score: int = 18,
) -> list[str]:
    existing = set(existing_ids or [])
    refs = [ref for ref in (record.get("source_refs") or []) if isinstance(ref, dict)]
    pages = expand_pages(pages_from_source_refs(refs), margin=page_margin)
    figure_ids = figure_ids_from_source_refs(refs)
    terms = extract_search_terms(record)
    prefer_screen_types = str(record.get("context_type") or "") in HMI_CONTEXT_TYPES or bool(
        VISUAL_STEP_RE.search(collect_record_text(record))
    )

    scored: list[tuple[int, str]] = []
    for artifact in artifacts:
        artifact_id = str(artifact.get("artifact_id") or "")
        if not artifact_id or artifact_id in existing:
            continue
        score = _score_artifact(
            artifact,
            terms=terms,
            pages=pages,
            figure_ids=figure_ids,
            prefer_screen_types=prefer_screen_types,
        )
        if score >= min_score:
            scored.append((score, artifact_id))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [artifact_id for _, artifact_id in scored[:max_results]]


def artifact_ids_from_contexts(
    context_ids: list[str],
    context_index: dict[str, dict[str, Any]],
) -> list[str]:
    artifact_ids: list[str] = []
    seen: set[str] = set()
    for context_id in context_ids:
        context = context_index.get(context_id)
        if not context:
            continue
        for field in ("related_artifact_ids", "image_refs"):
            for artifact_id in context.get(field) or []:
                text = str(artifact_id or "").strip()
                if text and text not in seen:
                    seen.add(text)
                    artifact_ids.append(text)
    return artifact_ids


def merge_artifact_ids(*groups: list[str], max_results: int = 8) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for artifact_id in group:
            text = str(artifact_id or "").strip()
            if not text or text in seen:
                continue
            seen.add(text)
            merged.append(text)
            if len(merged) >= max_results:
                return merged
    return merged


def enrich_context_record(
    record: dict[str, Any],
    artifacts: list[dict[str, Any]],
    *,
    max_artifact_ids: int = 6,
) -> tuple[dict[str, Any], list[str]]:
    updated = dict(record)
    notes: list[str] = []
    existing = set(str(item) for item in updated.get("related_artifact_ids") or [])
    matched = find_matching_artifact_ids(
        updated,
        artifacts,
        existing_ids=existing,
        max_results=max_artifact_ids,
    )
    related_artifact_ids = merge_artifact_ids(list(existing), matched, max_results=max_artifact_ids)
    if related_artifact_ids != list(updated.get("related_artifact_ids") or []):
        notes.append(
            f"Linked artifacts for context '{updated.get('context_id', '?')}': "
            + ", ".join(related_artifact_ids)
        )
    updated["related_artifact_ids"] = related_artifact_ids
    image_refs = list(updated.get("image_refs") or [])
    for artifact_id in related_artifact_ids:
        if artifact_id not in image_refs:
            image_refs.append(artifact_id)
    updated["image_refs"] = image_refs[:max_artifact_ids]
    return updated, notes


def enrich_context_records(
    records: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    *,
    max_artifact_ids: int = 6,
) -> tuple[list[dict[str, Any]], list[str]]:
    enriched: list[dict[str, Any]] = []
    notes: list[str] = []
    for record in records:
        updated, record_notes = enrich_context_record(record, artifacts, max_artifact_ids=max_artifact_ids)
        enriched.append(updated)
        notes.extend(record_notes)
    return enriched, notes


def collect_candidate_artifact_ids(
    candidate: dict[str, Any],
    artifacts: list[dict[str, Any]],
    context_index: dict[str, dict[str, Any]] | None = None,
    *,
    max_results: int = 8,
) -> list[str]:
    existing = set(str(item) for item in candidate.get("related_artifact_ids") or [])
    context_ids = [str(item) for item in candidate.get("related_context_ids") or []]
    from_context = artifact_ids_from_contexts(context_ids, context_index or {})
    matched = find_matching_artifact_ids(
        candidate,
        artifacts,
        existing_ids=existing | set(from_context),
        max_results=max_results,
        page_margin=5,
    )
    return merge_artifact_ids(
        list(existing),
        from_context,
        matched,
        max_results=max_results,
    )


def _artifact_description(artifact: dict[str, Any]) -> str:
    for field in ("short_description", "summary", "title"):
        text = str(artifact.get(field) or "").strip()
        if text:
            return text[:180]
    retrieval = str(artifact.get("retrieval_text") or "").strip()
    if retrieval:
        return retrieval[:180]
    return str(artifact.get("artifact_id") or "supporting source artifact")


def _build_image_note(step: str, artifact_index: dict[str, dict[str, Any]], artifact_ids: list[str]) -> str:
    for artifact_id in artifact_ids:
        artifact = artifact_index.get(artifact_id)
        if not artifact:
            continue
        return _artifact_description(artifact)
    if QUOTED_TEXT_RE.search(step):
        return "source figure, screen, or photo showing the referenced control, screen, or component"
    return "source figure, screen, or photo supporting this step"


def ensure_candidate_image_notes(
    candidate: dict[str, Any],
    artifact_index: dict[str, dict[str, Any]],
) -> tuple[list[str], bool]:
    artifact_ids = [str(item) for item in candidate.get("related_artifact_ids") or []]
    updated_steps: list[str] = []
    changed = False
    for step in candidate.get("rough_steps") or []:
        text = str(step or "").strip()
        if not text:
            continue
        if IMAGE_NOTE_RE.search(text):
            updated_steps.append(text)
            continue
        if not VISUAL_STEP_RE.search(text):
            updated_steps.append(text)
            continue
        note = _build_image_note(text, artifact_index, artifact_ids)
        updated_steps.append(f"{text} {IMAGE_NOTE_MARKER} {note}]")
        changed = True
    return updated_steps, changed



def enrich_runbook_candidate(
    candidate: dict[str, Any],
    artifacts: list[dict[str, Any]],
    context_index: dict[str, dict[str, Any]] | None = None,
    *,
    max_artifact_ids: int = 8,
) -> tuple[dict[str, Any], list[str]]:
    updated = dict(candidate)
    notes: list[str] = []
    if context_index:
        updated, context_notes = resolve_candidate_context_ids(updated, context_index)
        notes.extend(context_notes)
    artifact_index = index_artifacts(artifacts)
    related_artifact_ids = collect_candidate_artifact_ids(
        updated,
        artifacts,
        context_index,
        max_results=max_artifact_ids,
    )
    if related_artifact_ids != list(updated.get("related_artifact_ids") or []):
        notes.append(
            f"Linked artifacts for candidate '{updated.get('candidate_id', '?')}': "
            + ", ".join(related_artifact_ids)
        )
    updated["related_artifact_ids"] = related_artifact_ids
    rough_steps, notes_changed = ensure_candidate_image_notes(updated, artifact_index)
    if notes_changed:
        notes.append(f"Added inline image notes for candidate '{updated.get('candidate_id', '?')}'")
    updated["rough_steps"] = rough_steps
    return updated, notes


def enrich_runbook_candidates(
    candidates: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    contexts: list[dict[str, Any]] | None = None,
    *,
    max_artifact_ids: int = 8,
) -> tuple[list[dict[str, Any]], list[str]]:
    context_index = {str(item["context_id"]): item for item in (contexts or []) if item.get("context_id")}
    enriched: list[dict[str, Any]] = []
    notes: list[str] = []
    for candidate in candidates:
        updated, candidate_notes = enrich_runbook_candidate(
            candidate,
            artifacts,
            context_index,
            max_artifact_ids=max_artifact_ids,
        )
        enriched.append(updated)
        notes.extend(candidate_notes)
    return enriched, notes
