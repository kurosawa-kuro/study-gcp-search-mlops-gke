"""Step 6 of deploy-all: terraform apply staged (core → kube-ready wait → full).

deploy_all.py の orchestration 設計方針 (各 step の business logic は sibling
module に置く / `_run_*` は thin wrapper) に従い、step 6 の terraform apply
ロジックを本 module に分離している。

含む処理:
- recover_wif (PDCA loop safety、2026-05-09 incident: `--from-step tf-apply`
  単独実行で step 3 を skip すると WIF 409 で 30+ 分の出戻りが発生する)
- VVS Index/Endpoint state import (`docs/tasks/TASKS_ROADMAP.md §4.9`)
- orphan GCP resource state recovery (`docs/tasks/TASKS_ROADMAP.md §4.10`)
- VVS deployed_index 残置の解放待ち
- Vertex Feature Store / Feature Online Store 名前解放待ち (HTTP 409 回避)
- terraform apply stage1 (core infra: iam / data / vector_search / vertex /
  gke / messaging / monitoring / slo / composer)
- kubeconfig refresh + cluster API ready 待ち
- terraform apply stage2 (full graph including module.kserve)
"""

from __future__ import annotations

from pathlib import Path

from scripts._common import env, terraform_var_args
from scripts.infra.kubectl_context import ensure as ensure_kubectl_context
from scripts.infra.kubectl_context import wait_until_api_ready
from scripts.infra.state_recovery import recover_orphan_gcp_resources
from scripts.infra.terraform_lock import run_terraform_streaming_with_lock_retry
from scripts.infra.terraform_stage_apply import (
    TF_APPLY_STAGE1_TARGETS,
    terraform_apply_stage1_with_retries,
)
from scripts.infra.vertex_cleanup import wait_for_deployed_index_absent
from scripts.infra.vertex_feature_store_wait import wait_until_feature_store_names_released
from scripts.infra.vertex_import import import_persistent_vvs_resources
from scripts.lib.gcp_resources import GKE_CLUSTER_NAME_DEFAULT
from scripts.setup.recover_wif import main as recover_wif_main

INFRA = Path(__file__).resolve().parents[2] / "infra" / "terraform" / "environments" / "dev"


def main() -> int:
    project_id = env("PROJECT_ID")
    region = env("REGION", "asia-northeast1")
    cluster_name = env("GKE_CLUSTER_NAME", GKE_CLUSTER_NAME_DEFAULT)
    deployed_index_id = env("VERTEX_VECTOR_SEARCH_DEPLOYED_INDEX_ID", "property_embeddings_v3")

    # 2026-05-09 incident: `--from-step tf-apply` 単独実行で step 3 (recover-wif)
    # を skip すると、WIF pool / provider が soft-delete + tfstate 不一致で残存し、
    # tf-apply stage1 が `Error 409: Requested entity already exists` で fail する。
    # 30+ 分の出戻りを生むため、tf-apply の冒頭で recover_wif を idempotent に呼ぶ。
    # 通常の `make deploy-all` 経路では step 3 と本 hook で 2 回実行されるが、
    # recover_wif_main() は冪等なので副作用なし。
    print("==> tf-apply pre-step: recover_wif (PDCA loop safety, 2026-05-09 incident)")
    recover_wif_main()

    # 永続化アーキテクチャ (`docs/tasks/TASKS_ROADMAP.md §4.9`、2026-05-03):
    # 前回 destroy-all で `module.vector_search` の Index / Endpoint を **state rm
    # + GCP 残置** している場合がある。tf-apply 前に既存 GCP resource を state へ
    # import することで、terraform plan は「Index/Endpoint = no-op、deployed_index
    # のみ create」となり、Index build 5-15 min + Endpoint create + DNS propagation
    # を省略して deploy-all 27 min → 10-15 min に短縮できる。
    print(f"==> tf-apply pre-step: VVS Index/Endpoint state import check (region={region})")
    imported = import_persistent_vvs_resources(
        INFRA,
        project_id,
        region,
        terraform_var_args=list(terraform_var_args("GITHUB_REPO", "ONCALL_EMAIL")),
    )
    if imported:
        print(f"==> {imported} addr imported into state — terraform plan で no-op 扱いになる")

    # 2026-05-03 incident postmortem (`docs/tasks/TASKS_ROADMAP.md §4.10`):
    # 緊急 cleanup で `gcloud delete --async` で Composer/GKE/Cloud Run しか消さなかった
    # 後に runbook §1.4-emergency の `state rm` で全 state を消すと、IAM SA / BQ /
    # Pub/Sub / Cloud Function / Eventarc などが GCP 残置
    # かつ state 不在で、tf-apply stage1 が `Error: alreadyExists` で fail する。
    # IAM SA は soft-delete 30 日 window があるため gcloud delete → 即 terraform create
    # も fail する罠あり。本 helper は existing GCP resources を type ごとに list して
    # state へ import で吸収 (idempotent、何度叩いてもそれ以上 import しない)。
    print(f"==> tf-apply pre-step: orphan GCP resource state recovery (region={region})")
    recovered = recover_orphan_gcp_resources(
        INFRA,
        project_id,
        region,
        terraform_var_args=list(terraform_var_args("GITHUB_REPO", "ONCALL_EMAIL")),
    )
    if recovered:
        print(f"==> {recovered} orphan resource(s) imported — tf-apply 'alreadyExists' fail 回避")

    wait_for_deployed_index_absent(project_id, region, deployed_index_id)

    # destroy-all → deploy-all の短間隔では Vertex Feature Group / Feature Online Store が
    # GCP 側で非同期削除中のまま同名 create が走り HTTP 409 になる。list API で名前解放を待つ。
    vertex_region = env("VERTEX_LOCATION") or region
    wait_until_feature_store_names_released(project_id, vertex_region)

    stage1_args = [
        "terraform",
        f"-chdir={INFRA}",
        "apply",
        "-auto-approve",
        *terraform_var_args("GITHUB_REPO", "ONCALL_EMAIL"),
        *[f"-target={target}" for target in TF_APPLY_STAGE1_TARGETS],
    ]
    print(
        "==> terraform apply stage1 (core infra before kube provider resources): "
        + ", ".join(TF_APPLY_STAGE1_TARGETS)
    )
    terraform_apply_stage1_with_retries(stage1_args, chdir_infra=INFRA)

    print(f"==> refresh kubeconfig + wait for cluster API: cluster={cluster_name} region={region}")
    ensure_kubectl_context()
    wait_until_api_ready()

    print("==> terraform apply stage2 (full graph including module.kserve)")
    run_terraform_streaming_with_lock_retry(
        [
            "terraform",
            f"-chdir={INFRA}",
            "apply",
            "-auto-approve",
            *terraform_var_args("GITHUB_REPO", "ONCALL_EMAIL"),
        ],
        chdir_infra=INFRA,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
