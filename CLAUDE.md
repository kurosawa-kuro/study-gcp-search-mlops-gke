# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリの性質

不動産ハイブリッド検索 + 継続改善 MLOps サイクルの個人技術学習プロジェクト。題材は不動産検索、技術スタックは **Cloud Composer 本線 orchestration + Vertex AI Pipelines / Feature Store / Vector Search / Model Registry + GKE Deployment + KServe InferenceService + PMLE 統合技術 (BQML / Dataflow / TreeSHAP / Monitoring SLO)**。

最初に読むべきファイル:

- [README.md](README.md) — プロジェクト概要 + 技術スタック + 非負制約
- [docs/tasks/TASKS.md](docs/tasks/TASKS.md) — current sprint
- [docs/architecture/01_仕様と設計.md](docs/architecture/01_仕様と設計.md) — canonical 仕様
- [docs/architecture/03_実装カタログ.md](docs/architecture/03_実装カタログ.md) — 実装スナップショット

設計思想 (Port/Adapter / 依存方向 `core → ports ← adapters`) は不変、adapter 実装だけ差し替えで Local 検証 / Cloud canonical / 実案件 reference (Elasticsearch + Redis 同義語 + ME5 + Vertex Vector Search + LightGBM) に到達できる構造を維持する。

## 非負制約

- **中核 5 要素を必須**: **Elasticsearch BM25 + multilingual-e5 + Vertex AI Vector Search + RRF + LightGBM LambdaRank**。削除・置換・無効化は明示的な user 合意がない限り実施しない
- **Vertex Vector Search の役割**: ME5 ベクトル検索の本番 serving index。embedding 生成履歴・メタデータの正本は BigQuery 側 (data lake / serving index の二層構造)
- **Feature Store**: Vertex AI Feature Store (Feature Group / Feature View / Feature Online Store) により training-serving skew を防ぐ。Online Store を使う実務では **Feature View が serving 接続点**。KServe から Feature Online Store を Feature View 経由で opt-in 参照
- **Cloud Composer (本線 orchestration)**: Managed Airflow Gen 3 を本線オーケストレーターとして本実装 (`infra/terraform/modules/composer/` + `pipeline/dags/` の 3 DAG: `daily_feature_refresh` / `retrain_orchestration` / `monitoring_validation`)。本線 retrain schedule は Composer DAG。**Vertex `PipelineJobSchedule` は完全撤去** (同一 PipelineJob 二重起動禁止)。**Cloud Scheduler / Eventarc / Cloud Function trigger は軽量代替・smoke / manual trigger 用途として残す** (本線 retrain と同じ job を別系統で起動しないこと = 二重起動禁止)
- **実案件 reference architecture**: Elasticsearch + Redis 同義語辞書 + ME5 + Vertex Vector Search + LightGBM。本リポも lexical lane は Elasticsearch を canonical とする
- **Event schema 共通契約**: 検索 MLOps の継続改善サイクル (行動ログ → 正解データ → 再学習 → 評価 → deployment gate) を維持するため、以下の 3 テーブル + `action_type` enum + 重み付き relevance label を保つ:
  - `search_events` (`event_id` / `search_id` / `user_id` / `session_id` / `query` / `filters_json` / `timestamp` / `app_version` / `model_version`)
  - `search_impressions` (`event_id` / `search_id` / `property_id` / `rank` / `lexical_score` / `vector_score` / `rrf_score` / `rerank_score` / `timestamp`)
  - `user_actions` (`event_id` / `search_id` / `property_id` / `action_type` / `action_value` / `timestamp`)
  - `action_type` enum 8 種: アプリ emit 5 種 (`click` / `detail_view` / `favorite` / `request_button_click` / `request_complete`) + synthetic 注入専用 3 種 (`inquiry_complete` / `contract` / `bounce`)
  - 重み付き relevance label: `click`=1, `detail_view`=2, `favorite`=3, `request_button_click`=4, `request_complete`=5, `inquiry_complete`=7, `contract`=10, `no_action`=0, `bounce`=0/-1
  - **クリックは「完全な正解」ではなく弱教師信号**として扱う。複合ラベルで LightGBM LambdaRank 用 relevance label に変換するのが canonical
  - synthetic 注入は `definitions/labeling/synthetic_actions.yaml` から `ranking_labels.label_source='synthetic_*'` で擬似正解データを書き込む。`ml/labeling/` は psycopg / google.cloud import 禁止で純粋ロジック維持
