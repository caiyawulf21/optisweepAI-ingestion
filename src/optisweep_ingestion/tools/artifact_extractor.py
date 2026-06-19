"""Deterministic Stage 2 source artifact extraction for source knowledge extraction."""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from optisweep_ingestion.schemas.source_artifact import SourceArtifact
from optisweep_ingestion.schemas.source_bundle import SourceBundle, SourceFigureRef, SourcePage
from optisweep_ingestion.services.id_generator import (
    make_artifact_id_from_figure,
    make_artifact_id_from_page_image,
)
from optisweep_ingestion.services.source_ref_service import build_source_ref, lineage_from_bundle
from optisweep_ingestion.tools.source_bundle_loader import load_source_bundle
from optisweep_ingestion.utils.json_utils import write_json


@dataclass
class ExtractedImage:
    page_number: int
    image_index: int
    width: int
    height: int
    ext: str
    data: bytes
    digest: str


def extract_source_artifacts(
    source_bundle_path: str | Path,
    source_pdf: str | Path,
    output_dir: str | Path,
    min_width: int = 100,
    min_height: int = 100,
    min_file_size: int = 1024,
    duplicate_page_threshold: int = 12,
) -> tuple[list[SourceArtifact], dict[str, Any]]:
    bundle = load_source_bundle(source_bundle_path)
    output_path = Path(output_dir)
    images_dir = output_path / "images"
    fallback_pages_dir = images_dir / "fallback_pages"
    images_dir.mkdir(parents=True, exist_ok=True)
    fallback_pages_dir.mkdir(parents=True, exist_ok=True)

    extracted, pdf_warnings, total_pages = extract_pdf_images(source_pdf)
    useful_images, skipped_images = filter_useful_images(
        extracted,
        min_width=min_width,
        min_height=min_height,
        min_file_size=min_file_size,
        duplicate_page_threshold=duplicate_page_threshold,
    )
    images_by_page: dict[int, list[ExtractedImage]] = defaultdict(list)
    for image in useful_images:
        images_by_page[image.page_number].append(image)
    for page_images in images_by_page.values():
        page_images.sort(key=lambda item: item.image_index)

    artifacts: list[SourceArtifact] = []
    low_confidence_matches: list[dict[str, Any]] = []
    saved_count = 0
    lineage = lineage_from_bundle(bundle)
    for page_number, figure_refs in _figure_refs_by_page(bundle).items():
        page_images = images_by_page.get(page_number, [])
        page = _page_by_number(bundle).get(page_number)
        for index, figure_ref in enumerate(figure_refs):
            image = page_images[index] if index < len(page_images) else None
            confidence = _matching_confidence(figure_refs, page_images)
            metadata = {
                "image_extraction_status": "saved" if image else "missing_or_not_extracted",
                "matching_confidence": confidence,
            }
            if confidence == "low":
                metadata["matching_notes"] = "Multiple figures/images on page; matched by order."
                metadata["needs_visual_review"] = True
                low_confidence_matches.append(
                    {"figure_id": figure_ref.figure_id, "page_number": page_number, "notes": metadata["matching_notes"]}
                )
            storage_path = None
            file_name = None
            file_format = None
            if image:
                artifact_id_for_file = make_artifact_id_from_figure(
                    lineage.source_id,
                    lineage.source_type,
                    figure_ref.figure_number or figure_ref.figure_id,
                    figure_ref.title,
                )
                file_name = f"{artifact_id_for_file}.{image.ext}"
                storage_path = str(images_dir / file_name)
                Path(storage_path).write_bytes(image.data)
                file_format = image.ext
                saved_count += 1
            else:
                fallback_id = make_artifact_id_from_figure(
                    lineage.source_id,
                    lineage.source_type,
                    figure_ref.figure_number or figure_ref.figure_id,
                    figure_ref.title,
                )
                file_name = f"{fallback_id}_page_{page_number}.png"
                storage_path = str(fallback_pages_dir / file_name)
                rendered = render_pdf_page(source_pdf, page_number, storage_path)
                if rendered:
                    file_format = "png"
                    saved_count += 1
                    metadata.update(
                        {
                            "image_extraction_status": "page_render_fallback",
                            "fallback_type": "full_page_render",
                            "needs_crop_review": True,
                            "needs_visual_review": True,
                        }
                    )
                else:
                    storage_path = None
                    file_name = None
                    metadata["fallback_needed"] = True
            artifacts.append(build_artifact_from_figure_ref(bundle, figure_ref, page, storage_path, file_name, file_format, metadata))

    figure_pages = set(_figure_refs_by_page(bundle))
    for page_number, page_images in images_by_page.items():
        if page_number in figure_pages:
            continue
        page = _page_by_number(bundle).get(page_number)
        for image in page_images:
            artifact_id = make_artifact_id_from_page_image(
                lineage.source_id,
                lineage.source_type,
                page_number,
                image.image_index,
            )
            file_name = f"{artifact_id}.{image.ext}"
            storage_path = str(images_dir / file_name)
            Path(storage_path).write_bytes(image.data)
            saved_count += 1
            artifacts.append(build_artifact_from_page_image(bundle, page, image, storage_path, file_name))

    report = build_artifact_extraction_report(
        bundle=bundle,
        pdf_path=str(source_pdf),
        total_pdf_pages=total_pages,
        total_embedded_images_found=len(extracted),
        total_images_saved=saved_count,
        artifacts=artifacts,
        missing_figure_images=[
            artifact.model_dump(mode="json")
            for artifact in artifacts
            if artifact.figure_id and not artifact.storage_path
        ],
        low_confidence_matches=low_confidence_matches,
        skipped_images=skipped_images,
        warnings=pdf_warnings,
    )
    write_json(output_path / "source_artifacts.json", artifacts)
    write_json(output_path / "artifact_extraction_report.json", report)
    return artifacts, report


