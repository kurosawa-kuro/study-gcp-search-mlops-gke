# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済み実装ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)。

---

## 本 sprint scope (2026-05-09)

- 対象: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §1 #4 / #5 と Wave 5 / Wave 8 の残件
- **scope outside**: Wave 9 (独自ドメイン + HTTPS + DNS) — user 指示で本 sprint 除外

---

## 完成定義 (Definition of Done) — **本 sprint ✅ 完了 (2026-05-10)**

| ID | タスク | 結果 |
|---|---|---|
| T1 ⚠️ | M-Wave5 live 検証通し | ✅ `make verify-live-acceptance` PASS (e2e 22.68s)。canonical 経路: `lexical=4 / semantic=3 / rerank=5`、`ndcg_at_10=1.0`、KServe rerank 経由で `final_rank` / `me5_score` 返却 |
| T2-T5 | docs / contract test / framework | ✅ [`03_実装カタログ.md §7.3`](../architecture/03_実装カタログ.md) 移管済 |

⚠️ = canonical 必須項目。[`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) §0.1 ゴール劣化禁止対象。

---

## 2026-05-10 進捗 (live cluster、T1 検証直前)

**cluster は live**:
- `make deploy-all` step 1-15 全完走 (deploy-all complete、resume 経由で完了)
- ES on GKE (HTTP + anonymous superuser、(a') 解採用)、health=green、Phase=Ready
- GKE / Composer / KServe / VVS Index/Endpoint/deployed_index / Vertex Endpoints / Pub/Sub / Feature View sync 全 live

### 残: T1 (verify-live-acceptance)

```bash
make verify-live-acceptance
```

= run-all-core 相当の canonical 検証。期待: `lexical=N1 semantic=N2 rerank=N3` all non-zero、`ndcg_at_10=1.0`、`final_rank`/`me5_score` 返却。

T1 PASS 後は最後に `make destroy-all` (新 step 分離で安全 teardown)。

### 2026-05-10 incident と適用修正 (全件 contract test pin)

| # | 問題 | 適用修正 | contract test |
|---|---|---|---|
| 1 | WIF pool soft-delete 30日残置 → tf-apply 409 | `tf_apply.py` 冒頭 `recover_wif_main()` idempotent hook | `test_tf_apply_invokes_recover_wif_as_pre_step` |
| 2 | destroy-all step 分離なし (deploy 側との非対称) | `DestroyStep` + `--from-step/--to-step` slicing で対称化 | `test_destroy_all_provides_step_slicing_symmetric_with_deploy_all` |
| 3 | terraform_lock parser が ANSI escape で fail | ANSI strip + 緩い行頭 anchor | `test_parse_lock_id_handles_real_ansi_color_output` |
| 4 | sync-elasticsearch ECK ApplyingChanges race | `wait_until_es_healthy` precondition (`DeployStep.precondition` framework) | `test_sync_elasticsearch_step_waits_for_es_health_first` + 3 unit test |
| 5 | NetworkPolicy elastic-system ns ingress 漏れ | `networkpolicy.yaml` に追加 | `test_es_networkpolicy_allows_eck_operator_namespace` |
| 6 | canonical URL http vs ECK default HTTPS 不整合 | ES manifest `selfSignedCertificate.disabled: true` + `xpack.security.authc.anonymous` (学習用 (a') 解) | `test_es_manifest_pins_http_and_anonymous_auth` |
| 7 | tee block buffer で 40 分 visibility ゼロ | `stdbuf -oL` を推奨パターンに格上げ | doc: `bg-pipe-fake-exit-zero.md` |
| 8 | bg pipe 偽 exit 0 | `pipefail` 推奨 + Bash tool 完了通知後の output grep 必須化 | doc + CLAUDE.md 「Claude Code 自身の運用ルール」 |
| 9 | mock 漏れ (`wait_until_es_healthy`) | module-top-level import + framework 化で mock target 一意化 | unit test 3 件 (`test_main_invokes_precondition_before_run` 他) |

### 残課題 (別 sprint、Wave 8.7 として backlog 化)

production 化 (HTTPS + password auth) は [`TASKS_ROADMAP.md §2 Wave 8.7`](TASKS_ROADMAP.md):
- canonical URL を環境変数で http/https 切替可能化
- ECK auto-generated `elasticsearch-es-elastic-user` secret から password fetch 経路を `_run_sync_elasticsearch` に組込
- `xpack.security.authc.anonymous` 削除 → default HTTPS+auth へ
- Wave 8 contract test を HTTPS+auth pin に拡張

### 残課題 (Makefile / Bash 運用改善、優先度低)

| ID | 課題 | 詳細 |
|---|---|---|
| C3 | `verify-local-hybrid` の説明 (CLAUDE.md) と実装ズレ | ✅ 2026-05-10 解消、CLAUDE.md を `parity + ground-truth contract + verify-local-app + verify-local-ml` に精緻化 |
| C4 | Makefile target に `stdbuf -oL` を組込 | 現状は Bash tool 側で `bash -c 'set -o pipefail; ... \| stdbuf -oL -eL tee ...'` を毎回書いている。Makefile target で wrapping すれば次回から Bash tool 側のオペが軽くなる。Wave 7 (Makefile 整理) の延長 |

---

## 次 sprint (本 sprint 外)

- **M-Wave8.5 Phase 概念完全撤廃**: 現 sprint で canonical wording として残置した「Phase 7 で本実装、後方派生で Phase 6 へ引き算」(01 §3 / workflow contract test 15+ / runbook 数十箇所) を固有名 (canonical / Composer なし派生) へ完全置換。完了条件: `grep -rE "Phase [0-9]" docs/ tests/integration/workflow/` が **0 件**。詳細は [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §2 Wave 8.5
- **M-Wave8.6 orchestrator ドメイン分離 Phase 2/3**: Phase 1 (step 分離 + tf_apply.py 切り出し + destroy_all 対称化) は 2026-05-09 完了 (03_実装カタログ §7.3)。Phase 2 (`scripts/infra/*` → `scripts/domain/{gcp,k8s,terraform,data}/`) / Phase 3 (subprocess wrapper を `scripts/adapters/`) が残件。詳細は [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §2 Wave 8.6

---

## 参照

- 完了済み実装スナップショット + マイルストーン履歴: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- Wave / 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証ゲート定義 (V1-V6): [`../runbook/04_検証.md`](../runbook/04_検証.md)
- PDCA / 運用手順: [`../runbook/05_運用.md`](../runbook/05_運用.md)
