"""Salesforce connectivity helpers (development probe; not production ingest)."""

from connectors.salesforce.auth import SalesforceSession, load_credentials, soap_login
from connectors.salesforce.case_feed import pull_case_feed_and_images
from connectors.salesforce.case_repository import CaseSummary, query_case_by_number
from connectors.salesforce.client import SalesforceClient
from connectors.salesforce.errors import SalesforceProbeError
from connectors.salesforce.schema_discovery import CaseFieldMeta, describe_case_object

__all__ = [
    "CaseFieldMeta",
    "CaseSummary",
    "SalesforceClient",
    "SalesforceProbeError",
    "SalesforceSession",
    "describe_case_object",
    "load_credentials",
    "pull_case_feed_and_images",
    "query_case_by_number",
    "soap_login",
]