def extract_pdf_images(source_pdf: str | Path) -> tuple[list[ExtractedImage], list[str], int]:
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required for Stage 2 image extraction. Install pymupdf.") from exc

    images: list[ExtractedImage] = []
    warnings: list[str] = []
    with fitz.open(source_pdf) as document:
        for page_index in range(len(document)):
            page = document[page_index]
            for image_index, image_info in enumerate(page.get_images(full=True), start=1):
                xref = image_info[0]
                try:
                    extracted = document.extract_image(xref)
                except Exception as exc:  # pragma: no cover - depends on PDF internals
                    warnings.append(f"Could not extract image xref {xref} on page {page_index + 1}: {exc}")
                    continue
                data = extracted.get("image") or b""
                digest = hashlib.sha256(data).hexdigest()
                images.append(
                    ExtractedImage(
                        page_number=page_index + 1,
                        image_index=image_index,
                        width=int(extracted.get("width") or image_info[2] or 0),
                        height=int(extracted.get("height") or image_info[3] or 0),
                        ext=str(extracted.get("ext") or "png").lower(),
                        data=data,
                        digest=digest,
                    )
                )
        return images, warnings, len(document)


def render_pdf_page(source_pdf: str | Path, page_number: int, output_path: str | Path, zoom: float = 2.0) -> bool:
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required for Stage 2 page fallback rendering. Install pymupdf.") from exc

    try:
        with fitz.open(source_pdf) as document:
            if page_number < 1 or page_number > len(document):
                return False
            page = document[page_number - 1]
            matrix = fitz.Matrix(zoom, zoom)
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            pixmap.save(output_path)
            return True
    except Exception:
        return False


def filter_useful_images(
    images: list[ExtractedImage],
    min_width: int = 100,
    min_height: int = 100,
    min_file_size: int = 1024,
    duplicate_page_threshold: int = 12,
) -> tuple[list[ExtractedImage], list[dict[str, Any]]]:
    digest_pages: dict[str, set[int]] = defaultdict(set)
    for image in images:
        digest_pages[image.digest].add(image.page_number)
    useful: list[ExtractedImage] = []
    skipped: list[dict[str, Any]] = []
    for image in images:
        reason = None
        if image.width < min_width or image.height < min_height:
            reason = "below_min_dimensions"
        elif len(image.data) < min_file_size:
            reason = "below_min_file_size"
        elif len(digest_pages[image.digest]) >= duplicate_page_threshold:
            reason = "duplicate_on_many_pages"
        if reason:
            skipped.append(
                {
                    "page_number": image.page_number,
                    "image_index": image.image_index,
                    "width": image.width,
                    "height": image.height,
                    "file_size": len(image.data),
                    "reason": reason,
                }
            )
            continue
        useful.append(image)
    return useful, skipped


