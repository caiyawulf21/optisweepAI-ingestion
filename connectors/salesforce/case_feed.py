"""Case feed + file retrieval (raw Salesforce data only)."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from html import unescape
from pathlib import Path
from typing import Any

from connectors.salesforce.case_repository import CaseSummary
from connectors.salesforce.client import SalesforceClient
from connectors.salesforce.errors import CATEGORY_QUERY_FAILED, SalesforceProbeError
from connectors.salesforce.http_util import build_content_version_data_url

_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "tif", "tiff"}
_HTML_TAG_RE = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class CaseFeedEntry:
    id: str
    type: str
    created_date: str
    created_by: str
    body: str
    title: str
    related_record_id: str


@dataclass(frozen=True)
class CaseEmailEntry:
    id: str
    subject: str
    incoming: bool
    message_date: str
    from_address: str
    to_address: str
    text_body: str


@dataclass(frozen=True)
class CaseFileMeta:
    content_document_id: str
    title: str
    file_extension: str
    file_type: str
    content_size: int
    version_id: str
    is_image: bool


@dataclass
class CaseFeedPullResult:
    case: CaseSummary
    feed: list[CaseFeedEntry] = field(default_factory=list)
    emails: list[CaseEmailEntry] = field(default_factory=list)
    files: list[CaseFileMeta] = field(default_factory=list)
    downloaded_files: list[str] = field(default_factory=list)
    output_dir: str = ""


def fetch_case_feed(client: SalesforceClient, case_id: str) -> list[CaseFeedEntry]:
    soql = (
        "SELECT Id, Type, CreatedDate, CreatedBy.Name, Body, Title, RelatedRecordId "
        f"FROM CaseFeed WHERE ParentId = '{case_id}' ORDER BY CreatedDate ASC"
    )
    try:
        records = client.query_all(soql)
    except SalesforceProbeError as exc:
        raise SalesforceProbeError(
            CATEGORY_QUERY_FAILED,
            f"CaseFeed query failed: {exc.args[0]}",
        ) from None

    entries: list[CaseFeedEntry] = []
    for record in records:
        created_by = ""
        created = record.get("CreatedBy")
        if isinstance(created, dict):
            created_by = str(created.get("Name") or "")
        entries.append(
            CaseFeedEntry(
                id=str(record.get("Id") or ""),
                type=str(record.get("Type") or ""),
                created_date=str(record.get("CreatedDate") or ""),
                created_by=created_by,
                body=_html_to_text(str(record.get("Body") or "")),
                title=str(record.get("Title") or ""),
                related_record_id=str(record.get("RelatedRecordId") or ""),
            )
        )
    return entries


def fetch_case_emails(client: SalesforceClient, case_id: str) -> list[CaseEmailEntry]:
    soql = (
        "SELECT Id, Subject, Incoming, MessageDate, FromAddress, ToAddress, TextBody "
        f"FROM EmailMessage WHERE ParentId = '{case_id}' ORDER BY MessageDate ASC"
    )
    try:
        records = client.query_all(soql)
    except SalesforceProbeError as exc:
        raise SalesforceProbeError(
            CATEGORY_QUERY_FAILED,
            f"EmailMessage query failed: {exc.args[0]}",
        ) from None

    emails: list[CaseEmailEntry] = []
    for record in records:
        emails.append(
            CaseEmailEntry(
                id=str(record.get("Id") or ""),
                subject=str(record.get("Subject") or ""),
                incoming=bool(record.get("Incoming")),
                message_date=str(record.get("MessageDate") or ""),
                from_address=str(record.get("FromAddress") or ""),
                to_address=str(record.get("ToAddress") or ""),
                text_body=str(record.get("TextBody") or ""),
            )
        )
    return emails


def fetch_case_files(client: SalesforceClient, case_id: str) -> list[CaseFileMeta]:
    soql = (
        "SELECT ContentDocumentId, ContentDocument.Title, ContentDocument.FileType, "
        "ContentDocument.FileExtension, ContentDocument.ContentSize, "
        "ContentDocument.LatestPublishedVersionId "
        f"FROM ContentDocumentLink WHERE LinkedEntityId = '{case_id}'"
    )
    try:
        records = client.query_all(soql)
    except SalesforceProbeError as exc:
        raise SalesforceProbeError(
            CATEGORY_QUERY_FAILED,
            f"ContentDocumentLink query failed: {exc.args[0]}",
        ) from None

    files: list[CaseFileMeta] = []
    for record in records:
        doc = record.get("ContentDocument") or {}
        if not isinstance(doc, dict):
            doc = {}
        extension = str(doc.get("FileExtension") or "").lower().lstrip(".")
        files.append(
            CaseFileMeta(
                content_document_id=str(record.get("ContentDocumentId") or ""),
                title=str(doc.get("Title") or ""),
                file_extension=extension,
                file_type=str(doc.get("FileType") or ""),
                content_size=int(doc.get("ContentSize") or 0),
                version_id=str(doc.get("LatestPublishedVersionId") or ""),
                is_image=extension in _IMAGE_EXTENSIONS,
            )
        )
    return files


def download_case_file(client: SalesforceClient, file_meta: CaseFileMeta) -> bytes:
    if not file_meta.version_id:
        raise SalesforceProbeError(
            CATEGORY_QUERY_FAILED,
            f"File '{file_meta.title}' has no LatestPublishedVersionId.",
        )
    path = build_content_version_data_url(
        client.session.instance_url,
        client.session.api_version,
        file_meta.version_id,
    )
    return client.get_bytes(path, context=f"ContentVersion {file_meta.version_id}")


def pull_case_feed_and_images(
    client: SalesforceClient,
    case: CaseSummary,
    output_dir: Path,
    *,
    images_only: bool = True,
) -> CaseFeedPullResult:
    """Fetch CaseFeed, emails, and files; write JSON/markdown + downloaded binaries."""
    output_dir.mkdir(parents=True, exist_ok=True)
    images_dir = output_dir / "images"
    files_dir = output_dir / "files"
    images_dir.mkdir(exist_ok=True)
    files_dir.mkdir(exist_ok=True)

    feed = fetch_case_feed(client, case.id)
    emails = fetch_case_emails(client, case.id)
    files = fetch_case_files(client, case.id)

    downloaded: list[str] = []
    for file_meta in files:
        if images_only and not file_meta.is_image:
            continue
        raw = download_case_file(client, file_meta)
        target_dir = images_dir if file_meta.is_image else files_dir
        filename = _safe_filename(file_meta.title, file_meta.file_extension, file_meta.version_id)
        path = target_dir / filename
        path.write_bytes(raw)
        downloaded.append(str(path.relative_to(output_dir)).replace("\\", "/"))

    result = CaseFeedPullResult(
        case=case,
        feed=feed,
        emails=emails,
        files=files,
        downloaded_files=downloaded,
        output_dir=str(output_dir),
    )
    _write_feed_artifacts(output_dir, result)
    return result


def _write_feed_artifacts(output_dir: Path, result: CaseFeedPullResult) -> None:
    payload: dict[str, Any] = {
        "case": asdict(result.case),
        "feed": [asdict(entry) for entry in result.feed],
        "emails": [asdict(entry) for entry in result.emails],
        "files": [asdict(entry) for entry in result.files],
        "downloaded_files": result.downloaded_files,
    }
    (output_dir / "case_feed.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        f"# Case {result.case.case_number}",
        "",
        f"- Subject: {result.case.subject}",
        f"- Status: {result.case.status}",
        f"- Salesforce ID: {result.case.id}",
        "",
        "## Feed",
        "",
    ]
    for entry in result.feed:
        header = f"### {entry.created_date} | {entry.type} | {entry.created_by}"
        lines.append(header)
        if entry.title:
            lines.append(f"**Title:** {entry.title}")
        body = entry.body.strip() or "(no body)"
        lines.append(body)
        lines.append("")

    if result.emails:
        lines.extend(["## Emails", ""])
        for email in result.emails:
            direction = "incoming" if email.incoming else "outgoing"
            lines.append(f"### {email.message_date} | {direction} | {email.subject}")
            lines.append(email.text_body.strip() or "(no body)")
            lines.append("")

    if result.downloaded_files:
        lines.extend(["## Downloaded files", ""])
        for relative in result.downloaded_files:
            lines.append(f"- `{relative}`")
        lines.append("")

    (output_dir / "case_feed.md").write_text("\n".join(lines), encoding="utf-8")


def _html_to_text(value: str) -> str:
    if not value:
        return ""
    text = value.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    text = text.replace("</p>", "\n").replace("<p>", "")
    text = _HTML_TAG_RE.sub("", text)
    return unescape(text).strip()


def _safe_filename(title: str, extension: str, version_id: str) -> str:
    base = re.sub(r"[^\w.\-]+", "_", title).strip("._") or version_id
    base = re.sub(r"_+", "_", base)
    ext = extension.lower().lstrip(".")
    if ext and not base.lower().endswith(f".{ext}"):
        return f"{base}.{ext}"
    return base
