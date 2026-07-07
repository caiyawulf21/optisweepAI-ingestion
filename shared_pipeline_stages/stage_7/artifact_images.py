from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import hashlib
import html
import shutil

REPO_ROOT = Path(__file__).resolve().parents[2]

INGESTION_PACKAGES = (
    "operationalknowledgeingestion",
    "incidenceknowledgeingestion",
)


def collect_image_refs(runbook: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for bucket in (
        runbook.get("visual_references") or [],
        runbook.get("screens_or_images") or [],
    ):
        for ref in bucket:
            if not isinstance(ref, dict):
                continue
            artifact_id = str(ref.get("artifact_id") or "").strip()
            if artifact_id and artifact_id not in seen:
                seen.add(artifact_id)
                refs.append(ref)
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        for ref in step.get("screens_or_images") or []:
            if not isinstance(ref, dict):
                continue
            artifact_id = str(ref.get("artifact_id") or "").strip()
            if artifact_id and artifact_id not in seen:
                seen.add(artifact_id)
                refs.append(ref)
    return refs


@dataclass(frozen=True)
class ReviewImageFigure:
    artifact_id: str
    src: str
    caption: str
    found: bool


def build_review_image_figures(
    refs: list[Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_output_path: Path,
    repo_root: Path | None = None,
    asset_link_cache: dict[str, str] | None = None,
) -> list[ReviewImageFigure]:
    figures: list[ReviewImageFigure] = []
    cache = asset_link_cache if asset_link_cache is not None else {}
    root = repo_root or REPO_ROOT
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        artifact_id = str(ref.get("artifact_id") or "").strip()
        if not artifact_id or artifact_id in seen:
            continue
        seen.add(artifact_id)
        caption = _caption(ref)
        image_path = resolve_image_ref_path(ref, artifact_index=artifact_index, repo_root=root)
        if image_path and image_path.is_file():
            link = review_asset_link(artifact_id, image_path, review_output_path, cache)
            figures.append(
                ReviewImageFigure(
                    artifact_id=artifact_id,
                    src=link,
                    caption=caption,
                    found=True,
                )
            )
            continue
        figures.append(
            ReviewImageFigure(
                artifact_id=artifact_id,
                src="",
                caption=caption or "Image file not found",
                found=False,
            )
        )
    return figures


def render_image_markdown(
    refs: list[Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_markdown_path: Path,
    repo_root: Path | None = None,
    asset_link_cache: dict[str, str] | None = None,
) -> list[str]:
    lines: list[str] = []
    for figure in build_review_image_figures(
        refs,
        artifact_index=artifact_index,
        review_output_path=review_markdown_path,
        repo_root=repo_root,
        asset_link_cache=asset_link_cache,
    ):
        if figure.found:
            lines.extend([f"![{figure.artifact_id}]({figure.src})", ""])
            if figure.caption:
                lines.extend([f"*{figure.caption}*", ""])
            continue
        if figure.caption:
            lines.append(f"- `{figure.artifact_id}`: {figure.caption}")
        else:
            lines.append(f"- `{figure.artifact_id}` (image file not found)")
    return lines


def render_image_html(
    refs: list[Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    review_output_path: Path,
    repo_root: Path | None = None,
    asset_link_cache: dict[str, str] | None = None,
) -> list[str]:
    blocks: list[str] = []
    for figure in build_review_image_figures(
        refs,
        artifact_index=artifact_index,
        review_output_path=review_output_path,
        repo_root=repo_root,
        asset_link_cache=asset_link_cache,
    ):
        blocks.extend(_figure_to_html(figure))
    return blocks


def resolve_image_ref_path(
    ref: dict[str, Any],
    *,
    artifact_index: dict[str, dict[str, Any]] | None,
    repo_root: Path,
) -> Path | None:
    artifact_id = str(ref.get("artifact_id") or "").strip()
    artifact = (artifact_index or {}).get(artifact_id) if artifact_id else None
    raw_paths: list[str] = []
    if artifact:
        raw_paths.extend(
            [
                str(artifact.get("storage_path") or ""),
                str(artifact.get("image_ref") or ""),
                str(artifact.get("file_path") or ""),
            ]
        )
    raw_paths.extend(
        [
            str(ref.get("storage_path") or ""),
            str(ref.get("image_ref") or ""),
            str(ref.get("file_path") or ""),
        ]
    )
    for raw in raw_paths:
        path = resolve_artifact_image_path(raw, repo_root=repo_root)
        if path is not None:
            return path
    return None


def resolve_artifact_image_path(raw_path: str, *, repo_root: Path = REPO_ROOT) -> Path | None:
    cleaned = str(raw_path or "").strip()
    if not cleaned:
        return None
    normalized = Path(cleaned.replace("\\", "/"))
    candidates: list[Path] = [
        normalized,
        repo_root / normalized,
        Path.cwd() / normalized,
    ]
    for package in INGESTION_PACKAGES:
        package_root = repo_root / package
        candidates.append(package_root / normalized)
        parts = normalized.parts
        if parts and parts[0] == "data":
            candidates.append(package_root / normalized)
        if parts and parts[0] == package:
            candidates.append(repo_root / normalized)
            candidates.append(repo_root / Path(*parts[1:]))
    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved
    return None


def review_assets_dir(review_output_path: Path) -> Path:
    return review_output_path.resolve().parent / "assets"


def review_asset_link(
    artifact_id: str,
    image_path: Path,
    review_output_path: Path,
    asset_link_cache: dict[str, str],
) -> str:
    cached = asset_link_cache.get(artifact_id)
    if cached:
        return cached
    assets_dir = review_assets_dir(review_output_path)
    assets_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(artifact_id.encode("utf-8")).hexdigest()[:16]
    suffix = image_path.suffix.lower() or ".img"
    dest = assets_dir / f"{digest}{suffix}"
    if not dest.exists() or dest.stat().st_size != image_path.stat().st_size:
        shutil.copy2(image_path, dest)
    link = f"assets/{dest.name}".replace("\\", "/")
    asset_link_cache[artifact_id] = link
    return link


def _figure_to_html(figure: ReviewImageFigure) -> list[str]:
    if figure.found:
        return [
            f'<figure><img src="{html.escape(figure.src, quote=True)}" '
            f'alt="{html.escape(figure.artifact_id)}">'
            f"<figcaption>{html.escape(figure.caption or figure.artifact_id)}</figcaption></figure>"
        ]
    return [
        f'<figure class="missing-image"><div class="missing-image-label">{html.escape(figure.artifact_id)}</div>'
        f"<figcaption>{html.escape(figure.caption)}</figcaption></figure>"
    ]


def _caption(ref: dict[str, Any]) -> str:
    what_to_look_at = ref.get("what_to_look_at")
    if isinstance(what_to_look_at, list):
        joined = "; ".join(str(item).strip() for item in what_to_look_at if str(item).strip())
        if joined:
            return joined
    return str(
        ref.get("what_to_look_at")
        or ref.get("description")
        or ref.get("caption")
        or ""
    ).strip()
