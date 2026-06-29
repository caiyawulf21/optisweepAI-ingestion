"""Stages 1+ support - stable ID helpers for incident source records.

Creates deterministic source, package, page, artifact, and batch IDs used
across source packages, OCR artifacts, enrichment packets, and later records.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def make_ingestion_batch_id() -> str:
    return datetime.now(timezone.utc).strftime("batch_%Y%m%dT%H%M%SZ")


def make_source_id(case_id: str) -> str:
    return f"source_case_{slugify(case_id)}"


def make_source_package_id(case_id: str, source_path: str | Path) -> str:
    return f"incident_source_package_{slugify(case_id)}_{slugify(Path(source_path).stem)}"


def make_page_ref(case_id: str, page_number: int) -> str:
    return f"case_{slugify(case_id)}:page_{page_number}"


def make_artifact_id(case_id: str, page_number: int, kind: str, index: int | None = None) -> str:
    suffix = f"_{index:02d}" if index is not None else ""
    return f"artifact_incident_{slugify(case_id)}_page_{page_number:03d}_{slugify(kind)}{suffix}"
