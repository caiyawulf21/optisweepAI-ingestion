from __future__ import annotations

import re
from typing import Any

MAX_RAG_TEXT_CHARS = 4000


def build_operational_context_retrieval_text(record: dict[str, Any]) -> str:
    retrieval = str(record.get("retrieval_text") or "").strip()
    if retrieval:
        return _truncate(retrieval)
    parts = [
        str(record.get("title") or ""),
        str(record.get("summary") or ""),
        str(record.get("details") or ""),
        str(record.get("context_type") or ""),
        " ".join(str(item) for item in record.get("key_terms") or [] if str(item).strip()),
        " ".join(str(item) for item in record.get("applies_to") or [] if str(item).strip()),
    ]
    return _truncate(_compact(parts))


def build_source_artifact_retrieval_text(record: dict[str, Any]) -> str:
    retrieval = str(record.get("retrieval_text") or "").strip()
    if retrieval:
        return _truncate(retrieval)
    parts = [
        str(record.get("title") or ""),
        str(record.get("summary") or ""),
        str(record.get("short_description") or ""),
        str(record.get("detailed_description") or ""),
        str(record.get("caption_text") or ""),
        str(record.get("what_to_look_at") or ""),
        str(record.get("artifact_type") or ""),
        " ".join(str(item) for item in record.get("tags") or [] if str(item).strip()),
    ]
    return _truncate(_compact(parts))


def _compact(parts: list[str]) -> str:
    text = " ".join(part.strip() for part in parts if part and part.strip())
    return re.sub(r"\s+", " ", text).strip()


def _truncate(text: str) -> str:
    if len(text) <= MAX_RAG_TEXT_CHARS:
        return text
    return text[:MAX_RAG_TEXT_CHARS]