- ⚠️ **canonical 死守ライン (LightGBM 接続)**: `pipeline/training_job/main.py` から Repository 経由で実データを trainer に渡す配線を維持し、synthetic-only 学習へ退行させない

## 中核コードの不変ライン

- **`/search` デフォルト挙動 / 中核 5 要素の挙動・データフロー**は変えない
- **6 軸 Port/Adapter**: lexical retriever / semantic encoder / semantic vector store / reranker / feature fetcher / ranking log
- 検索品質改善は中核 5 要素を前提にした上で実施
- 教材対象外技術 (Agent Builder / Vizier / Model Garden / Gemini RAG / W&B / Looker Studio / Doppler) を導入しない

## コマンド早見

```bash
make doctor                    # 前提ツール確認
make sync                      # uv sync (full workspace)
make help                      # 全 target 一覧

# CI 同等チェック
make check                     # ruff + ruff format --check + mypy strict + pytest
make check-layers              # AST-based Port-Adapter 境界検査
make tf-validate               # terraform validate (offline)

# Local 検証 (GCP に触れない)
make verify-local-app          # FastAPI boot + DI + API contract
make verify-local-ml           # ML / pipeline 単体 + smoke train
make verify-local-hybrid       # verify-local-parity + ground-truth contract + verify-local-app + verify-local-ml (live なし全 PASS)

# Cloud canonical (実 GCP)
make deploy-all                # 15 step (tf-bootstrap → 2 段階 apply → seed → sync-elasticsearch → composer-deploy-dags → deploy-api)
make run-all                   # canonical validation 12 step
make destroy-all               # no-prompt teardown (4 段)
```

## current sprint の正本 (`docs/tasks/TASKS.md`)

`docs/tasks/TASKS.md` を **current sprint の正本** とする。「現在の目的 / 今回の作業対象 / 今回はやらない / 完了条件 / 実装済 / 未実装」を 1 ファイルに集約。長期 backlog は `docs/tasks/TASKS_ROADMAP.md`、過去判断履歴は `docs/decisions/`。

権威順位: `TASKS_ROADMAP > TASKS > 01_仕様と設計 > README > CLAUDE`

`docs/` 配下の構造:

```
docs/
├── architecture/{01_仕様と設計.md, 03_実装カタログ.md}
├── tasks/{TASKS.md, TASKS_ROADMAP.md, ...}
├── runbook/{04_検証.md, 05_運用.md}
├── decisions/{0001..0008.md}
└── conventions/{命名規約.md, スクリプト規約.md, フォルダ-ファイル.md, Docker配置規約.md, Makefile規約.md}
```

## Claude Code 標準セット (`.claude/` 一式)

エージェント / スキル / コマンド / フックは `.claude/` に集約。最小構成から開始し、有用性が出たもののみ追加する方針。

| 種別 | 名前 | 用途 |
|---|---|---|
| agent | `port-adapter-boundary-reviewer` | diff の Port-Adapter 境界違反 (adapter import 漏れ / RULES 更新忘れ / noop_adapter 不足 / DI 配線忘れ) を検出。`make check-layers` の補完。read-only |
| agent | `feature-parity-checker` | 特徴量変更 PR の **6 ファイル parity** を検証 (Dataform / `build_ranker_features` / `FEATURE_COLS_RANKER` / TF `ranking_log.features` / `validate_feature_skew.sql` / Vertex Feature Group)。read-only |
| skill | `port-adapter-scaffolder` | 新 Port を切るときの 6 ステップ (Port → Noop adapter → RULES → Fake → composition root → 本番 adapter → 03_実装カタログ追記) |
| command | `/check-parity` | `feature-parity-checker` を呼ぶ薄い wrapper |
| hook | `SessionStart` (`hooks/show-tasks.sh`) | `docs/tasks/TASKS.md` の先頭 50 行を表示 |
| hook | `PostToolUse` (`hooks/check-layers.sh`) | Edit/Write/MultiEdit の対象が Port-Adapter sensitive area なら `make check-layers` をバックグラウンド実行、失敗時のみ stderr に短い出力 |

