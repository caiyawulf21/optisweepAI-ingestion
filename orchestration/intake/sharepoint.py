"""SharePoint intake + review outbox.

Two modes (pick one via env):

1. Synced-folder (recommended for local handoff)
   Point SHAREPOINT_SYNC_ROOT at a OneDrive/SharePoint-synced library that contains:
     inbox/{incidents,manuals,videos}/   <- operators drop sources here
     review/                             <- SME markdown mirror is written here
   The watcher copies new inbox files into data/inbox/, runs the agent, then
   mirrors data/output/sme_review/ into SHAREPOINT_SYNC_ROOT/review/.

2. Microsoft Graph (app registration)
   Set SHAREPOINT_TENANT_ID, SHAREPOINT_CLIENT_ID, SHAREPOINT_CLIENT_SECRET,
   SHAREPOINT_SITE_URL (or SHAREPOINT_SITE_ID), optional SHAREPOINT_LIBRARY,
   SHAREPOINT_INBOX_FOLDER, SHAREPOINT_REVIEW_FOLDER.
   Poll downloads new files into data/inbox/; after ingest, uploads review files.

Neither mode replaces local data/inbox — SharePoint is a remote front door.
"""

from __future__ import annotations

import json
import os
import shutil
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from orchestration.paths import INBOX_ROOT, OUTPUT_SME_REVIEW, ensure_inbox_layout
from orchestration.routing import is_ingestible_file

