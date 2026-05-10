"""Overlay live Terraform / cluster values onto search-api ConfigMap.

Runs **before** ``deploy-api`` so new Pods read Vertex outputs and the in-cluster
Elasticsearch URL (defaults to cluster DNS when ``ELASTICSEARCH_URL`` is unset).

ConfigMap schema is defined only in ``scripts/lib/config.py`` (Phase 7 W2-5 drift fix).
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from scripts._common import env, gcs_bucket_name
from scripts.adapters.gcloud import gcloud_run
from scripts.adapters.kubectl import kubectl_run
from scripts.adapters.terraform import terraform_run
from scripts.lib.config import generate_configmap_data, render_configmap_yaml

INFRA = Path(__file__).resolve().parents[2] / "infra" / "terraform" / "environments" / "dev"


def _terraform_output_map() -> dict[str, str]:
    """Return `terraform output -json` as a flat name->string map."""
    proc = terraform_run(
        f"-chdir={INFRA}",
        "output",
        "-json",
        capture=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit("[error] terraform output -json failed for ConfigMap overlay")
    try:
        payload = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[error] terraform output JSON decode failed: {exc}") from exc
    resolved: dict[str, str] = {}
    for key, meta in payload.items():
        value = meta.get("value", "") if isinstance(meta, dict) else ""
        resolved[key] = str(value or "")
    return resolved


def _feature_online_store_public_domain_from_api(
    project_id: str, vertex_location: str, store_id: str
) -> str:
    """GET FeatureOnlineStore; return dedicatedServingEndpoint.publicEndpointDomainName."""
    proc = gcloud_run(
        "auth",
        "print-access-token",
        capture=True,
        check=False,
    )
    token = (proc.stdout or "").strip()
    if proc.returncode != 0 or not token:
        return ""
    url = (
        f"https://{vertex_location}-aiplatform.googleapis.com/v1beta1/"
        f"projects/{project_id}/locations/{vertex_location}/featureOnlineStores/{store_id}"
    )
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads((resp.read() or b"").decode() or "{}")
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, OSError):
        return ""
    dse = payload.get("dedicatedServingEndpoint") or {}
    return str(dse.get("publicEndpointDomainName") or "").strip()


def main() -> int:
    project_id = env("PROJECT_ID")
    if not project_id:
        raise SystemExit("[error] PROJECT_ID is empty")
    region = env("REGION", "asia-northeast1")
    models_bucket = env("MODELS_BUCKET", gcs_bucket_name("models"))
    tf_outputs = _terraform_output_map()
    print(f"[info] models_bucket={models_bucket}")

    vertex_location = env("VERTEX_LOCATION") or region
    fos_endpoint = (tf_outputs.get("vertex_feature_online_store_endpoint") or "").strip()
    fos_store_id = (tf_outputs.get("vertex_feature_online_store_id") or "").strip()
    if fos_store_id and not fos_endpoint:
        fos_endpoint = _feature_online_store_public_domain_from_api(
            project_id, vertex_location, fos_store_id
        )
        if fos_endpoint:
            print(
                "[info] vertex_feature_online_store_endpoint resolved via Vertex API "
                "(terraform output was empty; see vertex module lifecycle / async provisioning)"
            )
    if fos_store_id and not fos_endpoint:
        raise SystemExit(
            "[error] Feature Online Store serving endpoint is empty. "
            "Terraform output and live Vertex API both returned no "
            "dedicatedServingEndpoint.publicEndpointDomainName. "
            "Wait for Optimized store provisioning after apply, then re-run overlay-configmap."
        )

    es_url = env(
        "ELASTICSEARCH_URL",
        "http://elasticsearch.search.svc.cluster.local:9200",
    )
    es_index = env("ELASTICSEARCH_INDEX", "properties")
    print(f"[info] elasticsearch_url={es_url} index={es_index}")

    data = generate_configmap_data(
        project_id=project_id,
        models_bucket=models_bucket,
        elasticsearch_url=es_url,
        elasticsearch_index=es_index,
        vertex_vector_search_index_endpoint_id=tf_outputs.get(
            "vector_search_index_endpoint_id", ""
        ),
        vertex_vector_search_deployed_index_id=tf_outputs.get(
            "vector_search_deployed_index_id", ""
        ),
        vertex_feature_online_store_id=fos_store_id,
        vertex_feature_view_id=tf_outputs.get("vertex_feature_view_id", ""),
        vertex_feature_online_store_endpoint=fos_endpoint,
    )
    cm_yaml = render_configmap_yaml(data, with_header=False)

    print("==> kubectl apply -f - (search-api-config ConfigMap overlay)")
    proc = kubectl_run("apply", "-f", "-", input=cm_yaml, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"[error] kubectl apply ConfigMap failed rc={proc.returncode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
