"""End-to-end provisioning + rollout in one shot. Calls (in order):

1. `tf_bootstrap` — enable APIs + create tfstate bucket (idempotent)
2. `tf_init` — terraform init with bucket preflight
3. `recover_wif` — undelete + import WIF pool/provider if a previous
   `make destroy-all` left them soft-deleted (GCP keeps WIF resources for
   30 days after delete; recreating with the same ID otherwise hits HTTP
   409 "already exists"). Implementation lives in
   `scripts/setup/recover_wif.py` so the recovery is testable / reusable.
4. `sync_dataform` — regenerate pipeline/data_job/dataform/workflow_settings.yaml
5. `tf_plan` — terraform plan -out=tfplan (using setting.yaml defaults)
6. `terraform apply -auto-approve` — apply infra in two stages
7. `seed-lgbm-model` — `gs://<project>-models/lgbm/latest/model.bst` に
   合成 LightGBM ranker を seed (Phase 7 Run 5: tf-apply 直後の bucket は空で、
   step 10 で apply される `property-reranker` InferenceService の
   storage-initializer init container が ``RuntimeError: Failed to fetch
   model. No model found in gs://...`` で CrashLoopBackOff に陥る)。
8. `seed-test` — `feature_mart.property_features_daily` など smoke に必要な
   最小 row を seed。Feature View manual sync の source row をここで作る。
9. `sync-elasticsearch` — `feature_mart.properties_cleaned` を Elasticsearch
   `properties` index へ bulk upsert する。
   lexical lane が空だと `ops-search-components` が `lexical=0` で fail
   するため、canonical lexical path の一部として本線に組み込む。
10. `backfill-vvs` — `feature_mart.property_embeddings` から Vertex Vector Search
   index へ初回 datapoint を upsert する。endpoint / deployed index だけを作っても
   中身が空だと `ops-vertex-vector-search-smoke` が 0 neighbors で fail するため、
   Phase 7 canonical path の一部として本線に組み込む。
11. `trigger-fv-sync` — Feature Online Store / Feature View live path 向けに
   regional REST API で manual sync を起動し、完了まで poll する。
12. `apply-manifests` — `kubectl apply -k infra/manifests/` (Phase 7 Run 2:
   旧運用は手で `make apply-manifests` を叩く前提だったが、PDCA loop で
   毎回手作業を要求すると `destroy-all → deploy-all` が成立しない)。
13. `overlay-configmap` — search-api ConfigMap に Elasticsearch URL /
   Terraform の Vertex / Feature Store 出力を流し込む。実装は
   `scripts/deploy/configmap_overlay.py`
   で、ConfigMap schema は `scripts/lib/config.py` に集約 (Phase 7 W2-5 で
   `_run_overlay_configmap` と `sync_configmap.py` が独立にキー列を手書き
   していて drift した教訓 — 構造的に防止)。
14. `deploy/api_gke` — Cloud Build + kubectl rollout search-api。

Idempotent — re-running on an already-provisioned project applies a zero-diff
plan and rolls a fresh search-api image revision. Costs accrue from the
moment infra is created. See CLAUDE.md non-negotiables.

設計方針 (Phase 7 W3 リファクタ):
- 本ファイルは **orchestrator のみ**。各 step の business logic は
  sibling module (`scripts/{ci,deploy,setup}/<step>.py`) または
  topical module (`scripts/{lib,infra}/`) に置く。
- **Terraform**: stage1 の target 集合・409 リトライ・state lock 吸収は
  ``scripts/domain/terraform/stage_apply.py`` と ``scripts/domain/terraform/lock.py``
  に集約 (このファイルにロジックを再増殖させない)。
- _run_* は対応 module の `main()` を呼ぶだけの thin wrapper にする
  (drift 源にならないように)。
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from scripts._common import env
from scripts.adapters.kubectl import kubectl_run
from scripts.ci.sync_dataform import main as sync_dataform_main
from scripts.deploy.api_gke import main as deploy_api_main
from scripts.deploy.composer_deploy_dags import main as composer_deploy_dags_main
from scripts.deploy.configmap_overlay import main as overlay_configmap_main
from scripts.deploy.seed_lgbm_model import main as seed_lgbm_main
from scripts.domain.gcp.feature_view_sync import main as feature_view_sync_main
from scripts.domain.k8s.elasticsearch_wait import wait_until_es_healthy
from scripts.domain.k8s.kubectl_context import ensure as ensure_kubectl_context
from scripts.ops.sync_elasticsearch import run as sync_elasticsearch_run
from scripts.setup.backfill_vector_search_index import main as backfill_vector_search_main
from scripts.setup.recover_wif import main as recover_wif_main
from scripts.setup.seed_minimal import main as seed_minimal_main
from scripts.setup.tf_apply import main as tf_apply_main
from scripts.setup.tf_bootstrap import main as tf_bootstrap_main
from scripts.setup.tf_init import main as tf_init_main
from scripts.setup.tf_plan import main as tf_plan_main

_REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFESTS = _REPO_ROOT / "infra" / "manifests"

# Overall start time; per-step timing relates elapsed time to the wall-clock
# position in the deploy-all sequence so operators can see WHICH step is slow
# when a rollout hangs (e.g. Cloud Build wait dominating step 7).
_DEPLOY_ALL_STARTED_AT: float | None = None
_STEP_STARTED_AT: float | None = None

# Per-step wall-clock history (machine-local; logs/ is gitignored). Every
# completed step appends one row; at the start of a run we read it back to print
# an ETA derived from the median of recent successful runs on this host. The 58 min
# step 6 incident showed how easily "is it stuck?" gets misjudged without a baseline.
_TIMINGS_CSV = _REPO_ROOT / "logs" / "deploy_timings.csv"
_TIMINGS_HEADER = ("recorded_at_utc", "step_number", "step_name", "elapsed_sec", "status")
_TIMINGS_KEEP_PER_STEP = 10  # median over the most recent N successful runs
_TIMINGS_MAX_ROWS = 4000  # soft cap; oldest rows trimmed on append


@dataclass(frozen=True)
class DeployStep:
    number: int
    name: str
    label: str
    run: Callable[[], int]
    # 2026-05-10: 各 step が走る前に外部 reconciler の完了を待つ optional hook。
    # main loop が `step.run()` の直前に precondition を呼び、例外で fail する。
    # 例: step 10 (sync-elasticsearch) は `wait_until_es_healthy` を待ってから
    # 走らないと ECK の Phase=ApplyingChanges race で `Server disconnected` で
    # fail する。precondition を step に直接持たせることで:
    # 1. _run_* 関数本体は本来の責務 (sync) に集中
    # 2. 失敗時の error 報告が main loop 側で統一される (偽 exit 0 罠も波及しない)
    # 3. 将来 race が観測されたら precondition を 1 行追加するだけ
    precondition: Callable[[], object] | None = None


def _step(n: int, total: int, label: str) -> None:
    global _DEPLOY_ALL_STARTED_AT, _STEP_STARTED_AT
    now = time.monotonic()
    if _DEPLOY_ALL_STARTED_AT is None:
        _DEPLOY_ALL_STARTED_AT = now
    prev_elapsed = now - _STEP_STARTED_AT if _STEP_STARTED_AT is not None else 0.0
    total_elapsed = now - _DEPLOY_ALL_STARTED_AT
    _STEP_STARTED_AT = now
    print()
    print("================================================================")
    print(f" deploy-all  step {n}/{total}: {label}")
    if n > 1:
        print(f" (prev_step_elapsed={prev_elapsed:.0f}s total_elapsed={total_elapsed:.0f}s)")
    print("================================================================")


def _elapsed_since_step_start() -> float:
    return 0.0 if _STEP_STARTED_AT is None else time.monotonic() - _STEP_STARTED_AT


def _step_done(step: DeployStep) -> None:
    """Emit a `step-done` line and append the step's wall-clock time to the history CSV."""
    if _STEP_STARTED_AT is None:
        return
    elapsed = _elapsed_since_step_start()
    print(f" deploy-all  step-done elapsed={elapsed:.0f}s")
    _record_step_timing(step.number, step.name, elapsed, "ok")


