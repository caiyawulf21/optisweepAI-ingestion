"""Microsoft Graph / Teams connectivity probe (development only).

Primary mode: pull all messages from one named chat inside a date window.
Example: "Support chat for Haslet" for Case 00233681 dates.

Auth modes:
  device_code (default)  - sign in as yourself; only chats you belong to
  client_credentials     - app-only; needs admin-consented Chat.Read.All etc.

Azure app registration setup: connectors/microsoft_graph/README.md
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from connectors.microsoft_graph.auth import acquire_token, load_graph_credentials
from connectors.microsoft_graph.client import GraphClient
from connectors.microsoft_graph.errors import GraphProbeError
from connectors.microsoft_graph.teams_search import (
    infer_case_window_from_salesforce_probe,
    pull_chat_messages_by_topic,
    search_teams_for_case,
)

DEFAULT_OUT_ROOT = REPO_ROOT / "data" / "output" / "teams_probe"


def _parse_date(raw: str) -> date:
    return datetime.strptime(raw, "%Y-%m-%d").date()


def _slug(value: str) -> str:
    text = re.sub(r"[^\w\-]+", "_", value.strip()).strip("_")
    return text or "chat"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Development-only Microsoft Graph Teams chat probe.",
    )
    parser.add_argument(
        "--chat-topic",
        default="Support chat for Haslet",
        help='Exact Teams chat topic to read (default: "Support chat for Haslet").',
    )
    parser.add_argument(
        "--case-number",
        default="",
        help="Optional. If set (and --chat-topic empty), search chats/messages by case number.",
    )
    parser.add_argument(
        "--from-date",
        default="",
        help="Start date YYYY-MM-DD (UTC day).",
    )
    parser.add_argument(
        "--to-date",
        default="",
        help="End date YYYY-MM-DD (UTC day, inclusive).",
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="Output directory (default under data/output/teams_probe/).",
    )
    parser.add_argument(
        "--auth-only",
        action="store_true",
        help="Only authenticate and print signed-in user / token acquisition result.",
    )
    parser.add_argument(
        "--topic-contains",
        action="store_true",
        help="Allow substring topic match instead of exact match.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        credentials = load_graph_credentials()
        token = acquire_token(credentials)
    except GraphProbeError as exc:
        print(f"Microsoft Graph authentication failed: {exc}")
        return 1

    print("Microsoft Graph authentication successful.")
    print(f"Auth mode: {credentials.auth_mode}")
    print(f"Token acquired: yes (expires_in={token.expires_in or 'unknown'}s)")

    client = GraphClient(token)
    if args.auth_only:
        if credentials.auth_mode == "device_code":
            try:
                from connectors.microsoft_graph.teams_search import get_me

                me = get_me(client)
                print(f"Signed in as: {me.get('displayName')} <{me.get('userPrincipalName')}>")
            except GraphProbeError as exc:
                print(f"Signed-in user lookup failed: {exc}")
                return 2
        return 0

    from_date: date
    to_date: date
    if args.from_date and args.to_date:
        from_date = _parse_date(args.from_date)
        to_date = _parse_date(args.to_date)
    elif args.case_number:
        inferred = infer_case_window_from_salesforce_probe(args.case_number, REPO_ROOT)
        if inferred is None:
            print(
                "No --from-date/--to-date and no Salesforce probe feed found for that case. "
                "Pass --from-date/--to-date."
            )
            return 3
        from_date, to_date = inferred
        print(f"Date window inferred from Salesforce probe: {from_date} .. {to_date}")
    else:
        inferred = infer_case_window_from_salesforce_probe("00233681", REPO_ROOT)
        if inferred is None:
            print("Pass --from-date and --to-date (YYYY-MM-DD).")
            return 3
        from_date, to_date = inferred
        print(f"Date window inferred from Salesforce probe case 00233681: {from_date} .. {to_date}")

    if args.chat_topic:
        out_dir = (
            Path(args.out_dir)
            if args.out_dir
            else DEFAULT_OUT_ROOT / _slug(args.chat_topic)
        )
        try:
            result = pull_chat_messages_by_topic(
                client,
                args.chat_topic,
                from_date=from_date,
                to_date=to_date,
                output_dir=out_dir,
                exact_topic=not args.topic_contains,
            )
        except GraphProbeError as exc:
            print(f"Teams chat pull failed: {exc}")
            return 4
        print()
        print("Teams chat pull finished.")
        print(f"Chat: {result.chat_topic}")
        print(f"Signed in as: {result.me.get('displayName')} <{result.me.get('userPrincipalName')}>")
        print(f"Messages in window: {len(result.messages)}")
        print(f"Images downloaded: {len(result.downloaded_images)}")
        print(f"Output: {result.output_dir}")
        return 0

    if not args.case_number:
        print("Provide --chat-topic (preferred) or --case-number.")
        return 3

    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_ROOT / f"case_{args.case_number}"
    try:
        result = search_teams_for_case(
            client,
            args.case_number,
            from_date=from_date,
            to_date=to_date,
            output_dir=out_dir,
        )
    except GraphProbeError as exc:
        print(f"Teams search failed: {exc}")
        return 4

    print()
    print("Teams correlation probe finished.")
    print(f"Signed in as: {result.me.get('displayName')} <{result.me.get('userPrincipalName')}>")
    print(f"Topic-matching chats: {len(result.chats)}")
    print(f"Messages in window: {len(result.messages)}")
    print(f"Output: {result.output_dir}")
    if result.me.get("search_warning"):
        print(f"Warning: {result.me['search_warning']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
