"""Build all 5 local Docker images (no push) — the canonical "ローカルビルド".

「ローカルビルド」「ビルドして」= **この 5 image 全部**。search-api 単体では不足。
`infra/run/services/` に Dockerfile が 5 個あり、`ml_base` は `encoder` / `reranker`
の builder ベースなので必ず先に build する。GCP deploy 前にこれを通さないと、
この規模のコードベースでは deploy がほぼ確実に失敗する (= 前提条件)。

Makefile からは `make build-all-local` で 1 行呼び出し (Makefile 破綻防止仕様:
複数行アクションは script に切り出して呼ぶだけ — M-Wave0 止血)。

各 image:
  1. ml-base        → mlops-ml-base:local              (base deps、encoder/reranker の builder)
  2. search-api     → local-test/search-api:dev        (~700MB; 3GB 超なら [ml] extra 混入)
  3. encoder        → local-test/property-encoder:dev  (--build-arg ML_BUILDER_IMAGE=mlops-ml-base:local、ME5 weights で最重)
  4. reranker       → local-test/property-reranker:dev (--build-arg ML_BUILDER_IMAGE=mlops-ml-base:local)
  5. composer-runner→ local-test/composer-runner:dev   (ml/ scripts/ pipeline/ を bundle)
"""

from __future__ import annotations

import subprocess
import sys
import time

# (name, dockerfile, image_tag, extra_build_args)
_IMAGES: list[tuple[str, str, str, list[str]]] = [
    ("ml-base", "infra/run/services/ml_base/Dockerfile", "mlops-ml-base:local", []),
    ("search-api", "infra/run/services/search_api/Dockerfile", "local-test/search-api:dev", []),
    (
        "encoder",
        "infra/run/services/encoder/Dockerfile",
        "local-test/property-encoder:dev",
        ["--build-arg", "ML_BUILDER_IMAGE=mlops-ml-base:local"],
    ),
    (
        "reranker",
        "infra/run/services/reranker/Dockerfile",
        "local-test/property-reranker:dev",
        ["--build-arg", "ML_BUILDER_IMAGE=mlops-ml-base:local"],
    ),
    (
        "composer-runner",
        "infra/run/services/composer_runner/Dockerfile",
        "local-test/composer-runner:dev",
        [],
    ),
]


def _step(msg: str) -> None:
    print(f"==> {msg}", flush=True)


def _build(name: str, dockerfile: str, image_tag: str, extra_args: list[str]) -> bool:
    _step(f"[{name}] docker buildx build -f {dockerfile} -t {image_tag}")
    started = time.monotonic()
    cmd = ["docker", "buildx", "build", "--file", dockerfile, *extra_args, "--load", "-t", image_tag, "."]
    proc = subprocess.run(cmd, check=False)
    elapsed = time.monotonic() - started
    if proc.returncode != 0:
        print(f"[error] [{name}] build FAILED rc={proc.returncode} elapsed={elapsed:.0f}s", file=sys.stderr)
        return False
    _step(f"[{name}] DONE {image_tag} elapsed={elapsed:.0f}s")
    return True


def main() -> int:
    _step(f"build-all-local start ({len(_IMAGES)} image): " + " / ".join(t for _, _, t, _ in _IMAGES))
    for name, dockerfile, image_tag, extra_args in _IMAGES:
        if not _build(name, dockerfile, image_tag, extra_args):
            # ml-base failure → encoder/reranker can't layer on it; abort the rest.
            print(f"[error] aborting build-all-local after {name} failure", file=sys.stderr)
            return 1
    _step("build-all-local DONE: " + " / ".join(t for _, _, t, _ in _IMAGES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
