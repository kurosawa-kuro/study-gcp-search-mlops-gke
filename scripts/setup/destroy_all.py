"""End-to-end teardown of every Terraform-managed resource. **No interactive
prompt** — this is a learning / PDCA dev project (`mlops-dev-a`) where fast
iteration matters. Pair with `deploy-all` for a build-test-destroy loop.

Steps (use `--from-step` / `--to-step` to slice — symmetrical with deploy-all):

1. `seed-clean` — drop the out-of-Terraform-state table that
   `make seed-test` (`scripts/setup/seed_minimal.py`) creates. It blocks
   `feature_mart` dataset destroy with `resourceInUse` otherwise.
2. `undeploy-vertex-endpoints` — undeploy every `deployedModel` from the
   Terraform-managed Vertex Endpoint shells (server-side mutations not visible
   to Terraform). Any remaining DeployedModel blocks `terraform destroy` with
   HTTP 400.
3. `undeploy-vvs-deployed-indexes` — undeploy every Vector Search deployed
   index. PDCA reproducibility guard: 前 cycle で deployed index が残ると次の
   `deploy-all` が step 6 stage1 apply で 15 min wait timeout になる事故を防ぐ。
4. `state-rm-persistent-vvs` — `module.vector_search` の Index / Endpoint を
   **state rm + GCP 残置** に切り替える (`docs/tasks/TASKS_ROADMAP.md §4.9`)。
   Terraform 側の `lifecycle.prevent_destroy` だけだと依存閉包で touch されて
   `Instance cannot be destroyed` で全 destroy が止まる事故を 2026-05-03 に観測。
5. `wipe-gcs-buckets` — `gcs_cleanup.wipe_all_terraform_managed_buckets` で
   force_destroy=false の 4 buckets を空にする (object 残存だと bucket destroy
   が失敗)。
6. `flip-deletion-protection` — `terraform apply -auto-approve
   -var=enable_deletion_protection=false -target=<each>` で server-side
   protected resource (10 BQ tables + 1 GKE cluster + online serving view 1) の
   `deletion_protection` を flip。`filter_targets_in_state` で state にある
   ものだけに絞ること — そうしないと `-target` が依存閉包を pull して recreate
   に走る (Phase 7 Run 4 fix)。
7. `destroy-kserve` — `kube_cleanup.delete_orphan_workloads` + `terraform
   destroy -target=module.kserve`。K8s/Helm リソースを GKE cluster より先に
   destroy (provider が cluster endpoint に依存)。state に残った場合は
   `terraform_state.state_rm` で fallback。
8. `destroy-main` — `terraform destroy -auto-approve` (永続化 VVS resource は
   `-target` で除外、`prevent_destroy = true` と二重防御)。

What this does NOT touch (preserved for the next `make deploy-all`):
- The tfstate bucket (`<PROJECT_ID>-tfstate`).
- API enablements (cost nothing when no resource exists).
- Local artifacts (`infra/tfplan`, `pipeline/data_job/dataform/workflow_settings.yaml`).

Remote state **lock** (``default.tflock``): another ``terraform apply`` / interrupted
session may hold the lock. Terraform commands use ``scripts/infra/terraform_lock.py``
— on lock, print the ``force-unlock`` hint; optional auto-unlock when
``TERRAFORM_STATE_FORCE_UNLOCK=1`` (aliases: ``DESTROY_ALL_FORCE_UNLOCK``,
``DEPLOY_ALL_FORCE_UNLOCK``). **Only** if no other Terraform is running.

設計方針 (Phase 7 W3 リファクタ + 2026-05-09 step 分離):
- 本ファイルは **orchestrator のみ**。state query / Vertex Endpoint cleanup /
  K8s finalizer cleanup / GCS bucket wipe は `scripts/infra/*` に委譲し、
  ここは **step 定義 + 順序 + vars 引き渡し + slicing** だけを担う。
- `_run_*` は対応 module の関数を呼ぶ thin wrapper (drift 源にならないように)。
- `--from-step` / `--to-step` で step 単位リカバリー可能 (deploy-all と対称)。
"""

from __future__ import annotations

import argparse
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from scripts._common import env, terraform_var_args
from scripts.infra import gcs_cleanup, kube_cleanup, vertex_cleanup
from scripts.infra.terraform_lock import run_terraform_streaming_with_lock_retry
from scripts.infra.terraform_state import (
    addresses_starting_with,
    filter_targets_in_state,
    state_list,
    state_rm,
    state_size,
)
from scripts.setup.seed_minimal_clean import main as seed_clean_main

