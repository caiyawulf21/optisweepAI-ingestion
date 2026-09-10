from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from orchestration.paths import INBOX_INCIDENTS, INBOX_MANUALS, INBOX_VIDEOS
from orchestration.state import SourceType

CASE_ID_RE = re.compile(r"(?:case[_\s-]*)(\d{5,})", re.IGNORECASE)
VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm"}
TRANSCRIPT_SUFFIXES = {".vtt", ".srt"}
PDF_SUFFIXES = {".pdf"}


@dataclass(frozen=True)
class RoutedSource:
    source_type: SourceType
    source_path: Path
    companion_paths: list[Path]
    case_id: str | None
    source_id: str | None
    source_title: str | None


def classify_upload(path: Path, companion_paths: list[Path] | None = None) -> RoutedSource:
    resolved = path.resolve()
    companions = [p.resolve() for p in (companion_paths or [])]
    name = resolved.name
    parent = resolved.parent
    suffix = resolved.suffix.lower()

    if _is_under(resolved, INBOX_INCIDENTS) or CASE_ID_RE.search(name):
        case_id = extract_case_id(name) or extract_case_id(str(resolved))
        return RoutedSource(
            source_type="incident",
            source_path=resolved,
            companion_paths=companions,
            case_id=case_id,
            source_id=f"case_{case_id}" if case_id else None,
            source_title=resolved.stem,
        )

    if _is_under(resolved, INBOX_VIDEOS) or suffix in VIDEO_SUFFIXES:
        transcripts = [
            p
            for p in companions + list(parent.glob(f"{resolved.stem}*"))
            if p.suffix.lower() in TRANSCRIPT_SUFFIXES and p != resolved
        ]
        unique_transcripts = sorted({p.resolve() for p in transcripts})
        return RoutedSource(
            source_type="training_video",
            source_path=resolved,
            companion_paths=unique_transcripts,
            case_id=None,
            source_id=_slug(resolved.stem),
            source_title=resolved.stem,
        )

    if _is_under(resolved, INBOX_MANUALS) or suffix in PDF_SUFFIXES:
        return RoutedSource(
            source_type="manual",
            source_path=resolved,
            companion_paths=companions,
            case_id=None,
            source_id=_slug(resolved.stem),
            source_title=resolved.stem,
        )

    return RoutedSource(
        source_type="unknown",
        source_path=resolved,
        companion_paths=companions,
        case_id=None,
        source_id=None,
        source_title=resolved.stem,
    )


def extract_case_id(text: str) -> str | None:
    match = CASE_ID_RE.search(text)
    return match.group(1) if match else None


def is_ingestible_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name.startswith(".") or path.name.startswith("~"):
        return False
    suffix = path.suffix.lower()
    if suffix in TRANSCRIPT_SUFFIXES:
        return False
    return suffix in PDF_SUFFIXES | VIDEO_SUFFIXES


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value.strip())
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "source"