GRAPH_ROOT = "https://graph.microsoft.com/v1.0"
INGEST_SUFFIXES = {".pdf", ".mp4", ".mov", ".mkv", ".webm"}
TRANSCRIPT_SUFFIXES = {".vtt", ".srt"}
REVIEW_SUFFIXES = {".md", ".html", ".json", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


@dataclass(frozen=True)
class SharePointIntakeConfig:
    site_url: str = ""
    library_name: str = "Documents"
    folder_path: str = "inbox"
    review_folder: str = "review"
    local_inbox: Path | None = None
    sync_root: Path | None = None
    tenant_id: str = ""
    client_id: str = ""
    client_secret: str = ""
    site_id: str = ""
    drive_id: str = ""

    @property
    def mode(self) -> str:
        if self.sync_root:
            return "sync"
        if self.tenant_id and self.client_id and self.client_secret and (self.site_url or self.site_id):
            return "graph"
        return "none"

    def is_configured(self) -> bool:
        return self.mode != "none"


def load_sharepoint_config() -> SharePointIntakeConfig:
    load_dotenv()
    sync = _clean(os.getenv("SHAREPOINT_SYNC_ROOT"))
    return SharePointIntakeConfig(
        site_url=_clean(os.getenv("SHAREPOINT_SITE_URL")),
        library_name=_clean(os.getenv("SHAREPOINT_LIBRARY")) or "Documents",
        folder_path=_clean(os.getenv("SHAREPOINT_INBOX_FOLDER")) or "inbox",
        review_folder=_clean(os.getenv("SHAREPOINT_REVIEW_FOLDER")) or "review",
        local_inbox=INBOX_ROOT,
        sync_root=Path(sync) if sync else None,
        tenant_id=_clean(os.getenv("SHAREPOINT_TENANT_ID")),
        client_id=_clean(os.getenv("SHAREPOINT_CLIENT_ID")),
        client_secret=_clean(os.getenv("SHAREPOINT_CLIENT_SECRET")),
        site_id=_clean(os.getenv("SHAREPOINT_SITE_ID")),
        drive_id=_clean(os.getenv("SHAREPOINT_DRIVE_ID")),
    )


def ensure_sharepoint_sync_layout(config: SharePointIntakeConfig | None = None) -> Path | None:
    cfg = config or load_sharepoint_config()
    if cfg.mode != "sync" or cfg.sync_root is None:
        return None
    root = cfg.sync_root
    for rel in (
        "inbox/incidents",
        "inbox/manuals",
        "inbox/videos",
        "review",
        "_processed",
        "_failed",
    ):
        (root / rel).mkdir(parents=True, exist_ok=True)
    readme = root / "README.md"
    if not readme.exists():
        readme.write_text(
            "# OptiSweep SharePoint sync library\n\n"
            "Drop sources under `inbox/incidents`, `inbox/manuals`, or `inbox/videos`.\n"
            "SME review markdown appears under `review/` after ingestion.\n",
            encoding="utf-8",
        )
    return root


def poll_sharepoint_once(config: SharePointIntakeConfig | None = None) -> list[Path]:
    """Download/copy new SharePoint inbox files into local data/inbox. Returns local paths."""
    cfg = config or load_sharepoint_config()
    if cfg.mode == "sync":
        return _poll_sync_inbox(cfg)
    if cfg.mode == "graph":
        return _poll_graph_inbox(cfg)
    raise NotImplementedError(
        "SharePoint is not configured. Set SHAREPOINT_SYNC_ROOT (OneDrive sync) "
        "or SHAREPOINT_TENANT_ID/CLIENT_ID/CLIENT_SECRET + SHAREPOINT_SITE_URL."
    )


def push_review_outputs(
    config: SharePointIntakeConfig | None = None,
    *,
    review_dir: Path | None = None,
) -> dict[str, int]:
    """Mirror local SME review outputs into SharePoint review folder."""
    cfg = config or load_sharepoint_config()
    source = review_dir or OUTPUT_SME_REVIEW
    if not source.is_dir():
        return {"uploaded": 0, "skipped": 0}
    if cfg.mode == "sync":
        return _push_sync_review(cfg, source)
    if cfg.mode == "graph":
        return _push_graph_review(cfg, source)
    return {"uploaded": 0, "skipped": 0}


def _poll_sync_inbox(config: SharePointIntakeConfig) -> list[Path]:
    ensure_inbox_layout()
    ensure_sharepoint_sync_layout(config)
    assert config.sync_root is not None
    local_inbox = config.local_inbox or INBOX_ROOT
    remote_inbox = config.sync_root / "inbox"
    if not remote_inbox.is_dir():
        return []
    copied: list[Path] = []
    for path in sorted(remote_inbox.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in INGEST_SUFFIXES | TRANSCRIPT_SUFFIXES:
            continue
        rel = path.relative_to(remote_inbox)
        lane = rel.parts[0] if rel.parts else ""
        if lane not in {"incidents", "manuals", "videos"}:
            continue
        dest = local_inbox / rel
        if dest.exists() and dest.stat().st_size == path.stat().st_size:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        if is_ingestible_file(dest):
            copied.append(dest)
        processed = config.sync_root / "_processed" / rel
        processed.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(processed))
    return copied


def _push_sync_review(config: SharePointIntakeConfig, review_dir: Path) -> dict[str, int]:
    ensure_sharepoint_sync_layout(config)
    assert config.sync_root is not None
    dest_root = config.sync_root / "review"
    uploaded = 0
    skipped = 0
    for path in sorted(review_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in REVIEW_SUFFIXES:
            continue
        rel = path.relative_to(review_dir)
        dest = dest_root / rel
        if dest.exists() and dest.stat().st_size == path.stat().st_size and dest.stat().st_mtime >= path.stat().st_mtime:
            skipped += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        uploaded += 1
    return {"uploaded": uploaded, "skipped": skipped}


class _GraphClient:
    def __init__(self, config: SharePointIntakeConfig) -> None:
        self.config = config
        self._token: str | None = None
        self._site_id = config.site_id
        self._drive_id = config.drive_id

    def token(self) -> str:
        if self._token:
            return self._token
        url = f"https://login.microsoftonline.com/{self.config.tenant_id}/oauth2/v2.0/token"
        body = urllib.parse.urlencode(
            {
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "scope": "https://graph.microsoft.com/.default",
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        token = payload.get("access_token")
        if not token:
            raise RuntimeError("SharePoint Graph auth failed: no access_token")
        self._token = token
        return token

    def request(self, method: str, url: str, *, data: bytes | None = None, content_type: str | None = None) -> bytes:
        headers = {"Authorization": f"Bearer {self.token()}"}
        if content_type:
            headers["Content-Type"] = content_type
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Graph {method} {url} failed HTTP {exc.code}: {details[:800]}") from exc

    def site_id(self) -> str:
        if self._site_id:
            return self._site_id
        parsed = urllib.parse.urlparse(self.config.site_url)
        hostname = parsed.netloc
        path = parsed.path.strip("/")
        if not hostname or not path:
            raise RuntimeError("SHAREPOINT_SITE_URL must look like https://contoso.sharepoint.com/sites/OptiSweep")
        payload = json.loads(self.request("GET", f"{GRAPH_ROOT}/sites/{hostname}:/{path}").decode("utf-8"))
        self._site_id = payload["id"]
        return self._site_id

    def drive_id(self) -> str:
        if self._drive_id:
            return self._drive_id
        payload = json.loads(self.request("GET", f"{GRAPH_ROOT}/sites/{self.site_id()}/drives").decode("utf-8"))
        wanted = self.config.library_name.casefold()
        for drive in payload.get("value") or []:
            if str(drive.get("name") or "").casefold() == wanted:
                self._drive_id = drive["id"]
                return self._drive_id
        names = [d.get("name") for d in payload.get("value") or []]
        raise RuntimeError(f"SharePoint library '{self.config.library_name}' not found. Available: {names}")

    def list_children(self, folder_path: str) -> list[dict]:
        encoded = urllib.parse.quote(folder_path.strip("/"), safe="/")
        url = f"{GRAPH_ROOT}/drives/{self.drive_id()}/root:/{encoded}:/children"
        payload = json.loads(self.request("GET", url).decode("utf-8"))
        return list(payload.get("value") or [])

    def download_item(self, item_id: str, dest: Path) -> Path:
        data = self.request("GET", f"{GRAPH_ROOT}/drives/{self.drive_id()}/items/{item_id}/content")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return dest

    def upload_file(self, remote_path: str, local_path: Path) -> None:
        encoded = urllib.parse.quote(remote_path.strip("/"), safe="/")
        size = local_path.stat().st_size
        data = local_path.read_bytes()
        if size <= 4 * 1024 * 1024:
            url = f"{GRAPH_ROOT}/drives/{self.drive_id()}/root:/{encoded}:/content"
            self.request("PUT", url, data=data, content_type="application/octet-stream")
            return
        session_url = f"{GRAPH_ROOT}/drives/{self.drive_id()}/root:/{encoded}:/createUploadSession"
        session = json.loads(
            self.request(
                "POST",
                session_url,
                data=json.dumps(
                    {"item": {"@microsoft.graph.conflictBehavior": "replace", "name": local_path.name}}
                ).encode("utf-8"),
                content_type="application/json",
            ).decode("utf-8")
        )
        upload_url = session["uploadUrl"]
        chunk = 320 * 1024 * 10
        offset = 0
        while offset < size:
            end = min(offset + chunk, size) - 1
            part = data[offset : end + 1]
            req = urllib.request.Request(
                upload_url,
                data=part,
                headers={
                    "Content-Length": str(len(part)),
                    "Content-Range": f"bytes {offset}-{end}/{size}",
                },
                method="PUT",
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                resp.read()
            offset = end + 1

    def move_item(self, item_id: str, dest_folder_path: str, name: str) -> None:
        folder_encoded = urllib.parse.quote(dest_folder_path.strip("/"), safe="/")
        folder = json.loads(
            self.request("GET", f"{GRAPH_ROOT}/drives/{self.drive_id()}/root:/{folder_encoded}").decode("utf-8")
        )
        body = json.dumps({"parentReference": {"id": folder["id"]}, "name": name}).encode("utf-8")
        self.request(
            "PATCH",
            f"{GRAPH_ROOT}/drives/{self.drive_id()}/items/{item_id}",
            data=body,
            content_type="application/json",
        )


def _poll_graph_inbox(config: SharePointIntakeConfig) -> list[Path]:
    ensure_inbox_layout()
    client = _GraphClient(config)
    local_inbox = config.local_inbox or INBOX_ROOT
    copied: list[Path] = []
    for lane in ("incidents", "manuals", "videos"):
        folder = f"{config.folder_path.strip('/')}/{lane}"
        try:
            children = client.list_children(folder)
        except RuntimeError as exc:
            if "404" in str(exc) or "itemNotFound" in str(exc):
                continue
            raise
        for item in children:
            name = item.get("name") or ""
            if "folder" in item or not name:
                continue
            suffix = Path(name).suffix.lower()
            if suffix not in INGEST_SUFFIXES | TRANSCRIPT_SUFFIXES:
                continue
            dest = local_inbox / lane / name
            if dest.exists() and dest.stat().st_size == int(item.get("size") or 0):
                continue
            client.download_item(item["id"], dest)
            try:
                client.move_item(item["id"], f"{config.folder_path.strip('/')}/_processed/{lane}", name)
            except RuntimeError:
                pass
            if is_ingestible_file(dest):
                copied.append(dest)
    return copied


def _push_graph_review(config: SharePointIntakeConfig, review_dir: Path) -> dict[str, int]:
    client = _GraphClient(config)
    uploaded = 0
    skipped = 0
    for path in sorted(review_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in REVIEW_SUFFIXES:
            continue
        rel = path.relative_to(review_dir).as_posix()
        remote = f"{config.review_folder.strip('/')}/{rel}"
        try:
            client.upload_file(remote, path)
            uploaded += 1
        except RuntimeError:
            skipped += 1
    return {"uploaded": uploaded, "skipped": skipped}


def _clean(value: str | None) -> str:
    return (value or "").strip().strip('"').strip("'")
