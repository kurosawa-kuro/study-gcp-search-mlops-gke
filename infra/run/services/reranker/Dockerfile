# syntax=docker/dockerfile:1.7
# KServe-side LightGBM reranker explain server。
# Local build では ML_BUILDER_IMAGE=phase7-ml-base:local を渡し、
# base deps 解決済み builder から LightGBM 分だけ差分 install する。

ARG ML_BUILDER_IMAGE=ghcr.io/astral-sh/uv:0.5.4-python3.12-bookworm-slim
FROM ${ML_BUILDER_IMAGE} AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /src

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --extra ml-reranker --no-install-project


FROM python:3.12-slim-bookworm AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 1001 --home-dir /home/app app \
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
CMD ["python", "-m", "ml.serving.reranker"]
