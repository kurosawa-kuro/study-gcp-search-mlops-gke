# syntax=docker/dockerfile:1.7

FROM python:3.12-slim

WORKDIR /app

# libgomp1 = LightGBM。
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    pip install uv

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --no-dev --no-install-project --frozen

# multilingual-e5 model は **image に焼き込まない**。
# 初回 docker compose run 時に download → `hf_cache` volume で永続化、2 回目以降高速。
ARG E5_MODEL_NAME=intfloat/multilingual-e5-small
ENV E5_MODEL_NAME=${E5_MODEL_NAME}

COPY app/ app/
COPY ml/ ml/
COPY pipeline/ pipeline/
COPY env/config/ env/config/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
# uv が作る .venv を default Python に。docker-compose.yml の `command: ["python", ...]` から
# 直接 venv の Python が呼ばれる (uv run を経由しなくて済む)。
ENV PATH="/app/.venv/bin:${PATH}"

# entrypoint は docker-compose.yml の `command:` で seed / trainer / evaluator を切り替える。
CMD ["python", "-m", "pipeline.data_job.main"]