INFRA = Path(__file__).resolve().parents[2] / "infra" / "terraform" / "environments" / "dev"

# Resource addresses that carry **server-side `deletion_protection`** —
# Terraform refuses to destroy these while the attribute is `true`. Step
# `flip-deletion-protection` runs `terraform apply -var=enable_deletion_protection=false
# -target=<each>` to flip the attribute server-side **before** the body
# destroy. Kept in sync with the corresponding Terraform module sources;
# if a new resource that has its own `deletion_protection` is added,
# append it here.
#
# 履歴:
# - Phase 6 Run 2 で BQ table `ranking_log_hourly_ctr` (T2) を追加 → 9
# - Phase 7 Run 4 で **GKE cluster** を追加 (10)
# - Phase 7 Wave 2 で online serving view `property_features_online_latest`
#   を追加 → 11
PROTECTED_TARGETS = [
    "module.data.google_bigquery_table.training_runs",
    "module.data.google_bigquery_table.search_logs",
    "module.data.google_bigquery_table.ranking_log",
    "module.data.google_bigquery_table.feedback_events",
    "module.data.google_bigquery_table.search_events",
    "module.data.google_bigquery_table.search_impressions",
    "module.data.google_bigquery_table.user_actions",
    "module.data.google_bigquery_table.ranking_labels",
    "module.data.google_bigquery_table.evaluation_metrics",
    "module.data.google_bigquery_table.validation_results",
    "module.data.google_bigquery_table.property_features_daily",
    "module.data.google_bigquery_table.property_features_online_latest",
    "module.data.google_bigquery_table.property_embeddings",
    "module.data.google_bigquery_table.model_monitoring_alerts",
    "module.data.google_bigquery_table.ranking_log_hourly_ctr",
    "module.gke.google_container_cluster.hybrid_search",
]

# `module.kserve` 配下の K8s / Helm リソースを `terraform destroy` 本体より
# **先に** 個別 destroy するための target。`infra/terraform/environments/dev/provider.tf`
# の `kubernetes` / `helm` provider は `data.google_container_cluster.hybrid_search`
# (GKE cluster の endpoint / token) に依存しており、cluster が destroy 過程で
# 先に消えると provider が `localhost:80` に fallback して fail する。
# `module.kserve` を **module 単位で指定** することで、新規に
# `helm_release.<name>` / `kubernetes_*` を追加した時の取りこぼしを防ぐ。
KSERVE_MODULE_TARGET = "module.kserve"

# 永続化対象 (`docs/tasks/TASKS_ROADMAP.md §4.9` 採用、2026-05-03)。
#
# Vertex Vector Search の課金構造は非対称: **Index 自体 / 空の Index Endpoint
# は無料**、deployed_index (replica 起動状態) のみ課金。Index build には
# 5-15 min、Endpoint 作成には別途数分 + DNS propagation がかかるため、
# PDCA 1 cycle ごとに作り直すと deploy-all 全体が 10-15 min 短縮できない。
#
# 本契約: `destroy-all` は `module.vector_search` 内の Index / Endpoint を
# **state にも GCP にも残し**、deployed_index と FOS / GKE / Composer 等の
# 課金 resource のみを destroy する。Terraform 側にも `lifecycle.prevent_destroy
# = true` を入れて多重防御 (`infra/terraform/modules/vector_search/main.tf`)。
PERSISTENT_VVS_RESOURCES = (
    "module.vector_search.google_vertex_ai_index.property_embeddings",
    "module.vector_search.google_vertex_ai_index_endpoint.property_embeddings",
)


@dataclass(frozen=True)
class DestroyStep:
    number: int
    name: str
    label: str
    run: Callable[[], int]


# ---- step framework ----------------------------------------------------------

_DESTROY_ALL_STARTED_AT: float | None = None
_STEP_STARTED_AT: float | None = None


def _step(n: int, total: int, label: str) -> None:
    global _DESTROY_ALL_STARTED_AT, _STEP_STARTED_AT
    now = time.monotonic()
    if _DESTROY_ALL_STARTED_AT is None:
        _DESTROY_ALL_STARTED_AT = now
    prev_elapsed = now - _STEP_STARTED_AT if _STEP_STARTED_AT is not None else 0.0
    total_elapsed = now - _DESTROY_ALL_STARTED_AT
    _STEP_STARTED_AT = now
    print()
    print("================================================================")
    print(f" destroy-all  step {n}/{total}: {label}")
    if n > 1:
        print(f" (prev_step_elapsed={prev_elapsed:.0f}s total_elapsed={total_elapsed:.0f}s)")
    print("================================================================")


