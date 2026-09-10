# Brain HTTP API image. Build context is the REPO ROOT (not http_server/)
# -- brain/, brain_service/, providers/, mcp_server/providers_config.py,
# and the ~1.4MB of shared_pipeline_stages/*.py the embedding provider
# imports transitively all need to be on the image alongside http_server/
# itself, mirroring exactly how this app already runs locally (module
# execution from repo root, no per-package pip install). Build from repo
# root with:
#   az acr build --registry optisweepaiacr --image optisweep-brain-http:latest \
#       --file http_server/Dockerfile .

FROM python:3.11-slim

WORKDIR /app

# Only the packages http_server's own import chain actually reaches
# (confirmed by tracing real imports, not copying the whole repo) --
# .dockerignore already excludes every data/test/doc directory within
# these, so this is source code only.
COPY brain/ ./brain/
COPY brain_service/ ./brain_service/
COPY providers/ ./providers/
COPY mcp_server/ ./mcp_server/
COPY http_server/ ./http_server/
COPY shared_pipeline_stages/ ./shared_pipeline_stages/

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pydantic \
    python-dotenv

EXPOSE 8000

CMD ["uvicorn", "http_server.app:app", "--host", "0.0.0.0", "--port", "8000"]
