"""Teams chat image download helpers (hosted contents + image attachments)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from connectors.microsoft_graph.client import GraphClient
from connectors.microsoft_graph.errors import GraphProbeError

_IMAGE_CONTENT_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/bmp": ".bmp",
}
_IMAGE_NAME_RE = re.compile(r"\.(png|jpe?g|gif|webp|bmp)$", re.IGNORECASE)


def download_images_for_message(
    client: GraphClient,
    chat_id: str,
    message_id: str,
    message: dict[str, Any],
    images_dir: Path,
) -> list[str]:
    """Download inline hosted images and image file attachments for one message."""
    images_dir.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []
    saved.extend(_download_hosted_contents(client, chat_id, message_id, images_dir))
    saved.extend(_download_image_attachments(client, message, images_dir, message_id=message_id))
    return saved


def _download_hosted_contents(
    client: GraphClient,
    chat_id: str,
    message_id: str,
    images_dir: Path,
) -> list[str]:
    chat_q = quote(chat_id, safe="")
    msg_q = quote(message_id, safe="")
    list_path = f"/chats/{chat_q}/messages/{msg_q}/hostedContents"
    try:
        payload = client.get_json(list_path, context="list hostedContents")
    except GraphProbeError:
        return []

    saved: list[str] = []
    for index, item in enumerate(payload.get("value") or [], start=1):
        if not isinstance(item, dict):
            continue
        content_id = str(item.get("id") or "")
        if not content_id:
            continue
        # Prefer items that look like images; still try unknowns (Teams often omits contentType).
        content_type = str(item.get("contentType") or "").lower()
        if content_type and not content_type.startswith("image/") and "application/octet-stream" not in content_type:
            continue
        value_path = f"/chats/{chat_q}/messages/{msg_q}/hostedContents/{quote(content_id, safe='')}/$value"
        try:
            raw, response_type = client.get_bytes(value_path, context="hostedContent bytes")
        except GraphProbeError:
            continue
        if not raw:
            continue
        ext = _extension_for(response_type, content_type, fallback_sniff=raw)
        if ext is None:
            continue
        filename = f"{message_id}_{index}{ext}"
        path = images_dir / filename
        path.write_bytes(raw)
        saved.append(f"images/{filename}")
    return saved


def _download_image_attachments(
    client: GraphClient,
    message: dict[str, Any],
    images_dir: Path,
    *,
    message_id: str,
) -> list[str]:
    saved: list[str] = []
    attachments = message.get("attachments") or []
    for index, attachment in enumerate(attachments, start=1):
        if not isinstance(attachment, dict):
            continue
        name = str(attachment.get("name") or f"attachment_{index}")
        content_type = str(attachment.get("contentType") or "").lower()
        content_url = str(attachment.get("contentUrl") or "").strip()
        looks_image = content_type.startswith("image/") or bool(_IMAGE_NAME_RE.search(name))
        if not looks_image or not content_url:
            continue
        try:
            raw, response_type = client.get_bytes(content_url, context=f"attachment {name}")
        except GraphProbeError:
            continue
        if not raw:
            continue
        ext = _extension_for(response_type, content_type, name=name, fallback_sniff=raw)
        if ext is None:
            continue
        safe_name = re.sub(r"[^\w.\-]+", "_", name)
        if not safe_name.lower().endswith(ext):
            safe_name = f"{safe_name}{ext}"
        filename = f"{message_id}_{safe_name}"
        path = images_dir / filename
        path.write_bytes(raw)
        saved.append(f"images/{filename}")
    return saved


def _extension_for(
    response_type: str,
    declared_type: str = "",
    *,
    name: str = "",
    fallback_sniff: bytes | None = None,
) -> str | None:
    for candidate in (response_type, declared_type):
        mime = candidate.split(";")[0].strip().lower()
        if mime in _IMAGE_CONTENT_TYPES:
            return _IMAGE_CONTENT_TYPES[mime]
    match = _IMAGE_NAME_RE.search(name)
    if match:
        ext = match.group(1).lower()
        return ".jpg" if ext == "jpeg" else f".{ext}"
    if fallback_sniff:
        if fallback_sniff.startswith(b"\x89PNG\r\n\x1a\n"):
            return ".png"
        if fallback_sniff.startswith(b"\xff\xd8\xff"):
            return ".jpg"
        if fallback_sniff.startswith(b"GIF8"):
            return ".gif"
        if fallback_sniff.startswith(b"RIFF") and b"WEBP" in fallback_sniff[:16]:
            return ".webp"
    return None