def build_artifact_from_figure_ref(
    bundle: SourceBundle,
    figure_ref: SourceFigureRef,
    page: SourcePage | None = None,
    storage_path: str | None = None,
    file_name: str | None = None,
    file_format: str | None = None,
    extraction_metadata: dict[str, Any] | None = None,
) -> SourceArtifact:
    lineage = lineage_from_bundle(bundle)
    title = figure_ref.title or _title_from_caption(figure_ref.caption_text, figure_ref.figure_number)
    nearby_text = get_nearby_text(page.text if page else "", figure_ref.caption_text or title)
    return SourceArtifact(
        artifact_id=make_artifact_id_from_figure(
            lineage.source_id,
            lineage.source_type,
            figure_ref.figure_number or figure_ref.figure_id,
            title,
        ),
        source_id=lineage.source_id,
        source_type=lineage.source_type,
        source_title=lineage.source_title,
        source_version=lineage.source_version,
        ingestion_batch_id=lineage.ingestion_batch_id,
        source_document_id=bundle.source_document.source_document_id,
        source_bundle_id=bundle.source_bundle_id,
        artifact_type="manual_figure",
        image_type=classify_image_type(" ".join(part for part in [title, figure_ref.caption_text] if part)),
        title=title,
        figure_id=figure_ref.figure_id,
        figure_number=figure_ref.figure_number,
        page_number=figure_ref.page_number,
        section_id=figure_ref.section_id,
        storage_path=storage_path,
        file_name=file_name,
        file_format=file_format,
        caption_text=figure_ref.caption_text,
        nearby_text=nearby_text,
        retrieval_text=build_retrieval_text(bundle, figure_ref.figure_number, title, figure_ref.page_number, figure_ref.section_id, nearby_text),
        summary=build_summary(bundle, title, figure_ref.section_id, nearby_text),
        source_refs=[
            build_source_ref(
                lineage,
                page=figure_ref.page_number,
                section_id=figure_ref.section_id,
                figure_id=figure_ref.figure_id,
                figure_number=figure_ref.figure_number,
                quote_or_summary=(
                    f"{figure_ref.figure_number or 'Artifact'} appears on page {figure_ref.page_number}"
                    + (f" in section {figure_ref.section_id}." if figure_ref.section_id else ".")
                ),
            )
        ],
        extraction_metadata=extraction_metadata or {},
    )


def build_artifact_from_page_image(
    bundle: SourceBundle,
    page: SourcePage | None,
    image: ExtractedImage,
    storage_path: str,
    file_name: str,
) -> SourceArtifact:
    lineage = lineage_from_bundle(bundle)
    nearby_text = get_nearby_text(page.text if page else "", None)
    section_id = page.section_id if page else None
    return SourceArtifact(
        artifact_id=make_artifact_id_from_page_image(
            lineage.source_id,
            lineage.source_type,
            image.page_number,
            image.image_index,
        ),
        source_id=lineage.source_id,
        source_type=lineage.source_type,
        source_title=lineage.source_title,
        source_version=lineage.source_version,
        ingestion_batch_id=lineage.ingestion_batch_id,
        source_document_id=bundle.source_document.source_document_id,
        source_bundle_id=bundle.source_bundle_id,
        artifact_type="manual_page_image",
        image_type=classify_image_type(nearby_text),
        page_number=image.page_number,
        section_id=section_id,
        storage_path=storage_path,
        file_name=file_name,
        file_format=image.ext,
        nearby_text=nearby_text,
        retrieval_text=build_retrieval_text(bundle, None, None, image.page_number, section_id, nearby_text),
        summary=build_summary(bundle, None, section_id, nearby_text),
        source_refs=[
            build_source_ref(
                lineage,
                page=image.page_number,
                section_id=section_id,
            )
        ],
        extraction_metadata={"image_extraction_status": "saved", "matching_confidence": "page_only"},
    )


def classify_image_type(text: str | None) -> str:
    lowered = (text or "").lower()
    maintenance_terms = [
        "sensor",
        "gearbox",
        "pneumatic",
        "cable",
        "tipper components",
        "plastic blocks",
        "end stop",
        "clink controller",
        "controller pca",
        "tip pca",
        "pca connections",
        "teknic",
        "sd motor",
        "timing pulley",
        "timing belt",
        "idler pulley",
        "flat-flex",
        "ffc",
        "clearlink",
        "clink connections",
        "counterbalance",
        "counter-balance",
        "valve",
        "cylinder",
        "motor replacement",
    ]
    if any(term in lowered for term in maintenance_terms):
        return "maintenance_diagram"
    if "hospital hmi" in lowered:
        return "hospital_station_screen"
    if "operator station hmi" in lowered:
        return "operator_station_screen"
    if any(
        term in lowered
        for term in [
            "building overview screen",
            "system overview screen",
            "system statistics screen",
            "api controls",
            "api screen",
            "pop-up screen",
            "cellio screen",
            "wcommand screen",
            "system in shut-down mode",
            "startup screen",
            "start-up screen",
        ]
    ):
        return "system_screen"
    if "agv" in lowered:
        return "agv_screen"
    if "rms" in lowered:
        return "rms_screenshot"
    if "hmi" in lowered:
        return "hmi_screenshot"
    if "diagram" in lowered:
        return "diagram"
    if "stacklight" in lowered or "push-button" in lowered or "push button" in lowered or "station" in lowered:
        return "photo"
    return "unknown"


