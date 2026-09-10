from __future__ import annotations

import re
import shutil
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from orchestration.graph.ingestion_graph import run_ingestion
from orchestration.intake.sharepoint import (
    load_sharepoint_config,
    poll_sharepoint_once,
    push_review_outputs,
)
from orchestration.paths import (
    INBOX_FAILED,
    INBOX_PROCESSED,
    INBOX_PROCESSING,
    INBOX_ROOT,
    ensure_inbox_layout,
)
from orchestration.routing import is_ingestible_file
from orchestration.state import IngestionState

TRANSCRIPT_SUFFIXES = {".vtt", ".srt"}
STAMPED_NAME_RE = re.compile(r"^\d{8}T\d{6}Z_(.+)$")


def wait_until_stable(path: Path, *, settle_seconds: float = 3.0, timeout_seconds: float = 300.0) -> bool:
    deadline = time.time() + timeout_seconds
    last_size = -1
    stable_since: float | None = None
    while time.time() < deadline:
        if not path.exists():
            existing = _find_processing_copy(path)
            return existing is not None
        try:
            size = path.stat().st_size
        except OSError:
            time.sleep(0.5)
            continue
        if size == last_size and size > 0:
            if stable_since is None:
                stable_since = time.time()
            elif time.time() - stable_since >= settle_seconds:
                return True
        else:
            stable_since = None
            last_size = size
        time.sleep(0.5)
    return path.exists() or _find_processing_copy(path) is not None


