"""Error categories for Microsoft Graph / Teams probes."""

from __future__ import annotations


class GraphProbeError(Exception):
    def __init__(self, category: str, message: str) -> None:
        self.category = category
        super().__init__(message)

    def __str__(self) -> str:
        return f"[{self.category}] {self.args[0]}"


CATEGORY_MISSING_ENV = "missing_environment"
CATEGORY_AUTH = "authentication"
CATEGORY_AUTHORIZATION = "authorization"
CATEGORY_NETWORK = "network_or_dns"
CATEGORY_ENDPOINT = "graph_endpoint"
CATEGORY_MALFORMED = "malformed_response"
CATEGORY_NOT_FOUND = "not_found"
CATEGORY_QUERY_FAILED = "query_failed"
