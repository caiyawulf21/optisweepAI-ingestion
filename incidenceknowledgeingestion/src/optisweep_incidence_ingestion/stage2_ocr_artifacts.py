"""Stage 2 - OCR and evidence artifact extraction.

Renders PDF pages, OCRs page context, extracts clean embedded/nested evidence
images, suppresses wrapper screenshots, groups duplicates, and builds the
source bundle handoff for Stage 2.5 and later structured extraction stages.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import hashlib
import re

from optisweep_incidence_ingestion.ocr import (
    TesseractOCRClient,
    normalize_ocr_text,
    normalize_whitespace,
    ocr_text_hash,
)
from optisweep_incidence_ingestion.services.ids import make_artifact_id
from optisweep_incidence_ingestion.stage1_source_package import build_incident_source_ref
from optisweep_incidence_ingestion.utils.json_utils import read_json, write_json


@dataclass(frozen=True)
class ImageHash:
    average_hash: str
    width: int
    height: int


def prepare_generated_image_dir(path: Path) -> None:
    """Clear a Stage 2 managed image directory before regeneration."""
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.is_file():
            child.unlink()


def extract_incident_ocr_artifacts(
    source_package_path: str | Path,
    source_pdf: str | Path,
    output_dir: str | Path,
    ocr_backend: str = "tesseract",
    tesseract_command: str | None = None,
    render_zoom: float = 3.0,
    min_crop_area_ratio: float = 0.05,
    include_detected_crops: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    try:
        import cv2  # type: ignore
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyMuPDF and OpenCV are required for incident Stage 2.") from exc

    package = read_json(source_package_path)
    pdf_path = Path(source_pdf)
    output_path = Path(output_dir)
    pages_dir = output_path / "images" / "pages"
    embedded_dir = output_path / "images" / "embedded"
    crops_dir = output_path / "images" / "crops"
    for image_dir in (pages_dir, embedded_dir, crops_dir):
        prepare_generated_image_dir(image_dir)

    ocr_client = _build_ocr_client(ocr_backend, tesseract_command)
    artifacts: list[dict[str, Any]] = []
    page_inventory: list[dict[str, Any]] = []
    warnings: list[str] = []
    image_hashes: dict[str, ImageHash] = {}

    with fitz.open(pdf_path) as document:
        for page_index in range(len(document)):
            page_number = page_index + 1
            page = document[page_index]
            page_image_path = pages_dir / f"case_{package['source_case_id']}_page_{page_number:03d}.png"
            pixmap = page.get_pixmap(matrix=fitz.Matrix(render_zoom, render_zoom), alpha=False)
            pixmap.save(page_image_path)

            page_ocr = _ocr_image(ocr_client, page_image_path, warnings, page_number, "rendered_page")
            page_type = classify_incident_artifact(page_ocr["text"])
            page_image_infos = page.get_images(full=True)
            source_refs = [
                build_incident_source_ref(
                    source_id=package["source_id"],
                    source_title=package["source_title"],
                    ingestion_batch_id=package["ingestion_batch_id"],
                    case_id=package["source_case_id"],
                    page_number=page_number,
                    quote_or_summary=_source_summary_from_ocr(page_ocr["text"]),
                )
            ]

            embedded_artifacts, embedded_warnings = extract_embedded_image_artifacts(
                document=document,
                page=page,
                page_number=page_number,
                package=package,
                embedded_dir=embedded_dir,
                ocr_client=ocr_client,
                image_hashes=image_hashes,
            )
            artifacts.extend(embedded_artifacts)
            warnings.extend(embedded_warnings)

            crop_artifacts: list[dict[str, Any]] = []
            should_try_fallback_crops = (
                not embedded_artifacts
                and not page_image_infos
                and page_type != "unknown_incident_evidence"
                and page_ocr["word_count"] >= 20
            )
            if include_detected_crops or should_try_fallback_crops:
                crop_artifacts = extract_crop_artifacts(
                    page_image_path=page_image_path,
                    page_number=page_number,
                    package=package,
                    crops_dir=crops_dir,
                    ocr_client=ocr_client,
                    image_hashes=image_hashes,
                    min_crop_area_ratio=min_crop_area_ratio,
                )
            artifacts.extend(crop_artifacts)

            page_inventory.append(
                {
                    "page_number": page_number,
                    "page_ref": f"case_{package['source_case_id']}:page_{page_number}",
                    "rendered_page_image": str(page_image_path),
                    "full_page_artifact_id": None,
                    "ocr_text": page_ocr["text"],
                    "ocr_confidence": page_ocr["confidence"],
                    "ocr_word_count": page_ocr["word_count"],
                    "ocr_text_hash": page_ocr["text_hash"],
                    "detected_page_type": page_type,
                    "embedded_artifact_ids": [artifact["artifact_id"] for artifact in embedded_artifacts],
                    "crop_artifact_ids": [artifact["artifact_id"] for artifact in crop_artifacts],
                    "stage2_status": "ocr_complete",
                    "source_refs": source_refs,
                }
            )

    duplicate_groups = group_duplicate_artifacts(artifacts, image_hashes)
    apply_duplicate_metadata(artifacts, duplicate_groups)
    source_artifacts = sorted(artifacts, key=lambda item: (item["page_number"], item["artifact_id"]))
    contact_sheet_path = output_path / "artifact_contact_sheet.jpg"
    try:
        build_artifact_contact_sheet(source_artifacts, contact_sheet_path)
    except Exception as exc:
        warnings.append(f"Could not build artifact contact sheet: {exc}")
    report = build_stage2_report(
        package,
        source_artifacts,
        page_inventory,
        duplicate_groups,
        warnings,
        ocr_backend,
        include_detected_crops,
    )

    enriched_package = dict(package)
    page_by_number = {page["page_number"]: page for page in page_inventory}
    for page in enriched_package.get("pages", []):
        inventory = page_by_number.get(page.get("page_number"))
        if not inventory:
            continue
        page.update(
            {
                "rendered_page_image_ref": inventory["rendered_page_image"],
                "ocr_text": inventory["ocr_text"],
                "ocr_confidence": inventory["ocr_confidence"],
                "stage2_status": inventory["stage2_status"],
                "detected_page_type": inventory["detected_page_type"],
                "artifact_ids": inventory["embedded_artifact_ids"] + inventory["crop_artifact_ids"],
            }
        )
    enriched_package["source_bundle"] = build_incident_source_bundle(
        package=enriched_package,
        page_inventory=page_inventory,
        source_artifacts=source_artifacts,
        report=report,
        output_path=output_path,
    )
    enriched_package["stage2_output_refs"] = {
        "page_inventory": str(output_path / "page_inventory.json"),
        "source_artifacts": str(output_path / "source_artifacts.json"),
        "artifact_extraction_report": str(output_path / "artifact_extraction_report.json"),
        "artifact_contact_sheet": str(output_path / "artifact_contact_sheet.jpg"),
    }

    write_json(output_path / "incident_source_package.json", enriched_package)
    write_json(output_path / "page_inventory.json", page_inventory)
    write_json(output_path / "source_artifacts.json", source_artifacts)
    write_json(output_path / "artifact_extraction_report.json", report)
    return source_artifacts, report


def extract_embedded_image_artifacts(
    *,
    document: Any,
    page: Any,
    page_number: int,
    package: dict[str, Any],
    embedded_dir: Path,
    ocr_client: TesseractOCRClient | None,
    image_hashes: dict[str, ImageHash],
) -> tuple[list[dict[str, Any]], list[str]]:
    artifacts: list[dict[str, Any]] = []
    warnings: list[str] = []
    for image_index, image_info in enumerate(page.get_images(full=True), start=1):
        xref = image_info[0]
        try:
            extracted = document.extract_image(xref)
        except Exception as exc:
            warnings.append(f"Could not extract embedded image xref {xref} on page {page_number}: {exc}")
            continue
        data = extracted.get("image") or b""
        width = int(extracted.get("width") or image_info[2] or 0)
        height = int(extracted.get("height") or image_info[3] or 0)
        ext = str(extracted.get("ext") or "png").lower()
        if width < 120 or height < 120 or len(data) < 2048:
            continue
        artifact_id = make_artifact_id(package["source_case_id"], page_number, "embedded_image", image_index)
        file_path = embedded_dir / f"{artifact_id}.{ext}"
        file_path.write_bytes(data)
        ocr = _ocr_image(ocr_client, file_path, warnings, page_number, f"embedded_image_{image_index}")
        image_type = classify_incident_artifact(ocr["text"])
        is_wrapper = is_likely_evidence_wrapper(ocr)
        nested_artifacts = extract_nested_media_artifacts(
            wrapper_image_path=file_path,
            page_number=page_number,
            package=package,
            embedded_dir=embedded_dir,
            ocr_client=ocr_client,
            image_hashes=image_hashes,
            warnings=warnings,
            parent_image_index=image_index,
            parent_ocr=ocr,
        )
        if nested_artifacts:
            artifacts.extend(nested_artifacts)
            file_path.unlink(missing_ok=True)
            continue
        if is_wrapper:
            warnings.append(
                f"Suppressed text wrapper image on page {page_number}; surrounding OCR remains in page_inventory."
            )
            file_path.unlink(missing_ok=True)
            continue
        image_hashes[artifact_id] = hash_image(file_path)
        source_refs = [
            build_incident_source_ref(
                source_id=package["source_id"],
                source_title=package["source_title"],
                ingestion_batch_id=package["ingestion_batch_id"],
                case_id=package["source_case_id"],
                page_number=page_number,
                artifact_id=artifact_id,
                quote_or_summary=_source_summary_from_ocr(ocr["text"]),
            )
        ]
        artifacts.append(
            build_artifact_record(
                package=package,
                artifact_id=artifact_id,
                artifact_type="incident_embedded_pdf_image",
                image_type=image_type,
                page_number=page_number,
                title=f"Case {package['source_case_id']} Page {page_number} Embedded Image {image_index}",
                storage_path=file_path,
                ocr=ocr,
                source_refs=source_refs,
                extraction_metadata={
                    "capture_method": "pdf_embedded_image_extract",
                    "pdf_xref": xref,
                    "embedded_image_index": image_index,
                    "width": width,
                    "height": height,
                    "file_size_bytes": len(data),
                    "promotion_reason": _promotion_reason(ocr["text"], image_type),
                },
            )
        )
    return artifacts, warnings


def extract_nested_media_artifacts(
    *,
    wrapper_image_path: Path,
    page_number: int,
    package: dict[str, Any],
    embedded_dir: Path,
    ocr_client: TesseractOCRClient | None,
    image_hashes: dict[str, ImageHash],
    warnings: list[str],
    parent_image_index: int,
    parent_ocr: dict[str, Any],
) -> list[dict[str, Any]]:
    if not is_likely_evidence_wrapper(parent_ocr):
        return []
    try:
        import cv2  # type: ignore
    except ImportError:
        return []

    image = cv2.imread(str(wrapper_image_path))
    if image is None:
        return []
    image_height, image_width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 45, 140)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    candidates: list[tuple[int, int, int, int, float]] = []
    image_area = image_width * image_height
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area_ratio = (w * h) / image_area
        if area_ratio < 0.006 or area_ratio > 0.28:
            continue
        if w < 140 or h < 90:
            continue
        if w / max(h, 1) > 8 or h / max(w, 1) > 6:
            continue
        if _near_duplicate_box((x, y, w, h), candidates):
            continue
        candidates.append((x, y, w, h, area_ratio))

    artifacts: list[dict[str, Any]] = []
    candidates = sorted(candidates, key=lambda item: item[4], reverse=True)[:10]
    for candidate in candidates:
        if len(artifacts) >= 6:
            break
        x, y, w, h, area_ratio = candidate
        left, top, right, bottom = expand_media_box(
            x=x,
            y=y,
            w=w,
            h=h,
            image_width=image_width,
            image_height=image_height,
        )
        crop = image[top:bottom, left:right]
        artifact_id = make_artifact_id(
            package["source_case_id"],
            page_number,
            "nested_image",
            len(artifacts) + 1,
        )
        output_path = embedded_dir / f"{artifact_id}.png"
        cv2.imwrite(str(output_path), crop)
        ocr = _ocr_image(
            ocr_client,
            output_path,
            warnings,
            page_number,
            f"nested_image_{parent_image_index}_{len(artifacts) + 1}",
        )
        image_type = classify_incident_artifact(ocr["text"])
        crop_width = right - left
        crop_height = bottom - top
        tile_boxes = find_media_tiles_in_text_strip(crop, cv2, ocr)
        if tile_boxes:
            output_path.unlink(missing_ok=True)
            for tile_left, tile_top, tile_right, tile_bottom in tile_boxes:
                if len(artifacts) >= 6:
                    break
                abs_left = left + tile_left
                abs_top = top + tile_top
                abs_right = left + tile_right
                abs_bottom = top + tile_bottom
                tile = image[abs_top:abs_bottom, abs_left:abs_right]
                tile_artifact_id = make_artifact_id(
                    package["source_case_id"],
                    page_number,
                    "nested_image",
                    len(artifacts) + 1,
                )
                tile_output_path = embedded_dir / f"{tile_artifact_id}.png"
                cv2.imwrite(str(tile_output_path), tile)
                tile_ocr = _ocr_image(
                    ocr_client,
                    tile_output_path,
                    warnings,
                    page_number,
                    f"nested_image_{parent_image_index}_{len(artifacts) + 1}_tile",
                )
                tile_image_type = classify_incident_artifact(tile_ocr["text"])
                if not is_promotable_text_strip_tile(tile_image_type, tile_ocr):
                    tile_output_path.unlink(missing_ok=True)
                    continue
                image_hashes[tile_artifact_id] = hash_image(tile_output_path)
                tile_source_refs = [
                    build_incident_source_ref(
                        source_id=package["source_id"],
                        source_title=package["source_title"],
                        ingestion_batch_id=package["ingestion_batch_id"],
                        case_id=package["source_case_id"],
                        page_number=page_number,
                        artifact_id=tile_artifact_id,
                        quote_or_summary=_source_summary_from_ocr(tile_ocr["text"]),
                    )
                ]
                artifacts.append(
                    build_artifact_record(
                        package=package,
                        artifact_id=tile_artifact_id,
                        artifact_type="incident_nested_message_image",
                        image_type=tile_image_type,
                        page_number=page_number,
                        title=f"Case {package['source_case_id']} Page {page_number} Nested Message Image {len(artifacts) + 1}",
                        storage_path=tile_output_path,
                        ocr=tile_ocr,
                        source_refs=tile_source_refs,
                        extraction_metadata={
                            "capture_method": "nested_media_tile_from_chat_text_strip",
                            "parent_image_path": str(wrapper_image_path),
                            "parent_image_index": parent_image_index,
                            "crop_box": {
                                "left": abs_left,
                                "top": abs_top,
                                "right": abs_right,
                                "bottom": abs_bottom,
                                "width": abs_right - abs_left,
                                "height": abs_bottom - abs_top,
                            },
                            "source_text_strip_box": {
                                "left": left,
                                "top": top,
                                "right": right,
                                "bottom": bottom,
                                "width": right - left,
                                "height": bottom - top,
                            },
                            "area_ratio": round(((abs_right - abs_left) * (abs_bottom - abs_top)) / image_area, 4),
                            "promotion_reason": "Promoted thumbnail image from Teams/chat text strip; surrounding chat OCR remains in page_inventory.",
                        },
                    )
                )
            continue
        if crop_height / max(crop_width, 1) > 1.35 and int(ocr.get("word_count") or 0) >= 5:
            output_path.unlink(missing_ok=True)
            continue
        if not is_meaningful_nested_media(image_type, ocr):
            output_path.unlink(missing_ok=True)
            continue
        image_hashes[artifact_id] = hash_image(output_path)
        source_refs = [
            build_incident_source_ref(
                source_id=package["source_id"],
                source_title=package["source_title"],
                ingestion_batch_id=package["ingestion_batch_id"],
                case_id=package["source_case_id"],
                page_number=page_number,
                artifact_id=artifact_id,
                quote_or_summary=_source_summary_from_ocr(ocr["text"]),
            )
        ]
        artifacts.append(
            build_artifact_record(
                package=package,
                artifact_id=artifact_id,
                artifact_type="incident_nested_message_image",
                image_type=image_type,
                page_number=page_number,
                title=f"Case {package['source_case_id']} Page {page_number} Nested Message Image {len(artifacts) + 1}",
                storage_path=output_path,
                ocr=ocr,
                source_refs=source_refs,
                extraction_metadata={
                    "capture_method": "nested_media_crop_from_chat_wrapper",
                    "parent_image_path": str(wrapper_image_path),
                    "parent_image_index": parent_image_index,
                    "crop_box": {
                        "left": left,
                        "top": top,
                        "right": right,
                        "bottom": bottom,
                        "width": right - left,
                        "height": bottom - top,
                    },
                    "area_ratio": round(area_ratio, 4),
                    "promotion_reason": "Promoted nested image from Teams/chat wrapper; wrapper image suppressed from source_artifacts.",
                },
            )
        )
    return artifacts


def extract_crop_artifacts(
    *,
    page_image_path: Path,
    page_number: int,
    package: dict[str, Any],
    crops_dir: Path,
    ocr_client: TesseractOCRClient | None,
    image_hashes: dict[str, ImageHash],
    min_crop_area_ratio: float,
) -> list[dict[str, Any]]:
    try:
        import cv2  # type: ignore
    except ImportError:
        return []

    image = cv2.imread(str(page_image_path))
    if image is None:
        return []
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 160)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    candidates: list[tuple[int, int, int, int, float]] = []
    page_area = width * height
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area_ratio = (w * h) / page_area
        if area_ratio < min_crop_area_ratio:
            continue
        if w < 350 or h < 220:
            continue
        if w > width * 0.95 and h > height * 0.95:
            continue
        if _near_duplicate_box((x, y, w, h), candidates):
            continue
        candidates.append((x, y, w, h, area_ratio))
    candidates = sorted(candidates, key=lambda box: (box[4] > 0.55, box[4]), reverse=False)[:8]

    artifacts: list[dict[str, Any]] = []
    warnings: list[str] = []
    for index, (x, y, w, h, area_ratio) in enumerate(candidates, start=1):
        left, top, right, bottom = expand_crop_box(
            x=x,
            y=y,
            w=w,
            h=h,
            page_width=width,
            page_height=height,
        )
        crop = image[top:bottom, left:right]
        artifact_id = make_artifact_id(package["source_case_id"], page_number, "detected_region", index)
        file_path = crops_dir / f"{artifact_id}.png"
        cv2.imwrite(str(file_path), crop)
        ocr = _ocr_image(ocr_client, file_path, warnings, page_number, f"detected_region_{index}")
        image_type = classify_incident_artifact(ocr["text"])
        if ocr["word_count"] < 4 and area_ratio < 0.18 and image_type == "unknown_incident_evidence":
            file_path.unlink(missing_ok=True)
            continue
        image_hashes[artifact_id] = hash_image(file_path)
        source_refs = [
            build_incident_source_ref(
                source_id=package["source_id"],
                source_title=package["source_title"],
                ingestion_batch_id=package["ingestion_batch_id"],
                case_id=package["source_case_id"],
                page_number=page_number,
                artifact_id=artifact_id,
                quote_or_summary=_source_summary_from_ocr(ocr["text"]),
            )
        ]
        artifacts.append(
            build_artifact_record(
                package=package,
                artifact_id=artifact_id,
                artifact_type="incident_detected_evidence_region",
                image_type=image_type,
                page_number=page_number,
                title=f"Case {package['source_case_id']} Page {page_number} Detected Evidence Region {index}",
                storage_path=file_path,
                ocr=ocr,
                source_refs=source_refs,
                extraction_metadata={
                    "capture_method": "opencv_detected_region_crop",
                    "crop_box": {"left": left, "top": top, "right": right, "bottom": bottom, "width": right - left, "height": bottom - top},
                    "area_ratio": round(area_ratio, 4),
                    "promotion_reason": _promotion_reason(ocr["text"], image_type),
                },
            )
        )
    return artifacts


def build_artifact_record(
    *,
    package: dict[str, Any],
    artifact_id: str,
    artifact_type: str,
    image_type: str,
    page_number: int,
    title: str,
    storage_path: Path,
    ocr: dict[str, Any],
    source_refs: list[dict[str, Any]],
    extraction_metadata: dict[str, Any],
) -> dict[str, Any]:
    ocr_text = ocr["text"]
    retrieval_text = normalize_whitespace(
        " ".join(
            part
            for part in [
                title,
                f"Source case {package['source_case_id']}, page {page_number}.",
                f"Detected evidence type: {image_type}.",
                f"OCR text: {ocr_text}" if ocr_text else "",
            ]
            if part
        )
    )
    return {
        "artifact_id": artifact_id,
        "source_id": package["source_id"],
        "source_type": package["source_type"],
        "source_case_id": package["source_case_id"],
        "source_title": package["source_title"],
        "ingestion_batch_id": package["ingestion_batch_id"],
        "source_package_id": package["source_package_id"],
        "artifact_type": artifact_type,
        "image_type": image_type,
        "title": title,
        "page_number": page_number,
        "storage_path": str(storage_path),
        "file_name": storage_path.name,
        "file_format": storage_path.suffix.lstrip(".").lower(),
        "ocr_text": ocr_text,
        "ocr_confidence": ocr["confidence"],
        "ocr_provenance": ocr["provenance"],
        "ocr_text_hash": ocr["text_hash"],
        "ocr_word_count": ocr["word_count"],
        "summary": summarize_artifact(image_type, ocr_text),
        "retrieval_text": retrieval_text,
        "what_to_look_at": what_to_look_at(image_type, ocr_text),
        "evidence_role": evidence_role(image_type, ocr_text),
        "validation_status": "needs_sme_review",
        "source_refs": source_refs,
        "duplicate_group_id": None,
        "duplicate_role": "unique",
        "linked_timeline_event_ids": [],
        "linked_runbook_candidate_ids": [],
        "extraction_metadata": extraction_metadata,
    }


def build_incident_source_bundle(
    *,
    package: dict[str, Any],
    page_inventory: list[dict[str, Any]],
    source_artifacts: list[dict[str, Any]],
    report: dict[str, Any],
    output_path: Path,
) -> dict[str, Any]:
    text_pages = [
        {
            "page_number": page["page_number"],
            "page_ref": page["page_ref"],
            "detected_page_type": page.get("detected_page_type"),
            "ocr_confidence": page.get("ocr_confidence"),
            "ocr_word_count": page.get("ocr_word_count"),
            "artifact_ids": (page.get("embedded_artifact_ids") or []) + (page.get("crop_artifact_ids") or []),
            "ocr_text": page.get("ocr_text") or "",
            "source_refs": page.get("source_refs") or [],
        }
        for page in page_inventory
        if page.get("ocr_text")
    ]
    artifact_manifest = [
        {
            "artifact_id": artifact["artifact_id"],
            "artifact_type": artifact["artifact_type"],
            "image_type": artifact["image_type"],
            "evidence_role": artifact.get("evidence_role"),
            "page_number": artifact["page_number"],
            "storage_path": artifact["storage_path"],
            "ocr_confidence": artifact.get("ocr_confidence"),
            "ocr_word_count": artifact.get("ocr_word_count"),
            "summary": artifact.get("summary"),
            "what_to_look_at": artifact.get("what_to_look_at") or [],
            "duplicate_group_id": artifact.get("duplicate_group_id"),
            "duplicate_role": artifact.get("duplicate_role"),
            "source_refs": artifact.get("source_refs") or [],
        }
        for artifact in source_artifacts
    ]
    wrapper_pages = [
        {
            "page_number": page["page_number"],
            "page_ref": page["page_ref"],
            "detected_page_type": page.get("detected_page_type"),
            "ocr_word_count": page.get("ocr_word_count"),
            "ocr_text": page.get("ocr_text") or "",
            "artifact_ids": (page.get("embedded_artifact_ids") or []) + (page.get("crop_artifact_ids") or []),
        }
        for page in page_inventory
        if page.get("detected_page_type") in {"teams_chat_screenshot", "salesforce_case_screenshot"}
        or is_likely_evidence_wrapper({"text": page.get("ocr_text") or "", "word_count": page.get("ocr_word_count") or 0})
    ]
    condensed_text = "\n\n".join(
        f"[page {page['page_number']} | {page.get('detected_page_type') or 'unknown'}]\n{normalize_whitespace(page.get('ocr_text') or '')}"
        for page in text_pages
    )
    return {
        "bundle_type": "incident_source_bundle",
        "schema_version": "0.1",
        "source_package_id": package["source_package_id"],
        "source_id": package["source_id"],
        "source_case_id": package["source_case_id"],
        "source_title": package["source_title"],
        "ingestion_batch_id": package["ingestion_batch_id"],
        "stage_status": {
            "stage_1": "complete",
            "stage_2": "complete",
            "ready_for_stage_2_5_artifact_enrichment": True,
            "ready_for_canonical_incident_and_timeline_extraction": True,
        },
        "handoff_contract": {
            "text_context_source": "source_bundle.text_context.pages[].ocr_text",
            "image_artifact_source": "source_bundle.artifact_manifest[].storage_path",
            "lineage_source": "source_bundle.*.source_refs",
            "detail_files": "source_bundle.file_refs",
            "wrapper_policy": "Teams/Salesforce wrapper screenshots are not promoted as image artifacts when they mostly contain surrounding text; their OCR remains in text_context.",
        },
        "text_context": {
            "page_count": len(page_inventory),
            "ocr_page_count": len(text_pages),
            "pages": text_pages,
            "condensed_source_text": condensed_text,
        },
        "artifact_manifest": artifact_manifest,
        "wrapper_text_context": {
            "policy": "Retain OCR text from wrapper pages for canonical incident, timeline, and runbook extraction; pass only clean nested images/photos/screenshots to image enrichment.",
            "pages": wrapper_pages,
        },
        "duplicate_groups": report.get("duplicate_groups") or [],
        "counts": {
            "page_inventory_count": len(page_inventory),
            "source_artifact_count": len(source_artifacts),
            "wrapper_text_page_count": len(wrapper_pages),
            "duplicate_group_count": report.get("duplicate_group_count", 0),
            "artifacts_by_image_type": report.get("artifacts_by_image_type") or {},
        },
        "file_refs": {
            "incident_source_package": str(output_path / "incident_source_package.json"),
            "page_inventory": str(output_path / "page_inventory.json"),
            "source_artifacts": str(output_path / "source_artifacts.json"),
            "artifact_extraction_report": str(output_path / "artifact_extraction_report.json"),
            "artifact_contact_sheet": str(output_path / "artifact_contact_sheet.jpg"),
        },
        "warnings": report.get("warnings") or [],
    }


def build_artifact_contact_sheet(
    artifacts: list[dict[str, Any]],
    output_path: Path,
    thumb_size: tuple[int, int] = (260, 180),
    columns: int = 3,
) -> None:
    """Write a compact visual review sheet for promoted Stage 2 artifacts."""
    if not artifacts:
        return
    from PIL import Image, ImageDraw, ImageFont

    rows = (len(artifacts) + columns - 1) // columns
    label_height = 58
    padding = 16
    cell_width = thumb_size[0] + padding * 2
    cell_height = thumb_size[1] + label_height + padding * 2
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, artifact in enumerate(artifacts):
        row, col = divmod(index, columns)
        x0 = col * cell_width + padding
        y0 = row * cell_height + padding
        image_path = Path(artifact["storage_path"])
        if not image_path.exists():
            continue
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            image.thumbnail(thumb_size)
            image_x = x0 + (thumb_size[0] - image.width) // 2
            image_y = y0 + (thumb_size[1] - image.height) // 2
            sheet.paste(image, (image_x, image_y))
        label = "\n".join(
            [
                artifact["artifact_id"],
                f"page {artifact['page_number']} | {artifact.get('image_type')}",
                f"{artifact.get('duplicate_role') or 'unique'} | OCR {artifact.get('ocr_confidence')}",
            ]
        )
        draw.multiline_text((x0, y0 + thumb_size[1] + 8), label, fill="black", font=font, spacing=3)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=88)


def classify_incident_artifact(text: str) -> str:
    lowered = normalize_ocr_text(text)
    if "get agv statuses" in lowered or "getagvstatuses" in lowered or "api dog" in lowered:
        return "api_client_screenshot"
    if "microsoft windows" in lowered and ("gwcmd" in lowered or "gateway" in lowered):
        return "ignition_command_screenshot"
    if "services local" in lowered or ("services" in lowered and "optisweep" in lowered):
        return "windows_services_screenshot"
    checks = [
        ("teams_chat_screenshot", ["microsoft teams", "reply", "edited", "meeting chat"]),
        ("salesforce_case_screenshot", ["salesforce", "case owner", "case number", "subject", "status"]),
        ("ignition_command_screenshot", ["gwcmd", "gateway command", "ignition", "restart"]),
        ("ignition_status_screenshot", ["ignition", "gateway", "status", "performance"]),
        ("windows_services_screenshot", ["services", "windows", "optisweep", "running", "startup type"]),
        ("api_client_screenshot", ["api dog", "get agv", "request", "response", "status code"]),
        ("memory_trend_screenshot", ["memory", "trend", "heap", "cpu", "uptime"]),
        ("rms_screenshot", ["rms", "robot", "agv", "state", "task"]),
        ("hmi_screenshot", ["hmi", "question", "hospital", "tote", "estop"]),
        ("command_window_screenshot", ["c windows", "cmd", "powershell", "command prompt"]),
    ]
    scores: list[tuple[int, str]] = []
    for image_type, terms in checks:
        score = sum(1 for term in terms if term in lowered)
        if score:
            scores.append((score, image_type))
    if scores:
        priority = {
            "api_client_screenshot": 9,
            "ignition_command_screenshot": 8,
            "windows_services_screenshot": 7,
            "ignition_status_screenshot": 6,
            "memory_trend_screenshot": 5,
            "salesforce_case_screenshot": 4,
            "teams_chat_screenshot": 3,
            "rms_screenshot": 2,
            "hmi_screenshot": 1,
            "command_window_screenshot": 0,
        }
        return sorted(scores, key=lambda item: (item[0], priority.get(item[1], 0)), reverse=True)[0][1]
    if re.search(r"\b\d{1,2}:\d{2}\s*(am|pm)\b", lowered) and len(lowered.split()) > 20:
        return "teams_chat_screenshot"
    if "agv" in lowered:
        return "agv_or_rms_screenshot"
    return "unknown_incident_evidence"


def is_likely_chat_wrapper(ocr: dict[str, Any]) -> bool:
    text = ocr.get("text") or ""
    lowered = normalize_ocr_text(text)
    word_count = int(ocr.get("word_count") or 0)
    timestamp_hits = len(re.findall(r"\b\d{1,2}\s*/\s*\d{1,2}\s+\d{1,2}\s*:?\d{2}\s*(?:am|pm)?\b", text, flags=re.IGNORECASE))
    name_hits = sum(
        1
        for name in [
            "zane bubb",
            "christopher white",
            "michael langley",
            "jinhao liu",
            "kevin buczek",
            "mitchel flynn",
            "darrell halterman",
        ]
        if name in lowered
    )
    chat_terms = ["reply", "called", "on the call", "meeting", "estop", "e stop", "rejoin", "troubleshooting"]
    return word_count >= 45 and (timestamp_hits >= 2 or name_hits >= 2 or sum(term in lowered for term in chat_terms) >= 2)


def is_likely_evidence_wrapper(ocr: dict[str, Any]) -> bool:
    text = ocr.get("text") or ""
    lowered = normalize_ocr_text(text)
    word_count = int(ocr.get("word_count") or 0)
    if is_likely_chat_wrapper(ocr):
        return True
    wrapper_terms = [
        "they can t",
        "they cant",
        "to all",
        "comment",
        "february",
        "case updated",
        "case created",
        "verify the optisweep service",
        "if no response is given",
        "once restarted",
        "restart ignition",
        "first estop",
        "trying to see if any service failed",
    ]
    screenshot_terms = [
        "memory trend",
        "gwcmd",
        "get agv statuses",
        "services local",
        "event viewer",
        "rms",
        "ignition",
        "optisweep",
    ]
    wrapper_score = sum(term in lowered for term in wrapper_terms)
    screenshot_score = sum(term in lowered for term in screenshot_terms)
    if word_count >= 55 and wrapper_score >= 1 and screenshot_score >= 1:
        return True
    return word_count >= 10 and ("to all" in lowered or "they can t" in lowered or "they cant" in lowered)


def is_meaningful_nested_media(image_type: str, ocr: dict[str, Any]) -> bool:
    if is_likely_evidence_wrapper(ocr):
        return False
    text = normalize_ocr_text(ocr.get("text") or "")
    if any(term in text for term in ["verify the optisweep service", "if no response is given", "wait for ignition", "restart ignition running"]):
        return False
    if image_type in {"teams_chat_screenshot", "salesforce_case_screenshot"}:
        return False
    if image_type != "unknown_incident_evidence":
        return True
    media_terms = [
        "memory trend",
        "ignition",
        "gateway",
        "gwcmd",
        "api",
        "get agv",
        "services",
        "optisweep",
        "rms",
        "system errors",
        "agv errors",
        "14gb",
        "9gb",
        "5gb",
        "omb",
    ]
    return any(term in text for term in media_terms)


def is_promotable_text_strip_tile(image_type: str, ocr: dict[str, Any]) -> bool:
    if is_likely_evidence_wrapper(ocr):
        return False
    text = normalize_ocr_text(ocr.get("text") or "")
    if any(term in text for term in ["thinks there is", "removed agv", "which causing", "system stopped"]):
        return False
    if image_type in {"teams_chat_screenshot", "salesforce_case_screenshot"}:
        return False
    return True


def evidence_role(image_type: str, text: str) -> str:
    lowered = normalize_ocr_text(text)
    if image_type in {"hmi_screenshot", "rms_screenshot", "agv_or_rms_screenshot"}:
        return "symptom_or_state_evidence"
    if image_type in {"memory_trend_screenshot", "ignition_status_screenshot"}:
        return "diagnostic_evidence"
    if image_type in {"ignition_command_screenshot", "windows_services_screenshot"}:
        return "action_evidence"
    if image_type == "api_client_screenshot" or "confirm" in lowered or "response" in lowered:
        return "validation_evidence"
    if image_type in {"teams_chat_screenshot", "salesforce_case_screenshot"}:
        return "incident_context_evidence"
    return "unknown"


def summarize_artifact(image_type: str, text: str) -> str:
    snippet = _source_summary_from_ocr(text)
    if snippet:
        return f"{image_type.replace('_', ' ').title()} with OCR text: {snippet}"
    return f"{image_type.replace('_', ' ').title()} extracted from incident evidence."


def what_to_look_at(image_type: str, text: str) -> list[str]:
    items = {
        "teams_chat_screenshot": ["Visible message timestamps", "Actor names", "Action or diagnostic requests", "Embedded screenshot thumbnails"],
        "salesforce_case_screenshot": ["Case fields", "Status and timestamps", "Customer/site references", "Resolution notes"],
        "memory_trend_screenshot": ["Time range", "Memory trend shape", "Any visible threshold or crash indicator"],
        "ignition_command_screenshot": ["Exact command text", "Prompt/path context", "Restart confirmation or errors"],
        "api_client_screenshot": ["Request name or endpoint", "Response status/body", "Evidence that OptiSweep responded"],
        "windows_services_screenshot": ["Visible service name", "Service status", "Restart evidence"],
        "hmi_screenshot": ["Question marks or fault indicators", "Station/state context", "Visible HMI labels"],
        "rms_screenshot": ["AGV IDs or states", "Task/status columns", "Evidence of corrected state"],
    }
    return items.get(image_type, ["OCR text", "Visible UI labels", "Reviewer-confirmed incident relevance"])


def hash_image(path: Path, hash_size: int = 8) -> ImageHash:
    from PIL import Image

    image = Image.open(path).convert("L").resize((hash_size, hash_size))
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join("1" if pixel > avg else "0" for pixel in pixels)
    return ImageHash(average_hash=bits, width=image.width, height=image.height)


def group_duplicate_artifacts(
    artifacts: list[dict[str, Any]],
    image_hashes: dict[str, ImageHash],
    max_hamming_distance: int = 4,
) -> list[dict[str, Any]]:
    groups: list[list[str]] = []
    assigned: set[str] = set()
    artifact_ids = [artifact["artifact_id"] for artifact in artifacts if artifact["artifact_id"] in image_hashes]
    artifact_by_id = {artifact["artifact_id"]: artifact for artifact in artifacts}
    for artifact_id in artifact_ids:
        if artifact_id in assigned:
            continue
        group = [artifact_id]
        assigned.add(artifact_id)
        for other_id in artifact_ids:
            if other_id in assigned:
                continue
            if (
                hamming_distance(image_hashes[artifact_id].average_hash, image_hashes[other_id].average_hash) <= max_hamming_distance
                and artifacts_are_textually_similar(artifact_by_id[artifact_id], artifact_by_id[other_id])
            ):
                group.append(other_id)
                assigned.add(other_id)
        if len(group) > 1:
            groups.append(group)

    duplicate_groups: list[dict[str, Any]] = []
    for index, group in enumerate(groups, start=1):
        primary_id = sorted(
            group,
            key=lambda item: (
                artifact_by_id[item].get("ocr_confidence") or 0,
                artifact_by_id[item].get("ocr_word_count") or 0,
                Path(artifact_by_id[item]["storage_path"]).stat().st_size if Path(artifact_by_id[item]["storage_path"]).exists() else 0,
            ),
            reverse=True,
        )[0]
        duplicate_groups.append(
            {
                "duplicate_group_id": f"dup_incident_{index:03d}",
                "primary_artifact_id": primary_id,
                "artifact_ids": group,
                "group_size": len(group),
                "grouping_method": "average_hash_hamming_distance",
                "max_hamming_distance": max_hamming_distance,
            }
        )
    return duplicate_groups


def apply_duplicate_metadata(artifacts: list[dict[str, Any]], duplicate_groups: list[dict[str, Any]]) -> None:
    artifact_by_id = {artifact["artifact_id"]: artifact for artifact in artifacts}
    for group in duplicate_groups:
        for artifact_id in group["artifact_ids"]:
            artifact = artifact_by_id.get(artifact_id)
            if not artifact:
                continue
            artifact["duplicate_group_id"] = group["duplicate_group_id"]
            artifact["duplicate_role"] = "primary" if artifact_id == group["primary_artifact_id"] else "duplicate"
            artifact["extraction_metadata"]["duplicate_group_primary_artifact_id"] = group["primary_artifact_id"]


def hamming_distance(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right)) + abs(len(left) - len(right))


def expand_media_box(
    *,
    x: int,
    y: int,
    w: int,
    h: int,
    image_width: int,
    image_height: int,
) -> tuple[int, int, int, int]:
    margin_x = max(8, int(w * 0.025))
    margin_top = max(8, int(h * 0.08))
    margin_bottom = max(6, int(h * 0.04))
    left = max(0, x - margin_x)
    top = max(0, y - margin_top)
    right = min(image_width, x + w + margin_x)
    bottom = min(image_height, y + h + margin_bottom)
    return left, top, right, bottom


def find_media_tiles_in_text_strip(crop: Any, cv2: Any, ocr: dict[str, Any]) -> list[tuple[int, int, int, int]]:
    height, width = crop.shape[:2]
    word_count = int(ocr.get("word_count") or 0)
    if word_count < 5 or width / max(height, 1) < 3.0:
        return []

    text = normalize_ocr_text(ocr.get("text") or "")
    strip_terms = [
        "thinks there is",
        "removed agv",
        "optisweep service is crashed",
        "which causing",
        "system stopped",
    ]
    if not any(term in text for term in strip_terms):
        return []

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray, 246, 255, cv2.THRESH_BINARY_INV)[1]
    text_band = max(22, int(height * 0.22))
    mask[:text_band, :] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes: list[tuple[int, int, int, int, float]] = []
    crop_area = width * height
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area_ratio = (w * h) / crop_area
        if area_ratio < 0.06 or area_ratio > 0.45:
            continue
        if w < 70 or h < 55:
            continue
        if h / max(height, 1) < 0.38:
            continue
        if w / max(width, 1) > 0.65:
            continue
        if _near_duplicate_box((x, y, w, h), boxes):
            continue
        boxes.append((x, y, w, h, area_ratio))

    expanded: list[tuple[int, int, int, int]] = []
    for x, y, w, h, _ in sorted(boxes, key=lambda item: (item[1], item[0])):
        margin = 4
        expanded.append(
            (
                max(0, x - margin),
                max(0, y - margin),
                min(width, x + w + margin),
                min(height, y + h + margin),
            )
        )
    return expanded


def expand_crop_box(
    *,
    x: int,
    y: int,
    w: int,
    h: int,
    page_width: int,
    page_height: int,
    min_width_ratio: float = 0.70,
    min_height_ratio: float = 0.32,
) -> tuple[int, int, int, int]:
    """Expand tight contour crops into reviewer-friendly evidence windows."""
    margin_x = max(96, int(w * 0.18), int(page_width * 0.06))
    margin_y = max(96, int(h * 0.18), int(page_height * 0.045))
    left = max(0, x - margin_x)
    top = max(0, y - margin_y)
    right = min(page_width, x + w + margin_x)
    bottom = min(page_height, y + h + margin_y)

    min_width = int(page_width * min_width_ratio)
    min_height = int(page_height * min_height_ratio)
    if right - left < min_width:
        extra = min_width - (right - left)
        grow_left = extra // 2
        grow_right = extra - grow_left
        left = max(0, left - grow_left)
        right = min(page_width, right + grow_right)
        if right - left < min_width:
            if left == 0:
                right = min(page_width, min_width)
            elif right == page_width:
                left = max(0, page_width - min_width)
    if bottom - top < min_height:
        extra = min_height - (bottom - top)
        grow_top = extra // 2
        grow_bottom = extra - grow_top
        top = max(0, top - grow_top)
        bottom = min(page_height, bottom + grow_bottom)
        if bottom - top < min_height:
            if top == 0:
                bottom = min(page_height, min_height)
            elif bottom == page_height:
                top = max(0, page_height - min_height)
    return left, top, right, bottom


def artifacts_are_textually_similar(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left.get("image_type") != right.get("image_type"):
        return False
    left_tokens = set(normalize_ocr_text(left.get("ocr_text") or "").split())
    right_tokens = set(normalize_ocr_text(right.get("ocr_text") or "").split())
    if not left_tokens and not right_tokens:
        return True
    if min(len(left_tokens), len(right_tokens)) < 5:
        return left.get("ocr_text_hash") == right.get("ocr_text_hash")
    overlap = len(left_tokens & right_tokens)
    similarity = overlap / max(len(left_tokens), len(right_tokens))
    return similarity >= 0.62


def build_stage2_report(
    package: dict[str, Any],
    artifacts: list[dict[str, Any]],
    page_inventory: list[dict[str, Any]],
    duplicate_groups: list[dict[str, Any]],
    warnings: list[str],
    ocr_backend: str,
    include_detected_crops: bool,
) -> dict[str, Any]:
    by_type = Counter(artifact["image_type"] for artifact in artifacts)
    low_ocr = [
        artifact["artifact_id"]
        for artifact in artifacts
        if artifact.get("ocr_confidence") is not None and artifact["ocr_confidence"] < 55
    ]
    return {
        "source_package_id": package["source_package_id"],
        "source_id": package["source_id"],
        "source_case_id": package["source_case_id"],
        "ingestion_batch_id": package["ingestion_batch_id"],
        "stage": "stage_2_ocr_and_evidence_artifact_extraction",
        "ocr_backend": ocr_backend,
        "detected_crop_mode": "enabled" if include_detected_crops else "fallback_only",
        "page_count": len(page_inventory),
        "page_inventory_count": len(page_inventory),
        "total_artifacts_created": len(artifacts),
        "artifacts_by_image_type": dict(sorted(by_type.items())),
        "full_page_artifact_count": sum(1 for artifact in artifacts if artifact["artifact_type"] == "incident_full_page_evidence"),
        "embedded_pdf_image_artifact_count": sum(1 for artifact in artifacts if artifact["artifact_type"] == "incident_embedded_pdf_image"),
        "nested_message_image_artifact_count": sum(1 for artifact in artifacts if artifact["artifact_type"] == "incident_nested_message_image"),
        "detected_region_artifact_count": sum(1 for artifact in artifacts if artifact["artifact_type"] == "incident_detected_evidence_region"),
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_groups": duplicate_groups,
        "low_ocr_confidence_artifact_ids": low_ocr,
        "warnings": warnings + _quality_warnings(page_inventory, artifacts),
        "validation_errors": [],
    }


def _build_ocr_client(ocr_backend: str, tesseract_command: str | None) -> TesseractOCRClient | None:
    backend = (ocr_backend or "none").strip().lower()
    if backend == "none":
        return None
    if backend == "tesseract":
        return TesseractOCRClient(command=tesseract_command)
    raise ValueError("Unsupported OCR backend. Use 'none' or 'tesseract'.")


def _ocr_image(
    ocr_client: TesseractOCRClient | None,
    image_path: Path,
    warnings: list[str],
    page_number: int,
    context: str,
) -> dict[str, Any]:
    if ocr_client is None:
        return {"text": "", "confidence": None, "provenance": None, "word_count": 0, "text_hash": None}
    try:
        result = ocr_client.extract(image_path)
    except RuntimeError as exc:
        warnings.append(f"OCR failed for page {page_number} {context}: {exc}")
        return {"text": "", "confidence": None, "provenance": None, "word_count": 0, "text_hash": None}
    return {
        "text": result.text,
        "confidence": result.confidence,
        "provenance": result.provenance,
        "word_count": result.word_count,
        "text_hash": ocr_text_hash(result.text),
    }


def _source_summary_from_ocr(text: str, limit: int = 280) -> str | None:
    cleaned = normalize_whitespace(text)
    if not cleaned:
        return None
    if len(cleaned) <= limit:
        return cleaned
    cut = cleaned.rfind(" ", 0, limit)
    return cleaned[: cut if cut > 80 else limit].rstrip() + "..."


def _promotion_reason(text: str, image_type: str) -> str:
    if image_type != "unknown_incident_evidence":
        return f"Promoted because OCR/classification suggests {image_type}."
    if len(normalize_ocr_text(text).split()) >= 8:
        return "Promoted because OCR found reviewable incident text."
    return "Promoted as source evidence container for audit/review."


def _near_duplicate_box(candidate: tuple[int, int, int, int], boxes: list[tuple[int, int, int, int, float]]) -> bool:
    x, y, w, h = candidate
    for bx, by, bw, bh, _ in boxes:
        inter_left = max(x, bx)
        inter_top = max(y, by)
        inter_right = min(x + w, bx + bw)
        inter_bottom = min(y + h, by + bh)
        inter_area = max(0, inter_right - inter_left) * max(0, inter_bottom - inter_top)
        smaller = min(w * h, bw * bh)
        area = w * h
        other_area = bw * bh
        size_ratio = min(area, other_area) / max(area, other_area)
        if smaller and inter_area / smaller > 0.75 and size_ratio > 0.65:
            return True
    return False


def _quality_warnings(page_inventory: list[dict[str, Any]], artifacts: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    if any((page.get("ocr_word_count") or 0) == 0 for page in page_inventory):
        warnings.append("One or more pages produced no OCR words; inspect rendered page images manually.")
    page_text = normalize_ocr_text(" ".join(page.get("ocr_text") or "" for page in page_inventory))
    has_teams_context = "teams chat data" in page_text or "support chat" in page_text
    has_salesforce_context = "salesforce case data" in page_text or "case created" in page_text
    if not any(artifact["image_type"] == "teams_chat_screenshot" for artifact in artifacts):
        if has_teams_context:
            warnings.append("Teams chat wrapper text is retained in page_inventory; wrapper screenshots were not promoted as source_artifacts.")
        else:
            warnings.append("No Teams chat screenshot was classified; check OCR quality or classification rules.")
    if not any(artifact["image_type"] == "salesforce_case_screenshot" for artifact in artifacts):
        if has_salesforce_context:
            warnings.append("Salesforce case wrapper text is retained in page_inventory; wrapper screenshots were not promoted as source_artifacts.")
        else:
            warnings.append("No Salesforce case screenshot was classified; check OCR quality or classification rules.")
    return warnings