# ---------------------------------------------------------------------------
# step-timing history (CSV) + ETA
# ---------------------------------------------------------------------------


def _fmt_duration(sec: float) -> str:
    total = max(0, round(sec))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m"
    if m:
        return f"{m}m{s:02d}s"
    return f"{s}s"


def _record_step_timing(step_number: int, step_name: str, elapsed_sec: float, status: str) -> None:
    """Append one row to ``logs/deploy_timings.csv`` (best-effort; never fails the run)."""
    try:
        _TIMINGS_CSV.parent.mkdir(parents=True, exist_ok=True)
        new_file = not _TIMINGS_CSV.exists()
        row = [
            _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
            str(step_number),
            step_name,
            f"{elapsed_sec:.1f}",
            status,
        ]
        with _TIMINGS_CSV.open("a", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            if new_file:
                writer.writerow(_TIMINGS_HEADER)
            writer.writerow(row)
        _trim_timings_csv()
    except OSError:
        pass  # timing history is a convenience, not a requirement


def _trim_timings_csv() -> None:
    try:
        with _TIMINGS_CSV.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        if len(rows) <= _TIMINGS_MAX_ROWS + 1:  # +1 for header
            return
        header, body = rows[0], rows[1:]
        body = body[-_TIMINGS_MAX_ROWS:]
        with _TIMINGS_CSV.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            writer.writerows(body)
    except OSError:
        pass


def _load_step_baselines() -> dict[str, float]:
    """Median elapsed-seconds per step name over the most recent successful runs."""
    samples: dict[str, list[float]] = {}
    try:
        if not _TIMINGS_CSV.exists():
            return {}
        with _TIMINGS_CSV.open(newline="", encoding="utf-8") as fh:
            for rec in csv.DictReader(fh):
                if rec.get("status") != "ok":
                    continue
                name = rec.get("step_name") or ""
                try:
                    samples.setdefault(name, []).append(float(rec.get("elapsed_sec") or 0.0))
                except ValueError:
                    continue
    except OSError:
        return {}
    return {
        name: statistics.median(vals[-_TIMINGS_KEEP_PER_STEP:])
        for name, vals in samples.items()
        if vals
    }


def _print_eta(selected: list[DeployStep], baselines: dict[str, float]) -> None:
    if not baselines:
        print(
            "==> deploy-all ETA: no prior timing history yet (logs/deploy_timings.csv) — "
            "this run will seed it"
        )
        return
    known = [baselines[s.name] for s in selected if s.name in baselines]
    missing = [s.name for s in selected if s.name not in baselines]
    total = sum(known)
    prefix = "~" if not missing else "≥"
    print(
        f"==> deploy-all ETA: {prefix}{_fmt_duration(total)} for {len(selected)} step(s) "
        f"(median of recent runs; {len(known)}/{len(selected)} steps have history)"
    )
    # surface the heavy hitters so the operator knows which wait dominates.
    heavy = sorted(
        ((s.name, baselines[s.name]) for s in selected if s.name in baselines),
        key=lambda kv: kv[1],
        reverse=True,
    )[:3]
    if heavy:
        print("    biggest: " + ", ".join(f"{name}={_fmt_duration(sec)}" for name, sec in heavy))
    if missing:
        print(f"    no history yet for: {', '.join(missing)}")


def _run_tf_bootstrap() -> int:
    return tf_bootstrap_main()


def _run_tf_init() -> int:
    return tf_init_main()


def _run_recover_wif() -> int:
    return recover_wif_main()


def _run_sync_dataform() -> int:
    return sync_dataform_main()


def _run_tf_plan() -> int:
    return tf_plan_main()


def _run_tf_apply() -> int:
    return tf_apply_main()


def _run_seed_lgbm_model() -> int:
    return seed_lgbm_main()


def _run_seed_test() -> int:
    return seed_minimal_main()


def _run_sync_elasticsearch() -> int:
    # ECK health wait は precondition (DeployStep.precondition=wait_until_es_healthy)
    # で main loop が呼ぶ。ここは sync 本体の責務に集中する。
    project_id = env("PROJECT_ID")
    es_url = env(
        "ELASTICSEARCH_URL",
        "http://elasticsearch.search.svc.cluster.local:9200",
    )
    # sync_elasticsearch.run returns a shell exit code (0 = ok, non-zero = failure).
    return sync_elasticsearch_run(
        [
            f"--project-id={project_id}",
            f"--es-url={es_url}",
        ]
    )


def _run_trigger_feature_view_sync() -> int:
    return feature_view_sync_main()


def _run_backfill_vvs() -> int:
    return backfill_vector_search_main(["--apply"])


def _run_apply_manifests() -> int:
    """`kubectl apply -k infra/manifests/` against the freshly-provisioned cluster.

    Phase 7 Run 2 まで `infra/manifests/README.md §デプロイ` は「Terraform apply
    後に make apply-manifests を手で叩く」運用だった。PDCA dev loop
    (`destroy-all → deploy-all → run-all`) ではこの手作業が成立しないため、
    deploy-all に組み込んで一発で cluster ワークロードを展開する。
    試行錯誤目的の手 apply は引き続き ``make apply-manifests`` で可能。
    """
    ensure_kubectl_context()
    print(f"==> kubectl apply -k {MANIFESTS}")
    kubectl_run("apply", "-k", str(MANIFESTS))
    return 0


def _run_overlay_configmap() -> int:
    return overlay_configmap_main()


def _run_composer_deploy_dags() -> int:
    return composer_deploy_dags_main()


def _run_deploy_api() -> int:
    return deploy_api_main()


def _steps() -> list[DeployStep]:
    return [
        DeployStep(
            1,
            "tf-bootstrap",
            "tf-bootstrap (enable APIs + tfstate bucket, idempotent)",
            _run_tf_bootstrap,
        ),
        DeployStep(2, "tf-init", "tf-init (preflight + terraform init)", _run_tf_init),
        DeployStep(
            3,
            "recover-wif",
            "recover WIF pool/provider if soft-deleted (PDCA loop safety)",
            _run_recover_wif,
        ),
        DeployStep(
            4,
            "sync-dataform",
            "sync-dataform-config (regenerate workflow_settings.yaml)",
            _run_sync_dataform,
        ),
        DeployStep(5, "tf-plan", "tf-plan (saves infra/tfplan)", _run_tf_plan),
        DeployStep(
            6, "tf-apply", "terraform apply staged (core -> kube-ready -> full)", _run_tf_apply
        ),
        DeployStep(
            7,
            "seed-lgbm-model",
            "seed gs://<project>-models/lgbm/latest/model.bst (reranker bootstrap)",
            _run_seed_lgbm_model,
        ),
        DeployStep(
            8,
            "seed-test",
            "seed-test (populate feature_mart tables for smoke + Feature View sync)",
            _run_seed_test,
        ),
        DeployStep(
            9,
            "apply-manifests",
            "kubectl apply -k infra/manifests/ (Gateway / Deployment / ISVC / policies)",
            _run_apply_manifests,
        ),
        DeployStep(
            10,
            "sync-elasticsearch",
            "sync Elasticsearch from feature_mart.properties_cleaned (canonical lexical path)",
            _run_sync_elasticsearch,
            # 2026-05-09 incident: step 9 (apply-manifests) → step 10 race で
            # ECK ApplyingChanges 中に sync が走り `Server disconnected` で fail。
            # precondition で ES `.status.health` ∈ {green, yellow} まで待つ。
            # 5 min timeout = ECK Operator 停滞のシグナル
            # (see `docs/troubleshooting/eck-license-reconcile-stall.md`)。
            precondition=wait_until_es_healthy,
        ),
        DeployStep(
            11,
            "backfill-vvs",
            "backfill VVS from feature_mart.property_embeddings (canonical semantic path)",
            _run_backfill_vvs,
        ),
        DeployStep(
            12,
            "trigger-fv-sync",
            "trigger Feature View sync and wait for completion (FOS live path)",
            _run_trigger_feature_view_sync,
        ),
        DeployStep(
            13,
            "overlay-configmap",
            "overlay search-api-config (Elasticsearch URL + VVS/FOS outputs)",
            _run_overlay_configmap,
        ),
        DeployStep(
            14,
            "composer-deploy-dags",
            "upload pipeline/dags/*.py to Composer DAG GCS bucket (Phase 7 W2-4)",
            _run_composer_deploy_dags,
        ),
        DeployStep(
            15,
            "deploy-api",
            "deploy-api (Cloud Build + kubectl rollout search-api)",
            _run_deploy_api,
        ),
    ]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Phase 7 deploy-all flow with optional step slicing."
    )
    parser.add_argument(
        "--from-step",
        default="1",
        help="Start from this step number or name (e.g. 4, sync-dataform, tf-apply).",
    )
    parser.add_argument(
        "--to-step",
        default="15",
        help="Stop after this step number or name (e.g. 9, sync-elasticsearch, deploy-api).",
    )
    return parser.parse_args()