その他:

- `.github/agents/gcp-mlops-theme-research.agent.md` — 検索/ランキング設計比較と markdown 提案専用 agent (GitHub 側 user-invocable)
- `.claude/settings.local.json` (gitignore 対象) — 個人ごとの permissions allowlist。team 共有の hooks は `.claude/settings.json` に書く

## Claude Code 自身の運用ルール (2026-05-10 incident 反映)

過去の自分が踏んだ罠を再発させないためのチェックリスト。報告前に必ず通すこと。

### bg コマンド完了後の偽 exit 0 検出 (必須)

`Background command "..." completed (exit code 0)` を **そのまま信用しない**。
`make ... 2>&1 | tail -N` 形式は **末尾 `tail` の exit code が 0 = bash exit 0** で、中間 fail を黙殺する。

完了通知後は **必ず** output 末尾を以下で grep:

```bash
tail -30 <output-file> | grep -E "FAILED|Error:|Traceback|exit code [^0]|did not"
```

ヒットした場合は ✅ 報告禁止、原因究明に切り替える。詳細: [`docs/troubleshooting/bg-pipe-fake-exit-zero.md`](docs/troubleshooting/bg-pipe-fake-exit-zero.md)。

推奨パターン (新規 bg 実行時):

```bash
make foo 2>&1 | tee /tmp/foo.log; exit ${PIPESTATUS[0]}
```

または:

```bash
bash -c 'set -o pipefail; make foo 2>&1 | tail -100'
```

### bg job が予想時間を超えたら proactive に診断 (必須)

通常 30s で終わる test / 5 min で終わる terraform apply / 15 min で終わる Composer 起動 が **2 倍を超えても完了通知が来ない** なら、`bg notification 待ち` と惰性報告せず:

```bash
ps aux | grep <process>     # alive?
ls -la <output-file>        # mtime / size 動いているか
pgrep -af <stuck child>     # kubectl / terraform 等の child が hang していないか
```

を即実行して状態確認。沈黙より過剰報告。

### test 追加時の mock 漏れ防止 (必須)

副作用 (subprocess / network call) を持つ関数を内部で呼ぶ関数を test するときは:

1. **module top-level import** で書いて mock target を一意化 (関数内 delayed import は mock target が散らばる)
2. 関連する全 test ファイルで mock 漏れがないか grep:
   ```bash
   grep -rn "<関数名>" tests/  # 呼んでる箇所を全件確認
   ```
3. **foreground で 1 度走らせて** PASS 確認してから bg 化

### troubleshooting docs を必ず参照 / 追加

新しい failure mode を踏んだら [`docs/troubleshooting/README.md`](docs/troubleshooting/README.md) に 1 ファイル追加。format は既存 doc 参照。再発時の判断材料を残す。

---

## Claude Code に任せる作業 vs 人間判断

- **任せる**: Port/adapter/fake の boilerplate 提案、6 ファイル parity 同期、doc 同期、テスト雛形、`scripts/ci/layers.py` の `RULES` 追記提案、`mlops-dev-a` への `terraform apply` / `make deploy-all` (事前承認範囲)
- **人間判断**: 中核コード変更 (`search_service.py` / `ranking.py` / `build_ranker_features`)、hybrid-search 5 要素の変更、Composer 二重起動判定、Elasticsearch 基盤構成の大幅変更、ADR 起案、`git push --force` / 共有 main への push、別 project への波及
