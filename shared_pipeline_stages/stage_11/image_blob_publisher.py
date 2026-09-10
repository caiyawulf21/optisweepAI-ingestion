from __future__ import annotations

from datetime import UTC, datetime, timedelta
from mimetypes import guess_type
from pathlib import Path
from typing import Any

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobSasPermissions, BlobServiceClient, ContentSettings, generate_blob_sas

from shared_pipeline_stages.stage_7.artifact_images import resolve_artifact_image_path
from shared_pipeline_stages.stage_11.container_config import BlobImageSettings, load_blob_image_settings

REPO_ROOT = Path(__file__).resolve().parents[2]
SAS_DAYS = 365 * 2


def has_http_storage_uri(record: dict[str, Any] | None) -> bool:
    if not isinstance(record, dict):
        return False
    storage_uri = str(record.get("storage_uri") or "").strip()
    return storage_uri.startswith("http://") or storage_uri.startswith("https://")


def canonical_images_missing_storage_uri(docs: list[dict[str, Any]]) -> list[str]:
    missing: list[str] = []
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        if has_http_storage_uri(doc):
            continue
        missing.append(str(doc.get("image_id") or doc.get("id") or "unknown"))
    return missing


def assert_canonical_images_renderable(
    docs: list[dict[str, Any]],
    *,
    context: str = "canonical_images",
) -> None:
    """Fail closed when image metadata would publish without a renderable Blob URI."""
    if not docs:
        return
    missing = canonical_images_missing_storage_uri(docs)
    if not missing:
        return
    sample = ", ".join(missing[:8])
    more = f" (+{len(missing) - 8} more)" if len(missing) > 8 else ""
    raise ValueError(
        f"{context}: {len(missing)}/{len(docs)} canonical image(s) lack HTTPS storage_uri "
        f"(sample: {sample}{more}). Upload Blob bytes / mint SAS before Cosmos publish, "
        "or pass allow_metadata_only_images only for intentional offline bundles."
    )