def _find_processing_copy(source_path: Path) -> Path | None:
    wanted = original_filename(source_path).casefold()
    if not INBOX_PROCESSING.exists():
        return None
    matches = sorted(
        (
            path
            for path in INBOX_PROCESSING.iterdir()
            if path.is_file() and original_filename(path).casefold() == wanted
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def original_filename(path: Path) -> str:
    match = STAMPED_NAME_RE.match(path.name)
    return match.group(1) if match else path.name


def stamped_target(destination_root: Path, source_path: Path) -> Path:
    destination_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return destination_root / f"{stamp}_{original_filename(source_path)}"


def safe_relocate(
    source_path: Path,
    destination_root: Path,
    *,
    copy_first: bool = False,
    retries: int = 12,
    retry_delay_seconds: float = 1.0,
) -> Path:
    target = stamped_target(destination_root, source_path)
    last_error: OSError | None = None
    for attempt in range(1, retries + 1):
        try:
            if not source_path.exists():
                if target.exists():
                    return target
                existing = _find_processing_copy(source_path) if destination_root == INBOX_PROCESSING else None
                if existing is not None:
                    return existing
                raise FileNotFoundError(source_path)
            if copy_first:
                shutil.copy2(str(source_path), str(target))
                _safe_unlink(source_path, retries=retries, retry_delay_seconds=retry_delay_seconds)
            else:
                shutil.move(str(source_path), str(target))
            return target
        except OSError as exc:
            last_error = exc
            if getattr(exc, "winerror", None) not in {32, 33} and exc.errno not in {13, 16}:
                pass
            time.sleep(retry_delay_seconds * attempt)
    assert last_error is not None
    raise last_error


def _safe_unlink(path: Path, *, retries: int = 8, retry_delay_seconds: float = 0.75) -> None:
    for attempt in range(1, retries + 1):
        try:
            if path.exists():
                path.unlink()
            return
        except OSError:
            time.sleep(retry_delay_seconds * attempt)


def find_companions(source_path: Path) -> list[Path]:
    return [
        p
        for p in source_path.parent.glob(f"{source_path.stem}*")
        if p.is_file() and p != source_path and p.suffix.lower() in TRANSCRIPT_SUFFIXES
    ]


def process_inbox_file(
    source_path: Path,
    *,
    use_llm: bool = True,
    run_shared_publish: bool = True,
    publish_to_cosmos: bool = False,
    publish_scope: str = "all",
    source_stages: str | None = None,
    shared_stages: str | None = None,
    max_workers: int = 4,
    push_sharepoint_review: bool = True,
) -> IngestionState:
    ensure_inbox_layout()
    if not wait_until_stable(source_path):
        existing = _find_processing_copy(source_path)
        if existing is None:
            raise TimeoutError(f"Timed out waiting for upload to finish: {source_path}")
        processing_path = existing
        processing_companions: list[Path] = []
    else:
        companions = find_companions(source_path) if source_path.exists() else []
        if source_path.exists():
            processing_path = safe_relocate(source_path, INBOX_PROCESSING, copy_first=True)
            processing_companions = [
                safe_relocate(path, INBOX_PROCESSING, copy_first=True) for path in companions
            ]
        else:
            processing_path = _find_processing_copy(source_path)
            if processing_path is None:
                raise FileNotFoundError(f"Upload disappeared before processing: {source_path}")
            processing_companions = []

    try:
        result = run_ingestion(
            processing_path,
            companion_paths=processing_companions,
            use_llm=use_llm,
            run_shared_publish=run_shared_publish,
            publish_to_cosmos=publish_to_cosmos,
            publish_scope=publish_scope,
            source_stages=source_stages,
            shared_stages=shared_stages,
            max_workers=max_workers,
        )
        time.sleep(1.0)
        destination = INBOX_PROCESSED if result.get("status") == "succeeded" else INBOX_FAILED
        safe_relocate(processing_path, destination, copy_first=True)
        for companion in processing_companions:
            if companion.exists():
                safe_relocate(companion, destination, copy_first=True)
        if push_sharepoint_review and result.get("status") == "succeeded":
            sp = load_sharepoint_config()
            if sp.is_configured():
                summary = push_review_outputs(sp)
                messages = list(result.get("messages") or [])
                messages.append(
                    f"SharePoint review sync: uploaded={summary.get('uploaded')} skipped={summary.get('skipped')}"
                )
                result = {**result, "messages": messages}
        return result
    except Exception:
        time.sleep(1.0)
        if processing_path.exists():
            safe_relocate(processing_path, INBOX_FAILED, copy_first=True)
        for companion in processing_companions:
            if companion.exists():
                safe_relocate(companion, INBOX_FAILED, copy_first=True)
        raise


class InboxWatcher:
    def __init__(
        self,
        *,
        use_llm: bool = True,
        run_shared_publish: bool = True,
        publish_to_cosmos: bool = False,
        publish_scope: str = "all",
        source_stages: str | None = None,
        shared_stages: str | None = None,
        max_workers: int = 4,
        debounce_seconds: float = 3.0,
        push_sharepoint_review: bool = True,
    ) -> None:
        self.use_llm = use_llm
        self.run_shared_publish = run_shared_publish
        self.publish_to_cosmos = publish_to_cosmos
        self.publish_scope = publish_scope
        self.source_stages = source_stages
        self.shared_stages = shared_stages
        self.max_workers = max_workers
        self.debounce_seconds = debounce_seconds
        self.push_sharepoint_review = push_sharepoint_review
        self._lock = threading.Lock()
        self._queued_keys: set[str] = set()

    def handle_path(self, path: Path) -> None:
        try:
            resolved = path.resolve()
        except OSError:
            return
        if INBOX_PROCESSING in resolved.parents or INBOX_PROCESSED in resolved.parents or INBOX_FAILED in resolved.parents:
            return
        if not is_ingestible_file(resolved):
            return
        queue_key = original_filename(resolved).casefold()
        with self._lock:
            if queue_key in self._queued_keys:
                return
            self._queued_keys.add(queue_key)

        def _run() -> None:
            try:
                time.sleep(self.debounce_seconds)
                if not resolved.exists():
                    return
                print(f"[inbox] starting ingestion for {resolved}")
                result = process_inbox_file(
                    resolved,
                    use_llm=self.use_llm,
                    run_shared_publish=self.run_shared_publish,
                    publish_to_cosmos=self.publish_to_cosmos,
                    publish_scope=self.publish_scope,
                    source_stages=self.source_stages,
                    shared_stages=self.shared_stages,
                    max_workers=self.max_workers,
                    push_sharepoint_review=self.push_sharepoint_review,
                )
                status = result.get("status")
                print(f"[inbox] finished {resolved.name}: status={status}")
                for message in result.get("messages") or []:
                    print(f"  {message}")
                for error in result.get("errors") or []:
                    print(f"  ERROR: {error}")
            except Exception as exc:
                print(f"[inbox] failed {resolved}: {exc}")
            finally:
                with self._lock:
                    self._queued_keys.discard(queue_key)

        threading.Thread(target=_run, daemon=True).start()

    def scan_existing(self) -> None:
        for lane in ("incidents", "manuals", "videos"):
            root = INBOX_ROOT / lane
            if not root.is_dir():
                continue
            for path in sorted(root.iterdir()):
                if path.is_file() and is_ingestible_file(path):
                    self.handle_path(path)


def start_watch(
    *,
    use_llm: bool = True,
    run_shared_publish: bool = True,
    publish_to_cosmos: bool = False,
    publish_scope: str = "all",
    source_stages: str | None = None,
    shared_stages: str | None = None,
    max_workers: int = 4,
    push_sharepoint_review: bool = True,
    poll_sharepoint_seconds: float = 0.0,
) -> None:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    ensure_inbox_layout()
    watcher = InboxWatcher(
        use_llm=use_llm,
        run_shared_publish=run_shared_publish,
        publish_to_cosmos=publish_to_cosmos,
        publish_scope=publish_scope,
        source_stages=source_stages,
        shared_stages=shared_stages,
        max_workers=max_workers,
        push_sharepoint_review=push_sharepoint_review,
    )

    class Handler(FileSystemEventHandler):
        def on_created(self, event) -> None:  # noqa: ANN001
            if event.is_directory:
                return
            watcher.handle_path(Path(event.src_path))

        def on_moved(self, event) -> None:  # noqa: ANN001
            if event.is_directory:
                return
            watcher.handle_path(Path(event.dest_path))

    observer = Observer()
    observer.schedule(Handler(), str(INBOX_ROOT), recursive=True)
    observer.start()
    print(f"[inbox] watching {INBOX_ROOT}")
    print("[inbox] drop files into incidents/, manuals/, or videos/")
    print(
        f"[inbox] defaults: with_publish={run_shared_publish} "
        f"publish_to_cosmos={publish_to_cosmos} publish_scope={publish_scope}"
    )
    sp = load_sharepoint_config()
    if sp.is_configured():
        print(f"[inbox] SharePoint mode={sp.mode} — poll every {poll_sharepoint_seconds or 30:.0f}s")
        if poll_sharepoint_seconds <= 0:
            poll_sharepoint_seconds = 30.0
    watcher.scan_existing()
    last_poll = 0.0
    try:
        while True:
            now = time.time()
            if sp.is_configured() and poll_sharepoint_seconds > 0 and now - last_poll >= poll_sharepoint_seconds:
                try:
                    arrived = poll_sharepoint_once(sp)
                    for path in arrived:
                        print(f"[inbox] SharePoint brought {path}")
                        watcher.handle_path(path)
                except Exception as exc:
                    print(f"[inbox] SharePoint poll failed: {exc}")
                last_poll = now
            time.sleep(1)
    except KeyboardInterrupt:
        print("[inbox] stopping")
        observer.stop()
    observer.join()
