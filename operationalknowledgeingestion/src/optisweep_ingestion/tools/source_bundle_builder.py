"""Deterministic Stage 1 source bundle builder for source knowledge extraction."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from operationalknowledgeingestion.src.optisweep_ingestion.schemas.source_bundle import (
    SourceBundle,
    SourceDocument,
    SourceFigureRef,
    SourceMetadata,
    SourcePage,
    SourceSection,
    SourceTableRef,
)
from operationalknowledgeingestion.src.optisweep_ingestion.services.id_generator import (
    make_figure_id,
    make_section_id,
    make_source_bundle_id,
    make_table_id,
)
from operationalknowledgeingestion.src.optisweep_ingestion.services.source_ref_service import make_ingestion_batch_id
from operationalknowledgeingestion.src.optisweep_ingestion.tools.pdf_parser import parse_pdf
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import write_json

HEADING_RE = re.compile(r"^(?P<number>\d+(?:\.\d+)*)(?:\s*:\s*|\s+)(?P<title>[^\n]{2,110})$")
CHAPTER_RE = re.compile(
    r"^Chapter\s+(?P<number>\d+)(?:\s*[:.-]?\s*)(?P<title>[^\n]{2,90})$",
    re.IGNORECASE,
)
FIGURE_RE = re.compile(r"\bFigure\s+\d+(?:-\d+)+\b", re.IGNORECASE)
TABLE_RE = re.compile(r"\bTable\s+\d+(?:-\d+)+\b", re.IGNORECASE)
FRONT_MATTER_MARKERS = (
    "table of contents",
    "contents",
    "list of images",
    "list of tables",
    "version history",
    "preface",
)
FOOTER_MARKERS = ("copyright", "©", "fortna inc", "confidential")
STEP_VERBS = (
    "navigate",
    "press",
    "verify",
    "select",
    "open",
    "close",
    "remove",
    "install",
    "place",
    "scan",
    "record",
    "check",
    "turn",
    "set",
)


def build_source_bundle(
    source_pdf: str | Path,
    output_dir: str | Path,
    source_bundle_id: str | None = None,
    source_document_id: str | None = None,
    source_id: str | None = None,
    source_type: str = "manual",
    source_title: str | None = None,
    source_version: str | None = None,
    ingestion_batch_id: str | None = None,
) -> SourceBundle:
    parsed = parse_pdf(source_pdf)
    bundle = build_source_bundle_from_pages(
        pages=parsed["pages"],
        source_path=str(source_pdf),
        metadata=parsed.get("metadata") or {},
        source_bundle_id=source_bundle_id,
        source_document_id=source_document_id,
        source_id=source_id,
        source_type=source_type,
        source_title=source_title,
        source_version=source_version,
        ingestion_batch_id=ingestion_batch_id,
    )
    output_path = Path(output_dir)
    write_json(output_path / "source_bundle.json", bundle)
    write_json(output_path / "source_bundle_quality_report.json", build_quality_report(bundle))
    return bundle


def build_source_bundle_from_pages(
    pages: list[dict[str, Any]],
    source_path: str,
    metadata: dict[str, Any] | None = None,
    source_bundle_id: str | None = None,
    source_document_id: str | None = None,
    source_id: str | None = None,
    source_type: str = "manual",
    source_title: str | None = None,
    source_version: str | None = None,
    ingestion_batch_id: str | None = None,
) -> SourceBundle:
    metadata = metadata or {}
    bundle_id = source_bundle_id or make_source_bundle_id(source_path)
    document_id = source_document_id or bundle_id
    resolved_source_id = source_id or bundle_id
    resolved_title = source_title or _clean_metadata_value(metadata.get("title")) or _title_from_path(source_path) or bundle_id
    resolved_version = source_version or _extract_document_version(pages) or _clean_metadata_value(metadata.get("version"))
    batch_id = ingestion_batch_id or make_ingestion_batch_id()
    source_metadata = SourceMetadata(
        source_id=resolved_source_id,
        source_type=source_type,
        source_title=resolved_title,
        source_version=resolved_version,
        ingestion_batch_id=batch_id,
        source_document_id=document_id,
    )
    source_document = SourceDocument(
        source_document_id=document_id,
        title=resolved_title,
        document_type="operation_maintenance_manual",
        version=resolved_version,
        document_date=_extract_document_date(pages)
        or _normalize_pdf_date(_clean_metadata_value(metadata.get("creationDate") or metadata.get("modDate"))),
        source_type=source_type,
        source_path=source_path,
    )

    sections = detect_sections_from_pages(pages, bundle_id)
    source_pages = _build_pages(pages, sections)
    section_by_page = _section_by_page(sections)
    figure_refs = _detect_refs(pages, section_by_page, FIGURE_RE, "figure")
    table_refs = _detect_refs(pages, section_by_page, TABLE_RE, "table")

    return SourceBundle(
        source_bundle_id=bundle_id,
        source_metadata=source_metadata,
        source_document=source_document,
        pages=source_pages,
        sections=sections,
        figure_refs=figure_refs,
        table_refs=table_refs,
        build_metadata={
            "builder": "source_bundle_builder",
            "stage": "stage_1_source_bundle",
            "pipeline": "source_knowledge_extraction",
            "llm_used": False,
            "built_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def detect_sections_from_pages(pages: list[dict[str, Any]], bundle_id: str = "manual") -> list[SourceSection]:
    starts: list[tuple[int, SourceSection]] = []
    seen: set[str] = set()
    for page in pages:
        page_number = int(page["page_number"])
        if is_front_matter_page(str(page.get("text") or ""), page_number):
            continue
        for line in _candidate_lines(str(page.get("text") or "")):
            if not is_likely_section_heading(line):
                continue
            normalized = _normalize_line(line)
            match = CHAPTER_RE.match(normalized) or HEADING_RE.match(normalized)
            if not match:
                continue
            heading = normalized
            section_id = make_section_id(bundle_id, heading)
            if section_id in seen:
                continue
            seen.add(section_id)
            number = match.group("number")
            starts.append(
                (
                    page_number,
                    SourceSection(
                        section_id=section_id,
                        title=heading,
                        level=number.count(".") + 1,
                        page_start=page_number,
                        text_preview=_preview(page.get("text") or ""),
                    ),
                )
            )

    starts.sort(key=lambda item: (item[0], item[1].level))
    sections = [section for _, section in starts]
    for index, section in enumerate(sections):
        next_start = sections[index + 1].page_start if index + 1 < len(sections) else None
        section.page_end = max(section.page_start or 0, next_start - 1) if next_start else _last_page_number(pages)
        section.parent_section_id = _find_parent_section_id(section, sections[:index])
    return sections


def is_likely_section_heading(line: str) -> bool:
    normalized = _normalize_line(line)
    if not normalized or len(normalized) > 120:
        return False
    lowered = normalized.lower()
    if _is_metadata_line(normalized):
        return False
    if lowered.startswith(("this chapter ", "refer to chapter ")):
        return False

    chapter_match = CHAPTER_RE.match(normalized)
    if chapter_match:
        title = chapter_match.group("title").strip()
        return _is_reasonable_heading_title(title)

    match = HEADING_RE.match(normalized)
    if not match:
        return False
    number = match.group("number")
    title = match.group("title").strip()
    if _looks_like_torque_or_fraction_row(normalized, number, title):
        return False
    if "." not in number and int(number) > 9:
        return False
    if _looks_like_numbered_step(number, title):
        return False
    return _is_reasonable_heading_title(title)


def _build_pages(pages: list[dict[str, Any]], sections: list[SourceSection]) -> list[SourcePage]:
    section_by_page = _section_by_page(sections)
    section_ids_by_page: dict[int, list[str]] = {}
    for section in sections:
        if section.page_start is None or section.page_end is None:
            continue
        for page_number in range(section.page_start, section.page_end + 1):
            section_ids_by_page.setdefault(page_number, []).append(section.section_id)
    return [
        SourcePage(
            page_number=int(page["page_number"]),
            text=str(page.get("text") or ""),
            text_length=len(str(page.get("text") or "")),
            section_id=section_by_page.get(int(page["page_number"])),
            section_ids=section_ids_by_page.get(int(page["page_number"]), []),
        )
        for page in pages
    ]


def build_quality_report(bundle: SourceBundle) -> dict[str, Any]:
    page_52 = next((page for page in bundle.pages if page.page_number == 52), None)
    page_52_text = _normalize_line(page_52.text).lower() if page_52 else ""
    figures = {ref.figure_id: ref for ref in bundle.figure_refs}
    tables = {ref.table_id: ref for ref in bundle.table_refs}
    fig_4_22_page = figures.get("fig_4_22").page_number if figures.get("fig_4_22") else None
    table_4_8_page = tables.get("table_4_8").page_number if tables.get("table_4_8") else None
    heartbeat_text_ok = all(
        term in page_52_text
        for term in ["heartbeat stats", "last", "max", "min", "10 seconds"]
    )
    heartbeat_smoke_check = {
        "page_52_contains_heartbeat": heartbeat_text_ok,
        "fig_4_22_page": fig_4_22_page,
        "table_4_8_page": table_4_8_page,
        "page_52_section_id": page_52.section_id if page_52 else None,
        "passed": bool(
            heartbeat_text_ok
            and fig_4_22_page == 52
            and table_4_8_page == 52
            and page_52
            and page_52.section_id
        ),
    }
    return {
        "page_count": len(bundle.pages),
        "section_count": len(bundle.sections),
        "figure_ref_count": len(bundle.figure_refs),
        "table_ref_count": len(bundle.table_refs),
        "llm_used": bool(bundle.build_metadata.get("llm_used")),
        "heartbeat_smoke_check": heartbeat_smoke_check,
        "warnings": [
            "Some pages contain multiple section headings; section_ids lists all page-level section matches while section_id keeps the active page section.",
            "Appendix tables may not all be captured as canonical table refs.",
        ],
    }


def _detect_refs(
    pages: list[dict[str, Any]],
    section_by_page: dict[int, str],
    pattern: re.Pattern[str],
    ref_type: str,
) -> list[SourceFigureRef] | list[SourceTableRef]:
    occurrences: dict[str, list[dict[str, Any]]] = {}
    for page in pages:
        page_number = int(page["page_number"])
        text = str(page.get("text") or "")
        front_matter = is_front_matter_page(text, page_number)
        for line in text.splitlines():
            normalized_line = _normalize_line(line)
            for match in pattern.finditer(normalized_line):
                ref_number = _normalize_ref_number(match.group(0))
                ref_id = make_figure_id(ref_number) if ref_type == "figure" else make_table_id(ref_number)
                caption = normalized_line or ref_number
                title = caption[match.end() :].strip(" :-") or None
                occurrences.setdefault(ref_id, []).append(
                    {
                        "ref_id": ref_id,
                        "ref_number": ref_number,
                        "page_number": page_number,
                        "section_id": section_by_page.get(page_number),
                        "caption_text": caption,
                        "title": title,
                        "is_front_matter": front_matter,
                    }
                )

    refs: list[SourceFigureRef | SourceTableRef] = []
    for ref_id in sorted(occurrences):
        occurrence = _choose_canonical_occurrence(occurrences[ref_id])
        fields = {
            "page_number": occurrence["page_number"],
            "section_id": occurrence["section_id"],
            "caption_text": occurrence["caption_text"],
            "title": occurrence["title"],
        }
        if ref_type == "figure":
            refs.append(
                SourceFigureRef(
                    figure_id=ref_id,
                    figure_number=occurrence["ref_number"],
                    **fields,
                )
            )
        else:
            refs.append(
                SourceTableRef(
                    table_id=ref_id,
                    table_number=occurrence["ref_number"],
                    **fields,
                )
            )
    return refs


def _choose_canonical_occurrence(occurrences: list[dict[str, Any]]) -> dict[str, Any]:
    def score(occurrence: dict[str, Any]) -> tuple[int, int, int, int]:
        return (
            0 if occurrence["is_front_matter"] else 1,
            1 if occurrence["section_id"] else 0,
            1 if occurrence["caption_text"] and occurrence["caption_text"] != occurrence["ref_number"] else 0,
            -occurrence["page_number"],
        )

    return max(occurrences, key=score)


def is_front_matter_page(page_text: str, page_number: int) -> bool:
    normalized = _normalize_line(page_text).lower()
    if any(marker in normalized for marker in FRONT_MATTER_MARKERS):
        return True
    if page_number <= 20:
        lines = [_normalize_line(line).lower() for line in page_text.splitlines()]
        list_like = sum(
            1
            for line in lines
            if re.match(r"^(chapter|figure|table)\s+\d", line)
            or re.match(r"^\d+(?:\.\d+)*\s+.+\s+\d+$", line)
        )
        return list_like >= 5
    return False


def _candidate_lines(text: str) -> list[str]:
    return [
        normalized
        for line in text.splitlines()
        if 3 <= len((normalized := _normalize_line(line))) <= 140
    ]


def _section_by_page(sections: list[SourceSection]) -> dict[int, str]:
    by_page: dict[int, str] = {}
    for section in sections:
        if section.page_start is None or section.page_end is None:
            continue
        for page_number in range(section.page_start, section.page_end + 1):
            by_page[page_number] = section.section_id
    return by_page


def _find_parent_section_id(section: SourceSection, previous: list[SourceSection]) -> str | None:
    section_number = _section_number(section.title)
    if section_number and "." in section_number:
        parent_number = section_number.rsplit(".", 1)[0]
        for candidate in reversed(previous):
            if _section_number(candidate.title) == parent_number:
                return candidate.section_id
    for candidate in reversed(previous):
        if candidate.level < section.level:
            return candidate.section_id
    return None


def _last_page_number(pages: list[dict[str, Any]]) -> int | None:
    return max((int(page["page_number"]) for page in pages), default=None)


def _preview(text: str, limit: int = 240) -> str | None:
    preview = re.sub(r"\s+", " ", text).strip()
    return preview[:limit] if preview else None


def _clean_metadata_value(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()
    return cleaned or None


def _extract_document_version(pages: list[dict[str, Any]]) -> str | None:
    first_page_text = str(pages[0].get("text") or "") if pages else ""
    match = re.search(r"\bVersion\s+([A-Za-z0-9._-]+)\b", _normalize_line(first_page_text), re.IGNORECASE)
    return match.group(1) if match else None


def _extract_document_date(pages: list[dict[str, Any]]) -> str | None:
    first_page_text = _normalize_line(str(pages[0].get("text") or "")) if pages else ""
    match = re.search(r"\b(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})\b", first_page_text)
    if not match:
        return None
    day, month_name, year = match.groups()
    try:
        parsed = datetime.strptime(f"{day} {month_name} {year}", "%d %B %Y")
    except ValueError:
        try:
            parsed = datetime.strptime(f"{day} {month_name} {year}", "%d %b %Y")
        except ValueError:
            return None
    return parsed.date().isoformat()


def _normalize_pdf_date(value: str | None) -> str | None:
    if not value:
        return None
    match = re.match(r"D:(\d{4})(\d{2})(\d{2})", value)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    return value


def _title_from_path(source_path: str) -> str | None:
    stem = Path(source_path).stem
    title = re.sub(r"\s+-\s+Final\s+\d+$", "", stem, flags=re.IGNORECASE)
    return title.strip() or None


def _normalize_ref_number(value: str) -> str:
    words = _normalize_line(value).split()
    if len(words) < 2:
        return value
    return f"{words[0].title()} {words[1]}"


def _section_number(title: str) -> str | None:
    normalized = _normalize_line(title)
    chapter_match = CHAPTER_RE.match(normalized)
    if chapter_match:
        return chapter_match.group("number")
    heading_match = HEADING_RE.match(normalized)
    if heading_match:
        return heading_match.group("number")
    return None


def _normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.replace("\xa0", " ")).strip()


def _is_metadata_line(line: str) -> bool:
    lowered = line.lower()
    if any(marker in lowered for marker in FOOTER_MARKERS):
        return True
    if re.search(r"\b(www\.|\.com|@|phone|fax)\b", lowered):
        return True
    if re.match(r"^\d{1,2}\s+[a-z]+\s*,?\s+\d{4}$", lowered):
        return True
    if re.match(r"^\d+\s+[a-z0-9 .,-]+(?:st|street|dr|drive|suite|ste|nw)\b", lowered):
        return True
    if re.match(r"^[ivxlcdm]+$", lowered):
        return True
    return False


def _is_reasonable_heading_title(title: str) -> bool:
    stripped = title.strip(" :-")
    lowered = stripped.lower()
    if len(stripped) < 3 or _is_metadata_line(stripped):
        return False
    if lowered.endswith("."):
        return False
    if lowered.startswith(("provides ", "describes ", "contains ", "will ", "should ")):
        return False
    prose_words = {"provides", "describes", "information", "reference", "procedures"}
    if len(stripped.split()) > 10 and any(word in lowered for word in prose_words):
        return False
    return True


def _looks_like_numbered_step(number: str, title: str) -> bool:
    if "." in number:
        return False
    first_word = title.strip().split()[0].lower().strip(".,:;") if title.strip() else ""
    return first_word in STEP_VERBS


def _looks_like_torque_or_fraction_row(line: str, number: str, title: str) -> bool:
    if "/" in line:
        return True
    if re.search(r"\b(?:n-?m|nm|ft-?lb|in-?lb|lb-?ft|torque)\b", line, re.IGNORECASE):
        return True
    if re.fullmatch(r"\d+(?:\.\d+)?\s+[0-9/.\- ]+", line):
        return True
    if re.fullmatch(r"\d+(?:\.\d+)?\s+M\d+(?:x\d+)?", line, re.IGNORECASE):
        return True
    return False
