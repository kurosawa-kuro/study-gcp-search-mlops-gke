# syntax=docker/dockerfile:1.7
# Local buildx fast path for ML images.
# Installs only the project base dependencies into /opt/venv so encoder/reranker
# can layer their own extras on top without re-solving the whole workspace.

FROM ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /src

COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project
