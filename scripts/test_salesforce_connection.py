"""Salesforce connectivity probe (development only).

Answers:
  1) Can these credentials authenticate to the Salesforce API?
  2) Can Case 228086 be retrieved?
  3) Optionally, what fields exist on the Case object?

Production architecture should NOT use personal username/password/security-token.
Use a dedicated integration user + External Client App + OAuth client credentials.

Usage:
  1. Reset/generate a Salesforce security token in the UI.
  2. Copy .env.example values into .env (never commit real secrets).
  3. Set:
       SALESFORCE_USERNAME
       SALESFORCE_PASSWORD
       SALESFORCE_SECURITY_TOKEN
       SALESFORCE_LOGIN_URL   # optional; defaults to production login
  4. Run:
       python scripts/test_salesforce_connection.py --case-number 00233681
       python scripts/test_salesforce_connection.py --case-number 00233681 --pull-feed
       python scripts/test_salesforce_connection.py --describe-case

Sandbox login URL example:
  https://test.salesforce.com/services/Soap/u/59.0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from connectors.salesforce.auth import load_credentials, soap_login
from connectors.salesforce.case_feed import pull_case_feed_and_images
from connectors.salesforce.case_repository import query_case_by_number
from connectors.salesforce.client import SalesforceClient
from connectors.salesforce.errors import SalesforceProbeError
from connectors.salesforce.schema_discovery import (
    describe_case_object,
    filter_fields,
    format_field_line,
)

DEFAULT_OUT_ROOT = REPO_ROOT / "data" / "output" / "salesforce_probe"


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Development-only Salesforce SOAP login + Case query probe.",
    )
    parser.add_argument(
        "--case-number",
        default="228086",
        help="Salesforce CaseNumber to query (default: 228086).",
    )
    parser.add_argument(
        "--describe-case",
        action="store_true",
        help="After a successful query, inspect Case field metadata.",
    )
    parser.add_argument(
        "--describe-all-fields",
        action="store_true",
        help="With --describe-case, print every field (can be hundreds).",
    )
    parser.add_argument(
        "--describe-filter",
        default="",
        help="With --describe-case, only print fields whose label or API name contains this text.",
    )
    parser.add_argument(
        "--pull-feed",
        action="store_true",
        help="Pull CaseFeed, emails, and download case images/files under data/output/salesforce_probe/.",
    )
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="With --pull-feed, download all ContentDocument files (not only images).",
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="Optional output directory for --pull-feed (default: data/output/salesforce_probe/case_<number>/).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        credentials = load_credentials()
        session = soap_login(credentials)
    except SalesforceProbeError as exc:
        print(f"Salesforce authentication failed: {exc}")
        return 1

    print("Salesforce authentication successful.")
    print(f"Instance/server: {session.instance_url}")
    print(f"Session established: {'yes' if session.session_established else 'no'}")

    client = SalesforceClient(session)
    try:
        case = query_case_by_number(client, args.case_number)
    except SalesforceProbeError as exc:
        print(f"Salesforce Case query failed: {exc}")
        return 2

    assert case is not None
    print()
    print("Salesforce API connection successful.")
    print()
    print("Case found:")
    print(f"Case Number: {case.case_number}")
    print(f"Subject: {case.subject}")
    print(f"Status: {case.status}")
    print(f"Salesforce ID: {case.id}")

    if args.pull_feed:
        out_dir = (
            Path(args.out_dir)
            if args.out_dir
            else DEFAULT_OUT_ROOT / f"case_{case.case_number}"
        )
        try:
            result = pull_case_feed_and_images(
                client,
                case,
                out_dir,
                images_only=not args.all_files,
            )
        except SalesforceProbeError as exc:
            print()
            print(f"Case feed pull failed: {exc}")
            return 4

        image_count = sum(1 for item in result.files if item.is_image)
        print()
        print("Case feed pull successful.")
        print(f"Feed entries: {len(result.feed)}")
        print(f"Emails: {len(result.emails)}")
        print(f"Files linked: {len(result.files)} ({image_count} images)")
        print(f"Downloaded: {len(result.downloaded_files)}")
        print(f"Output: {result.output_dir}")

    if args.describe_case:
        try:
            fields = describe_case_object(client)
        except SalesforceProbeError as exc:
            print()
            print(f"Case schema discovery failed: {exc}")
            return 3

        custom_count = sum(1 for field in fields if field.custom)
        standard_count = len(fields) - custom_count
        print()
        print(
            f"Case object schema: {len(fields)} fields "
            f"({custom_count} custom, {standard_count} standard)."
        )

        if args.describe_all_fields:
            selected = fields
            mode = "all fields"
        elif args.describe_filter:
            selected = filter_fields(fields, substring=args.describe_filter)
            mode = f"filter={args.describe_filter!r}"
        else:
            selected = filter_fields(fields, custom_only=True)
            mode = "custom fields only (use --describe-all-fields or --describe-filter for more)"

        print(f"Showing: {mode} ({len(selected)} field(s)).")
        for field in selected:
            print(format_field_line(field))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