def _step_done() -> None:
    """Emit a `step-done` line with elapsed seconds for the step just finished."""
    if _STEP_STARTED_AT is None:
        return
    elapsed = time.monotonic() - _STEP_STARTED_AT
    print(f" destroy-all  step-done elapsed={elapsed:.0f}s")


# ---- common vars (terraform 引数共通化、散防止) -----------------------------

def _common_vars() -> list[str]:
    return [
        "-var=enable_deletion_protection=false",
        *terraform_var_args("GITHUB_REPO", "ONCALL_EMAIL"),
    ]


# ---- _run_* thin wrappers (実装は scripts/infra/* に委譲) -------------------

def _run_seed_clean() -> int:
    return seed_clean_main()


def _run_undeploy_vertex_endpoints() -> int:
    project_id = env("PROJECT_ID")
    region = env("VERTEX_LOCATION") or env("REGION")
    print(f"==> undeploy Vertex endpoint deployed_models (region={region})")
    vertex_cleanup.undeploy_all_endpoint_shells(project_id, region)
    return 0


def _run_undeploy_vvs_deployed_indexes() -> int:
    project_id = env("PROJECT_ID")
    region = env("VERTEX_LOCATION") or env("REGION")
    # PDCA reproducibility guard: 前 cycle で deployed index が残ると次の
    # deploy-all が step 6 stage1 apply で 15 min wait timeout になる事故を
    # 防ぐ。`deploy-all` 側 `wait_for_deployed_index_absent` は wait しか
    # しないので、destroy 側でも能動的に undeploy しておく。
    print(f"==> undeploy Vector Search deployed indexes (region={region})")
    vertex_cleanup.undeploy_all_vvs_deployed_indexes(project_id, region)
    return 0


def _run_state_rm_persistent_vvs() -> int:
    # 永続化 VVS resource を **state rm で外す** (= GCP には残置)。
    # `lifecycle.prevent_destroy = true` だけでは依存閉包で touch されて
    # `Instance cannot be destroyed` で全 destroy が止まる事故を 2026-05-03
    # に観測したため、state rm pattern に変更。`module.vector_search` 内の
    # `deployed_index` は GCP 上は previous step で undeploy 済なので、state rm
    # するだけで OK (terraform は state にないので touch しない)。次回
    # `deploy-all` は `terraform import` で復元する設計。
    persistent_state_addrs = [
        "module.vector_search.google_vertex_ai_index_endpoint_deployed_index.property_embeddings[0]",
        *(f"{p}[0]" for p in PERSISTENT_VVS_RESOURCES),
    ]
    rm_count = 0
    for addr in persistent_state_addrs:
        if state_rm(INFRA, addr):
            print(f"    state rm: {addr}")
            rm_count += 1
    if rm_count:
        print(
            f"==> state rm 永続化 VVS {rm_count} addr (GCP 残置、次回 deploy-all で import)"
        )
    return 0


def _run_wipe_gcs_buckets() -> int:
    project_id = env("PROJECT_ID")
    print("==> wipe GCS buckets (force_destroy=false blockers)")
    gcs_cleanup.wipe_all_terraform_managed_buckets(project_id)
    return 0


def _run_flip_deletion_protection() -> int:
    # state に実存する PROTECTED_TARGETS のみ flip 対象に。state にないものを
    # `-target` で渡すと Terraform は依存閉包を pull して **recreate** に走る
    # (Phase 7 Run 4 で empty-state の destroy-all 再走 → 12 resources added の
    # 事故)。filter で「flip だけ」に絞る。
    flip_targets = filter_targets_in_state(INFRA, list(PROTECTED_TARGETS))
    if not flip_targets:
        print(
            "==> state-flip skipped — "
            f"PROTECTED_TARGETS ({len(PROTECTED_TARGETS)}) はいずれも state 不在"
        )
        return 0

    print(
        f"==> terraform apply -target=<{len(flip_targets)}/{len(PROTECTED_TARGETS)} "
        "in-state resources with deletion_protection> "
        "-var=enable_deletion_protection=false (state-flip only, no recreate)"
    )
    targets = [arg for tgt in flip_targets for arg in ("-target", tgt)]
    run_terraform_streaming_with_lock_retry(
        [
            "terraform",
            f"-chdir={INFRA}",
            "apply",
            "-auto-approve",
            *_common_vars(),
            *targets,
        ],
        chdir_infra=INFRA,
    )
    return 0


