"""Local-build alternative to scripts.deploy.build_kserve_images.

Builds the Phase 7 encoder / reranker images with local ``docker buildx`` and
pushes them to Artifact Registry, then patches the cluster like the Cloud Build
path does. This keeps iterative image work local-first so BuildKit cache mounts
inside the Dockerfiles actually pay off across runs.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import time

from scripts._common import env, resolve_git_sha
from scripts.adapters.gcloud import gcloud_run
from scripts.adapters.kubectl import kubectl_run

NAMESPACE = "kserve-inference"
ML_BASE_IMAGE = "phase7-ml-base:local"


def _step(msg: str) -> None:
    print(f"==> {msg}", flush=True)


def _info(msg: str) -> None:
    print(f"[info] {msg}", flush=True)


def _error(msg: str) -> None:
    print(f"[error] {msg}", file=sys.stderr, flush=True)


def _require(name: str) -> str:
    value = env(name)
    if not value:
        raise SystemExit(f"[error] required env var {name} is empty")
    return value


def _diag(label: str, proc: subprocess.CompletedProcess[str]) -> None:
    _error(f"---- diag {label} exit={proc.returncode} ----")
    if proc.stdout:
        sys.stderr.write(proc.stdout)
        if not proc.stdout.endswith("\n"):
            sys.stderr.write("\n")
    if proc.stderr:
        sys.stderr.write(proc.stderr)
        if not proc.stderr.endswith("\n"):
            sys.stderr.write("\n")
    sys.stderr.flush()


def _ensure_docker_buildx() -> None:
    if shutil.which("docker") is None:
        raise SystemExit("[error] docker CLI not found — install Docker first")
    proc = subprocess.run(
        ["docker", "buildx", "version"], capture=True, check=False
    )
    if proc.returncode != 0:
        raise SystemExit("[error] `docker buildx` not available.")


def _ensure_ar_auth(region: str) -> None:
    registry = f"{region}-docker.pkg.dev"
    proc = gcloud_run("auth", "configure-docker", registry, "--quiet",
        capture=True,
        check=False,
    )
    if proc.returncode != 0:
        _diag("gcloud auth configure-docker", proc)
        raise SystemExit(
            f"[error] `gcloud auth configure-docker {registry}` failed — run `gcloud auth login` first."
        )


def _ensure_kubectl_context(cluster_name: str, region: str, project_id: str) -> None:
    gcloud_run("container",
            "clusters",
            "get-credentials",
            cluster_name,
            f"--region={region}",
            f"--project={project_id}",
    )


def _build_local_image(*, dockerfile: str, image_uri: str) -> None:
    _step(f"docker buildx build --push image={image_uri}")
    started = time.monotonic()
    proc = subprocess.run(
        [
            "docker",
            "buildx",
            "build",
            "--file",
            dockerfile,
            "--build-arg",
            f"ML_BUILDER_IMAGE={ML_BASE_IMAGE}",
            "--tag",
            image_uri,
            "--push",
            ".",
        ],
        check=False,
    )
    if proc.returncode != 0:
        _error(
            f"docker buildx build FAILED image={image_uri} elapsed={(time.monotonic() - started):.0f}s"
        )
        raise SystemExit(proc.returncode)
    _info(
        f"docker buildx build SUCCESS image={image_uri} elapsed={(time.monotonic() - started):.0f}s"
    )


def _patch_inference_service_image(isvc_name: str, image_uri: str) -> None:
    patch = (
        '{"spec":{"predictor":{"containers":[{'
        '"name":"kserve-container",'
        f'"image":"{image_uri}"'
        "}]}}}"
    )
    kubectl_run("patch",
            "inferenceservice",
            isvc_name,
            f"--namespace={NAMESPACE}",
            "--type=merge",
            f"--patch={patch}",
    )


def _set_deployment_image(deployment: str, container: str, image_uri: str) -> None:
    kubectl_run("set",
            "image",
            f"deployment/{deployment}",
            f"{container}={image_uri}",
            f"--namespace={NAMESPACE}",
    )


def main() -> int:
    project_id = _require("PROJECT_ID")
    region = env("REGION", "asia-northeast1")
    cluster_name = env("GKE_CLUSTER_NAME", "hybrid-search")
    artifact_repo = env("ARTIFACT_REPO_ID", "mlops")
    sha = resolve_git_sha()
    ts = int(time.time())

    encoder_image = (
        f"{region}-docker.pkg.dev/{project_id}/{artifact_repo}/property-encoder:{sha}-{ts}"
    )
    reranker_image = (
        f"{region}-docker.pkg.dev/{project_id}/{artifact_repo}/property-reranker:{sha}-{ts}"
    )

    _step(
        f"deploy-kserve-images-local start project={project_id} region={region} "
        f"cluster={cluster_name} repo={artifact_repo}"
    )
    _ensure_docker_buildx()
    _ensure_ar_auth(region)
    _ensure_kubectl_context(cluster_name, region, project_id)

    _step(f"build shared ml base image={ML_BASE_IMAGE}")
    base_proc = subprocess.run(
        [
            "docker",
            "buildx",
            "build",
            "--file",
            "infra/run/services/ml_base/Dockerfile",
            "--tag",
            ML_BASE_IMAGE,
            "--load",
            ".",
        ],
        check=False,
    )
    if base_proc.returncode != 0:
        _error("docker buildx build FAILED for shared ml base image")
        raise SystemExit(base_proc.returncode)

    _build_local_image(
        dockerfile="infra/run/services/encoder/Dockerfile",
        image_uri=encoder_image,
    )
    _build_local_image(
        dockerfile="infra/run/services/reranker/Dockerfile",
        image_uri=reranker_image,
    )

    _step(f"patch encoder image={encoder_image}")
    _patch_inference_service_image("property-encoder", encoder_image)

    _step(f"patch reranker-explain image={reranker_image}")
    _set_deployment_image("property-reranker-explain", "reranker", reranker_image)

    _step(
        f"deploy-kserve-images-local DONE encoder={encoder_image} reranker_explain={reranker_image}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
