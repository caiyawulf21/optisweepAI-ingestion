"""Shared Stage 11 Cosmos publish bundle, SME review sheet, and multi-container upload."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import urllib.error
import urllib.parse
import urllib.request
from email.utils import formatdate
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_10.source_loader import load_source_roots_contexts_and_artifacts
from shared_pipeline_stages.stage_11.container_config import (
    DATASET_CANONICAL_IMAGES,
    DATASET_GATE_PHRASE_TABLES,
    DATASET_OPERATIONAL_CONTEXT,
    DATASET_PLAYBOOKS_A,
    DATASET_PLAYBOOKS_B,
    DATASET_RELATIONSHIP_LINKS,
    DATASET_RUNBOOKS,
    DATASET_SOURCE_ARTIFACTS,
    load_blob_image_settings,
    load_cosmos_settings,
)
from shared_pipeline_stages.stage_11.image_blob_publisher import (
    assert_canonical_images_renderable,
    build_canonical_image_documents,
    has_http_storage_uri,
)
from shared_pipeline_stages.stage_11.schemas import PublishManifest
from shared_pipeline_stages.stage_11.sme_review_sheet import build_sme_review_sheet

STAGE10_DIR_NAME = "stage_10_embeddings"
STAGE11_DIR_NAME = "stage_11_cosmos_publish"
STAGE8_VARIANTS = {
    "prompt_a_one_per_incident": DATASET_PLAYBOOKS_A,
    "prompt_b_multi_flow": DATASET_PLAYBOOKS_B,
}
COSMOS_MAX_DOC_BYTES = 1_800_000
RELATIONSHIP_SHARD_LINK_LIMIT = 2000
DEFAULT_SOURCE_ROOTS = (
    "operationalknowledgeingestion/data/output/manual_optisweep_om_v3",
    "operationalknowledgeingestion/data/output/training_video_day1",
    "incidenceknowledgeingestion/data/output/incidents/case_228086",
    "incidenceknowledgeingestion/data/output/incidents/case_228723",
)


@dataclass
class CosmosPublishResult:
    publish_version_id: str
    document_count: int
    embedding_count: int
    runbook_count: int
    playbook_prompt_a_count: int
    playbook_prompt_b_count: int
    operational_context_count: int
    source_artifact_count: int
    canonical_image_count: int
    relationship_link_count: int
    relationship_shard_count: int
    uploaded: bool
    warnings: list[str] = field(default_factory=list)

    @property
    def playbook_count(self) -> int:
        return self.playbook_prompt_a_count + self.playbook_prompt_b_count


def publish_corpus_to_cosmos(
    *,
    stage7_dir: str | Path,
    stage8_dir: str | Path,
    stage10_dir: str | Path,
    stage85_dir: str | Path | None = None,
    stage9_dir: str | Path | None = None,
    output_dir: str | Path,
    source_roots: list[str | Path] | None = None,
    publish: bool = False,
    publish_version_id: str | None = None,
    upload_image_blobs: bool | None = None,
) -> CosmosPublishResult:
    stage7_path = Path(stage7_dir)
    stage8_path = _resolve_stage8_dir(Path(stage8_dir))
    stage10_path = _resolve_stage10_dir(Path(stage10_dir))
    stage85_path = Path(stage85_dir) if stage85_dir else None
    stage9_path = Path(stage9_dir) if stage9_dir else None
    output_path = _resolve_output_path(Path(output_dir))
    bundle_dir = output_path / "publish_bundle"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(UTC).isoformat()
    version_id = publish_version_id or f"publish_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    warnings: list[str] = []
    cosmos_settings = load_cosmos_settings()
    blob_settings = load_blob_image_settings()
    should_upload_blobs = blob_settings.is_complete() if upload_image_blobs is None else upload_image_blobs

    canonical_payload = read_json(stage7_path / "canonical_runbooks.json")
    runbooks = canonical_payload.get("runbooks") if isinstance(canonical_payload, dict) else canonical_payload
    if not isinstance(runbooks, list):
        raise ValueError("Stage 7 canonical_runbooks.json must contain a runbooks list.")

    playbooks_by_dataset: dict[str, list[dict[str, Any]]] = {
        DATASET_PLAYBOOKS_A: [],
        DATASET_PLAYBOOKS_B: [],
    }
    for variant, dataset in STAGE8_VARIANTS.items():
        path = stage8_path / variant / "canonical_playbooks.json"
        if not path.exists():
            warnings.append(f"Missing playbooks at {path}")
            continue
        payload = read_json(path)
        rows = payload.get("playbooks") if isinstance(payload, dict) else payload
        if isinstance(rows, list):
            playbooks_by_dataset[dataset].extend(row for row in rows if isinstance(row, dict))

    embeddings = read_json(stage10_path / "embedding_records.json")
    if not isinstance(embeddings, list):
        raise ValueError("Stage 10 embedding_records.json must contain a list.")

    embeddings_by_type: dict[str, list[dict[str, Any]]] = {
        "canonical_runbook": [],
        "playbook_prompt_a": [],
        "playbook_prompt_b": [],
        "operational_context": [],
        "source_artifact": [],
    }
    for record in embeddings:
        if not isinstance(record, dict):
            continue
        record_type = str(record.get("record_type") or "")
        if record_type in embeddings_by_type:
            embeddings_by_type[record_type].append(record)

    relationship_links: list[dict[str, Any]] = []
    if stage85_path is not None:
        links_path = stage85_path / "relationship_links.json" if stage85_path.is_dir() else stage85_path
        if links_path.exists():
            payload = read_json(links_path)
            if isinstance(payload, list):
                relationship_links = payload
            else:
                warnings.append(f"{links_path} must contain a JSON list.")
        else:
            warnings.append(f"Missing relationship links at {links_path}")

    runbook_docs = [_publish_doc("runbook", runbook, version_id) for runbook in runbooks if isinstance(runbook, dict)]
    runbook_embeddings = [
        _publish_embedding_doc(record, version_id) for record in embeddings_by_type["canonical_runbook"]
    ]
    playbook_a_docs = [
        _publish_doc("playbook", playbook, version_id) for playbook in playbooks_by_dataset[DATASET_PLAYBOOKS_A]
    ]
    playbook_b_docs = [
        _publish_doc("playbook", playbook, version_id) for playbook in playbooks_by_dataset[DATASET_PLAYBOOKS_B]
    ]
    playbook_a_embeddings = [
        _publish_embedding_doc(record, version_id) for record in embeddings_by_type["playbook_prompt_a"]
    ]
    playbook_b_embeddings = [
        _publish_embedding_doc(record, version_id) for record in embeddings_by_type["playbook_prompt_b"]
    ]
    context_rag_docs = [
        _publish_rag_doc(record, version_id, "operational_context")
        for record in embeddings_by_type["operational_context"]
    ]
    context_embeddings = [
        _publish_embedding_doc(record, version_id) for record in embeddings_by_type["operational_context"]
    ]
    artifact_rag_docs = [
        _publish_rag_doc(record, version_id, "source_artifact")
        for record in embeddings_by_type["source_artifact"]
    ]
    artifact_embeddings = [
        _publish_embedding_doc(record, version_id) for record in embeddings_by_type["source_artifact"]
    ]
    relationship_shards = _shard_relationship_links(relationship_links, version_id, generated_at)

    repo_root = Path(__file__).resolve().parents[2]
    resolved_source_roots = _resolve_source_roots(source_roots, repo_root)
    _contexts, source_artifacts, artifact_load_warnings = load_source_roots_contexts_and_artifacts(
        resolved_source_roots
    )
    warnings.extend(artifact_load_warnings)
    canonical_image_docs, image_warnings = build_canonical_image_documents(
        artifacts=source_artifacts,
        relationship_links=relationship_links,
        publish_version_id=version_id,
        repo_root=repo_root,
        upload_blobs=should_upload_blobs,
        blob_settings=blob_settings,
    )
    warnings.extend(image_warnings)

    _write_bundle_file(bundle_dir / "runbooks/documents.json", runbook_docs)
    _write_bundle_file(bundle_dir / "runbooks/embeddings.json", runbook_embeddings)
    _write_bundle_file(bundle_dir / "playbooks_prompt_a/documents.json", playbook_a_docs)
    _write_bundle_file(bundle_dir / "playbooks_prompt_a/embeddings.json", playbook_a_embeddings)
    _write_bundle_file(bundle_dir / "playbooks_prompt_b/documents.json", playbook_b_docs)
    _write_bundle_file(bundle_dir / "playbooks_prompt_b/embeddings.json", playbook_b_embeddings)
    _write_bundle_file(bundle_dir / "operational_context/rag_records.json", context_rag_docs)
    _write_bundle_file(bundle_dir / "operational_context/embeddings.json", context_embeddings)
    _write_bundle_file(bundle_dir / "source_artifacts/rag_records.json", artifact_rag_docs)
    _write_bundle_file(bundle_dir / "source_artifacts/embeddings.json", artifact_embeddings)
    _write_bundle_file(bundle_dir / "canonical_images/documents.json", canonical_image_docs)
    for index, shard in enumerate(relationship_shards):
        _write_bundle_file(bundle_dir / f"relationship_links/shard_{index:03d}.json", shard)

    link_counts: dict[str, int] = {}
    for link in relationship_links:
        if isinstance(link, dict):
            link_type = str(link.get("link_type") or "unknown")
            link_counts[link_type] = link_counts.get(link_type, 0) + 1

    embedding_model = str(embeddings[0].get("embedding_model") or "") if embeddings else ""
    checksums = {
        rel_path: _checksum(bundle_dir / rel_path)
        for rel_path in _bundle_relative_paths(len(relationship_shards))
    }
    record_counts = {
        "runbooks": len(runbook_docs),
        "playbooks_prompt_a": len(playbook_a_docs),
        "playbooks_prompt_b": len(playbook_b_docs),
        "embeddings_total": len(embeddings),
        "embeddings_runbooks": len(runbook_embeddings),
        "embeddings_playbooks_prompt_a": len(playbook_a_embeddings),
        "embeddings_playbooks_prompt_b": len(playbook_b_embeddings),
        "embeddings_operational_context": len(context_embeddings),
        "embeddings_source_artifacts": len(artifact_embeddings),
        "operational_context_rag": len(context_rag_docs),
        "source_artifacts_rag": len(artifact_rag_docs),
        "canonical_images": len(canonical_image_docs),
        "canonical_images_with_storage_uri": sum(
            1 for doc in canonical_image_docs if has_http_storage_uri(doc)
        ),
        "relationship_links": len(relationship_links),
        "relationship_shards": len(relationship_shards),
    }
    manifest = PublishManifest(
        publish_version_id=version_id,
        generated_at=generated_at,
        embedding_model=embedding_model,
        record_counts=record_counts,
        link_counts_by_type=link_counts,
        checksums=checksums,
        cosmos={
            "endpoint": cosmos_settings.endpoint,
            "database": cosmos_settings.database,
            "blob_account_url": blob_settings.account_url,
            "blob_images_container": blob_settings.container,
        },
        containers=cosmos_settings.containers,
        source_paths={
            "stage7_dir": str(stage7_path),
            "stage8_dir": str(stage8_path),
            "stage10_dir": str(stage10_path),
            "stage85_dir": str(stage85_path) if stage85_path else "",
            "stage9_dir": str(stage9_path) if stage9_path else "",
            "source_roots": ";".join(str(path) for path in resolved_source_roots),
            "publish_bundle": str(bundle_dir),
        },
    )
    write_json(output_path / "publish_manifest.json", manifest.model_dump(mode="json"))

    stage9_validation_path = None
    if stage9_path is not None:
        candidate = stage9_path / "validation_report.json" if stage9_path.is_dir() else stage9_path
        if candidate.exists():
            stage9_validation_path = candidate
    stage85_links_path = None
    if stage85_path is not None:
        stage85_links_path = stage85_path / "relationship_links.json" if stage85_path.is_dir() else stage85_path

    build_sme_review_sheet(
        publish_version_id=version_id,
        manifest=manifest.model_dump(mode="json"),
        bundle_dir=bundle_dir,
        stage9_validation_path=stage9_validation_path,
        stage85_links_path=stage85_links_path,
        output_dir=output_path,
    )

    uploaded = False
    if publish:
        if canonical_image_docs and upload_image_blobs is False:
            raise ValueError(
                "Refusing Cosmos publish with upload_image_blobs=False while canonical "
                "images are present. Omit --skip-image-blobs so Blob SAS URIs are written, "
                "or pass allow_metadata_only_images only via upload_existing_publish_bundle."
            )
        assert_canonical_images_renderable(
            canonical_image_docs,
            context=f"Stage 11 Cosmos publish publish_version_id={version_id}",
        )
        uploaded, upload_warnings = _upload_multi_container_bundle(
            cosmos_settings=cosmos_settings,
            publish_version_id=version_id,
            datasets=_upload_datasets(
                runbook_docs=runbook_docs,
                runbook_embeddings=runbook_embeddings,
                playbook_a_docs=playbook_a_docs,
                playbook_a_embeddings=playbook_a_embeddings,
                playbook_b_docs=playbook_b_docs,
                playbook_b_embeddings=playbook_b_embeddings,
                context_rag_docs=context_rag_docs,
                context_embeddings=context_embeddings,
                artifact_rag_docs=artifact_rag_docs,
                artifact_embeddings=artifact_embeddings,
                canonical_image_docs=canonical_image_docs,
                relationship_shards=relationship_shards,
                gate_phrase_docs=[],
            ),
        )
        warnings.extend(upload_warnings)
    else:
        warnings.append("Cosmos upload skipped (--publish not set). Local publish bundle written.")

    smoke_image = next(
        (doc for doc in canonical_image_docs if has_http_storage_uri(doc)),
        None,
    )
    report = {
        "stage": "11",
        "stage_name": "cosmos_publish",
        "generated_at": generated_at,
        "publish_version_id": version_id,
        "uploaded": uploaded,
        "record_counts": record_counts,
        "link_counts_by_type": link_counts,
        "containers": cosmos_settings.containers,
        "blob_images": {
            "account_url": blob_settings.account_url,
            "container": blob_settings.container,
            "uploaded": should_upload_blobs and bool(smoke_image),
            "smoke_test_image_id": (smoke_image or {}).get("image_id", ""),
            "smoke_test_storage_uri_present": bool(smoke_image),
        },
        "warnings": warnings,
        "outputs": {
            "publish_manifest": str(output_path / "publish_manifest.json"),
            "publish_bundle": str(bundle_dir),
            "sme_review_sheet_md": str(output_path / "sme_review_sheet.md"),
            "sme_review_sheet_json": str(output_path / "sme_review_sheet.json"),
        },
    }
    write_json(output_path / "cosmos_publish_report.json", report)

    document_count = (
        len(runbook_docs)
        + len(runbook_embeddings)
        + len(playbook_a_docs)
        + len(playbook_a_embeddings)
        + len(playbook_b_docs)
        + len(playbook_b_embeddings)
        + len(context_rag_docs)
        + len(context_embeddings)
        + len(artifact_rag_docs)
        + len(artifact_embeddings)
        + len(canonical_image_docs)
        + len(relationship_shards)
    )
    return CosmosPublishResult(
        publish_version_id=version_id,
        document_count=document_count,
        embedding_count=len(embeddings),
        runbook_count=len(runbook_docs),
        playbook_prompt_a_count=len(playbook_a_docs),
        playbook_prompt_b_count=len(playbook_b_docs),
        operational_context_count=len(context_rag_docs),
        source_artifact_count=len(artifact_rag_docs),
        canonical_image_count=len(canonical_image_docs),
        relationship_link_count=len(relationship_links),
        relationship_shard_count=len(relationship_shards),
        uploaded=uploaded,
        warnings=warnings,
    )


def delete_publish_versions(
    publish_version_ids: list[str],
    *,
    datasets: list[str] | None = None,
) -> dict[str, Any]:
    """Delete all documents for one or more publish_version_id partitions from Cosmos."""
    versions = [str(value).strip() for value in publish_version_ids if str(value).strip()]
    if not versions:
        raise ValueError("At least one publish_version_id is required.")

    cosmos_settings = load_cosmos_settings()
    if not cosmos_settings.is_complete():
        raise RuntimeError(
            "Cosmos settings incomplete. Set COSMOS_ENDPOINT, COSMOS_KEY, COSMOS_DATABASE, "
            "and COSMOS_CONTAINER_* variables."
        )

    selected = datasets or list(cosmos_settings.containers.keys())
    per_version: dict[str, dict[str, int]] = {}
    warnings: list[str] = []
    total_deleted = 0

    for version_id in versions:
        dataset_counts: dict[str, int] = {}
        for dataset in selected:
            container = cosmos_settings.containers.get(dataset, "")
            if not container:
                warnings.append(f"Missing container mapping for dataset {dataset}.")
                continue
            deleted, delete_warnings = _delete_partition_documents(
                cosmos_settings=cosmos_settings,
                container=container,
                publish_version_id=version_id,
            )
            dataset_counts[dataset] = deleted
            total_deleted += deleted
            warnings.extend(delete_warnings)
        per_version[version_id] = dataset_counts

    return {
        "deleted": True,
        "publish_version_ids": versions,
        "total_deleted": total_deleted,
        "per_version": per_version,
        "warnings": warnings,
    }


def upload_existing_publish_bundle(
    cosmos_publish_dir: str | Path,
    *,
    publish_scope: str | None = None,
    default_case_id: str | None = None,
    allow_partial_publish: bool = False,
    baseline_publish_dir: str | Path | None = None,
    allow_metadata_only_images: bool = False,
) -> tuple[bool, str, list[str], dict[str, int]]:
    """Upload a previously assembled Stage 11 publish directory to Cosmos.

    Expects ``cosmos_publish_dir/publish_bundle/...`` plus optional
    ``publish_manifest.json``.

    ``publish_scope`` may be ``all``, ``case:<id>``, ``case:auto``, or ``source:<id>``.
    Scoped uploads into a new partition are rejected unless ``allow_partial_publish``.
    """
    from shared_pipeline_stages.stage_11.image_blob_publisher import (
        assert_canonical_images_renderable,
        ensure_canonical_image_storage_uris,
    )
    from shared_pipeline_stages.stage_11.publish_gate import (
        inventory_from_bundle,
        validate_cumulative_publish,
    )
    from shared_pipeline_stages.stage_11.publish_scope import filter_upload_datasets, parse_publish_scope

    root = Path(cosmos_publish_dir)
    bundle_dir = root / "publish_bundle" if (root / "publish_bundle").is_dir() else root
    if not bundle_dir.is_dir():
        raise FileNotFoundError(f"Publish bundle not found under {root}")

    manifest_path = root / "publish_manifest.json"
    if not manifest_path.exists() and (bundle_dir.parent / "publish_manifest.json").exists():
        manifest_path = bundle_dir.parent / "publish_manifest.json"
    version_id = ""
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        if isinstance(manifest, dict):
            version_id = str(manifest.get("publish_version_id") or "")

    def _load_list(relative: str) -> list[dict[str, Any]]:
        path = bundle_dir / relative
        if not path.exists():
            return []
        payload = read_json(path)
        if isinstance(payload, list):
            return [row for row in payload if isinstance(row, dict)]
        return []

    relationship_shards: list[dict[str, Any]] = []
    links_dir = bundle_dir / "relationship_links"
    if links_dir.is_dir():
        for shard_path in sorted(links_dir.glob("shard_*.json")):
            payload = read_json(shard_path)
            if isinstance(payload, dict):
                relationship_shards.append(payload)

    image_docs = _load_list("canonical_images/documents.json")
    image_warnings: list[str] = []
    if image_docs and not allow_metadata_only_images:
        image_docs, image_warnings = ensure_canonical_image_storage_uris(image_docs)
        write_json(bundle_dir / "canonical_images/documents.json", image_docs)
        assert_canonical_images_renderable(
            image_docs,
            context=f"Cosmos upload publish_version_id={version_id or 'unknown'}",
        )

    datasets = _upload_datasets(
        runbook_docs=_load_list("runbooks/documents.json"),
        runbook_embeddings=_load_list("runbooks/embeddings.json"),
        playbook_a_docs=_load_list("playbooks_prompt_a/documents.json"),
        playbook_a_embeddings=_load_list("playbooks_prompt_a/embeddings.json"),
        playbook_b_docs=_load_list("playbooks_prompt_b/documents.json"),
        playbook_b_embeddings=_load_list("playbooks_prompt_b/embeddings.json"),
        context_rag_docs=_load_list("operational_context/rag_records.json"),
        context_embeddings=_load_list("operational_context/embeddings.json"),
        artifact_rag_docs=_load_list("source_artifacts/rag_records.json"),
        artifact_embeddings=_load_list("source_artifacts/embeddings.json"),
        canonical_image_docs=image_docs,
        relationship_shards=relationship_shards,
        gate_phrase_docs=_load_list("gate_phrase_tables/documents.json"),
    )
    scope = parse_publish_scope(publish_scope, default_case_id=default_case_id)
    if scope.kind != "all" and not allow_partial_publish:
        raise ValueError(
            f"Refusing scoped Cosmos upload ({scope.label}) for publish_version_id={version_id or 'new'}. "
            "AUTO_PUBLISH_VERSION apps load the newest partition; partial uploads create a thin corpus. "
            "Use --publish-scope all, or pass allow_partial_publish=True only for intentional in-place patches."
        )
    datasets, scope_counts = filter_upload_datasets(datasets, scope)

    if baseline_publish_dir is not None:
        baseline_bundle = Path(baseline_publish_dir)
        if (baseline_bundle / "publish_bundle").is_dir():
            baseline_bundle = baseline_bundle / "publish_bundle"
        gate = validate_cumulative_publish(
            candidate=inventory_from_bundle(bundle_dir),
            baseline=inventory_from_bundle(baseline_bundle),
            require_image_storage_uri=not allow_metadata_only_images,
        )
        write_json(root / "publish_manifest_diff.json", gate.to_dict())
        if not gate.passed:
            raise ValueError("Pre-publish cumulative gate failed: " + "; ".join(gate.errors))

    total_docs = sum(scope_counts.values())
    warnings: list[str] = [
        f"publish_scope={scope.label}",
        f"scoped_document_counts={scope_counts}",
        *image_warnings,
    ]
    if total_docs == 0:
        warnings.append(f"No documents matched publish scope {scope.label}.")
        report = {
            "stage": "11",
            "stage_name": "cosmos_publish_from_bundle",
            "generated_at": datetime.now(UTC).isoformat(),
            "publish_version_id": version_id,
            "uploaded": False,
            "publish_scope": scope.label,
            "scoped_document_counts": scope_counts,
            "warnings": warnings,
            "source_bundle": str(bundle_dir),
        }
        write_json(root / "cosmos_upload_report.json", report)
        return False, version_id, warnings, scope_counts

    cosmos_settings = load_cosmos_settings()
    uploaded, upload_warnings = _upload_multi_container_bundle(
        cosmos_settings=cosmos_settings,
        publish_version_id=version_id or "existing_bundle",
        datasets=datasets,
    )
    warnings.extend(upload_warnings)
    report = {
        "stage": "11",
        "stage_name": "cosmos_publish_from_bundle",
        "generated_at": datetime.now(UTC).isoformat(),
        "publish_version_id": version_id,
        "uploaded": uploaded,
        "publish_scope": scope.label,
        "scoped_document_counts": scope_counts,
        "warnings": warnings,
        "source_bundle": str(bundle_dir),
    }
    write_json(root / "cosmos_upload_report.json", report)
    return uploaded, version_id, warnings, scope_counts


def _upload_datasets(
    *,
    runbook_docs: list[dict[str, Any]],
    runbook_embeddings: list[dict[str, Any]],
    playbook_a_docs: list[dict[str, Any]],
    playbook_a_embeddings: list[dict[str, Any]],
    playbook_b_docs: list[dict[str, Any]],
    playbook_b_embeddings: list[dict[str, Any]],
    context_rag_docs: list[dict[str, Any]],
    context_embeddings: list[dict[str, Any]],
    artifact_rag_docs: list[dict[str, Any]],
    artifact_embeddings: list[dict[str, Any]],
    canonical_image_docs: list[dict[str, Any]],
    relationship_shards: list[dict[str, Any]],
    gate_phrase_docs: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    return {
        DATASET_RUNBOOKS: runbook_docs + runbook_embeddings,
        DATASET_PLAYBOOKS_A: playbook_a_docs + playbook_a_embeddings,
        DATASET_PLAYBOOKS_B: playbook_b_docs + playbook_b_embeddings,
        DATASET_OPERATIONAL_CONTEXT: context_rag_docs + context_embeddings,
        DATASET_SOURCE_ARTIFACTS: artifact_rag_docs + artifact_embeddings,
        DATASET_CANONICAL_IMAGES: canonical_image_docs,
        DATASET_RELATIONSHIP_LINKS: relationship_shards,
        DATASET_GATE_PHRASE_TABLES: list(gate_phrase_docs or []),
    }


def _cosmos_authorization_header(
    *,
    verb: str,
    resource_type: str,
    resource_id: str,
    key: str,
    date: str,
) -> str:
    string_to_sign = (
        f"{verb.lower()}\n{resource_type.lower()}\n{resource_id}\n{date.lower()}\n\n"
    )
    key_bytes = base64.b64decode(key)
    signature = base64.b64encode(
        hmac.new(key_bytes, string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")
    return f"type=master&ver=1.0&sig={urllib.parse.quote(signature, safe='')}"


def _delete_partition_documents(
    *,
    cosmos_settings,
    container: str,
    publish_version_id: str,
) -> tuple[int, list[str]]:
    warnings: list[str] = []
    deleted = 0
    collection_id = f"dbs/{cosmos_settings.database}/colls/{container}"
    query_url = f"{cosmos_settings.endpoint.rstrip('/')}/{collection_id}/docs"
    continuation: str | None = None
    while True:
        request_date = formatdate(timeval=None, localtime=False, usegmt=True)
        headers = {
            "Authorization": _cosmos_authorization_header(
                verb="POST",
                resource_type="docs",
                resource_id=collection_id,
                key=cosmos_settings.key,
                date=request_date,
            ),
            "Content-Type": "application/query+json",
            "x-ms-date": request_date,
            "x-ms-version": "2018-12-31",
            "x-ms-documentdb-isquery": "True",
            "x-ms-documentdb-partitionkey": json.dumps([publish_version_id]),
            "x-ms-max-item-count": "100",
        }
        if continuation:
            headers["x-ms-continuation"] = continuation
        body = {
            "query": "SELECT c.id FROM c WHERE c.publish_version_id = @publish_version_id",
            "parameters": [{"name": "@publish_version_id", "value": publish_version_id}],
        }
        request = urllib.request.Request(
            query_url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
                continuation = response.headers.get("x-ms-continuation") or None
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            warnings.append(
                f"Cosmos query failed for container={container} version={publish_version_id}: "
                f"HTTP {exc.code} {details}"
            )
            return deleted, warnings
        except urllib.error.URLError as exc:
            warnings.append(
                f"Cosmos query failed for container={container} version={publish_version_id}: {exc.reason}"
            )
            return deleted, warnings

        for row in payload.get("Documents") or []:
            doc_id = str((row or {}).get("id") or "").strip()
            if not doc_id:
                continue
            ok, warning = _delete_document(
                cosmos_settings=cosmos_settings,
                container=container,
                document_id=doc_id,
                publish_version_id=publish_version_id,
            )
            if ok:
                deleted += 1
            elif warning:
                warnings.append(warning)

        if not continuation:
            break
    return deleted, warnings


def _delete_document(
    *,
    cosmos_settings,
    container: str,
    document_id: str,
    publish_version_id: str,
) -> tuple[bool, str | None]:
    resource_id = f"dbs/{cosmos_settings.database}/colls/{container}/docs/{document_id}"
    encoded_id = urllib.parse.quote(document_id, safe="")
    url = (
        f"{cosmos_settings.endpoint.rstrip('/')}/"
        f"dbs/{cosmos_settings.database}/colls/{container}/docs/{encoded_id}"
    )
    request_date = formatdate(timeval=None, localtime=False, usegmt=True)
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": _cosmos_authorization_header(
                verb="DELETE",
                resource_type="docs",
                resource_id=resource_id,
                key=cosmos_settings.key,
                date=request_date,
            ),
            "x-ms-date": request_date,
            "x-ms-version": "2018-12-31",
            "x-ms-documentdb-partitionkey": json.dumps([publish_version_id]),
        },
        method="DELETE",
    )
    try:
        with urllib.request.urlopen(request, timeout=60):
            return True, None
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return True, None
        details = exc.read().decode("utf-8", errors="replace")
        return False, (
            f"Cosmos delete failed for container={container} doc={document_id}: "
            f"HTTP {exc.code} {details}"
        )
    except urllib.error.URLError as exc:
        return False, f"Cosmos delete failed for container={container} doc={document_id}: {exc.reason}"


def _upload_multi_container_bundle(
    *,
    cosmos_settings,
    publish_version_id: str,
    datasets: dict[str, list[dict[str, Any]]],
) -> tuple[bool, list[str]]:
    warnings: list[str] = []
    if not cosmos_settings.is_complete():
        warnings.append(
            "Cosmos publish requested but COSMOS_ENDPOINT, COSMOS_KEY, COSMOS_DATABASE, "
            "or one of the COSMOS_CONTAINER_* variables is incomplete."
        )
        return False, warnings

    uploaded = 0
    expected = 0
    for dataset, docs in datasets.items():
        container = cosmos_settings.containers.get(dataset, "")
        if not container:
            warnings.append(f"Missing container mapping for dataset {dataset}.")
            continue
        for doc in docs:
            expected += 1
            doc_id = str(doc.get("id") or uuid4().hex)
            collection_id = f"dbs/{cosmos_settings.database}/colls/{container}"
            url = f"{cosmos_settings.endpoint.rstrip('/')}/{collection_id}/docs"
            request_date = formatdate(timeval=None, localtime=False, usegmt=True)
            request = urllib.request.Request(
                url,
                data=json.dumps(doc).encode("utf-8"),
                headers={
                    "Authorization": _cosmos_authorization_header(
                        verb="POST",
                        resource_type="docs",
                        resource_id=collection_id,
                        key=cosmos_settings.key,
                        date=request_date,
                    ),
                    "Content-Type": "application/json",
                    "x-ms-date": request_date,
                    "x-ms-version": "2018-12-31",
                    "x-ms-documentdb-is-upsert": "true",
                    "x-ms-documentdb-partitionkey": json.dumps([publish_version_id]),
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=60):
                    uploaded += 1
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                warnings.append(
                    f"Cosmos upload failed for dataset={dataset} doc={doc_id}: HTTP {exc.code} {details}"
                )
            except urllib.error.URLError as exc:
                warnings.append(f"Cosmos upload failed for dataset={dataset} doc={doc_id}: {exc.reason}")
                warnings.append(f"Cosmos upload aborted after network error: {uploaded}/{expected} documents.")
                return False, warnings

    if uploaded == expected:
        return True, warnings
    warnings.append(f"Cosmos upload partial success: {uploaded}/{expected} documents.")
    return False, warnings


def _publish_doc(doc_type: str, payload: dict[str, Any], version_id: str) -> dict[str, Any]:
    record_id = str(payload.get("procedure_id") or payload.get("playbook_id") or uuid4().hex)
    return {
        "id": f"{doc_type}_{record_id}",
        "doc_type": doc_type,
        "publish_version_id": version_id,
        "record_id": record_id,
        "payload": payload,
    }


def _publish_embedding_doc(record: dict[str, Any], version_id: str) -> dict[str, Any]:
    record_id = str(record.get("record_id") or record.get("source_record_id") or uuid4().hex)
    return {
        "id": record_id,
        "doc_type": "embedding",
        "publish_version_id": version_id,
        "record_type": record.get("record_type"),
        "source_record_id": record.get("source_record_id"),
        "embedded_text": record.get("embedded_text"),
        "vector": record.get("vector") or [],
        "embedding_model": record.get("embedding_model"),
        "embedding_dimensions": record.get("embedding_dimensions"),
        "retrieval_text_hash": record.get("retrieval_text_hash"),
        "filter_metadata": record.get("filter_metadata") or {},
        "source_refs": record.get("source_refs") or [],
    }


def _publish_rag_doc(record: dict[str, Any], version_id: str, record_type: str) -> dict[str, Any]:
    metadata = record.get("filter_metadata") or {}
    record_id = str(record.get("record_id") or uuid4().hex)
    return {
        "id": f"rag_{record_id}",
        "doc_type": "rag_record",
        "publish_version_id": version_id,
        "record_type": record_type,
        "source_record_id": record.get("source_record_id"),
        "retrieval_text": record.get("embedded_text"),
        "summary": metadata.get("summary", ""),
        "vector": record.get("vector") or [],
        "embedding_model": record.get("embedding_model"),
        "embedding_dimensions": record.get("embedding_dimensions"),
        "retrieval_text_hash": record.get("retrieval_text_hash"),
        "filter_metadata": metadata,
        "source_refs": record.get("source_refs") or [],
    }


def _shard_relationship_links(
    links: list[dict[str, Any]],
    version_id: str,
    generated_at: str,
) -> list[dict[str, Any]]:
    if not links:
        return []
    shards: list[dict[str, Any]] = []
    batch: list[dict[str, Any]] = []
    shard_index = 0
    for link in links:
        batch.append(link)
        if len(batch) >= RELATIONSHIP_SHARD_LINK_LIMIT:
            shards.append(_relationship_shard_doc(batch, version_id, generated_at, shard_index))
            shard_index += 1
            batch = []
    if batch:
        shards.append(_relationship_shard_doc(batch, version_id, generated_at, shard_index))
    sized: list[dict[str, Any]] = []
    for shard in shards:
        if len(json.dumps(shard).encode("utf-8")) <= COSMOS_MAX_DOC_BYTES:
            sized.append(shard)
            continue
        mid = max(1, len(shard["links"]) // 2)
        sized.extend(
            [
                _relationship_shard_doc(shard["links"][:mid], version_id, generated_at, len(sized)),
                _relationship_shard_doc(shard["links"][mid:], version_id, generated_at, len(sized) + 1),
            ]
        )
    for index, shard in enumerate(sized):
        shard["id"] = f"relationship_graph_{version_id}_{index:03d}"
        shard["shard_index"] = index
        shard["shard_count"] = len(sized)
    return sized


def _relationship_shard_doc(
    links: list[dict[str, Any]],
    version_id: str,
    generated_at: str,
    shard_index: int,
) -> dict[str, Any]:
    return {
        "id": f"relationship_graph_{version_id}_{shard_index:03d}",
        "doc_type": "relationship_graph",
        "publish_version_id": version_id,
        "generated_at": generated_at,
        "shard_index": shard_index,
        "link_count": len(links),
        "links": links,
    }


def _bundle_relative_paths(shard_count: int) -> list[str]:
    paths = [
        "runbooks/documents.json",
        "runbooks/embeddings.json",
        "playbooks_prompt_a/documents.json",
        "playbooks_prompt_a/embeddings.json",
        "playbooks_prompt_b/documents.json",
        "playbooks_prompt_b/embeddings.json",
        "operational_context/rag_records.json",
        "operational_context/embeddings.json",
        "source_artifacts/rag_records.json",
        "source_artifacts/embeddings.json",
        "canonical_images/documents.json",
    ]
    paths.extend(f"relationship_links/shard_{index:03d}.json" for index in range(shard_count))
    return paths


def _resolve_source_roots(source_roots: list[str | Path] | None, repo_root: Path) -> list[Path]:
    if source_roots:
        return [Path(root) for root in source_roots]
    return [repo_root / relative for relative in DEFAULT_SOURCE_ROOTS if (repo_root / relative).exists()]


def _write_bundle_file(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, data)


def _checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_stage8_dir(stage8_dir: Path) -> Path:
    if stage8_dir.name == "stage_8_finalized_playbooks":
        return stage8_dir
    nested = stage8_dir / "stage_8_finalized_playbooks"
    return nested if nested.exists() else stage8_dir


def _resolve_stage10_dir(stage10_dir: Path) -> Path:
    if stage10_dir.name == STAGE10_DIR_NAME:
        return stage10_dir
    nested = stage10_dir / STAGE10_DIR_NAME
    return nested if nested.exists() else stage10_dir


def _resolve_output_path(output_dir: Path) -> Path:
    if output_dir.name == STAGE11_DIR_NAME:
        return output_dir
    return output_dir / STAGE11_DIR_NAME