def _run_destroy_kserve() -> int:
    print(
        "==> terraform destroy -target=module.kserve "
        "(K8s/Helm を GKE cluster より先に削除 — provider が cluster endpoint に依存するため)"
    )
    # operator destroy より先に CR を消して finalizer deadlock を避ける。
    kube_cleanup.delete_orphan_workloads()
    proc_rc = 0
    try:
        run_terraform_streaming_with_lock_retry(
            [
                "terraform",
                f"-chdir={INFRA}",
                "destroy",
                "-auto-approve",
                *_common_vars(),
                f"-target={KSERVE_MODULE_TARGET}",
            ],
            chdir_infra=INFRA,
        )
    except subprocess.CalledProcessError as exc:
        proc_rc = exc.returncode
    # exit code が 0 でも、cluster unreachable で何も消せなかった ↔ state には
    # 残ってる、というケースが起きうる (Phase 7 Run 4 で観測)。後方確認として
    # `terraform state list` で残存を直接見る。
    remaining = addresses_starting_with(INFRA, f"{KSERVE_MODULE_TARGET}.")
    if proc_rc != 0 or remaining:
        reason = (
            "exit code 非 0" if proc_rc != 0 else f"exit 0 だが state に {len(remaining)} 件残存"
        )
        print(
            f"    targeted destroy で K8s/Helm を片付けきれず ({reason}) — "
            "GKE cluster 既消滅の可能性。state rm で fallback 後、本体 destroy へ進む。"
        )
        if remaining:
            print(f"    module.kserve in state: {len(remaining)} address(es) → state rm")
            for addr in remaining:
                print(f"      {addr}")
            state_rm(INFRA, KSERVE_MODULE_TARGET)
        else:
            print("    module.kserve in state: empty (nothing to rm)")
    return 0


def _run_destroy_main() -> int:
    # 永続化 VVS resource (Index / Endpoint) は destroy 対象から除外する。
    # 「除外」は terraform に `-target=` で指定したものだけを destroy する仕様
    # を逆手に取り、state list 全 address から永続化対象を引いた集合を全件
    # `-target` で渡す方式で実現する (Index / Endpoint には Terraform 側に
    # `prevent_destroy = true` も入っているため二重防御)。
    all_addrs = state_list(INFRA)
    persistent_prefixes = tuple(f"{p}" for p in PERSISTENT_VVS_RESOURCES)
    destroy_addrs = [a for a in all_addrs if not a.startswith(persistent_prefixes)]

    if not destroy_addrs:
        print("==> state は永続化 VVS resource のみ — 本体 destroy をスキップ")
        return 0

    excluded = len(all_addrs) - len(destroy_addrs)
    if excluded:
        print(
            f"==> terraform destroy -auto-approve "
            f"(本体: {len(destroy_addrs)} addr 対象、永続 VVS {excluded} addr 除外)"
        )
        target_args = [arg for addr in destroy_addrs for arg in ("-target", addr)]
        run_terraform_streaming_with_lock_retry(
            [
                "terraform",
                f"-chdir={INFRA}",
                "destroy",
                "-auto-approve",
                *_common_vars(),
                *target_args,
            ],
            chdir_infra=INFRA,
        )
    else:
        print("==> terraform destroy -auto-approve (本体)")
        run_terraform_streaming_with_lock_retry(
            [
                "terraform",
                f"-chdir={INFRA}",
                "destroy",
                "-auto-approve",
                *_common_vars(),
            ],
            chdir_infra=INFRA,
        )
    return 0


# ---- step list ---------------------------------------------------------------