def ensure_canonical_image_storage_uris(
    docs: list[dict[str, Any]],
    *,
    blob_settings: BlobImageSettings | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Mint HTTPS SAS URLs from existing blob_path values when storage_uri is empty."""
    settings = blob_settings if blob_settings is not None else load_blob_image_settings()
    warnings: list[str] = []
    if not docs:
        return docs, warnings
    if not settings.is_complete():
        warnings.append(
            "Cannot mint image storage_uri values: AZURE_STORAGE_CONNECTION_STRING "
            "or AZURE_CANONICAL_IMAGES_CONTAINER is incomplete."
        )
        return [dict(doc) for doc in docs if isinstance(doc, dict)], warnings

    blob_client = BlobServiceClient.from_connection_string(settings.connection_string)
    account_name, account_key = _parse_account(settings.connection_string)
    if not account_name or not account_key:
        warnings.append("Cannot mint image storage_uri values: AccountName/AccountKey missing.")
        return [dict(doc) for doc in docs if isinstance(doc, dict)], warnings

    updated: list[dict[str, Any]] = []
    minted = 0
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        row = dict(doc)
        if has_http_storage_uri(row):
            updated.append(row)
            continue
        blob_name = str(row.get("blob_path") or row.get("blob_name") or "").strip()
        if not blob_name:
            updated.append(row)
            continue
        try:
            blob = blob_client.get_blob_client(container=settings.container, blob=blob_name)
            blob.get_blob_properties()
            row["storage_uri"] = _sas_uri(
                account_name=account_name,
                account_key=account_key,
                account_url=settings.account_url,
                container=settings.container,
                blob_name=blob_name,
            )
            minted += 1
        except ResourceNotFoundError:
            warnings.append(f"Blob missing for image storage_uri mint: {blob_name}")
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Failed to mint storage_uri for {blob_name}: {exc}")
        updated.append(row)
    if minted:
        warnings.append(f"Minted HTTPS storage_uri for {minted} canonical image(s) from blob_path.")
    return updated, warnings


def build_canonical_image_documents(
    *,
    artifacts: list[dict[str, Any]],
    relationship_links: list[dict[str, Any]],
    publish_version_id: str,
    repo_root: Path | None = None,
    upload_blobs: bool = False,
    blob_settings: BlobImageSettings | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    root = repo_root or REPO_ROOT
    settings = blob_settings if blob_settings is not None else load_blob_image_settings()
    warnings: list[str] = []
    procedure_links, incident_links = _build_link_indexes(relationship_links)

    blob_client: BlobServiceClient | None = None
    account_name = ""
    account_key = ""
    if upload_blobs:
        if not settings.is_complete():
            warnings.append(
                "Canonical image Blob upload requested but AZURE_STORAGE_CONNECTION_STRING "
                "or AZURE_CANONICAL_IMAGES_CONTAINER is incomplete."
            )
        else:
            blob_client = BlobServiceClient.from_connection_string(settings.connection_string)
            account_name, account_key = _parse_account(settings.connection_string)
            _ensure_container(blob_client, settings.container, warnings)

    docs: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_id = str(artifact.get("artifact_id") or "").strip()
        if not artifact_id:
            continue
        image_path = _resolve_artifact_file(artifact, repo_root=root)
        if image_path is None:
            warnings.append(f"Canonical image skipped (file not found): {artifact_id}")
            continue

        content_type = guess_type(str(image_path))[0] or "application/octet-stream"
        suffix = image_path.suffix.lower() or ".bin"
        blob_name = f"{publish_version_id}/{artifact_id}{suffix}"
        storage_uri = ""
        if blob_client is not None and account_name and account_key:
            try:
                storage_uri = _upload_blob(
                    blob_client=blob_client,
                    container=settings.container,
                    blob_name=blob_name,
                    image_path=image_path,
                    content_type=content_type,
                    account_name=account_name,
                    account_key=account_key,
                    account_url=settings.account_url,
                )
            except Exception as exc:  # noqa: BLE001 — surface as publish warning
                warnings.append(f"Blob upload failed for {artifact_id}: {exc}")
                continue
        elif upload_blobs:
            continue

        if upload_blobs and not (
            storage_uri.startswith("http://") or storage_uri.startswith("https://")
        ):
            warnings.append(f"Canonical image skipped (missing storage_uri after upload): {artifact_id}")
            continue

        case_id = _case_id(artifact, incident_links.get(artifact_id, []))
        docs.append(
            {
                "id": f"image_{artifact_id}",
                "doc_type": "canonical_image",
                "publish_version_id": publish_version_id,
                "image_id": artifact_id,
                "title": _title(artifact, artifact_id),
                "description": _description(artifact),
                "category": str(
                    artifact.get("artifact_type")
                    or artifact.get("image_type")
                    or artifact.get("artifact_image_type")
                    or ""
                ),
                "storage_uri": storage_uri,
                "content_type": content_type,
                "blob_path": blob_name,
                "linked_procedure_ids": sorted(procedure_links.get(artifact_id, set())),
                "linked_incident_ids": sorted(incident_links.get(artifact_id, set())),
                "case_id": case_id,
                "source_artifact_ids": [artifact_id],
                "filter_metadata": {
                    "source_id": str(artifact.get("source_id") or ""),
                    "source_type": str(artifact.get("source_type") or ""),
                    "storage_path_local": str(artifact.get("storage_path") or ""),
                    "artifact_type": str(artifact.get("artifact_type") or ""),
                },
            }
        )

    if upload_blobs and docs and not any(has_http_storage_uri(doc) for doc in docs):
        warnings.append("Canonical image Blob upload produced no storage_uri values.")
    return docs, warnings


def _ensure_container(blob_client: BlobServiceClient, container: str, warnings: list[str]) -> None:
    try:
        blob_client.create_container(container)
    except ResourceExistsError:
        return
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"Could not ensure Blob container '{container}': {exc}")


def _upload_blob(
    *,
    blob_client: BlobServiceClient,
    container: str,
    blob_name: str,
    image_path: Path,
    content_type: str,
    account_name: str,
    account_key: str,
    account_url: str,
) -> str:
    blob = blob_client.get_blob_client(container=container, blob=blob_name)
    with image_path.open("rb") as handle:
        blob.upload_blob(
            handle,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type),
        )
    return _sas_uri(
        account_name=account_name,
        account_key=account_key,
        account_url=account_url,
        container=container,
        blob_name=blob_name,
    )


def _sas_uri(
    *,
    account_name: str,
    account_key: str,
    account_url: str,
    container: str,
    blob_name: str,
) -> str:
    expiry = datetime.now(UTC) + timedelta(days=SAS_DAYS)
    sas = generate_blob_sas(
        account_name=account_name,
        container_name=container,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
    base = account_url.rstrip("/") if account_url else f"https://{account_name}.blob.core.windows.net"
    return f"{base}/{container}/{blob_name}?{sas}"


def _parse_account(connection_string: str) -> tuple[str, str]:
    account_name = ""
    account_key = ""
    for part in connection_string.split(";"):
        if "=" not in part:
            continue
        name, value = part.split("=", 1)
        key = name.strip()
        if key == "AccountName":
            account_name = value.strip()
        elif key == "AccountKey":
            account_key = value.strip()
    return account_name, account_key


def _build_link_indexes(
    relationship_links: list[dict[str, Any]],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    procedure_links: dict[str, set[str]] = {}
    incident_links: dict[str, set[str]] = {}
    for link in relationship_links:
        if not isinstance(link, dict):
            continue
        link_type = str(link.get("link_type") or "")
        source_id = str(link.get("source_record_id") or "").strip()
        target_id = str(link.get("target_record_id") or "").strip()
        if not source_id or not target_id:
            continue
        if link_type == "artifact_runbook":
            procedure_links.setdefault(source_id, set()).add(target_id)
        elif link_type == "artifact_incident":
            incident_links.setdefault(source_id, set()).add(target_id)
    return procedure_links, incident_links


def _resolve_artifact_file(artifact: dict[str, Any], *, repo_root: Path) -> Path | None:
    for key in ("storage_path", "image_path", "image_ref", "file_path"):
        path = resolve_artifact_image_path(str(artifact.get(key) or ""), repo_root=repo_root)
        if path is not None:
            return path
    source_root = str(artifact.get("source_root") or "").strip()
    storage_path = str(artifact.get("storage_path") or "").strip()
    if source_root and storage_path:
        candidate = Path(source_root) / storage_path
        if candidate.is_file():
            return candidate.resolve()
        parts = Path(storage_path.replace("\\", "/")).parts
        if "data" in parts:
            idx = parts.index("data")
            candidate = Path(source_root) / Path(*parts[idx:])
            if candidate.is_file():
                return candidate.resolve()
    return None


def _title(artifact: dict[str, Any], artifact_id: str) -> str:
    for key in ("short_description", "title", "caption", "heading"):
        value = str(artifact.get(key) or "").strip()
        if value:
            return value
    return artifact_id


def _description(artifact: dict[str, Any]) -> str:
    for key in ("detailed_description", "summary", "description", "retrieval_text"):
        value = str(artifact.get(key) or "").strip()
        if value:
            return value
    return ""


def _case_id(artifact: dict[str, Any], incident_ids: list[str] | set[str]) -> str:
    for key in ("case_id", "incident_id"):
        value = str(artifact.get(key) or "").strip()
        if value:
            return value.removeprefix("incident_").removeprefix("case_")
    source_id = str(artifact.get("source_id") or "")
    if source_id.startswith("case_"):
        return source_id.removeprefix("case_")
    for incident_id in incident_ids:
        cleaned = str(incident_id).strip()
        if cleaned:
            return cleaned.removeprefix("incident_").removeprefix("case_")
    return ""