def _resolve_step_ref(ref: str, steps: list[DeployStep]) -> int:
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


def main() -> int:
    global _DEPLOY_ALL_STARTED_AT, _STEP_STARTED_AT
    _DEPLOY_ALL_STARTED_AT = None
    _STEP_STARTED_AT = None

    args = _parse_args()
    steps = _steps()
    total = len(steps)
    from_step = _resolve_step_ref(args.from_step, steps)
    to_step = _resolve_step_ref(args.to_step, steps)
    if from_step > to_step:
        raise SystemExit(f"[error] --from-step ({from_step}) must be <= --to-step ({to_step})")

    selected = [step for step in steps if from_step <= step.number <= to_step]
    print(
        f"==> deploy-all selection: from_step={from_step} to_step={to_step} "
        f"steps={[step.name for step in selected]}"
    )
    _print_eta(selected, _load_step_baselines())

    current_step: DeployStep | None = None
    try:
        for step in selected:
            current_step = step
            _step(step.number, total, step.label)
            # 2026-05-10: precondition (外部 reconciler 完了待ち) があれば step.run()
            # の前に実行。例外で fail させ、main loop 側で統一 error 報告する。
            if step.precondition is not None:
                print(
                    f"==> step {step.number} ({step.name}) precondition: {step.precondition.__name__}"
                )
                step.precondition()
            rc = step.run()
            if rc != 0:
                _record_step_timing(step.number, step.name, _elapsed_since_step_start(), "failed")
                print(f"==> deploy-all FAILED at step {step.number} ({step.name}) — see logs above")
                return rc
            _step_done(step)
    except BaseException:
        if current_step is not None:
            _record_step_timing(
                current_step.number, current_step.name, _elapsed_since_step_start(), "failed"
            )
            print(
                f"==> deploy-all FAILED at step {current_step.number} ({current_step.name}) "
                "— see traceback above"
            )
        raise

    if _DEPLOY_ALL_STARTED_AT is not None:
        total_elapsed = time.monotonic() - _DEPLOY_ALL_STARTED_AT
        print()
        print(
            f"==> deploy-all complete. total_elapsed={total_elapsed:.0f}s "
            f"({_fmt_duration(total_elapsed)})"
        )
    else:
        print()
        print("==> deploy-all complete.")
    print("    Verify with: make ops-livez && make ops-api-url")
    print("    Pipeline submit is separate: make ops-train-now")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
