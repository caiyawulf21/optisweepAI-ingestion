"""Stage 1 - Incident source package loading.

Loads an incident PDF into a stable source package with case metadata, page
inventory, source refs, and a Stage 1 report for downstream OCR stages.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from optisweep_incidence_ingestion.services.ids import (
    make_ingestion_batch_id,
    make_page_ref,
    make_source_id,
    make_source_package_id,
)
from optisweep_incidence_ingestion.utils.json_utils import write_json


def build_incident_source_package(
    source_pdf: str | Path,
    output_dir: str | Path,
    case_id: str,
    source_title: str | None = None,
    ingestion_batch_id: str | None = None,
) -> dict[str, Any]:
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required for incident Stage 1. Install pymupdf.") from exc

    pdf_path = Path(source_pdf)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    batch_id = ingestion_batch_id or make_ingestion_batch_id()
    source_id = make_source_id(case_id)
    package_id = make_source_package_id(case_id, pdf_path)
    title = source_title or pdf_path.stem
    pages: list[dict[str, Any]] = []
    with fitz.open(pdf_path) as document:
        metadata = dict(document.metadata or {})
        for index, page in enumerate(document, start=1):
            text = page.get_text("text") or ""
            image_count = len(page.get_images(full=True))
            parsed_text_length = len(text.strip())
            page_diagnostics = build_stage1_page_diagnostics(
                parsed_text_length=parsed_text_length,
                embedded_image_count=image_count,
                width=float(page.rect.width),
                height=float(page.rect.height),
            )
            pages.append(
                {
                    "page_number": index,
                    "page_ref": make_page_ref(case_id, index),
                    "width": round(float(page.rect.width), 2),
                    "height": round(float(page.rect.height), 2),
                    "parsed_text": text,
                    "parsed_text_length": parsed_text_length,
                    "embedded_image_count": image_count,
                    "page_diagnostics": page_diagnostics,
                    "likely_scanned_or_screenshot": page_diagnostics["likely_scanned_or_screenshot"],
                    "needs_ocr": page_diagnostics["needs_ocr"],
                    "rendered_page_image_ref": None,
                    "ocr_text": None,
                    "ocr_confidence": None,
                    "stage2_status": "not_run",
                    "source_refs": [
                        build_incident_source_ref(
                            source_id=source_id,
                            source_title=title,
                            ingestion_batch_id=batch_id,
                            case_id=case_id,
                            page_number=index,
                        )
                    ],
                }
            )
        page_count = len(document)

    package = {
        "source_package_id": package_id,
        "record_type": "incident_source_package",
        "source_id": source_id,
        "source_type": "incident_evidence_pdf",
        "source_case_id": case_id,
        "source_title": title,
        "source_file_path": str(pdf_path),
        "source_file_name": pdf_path.name,
        "ingestion_batch_id": batch_id,
        "page_count": page_count,
        "pages": pages,
        "source_metadata": {
            "pdf_metadata": metadata,
            "file_size_bytes": pdf_path.stat().st_size,
        },
        "build_metadata": {
            "builder": "stage1_source_package",
            "pipeline": "incidence_knowledge_ingestion",
            "stage": "stage_1_incident_source_package_loading",
            "llm_used": False,
            "built_at": datetime.now(timezone.utc).isoformat(),
        },
        "warnings": _stage1_warnings(pages),
    }
    output_path = Path(output_dir)
    write_json(output_path / "incident_source_package.json", package)
    write_json(output_path / "stage1_source_package_report.json", build_stage1_report(package))
    return package


def build_incident_source_ref(
    *,
    source_id: str,
    source_title: str,
    ingestion_batch_id: str,
    case_id: str,
    page_number: int,
    artifact_id: str | None = None,
    quote_or_summary: str | None = None,
) -> dict[str, Any]:
    ref: dict[str, Any] = {
        "source_id": source_id,
        "source_type": "incident_evidence_pdf",
        "source_title": source_title,
        "source_case_id": case_id,
        "ingestion_batch_id": ingestion_batch_id,
        "page": page_number,
        "page_ref": make_page_ref(case_id, page_number),
    }
    if artifact_id:
        ref["artifact_id"] = artifact_id
    if quote_or_summary:
        ref["quote_or_summary"] = quote_or_summary
    return ref


def build_stage1_report(package: dict[str, Any]) -> dict[str, Any]:
    pages = package.get("pages") or []
    return {
        "source_package_id": package["source_package_id"],
        "source_id": package["source_id"],
        "source_case_id": package["source_case_id"],
        "source_type": package["source_type"],
        "ingestion_batch_id": package["ingestion_batch_id"],
        "page_count": len(pages),
        "pages_with_selectable_text": sum(1 for page in pages if page.get("parsed_text_length", 0) > 20),
        "pages_with_embedded_images": sum(1 for page in pages if page.get("embedded_image_count", 0) > 0),
        "total_embedded_images": sum(int(page.get("embedded_image_count") or 0) for page in pages),
        "pages_needing_ocr": sum(1 for page in pages if page.get("needs_ocr")),
        "likely_scanned_or_screenshot_pages": sum(1 for page in pages if page.get("likely_scanned_or_screenshot")),
        "warnings": package.get("warnings") or [],
    }


def build_stage1_page_diagnostics(
    *,
    parsed_text_length: int,
    embedded_image_count: int,
    width: float,
    height: float,
) -> dict[str, Any]:
    page_area = max(width * height, 1.0)
    aspect_ratio = round(width / max(height, 1.0), 4)
    has_selectable_text = parsed_text_length > 20
    likely_scanned_or_screenshot = embedded_image_count > 0 and parsed_text_length < 80
    needs_ocr = not has_selectable_text or likely_scanned_or_screenshot
    return {
        "has_selectable_text": has_selectable_text,
        "selectable_text_length": parsed_text_length,
        "embedded_image_count": embedded_image_count,
        "page_area": round(page_area, 2),
        "aspect_ratio": aspect_ratio,
        "likely_scanned_or_screenshot": likely_scanned_or_screenshot,
        "needs_ocr": needs_ocr,
        "ocr_priority": "high" if likely_scanned_or_screenshot or parsed_text_length == 0 else "normal",
    }


def _stage1_warnings(pages: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    pages_with_text = sum(1 for page in pages if page.get("parsed_text_length", 0) > 20)
    if pages and pages_with_text / len(pages) < 0.25:
        warnings.append(
            "Most PDF pages have little or no selectable text; Stage 2 OCR is required and should be treated as primary extraction evidence."
        )
    if any(page.get("embedded_image_count", 0) > 0 for page in pages):
        warnings.append("PDF contains embedded images; Stage 2 should extract both rendered pages and embedded image evidence.")
    if any(page.get("likely_scanned_or_screenshot") for page in pages):
        warnings.append("One or more pages look like scanned screenshots; Stage 2 should use OCR retries and quality reporting.")
    return warnings
