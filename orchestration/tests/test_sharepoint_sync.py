from __future__ import annotations

from pathlib import Path

from orchestration.intake.sharepoint import (
    SharePointIntakeConfig,
    ensure_sharepoint_sync_layout,
    poll_sharepoint_once,
    push_review_outputs,
)


def test_sync_poll_copies_and_moves(tmp_path: Path, monkeypatch) -> None:
    sync = tmp_path / "sp"
    local_inbox = tmp_path / "inbox"
    cfg = SharePointIntakeConfig(sync_root=sync, local_inbox=local_inbox)
    ensure_sharepoint_sync_layout(cfg)
    src = sync / "inbox" / "incidents" / "Case 228086 Data.pdf"
    src.write_bytes(b"%PDF-1.4 test")

    monkeypatch.setattr("orchestration.intake.sharepoint.INBOX_ROOT", local_inbox)
    monkeypatch.setattr("orchestration.paths.INBOX_ROOT", local_inbox)

    arrived = poll_sharepoint_once(cfg)
    assert len(arrived) == 1
    assert arrived[0].name == "Case 228086 Data.pdf"
    assert arrived[0].exists()
    assert not src.exists()
    assert (sync / "_processed" / "incidents" / "Case 228086 Data.pdf").exists()


def test_sync_push_review(tmp_path: Path) -> None:
    sync = tmp_path / "sp"
    review = tmp_path / "sme_review"
    cfg = SharePointIntakeConfig(sync_root=sync)
    ensure_sharepoint_sync_layout(cfg)
    md = review / "case_228086" / "runbook.md"
    md.parent.mkdir(parents=True)
    md.write_text("# review\n", encoding="utf-8")

    summary = push_review_outputs(cfg, review_dir=review)
    assert summary["uploaded"] == 1
    assert (sync / "review" / "case_228086" / "runbook.md").read_text(encoding="utf-8") == "# review\n"