def get_nearby_text(page_text: str, caption: str | None = None, limit: int = 1200) -> str:
    normalized = _normalize_text(page_text)
    if len(normalized) <= limit:
        return normalized
    if caption:
        caption_text = _normalize_text(caption)
        index = normalized.lower().find(caption_text.lower())
        if index >= 0:
            start = max(0, index - limit // 3)
            end = min(len(normalized), start + limit)
            return normalized[start:end].strip()
    return normalized[:limit].strip()


def build_retrieval_text(
    bundle: SourceBundle,
    ref_number: str | None,
    title: str | None,
    page_number: int | None,
    section_id: str | None,
    nearby_text: str | None,
) -> str:
    section_title = _section_title(bundle, section_id)
    label = f"{ref_number}: {title}" if ref_number and title else title or ref_number or "Manual page image"
    parts = [
        label + ".",
        f"Source: {bundle.source_document.title or bundle.source_document.source_document_id}",
        f"page {page_number}" if page_number else None,
        f"section {section_title}" if section_title else None,
        f"Nearby text: {nearby_text}" if nearby_text else None,
    ]
    return " ".join(part for part in parts if part)


def build_summary(bundle: SourceBundle, title: str | None, section_id: str | None, nearby_text: str | None) -> str:
    section_title = _section_title(bundle, section_id)
    subject = title or "This manual image"
    if section_title and nearby_text:
        return _truncate_cleanly(
            f"This manual figure appears in the {section_title} section and is associated with {subject}. "
            f"Nearby source text says: {nearby_text}",
            limit=850,
        )
    if section_title:
        return f"This manual figure appears in the {section_title} section and is associated with {subject}."
    return f"This source artifact is associated with {subject}."


def build_artifact_extraction_report(
    bundle: SourceBundle,
    pdf_path: str,
    total_pdf_pages: int,
    total_embedded_images_found: int,
    total_images_saved: int,
    artifacts: list[SourceArtifact],
    missing_figure_images: list[dict[str, Any]],
    low_confidence_matches: list[dict[str, Any]],
    skipped_images: list[dict[str, Any]],
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    lineage = lineage_from_bundle(bundle)
    by_image_type = Counter(artifact.image_type or "unknown" for artifact in artifacts)
    return {
        "source_id": lineage.source_id,
        "source_type": lineage.source_type,
        "ingestion_batch_id": lineage.ingestion_batch_id,
        "source_bundle_id": bundle.source_bundle_id,
        "source_document_id": bundle.source_document.source_document_id,
        "pdf_path": pdf_path,
        "total_pdf_pages": total_pdf_pages,
        "total_figure_refs": len(bundle.figure_refs),
        "total_embedded_images_found": total_embedded_images_found,
        "total_images_saved": total_images_saved,
        "total_artifacts_created": len(artifacts),
        "artifacts_with_saved_images": sum(1 for artifact in artifacts if artifact.storage_path),
        "artifacts_missing_images": sum(1 for artifact in artifacts if not artifact.storage_path),
        "artifacts_by_image_type": dict(sorted(by_image_type.items())),
        "missing_figure_images": missing_figure_images,
        "low_confidence_matches": low_confidence_matches,
        "skipped_image_summary": build_skipped_image_summary(skipped_images),
        "debug": {
            "skipped_images": skipped_images,
        },
        "warnings": warnings or [],
        "heartbeat_artifact_check": heartbeat_artifact_check(artifacts),
        "priority_artifact_check": priority_artifact_check(artifacts),
    }


def heartbeat_artifact_check(artifacts: list[SourceArtifact]) -> dict[str, Any]:
    artifact = next((item for item in artifacts if item.figure_id == "fig_4_22"), None)
    retrieval_text = artifact.retrieval_text if artifact else ""
    storage_path = Path(artifact.storage_path) if artifact and artifact.storage_path else None
    return {
        "figure_id": "fig_4_22",
        "expected_page": 52,
        "artifact_found": artifact is not None,
        "page_number": artifact.page_number if artifact else None,
        "section_id": artifact.section_id if artifact else None,
        "retrieval_text_contains_heartbeat": "heartbeat" in retrieval_text.lower(),
        "retrieval_text_contains_10_seconds": "10 seconds" in retrieval_text.lower(),
        "storage_path_exists": bool(storage_path and storage_path.exists()),
    }


def priority_artifact_check(artifacts: list[SourceArtifact]) -> dict[str, dict[str, Any]]:
    expected = {
        "fig_4_20": "Operator Station HMI Data Screen",
        "fig_4_22": "Heartbeat Stats",
        "fig_4_28": "Operator Station HMI Alarms Screen",
        "fig_4_30": "Hospital HMI Operations Screen",
        "fig_4_31": "Hospital HMI Add Tote Screen",
        "fig_4_32": "Hospital HMI Remove Tote Screen",
        "fig_5_2": "AGV Bump Fault Screen",
        "fig_5_4": "Faulted AGV with Tote Screen",
    }
    checks: dict[str, dict[str, Any]] = {}
    for figure_id, expected_title in expected.items():
        artifact = next((item for item in artifacts if item.figure_id == figure_id), None)
        storage_path = Path(artifact.storage_path) if artifact and artifact.storage_path else None
        checks[figure_id] = {
            "expected_title": expected_title,
            "artifact_found": artifact is not None,
            "artifact_id": artifact.artifact_id if artifact else None,
            "page_number": artifact.page_number if artifact else None,
            "image_type": artifact.image_type if artifact else None,
            "storage_path_exists": bool(storage_path and storage_path.exists()),
            "image_extraction_status": (artifact.extraction_metadata or {}).get("image_extraction_status") if artifact else None,
            "needs_visual_review": bool((artifact.extraction_metadata or {}).get("needs_visual_review")) if artifact else False,
        }
    return checks


def build_skipped_image_summary(skipped_images: list[dict[str, Any]]) -> dict[str, int]:
    summary: Counter[str] = Counter()
    for image in skipped_images:
        width = int(image.get("width") or 0)
        height = int(image.get("height") or 0)
        reason = str(image.get("reason") or "unknown")
        if reason == "below_min_dimensions" and width >= 500 and height < 120:
            summary["likely_repeated_header_footer"] += 1
        elif reason == "below_min_dimensions" and (width < 120 or height < 120):
            summary["tiny_icon"] += 1
        else:
            summary[reason] += 1
    return dict(sorted(summary.items()))


def _figure_refs_by_page(bundle: SourceBundle) -> dict[int, list[SourceFigureRef]]:
    grouped: dict[int, list[SourceFigureRef]] = defaultdict(list)
    for figure_ref in bundle.figure_refs:
        if figure_ref.page_number is not None:
            grouped[figure_ref.page_number].append(figure_ref)
    for refs in grouped.values():
        refs.sort(key=lambda ref: ref.figure_id)
    return grouped


def _page_by_number(bundle: SourceBundle) -> dict[int, SourcePage]:
    return {page.page_number: page for page in bundle.pages}


def _matching_confidence(figure_refs: list[SourceFigureRef], images: list[ExtractedImage]) -> str:
    if len(figure_refs) == 1 and len(images) == 1:
        return "high"
    if len(figure_refs) and len(images) and len(figure_refs) == len(images):
        return "low"
    return "low"


def _section_title(bundle: SourceBundle, section_id: str | None) -> str | None:
    if not section_id:
        return None
    section = next((item for item in bundle.sections if item.section_id == section_id), None)
    return section.title if section else section_id


def _title_from_caption(caption: str | None, ref_number: str | None) -> str | None:
    if not caption:
        return None
    title = caption
    if ref_number:
        title = re.sub(re.escape(ref_number), "", title, flags=re.IGNORECASE).strip(" :-")
    return title or None


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _truncate_cleanly(text: str, limit: int = 850) -> str:
    normalized = _normalize_text(text)
    if len(normalized) <= limit:
        return normalized
    sentence_cut = normalized.rfind(".", 0, limit)
    if sentence_cut >= int(limit * 0.55):
        return normalized[: sentence_cut + 1]
    word_cut = normalized.rfind(" ", 0, limit)
    if word_cut >= int(limit * 0.55):
        return normalized[:word_cut].rstrip() + "."
    return normalized[:limit].rstrip() + "."
