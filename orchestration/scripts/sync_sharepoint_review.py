#!/usr/bin/env python
"""One-shot: pull SharePoint inbox and/or push local SME review to SharePoint."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.intake.sharepoint import (
    ensure_sharepoint_sync_layout,
    load_sharepoint_config,
    poll_sharepoint_once,
    push_review_outputs,
)
from orchestration.paths import OUTPUT_SME_REVIEW, ensure_inbox_layout


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync SharePoint inbox/review with local ingestion folders.")
    parser.add_argument("--pull-inbox", action="store_true", help="Copy new SharePoint inbox files into data/inbox.")
    parser.add_argument("--push-review", action="store_true", help="Mirror data/output/sme_review to SharePoint review/.")
    parser.add_argument("--review-dir", type=Path, default=None)
    args = parser.parse_args()

    if not args.pull_inbox and not args.push_review:
        args.pull_inbox = True
        args.push_review = True

    cfg = load_sharepoint_config()
    if not cfg.is_configured():
        raise SystemExit(
            "SharePoint not configured. Set SHAREPOINT_SYNC_ROOT or Graph app credentials "
            "(SHAREPOINT_TENANT_ID/CLIENT_ID/CLIENT_SECRET + SHAREPOINT_SITE_URL)."
        )

    ensure_inbox_layout()
    if cfg.mode == "sync":
        ensure_sharepoint_sync_layout(cfg)
        print(f"mode=sync root={cfg.sync_root}")
    else:
        print(f"mode=graph site={cfg.site_url or cfg.site_id} library={cfg.library_name}")

    if args.pull_inbox:
        arrived = poll_sharepoint_once(cfg)
        print(f"pulled {len(arrived)} ingestible file(s) into data/inbox/")
        for path in arrived:
            print(f"  {path}")

    if args.push_review:
        summary = push_review_outputs(cfg, review_dir=args.review_dir or OUTPUT_SME_REVIEW)
        print(f"review sync: uploaded={summary.get('uploaded')} skipped={summary.get('skipped')}")


if __name__ == "__main__":
    main()
