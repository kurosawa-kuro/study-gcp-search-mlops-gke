# syntax=docker/dockerfile:1.7
# KServe InferenceService: multilingual-e5-base encoder。
# Local build を高速化するため、search-api と同じく uv multi-stage +
# BuildKit cache mount で third-party venv を先に固める。

FROM ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /src

COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --extra ml --no-install-project


FROM python:3.12-slim-bookworm AS runtime

RUN useradd --system --uid 1001 --home-dir /home/app app \
    && mkdir -p /home/app

COPY --from=builder --chown=app:app /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONPATH="/home/app" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    AIP_HTTP_PORT=8080

COPY --chown=app:app ml /home/app/ml

USER app
WORKDIR /home/app

EXPOSE 8080
CMD ["python", "-m", "ml.serving.encoder"]
