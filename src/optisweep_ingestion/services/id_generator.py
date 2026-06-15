"""Stable ID helpers for source-derived records."""

from __future__ import annotations

import re
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text into a stable lowercase identifier fragment."""
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def make_section_id(prefix: str, heading: str) -> str:
    prefix_slug = slugify(prefix)
    heading_slug = slugify(heading.replace(".", "_"))
    return "_".join(part for part in [prefix_slug, heading_slug] if part)


def make_figure_id(figure_number: str) -> str:
    number = figure_number.strip()
    number = re.sub(r"^figure\s+", "", number, flags=re.IGNORECASE)
    return f"fig_{slugify(number)}"


def make_table_id(table_number: str) -> str:
    number = table_number.strip()
    number = re.sub(r"^table\s+", "", number, flags=re.IGNORECASE)
    return f"table_{slugify(number)}"


def make_source_bundle_id(source_path: str) -> str:
    return slugify(Path(source_path).stem)


def make_artifact_id_from_figure(figure_number: str, title: str | None) -> str:
    number = figure_number.strip()
    number = re.sub(r"^figure\s+", "", number, flags=re.IGNORECASE)
    parts = ["artifact", "fig", slugify(number)]
    title_slug = slugify(title or "")
    if title_slug:
        parts.append(title_slug)
    return "_".join(part for part in parts if part)


def make_artifact_id_from_page_image(page_number: int, image_index: int) -> str:
    return f"artifact_page_{page_number}_image_{image_index}"
