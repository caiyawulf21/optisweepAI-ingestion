"""FastAPI app exposing the four appcode-facing Brain routes
(OPTISWEEP_APP_BRAIN_HTTP_BOUNDARY.md). Thin wiring only -- every handler
delegates immediately to http_server/routes.py, which has no FastAPI
import of its own and is unit-tested directly.

Run with:
    uvicorn http_server.app:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import threading

from fastapi import FastAPI, HTTPException

from http_server import routes
from http_server.models import (
    ContextResponse,
    ContextRetrieveRequest,
    FeedbackEvent,
    FeedbackResponse,
    ReviewListResponse,
    ReviewResolveRequest,
    ReviewResolveResponse,
    TroubleshootRequest,
)
from mcp_server.providers_config import get_embedding_provider, get_llm_provider, get_storage_provider
from http_server.routes import ReviewNotFoundError
from brain_service.audit_execution import NoWinnerRecordError, RetypeTargetError, UnresolvableRecordError
from providers.embeddings import EmbeddingProvider
from providers.llm import LLMProvider
from providers.storage import StorageProvider

app = FastAPI(
    title="OptiSweep Brain HTTP API",
    description=(
        "The four appcode-facing Brain routes: context/retrieve, context/troubleshoot, "
        "feedback, and reviews/{id}/resolve. Brain owns all brain_* container mutation; "
        "appcode is a client only, holding no Brain write credentials of its own."
    ),
    version="0.1.0",
)


# Process-lifetime provider singletons (2026-09-10). Previously every route
# called get_storage_provider()/get_embedding_provider() fresh per request,
# which meant AzureStorageProvider's own embeddings cache (already built,
# already tested) never actually warmed up -- every single call, not just
# the first, paid a full ~210-235s cross-partition Cosmos scan of the whole
# ~20K-vector embeddings container. This was the actual root cause of the
# cold-latency number appcode measured, found by reading the call sites
# directly rather than assuming a search-algorithm/ANN problem. Reusing one
# instance for the container's whole life lets that cache do its job: only
# the first request (or the first after a write invalidates it) pays the
# full scan; every request after that is an in-memory cosine loop over
# already-fetched vectors.
#
# uvicorn runs this app as a single process with no --workers flag (see
# Dockerfile), so one singleton per process is correct -- if this ever
# moves to multiple worker processes, each would need its own warm cache
# (a shared cache would need a different mechanism, e.g. a real vector
# store), but that is not today's deployment.
#
# FastAPI (via Starlette) runs sync def route handlers in a thread pool,
# so first-construction is guarded by a lock -- without it, two concurrent
# cold requests could each construct and discard a provider instead of
# safely sharing the one that wins.
_singleton_lock = threading.Lock()
_storage_singleton: StorageProvider | None = None
_embeddings_singleton: EmbeddingProvider | None = None
_llm_singleton: LLMProvider | None = None


def _get_storage() -> StorageProvider:
    global _storage_singleton
    if _storage_singleton is None:
        with _singleton_lock:
            if _storage_singleton is None:
                _storage_singleton = get_storage_provider()
    return _storage_singleton


def _get_embeddings() -> EmbeddingProvider:
    global _embeddings_singleton
    if _embeddings_singleton is None:
        with _singleton_lock:
            if _embeddings_singleton is None:
                _embeddings_singleton = get_embedding_provider()
    return _embeddings_singleton


def _get_llm() -> LLMProvider:
    global _llm_singleton
    if _llm_singleton is None:
        with _singleton_lock:
            if _llm_singleton is None:
                _llm_singleton = get_llm_provider()
    return _llm_singleton


@app.post("/brain/v1/context/retrieve", response_model=ContextResponse)
def context_retrieve(request: ContextRetrieveRequest) -> ContextResponse:
    return routes.handle_context_retrieve(request, storage=_get_storage(), embeddings=_get_embeddings())


@app.post("/brain/v1/context/troubleshoot", response_model=ContextResponse)
def context_troubleshoot(request: TroubleshootRequest) -> ContextResponse:
    return routes.handle_troubleshoot(request, storage=_get_storage(), embeddings=_get_embeddings())


@app.post("/brain/v1/feedback", response_model=FeedbackResponse)
def feedback(event: FeedbackEvent) -> FeedbackResponse:
    return routes.handle_feedback(event, llm=_get_llm(), storage=_get_storage())


@app.get("/brain/v1/reviews", response_model=ReviewListResponse)
def list_reviews(status: str | None = "open") -> ReviewListResponse:
    return routes.handle_list_reviews(storage=_get_storage(), status=status)


@app.post("/brain/v1/reviews/{review_id}/resolve", response_model=ReviewResolveResponse)
def resolve_review(review_id: str, request: ReviewResolveRequest) -> ReviewResolveResponse:
    try:
        return routes.handle_resolve_review(review_id, request, llm=_get_llm(), storage=_get_storage())
    except ReviewNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (NoWinnerRecordError, RetypeTargetError, UnresolvableRecordError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