def _steps() -> list[DestroyStep]:
    return [
        DestroyStep(
            1,
            "seed-clean",
            "seed-test-clean (drop out-of-TF tables that block dataset destroy)",
            _run_seed_clean,
        ),
        DestroyStep(
            2,
            "undeploy-vertex-endpoints",
            "undeploy Vertex endpoint deployed_models (HTTP 400 回避)",
            _run_undeploy_vertex_endpoints,
        ),
        DestroyStep(
            3,
            "undeploy-vvs-deployed-indexes",
            "undeploy Vector Search deployed indexes (PDCA reproducibility guard)",
            _run_undeploy_vvs_deployed_indexes,
        ),
        DestroyStep(
            4,
            "state-rm-persistent-vvs",
            "state rm 永続化 VVS Index/Endpoint (GCP 残置、次回 deploy-all で import)",
            _run_state_rm_persistent_vvs,
        ),
        DestroyStep(
            5,
            "wipe-gcs-buckets",
            "wipe GCS buckets (force_destroy=false blockers)",
            _run_wipe_gcs_buckets,
        ),
        DestroyStep(
            6,
            "flip-deletion-protection",
            "terraform apply -var=enable_deletion_protection=false (state-flip only)",
            _run_flip_deletion_protection,
        ),
        DestroyStep(
            7,
            "destroy-kserve",
            "terraform destroy -target=module.kserve (K8s/Helm を GKE より先に)",
            _run_destroy_kserve,
        ),
        DestroyStep(
            8,
            "destroy-main",
            "terraform destroy 本体 (永続化 VVS 除外)",
            _run_destroy_main,
        ),
    ]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run destroy-all flow with optional step slicing (symmetrical with deploy-all)."
    )
    parser.add_argument(
        "--from-step",
        default="1",
        help="Start from this step number or name (e.g. 6, flip-deletion-protection).",
    )
    parser.add_argument(
        "--to-step",
        default="8",
        help="Stop after this step number or name (e.g. 7, destroy-kserve).",
    )
    return parser.parse_args()


def _resolve_step_ref(ref: str, steps: list[DestroyStep]) -> int:
    raw = ref.strip()
    if raw.isdigit():
        step_no = int(raw)
        if any(step.number == step_no for step in steps):
            return step_no
    lowered = raw.lower()
    for step in steps:
        if lowered == step.name:
            return step.number
    valid = ", ".join([str(step.number) for step in steps] + [step.name for step in steps])
    raise SystemExit(f"[error] unknown step {ref!r}. valid values: {valid}")


# ---- orchestration entrypoint -----------------------------------------------

def main() -> int:
    global _DESTROY_ALL_STARTED_AT, _STEP_STARTED_AT
    _DESTROY_ALL_STARTED_AT = None
    _STEP_STARTED_AT = None

    args = _parse_args()
    steps = _steps()
    total = len(steps)
    from_step = _resolve_step_ref(args.from_step, steps)
    to_step = _resolve_step_ref(args.to_step, steps)
    if from_step > to_step:
        raise SystemExit(f"[error] --from-step ({from_step}) must be <= --to-step ({to_step})")

    project_id = env("PROJECT_ID")
    print(f"==> destroy-all on project {project_id!r}")

    # Pre-check (slicing 範囲に関わらず必ず走る early-return guard):
    # state が空なら destroy は何もすることがない。`-target` apply が
    # 依存ごと resource を recreate してしまう副作用 (Phase 7 Run 4 で
    # WIF pool 30 日 soft-delete に再衝突した事故) を避けるため early-return。
    state_count = state_size(INFRA)
    if state_count == 0:
        print("==> state list is empty — nothing to destroy. (前回の destroy-all で完了済)")
        print("    Re-provision with: make deploy-all")
        return 0
    print(f"==> state has {state_count} address(es) — proceeding")

    selected = [step for step in steps if from_step <= step.number <= to_step]
    print(
        f"==> destroy-all selection: from_step={from_step} to_step={to_step} "
        f"steps={[step.name for step in selected]}"
    )

    current_step: DestroyStep | None = None
    try:
        for step in selected:
            current_step = step
            _step(step.number, total, step.label)
            rc = step.run()
            if rc != 0:
                print(
                    f"==> destroy-all FAILED at step {step.number} ({step.name}) — see logs above"
                )
                return rc
            _step_done()
    except BaseException:
        if current_step is not None:
            print(
                f"==> destroy-all FAILED at step {current_step.number} ({current_step.name}) "
                "— see traceback above"
            )
        raise

    if _DESTROY_ALL_STARTED_AT is not None:
        total_elapsed = time.monotonic() - _DESTROY_ALL_STARTED_AT
        print()
        print(f"==> destroy-all complete. total_elapsed={total_elapsed:.0f}s")
    else:
        print()
        print("==> destroy-all complete.")
    print("    tfstate bucket preserved. Re-provision with: make deploy-all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
