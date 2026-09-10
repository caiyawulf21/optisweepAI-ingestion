"""Error categories for the Salesforce connectivity probe."""

from __future__ import annotations


class SalesforceProbeError(Exception):
    """Raised when a Salesforce probe step fails without exposing secrets."""

    def __init__(self, category: str, message: str) -> None:
        self.category = category
        super().__init__(message)

    def __str__(self) -> str:
        return f"[{self.category}] {self.args[0]}"


CATEGORY_MISSING_ENV = "missing_environment"
CATEGORY_INVALID_CREDENTIALS = "invalid_credentials"
CATEGORY_API_ACCESS = "api_access_denied"
CATEGORY_NETWORK = "network_or_dns"
CATEGORY_ENDPOINT = "salesforce_endpoint"
CATEGORY_MALFORMED = "malformed_response"
CATEGORY_QUERY_EMPTY = "query_no_match"
CATEGORY_AUTHORIZATION = "authorization"
CATEGORY_QUERY_FAILED = "query_failed"
CATEGORY_UNEXPECTED = "unexpected_authentication_error"
