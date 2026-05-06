"""Start the local hybrid-search stack with one command.

What this does:

1. resolve non-secret config from ``env/config/setting.yaml``
2. resolve local secrets from ``env/secret/credential.yaml`` (fallback:
   env vars)
3. ensure a synthetic LightGBM model exists for the local reranker
4. boot:
   - local encoder server
   - local reranker server
   - local app server

This keeps the local startup path aligned with the production app contract:
the app still talks to KServe-like HTTP endpoints, but the endpoints are
provided by local dev servers instead of cluster-local Services.

Lexical lane uses **Elasticsearch** only. Point ``ELASTICSEARCH_URL`` at a local
or tunneled cluster ES instance; if none is reachable and no URL is set,
``ENABLE_SEARCH`` is forced off so the stack still boots (encoder + reranker
only).
"""

from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

from scripts._common import env, run, secret


def _log(msg: str) -> None:
    print(f"==> {msg}", flush=True)


def _http_available(url: str, *, timeout_sec: float = 1.5) -> bool:
    import urllib.error
    import urllib.request

    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=0.5) as resp:
                if 200 <= resp.status < 500:
                    return True
        except urllib.error.URLError:
            time.sleep(0.2)
    return False


def _resolve_elasticsearch_url() -> str:
    explicit = env("ELASTICSEARCH_URL")
    if explicit:
        return explicit.rstrip("/")
    local_url = env("LOCAL_ELASTICSEARCH_URL", "http://127.0.0.1:9200").rstrip("/")
    if _http_available(f"{local_url}/"):
        _log(f"use local Elasticsearch {local_url}")
        return local_url
    _log(
        "Elasticsearch not reachable; set ELASTICSEARCH_URL or run ES locally "
        "(ENABLE_SEARCH will be disabled for this session)."
    )
    return ""


def _resolve_elasticsearch_api_key(*, elasticsearch_url: str) -> str:
    if not elasticsearch_url:
        return ""
    preset = secret("ELASTICSEARCH_API_KEY")
    if preset:
        return preset
    return env("ELASTICSEARCH_API_KEY", "")


def _ensure_local_reranker_model(model_path: Path) -> None:
    if model_path.exists() and model_path.stat().st_size > 0:
        _log(f"reuse local reranker model {model_path}")
        return
    model_path.parent.mkdir(parents=True, exist_ok=True)
    _log(f"build synthetic reranker model {model_path}")
    run(
        ["uv", "run", "rank-train", "--dry-run", "--save-to", str(model_path)],
        check=True,
    )


def _wait_http(url: str, *, timeout_sec: float = 120.0) -> None:
    import urllib.error
    import urllib.request

    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                if 200 <= resp.status < 500:
                    return
        except urllib.error.URLError:
            time.sleep(0.5)
    raise SystemExit(f"[error] startup timeout waiting for {url}")


def _port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _spawn(cmd: list[str], *, child_env: dict[str, str]) -> subprocess.Popen[bytes]:
    return subprocess.Popen(cmd, env=child_env)


def main() -> int:
    encoder_port = env("LOCAL_ENCODER_PORT", "18081")
    reranker_port = env("LOCAL_RERANKER_PORT", "18082")
    app_port = env("LOCAL_API_PORT", "8000")
    es_url = _resolve_elasticsearch_url()
    es_api_key = _resolve_elasticsearch_api_key(elasticsearch_url=es_url)
    enable_search = "true" if es_url else "false"
    model_path = Path(
        env("LOCAL_RERANKER_MODEL_PATH", "/tmp/hybrid-search-cloud-smoke-model.txt")
    ).expanduser()

    for label, port_str in (
        ("encoder", encoder_port),
        ("reranker", reranker_port),
        ("app", app_port),
    ):
        port = int(port_str)
        if _port_in_use(port):
            raise SystemExit(
                f"[error] local {label} port {port} is already in use. "
                "Stop the existing process or override LOCAL_*_PORT."
            )

    _ensure_local_reranker_model(model_path)

    base_env = os.environ.copy()
    base_env.setdefault("UV_CACHE_DIR", "/tmp/uv-cache")

    encoder_env = base_env | {
        "HOST": "127.0.0.1",
        "AIP_HTTP_PORT": encoder_port,
    }
    reranker_env = base_env | {
        "HOST": "127.0.0.1",
        "AIP_HTTP_PORT": reranker_port,
        "LOCAL_RERANKER_MODEL_PATH": str(model_path),
    }
    app_env = base_env | {
        "ENABLE_SEARCH": enable_search,
        "ENABLE_RERANK": "true",
        "KSERVE_ENCODER_URL": f"http://127.0.0.1:{encoder_port}/predict",
        "KSERVE_RERANKER_URL": f"http://127.0.0.1:{reranker_port}/predict",
        "KSERVE_RERANKER_EXPLAIN_URL": f"http://127.0.0.1:{reranker_port}/explain",
        "ELASTICSEARCH_URL": es_url,
        "ELASTICSEARCH_API_KEY": es_api_key,
    }

    processes: list[subprocess.Popen[bytes]] = []
    try:
        _log("start local encoder")
        processes.append(
            _spawn(["uv", "run", "python", "-m", "ml.serving.encoder"], child_env=encoder_env)
        )
        _wait_http(f"http://127.0.0.1:{encoder_port}/health")

        _log("start local reranker")
        processes.append(
            _spawn(["uv", "run", "python", "-m", "ml.serving.reranker"], child_env=reranker_env)
        )
        _wait_http(f"http://127.0.0.1:{reranker_port}/health")

        _log("start local app")
        processes.append(
            _spawn(
                [
                    "uv",
                    "run",
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    app_port,
                ],
                child_env=app_env,
            )
        )
        _wait_http(f"http://127.0.0.1:{app_port}/healthz")
        _log(
            f"local hybrid stack READY app=http://127.0.0.1:{app_port} "
            f"encoder=http://127.0.0.1:{encoder_port} reranker=http://127.0.0.1:{reranker_port}"
        )

        app_proc = processes[-1]
        while True:
            rc = app_proc.poll()
            if rc is not None:
                return rc
            time.sleep(1.0)
    except KeyboardInterrupt:
        return 130
    finally:
        for proc in reversed(processes):
            if proc.poll() is not None:
                continue
            proc.send_signal(signal.SIGINT)
        for proc in reversed(processes):
            if proc.poll() is not None:
                continue
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)


if __name__ == "__main__":
    sys.exit(main())
